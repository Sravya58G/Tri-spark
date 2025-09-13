import streamlit as st
from studymate.pdf_parser import extract_text_from_pdf
from studymate.chunker import chunk_text
from studymate.retriever import Retriever
from studymate.llm_client import assemble_prompt, call_watsonx, local_fallback_answer
from studymate.session_store import SessionStore
from studymate.utils import save_uploaded_file
import os

st.set_page_config(page_title='StudyMate — PDF Q&A', layout='wide')

if 'store' not in st.session_state:
    st.session_state['store'] = SessionStore()

st.title('StudyMate — AI PDF Q&A')
st.markdown('Upload PDFs and ask questions grounded in your documents.')

with st.sidebar:
    st.header('Configuration')
    chunk_size = st.number_input('Chunk size (words)', value=500, step=100)
    overlap = st.number_input('Overlap (words)', value=100, step=50)
    top_k = st.number_input('Top-k retrieval', value=3, min_value=1, max_value=10)
    provider = st.selectbox('Model provider (demo)', ['local_fallback', 'watsonx'])

uploaded = st.file_uploader('Upload one or more PDFs', type=['pdf'], accept_multiple_files=True)
process_btn = st.button('Process PDFs')

if 'chunks' not in st.session_state:
    st.session_state['chunks'] = []
    st.session_state['retriever'] = None

if process_btn and uploaded:
    st.info('Processing PDFs — extracting text and chunking...')
    all_chunks = []
    for f in uploaded:
        path = save_uploaded_file(f, target_dir='uploads')
        text = extract_text_from_pdf(path)
        chunks = chunk_text(text, chunk_size_words=chunk_size, overlap_words=overlap)
        # annotate
        for c in chunks:
            c['meta']['source'] = f.name
        all_chunks.extend(chunks)
    st.session_state['chunks'] = all_chunks
    retr = Retriever()
    retr.build_from_chunks(all_chunks)
    st.session_state['retriever'] = retr
    st.success(f'Processed {len(all_chunks)} chunks from {len(uploaded)} files.')

st.markdown('---')

query = st.text_area('Ask a question about the uploaded PDFs', height=120)
if st.button('Ask') and query.strip():
    if not st.session_state.get('retriever'):
        st.warning('No documents processed. Upload and process PDFs first.')
    else:
        with st.spinner('Retrieving relevant context...'):
            retr = st.session_state['retriever']
            top_chunks = retr.retrieve(query, top_k=top_k)
        st.subheader('Answer')
        system_instruction = "Answer using ONLY the provided context. If unsure, state that the answer isn't present."
        prompt = assemble_prompt(top_chunks, query, system_instruction=system_instruction)
        # call chosen provider
        if provider == 'watsonx':
            try:
                resp = call_watsonx(prompt)
                answer_text = resp.get('text', str(resp))
                sources = [f"{c['meta'].get('source')}|chunk:{c['meta'].get('chunk_id')}" for c in top_chunks]
            except Exception as e:
                st.error(f'Watsonx call failed: {e} — using local fallback.')
                fallback = local_fallback_answer(top_chunks, query)
                answer_text = fallback['answer']
                sources = fallback['sources']
        else:
            fallback = local_fallback_answer(top_chunks, query)
            answer_text = fallback['answer']
            sources = fallback['sources']

        st.markdown(answer_text)
        with st.expander('Referenced paragraphs (from retrieved chunks)'):
            for c in top_chunks:
                st.markdown(f"**{c['meta'].get('source')} — chunk {c['meta'].get('chunk_id')}**\n\n{c['text']}")


        # store session
        st.session_state['store'].add(query, answer_text, sources)

st.markdown('---')
st.subheader('Q&A History')
if st.session_state['store'].history:
    for i, e in enumerate(reversed(st.session_state['store'].history), 1):
        st.markdown(f"**Q:** {e['question']}  \n**A:** {e['answer']}  \n*Sources:* {', '.join(e['sources'])}")


if st.button('Download Q&A History'):
    txt = st.session_state['store'].export_txt()
    st.download_button('Download transcript (txt)', txt, file_name='studymate_transcript.txt', mime='text/plain')
