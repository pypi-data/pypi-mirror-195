# openai_helpers

`openai_helpers` is a Python package that provides helper functions for working with OpenAI's machine learning APIs, specifically the Embedding API. The package contains two modules: `text/chunk.py` and `embeddings/embeddings.py`.

Installation
You can install `openai_helpers` using pip:

```
pip install openai_helpers
```

Alternatively, you can install the package directly from the source code by following these steps:

Clone the repository:

```
git clone git@github.com:et0x/openai_helpers.git
```

Change to the `openai_helpers` directory:

```
cd openai_helpers
```

Create a virtual environment:

```
python -m venv env
```

Activate the virtual environment:

```
source env/bin/activate
```

Install the package in editable mode:

```
pip install -e .
```

Usage
The `openai_helpers` package provides functions for generating embeddings for text using OpenAI's Embedding API. Here is an example usage:

```python
from openai_helpers.embeddings import len_safe_get_embedding

text = "Hello, world!"
embedding = len_safe_get_embedding(text)
print(embedding)
```

This will output a list of floats representing the embedding of the input text.

Modules
`text/chunk.py`
The `text/chunk.py` module provides a function for chunking a long text into smaller pieces, each represented as a list of tokens. This function can be useful for processing long texts that are too large to be processed in a single request to OpenAI's API.

`embeddings/embeddings.py`
The `embeddings/embeddings.py` module provides functions for generating embeddings for text using OpenAI's Embedding API.

`get_embedding`
This function generates an embedding for a given text or tokens using OpenAI's Embedding API. Here's an example usage:

```python
from openai_helpers.embeddings import get_embedding

text = "Hello, world!"
embedding = get_embedding(text)
print(embedding)
```

This will output a list of floats representing the embedding of the input text.

`len_safe_get_embedding`
This function generates embeddings for a text in a safe way by chunking it into smaller pieces and calling `get_embedding` on each chunk. This function can handle long texts that may exceed the limits of OpenAI's API. Here's an example usage:

```python
from openai_helpers.embeddings import len_safe_get_embedding

text = "Hello, world!"
embedding = len_safe_get_embedding(text)
print(embedding)
```

This will output a list of floats representing the embedding of the input text.