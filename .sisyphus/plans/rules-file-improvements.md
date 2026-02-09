# Rules File Improvements

## TL;DR

> **Quick Summary**: Harmonize two rules files by adding cross-references, resolving terminology conflicts, and ensuring each file contains critical content from the other.
> 
> **Deliverables**:
> - Updated `.sisyphus/rules/technical-report-generation.md` with overflow prevention, quality checklist, and cross-references
> - Updated `.sisyphus/rules/protocol-technical-reports.md` with unified section type terminology and cross-references
> 
> **Estimated Effort**: Quick
> **Parallel Execution**: NO - sequential (file edits depend on each other for consistency)
> **Critical Path**: Task 1 → Task 2 → Task 3 → Task 4

---

## Context

### Original Request
User asked to compare and contrast the two rules files and decide whether to merge or keep separate. After detailed analysis, user chose:
- **Option B**: Keep files separate with improvements (not merge)
- **Option #3**: Keep YAML as intermediate format (not switch to Markdown)

### Interview Summary
**Key Discussions**:
- Compared both files in detail (417 lines vs 505 lines)
- Identified overlapping content (YAML section types, table formats, report structure)
- Found conflicts: `item_list` vs `bullets` naming, different section ordering
- Determined files serve different purposes in the pipeline

**Research Findings**:
- **CLI supports BOTH `item_list` AND `bullets`** - they are aliases (cli.py lines 158-176)
- Existing YAML reports use mixed terminology:
  - `item_list`: technical_report_ue.yaml, technical_report.yaml, status_report.yaml
  - `bullets`: technical_report_roce.yaml, technical_report_ethernet.yaml, technical_report_cornelis.yaml
- Both formats work because cli.py handles both (lines 166-176)

### Metis Review
**Identified Gaps** (addressed):
- Need to verify `item_list` vs `bullets` before documenting → **RESOLVED**: Both work, document both
- Need cross-reference syntax → Using relative links: `[file.md](./file.md#section)`
- Need precedence rule for conflicting guidance → Adding to both files
- Need "Adding New Protocols" template → Adding to protocol file

---

## Work Objectives

### Core Objective
Improve both rules files so they are consistent, cross-referenced, and each contains critical content from the other while maintaining their distinct purposes.

### Concrete Deliverables
- `.sisyphus/rules/technical-report-generation.md` - updated with new sections
- `.sisyphus/rules/protocol-technical-reports.md` - updated with unified terminology

### Definition of Done
- [x] Both files have cross-reference sections pointing to each other
- [x] Both files document that `item_list` and `bullets` are both valid
- [x] `technical-report-generation.md` has overflow prevention section
- [x] `technical-report-generation.md` has quality checklist
- [x] `protocol-technical-reports.md` has "Adding New Protocols" template
- [x] Existing YAML reports still generate PPTX successfully

### Must Have
- Cross-references in both files
- Unified section type documentation (both `item_list` and `bullets` documented as valid)
- Overflow prevention in both files
- Quality checklist in both files
- Precedence rule for conflicting guidance

### Must NOT Have (Guardrails)
- Do NOT merge files into one
- Do NOT change existing YAML report files
- Do NOT modify Python implementation code
- Do NOT introduce new section types not supported by implementation
- Do NOT change file locations

---

## Verification Strategy (MANDATORY)

### Test Decision
- **Infrastructure exists**: YES (existing PPTX generation)
- **User wants tests**: Manual verification
- **Framework**: Bash commands + PPTX generation

### Automated Verification

Each TODO includes executable verification that agents can run directly.

---

## Execution Strategy

### Parallel Execution Waves

```
Wave 1 (Sequential - edits to same conceptual content):
├── Task 1: Add cross-references and scope sections to both files
└── Task 2: Unify section type documentation in both files

Wave 2 (After Wave 1):
├── Task 3: Add overflow prevention to technical-report-generation.md
└── Task 4: Add quality checklist and new protocol template

Wave 3 (Final):
└── Task 5: Validate all changes with PPTX generation
```

### Dependency Matrix

| Task | Depends On | Blocks | Can Parallelize With |
|------|------------|--------|---------------------|
| 1 | None | 2, 3, 4 | None |
| 2 | 1 | 5 | None |
| 3 | 1 | 5 | 4 |
| 4 | 1 | 5 | 3 |
| 5 | 2, 3, 4 | None | None (final) |

