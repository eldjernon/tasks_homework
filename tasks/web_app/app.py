from flask import Flask
from flask import request
from flask import jsonify
from flask.logging import create_logger

from .utils import EmailSender

from tasks.core.execute import run_task
from tasks.exceptions import BaseTasksError

import jsonschema

app = Flask("tasks_server")

logger = create_logger(app)

run_schema = {'type': 'object',
              'properties': {
                  'task_name': {'type': 'string'},
                  'params': {'type': ['object', 'null']},
                  'email': {'type': 'string'}
              },
              'required': ['task_name', 'params']}


@app.route('/v1/run', methods=['POST'])
def run():
    try:
        data = request.get_json(force=True)
        jsonschema.validate(data, run_schema)
        task_name = data["task_name"]
        params = data["params"] or {}
        email = data.get("email")

        task_result = run_task(task_name, params)

        if not email:
            result = {"result": task_result}
        else:
            EmailSender().send_email(msg=str(task_result),
                                     to_addr=email)
            result = {"result": "OK"}

        return jsonify(result), 200
    except BaseTasksError as exc:
        logger.exception(exc)
        err_msg = {
            "status": "ERROR",
            "error_code": exc.code,
            "error_msg": f"{exc}"
        }
        return jsonify(err_msg), 400


def runserver():
    app.run(port=8081)
