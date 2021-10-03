#!/usr/bin/env bash
set -eufo pipefail

cd "$(dirname "$0")"

echo '===> Build downloader binary file'
.venv/bin/pyinstaller --noconfirm --onefile --name downloader487 main.py
