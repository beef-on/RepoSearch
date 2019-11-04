from github import Github

class Searcher:

    def __init__(self, username = None, password = None, access_token = None, base_url = None):
        if username and password:
            self.github = Github(username, password)
        elif access_token and base_url:
            self.github = Github(base_url = base_url, login_or_token = access_token)
        elif access_token:
            self.github = Github(access_token)

        self.repo = None

    def set_repository(self, repo):
        self.repo = self.github.get_repo(repo)

    def search(self, input_path):
        with open(input_path) as input_file:


    def contents(self):
        if not repo:
            print("No repository is currently set for search.")
            return

        contents = repo.get_contents("")
        while contents:
            file_or_dir = contents.pop(0)
            if file_or_dir.type = "dir":
                contents.extend(repo.get_contents(file_or_dir.path))    
            else:
                yield file_or_dir
