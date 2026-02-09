-- typst-compat.lua
-- Filter to handle pandoc -> typst compatibility issues

function HorizontalRule()
    -- Replace horizontal rule with a Typst line command
    return pandoc.RawBlock('typst', '#line(length: 100%)')
end

function BlockQuote(el)
    -- Convert blockquote to a styled block
    return pandoc.Div(el.content, pandoc.Attr("", {"note"}))
end

return {
    {HorizontalRule = HorizontalRule},
    {BlockQuote = BlockQuote}
}
