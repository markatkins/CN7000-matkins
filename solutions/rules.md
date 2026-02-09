# Solutions Matrix Rules

Rules are organized by output format in the `rules/` directory:

- [Common Rules](rules/common.md) - shared across all formats
- [Markdown Rules](rules/markdown.md) - source authoring
- [DOCX Rules](rules/docx.md) - Word document generation
- [PPTX Rules](rules/pptx.md) - PowerPoint generation
- [PDF Rules](rules/pdf.md) - PDF generation

---

## Quick Reference

### Content Rules (from [common.md](rules/common.md))

- Minimize cell text, use glossary for acronyms
- Use ✓ for fully supported features
- Use "(island)" for heterogeneous interop
- Scale: Small-Medium ≤10K, Large 10K-93K, Hyperscalar 100K-1.44M

### Markdown Rules (from [markdown.md](rules/markdown.md))

- Table caption format: `Table: <caption> {#tbl:ref}`
- Do NOT include "CN7000" in column headers
- H1 = title, H2 = sections, glossary at end

### PPTX Rules (from [pptx.md](rules/pptx.md))

- Max 12 rows per slide
- Min 14pt font
- Split tables at "Value-Add" rows
- Caption becomes slide title
- Continuation slides: "(cont.)" suffix

### DOCX Rules (from [docx.md](rules/docx.md))

- Thin black table borders (all edges)
- Bold header rows
- Zero cell indentation
- Caption format: `Table {STYLEREF}-{SEQ}: <caption>`
- Document properties: Item Description, Doc Type=Requirements, Classification=Confidential

### PDF Rules (from [pdf.md](rules/pdf.md))

- Two-step: pandoc → Typst source → `typst compile` → PDF
- Typst compatibility filter handles HorizontalRule and BlockQuote
- For branded PDFs, use DOCX → PDF conversion

---

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
