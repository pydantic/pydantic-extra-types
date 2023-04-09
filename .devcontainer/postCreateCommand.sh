#!/usr/bin/env bash
set -e

# git settings
git config --global pull.rebase true

# dependencies
pip install pip-tools
make install

# for background logs
mkdir -p .dev_container_logs
