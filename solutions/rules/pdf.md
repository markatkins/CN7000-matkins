# PDF Generation Rules

Rules for generating PDF output from markdown.

## Generation Method

Use Typst as the PDF engine via a two-step process:

1. Pandoc converts markdown to Typst format
2. Typst compiles to PDF

```bash
# Step 1: Markdown -> Typst
pandoc solutions.md \
    --from markdown \
    --to typst \
    --lua-filter=typst-compat.lua \
    --toc \
    --toc-depth=3 \
    -o temp.typ

# Step 2: Typst -> PDF
typst compile temp.typ solutions.pdf
```

## Why Typst

- Modern, fast PDF generation
- Better table handling than LaTeX
- Native Unicode support (✓, etc.)
- Simpler syntax for customization

## Compatibility Filter (typst-compat.lua)

The `typst-compat.lua` filter handles pandoc 3.1.3 → Typst compatibility issues:

| Pandoc Element | Typst Output | Purpose |
|---------------|-------------|---------|
| `HorizontalRule` (`---`) | `#line(length: 100%)` | Pandoc doesn't convert `---` to Typst natively |
| `BlockQuote` (`> text`) | `Div` with "note" class | Preserves blockquote content as styled block |

### BlockQuote Handling

The `solutions.md` file uses blockquotes for important notes (e.g., the Scale-Up NIC disclaimer). Without this filter, pandoc's Typst writer may not render blockquotes correctly. The filter converts them to Div elements with a "note" class, which Typst renders as styled blocks.

## Page Layout

| Setting | Value |
|---------|-------|
| Paper size | US Letter (default) |
| Margins | Typst defaults |
| Font | Typst defaults |

## Table of Contents

- Auto-generated via `--toc`
- Depth: 3 levels (H1, H2, H3)

## Customization

For custom styling, create a Typst template and use:

```bash
typst compile --input template=custom.typ temp.typ output.pdf
```

## Installation

Typst must be installed:
- macOS: `brew install typst`
- Linux: See https://github.com/typst/typst/releases
- Verify: `typst --version`

## Files

| File | Purpose |
|------|---------|
| `build.sh` | Build script with `build_pdf()` function |
| `templates/filters/typst-compat.lua` | Pandoc filter for Typst compatibility |

## Known Limitations

1. **Tables**: Very wide tables may overflow page margins
2. **Branding**: For corporate branding, need custom Typst template
3. **Direct pandoc**: `--pdf-engine=typst` has issues with pandoc 3.1.3; use two-step process instead
