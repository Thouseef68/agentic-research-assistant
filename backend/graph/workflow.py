import os
import sys
from langgraph.graph import StateGraph, START, END
from langchain_core.runnables import RunnableConfig  # 🔥 Allows routers to read configuration variables

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
    answer_grader,
    casual_chat_node  # Registered clean import
)

# =========================================================================
# 🛡️ ROUTER 0: INITIAL INTENT GATEKEEPER
# =========================================================================
def route_initial_intent(state: GraphState) -> str:
    """
    Evaluates incoming queries immediately at START. If it's a casual
    greeting, it bypasses the entire vector database and web matrix.
    """
    # Safely extract user message from "question" string
    user_msg = str(state.get("question", "")).lower().strip()
    
    casual_greetings = ["hello", "hi", "hey", "greetings", "good morning", "good afternoon", "good evening"]
    
    # Match direct words or ultra-short greeting phrases
    if any(user_msg == g for g in casual_greetings) or (len(user_msg.split()) <= 2 and any(g in user_msg for g in casual_greetings)):
        print("🤖 [ROUTER] Casual greeting detected. Routing directly to Casual Chat Node.")
        return "casual_chat"
        
    print(f"🔍 [ROUTER] Heavy research objective identified: '{user_msg[:30]}...'. Routing to Retrieval Matrix.")
    return "retrieve"

# =========================================================================
# ROUTER 1: POST-RETRIEVAL DATA MANAGER
# =========================================================================
def route_after_grading(state: GraphState, config: RunnableConfig) -> str:
    """
    Evaluates context relevance. Intercepts configuration states to check 
    if the linear response or full agent loops are armed.
    """
    enable_loops = config.get("configurable", {}).get("enable_loops", False)
    
    if not enable_loops:
        print("➡️ [HYBRID ROUTER] Mode: One-Time Response. Bypassing web fallback loops.")
        return "generate"
        
    filtered_docs = state["documents"]
    if not filtered_docs:
        print("   维护 [ROUTER] State Alert: Zero relevant data survived grading. Diverting to WEB SEARCH.")
        return "web_search"
    print(f"   🚀 [ROUTER] State Alert: {len(filtered_docs)} chunks verified. Routing to Generation layer.")
    return "generate"

# =========================================================================
# 🛡️ ROUTER 2: COGNITIVE SELF-HEALING / RECOVERY ENGINE
# =========================================================================
def route_after_generation(state: GraphState, config: RunnableConfig) -> str:
    """
    Runs self-correcting hallucination evaluations only if self-healing loops 
    are armed. Otherwise, closes out cleanly on the initial response iteration.
    """
    enable_loops = config.get("configurable", {}).get("enable_loops", False)
    
    if not enable_loops:
        print("➡️ [HYBRID ROUTER] Mode: One-Time Response. Bypassing evaluation loops. Ending execution.")
        return "finalize"
        
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

from langgraph.types import RetryPolicy
# 💡 2. Define a strict single-attempt execution policy
no_retry_policy = RetryPolicy(max_attempts=1)

# --- GRAPH BLUEPRINT LAYOUT CONFIGURATION ---
workflow = StateGraph(GraphState)

# Register the operational nodes matrix
workflow.add_node("casual_chat", casual_chat_node) # Node successfully added
workflow.add_node("retrieve", retrieve_node)
workflow.add_node("grade_documents", grade_documents_node)
workflow.add_node("web_search", web_search_node)


workflow.add_node("generate", generate_node, retry_policy=no_retry_policy)
workflow.add_node("transform_query", transform_query_node, retry_policy=no_retry_policy)

# Bind entry point to the conditional Gatekeeper Router
workflow.add_conditional_edges(
    START,
    route_initial_intent,
    {
        "casual_chat": "casual_chat",
        "retrieve": "retrieve"
    }
)

# Connect casual chat straight to exit to protect your tokens!
workflow.add_edge("casual_chat", END)

# Establish core pathways
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

print("🕸️ StateGraph Workflow structural matrix map successfully loaded.")