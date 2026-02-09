# Reorder HAS Comparison Sections and Archive Previous Review

## TL;DR

> **Quick Summary**: Restructure the HAS vs Datamodel comparison document by moving actionable sections (Recommended Work Items, Summary of Mismatches) before the lengthy Detailed Comparison, and move the archived previous review into an `archive/` subdirectory with all internal references updated.
> 
> **Deliverables**:
> - Reordered `has-datamodel-comparison.md` with Work Items → Mismatches → Detailed Comparison order
> - Archived review moved to `reviews/archive/` subdirectory
> - All internal references (ToC, metadata, Document Structure Rules, Archival Rules) updated
> - Clean conventional commit
> 
> **Estimated Effort**: Quick
> **Parallel Execution**: NO - sequential (each step depends on the previous)
> **Critical Path**: Task 1 → Task 2 → Task 3 → Task 4

---

## Context

### Original Request
User requested four changes to finalize the HAS vs Datamodel comparison document:
1. Reorder sections so Recommended Work Items and Summary of Mismatches appear before Detailed Comparison
2. Move the archived previous review file into an `archive/` subdirectory
3. Update all internal references to reflect both changes
4. Commit everything

### Interview Summary
**Key Discussions**:
- Section reorder: Recommended Work Items FIRST, then Summary of Mismatches, then Detailed Comparison
- Archive path: `reviews/archive/has-datamodel-comparison.YYYYMMDD.md`
- Commit exclusions: Do NOT commit `prompts.md` or `docs/references/IBTA/`

**Research Findings**:
- File is 736 lines, well-structured markdown
- Git working tree is clean, 2 commits ahead of origin/main
- No `archive/` subdirectory exists yet under `reviews/`
- Only 2 files reference the archived filename: the comparison doc itself (4 references) and `prompts.md` (excluded from commit)

### Metis Review
**Identified Gaps** (addressed):
- Section boundary precision: Summary of Mismatches includes "Path Corrections Needed" subsection (lines 457–500) — must move as a unit
- Document Structure Rules numbered list (lines 683–707) must be renumbered to match new order
- Archival Rules (lines 720–724) must mention `archive/` subdirectory
- Use `git mv` (not `mv`) to preserve history
- Line count should be preserved (736 ± 2 lines)

---

## Work Objectives

### Core Objective
Restructure the HAS comparison document for better readability by surfacing actionable content (work items, mismatches) before the lengthy detailed comparison, and organize archived reviews into a dedicated subdirectory.

### Concrete Deliverables
- `datamodel/protocols/working/reviews/has-datamodel-comparison.md` — reordered and reference-updated
- `datamodel/protocols/working/reviews/archive/has-datamodel-comparison.20260206.md` — moved from parent directory
- One git commit capturing both changes

### Definition of Done
- [ ] Recommended Work Items section appears before Summary of Mismatches
- [ ] Summary of Mismatches section appears before Detailed Comparison
- [ ] Archived file exists at `reviews/archive/has-datamodel-comparison.20260206.md`
- [ ] Archived file does NOT exist at `reviews/has-datamodel-comparison.20260206.md`
- [ ] All internal references updated (5 locations)
- [ ] Clean commit with conventional message

### Must Have
- Section order: Work Items → Mismatches → Detailed Comparison
- Archive in `archive/` subdirectory
- All 5 internal reference locations updated
- `git mv` used (not plain `mv`)

### Must NOT Have (Guardrails)
- Do NOT modify content within sections — only move sections and update references
- Do NOT change heading text (markdown anchors depend on it)
- Do NOT stage or commit `datamodel/protocols/working/prompts.md`
- Do NOT stage or commit `docs/references/IBTA/`
- Do NOT touch any file outside `datamodel/protocols/working/reviews/`
- Do NOT add or remove content lines (line count should be 736 ± 2)

---

## Verification Strategy (MANDATORY)

### Test Decision
- **Infrastructure exists**: N/A (documentation task)
- **User wants tests**: Manual-only
- **Framework**: N/A

### Automated Verification (Agent-Executable)

Each TODO includes executable verification commands. All verification is via shell commands — no user intervention required.

---

## Execution Strategy

### Sequential Execution (No Parallelism)

