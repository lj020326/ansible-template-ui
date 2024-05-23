#FROM python:3.9
#FROM python:3.10
FROM python:3.11

# Defining default variables and build arguments
ARG USER=gunicorn
ARG GROUP=gunicorn
ARG UID=1000
ARG GID=1000
ARG USER_HOMEDIR=/home/${USER}

ENV USER_HOMEDIR=${USER_HOMEDIR}
ENV LANG=C.UTF-8
ENV DOCKER_IMAGE_CACHE_DIR=/docker-cache
ENV AUTOCONFIGURE_DOCKER_STORAGE=true

## ref: https://www.how2shout.com/linux/install-python-3-x-or-2-7-on-debian-11-bullseye-linux/
RUN apt-get update -y
RUN apt-get install --no-install-recommends -y \
    apt-utils \
    sudo bash \
    build-essential \
    ca-certificates \
    dnsutils \
    iproute2 \
    openssh-client \
    iputils-ping \
    inetutils-telnet \
    ssh-askpass sshpass \
    curl wget git \
    jq

###############################################
## flask client will be running docker in docker
## ref: https://devopscube.com/run-docker-in-docker/
## Adding the default user to groups used by Docker engine
## "docker" for avoiding sudo, and "dockremap" if you enable user namespacing
# Set up default user for jenkins
RUN addgroup --gid ${GID} ${GROUP} \
  && adduser --quiet \
    --home "${USER_HOMEDIR}" \
    --uid "${UID}" \
    --ingroup "${GROUP}" \
    --shell /bin/bash \
    --disabled-password "${USER}" \
  && echo "${USER}:${USER}" | chpasswd

# Adding the default user to groups used by Docker engine
# "docker" for avoiding sudo, and "dockremap" if you enable user namespacing
#RUN addgroup docker \
#  && addgroup ${user} docker \
#  && addgroup ${user} dockremap
RUN addgroup docker \
  && adduser ${USER} docker

# Those folders should not be on the Docker "layers"
VOLUME ${USER_HOMEDIR} /docker-cache /tmp

## ref: https://developers.redhat.com/articles/2023/08/17/how-deploy-flask-application-python-gunicorn#containerization
## ref: https://stackoverflow.com/questions/43925487/how-to-run-gunicorn-on-docker

WORKDIR ${USER_HOMEDIR}/app
#WORKDIR /home/gunicorn/app

COPY ./requirements.txt /home/gunicorn/requirements.txt
COPY ./deploy-requirements.txt /home/gunicorn/deploy-requirements.txt

#RUN pip install --no-cache-dir --upgrade -r /home/gunicorn/requirements.txt
RUN pip install -r /home/gunicorn/requirements.txt -r /home/gunicorn/deploy-requirements.txt

COPY ./ansible_template_ui /home/gunicorn/app/ansible_template_ui
COPY gunicorn.config.py /home/gunicorn/app
COPY test-docker.py /home/gunicorn/app

#USER $USER

EXPOSE 8080

#CMD ["uvicorn", "ansible_template_ui.main:app", "--host", "0.0.0.0", "--port", "8080"]
#CMD ["gunicorn"  , "-b", "0.0.0.0:8000", "ansible_template_ui:app"]
CMD ["gunicorn","--config", "gunicorn.config.py", "ansible_template_ui:app"]
