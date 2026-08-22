import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# ==========================================
# ENVIRONMENT
# ==========================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.abspath(os.path.join(BASE_DIR, "../../data/.env"))

load_dotenv(dotenv_path=ENV_PATH)


# ==========================================
# GROQ — BRAIN
# ==========================================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("❌ GROQ_API_KEY is missing")

llm = ChatOpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=GROQ_API_KEY,
    model="openai/gpt-oss-120b",
    temperature=0.0
)


# ==========================================
# GEMINI — RAG EMBEDDINGS
# ==========================================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("❌ GEMINI_API_KEY is missing")

embedding_model = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=GEMINI_API_KEY
)


# ==========================================
# STATUS
# ==========================================

print("🧠 Brain: Groq GPT-OSS 120B")
print("📚 Embeddings: Gemini Embedding 001")