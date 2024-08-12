import chromadb
from chromadb.config import Settings


def initialize_chroma(db_directory):
    """Initialize the Chroma client.

    Using combined duckdb and parquet. duckdb is an in-process SQL OLAP
    DBMS. It's designed for analytical queries rather than transactional
    workloads, meaning it's optimized for operations like aggregations,
    joins, and complex queries over large datasets. parquet is a columnar
    storage file format optimized for big data processing. It's particularly
    well-suited for storing large datasets that need to be queried efficiently
    """
    #client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet",
    #                                  persist_directory=db_directory))

    # Chroma's syntax has changed and the docs do not currently specify how
    # or whether you can choose a db implementation
    client = chromadb.PersistentClient(path=db_directory)
    return client


def get_or_create_collection(client, collection_name="documents"):
    """Creates a new collection in Chroma. Returns the collection instance.
    """
    collection = client.get_or_create_collection(name=collection_name)
    return collection


def add_records_to_collection(collection, records):
    """Adds records to the specified collection in Chroma where the records
    argument takes the following data structure:

    [
        {
            "file_path": os.path.join(directory, "file1.pdf"),
            "chunks": [
                {"text": "chunk1_file1", "position": 0},
                {"text": "chunk2_file1", "position": 1024},
            ],
            "vectors": [vector1_file1, vector2_file1]
        },
            "file_path": os.path.join(directory, "file2.docx"),
            "chunks": [
                {"text": "chunk1_file2", "position": 0},
                {"text": "chunk2_file2", "position": 1024},
                {"text": "chunk3_file2", "position": 2048}
            ],
            "vectors": [vector1_file2, vector2_file2, vector3_file2]
        {
        }, etc
    ]
    
    """

    # A unique ID is required for each vector
    #ids = [f"id_{i}" for i in range(len(vectors))]
    '''
    for i, record in enumerate(records):
        # add some testing here to ensure, e.g., len(record["chunks"]) == len(record["vectors"])
        for j, (chunk, vector) in enumerate(zip(record["chunks"], record["vectors"])):
            record_id = f"{i}-{j}"
            collection.add([{"id": record_id, "content": vector}], metadata=[{
                "filename": record["file_path"],
                "chunk_index": j,
                "chunk_text": chunk["text"],
                "chunk_position": chunk["position"]
            }])
    '''

    # if the above doesn't work then try the following instead
    '''
    for i, record in enumerate(records):
        # add some testing here to ensure, e.g., len(record["chunks"]) == len(record["vectors"])
        for j, (chunk, vector) in enumerate(zip(record["chunks"], record["vectors"])):
            metadata = {
                "filename": record["file_path"],
                "chunk_index": j,
                "chunk_text": chunk["text"],
                "chunk_position": chunk["position"]
            }
            collection.add(
                embeddings=[vector],
                metadata=[metadata],
                ids=[f"{i}-{j}"]
            )
    '''
    # or
    embeddings = []
    metadatas = []
    ids = []
    for i, record in enumerate(records):
        # add some testing...
        for j, (chunk, vector) in enumerate(zip(record["chunks"], record["vectors"])):
            chunk_id = f"{i}-{j}"
            metadata = {
                "filename": record["file_path"],
                "chunk_index": j,
                "chunk_text": chunk["text"],
                "chunk_position": chunk["position"]
            }
            embeddings.append(vector)
            metadatas.append(metadata)
            ids.append(chunk_id)
    collection.add(
        embeddings=embeddings,
        metadata=metadata,
        ids=ids
    )

def persist_chroma(client):
    client.persist()


def search_vectors(collection, query_vector, top_k=5):
    """Searches the collection for the `top_k` most similar vectors to the
    `query_vector`.

    Args:
    - `collection`: The Chroma collection instance
    - `query_vector`: The vector embedding to search for
    - `top_k`: tghe number of top results to return

    Returns:
    A list of search results
    """
    results = collection.query(
        query_embeddings=[query_vector],
        n_results=top_k
    )
    return results

