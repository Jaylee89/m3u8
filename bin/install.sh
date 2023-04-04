#!/bin/bash

set -e
# set -x

echo "installing python3 virtaul env"

TOP=$(cd "$(dirname $0)"/..;pwd)
rm -rf "$TOP/venv"

python3 -m venv "$TOP/venv"

"$TOP/venv/bin/python3" -m pip install --upgrade pip
"$TOP/venv/bin/pip3" install -r "$TOP/requirements.txt" --index-url=https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
