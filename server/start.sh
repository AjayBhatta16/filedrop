#!/bin/bash
CONFIG_FILE_PATH="../functions/env.json"

eval $(python3 -c "
import json
with open('$CONFIG_FILE_PATH') as f:
    config = json.load(f)
for k, v in config.items():
    print(f'export {k}={json.dumps(str(v))}')
")

python3 application.py && echo