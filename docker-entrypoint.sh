#!/bin/bash

if [[ "$1" = *".py" ]]; then
    PYTHONPATH=.:./lib exec python $@
    exit $?
fi

if [[ "$1" = "python"* ]]; then
    shift
    PYTHONPATH=.:./lib exec python $@
fi

FLASK_APP=api flask routes
FLASK_DEBUG=1 FLASK_ENV=production FLASK_APP=api flask run --host=0.0.0.0 --port=5000
