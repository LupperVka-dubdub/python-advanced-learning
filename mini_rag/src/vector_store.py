import math
from typing import List, Tuple, Callable


class InMemoryVectorStore:
    """轻量级内存向量库：基于余弦相似度"""

    def __init__(self, embed_fn: Callable[[str], List[float]]):
        self.embed_fn = embed_fn
        self.storage: List[Tuple[str, List[float]]] = []

    def normlise(self,vec:List[float]) -> float:
        
        norm_vec = math.sqrt(sum(a*a for a in vec))
        if norm_vec == 0.0:
            return vec
        return [x/norm_vec for x in vec]
    
    @staticmethod
    def _cosine_similarity(norm_query_vec,norm_vec) -> float:
        
        return sum(a*b for a,b in zip(norm_query_vec,norm_vec))

    def add_texts(self, texts: List[str]) -> None:
        
        for text in texts:
            vector = self.embed_fn(text)
            norm_vec = self.normlise(vector)
            self.storage.append((text,norm_vec))

        

    def search(self, query: str, top_k: int = 3) -> List[Tuple[float, str]]:
        if not self.storage:
            return []

        query_vec = self.embed_fn(query)
        norm_query_vec = self.normlise(query_vec)
        scores = [
            (self._cosine_similarity(norm_query_vec, norm_vec), text)
            for text, norm_vec in self.storage
        ]
        scores.sort(key=lambda x: x[0], reverse=True)
        return scores[:top_k]


if __name__ == "__main__":
    def mock_embed(text: str) -> List[float]:
        if "微积分" in text or "方程" in text:
            return [0.9, 0.1, 0.0]
        if "电磁" in text or "力学" in text:
            return [0.1, 0.9, 0.0]
        return [0.0, 0.0, 1.0]

    store = InMemoryVectorStore(embed_fn=mock_embed)
    store.add_texts(["高等数学：常微分方程", "大学物理：电磁学", "红楼梦导读"])
    hits = store.search("怎么学微积分？", top_k=2)
    print(f"✅ 向量库自测成功: {hits}")