import sys
import chromadb
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer

CHROMA_PATH = "./chroma_db"
COLLECTION_NAME = "pdf_rag"
EMBED_MODEL = "all-MiniLM-L6-v2"
OPENAI_MODEL = "gpt-4o-mini"
CHUNK_SIZE = 500
OVERLAP = 50
TOP_K = 5

_embedder = None
_collection = None


def get_embedder():
    global _embedder
    if _embedder is None:
        _embedder = SentenceTransformer(EMBED_MODEL)
    return _embedder


def get_collection():
    global _collection
    if _collection is None:
        client = chromadb.PersistentClient(path=CHROMA_PATH)
        _collection = client.get_or_create_collection(COLLECTION_NAME)
    return _collection


def chunk_text(text: str) -> list[str]:
    chunks = []
    start = 0
    while start < len(text):
        end = start + CHUNK_SIZE
        chunks.append(text[start:end])
        start += CHUNK_SIZE - OVERLAP
    return [c for c in chunks if c.strip()]


def ingest(pdf_path: str) -> None:
    reader = PdfReader(pdf_path)
    full_text = "\n".join(page.extract_text() or "" for page in reader.pages)

    chunks = chunk_text(full_text)
    embeddings = get_embedder().encode(chunks).tolist()

    get_collection().upsert(
        ids=[f"chunk_{i}" for i in range(len(chunks))],
        embeddings=embeddings,
        documents=chunks,
    )
    print(f"Ingested {len(chunks)} chunks from {pdf_path}")


def retrieve(query: str) -> list[str]:
    query_embedding = get_embedder().encode(query).tolist()
    results = get_collection().query(query_embeddings=[query_embedding], n_results=TOP_K)
    return results["documents"][0]


def generate(query: str, context_chunks: list[str]) -> str:
    context = "\n\n---\n\n".join(context_chunks)
    response = OpenAI().chat.completions.create(
        model=OPENAI_MODEL,
        max_tokens=1024,
        messages=[
            {
                "role": "system",
                "content": "Answer using only the provided context. If the answer is not in the context, say so.",
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion: {query}",
            },
        ],
    )
    return response.choices[0].message.content


def main():
    if len(sys.argv) < 3:
        print("Usage:")
        print("  python rag.py ingest <path_to_pdf>")
        print('  python rag.py query "<question>"')
        sys.exit(1)

    command = sys.argv[1]

    if command == "ingest":
        ingest(sys.argv[2])
    elif command == "query":
        chunks = retrieve(sys.argv[2])
        answer = generate(sys.argv[2], chunks)
        print(answer)
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
