"""Langflow main module."""

# 在模块初始化时设置警告过滤器，确保清洁的日志输出
import langflow.logging.suppress_warnings  # noqa: F401

__version__ = "1.0.20"

__all__ = ["__version__"]
