#!/bin/bash
gunicorn -b 127.0.0.1:8001 run:app
