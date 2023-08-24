import ast


def extract_functions_from_code(code):
    functions = []
    tree = ast.parse(code)

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            functions.append(node)

    return functions


def compare_functions(string1, string2):
    functions1 = extract_functions_from_code(string1)
    tree2 = ast.parse(string2).body[0]

    similar_functions = []

    for function1 in functions1:
        if ast.dump(function1) == ast.dump(tree2):
            similar_functions.append(function1)

    return similar_functions


def print_matching_functions(matching_functions):
    if matching_functions:
        print("Similar Functions Found:")
        for function in matching_functions:
            print(ast.dump(function))
    else:
        print("No Similar Functions Found.")


# Example usage
string1 = """
import math

class Calculator:
    def add(self, a, b):
        return a + b

def subtract(a, b):
    return a - b
"""

string2 = """
def add(self,a, b):
    return a + b
"""

similar_functions = compare_functions(string1, string2)
print_matching_functions(similar_functions)
