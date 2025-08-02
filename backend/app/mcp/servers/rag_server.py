# app/mcp/servers/rag_server.py
"""
DEPRECATED: This file contains legacy/test code for a FAISS-based RAG server.
Do NOT use in production. All property search and retrieval should use MongoDB Atlas vector search.
"""

# --- DEPRECATED: All code below is commented out. ---
# from __future__ import annotations
# import os, pathlib, faiss, numpy as np, openai
# import tiktoken
# import uuid, json
# from dotenv import load_dotenv
# load_dotenv()           # this reads .env into the process


# ── 1. Where will we keep the index on disk? ─────────────────────────
# ROOT = pathlib.Path("data/vector_db")
# ROOT.mkdir(parents=True, exist_ok=True)
# INDEX_FILE = ROOT / "faiss.index"

# ── 2. OpenAI setup (make sure OPENAI_API_KEY is in your .env) ───────
# import openai
# openai.api_key = os.getenv("OPENAI_API_KEY")
# EMBED_MODEL = "text-embedding-3-small"   # 1536-D output

# ── 3. Load existing index or start a fresh one ──────────────────────
# DIM = 1536
# if INDEX_FILE.exists():
#     index: faiss.Index = faiss.read_index(str(INDEX_FILE))
# else:
#     index = faiss.IndexFlatL2(DIM)  # simple, no-frills index

# ── 4. Tiny helper: turn text → vector(np.ndarray[float32, (1536,)]) ─
# def embed(text: str) -> np.ndarray:
#     """Return OpenAI embedding as float32 numpy array."""
#     resp = openai.embeddings.create(model=EMBED_MODEL, input=[text])
#     vec = np.array(resp.data[0].embedding, dtype="float32")
#     return vec

# --- helper: split long text into ≈500-token chunks ------------------


# _tokenizer = tiktoken.encoding_for_model("gpt-4o-mini")
# CHUNK_TOKENS = 500

# def split_text(text: str) -> list[str]:
#     """Yield 500-token chunks (roughly) from the input text."""
#     tokens = _tokenizer.encode(text)
#     for i in range(0, len(tokens), CHUNK_TOKENS):
#         chunk_ids = tokens[i : i + CHUNK_TOKENS]
#         yield _tokenizer.decode(chunk_ids)



# META_FILE = ROOT / "meta.jsonl"

# def ingest_file(path: pathlib.Path):
#     """
#     Read a TXT / CSV / PDF (already extracted to plain text), chunk, embed,
#     and append to FAISS + meta.jsonl.
#     """
#     text = path.read_text(errors="ignore")

#     lines_to_append = []
#     vectors = []

#     for chunk in split_text(text):
#         vec = embed(chunk)
#         vectors.append(vec)
#         uid = str(uuid.uuid4())

#         lines_to_append.append(json.dumps({
#             "id": uid,
#             "file": str(path.name),
#             "text": chunk
#         }))

#     if vectors:
#         index.add(np.vstack(vectors).astype("float32"))
#         # persist index
#         faiss.write_index(index, str(INDEX_FILE))

#         # append metadata
#         with META_FILE.open("a", encoding="utf-8") as f:
#             f.write("\n".join(lines_to_append) + "\n")

# --- helper: retrieve top-k chunks ----------------------------------
# def search(query: str, *, k: int = 4) -> list[str]:
#     """
#     Return up to k chunk texts most similar to the query.
#     """
#     if index.ntotal == 0:
#         return []

#     qvec = embed(query).reshape(1, -1)
#     distances, idxs = index.search(qvec, k)

#     # meta.jsonl has one line per vector in the SAME order FAISS received them
#     meta_lines = list(META_FILE.open("r", encoding="utf-8"))
#     results = []

#     for i in idxs[0]:
#         if i == -1 or i >= len(meta_lines):
#             continue
#         text = json.loads(meta_lines[i])["text"]
#         results.append(text)

#     return results


def not_implemented():
    raise NotImplementedError("FAISS-based RAG server is deprecated. Use MongoDB Atlas vector search for all property retrieval.")

class RAGServer:
    """DEPRECATED: MCP RAG server for document retrieval and search."""
    def __init__(self):
        not_implemented()
    def search_documents(self, query: str, k: int = 4):
        not_implemented()
    def ingest_document(self, file_path: str):
        not_implemented()
    def get_stats(self):
        not_implemented() 