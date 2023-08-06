# mypackage

`rdsutilspack` is a Python package that sends a "hi" message to a server.

## Installation

You can install `rdsutilspack` using `pip`:

```bash
pip install rdsutilspack

python setup.py sdist
twine upload dist/*

>python -m twine upload --repository-url http://localhost:8080/ dist\*

```
Usage
To use rdsutilspack, simply execute it from the command line:

This will send a "hi" message to a server and print the response to the console.
