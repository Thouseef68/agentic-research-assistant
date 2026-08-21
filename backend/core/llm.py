import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

# 1. Dynamically locate your data/.env file (2 levels up from backend/core)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.abspath(os.path.join(BASE_DIR, "../../data/.env"))
load_dotenv(dotenv_path=ENV_PATH)

# ============================================================
# GITHUB MODELS — EXISTING EMBEDDINGS
# ============================================================

if not os.getenv("GITHUB_TOKEN"):
    raise ValueError(
        f"❌ Error: GITHUB_TOKEN could not be resolved from: {ENV_PATH}"
    )

GITHUB_MODELS_URL = "https://models.github.ai/inference"

embedding_model = OpenAIEmbeddings(
    base_url=GITHUB_MODELS_URL,
    api_key=os.getenv("GITHUB_TOKEN"),
    model="text-embedding-3-small"
)

# ============================================================
# GROK — NEW ORCHESTRATION BRAIN
# ============================================================

if not os.getenv("XAI_API_KEY"):
    raise ValueError(
        "❌ Error: XAI_API_KEY could not be resolved."
    )

XAI_BASE_URL = "https://api.x.ai/v1"

llm = ChatOpenAI(
    base_url=XAI_BASE_URL,
    api_key=os.getenv("XAI_API_KEY"),
    model="grok-4.6",
    temperature=0.0
)

print(
    "🧬 Infrastructure Baseline Online: "
    "Grok 4.6 Brain + GitHub Embeddings initialized."
)