---

## TODOs

- [x] 1. Add Cross-References and Scope Sections to Both Files

  **What to do**:
  - Add "Scope" section at top of both files clarifying purpose
  - Add "Related Rules" section to both files with links to the other
  - Add "Precedence" section explaining which file to use when

  **Must NOT do**:
  - Do not change existing content structure
  - Do not remove any existing sections

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Simple text additions to existing files
  - **Skills**: [`git-master`]
    - `git-master`: May need to commit changes

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Sequential (Task 1)
  - **Blocks**: Tasks 2, 3, 4
  - **Blocked By**: None

  **References**:

  **Pattern References**:
  - `.sisyphus/rules/technical-report-generation.md:1-10` - Current file header to preserve
  - `.sisyphus/rules/protocol-technical-reports.md:1-10` - Current file header to preserve

  **Content to Add**:

  For `technical-report-generation.md`, add after line 5:
  ```markdown
  ## Scope

  This document defines **HOW** to extract data from KSY datamodel files and format it into YAML sections. It is a **data extraction specification**.

  **Use this file when**: Parsing KSY files, formatting YAML sections, understanding field mappings.

  **For protocol-specific content requirements**: See [protocol-technical-reports.md](./protocol-technical-reports.md)

  ---

  ## Related Rules

  | File | Purpose | When to Use |
  |------|---------|-------------|
  | [protocol-technical-reports.md](./protocol-technical-reports.md) | Protocol-specific content requirements | Deciding WHAT content each protocol report needs |
  | This file | KSY extraction and YAML formatting | Deciding HOW to format extracted data |

  ### Precedence

  When guidance conflicts:
  1. **YAML syntax/format**: This file takes precedence
  2. **Protocol-specific content**: `protocol-technical-reports.md` takes precedence
  3. **Overflow handling**: Both files - follow the more restrictive guidance
  ```

  For `protocol-technical-reports.md`, add after line 5:
  ```markdown
  ## Scope

  This document defines **WHAT** content each protocol report must contain and how to generate PPTX presentations. It is a **content requirements specification**.

  **Use this file when**: Determining required sections per protocol, generating PPTX, checking quality.

  **For YAML formatting standards**: See [technical-report-generation.md](./technical-report-generation.md)

  ---

  ## Related Rules

  | File | Purpose | When to Use |
  |------|---------|-------------|
  | [technical-report-generation.md](./technical-report-generation.md) | KSY extraction and YAML formatting | Deciding HOW to format extracted data |
  | This file | Protocol-specific content requirements | Deciding WHAT content each protocol report needs |

  ### Precedence

  When guidance conflicts:
  1. **Protocol-specific content**: This file takes precedence
  2. **YAML syntax/format**: `technical-report-generation.md` takes precedence
  3. **Overflow handling**: Both files - follow the more restrictive guidance
  ```

  **Acceptance Criteria**:

  ```bash
  # 1. Cross-references exist in both files
  grep -q "protocol-technical-reports.md" .sisyphus/rules/technical-report-generation.md && echo "PASS: cross-ref in tech-report" || echo "FAIL"
  grep -q "technical-report-generation.md" .sisyphus/rules/protocol-technical-reports.md && echo "PASS: cross-ref in protocol-report" || echo "FAIL"

  # 2. Scope sections exist
  grep -q "## Scope" .sisyphus/rules/technical-report-generation.md && echo "PASS: scope in tech-report" || echo "FAIL"
  grep -q "## Scope" .sisyphus/rules/protocol-technical-reports.md && echo "PASS: scope in protocol-report" || echo "FAIL"

  # 3. Precedence sections exist
  grep -q "### Precedence" .sisyphus/rules/technical-report-generation.md && echo "PASS: precedence in tech-report" || echo "FAIL"
  grep -q "### Precedence" .sisyphus/rules/protocol-technical-reports.md && echo "PASS: precedence in protocol-report" || echo "FAIL"
  ```

  **Commit**: YES
  - Message: `docs(rules): add cross-references and scope sections to rules files`
  - Files: `.sisyphus/rules/technical-report-generation.md`, `.sisyphus/rules/protocol-technical-reports.md`

---

