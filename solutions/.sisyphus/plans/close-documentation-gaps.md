# Close Documentation Gaps in Rules System

## TL;DR

> **Quick Summary**: Update all rule files to close 18 identified documentation gaps — stale content, missing toolchain constraints, maintenance traps, undocumented design decisions, and file cleanup.
> 
> **Deliverables**:
> - Backup of all files to be changed in `rules.backup/`
> - Updated `rules.md` (fix stale Quick Reference, complete File Locations table)
> - Updated `rules/common.md` (toolchain versions, Scale-Up constraint)
> - Updated `rules/docx.md` (caption maintenance trap, heading shift explanation)
> - Updated `rules/pptx.md` (post-processor docs, template history, repair issue, backup docs)
> - Updated `rules/pdf.md` (BlockQuote conversion explanation)
> - Deleted root-level legacy files (`CN7000_solutions_features.docx`, `cn7000_solutions_features.pptx`)
> 
> **Estimated Effort**: Medium
> **Parallel Execution**: YES - 2 waves
> **Critical Path**: Task 1 (backup) → Tasks 2-6 (parallel edits) → Task 7 (cleanup + verify)

---

## Context

### Original Request
Comprehensive audit revealed 18 documentation gaps where knowledge exists in code, session memory, or learnings notepads but is NOT captured in rule files. User wants all gaps closed in a single plan.

### Interview Summary
**Key Decisions**:
- **No git init** — instead, backup all files to be changed/deleted into `rules.backup/` directory before any modifications
- **Keep all dead/legacy files** — `pptx-slides.lua`, `pptx-layout-map.lua`, PowerShell utilities, `.md.backup` files all stay (but document their status)
- **Delete root-level legacy outputs** — `CN7000_solutions_features.docx` and `.pptx` are superseded by pipeline
- **Keep both PPTX template backups** — document which is which in `rules/pptx.md`
- **Toolchain versions as "tested with"** — not hard requirements

### Metis Review
**Identified Gaps** (addressed):
- No git safety net → resolved via `rules.backup/` directory
- Hardcoded caption list is a maintenance trap → documented as Known Limitation with update instructions
- Deletion confirmation needed → user confirmed: delete root-level files, keep everything else
- Learnings notepad content should fold into rules → incorporated into `rules/pptx.md` updates

---

## Work Objectives

### Core Objective
Close all 18 identified documentation gaps so that rule files are the single source of truth for the entire pipeline.

### Concrete Deliverables
- `rules.backup/` directory with copies of all files before modification
- 5 updated rule files (`rules.md`, `rules/common.md`, `rules/docx.md`, `rules/pptx.md`, `rules/pdf.md`)
- 2 deleted legacy files at project root

### Definition of Done
- [x] Zero stale references to xelatex in any rule file
- [x] Toolchain versions documented in `rules/common.md`
- [x] `pptx-postprocess.py` documented in `rules/pptx.md`
- [x] All pipeline files listed in `rules.md` File Locations table
- [x] Every file listed in File Locations table actually exists on disk

### Must Have
- Backup of all modified files before any changes
- Fix stale xelatex reference in `rules.md` Quick Reference
- Toolchain version constraints in `rules/common.md`
- Caption maintenance trap warning in `rules/docx.md`
- PPTX post-processor documentation in `rules/pptx.md`
- Template backup documentation in `rules/pptx.md`
- PPTX repair open issue in `rules/pptx.md`

### Must NOT Have (Guardrails)
- NO changes to any `.lua`, `.py`, or `.sh` code files
- NO changes to `solutions.md` content
- NO changes to template files (`.pptx`, `.dotx`)
- NO deletion of dead/legacy files (user chose to keep them) — only delete the 2 root-level outputs
- NO new rule files — all additions go into existing files
- NO over-documentation — keep additions in the same terse style (tables, bullets, code blocks)
- NO TODO/FIXME items implying future code changes — document as "Known Limitations"

---

## Verification Strategy

> **UNIVERSAL RULE: ZERO HUMAN INTERVENTION**
>
> ALL tasks are verifiable by running commands. No manual file opening required.

### Test Decision
- **Infrastructure exists**: N/A (documentation changes only)
- **Automated tests**: None (no code changes)
- **Framework**: N/A

### Agent-Executed QA Scenarios (MANDATORY — ALL tasks)

Verification is via `grep`, `test -e`, and `diff` commands against the modified rule files.

---

## Execution Strategy

### Parallel Execution Waves

```
Wave 1 (Start Immediately):
└── Task 1: Backup all files to rules.backup/

Wave 2 (After Wave 1):
├── Task 2: Update rules.md
├── Task 3: Update rules/common.md
├── Task 4: Update rules/docx.md
├── Task 5: Update rules/pptx.md
└── Task 6: Update rules/pdf.md

Wave 3 (After Wave 2):
└── Task 7: Delete root-level legacy files + final verification
```

