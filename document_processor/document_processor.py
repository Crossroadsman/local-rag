# This will be the document processor app
from file_handler import list_files
from text_extractor import extract_content
from vectorizer import chunk_text, vectorize_text


directory = './test' # this will be an argument to the file, and we'll use os to process paths


def create_db_records(directory):
    records = []

    valid_files = list_files(directory)

    for file in valid_files:
        text = extract_content(file)
        chunks = chunk_text(text)
        vectors = vectorize_chunks(chunks)

        records.append({
            "file_path": file,
            "chunks": chunks,
            "vectors": vectors
        })

    return records
