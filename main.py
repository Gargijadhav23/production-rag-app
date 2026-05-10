import os
import asyncio
import nest_asyncio
nest_asyncio.apply()
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
load_dotenv()

os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY", "")

st.markdown("""
    <style>
    .stApp { background-color: #0f1117 !important; }
    section[data-testid="stSidebar"] { background-color: #1a1d27 !important; border-right: 1px solid #2e3347; }
    .stTextInput>div>div>input { background-color: #1e2130 !important; border: 1px solid #3a3f55 !important; color: #ffffff !important; border-radius: 6px !important; }
    h1 { color: #ffffff !important; font-weight: 700 !important; }
    h2, h3 { color: #4a9eff !important; }
    p, span, label, .stMarkdown { color: #c8ccd8 !important; }
    .stButton>button { background-color: #4a9eff !important; color: #ffffff !important; border-radius: 6px !important; border: none !important; font-weight: 600 !important; width: 100% !important; }
    .stButton>button:hover { background-color: #2d7dd2 !important; }
    </style>
""", unsafe_allow_html=True)

st.title("🔍 NewsBot: AI News Research Tool")
st.markdown("---")
st.sidebar.title("📰 News Article URLs")
st.sidebar.markdown("Paste up to 3 news article URLs below:")

urls = []
for i in range(3):
    url = st.sidebar.text_input(f"URL {i+1}", placeholder="https://...")
    urls.append(url)

process_url_clicked = st.sidebar.button("⚡ Process URLs")
st.sidebar.markdown("---")
st.sidebar.markdown("**How to use:**")
st.sidebar.markdown("1. Paste news article URLs")
st.sidebar.markdown("2. Click Process URLs")
st.sidebar.markdown("3. Ask your question below")

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.9, convert_system_message_to_human=True)

if process_url_clicked:
    urls_clean = [u for u in urls if u.strip()]
    if not urls_clean:
        st.error("Please enter at least one URL!")
    else:
        with st.spinner("Loading data from URLs..."):
            loader = UnstructuredURLLoader(urls=urls_clean)
            data = loader.load()
        with st.spinner("Splitting text into chunks..."):
            text_splitter = RecursiveCharacterTextSplitter(
                separators=['\n\n', '\n', '.', ','],
                chunk_size=1000
            )
            docs = text_splitter.split_documents(data)
        with st.spinner("Building vector embeddings..."):
            embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
            vectorstore = FAISS.from_documents(docs, embeddings)
            vectorstore.save_local("faiss_index")
        st.success("✅ URLs processed! Ask your question below.")

query = st.text_input("💬 Ask a question:", placeholder="e.g. What are the key highlights?")
if query:
    if os.path.exists("faiss_index"):
        with st.spinner("Thinking..."):
            embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
            vectorstore = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
            chain = RetrievalQA.from_chain_type(
                llm=llm,
                chain_type="stuff",
                retriever=vectorstore.as_retriever()
            )
            result = chain.run(query)
            st.markdown("### 📋 Answer")
            st.write(result)
    else:
        st.warning("⚠️ Please process URLs first!")