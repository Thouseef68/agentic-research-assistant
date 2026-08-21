import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

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
# GITHUB — EXISTING EMBEDDINGS
# ==========================================

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

if not GITHUB_TOKEN:
    raise ValueError("❌ GITHUB_TOKEN is missing")

embedding_model = OpenAIEmbeddings(
    base_url="https://models.github.ai/inference",
    api_key=GITHUB_TOKEN,
    model="text-embedding-3-small"
)


print("🧠 Brain: Groq GPT-OSS 120B")
print("📚 Embeddings: GitHub text-embedding-3-small")