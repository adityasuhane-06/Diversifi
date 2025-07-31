#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Run the FastAPI application with gunicorn
exec gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
