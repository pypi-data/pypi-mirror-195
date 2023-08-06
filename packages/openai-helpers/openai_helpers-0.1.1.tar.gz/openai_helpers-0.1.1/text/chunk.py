from itertools import islice
import tiktoken

def batched(iterable, n):
    """Batch data into tuples of length n. The last batch may be shorter."""
    # batched('ABCDEFG', 3) --> ABC DEF G
    if n < 1:
        raise ValueError('n must be at least one')
    it = iter(iterable)
    while batch := tuple(islice(it, n)):
        yield batch

def chunked_tokens(text, encoding_name, chunk_length):
    """
    Split the text into chunks of specified length and tokenize them using the provided encoding.

    Parameters:
    text (str): The input text to be chunked.
    encoding_name (str): The name of the encoding to use for tokenization.
    chunk_length (int): The desired length of each chunk.

    Yields:
    list: A list of tokens from a single chunk.

    This function tokenizes the input text based on the specified encoding. It then splits the text into chunks of specified length 
    and yields these chunks one by one. Each chunk is represented as a list that contains tokens of that chunk length.
    """
    encoding = tiktoken.get_encoding(encoding_name)
    tokens = encoding.encode(text)
    chunks_iterator = batched(tokens, chunk_length)
    yield from chunks_iterator