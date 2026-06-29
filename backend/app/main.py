import os
import sys
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import shutil
from langchain_chroma import Chroma  
import pathlib
# Add this near the top of backend/app/main.py with your other cross-imports

from backend.graph.state import GraphState
import json
from fastapi.responses import StreamingResponse
# 1. 💡 Add the new multimodal parser import at the top of backend/app/main.py
from backend.services.multimodal_parser import process_multimodal_pdf
from langchain_community.vectorstores import Chroma
from backend.core.llm import embedding_model  # Ensure your embedding model is pulled correctly
from backend.core.config import CHROMA_DIR
from backend.graph.workflow import workflow
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
# System Path Alignment: Ensure app can cross-import from backend/ services and core
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from services.vector_store import save_and_index_uploaded_file

# Initialize the FastAPI App
app = FastAPI(
    title="Agentic RAG Research Assistant API",
    description="Production multi-user session-isolated cognitive architecture gateway."
)

# Enable CORS so your frontend server can securely talk to this backend server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, lock this down to your specific frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the structured data schema for user questions
class ResearchRequest(BaseModel):
    session_id: str
    question: str

DB_PATH = os.path.abspath(os.path.join(PROJECT_ROOT, "checkpoints.sqlite"))

@app.get("/")
def read_root():
    return {"status": "online", "message": "Agentic Research Assistant Gateway is active."}

@app.post("/upload")
async def upload_knowledge_document(file: UploadFile = File(...), session_id: str = Form(...)):
    print(f"\n📥 [API UPLOAD ENTRY] Receiving document vector payload for session thread: {session_id}")
    session_upload_dir = os.path.join(os.getcwd(), "data", f"upload_{session_id}")
    os.makedirs(session_upload_dir, exist_ok=True)
    file_path = os.path.join(session_upload_dir, file.filename)
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        parsed_documents = process_multimodal_pdf(file_path)
        if not parsed_documents:
            return {"status": "error", "message": "Layout processing generated empty structure maps."}
            
        print(f"   💾 Committing {len(parsed_documents)} layout-aware chunks to Chroma DB space...")
        
        # 💡 WINDOWS FIX: Wrap CHROMA_DIR in str() to prevent C++ binding type errors
        vector_db = Chroma(
            persist_directory=str(CHROMA_DIR),
            embedding_function=embedding_model,
            collection_name=f"session_{session_id}"
        )
        
        vector_db.add_documents(parsed_documents)
        print("   ✅ Vector embedding synchronization successfully indexed to disk storage.")
        
        os.remove(file_path)
        os.rmdir(session_upload_dir)
        return {"status": "success", "message": f"Successfully indexed multi-modal architecture layers for {file.filename}."}
        
    except Exception as e:
        print(f"   ❌ Ingestion lifecycle failure encountered: {e}")
        if os.path.exists(file_path):
            os.remove(file_path)
        return {"status": "error", "message": f"Internal parser initialization failure: {str(e)}"}


@app.post("/research")
async def run_agent_research(request: ResearchRequest):
    print(f"\n🤖 [API STREAM ENTRY] Initializing Stream Event Stream for Session: {request.session_id}")

    async def stream_generator():
        initial_inputs = {
            "question": request.question,
            "session_id": request.session_id,
            "documents": []
        }
        
        agent_config = {
            "configurable": {
                "thread_id": request.session_id
            }
        }
        
        # 💡 SOLUTION: Open the Asynchronous Checkpointer context safely inside the stream lifecycle block!
        async with AsyncSqliteSaver.from_conn_string(DB_PATH) as checkpointer:
            # Setup database tables if they do not already exist
            await checkpointer.setup()
            
            # Compile the raw StateGraph blueprint right inside the open connection scope
            local_compiled_graph = workflow.compile(checkpointer=checkpointer)
            
            # Stream the graph events over the connection stream
            async for event in local_compiled_graph.astream_events(initial_inputs, config=agent_config, version="v2"):
                kind = event.get("event")
                
                if kind == "on_chat_model_stream":
                    chunk = event["data"].get("chunk")
                    if chunk and chunk.content:
                        yield f"TOKEN:{chunk.content}\n"
                
                elif kind == "on_node_end" and event.get("name") == "grade_documents":
                    output = event["data"].get("output", {})
                    docs = output.get("documents", [])
                    citations = list(set([doc.metadata.get("source", "Unknown Document") for doc in docs]))
                    yield f"SOURCES:{json.dumps(citations)}\n"

    return StreamingResponse(stream_generator(), media_type="text/plain")