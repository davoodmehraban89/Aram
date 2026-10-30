from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict, Field, StrictInt, StrictStr
from aram_backend.authenticated_identity import VerifiedPrincipal, require_verified_principal
from sqlalchemy.orm import Session
from aram_backend.database import get_session
from aram_backend.mapping_year_authorization import require_year_access
from aram_backend.mapping_batch_review import ProposedMappingRow, preview_mapping_batch
from aram_backend.authored_mapping_draft import (
    MappingAuthorConflict, stage_authored_unreviewed_batch,
)
from aram_backend.mapping_service import MappingValidationError

from aram_backend import __version__
from aram_backend.config import get_settings
from aram_backend.models import FiscalYearStatus, StatementType
from aram_backend.schemas import EntityDescriptor, EnumCatalog, HealthResponse, SchemaCatalog

settings = get_settings()
app = FastAPI(title=settings.app_name, version=__version__)


@app.get("/api/v1/auth/me", tags=["identity"])
def authenticated_identity(
    principal: VerifiedPrincipal = Depends(require_verified_principal),
) -> dict[str, object]:
    """Read-only proof of a verified token; no Mapping decision is made."""
    return {
        "issuer": principal.issuer,
        "subject": principal.subject,
        "roles": list(principal.roles),
        "expires_at": principal.expires_at,
    }


@app.get("/api/v1/auth/year-access/{year_id}", tags=["identity"])
def authenticated_year_access(
    year_id: int,
    principal: VerifiedPrincipal = Depends(require_verified_principal),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    """Read-only company/year role preflight; NOT approval or apply authority."""
    role = principal.roles[0]
    grant = require_year_access(
        session, principal=principal, year_id=year_id,
        required_role=role,
    )
    return {
        "year_id": year_id,
        "company_code": grant.company_code,
        "fiscal_year": grant.fiscal_year,
        "role": grant.role,
        "verified_scope": True,
    }


class MappingStagingRow(BaseModel):
    model_config = ConfigDict(extra="forbid")
    source_locator: StrictStr
    rule_key: StrictStr
    account_code: StrictStr
    target_note_id: StrictInt
    mapping_type: StrictStr
    expected_base_version: StrictInt


class MappingStagingRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    year_id: StrictInt = Field(gt=0)
    request_key: StrictStr
    rows: list[MappingStagingRow] = Field(min_length=1, max_length=10000)


@app.post("/api/v1/mapping/unreviewed-drafts", status_code=201, tags=["mapping"])
def stage_unreviewed_mapping_proposal(
    request: MappingStagingRequest,
    principal: VerifiedPrincipal = Depends(require_verified_principal),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    """Verified signer+year-scoped proposal staging; NEVER a financial apply.

    All three records (draft, system staging event, signed author evidence)
    are committed together or rolled back together. Request-supplied actor
    identity is forbidden by the strict body model.
    """
    try:
        with session.begin():
            # Security order: check company/year scope BEFORE even classifying
            # user-supplied Mapping data, to avoid cross-entity information leaks.
            require_year_access(
                session, principal=principal, year_id=request.year_id,
                required_role="mapping_proposer",
            )
            snapshot = preview_mapping_batch(
                session, year_id=request.year_id,
                rows=tuple(
                    ProposedMappingRow(**row.model_dump()) for row in request.rows
                ),
            )
            saved = stage_authored_unreviewed_batch(
                session, snapshot=snapshot, request_key=request.request_key,
                principal=principal,
            )
        return {
            "draft_id": saved.id, "year_id": saved.year_id,
            "state": saved.state, "request_key": saved.request_key,
        }
    except MappingAuthorConflict as exc:
        raise HTTPException(
            status_code=409, detail="Mapping proposal request identity conflict"
        ) from exc
    except MappingValidationError as exc:
        raise HTTPException(status_code=422, detail="Invalid Mapping proposal") from exc


@app.get("/api/v1/health", response_model=HealthResponse, tags=["system"])
def health() -> HealthResponse:
    return HealthResponse(status="ok", service=settings.app_name, version=__version__)


@app.get("/api/v1/schema/entities", response_model=SchemaCatalog, tags=["schema"])
def schema_entities() -> SchemaCatalog:
    return SchemaCatalog(entities=[
        EntityDescriptor(name="Company", table="companies", purpose="Legal/reporting entity"),
        EntityDescriptor(name="FiscalYear", table="fiscal_years", purpose="Isolated approval and lock boundary"),
        EntityDescriptor(name="SourceDocument", table="source_documents", purpose="Immutable source metadata"),
        EntityDescriptor(name="AccountVersion", table="account_versions", purpose="Year-specific account versions"),
        EntityDescriptor(name="MappingRule", table="mapping_rules", purpose="Versioned note mapping proposals/rules"),
        EntityDescriptor(name="NoteDefinition", table="note_definitions", purpose="Versioned disclosure definitions"),
        EntityDescriptor(name="NoteRow", table="note_rows", purpose="Ordered disclosure rows"),
        EntityDescriptor(name="FinancialStatement", table="financial_statements", purpose="Versioned primary statements"),
        EntityDescriptor(name="StatementLine", table="statement_lines", purpose="Ordered statement lines"),
    ])


@app.get("/api/v1/schema/enums", response_model=EnumCatalog, tags=["schema"])
def schema_enums() -> EnumCatalog:
    return EnumCatalog(
        fiscal_year_statuses=[item.value for item in FiscalYearStatus],
        statement_types=[item.value for item in StatementType],
    )