### Dependency Matrix

| Task | Depends On | Blocks | Can Parallelize With |
|------|------------|--------|---------------------|
| 1 | None | 2, 3, 4, 5, 6 | None |
| 2 | 1 | 7 | 3, 4, 5, 6 |
| 3 | 1 | 7 | 2, 4, 5, 6 |
| 4 | 1 | 7 | 2, 3, 5, 6 |
| 5 | 1 | 7 | 2, 3, 4, 6 |
| 6 | 1 | 7 | 2, 3, 4, 5 |
| 7 | 2, 3, 4, 5, 6 | None | None (final) |

### Agent Dispatch Summary

| Wave | Tasks | Recommended Agents |
|------|-------|-------------------|
| 1 | 1 | delegate_task(category="quick", ...) |
| 2 | 2, 3, 4, 5, 6 | dispatch all 5 in parallel, category="quick" |
| 3 | 7 | delegate_task(category="quick", ...) |

---

## TODOs

- [x] 1. Backup all files to be modified

  **What to do**:
  - Create `rules.backup/` directory at project root
  - Copy these files into it (preserving names):
    - `rules.md`
    - `rules/common.md`
    - `rules/docx.md`
    - `rules/pptx.md`
    - `rules/pdf.md`
    - `CN7000_solutions_features.docx`
    - `cn7000_solutions_features.pptx`

  **Must NOT do**:
  - Do NOT copy template files, code files, or solutions.md
  - Do NOT create nested directory structure — flat copy with original filenames

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: `[]`

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Wave 1 (solo)
  - **Blocks**: Tasks 2, 3, 4, 5, 6, 7
  - **Blocked By**: None

  **References**:
  - Files to backup are listed above — all exist at known paths under `/home/matkins/CN7000/solutions/`

  **Acceptance Criteria**:
  - [ ] `rules.backup/` directory exists
  - [ ] All 7 files copied into it
  - [ ] Original files unchanged

  **Agent-Executed QA Scenarios**:

  ```
  Scenario: Verify backup directory and contents
    Tool: Bash
    Preconditions: None
    Steps:
      1. ls -la /home/matkins/CN7000/solutions/rules.backup/
      2. Assert: 7 files present (rules.md, common.md, docx.md, pptx.md, pdf.md, CN7000_solutions_features.docx, cn7000_solutions_features.pptx)
      3. diff /home/matkins/CN7000/solutions/rules.md /home/matkins/CN7000/solutions/rules.backup/rules.md
      4. Assert: no differences (originals unchanged)
    Expected Result: All 7 files backed up, originals intact
    Evidence: Terminal output captured
  ```

  **Commit**: NO

---

