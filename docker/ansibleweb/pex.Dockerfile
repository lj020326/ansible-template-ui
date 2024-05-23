FROM python:3.11 AS deps

## ref: https://pythonspeed.com/articles/multi-stage-docker-python/

RUN apt-get update
RUN apt-get install -y --no-install-recommends build-essential gcc

#RUN python -m venv /opt/venv
## Make sure we use the virtualenv:
#ENV PATH="/opt/venv/bin:$PATH"

RUN pip install pex

WORKDIR /code

#COPY ansible_template_ui.pex /home/gunicorn/ansible_template_ui.pex
COPY ansible_template_ui.pex /home/gunicorn

COPY requirements.txt /home/gunicorn/
COPY deploy-requirements.txt /home/gunicorn/
COPY pex-requirements.txt /home/gunicorn/
COPY setup.py /home/gunicorn/
COPY README.md /home/gunicorn/

#RUN pip install -r /home/gunicorn/requirements.txt -r /home/gunicorn/deploy-requirements.txt
RUN pip install -r /home/gunicorn/requirements.txt

#COPY build_pex.sh /home/gunicorn/build_pex.sh
#RUN /home/gunicorn/build_pex.sh

## ref: https://dev.to/cwprogram/python-executable-packaging-with-pex-50g9
## ref: https://github.com/cwgem/pex_web_example/blob/main/Dockerfile_pex_tools

RUN PEX_TOOLS=1 python /home/gunicorn/ansible_template_ui.pex venv --scope=deps --compile /home/gunicorn/app

FROM python:3.11 AS srcs

RUN mkdir -p /home/gunicorn/app
#COPY ansible_template_ui.pex /home/gunicorn/ansible_template_ui.pex
COPY ansible_template_ui.pex /home/gunicorn
COPY gunicorn.config.py /home/gunicorn/app

RUN PEX_TOOLS=1 python /home/gunicorn/ansible_template_ui.pex venv --scope=srcs --compile /home/gunicorn/app

FROM python:3.11 AS build-image

## ref: https://dev.to/cwprogram/python-executable-packaging-with-pex-50g9
## ref: https://github.com/cwgem/pex_web_example

RUN useradd -d /home/gunicorn -r -m -U -s /bin/bash gunicorn
USER gunicorn

COPY --from=deps --chown=gunicorn:gunicorn /home/gunicorn/app /home/gunicorn/app
COPY --from=srcs --chown=gunicorn:gunicorn /home/gunicorn/app /home/gunicorn/app
USER gunicorn
ENTRYPOINT /home/gunicorn/app/pex

COPY ansible_run_env /home/gunicorn/ansible

ENTRYPOINT /home/gunicorn/app/pex
#ENTRYPOINT /home/gunicorn/app/web_app.pex
#ENTRYPOINT /home/gunicorn/app/web_app.pex -k gevent web_app:app
EXPOSE 8080
