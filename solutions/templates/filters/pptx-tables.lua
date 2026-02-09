local CONFIG = {
    min_font_size = 14,
    max_slide_rows = 12,
    value_add_split = true,
}

local table_count = 0

local function cell_text_length(cell)
    local length = 0
    pandoc.walk_block(pandoc.Div(cell.contents), {
        Str = function(el)
            length = length + #el.text
        end,
        Space = function()
            length = length + 1
        end
    })
    return length
end

local function cell_to_text(cell)
    local text = ""
    pandoc.walk_block(pandoc.Div(cell.contents), {
        Str = function(el)
            text = text .. el.text
        end,
        Space = function()
            text = text .. " "
        end
    })
    return text
end

local function calculate_column_widths(tbl)
    local num_cols = #tbl.colspecs
    local max_lengths = {}
    
    for i = 1, num_cols do
        max_lengths[i] = 0
    end
    
    if tbl.head and tbl.head.rows then
        for _, row in ipairs(tbl.head.rows) do
            for i, cell in ipairs(row.cells) do
                local len = cell_text_length(cell)
                if len > max_lengths[i] then
                    max_lengths[i] = len
                end
            end
        end
    end
    
    for _, body in ipairs(tbl.bodies) do
        for _, row in ipairs(body.body) do
            for i, cell in ipairs(row.cells) do
                local len = cell_text_length(cell)
                if len > max_lengths[i] then
                    max_lengths[i] = len
                end
            end
        end
    end
    
    local total = 0
    for _, len in ipairs(max_lengths) do
        total = total + math.max(len, 5)
    end
    
    local widths = {}
    for i, len in ipairs(max_lengths) do
        widths[i] = math.max(len, 5) / total
    end
    
    return widths
end

local function is_value_add_row(row)
    if #row.cells > 0 then
        local text = cell_to_text(row.cells[1])
        return text:match("Value%-Add") ~= nil
    end
    return false
end

local function is_category_row(row)
    if #row.cells > 0 then
        local text = cell_to_text(row.cells[1])
        return text:match("^%*%*") and text:match("%*%*$")
    end
    return false
end

local function find_value_add_split(rows)
    for i, row in ipairs(rows) do
        if is_value_add_row(row) then
            return i
        end
    end
    return nil
end

local function make_empty_caption()
    return {long = {}, short = nil}
end

local function clone_table_simple(original, body_rows)
    local new_colspecs = {}
    for i, spec in ipairs(original.colspecs) do
        new_colspecs[i] = {spec[1], spec[2]}
    end
    
    local new_head = original.head
    
    local new_bodies = {}
    if #body_rows > 0 then
        local body_attr = pandoc.Attr()
        local row_head_columns = 0
        local intermediate_head = {}
        table.insert(new_bodies, {
            attr = body_attr,
            row_head_columns = row_head_columns,
            head = intermediate_head,
            body = body_rows
        })
    end
    
    return pandoc.Table(
        make_empty_caption(),
        new_colspecs,
        new_head,
        new_bodies,
        original.foot
    )
end

local function split_table_at_value_add(tbl)
    local results = {}
    
    local all_rows = {}
    for _, body in ipairs(tbl.bodies) do
        for _, row in ipairs(body.body) do
            table.insert(all_rows, row)
        end
    end
    
    local split_point = find_value_add_split(all_rows)
    
    if not split_point or split_point <= 1 then
        return {tbl}
    end
    
    local first_rows = {}
    for i = 1, split_point - 1 do
        table.insert(first_rows, all_rows[i])
    end
    
    if #first_rows > 0 then
        local first_table = clone_table_simple(tbl, first_rows)
        table.insert(results, first_table)
    end
    
    local second_rows = {}
    for i = split_point, #all_rows do
        table.insert(second_rows, all_rows[i])
    end
    
    if #second_rows > 0 then
        local second_table = clone_table_simple(tbl, second_rows)
        table.insert(results, second_table)
    end
    
    return results
end

local function split_large_table(tbl, max_rows)
    local results = {}
    
    local all_rows = {}
    for _, body in ipairs(tbl.bodies) do
        for _, row in ipairs(body.body) do
            table.insert(all_rows, row)
        end
    end
    
    if #all_rows <= max_rows then
        return {tbl}
    end
    
    local chunk_start = 1
    
    while chunk_start <= #all_rows do
        local chunk_end = math.min(chunk_start + max_rows - 1, #all_rows)
        
        if chunk_end < #all_rows then
            for i = chunk_end, chunk_start + 1, -1 do
                if is_category_row(all_rows[i]) then
                    chunk_end = i - 1
                    break
                end
            end
        end
        
        local chunk_rows = {}
        for i = chunk_start, chunk_end do
            table.insert(chunk_rows, all_rows[i])
        end
        
        if #chunk_rows > 0 then
            local chunk_table = clone_table_simple(tbl, chunk_rows)
            table.insert(results, chunk_table)
        end
        
        chunk_start = chunk_end + 1
    end
    
    return results
end

local function extract_caption_text(caption)
    if not caption or not caption.long or #caption.long == 0 then
        return nil
    end
    
    local text = pandoc.utils.stringify(caption.long)
    
    text = text:gsub("%s*{#[^}]+}%s*$", "")
    text = text:gsub("^%s+", ""):gsub("%s+$", "")
    
    if text == "" then
        return nil
    end
    
    return text
end

function Table(tbl)
    table_count = table_count + 1
    
    local widths = calculate_column_widths(tbl)
    for i, width in ipairs(widths) do
        if tbl.colspecs[i] then
            tbl.colspecs[i][2] = width
        end
    end
    
    local caption_text = extract_caption_text(tbl.caption)
    
    local row_count = 0
    for _, body in ipairs(tbl.bodies) do
        row_count = row_count + #body.body
    end
    
    local blocks = {}
    
    if caption_text then
        table.insert(blocks, pandoc.Header(3, pandoc.Str(caption_text)))
    end
    
    tbl.caption = make_empty_caption()
    
    if row_count > CONFIG.max_slide_rows then
        local split_tables = {}
        
        if CONFIG.value_add_split then
            split_tables = split_table_at_value_add(tbl)
        else
            split_tables = {tbl}
        end
        
        local final_tables = {}
        for _, t in ipairs(split_tables) do
            local sub_splits = split_large_table(t, CONFIG.max_slide_rows)
            for _, st in ipairs(sub_splits) do
                table.insert(final_tables, st)
            end
        end
        
        if #final_tables > 1 then
            for i, t in ipairs(final_tables) do
                table.insert(blocks, t)
                if i < #final_tables then
                    table.insert(blocks, pandoc.HorizontalRule())
                    if caption_text then
                        table.insert(blocks, pandoc.Header(3, pandoc.Str(caption_text .. " (cont.)")))
                    end
                end
            end
            return blocks
        end
    end
    
    table.insert(blocks, tbl)
    return blocks
end

function Meta(meta)
    meta['fontsize'] = pandoc.MetaString(tostring(CONFIG.min_font_size) .. "pt")
    return meta
end

return {
    {Meta = Meta},
    {Table = Table}
}
