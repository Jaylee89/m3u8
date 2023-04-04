#!/bin/bash

set -e
# set -x

TOP=$(cd "$(dirname $0)"/..;pwd)

source "$TOP/venv/bin/activate"

"$TOP/venv/bin/python3" -s "$TOP/tests/tests.py"

# mkdir -p "$TOP/test-reports"

# "$TOP/venv/bin/python3" -m flake8 | tee "$TOP/test-reports/flake8.log"
