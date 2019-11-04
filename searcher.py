# Imports
import base64
import gensim
from gensim import corpora
from github import Github
from io import BytesIO
import string
from tokenize import tokenize

"""
This class will be instantiated and used in the search.

User instantiates Searcher with GitHub access information,
uses set_repository to define the repository being searched
and to generate a TF-IDF model for similarity matching,
and uses search to conduct search with a given query file.

String splitting and gensim modelling is not specifically
applied to code language - other tools / packages will
definitely be more relevant.
"""
class Searcher:

    # Instantiate a Searcher with provided GitHub access information.
    def __init__(self, username=None, password=None,
                 access_token=None, base_url=None):
        if username and password:
            self.github = Github(username, password)
        elif access_token and base_url:
            self.github = Github(base_url=base_url,
                                 login_or_token=access_token)
        elif access_token:
            self.github = Github(access_token)

        self.repo = None

    # Takes in path to GitHub repository without github.com prefix.
    # Set searchable repository, read contents, and generate
    # TD-IDF model for repository.
    def set_repository(self, repo):
        self.repo = self.github.get_repo(repo)
        self.contents = self.contents()
        self.num_contents = len(self.contents)
        self.create_tfidf_model()

    # Splits file contents into tokens, using gensim to create TF-IDF model
    # over corpus of file contents.
    def create_tfidf_model(self):
        content_tokens = [base64.b64decode(c.content).decode("utf-8").split() \
                            for c in self.contents]
        self.dictionary = gensim.corpora.Dictionary(content_tokens)
        corpus = [self.dictionary.doc2bow(tokens) \
                    for tokens in content_tokens]
        self.tf_idf = gensim.models.TfidfModel(corpus)
        self.sim = gensim.similarities.Similarity('RepoSearch/sim/',
                    self.tf_idf[corpus],
                    num_features = len(self.dictionary))

    # Recursively generate list of ContentFile instances of all files
    # within repository.
    # Returns list of ContentFiles.
    def contents(self):
        if not self.repo:
            print("No repository is currently set for search.")
            return

        contents = self.repo.get_contents("")
        for file_or_dir in contents:
            if file_or_dir.type == "dir":
                contents.remove(file_or_dir)
                contents.extend(self.repo.get_contents(file_or_dir.path))

        return contents

    # Takes in relative path to query file, and optional limit
    # on the number of files returned.
    # Returns the file_max most simiilar files according to similarity
    # according to the TD-IDF score.
    def search(self, query_path, file_max=None):
        if not self.repo:
            print("No repository is currently set for search.")
            return

        if not file_max:
            file_max = self.num_contents

        with open(query_path) as query_file:
            query_tokens = query_file.read().split()
            query_bow = self.dictionary.doc2bow(query_tokens)
            similarities = self.sim[self.tf_idf[query_bow]]

            index_and_score = sorted(enumerate(similarities),
                                key=lambda x: x[1],
                                reverse=True)[:file_max]
            return [(self.contents[index], score) for index, score in index_and_score]
