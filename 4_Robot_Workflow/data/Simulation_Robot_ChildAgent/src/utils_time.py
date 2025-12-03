"""
Utility functions for measuring time
"""

import time
from typing import Tuple, Any, Callable


def measure_time(func: Callable) -> Tuple[Any, float]:
    """
    Measure the execution time of a function.
    
    Args:
        func: Function to measure
        
    Returns:
        Tuple of (result, elapsed_time_in_seconds)
    """
    start_time = time.time()
    result = func()
    end_time = time.time()
    elapsed_time = end_time - start_time
    return result, elapsed_time


def measure_api_call(api_call_func: Callable) -> Tuple[Any, float]:
    """
    Measure the execution time of an API call.
    
    Args:
        api_call_func: Function that makes an API call (should return the response)
        
    Returns:
        Tuple of (response, elapsed_time_in_seconds)
        
    Example:
        response, response_time = measure_api_call(lambda: requests.post(url, json=data))
    """
    start_time = time.time()
    try:
        response = api_call_func()
        end_time = time.time()
        elapsed_time = round(end_time - start_time, 6)
        return response, elapsed_time
    except Exception as e:
        end_time = time.time()
        elapsed_time = round(end_time - start_time, 6)
        # Re-raise the exception but still return the elapsed time
        raise e


