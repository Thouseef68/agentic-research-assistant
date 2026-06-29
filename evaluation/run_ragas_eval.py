import streamlit as st
import requests
import uuid
import json

# 1. Page Configurations & Premium Layout Foundations
st.set_page_config(
    page_title="Cognitive RAG Command Console",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Advanced CSS Injection: Glassmorphism, Custom Fonts, Custom Chat Inputs, Branding Hidden
premium_css = """
<style>
    /* Import modern clean fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Inter', sans-serif;
        background-color: #0E1117;
    }
    
    /* Remove default Streamlit top header line clutter */
    header { visibility: hidden; }
    footer { visibility: hidden; }
    
    #MainMenu { visibility: hidden; }
    
    /* Glassmorphic Metric KPI Boxes */
    div[data-testid="stMetricValue"] {
        font-size: 1.8rem !important;
        font-weight: 700 !important;
        color: #00FFCC !important;
        font-family: 'JetBrains Mono', monospace;
    }
    
    div[data-testid="stMetricLabel"] {
        font-size: 0.85rem !important;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: #8A99AD !important;
    }
    
    /* Premium Sidebar Enhancements */
    section[data-testid="stSidebar"] {
        background-color: #161A22 !important;
        border-right: 1px solid #262D3D !important;
    }
    
    /* Sleek Customizing for the Chat Input Area at bottom */
    .stChatInputContainer > div {
        background-color: #1F2430 !important;
        border: 1px solid #343E56 !important;
        border-radius: 10px !important;
    }
    
    .stChatInputContainer textarea {
        color: #E2E8F0 !important;
    }
    
    /* Code Blocks Styling */
    code {
        font-family: 'JetBrains Mono', monospace !important;
        background-color: #1A1F2C !important;
        color: #FF79C6 !important;
        padding: 2px 6px !important;
        border-radius: 4px !important;
    }
    
    /* Success/Error Alerts glow properties */
    div.stAlert {
        background-color: #1A2333 !important;
        border: 1px solid #2B3B54 !important;
        border-left: 5px solid #00FFCC !important;
        border-radius: 8px !important;
    }
</style>
"""
st.markdown(premium_css, unsafe_allow_html=True)

# 3. Backend Routing Gateway URL
BACKEND_URL = "http://127.0.0.1:8000"

# 4. State Initializations
if "session_id" not in st.session_state:
    st.session_state["session_id"] = str(uuid.uuid4())[:8].upper()

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

if "document_indexed" not in st.session_state:
    st.session_state["document_indexed"] = "No Active Files"

if "last_routing_strategy" not in st.session_state:
    st.session_state["last_routing_strategy"] = "Standby"

# --- TOP HEADER PLATFORM DASHBOARD RIBBON ---
st.title("🧬 COGNITIVE AGENT RESEARCH INTERACTION HUB")
st.caption("Production Blueprint Layer: Synchronous Multi-User Token Streams & SQLite Memory Isolation")

# Premium Metric Block Layout Ribbon
m_col1, m_col2, m_col3, m_col4 = st.columns(4)
with m_col1:
    st.metric(label="Active Thread Token ID", value=f"USR-{st.session_state['session_id']}")
with m_col2:
    st.metric(label="Data Indexing Space", value=st.session_state["document_indexed"])
with m_col3:
    st.metric(label="Active Routing Logic", value=st.session_state["last_routing_strategy"])
with m_col4:
    st.metric(label="System Core Status", value="ONLINE", delta="⚡ SQLite Secure")

st.markdown("<hr style='border: 1px solid #262D3D; margin-top: 0px; margin-bottom: 25px;'>", unsafe_allow_html=True)

# --- SIDEBAR PANEL COMMAND CONTROLLER ---
with st.sidebar:
    st.markdown("<h2 style='color:#00FFCC; font-size:1.4rem; margin-bottom:5px;'>⚙️ WORKSPACE PANEL</h2>", unsafe_allow_html=True)
    st.markdown(f"**Session Identity:** `Thread_ID_{st.session_state['session_id']}`")
    st.markdown("---")
    
    st.markdown("<h3 style='font-size:1.1rem;'>📥 Knowledge Feed Layer</h3>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Feed PDF/TXT documents into session database space:", 
        type=["txt", "pdf"],
        label_visibility="collapsed"
    )
    
    if uploaded_file is not None:
        if st.button("🚀 Index Into Memory Core", use_container_width=True):
            with st.spinner("Processing document embeddings (1536-dim)..."):
                try:
                    file_bytes = uploaded_file.read()
                    files = {"file": (uploaded_file.name, file_bytes, "application/octet-stream")}
                    data = {"session_id": st.session_state["session_id"]}
                    
                    response = requests.post(f"{BACKEND_URL}/upload", files=files, data=data)
                    
                    if response.status_code == 200:
                        st.session_state["document_indexed"] = "ACTIVE CORE"
                        st.success(f"Successfully compiled: {uploaded_file.name}")
                        st.rerun()
                    else:
                        st.error("Upload process rejected by backend broker.")
                except Exception as e:
                    st.error(f"Network Connection Failed: {e}")

    st.markdown("<br><br>" * 5, unsafe_allow_html=True) # Push clear button down
    st.markdown("---")
    if st.button("🔄 Purge Thread Memory Space", use_container_width=True):
        st.session_state["session_id"] = str(uuid.uuid4())[:8].upper()
        st.session_state["chat_history"] = []
        st.session_state["document_indexed"] = "No Active Files"
        st.session_state["last_routing_strategy"] = "Standby"
        st.rerun()

# --- MAIN CHAT APPLICATION DISPLAY SPACE ---

# Render message history using premium default emojis and clean blocks
for chat in st.session_state["chat_history"]:
    avatar = "👤" if chat["role"] == "user" else "🤖"
    with st.chat_message(chat["role"], avatar=avatar):
        st.markdown(chat["message"])
        if chat.get("sources"):
            st.markdown(f"<div style='color:#8A99AD; font-size:0.85rem; margin-top:5px;'>📚 <b>Citations verified:</b> {', '.join(chat['sources'])}</div>", unsafe_allow_html=True)

# Input Box processing
if user_input := st.chat_input("Input complex inquiry or policy interrogation directives..."):
    
    st.session_state["chat_history"].append({"role": "user", "message": user_input})
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)
        
    with st.chat_message("assistant", avatar="🤖"):
        text_placeholder = st.empty()
        full_response = ""
        sources_cited = []
        
        try:
            payload = {
                "session_id": st.session_state["session_id"],
                "question": user_input
            }
            
            # Streaming reader block
            with requests.post(f"{BACKEND_URL}/research", json=payload, stream=True) as response:
                if response.status_code == 200:
                    for line in response.iter_lines():
                        if line:
                            decoded_line = line.decode("utf-8")
                            
                            if decoded_line.startswith("TOKEN:"):
                                token_content = decoded_line[len("TOKEN:"):]
                                full_response += token_content
                                text_placeholder.markdown(full_response + "█") # Sleek block cursor
                                
                            elif decoded_line.startswith("SOURCES:"):
                                json_sources = decoded_line[len("SOURCES:"):]
                                sources_cited = json.loads(json_sources)
                                
                    # Clean finalize
                    text_placeholder.markdown(full_response)
                    
                    # Intelligently deduce which route the agent chose to show on the dashboard cards
                    if "Tavily Live Web Engine" in str(sources_cited) or not sources_cited and "No relevant context" in full_response:
                        st.session_state["last_routing_strategy"] = "🌐 Tavily Search"
                    else:
                        st.session_state["last_routing_strategy"] = "💾 Isolated RAG"
                        
                    if sources_cited:
                        st.markdown(f"<div style='color:#8A99AD; font-size:0.85rem; margin-top:5px;'>📚 <b>Citations verified:</b> {', '.join(sources_cited)}</div>", unsafe_allow_html=True)
                        
                    # Commit state record histories
                    st.session_state["chat_history"].append({
                        "role": "assistant", 
                        "message": full_response,
                        "sources": sources_cited
                    })
                    st.rerun() # Refresh layout to cleanly capture upper metrics updates
                else:
                    st.error("❌ High-speed stream packet loss encountered.")
        except Exception as e:
            st.error(f"❌ Connection drop from backend orchestration core: {e}")