"""Conservative mapping ambiguity report; never infers approval from a workbook."""
from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable
from dataclasses import dataclass

from aram_backend.mapping_workflow import MappingDecision, MappingWorkflowError


@dataclass(frozen=True)
class MappingQuality:
    company_code: str
    fiscal_year: int
    unmapped_accounts: tuple[str, ...]
    pending_accounts: tuple[str, ...]
    conflicting_accounts: tuple[str, ...]
    approved_accounts: tuple[str, ...]

    @property
    def ready(self) -> bool:
        return not (self.unmapped_accounts or self.pending_accounts or self.conflicting_accounts)


def assess_mapping_quality(
    accounts: Iterable[str], decisions: Iterable[MappingDecision], *,
    company_code: str, fiscal_year: int,
) -> MappingQuality:
    """Classify all accounts; never silently select between conflicting mappings."""
    if not company_code.strip() or isinstance(fiscal_year, bool) or fiscal_year <= 0:
        raise MappingWorkflowError("invalid quality scope")
    codes = tuple(accounts)
    if any(not isinstance(code, str) or not code.strip() for code in codes):
        raise MappingWorkflowError("invalid account code")
    grouped: dict[str, list[MappingDecision]] = defaultdict(list)
    for d in decisions:
        if (d.company_code, d.fiscal_year) != (company_code, fiscal_year):
            raise MappingWorkflowError("foreign mapping in quality assessment")
        if d.account_full_code not in codes:
            raise MappingWorkflowError("mapping references unknown account")
        grouped[d.account_full_code].append(d)
    unmapped, pending, conflicting, approved = [], [], [], []
    for code in sorted(set(codes)):
        mappings = grouped[code]
        if not mappings:
            unmapped.append(code)
        elif len(mappings) > 1:
            conflicting.append(code)
        elif mappings[0].status != "Approved":
            pending.append(code)
        else:
            approved.append(code)
    return MappingQuality(company_code, fiscal_year, tuple(unmapped),
                          tuple(pending), tuple(conflicting), tuple(approved))
