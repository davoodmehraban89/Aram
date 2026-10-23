/*
Aram / Peyvast: metadata-only discovery aid for a DBA.
Target syntax: Microsoft SQL Server 2019 / 2022.

UNEXECUTED: this file has received static content/syntax review only.
It has NOT been run against SQL Server, a test instance, or a customer database.
It is not a connector and makes no claim about the customer's Peyvast schema.

In SSMS, select the intended customer database before running this script.
Use the customer's approved read-only identity. This script does not switch
databases, query application/financial rows, or alter data, objects, permissions,
or server/database settings. Every executable statement is a metadata SELECT.

Metadata visibility depends on the executing identity's permissions. Results
may be incomplete or empty. Empty output is NOT evidence that an object, key,
relationship, or column does not exist. Do not share credentials. Metadata can
identify a customer; redact output consistently before sharing if needed.

Documentation basis: Microsoft SQL Server documentation, including
SERVERPROPERTY, sys.columns joined to sys.types, and metadata visibility:
https://learn.microsoft.com/en-us/sql/t-sql/functions/serverproperty-transact-sql
https://learn.microsoft.com/en-us/sql/relational-databases/system-catalog-views/sys-columns-transact-sql
https://learn.microsoft.com/en-us/sql/relational-databases/security/metadata-visibility-configuration
*/

-- 1. Engine version and edition reported by the connected SQL Server instance.
SELECT
    CONVERT(nvarchar(128), SERVERPROPERTY('ProductVersion')) AS product_version,
    CONVERT(nvarchar(128), SERVERPROPERTY('ProductMajorVersion')) AS product_major_version,
    CONVERT(nvarchar(128), SERVERPROPERTY('ProductLevel')) AS product_level,
    CONVERT(nvarchar(128), SERVERPROPERTY('ProductUpdateLevel')) AS product_update_level,
    CONVERT(nvarchar(128), SERVERPROPERTY('Edition')) AS edition,
    CONVERT(int, SERVERPROPERTY('EngineEdition')) AS engine_edition;

-- 2. Only the currently selected database and its compatibility/collation.
SELECT
    DB_NAME() AS current_database_name,
    DB_ID() AS current_database_id,
    d.compatibility_level,
    d.collation_name
FROM sys.databases AS d
WHERE d.database_id = DB_ID();

-- 3. Visible user tables and views in the current database.
SELECT
    s.name AS schema_name,
    o.name AS object_name,
    o.object_id,
    o.type_desc AS object_type
FROM sys.objects AS o
INNER JOIN sys.schemas AS s
    ON s.schema_id = o.schema_id
WHERE o.type IN ('U', 'V')
    AND o.is_ms_shipped = 0
ORDER BY s.name, o.name, o.object_id;

-- 4. Visible column definitions for those tables and views.
-- max_length is in bytes; -1 denotes a MAX/large-value type where applicable.
-- declared_type preserves alias/CLR type identity; base_type may be NULL.
SELECT
    s.name AS schema_name,
    o.name AS object_name,
    o.type_desc AS object_type,
    c.column_id,
    c.name AS column_name,
    ts.name AS declared_type_schema,
    ut.name AS declared_type,
    bt.name AS base_type,
    c.max_length AS max_length_bytes,
    c.precision AS numeric_precision,
    c.scale AS numeric_scale,
    c.is_nullable,
    c.is_identity,
    c.is_computed,
    c.collation_name
FROM sys.columns AS c
INNER JOIN sys.objects AS o
    ON o.object_id = c.object_id
INNER JOIN sys.schemas AS s
    ON s.schema_id = o.schema_id
INNER JOIN sys.types AS ut
    ON ut.user_type_id = c.user_type_id
INNER JOIN sys.schemas AS ts
    ON ts.schema_id = ut.schema_id
LEFT JOIN sys.types AS bt
    ON bt.system_type_id = c.system_type_id
    AND bt.user_type_id = bt.system_type_id
WHERE o.type IN ('U', 'V')
    AND o.is_ms_shipped = 0
ORDER BY s.name, o.name, c.column_id;

-- 5. Declared primary/unique keys and other unique indexes, one row per key
-- column in key order. Included non-key columns are intentionally omitted.
-- Flags distinguish PK/UQ constraints from standalone unique indexes.
-- A filtered or disabled unique index must not be assumed to identify all rows.
SELECT
    s.name AS schema_name,
    o.name AS object_name,
    o.type_desc AS object_type,
    i.name AS index_name,
    kc.name AS constraint_name,
    kc.type_desc AS constraint_type,
    i.is_primary_key,
    i.is_unique_constraint,
    i.is_unique,
    i.has_filter,
    i.is_disabled,
    i.is_hypothetical,
    ic.key_ordinal,
    c.name AS column_name,
    ic.is_descending_key
FROM sys.indexes AS i
INNER JOIN sys.objects AS o
    ON o.object_id = i.object_id
INNER JOIN sys.schemas AS s
    ON s.schema_id = o.schema_id
INNER JOIN sys.index_columns AS ic
    ON ic.object_id = i.object_id
    AND ic.index_id = i.index_id
INNER JOIN sys.columns AS c
    ON c.object_id = ic.object_id
    AND c.column_id = ic.column_id
LEFT JOIN sys.key_constraints AS kc
    ON kc.parent_object_id = i.object_id
    AND kc.unique_index_id = i.index_id
WHERE o.type IN ('U', 'V')
    AND o.is_ms_shipped = 0
    AND i.is_unique = 1
    AND ic.key_ordinal > 0
ORDER BY s.name, o.name, i.name, ic.key_ordinal;

-- 6. Declared foreign keys only, one row per paired column in FK order.
-- This does not infer undeclared relationships or accounting semantics.
SELECT
    ps.name AS parent_schema,
    pt.name AS parent_table,
    fk.name AS foreign_key_name,
    fkc.constraint_column_id AS column_pair_ordinal,
    pc.name AS parent_column,
    rs.name AS referenced_schema,
    rt.name AS referenced_table,
    rc.name AS referenced_column,
    fk.is_disabled,
    fk.is_not_trusted,
    fk.delete_referential_action_desc,
    fk.update_referential_action_desc
FROM sys.foreign_keys AS fk
INNER JOIN sys.foreign_key_columns AS fkc
    ON fkc.constraint_object_id = fk.object_id
INNER JOIN sys.tables AS pt
    ON pt.object_id = fkc.parent_object_id
INNER JOIN sys.schemas AS ps
    ON ps.schema_id = pt.schema_id
INNER JOIN sys.columns AS pc
    ON pc.object_id = fkc.parent_object_id
    AND pc.column_id = fkc.parent_column_id
INNER JOIN sys.tables AS rt
    ON rt.object_id = fkc.referenced_object_id
INNER JOIN sys.schemas AS rs
    ON rs.schema_id = rt.schema_id
INNER JOIN sys.columns AS rc
    ON rc.object_id = fkc.referenced_object_id
    AND rc.column_id = fkc.referenced_column_id
WHERE pt.is_ms_shipped = 0
    AND rt.is_ms_shipped = 0
ORDER BY ps.name, pt.name, fk.name, fkc.constraint_column_id;
