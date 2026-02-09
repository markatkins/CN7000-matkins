# Document Synchronization Consolidation

## TL;DR

> **Quick Summary**: Consolidate work tracking into WORK_ITEMS.md, update DATAMODEL_UPDATES.md with missing history, and sync document index.
> 
> **Deliverables**:
> - Updated `WORK_ITEMS.md` with all open/deferred items
> - Updated `DATAMODEL_UPDATES.md` with W-10 through W-14 history
> - Updated `packet_taxonomy.md` Document Index
> - Consistent "Last Updated" dates across all files
> 
> **Estimated Effort**: Short (1-2 hours)
> **Parallel Execution**: YES - Tasks 1-3 can run in parallel, Task 4 after
> **Critical Path**: Tasks 1,2,3 (parallel) → Task 4

---

## Context

### Original Request
User requested Option A consolidation with 4 tasks:
1. Consolidate WORK_ITEMS.md with all open/deferred items from packet_taxonomy.md Section 5
2. Update DATAMODEL_UPDATES.md with W-10 through W-14 change history
3. Update packet_taxonomy.md Document Index with new packet_taxonomy_ue_tagged_send_variants.md
4. Add "Last Updated" consistency across all files

### Research Findings

**Open/Deferred Items to migrate** (from packet_taxonomy.md Section 5.1):
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

**Missing from DATAMODEL_UPDATES.md**:
- W-10 series: CMS enumerations (2026-01-27)
- W-11 series: RoCE BTH/AETH updates (2026-01-27)
- W-12 series: RoCE cross-references (2026-01-27-28)
- W-13 series: Ethernet metadata and RSS (2026-01-28)
- W-14 series: UALink expansion (2026-01-29-30)

---

## Work Objectives

### Core Objective
Establish WORK_ITEMS.md as the single source of truth for active work tracking, with proper synchronization to related documents.

### Concrete Deliverables
1. `WORK_ITEMS.md` - Complete with all open/deferred items (~5-10KB)
2. `DATAMODEL_UPDATES.md` - Complete history through W-14
3. `packet_taxonomy.md` - Updated Document Index
4. All files with consistent "Last Updated: 2026-02-02" dates

### Definition of Done
- [ ] WORK_ITEMS.md contains all open/deferred items from packet_taxonomy.md
- [ ] DATAMODEL_UPDATES.md contains W-10 through W-14 entries
- [ ] packet_taxonomy.md Document Index includes packet_taxonomy_ue_tagged_send_variants.md
- [ ] All 4 files have consistent Last Updated date

### Must Have
- All open work items migrated to WORK_ITEMS.md
- Clear archive reference in WORK_ITEMS.md pointing to packet_taxonomy.md Section 5
- W-10 through W-14 change history in DATAMODEL_UPDATES.md

### Must NOT Have (Guardrails)
- Do NOT delete closed items from packet_taxonomy.md (keep as archive)
- Do NOT duplicate closed items in WORK_ITEMS.md
- Do NOT modify datamodel files

---

## Verification Strategy

### Automated Verification

```bash
# Task 1: Verify WORK_ITEMS.md has open items
grep -c "W-06-001\|W-07-003\|W-09-009\|W-10-013\|W-11-009\|D-001" analysis/packet_taxonomy/WORK_ITEMS.md
# Assert: >= 5

# Task 2: Verify DATAMODEL_UPDATES.md has W-10 through W-14
grep -c "W-10\|W-11\|W-12\|W-13\|W-14" analysis/packet_taxonomy/DATAMODEL_UPDATES.md
# Assert: >= 10

# Task 3: Verify Document Index has new doc
grep -c "packet_taxonomy_ue_tagged_send_variants.md" analysis/packet_taxonomy/packet_taxonomy.md
# Assert: >= 1

# Task 4: Verify consistent dates
grep -c "2026-02-02" analysis/packet_taxonomy/WORK_ITEMS.md analysis/packet_taxonomy/DATAMODEL_UPDATES.md analysis/packet_taxonomy/packet_taxonomy.md
# Assert: >= 3
```

---

## Execution Strategy

### Parallel Execution Waves

```
Wave 1 (Start Immediately):
├── Task 1: Consolidate WORK_ITEMS.md
├── Task 2: Update DATAMODEL_UPDATES.md
└── Task 3: Update packet_taxonomy.md Document Index

Wave 2 (After Wave 1):
└── Task 4: Update Last Updated dates
```

---

## TODOs

