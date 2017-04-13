[![Build Status](https://travis-ci.org/pkch/graphtypes.svg?tx=1)](https://travis-ci.org/pkch/graphtypes)
[![Coverage Status](https://coveralls.io/repos/pkch/graphtypes/badge.svg?tx=1)](https://coveralls.io/r/pkch/graphtypes)
[![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/pkch/graphtypes/LICENSE)

Type Annotated Graphs in Python
===============================

This repo contains the source code for a series of blog posts:

- [Part I - Representing graphs as dictionaries or sets](https://pkch.io/2017/03/31/python-graphs-part1)
- [Part II - Representing graphs as classes](https://pkch.io/2017/04/12/python-graphs-part2/)
- Part III - Implementing graph traversal
- Part IV - Trees

These posts summarize my experience with type hints in a small project. I go
through several iterations of graph representation and traversal, and discuss
various design and type checking issues. I use python 3.6 and the latest
version of [mypy](http://mypy.readthedocs.io/en/latest/).

I push my code to this repo to run tests and type check using Travis CI; once
I get a green mark, I push it to gist, which is [directly
embedded](https://help.github.com/articles/about-gists/#embedding-gists) in
the blog. I like this workflow because it makes sure the code on my blog is
fully tested.
