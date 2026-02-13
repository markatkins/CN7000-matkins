# Reports/Packet_Taxonomy Folder Reorganization

## TL;DR

> **Quick Summary**: Reorganize `reports/packet_taxonomy/` from a flat directory into structured subfolders: `status_report/`, `technical_report/`, each with an `archive/` subfolder. Move draft/backup files to archive.
> 
> **Deliverables**:
> - `reports/packet_taxonomy/status_report/` with status report files
> - `reports/packet_taxonomy/status_report/archive/` (empty, .gitkeep)
> - `reports/packet_taxonomy/technical_report/` with technical report files
> - `reports/packet_taxonomy/technical_report/archive/` with draft/backup files
> - Updated cross-references in `analysis/packet_taxonomy/WORK_ITEMS.md` and `reports/packet_taxonomy/ualink-1.5-datamodel-update-session-report.md`
> 
> **Estimated Effort**: Quick
> **Parallel Execution**: NO — sequential (moves then reference updates)
> **Critical Path**: Task 1 → Task 2 → Task 3

---

## Context

### Original Request
Reorganize the `reports/packet_taxonomy` folder. Status report and technical report files should be in sub-folders (`status_report/` and `technical_report/`). Each should also have an `archive/` folder.

### Interview Summary
**Key Decisions**:
- Draft/backup files (`technical_report_ue_draft.pptx`, `technical_report_ue.yaml.bak`) → `technical_report/archive/`
- `ualink-1.5-datamodel-update-session-report.md` stays at top level (not moved)
- Archive folders get draft/backup files moved into them (not left empty)

---

## Work Objectives

### Core Objective
Restructure `reports/packet_taxonomy/` from flat layout to organized subfolders.

### Current Layout
```
reports/packet_taxonomy/
├── ualink-1.5-datamodel-update-session-report.md   ← STAYS HERE
├── status_report.yaml
├── status_report.pptx
├── technical_report.yaml
├── technical_report.pptx
├── technical_report_cornelis.yaml
├── technical_report_cornelis.pptx
├── technical_report_ethernet.yaml
├── technical_report_ethernet.pptx
├── technical_report_roce.yaml
├── technical_report_roce.pptx
├── technical_report_ualink.yaml
├── technical_report_ualink.pptx
├── technical_report_ue.yaml
├── technical_report_ue.pptx
├── technical_report_ue.yaml.bak                     ← ARCHIVE
└── technical_report_ue_draft.pptx                   ← ARCHIVE
```

### Target Layout
```
reports/packet_taxonomy/
├── ualink-1.5-datamodel-update-session-report.md
├── status_report/
│   ├── status_report.yaml
│   ├── status_report.pptx
│   └── archive/
│       └── .gitkeep
└── technical_report/
    ├── technical_report.yaml
    ├── technical_report.pptx
    ├── technical_report_cornelis.yaml
    ├── technical_report_cornelis.pptx
    ├── technical_report_ethernet.yaml
    ├── technical_report_ethernet.pptx
    ├── technical_report_roce.yaml
    ├── technical_report_roce.pptx
    ├── technical_report_ualink.yaml
    ├── technical_report_ualink.pptx
    ├── technical_report_ue.yaml
    ├── technical_report_ue.pptx
    └── archive/
        ├── technical_report_ue.yaml.bak
        └── technical_report_ue_draft.pptx
```

### Must NOT Have (Guardrails)
- Do NOT rename any files — only move them
- Do NOT modify file contents (except updating path references in other files)
- Do NOT move `ualink-1.5-datamodel-update-session-report.md`

---

## Verification Strategy

### Test Decision
- **Automated tests**: None (file reorganization)
- **Verification**: `ls -R reports/packet_taxonomy/` confirms target layout

---

## TODOs

