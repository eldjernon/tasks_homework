"""
Exceptions raised by delayed tasks
"""


class BaseTasksError(Exception):
    """
    Base exceptions class
    """
    code = 100


class TaskExecutionError(BaseTasksError):
    """
    Raise exception which catched in task executions
    """
    code = 200


class TaskConfigurationError(BaseTasksError):
    """
    Raised if  task's configuration failed
    """
    code = 300
