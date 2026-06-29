import os
from pathlib import Path

# 1. Base Project Directory Mappings
CORE_DIR = Path(__file__).resolve().parent
BACKEND_ROOT = CORE_DIR.parent
PROJECT_ROOT = BACKEND_ROOT.parent

# 2. Storage Directory Targets
DATA_DIR = PROJECT_ROOT / "data"
CHROMA_DIR = PROJECT_ROOT / "chroma_db"

# Ensure data storage path exists safely
os.makedirs(DATA_DIR, exist_ok=True)

# 3. Model Configuration Hyperparameters
EMBEDDING_MODEL_NAME = "text-embedding-3-small"
LLM_MODEL_NAME = "gpt-4o"
LLM_TEMPERATURE = 0.0  # Zero out creativity for maximum grounding

# 4. Global RAG Hyperparameters
RETRIEVER_K_VAL = 4  # Number of document context chunks extracted per loop