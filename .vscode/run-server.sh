#!/usr/bin/env bash

if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source venv/bin/activate

pip install -r requirements.txt

cd src
python generate.py
python app.py --config ../config/config.yml