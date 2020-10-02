#import Main_backend
import foo
import ast
import inspect
def contains_explicit_return(f):
    return any(isinstance(node, ast.Return) for node in ast.walk(ast.parse(inspect.getsource(f))))

for name, val in foo.__dict__.items(): # iterate through every module's attributes
    if callable(val):                      # check if callable (normally functions)
        if contains_explicit_return(val):
            print("not threadable"   )# call it
        else:
            print("threadable: " + val.__name__)