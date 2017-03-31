Type Annotated Graphs in Python
===============================

This repo contains the source code for my blog post, [Type Annotated Graphs
in Python](http://).

I wrote that article to summarize my experience with simple graph
implementations, and to get a feel for type hints in a small project. I go
through several design iterations of graph representation and traversal,
using type annotations as comprehensive as the current version of
[mypy](http://mypy.readthedocs.io/en/latest/) permits.

I push my code to this repo to run tests and type check using Travis CI; once
I get a green mark, I push it to gist, which is [directly
embedded](https://help.github.com/articles/about-gists/#embedding-gists) in
the blog. I found this workflow super convenient, since I don't need to
copy/paste anything, and can still ensure that the code on the blog is fully
tested.
