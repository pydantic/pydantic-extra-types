#!/usr/bin/env bash
set -e

# git settings
git config --global pull.rebase true


pip install pip-tools
make install

mkdir -p .dev_container_logs
