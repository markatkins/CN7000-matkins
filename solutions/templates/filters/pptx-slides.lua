-- pptx-slides.lua
-- Lua filter to handle slide breaks and formatting for PowerPoint

local slide_count = 0

function Header(el)
    if el.level == 3 then
        slide_count = slide_count + 1
    end
    return el
end

function HorizontalRule()
    return pandoc.RawBlock('openxml', '')
end

return {
    {Header = Header},
    {HorizontalRule = HorizontalRule}
}
