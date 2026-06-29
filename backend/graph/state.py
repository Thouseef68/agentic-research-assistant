from typing import List, TypedDict
from langchain_core.documents import Document

class GraphState(TypedDict):
    """
    Represents the operational memory state of our Agentic RAG Assistant.
    """
    question: str              # User query
    session_id: str            # Unique tracking key for multi-user isolation
    generation: str            # Final answer text output
    documents: List[Document]  # Chunks actively flowing through pipeline nodes