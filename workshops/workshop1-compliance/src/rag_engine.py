"""
Workshop 1 — Step 3: RAG 知识库引擎
将企业合规手册向量化，支持语义检索
"""
from langchain_openai import AzureOpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

from config import (
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_API_VERSION,
    AZURE_EMBEDDING_DEPLOYMENT,
    CHROMA_PERSIST_DIR,
)


def get_embeddings() -> AzureOpenAIEmbeddings:
    """获取 Azure OpenAI 嵌入模型"""
    return AzureOpenAIEmbeddings(
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        api_key=AZURE_OPENAI_API_KEY,
        api_version=AZURE_OPENAI_API_VERSION,
        azure_deployment=AZURE_EMBEDDING_DEPLOYMENT,
    )


def build_vectorstore(chunks: list[dict], collection_name: str = "compliance") -> Chroma:
    """将文档块存入 ChromaDB 向量库"""
    documents = [
        Document(page_content=c["page_content"], metadata=c["metadata"])
        for c in chunks
    ]
    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=get_embeddings(),
        collection_name=collection_name,
        persist_directory=CHROMA_PERSIST_DIR,
    )
    print(f"Built vectorstore: {len(documents)} chunks in '{collection_name}'")
    return vectorstore


def load_vectorstore(collection_name: str = "compliance") -> Chroma:
    """加载已有的向量库"""
    return Chroma(
        collection_name=collection_name,
        embedding_function=get_embeddings(),
        persist_directory=CHROMA_PERSIST_DIR,
    )


def search(query: str, vectorstore: Chroma, top_k: int = 5) -> list[dict]:
    """语义检索，返回最相关的文档块"""
    results = vectorstore.similarity_search_with_score(query, k=top_k)
    return [
        {
            "content": doc.page_content,
            "metadata": doc.metadata,
            "relevance_score": round(1 - score, 3),  # ChromaDB 返回距离，转为相似度
        }
        for doc, score in results
    ]


if __name__ == "__main__":
    from document_parser import load_document, split_documents
    import sys

    if len(sys.argv) > 1:
        docs = load_document(sys.argv[1])
        chunks = split_documents(docs)
        vs = build_vectorstore(chunks)
        results = search("反洗钱 客户尽职调查", vs)
        for r in results:
            print(f"  [score={r['relevance_score']}] {r['content'][:80]}...")
