import math
from typing import List, Dict

def chunk_text(text: str, chunk_size_words=500, overlap_words=100):
    words = text.split()
    chunks = []
    if not words:
        return chunks
    start = 0
    total = len(words)
    chunk_id = 0
    while start < total:
        end = min(start + chunk_size_words, total)
        chunk_words = words[start:end]
        chunk_text = ' '.join(chunk_words)
        meta = {'chunk_id': chunk_id, 'start_word': start, 'end_word': end}
        chunks.append({'text': chunk_text, 'meta': meta})
        chunk_id += 1
        if end == total:
            break
        start = end - overlap_words
    return chunks
