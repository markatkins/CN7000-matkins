# Cornelis Networks PowerPoint Template Specification

Template: `Standard PPT Template_Light.potx`  
Version: New Cornelis Brand  
Format: Widescreen 16:9 (13.33" × 7.50")

---

## Quick Reference

### Progress Reports
| Use Case | Layout Index | Layout Name |
|----------|--------------|-------------|
| Title slide | 1 | Cover with motion |
| Status update | 8 | title and 1 content |
| Item list with context | 9 | Title subtitle and content |
| Side-by-side comparison | 13 | Title and Content - 2 Column |
| Data/metrics table | 30 | Title details and Table |
| Section divider | 37 | Section Header |

### Technical Presentations
| Use Case | Layout Index | Layout Name |
|----------|--------------|-------------|
| Title slide | 1 | Cover with motion |
| Standard content | 8 | title and 1 content |
| Text + diagram/image | 25 | 1/2 Content and Picture Insert |
| Data table | 30 | Title details and Table |
| Comparison | 13 | Title and Content - 2 Column |
| Custom/code blocks | 5 | Blank Layout |
| Section divider | 37 | Section Header |

---

## Brand Colors

Color Scheme: **New Cornelis Brand**

| Name | Hex | RGB | Theme Key | Usage |
|------|-----|-----|-----------|-------|
| Primary Purple | #6400B9 | (100, 0, 185) | dk1 | Main brand color, headings |
| Deep Purple | #3D0070 | (61, 0, 112) | dk2 | Dark accents |
| White | #FFFFFF | (255, 255, 255) | lt1 | Backgrounds |
| Bright Purple | #991DFF | (153, 29, 255) | lt2 | Highlights |
| Accent Purple | #8B00FE | (139, 0, 254) | accent1 | Links, emphasis |
| Accent 2 | #991DFF | (153, 29, 255) | accent2 | Secondary emphasis |
| Light Purple | #AD53FD | (173, 83, 253) | accent3 | Tertiary elements |
| Dark Gray | #35343C | (53, 52, 60) | accent4 | Body text |
| Medium Gray | #4C4B57 | (76, 75, 87) | accent5 | Secondary text |
| Light Gray | #9D9CAA | (157, 156, 170) | accent6 | Subtle elements |

### Python Color Constants

```python
from pptx.dml.color import RGBColor

CORNELIS_COLORS = {
    "primary_purple": RGBColor(100, 0, 185),    # #6400B9
    "deep_purple": RGBColor(61, 0, 112),        # #3D0070
    "bright_purple": RGBColor(153, 29, 255),    # #991DFF
    "white": RGBColor(255, 255, 255),           # #FFFFFF
    "accent_purple": RGBColor(139, 0, 254),     # #8B00FE
    "light_purple": RGBColor(173, 83, 253),     # #AD53FD
    "dark_gray": RGBColor(53, 52, 60),          # #35343C
    "medium_gray": RGBColor(76, 75, 87),        # #4C4B57
    "light_gray": RGBColor(157, 156, 170),      # #9D9CAA
}
```

---

## Fonts

| Role | Font Family | Weight |
|------|-------------|--------|
| Major (Headings) | Saira Expanded | SemiBold |
| Minor (Body) | Saira | Regular |

**Note**: Saira fonts must be installed on the system. If unavailable, PowerPoint will substitute a fallback font.

---

## Key Slide Layouts

### Layout 1: Cover with motion
**Best for**: Title slides with presenter information

| Placeholder | Index | Type |
|-------------|-------|------|
| Title | 0 | title |
| Subtitle | 1 | subTitle |
| Presenter Name | 11 | body |
| Presenter Info | 12 | body |
| Presenter Name 2 | 13 | body |

### Layout 5: Blank Layout
**Best for**: Custom content, code blocks, freeform layouts

No placeholders - add shapes manually.

### Layout 8: title and 1 content
**Best for**: Standard content slides, bullet lists

| Placeholder | Index | Type |
|-------------|-------|------|
| Title | 0 | title |
| Content | 1 | body |

### Layout 9: Title subtitle and content
**Best for**: Content with additional context

| Placeholder | Index | Type |
|-------------|-------|------|
| Title | 0 | title |
| Subtitle | 13 | body |
| Content | 1 | body |

