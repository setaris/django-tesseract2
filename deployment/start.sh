#!/bin/bash
set -e
LOGFILE=/home/ubuntu/webapps/setarisocr/setarisocr.log
NUM_WORKERS=2
USER=ubuntu

# user/group to run as
cd /home/ubuntu/webapps/setarisocr/setarisocr
source /home/ubuntu/envs/setarisocrenv/bin/activate
exec python manage.py run_gunicorn --bind=127.0.0.1:8000 --settings=setarisocr.settings.production --workers=$NUM_WORKERS --timeout=120 --graceful-timeout=120 1>>$LOGFILE 2>>$LOGFILE
