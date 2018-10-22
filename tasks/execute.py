from typing import Text, Dict
from multiprocessing import Process, Manager
from functools import wraps
import jsonschema

from tasks.exceptions import TaskExecutionError
from tasks.tasks import get_task_from_namespace


def save_result(results):
    """
    Decorator to save target func result in shared dict
    Args:
        results:
    Returns:
        wrap
    """
    def wrap(func):
        @wraps(func)
        def _wrap(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                results["task"] = result
            except Exception as exc:
                results["error"] = exc
        return _wrap

    return wrap


def run_task(name: Text, params: Dict):
    """
    Task running
    Args:
        name: task registered name
        params: task's kwargs

    Returns:
        task out
    """

    task = get_task_from_namespace(name)
    manager = Manager()
    results = manager.dict()

    if task.json_schema is not None:
        jsonschema.validate(params, task.json_schema)

    process = Process(target=save_result(results)(task().run), kwargs=params)
    process.start()
    process.join()

    if "error" in results:
        raise TaskExecutionError(results["error"])

    return results["task"]
