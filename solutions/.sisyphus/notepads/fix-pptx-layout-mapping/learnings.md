# Learnings: PPTX Layout Mapping Fix

## 2026-02-06 Session: ses_3d03e2ed2ffeiw4k5t2CQNWJY8

### Pandoc PPTX Layout Requirements

Pandoc expects these **exact** layout names (case-sensitive) in the reference template:

| Layout Name | Purpose | Type Attribute |
|-------------|---------|----------------|
| `Title Slide` | Initial slide from metadata | `title` |
| `Section Header` | Headers above slide level | `secHead` |
| `Two Content` | Two-column slides | `twoObj` |
| `Comparison` | Two-column with text + image/table | `twoTxTwoObj` |
| `Content with Caption` | Text followed by non-text | `objTx` |
| `Blank` | Speaker notes only or blank | `blank` |
| `Title and Content` | Default for all other slides | `obj` |

### Original Template Issues

The Cornelis custom-reference.pptx had 41 layouts but was missing:
- `Comparison` - completely absent
- `Content with Caption` - completely absent
- `Blank` - existed as "Blank Layout" (wrong name)

### Fix Applied

1. **Renamed**: `Blank Layout` → `Blank` in slideLayout5.xml
2. **Added**: `Comparison` as slideLayout42.xml (copied from pandoc default)
3. **Added**: `Content with Caption` as slideLayout43.xml (copied from pandoc default)
4. **Updated**: `[Content_Types].xml` with new layout entries
5. **Updated**: `slideMaster1.xml.rels` with relationships to new layouts
6. **Created**: `_rels/slideLayout42.xml.rels` and `_rels/slideLayout43.xml.rels`

### Key Technical Details

- Layout names are in `<p:cSld name="Layout Name">` element
- Each layout needs:
  - The XML file in `ppt/slideLayouts/`
  - A rels file in `ppt/slideLayouts/_rels/`
  - Entry in `[Content_Types].xml`
  - Relationship in `ppt/slideMasters/_rels/slideMaster1.xml.rels`

### Commands for Future Reference

Extract layout names from PPTX:
```bash
unzip -p template.pptx "ppt/slideLayouts/*.xml" | grep -oP 'name="[^"]*"' | sort -u
```

Generate pandoc default reference:
```bash
pandoc -o pandoc-reference.pptx --print-default-data-file reference.pptx
```

### Remaining Manual Verification

The final success criterion requires opening `output/solutions.pptx` in PowerPoint to confirm no repair prompt appears. This cannot be automated.

**BLOCKER**: Manual verification required - user must open the file in PowerPoint/LibreOffice to confirm no repair prompt.

**File to verify**: `/home/matkins/CN7000/solutions/output/solutions.pptx`
