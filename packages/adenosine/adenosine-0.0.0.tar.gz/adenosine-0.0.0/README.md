
`adenosine`: enthusiast-grade implementation of atproto.com in Python
=====================================================================

**Status:** it doesn't really work yet and will eat your data

This is a hobby project to implement components of the proposed Bluesky AT
Protocol ([atproto.com](https://atproto.com)) for federated social media, as
initially announced in Fall 2022. This might be interesting for other folks to
take a spin with, but isn't intended to host real content from real people. The
goal is to think through how the protocol might work by implementing it.

The intent is for this to roughly track the `adenosine` Rust implementation.
This will probably be just a Python library, not a CLI or PDS implementation.


## Disclaimer

In addition to the below standard Free Software disclaimer from the LICENSE
file, note that this project is likely to be out of sync with upstream protocol
specifications; is not intended for real-world use; is entirely naive about
abuse, security, and privacy; will not have an upgrade/migration path; etc.

> [CONTRIBUTORS] PROVIDE THE PROGRAM "AS IS" WITHOUT WARRANTY OF ANY KIND, >
> EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED >
> WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.


## HOWTO: Release pypi.org Package

Go to `test.pypi.org` (and then later `pypi.org`) and generate an API token for
your account (assumign you already have an account).

Install deps (on Debian/Ubuntu):

    sudo apt install python3-build python3-twine

Build this package:

    python3 -m build

Run the upload:

    # for test.pypi.org
    python3 -m twine upload --repository testpypi dist/*

    # for regular pypi.org
    python3 -m twine upload dist/*
