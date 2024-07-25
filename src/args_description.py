from functools import wraps

def describe_args(**descriptions):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        wrapper.__descriptions__ = descriptions
        return wrapper
    return decorator

# @describe_args(arg1="This is the first argument, an integer.", arg2="This is the second argument, a string.")
# def my_function(arg1: int, arg2: str):
#     print(f"arg1: {arg1}, arg2: {arg2}")

# # Accessing descriptions
# print(my_function.__descriptions__)

# # Usage
# my_function(10, "example")
