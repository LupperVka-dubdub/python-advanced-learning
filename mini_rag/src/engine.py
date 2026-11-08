from pathlib import Path
from typing import List, Tuple, Callable

from src.extractors import PDFExtractor
from src.chunkers import FixedSizeChunker
from src.vector_store import InMemoryVectorStore


def default_mock_embed(text: str) -> List[float]:
    """默认本地测试用的特征向量生成函数（无需联网即可跑通闭环）"""
    v1 = float(len(text) % 10 + 1)
    v2 = float(sum(ord(c) for c in text[:5]) % 10 + 1) if text else 1.0
    return [v1, v2, 1.0]


class RAGEngine:
    """RAG 核心总控引擎：提取 -> 切片 -> 入库 -> 检索"""

    def __init__(
        self,
        chunk_size: int = 500,
        overlap: int = 50,
        embed_fn: Callable[[str], List[float]] = default_mock_embed,
    ):
        self.extractor = PDFExtractor()
        self.chunker = FixedSizeChunker(chunk_size=chunk_size, overlap=overlap)
        self.vector_store = InMemoryVectorStore(embed_fn=embed_fn)

    def ingest_pdf(self, file_path: Path) -> int:
        """读取 PDF 并完成切片与向量入库，返回存入的切片数量"""
        raw_text = self.extractor.extract(file_path)
        chunks = self.chunker.chunk(raw_text)
        self.vector_store.add_texts(chunks)
        print(f"📄 文本提取成功，总字数: {len(raw_text)} | 🔪 入库切片数: {len(chunks)}")
        return len(chunks)

    def retrieve(self, query: str, top_k: int = 2) -> List[Tuple[float, str]]:
        """检索与问题最相关的 top_k 个文本块"""
        return self.vector_store.search(query=query, top_k=top_k)


if __name__ == "__main__":
    engine = RAGEngine(chunk_size=200, overlap=30)
    pdf_path = Path("test.pdf")

    if pdf_path.exists():
        count = engine.ingest_pdf(pdf_path)
        if count > 0:
            results = engine.retrieve("测试查询问题", top_k=2)
            print("\n🔍 --- 检索结果预览 ---")
            for score, text in results:
                print(f"匹配得分: {score:.4f} | 内容: {text[:60]}...")
    else:
        print("❌ 未找到 test.pdf，请检查根目录是否有该文件。")