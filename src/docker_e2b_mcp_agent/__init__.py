"""Docker E2B MCP Agent package."""

from .config import ConfigurationError, Settings
from .workflow import DEFAULT_TASK, run_workflow

__all__ = ["DEFAULT_TASK", "ConfigurationError", "Settings", "run_workflow"]
__version__ = "1.0.0"
