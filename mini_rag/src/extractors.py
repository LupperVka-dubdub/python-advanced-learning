from abc import ABC, abstractmethod
from pathlib import Path
import fitz  # PyMuPDF


class BaseExtractor(ABC):
    """提取器抽象基类：规定所有提取器必须实现 extract 方法"""

    @abstractmethod
    def extract(self, file_path: Path) -> str:
        pass


class PDFExtractor(BaseExtractor):
    """PDF 文本提取器"""

    def extract(self, file_path: Path) -> str:
        if not file_path.exists():
            raise FileNotFoundError(f"找不到文件: {file_path}")

        text_blocks = []
        with fitz.open(file_path) as doc:
            for page in doc:
                text_blocks.append(page.get_text())

        return "".join(text_blocks)


if __name__ == "__main__":
    extractor = PDFExtractor()
    pdf_path = Path("test.pdf")
    if pdf_path.exists():
        content = extractor.extract(pdf_path)
        print(f"✅ 提取成功，总字数: {len(content)}")