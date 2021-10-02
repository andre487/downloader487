#!/usr/bin/env bash
set -eufo pipefail

cd "$(dirname "$0")"

./build.sh
dist/downloader487 "$@"
