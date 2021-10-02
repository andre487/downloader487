#!/usr/bin/env bash
set -eufo pipefail

cd "$(dirname "$0")"

.venv/bin/autopep8 \
    --in-place \
    --recursive \
    --aggressive \
    --global-config .pep8  \
    --pep8-passes 2 \
    .
