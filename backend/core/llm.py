import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.abspath(os.path.join(BASE_DIR, "../../data/.env"))
load_dotenv(dotenv_path=ENV_PATH)

# ==============================
# GROQ API
# ==============================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError(
        f"❌ Error: GROQ_API_KEY could not be resolved from: {ENV_PATH}"
    )

GROQ_BASE_URL = "https://api.groq.com/openai/v1"

# ==============================
# EMBEDDINGS
# ==============================
# KEEP YOUR EXISTING EMBEDDING SYSTEM HERE.
# Do NOT try to use Groq for embeddings unless we specifically decide
# to change the embedding architecture.

# ==============================
# GROQ BRAIN
# ==============================

llm = ChatOpenAI(
    base_url=GROQ_BASE_URL,
    api_key=GROQ_API_KEY,
    model="openai/gpt-oss-120b",
    temperature=0.0
)

print("🧬 Infrastructure Baseline Online: Groq GPT-OSS 120B initialized.")