"""Read-only preview of account-to-note Mapping coverage.

NEVER use the returned amounts as official financial statements. The workbook
can claim 'Approved', but a cell is not a verified reviewer identity. This
module performs no database writes, postings, imports or export of reports.
"""
from __future__ import annotations

from collections import defaultdict
from dataclasses import asdict, dataclass
from decimal import Decimal, InvalidOperation, localcontext
from hashlib import sha256
from io import BytesIO
from typing import Any
from zipfile import BadZipFile, ZipFile

from openpyxl import load_workbook

from aram_backend.pilot_workbook import SHEET_HEADERS, preflight_pilot_workbook

MAX_INPUT_BYTES = 20 * 1024 * 1024
MAX_ZIP_ENTRIES = 500
MAX_EXPANDED_BYTES = 128 * 1024 * 1024


class CoverageError(ValueError):
    """A deterministic fail-closed coverage precondition violation."""

    def __init__(self, code: str) -> None:
        self.code = code
        super().__init__(code)


@dataclass(frozen=True)
class CoverageException:
    code: str
    account_code: str
    account_excel_row: int
    mapping_excel_rows: tuple[int, ...]


@dataclass(frozen=True)
class AccountTrace:
    account_code: str
    account_name: str
    account_excel_row: int
    source_row: int
    closing_exposure: str
    mapping_excel_row: int | None
    mapping_id: str | None
    target_statement: str | None
    target_section: str | None
    target_note: str | None
    target_subnote: str | None
    included: bool


@dataclass(frozen=True)
class NoteExposure:
    statement: str
    section: str
    note_number: str
    subnote_code: str
    closing_exposure: str
    account_codes: tuple[str, ...]


@dataclass(frozen=True)
class CoveragePreview:
    company_code: str
    fiscal_year: int
    source_sha256: str
    workbook_company_status: str
    account_count: int
    candidate_mapped_accounts: int
    blocked_accounts: int
    source_closing_exposure: str
    candidate_closing_exposure: str
    blocked_closing_exposure: str
    notes: tuple[NoteExposure, ...]
    accounts: tuple[AccountTrace, ...]
    exceptions: tuple[CoverageException, ...]
    kind: str = "UNAPPROVED_MAPPING_COVERAGE_PREVIEW"
    financial_statement: bool = False
    trusted_approvals: bool = False
    releasable: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _guard_archive(content: bytes) -> None:
    try:
        with ZipFile(BytesIO(content)) as archive:
            members = archive.infolist()
            if len(members) > MAX_ZIP_ENTRIES:
                raise CoverageError("WORKBOOK_ARCHIVE_LIMIT")
            expanded = 0
            for member in members:
                if member.file_size < 0 or member.file_size > MAX_EXPANDED_BYTES:
                    raise CoverageError("WORKBOOK_ARCHIVE_LIMIT")
                expanded += member.file_size
                if expanded > MAX_EXPANDED_BYTES:
                    raise CoverageError("WORKBOOK_ARCHIVE_LIMIT")
    except (BadZipFile, ValueError, OSError) as exc:
        if isinstance(exc, CoverageError):
            raise
        raise CoverageError("WORKBOOK_ARCHIVE_INVALID") from exc


def _read_rows(sheet: Any, headers: tuple[str, ...]) -> list[tuple[int, dict[str, Any]]]:
    rows = []
    for excel_row, values in enumerate(sheet.iter_rows(min_row=2, values_only=True), 2):
        row = dict(zip(headers, values))
        if any(value is not None and str(value).strip() for value in row.values()):
            rows.append((excel_row, row))
    return rows


def _literal_code(value: Any) -> str:
    if not isinstance(value, str) or not value.strip() or value.lstrip().startswith("="):
        raise CoverageError("INVALID_ACCOUNT_OR_NOTE_CODE")
    return value.strip()


def _closing_decimal(value: Any) -> Decimal:
    if value is None or isinstance(value, bool):
        raise CoverageError("INVALID_CLOSING")
    try:
        amount = Decimal(str(value).strip())
    except (TypeError, ValueError, InvalidOperation) as exc:
        raise CoverageError("INVALID_CLOSING") from exc
    if not amount.is_finite() or (amount != 0 and abs(amount.adjusted()) > 70):
        raise CoverageError("UNSUPPORTED_CLOSING_MAGNITUDE")
    return amount


