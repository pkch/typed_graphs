[![Build Status](https://travis-ci.org/pkch/graphtypes.svg)](https://travis-ci.org/pkch/graphtypes)
[![Coverage Status](https://coveralls.io/repos/pkch/graphtypes/badge.svg)](https://coveralls.io/r/pkch/graphtypes)
[![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/pkch/graphtypes/LICENSE)

Type Annotated Graphs in Python
===============================

This is not a graph library! It is just the source code for a series of blog
articles. It's not tested as extensively as a library should be, and it's
also not optimized in any way. In addition, to make it easy for me to push it
go `gist`, I keep everything in a single folder.

If you do want to use it in your project, the most reasonable implementations
are:

- [`graph_reverse`](graph_reverse.py) for directed graphs
- [`graph_undirected`](graph_undirected.py) for undirected Graphs

The blog posts are here:

- [Part I - Representing graphs as dictionaries or sets](https://pkch.io/2017/03/31/python-graphs-part1)
- [Part II - Representing graphs as classes](https://pkch.io/2017/04/12/python-graphs-part2/)
- Part III - Implementing graph traversal
- Part IV - Trees

They summarize my experience with type hints in a small project. I go through
several iterations of graph representation and traversal, and discuss various
design and type checking issues. I use python 3.6 and the latest version of
[mypy](http://mypy.readthedocs.io/en/latest/).

I push my code to this repo to run tests and type check using Travis CI. I
then manually push it to gist, from which it is [directly
embedded](https://help.github.com/articles/about-gists/#embedding-gists) in
the blog. I like this workflow because it effectively tests the code shown in
the posts.
