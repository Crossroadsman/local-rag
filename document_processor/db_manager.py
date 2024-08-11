import os
import chromadb
from chromadb.config import Settings


def initialize_chroma():
    """Initialize the Chroma client with Faiss GPU backend for vector storage
    and search. Returns the client instance.
    """
    db_directory = os.path.join(os.getcwd(), "chroma_db")

    client = chromadb.PersistentClient(path=db_directory)
    return client


def create_collection(client, name="my_collection"):
    """Creates a new collection in Chroma. Returns the collection instance.
    """
    collection = client.create_collection(name)
    return collection


def add_vectors_to_collection(collection, vectors, metadata):
    """Adds vectors to the specified collection in Chroma along with their
    metadata.
    
    Args:
    - `collection`: The Chroma collection instance
    - `vectors`: a list of vector embeddings to be added
    - `metadata`: a list of metadata dictionaries corresponding to each vector
    """

    # A unique ID is required for each vector
    ids = [f"id_{i}" for i in range(len(vectors))]
    collection.add(ids=ids, embeddings=vectors, metadatas=metadata)


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


if __name__ == "__main__":
    # Standalone example
    client = initialize_chroma()
    collection = create_collection(client)

    # Example vectors and metadata
    vectors = [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]
    metadata = [{"id": "vector1"}, {"id": "vector2"}]

    add_vectors_to_collection(collection, vectors, metadata)

    # Perform a search
    query_vector = [0.1, 0.2, 0.6]
    results = search_vectors(collection, query_vector)

    print("Search results: ", results)