- [x] 2. Update `rules.md` — Fix Quick Reference and File Locations

  **What to do**:

  **Fix 1 — Stale PDF Quick Reference (lines 44-48)**:
  Replace the current PDF section:
  ```markdown
  ### PDF Rules (from [pdf.md](rules/pdf.md))

  - Primary: xelatex with 1" margins, 11pt font
  - Fallback: LibreOffice conversion from DOCX
  - For branded PDFs, use DOCX → PDF
  ```
  With:
  ```markdown
  ### PDF Rules (from [pdf.md](rules/pdf.md))

  - Two-step: pandoc → Typst source → `typst compile` → PDF
  - Typst compatibility filter handles HorizontalRule and BlockQuote
  - For branded PDFs, use DOCX → PDF conversion
  ```

  **Fix 2 — Incomplete File Locations table (lines 54-66)**:
  Replace the current table with a complete version that includes ALL pipeline files:
  ```markdown
  ## File Locations

  | File | Purpose |
  |------|---------|
  | `solutions.md` | Main content source (markdown) |
  | `build.sh` | Build script (docx, pdf, pptx) |
  | `rules.md` | This index file |
  | `rules/common.md` | Shared rules |
  | `rules/markdown.md` | Source authoring rules |
  | `rules/docx.md` | Word generation rules |
  | `rules/pptx.md` | PowerPoint generation rules |
  | `rules/pdf.md` | PDF generation rules |
  | `templates/Standard_Tech Doc Word Template.dotx` | DOCX reference template |
  | `templates/custom-reference.pptx` | PPTX reference template |
  | `templates/custom-reference.pptx.backup-donot-touch` | Original pristine PPTX template (Dec 2025) |
  | `templates/custom-reference-backup.pptx` | Pre-layout-fix PPTX template backup (Feb 2026) |
  | `templates/filters/docx-format.lua` | DOCX Lua filter (H1 removal, caption numbering) |
  | `templates/filters/docx-postprocess.py` | DOCX post-processor (borders, captions, TOT, properties) |
  | `templates/filters/pptx-tables.lua` | PPTX Lua filter (table splitting, column widths, slide titles) |
  | `templates/filters/pptx-postprocess.py` | PPTX post-processor (layout remapping) |
  | `templates/filters/typst-compat.lua` | PDF/Typst compatibility filter |
  | `templates/filters/pptx-slides.lua` | Legacy stub (unused, not in build pipeline) |
  | `templates/filters/pptx-layout-map.lua` | Documentation-only stub (unused, not in build pipeline) |
  | `utilities/todocx.psm1` | Legacy PowerShell DOCX script (Windows, unused) |
  | `utilities/topptx.psm1` | Legacy PowerShell PPTX script (Windows, unused) |
  ```

  **Must NOT do**:
  - Do NOT change the DOCX or PPTX Quick Reference sections (they are accurate)
  - Do NOT change the Markdown Quick Reference section

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: `[]`

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 3, 4, 5, 6)
  - **Blocks**: Task 7
  - **Blocked By**: Task 1

  **References**:
  - `rules.md:44-48` — stale PDF Quick Reference to replace
  - `rules.md:54-66` — incomplete File Locations table to replace
  - `build.sh:35-52` — actual PDF build process (Typst two-step)
  - `templates/filters/typst-compat.lua` — the filter referenced in new text

  **Acceptance Criteria**:
  - [ ] `grep -c "xelatex" rules.md` returns 0
  - [ ] `grep -c "Typst" rules.md` returns ≥1
  - [ ] `grep -c "pptx-postprocess" rules.md` returns ≥1
  - [ ] `grep -c "typst-compat" rules.md` returns ≥1
  - [ ] `grep -c "solutions.md" rules.md` returns ≥1

  **Agent-Executed QA Scenarios**:

  ```
  Scenario: No stale xelatex references remain
    Tool: Bash
    Preconditions: rules.md has been edited
    Steps:
      1. grep -c "xelatex" /home/matkins/CN7000/solutions/rules.md
      2. Assert: output is "0"
    Expected Result: Zero matches for xelatex
    Evidence: Terminal output captured

  Scenario: File Locations table lists all pipeline files
    Tool: Bash
    Preconditions: rules.md has been edited
    Steps:
      1. grep -c "pptx-postprocess" /home/matkins/CN7000/solutions/rules.md
      2. Assert: output is ≥1
      3. grep -c "typst-compat" /home/matkins/CN7000/solutions/rules.md
      4. Assert: output is ≥1
      5. grep -c "solutions.md" /home/matkins/CN7000/solutions/rules.md
      6. Assert: output is ≥1
      7. grep -c "custom-reference.pptx.backup-donot-touch" /home/matkins/CN7000/solutions/rules.md
      8. Assert: output is ≥1
    Expected Result: All key files appear in the table
    Evidence: Terminal output captured
  ```

  **Commit**: YES (groups with Tasks 3-6)
  - Message: `docs(rules): fix stale PDF reference and complete file locations table`
  - Files: `rules.md`

---

