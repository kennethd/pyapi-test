# pyapi-test

This package provides tested reference implementations of a few popular Python
API servers, and some basic tooling for making performance comparisons between
them, and soon, comparisons between them running via a few popular WSGI & ASGI
servers.

Why? It's been a long time since I geeked out on this stuff, and it's overdue.

## goals

  * comparison of WSGI/ASGI frameworks
  * comparison of WSGI/ASGI servers
  * exploration of Python profilers, performance analysis tools, load testers

## tests

The same API has been implemented for each of the frameworks, and all share a
common implementation, thinly exposed via API.

## todo/roadmap

  * Add locust real-time/live support
  * Add async endpoints/celery task runner
  * Add more frameworks support: fastapi, tornado, django to start
  * Add more WSGI/ASGI server support: gunicorn, uvicorn
  * Store performance data on docker volume for comparison
  * Add profiler support, output to docker volume
  * Add Grafana(?) interface & timescale db for comparisons
  * Comparative tests with & without 'use epoll' in `nginx.conf`
  * Upgrade to new debian stable released 2025-08-12
  * Explore uwsgi-stats server


## getting started

To build the docker image & launch a container:
```sh
$ docker-compose up
```
Visit http://localhost:9001 for access to supervisor admin.

You should also be able to interact with the apps:

  * uwsgi-flask: http://localhost:9099/v1/hello


## development environment

Example performance results have been obtained on dev machine with specs:

  * Linux fado 6.1.0-37-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.140-1 (2025-05-22) x86_64 GNU/Linux
  * 16-core AMD Ryzen 7 5800H with Radeon Graphics w/ 13196868 kB MemTotal
  * Python 3.11.2
  * Docker version 20.10.24+dfsg1, build 297e128

### rake interface

Task orchestration is provided via Rake, a make-like build system from the
ruby community.  Locally I am using rake version 13.0.6 w/ruby 3.1.2p20.
Debian packages to install are called `rake` and `ruby`.


## working locally

To create a local virtualenv with this package and all dependencies:
```sh
$ rake venv:install venv:test
```


## docker setup

The docker setup is a little convoluted with `supervisor` acting as the init
process monitoring `nginx`, `uwsgi` & `gunicorn`, each configured for each of
the frameworks under test: `flask`, `fastapi`, `tornado`, etc.

The intention is to simplify container creation and maintenance, and expected
usage is to run tests against only one wsgi-server/app-server combination at a
time.

A docker volume, `pyapi-test-data`, is created for outputs which may be used
for comparisons between configurations (or indeed app algorithm implementations)


## quick intro to rake

Because it's not that commonly used in the Python world, and there are similar
Python projects, here's a 30-second intro to `rake` and why I chose to use it.

I have been automating web app builds and deploys and data migration processes
for 25 years, from `bash`+`tar` to gnu `make` to `fabric`, etc.  I really
love the low barrier-to-entry of `ruby` for teammates, while retaining
`make`'s powerful composability of Tasks via dependencies.

One of my favorite things about Rake is the transparency of what it is doing,
I very much prefer my team to know how to interact with project components
from the command line, and `rakelib` provides a valuable reference while
reinforcing that knowledge each time you run it by echoing commands it is
running back to you.

Also, as someone who switches between projects frequently, the built-in menu
of tasks is fantastic for remembering the workflow of a specific project, and
maximizing the amount of projects using the same interface, even if not the
same implementation is huge for efficiency, at least I find it to be for my
personal projects which span years of evolving preferences (it probably
doesn't scale to "enterprise" well, but neither do I).


## quirks

A few personal conventions that may require elaboration:

  * `pip-freeze-3.11.txt` is not used for installation, has nothing to do with
    the purpose of a `requirements.txt` file or anything like that.  For
    library packages, dependencies are declared in `pyproject.toml` or similar.
    The only purpose of `pip-freeze-3.*.txt` (which is recreated every time
    `rake venv:test` is run) is to surface dependenceny changes at the PR level.

  * I prefer to edit with `vim`, so there is no benefit of type hinting for me.
    I am a big fan of TypeScript, which introduced a much needed vector for
    catching errors in front-end apps, but in Python it is just ugly noise
    making coders subservient to their IDEs.  That said, if your team uses it,
    I am perfectly fine adhering to standards.  In any case, both front-end
    and server-side apps should be well tested.

  * No AI assistance has been used in this project.  I don't generally care
    what tools a contributor uses on the other side of a PR, but because one
    reason I put this together is as a resume aid, I want to emphasize that
    this is my code.  I've been working with Flask for about a dozen years,
    and this implementation is essentially the same as a dozen other projects
    I've created, similarly the `rakelib` files included here come from a
    personal project I've been using elsewhere for several years.  It took two
    mornings to pull this project together and have that much working, every
    line of code written by hand, with careful thought, and no AI.

