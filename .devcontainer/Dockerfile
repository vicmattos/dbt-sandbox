# [Choice] Python version (use -bullseye variants on local arm64/Apple Silicon): 3, 3.9, 3.8, 3.7, 3.6, 3-bullseye, 3.9-bullseye, 3.8-bullseye, 3.7-bullseye, 3.6-bullseye, 3-buster, 3.9-buster, 3.8-buster, 3.7-buster, 3.6-buster
ARG PYTHON_VARIANT=3.8-buster
FROM mcr.microsoft.com/vscode/devcontainers/python:0-${PYTHON_VARIANT} AS base

ENV PYTHONUNBUFFERED 1
ENV DBT_HOME=/usr/app
ENV PYTHONIOENCODING=utf-8


FROM base AS build
ARG DBT_DIST_MIRROR=https://github.com/dbt-labs/dbt-core/archive/refs/tags
ARG DBT_VERSION=''
ARG DBT_PLUGINS=''
RUN apt update && \
    apt install -y --no-install-recommends \
        software-properties-common \
        make \
        build-essential \
        libpq-dev \
        curl && \
    pip install --no-cache-dir --upgrade pip setuptools wheel && \
    mkdir -p ${DBT_HOME} && \
    if [ -z "$DBT_VERSION" ]; then DBT_VERSION=$(curl -s \
        https://api.github.com/repos/dbt-labs/dbt-core/releases/latest | grep tag_name | \
        tr -d ' ' | cut -d: -f 2,3 | tr -d \" | tr -d , | tr -d v); fi && \
    curl -L ${DBT_DIST_MIRROR}/v${DBT_VERSION}.tar.gz | tar xvz -C ${DBT_HOME} && \
    mv ${DBT_HOME}/dbt-core-${DBT_VERSION}/* ${DBT_HOME} && \
    rm -f *.tar.gz && rm -rf ${DBT_HOME}/dbt-core-${DBT_VERSION} && \
    cd ${DBT_HOME} && \
    if [ ! -z "$DBT_PLUGINS" ]; then sed -i '/'$( \
        echo 'core '$DBT_PLUGINS | \
        sed -e 's/\s/,/g' -e 's/\(,\)*/\1/g' -e 's/,/\\\|/g' \
        )'/!d' requirements.txt; fi && \
    pip wheel --wheel-dir ${DBT_HOME}/wheels \
        --find-links ${DBT_HOME}/wheels \
        --requirement requirements.txt


FROM base
ARG WORKSPACE="/workspace"
LABEL maintainer="Victor Mattos <5757883+vicmattos@users.noreply.github.com>"
COPY --from=build ${DBT_HOME} ${DBT_HOME}
RUN cd ${DBT_HOME} && \
    pip --no-cache-dir install \
        --find-links ${DBT_HOME}/wheels \
        --no-index -r requirements.txt
COPY ./config/dbt/profiles.yml /root/.dbt/profiles.yml
WORKDIR ${WORKSPACE}
# CMD ["dbt", "--version"]