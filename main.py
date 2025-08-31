import time
import streamlit as st

from app.ui import pdf_upload
from app.pdf_utils import extract_text_from_pdf
from app.vectorstore_utils import create_faiss_index, retrive_relevant_docs
from app.chat_utils import get_chat_model, ask_chat_model
from app.config import EURI_API_KEY
from langchain.text_splitter import RecursiveCharacterTextSplitter

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="MediChat Pro - Medical Document Assistant",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------- CUSTOM CSS --------------------
st.markdown("""
<style>
    .chat-message { padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex; flex-direction: column; }
    .chat-message.user { background-color: #2b313e; color: white; }
    .chat-message.assistant { background-color: #f0f2f6; color: black; }
    .chat-message .timestamp { font-size: 0.8rem; opacity: 0.7; margin-top: 0.5rem; }
    .stButton > button { background-color: #ff4b4b; color: white; border-radius: 0.5rem; border: none; padding: 0.5rem 1rem; font-weight: bold; }
    .stButton > button:hover { background-color: #ff3333; }
    .upload-section { background-color: #f8f9fa; padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem; }
</style>
""", unsafe_allow_html=True)

# -------------------- SESSION STATE --------------------
if "messages" not in st.session_state:
    st.session_state.messages = []
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None
if "chat_model" not in st.session_state:
    st.session_state.chat_model = None

# -------------------- HEADER --------------------
st.markdown("""
<div style="text-align: center; padding: 2rem 0;">
    <h1 style="color: #ff4b4b; font-size: 3rem; margin-bottom: 0.5rem;">🏥 MediChat Pro</h1>
    <p style="font-size: 1.2rem; color: #666; margin-bottom: 2rem;">Your Intelligent Medical Document Assistant</p>
</div>
""", unsafe_allow_html=True)

# -------------------- SIDEBAR: UPLOAD + PROCESS --------------------
with st.sidebar:
    st.markdown("### 📁 Document Upload")
    st.markdown("Upload your medical documents to start chatting!")

    uploaded_files = pdf_upload()

    if uploaded_files:
        st.success(f"📄 {len(uploaded_files)} document(s) uploaded")

        if st.button("🚀 Process Documents", type="primary"):
            with st.spinner("Processing your medical documents..."):
                # 1) Extract text
                all_texts = []
                for f in uploaded_files:
                    text = extract_text_from_pdf(f)
                    if text.strip():
                        all_texts.append(text)
                    else:
                        st.warning(f"⚠️ No text extracted from: {getattr(f, 'name', 'PDF')}")

                if not all_texts:
                    st.error("❌ Could not extract text from any file. Are they scanned/image-only PDFs?")
                else:
                    # 2) Chunk text
                    splitter = RecursiveCharacterTextSplitter(
                        chunk_size=1000,
                        chunk_overlap=200,
                        length_function=len
                    )
                    chunks = []
                    for t in all_texts:
                        chunks.extend(splitter.split_text(t))

                    if not chunks:
                        st.error("❌ No chunks produced from the extracted text.")
                    else:
                        # 3) Build FAISS
                        try:
                            st.session_state.vectorstore = create_faiss_index(chunks)
                        except Exception as e:
                            st.error(f"❌ Error creating FAISS index: {e}")
                            st.stop()

                        # 4) Init Chat Model
                        if not EURI_API_KEY:
                            st.warning("ℹ️ EURI_API_KEY not set. Add it to .streamlit/secrets.toml or app/config.py.")
                        try:
                            st.session_state.chat_model = get_chat_model(EURI_API_KEY)
                        except Exception as e:
                            st.error(f"❌ Error initializing chat model: {e}")
                            st.stop()

                        st.success("✅ Documents processed successfully!")
                        st.balloons()

# -------------------- CHAT UI --------------------
st.markdown("### 💬 Chat with Your Medical Documents")

# Show previous messages
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])
        st.caption(m["timestamp"])

# Input
prompt = st.chat_input("Ask about your medical documents...")
if prompt:
    timestamp = time.strftime("%H:%M")

    # Save + show user message
    st.session_state.messages.append({"role": "user", "content": prompt, "timestamp": timestamp})
    with st.chat_message("user"):
        st.markdown(prompt)
        st.caption(timestamp)

    # Generate response
    if st.session_state.vectorstore and st.session_state.chat_model:
        with st.chat_message("assistant"):
            with st.spinner("🔍 Searching documents..."):
                # Retrieve relevant chunks
                relevant_docs = retrive_relevant_docs(st.session_state.vectorstore, prompt, k=3)
                context = "\n\n".join([d.page_content for d in relevant_docs])

                system_prompt = f"""
You are MediChat Pro, an intelligent medical document assistant.
Based on the following medical documents, provide accurate and helpful answers.
If the information is not in the documents, clearly state that.
When answering, combine insights from the documents with careful medical reasoning.

Medical Documents:
{context}

User Question: {prompt}

Answer:
""".strip()

                try:
                    response_text = ask_chat_model(st.session_state.chat_model, system_prompt)
                except Exception as e:
                    response_text = f"Error from LLM: {e}"

            st.markdown(response_text)
            st.caption(timestamp)

            st.session_state.messages.append({"role": "assistant", "content": response_text, "timestamp": timestamp})
    else:
        with st.chat_message("assistant"):
            st.error("⚠️ Please upload and process documents first!")
            st.caption(timestamp)

# activate environment: conda activate medicalchatbot
# run streamlit file: streamlit run main.py  




