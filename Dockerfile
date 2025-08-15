# vim:set syntax=dockerfile:
FROM debian:bookworm-slim AS base

# create app user & install some utilities commonly useful for diagnosing issues
RUN echo "debconf debconf/frontend select Noninteractive" | debconf-set-selections \
 && apt-get update && apt-get upgrade -y && apt-get install -y apt-utils \
 && apt-get install -y python3.11 python3-venv supervisor nginx \
    python3-dev build-essential \
    curl wget jq less lsof procps htop sed sudo tar unzip locales vim-tiny \
    inetutils-ping inetutils-telnet inetutils-traceroute ca-certificates \
 && useradd --create-home --home-dir /app --shell /bin/bash --groups sudo app \
 && echo 'Defaults lecture = never' > /etc/sudoers.d/lecture \
 && echo '%sudo ALL = (root) NOPASSWD: ALL' > /etc/sudoers.d/app \
 && apt-get -y autoremove \
 && mkdir /var/run/uwsgi/ && chown www-data:www-data /var/run/uwsgi \
 && sed -i 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen \
 && locale-gen

# /etc config files created by copying from fresh debian install & modifying
COPY ./docker-files/etc/motd /etc/motd
COPY ./docker-files/etc/supervisor/supervisord.conf /etc/supervisor/
COPY ./docker-files/etc/supervisor/conf.d/nginx.conf /etc/supervisor/conf.d/
COPY ./docker-files/etc/nginx/nginx.conf /etc/nginx/
COPY ./docker-files/etc/nginx/nginx-epoll.conf /etc/nginx/
COPY ./docker-files/etc/nginx/sites-available/default /etc/nginx/sites-available/
COPY ./docker-files/etc/supervisor/conf.d/uwsgi.conf /etc/supervisor/conf.d/
COPY ./docker-files/etc/uwsgi-emperor/emperor.ini /etc/uwsgi-emperor/
COPY ./docker-files/etc/uwsgi-emperor/vassals/*.ini /etc/uwsgi-emperor/vassals/

FROM base
USER app
WORKDIR /app
ENV DOCKERFILE_VERSION 2025-08-12
COPY --chown=app:app ./docker-files/app/.bashrc /app/
COPY --chown=app:app . ./
RUN ls -lAh \
    && mkdir pyapi-test-data \
    && python3 -m venv ./venv3.11 \
    && . ./venv3.11/bin/activate \
    && pip install -U build setuptools wheel \
    && pip install . \
    && pip install .[dev] \
    && python -c 'from pyapi import VERSION; print("Installed pyapi version", VERSION)' \
    && ls -lAh
CMD ["sudo", "/usr/bin/supervisord", "-c", "/etc/supervisor/supervisord.conf"]
