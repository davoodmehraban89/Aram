from typing import Dict, Any, List


DEFAULT_COLUMN_MAPPING = {
    "account_code": ["account_code", "code", "کد حساب"],
    "account_name": ["account_name", "title", "name", "نام حساب"],
    "debit": ["debit", "bedehkar", "بدهکار"],
    "credit": ["credit", "bestankar", "بستانکار"],
    "amount": ["amount", "net", "mablagh", "مبلغ"],
    "t1": ["t1", "tafsil1"],
    "t2": ["t2", "tafsil2"],
    "t3": ["t3", "tafsil3"],
    "t4": ["t4", "tafsil4"],
}


class NormalizationMapper:
    """Maps raw source row dictionary into standardized record attributes based on mapping template."""
    def __init__(self, mapping_template: Dict[str, Any] = None):
        self.mapping = mapping_template or DEFAULT_COLUMN_MAPPING

    def map_row(self, row_data: Dict[str, Any], row_index: int) -> Dict[str, Any]:
        mapped = {
            "row_index": row_index,
            "account_code": "",
            "account_name": "",
            "debit": 0.00,
            "credit": 0.00,
            "net_amount": 0.00,
            "t1": None,
            "t2": None,
            "t3": None,
            "t4": None,
            "raw_payload": row_data,
        }

        # Normalize keys in row_data for matching
        normalized_row = {str(k).strip().lower(): v for k, v in row_data.items()}

        for field, possible_headers in self.mapping.items():
            val = None
            if isinstance(possible_headers, list):
                for header in possible_headers:
                    if header.lower() in normalized_row:
                        val = normalized_row[header.lower()]
                        break
            elif isinstance(possible_headers, str) and possible_headers.lower() in normalized_row:
                val = normalized_row[possible_headers.lower()]

            if val is not None:
                if field in ("debit", "credit", "amount", "net_amount"):
                    try:
                        mapped[field if field != "amount" else "net_amount"] = float(str(val).replace(",", "").strip())
                    except (ValueError, TypeError):
                        mapped[field if field != "amount" else "net_amount"] = 0.00
                elif field in mapped:
                    mapped[field] = str(val).strip()

        # Calculate net amount if debit/credit provided
        if mapped["net_amount"] == 0.00 and (mapped["debit"] != 0.00 or mapped["credit"] != 0.00):
            mapped["net_amount"] = mapped["debit"] - mapped["credit"]

        return mapped
