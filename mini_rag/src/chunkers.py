from abc import ABC, abstractmethod
from typing import List



class BaseChunker(ABC):
    """切片器抽象基类：规定所有切片器必须实现 chunk 方法"""

    @abstractmethod
    def chunk(self, text: str) -> List[str]:
        pass


class FixedSizeChunker(BaseChunker):
    """固定长度滑动窗口切片器"""

    def __init__(self, chunk_size: int = 500, overlap: int = 50):
        if overlap >= chunk_size:
            raise ValueError(f"overlap ({overlap}) 必须严格小于 chunk_size ({chunk_size})")
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(self, text: str) -> List[str]:
        if not text or not text.strip():
            return []
        start = 0
        text_len = len(text)
        chunks = []

        while start < text_len :
            end = min(start + self.chunk_size,text_len)
            

            if end < text_len:
                last_ = max(text.rfind(p,start,end) for p in ".!?。！？")

                if last_ == -1 :
                    last_ = text.rfind("\n",start,end)  
                    

                if last_ != -1 and last_ + 1 - start > self.overlap :  
                    end = last_ + 1    

            chunks.append(text[start:end])

            if end == text_len :
                break

            start = end - self.overlap
        return chunks
                


        
        

if __name__ == "__main__":
    chunker = FixedSizeChunker(chunk_size=30, overlap=5)
    test_text = "这是第一句话。这是第二句话，内容稍微长一点。这是第三句话。这是最后一句话。"
    result = chunker.chunk(test_text)
    for i, c in enumerate(result):
        print(f"块 {i + 1}: {c}")