- [x] 3. Update `rules/common.md` — Toolchain versions and Scale-Up constraint

  **What to do**:

  **Addition 1 — Toolchain Requirements section** (add after the Glossary Requirements section, before end of file):
  ```markdown
  ## Toolchain Requirements

  | Tool | Tested Version | Known Issues |
  |------|---------------|--------------|
  | Pandoc | 3.1.3 | `pandoc.Caption()` API unavailable; `--pdf-engine=typst` broken (use two-step process) |
  | Typst | 0.14.2 | None known |
  | Python | 3.x | Required for `docx-postprocess.py` and `pptx-postprocess.py` |

  ### Pandoc 3.1.3 Limitations
  - `pandoc.Caption()` constructor does not exist — Lua filters must use table-based caption format: `{long = {...}, short = nil}`
  - `--pdf-engine=typst` fails — must use two-step process: `pandoc → .typ` then `typst compile`
  - PPTX layout selection is not exposed to Lua filters — layout remapping requires Python post-processing
  ```

  **Addition 2 — Scale-Up Design Constraints section** (add after Topology Rules section):
  ```markdown
  ## Scale-Up Design Constraints

  - **Cornelis does not currently have a scale-up NIC or embedded accelerator HFI**
  - Scale-Up solutions assume third-party endpoint vendors connecting to Cornelis switches
  - Scale-Up interoperability is **Homogeneous only** (no heterogeneous/island mode)
  - This constraint applies to both Scale-Up AI (UALink) and Scale-Up HPC (UE/ULN)
  ```

  **Must NOT do**:
  - Do NOT modify existing sections (Scale Specifications, Topology Rules, Feature Naming, etc.)
  - Do NOT add version numbers as hard requirements — use "Tested Version" column

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: `[]`

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 2, 4, 5, 6)
  - **Blocks**: Task 7
  - **Blocked By**: Task 1

  **References**:
  - `rules/common.md` — current file (54 lines), additions go at end and after Topology Rules
  - `solutions.md:103` — blockquote with Scale-Up NIC constraint
  - `solutions.md:139` — same blockquote repeated for Scale-Up HPC
  - `build.sh:35-52` — Typst two-step process showing pandoc limitation
  - `templates/filters/pptx-tables.lua:103-105` — example of table-based caption format (no `pandoc.Caption()`)

  **Acceptance Criteria**:
  - [ ] `grep -c "3.1.3" rules/common.md` returns ≥1
  - [ ] `grep -c "0.14.2" rules/common.md` returns ≥1
  - [ ] `grep -c "scale-up NIC" rules/common.md` returns ≥1
  - [ ] `grep -c "Homogeneous only" rules/common.md` returns ≥1

  **Agent-Executed QA Scenarios**:

  ```
  Scenario: Toolchain versions documented
    Tool: Bash
    Preconditions: rules/common.md has been edited
    Steps:
      1. grep "3.1.3" /home/matkins/CN7000/solutions/rules/common.md
      2. Assert: at least one match containing "Pandoc"
      3. grep "0.14.2" /home/matkins/CN7000/solutions/rules/common.md
      4. Assert: at least one match containing "Typst"
    Expected Result: Both versions documented
    Evidence: Terminal output captured

  Scenario: Scale-Up constraint documented
    Tool: Bash
    Preconditions: rules/common.md has been edited
    Steps:
      1. grep -i "scale-up NIC" /home/matkins/CN7000/solutions/rules/common.md
      2. Assert: at least one match
      3. grep "Homogeneous only" /home/matkins/CN7000/solutions/rules/common.md
      4. Assert: at least one match
    Expected Result: Scale-Up design constraint clearly stated
    Evidence: Terminal output captured
  ```

  **Commit**: YES (groups with Tasks 2, 4-6)
  - Message: `docs(rules): add toolchain versions and scale-up constraints`
  - Files: `rules/common.md`

---

- [x] 4. Update `rules/docx.md` — Caption maintenance trap and heading shift

  **What to do**:

  **Addition 1 — Maintenance trap warning** (add new section after "Lua Filter" section, before "Post-Processor" section):
  ```markdown
  ## ⚠️ Maintenance: Hardcoded Caption List

  `docx-format.lua` (lines 4-11) contains a **hardcoded list** of table captions:

  ```lua
  local table_captions = {
      "Scale-Out AI Workload Solutions",
      "Scale-Out HPC Workload Solutions",
      "Scale-Up AI Workload Solutions",
      "Scale-Up HPC Workload Solutions",
      "Feature Applicability by Solution",
      "Key Differentiators by Solution Type"
  }
  ```

  **If you add, remove, or reorder tables in `solutions.md`, you MUST update this list.**

  The filter assigns captions by position (1st table → 1st caption, 2nd table → 2nd caption, etc.). If the list doesn't match the tables, captions will be silently wrong in DOCX output.

  ### How to Update
  1. Edit `templates/filters/docx-format.lua`
  2. Update the `table_captions` list to match the tables in `solutions.md` (same order)
  3. Rebuild: `./build.sh docx`
  4. Verify captions in output
  ```

  **Addition 2 — Explain `--shift-heading-level-by=-1`** (add explanation after the Build Configuration code block, around line 22):
  ```markdown
  ### Heading Level Shift

  The `--shift-heading-level-by=-1` flag shifts all headings down one level:
  - H1 in markdown → removed by `docx-format.lua` (becomes document title via `-M title=`)
  - H2 in markdown → H1 in DOCX (top-level sections)
  - H3 in markdown → H2 in DOCX

  This ensures the document title comes from metadata (displayed on the template's title page) rather than appearing as a heading in the body.
  ```

  **Must NOT do**:
  - Do NOT modify the existing Build Configuration code block
  - Do NOT change the table formatting or caption format sections

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: `[]`

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 2, 3, 5, 6)
  - **Blocks**: Task 7
  - **Blocked By**: Task 1

  **References**:
  - `rules/docx.md` — current file (106 lines)
  - `templates/filters/docx-format.lua:4-11` — the hardcoded caption list
  - `templates/filters/docx-format.lua:13-17` — H1 removal logic
  - `build.sh:25` — the `--shift-heading-level-by=-1` flag
  - `solutions.md` — has exactly 6 `Table:` caption lines matching the hardcoded list

  **Acceptance Criteria**:
  - [ ] `grep -c "Hardcoded Caption" rules/docx.md` returns ≥1
  - [ ] `grep -c "table_captions" rules/docx.md` returns ≥1
  - [ ] `grep -c "shift-heading-level" rules/docx.md` returns ≥2 (config block + explanation)
  - [ ] The hardcoded list in the documentation matches `docx-format.lua:4-11` exactly

  **Agent-Executed QA Scenarios**:

  ```
  Scenario: Caption maintenance trap documented
    Tool: Bash
    Preconditions: rules/docx.md has been edited
    Steps:
      1. grep -c "Hardcoded Caption" /home/matkins/CN7000/solutions/rules/docx.md
      2. Assert: output is ≥1
      3. grep -c "table_captions" /home/matkins/CN7000/solutions/rules/docx.md
      4. Assert: output is ≥1
      5. grep "MUST update" /home/matkins/CN7000/solutions/rules/docx.md
      6. Assert: at least one match
    Expected Result: Maintenance trap clearly documented with update instructions
    Evidence: Terminal output captured

  Scenario: Heading shift explained
    Tool: Bash
    Preconditions: rules/docx.md has been edited
    Steps:
      1. grep -c "shift-heading-level" /home/matkins/CN7000/solutions/rules/docx.md
      2. Assert: output is ≥2
      3. grep "H1 in markdown" /home/matkins/CN7000/solutions/rules/docx.md
      4. Assert: at least one match explaining the shift
    Expected Result: Heading level shift purpose explained
    Evidence: Terminal output captured
  ```

  **Commit**: YES (groups with Tasks 2, 3, 5, 6)
  - Message: `docs(rules): add caption maintenance trap and heading shift explanation`
  - Files: `rules/docx.md`

