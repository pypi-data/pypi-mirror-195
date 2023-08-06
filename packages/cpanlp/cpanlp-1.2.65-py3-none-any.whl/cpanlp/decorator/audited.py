def audited(func):
    """
    #### This decorator checks if a function has been audited before allowing it to be executed.

    ### Example:
    ```
    @audited
    def my_function():
        # some code here
        pass

    my_function.audited = True

    ```
    """
    func.audited = True
    def wrapper(*args, **kwargs):
        if func.audited:
            return func(*args, **kwargs)
        else:
            raise Exception(f"{func.__name__} has not been audited.")
    return wrapper