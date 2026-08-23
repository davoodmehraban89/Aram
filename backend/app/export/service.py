import csv
import io
from typing import Dict, Any


def export_statement_to_csv(statement_data: Dict[str, Any]) -> str:
    """Exports financial statement calculation dict to CSV string."""
    output = io.StringIO()
    writer = csv.writer(output)

    stmt_type = statement_data.get("statement_type", "REPORT")
    title = statement_data.get("title", "Financial Statement")
    writer.writerow(["Statement", title, f"Type: {stmt_type}"])
    writer.writerow([])

    if stmt_type == "TB":
        writer.writerow(["Account Code", "Account Name", "Total Debit", "Total Credit", "Net Balance"])
        for row in statement_data.get("rows", []):
            writer.writerow([
                row.get("account_code", ""),
                row.get("account_name", ""),
                row.get("total_debit", 0.0),
                row.get("total_credit", 0.0),
                row.get("net_balance", 0.0),
            ])
        writer.writerow([])
        writer.writerow(["TOTALS", "", statement_data.get("total_debit", 0.0), statement_data.get("total_credit", 0.0), ""])
    elif stmt_type in ("BS", "IS"):
        writer.writerow(["Section", "Group Name", "Amount"])
        sections = statement_data.get("sections", {})
        for sec_name, groups in sections.items():
            for group_name, amount in groups.items():
                writer.writerow([sec_name, group_name, amount])

    return output.getvalue()


def export_statement_to_pdf_structure(statement_data: Dict[str, Any]) -> Dict[str, Any]:
    """Formats financial statement dict into structured payload ready for PDF rendering."""
    return {
        "title": statement_data.get("title", "Financial Statement"),
        "statement_type": statement_data.get("statement_type"),
        "formatted_totals": {
            "total_debit": f"{statement_data.get('total_debit', 0.0):,.2f}" if "total_debit" in statement_data else None,
            "total_credit": f"{statement_data.get('total_credit', 0.0):,.2f}" if "total_credit" in statement_data else None,
            "net_profit": f"{statement_data.get('net_profit', 0.0):,.2f}" if "net_profit" in statement_data else None,
            "total_assets": f"{statement_data.get('total_assets', 0.0):,.2f}" if "total_assets" in statement_data else None,
        },
        "raw_data": statement_data,
    }
