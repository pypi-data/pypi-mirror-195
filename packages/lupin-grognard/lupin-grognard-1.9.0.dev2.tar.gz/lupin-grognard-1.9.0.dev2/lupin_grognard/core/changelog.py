import re
from typing import List, Dict, Union

from jinja2 import Template, Environment, PackageLoader, select_autoescape

from lupin_grognard.core.commit.commit import Commit
from lupin_grognard.core.git import Git
from lupin_grognard.core.tools.utils import write_file


class Changelog:
    def __init__(self, commit_list: List[str]):
        self.commit_list = commit_list
        self.git = Git()

    def generate(self) -> None:
        """Generate changelog"""
        project_name = self.git.get_git_project_name()
        classified_commits = self._classify_commits()
        self._generate_markdown_file(
            classified_commits=classified_commits, project_name=project_name
        )

    def _get_local_template(self) -> Template:
        env = Environment(
            loader=PackageLoader("lupin_grognard", "templates"),
            autoescape=select_autoescape(),
            trim_blocks=True,  # supprime les espaces inutiles avant et après les blocs et les boucles
        )
        return env.get_template("changelog.j2")

    def _generate_markdown_file(
        self,
        classified_commits: Dict,
        project_name: str = "Project name",
    ) -> None:
        """Generate changelog markdown file from template with version and commits"""
        template = self._get_local_template()
        context = {"tree": classified_commits, "project_name": project_name}
        markdown_str = template.render(context)
        write_file(file="CHANGELOG.md", content=markdown_str)

    def _append_commit_without_type_scope(
        self, commits: List[str], commit: Commit
    ) -> None:
        commits.append(commit.title_without_type_scope)

    def _if_commit_is_tagged(self, commit: Commit) -> bool:
        tag_regex = r"^v\d+\.\d+\.\d+$"  # ex: v1.0.0
        return (
            bool(re.match(tag_regex, commit.tag)) if commit.tag is not None else False
        )

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
        return versioned_commits

    def _classify_commits_by_version(self) -> List[Dict[str, List[Commit]]]:
        version = []
        current_version = {}
        for c in self.commit_list:
            commit = Commit(c)
            if self._if_commit_is_tagged(commit):
                if current_version:
                    version.append(current_version)
                current_version = {
                    "version": commit.tag,
                    "date": self.git.get_tag_date(tag=commit.tag),
                    "commits": [],
                }
            else:
                if not current_version:
                    current_version = {
                        "version": "Unreleased",
                        "date": "",
                        "commits": [],
                    }
            current_version["commits"].append(commit)
        if current_version:
            version.append(current_version)
        return version

    def _classify_commits_by_type_and_scope(
        self, commits: List[Commit]
    ) -> Dict[str, Union[Dict[str, List[str]], List[str]]]:
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
