from pathlib import Path
import pdfplumber
import docx
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
class CVReadToolInput(BaseModel):
    file_path: str = Field(description="Absolute path to the CV file (.txt, .pdf, or .docx).")

class CVReadTool(BaseTool):
    name: str = "CVReaderTool"
    description: str = "Extracts raw text from CV files (.txt, .pdf, .docx)."
    args_schema: Type[BaseModel] = CVReadToolInput

    def _run(self, file_path: str) -> str:
        path = Path(file_path).resolve()
        if not path.exists():
            return f"Error: File not found at {path}"

        ext = path.suffix.lower()

        if ext == ".txt":
            return path.read_text(encoding="utf-8")

        elif ext == ".pdf":
            try:
                text = ""
                with pdfplumber.open(path) as pdf:
                    for page in pdf.pages:
                        extracted = page.extract_text()
                        if extracted:
                            text += extracted + "\n"
                return text
            except Exception as e:
                return f"Error reading PDF: {e}"

        elif ext == ".docx":
            try:
                doc = docx.Document(path)
                return "\n".join(p.text for p in doc.paragraphs)
            except Exception as e:
                return f"Error reading DOCX: {e}"

        else:
            return f"Unsupported file type: {ext}"