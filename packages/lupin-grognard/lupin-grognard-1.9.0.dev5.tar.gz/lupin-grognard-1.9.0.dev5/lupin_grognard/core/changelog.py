from typing import List, Dict, Union

from jinja2 import (
    Template,
    Environment,
    PackageLoader,
    select_autoescape,
    TemplateNotFound,
    TemplateError,
    TemplateRuntimeError,
)

from lupin_grognard.core.commit.commit import Commit
from lupin_grognard.core.git import Git
from lupin_grognard.core.tools.utils import die, info, write_file


class Changelog:
    def __init__(self, commit_list: List[str]):
        self.commit_list = commit_list
        self.git = Git()

    def generate(self) -> None:
        """Generate changelog"""
        project_name = self.git.get_git_project_name()
        info(msg=f"Collecting data from {project_name}")
        classified_commits = self._classify_commits()
        self._generate_markdown_file(
            classified_commits=classified_commits, project_name=project_name
        )

    def _get_local_template(self) -> Template:
        try:
            env = Environment(
                loader=PackageLoader("lupin_grognard", "templates"),
                autoescape=select_autoescape(),
                trim_blocks=True,  # Removes unnecessary spaces before and after blocks and loop
            )
            return env.get_template("changelog.j2")
        except TemplateNotFound:
            die(msg="Template 'lupin_grognard/templates/changelog.j2' not found")

    def _generate_markdown_file(
        self,
        classified_commits: Dict,
        project_name: str,
    ) -> None:
        """Generate changelog markdown file from template with version and commits"""
        template = self._get_local_template()
        context = {"tree": classified_commits, "project_name": project_name}
        info(msg="Generating changelog file from lupin_grognard/templates/changelog.j2")
        try:
            markdown_str = template.render(context)
        except (TemplateError, TemplateRuntimeError) as e:
            die(msg=f"Error rendering Jinja2 template: {e}")
        write_file(file="CHANGELOG.md", content=markdown_str)
        info(msg="Changelog file generated")

    def _append_commit_without_type_scope(
        self, commits: List[str], commit: Commit
    ) -> None:
        commits.append(commit.title_without_type_scope)

    def _classify_commits(self) -> List[Dict[str, List[str]]]:
        """
        Classify commits by version and by type and scope
        Returns:
            List[Dict[str, List[str]]]: List of version with commits classified by type and scope

            Example:
            [
                {
                    "version": "v1.0.0",
                    "date": "2020-02-20",
                    "commits": [
                        {
                            "feature": {
                                "added": [
                                    "Add new feature",
                                    ],
                                "changed": [
                                    "change new feature",
                                ],
                                "removed": [
                                    "remove new feature",
                                ],
                            },
                            "fix": [
                                "Fix bug",
                            ],
                            "other": [
                                "add README.md",
                            ],
                        },
                    ],
                },
            ]
        """
        versioned_commits = self._classify_commits_by_version()
        for v in versioned_commits:
            classified_commits = self._classify_commits_by_type_and_scope(v["commits"])
            v["commits"] = classified_commits
        self._display_number_of_commits_found_for_changelog(
            versioned_commits=versioned_commits
        )
        return versioned_commits

    def _classify_commits_by_version(self) -> List[Dict[str, List[Commit]]]:
        versions = []
        current_version = {}
        tag_list = self.git.get_tags()
        for c in self.commit_list:
            commit = Commit(c)
            for tag in tag_list:
                if commit.hash in tag[1]:
                    info(msg=f"Found in tag {tag[0]}")
                    commit_tag = tag[0]
                    date_tag = tag[2]
                    if current_version:
                        versions.append(current_version)
                    current_version = {
                        "version": commit_tag,
                        "date": date_tag,
                        "commits": [],
                    }
                    current_version["commits"].append(commit)
                    break
            else:
                if not current_version:
                    current_version = {
                        "version": "Unreleased",
                        "date": "",
                        "commits": [],
                    }
                current_version["commits"].append(commit)
        if current_version:
            versions.append(current_version)
        return versions

    def _classify_commits_by_type_and_scope(
        self, commits: List[Commit]
    ) -> Dict[str, Union[Dict[str, List[str]], List[str]]]:
        """Classify commits by type and scope and exclude merge commits"""
        commits_feat_add = []
        commits_feat_change = []
        commits_feat_remove = []
        commits_fix = []
        commits_other = []
        for commit in commits:
            match (commit.type, commit.scope):
                case ("feat", "(add)"):
                    self._append_commit_without_type_scope(
                        commits=commits_feat_add, commit=commit
                    )
                case ("feat", "(change)"):
                    self._append_commit_without_type_scope(
                        commits=commits_feat_change, commit=commit
                    )
                case ("feat", "(remove)"):
                    self._append_commit_without_type_scope(
                        commits=commits_feat_remove, commit=commit
                    )
                case ("fix", None):
                    self._append_commit_without_type_scope(
                        commits=commits_fix, commit=commit
                    )
                case (_, _) if commit.type is not None:
                    commits_other.append(commit.title.capitalize())
        result = {
            "feature": {},
            "fix": [],
            "other": [],
        }
        if commits_feat_add:
            result["feature"]["added"] = commits_feat_add
        if commits_feat_change:
            result["feature"]["changed"] = commits_feat_change
        if commits_feat_remove:
            result["feature"]["removed"] = commits_feat_remove
        if commits_fix:
            result["fix"] = commits_fix
        if commits_other:
            result["other"] = commits_other
        return result

    def _display_number_of_commits_found_for_changelog(
        self, versioned_commits: List[Dict[str, List[str]]]
    ) -> None:
        commit_number = 0
        for v in versioned_commits:
            commit_number += len(v["commits"]["feature"].get("added", []))
            commit_number += len(v["commits"]["feature"].get("changed", []))
            commit_number += len(v["commits"]["feature"].get("removed", []))
            commit_number += len(v["commits"]["fix"])
            commit_number += len(v["commits"]["other"])
        info(msg=f"Found {commit_number} commits")
