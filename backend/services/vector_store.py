import os
import sys
import io
import pypdf
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_core.documents import Document

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, "../.."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from backend.core.llm import embedding_model

CHROMA_DIR = os.path.abspath(os.path.join(BASE_DIR, "../../chroma_db"))

def save_and_index_uploaded_file(file_name: str, file_content: bytes, session_id: str):
    """
    Accepts raw uploaded document bytes, dynamically extracts content 
    based on extension, chunks it, and isolates it into a session index.
    """
    print(f"🚀 Processing uploaded file: {file_name} for Session: {session_id}")
    
    try:
        # 💡 New: Check extension type and extract text safely from bytes
        if file_name.lower().endswith('.pdf'):
            pdf_stream = io.BytesIO(file_content)
            reader = pypdf.PdfReader(pdf_stream)
            text_data = ""
            for page in reader.pages:
                text_data += page.extract_text() or ""
            print(f"📄 Successfully parsed PDF binary stream ({len(reader.pages)} pages extracted).")
        else:
            text_data = file_content.decode("utf-8", errors="ignore")
            print("📝 Successfully parsed standard text stream.")
            
        if not text_data.strip():
            print("⚠️ Warning: Extracted text context is completely empty.")
            return False

        raw_document = Document(
            page_content=text_data, 
            metadata={"source": file_name, "session_id": session_id}
        )
        
        # Chunking strategy
        splitter = RecursiveCharacterTextSplitter(chunk_size=700, chunk_overlap=70)
        text_chunks = splitter.split_documents([raw_document])
        
        # Save to session collection
        vector_db = Chroma.from_documents(
            documents=text_chunks,
            embedding=embedding_model,
            persist_directory=CHROMA_DIR,
            collection_name=f"session_{session_id}"
        )
        
        print(f"🎯 Successfully indexed {len(text_chunks)} chunks for this user session.")
        return True
    except Exception as e:
        print(f"❌ Failed processing document context: {e}")
        return False

# Change this at the bottom of backend/services/vector_store.py
def get_session_retriever(session_id: str):
    vector_db = Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=embedding_model,
        collection_name=f"session_{session_id}"
    )
    # 💡 Optimization: Increase k from 2 to 4 to catch distributed context chunks
    return vector_db.as_retriever(search_kwargs={"k": 4})