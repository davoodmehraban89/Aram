"""Bounded, read-only source-detail rows for the ARAM desktop review."""
from __future__ import annotations

from dataclasses import dataclass

from aram_backend.coverage_preview import CoverageError
from aram_backend.desktop_five_statement_integrity import validate_desktop_pipeline_result
from aram_backend.five_statement_pipeline import FiveStatementPipelineResult
from aram_backend.reconciliation_review import _money

MAX_DETAIL_ROWS = 75_000


@dataclass(frozen=True)
class PreviewDetail:
    statement: str
    item: str
    reference: str
    source_detail: str
    opening_or_source: str
    debit_or_inflow: str
    credit_or_outflow: str
    movement: str
    closing_or_presentation: str
    trace: str
    state: str

    def values(self) -> tuple[str, ...]:
        return (
            self.statement, self.item, self.reference, self.source_detail,
            self.opening_or_source, self.debit_or_inflow, self.credit_or_outflow,
            self.movement, self.closing_or_presentation, self.trace, self.state,
        )


def _text(value: object, label: str, *, blank_ok: bool = False) -> str:
    if (not isinstance(value, str) or len(value) > 1024
            or value != value.strip() or (not value and not blank_ok)
            or any(ord(char) < 32 or ord(char) == 127 for char in value)):
        raise CoverageError("DESKTOP_DETAIL_" + label + "_INVALID")
    return value


def _note_reference(section: object, note: object, subnote: object) -> str:
    section_text = _text(section, "SECTION")
    note_text = _text(note, "NOTE")
    subnote_text = _text(subnote, "SUBNOTE", blank_ok=True)
    parts = [section_text, "یادداشت " + note_text]
    if subnote_text:
        parts.append("زیرعنوان " + subnote_text)
    return " / ".join(parts)


def _amount(value: object, label: str) -> str:
    try:
        return format(_money(value), ",f")
    except CoverageError as exc:
        raise CoverageError("DESKTOP_DETAIL_" + label + "_INVALID") from exc


def _optional_amount(value: object, label: str) -> str:
    if value is None:
        return ""
    return _amount(value, label)


def _row(
    statement: str, item: object, reference: object, source_detail: object,
    opening: object = None, debit: object = None, credit: object = None,
    movement: object = None, closing: object = None, trace: object = "",
    state: str = "", source_amount: bool = False,
) -> PreviewDetail:
    source_value = (
        _amount(source_detail, "SOURCE") if source_amount
        else _text(source_detail, "SOURCE", blank_ok=True)
    )
    return PreviewDetail(
        statement=_text(statement, "STATEMENT"),
        item=_text(item, "ITEM"),
        reference=_text(reference, "REFERENCE", blank_ok=True),
        source_detail=source_value,
        opening_or_source=_optional_amount(opening, "OPENING"),
        debit_or_inflow=_optional_amount(debit, "DEBIT"),
        credit_or_outflow=_optional_amount(credit, "CREDIT"),
        movement=_optional_amount(movement, "MOVEMENT"),
        closing_or_presentation=_optional_amount(closing, "CLOSING"),
        trace=_text(trace, "TRACE", blank_ok=True),
        state=state,
    )


