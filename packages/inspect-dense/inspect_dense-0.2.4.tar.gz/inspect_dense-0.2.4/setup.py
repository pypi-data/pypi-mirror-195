# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['inspect_dense']

package_data = \
{'': ['*']}

install_requires = \
['chardet>=5.1.0,<6.0.0', 'gitignore-parser>=0.1.3,<0.2.0']

entry_points = \
{'console_scripts': ['inspect-dense = inspect_dense.getcode:main']}

setup_kwargs = {
    'name': 'inspect-dense',
    'version': '0.2.4',
    'description': 'A tool for recursively describing all files in a directory.',
    'long_description': 'inspect-dense\n==========\n\ninspect-dense is a Python package for recursively describing all python files in a directory. \nProvides a simple way to get a high-level overview of a project\'s codebase in a conscise format to minimize tokens used.\n\nInstallation\n------------\n\nYou can install inspect-dense using pip:\n\nCopy code\n\n`pip install inspect-dense`\n\nUsage\n-----\n\nTo use inspect-dense, simply import the `describe_directory` function from the package and pass it the directory path you want to describe:\n\npython code\n```python\nfrom inspect-dense import describe_directory  \n\ndirectory = "/path/to/directory" \noutput = describe_directory(directory)\n```\n\nThe `describe_directory` function returns a dictionary with the following structure:\n\n```json\n{     "/path/to/file.py": {         "functions": {             "function_name(args)": "Function docstring"         },         "classes": {             "Class1": {                 "methods": {                     "method1(args)": "Method docstring",                     "method2(args)": "Method docstring"                 }             },             "Class2": {                 "methods": {                     "method3(args)": "Method docstring",                     "method4(args)": "Method docstring"                 }             }         }     } }\n```\nCommand Line Interface\n----------------------\n\ninspect-dense also comes with a command line interface. You can use it to describe a directory and output the results to a file:\n\n`inspect-dense <directory> [--no-gitignore]`\n\nFor example:\n\n`inspect-dense /path/to/directory --no-gitignore`\n\nThis will output the results.\n\nLicense\n-------\n\nThis project is licensed under the Apache 2 License - see the [LICENSE](LICENSE) file for details.',
    'author': 'Justin Riddiough',
    'author_email': 'justin@visioninit.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/neural-loop/inspect_dense',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
