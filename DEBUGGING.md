
# Docker images for running ansible-template-ui

You can use this image to run ansible-template-ui.

## Usage

### 1. Run the container as a daemon

`docker run -d -p 8080:8080 -v /var/run/docker.sock:/var/run/docker.sock --name ansible-web ansible-template-ui:latest`

#### 1.1 to run with a specified path prefix

```shell
docker run -d \
  --name ansible-web \
  -e SCRIPT_NAME='/ansible-template-ui' \
  -p 8080:8080 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  ansible-template-ui:latest
```

#### 1.2 to run specified ansible-execution-env container

```shell
## using `socket_proxy` instead of directly mounting the docker driver device 
docker run -d -p 8080:8080 \
    --name ansible-web \
    --env DOCKER_HOST=tcp://socket-proxy:2375 \
    --env DOCKER_ANSIBLE_EE_IMAGE=ansible-execution-env:devel \
    ansible-template-ui:latest
```

Specify docker registry cred
```shell
$ docker buildx debug --on=error build -t ansible-execution-env:devel \
    --build-arg IMAGE_REGISTRY=media.johnson.int:5000 \
    --build-arg DOCKER_REGISTRY_USERNAME=username \
    --build-arg DOCKER_REGISTRY_PASSWORD=password \
    -f docker/devel/Dockerfile \
    docker/devel
```

2. Enter to the container

`docker exec -it ansible-web sh`

3. Remove the container

`docker rm -f ansible-web`

## Building images

To build the image:
```shell
$ docker build -t ansible-template-ui -f docker/ansibleweb/Dockerfile docker/ansibleweb
$ docker build -t ansible-base-env -f docker/base/Dockerfile docker/base/
$ docker build -t ansible-execution-env:devel -f docker/devel/Dockerfile docker/devel/
$ docker build -t ansible-execution-env:stable -f docker/stable/Dockerfile docker/stable/
```

## Building directly in the respective image source directory

```shell
$ cd docker/base/
$ docker build -t ansible-base-env -f Dockerfile .
```

### Running bash in image

To run bash in newly built image:

```shell
## if testing the locally built image
$ docker run --rm -it ansible-template-ui bash -il
## if testing the image pushed to the registry
$ docker run --rm -it media.johnson.int:5000/ansible-template-ui bash -il
```

### Debugging failed build

When one of the Dockerfile build command fails, look for the **id of the preceding layer** and run a shell in a container created from that id:

```shell
$ docker run --rm -it ansible-template-ui bash -il
$ docker run --rm -it ansible-template-ui bash -il
$ docker run --rm -it <id_last_working_layer> bash -il
```

#### `on` flag

To start the debugger, first, ensure that `BUILDX_EXPERIMENTAL=1` is set in
your environment.

```console
$ export BUILDX_EXPERIMENTAL=1
```

If you want to start a debug session when a build fails, you can use
`--on=error` to start a debug session when the build fails.

```console
$ export BUILDX_EXPERIMENTAL=1
$ docker buildx debug --on=error build -t ansible-template-ui -f docker/ansibleweb/Dockerfile docker/ansibleweb
$ docker buildx debug --on=error build -t ansible-base-env -f docker/base/Dockerfile docker/base/
$ docker buildx debug --on=error build -t ansible-execution-env:devel \
    --build-arg IMAGE_REGISTRY=media.johnson.int:5000 \
    --build-arg BASE_IMAGE_LABEL=ansible-base-env \
    -f docker/devel/Dockerfile \
    docker/devel
```

Build image for ansible-execution-env registry tag deployment
```console
$ export BUILDX_EXPERIMENTAL=1
$ docker buildx debug --on=error build -t ansible-execution-env:devel \
    --build-arg BASE_IMAGE_LABEL=lj020326/ansible-base-env \
    -f docker/devel/Dockerfile \
    docker/devel
```

UPDATE
Intermediate container hashes are not supported as of Docker version 20.10. 
To view intermediate container hashes:

```shell
$ DOCKER_BUILDKIT=0 docker build -t ansible-template-ui -f docker/ansibleweb/Dockerfile docker/ansibleweb
DEPRECATED: The legacy builder is deprecated and will be removed in a future release.
            BuildKit is currently disabled; enable it by removing the DOCKER_BUILDKIT=0
            environment-variable.

Sending build context to Docker daemon  62.46kB
Step 1/25 : ARG IMAGE_REGISTRY=lj020326
Step 2/25 : FROM $IMAGE_REGISTRY/ansible-template-ui:latest
 ---> e073c8665ceb
...
Step 20/25 : ENV PATH="$PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH"
 ---> Running in 51ebbfe0c1eb
 ---> Removed intermediate container 51ebbfe0c1eb
 ---> b1c595d36fc4
 ---> Running in 4253d5ef2e94

BUILD FAILED (Debian GNU/Linux 8 using python-build 20180424)

Inspect or clean up the working tree at /tmp/python-build.20240416133411.74
Results logged to /tmp/python-build.20240416133411.74.log

Last 10 log lines:
		$ensurepip --root=/ ; \
fi
Looking in links: /tmp/tmpo4sotjqo
Processing /tmp/tmpo4sotjqo/setuptools-65.5.0-py3-none-any.whl
Processing /tmp/tmpo4sotjqo/pip-23.2.1-py3-none-any.whl
Installing collected packages: setuptools, pip
  WARNING: The scripts pip3 and pip3.11 are installed in '/pyenv/versions/3.11.7/bin' which is not on PATH.
  Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
Successfully installed pip-23.2.1 setuptools-65.5.0
WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv
The command '/bin/sh -c CPPFLAGS="-I/usr/local/openssl/include -I/usr/local/openssl/include/openssl"     LDFLAGS="-L/usr/local/openssl/lib -L/usr/local/openssl/lib64"     pyenv install $PYTHON_VERSION' returned a non-zero code: 1
$ 
$ docker run --rm -it b1c595d36fc4 bash -il

```