def build_preview_details(
    result: FiveStatementPipelineResult,
) -> tuple[PreviewDetail, ...]:
    """Expose source/presentation detail without changing or exporting inputs."""
    validate_desktop_pipeline_result(result)
    state = (
        "قابل بررسی؛ غیررسمی" if result.eligible_for_analyst_review
        else "مسدود؛ صرفاً تشخیصی"
    )
    rows: list[PreviewDetail] = []

    for line in result.balance_sheet.lines:
        rows.append(_row(
            "ترازنامه", line.line_label,
            _note_reference(line.statement_section, line.note_number, line.subnote_code),
            line.source_closing_exposure, closing=line.presentation_amount,
            source_amount=True,
            trace=(
                f"دسته: {line.category} | ضریب: {line.sign_multiplier} | "
                f"مرجع: {line.note_reference_evidence} | سیاست: {line.policy_evidence_ref}"
            ),
            state=state,
        ))
    for line in result.income_statement.lines:
        rows.append(_row(
            "سود و زیان", line.line_label,
            _note_reference(line.statement_section, line.note_number, line.subnote_code),
            line.source_closing_exposure, closing=line.presentation_amount,
            trace=(
                f"دسته: {line.category} | ضریب: {line.sign_multiplier} | "
                f"مرجع: {line.note_reference_evidence} | سیاست: {line.policy_evidence_ref}"
            ),
            state=state,
        ))
    for line in result.equity_changes.note_movements:
        rows.append(_row(
            "تغییرات حقوق مالکانه", line.line_label,
            _note_reference(line.statement_section, line.note_number, line.subnote_code),
            line.source_closing_exposure, opening=line.opening_balance,
            source_amount=True,
            movement=line.movement_amount, closing=line.closing_balance,
            trace=(
                f"جزء: {line.equity_component} | نوع تغییر: {line.movement_category} | "
                f"مرجع: {line.note_reference_evidence} | سیاست: {line.policy_evidence_ref}"
            ),
            state=state,
        ))
    for line in result.equity_changes.account_movements:
        rows.append(_row(
            "تغییرات حقوق مالکانه", line.account_name,
            f"حساب {line.account_code} / " + _note_reference(
                line.statement_section, line.note_number, line.subnote_code,
            ),
            f"ردیف اکسل {line.source_excel_row} / ردیف منبع {line.source_row}",
            opening=line.opening_balance, debit=line.debit_turnover,
            credit=line.credit_turnover, movement=line.movement_amount,
            closing=line.closing_balance,
            trace=(
                f"جزء: {line.equity_component} | نوع تغییر: {line.movement_category} | "
                f"سیاست: {line.policy_evidence_ref}"
            ),
            state=state,
        ))
    for line in result.cash_flow.cash_flow_lines:
        rows.append(_row(
            "جریان وجوه نقد", line.activity,
            f"شناسه ردیف {line.line_id} / سند {line.transaction_id}",
            f"تاریخ {line.posting_date} / حساب نقد {line.cash_account_code}",
            debit=line.cash_inflow, credit=line.cash_outflow,
            trace=(
                f"طرف مقابل: {line.counterpart_account_code} | "
                f"سند: {line.source_evidence_ref} | "
                f"طبقه‌بندی: {line.classification_evidence_ref or 'ندارد'}"
            ),
            state=state,
        ))
    for account in result.cash_flow.account_reconciliations:
        rows.append(_row(
            "جریان وجوه نقد", account.account_name,
            f"حساب نقد {account.account_code}",
            f"ردیف منبع {account.source_row}",
            opening=account.opening_balance,
            debit=account.source_debit_turnover,
            credit=account.source_credit_turnover,
            movement=account.rollforward_difference,
            closing=account.closing_balance,
            trace=(
                f"گردش بدهکار اسناد: {account.transaction_debit_turnover} | "
                f"گردش بستانکار اسناد: {account.transaction_credit_turnover} | "
                f"سیاست: {account.policy_evidence_ref}"
            ),
            state=state,
        ))
    for account in result.trial_balance.accounts:
        rows.append(_row(
            "تراز آزمایشی", account.account_name,
            f"کد حساب {account.account_code}",
            f"ردیف اکسل {account.excel_row} / ردیف منبع {account.source_row}",
            opening=account.opening, debit=account.debit, credit=account.credit,
            movement=account.debit_net_movement, closing=account.closing,
            state=state,
        ))
    if len(rows) > MAX_DETAIL_ROWS:
        raise CoverageError("DESKTOP_DETAIL_ROW_LIMIT_EXCEEDED")
    return tuple(rows)