---

- [x] 5. Update `rules/pptx.md` — Post-processor, template history, repair issue, backups

  **What to do**:

  This is the largest update. Add 4 new sections to `rules/pptx.md`.

  **Addition 1 — Post-Processor section** (add after Build Configuration section, around line 43):
  ```markdown
  ## Post-Processor (pptx-postprocess.py)

  After pandoc generates the PPTX, a Python post-processor remaps slide layouts.

  ### Why Post-Processing Is Needed

  Pandoc uses standard layout names internally, but our Cornelis template uses different names. Pandoc doesn't expose layout selection to Lua filters, so remapping must happen after PPTX generation by modifying the XML inside the zip.

  ### Layout Remapping

  | Pandoc Creates | Template Has | Action |
  |----------------|-------------|--------|
  | `Title Slide` | `Title` | Remap slides → existing `Title` layout, delete pandoc's fallback |
  | `Two Content` | `Title and Content - 2 Column` | Remap slides → existing layout, delete fallback |
  | `Comparison` | `Title and Content - 2 Column` | Remap slides → existing layout, delete fallback |
  | `Title and Content` | *(not in template)* | Rename layout to `title and 1 content` |

  ### What the Post-Processor Does

  1. Extracts PPTX (zip) to temp directory
  2. Builds map of layout names → layout XML files
  3. For each mapping where target layout already exists in template:
     - Finds all slides using the source layout
     - Updates slide `.rels` files to point to the target layout
     - Deletes the pandoc-created fallback layout XML and its `.rels`
  4. For each mapping where target doesn't exist:
     - Renames the layout's `<p:cSld name="...">` attribute
  5. Cleans up `[Content_Types].xml` (removes entries for deleted layouts)
  6. Cleans up `slideMaster1.xml.rels` (removes relationships to deleted layouts)
  7. Repacks the PPTX zip
  ```

  **Addition 2 — Template Modification History section** (add after Layout Name Mapping section):
  ```markdown
  ## Template Modification History

  The `custom-reference.pptx` template was modified from the original Cornelis template to add layouts pandoc requires but the original lacked.

  ### Modifications Applied (Feb 2026)

  | Change | File | Details |
  |--------|------|---------|
  | Renamed layout | `slideLayout5.xml` | `Blank Layout` → `Blank` |
  | Added layout | `slideLayout42.xml` | `Comparison` (copied from pandoc default reference) |
  | Added layout | `slideLayout43.xml` | `Content with Caption` (copied from pandoc default reference) |
  | Updated | `[Content_Types].xml` | Added entries for slideLayout42 and slideLayout43 |
  | Updated | `slideMaster1.xml.rels` | Added relationships to new layouts |
  | Created | `_rels/slideLayout42.xml.rels` | Relationship file for Comparison layout |
  | Created | `_rels/slideLayout43.xml.rels` | Relationship file for Content with Caption layout |

  ### Template Backups

  | File | Date | Description |
  |------|------|-------------|
  | `custom-reference.pptx.backup-donot-touch` | Dec 2025 | **Original pristine** Cornelis template before any modifications |
  | `custom-reference-backup.pptx` | Feb 2026 | Backup taken before layout-fix modifications were applied |
  | `custom-reference.pptx` | Feb 2026 | **Current working template** with all modifications applied |

  > **WARNING**: Do NOT modify `custom-reference.pptx` by directly editing its XML. The template was corrupted once during manual XML editing and had to be restored from backup. Use PowerPoint or LibreOffice to make template changes, then verify by building.
  ```

  **Addition 3 — Update Known Limitations section** (replace existing section at lines 96-101):
  ```markdown
  ## Known Limitations

  1. **PPTX Repair Issue (OPEN)**: PowerPoint may report the generated PPTX needs repair when opening. This occurs after post-processing and is under investigation. The file opens correctly after repair. Possible causes:
     - Slides referencing deleted layouts not fully caught by post-processor
     - `presentation.xml` may reference layouts that were deleted
     - Pandoc's fallback layouts may have different slide master references than template layouts
  2. **Missing Layouts**: If template lacks required layouts, pandoc falls back to its built-in defaults which may cause formatting issues or require PowerPoint to repair the file
  3. **Complex Tables**: Very wide tables may not fit on slides
  4. **Images**: Not currently supported in table cells
  5. **Layout Selection**: Pandoc does not expose layout selection to Lua filters — all layout remapping must be done via Python post-processing
  ```

  **Must NOT do**:
  - Do NOT modify the Table Formatting, Slide Titles, or Horizontal Rules sections
  - Do NOT change the Slide Layout Requirements table (it's accurate)
  - Do NOT suggest code fixes for the repair issue — document it as a known limitation only

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: `[]`

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 2, 3, 4, 6)
  - **Blocks**: Task 7
  - **Blocked By**: Task 1

  **References**:
  - `rules/pptx.md` — current file (101 lines)
  - `templates/filters/pptx-postprocess.py` — the post-processor being documented (275 lines)
  - `templates/filters/pptx-postprocess.py:40-45` — the LAYOUT_MAP constant
  - `templates/filters/pptx-postprocess.py:139-201` — main processing logic
  - `.sisyphus/notepads/fix-pptx-layout-mapping/learnings.md` — template modification history to fold in
  - `build.sh:64-65` — post-processor invocation

  **Acceptance Criteria**:
  - [ ] `grep -c "pptx-postprocess" rules/pptx.md` returns ≥3
  - [ ] `grep -c "Layout Remapping" rules/pptx.md` returns ≥1
  - [ ] `grep -c "Repair Issue" rules/pptx.md` returns ≥1
  - [ ] `grep -c "backup-donot-touch" rules/pptx.md` returns ≥1
  - [ ] `grep -c "WARNING" rules/pptx.md` returns ≥1
  - [ ] `grep -c "Modification History" rules/pptx.md` returns ≥1

  **Agent-Executed QA Scenarios**:

  ```
  Scenario: Post-processor documented
    Tool: Bash
    Preconditions: rules/pptx.md has been edited
    Steps:
      1. grep -c "pptx-postprocess" /home/matkins/CN7000/solutions/rules/pptx.md
      2. Assert: output is ≥3
      3. grep "Layout Remapping" /home/matkins/CN7000/solutions/rules/pptx.md
      4. Assert: at least one match
    Expected Result: Post-processor fully documented
    Evidence: Terminal output captured

  Scenario: Template history and backups documented
    Tool: Bash
    Preconditions: rules/pptx.md has been edited
    Steps:
      1. grep "Modification History" /home/matkins/CN7000/solutions/rules/pptx.md
      2. Assert: at least one match
      3. grep "backup-donot-touch" /home/matkins/CN7000/solutions/rules/pptx.md
      4. Assert: at least one match
      5. grep "WARNING" /home/matkins/CN7000/solutions/rules/pptx.md
      6. Assert: at least one match (XML editing warning)
    Expected Result: Template history, backups, and warning all present
    Evidence: Terminal output captured

  Scenario: PPTX repair issue documented as known limitation
    Tool: Bash
    Preconditions: rules/pptx.md has been edited
    Steps:
      1. grep "Repair Issue" /home/matkins/CN7000/solutions/rules/pptx.md
      2. Assert: at least one match
      3. grep "OPEN" /home/matkins/CN7000/solutions/rules/pptx.md
      4. Assert: at least one match
    Expected Result: Repair issue documented with OPEN status
    Evidence: Terminal output captured
  ```

  **Commit**: YES (groups with Tasks 2, 3, 4, 6)
  - Message: `docs(rules): add PPTX post-processor, template history, and repair issue`
  - Files: `rules/pptx.md`

