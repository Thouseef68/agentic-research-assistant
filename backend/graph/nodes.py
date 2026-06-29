import os
import sys
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
# Add this alongside your other langchain_core imports at the top
from langchain_core.runnables import RunnableConfig

# Ensure internal cross-folder imports resolve smoothly
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, "../.."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from backend.core.llm import llm
from backend.services.vector_store import get_session_retriever
from backend.graph.state import GraphState
# 💡 Upgraded: Import Tavily optimized search results tool
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.documents import Document

# Instantiate Tavily to gather the top 2 highly pristine text snippets
web_search_tool = TavilySearchResults(max_results=2)

# ... (Keep your existing structured_llm_grader, retrieve_node, and grade_documents_node exactly as they are) ...

def web_search_node(state: GraphState) -> dict:
    """
    NODE 4: The Intelligent Internet Fallback Operator.
    Triggers dynamically if local documents fail the grader quality audit.
    Queries Tavily and injects clean text context right into the state.
    """
    print("\n🌐 [NODE: WEB SEARCH] Local context insufficient. Querying Tavily Search API...")
    question = state["question"]
    documents = state.get("documents", [])
    
    try:
        # Execute the optimized Tavily search
        search_results = web_search_tool.invoke({"query": question})
        
        # Tavily returns a list of dictionaries with 'url' and 'content' keys
        combined_web_content = ""
        for result in search_results:
            combined_web_content += f"\n\nSource Link: {result['url']}\nContent: {result['content']}"
            
        # Wrap the parsed results inside a unified LangChain Document object block
        web_doc = Document(
            page_content=combined_web_content.strip(),
            metadata={"source": "Tavily Live Web Engine"}
        )
        
        # Append the web payload straight into our active document loop memory
        documents.append(web_doc)
        print("   ✅ Tavily internet insights successfully injected into agent state memory.")
        
    except Exception as e:
        print(f"   ❌ Tavily execution failed: {e}. Defaulting to empty fallback state.")
        
    return {"documents": documents, "question": question}

# --- 1. Define Structured Output Schema for the Document Grader ---
class GradeDocuments(BaseModel):
    """Binary score to evaluate if a retrieved document chunk is relevant to the question."""
    binary_score: str = Field(
        description="Documents are relevant to the question? 'yes' or 'no'"
    )

# Establish the structured grader instance
structured_llm_grader = llm.with_structured_output(GradeDocuments)

# --- 2. Define the Operational Graph Nodes ---

def retrieve_node(state: GraphState) -> dict:
    """
    NODE 1: Dynamic multi-user retrieval.
    Extracts the user's question and session_id from the state, 
    and queries their isolated database collection.
    """
    print("\n📥 [NODE: RETRIEVE] Accessing session-isolated vector database...")
    question = state["question"]
    session_id = state.get("session_id", "default")
    
    # Connect to this user's specific collection forklift
    retRIever = get_session_retriever(session_id)
    retrieved_docs = retRIever.invoke(question)
    
    print(f"   -> Successfully extracted {len(retrieved_docs)} potential context chunks.")
    return {"documents": retrieved_docs, "question": question}


def grade_documents_node(state: GraphState) -> dict:
    """
    NODE 2: The Quality Filter.
    Inspects every retrieved chunk. If a chunk is irrelevant, it gets dropped.
    """
    print("\n⚖️ [NODE: GRADE DOCUMENTS] Grading context relevance using Gemini...")
    question = state["question"]
    documents = state["documents"]
    
    # Prompt instructing Gemini to act as a strict binary grader
    grader_prompt = ChatPromptTemplate.from_template("""
        You are an expert auditor grading the relevance of a retrieved document chunk to a user question.
        
        RETRIVED CHUNK CONTEXT:
        {context}
        
        USER QUESTION:
        {question}
        
        Carefully evaluate if the text contains information that helps answer the question. 
        Respond strictly with a binary score: 'yes' (relevant) or 'no' (irrelevant).
    """)
    
    filtered_documents = []
    
    for doc in documents:
        # Format the prompt with the current chunk data
        formatted_prompt = grader_prompt.format(context=doc.page_content, question=question)
        score = structured_llm_grader.invoke(formatted_prompt)
        
        grade = score.binary_score.lower().strip()
        if grade == "yes":
            print("   ✅ Chunk approved: Highly relevant context.")
            filtered_documents.append(doc)
        else:
            print("   ❌ Chunk filtered out: Lacks relevant answers.")
            
    return {"documents": filtered_documents, "question": question}


