from fastapi import FastAPI

from aram_backend import __version__
from aram_backend.config import get_settings
from aram_backend.models import FiscalYearStatus, StatementType, MappingStatus
from aram_backend.schemas import EntityDescriptor, EnumCatalog, HealthResponse, SchemaCatalog

settings = get_settings()
app = FastAPI(title=settings.app_name, version=__version__)


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
        mapping_statuses=[item.value for item in MappingStatus],
    )

