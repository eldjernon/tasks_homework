from typing import Text, Dict
import argparse
import json
import sys

from tasks.core.execute import run_task
from tasks.web_app.app import runserver

parser = argparse.ArgumentParser()
parser.add_argument("command", type=str, help="name")
parser.add_argument("-p", "--params", type=str, help="params", required=False)


def run_cli():
    args = parser.parse_args()
    command = args.command
    if command == "runserver" and args.params is None:
        runserver()
    else:
        params = _load_params(args.params) if args.params else {}
        sys.stdout.write(str(run_task(command, params)))


def _load_params(params: Text) -> Dict:
    try:
        return json.loads(params)
    except json.JSONDecodeError:
        print("Params bad value, need json serializable string")
        sys.exit(1)
