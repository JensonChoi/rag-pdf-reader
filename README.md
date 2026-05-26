# rag-pdf-reader

CLI RAG tool: ingest a PDF into a local ChromaDB, then ask questions answered by OpenAI grounded on retrieved chunks.

## Stack

- `pypdf` — PDF text extraction
- `sentence-transformers` (`all-MiniLM-L6-v2`) — local embeddings
- `chromadb` — local persistent vector store (`./chroma_db`)
- `openai` (`gpt-4o-mini`) — answer generation

## Setup

Requires Python ≥3.10 and [uv](https://docs.astral.sh/uv/).

```bash
uv sync
```

Create `.env` with your OpenAI key:

```
OPENAI_API_KEY=sk-...
```

## Usage

Ingest a PDF (chunks + embeds + stores):

```bash
uv run python rag.py ingest path/to/file.pdf
```

Query:

```bash
uv run python rag.py query "your question"
```

First ingest is slow — downloads the embedding model (~90MB) on first run. Cached afterward.

## Config

Tunables at the top of `rag.py`: `CHUNK_SIZE`, `OVERLAP`, `TOP_K`, `EMBED_MODEL`, `OPENAI_MODEL`.
