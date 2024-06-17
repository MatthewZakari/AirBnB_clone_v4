#!/usr/bin/python3
"""
W3C validator script for Holberton School

This script validates HTML and CSS files using W3C APIs.

Functionality:
- Validates single or multiple files provided as arguments.
- Supports HTML and CSS file formats.
- Prints validation errors to STDERR.
- Returns the number of errors (0 for success) as the exit status.

API references:
  - HTML: https://validator.w3.org/nu/
  - CSS: http://jigsaw.w3.org/css-validator/validator
"""

import sys
import requests


def print_stdout(message):
  """Prints a message to standard output."""
  sys.stdout.write(message)


def print_stderr(message):
  """Prints a message to standard error."""
  sys.stderr.write(message)


def analyze_html(file_path):
  """Analyzes an HTML file using the W3C validator API."""
  headers = {'Content-Type': 'text/html; charset=utf-8'}
  data = open(file_path, 'rb').read()
  url = 'https://validator.w3.org/nu/?out=json'
  response = requests.post(url, headers=headers, data=data)

  if response.status_code < 400:
    messages = response.json().get('messages', [])
    results = []
    for message in messages:
      results.append(f"[{file_path}:{message['lastLine']}] {message['message']}")
    return results
  else:
    raise ConnectionError(f"Failed to connect to W3C validator API.")


def analyze_css(file_path):
  """Analyzes a CSS file using the W3C validator API."""
  data = {'output': 'json'}
  files = {'file': (file_path, open(file_path, 'rb'), 'text/css')}
  url = 'http://jigsaw.w3.org/css-validator/validator'
  response = requests.post(url, data=data, files=files)

  if response.status_code < 400:
    errors = response.json().get('cssvalidation', {}).get('errors', [])
    results = []
    for error in errors:
      results.append(f"[{file_path}:{error['line']}] {error['message']}")
    return results
  else:
    raise ConnectionError(f"Failed to connect to W3C validator API.")


def analyze(file_path):
  """Analyzes a file based on its extension and prints results."""
  errors = 0
  try:
    if file_path.endswith('.css'):
      results = analyze_css(file_path)
    else:
      results = analyze_html(file_path)

    if results:
      for message in results:
        print_stderr(f"{message}\n")
        errors += 1
    else:
      print_stdout(f"{file_path}: OK\n")
  except Exception as e:
    print_stderr(f"[{e.__class__.__name__}] {e}\n")
  return errors


def process_files():
  """Loops through provided file arguments and analyzes each file."""
  errors = 0
  for file_path in sys.argv[1:]:
    errors += analyze(file_path)
  return errors


if __name__ == "__main__":
  """Script entry point. Handles argument validation and exit code."""
  if len(sys.argv) < 2:
    print_stderr("Usage: w3c_validator.py file1 file2 ...\n")
    exit(1)

  exit(process_files())
