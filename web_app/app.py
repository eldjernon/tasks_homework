from flask import Flask
from flask import request
from flask import jsonify
from tasks.execute import run_task
from flask.logging import create_logger
import jsonschema


app = Flask("tasks_server")

logger = create_logger(app)

run_schema = {'type': 'object',
              'properties': {
                  'task_name': {'type': 'string'},
                  'params': {'type': ['object', 'null']}
              },
              'required': ['task_name', 'params']}


@app.route('/v1/run', methods=['POST'])
def run():
    try:
        data = request.get_json(force=True)
        jsonschema.validate(data, run_schema)
        task_name = data["task_name"]
        params = data["params"] or {}

        task_result = run_task(task_name, params)

        result = {"result": task_result}
        return jsonify(result), 200
    except Exception as exc:
        logger.exception(exc)
        err_msg = {
            "status": "ERROR",
            "error_code": 100,
            "error_msg": f"{exc}"
        }
        return jsonify(err_msg), 400


def runserver():
    app.run(port=8081)
