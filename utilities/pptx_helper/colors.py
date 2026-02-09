"""
Cornelis Networks brand color constants for PowerPoint generation.

Usage:
    from utilities.pptx_helper.colors import PRIMARY_PURPLE, CORNELIS_COLORS
    
    # Apply to text
    run.font.color.rgb = PRIMARY_PURPLE
    
    # Or use dict
    run.font.color.rgb = CORNELIS_COLORS["primary_purple"]

Design:
    Colors extracted from the "New Cornelis Brand" theme in the corporate
    PowerPoint template. All colors are RGBColor objects from python-pptx.
"""

from pptx.dml.color import RGBColor

# Primary brand colors
PRIMARY_PURPLE = RGBColor(100, 0, 185)      # #6400B9 - Main brand color, headings
DEEP_PURPLE = RGBColor(61, 0, 112)          # #3D0070 - Dark accents
BRIGHT_PURPLE = RGBColor(153, 29, 255)      # #991DFF - Highlights
WHITE = RGBColor(255, 255, 255)             # #FFFFFF - Backgrounds

# Accent colors
ACCENT_PURPLE = RGBColor(139, 0, 254)       # #8B00FE - Links, emphasis
LIGHT_PURPLE = RGBColor(173, 83, 253)       # #AD53FD - Tertiary elements

# Gray scale
DARK_GRAY = RGBColor(53, 52, 60)            # #35343C - Body text
MEDIUM_GRAY = RGBColor(76, 75, 87)          # #4C4B57 - Secondary text
LIGHT_GRAY = RGBColor(157, 156, 170)        # #9D9CAA - Subtle elements

# Complete color dictionary for programmatic access
CORNELIS_COLORS = {
    "primary_purple": PRIMARY_PURPLE,
    "deep_purple": DEEP_PURPLE,
    "bright_purple": BRIGHT_PURPLE,
    "white": WHITE,
    "accent_purple": ACCENT_PURPLE,
    "light_purple": LIGHT_PURPLE,
    "dark_gray": DARK_GRAY,
    "medium_gray": MEDIUM_GRAY,
    "light_gray": LIGHT_GRAY,
}

# Hex values for reference (useful for documentation or CSS)
CORNELIS_HEX = {
    "primary_purple": "#6400B9",
    "deep_purple": "#3D0070",
    "bright_purple": "#991DFF",
    "white": "#FFFFFF",
    "accent_purple": "#8B00FE",
    "light_purple": "#AD53FD",
    "dark_gray": "#35343C",
    "medium_gray": "#4C4B57",
    "light_gray": "#9D9CAA",
}
