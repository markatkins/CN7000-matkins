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

## Compatibility Filter

The `typst-compat.lua` filter handles pandoc -> typst compatibility:

- `HorizontalRule` → `#line(length: 100%)`
- `BlockQuote` → styled div (note class)

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
