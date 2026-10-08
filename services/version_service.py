from git import Repo
from datetime import datetime

def get_application_version():
    last_commit = get_last_commit()
    last_commit_date = datetime.fromisoformat(str(last_commit.committed_datetime))
    application_version = last_commit_date.strftime("%Y.%m.%d")
    return application_version

def get_last_commit():
    git_repository_path = ".git"
    repository = Repo(git_repository_path)
    last_commit = list(repository.iter_commits("main"))[0]
    return last_commit

def get_author():
    last_commit = get_last_commit()
    author = last_commit.author.name
    return author
    