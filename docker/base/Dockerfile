#FROM alpine
#FROM debian:bullseye-slim
FROM debian:bookworm-slim
ARG BUILD_ID=devel
LABEL build=$BUILD_ID

COPY clean_collections.py /tmp/clean_collections.py
COPY execute.sh /execute.sh
COPY playbook.yml /playbook.yml

ENV PIP_BREAK_SYSTEM_PACKAGES=1

## ref: https://octopus.com/blog/using-ubuntu-docker-image
RUN echo 'APT::Install-Suggests "0";' >> /etc/apt/apt.conf.d/00-docker
RUN echo 'APT::Install-Recommends "0";' >> /etc/apt/apt.conf.d/00-docker

ENV container docker
ENV LC_ALL C
ENV DEBIAN_FRONTEND noninteractive

## ref: https://www.cyberciti.biz/faq/failed-to-set-locale-defaulting-to-c-warning-message-on-centoslinux/
ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US.UTF-8
ENV LC_CTYPE=en_US.UTF-8
#ENV LANG=C.UTF-8
#ENV LANGUAGE=C.UTF-8
#ENV LC_COLLATE=C
#ENV LC_CTYPE=C.UTF-8

ENV TZ=UTC

ENV HOME="/root"
ENV PYTHON_VERSION="3.11.7"

## ref: https://askubuntu.com/questions/1460877/gitgit-ansible-version-error-ansible-requires-the-locale-encoding-to-be-u
#RUN echo "LC_ALL=en_US.UTF-8" >> /etc/environment
#RUN echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen
#RUN echo "LANG=en_US.UTF-8" > /etc/locale.conf

## ref: https://stackoverflow.com/questions/28405902/how-to-set-the-locale-inside-a-debian-ubuntu-docker-container#28406007
# Set the locale
RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y locales
RUN sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && locale-gen
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

#RUN apt-get clean && apt-get update -y
#RUN apt-get install -y locales
#RUN locale-gen en_US.UTF-8

## ref: https://www.how2shout.com/linux/install-python-3-x-or-2-7-on-debian-11-bullseye-linux/
RUN apt-get install --no-install-recommends -y \
    apt-utils \
    sudo bash \
    build-essential \
    ca-certificates \
    curl wget git \
    jq

## ref: https://stackoverflow.com/questions/75159821/installing-python-3-11-1-on-a-docker-container
## ref: https://stackoverflow.com/questions/63314253/how-to-install-python3-8-using-checkinstall-on-debian-10
RUN apt-get update -y \
    && apt-get upgrade -y \
    && apt-get -y install \
        libbz2-dev \
        libbz2-dev \
        libc6-dev \
        libffi-dev \
        libgdbm-dev \
        liblzma-dev \
        libncurses5-dev \
        libncursesw5-dev \
        libnss3-dev \
        libreadline-dev \
        libsqlite3-dev \
        libssl-dev \
        zlib1g-dev \
        xz-utils \
        tk-dev

#################################################
## install internal cacerts
COPY import-ssl-certs.sh /
RUN chmod +x /import-ssl-certs.sh
#RUN bash -x /import-ssl-certs.sh
RUN bash /import-ssl-certs.sh


####################
## pyenv
#WORKDIR $HOME
#RUN git clone --depth=1 https://github.com/pyenv/pyenv.git .pyenv
#ENV PYENV_ROOT="$HOME/.pyenv"

WORKDIR /
RUN git clone --depth=1 https://github.com/pyenv/pyenv.git /pyenv

ENV PYENV_ROOT="/pyenv"
#ENV PATH="${PYENV_ROOT}/shims:${PYENV_ROOT}/bin:$PATH"
ENV PATH="${PYENV_ROOT}/shims:${PYENV_ROOT}/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

## ref: https://github.com/pyenv/pyenv/issues/2416#issuecomment-1219484906
## ref: https://github.com/pyenv/pyenv/issues/2760#issuecomment-1868608898
## ref: https://stackoverflow.com/questions/57743230/userwarning-could-not-import-the-lzma-module-your-installed-python-is-incomple#57773679
## ref: https://superuser.com/questions/1346141/how-to-link-python-to-the-manually-compiled-openssl-rather-than-the-systems-one
## ref: https://github.com/pyenv/pyenv/issues/2416
RUN pyenv install $PYTHON_VERSION
#RUN pyenv global $PYTHON_VERSION
#RUN pyenv rehash
## resolve source not found issue since completions/pyenv.bash does not initially exist in cloned pyenv dir
RUN touch /pyenv/completions/pyenv.bash
RUN eval "$(/pyenv/bin/pyenv init -)" && /pyenv/bin/pyenv local $PYTHON_VERSION

CMD ["/bin/sh", "/execute.sh"]
