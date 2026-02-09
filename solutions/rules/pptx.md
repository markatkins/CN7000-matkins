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

## Build Configuration

From `build.sh`:
```bash
pandoc --to pptx \
    --reference-doc=custom-reference.pptx \
    --lua-filter=pptx-tables.lua \
    --slide-level=3
```

- `--slide-level=3`: H3 headers create new slides

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

1. **PPTX Repair Issue (OPEN)**: PowerPoint may report the generated PPTX needs repair when opening. This occurs after post-processing and is under investigation. The file opens correctly after repair. Possible causes:
   - Slides referencing deleted layouts not fully caught by post-processor
   - `presentation.xml` may reference layouts that were deleted
   - Pandoc's fallback layouts may have different slide master references than template layouts
2. **Missing Layouts**: If template lacks required layouts, pandoc falls back to its built-in defaults which may cause formatting issues or require PowerPoint to repair the file
3. **Complex Tables**: Very wide tables may not fit on slides
4. **Images**: Not currently supported in table cells
5. **Layout Selection**: Pandoc does not expose layout selection to Lua filters — all layout remapping must be done via Python post-processing
