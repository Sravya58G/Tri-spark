import os
import time

def assemble_prompt(chunks, question, system_instruction=None):
    if system_instruction is None:
        system_instruction = "Answer the question using ONLY the provided context. If unknown, say you cannot find the answer."
    parts = ["---SYSTEM---", system_instruction, "---CONTEXT---"]
    for i, c in enumerate(chunks):
        parts.append(f"[{c['meta'].get('source','unknown')} | chunk {c['meta'].get('chunk_id')}]\n{c['text']}")
    parts.append("---USER---")
    parts.append(f"Question: {question}")
    parts.append("Final instruction: Keep answer concise and base it only on context.")
    return "\n\n".join(parts)

def call_watsonx(prompt, max_tokens=300, temperature=0.5):
    # Placeholder for IBM Watsonx API call. Replace with real SDK usage.
    api_key = os.getenv('IBM_API_KEY')
    if not api_key:
        raise EnvironmentError('IBM_API_KEY not set — set in .env to enable Watsonx integration.')
    # Example: Use ibm_watsonx_ai client here to call mistralai/mixtral-8x7b-instruct-v01
    # For now raise NotImplementedError to indicate placeholder.
    raise NotImplementedError('Watsonx integration is not implemented in this starter. See README for instructions.')

def local_fallback_answer(chunks, question):
    # Simple fallback that concatenates top chunks and returns a synthesized answer
    texts = "\n\n".join([c['text'] for c in chunks])
    answer = f"Based on the provided context, here are key points related to your question:\n\n"
    # naive summarization: take first 300 chars as 'summary' (placeholder)
    answer += texts[:800] + ("..." if len(texts) > 800 else "")
    sources = [f"{c['meta'].get('source','unknown')}|chunk:{c['meta'].get('chunk_id')}" for c in chunks]
    return {'answer': answer, 'sources': sources}
