-- Contract phase: run only after all application versions use email_v2.
-- Precondition: backfill is complete and verified; old-version compatibility is retired.
-- SQLite 3.40.0 supports DROP COLUMN.
ALTER TABLE customers DROP COLUMN email;
