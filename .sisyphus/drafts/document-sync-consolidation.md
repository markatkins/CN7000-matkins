# Draft: Document Synchronization Consolidation

## Requirements (confirmed)
- Option A: WORK_ITEMS.md as primary work tracking
- 4 tasks to execute:
  1. Consolidate WORK_ITEMS.md with all open/deferred items from packet_taxonomy.md Section 5
  2. Update DATAMODEL_UPDATES.md with W-10 through W-14 change history
  3. Update packet_taxonomy.md Document Index with new packet_taxonomy_ue_tagged_send_variants.md
  4. Add "Last Updated" consistency across all files

## Technical Decisions
- WORK_ITEMS.md becomes primary for active work tracking
- packet_taxonomy.md Section 5 becomes historical archive (read-only)
- Standardize date format: YYYY-MM-DD
- Target WORK_ITEMS.md size: 5-10KB

## Research Findings

### Open/Deferred Items from packet_taxonomy.md Section 5

**Open Items**:
- W-06-001: UFH-32 entropy field (Deferred)
- W-07-003: ue_plus.ksy Length field units (Investigation)
- W-09-009: PMR standard Ethernet vs UE+ header rules (Pending)
- W-09-010: UFH headers when UEC standardizes (Deferred)
- W-10-007 through W-10-012: CMS algorithm stubs (Deferred)
- W-10-013: CC_TYPE proprietary extensions (Investigation)
- W-10-015: nscc_source.ksy review (Pending)
- W-11-009: IB Spec 2.0 review (Pending)
- D-001 through D-003: Datamodel gaps (Spec Update)
- Q1: Lightweight Interface Scope (Investigation)

**W-15**: Already in WORK_ITEMS.md (CN7000 PPT comparison)

### Missing from DATAMODEL_UPDATES.md (W-10 through W-14)
- W-10-001 through W-10-006: CMS enumerations and expansions (2026-01-27)
- W-10-014: ack_cc_state_rccc_tfc.ksy fix (2026-01-27)
- W-11-001 through W-11-008: RoCE BTH/AETH updates (2026-01-27)
- W-12-001 through W-12-018: RoCE cross-references (2026-01-27-28)
- W-13-001 through W-13-021: Ethernet metadata and RSS (2026-01-28)
- W-14-001 through W-14-011: UALink expansion (2026-01-29-30)

## Scope Boundaries
- INCLUDE: All open/deferred work items, missing DATAMODEL_UPDATES entries, document index update
- EXCLUDE: Closed work items (keep in packet_taxonomy.md as archive)
