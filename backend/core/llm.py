import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

# 1. Dynamically locate your data/.env file (2 levels up from backend/core)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.abspath(os.path.join(BASE_DIR, "../../data/.env"))
load_dotenv(dotenv_path=ENV_PATH)

# Validate token presence before booting model instances
if not os.getenv("GITHUB_TOKEN"):
    raise ValueError(f"❌ Error: GITHUB_TOKEN could not be resolved from: {ENV_PATH}")

# GitHub Models universal inference endpoint
GITHUB_MODELS_URL = "https://models.inference.ai.azure.com"

# 2. Initialize OpenAI Embeddings via GitHub Proxy (Generates 1536-dimensional vectors)
embedding_model = OpenAIEmbeddings(
    base_url=GITHUB_MODELS_URL,
    api_key=os.getenv("GITHUB_TOKEN"),
    model="text-embedding-3-small"
)

# 3. Initialize GPT-4o Orchestration Brain
llm = ChatOpenAI(
    base_url=GITHUB_MODELS_URL,
    api_key=os.getenv("GITHUB_TOKEN"),
    model="gpt-4o",
    temperature=0.0  # Grounded, strict responses
)

print("🧬 Infrastructure Baseline Online: GitHub Models (GPT-4o & Text-Embedding-3) initialized.")