from typing import List, Dict
from .embeddings_index import EmbeddingsIndex

class Retriever:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.index = EmbeddingsIndex(model_name=model_name)

    def build_from_chunks(self, chunks: List[Dict]):
        texts = [c['text'] for c in chunks]
        self.index.build_index(texts)
        # keep mapping to chunks
        self.chunks = chunks

    def retrieve(self, query: str, top_k=3):
        results = self.index.query(query, top_k=top_k)
        # map back to chunks with metadata
        enriched = []
        for r in results:
            idx = r['idx']
            enriched.append({'score': r['score'], 'text': self.chunks[idx]['text'], 'meta': self.chunks[idx]['meta']})
        return enriched
