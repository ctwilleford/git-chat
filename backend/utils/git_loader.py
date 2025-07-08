import tempfile
import git
from pathlib import Path

def clone_repo(git_url: str, access_token: str, branch: str = "main") -> Path:
    """
    Clone a Git repo to a temp directory and return the path.
    """
    temp_dir = tempfile.TemporaryDirectory()
    clone_path = Path(temp_dir.name)

    # Inject token into the URL for auth
    if access_token:
        git_url = git_url.replace("https://", f"https://{access_token}@")

    git.Repo.clone_from(git_url, str(clone_path), branch=branch, depth=1)
    return clone_path