---

- [x] 6. Update `rules/pdf.md` — BlockQuote conversion explanation

  **What to do**:

  **Addition 1 — Expand Compatibility Filter section** (replace lines 34-39):
  ```markdown
  ## Compatibility Filter (typst-compat.lua)

  The `typst-compat.lua` filter handles pandoc 3.1.3 → Typst compatibility issues:

  | Pandoc Element | Typst Output | Purpose |
  |---------------|-------------|---------|
  | `HorizontalRule` (`---`) | `#line(length: 100%)` | Pandoc doesn't convert `---` to Typst natively |
  | `BlockQuote` (`> text`) | `Div` with "note" class | Preserves blockquote content as styled block |

  ### BlockQuote Handling

  The `solutions.md` file uses blockquotes for important notes (e.g., the Scale-Up NIC disclaimer). Without this filter, pandoc's Typst writer may not render blockquotes correctly. The filter converts them to Div elements with a "note" class, which Typst renders as styled blocks.
  ```

  **Must NOT do**:
  - Do NOT change the Generation Method, Why Typst, or Page Layout sections
  - Do NOT change the Known Limitations section

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: `[]`

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 2, 3, 4, 5)
  - **Blocks**: Task 7
  - **Blocked By**: Task 1

  **References**:
  - `rules/pdf.md` — current file (80 lines)
  - `templates/filters/typst-compat.lua` — the filter being documented (18 lines)
  - `solutions.md:103` — example blockquote: "Cornelis does not currently have a scale-up NIC..."
  - `solutions.md:139` — same blockquote repeated

  **Acceptance Criteria**:
  - [ ] `grep -c "BlockQuote" rules/pdf.md` returns ≥2
  - [ ] `grep -c "note.*class" rules/pdf.md` returns ≥1
  - [ ] `grep -c "Scale-Up" rules/pdf.md` returns ≥1

  **Agent-Executed QA Scenarios**:

  ```
  Scenario: BlockQuote conversion explained
    Tool: Bash
    Preconditions: rules/pdf.md has been edited
    Steps:
      1. grep -c "BlockQuote" /home/matkins/CN7000/solutions/rules/pdf.md
      2. Assert: output is ≥2
      3. grep "note.*class\|class.*note" /home/matkins/CN7000/solutions/rules/pdf.md
      4. Assert: at least one match
    Expected Result: BlockQuote→Div conversion purpose explained
    Evidence: Terminal output captured
  ```

  **Commit**: YES (groups with Tasks 2, 3, 4, 5)
  - Message: `docs(rules): explain BlockQuote conversion in PDF filter`
  - Files: `rules/pdf.md`

---

- [x] 7. Delete root-level legacy files and run final verification

  **What to do**:

  **Step 1 — Delete legacy files**:
  - Delete `CN7000_solutions_features.docx` (264KB, earlier manual version)
  - Delete `cn7000_solutions_features.pptx` (2.8MB, earlier manual version)
  - These are superseded by the pipeline output in `output/`
  - Backups were already created in Task 1

  **Step 2 — Run comprehensive verification**:
  - Verify zero stale xelatex references across all rule files
  - Verify all files listed in `rules.md` File Locations table exist on disk
  - Verify no rule file references deleted files without noting them as legacy
  - Verify key content is present in each updated file

  **Must NOT do**:
  - Do NOT delete any other files (dead/legacy files are kept per user decision)
  - Do NOT modify any rule files in this task

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: `[]`

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Wave 3 (solo, final)
  - **Blocks**: None
  - **Blocked By**: Tasks 2, 3, 4, 5, 6

  **References**:
  - `rules.backup/CN7000_solutions_features.docx` — backup of file being deleted
  - `rules.backup/cn7000_solutions_features.pptx` — backup of file being deleted
  - `rules.md` — File Locations table to verify against

  **Acceptance Criteria**:
  - [ ] `test -e CN7000_solutions_features.docx` returns false (file deleted)
  - [ ] `test -e cn7000_solutions_features.pptx` returns false (file deleted)
  - [ ] `grep -r "xelatex" rules/ rules.md` returns zero matches
  - [ ] `grep -c "pptx-postprocess" rules/pptx.md` returns ≥3
  - [ ] `grep -c "3.1.3" rules/common.md` returns ≥1
  - [ ] `grep -c "Hardcoded Caption" rules/docx.md` returns ≥1
  - [ ] `grep -c "BlockQuote" rules/pdf.md` returns ≥2
  - [ ] `grep -c "Repair Issue" rules/pptx.md` returns ≥1
  - [ ] All files in `rules.md` File Locations table that are NOT marked "Legacy" exist on disk

  **Agent-Executed QA Scenarios**:

  ```
  Scenario: Legacy files deleted
    Tool: Bash
    Preconditions: Files backed up in Task 1
    Steps:
      1. test -e /home/matkins/CN7000/solutions/CN7000_solutions_features.docx && echo "EXISTS" || echo "DELETED"
      2. Assert: output is "DELETED"
      3. test -e /home/matkins/CN7000/solutions/cn7000_solutions_features.pptx && echo "EXISTS" || echo "DELETED"
      4. Assert: output is "DELETED"
      5. test -e /home/matkins/CN7000/solutions/rules.backup/CN7000_solutions_features.docx && echo "BACKED UP" || echo "MISSING"
      6. Assert: output is "BACKED UP"
    Expected Result: Files deleted, backups exist
    Evidence: Terminal output captured

  Scenario: Zero stale references across all rule files
    Tool: Bash
    Preconditions: All rule files updated
    Steps:
      1. grep -r "xelatex" /home/matkins/CN7000/solutions/rules/ /home/matkins/CN7000/solutions/rules.md || echo "CLEAN"
      2. Assert: output is "CLEAN" (no matches)
    Expected Result: No stale xelatex references anywhere
    Evidence: Terminal output captured

  Scenario: All File Locations entries exist on disk
    Tool: Bash
    Preconditions: rules.md File Locations table updated
    Steps:
      1. For each non-legacy file in the File Locations table, run: test -e /home/matkins/CN7000/solutions/<path>
      2. Specifically verify:
         - test -e solutions.md
         - test -e build.sh
         - test -e templates/filters/pptx-postprocess.py
         - test -e templates/filters/typst-compat.lua
         - test -e templates/custom-reference.pptx.backup-donot-touch
      3. Assert: all return true
    Expected Result: Every listed file exists
    Evidence: Terminal output captured

  Scenario: Comprehensive content verification
    Tool: Bash
    Preconditions: All tasks complete
    Steps:
      1. grep -c "pptx-postprocess" /home/matkins/CN7000/solutions/rules/pptx.md
      2. Assert: ≥3
      3. grep -c "3.1.3" /home/matkins/CN7000/solutions/rules/common.md
      4. Assert: ≥1
      5. grep -c "Hardcoded Caption" /home/matkins/CN7000/solutions/rules/docx.md
      6. Assert: ≥1
      7. grep -c "BlockQuote" /home/matkins/CN7000/solutions/rules/pdf.md
      8. Assert: ≥2
      9. grep -c "Repair Issue" /home/matkins/CN7000/solutions/rules/pptx.md
      10. Assert: ≥1
    Expected Result: All key documentation additions verified
    Evidence: Terminal output captured
  ```

  **Commit**: YES
  - Message: `docs: remove superseded legacy output files`
  - Files: deleted `CN7000_solutions_features.docx`, `cn7000_solutions_features.pptx`

---

## Commit Strategy

| After Task(s) | Message | Files | Verification |
|---------------|---------|-------|--------------|
| 2, 3, 4, 5, 6 | `docs(rules): close 18 documentation gaps across all rule files` | `rules.md`, `rules/common.md`, `rules/docx.md`, `rules/pptx.md`, `rules/pdf.md` | grep checks per task |
| 7 | `docs: remove superseded legacy output files` | deleted files | test -e checks |

---

## Success Criteria

### Verification Commands
```bash
# Zero stale xelatex references
grep -r "xelatex" rules/ rules.md  # Expected: no output

# Toolchain versions documented
grep "3.1.3" rules/common.md  # Expected: match
grep "0.14.2" rules/common.md  # Expected: match

# PPTX post-processor documented
grep -c "pptx-postprocess" rules/pptx.md  # Expected: ≥3

# Caption trap documented
grep "Hardcoded Caption" rules/docx.md  # Expected: match

# Repair issue documented
grep "Repair Issue" rules/pptx.md  # Expected: match

# BlockQuote explained
grep -c "BlockQuote" rules/pdf.md  # Expected: ≥2

# Legacy files deleted
test -e CN7000_solutions_features.docx && echo FAIL || echo PASS  # Expected: PASS
test -e cn7000_solutions_features.pptx && echo FAIL || echo PASS  # Expected: PASS

# Backups exist
test -d rules.backup && echo PASS || echo FAIL  # Expected: PASS
```

### Final Checklist
- [x] All "Must Have" items present in rule files
- [x] All "Must NOT Have" guardrails respected (no code changes, no template changes)
- [x] Zero stale references to xelatex
- [x] All File Locations entries verified on disk
- [x] Backups created before any modifications
- [x] Legacy root-level files deleted (with backups)
