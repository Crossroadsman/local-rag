import os

# `file_handler.py` is responsible for iterating through files in a directory
# and determining their type

def list_files(directory):
    supported_extensions = [
        '.txt',
        '.md',
        '.docx',
        '.xlsx',
        '.pdf',
    ]

    files = []

    for file in os.listdir(directory):
        ext = os.path.splitext(file)[1]
        if ext in supported_extensions:
            files.append(os.path.join(directory, file))

    return files
