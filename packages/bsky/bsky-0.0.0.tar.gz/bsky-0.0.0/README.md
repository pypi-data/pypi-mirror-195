
`bsky`: Simple, idiomatic client library for atproto.com ("Bluesky")
=====================================================================

**Status:** it doesn't really work yet and will eat your data

This is a project to implement components of the proposed Bluesky AT
Protocol ([atproto.com](https://atproto.com)) for federated social media.


## HOWTO: Release pypi.org Package

Go to `test.pypi.org` (and then later `pypi.org`) and generate an API token for
your account (assumign you already have an account).

Install deps (on Debian/Ubuntu):

    sudo apt install python3-build python3-twine

Build this package:

    python3 -m build

Run the upload. When propted, use `__token__` for username, and the API token
as password.

    # for test.pypi.org
    python3 -m twine upload --repository testpypi dist/*

    # for regular pypi.org
    python3 -m twine upload dist/*
