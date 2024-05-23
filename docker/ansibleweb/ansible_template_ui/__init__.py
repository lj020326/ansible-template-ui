#!/usr/bin/env python

__version__ = '1.0.0'

import base64
import json
import os
import pprint
from collections import OrderedDict

import docker

from . import text

# from flask_lambda import FlaskLambda
from flask import Flask
from flask import request, jsonify

# ref: https://flask.palletsprojects.com/en/2.3.x/logging/
from logging.config import dictConfig


# _DO_NOT_REMOVE_EXECUTION_ENV = False
_DO_NOT_REMOVE_EXECUTION_ENV = True

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

kwargs = {}
app_path = os.path.dirname(__file__)
kwargs.update({
    'static_url_path': '',
    'static_folder': os.path.join(
        os.path.abspath(app_path),
        'client'
    )
})


# ref: https://dave.dkjones.org/posts/2013/pretty-print-log-python/
# ref: https://realpython.com/python-pretty-print/
class PrettyLog:
    def __init__(self, obj):
        self.obj = obj

    def __repr__(self):
        # ref: https://stackoverflow.com/questions/21420243/pretty-printing-ordereddicts-using-pprint
        # ref: https://stackoverflow.com/questions/4301069/any-way-to-properly-pretty-print-ordereddict
        if isinstance(object, OrderedDict):
            return pprint.pformat(dict(self.obj))
        return pprint.pformat(self.obj)

# ref: https://stackoverflow.com/questions/18967441/add-a-prefix-to-all-flask-routes
# ref: https://gist.github.com/Larivact/1ee3bad0e53b2e2c4e40
class PrefixMiddleware(object):

    def __init__(self, app, prefix=''):
        self.app = app
        self.prefix = prefix

    def __call__(self, environ, start_response):

        if environ['PATH_INFO'].startswith(self.prefix):
            environ['PATH_INFO'] = environ['PATH_INFO'][len(self.prefix):]
            environ['SCRIPT_NAME'] = self.prefix
            return self.app(environ, start_response)
        else:
            start_response('404', [('Content-Type', 'text/plain')])
            return ["This url does not belong to the app.".encode()]


#app = FlaskLambda(__name__, **kwargs)
app = Flask(__name__, **kwargs)

app_prefix = os.getenv("SCRIPT_NAME")

if app_prefix:
    app.wsgi_app = PrefixMiddleware(app.wsgi_app, prefix=app_prefix)

# # ref: https://stackoverflow.com/questions/18967441/add-a-prefix-to-all-flask-routes
# # ref: https://flask.palletsprojects.com/en/2.3.x/config/#configuring-from-environment-variables
# app.config.from_prefixed_env()


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/render', methods=['POST'])
def render_template():
    data = request.get_json()

    client = docker.from_env()

    # repository, tag = docker.utils.parse_repository_tag(
    #     os.getenv('DOCKER_IMAGE', 'sivel/ansible-template-ui')
    # )
    repository, tag = docker.utils.parse_repository_tag(
        os.getenv('DOCKER_ANSIBLE_EE_IMAGE', 'lj020326/ansible-execution-env')
    )
    docker_registry_username = os.getenv('DOCKER_REGISTRY_USERNAME')
    docker_registry_password = os.getenv('DOCKER_REGISTRY_PASSWORD')

    if not tag:
        tag = data.get('tag', 'stable')
        # tag = data.get('tag', 'latest')

    image = '%s:%s' % (repository, tag)
    app.logger.info("image=%s" % image)

    try:
        # ref: https://stackoverflow.com/questions/45663542/login-to-registry-with-docker-python-sdk-docker-py
        if docker_registry_username and docker_registry_password:
            client.login(username=docker_registry_username, password=docker_registry_password, registry=repository)

        client.images.pull(repository, tag=tag)

        container = client.containers.create(
            image,
            environment={
                'TEMPLATE': text.native(
                    base64.b64encode(
                        text.b(data['template'])
                    )
                ),
                'VARIABLES': text.native(
                    base64.b64encode(
                        text.b(data['variables']) or b'{}'
                    )
                ),
            },
            mem_limit='96m',
        )
        app.logger.info("starting container")
        container.start()
    except Exception as e:
        app.logger.exception('Failed to create and start container')
        return jsonify(**{'error': str(e)}), 400
    else:
        exit_status = container.wait()
        app.logger.info("exit_status=%s" % exit_status)
        stdout = container.logs(stdout=True, stderr=False)
        stderr = container.logs(stdout=False, stderr=True)

        app.logger.info("container.stdout=%s" % PrettyLog(stdout))
        app.logger.info("container.stderr=%s" % PrettyLog(stderr))

        # if stderr:
        #     return jsonify(**{'error': text.native(stderr)}), 400

        error = None
        try:
            response = json.loads(stdout)
        except ValueError:
            app.logger.exception('Could not parse JSON')
            error = stderr or 'Unknown Error'
        else:
            app.logger.info("response=%s" % PrettyLog(response))
            play = response['plays'][0]
            app.logger.info("play=%s" % PrettyLog(play))
            # if exit_status != 0:
            if exit_status['StatusCode'] != 0:
                error = play['tasks'][-1]['hosts']['localhost']['msg']
        if error:
            return jsonify(**{'error': text.native(error)}), 400
    finally:
        if not _DO_NOT_REMOVE_EXECUTION_ENV:
            try:
                container.remove(force=True)
            except NameError:
                pass

    b64_content = play['tasks'][1]['hosts']['localhost']['content']
    content = text.native(base64.b64decode(b64_content))

    return jsonify(**{'content': content})
