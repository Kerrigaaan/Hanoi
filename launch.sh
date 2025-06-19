#!/bin/bash

set -x

#cd "$(cd $(dirname $0); pwd)"

if [ ! -d venv ]; then
	python -m venv venv
fi

. venv/bin/activate

pip install -f ../../libs --no-index notebook pygame

./reset.sh
jupyter notebook
