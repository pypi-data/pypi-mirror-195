from functools import wraps

def future_tense(func):
    """
    Decorator that prints the function name in future tense.

    Example:
    ```
    @future_tense
    def greet(name):
        print(f"Hello, {name}!")

    greet("John")
    ```
    Output:
    ```
    future_tense: greet
    Hello, John!
    ```

    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"future_tense: {func.__name__}")
        result = func(*args, **kwargs)
        return result
    return wrapper