```
Task 1: Create archive/ directory and git mv the archived file
    ↓
Task 2: Reorder sections in has-datamodel-comparison.md
    ↓
Task 3: Update all internal references (ToC, metadata, Document Structure Rules, Archival Rules, Changes section)
    ↓
Task 4: Verify and commit
```

### Dependency Matrix

| Task | Depends On | Blocks | Can Parallelize With |
|------|------------|--------|---------------------|
| 1 | None | 3, 4 | None |
| 2 | None | 3, 4 | 1 (theoretically, but safer sequential) |
| 3 | 1, 2 | 4 | None |
| 4 | 1, 2, 3 | None | None (final) |

### Agent Dispatch Summary

| Task | Recommended Dispatch |
|------|---------------------|
| 1 | `delegate_task(category="quick", load_skills=["git-master"])` |
| 2 | `delegate_task(category="quick", load_skills=[])` |
| 3 | `delegate_task(category="quick", load_skills=[])` |
| 4 | `delegate_task(category="quick", load_skills=["git-master"])` |

---

## TODOs

- [ ] 1. Create archive/ directory and move archived review file

  **What to do**:
  - Create directory `datamodel/protocols/working/reviews/archive/` (if it doesn't exist)
  - Use `git mv` to move `datamodel/protocols/working/reviews/has-datamodel-comparison.20260206.md` to `datamodel/protocols/working/reviews/archive/has-datamodel-comparison.20260206.md`

  **Must NOT do**:
  - Do NOT use plain `mv` (must use `git mv` to preserve history)
  - Do NOT modify the archived file's content

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Single shell command, trivial task
  - **Skills**: [`git-master`]
    - `git-master`: Needed for `git mv` operation

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Sequential (Task 1)
  - **Blocks**: Tasks 3, 4
  - **Blocked By**: None

  **References**:

  **Pattern References**:
  - None needed — standard git operation

  **File References**:
  - `datamodel/protocols/working/reviews/has-datamodel-comparison.20260206.md` — file to move (currently exists here)

  **Acceptance Criteria**:

  ```bash
  # AC1: Archive directory exists
  ls -d earlysim/datamodel/protocols/working/reviews/archive/
  # Assert: exit code 0

  # AC2: File exists in new location
  ls earlysim/datamodel/protocols/working/reviews/archive/has-datamodel-comparison.20260206.md
  # Assert: exit code 0

  # AC3: File does NOT exist in old location
  ls earlysim/datamodel/protocols/working/reviews/has-datamodel-comparison.20260206.md 2>&1
  # Assert: "No such file or directory" (exit code 2)

  # AC4: git status shows rename
  git -C earlysim status --porcelain datamodel/protocols/working/reviews/
  # Assert: Shows "R" (rename) for the file
  ```

  **Commit**: NO (groups with Task 4)

---

- [ ] 2. Reorder sections in has-datamodel-comparison.md

  **What to do**:
  - In `datamodel/protocols/working/reviews/has-datamodel-comparison.md`, move three section blocks:
    1. **Cut** "Recommended Work Items" section (lines 502–555, from `## Recommended Work Items` through the line before `---` + `## KSY File Coverage Matrix`)
    2. **Cut** "Summary of Mismatches" section (lines 457–500, from `## Summary of Mismatches` through the "Path Corrections Needed" subsection, ending before `---` + `## Recommended Work Items`)
    3. **Paste** both sections BEFORE "Detailed Comparison" (currently line 123), in this order:
       - `## Recommended Work Items` (with its `---` separator before it)
       - `## Summary of Mismatches` (with its `---` separator before it)
       - Then `## Detailed Comparison` follows

  - The resulting section order after "Cross-Reference to Existing Work Tracking" should be:
    ```
    ## Recommended Work Items        (was lines 502-555)
    ## Summary of Mismatches         (was lines 457-500, includes Path Corrections Needed)
    ## Detailed Comparison           (was lines 123-454)
    ## KSY File Coverage Matrix      (unchanged)
    ## Changes from Previous Review  (unchanged)
    ## Generation Prompt and Rules   (unchanged)
    ```

  **Must NOT do**:
  - Do NOT modify any content within the sections — only move them
  - Do NOT change any heading text (anchors depend on exact text)
  - Do NOT lose the "Path Corrections Needed" subsection (it's part of Summary of Mismatches)
  - Do NOT add or remove content lines

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Text block move in a single markdown file
  - **Skills**: []
    - No special skills needed — standard file editing

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Sequential (Task 2)
  - **Blocks**: Task 3, 4
  - **Blocked By**: None (but safer after Task 1)

  **References**:

  **File References**:
  - `datamodel/protocols/working/reviews/has-datamodel-comparison.md` — the file being edited
  - Lines 123–454: Detailed Comparison section (stays in place, other sections move before it)
  - Lines 457–500: Summary of Mismatches section (includes "Path Corrections Needed" subsection at line 489)
  - Lines 502–555: Recommended Work Items section

  **Section Boundary Details** (CRITICAL — get these right):
  - Summary of Mismatches starts at line 457 (`## Summary of Mismatches`) and ends at line 499 (last line of Path Corrections table: `| \`datamodel/rdma/\` | \`datamodel/protocols/roce/\` | ❌ NOT TRACKED (also wrong directory name) |`)
  - Line 500 is blank, line 501 is `---`
  - Recommended Work Items starts at line 502 (`## Recommended Work Items`) and ends at line 554 (last line: `Both are important, but they require separate work tracking.`)
  - Line 555 is blank, line 556 is `---`

  **Acceptance Criteria**:

  ```bash
  # AC1: Section order is correct
  grep -n "^## " earlysim/datamodel/protocols/working/reviews/has-datamodel-comparison.md
  # Assert: "Recommended Work Items" line < "Summary of Mismatches" line < "Detailed Comparison" line

  # AC2: Path Corrections Needed is still inside Summary of Mismatches (between Summary heading and next ## heading)
  awk '/^## Summary of Mismatches/,/^## [^#]/' earlysim/datamodel/protocols/working/reviews/has-datamodel-comparison.md | grep "Path Corrections Needed"
  # Assert: Found (exit code 0)

  # AC3: Line count preserved
  wc -l < earlysim/datamodel/protocols/working/reviews/has-datamodel-comparison.md
  # Assert: 736 (± 2 lines acceptable)
  ```

  **Commit**: NO (groups with Task 4)

---

- [ ] 3. Update all internal references

  **What to do**:
  Update 5 reference locations in `has-datamodel-comparison.md` to reflect the section reorder (Task 2) and archive file move (Task 1):

  **3a. Table of Contents (near line 11)**:
  - Reorder the ToC entries to match new section order:
    ```
    - [Executive Summary](#executive-summary)
    - [Overview](#overview)
    - [Cross-Reference to Existing Work Tracking](#cross-reference-to-existing-work-tracking)
    - [Recommended Work Items](#recommended-work-items)          ← moved up
    - [Summary of Mismatches](#summary-of-mismatches)            ← moved up
    - [Detailed Comparison](#detailed-comparison)                 ← moved down
      - [1. UE+ L2 Header ...] (sub-items unchanged)
      - ...
    - [KSY File Coverage Matrix](#ksy-file-coverage-matrix)
    - [Changes from Previous Review ...](#changes-from-previous-review-2026-02-06)
    - [Generation Prompt and Rules](#generation-prompt-and-rules)
    ```
  - Do NOT change anchor text — only reorder the lines

  **3b. Metadata block (line 7)**:
  - Change: `Archived as \`has-datamodel-comparison.20260206.md\` (2026-02-06)`
  - To: `Archived as \`archive/has-datamodel-comparison.20260206.md\` (2026-02-06)`

  **3c. Changes from Previous Review section (around line 580 before reorder)**:
  - Change: `archived review (\`has-datamodel-comparison.20260206.md\`, dated 2026-02-06)`
  - To: `archived review (\`archive/has-datamodel-comparison.20260206.md\`, dated 2026-02-06)`

  **3d. Document Structure Rules (around lines 683–707 before reorder)**:
  - Renumber the section list to reflect new order:
    - 7 → **Recommended Work Items**: Tables grouped by priority (1-4) with Suggested ID, Description, and Rationale columns
    - 8 → **Summary of Mismatches**: Two tables — Critical Issues (❌) and Significant Gaps (⚠️) — with Location, Impact, and Existing Work Item columns
    - 9 → **Path Corrections Needed**: Table of HAS Reference → Correct Path
    - 10 → **Detailed Comparison**: One subsection per protocol area (with existing sub-rules)
    - 11 → **KSY File Coverage Matrix**: Table showing per-family coverage percentages
    - 12 → **Changes from Previous Review**: (existing sub-rules)
    - 13 → **Generation Prompt and Rules**: This section

  **3e. Archival Rules (around lines 720–724 before reorder)**:
  - Update rule 1 to mention `archive/` subdirectory:
    - Change: `archive the current file as \`has-datamodel-comparison.YYYYMMDD.md\``
    - To: `archive the current file to \`archive/has-datamodel-comparison.YYYYMMDD.md\``
  - Add rule about archive subdirectory:
    - `Archives are stored in the \`archive/\` subdirectory of the reviews directory.`
  - Update rule 3 to reference the full archive path:
    - Change: `reference the archived filename`
    - To: `reference the archived filename including the \`archive/\` path prefix`

  **Must NOT do**:
  - Do NOT change heading text (only reorder ToC entries and update reference strings)
  - Do NOT modify content in sections other than the 5 reference locations listed above

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: String replacements in a single file
  - **Skills**: []
    - No special skills needed — standard file editing

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Sequential (Task 3)
  - **Blocks**: Task 4
  - **Blocked By**: Tasks 1, 2

  **References**:

  **File References**:
  - `datamodel/protocols/working/reviews/has-datamodel-comparison.md` — the file being edited
  - Line 7: metadata block with "Previous Review" reference
  - Lines 11–33: Table of Contents
  - Line 580: Changes from Previous Review section header paragraph
  - Lines 683–707: Document Structure Rules numbered list
  - Lines 720–724: Archival Rules

  **Acceptance Criteria**:

  ```bash
  # AC1: Metadata block references archive/ path
  grep "Previous Review" earlysim/datamodel/protocols/working/reviews/has-datamodel-comparison.md | grep "archive/"
  # Assert: Found (exit code 0)

  # AC2: Changes from Previous Review references archive/ path
  grep "has-datamodel-comparison.20260206.md" earlysim/datamodel/protocols/working/reviews/has-datamodel-comparison.md
  # Assert: ALL occurrences contain "archive/" prefix (2 occurrences expected)

  # AC3: ToC order matches section order
  # Extract ToC entries for the 3 reordered sections
  grep -n "Recommended Work Items\|Summary of Mismatches\|Detailed Comparison" earlysim/datamodel/protocols/working/reviews/has-datamodel-comparison.md | head -6
  # Assert: In ToC block (lines <35), order is: Recommended Work Items, Summary of Mismatches, Detailed Comparison

  # AC4: Document Structure Rules reflect new order
  grep -A30 "### Document Structure Rules" earlysim/datamodel/protocols/working/reviews/has-datamodel-comparison.md | grep -E "^\s+[0-9]+\." | head -7
  # Assert: Recommended Work Items item number < Summary of Mismatches item number < Detailed Comparison item number

  # AC5: Archival Rules mention archive/ subdirectory
  grep -A5 "### Archival Rules" earlysim/datamodel/protocols/working/reviews/has-datamodel-comparison.md | grep "archive/"
  # Assert: Found (exit code 0)

  # AC6: No stale references to old archive path (without archive/ prefix)
  grep "has-datamodel-comparison.20260206.md" earlysim/datamodel/protocols/working/reviews/has-datamodel-comparison.md | grep -v "archive/"
  # Assert: No matches (exit code 1) — all references should have archive/ prefix
  ```

  **Commit**: NO (groups with Task 4)

---

- [ ] 4. Verify and commit

  **What to do**:
  - Run all acceptance criteria from Tasks 1–3
  - Stage ONLY files under `datamodel/protocols/working/reviews/` (use `git add -A datamodel/protocols/working/reviews/`)
  - Verify with `git status` that ONLY the intended files are staged (the moved archive file + the edited comparison file)
  - Verify that `prompts.md` and `docs/references/IBTA/` are NOT staged
  - Commit with message: `docs(datamodel): reorder HAS comparison sections and archive previous review`

  **Must NOT do**:
  - Do NOT stage `datamodel/protocols/working/prompts.md`
  - Do NOT stage `docs/references/IBTA/`
  - Do NOT push to remote (user will push when ready)

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Standard git commit operation
  - **Skills**: [`git-master`]
    - `git-master`: Needed for staging and committing

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Sequential (Task 4 — final)
  - **Blocks**: None
  - **Blocked By**: Tasks 1, 2, 3

  **References**:

  **Pattern References**:
  - Recent commit messages from `git log --oneline -5`:
    - `e23afdea docs(datamodel): restructure HAS vs datamodel comparison to follow template format`
    - `73249584 docs(datamodel): refresh HAS vs datamodel comparison for Chapter 5`

  **Acceptance Criteria**:

  ```bash
  # AC1: Only intended files staged
  git -C earlysim diff --cached --name-only
  # Assert: Exactly 2 entries:
  #   datamodel/protocols/working/reviews/archive/has-datamodel-comparison.20260206.md (new)
  #   datamodel/protocols/working/reviews/has-datamodel-comparison.md (modified)
  # Note: git mv shows as rename, so may appear as:
  #   R datamodel/protocols/working/reviews/has-datamodel-comparison.20260206.md -> .../archive/...

  # AC2: prompts.md is NOT staged
  git -C earlysim diff --cached --name-only | grep prompts
  # Assert: No matches (exit code 1)

  # AC3: IBTA is NOT staged
  git -C earlysim diff --cached --name-only | grep IBTA
  # Assert: No matches (exit code 1)

  # AC4: Commit succeeds
  git -C earlysim commit -m "docs(datamodel): reorder HAS comparison sections and archive previous review"
  # Assert: exit code 0

  # AC5: Commit message follows convention
  git -C earlysim log -1 --format='%s'
  # Assert: "docs(datamodel): reorder HAS comparison sections and archive previous review"

  # AC6: Working tree is clean after commit (except untracked files)
  git -C earlysim status --porcelain
  # Assert: Only untracked files remain (prompts.md, docs/references/IBTA/)
  ```

  **Commit**: YES
  - Message: `docs(datamodel): reorder HAS comparison sections and archive previous review`
  - Files: `datamodel/protocols/working/reviews/archive/has-datamodel-comparison.20260206.md`, `datamodel/protocols/working/reviews/has-datamodel-comparison.md`
  - Pre-commit: Acceptance criteria from Tasks 1–3

---

## Commit Strategy

| After Task | Message | Files | Verification |
|------------|---------|-------|--------------|
| 4 (all tasks) | `docs(datamodel): reorder HAS comparison sections and archive previous review` | `reviews/archive/has-datamodel-comparison.20260206.md` (moved), `reviews/has-datamodel-comparison.md` (edited) | All AC from Tasks 1–4 |

---

## Success Criteria

### Verification Commands
```bash
# Section order correct
grep -n "^## " earlysim/datamodel/protocols/working/reviews/has-datamodel-comparison.md
# Expected: Recommended Work Items < Summary of Mismatches < Detailed Comparison

# Archive file in correct location
ls earlysim/datamodel/protocols/working/reviews/archive/has-datamodel-comparison.20260206.md
# Expected: file exists

# All archive references updated
grep "has-datamodel-comparison.20260206.md" earlysim/datamodel/protocols/working/reviews/has-datamodel-comparison.md | grep -v "archive/"
# Expected: no matches (all references have archive/ prefix)

# Line count preserved
wc -l < earlysim/datamodel/protocols/working/reviews/has-datamodel-comparison.md
# Expected: ~736 (± 4 lines for archival rule additions)

# Clean commit
git -C earlysim log -1 --format='%s'
# Expected: "docs(datamodel): reorder HAS comparison sections and archive previous review"
```

### Final Checklist
- [ ] Recommended Work Items appears before Summary of Mismatches
- [ ] Summary of Mismatches appears before Detailed Comparison
- [ ] Path Corrections Needed subsection is still inside Summary of Mismatches
- [ ] Archived file at `reviews/archive/has-datamodel-comparison.20260206.md`
- [ ] No archived file at `reviews/has-datamodel-comparison.20260206.md`
- [ ] Table of Contents order matches section order
- [ ] Metadata block references `archive/` path
- [ ] Changes from Previous Review references `archive/` path
- [ ] Document Structure Rules numbered list reflects new order
- [ ] Archival Rules mention `archive/` subdirectory
- [ ] Commit message is conventional format
- [ ] Only intended files committed
- [ ] `prompts.md` and `docs/references/IBTA/` NOT committed
