#!/usr/bin/env bash
set -eufo pipefail

cd "$(dirname "$0")"

export GOOS=linux
export GOARCH=amd64

go build -o downloader487-sync .
