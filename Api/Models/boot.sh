#!/bin/sh
conda activate opanalytics
exec gunicorn -b 0.0.0.0:5000 --timeout 600 --access-logfile - --error-logfile - api:app