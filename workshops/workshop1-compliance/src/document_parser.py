"""
Workshop 1 — Step 2: 文档解析 Agent
支持 PDF / HTML / TXT 格式（对应 SDD 规范 §2.1）
"""
from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, TextLoader

from config import CHUNK_SIZE, CHUNK_OVERLAP


# ── 文档加载 ───────────────────────────────────────────────────

def load_document(path: str) -> list[dict]:
    """加载文档并返回 [{page_content, metadata}]"""
    p = Path(path)
    suffix = p.suffix.lower()

    if suffix == ".pdf":
        loader = PyPDFLoader(str(p))
        pages = loader.load()
        return [{"page_content": pg.page_content,
                 "metadata": {"source": str(p), "page": pg.metadata.get("page", 0)}}
                for pg in pages]

    if suffix in (".html", ".htm"):
        from bs4 import BeautifulSoup

        html = p.read_text(encoding="utf-8")
        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text(separator="\n", strip=True)
        return [{"page_content": text, "metadata": {"source": str(p)}}]

    # 默认当纯文本处理
    loader = TextLoader(str(p), encoding="utf-8")
    docs = loader.load()
    return [{"page_content": d.page_content,
             "metadata": {"source": str(p)}}
            for d in docs]


# ── 文本分块 ───────────────────────────────────────────────────

def split_documents(docs: list[dict]) -> list[dict]:
    """将文档切分为适合向量化的块"""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", "。", ". ", " "],
    )
    chunks = []
    for doc in docs:
        splits = splitter.split_text(doc["page_content"])
        for i, s in enumerate(splits):
            chunks.append({
                "page_content": s,
                "metadata": {**doc["metadata"], "chunk_index": i},
            })
    return chunks


# ── 结构化提取 ─────────────────────────────────────────────────

def extract_sections(text: str) -> list[dict]:
    """从监管文档中提取章节结构（简化版）"""
    sections = []
    current_section = None
    current_content = []

    for line in text.split("\n"):
        stripped = line.strip()
        # 简单启发式：以数字开头或全大写的行视为章节标题
        if (stripped and
            (stripped[0].isdigit() and "." in stripped[:5]) or
            stripped.isupper()):
            if current_section:
                sections.append({
                    "title": current_section,
                    "content": "\n".join(current_content),
                })
            current_section = stripped
            current_content = []
        else:
            current_content.append(line)

    if current_section:
        sections.append({
            "title": current_section,
            "content": "\n".join(current_content),
        })

    return sections


if __name__ == "__main__":
    # 快速测试
    import sys
    if len(sys.argv) > 1:
        docs = load_document(sys.argv[1])
        chunks = split_documents(docs)
        print(f"Loaded {len(docs)} pages, split into {len(chunks)} chunks")
        for c in chunks[:3]:
            print(f"  [{c['metadata']}] {c['page_content'][:80]}...")
