# vim:set syntax=dockerfile:
FROM debian:bookworm-slim
ENV DOCKERFILE_VERSION 2025-08-12
ARG PYAPI_TEST_LISTEN_PORT=8080
ENV PYAPI_TEST_LISTEN_PORT $PYAPI_TEST_LISTEN_PORT
ENV PYAPI_TEST_UWSGI_FLASK_PORT 9099
ENV PYAPI_TEST_UWSGI_FASTAPI_PORT 9199
ENV PYAPI_TEST_UWSGI_TORNADO_PORT 9299
ENV PYAPI_TEST_UWSGI_DJANGO_PORT 9399
ENV PYAPI_TEST_GUNICORN_FLASK_PORT 9098
ENV PYAPI_TEST_GUNICORN_FASTAPI_PORT 9198
ENV PYAPI_TEST_GUNICORN_TORNADO_PORT 9298
ENV PYAPI_TEST_GUNICORN_DJANGO_PORT 9398

# create app user & install some utilities commonly useful for diagnosing issues
RUN echo "debconf debconf/frontend select Noninteractive" | debconf-set-selections \
 && apt-get update && apt-get upgrade -y && apt-get install -y apt-utils \
 && apt-get install -y python3.11 python3-venv supervisor nginx uwsgi gunicorn \
    curl wget jq less lsof procps htop sed sudo tar unzip locales vim-tiny \
    inetutils-ping inetutils-telnet inetutils-traceroute ca-certificates \
 && useradd --create-home --home-dir /app --shell /bin/bash --groups sudo app \
 && echo 'Defaults lecture = never' > /etc/sudoers.d/lecture \
 && echo '%sudo ALL = (root) NOPASSWD: ALL' > /etc/sudoers.d/app \
 && apt-get -y autoremove \
 && sed -i 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen \
 && locale-gen

COPY ./docker-files/etc/motd /etc/motd
COPY ./docker-files/etc/supervisor/supervisord.conf /etc/supervisor/
COPY ./docker-files/etc/supervisor/conf.d/nginx.conf /etc/supervisor/conf.d/
COPY ./docker-files/etc/nginx/nginx.conf /etc/nginx/
COPY ./docker-files/etc/nginx/sites-available/default /etc/nginx/sites-available/
#COPY ./docker-files/etc/supervisor/conf.d/uwsgi.conf /etc/supervisor/conf.d/
#COPY ./docker-files/etc/supervisor/conf.d/gunicorn.conf /etc/supervisor/conf.d/

USER app
WORKDIR /app
COPY ./docker-files/app/.bashrc /app/
COPY . ./
RUN ls -lAh \
    && python3 -m venv ./venv3.11 \
    && . ./venv3.11/bin/activate \
    && pip install . \
    && pip install .[dev] \
    && python -c 'from pyapi import VERSION; print("Installed pyapi version", VERSION)' \
    && ls -lAh
CMD ["sudo", "/usr/bin/supervisord", "-c", "/etc/supervisor/supervisord.conf"]