- [x] 2. Unify Section Type Documentation in Both Files

  **What to do**:
  - Update both files to document that `item_list` AND `bullets` are both valid section types
  - Document that they are aliases handled by cli.py
  - Show examples of both formats

  **Must NOT do**:
  - Do not change existing YAML reports
  - Do not modify cli.py

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Documentation update only
  - **Skills**: []
    - No special skills needed

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Sequential (after Task 1)
  - **Blocks**: Task 5
  - **Blocked By**: Task 1

  **References**:

  **Implementation References**:
  - `utilities/pptx_helper/cli.py:158-176` - Shows both `bullets` and `item_list` are handled
  - `utilities/pptx_helper/cli.py:89-96` - Shows `item_list` handling in progress reports

  **Existing YAML Examples**:
  - `reports/packet_taxonomy/technical_report_ue.yaml:10` - Uses `item_list`
  - `reports/packet_taxonomy/technical_report_roce.yaml:10` - Uses `bullets`

  **Content to Add/Update**:

  In `technical-report-generation.md`, update the enumeration/list section to include:
  ```markdown
  ### Bullet/Item List Section Types

  The YAML parser accepts **both** `item_list` and `bullets` as section types. They are functionally equivalent.

  **Format 1: `bullets` (preferred for new reports)**
  ```yaml
  - type: bullets
    title: "Key Points"
    bullets:
      - "First point"
      - "Second point"
  ```

  **Format 2: `item_list` (legacy, still supported)**
  ```yaml
  - type: item_list
    title: "Key Points"
    items:
      - "First point"
      - "Second point"
    item_type: closed  # or "open" for ○ bullets
  ```

  **Note**: `item_type: open` renders with ○ bullets, `item_type: closed` (default) renders with • bullets.
  ```

  In `protocol-technical-reports.md`, update the YAML section types to match.

  **Acceptance Criteria**:

  ```bash
  # 1. Both section types documented in tech-report
  grep -q "type: bullets" .sisyphus/rules/technical-report-generation.md && echo "PASS: bullets in tech-report" || echo "FAIL"
  grep -q "type: item_list" .sisyphus/rules/technical-report-generation.md && echo "PASS: item_list in tech-report" || echo "FAIL"

  # 2. Both section types documented in protocol-report
  grep -q "type: bullets" .sisyphus/rules/protocol-technical-reports.md && echo "PASS: bullets in protocol-report" || echo "FAIL"
  grep -q "type: item_list" .sisyphus/rules/protocol-technical-reports.md && echo "PASS: item_list in protocol-report" || echo "FAIL"
  ```

  **Commit**: YES
  - Message: `docs(rules): unify section type documentation (bullets and item_list)`
  - Files: `.sisyphus/rules/technical-report-generation.md`, `.sisyphus/rules/protocol-technical-reports.md`

---

- [x] 3. Add Overflow Prevention to technical-report-generation.md

  **What to do**:
  - Copy overflow prevention content from `protocol-technical-reports.md` lines 9-17
  - Add to `technical-report-generation.md` in the General Principles section
  - Adapt wording to fit the KSY extraction context

  **Must NOT do**:
  - Do not remove overflow content from protocol file
  - Do not change the meaning of the rules

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Copy and adapt existing content
  - **Skills**: []
    - No special skills needed

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Task 4)
  - **Blocks**: Task 5
  - **Blocked By**: Task 1

  **References**:

  **Source Content**:
  - `.sisyphus/rules/protocol-technical-reports.md:9-17` - Overflow prevention rules to copy

  **Content to Add**:

  Add to `technical-report-generation.md` after the Required Sections:
  ```markdown
  ---

  ## Content Overflow Prevention (CRITICAL)

  **ALL slides and content MUST fit within slide boundaries.** When generating YAML sections, consider overflow:

  1. **Tables**: If >15 rows, add pagination markers (e.g., "Field Definitions (1/3)")
  2. **Bullet Lists**: If >10 items, split at logical breakpoints
  3. **Wire Diagrams**: Keep to 8 bytes per line maximum
  4. **Code Blocks**: Truncate with "..." if >20 lines
  5. **TOC**: Multi-column layout handled automatically by PPTX generator

  **Note**: The PPTX generator (`utilities/pptx_helper`) handles some overflow automatically, but YAML authors should design for readability.
  ```

  **Acceptance Criteria**:

  ```bash
  # 1. Overflow prevention exists in tech-report
  grep -q "Overflow Prevention" .sisyphus/rules/technical-report-generation.md && echo "PASS: overflow in tech-report" || echo "FAIL"

  # 2. Key rules present
  grep -q "Tables.*split" .sisyphus/rules/technical-report-generation.md && echo "PASS: table split rule" || echo "FAIL"
  grep -q "Bullet Lists.*split" .sisyphus/rules/technical-report-generation.md && echo "PASS: bullet split rule" || echo "FAIL"
  ```

  **Commit**: YES (group with Task 4)
  - Message: `docs(rules): add overflow prevention and quality checklist`
  - Files: `.sisyphus/rules/technical-report-generation.md`

