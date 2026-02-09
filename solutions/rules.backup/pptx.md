# PowerPoint Generation Rules

Rules for generating PPTX output from markdown.

## Slide Layout Requirements

The reference template (`custom-reference.pptx`) must contain these exact layout names:

| Pandoc Layout | Template Layout Name | Purpose |
|---------------|---------------------|---------|
| Title Slide | Title | Initial slide from metadata (title, author, date) |
| Section Header | Section Header | Section headers (H1, H2 above slide level) |
| Two Content | Title and Content - 2 Column | Two-column slides |
| Comparison | Title and Content - 2 Column | Two-column with text + image/table |
| Content with Caption | Content with Caption | Text followed by non-text content |
| Blank | Blank | Slides with only speaker notes or blank |
| Title and Content | title and 1 content | Default layout for all other slides |

**Note**: Layout names are case-sensitive and must match exactly.

### Layout Name Mapping

Pandoc expects standard layout names, but our template uses different names. The mapping is:

| Pandoc Expects | Our Template Has |
|----------------|------------------|
| Title Slide | Title |
| Two Content | Title and Content - 2 Column |
| Comparison | Title and Content - 2 Column |
| Title and Content | title and 1 content |

**Warning**: If pandoc can't find a layout, it falls back to its built-in defaults which may cause formatting issues or require PowerPoint to repair the file.

## Build Configuration

From `build.sh`:
```bash
pandoc --to pptx \
    --reference-doc=custom-reference.pptx \
    --lua-filter=pptx-tables.lua \
    --slide-level=3
```

- `--slide-level=3`: H3 headers create new slides

## Table Formatting

Configuration in `pptx-tables.lua`:

| Setting | Value | Description |
|---------|-------|-------------|
| max_slide_rows | 12 | Maximum table rows per slide |
| min_font_size | 14pt | Minimum font size for readability |
| value_add_split | true | Split tables at "Value-Add" rows |

### Column Widths

Column widths are calculated proportionally based on content length:
1. Measure max text length in each column (header + all cells)
2. Minimum column width: 5 characters equivalent
3. Total width distributed proportionally

### Table Splitting

Tables exceeding 12 rows are split across multiple slides:

1. **Value-Add Split**: First split at rows containing "Value-Add"
2. **Category Split**: Then split at category boundaries (bold rows)
3. **Row Limit Split**: Finally split at max_slide_rows if still too large

## Slide Titles

Table captions become slide titles:

1. Extract caption from `Table: <caption> {#tbl:ref}` format
2. Strip the `{#tbl:ref}` reference
3. Create H3 header with caption text
4. H3 becomes slide title in PPTX

### Continuation Slides

When tables split across slides:
- First slide: original caption as title
- Subsequent slides: caption + " (cont.)" suffix

Example:
- Slide 1: "Scale-Out AI Workload Solutions"
- Slide 2: "Scale-Out AI Workload Solutions (cont.)"

## Horizontal Rules

`---` in markdown creates slide breaks:
- Use between tables to force new slides
- Filter converts to appropriate PPTX structure

## Known Limitations

1. **Missing Layouts**: If template lacks required layouts, pandoc falls back to defaults (may cause formatting issues)
2. **Complex Tables**: Very wide tables may not fit on slides
3. **Images**: Not currently supported in table cells
