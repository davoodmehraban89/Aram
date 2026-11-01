from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable, Iterator, Mapping
from dataclasses import dataclass
from decimal import Decimal, localcontext

from aram_backend.ledger_parser import LedgerRecord
from aram_backend.mapping_source_parser import MappingSourceRow


DIMENSION_HEADERS = ("T1_CODE", "جاری / سرمایه ای", "T4_CODE")
DEFAULT_EXCLUDED_ACCOUNT_CODES = frozenset({"8999"})


class MappingMatchError(ValueError):
    """Raised when source mapping dimensions are missing or malformed."""


@dataclass(frozen=True)
class MappingRule:
    source_row: int
    account_code: str
    mapping_type: str
    note_code: str
    note_description: str
    dimensions: tuple[tuple[str, str | None], ...]

    @property
    def dimension_map(self) -> Mapping[str, str | None]:
        return dict(self.dimensions)


@dataclass(frozen=True)
class LedgerMappingResult:
    ledger_row: int
    account_code: str
    status: str
    matching_mapping_rows: tuple[int, ...]
    closing: Decimal


@dataclass(frozen=True)
class MappingCoverageSummary:
    total_source_rows: int
    eligible_rows: int
    excluded_rows: int
    unique_rows: int
    ambiguous_rows: int
    unmapped_rows: int
    source_closing: Decimal
    eligible_closing: Decimal
    unique_closing: Decimal
    ambiguous_closing: Decimal
    unmapped_closing: Decimal

    @property
    def any_match_rows(self) -> int:
        return self.unique_rows + self.ambiguous_rows


def build_mapping_rules(
    rows: Iterable[MappingSourceRow],
    *,
    dimension_headers: tuple[str, ...] = DIMENSION_HEADERS,
) -> tuple[MappingRule, ...]:
    """Convert parsed mapping source rows into explicit wildcard-capable rules.

    Blank mapping dimensions are wildcards. A populated rule dimension must
    equal the corresponding ledger dimension after whitespace trimming.
    A populated mapping dimension never matches a missing ledger dimension.
    No ranking, precedence, formula execution, or approval is inferred.
    """
    rules: list[MappingRule] = []
    for row in rows:
        raw = dict(row.source_values)
        legacy_dimension = "جاري / سرمایه ای"
        canonical_dimension = "جاری / سرمایه ای"
        if legacy_dimension in raw and canonical_dimension in raw:
            legacy_value = _dimension_value(raw[legacy_dimension], row.row_number, legacy_dimension)
            canonical_value = _dimension_value(raw[canonical_dimension], row.row_number, canonical_dimension)
            if legacy_value != canonical_value:
                raise MappingMatchError(
                    f"mapping row {row.row_number}: conflicting current/capital dimension aliases"
                )
        elif legacy_dimension in raw:
            raw[canonical_dimension] = raw[legacy_dimension]
        missing = set(dimension_headers).difference(raw)
        if missing:
            raise MappingMatchError(
                f"mapping row {row.row_number}: missing dimension headers {sorted(missing)}"
            )
        dimensions = tuple(
            (header, _dimension_value(raw[header], row.row_number, header))
            for header in dimension_headers
        )
        rules.append(
            MappingRule(
                source_row=row.row_number,
                account_code=row.account_code,
                mapping_type=row.mapping_type,
                note_code=row.note_code,
                note_description=row.note_description,
                dimensions=dimensions,
            )
        )
    return tuple(rules)


def classify_ledger_rows(
    ledger_rows: Iterable[LedgerRecord],
    mapping_rules: Iterable[MappingRule],
    *,
    excluded_account_codes: frozenset[str] = DEFAULT_EXCLUDED_ACCOUNT_CODES,
) -> Iterator[LedgerMappingResult]:
    """Stream each ledger row into unique, ambiguous, unmapped, or excluded.

    Mapping rows are indexed by account. Each nonblank rule dimension is an
    exact constraint; each blank rule dimension is an explicit wildcard.
    Multiple matching source rows remain ambiguous, including duplicate rules.
    """
    by_account: dict[str, list[MappingRule]] = defaultdict(list)
    for rule in mapping_rules:
        by_account[rule.account_code].append(rule)

    for ledger in ledger_rows:
        if ledger.account_code in excluded_account_codes:
            yield LedgerMappingResult(
                ledger_row=ledger.row_number,
                account_code=ledger.account_code,
                status="EXCLUDED",
                matching_mapping_rows=(),
                closing=ledger.closing,
            )
            continue

        matches = tuple(
            rule.source_row
            for rule in by_account.get(ledger.account_code, ())
            if _matches(ledger, rule)
        )
        status = (
            "UNMAPPED" if not matches
            else "UNIQUE" if len(matches) == 1
            else "AMBIGUOUS"
        )
        yield LedgerMappingResult(
            ledger_row=ledger.row_number,
            account_code=ledger.account_code,
            status=status,
            matching_mapping_rows=matches,
            closing=ledger.closing,
        )


def summarize_mapping_coverage(
    results: Iterable[LedgerMappingResult],
) -> MappingCoverageSummary:
    """Aggregate row counts and closing exposure without rounding."""
    counts = {"EXCLUDED": 0, "UNIQUE": 0, "AMBIGUOUS": 0, "UNMAPPED": 0}
    amounts = {key: Decimal(0) for key in counts}
    total_rows = 0
    source_closing = Decimal(0)
    with localcontext() as context:
        context.prec = 1000
        for result in results:
            if result.status not in counts:
                raise MappingMatchError(f"unknown result status: {result.status}")
            total_rows += 1
            source_closing += result.closing
            counts[result.status] += 1
            amounts[result.status] += result.closing
        eligible_closing = source_closing - amounts["EXCLUDED"]

    return MappingCoverageSummary(
        total_source_rows=total_rows,
        eligible_rows=total_rows - counts["EXCLUDED"],
        excluded_rows=counts["EXCLUDED"],
        unique_rows=counts["UNIQUE"],
        ambiguous_rows=counts["AMBIGUOUS"],
        unmapped_rows=counts["UNMAPPED"],
        source_closing=source_closing,
        eligible_closing=eligible_closing,
        unique_closing=amounts["UNIQUE"],
        ambiguous_closing=amounts["AMBIGUOUS"],
        unmapped_closing=amounts["UNMAPPED"],
    )


def _matches(ledger: LedgerRecord, rule: MappingRule) -> bool:
    ledger_dimensions = {
        "T1_CODE": ledger.t1_code,
        "جاری / سرمایه ای": None,
        "T4_CODE": ledger.t4_code,
    }
    for header, rule_value in rule.dimensions:
        if rule_value is None:
            continue
        ledger_value = ledger_dimensions[header]
        if ledger_value is None or ledger_value != rule_value:
            return False
    return True


def _dimension_value(value: object, row_number: int, header: str) -> str | None:
    if value is None:
        return None
    if isinstance(value, bool):
        raise MappingMatchError(
            f"mapping row {row_number}: {header} must be text or a code"
        )
    if isinstance(value, float):
        if not value.is_integer():
            raise MappingMatchError(
                f"mapping row {row_number}: {header} must be an integer code"
            )
        return str(int(value))
    text = str(value).strip()
    return text or None