---

- [x] 4. Add Quality Checklist and New Protocol Template

  **What to do**:
  - Add quality checklist to `technical-report-generation.md` (adapted from protocol file)
  - Add "Adding New Protocols" template section to `protocol-technical-reports.md`

  **Must NOT do**:
  - Do not duplicate the full protocol-specific checklist
  - Do not add protocols that don't exist

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Documentation additions
  - **Skills**: []
    - No special skills needed

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Task 3)
  - **Blocks**: Task 5
  - **Blocked By**: Task 1

  **References**:

  **Source Content**:
  - `.sisyphus/rules/protocol-technical-reports.md:490-505` - Quality checklist to adapt

  **Content to Add**:

  Add to `technical-report-generation.md` at end:
  ```markdown
  ---

  ## Quality Checklist

  Before finalizing any YAML report:

  - [ ] All required sections from this document included
  - [ ] All tables have headers and consistent column counts
  - [ ] All wire diagrams use ASCII box drawing characters
  - [ ] All enumerations include value, name, description columns
  - [ ] All spec references include table/section/page numbers
  - [ ] Field offsets are sequential and non-overlapping
  - [ ] `x-packet.size_bytes` matches sum of field sizes
  - [ ] No content overflow on any section (see Overflow Prevention)

  For protocol-specific checklists, see [protocol-technical-reports.md](./protocol-technical-reports.md#quality-checklist).
  ```

  Add to `protocol-technical-reports.md` before Quality Checklist:
  ```markdown
  ---

  ## Adding New Protocols

  When adding a new protocol to the technical report system:

  ### 1. Create Analysis Document
  - Location: `analysis/packet_taxonomy/packet_taxonomy_{protocol}.md`
  - Include: Overview, packet formats, field definitions, enumerations

  ### 2. Create KSY Datamodel (if applicable)
  - Location: `earlysim/datamodel/protocols/{protocol}/`
  - Follow KSY metadata standards in [technical-report-generation.md](./technical-report-generation.md)

  ### 3. Add Protocol Section to This File
  Copy this template and fill in:

  ```markdown
  ## {Protocol Name}

  ### Source Documents
  - `analysis/packet_taxonomy/packet_taxonomy_{protocol}.md`

  ### Datamodel Directory
  `earlysim/datamodel/protocols/{protocol}/`

  ### Required Sections

  #### 1. Overview
  - Protocol purpose and context
  - Key characteristics

  #### 2. Packet Variants Matrix
  | Variant | Header Stack | Total Overhead | Use Case |
  |---------|--------------|----------------|----------|

  #### 3. Header Overhead Summary
  | Variant | L2 | L3 | L4 | ... | Total |
  |---------|----|----|----|----|-------|

  #### 4. Wire Format Diagrams
  - List key formats to diagram

  #### 5. Field Definition Tables
  - List headers requiring field tables

  #### 6. Spec References
  - Cite specification with version, section, page
  ```

  ### 4. Generate YAML Report
  - Location: `reports/packet_taxonomy/technical_report_{protocol}.yaml`
  - Follow YAML format in [technical-report-generation.md](./technical-report-generation.md)

  ### 5. Generate PPTX
  ```bash
  python -m utilities.pptx_helper --type technical \
    --data reports/packet_taxonomy/technical_report_{protocol}.yaml \
    --output reports/packet_taxonomy/technical_report_{protocol}.pptx \
    --toc -v
  ```
  ```

  **Acceptance Criteria**:

  ```bash
  # 1. Quality checklist in tech-report
  grep -q "## Quality Checklist" .sisyphus/rules/technical-report-generation.md && echo "PASS: checklist in tech-report" || echo "FAIL"

  # 2. New protocol template in protocol-report
  grep -q "## Adding New Protocols" .sisyphus/rules/protocol-technical-reports.md && echo "PASS: new protocol template" || echo "FAIL"

  # 3. Template has required sections
  grep -q "### 1. Create Analysis Document" .sisyphus/rules/protocol-technical-reports.md && echo "PASS: template step 1" || echo "FAIL"
  grep -q "### 5. Generate PPTX" .sisyphus/rules/protocol-technical-reports.md && echo "PASS: template step 5" || echo "FAIL"
  ```

  **Commit**: YES (group with Task 3)
  - Message: `docs(rules): add overflow prevention and quality checklist`
  - Files: `.sisyphus/rules/technical-report-generation.md`, `.sisyphus/rules/protocol-technical-reports.md`

