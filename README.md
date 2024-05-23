# ansible-template-ui

Web UI for testing ansible templates

## Docker Container

### Pull

```
docker pull lj020326/ansible-template-ui:devel
```

#### Pull from local registry

```shell
docker pull media.johnson.int:5000/alsac-infra-docker/ansible-template-ui:devel
```

### Build

```shell
$ docker build -t ansible-template-ui:devel docker/devel
## build for internal registry
$ DOCKER_BUILDKIT=0 docker build -t ansible-template-ui:devel \
    --build-arg IMAGE_REGISTRY=media.johnson.int:5000 \
    docker/devel
```

### Run container

```shell
$ docker run -ti --name ansible-template-ui -d lj020326/ansible-template-ui
```

#### Run local built container

Run ansible-template-ui
```shell
$ docker run -ti --name ansible-template-ui -d ansible-template-ui
## OR
$ docker run -ti --name ansible-template-ui -d media.johnson.int:5000/ansible-template-ui:latest
```

Run locally built developer images
```shell
$ docker build -t ansible-base-env:latest -f docker/base/Dockerfile docker/base
$ docker build -t ansible-execution-env:devel \
    --build-arg BASE_IMAGE_LABEL=ansible-base-env \
    -f docker/devel/Dockerfile \
    docker/devel
## bash into the newly created image
$ docker run --rm -it ansible-execution-env:devel bash -il
## if terminal ansible testing is successful, then run via the web UI
$ docker build -t ansible-template-ui:latest -f docker/ansibleweb/Dockerfile docker/ansibleweb
$ docker run -d --name ansible-web \
    --env DOCKER_ANSIBLE_EE_IMAGE=ansible-execution-env:devel \
    -p 8123:8080 \
    -v /var/run/docker.sock:/var/run/docker.sock
    ansible-template-ui:latest
```

If experiencing any build related issues, see the [DEBUGGING.md](DEBUGGING.md) for details on debugging a failed build.

## Web App

### Dev

```shell
python -m ansible_template_ui
```

### Production

#### PEX

```shell
pip install pex
./build_pex.sh
ansible_template_ui.pex -k gevent ansible_template_ui:app
```

#### Without PEX

```shell
$ cd docker/ansibleweb
$ pip install -r requirements.txt -r deploy-requirements.txt
$ gunicorn -k gevent ansible_template_ui:app
```