- [x] 1. Create directories and move files with `git mv`

  **What to do**:
  - Create the target directory structure:
    ```bash
    mkdir -p reports/packet_taxonomy/status_report/archive
    mkdir -p reports/packet_taxonomy/technical_report/archive
    ```
  - Move status report files:
    ```bash
    git mv reports/packet_taxonomy/status_report.yaml reports/packet_taxonomy/status_report/
    git mv reports/packet_taxonomy/status_report.pptx reports/packet_taxonomy/status_report/
    ```
  - Create `.gitkeep` in `status_report/archive/` (it has no files to move there):
    ```bash
    touch reports/packet_taxonomy/status_report/archive/.gitkeep
    git add reports/packet_taxonomy/status_report/archive/.gitkeep
    ```
  - Move technical report files:
    ```bash
    git mv reports/packet_taxonomy/technical_report.yaml reports/packet_taxonomy/technical_report/
    git mv reports/packet_taxonomy/technical_report.pptx reports/packet_taxonomy/technical_report/
    git mv reports/packet_taxonomy/technical_report_cornelis.yaml reports/packet_taxonomy/technical_report/
    git mv reports/packet_taxonomy/technical_report_cornelis.pptx reports/packet_taxonomy/technical_report/
    git mv reports/packet_taxonomy/technical_report_ethernet.yaml reports/packet_taxonomy/technical_report/
    git mv reports/packet_taxonomy/technical_report_ethernet.pptx reports/packet_taxonomy/technical_report/
    git mv reports/packet_taxonomy/technical_report_roce.yaml reports/packet_taxonomy/technical_report/
    git mv reports/packet_taxonomy/technical_report_roce.pptx reports/packet_taxonomy/technical_report/
    git mv reports/packet_taxonomy/technical_report_ualink.yaml reports/packet_taxonomy/technical_report/
    git mv reports/packet_taxonomy/technical_report_ualink.pptx reports/packet_taxonomy/technical_report/
    git mv reports/packet_taxonomy/technical_report_ue.yaml reports/packet_taxonomy/technical_report/
    git mv reports/packet_taxonomy/technical_report_ue.pptx reports/packet_taxonomy/technical_report/
    ```
  - Move draft/backup files to archive:
    ```bash
    git mv reports/packet_taxonomy/technical_report_ue.yaml.bak reports/packet_taxonomy/technical_report/archive/
    git mv reports/packet_taxonomy/technical_report_ue_draft.pptx reports/packet_taxonomy/technical_report/archive/
    ```

  **Must NOT do**:
  - Do NOT rename any files
  - Do NOT move `ualink-1.5-datamodel-update-session-report.md`

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: [`git-master`]
    - `git-master`: git mv operations, staging

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Sequential (must complete before Task 2)
  - **Blocks**: Tasks 2, 3
  - **Blocked By**: None

  **References**:
  - Current directory listing above (17 files total)

  **Acceptance Criteria**:
  - [x] `ls reports/packet_taxonomy/status_report/` shows `status_report.yaml`, `status_report.pptx`, `archive/`
  - [x] `ls reports/packet_taxonomy/status_report/archive/` shows `.gitkeep`
  - [x] `ls reports/packet_taxonomy/technical_report/` shows 12 files (6 .yaml + 6 .pptx) plus `archive/`
  - [x] `ls reports/packet_taxonomy/technical_report/archive/` shows `technical_report_ue.yaml.bak`, `technical_report_ue_draft.pptx`
  - [x] `ls reports/packet_taxonomy/` shows only: `ualink-1.5-datamodel-update-session-report.md`, `status_report/`, `technical_report/`
  - [x] `git status` shows all moves as renamed (not delete+add)

  **Commit**: YES
  - Message: `refactor: reorganize reports/packet_taxonomy into status_report/ and technical_report/ subfolders`
  - Files: All moved files
  - Pre-commit: `ls -R reports/packet_taxonomy/`

