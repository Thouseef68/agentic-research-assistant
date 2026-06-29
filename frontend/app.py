import streamlit as st
import requests
import uuid
import json

# 1. High-Fidelity Page Foundation & Setup
st.set_page_config(
    page_title="Cognitive RAG Control Center",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Advanced Premium CSS Injection (Glassmorphism & Liquid Glow Architecture)
premium_ui_css = """
<style>
    /* Global Inter and Coding Monospace Typeface Injections */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background: radial-gradient(circle at 50% 0%, #131722 0%, #090B10 100%) !important;
        color: #F1F5F9 !important;
    }
    
    /* Neutralize & Hide Default Streamlit Branding Elements */
    header, footer, #MainMenu { visibility: hidden !important; height: 0 !important; }
    
    /* Premium Frosted Glass Sidebar Implementation */
    section[data-testid="stSidebar"] {
        background: rgba(22, 28, 45, 0.45) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
    }
    /* 💡 Paste this updated layout block inside premium_ui_css in frontend/app.py */
    div[data-testid="stChatMessageContent"] p {
        font-size: 0.95rem !important;
        line-height: 1.65 !important;
        color: #E2E8F0 !important;
        margin-top: 0px !important;
        margin-bottom: 14px !important; /* Forces breathing room after every paragraph */
    }
    
    /* Strict padding isolation rules for streamed headers */
    div[data-testid="stChatMessageContent"] h1,
    div[data-testid="stChatMessageContent"] h2,
    div[data-testid="stChatMessageContent"] h3,
    div[data-testid="stChatMessageContent"] h4 {
        color: #00FFCC !important;
        font-weight: 600 !important;
        margin-top: 24px !important;    /* Pushes text above away from the header */
        margin-bottom: 12px !important; /* Pushes content below away from the header */
        display: block !important;
    }
    
    div[data-testid="stChatMessageContent"] ul {
        margin-bottom: 16px !important;
        padding-left: 20px !important;
    }
    
    div[data-testid="stChatMessageContent"] li {
        margin-bottom: 6px !important;
        line-height: 1.6 !important;
    }
    
    div[data-testid="stChatMessageContent"] hr {
        border-color: rgba(255, 255, 255, 0.08) !important;
        margin-top: 20px !important;
        margin-bottom: 20px !important;
    }
    
    /* Top Telemetry Metric Blocks: Liquid Glow Accent Framework */
    div[data-testid="stMetricContainer"] {
        background: rgba(30, 41, 59, 0.3) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 12px !important;
        padding: 16px 20px !important;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.2);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    /* Decorative Gradient "Liquid Border" Accent Effect */
    div[data-testid="stMetricContainer"]::before {
        content: "";
        position: absolute;
        top: 0; left: 0; width: 4px; height: 100%;
        background: linear-gradient(180deg, #00FFCC 0%, #7928CA 100%);
    }

    div[data-testid="stMetricContainer"]:hover {
        transform: translateY(-2px);
        border-color: rgba(0, 255, 204, 0.3) !important;
        box-shadow: 0 8px 30px rgba(0, 255, 204, 0.05);
    }
    
    div[data-testid="stMetricValue"] {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 1.6rem !important;
        font-weight: 600 !important;
        color: #00FFCC !important;
        letter-spacing: -0.02em;
    }
    
    div[data-testid="stMetricLabel"] {
        font-size: 0.75rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.12em !important;
        color: #94A3B8 !important;
        margin-bottom: 4px !important;
    }
    
    /* Chat Input Bar Floating Glass Layout Customization */
    .stChatInputContainer {
        padding-bottom: 20px !important;
        background-color: transparent !important;
    }
    
    .stChatInputContainer > div {
        background: rgba(30, 41, 59, 0.6) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 14px !important;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3) !important;
    }
    
    /* Advanced Message Bubble Component Formatting */
    div[data-testid="stChatMessage"] {
        background-color: transparent !important;
        padding: 20px 0px !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.03) !important;
    }
    
    /* Clean formatting for embedded technical code strings */
    code {
        font-family: 'JetBrains Mono', monospace !important;
        background: rgba(244, 63, 94, 0.1) !important;
        color: #FB7185 !important;
        padding: 3px 6px !important;
        border-radius: 6px !important;
        font-size: 0.9em !important;
    }
    
    /* Onboarding Rich Text Block Adjustments */
    .onboarding-card {
        background: rgba(255, 255, 255, 0.02) !important;
        border: 1px solid rgba(255, 255, 255, 0.04) !important;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
    }
    
    /* Buttons Customization Core Override */
    button[kind="primary"], button[kind="secondary"] {
        background: linear-gradient(90deg, rgba(0,255,204,0.15) 0%, rgba(121,40,202,0.15) 100%) !important;
        border: 1px solid rgba(0, 255, 204, 0.4) !important;
        color: #00FFCC !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
        transition: all 0.25s ease !important;
    }
    
    button:hover {
        background: linear-gradient(90deg, rgba(0,255,204,0.25) 0%, rgba(121,40,202,0.25) 100%) !important;
        box-shadow: 0 0 15px rgba(0, 255, 204, 0.2) !important;
        border-color: #00FFCC !important;
    }
</style>
"""
st.markdown(premium_ui_css, unsafe_allow_html=True)

# 3. Dynamic API Configuration Link
BACKEND_URL = "http://127.0.0.1:8000"

# 4. Global State Tracking Architecture
if "session_id" not in st.session_state:
    st.session_state["session_id"] = str(uuid.uuid4())[:8].upper()

if "document_indexed" not in st.session_state:
    st.session_state["document_indexed"] = "STANDBY"

if "last_routing_strategy" not in st.session_state:
    st.session_state["last_routing_strategy"] = "INITIALIZED"

# 💡 UPGRADED: Initialize the history with a comprehensive onboarding introduction
if "chat_history" not in st.session_state:
    introduction_payload = """### 🧬 Welcome to the Cognitive Research Command Center!
    
I am your **Autonomous Agentic RAG Assistant**, engineered to bridge the gap between complex engineering corpora and instant, data-verified intelligence. 

<div class="onboarding-card">
<h4>🚀 What I Do</h4>
<ul>
    <li><b>Session-Isolated Vector Storage:</b> Once you upload documents, I embed them into a localized chunking database utilizing 1536-dimensional vectors.</li>
    <li><b>Self-Planning Evaluation Loop:</b> I autonomously audit document context relevance. If files are missing facts, I execute an automatic fallback route to query the live internet via <b>Tavily Search API</b>.</li>
    <li><b>Network Token Streaming:</b> Responses bypass blocking latency and animate onto your screen token-by-token in real time.</li>
</ul>
</div>

<div class="onboarding-card">
<h4>👥 Who Can Use This?</h4>
<ul>
    <li><b>Research Scholars & Academics:</b> Rapidly isolate math equations, performance thresholds, and data plots across complex scientific manuscripts.</li>
    <li><b>Software Engineers & Systems Architects:</b> Interrogate dense documentation maps and system requirements with structural multi-turn context persistence.</li>
</ul>
</div>

<div class="onboarding-card">
<h4>🎨 Advanced UI/UX Implementation Layer</h4>
Inspired by elite dark-mode infrastructure blueprints (modeled closely alongside components seen in <code>image_ae8960.png</code>), this frontend utilizes an explicit <b>Glassmorphism Design System</b>:
<ul>
    <li><b>Frosted Layout Blur:</b> Side-navigation boundaries run 20px blur filters to maintain depth over a dynamic background gradient.</li>
    <li><b>Fluid Neon Accents:</b> Core telemetry cards feature multi-gradient glowing dividers to make tracking KPIs completely intuitive.</li>
    <li><b>Real-Time Tracking:</b> The metric ribbon monitors whether my current active routing logic is reading from disk data or browsing the open web.</li>
</ul>
</div>

*Please upload your target reference documentation files in the control station sidebar, or transmit an initial exploration directive below to begin.*"""

    st.session_state["chat_history"] = [{
        "role": "assistant",
        "message": introduction_payload,
        "sources": []
    }]


# --- TOP PLATFORM CONTROL BANNER PANEL ---
st.markdown("<h1 style='font-size:1.8rem; font-weight:700; letter-spacing:-0.03em; margin-bottom:5px; background: linear-gradient(90deg, #00FFCC, #7928CA); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>🧬 COGNITIVE OPERATIONS RESEARCH NODE</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#64748B; font-size:0.85rem; margin-top:0px; margin-bottom:20px; text-transform: uppercase; letter-spacing:0.08em;'>Production Blueprint Stack: Stream-Linked LangGraph Memory Threading Engine</p>", unsafe_allow_html=True)

# Generate high-fidelity top dashboard ribbon cards
col_a, col_b, col_c, col_d = st.columns(4)
with col_a:
    st.metric(label="Active Thread Track", value=f"TH-{st.session_state['session_id']}")
with col_b:
    st.metric(label="Core Knowledge Base", value=st.session_state["document_indexed"])
with col_c:
    st.metric(label="Last Graph Route Decision", value=st.session_state["last_routing_strategy"])
with col_d:
    st.metric(label="Operational Layer Lock", value="ACTIVE", delta="⚡ SQLite Preserved")

st.markdown("<div style='margin-top:25px; margin-bottom:25px; height:1px; background:linear-gradient(90deg, rgba(255,255,255,0.05), transparent);'></div>", unsafe_allow_html=True)

# --- SIDEBAR INTERFACE CONTROL SYSTEM ---
with st.sidebar:
    st.markdown("<h2 style='color:#00FFCC; font-size:1.2rem; font-weight:600; letter-spacing:-0.01em; margin-bottom:15px;'>⚙️ CONTROL STATION</h2>", unsafe_allow_html=True)
    st.markdown(f"**Security Context Identifier:** `Thread_Hash_{st.session_state['session_id']}`")
    st.markdown("<div style='margin-top:15px; margin-bottom:20px; height:1px; background:rgba(255,255,255,0.06);'></div>", unsafe_allow_html=True)
    
    st.markdown("<p style='font-size:0.8rem; font-weight:600; color:#94A3B8; text-transform:uppercase; letter-spacing:0.05em; margin-bottom:10px;'>Index Corporate Corpus</p>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Upload contextual documentation layers:", 
        type=["txt", "pdf"],
        label_visibility="collapsed"
    )
    
    if uploaded_file is not None:
        if st.button("🚀 Push Matrix Layer", use_container_width=True):
            with st.spinner("Extracting parameters & generating 1536-dim tensor embeddings..."):
                try:
                    file_bytes = uploaded_file.read()
                    files = {"file": (uploaded_file.name, file_bytes, "application/octet-stream")}
                    data = {"session_id": st.session_state["session_id"]}
                    
                    st.session_state["document_indexed"] = "PROCESSING..."
                    response = requests.post(f"{BACKEND_URL}/upload", files=files, data=data)
                    
                    if response.status_code == 200:
                        st.session_state["document_indexed"] = "CONNECTED"
                        st.sidebar.success(f"Successfully compiled vector schema.")
                        st.rerun()
                    else:
                        st.session_state["document_indexed"] = "STANDBY"
                        st.sidebar.error("Data block initialization rejected.")
                except Exception as e:
                    st.session_state["document_indexed"] = "STANDBY"
                    st.sidebar.error(f"Broker connection offline: {e}")

    # Layout spacing utility
    st.markdown("<br>" * 8, unsafe_allow_html=True)
    st.markdown("<div style='margin-top:15px; margin-bottom:15px; height:1px; background:rgba(255,255,255,0.06);'></div>", unsafe_allow_html=True)
    if st.button("🔄 Purge Thread Cache", use_container_width=True):
        st.session_state["session_id"] = str(uuid.uuid4())[:8].upper()
        st.session_state["document_indexed"] = "STANDBY"
        st.session_state["last_routing_strategy"] = "INITIALIZED"
        
        # Reset chat history back to onboarding intro state
        st.session_state["chat_history"] = [{
            "role": "assistant",
            "message": introduction_payload,
            "sources": []
        }]
        st.rerun()

# --- CONVERSATIONAL INTERROGATION SPACE ---

# Smooth display of past context streaming items
for chat in st.session_state["chat_history"]:
    avatar = "👤" if chat["role"] == "user" else "🤖"
    with st.chat_message(chat["role"], avatar=avatar):
        st.markdown(chat["message"], unsafe_allow_html=True)
        if chat.get("sources"):
            st.markdown(f"<div style='color:#64748B; font-size:0.8rem; font-weight:500; margin-top:6px; font-family:\"JetBrains Mono\", monospace;'>📚 CITATIONS VERIFIED: {', '.join(chat['sources'])}</div>", unsafe_allow_html=True)

# User query capture sequence
if user_input := st.chat_input("Transmit operational or technical inquiry vectors..."):
    
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
            
            # Initiate streaming channel pipeline connection
            with requests.post(f"{BACKEND_URL}/research", json=payload, stream=True) as response:
                if response.status_code == 200:
                    for line in response.iter_lines():
                        if line:
                            decoded_line = line.decode("utf-8")
                            
                            if decoded_line.startswith("TOKEN:"):
                                token_content = decoded_line[len("TOKEN:"):]
                                full_response += token_content
                                # Ultra-premium glowing solid cursor block tracking typing telemetry
                                text_placeholder.markdown(full_response + "<span style='color:#00FFCC;'>█</span>", unsafe_allow_html=True)
                                
                            elif decoded_line.startswith("SOURCES:"):
                                json_sources = decoded_line[len("SOURCES:"):]
                                sources_cited = json.loads(json_sources)
                                
                    # Drop cursor block upon conclusion
                    text_placeholder.markdown(full_response)
                    
                    # Dynamically compute upper metrics card status values
                    if "Tavily Live Web Engine" in str(sources_cited) or not sources_cited and "No relevant context" in full_response:
                        st.session_state["last_routing_strategy"] = "🌐 WEB FALLBACK"
                    else:
                        st.session_state["last_routing_strategy"] = "💾 VECTOR RAG"
                        
                    if sources_cited:
                        st.markdown(f"<div style='color:#64748B; font-size:0.8rem; font-weight:500; margin-top:6px; font-family:\"JetBrains Mono\", monospace;'>📚 CITATIONS VERIFIED: {', '.join(sources_cited)}</div>", unsafe_allow_html=True)
                        
                    # Save state records
                    st.session_state["chat_history"].append({
                        "role": "assistant", 
                        "message": full_response,
                        "sources": sources_cited
                    })
                    st.rerun() # Refresh layout layers to capture telemetry modifications on top ribbon cards
                else:
                    st.error("❌ Critical streaming anomaly: Network token data frame dropped.")
        except Exception as e:
            st.error(f"❌ Core engine connection failure encountered: {e}")