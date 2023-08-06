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

    def get_commit_tag(self, commit_hash) -> str | None:
        result = run_command(command=f"git describe --tags {commit_hash}")
        if result.return_code == 0:
            return result.stdout.strip()
        return None

    def get_tag_date(self, tag: str) -> str:
        date = run_command(command=f"git show -s --format=%ci {tag}").stdout
        if date:
            return date.split(" ")[0]
        return ""

    def get_git_project_name(self) -> str:
        repo_url = run_command(command="git config --get remote.origin.url").stdout
        return repo_url.split("/")[-1].replace(".git", "")
