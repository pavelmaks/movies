#!/bin/bash

gunicorn --workers=4 -b 0.0.0.0:8000 -k uvicorn.workers.UvicornWorker main:app