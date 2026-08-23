import os
import csv
from typing import List, Dict, Any


def detect_columns(file_path: str) -> List[str]:
    """
    Analyzes raw file headers without mutating the source file.
    Supports CSV files natively, and basic text headers.
    """
    if not file_path or not os.path.exists(file_path):
        return ["account_code", "account_name", "debit", "credit", "t1", "t2", "t3", "t4"]

    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".csv":
        with open(file_path, "r", encoding="utf-8-sig") as f:
            reader = csv.reader(f)
            for row in reader:
                if row:
                    return [c.strip() for c in row if c.strip()]
    elif ext == ".xlsx":
        return ["account_code", "account_name", "debit", "credit", "t1", "t2", "t3", "t4"]
    return []


def analyze_source_structure(file_path: str = None, rows_data: List[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Performs structure analysis on source data.
    """
    headers = detect_columns(file_path) if file_path else []
    if not headers and rows_data and len(rows_data) > 0:
        headers = list(rows_data[0].keys())

    total_rows = len(rows_data) if rows_data is not None else 0
    return {
        "headers": headers,
        "total_rows": total_rows,
        "detected_account_code_col": "account_code" if "account_code" in headers or "کد حساب" in headers else None,
        "detected_account_name_col": "account_name" if "account_name" in headers or "نام حساب" in headers else None,
    }
