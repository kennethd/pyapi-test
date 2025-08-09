# pyapi-test

This package provides tested reference implementations of a few popular Python
API servers, and some basic tooling for making performance comparisons between
them, and soon, comparisons between them running via a few popular WSGI servers.

## tests

The same API has been implemented for each of the frameworks, and all share a
common implementation, thinly exposed via API.

## development environment

Example performance results have been obtained on dev machine with specs:

    * Linux fado 6.1.0-37-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.140-1 (2025-05-22) x86_64 GNU/Linux
    * 16-core AMD Ryzen 7 5800H with Radeon Graphics w/ 13196868 kB MemTotal
    * Python 3.11.2
    * Docker version 20.10.24+dfsg1, build 297e128

## rake interface

Task orchestration is provided via Rake, a make-like build system from the
ruby community.  Locally I am using rake version 13.0.6 w/ruby 3.1.2p20.
Debian packages to install are:
```
ii  rake   13.0.6-3  all    ruby make-like utility
ii  ruby   1:3.1     amd64  Interpreter of object-oriented scripting language Ruby (default version)
```

## getting started

To create a local virtualenv with this package and all dependencies:
```sh
$ rake venv:install venv:test
```


## quirks

A few personal conventions that may require explanation:

  * `pip-freeze-3.11.txt` is not used for installation, has nothing to do with
    the purpose of a `requirements.txt` file or anything like that.  For
    library packages, dependencies are declared in `pyproject.toml` or similar.
    The only purpose of `pip-freeze-3.*.txt` (which is recreated every time
    `rake venv:install` is run) is to surface dependenceny changes at the PR level.


