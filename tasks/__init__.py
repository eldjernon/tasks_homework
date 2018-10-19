"""
tasks - delayed task execution system
"""

from .tasks import task_decorator as task
from .tasks import BaseTask
from .cli import run_cli

__version__ = "0.2.0"
