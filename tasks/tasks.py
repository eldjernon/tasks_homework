from typing import Text, Dict, Callable
from abc import ABCMeta, abstractmethod
import inspect
import jsonschema
from logging import getLogger

logger = getLogger(__name__)

_namespace = {}


class TaskMeta(ABCMeta):
    """
    Register task classes
    """

    def __new__(mcs, name, bases, attrs):
        cls = super().__new__(mcs, name, bases, attrs)
        if not inspect.isabstract(cls):
            _register_task(cls)
        return cls


class BaseTask(metaclass=TaskMeta):
    """
    Task abstract class
    """
    name = None
    json_schema = None

    @staticmethod
    @abstractmethod
    def run(*args, **kwargs):
        pass

    def __repr__(self):
        return f"Task(name={self.name})"


def task_decorator(name: Text, json_schema: Dict = None):
    def dec(func):
        _create_task_cls(name, func, json_schema)
        return func

    return dec


def _register_task(cls: "BaseTask"):
    if cls.name is None or not isinstance(cls.name, str):
        raise AttributeError(f"Name must be string!")
    if cls.name in _namespace:
        raise ValueError(f"Name {cls.name} is already in namespace!")
    logger.info(f"{cls} registered ")
    _namespace[cls.name] = cls


def _create_task_cls(name: Text, run: Callable, json_schema: Dict):
    """
    Create task class from decorated function
    Args:
        name: task name
        run: task function
        json_schema: params validator

    Returns:
        BaseTask subclass
    """
    return type(name, (BaseTask,),
                {"name": name,
                 "run": staticmethod(run),
                 "json_schema": json_schema})


def run_task(name: Text, params: Dict):
    """
    Task running
    Args:
        name: task registered name
        params: task's kwargs

    Returns:
        task out
    """
    task: BaseTask = _namespace.get(name, None)

    if task is None:
        raise KeyError(f"Task {name} does not registered!")

    if task.json_schema is not None:
        jsonschema.validate(params, task.json_schema)

    if issubclass(task, BaseTask):
        return task().run(**params)
    else:
        raise TypeError(f"{name} with type {type(task)} must be task decorated function or BaseTask subclass!")
