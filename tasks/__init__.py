"""
tasks - delayed task execution system
"""

from tasks.core.tasks import task_decorator as task
from tasks.core.tasks import BaseTask
from .cli import run_cli
from tasks.core.execute import run_task

__version__ = "0.3.0"
