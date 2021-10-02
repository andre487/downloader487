#!/usr/bin/env bash
set -eufo pipefail

cd "$(dirname "$0")"

set -x
.venv/bin/mypy . --ignore-missing-imports --disallow-untyped-defs "$@"
