from functools import wraps
def with_side_effects(side_effects):
    """
    #### A decorator that adds possible side effects to a function and prints them after the function execution.

    Args:
    side_effects: a list of strings describing possible side effects of the function.

    Returns:
    The decorated function.

    Example:
    ```
    @with_side_effects(["may cause drowsiness", "do not operate heavy machinery after use"])
    def my_function():
        # some code here
        pass

    my_function()
    ```
    """
    if not isinstance(side_effects, list):
        raise TypeError("The 'side_effects' argument must be a list of strings")

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            result = fn(*args, **kwargs)
            fn.side_effects = side_effects
            print("Possible Side Effects:")
            if hasattr(fn, 'side_effects'):
                for effect in fn.side_effects:
                    print(f"- {effect}")
            return result
        return wrapper
    return decorator

def with_positive_effects(positive_effects):
    """
    #### A decorator that adds possible positive effects to a function.

    Args:
        positive_effects (list): A list of positive effects that the function can produce.

    Returns:
        function: A wrapped function that includes the specified positive effects.

    Example:
    ```
    @with_positive_effects(['Increased productivity', 'Improved customer satisfaction'])
    def my_function():
        # some code here
        pass

    my_function()
    ```
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            result = fn(*args, **kwargs)
            fn.positive_effects = positive_effects
            print("Possible Positive Effects:")
            if hasattr(fn, 'positive_effects'):
                for effect in fn.positive_effects:
                    print(f"- {effect}")
            return result
        return wrapper
    return decorator