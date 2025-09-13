import os
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
from typing import List, Dict, Any

class EmbeddingsIndex:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.model_name = model_name
        self.model = None
        self.index = None
        self.meta = []

    def load_model(self):
        if self.model is None:
            self.model = SentenceTransformer(self.model_name)

    def build_index(self, texts: List[str]):
        # texts: list of chunk strings
        self.load_model()
        embeddings = self.model.encode(texts, show_progress_bar=True, convert_to_numpy=True)
        d = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(d)
        self.index.add(embeddings)
        self.meta = [{'text': t} for t in texts]
        return embeddings

    def query(self, query_text: str, top_k=3):
        self.load_model()
        q_emb = self.model.encode([query_text], convert_to_numpy=True)
        if self.index is None or self.index.ntotal == 0:
            return []
        D, I = self.index.search(q_emb, top_k)
        results = []
        for dist, idx in zip(D[0], I[0]):
            results.append({'score': float(dist), 'idx': int(idx), 'text': self.meta[idx]['text']})
        return results
