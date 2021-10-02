#!/usr/bin/env bash
set -eufo pipefail

cd "$(dirname "$0")"

export GOOS=linux
export GOARCH=arm

go build -o downloader487-sync .
