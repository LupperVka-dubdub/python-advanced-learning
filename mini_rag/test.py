import pytest
from src.chunkers import FixedSizeChunker
from src.vector_store import InMemoryVectorStore


def test_chunker_normal():
    chunker = FixedSizeChunker(chunk_size=10, overlap=2)
    text = "0123456789abcdefghij"  # 20 个字符
    chunks = chunker.chunk(text)
    assert len(chunks) == 3
    assert chunks[0] == "0123456789"
    assert chunks[1] == "89abcdefgh"  # 验证重叠了 '89'


def test_chunker_invalid_overlap():
    # 验证当 overlap >= chunk_size 时，是否按预期抛出 ValueError
    with pytest.raises(ValueError):
        FixedSizeChunker(chunk_size=10, overlap=10)


def test_vector_store_search():
    def dummy_embed(t: str):
        return [1.0, 0.0] if "Python" in t else [0.0, 1.0]

    store = InMemoryVectorStore(embed_fn=dummy_embed)
    store.add_texts(["我爱写 Python 代码", "今天天气不错"])
    results = store.search("Python 教程", top_k=1)

    assert len(results) == 1
    score, matched_text = results[0]
    assert score > 0.99
    assert "Python" in matched_text