- [x] 1. Consolidate WORK_ITEMS.md with open/deferred items

  **What to do**:
  - Rewrite WORK_ITEMS.md with complete structure:
    - Open Work Items section (active tasks)
    - Deferred Work Items section (low priority)
    - Datamodel Gaps section (D-001 through D-003)
    - Specification Questions section (Q1)
    - Recently Closed section (W-14 series summary)
    - Archive Reference (pointer to packet_taxonomy.md Section 5)
  - Migrate all open/deferred items from packet_taxonomy.md Section 5.1

  **Items to include**:
  - W-06-001: UFH-32 entropy (Deferred)
  - W-07-003: ue_plus.ksy Length units (Investigation)
  - W-09-009: PMR Ethernet vs UE+ rules (Pending)
  - W-09-010: UFH UEC standardization (Deferred)
  - W-10-007 through W-10-012: CMS stubs (Deferred)
  - W-10-013: CC_TYPE extensions (Investigation)
  - W-10-015: nscc_source.ksy review (Pending)
  - W-11-009: IB Spec 2.0 review (Pending)
  - W-15: CN7000 PPT comparison (Open)
  - D-001 through D-003: Datamodel gaps
  - Q1: Lightweight Interface Scope

  **Must NOT do**:
  - Do NOT include closed items (keep in packet_taxonomy.md)

  **Recommended Agent Profile**:
  - **Category**: `writing`
  - **Skills**: `[]`

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Tasks 2, 3)
  - **Blocks**: Task 4
  - **Blocked By**: None

  **References**:
  - `analysis/packet_taxonomy/packet_taxonomy.md:180-300` - Section 5 Work List
  - `analysis/packet_taxonomy/WORK_ITEMS.md` - Current file to rewrite

  **Acceptance Criteria**:
  ```bash
  grep -c "W-06-001\|W-07-003\|W-09-009\|W-10-013\|W-11-009\|D-001\|W-15" analysis/packet_taxonomy/WORK_ITEMS.md
  # Assert: >= 6
  ```

  **Commit**: NO (grouped with Task 4)

---

- [x] 2. Update DATAMODEL_UPDATES.md with W-10 through W-14

  **What to do**:
  - Add Section 2.10: CMS Enumerations and Expansions (W-10 series, 2026-01-27)
  - Add Section 2.11: RoCE BTH/AETH Updates (W-11 series, 2026-01-27)
  - Add Section 2.12: RoCE Cross-References (W-12 series, 2026-01-27-28)
  - Add Section 2.13: Ethernet Metadata and RSS (W-13 series, 2026-01-28)
  - Add Section 2.14: UALink Expansion (W-14 series, 2026-01-29-30)

  **Content source**:
  - packet_taxonomy.md Section 5.1 has work item descriptions
  - analysis/ualink/ualink_issues.md has W-14 details

  **Must NOT do**:
  - Do NOT duplicate existing entries (2.1-2.9)

  **Recommended Agent Profile**:
  - **Category**: `writing`
  - **Skills**: `[]`

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Tasks 1, 3)
  - **Blocks**: Task 4
  - **Blocked By**: None

  **References**:
  - `analysis/packet_taxonomy/packet_taxonomy.md:209-286` - W-10 through W-14 details
  - `analysis/packet_taxonomy/DATAMODEL_UPDATES.md` - Current file to extend
  - `analysis/ualink/ualink_issues.md` - W-14 UALink details

  **Acceptance Criteria**:
  ```bash
  grep -c "### 2.10\|### 2.11\|### 2.12\|### 2.13\|### 2.14" analysis/packet_taxonomy/DATAMODEL_UPDATES.md
  # Assert: >= 5
  ```

  **Commit**: NO (grouped with Task 4)

---

- [x] 3. Update packet_taxonomy.md Document Index

  **What to do**:
  - Add `packet_taxonomy_ue_tagged_send_variants.md` to Section 3 Document Index
  - Add entry in "Ultra Ethernet+ (UE+) Formats" table
  - Update Document Relationships diagram

  **Entry to add**:
  ```markdown
  | [packet_taxonomy_ue_tagged_send_variants.md](packet_taxonomy_ue_tagged_send_variants.md) | Tagged-Send Variants | UE Standard, CSIG, IPv4, TSS, Small, Rendezvous, Deferrable | `ue/transport/` |
  ```

  **Must NOT do**:
  - Do NOT modify Section 5 Work List (keep as archive)

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: `[]`

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Tasks 1, 2)
  - **Blocks**: Task 4
  - **Blocked By**: None

  **References**:
  - `analysis/packet_taxonomy/packet_taxonomy.md:83-91` - UE+ Formats table

  **Acceptance Criteria**:
  ```bash
  grep -c "packet_taxonomy_ue_tagged_send_variants.md" analysis/packet_taxonomy/packet_taxonomy.md
  # Assert: >= 1
  ```

  **Commit**: NO (grouped with Task 4)

---

- [x] 4. Update Last Updated dates for consistency

  **What to do**:
  - Update WORK_ITEMS.md header: Last Updated: 2026-02-02
  - Update DATAMODEL_UPDATES.md header: Last Updated: 2026-02-02
  - Update packet_taxonomy.md header: Last Reviewed: 2026-02-02

  **Must NOT do**:
  - Do NOT change other header fields

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: `[]`

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Wave 2 (after Tasks 1-3)
  - **Blocks**: None
  - **Blocked By**: Tasks 1, 2, 3

  **Acceptance Criteria**:
  ```bash
  grep "2026-02-02" analysis/packet_taxonomy/WORK_ITEMS.md analysis/packet_taxonomy/DATAMODEL_UPDATES.md analysis/packet_taxonomy/packet_taxonomy.md | wc -l
  # Assert: >= 3
  ```

  **Commit**: YES
  - Message: `docs(taxonomy): consolidate work tracking and sync documents`
  - Files: `WORK_ITEMS.md`, `DATAMODEL_UPDATES.md`, `packet_taxonomy.md`

---

## Success Criteria

### Final Checklist
- [x] WORK_ITEMS.md contains all open/deferred items
- [x] WORK_ITEMS.md has archive reference to packet_taxonomy.md Section 5
- [x] DATAMODEL_UPDATES.md has sections 2.10-2.14
- [x] packet_taxonomy.md Document Index includes tagged_send_variants doc
- [x] All files have consistent dates (2026-02-03)

**Status**: COMPLETE (verified 2026-02-03)
