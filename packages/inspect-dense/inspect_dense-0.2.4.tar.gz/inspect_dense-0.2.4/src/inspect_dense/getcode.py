import ast
import json
import os
import sys

import chardet
import gitignore_parser


import os
import ast
import chardet
import argparse
import gitignore_parser


def describe_directory(directory, ignore_git=True):
    """
    Recursively describe all files in a directory.
    """
    gitignore_path = os.path.join(directory, '.gitignore')
    gitignore = gitignore_parser.parse_gitignore(gitignore_path) if ignore_git and os.path.isfile(
        gitignore_path) else None
    output = {}
    for root, dirs, files in os.walk(directory):
        for file in files:
            path = os.path.join(root, file)
            if file.endswith('.py') and (gitignore is None or not gitignore(path)):
                with open(path, 'rb') as f:
                    content = f.read()
                    encoding = chardet.detect(content)['encoding']
                with open(path, encoding=encoding) as f:
                    code = f.read()
                    module = ast.parse(code)
                    module_data = {}
                    functions = {}
                    classes = {}
                    args = {}
                    for node in module.body:
                        if isinstance(node, ast.FunctionDef):
                            signature = ast.unparse(node.args)
                            if ast.get_docstring(node) != None:
                                docstring = _clean_output(ast.get_docstring(node))
                            else:
                                docstring = ""
                            functions.update(
                                {node.name.replace(" ", "") + "(" + signature.replace(" ", "") + ")": docstring})
                        elif isinstance(node, ast.ClassDef):
                            if ast.get_docstring(node) != None:
                                docstring = _clean_output(ast.get_docstring(node))
                            else:
                                docstring = ""
                            methods = {}
                            for method in node.body:
                                if isinstance(method, ast.FunctionDef):
                                    signature = ast.unparse(method.args)
                                    if ast.get_docstring(method) != None:
                                        docstring = _clean_output(ast.get_docstring(method))
                                    else:
                                        docstring = ""
                                    methods.update({method.name.replace(" ", "") + "(" + signature.replace(" ",
                                                                                                           "") + ")": docstring})
                                elif isinstance(method, ast.Assign):
                                    if isinstance(method.value, ast.Call):
                                        if isinstance(method.value.func, ast.Name) and method.value.func.id == 'argparse':
                                            for arg in method.value.keywords:
                                                args[arg.arg] = arg.value.s if isinstance(arg.value, ast.Str) else None
                            classes.update({node.name.replace(" ", ""): {"methods": methods}})
                    if functions:
                        module_data["functions"] = functions
                    if classes:
                        module_data["classes"] = classes
                    if args:
                        module_data["args"] = args
                    if module_data or code.strip() == "":
                        output[path.replace(" ", "")] = module_data

    return output


def _clean_output(output):
    """
    Removes extra spaces, tabs, and newlines from argparse output.
    """
    output = output.replace('\n', ' ')
    output = output.replace('\t', '')
    output = ' '.join(output.split())
    return output


def main():
    """
    Parse command line arguments and describe directory.
    """
    if len(sys.argv) < 2:
        print("Usage: pydescribe.py <directory>")
        sys.exit(1)
    directory = sys.argv[1]
    ignore_git = True
    if len(sys.argv) > 2 and sys.argv[2] == '--no-gitignore':
        ignore_git = False
    output = describe_directory(directory, ignore_git=ignore_git)
    print(json.dumps(output, indent=4))


if __name__ == '__main__':
    main()
