# NovaPay Digital Bank - Zero-Downtime Database Migration Blueprint

This strategy outlines the structural pattern for managing high-volume data modifications at the persistent storage layer for NovaPay Digital Bank without triggering transaction locking or system degradation.

---

## 1. The Expand-Contract Database Schema Migration Pattern

To ensure continuous transactional availability for the `customer_profiles` table (100M+ rows), all schema modifications must be decoupled into three independent, non-breaking execution horizons:

```mermaid
chronology
    title Database Schema Transformation Pipeline Phase Execution Windows
    box Expand Phase : Application V(N-1) and V(N) share compatible baseline fields safely
    box Migrate Phase : Throttled batch job handles backfill processing asynchronously
    box Contract Phase : Irreversible step drops old structural columns entirely
```

### Three-Step Operational Blueprint

#### I. EXPAND PHASE (Backward-Compatible Schema Adjustments)
* **Execution Goal:** Introduce new data components without altering structural dependencies used by the current active code.
* **Application Behavior:** Application versions \(V(N-1)\) and \(V(N)\) operate against this schema seamlessly.
* **Lock Elimination Pattern:** Indexes must be constructed using the `CONCURRENTLY` parameter to prevent write-blocking across transaction queues.

#### II. MIGRATE PHASE (Asynchronous Batch Data Backfilling)
* **Execution Goal:** Synchronize historical data rows into the new database fields safely.
* **Throttling Framework:** Migration jobs process rows via throttled batch intervals (`LIMIT 1000`) followed by a standard operational sleep interval (`pg_sleep(0.1)`).
* **Automatic Abort Criterion:** If the backfill runtime inflates core application query latency by more than **20%**, the pipeline aborts the operation instantly and routes a priority notification alert to the on-call Database Administrator (DBA).

#### III. CONTRACT PHASE (Structural Simplification and Cleanup)
* **Execution Goal:** Remove legacy database components once all services have migrated to the updated software layers.
* **Governance Gate:** This step is completely **irreversible** and requires an independent Change Advisory Board (CAB) layout override verification checklist.

---

## 2. Version Schema Compatibility Matrix

| Phase Vector | Target Schema Version | App Version \(V(N-1)\) Behavior | App Version \(V(N)\) Behavior | System Rollback Blueprint |
| :--- | :--- | :--- | :--- | :--- |
| **1. Expand** | `V2.0_expand.sql` | Reads and writes old database fields safely; ignores new table slots. | Writes duplicate data parameters into both structural fields. | Drop newly initialized field elements via instantaneous `ALTER TABLE` statement. |
| **2. Migrate**| `V2.1_migrate.sql` | Fully functional; immune to throttled batch processes running underneath. | Reads and updates active row entities using new properties. | Halt execution script; no data loss since existing fields remain active. |
| **3. Contract**| `V2.2_contract.sql`| **Unsupported.** Execution parameters completely incompatible. | Full native functionality; reads and writes exclusive to new table fields. | **Forward-Only Vector.** Restore database state using point-in-time recovery logs. |

---

## 3. Regulatory Compliance Control Mappings
* **RBI Master Direction Sec 4.2:** Standardizes strict dual-approval verification thresholds for persistent data alterations.
* **PCI-DSS v4.0 Req 6.5:** Guarantees comprehensive environment parity checks before introducing data model transformations to the production environment.
