from functools import wraps

def importance(importance_level):
    """
    #### A decorator that adds an importance level to a function.
    Args:
    - importance_level: int or str, representing the level of importance of the function.
    
    Returns:
    - A wrapper function that adds the importance level as a print statement before executing the original function.
    
    Example:
    ```
    @importance("HIGH")
    def my_function():
        # some code here
        pass
    
    my_function()
    ```
    """
    def important_annotation(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(f"Importance_Level: {importance_level}")
            return func(*args, **kwargs)
        return wrapper
    return important_annotation
    