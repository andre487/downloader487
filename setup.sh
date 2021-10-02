#!/usr/bin/env bash
set -eufo pipefail

cd "$(dirname "$0")"

echo '===> Create virtual env'
python3 -m venv .venv

echo '===> Update pip'
.venv/bin/python3 -m pip install -U pip
