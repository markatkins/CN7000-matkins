# Organize Document Format Rules

## TL;DR

> **Quick Summary**: Create a structured rules system with separate rule files for each output format (md, docx, pptx, pdf) plus common rules, with backups of current state.
> 
> **Deliverables**:
> - Backup of current rules.md
> - rules/common.md - shared rules across all formats
> - rules/markdown.md - source markdown authoring rules
> - rules/docx.md - Word document generation rules
> - rules/pptx.md - PowerPoint generation rules  
> - rules/pdf.md - PDF generation rules
> 
> **Estimated Effort**: Medium
> **Parallel Execution**: NO - sequential
> **Critical Path**: Task 1 → Task 2 → Task 3 → Task 4 → Task 5

---

## Context

### Problem
Rules for different output formats have been mixed together or lost. The current rules.md only contains markdown content rules. PPTX rules are embedded in Lua code but not documented. DOCX rules are in Python code but not documented.

### Current State (to preserve)

**rules.md** contains:
- Table header rules (no "CN7000", concise headers)
- Cell content rules (minimize chars, checkmarks, acronyms in glossary)
- Scale specifications (Small-Medium ≤10K, Large 10K-93K, Hyperscalar 100K-1.44M)
- Topology rules (Fat-Tree variants by scale)
- Feature naming conventions (FGAR, ECAR, NSCC, etc.)
- Glossary requirements

**pptx-tables.lua** contains (undocumented):
- min_font_size = 14pt
- max_slide_rows = 12
- value_add_split = true (split at "Value-Add" rows)
- Column widths proportional to content length
- Caption → H3 header conversion for slide titles
- Continuation slides labeled "(cont.)"

**docx-postprocess.py** contains (undocumented):
- Table borders: thin black, all edges
- Header row: bold
- Cell indent: zero
- Caption format: "Table {STYLEREF}-{SEQ}: caption"
- Caption style: "Caption"
- Table of Tables with TOC field
- Page breaks: after title, before/after Table of Tables
- Document properties: Item Description, Doc Type=Requirements, Classification=Confidential

---

## TODOs

- [x] 1. Create backup of current rules

  **What to do**:
  - Copy rules.md to rules.md.backup
  - Record current state of all filter files

  **Acceptance Criteria**:
  - [ ] rules.md.backup exists with original content
  - [ ] Timestamp recorded for backup

---

- [x] 2. Create rules directory structure

  **What to do**:
  - Create /home/matkins/CN7000/solutions/rules/ directory
  - Create placeholder files for each format

  **Acceptance Criteria**:
  - [ ] rules/ directory exists
  - [ ] common.md, markdown.md, docx.md, pptx.md, pdf.md files created

---

- [x] 3. Populate common.md with shared rules

  **What to do**:
  - Extract rules that apply to ALL formats
  - Include: scale specifications, feature naming, glossary requirements

  **Content to include**:
  ```markdown
  # Common Rules (All Formats)
  
  ## Scale Specifications
  - Small-Medium Scale: Max endpoints ≤10K
  - Large Scale: Max endpoints 10K-93K
  - Hyperscalar: Max endpoints 100K-1.44M
  - Always show per-rail values assuming 8 rails
  
  ## Feature Naming Conventions
  - FGAR - Fine-Grained Adaptive Routing (do not expand in tables)
  - ECAR - Entropy Controlled Adaptive Routing
  - Dynamic Route Recovery (not "Fast Route Recovery")
  - NSCC - supports both lossless and lossy
  - RCCC - do not expand
  - Collective Accel - indicate "homogeneous/island only"
  
  ## Glossary Requirements
  - All acronyms MUST be defined in glossary
  - Alphabetically ordered
  - Format: **ACRONYM** - Full expansion and description
  ```

  **Acceptance Criteria**:
  - [ ] common.md contains scale specs
  - [ ] common.md contains feature naming conventions
  - [ ] common.md contains glossary requirements

---

