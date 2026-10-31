"""Strict offline CLI for the five-statement nonofficial pipeline."""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from typing import Any

from aram_backend.balance_sheet_candidate import BalanceSheetLinePolicy
from aram_backend.cash_flow_direct_candidate import (
    MAX_CASH_ACCOUNTS, MAX_CASH_COUNTERPART_POLICIES, MAX_CASH_TRANSACTIONS,
    CashAccountPolicy, CashCounterpartPolicy, CashFlowEntry,
)
from aram_backend.cash_flow_direct_candidate_cli import (
    MAX_CASH_MANIFEST_BYTES, safe_read_cash_manifest,
)
from aram_backend.coverage_preview import CoverageError
from aram_backend.coverage_preview_cli import safe_read_workbook
from aram_backend.cross_statement_reconciliation import CashBalanceNoteSelection
from aram_backend.equity_changes_candidate import EquityMovementPolicy
from aram_backend.five_statement_pipeline import (
    FiveStatementPipelineResult, build_five_statement_pipeline,
)
from aram_backend.income_statement_candidate import IncomeStatementLinePolicy
from aram_backend.reconciliation_review import NoteReference
from aram_backend.reconciliation_review_cli import _strict_pairs


ROOT_FIELDS = frozenset({
    "schema_version", "company_code", "fiscal_year", "currency", "unit",
    "references", "balance_sheet_policies", "income_statement_policies",
    "equity_movement_policies", "cash_accounts", "counterpart_policies",
    "transactions", "cash_balance_notes",
})
REFERENCE_FIELDS = frozenset({
    "statement", "section", "note_number", "subnote_code",
    "expected_closing_exposure", "evidence_ref",
})
BS_POLICY_FIELDS = frozenset({
    "statement_section", "note_number", "subnote_code", "category",
    "sign_multiplier", "line_label", "policy_evidence_ref",
})
IS_POLICY_FIELDS = BS_POLICY_FIELDS
EQ_POLICY_FIELDS = frozenset({
    "statement_section", "note_number", "subnote_code", "equity_component",
    "movement_category", "sign_multiplier", "line_label", "policy_evidence_ref",
})
CASH_ACCOUNT_FIELDS = frozenset({"account_code", "evidence_ref"})
COUNTERPART_FIELDS = frozenset({"account_code", "activity", "evidence_ref"})
TRANSACTION_FIELDS = frozenset({
    "company_code", "fiscal_year", "line_id", "transaction_id", "posting_date",
    "cash_account_code", "counterpart_account_code", "cash_debit", "cash_credit",
    "counterpart_debit", "counterpart_credit", "evidence_ref",
})
CASH_NOTE_FIELDS = frozenset({
    "statement_section", "note_number", "subnote_code", "evidence_ref",
})
MAX_POLICY_ROWS = 10_000


@dataclass(frozen=True)
class ParsedPipelineManifest:
    company_code: str
    fiscal_year: int
    currency: str
    unit: str
    references: tuple[NoteReference, ...]
    balance_sheet_policies: tuple[BalanceSheetLinePolicy, ...]
    income_statement_policies: tuple[IncomeStatementLinePolicy, ...]
    equity_movement_policies: tuple[EquityMovementPolicy, ...]
    cash_accounts: tuple[CashAccountPolicy, ...]
    counterpart_policies: tuple[CashCounterpartPolicy, ...]
    transactions: tuple[CashFlowEntry, ...]
    cash_balance_notes: tuple[CashBalanceNoteSelection, ...]


def _reject_json_constant(value: str) -> None:
    raise CoverageError("PIPELINE_MANIFEST_NONFINITE_NUMBER")


def _rows(
    payload: dict[str, Any], key: str, fields: frozenset[str],
    factory: type, maximum: int, *, minimum: int = 0,
) -> tuple[Any, ...]:
    items = payload[key]
    if (not isinstance(items, list) or len(items) < minimum
            or len(items) > maximum):
        raise CoverageError("PIPELINE_MANIFEST_" + key.upper() + "_INVALID")
    result = []
    for item in items:
        if not isinstance(item, dict) or set(item) != fields:
            raise CoverageError("PIPELINE_MANIFEST_" + key.upper() + "_ROW_INVALID")
        if any(
            not isinstance(item[field], str) or not item[field]
            for field in string_fields
        ):
            raise CoverageError("PIPELINE_MANIFEST_" + key.upper() + "_ROW_INVALID")
        if sign_field is not None and (
            type(item[sign_field]) is not int or item[sign_field] not in (-1, 1)
        ):
            raise CoverageError("PIPELINE_MANIFEST_" + key.upper() + "_ROW_INVALID")
        try:
            result.append(factory(**item))
        except (TypeError, ValueError) as exc:
            raise CoverageError(
                "PIPELINE_MANIFEST_" + key.upper() + "_ROW_INVALID"
            ) from exc
    return tuple(result)


