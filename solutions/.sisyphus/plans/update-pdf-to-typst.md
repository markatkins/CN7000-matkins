# Update PDF Generation to Use Typst

## TL;DR

> **Quick Summary**: Update pdf.md rules and build.sh to use Typst instead of xelatex/LibreOffice
> 
> **Deliverables**:
> - Updated rules/pdf.md with Typst configuration
> - Updated build.sh with Typst PDF engine
> 
> **Estimated Effort**: Quick
> **Parallel Execution**: NO

---

## TODOs

- [x] 1. Update rules/pdf.md to document Typst usage

  **Replace content with**:
  ```markdown
  # PDF Generation Rules

  Rules for generating PDF output from markdown.

  ## Generation Method

  Use Typst as the PDF engine:

  ```bash
  pandoc --to pdf \
      --pdf-engine=typst \
      --toc \
      --toc-depth=3
  ```

  ## Why Typst

  - Modern, fast PDF generation
  - Better table handling than LaTeX
  - Native Unicode support (✓, etc.)
  - Simpler syntax for customization

  ## Page Layout

  | Setting | Value |
  |---------|-------|
  | Paper size | US Letter (default) |
  | Margins | Typst defaults |
  | Font | Typst defaults |

  ## Table of Contents

  - Auto-generated via `--toc`
  - Depth: 3 levels (H1, H2, H3)

  ## Installation

  Typst must be installed:
  - macOS: `brew install typst`
  - Linux: See https://github.com/typst/typst/releases
  - Verify: `typst --version`
  ```

---

- [x] 2. Update build.sh to use Typst

  **Replace build_pdf() function with**:
  ```bash
  build_pdf() {
      echo "Building PDF..."
      pandoc "${INPUT_FILE}" \
          --from markdown \
          --to pdf \
          --pdf-engine=typst \
          --toc \
          --toc-depth=3 \
          -o "${OUTPUT_DIR}/solutions.pdf"
      echo "Created: ${OUTPUT_DIR}/solutions.pdf"
  }
  ```

  **Remove**: build_pdf_via_docx() function (no longer needed)

---

## Success Criteria

- [x] rules/pdf.md documents Typst usage
- [x] build.sh uses Typst (two-step process due to pandoc 3.1.3 compatibility)
- [x] PDF builds successfully with Typst (258KB output)
