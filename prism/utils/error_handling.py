"""
This module provides error handling functionality for PRISM.
"""

from functools import wraps
from typing import Any, Callable

from .logging import prism_logger


class PRISMError(Exception):
    """Base exception class for PRISM-specific errors."""

    pass


class DataCollectionError(PRISMError):
    """Exception raised for errors in the data collection process."""

    pass


class AnalysisError(PRISMError):
    """Exception raised for errors in the analysis process."""

    pass


class ReportingError(PRISMError):
    """Exception raised for errors in the reporting process."""

    pass


def handle_errors(func: Callable) -> Callable:
    """
    Decorate a function to handle errors.

    Args:
    func (Callable): The function to decorate.

    Returns:
    Callable: Decorated function with error handling.
    """

    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        try:
            return func(*args, **kwargs)
        except PRISMError as e:
            prism_logger.error(f"PRISM-specific error in {func.__name__}: {str(e)}")
            raise
        except Exception as e:
            prism_logger.error(f"Unexpected error in {func.__name__}: {str(e)}")
            raise PRISMError(f"An unexpected error occurred in {func.__name__}") from e

    return wrapper


def safe_execute(func: Callable, *args, **kwargs) -> Any:
    """
    Safely execute a function and handle any errors.

    Args:
    func (Callable): The function to execute.
    *args: Positional arguments to pass to the function.
    **kwargs: Keyword arguments to pass to the function.

    Returns:
    Any: The result of the function if successful, None otherwise.
    """
    try:
        return func(*args, **kwargs)
    except Exception as e:
        prism_logger.error(f"Error executing {func.__name__}: {str(e)}")
        return None
