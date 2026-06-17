# Repository Guidelines

## Project Structure & Module Organization

This repository is a compact Python CLI for retrieval-augmented PDF question answering.

- `rag.py` contains the full application: PDF extraction, chunking, embedding, ChromaDB storage, retrieval, and OpenAI response generation.
- `README.md` documents setup and basic usage.
- `pyproject.toml`, `uv.lock`, and `requirements.txt` define dependencies.
- `sample.pdf` is a local example asset for manual testing.
- `chroma_db/` is created at runtime for the persistent vector store and should not be committed.

There is currently no dedicated `tests/` directory.

## Build, Test, and Development Commands

- `uv sync` installs the locked Python environment.
- `uv run python rag.py ingest sample.pdf` extracts, chunks, embeds, and stores the sample PDF in local ChromaDB.
- `uv run python rag.py query "What is this document about?"` retrieves relevant chunks and asks OpenAI for a grounded answer.
- `uv run python rag.py` prints command usage.

The app requires `OPENAI_API_KEY` in a local `.env` file before running queries.

## Coding Style & Naming Conventions

Use Python 3.10+ syntax and keep the current simple module layout unless the code grows enough to justify packages. Follow PEP 8 conventions: 4-space indentation, snake_case functions and variables, and UPPER_CASE constants for configuration values such as `CHUNK_SIZE` and `TOP_K`.

Prefer small, direct functions like the existing `ingest`, `retrieve`, and `generate`. Keep comments sparse and useful.

## Testing Guidelines

No automated test framework is configured yet. For changes, run a manual smoke test with `sample.pdf`:

```bash
uv run python rag.py ingest sample.pdf
uv run python rag.py query "What is this document about?"
```

If adding tests, create a `tests/` directory and prefer `pytest` with files named `test_*.py`. Mock OpenAI calls in unit tests so tests do not require network access or API credentials.

## Commit & Pull Request Guidelines

The existing history uses short imperative commit messages, for example `Add README.md`. Continue that style: `Add query tests`, `Handle empty PDF pages`, or `Document Chroma setup`.

Pull requests should include a brief description, the reason for the change, manual or automated test results, and any configuration changes. Link related issues when available. Do not include generated local data such as `.env` or `chroma_db/`.

## Security & Configuration Tips

Keep API keys in `.env` and never commit secrets. Treat ingested PDFs as local data; review privacy expectations before uploading document content to OpenAI through query context.