# 💡 Updated: Changed to async and added config parameter
async def generate_node(state: GraphState, config: RunnableConfig) -> dict:
    """
    NODE 3: Grounded Synthesizer.
    Generates structured, perfectly padded executive reports.
    """
    print("\n🧠 [NODE: GENERATE] Synthesizing final answer report...")
    question = state["question"]
    documents = state["documents"]
    
    context_text = "\n\n".join([doc.page_content for doc in documents])
    if not context_text:
        context_text = "No relevant context documents were found in the database for this query."
        
    generation_prompt = ChatPromptTemplate.from_template("""
        You are an elite, production-grade Agentic Research Assistant.
        Synthesize a comprehensive, beautifully structured report answering the user's question based strictly on the provided context.
        
        CRITICAL MARKDOWN SPACING DIRECTIONS:
        - Every single heading (##, ###, ####) MUST be preceded and followed by exactly TWO blank newlines (\\n\\n). Never let a heading sit directly against text.
        - Every bullet point item (*) must be on its own fresh line with clean padding spacing.
        - Use bolding (**text**) effectively to highlight important structural concepts.
        - Use horizontal rules (---) cleanly with blank space breaks above and below them to split logical chapters.
        
        CONTEXT ARCHIVE:
        {context}
        
        USER QUESTION:
        {question}
        
        YOUR SYSTEMATIC DETAILED REPORT:
    """)
    
    formatted_prompt = generation_prompt.format(context=context_text, question=question)
    ai_response = await llm.ainvoke(formatted_prompt, config=config)
    
    return {"generation": ai_response.content, "documents": documents, "question": question}

# Add these imports at the very top of backend/graph/nodes.py if not present
from pydantic import BaseModel, Field

# =========================================================================
# 🛡️ HYPER-ADVANCED: STRUCTURED EVALUATOR SCHEMAS
# =========================================================================
class HallucinationSchema(BaseModel):
    """Binary score to evaluate if the generation is grounded in the retrieved context."""
    binary_score: str = Field(
        description="Is the answer grounded in the provided facts? Answer 'yes' or 'no'."
    )

class AnswerRelevanceSchema(BaseModel):
    """Binary score to evaluate if the generation fully addresses the user question."""
    binary_score: str = Field(
        description="Does the answer completely address the user's specific question? Answer 'yes' or 'no'."
    )

# Instantiate the structured output graders using GPT-4o
hallucination_grader = llm.with_structured_output(HallucinationSchema)
answer_grader = llm.with_structured_output(AnswerRelevanceSchema)

# =========================================================================
# 🛠️ NEW NODE: THE QUERY TRANSFORMER
# =========================================================================
def transform_query_node(state: GraphState) -> dict:
    """
    NODE 5: Query Optimizer / Transformer.
    Triggers if a generation hallucinates or fails answer relevance tests.
    Rewrites the prompt into a high-performance web search vector.
    """
    print("\n🔄 [NODE: TRANSFORM QUERY] Generation failed validation. Rewriting query for web optimization...")
    question = state["question"]
    documents = state.get("documents", [])
    
    rewrite_prompt = ChatPromptTemplate.from_template("""
        You are an elite search optimization engine. Your job is to analyze an initial user question 
        that failed to yield a high-quality grounded answer from local documents, and transform it 
        into an optimized, keyword-dense query specifically tailored for web search engine APIs like Tavily.
        
        CRITICAL: Do not include punctuation, search operators, or filler text. Output ONLY the optimized search keywords.
        
        INITIAL QUESTION: {question}
        OPTIMIZED WEB QUERY:
    """)
    
    # Process the transformation cleanly via GPT-4o
    optimized_query_response = llm.invoke(rewrite_prompt.format(question=question))
    optimized_query = optimized_query_response.content.strip()
    
    print(f"   👉 Optimized Target Vector Compiled: '{optimized_query}'")
    
    # Update the active question variable inside the state loop memory
    return {"question": optimized_query, "documents": documents}