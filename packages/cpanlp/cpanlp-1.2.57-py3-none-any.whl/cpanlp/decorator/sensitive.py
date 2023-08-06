def sensitive(sensitivity_level):
    """
    ### Example:
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
