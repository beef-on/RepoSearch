import nltk
from github import Github
from nltk.tokenize import word_tokenize

class Searcher:

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

    def set_repository(self, repo):
        self.repo = self.github.get_repo(repo)
        self.create_tfidf_model()

    def create_tfidf_model(self):
        self.contents = self.contents()
        self.num_contents = len(self.contents)
        content_tokens = [[w.lower() for w in word_tokenize(c.decoded_contents)] \
                            for c in content]
        self.dictionary = gensim.corpora.Dictionary(tokens)
        corpus = [self.dictionary.doc2bow(tokens) \
                    for tokens in content_tokens]
        self.tf_idf = gensim.models.TfidfModel(corpus)
        self.sim = gensim.similarities.Similarity('sim/',
                    self.tf_idf[self.corpus],
                    num_features = len(self.dictionary))

    def contents(self):
        if not repo:
            print("No repository is currently set for search.")
            return

        contents = repo.get_contents("")
        for file_or_dir in contents:
            if file_or_dir.type = "dir":
                contents.extend(repo.get_contents(file_or_dir.path))

        return contents

    def search(self, query_path, file_limit=float("inf")):
        if not repo:
            print("No repository is currently set for search.")
            return

        with open(query_path) as query_file:
            query_tokens = [w.lower() for w in word_tokenize(query_file.read())]
            query_bow = self.dictionary.doc2bow(query_tokens)
            similarities = self.sim(self.tf_idf(query_bow))

            index_and_score = sorted(enumerate(similarities),
                                key=lambda x: x[1])[:file_limit]
            return [(self.contents[index], score) for index, score in index_and_score]