---

- [x] 5. Validate All Changes with PPTX Generation

  **What to do**:
  - Run PPTX generation for at least one report using each section type format
  - Verify no errors occur
  - Confirm rules files are valid Markdown

  **Must NOT do**:
  - Do not modify YAML reports
  - Do not modify Python code

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Validation commands only
  - **Skills**: []
    - No special skills needed

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Final (Wave 3)
  - **Blocks**: None
  - **Blocked By**: Tasks 2, 3, 4

  **References**:

  **Test Files**:
  - `reports/packet_taxonomy/technical_report_ue.yaml` - Uses `item_list` format
  - `reports/packet_taxonomy/technical_report_roce.yaml` - Uses `bullets` format

  **Acceptance Criteria**:

  ```bash
  # 1. Generate PPTX with item_list format (UE report)
  python -m utilities.pptx_helper --type technical \
    --data reports/packet_taxonomy/technical_report_ue.yaml \
    --output /tmp/test_ue.pptx --toc -v 2>&1 | tail -5
  # Assert: No errors, file created

  # 2. Generate PPTX with bullets format (RoCE report)
  python -m utilities.pptx_helper --type technical \
    --data reports/packet_taxonomy/technical_report_roce.yaml \
    --output /tmp/test_roce.pptx --toc -v 2>&1 | tail -5
  # Assert: No errors, file created

  # 3. Verify output files exist
  test -f /tmp/test_ue.pptx && echo "PASS: UE PPTX created" || echo "FAIL"
  test -f /tmp/test_roce.pptx && echo "PASS: RoCE PPTX created" || echo "FAIL"

  # 4. Verify rules files are valid (no broken markdown)
  head -50 .sisyphus/rules/technical-report-generation.md
  head -50 .sisyphus/rules/protocol-technical-reports.md
  # Assert: Files render correctly, no syntax errors
  ```

  **Commit**: NO (validation only)

---

## Commit Strategy

| After Task | Message | Files | Verification |
|------------|---------|-------|--------------|
| 1 | `docs(rules): add cross-references and scope sections` | Both rules files | grep for cross-refs |
| 2 | `docs(rules): unify section type documentation` | Both rules files | grep for both types |
| 3+4 | `docs(rules): add overflow prevention and quality checklist` | Both rules files | grep for sections |
| 5 | No commit | N/A | PPTX generation |

---

## Success Criteria

### Verification Commands
```bash
# All cross-references present
grep -c "protocol-technical-reports.md" .sisyphus/rules/technical-report-generation.md  # Expected: ≥2
grep -c "technical-report-generation.md" .sisyphus/rules/protocol-technical-reports.md  # Expected: ≥2

# Both section types documented
grep -c "type: bullets" .sisyphus/rules/technical-report-generation.md  # Expected: ≥1
grep -c "type: item_list" .sisyphus/rules/technical-report-generation.md  # Expected: ≥1

# Overflow prevention in both
grep -c "Overflow Prevention" .sisyphus/rules/technical-report-generation.md  # Expected: 1
grep -c "Overflow Prevention" .sisyphus/rules/protocol-technical-reports.md  # Expected: 1

# PPTX generation works
python -m utilities.pptx_helper --type technical \
  --data reports/packet_taxonomy/technical_report_ue.yaml \
  --output /tmp/final_test.pptx --toc -v  # Expected: Success
```

### Final Checklist
- [x] Both files have Scope sections
- [x] Both files have Related Rules sections with links
- [x] Both files have Precedence rules
- [x] Both files document `bullets` and `item_list` as valid
- [x] `technical-report-generation.md` has Overflow Prevention
- [x] `technical-report-generation.md` has Quality Checklist
- [x] `protocol-technical-reports.md` has Adding New Protocols template
- [x] Existing YAML reports still generate PPTX successfully
