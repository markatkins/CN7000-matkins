-- pptx-layout-map.lua
-- Maps pandoc's expected layout names to our template's layout names
--
-- Pandoc expects:          Our template has:
-- "Title Slide"         -> "Title"
-- "Two Content"         -> "Title and Content - 2 Column"
-- "Comparison"          -> "Title and Content - 2 Column"
-- "Title and Content"   -> "title and 1 content"

-- This filter runs AFTER pandoc generates the PPTX AST but BEFORE writing
-- Unfortunately, pandoc doesn't expose layout selection to Lua filters for PPTX
-- The layout mapping must be done via post-processing the PPTX XML

-- For now, this filter serves as documentation of the mapping
-- Actual remapping requires a Python post-processor similar to docx-postprocess.py

return {}
