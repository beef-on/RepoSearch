# RepoSearch

RepoSearch is used to search an existing GitHub repository for similar files to provide query files. Uses PyGitHub to access and read from GitHub, string splitting when tokenizing files, and [gensim](https://github.com/RaRe-Technologies/gensim) to model and retrieve similar documents.

## Setup

Before use, install the following dependencies:

```bash
pip install PyGithub
pip install gensim
```

## Sample Usage

```python
from RepoSearch.searcher import Searcher

# Initialize Seacher with Github username and password.
s = Searcher("username", "password")

# or initialize with Github personal access token.
s = Searcher("access_token")

# Set the path of the searched repository, and
# create TF-IDF model over contents of repository.
s.set_repository("fshface/RepoSearch")

# Search using a path to a local file, relative to
# the location of RepoSearch, returning at most the
# 10 most similar files.
similar_files = s.search("test_code.py", file_limit = 10)

# Use and review returned (ContentFile, score) tuples.
for content_file, score in similar_files:
    print("Score: {0}, Path: {1}".format(score, content_file.path))

```

# Limitations

- Since file contents are being read from GitHub and decoded into utf-8 encoding, repositories containing files that cannot be decoded / contain invalid bytes will error.
