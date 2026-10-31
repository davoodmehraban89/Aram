"""Exact, read-only figures for the Windows analyst preview."""
from __future__ import annotations
from dataclasses import dataclass
from aram_backend.coverage_preview import CoverageError
from aram_backend.five_statement_pipeline import FiveStatementPipelineResult
from aram_backend.reconciliation_review import _money
from aram_backend.desktop_five_statement_integrity import validate_desktop_pipeline_result

@dataclass(frozen=True)
class PreviewFigure:
    statement: str
    label: str
    value: str
    state: str

SPECS = (
    ("balance_sheet", "ترازنامه", "دارایی‌ها", "assets_total"),
    ("balance_sheet", "ترازنامه", "بدهی‌ها", "liabilities_total"),
    ("balance_sheet", "ترازنامه", "حقوق مالکانه", "equity_total"),
    ("balance_sheet", "ترازنامه", "اختلاف", "balance_difference"),
    ("income_statement", "سود و زیان", "درآمد", "revenue_total"),
    ("income_statement", "سود و زیان", "بهای تمام‌شده", "cost_of_revenue_total"),
    ("income_statement", "سود و زیان", "سود ناخالص", "gross_profit"),
    ("income_statement", "سود و زیان", "سود عملیاتی", "operating_profit"),
    ("income_statement", "سود و زیان", "سود قبل از مالیات", "profit_before_tax"),
    ("income_statement", "سود و زیان", "مالیات", "tax_expense_total"),
    ("income_statement", "سود و زیان", "سود خالص", "net_result"),
    ("equity_changes", "تغییرات حقوق مالکانه", "اول دوره", "opening_equity_total"),
    ("equity_changes", "تغییرات حقوق مالکانه", "تغییر دوره", "total_movement"),
    ("equity_changes", "تغییرات حقوق مالکانه", "سود دوره", "net_profit_loss_movements"),
    ("equity_changes", "تغییرات حقوق مالکانه", "پایان دوره", "closing_equity_total"),
    ("cash_flow", "جریان نقد", "نقد اول دوره", "opening_cash_and_equivalents"),
    ("cash_flow", "جریان نقد", "عملیاتی", "operating_net_cash_flow"),
    ("cash_flow", "جریان نقد", "سرمایه‌گذاری", "investing_net_cash_flow"),
    ("cash_flow", "جریان نقد", "تأمین مالی", "financing_net_cash_flow"),
    ("cash_flow", "جریان نقد", "تغییر نقد", "net_change_in_cash"),
    ("cash_flow", "جریان نقد", "نقد پایان دوره", "closing_cash_and_equivalents"),
    ("trial_balance", "تراز آزمایشی", "افتتاحیه خالص", "opening_debit_net_total"),
    ("trial_balance", "تراز آزمایشی", "گردش بدهکار", "debit_turnover_total"),
    ("trial_balance", "تراز آزمایشی", "گردش بستانکار", "credit_turnover_total"),
    ("trial_balance", "تراز آزمایشی", "اختتامیه خالص", "closing_debit_net_total"),
    ("reconciliation", "تطبیق", "اختلاف حقوق مالکانه", "balance_sheet_equity_difference"),
    ("reconciliation", "تطبیق", "اختلاف سود", "net_profit_equity_difference"),
    ("reconciliation", "تطبیق", "اختلاف نقد", "balance_sheet_cash_difference"),
)

def build_preview_figures(result: FiveStatementPipelineResult) -> tuple[PreviewFigure, ...]:
    validate_desktop_pipeline_result(result)
    if any((
        result.official_financial_statement, result.accounting_policy_authorized,
        result.independently_reviewed, result.export_authorized, result.releasable,
        result.reconciliation.official_financial_statement,
        result.reconciliation.releasable,
    )):
        raise CoverageError("DESKTOP_FIGURES_FALSE_APPROVAL")
    if type(result.eligible_for_analyst_review) is not bool:
        raise CoverageError("DESKTOP_FIGURES_INVALID_ELIGIBILITY")
    state = (
        "پیش‌نویس قابل بررسی؛ غیررسمی" if result.eligible_for_analyst_review
        else "مسدود؛ مبالغ صرفاً تشخیصی"
    )
    return tuple(
        PreviewFigure(
            statement, label, format(_money(getattr(getattr(result, part), field)), ",f"),
            state,
        )
        for part, statement, label, field in SPECS
    )
