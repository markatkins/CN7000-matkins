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

- Primary: xelatex with 1" margins, 11pt font
- Fallback: LibreOffice conversion from DOCX
- For branded PDFs, use DOCX → PDF

---

## File Locations

| File | Purpose |
|------|---------|
| `rules.md` | This index file |
| `rules/common.md` | Shared rules |
| `rules/markdown.md` | Source authoring rules |
| `rules/docx.md` | Word generation rules |
| `rules/pptx.md` | PowerPoint generation rules |
| `rules/pdf.md` | PDF generation rules |
| `templates/filters/pptx-tables.lua` | PPTX Lua filter |
| `templates/filters/docx-format.lua` | DOCX Lua filter |
| `templates/filters/docx-postprocess.py` | DOCX post-processor |
| `build.sh` | Build script |
