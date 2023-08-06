def sensitive(sensitivity_level):
    """
    #### Decorator that adds a sensitivity level to a function or class.

    Args:
    - sensitivity_level (str): A string representing the sensitivity level of the function or class.

    Returns:
    - A decorator that adds a sensitivity level attribute to the decorated function or class.

    Example:
    ```
    @sensitive(sensitivity_level="high")
    def my_sensitive_function():
        # do something sensitive
        pass
    ```
    """
    def decorator(func_or_class):
        def wrapper(*args, **kwargs):
            print("This information is sensitive and should be handled with care.")
            return func_or_class(*args, **kwargs)
        wrapper.sensitivity_level = sensitivity_level
        return wrapper
    return decorator
