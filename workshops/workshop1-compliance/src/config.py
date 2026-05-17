"""
Workshop 1 — 配置文件
使用 Azure OpenAI endpoint（适配 LSEG 技术栈）
"""
import os
from dotenv import load_dotenv

load_dotenv()

# ── Azure OpenAI 配置 ──────────────────────────────────────────
# LSEG 使用 Microsoft AI Foundry，通过 Azure OpenAI endpoint 调用模型
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "https://your-resource.openai.azure.com/")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY", "your-api-key")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-06-01")
AZURE_DEPLOYMENT_NAME = os.getenv("AZURE_DEPLOYMENT_NAME", "gpt-4o")
AZURE_EMBEDDING_DEPLOYMENT = os.getenv("AZURE_EMBEDDING_DEPLOYMENT", "text-embedding-3-small")

# ── RAG 配置 ───────────────────────────────────────────────────
CHROMA_PERSIST_DIR = "./chroma_db"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# ── 质量阈值（来自 SDD 规范） ──────────────────────────────────
CONFIDENCE_THRESHOLD = 0.8  # 低于此值标记为待人工复核
