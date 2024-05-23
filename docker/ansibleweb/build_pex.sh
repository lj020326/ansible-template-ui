#!/bin/bash
python setup.py sdist
pex -o web_app.pex \
  -r deploy-requirements.txt \
  -r pex-requirements.txt \
  -f ./dist \
  -m 'gunicorn.app.wsgiapp:run' \
  --python-shebang='#!/usr/bin/env python' \
  --inject-args "--config /home/gunicorn/app/gunicorn.config.py"

