#!/usr/bin/env fish
source venv/bin/activate.fish
export GOOGLE_APPLICATION_CREDENTIALS="./todo-fask-6ed076744681.json"
export FLASK_ENV=development
export FLASK_DEBUG=1
export FLASK_APP=main.py
