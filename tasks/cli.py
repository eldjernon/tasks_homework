from typing import Text, Dict
import argparse
import json
import sys
from .tasks import run_task

parser = argparse.ArgumentParser()
parser.add_argument("name", type=str, help="name")
parser.add_argument("-p", "--params", type=str, default="{}", help="params")


def run_cli():
    args = parser.parse_args()
    name = args.name
    params = _load_params(args.params)
    sys.stdout.write(str(run_task(name, params)))


def _load_params(params: Text) -> Dict:
    try:
        return json.loads(params)
    except json.JSONDecodeError:
        print("Params bad value, need json serializable string")
        sys.exit(1)
