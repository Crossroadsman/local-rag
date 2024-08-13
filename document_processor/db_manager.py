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

    embeddings = []
    metadatas = []
    ids = []
    for i, record in enumerate(records):
        for j, (chunk, vector) in enumerate(zip(record["chunks"], record["vectors"])):
            chunk_id = f"{i}-{j}"
            metadata = {
                "filename": record["file_path"],
                "chunk_index": j,
                "chunk_text": chunk["text"],
                "chunk_position": chunk["position"]
            }
            embeddings.append(vector.tolist())  # convert numpy ndarray to python list
            metadatas.append(metadata)
            ids.append(chunk_id)
    collection.add(
        embeddings=embeddings,
        metadatas=metadatas,
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


def nice_results(results):
    """flattens and reformats the search results
    - flattens in the sense that the results dict has nested lists, the outer
      list represents each embedding, the inner list represents each result
      for that embedding. Usually we only have one embedding, so we just want
      the results
    """
    nice_results = []
    for i in range(len(results["ids"])):
        for j in range(len(results["ids"][i])):
            doc_id, chunk_id = results["ids"][i][j].split('-')
            distance = results["distances"][i][j]
            metadata = results["metadatas"][i][j]
            dict = {
                "doc_id": doc_id,
                "chunk_id": chunk_id,
                "distance": distance,
                "text": metadata["chunk_text"],
                "position": metadata["chunk_position"]
            }
            nice_results.append(dict)
    return nice_results
