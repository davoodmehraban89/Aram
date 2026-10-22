"""Explicit initial Phase 2A schema, reversible without ORM metadata DDL.

Revision ID: 20260820_01
"""
from alembic import op
import sqlalchemy as sa

revision = "20260820_01"
down_revision = None
branch_labels = None
depends_on = None


def timestamps():
    return [sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False)]


def year_fk():
    return sa.Column("year_id", sa.Integer(), sa.ForeignKey("fiscal_years.id", ondelete="RESTRICT"), nullable=False)


def upgrade() -> None:
    op.create_table("companies",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("code", sa.String(64), nullable=False),
        sa.Column("name", sa.String(255), nullable=False), *timestamps(),
        sa.UniqueConstraint("code", name="uq_companies_code"))
    op.create_index("ix_companies_code", "companies", ["code"], unique=True)
    op.create_table("fiscal_years",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("company_id", sa.Integer(), sa.ForeignKey("companies.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("status", sa.Enum("DRAFT", "APPROVED", "LOCKED", name="fiscalyearstatus", native_enum=False), nullable=False),
        *timestamps(), sa.UniqueConstraint("company_id", "year", name="uq_fiscal_year_company_year"),
        sa.CheckConstraint("year > 0", name="ck_fiscal_years_positive_year"))
    op.create_table("source_documents",
        sa.Column("id", sa.Integer(), primary_key=True), year_fk(),
        sa.Column("filename", sa.String(512), nullable=False),
        sa.Column("file_hash", sa.String(128), nullable=False),
        sa.Column("document_type", sa.String(64), nullable=False),
        sa.Column("uploaded_at", sa.DateTime(timezone=True), nullable=False), *timestamps(),
        sa.UniqueConstraint("year_id", "file_hash", name="uq_source_document_year_hash"))
    op.create_index("ix_source_documents_year_id", "source_documents", ["year_id"])
    op.create_table("account_versions",
        sa.Column("id", sa.Integer(), primary_key=True), year_fk(),
        sa.Column("account_code", sa.String(64), nullable=False),
        sa.Column("account_name", sa.String(512), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        *[sa.Column("t" + str(i), sa.String(128)) for i in range(1, 5)],
        sa.Column("nature", sa.String(64)), *timestamps(),
        sa.UniqueConstraint("year_id", "account_code", "version", name="uq_account_year_code_version"),
        sa.CheckConstraint("version > 0", name="ck_account_versions_positive_version"))
    op.create_index("ix_account_versions_year_id", "account_versions", ["year_id"])
    op.create_index("ix_account_versions_account_code", "account_versions", ["account_code"])
    op.create_table("note_definitions",
        sa.Column("id", sa.Integer(), primary_key=True), year_fk(),
        sa.Column("note_number", sa.String(32), nullable=False),
        sa.Column("title", sa.String(512), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("configuration_json", sa.JSON(), nullable=False), *timestamps(),
        sa.UniqueConstraint("year_id", "note_number", "version", name="uq_note_year_number_version"),
        sa.CheckConstraint("version > 0", name="ck_note_definitions_positive_version"))
    op.create_index("ix_note_definitions_year_id", "note_definitions", ["year_id"])
    op.create_table("note_rows",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("note_id", sa.Integer(), sa.ForeignKey("note_definitions.id", ondelete="CASCADE"), nullable=False),
        sa.Column("row_order", sa.Integer(), nullable=False),
        sa.Column("label", sa.String(512), nullable=False),
        sa.Column("formula_logic", sa.Text()), sa.Column("sorting_rule_id", sa.String(128)), *timestamps(),
        sa.UniqueConstraint("note_id", "row_order", name="uq_note_row_order"),
        sa.CheckConstraint("row_order >= 0", name="ck_note_rows_nonnegative_row_order"))
    op.create_index("ix_note_rows_note_id", "note_rows", ["note_id"])
    op.create_table("mapping_rules",
        sa.Column("id", sa.Integer(), primary_key=True), year_fk(),
        sa.Column("rule_key", sa.String(128), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("account_code", sa.String(64), nullable=False),
        sa.Column("target_note_id", sa.Integer(), sa.ForeignKey("note_definitions.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("mapping_type", sa.String(32), nullable=False), *timestamps(),
        sa.UniqueConstraint("year_id", "rule_key", "version", name="uq_mapping_year_key_version"),
        sa.CheckConstraint("version > 0", name="ck_mapping_rules_positive_version"))
    op.create_index("ix_mapping_rules_year_id", "mapping_rules", ["year_id"])
    op.create_index("ix_mapping_rules_account_code", "mapping_rules", ["account_code"])
    op.create_table("financial_statements",
        sa.Column("id", sa.Integer(), primary_key=True), year_fk(),
        sa.Column("statement_type", sa.Enum("BALANCE_SHEET", "INCOME_STATEMENT", "CASH_FLOW", "EQUITY", name="statementtype", native_enum=False), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False), *timestamps(),
        sa.UniqueConstraint("year_id", "statement_type", "version", name="uq_statement_year_type_version"),
        sa.CheckConstraint("version > 0", name="ck_financial_statements_positive_version"))
    op.create_index("ix_financial_statements_year_id", "financial_statements", ["year_id"])
    op.create_table("statement_lines",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("statement_id", sa.Integer(), sa.ForeignKey("financial_statements.id", ondelete="CASCADE"), nullable=False),
        sa.Column("line_order", sa.Integer(), nullable=False),
        sa.Column("line_label", sa.String(512), nullable=False),
        sa.Column("target_note_id", sa.Integer(), sa.ForeignKey("note_definitions.id", ondelete="RESTRICT")),
        sa.Column("mapped_total", sa.Numeric(24, 4)), *timestamps(),
        sa.UniqueConstraint("statement_id", "line_order", name="uq_statement_line_order"),
        sa.CheckConstraint("line_order >= 0", name="ck_statement_lines_nonnegative_line_order"))
    op.create_index("ix_statement_lines_statement_id", "statement_lines", ["statement_id"])


def downgrade() -> None:
    for name in ("statement_lines", "financial_statements", "mapping_rules",
                 "note_rows", "note_definitions", "account_versions",
                 "source_documents", "fiscal_years", "companies"):
        op.drop_table(name)