### Layout 13: Title and Content - 2 Column
**Best for**: Comparisons, before/after, plan vs actual

| Placeholder | Index | Type |
|-------------|-------|------|
| Title | 0 | title |
| Left Content | 1 | body |
| Right Content | 11 | body |

### Layout 25: 1/2 Content and Picture Insert
**Best for**: Text with accompanying image/diagram

| Placeholder | Index | Type |
|-------------|-------|------|
| Title | 0 | title |
| Content | 1 | body |
| Picture | 13 | pic |

### Layout 30: Title details and Table
**Best for**: Data tables with description

| Placeholder | Index | Type |
|-------------|-------|------|
| Title | 0 | title |
| Description | 10 | body |
| Table | 11 | tbl |

### Layout 37: Section Header
**Best for**: Section dividers

| Placeholder | Index | Type |
|-------------|-------|------|
| Title | 0 | title |
| Subtitle | 1 | body |

---

## All Slide Layouts (0-38)

| Index | Name | Key Placeholders | Best Use |
|-------|------|------------------|----------|
| 1 | Cover with motion | title(0), subtitle(1), presenter(11-13) | Title with presenter |
| 2 | Cover Plain presenter on right | title(0), presenter(11-14) | Alt title slide |
| 3 | 1_Cover Plain presenter on right | title(0), presenter(11-14) | Alt title slide |
| 4 | Cover B | title(0), subtitle(1), body(2-4) | Alt cover |
| 5 | Blank Layout | (none) | Custom content |
| 6 | Blank with logo | (none) | Custom with branding |
| 7 | 1_Title Only | title(0) | Title only |
| 8 | title and 1 content | title(0), body(1) | Standard content |
| 9 | Title subtitle and content | title(0), subtitle(13), body(1) | Content with context |
| 10 | 2_Title + Content + background | title(0), body(1) | Content with bg |
| 11 | 3_Title + Content + background | title(0), body(1) | Content with bg |
| 12 | Title and 3 Claims | title(0), body(10-18) | Three claims |
| 13 | Title and Content - 2 Column | title(0), left(1), right(11) | Comparison |
| 14 | B/W Half | title(0), body(1,11,12) | Half layout |
| 15 | 1/2 Page Title and Content | title(0), text(10,11) | Half page |
| 16 | 1:3 text image with fade | title(0), body(1), footer(11), pic(13) | Text + image |
| 17 | 1/3 Image Left | title(0), body(1), pic(15) | Image left |
| 18 | Image Left 1:3 | title(0), subtitle(13), body(1), pic(15) | Image left |
| 19 | 2_title and 1 content | title(0), body(1) | Content variant |
| 20 | 1_Image Left 1:3 | title(0), body(1), pic(15) | Image left |
| 21 | Image Right 2:3 | title(0), subtitle(13), body(1), pic(15) | Image right |
| 22 | Half Image Right | title(0), subtitle(13), body(1), pic(15) | Half image |
| 23 | Half Image Left | title(0), subtitle(13), body(1), pic(15) | Half image |
| 24 | Title, Text, and intruding Image | title(0), body(1), pic(11) | Overlapping image |
| 25 | 1/2 Content and Picture Insert | title(0), body(1), pic(13) | Text + image |
| 26 | Title content and 3 Images | title(0), text(10), pic(11-13) | Multiple images |
| 27 | 4-to-a-Page | title(0), multiple body | Grid layout |
| 28 | 6-to-a-Page | title(0), multiple body | Grid layout |
| 29 | Picture Above title and details | title(0), text(10), pic(11) | Image above |
| 30 | Title details and Table | title(0), text(10), tbl(11) | Data table |
| 31 | Keyword Slide | title(0) | Emphasis |
| 32 | Image Keyword Slide | pic(15) | Full image |
| 33 | Two Content | title(0), body(1,2) | Two content areas |
| 34 | 3_Blank | multiple body | Complex grid |
| 35 | 4_Blank | title(0), multiple body | Complex grid |
| 36 | 2_Blank | pic(10), text(13) | Image + text |
| 37 | Section Header | title(0), body(1) | Section divider |
| 38 | 1_Cover B | title(0) | Alt cover |
| 39 | 1_title and 1 content | title(0), body(1) | Content variant |

---

