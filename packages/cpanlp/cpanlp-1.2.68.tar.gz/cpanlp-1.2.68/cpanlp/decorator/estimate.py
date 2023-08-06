from functools import wraps

def prob(probability):
    """
    #### A decorator that estimates the probability of a function's return value.

    Args:
    - probability (float): the estimated probability of the function's return value.

    Returns:
    - wrapper (function): the decorated function that estimates the probability of its return value.

    ### Example:
    ```
    @prob(0.8)
    def toss_coin():
        import random
        return "heads" if random.random() < 0.5 else "tails"

    result = toss_coin()
    print(f"Probability of heads: {toss_coin.probability}")
    ```

    """
    def estimated(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            func.probability = probability
            print(f"Estimate probability of {probability}: {result}")
            return result
        return wrapper
    return estimated

