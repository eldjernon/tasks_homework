from typing import Text, Dict, Callable
from abc import ABCMeta, abstractmethod
import inspect
from logging import getLogger

from tasks.exceptions import TaskConfigurationError

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
        raise TaskConfigurationError(f"Name must be string!")
    if cls.name in _namespace:
        raise TaskConfigurationError(f"Name {cls.name} is already in namespace!")
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


def get_task_from_namespace(name: Text):
    task: BaseTask = _namespace.get(name, None)

    if task is None:
        raise TaskConfigurationError(f"Task {name} does not registered!")

    if not issubclass(task, BaseTask):
        raise TaskConfigurationError(f"{name} with type {type(task)} "
                                     f"must be task decorated function or BaseTask subclass!")

    return task
