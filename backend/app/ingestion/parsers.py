import os
import hashlib
from typing import Dict, Any


def compute_file_hash(file_path: str) -> str:
    """Computes SHA256 checksum of a file without modifying it."""
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


class BaseParser:
    """Base parser interface for immutable file extraction."""
    def extract_metadata(self, file_path: str) -> Dict[str, Any]:
        raise NotImplementedError()


class XLSXParser(BaseParser):
    def extract_metadata(self, file_path: str) -> Dict[str, Any]:
        file_size = os.path.getsize(file_path)
        file_hash = compute_file_hash(file_path)
        return {
            "format": "xlsx",
            "file_size": file_size,
            "file_hash": file_hash,
            "filename": os.path.basename(file_path),
        }


class CSVParser(BaseParser):
    def extract_metadata(self, file_path: str) -> Dict[str, Any]:
        file_size = os.path.getsize(file_path)
        file_hash = compute_file_hash(file_path)
        return {
            "format": "csv",
            "file_size": file_size,
            "file_hash": file_hash,
            "filename": os.path.basename(file_path),
        }


class PDFParser(BaseParser):
    def extract_metadata(self, file_path: str) -> Dict[str, Any]:
        file_size = os.path.getsize(file_path)
        file_hash = compute_file_hash(file_path)
        return {
            "format": "pdf",
            "file_size": file_size,
            "file_hash": file_hash,
            "filename": os.path.basename(file_path),
        }


def get_parser(file_path: str) -> BaseParser:
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".xlsx":
        return XLSXParser()
    elif ext == ".csv":
        return CSVParser()
    elif ext == ".pdf":
        return PDFParser()
    else:
        raise ValueError(f"Unsupported file format '{ext}'. Only .xlsx, .csv, and .pdf are supported.")