- [x] 4. Populate markdown.md with source authoring rules

  **What to do**:
  - Extract markdown-specific rules from current rules.md
  - Add table caption format rules

  **Content to include**:
  ```markdown
  # Markdown Source Rules
  
  ## Table Headers
  - Do NOT include "CN7000" in column headers
  - Use concise headers: "Small-Medium Scale", "Large Scale", "Hyperscalar"
  
  ## Cell Content
  - Minimize characters - brevity is paramount
  - Use ✓ for fully supported features
  - Use parentheses for qualifications: "(island)"
  - Do NOT expand acronyms - use glossary
  
  ## Table Captions
  - Format: `Table: <Caption Text> {#tbl:reference-id}`
  - Caption text becomes slide title in PPTX
  - Reference ID used for cross-references
  
  ## Document Structure
  - H1: Document title
  - H2: Major sections
  - Tables follow section headers
  - Glossary at end of document
  ```

  **Acceptance Criteria**:
  - [ ] markdown.md contains table header rules
  - [ ] markdown.md contains cell content rules
  - [ ] markdown.md contains caption format rules

---

- [x] 5. Populate pptx.md with PowerPoint generation rules

  **What to do**:
  - Document all rules from pptx-tables.lua
  - Include layout requirements

  **Content to include**:
  ```markdown
  # PowerPoint Generation Rules
  
  ## Slide Layout Requirements
  Template must contain these exact layout names:
  - "Title Slide" - for title slide from metadata
  - "Section Header" - for section headers
  - "Two Content" - for two-column slides
  - "Comparison" - for comparison slides
  - "Content with Caption" - for captioned content
  - "Blank" - for blank slides
  - "Title and Content" - default layout
  
  ## Table Formatting
  - Maximum rows per slide: 12
  - Minimum font size: 14pt
  - Split tables at "Value-Add" rows
  - Column widths: proportional to content length
  
  ## Slide Titles
  - Table caption becomes slide title (H3)
  - Strip "{#ref}" from caption
  - Continuation slides: add "(cont.)" suffix
  
  ## Table Splitting
  - Tables > 12 rows split across slides
  - Split preferentially at category boundaries
  - Each continuation slide gets header row repeated
  ```

  **Acceptance Criteria**:
  - [ ] pptx.md contains layout requirements
  - [ ] pptx.md contains table formatting rules
  - [ ] pptx.md contains slide title rules
  - [ ] pptx.md contains table splitting rules

---

- [x] 6. Populate docx.md with Word generation rules

  **What to do**:
  - Document all rules from docx-postprocess.py
  - Include template requirements

  **Content to include**:
  ```markdown
  # Word Document Generation Rules
  
  ## Template Requirements
  - Use: Standard_Tech Doc Word Template.dotx
  - Title page preserved from template
  - Document properties set automatically
  
  ## Document Properties
  - Item Description: from H1 title
  - Doc Type: "Requirements"
  - Classification: "Confidential"
  - Title: from H1 title
  
  ## Table Formatting
  - Borders: thin black, all edges (top, left, bottom, right, insideH, insideV)
  - Header row: bold
  - Cell indent: zero (no indentation)
  
  ## Table Captions
  - Style: "Caption"
  - Format: "Table {STYLEREF 1 \s}-{SEQ Table \* ARABIC \s 1}: <caption>"
  - Position: above table
  
  ## Document Structure
  - Page break after title page
  - Table of Contents (auto-generated)
  - Page break before Table of Tables
  - Table of Tables (TOC field for tables)
  - Page break after Table of Tables
  - Content sections
  ```

  **Acceptance Criteria**:
  - [ ] docx.md contains template requirements
  - [ ] docx.md contains document property rules
  - [ ] docx.md contains table formatting rules
  - [ ] docx.md contains caption format rules
  - [ ] docx.md contains document structure rules

---

- [x] 7. Populate pdf.md with PDF generation rules

  **What to do**:
  - Document PDF-specific rules
  - Note: currently generated via xelatex or libreoffice fallback

  **Content to include**:
  ```markdown
  # PDF Generation Rules
  
  ## Generation Method
  - Primary: xelatex (if available)
  - Fallback: libreoffice conversion from DOCX
  
  ## Page Layout
  - Margins: 1 inch all sides
  - Font size: 11pt
  
  ## Table of Contents
  - Auto-generated
  - Depth: 3 levels
  
  ## Notes
  - PDF inherits most formatting from LaTeX defaults
  - For branded PDFs, use DOCX → PDF conversion
  ```

  **Acceptance Criteria**:
  - [ ] pdf.md contains generation method
  - [ ] pdf.md contains page layout rules
  - [ ] pdf.md contains TOC rules

---

- [x] 8. Update main rules.md to reference new structure

  **What to do**:
  - Replace rules.md with index pointing to rules/ directory
  - Keep backward compatibility note

  **Content**:
  ```markdown
  # Solutions Matrix Rules
  
  Rules are organized by output format:
  
  - [Common Rules](rules/common.md) - shared across all formats
  - [Markdown Rules](rules/markdown.md) - source authoring
  - [DOCX Rules](rules/docx.md) - Word document generation
  - [PPTX Rules](rules/pptx.md) - PowerPoint generation
  - [PDF Rules](rules/pdf.md) - PDF generation
  
  ## Quick Reference
  
  See individual rule files for details. Key points:
  
  ### Content Rules
  - Minimize cell text, use glossary for acronyms
  - Use ✓ for supported features
  - Table caption format: `Table: <caption> {#tbl:ref}`
  
  ### PPTX Rules
  - Max 12 rows per slide
  - Min 14pt font
  - Split at "Value-Add" rows
  
  ### DOCX Rules
  - Thin black table borders
  - Bold header rows
  - Caption style with field codes
  ```

  **Acceptance Criteria**:
  - [ ] rules.md updated with index
  - [ ] Links to all rule files included

---

## Success Criteria

- [x] Backup of original rules.md exists
- [x] rules/ directory with 5 rule files created
- [x] All current rules documented (none lost)
- [x] PPTX rules from Lua code documented
- [x] DOCX rules from Python code documented
- [x] Main rules.md serves as index
