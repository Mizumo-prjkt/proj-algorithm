#!/bin/bash

if [ -e '/usr/bin/python' ] || [ -e '/usr/bin/python3' ]; then
    python -m venv .venv
    # or
    python3 -m venv .venv
else
    echo "No python installed, exiting"
    exit 0
fi

source .venv/bin/activate

pip install pygame numpy