import os
import sys
import gitignore_parser
import ast
import json
import argparse

def describe_directory(directory, ignore_git=True):
    """
    Recursively describe all files in a directory.
    """
    gitignore_path = os.path.abspath(os.path.join(directory, '.gitignore'))
    gitignore = gitignore_parser.parse_gitignore(gitignore_path) if ignore_git and os.path.isfile(gitignore_path) else None
    output = {}
    for root, dirs, files in os.walk(directory):
        for file in files:
            path = os.path.join(root, file)
            if file.endswith('.py') and (gitignore is None or not gitignore(path)):
                with open(path) as f:
                    code = f.read()
                    module = ast.parse(code)
                    module_data = {}
                    functions = {}
                    classes = {}
                    argparse_args = []
                    for node in module.body:
                        if isinstance(node, ast.FunctionDef):
                            signature = ast.unparse(node.args)
                            if ast.get_docstring(node) is None:
                                docstring = ""
                            else:
                                docstring = ast.get_docstring(node)
                            functions.update({node.name.replace(" ", "") + "(" + signature.replace(" ", "") + ")": docstring})
                            # Search for an argparse object in the function body
                            for child_node in node.body:
                                if isinstance(child_node, ast.Assign):
                                    if isinstance(child_node.value, ast.Call):
                                        if isinstance(child_node.value.func, ast.Attribute) and child_node.value.func.attr == "ArgumentParser":
                                            argparse_obj = child_node.value
                                            # Extract the help text for each argument
                                            for arg_node in argparse_obj.keywords:
                                                if arg_node.arg == "description":
                                                    argparse_args.append(arg_node.value.s)
                                                elif arg_node.arg == "argument_default":
                                                    argparse_args.append(arg_node.value)
                                                elif arg_node.arg == "argument_default":
                                                    argparse_args.append(arg_node.value.s)
                        elif isinstance(node, ast.ClassDef):
                            if ast.get_docstring(node) is None:
                                docstring = ""
                            else:
                                docstring = ast.get_docstring(node)
                            methods = {}
                            for method in node.body:
                                if isinstance(method, ast.FunctionDef):
                                    signature = ast.unparse(method.args)
                                    if ast.get_docstring(method) is None:
                                        docstring = ""
                                    else:
                                        docstring = ast.get_docstring(method)
                                    methods.update({method.name.replace(" ", "") + "(" + signature.replace(" ", "") + ")": docstring})
                            classes.update({node.name.replace(" ", ""): {"methods": methods}})
                    if functions:
                        module_data["functions"] = functions
                    if classes:
                        module_data["classes"] = classes
                    if argparse_args:
                        module_data["argparse_args"] = argparse_args
                    if module_data:
                        output[path.replace(" ", "")] = module_data
    return output

def main():
    """
    Parse command line arguments and describe directory.
    """
    parser = argparse.ArgumentParser(description='Describe Python directory')
    parser.add_argument('directory', type=str, help='directory to describe')
    parser.add_argument('--no-gitignore', action='store_true', help='ignore .gitignore')
    args = parser.parse_args()

    directory = args.directory
    ignore_git = args.no_gitignore
    output = describe_directory(directory, ignore_git=ignore_git)
    output_str = '\n'.join(f"{k}: {v}" for k, v in {
        k: {x: {y + f'({z})' * (y != '__init__'): a} for x, b in v.items() for y, z, a in [(k, x, b)] if x == 'classes' or x == 'arguments'}
        for k, v in output.items() if v}.items())
    print(output_str)

if __name__ == '__main__':
    main()
