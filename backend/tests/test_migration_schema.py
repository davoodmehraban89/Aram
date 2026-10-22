"""Validate explicit Alembic DDL against the actual SQLAlchemy models.

Runs on a disposable in-memory SQLite database only; never touches canonical data.
"""

from alembic.migration import MigrationContext
from alembic.operations import Operations
from sqlalchemy import create_engine, inspect

from aram_backend.database import Base
from aram_backend import models  # noqa: F401


def test_explicit_migration_schema_matches_metadata():
    # Import via path because the revision filename begins with digits.
    import importlib.util
    from pathlib import Path

    path = Path(__file__).parents[1] / "migrations" / "versions" / "20260820_01_initial_schema.py"
    spec = importlib.util.spec_from_file_location("aram_initial_migration", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    engine = create_engine("sqlite:///:memory:")
    with engine.connect() as connection:
        context = MigrationContext.configure(connection)
        operations = Operations(context)
        original = module.op
        module.op = operations
        try:
            module.upgrade()
            inspector = inspect(connection)
            assert set(inspector.get_table_names()) == set(Base.metadata.tables)
            for table in Base.metadata.tables.values():
                actual = {c["name"]: c for c in inspector.get_columns(table.name)}
                assert set(actual) == {c.name for c in table.columns}, table.name
                for column in table.columns:
                    assert actual[column.name]["nullable"] == column.nullable, (table.name, column.name)
                expected_unique = {
                    tuple(c.columns.keys()) for c in table.constraints
                    if c.__class__.__name__ == "UniqueConstraint"
                }
                actual_unique = {tuple(c["column_names"]) for c in inspector.get_unique_constraints(table.name)}
                assert expected_unique <= actual_unique, table.name
                expected_indexes = {
                    (tuple(idx.columns.keys()), bool(idx.unique)) for idx in table.indexes
                }
                actual_indexes = {
                    (tuple(idx["column_names"]), bool(idx["unique"]))
                    for idx in inspector.get_indexes(table.name)
                }
                assert expected_indexes == actual_indexes, table.name
                expected_fks = {
                    (tuple(fk.column_keys), tuple(col.name for col in fk.elements),
                     fk.referred_table.name)
                    for fk in table.foreign_key_constraints
                }
                actual_fks = {
                    (tuple(fk["constrained_columns"]), tuple(fk["referred_columns"]),
                     fk["referred_table"])
                    for fk in inspector.get_foreign_keys(table.name)
                }
                assert expected_fks == actual_fks, table.name
            module.downgrade()
            assert inspect(connection).get_table_names() == []
        finally:
            module.op = original
