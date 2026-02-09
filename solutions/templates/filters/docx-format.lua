local title_found = false
local table_counter = 0

local table_captions = {
    "Scale-Out AI Workload Solutions",
    "Scale-Out HPC Workload Solutions",
    "Scale-Up AI Workload Solutions",
    "Scale-Up HPC Workload Solutions",
    "Feature Applicability by Solution",
    "Key Differentiators by Solution Type"
}

function Header(el)
    if el.level == 1 and not title_found then
        title_found = true
        return {}
    end
    
    return el
end

function Table(tbl)
    table_counter = table_counter + 1
    
    local caption_text = ""
    if table_counter <= #table_captions then
        caption_text = "Table " .. table_counter .. ": " .. table_captions[table_counter]
    else
        caption_text = "Table " .. table_counter
    end
    
    tbl.caption.long = {pandoc.Plain({pandoc.Str(caption_text)})}
    
    return tbl
end

return {
    {Header = Header},
    {Table = Table}
}