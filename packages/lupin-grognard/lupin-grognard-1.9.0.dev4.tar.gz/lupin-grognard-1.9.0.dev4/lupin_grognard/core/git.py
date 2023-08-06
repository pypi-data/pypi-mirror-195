import sys
from typing import List

from lupin_grognard.core.cmd import Command, run_command
from lupin_grognard.core.config import COMMIT_DELIMITER


class Git:
    def get_log(
        self, max_line_count: int = None, first_parent: bool = False
    ) -> Command:
        format: str = "hash>>%H%nauthor>>%cN%nauthor_mail>>%cE%nauthor_date>>%ct%ntitle>>%s%nbody>>%b<<body%n"
        delimiter = COMMIT_DELIMITER
        if first_parent:
            command = f'git log --first-parent --format="{format}"{delimiter}'
        else:
            command = f'git log --format="{format}"{delimiter}'
        if max_line_count:
            max_count = f"--max-count={max_line_count}"
            command = f"{command} {max_count}"
        return run_command(command=command)

    def get_branch_name(self) -> str:
        return run_command(command="git branch --show-current").stdout

    def get_git_project_name(self) -> str:
        repo_url = run_command(command="git config --get remote.origin.url").stdout
        return repo_url.split("/")[-1].replace(".git", "")

    def get_tags(self) -> List:
        """Returns a list of tags with the following format:
        [
            ["tag_name", "tag_hash", "tag_date"],
            ["tag_name", "tag_hash", "tag_date"],
            ...
        ]
        """
        inner_delimiter = "---inner_delimiter---"
        dateformat = "%Y-%m-%d"
        formatter = (
            f'"%(refname:lstrip=2){inner_delimiter}'
            f"%(objectname){inner_delimiter}"
            f"%(creatordate:format:{dateformat}){inner_delimiter}"
            f'%(object)"'
        )
        c = run_command(f"git tag --format={formatter} --sort=-creatordate")

        if c.return_code != 0:
            print(f"Git error while getting tags: {c.stderr}")
            sys.exit(1)
        if not c.stdout:
            return []

        tags_list = [line for line in c.stdout.splitlines()]
        return [tag.split(inner_delimiter)[:-1] for tag in tags_list]
