#! /bin/bash

set -e

# store location of this script
STATIC_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# test all Python files
for PY_FILE in `ls ${STATIC_DIR}/*.py`; do
    python ${PY_FILE}
done