- [x] 2. Update cross-references in WORK_ITEMS.md

  **What to do**:
  - Edit `analysis/packet_taxonomy/WORK_ITEMS.md` to update 3 path references:
    - Line 637: `reports/packet_taxonomy/status_report.yaml` → `reports/packet_taxonomy/status_report/status_report.yaml`
    - Line 638: `reports/packet_taxonomy/status_report.pptx` → `reports/packet_taxonomy/status_report/status_report.pptx`
    - Line 650: Update both `--data` and `--output` paths in the generation command to include `status_report/` subfolder

  **Must NOT do**:
  - Do NOT change any content other than the file paths

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: [`git-master`]

  **Parallelization**:
  - **Can Run In Parallel**: YES — with Task 3
  - **Parallel Group**: Wave 2 (with Task 3)
  - **Blocks**: None
  - **Blocked By**: Task 1

  **References**:
  - `analysis/packet_taxonomy/WORK_ITEMS.md` lines 637-650 — the 3 lines containing `reports/packet_taxonomy/status_report` paths

  **Acceptance Criteria**:
  - [x] `grep -n 'reports/packet_taxonomy/status_report' analysis/packet_taxonomy/WORK_ITEMS.md` shows updated paths with `status_report/` subfolder
  - [x] No other lines in the file were modified

  **Commit**: YES (group with Task 3)
  - Message: `docs: update report paths after reorganization`
  - Files: `analysis/packet_taxonomy/WORK_ITEMS.md`, `reports/packet_taxonomy/ualink-1.5-datamodel-update-session-report.md`

- [x] 3. Update cross-references in session report

  **What to do**:
  - Edit `reports/packet_taxonomy/ualink-1.5-datamodel-update-session-report.md` to update 2 path references:
    - Line 362: `reports/packet_taxonomy/technical_report_ualink.yaml` → `reports/packet_taxonomy/technical_report/technical_report_ualink.yaml`
    - Line 363: `reports/packet_taxonomy/status_report.yaml` → `reports/packet_taxonomy/status_report/status_report.yaml`

  **Must NOT do**:
  - Do NOT change any content other than the file paths

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: [`git-master`]

  **Parallelization**:
  - **Can Run In Parallel**: YES — with Task 2
  - **Parallel Group**: Wave 2 (with Task 2)
  - **Blocks**: None
  - **Blocked By**: Task 1

  **References**:
  - `reports/packet_taxonomy/ualink-1.5-datamodel-update-session-report.md` lines 362-363 — the 2 lines containing report paths

  **Acceptance Criteria**:
  - [x] `grep -n 'reports/packet_taxonomy/technical_report' reports/packet_taxonomy/ualink-1.5-datamodel-update-session-report.md` shows updated path with `technical_report/` subfolder
  - [x] `grep -n 'reports/packet_taxonomy/status_report' reports/packet_taxonomy/ualink-1.5-datamodel-update-session-report.md` shows updated path with `status_report/` subfolder

  **Commit**: YES (group with Task 2)
  - Message: `docs: update report paths after reorganization`

---

## Commit Strategy

| After Task | Message | Files | Verification |
|------------|---------|-------|--------------|
| 1 | `refactor: reorganize reports/packet_taxonomy into status_report/ and technical_report/ subfolders` | All 17 moved files + .gitkeep | `ls -R reports/packet_taxonomy/` |
| 2+3 | `docs: update report paths after reorganization` | WORK_ITEMS.md + session-report.md | `grep 'reports/packet_taxonomy' analysis/packet_taxonomy/WORK_ITEMS.md` |

---

## Success Criteria

### Verification Commands
```bash
ls -R reports/packet_taxonomy/   # Expected: 3 items at top level, subfolders populated correctly
grep -rn 'reports/packet_taxonomy/' analysis/packet_taxonomy/WORK_ITEMS.md  # Expected: updated paths
```

### Final Checklist
- [x] Flat files moved to correct subfolders
- [x] Draft/backup files in `technical_report/archive/`
- [x] `status_report/archive/.gitkeep` exists
- [x] Session report stays at top level
- [x] All cross-references updated
- [x] No files renamed, only moved
- [x] Git history preserved (git mv, not delete+add)