## Python Usage Examples

### Loading the Template

```python
from pptx import Presentation
import shutil
import tempfile
import os

def load_potx_template(potx_path):
    """
    Load a .potx template file.
    
    Workaround: python-pptx may reject .potx files due to content type.
    Copy to temp .pptx before loading.
    """
    # Create temp file with .pptx extension
    temp_fd, temp_path = tempfile.mkstemp(suffix='.pptx')
    os.close(temp_fd)
    
    try:
        shutil.copy2(potx_path, temp_path)
        prs = Presentation(temp_path)
        return prs
    finally:
        # Clean up temp file after loading
        if os.path.exists(temp_path):
            os.remove(temp_path)

# Usage
prs = load_potx_template('templates/Standard PPT Template_Light.potx')
```

### Adding a Content Slide (Layout 8)

```python
# Get layout by index
layout = prs.slide_layouts[8]  # "title and 1 content"
slide = prs.slides.add_slide(layout)

# Access title placeholder (always idx=0)
slide.shapes.title.text = "Slide Title"

# Access body placeholder
slide.placeholders[1].text = "• First bullet point\n• Second bullet point\n• Third bullet point"
```

### Adding a Two-Column Comparison (Layout 13)

```python
layout = prs.slide_layouts[13]  # "Title and Content - 2 Column"
slide = prs.slides.add_slide(layout)

slide.shapes.title.text = "Plan vs Actual"
slide.placeholders[1].text = "Planned:\n• Feature A\n• Feature B\n• Feature C"
slide.placeholders[11].text = "Delivered:\n• Feature A ✓\n• Feature B ✓\n• Feature C (80%)"
```

### Adding a Slide with Image (Layout 25)

```python
layout = prs.slide_layouts[25]  # "1/2 Content and Picture Insert"
slide = prs.slides.add_slide(layout)

slide.shapes.title.text = "System Architecture"
slide.placeholders[1].text = "Key components:\n• API Gateway\n• Service Mesh\n• Database Cluster"

# Insert image into picture placeholder
picture_placeholder = slide.placeholders[13]
picture_placeholder.insert_picture('path/to/architecture.png')
```

### Adding a Table Slide (Layout 30)

```python
layout = prs.slide_layouts[30]  # "Title details and Table"
slide = prs.slides.add_slide(layout)

slide.shapes.title.text = "Performance Metrics"
slide.placeholders[10].text = "Q4 2025 Results"

# Get table placeholder and insert table
table_placeholder = slide.placeholders[11]
table = table_placeholder.insert_table(rows=4, cols=3).table

# Set headers
table.cell(0, 0).text = "Metric"
table.cell(0, 1).text = "Target"
table.cell(0, 2).text = "Actual"

# Add data rows
data = [
    ("Latency", "10ms", "8ms"),
    ("Throughput", "1000/s", "1200/s"),
    ("Uptime", "99.9%", "99.95%"),
]
for row_idx, (metric, target, actual) in enumerate(data, start=1):
    table.cell(row_idx, 0).text = metric
    table.cell(row_idx, 1).text = target
    table.cell(row_idx, 2).text = actual
```

### Saving the Presentation

```python
prs.save('output/my_presentation.pptx')
```

---

## Important Notes

1. **Placeholder Access**:
   - Title: `slide.shapes.title` or `slide.placeholders[0]`
   - Other placeholders: `slide.placeholders[idx]`
   - List available: `[p.placeholder_format.idx for p in slide.placeholders]`

2. **Font Availability**: Saira and Saira Expanded fonts must be installed. Without them, PowerPoint substitutes fallback fonts which may affect layout.

3. **Color Application**:
   ```python
   from pptx.dml.color import RGBColor
   from pptx.enum.dml import MSO_THEME_COLOR
   
   # Theme color (preferred for consistency)
   run.font.color.theme_color = MSO_THEME_COLOR.ACCENT_1
   
   # Or explicit RGB
   run.font.color.rgb = RGBColor(100, 0, 185)  # Primary Purple
   ```

4. **Slide Size**: Template is widescreen 16:9 (13.33" × 7.50"). Do not mix with 4:3 content.

5. **.potx Workaround**: The python-pptx library may reject .potx files due to content type validation. Always use the workaround function that copies to a temp .pptx file.
