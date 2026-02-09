# Markdown Source Rules

Rules for authoring the source markdown files.

## Table Headers

1. Do NOT include "CN7000" in table column headers - it is implied
2. Column headers should be concise:
   - "Small-Medium Scale" (not "CN7000 Small-Medium Scale")
   - "Large Scale"
   - "Hyperscalar"

## Cell Content

1. **Minimize characters in cells** - brevity is paramount
2. Use checkmarks (✓) when a feature is fully supported with no qualifications
3. Use parentheses for qualifications only when necessary:
   - "(island)" for heterogeneous interop
   - "(interop)" for interoperability mode
4. Do NOT expand acronyms in table cells - define them in the glossary
5. If both options of a pair are supported (e.g., SDR and Packet Spray), use only ✓
6. If only one option is supported, indicate which one in parentheses

## Table Captions

Format: `Table: <Caption Text> {#tbl:reference-id}`

Example:
```markdown
Table: Scale-Out AI Workload Solutions {#tbl:scale-out-ai}
```

- Caption text becomes the slide title in PPTX output
- Reference ID is used for cross-references and List of Tables
- Do NOT include "Table N:" prefix - numbering is automatic

## Document Structure

```
# Document Title (H1)

## Major Section (H2)

Table: Caption {#tbl:ref}

| Header | Header |
|--------|--------|
| Cell   | Cell   |

## Another Section (H2)

...

## Glossary (H2)

**ACRONYM** - Definition
```

- H1: Document title (one per document)
- H2: Major sections
- Tables follow section headers with caption line
- Glossary at end of document

## Cross-References

Use pandoc cross-reference syntax:
- `@tbl:scale-out-ai` - reference to table
- Creates hyperlinks in DOCX and PDF output

## Horizontal Rules

Use `---` to create slide breaks in PPTX output:
```markdown
Table: First Table {#tbl:first}
| ... |

---

Table: Second Table {#tbl:second}
| ... |
```
