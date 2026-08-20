from pydantic import BaseModel, ConfigDict


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str


class EntityDescriptor(BaseModel):
    name: str
    table: str
    purpose: str


class SchemaCatalog(BaseModel):
    model_config = ConfigDict(frozen=True)
    entities: list[EntityDescriptor]


class EnumCatalog(BaseModel):
    fiscal_year_statuses: list[str]
    statement_types: list[str]

