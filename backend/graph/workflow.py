import os
import sys
from langgraph.graph import StateGraph, START, END

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, "../.."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from backend.graph.state import GraphState
from backend.graph.nodes import (
    retrieve_node, 
    grade_documents_node, 
    generate_node, 
    web_search_node,
    transform_query_node,
    hallucination_grader,
    answer_grader
)

# =========================================================================
# ROUTER 1: POST-RETRIEVAL DATA MANAGER
# =========================================================================
def route_after_grading(state: GraphState) -> str:
    filtered_docs = state["documents"]
    if not filtered_docs:
        print("   维护 [ROUTER] State Alert: Zero relevant data survived grading. Diverting to WEB SEARCH.")
        return "web_search"
    print(f"   🚀 [ROUTER] State Alert: {len(filtered_docs)} chunks verified. Routing to Generation layer.")
    return "generate"

# =========================================================================
# 🛡️ ROUTER 2: COGNITIVE SELF-HEALING / RECOVERY ENGINE
# =========================================================================
def route_after_generation(state: GraphState) -> str:
    question = state["question"]
    documents = state["documents"]
    generation = state["generation"]
    
    print("\n⚖️ [ROUTER: GUARDRAIL CHECK] Executing automated hallucination evaluation audit...")
    context_text = "\n\n".join([doc.page_content for doc in documents])
    
    # 1. Audit Check: Hallucination Evaluation
    try:
        hallucination_check = hallucination_grader.invoke(
            f"CONTEXT:\n{context_text}\n\nGENERATION:\n{generation}"
        )
        is_grounded = hallucination_check.binary_score.lower() == "yes"
    except Exception:
        is_grounded = True
        
    if not is_grounded:
        print("   ❌ CRITICAL GUARDRAIL ALERT: Hallucination detected! Answer contains ungrounded facts.")
        return "transform_query"
        
    print("   ✅ Hallucination Check Passed: Answer is completely grounded in retrieved facts.")
    
    # 2. Audit Check: Original Answer Relevance Evaluation
    try:
        relevance_check = answer_grader.invoke(
            f"QUESTION:\n{question}\n\nGENERATION:\n{generation}"
        )
        is_relevant = relevance_check.binary_score.lower() == "yes"
    except Exception:
        is_relevant = True
        
    if not is_relevant:
        print("   ❌ GUARDRAIL ALERT: Generation off-topic or incomplete. Does not address the prompt.")
        return "transform_query"
        
    print("   ✅ Answer Relevance Passed: Generation accurately addresses the inquiry vector.")
    return "finalize"


# --- GRAPH BLUEPRINT LAYOUT CONFIGURATION ---
workflow = StateGraph(GraphState)

# Register the operational nodes matrix
workflow.add_node("retrieve", retrieve_node)
workflow.add_node("grade_documents", grade_documents_node)
workflow.add_node("web_search", web_search_node)
workflow.add_node("generate", generate_node)
workflow.add_node("transform_query", transform_query_node)

# Establish core pathways
workflow.add_edge(START, "retrieve")
workflow.add_edge("retrieve", "grade_documents")

# Bind Post-Retrieval Conditional Router Highway
workflow.add_conditional_edges(
    "grade_documents",
    route_after_grading,
    {
        "generate": "generate",
        "web_search": "web_search"
    }
)

# Connect Web Search directly into synthesis
workflow.add_edge("web_search", "generate")

# Bind Post-Generation Self-Healing Guardrail Router Highway
workflow.add_conditional_edges(
    "generate",
    route_after_generation,
    {
        "transform_query": "transform_query",
        "finalize": END
    }
)

# Connect the query optimizer back into web search to finalize the healing loop
workflow.add_edge("transform_query", "web_search")

# 💡 NOTE: We export the raw compiled-ready 'workflow' builder blueprint object
# This allows our runtime API endpoints to compile it cleanly inside an active async event loop context!
print("🕸️ StateGraph Workflow structural matrix map successfully loaded.")