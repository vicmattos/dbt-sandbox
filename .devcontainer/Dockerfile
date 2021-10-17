# [Choice] Python version (use -bullseye variants on local arm64/Apple Silicon): 3, 3.9, 3.8, 3.7, 3.6, 3-bullseye, 3.9-bullseye, 3.8-bullseye, 3.7-bullseye, 3.6-bullseye, 3-buster, 3.9-buster, 3.8-buster, 3.7-buster, 3.6-buster
ARG VARIANT=3.8-buster
FROM mcr.microsoft.com/vscode/devcontainers/python:0-${VARIANT} AS base

ENV PYTHONUNBUFFERED 1
ENV DBT_HOME=/usr/app
ENV PYTHONIOENCODING=utf-8


FROM base AS build
ARG DIST_MIRROR=https://github.com/dbt-labs/dbt-core/archive/refs/tags
ARG VERSION=''
ARG PLUGINS=''
RUN apt update && \
    apt install -y --no-install-recommends \
        software-properties-common \
        make \
        build-essential \
        libpq-dev \
        curl && \
    pip install --no-cache-dir --upgrade pip setuptools wheel && \
    mkdir -p ${DBT_HOME} && \
    if [ -z "$VERSION" ]; then VERSION=$(curl -s \
        https://api.github.com/repos/dbt-labs/dbt-core/releases/latest | grep tag_name | \
        tr -d ' ' | cut -d: -f 2,3 | tr -d \" | tr -d , | tr -d v); fi && \
    curl -L ${DIST_MIRROR}/v${VERSION}.tar.gz | tar xvz -C ${DBT_HOME} && \
    mv ${DBT_HOME}/dbt-core-${VERSION}/* ${DBT_HOME} && \
    rm -f *.tar.gz && rm -rf ${DBT_HOME}/dbt-core${VERSION} && \
    cd ${DBT_HOME} && \
    if [ ! -z "$PLUGINS" ]; then sed -i '/'$( \
        echo 'core '$PLUGINS | \
        sed -e 's/\s/,/g' -e 's/\(,\)*/\1/g' -e 's/,/\\\|/g' \
        )'/!d' requirements.txt; fi && \
    pip wheel --wheel-dir ${DBT_HOME}/wheels \
        --find-links ${DBT_HOME}/wheels \
        --requirement requirements.txt


FROM base
LABEL maintainer="Victor Mattos <5757883+vicmattos@users.noreply.github.com>"
COPY --from=build ${DBT_HOME} ${DBT_HOME}
RUN cd ${DBT_HOME} && \
    pip --no-cache-dir install \
        --find-links ${DBT_HOME}/wheels \
        --no-index -r requirements.txt
WORKDIR ${DBT_HOME}
CMD ["dbt", "--version"]