import os
import csv

def read_file(file_path):
    """
    Reads the content of a given file based on its extension.

    Supported:
    - .txt, .py, .c, .java → returns full text as a string
    - .csv → returns list of rows (each row is a list of columns)

    Raises:
    - ValueError for unsupported file types
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    _, ext = os.path.splitext(file_path)
    ext = ext.lower()

    text_extensions = ['.txt', '.py', '.c', '.java']

    if ext in text_extensions:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

    elif ext == '.csv':
        with open(file_path, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            return list(reader)

    else:
        raise ValueError(f"Unsupported file type: {ext}")
