from sentence_transformers import SentenceTransformer

# Available models:
#
# model                            | lays | size | mem | performance | time
# ---------------------------------|-----:|-----:|----:|-------------|------
# paraphrase-MiniLM-L6-v2          |    6 |  22  | 0.3 | fastest     | ~1–1.5
# all-MiniLM-L6-v2                 |    6 |  22? | 0.3 | very fast   |
# paraphrase-distilroberta-base-v1 |    6 |  82  | 1.0 | medium      |
# paraphrase-mpnet-base-v2         |   12 | 110  | 1.3 | slowest     | ~5–7
#
# lays: architecture (all transformers) number of layers
# size: number of parameters in millions
# mem: memory usage in GB
# performance: relative performance
# time: estimated time to convert a 10,000 word (~100 chunk) doc in seconds

model = SentenceTransformer('paraphrase-mpnet-base-v2')

def chunk_text(text, chunk_size=1024, overlap=128):
    """break text into chunks. Because of the smaller context available with
    MiniLM models, 512 is about the max chunk size. 1024 is about the max
    chunk size for mpnet models. Larger chunk sizes are often but not always
    better than smaller chunk sizes.

    Overlap helps to ensure context isn't lost when an important concept
    crosses a chunk break, but downsides include adding bias, bloating the DB,
    complexity if later deduplication is required."""
    words = text.split()
    chunks = []
    position = 0
    chunk_advance = chunk_size - overlap

    for i in range(0, len(words), chunk_advance):
        chunk = " ".join(words[i:i + chunk_size])
        chunk_dict = {"text": chunk, "position": position}
        chunks.append(chunk_dict)
        position += chunk_advance

    return chunks


def vectorize_text(text):
    """Use this for just encoding a snippet of text, e.g., a query
    """
    return model.encode(text)


def vectorize_chunks(chunks):
    """use this for encoding a chunks dict
    """
    return [model.encode(chunk["text"]) for chunk in chunks]
