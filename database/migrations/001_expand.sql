-- Expand phase: add a new nullable column without removing old columns.
ALTER TABLE customers ADD COLUMN email_v2 TEXT;
