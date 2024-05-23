#!/usr/bin/env python

# ref: https://forums.docker.com/t/docker-errors-dockerexception-error-while-fetching-server-api-version-connection-aborted-filenotfounderror-2-no-such-file-or-directory-error-in-python/135637/3
import os
import docker

app_image = os.getenv('DOCKER_ANSIBLE_EE_IMAGE', 'lj020326/ansible-execution-env')
print("app_image=%s" % app_image)

client = docker.from_env()

# res = client.containers.run("ubuntu", "echo hello world")
# res = client.containers.run("sivel/ansible-template-ui", "echo hello world")
# res = client.containers.run("lj020326/ansible-execution-env", "echo hello world")
# res = client.containers.run("media.johnson.int:5000/ansible-template-ui", "echo hello world")
res = client.containers.run(app_image, "echo hello world")

print("Running", res)
