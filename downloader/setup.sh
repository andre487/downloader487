#!/usr/bin/env bash
set -eufo pipefail

cd "$(dirname "$0")"

echo '===> Create virtual env'
python3.8 -m venv --copies .venv

echo '===> Update pip'
.venv/bin/python3 -m pip install -U pip

echo '===> Install requirements'
.venv/bin/python3 -m pip install -r requirements.txt