def parse_pipeline_manifest(content: bytes) -> ParsedPipelineManifest:
    if (not isinstance(content, bytes)
            or not 0 < len(content) <= MAX_CASH_MANIFEST_BYTES):
        raise CoverageError("PIPELINE_MANIFEST_SIZE_INVALID")
    try:
        payload = json.loads(
            content.decode("utf-8"),
            object_pairs_hook=_strict_pairs,
            parse_constant=_reject_json_constant,
        )
    except CoverageError:
        raise
    except (UnicodeError, ValueError, RecursionError) as exc:
        raise CoverageError("PIPELINE_MANIFEST_JSON_INVALID") from exc
    if not isinstance(payload, dict) or set(payload) != ROOT_FIELDS:
        raise CoverageError("PIPELINE_MANIFEST_SCHEMA_INVALID")
    if type(payload["schema_version"]) is not int or payload["schema_version"] != 1:
        raise CoverageError("PIPELINE_MANIFEST_VERSION_INVALID")

    company = payload["company_code"]
    if (not isinstance(company, str) or not company
            or company != company.strip() or len(company) > 64
            or any(ord(char) < 32 or ord(char) == 127 for char in company)):
        raise CoverageError("PIPELINE_MANIFEST_COMPANY_INVALID")
    year = payload["fiscal_year"]
    if type(year) is not int or year <= 0:
        raise CoverageError("PIPELINE_MANIFEST_YEAR_INVALID")
    currency, unit = payload["currency"], payload["unit"]
    for value in (currency, unit):
        if (not isinstance(value, str) or not value or value != value.strip()
                or len(value) > 32
                or any(ord(char) < 32 or ord(char) == 127 for char in value)):
            raise CoverageError("PIPELINE_MANIFEST_CURRENCY_UNIT_INVALID")

    return ParsedPipelineManifest(
        company_code=company,
        fiscal_year=year,
        currency=currency,
        unit=unit,
        references=_rows(
            payload, "references", REFERENCE_FIELDS, NoteReference,
            MAX_POLICY_ROWS, minimum=1,
            string_fields=("expected_closing_exposure",),
        ),
        balance_sheet_policies=_rows(
            payload, "balance_sheet_policies", BS_POLICY_FIELDS,
            BalanceSheetLinePolicy, MAX_POLICY_ROWS, sign_field="sign_multiplier",
        ),
        income_statement_policies=_rows(
            payload, "income_statement_policies", IS_POLICY_FIELDS,
            IncomeStatementLinePolicy, MAX_POLICY_ROWS, sign_field="sign_multiplier",
        ),
        equity_movement_policies=_rows(
            payload, "equity_movement_policies", EQ_POLICY_FIELDS,
            EquityMovementPolicy, MAX_POLICY_ROWS, sign_field="sign_multiplier",
        ),
        cash_accounts=_rows(
            payload, "cash_accounts", CASH_ACCOUNT_FIELDS,
            CashAccountPolicy, MAX_CASH_ACCOUNTS, minimum=1,
        ),
        counterpart_policies=_rows(
            payload, "counterpart_policies", COUNTERPART_FIELDS,
            CashCounterpartPolicy, MAX_CASH_COUNTERPART_POLICIES,
        ),
        transactions=_rows(
            payload, "transactions", TRANSACTION_FIELDS,
            CashFlowEntry, MAX_CASH_TRANSACTIONS,
            string_fields=(
                "cash_debit", "cash_credit",
                "counterpart_debit", "counterpart_credit",
            ),
        ),
        cash_balance_notes=_rows(
            payload, "cash_balance_notes", CASH_NOTE_FIELDS,
            CashBalanceNoteSelection, MAX_POLICY_ROWS, minimum=1,
        ),
    )


def run_pipeline_cli(workbook_path: str, manifest_path: str) -> FiveStatementPipelineResult:
    manifest = parse_pipeline_manifest(safe_read_cash_manifest(manifest_path))
    workbook = safe_read_workbook(workbook_path)
    return build_five_statement_pipeline(
        workbook,
        company_code=manifest.company_code,
        fiscal_year=manifest.fiscal_year,
        references=manifest.references,
        balance_sheet_policies=manifest.balance_sheet_policies,
        income_statement_policies=manifest.income_statement_policies,
        equity_movement_policies=manifest.equity_movement_policies,
        currency=manifest.currency,
        unit=manifest.unit,
        cash_accounts=manifest.cash_accounts,
        counterpart_policies=manifest.counterpart_policies,
        transactions=manifest.transactions,
        cash_balance_notes=manifest.cash_balance_notes,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="ARAM offline NONOFFICIAL five-statement analyst preview"
    )
    parser.add_argument("--file", required=True, help="Local Pilot XLSX snapshot")
    parser.add_argument("--manifest", required=True, help="Strict JSON policy/transaction manifest")
    args = parser.parse_args(argv)
    try:
        result = run_pipeline_cli(args.file, args.manifest)
    except CoverageError as exc:
        print("ARAM five-statement pipeline blocked: " + exc.code, file=sys.stderr)
        return 2
    print(json.dumps(
        result.to_dict(), ensure_ascii=True, sort_keys=True, separators=(",", ":"),
    ))
    return 0 if result.eligible_for_analyst_review else 3


if __name__ == "__main__":
    raise SystemExit(main())
