from functools import wraps

""" A decorator in Python is a function that wraps another function to add functionality to it, without modifying
the original function’s code. Decorators are often used for tasks such as logging, enforcing access control and
authentication, modifying input or output, and measuring performance, among others. 

wrapper():
    Purpose: This inner function (the actual wrapper) is where the additional behavior or functionality is defined. 
    It wraps the original function and can execute code before and after calling it.

decorator(func):
    Purpose: This is the outer function that takes the original function as an argument (often referred to as func). 
    Its main job is to define how the original function will be modified or enhanced.
    
@wraps(func) is a decorator from the functools module in Python that is used to preserve the metadata of the original 
function when creating a wrapper function inside another function (like a decorator). It is essential for maintaining the original function's name, docstring, and other attributes.
"""
def captatlize_input(func):
    print("code here will be run no matter if func was invoked or not...")
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("start running decorator (when func will be invoke), replace the code of the original function...")
        result = func()
        return result.upper()
    return wrapper

@captatlize_input
def some_function():
    return "abcdefg"

print(some_function())