def _assert_visible(sheet: Any) -> None:
    if sheet.sheet_state != "visible":
        raise CoverageError("HIDDEN_INPUT")
    if any(item.hidden for item in sheet.row_dimensions.values()):
        raise CoverageError("HIDDEN_INPUT")
    if any(item.hidden for item in sheet.column_dimensions.values()):
        raise CoverageError("HIDDEN_INPUT")
    if sheet.merged_cells.ranges:
        raise CoverageError("MERGED_INPUT")


def preview_mapping_coverage(
    content: bytes, *, company_code: str, fiscal_year: int
) -> CoveragePreview:
    """Inspect one explicit company/year in a structurally valid Pilot workbook.

    Only unique mapping rows marked Approved+Valid *inside the untrusted file*
    contribute to a CANDIDATE closing-exposure grouping. Ambiguous, missing
    and non-approved mappings stay blocked. No financial statement is created.
    """
    if not isinstance(company_code, str) or not company_code.strip():
        raise CoverageError("COMPANY_SCOPE_REQUIRED")
    if type(fiscal_year) is not int or fiscal_year <= 0:
        raise CoverageError("FISCAL_YEAR_SCOPE_REQUIRED")
    if not isinstance(content, bytes) or not 0 < len(content) <= MAX_INPUT_BYTES:
        raise CoverageError("WORKBOOK_SIZE_INVALID")
    _guard_archive(content)

    try:
        preflight = preflight_pilot_workbook(content)
    except Exception as exc:
        raise CoverageError("WORKBOOK_INVALID") from exc
    if not preflight.valid:
        raise CoverageError("WORKBOOK_INVALID")

    scope = (company_code.strip(), fiscal_year)

    def scoped(row: dict[str, Any]) -> bool:
        return (
            isinstance(row.get("company_code"), str)
            and row["company_code"].strip() == scope[0]
            and type(row.get("fiscal_year")) is int
            and row["fiscal_year"] == scope[1]
        )

    try:
        book = load_workbook(BytesIO(content), read_only=False, data_only=False,
                             keep_links=False)
    except Exception as exc:
        raise CoverageError("WORKBOOK_INVALID") from exc

    try:
        for name in ("Company", "Accounts", "Notes", "Mapping"):
            if name not in book:
                raise CoverageError("WORKBOOK_INVALID")
            sheet = book[name]
            _assert_visible(sheet)
            headers = tuple(cell.value for cell in sheet[1])
            if headers != SHEET_HEADERS[name]:
                raise CoverageError("WORKBOOK_INVALID")

        company_rows = [
            row for _, row in _read_rows(book["Company"], SHEET_HEADERS["Company"])
            if scoped(row)
        ]
        if len(company_rows) != 1:
            raise CoverageError("COMPANY_SCOPE_NOT_FOUND")
        status = str(company_rows[0]["status"])

        accounts: dict[str, tuple[int, dict[str, Any], Decimal]] = {}
        for excel_row, row in _read_rows(book["Accounts"], SHEET_HEADERS["Accounts"]):
            if not scoped(row):
                continue
            code = _literal_code(row["account_full_code"])
            if code in accounts:
                raise CoverageError("DUPLICATE_ACCOUNT")
            accounts[code] = (excel_row, row, _closing_decimal(row["closing"]))
        if not accounts:
            raise CoverageError("NO_ACCOUNTS_IN_SCOPE")

        note_keys = {
            (
                str(row["statement"]).strip(),
                str(row["statement_section"]).strip(),
                _literal_code(row["note_number"]),
                row["subnote_code"].strip() if isinstance(row["subnote_code"], str) else "",
            )
            for _, row in _read_rows(book["Notes"], SHEET_HEADERS["Notes"])
            if scoped(row)
        }

        mappings: dict[str, list[tuple[int, dict[str, Any]]]] = defaultdict(list)
        for excel_row, row in _read_rows(book["Mapping"], SHEET_HEADERS["Mapping"]):
            if not scoped(row):
                continue
            code = _literal_code(row["account_full_code"])
            if code not in accounts:
                raise CoverageError("UNKNOWN_MAPPING_ACCOUNT")
            mappings[code].append((excel_row, row))

        exceptions: list[CoverageException] = []
        traces: list[AccountTrace] = []
        grouped: dict[tuple[str, str, str, str], list[tuple[str, Decimal]]] = defaultdict(list)
        eligible: list[Decimal] = []
        blocked: list[Decimal] = []
        all_amounts: list[Decimal] = []

        for code in sorted(accounts):
            excel_row, source, closing = accounts[code]
            all_amounts.append(closing)
            matches = mappings.get(code, [])
            candidate = False
            target: tuple[str, str, str, str] | None = None
            mapping_row: int | None = None
            mapping_id: str | None = None
            if not matches:
                exceptions.append(CoverageException("UNMAPPED_ACCOUNT", code, excel_row, ()))
            elif len(matches) != 1:
                exceptions.append(CoverageException(
                    "AMBIGUOUS_ACCOUNT_MAPPING", code, excel_row,
                    tuple(number for number, _ in matches),
                ))
            else:
                mapping_row, mapping = matches[0]
                mapping_id = _literal_code(mapping["mapping_id"])
                if (mapping["approval_status"] != "Approved"
                        or mapping["validation_status"] != "Valid"):
                    exceptions.append(CoverageException(
                        "MAPPING_NOT_FILE_MARKED_APPROVED", code, excel_row,
                        (mapping_row,),
                    ))
                else:
                    target = (
                        str(mapping["target_statement"]).strip(),
                        str(mapping["statement_section"]).strip(),
                        _literal_code(mapping["note_number"]),
                        mapping["subnote_code"].strip()
                        if isinstance(mapping["subnote_code"], str) else "",
                    )
                    if target not in note_keys:
                        raise CoverageError("UNKNOWN_MAPPING_NOTE")
                    grouped[target].append((code, closing))
                    candidate = True
            (eligible if candidate else blocked).append(closing)
            traces.append(AccountTrace(
                account_code=code, account_name=str(source["account_name"]),
                account_excel_row=excel_row, source_row=int(source["source_row"]),
                closing_exposure=str(closing), mapping_excel_row=mapping_row,
                mapping_id=mapping_id,
                target_statement=target[0] if target else None,
                target_section=target[1] if target else None,
                target_note=target[2] if target else None,
                target_subnote=target[3] if target else None,
                included=candidate,
            ))

        # Exact decimal aggregation, including mixed tiny and huge balances.
        positive_digits = max(1, *(amount.adjusted() + 1 for amount in all_amounts if amount))
        fractional_digits = max(0, *(-amount.as_tuple().exponent for amount in all_amounts))
        precision = max(100, positive_digits + fractional_digits + len(str(len(all_amounts))) + 4)
        with localcontext() as ctx:
            ctx.prec = precision
            source_total = sum(all_amounts, Decimal(0))
            eligible_total = sum(eligible, Decimal(0))
            blocked_total = sum(blocked, Decimal(0))
            if source_total != eligible_total + blocked_total:
                raise CoverageError("COVERAGE_RECONCILIATION_FAILED")
            note_results = tuple(
                NoteExposure(
                    statement=key[0], section=key[1],
                    note_number=key[2], subnote_code=key[3],
                    closing_exposure=str(sum(
                        (amount for _, amount in grouped[key]), Decimal(0)
                    )),
                    account_codes=tuple(code for code, _ in grouped[key]),
                )
                for key in sorted(grouped)
            )

        return CoveragePreview(
            company_code=scope[0], fiscal_year=fiscal_year,
            source_sha256=sha256(content).hexdigest(),
            workbook_company_status=status, account_count=len(accounts),
            candidate_mapped_accounts=len(eligible), blocked_accounts=len(blocked),
            source_closing_exposure=str(source_total),
            candidate_closing_exposure=str(eligible_total),
            blocked_closing_exposure=str(blocked_total),
            notes=note_results, accounts=tuple(traces),
            exceptions=tuple(sorted(
                exceptions, key=lambda entry: (entry.account_code, entry.code)
            )),
        )
    finally:
        book.close()
