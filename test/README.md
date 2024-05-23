
# Notes for testing with docker-compose

## Simple compose

```shell
$ docker-compose up -d
[+] Building 0.0s (0/0)
[+] Running 3/3
 ✔ Container ansible-template-ui  Started  0.4s 
 ✔ Container portainer            Running  0.0s 
 ✔ Container dozzle               Running  0.0s 

```

## Stop, rebuild and restart
```shell
$ docker-compose stop ansible-template-ui || true && \
    docker-compose rm -f ansible-template-ui
$ docker build -t ansible-template-ui:latest -f docker/ansibleweb/Dockerfile docker/ansibleweb
$ docker-compose up -d ansible-template-ui
```

Restart container with newly built image
```shell
$ docker-compose stop ansible-template-ui || true && \
    docker-compose rm -f ansible-template-ui && \
    docker-compose up -d ansible-template-ui
[+] Stopping 1/0
 ✔ Container ansible-template-ui  Stopped  0.0s 
Going to remove ansible-template-ui
[+] Removing 1/0
 ✔ Container ansible-template-ui  Removed  0.0s 
[+] Building 0.0s (0/0)
[+] Running 1/1
 ✔ Container ansible-template-ui  Started  0.5s 
$ 

```

## Compose stack using socket_proxy network and remove direct access to docker driver

```shell
$ docker-compose -f docker-compose.socket-proxy.yml up -d
[+] Building 0.0s (0/0)
[+] Running 5/5
 ✔ Network test_default           Created 
 ✔ Container socket-proxy         Started 
 ✔ Container portainer            Started 
 ✔ Container dozzle               Started 
 ✔ Container ansible-template-ui  Started 
$ docker-compose -f docker-compose.socket-proxy.yml ps
NAME                  IMAGE                             COMMAND                  SERVICE               CREATED             STATUS              PORTS
ansible-template-ui   ansible-template-ui:latest        "gunicorn --config g…"   ansible-template-ui   6 seconds ago       Up 5 seconds        0.0.0.0:8080->8080/tcp
dozzle                amir20/dozzle:latest              "/dozzle"                dozzle                6 seconds ago       Up 5 seconds        0.0.0.0:8888->8080/tcp
portainer             portainer/portainer-ce:latest     "/portainer"             portainer             6 seconds ago       Up 5 seconds        8000/tcp, 9443/tcp, 0.0.0.0:9000->9000/tcp
socket-proxy          fluencelabs/docker-socket-proxy   "/docker-entrypoint.…"   socket-proxy          7 seconds ago       Up 5 seconds        127.0.0.1:2375->2375/tcp

```

