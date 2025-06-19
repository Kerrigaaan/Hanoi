#!/bin/bash

set -x
# SCRIPT_DIR="$(cd $(dirname $0); pwd)"
# cd "${SCRIPT_DIR}"
rm -rf '.ipynb_checkpoints'
find . -name '__pycache__' | xargs rm -rf
git reset --hard HEAD
