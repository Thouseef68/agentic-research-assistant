import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEmbeddings

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
# LOCAL — RAG EMBEDDINGS
# ==========================================

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": True}
)


# ==========================================
# STATUS
# ==========================================

print("🧠 Brain: Groq GPT-OSS 120B")
print("📚 Embeddings: Local HuggingFace all-MiniLM-L6-v2")