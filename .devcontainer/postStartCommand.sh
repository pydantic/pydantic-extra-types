#!/usr/bin/env bash

# run in the background at startup
nohup bash .devcontainer/postStartBackground.sh > ".dev_container_logs/postStartBackground.out" &
