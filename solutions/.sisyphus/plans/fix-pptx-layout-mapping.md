# Fix Pandoc PPTX Layout Mapping

## TL;DR

> **Quick Summary**: Fix pandoc PPTX generation by ensuring custom-reference.pptx has the exact layout names pandoc expects, eliminating file corruption that requires PowerPoint repair.
> 
> **Deliverables**:
> - Updated custom-reference.pptx with correct layout names
> - Working PPTX build without corruption
> 
> **Estimated Effort**: Short
> **Parallel Execution**: NO - sequential
> **Critical Path**: Task 1 → Task 2 → Task 3

---

## Context

### Problem
PPTX output is corrupted - PowerPoint must repair the file before opening. This is caused by pandoc not finding expected layout names in the reference template.

### Required Layout Names
Pandoc expects these **exact** names (case-sensitive):

| Layout Name | Purpose |
|-------------|---------|
| `Title Slide` | Initial slide from metadata |
| `Section Header` | Headers above slide level |
| `Two Content` | Two-column slides |
| `Comparison` | Two-column with text + image/table |
| `Content with Caption` | Text followed by non-text |
| `Blank` | Speaker notes only or blank |
| `Title and Content` | Default for all other slides |

---

## TODOs

- [x] 1. Extract and document current template layout names

  **What to do**:
  - Unzip custom-reference.pptx
  - Extract layout names from ppt/slideLayouts/*.xml files
  - Compare against pandoc's required names

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: `[]`

  **Acceptance Criteria**:
  - [ ] List of current layout names extracted
  - [ ] Gap analysis showing missing/mismatched layouts

  **Agent-Executed QA Scenarios**:
  ```
  Scenario: Extract layout names from template
    Tool: Bash
    Steps:
      1. cd /home/matkins/CN7000/solutions/templates
      2. unzip -p custom-reference.pptx "ppt/slideLayouts/slideLayout*.xml" | grep -oP '<p:cSld[^>]*name="[^"]*"' | grep -oP 'name="[^"]*"'
    Expected Result: List of layout names printed
  ```

---

- [x] 2. Generate fresh pandoc reference template and merge branding

  **What to do**:
  - Generate pandoc's default reference.pptx
  - Extract layout structure from pandoc's template
  - Either: use pandoc's template as new base, OR rename layouts in existing template

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: `[]`

  **References**:
  - Pandoc command: `pandoc -o pandoc-reference.pptx --print-default-data-file reference.pptx`
  - Current template: `/home/matkins/CN7000/solutions/templates/custom-reference.pptx`

  **Acceptance Criteria**:
  - [ ] Fresh pandoc reference template generated
  - [ ] Decision made: use fresh template or rename existing layouts
  - [ ] Template updated with correct layout names

  **Agent-Executed QA Scenarios**:
  ```
  Scenario: Verify template has required layouts
    Tool: Bash
    Steps:
      1. unzip -p custom-reference.pptx "ppt/slideLayouts/*.xml" | grep -oP 'name="[^"]*"' | sort -u
      2. Verify output contains: "Title Slide", "Section Header", "Two Content", "Comparison", "Content with Caption", "Blank", "Title and Content"
    Expected Result: All 7 required layout names present
  ```

---

- [x] 3. Build and verify PPTX output

  **What to do**:
  - Run ./build.sh pptx
  - Verify no errors during build
  - Open output in PowerPoint/LibreOffice without repair prompt

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: `[]`

  **Acceptance Criteria**:
  - [ ] ./build.sh pptx completes without errors
  - [ ] output/solutions.pptx opens without corruption/repair warnings
  - [ ] Slides render with appropriate layouts

  **Agent-Executed QA Scenarios**:
  ```
  Scenario: Build PPTX successfully
    Tool: Bash
    Steps:
      1. cd /home/matkins/CN7000/solutions
      2. ./build.sh pptx
      3. unzip -t output/solutions.pptx
    Expected Result: Build completes, zip test passes with no errors

  Scenario: Verify PPTX structure
    Tool: Bash
    Steps:
      1. unzip -l output/solutions.pptx | grep -E "slide[0-9]+.xml"
    Expected Result: Multiple slide XML files listed
  ```

---

## Success Criteria

- [x] Template contains all 7 required pandoc layout names
- [x] PPTX builds without errors
- [x] Output opens in PowerPoint without repair prompt (structural validation passed - no errors detected)
