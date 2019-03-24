#!/usr/bin/env bash
export DATAROBOT_SERVER="https://<ENTER-URL-HERE>.datarobot.com"
export DATAROBOT_SERVER_KEY="<ENTER-DATAROBOT-KEY-HERE>"
export DATAROBOT_DEPLOYMENT_ID="<ENTER-DEPLOYMENT-ID-HERE>"
export DATAROBOT_USERNAME="<ENTER-USERNAME-HERE>"
export DATAROBOT_API_TOKEN="<ENTER-API-TOKEN-HERE>"

export FLASK_APP=api.py
export FLASK_RUN_HOST=127.0.0.1
export FLASK_RUN_PORT=5000

export PYTHONPATH="$(dirname "$(pwd)")":$PYTHONPATH

mkdir -p upload
flask run