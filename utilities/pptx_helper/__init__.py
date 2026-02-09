"""
Cornelis Networks PowerPoint Helper Module.

A Python module for generating PowerPoint presentations using the Cornelis
Networks corporate template. Supports progress reports and technical
presentations with brand-compliant styling.

Quick Start:
    >>> from utilities.pptx_helper import create_presentation, save_presentation
    >>> from utilities.pptx_helper.progress_report import add_title_slide, add_status_summary_slide
    >>> 
    >>> # Create presentation
    >>> prs = create_presentation()
    >>> 
    >>> # Add slides
    >>> add_title_slide(prs, "Q4 Report", "Engineering Status", "John Doe", "Engineer")
    >>> add_status_summary_slide(prs, "Sprint Status", open_count=5, closed_count=12)
    >>> 
    >>> # Save
    >>> save_presentation(prs, "output/report.pptx")

Available Functions:
    Core:
        - create_presentation() - Create new presentation from template
        - load_template() - Load template (advanced usage)
        - save_presentation() - Save presentation to file
    
    Layouts:
        - get_layout() - Get layout by name
        - LAYOUTS - Dict of layout name to index
        - CONTENT, TWO_COLUMN, TABLE, etc. - Layout index constants
    
    Colors:
        - CORNELIS_COLORS - Dict of color name to RGBColor
        - PRIMARY_PURPLE, DEEP_PURPLE, etc. - Color constants

Template Documentation:
    See templates/template-spec.md for complete layout and color reference.

Example - Progress Report:
    >>> from utilities.pptx_helper import create_presentation, save_presentation
    >>> from utilities.pptx_helper.progress_report import (
    ...     add_title_slide, add_status_summary_slide, add_item_list_slide
    ... )
    >>> 
    >>> prs = create_presentation()
    >>> add_title_slide(prs, "Weekly Status", "Week 42", "Jane Smith", "PM")
    >>> add_status_summary_slide(prs, "Overview", open_count=3, closed_count=8)
    >>> add_item_list_slide(prs, "Open Items", ["Bug #123", "Feature #456"])
    >>> save_presentation(prs, "status.pptx")

Example - Technical Presentation:
    >>> from utilities.pptx_helper import create_presentation, save_presentation
    >>> from utilities.pptx_helper.technical import (
    ...     add_content_slide, add_table_slide, add_two_column_slide
    ... )
    >>> 
    >>> prs = create_presentation()
    >>> add_content_slide(prs, "Architecture", ["Component A", "Component B"])
    >>> add_table_slide(prs, "Metrics", ["Name", "Value"], [["Latency", "10ms"]])
    >>> save_presentation(prs, "tech.pptx")
"""

from utilities.pptx_helper.core import (
    create_presentation,
    load_template,
    save_presentation,
)
from utilities.pptx_helper.layouts import (
    LAYOUTS,
    get_layout,
    get_placeholder_idx,
    # Layout constants
    COVER,
    BLANK,
    CONTENT,
    CONTENT_WITH_SUBTITLE,
    TWO_COLUMN,
    CONTENT_AND_PICTURE,
    TABLE,
    SECTION_HEADER,
)
from utilities.pptx_helper.colors import (
    CORNELIS_COLORS,
    CORNELIS_HEX,
    # Color constants
    PRIMARY_PURPLE,
    DEEP_PURPLE,
    BRIGHT_PURPLE,
    WHITE,
    ACCENT_PURPLE,
    LIGHT_PURPLE,
    DARK_GRAY,
    MEDIUM_GRAY,
    LIGHT_GRAY,
)

__all__ = [
    # Core functions
    "create_presentation",
    "load_template",
    "save_presentation",
    # Layout functions
    "get_layout",
    "get_placeholder_idx",
    "LAYOUTS",
    # Layout constants
    "COVER",
    "BLANK",
    "CONTENT",
    "CONTENT_WITH_SUBTITLE",
    "TWO_COLUMN",
    "CONTENT_AND_PICTURE",
    "TABLE",
    "SECTION_HEADER",
    # Color dicts
    "CORNELIS_COLORS",
    "CORNELIS_HEX",
    # Color constants
    "PRIMARY_PURPLE",
    "DEEP_PURPLE",
    "BRIGHT_PURPLE",
    "WHITE",
    "ACCENT_PURPLE",
    "LIGHT_PURPLE",
    "DARK_GRAY",
    "MEDIUM_GRAY",
    "LIGHT_GRAY",
]

__version__ = "1.0.0"
