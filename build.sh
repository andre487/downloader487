#!/usr/bin/env bash
set -eufo pipefail

cd "$(dirname "$0")"

.venv/bin/pyinstaller --noconfirm --onefile --name downloader487 main.py
