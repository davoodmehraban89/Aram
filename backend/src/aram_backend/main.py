from fastapi import Depends, FastAPI
from aram_backend.authenticated_identity import VerifiedPrincipal, require_verified_principal
from sqlalchemy.orm import Session
from aram_backend.database import get_session
from aram_backend.mapping_year_authorization import require_year_access

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

