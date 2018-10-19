from typing import Text, Dict
from abc import ABCMeta, abstractmethod
import inspect
from logging import getLogger

logger = getLogger(__name__)

_namespace = {}


def register_task(name: Text, obj: object):
    if name is None or not isinstance(name, str):
        raise AttributeError(f"Name must be str!")
    if name in _namespace:
        raise ValueError(f"Name {name} is already in namespace!")
    logger.info(f"{obj} registered ")
    _namespace[name] = obj


def run_task(name: Text, params: Dict):
    """
    Task running
    Args:
        name: task registered name
        params: task's kwargs

    Returns:
        task out
    """
    executor = _namespace.get(name, None)

    if executor is None:
        raise KeyError(f"Task {name} does not registered!")

    if issubclass(executor, BaseTask):
        executor = executor().run

    elif not inspect.isfunction(executor):
        raise TypeError(f"{name} with type {type(executor)} must be function or BaseTask class!")

    return executor(**params)


def task(name: Text):
    def dec(func):
        register_task(name, func)
        return func
    return dec


class TaskMeta(ABCMeta):
    """
    Register task classes
    """
    def __new__(mcs, name, bases, attrs):
        cls = super().__new__(mcs, name, bases, attrs)
        if not inspect.isabstract(cls):
            register_task(cls.name, cls)
        return cls


class BaseTask(metaclass=TaskMeta):
    """
    Task abstract class
    """
    name = None

    @staticmethod
    @abstractmethod
    def run(*args, **kwargs):
        pass
