ARG IMAGE_REGISTRY=docker.io
ARG BASE_IMAGE_LABEL=lj020326/ansible-base-env
FROM $IMAGE_REGISTRY/$BASE_IMAGE_LABEL:latest
## ref: https://schneide.blog/2019/10/21/using-parameterized-docker-builds/
ARG BUILD_ID=devel
ARG BUILD_DATE="2024-05-01"

LABEL maintainer="Lee Johnson <ljohnson@dettonville.org>"
LABEL build_date=$BUILD_DATE
LABEL build=$BUILD_ID

RUN set -x && \
    pip3 install --no-cache-dir --no-compile -U pip && \
    pip3 install --no-cache-dir --no-compile ansible jmespath netaddr && \
    python3 /tmp/clean_collections.py && \
    rm -rf /root/.cache && \
    rm -rf /root/.cargo

#RUN set -x && \
#    apt install -y --no-cache python3 py3-pip openssl-dev python3-dev libffi-dev ca-certificates gcc make musl-dev git yaml-dev rust cargo && \
#    pip3 install --no-cache-dir --no-compile -U pip && \
#    pip3 install --no-cache-dir --no-compile ansible jmespath netaddr && \
#    apk del py3-pip openssl-dev python3-dev libffi-dev ca-certificates gcc make musl-dev git yaml rust cargo && \
#    python3 /tmp/clean_collections.py && \
#    rm -rf /root/.cache && \
#    rm -rf /root/.cargo


CMD ["/bin/sh", "/execute.sh"]
