#!/usr/bin/env python3
"""
Post-processor for pandoc-generated DOCX files.

This script:
1. Preserves the title page from the template (removes pandoc's Title paragraph)
2. Sets custom document properties (Item Description, Doc Type, Classification)
3. Sets core Title property
4. Adds page breaks: after title page, before Table of Tables, after Table of Tables
5. Formats tables: borders, bold headers, zero cell indent
6. Converts table captions to Word field codes
"""

import sys
import zipfile
import tempfile
import shutil
import os
import re
from xml.etree import ElementTree as ET

# XML namespaces
WORD_NS = {
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
}

CUSTOM_NS = 'http://schemas.openxmlformats.org/officeDocument/2006/custom-properties'
VT_NS = 'http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes'
CORE_NS = 'http://schemas.openxmlformats.org/package/2006/metadata/core-properties'
DC_NS = 'http://purl.org/dc/elements/1.1/'

# Register namespaces to preserve them in output
for prefix, uri in WORD_NS.items():
    ET.register_namespace(prefix, uri)
ET.register_namespace('', CUSTOM_NS)
ET.register_namespace('vt', VT_NS)
ET.register_namespace('cp', CORE_NS)
ET.register_namespace('dc', DC_NS)

W_NS = WORD_NS['w']

# Document metadata - extracted from first H1 in markdown
DOC_TITLE = "CN7000 Solution and Feature Matrices"


def get_text_content(element):
    """Extract all text content from an element and its descendants."""
    text = ''
    for t in element.iter(f'{{{W_NS}}}t'):
        if t.text:
            text += t.text
    return text


def get_para_style(para):
    """Get the style name of a paragraph."""
    pPr = para.find(f'{{{W_NS}}}pPr')
    if pPr is not None:
        pStyle = pPr.find(f'{{{W_NS}}}pStyle')
        if pStyle is not None:
            return pStyle.get(f'{{{W_NS}}}val', '')
    return ''


def create_page_break():
    """Create a paragraph containing a page break."""
    p = ET.Element(f'{{{W_NS}}}p')
    r = ET.SubElement(p, f'{{{W_NS}}}r')
    br = ET.SubElement(r, f'{{{W_NS}}}br')
    br.set(f'{{{W_NS}}}type', 'page')
    return p


def create_field(instr_text):
    """Create Word field code runs."""
    runs = []
    
    # Begin field
    r_begin = ET.Element(f'{{{W_NS}}}r')
    fldChar_begin = ET.SubElement(r_begin, f'{{{W_NS}}}fldChar')
    fldChar_begin.set(f'{{{W_NS}}}fldCharType', 'begin')
    runs.append(r_begin)
    
    # Field instruction
    r_instr = ET.Element(f'{{{W_NS}}}r')
    instrText = ET.SubElement(r_instr, f'{{{W_NS}}}instrText')
    instrText.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
    instrText.text = instr_text
    runs.append(r_instr)
    
    # Separator
    r_sep = ET.Element(f'{{{W_NS}}}r')
    fldChar_sep = ET.SubElement(r_sep, f'{{{W_NS}}}fldChar')
    fldChar_sep.set(f'{{{W_NS}}}fldCharType', 'separate')
    runs.append(r_sep)
    
    # Placeholder text
    r_text = ET.Element(f'{{{W_NS}}}r')
    t_text = ET.SubElement(r_text, f'{{{W_NS}}}t')
    t_text.text = '#'
    runs.append(r_text)
    
    # End field
    r_end = ET.Element(f'{{{W_NS}}}r')
    fldChar_end = ET.SubElement(r_end, f'{{{W_NS}}}fldChar')
    fldChar_end.set(f'{{{W_NS}}}fldCharType', 'end')
    runs.append(r_end)
    
    return runs


def create_text_run(text):
    """Create a text run."""
    r = ET.Element(f'{{{W_NS}}}r')
    t = ET.SubElement(r, f'{{{W_NS}}}t')
    t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
    t.text = text
    return r


def create_caption_paragraph(caption_text):
    """Create a table caption paragraph with Word field codes."""
    p = ET.Element(f'{{{W_NS}}}p')
    
    # Set Caption style
    pPr = ET.SubElement(p, f'{{{W_NS}}}pPr')
    pStyle = ET.SubElement(pPr, f'{{{W_NS}}}pStyle')
    pStyle.set(f'{{{W_NS}}}val', 'Caption')
    
    # Build caption: "Table {STYLEREF}-{SEQ}: caption_text"
    p.append(create_text_run('Table '))
    
    for run in create_field(' STYLEREF 1 \\s '):
        p.append(run)
    
    p.append(create_text_run('-'))
    
    for run in create_field(' SEQ Table \\* ARABIC \\s 1 '):
        p.append(run)
    
    p.append(create_text_run(': ' + caption_text))
    
    return p


def remove_cell_indent(tbl):
    """Remove all cell indentation from a table."""
    for tc in tbl.findall(f'.//{{{W_NS}}}tc'):
        tcPr = tc.find(f'{{{W_NS}}}tcPr')
        if tcPr is None:
            tcPr = ET.Element(f'{{{W_NS}}}tcPr')
            tc.insert(0, tcPr)
        
        # Remove existing margins and set to zero
        tcMar = tcPr.find(f'{{{W_NS}}}tcMar')
        if tcMar is not None:
            tcPr.remove(tcMar)
        
        tcMar = ET.SubElement(tcPr, f'{{{W_NS}}}tcMar')
        for side in ['top', 'left', 'bottom', 'right']:
            margin = ET.SubElement(tcMar, f'{{{W_NS}}}{side}')
            margin.set(f'{{{W_NS}}}w', '0')
            margin.set(f'{{{W_NS}}}type', 'dxa')
        
        # Remove paragraph indentation
        for p in tc.findall(f'{{{W_NS}}}p'):
            pPr = p.find(f'{{{W_NS}}}pPr')
            if pPr is None:
                pPr = ET.Element(f'{{{W_NS}}}pPr')
                p.insert(0, pPr)
            
            ind = pPr.find(f'{{{W_NS}}}ind')
            if ind is not None:
                pPr.remove(ind)
            
            ind = ET.SubElement(pPr, f'{{{W_NS}}}ind')
            ind.set(f'{{{W_NS}}}left', '0')
            ind.set(f'{{{W_NS}}}right', '0')
            ind.set(f'{{{W_NS}}}firstLine', '0')


def set_table_borders(tbl):
    """Set thin black borders on all table edges."""
    tblPr = tbl.find(f'{{{W_NS}}}tblPr')
    if tblPr is None:
        tblPr = ET.SubElement(tbl, f'{{{W_NS}}}tblPr')
        tbl.insert(0, tblPr)
    
    # Remove existing borders
    tblBorders = tblPr.find(f'{{{W_NS}}}tblBorders')
    if tblBorders is not None:
        tblPr.remove(tblBorders)
    
    # Add new borders
    tblBorders = ET.SubElement(tblPr, f'{{{W_NS}}}tblBorders')
    
    for border_type in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']:
        border = ET.SubElement(tblBorders, f'{{{W_NS}}}{border_type}')
        border.set(f'{{{W_NS}}}val', 'single')
        border.set(f'{{{W_NS}}}sz', '4')
        border.set(f'{{{W_NS}}}space', '0')
        border.set(f'{{{W_NS}}}color', '000000')


def set_header_row_bold(tbl):
    """Make the first row of a table bold."""
    rows = tbl.findall(f'{{{W_NS}}}tr')
    if not rows:
        return
    
    header_row = rows[0]
    
    for tc in header_row.findall(f'{{{W_NS}}}tc'):
        for p in tc.findall(f'{{{W_NS}}}p'):
            for r in p.findall(f'{{{W_NS}}}r'):
                rPr = r.find(f'{{{W_NS}}}rPr')
                if rPr is None:
                    rPr = ET.SubElement(r, f'{{{W_NS}}}rPr')
                    r.insert(0, rPr)
                
                if rPr.find(f'{{{W_NS}}}b') is None:
                    ET.SubElement(rPr, f'{{{W_NS}}}b')


def extract_caption_text(text):
    """Extract caption text from 'Table N: caption' format."""
    match = re.match(r'^Table\s*\d+:\s*(.+)$', text.strip())
    if match:
        return match.group(1)
    return text.strip()


def fix_table_captions(body):
    """Convert table captions to Word field code format."""
    children = list(body)
    replacements = []
    
    for i, child in enumerate(children):
        if child.tag == f'{{{W_NS}}}tbl':
            if i > 0:
                prev = children[i - 1]
                if prev.tag == f'{{{W_NS}}}p':
                    text = get_text_content(prev)
                    current_style = get_para_style(prev)
                    
                    # Detect caption paragraphs
                    if (current_style == 'TableCaption' or 
                        current_style == 'Caption' or
                        text.startswith('Table ') or 
                        'Workload Solutions' in text or 
                        'Applicability' in text or 
                        'Differentiators' in text):
                        caption_text = extract_caption_text(text)
                        new_caption = create_caption_paragraph(caption_text)
                        replacements.append((i - 1, prev, new_caption))
                        print(f"  Created field-based caption: {caption_text[:50]}...")
    
    # Apply replacements
    for idx, old_elem, new_elem in replacements:
        body_idx = list(body).index(old_elem)
        body.remove(old_elem)
        body.insert(body_idx, new_elem)


def create_table_of_tables_section():
    """Create Table of Tables section with page breaks before and after."""
    elements = []
    
    # Page break before Table of Tables
    elements.append(create_page_break())
    
    # Heading
    p_heading = ET.Element(f'{{{W_NS}}}p')
    
    pPr = ET.SubElement(p_heading, f'{{{W_NS}}}pPr')
    pStyle = ET.SubElement(pPr, f'{{{W_NS}}}pStyle')
    pStyle.set(f'{{{W_NS}}}val', 'TOCHeading')
    
    # Exclude from TOC by setting outline level to 9
    outlineLvl = ET.SubElement(pPr, f'{{{W_NS}}}outlineLvl')
    outlineLvl.set(f'{{{W_NS}}}val', '9')
    
    r = ET.SubElement(p_heading, f'{{{W_NS}}}r')
    rPr = ET.SubElement(r, f'{{{W_NS}}}rPr')
    ET.SubElement(rPr, f'{{{W_NS}}}b')
    sz = ET.SubElement(rPr, f'{{{W_NS}}}sz')
    sz.set(f'{{{W_NS}}}val', '28')
    
    t = ET.SubElement(r, f'{{{W_NS}}}t')
    t.text = 'Table of Tables'
    
    elements.append(p_heading)
    
    # TOC field for tables
    p_field = ET.Element(f'{{{W_NS}}}p')
    
    pPr2 = ET.SubElement(p_field, f'{{{W_NS}}}pPr')
    tabs = ET.SubElement(pPr2, f'{{{W_NS}}}tabs')
    tab = ET.SubElement(tabs, f'{{{W_NS}}}tab')
    tab.set(f'{{{W_NS}}}val', 'right')
    tab.set(f'{{{W_NS}}}leader', 'dot')
    tab.set(f'{{{W_NS}}}pos', '9360')
    
    r_begin = ET.SubElement(p_field, f'{{{W_NS}}}r')
    fldChar_begin = ET.SubElement(r_begin, f'{{{W_NS}}}fldChar')
    fldChar_begin.set(f'{{{W_NS}}}fldCharType', 'begin')
    
    r_instr = ET.SubElement(p_field, f'{{{W_NS}}}r')
    instrText = ET.SubElement(r_instr, f'{{{W_NS}}}instrText')
    instrText.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
    instrText.text = ' TOC \\h \\z \\c "Table" '
    
    r_sep = ET.SubElement(p_field, f'{{{W_NS}}}r')
    fldChar_sep = ET.SubElement(r_sep, f'{{{W_NS}}}fldChar')
    fldChar_sep.set(f'{{{W_NS}}}fldCharType', 'separate')
    
    r_text = ET.SubElement(p_field, f'{{{W_NS}}}r')
    t_text = ET.SubElement(r_text, f'{{{W_NS}}}t')
    t_text.text = 'Right-click and select "Update Field" to generate'
    
    r_end = ET.SubElement(p_field, f'{{{W_NS}}}r')
    fldChar_end = ET.SubElement(r_end, f'{{{W_NS}}}fldChar')
    fldChar_end.set(f'{{{W_NS}}}fldCharType', 'end')
    
    elements.append(p_field)
    
    # Page break after Table of Tables
    elements.append(create_page_break())
    
    return elements


def find_toc_end(body):
    """Find the index after the Table of Contents."""
    children = list(body)
    
    # Look for structured document tag (sdt) which contains TOC
    for i, child in enumerate(children):
        if child.tag == f'{{{W_NS}}}sdt':
            return i + 1
    
    return None


def remove_title_paragraph(body):
    """
    Remove the pandoc-generated Title paragraph.
    The template's title page content is preserved; we just remove pandoc's addition.
    """
    children = list(body)
    removed = False
    
    for child in children:
        if child.tag == f'{{{W_NS}}}p':
            style = get_para_style(child)
            if style == 'Title':
                body.remove(child)
                print("  Removed pandoc-generated Title paragraph (template title page preserved)")
                removed = True
                break
    
    return removed


def add_page_break_before_toc(body):
    """Add a page break before the TOC (after title page content)."""
    children = list(body)
    
    # Find the TOC (sdt element)
    for i, child in enumerate(children):
        if child.tag == f'{{{W_NS}}}sdt':
            # Insert page break before TOC
            body.insert(i, create_page_break())
            print("  Added page break before TOC")
            return True
    
    return False


def create_custom_properties_xml():
    """Create custom.xml with required properties."""
    # Create root element with namespace
    root = ET.Element(f'{{{CUSTOM_NS}}}Properties')
    root.set(f'xmlns:vt', VT_NS)
    
    properties = [
        ('Item Description', DOC_TITLE, 2),
        ('Doc Type', 'Requirements', 3),
        ('Classification', 'Confidential', 4),
    ]
    
    for name, value, pid in properties:
        prop = ET.SubElement(root, f'{{{CUSTOM_NS}}}property')
        prop.set('fmtid', '{D5CDD505-2E9C-101B-9397-08002B2CF9AE}')
        prop.set('pid', str(pid))
        prop.set('name', name)
        
        lpwstr = ET.SubElement(prop, f'{{{VT_NS}}}lpwstr')
        lpwstr.text = value
    
    return root


def update_custom_properties(temp_dir):
    """Update or create custom properties file."""
    custom_path = os.path.join(temp_dir, 'docProps', 'custom.xml')
    
    # Ensure docProps directory exists
    os.makedirs(os.path.dirname(custom_path), exist_ok=True)
    
    if os.path.exists(custom_path):
        tree = ET.parse(custom_path)
        root = tree.getroot()
        
        # Check if properties exist
        existing_props = {prop.get('name'): prop for prop in root.findall(f'.//{{{CUSTOM_NS}}}property')}
        
        if not existing_props:
            # Empty properties element - replace with our content
            root = create_custom_properties_xml()
            print(f"  Created custom properties (Item Description, Doc Type, Classification)")
        else:
            # Update existing properties
            for prop in root.findall(f'.//{{{CUSTOM_NS}}}property'):
                name = prop.get('name', '')
                lpwstr = prop.find(f'{{{VT_NS}}}lpwstr')
                
                if name == 'Item Description' and lpwstr is not None:
                    lpwstr.text = DOC_TITLE
                    print(f"  Set Item Description: {DOC_TITLE}")
                elif name == 'Doc Type' and lpwstr is not None:
                    lpwstr.text = 'Requirements'
                    print("  Set Doc Type: Requirements")
                elif name == 'Classification' and lpwstr is not None:
                    lpwstr.text = 'Confidential'
                    print("  Set Classification: Confidential")
    else:
        # Create new custom.xml
        root = create_custom_properties_xml()
        print(f"  Created custom properties (Item Description, Doc Type, Classification)")
    
    # Write the file
    tree = ET.ElementTree(root)
    tree.write(custom_path, xml_declaration=True, encoding='UTF-8')
    
    # Update [Content_Types].xml to include custom.xml if needed
    update_content_types_for_custom(temp_dir)
    
    # Update relationships to include custom.xml if needed
    update_rels_for_custom(temp_dir)


def update_content_types_for_custom(temp_dir):
    """Ensure [Content_Types].xml includes custom.xml."""
    content_types_path = os.path.join(temp_dir, '[Content_Types].xml')
    
    if not os.path.exists(content_types_path):
        return
    
    CT_NS = 'http://schemas.openxmlformats.org/package/2006/content-types'
    ET.register_namespace('', CT_NS)
    
    tree = ET.parse(content_types_path)
    root = tree.getroot()
    
    # Check if custom.xml override exists
    custom_override = None
    for override in root.findall(f'.//{{{CT_NS}}}Override'):
        if override.get('PartName') == '/docProps/custom.xml':
            custom_override = override
            break
    
    if custom_override is None:
        # Add override for custom.xml
        override = ET.SubElement(root, f'{{{CT_NS}}}Override')
        override.set('PartName', '/docProps/custom.xml')
        override.set('ContentType', 'application/vnd.openxmlformats-officedocument.custom-properties+xml')
        tree.write(content_types_path, xml_declaration=True, encoding='UTF-8')


def update_rels_for_custom(temp_dir):
    """Ensure .rels includes relationship to custom.xml."""
    rels_path = os.path.join(temp_dir, '_rels', '.rels')
    
    if not os.path.exists(rels_path):
        return
    
    RELS_NS = 'http://schemas.openxmlformats.org/package/2006/relationships'
    ET.register_namespace('', RELS_NS)
    
    tree = ET.parse(rels_path)
    root = tree.getroot()
    
    # Check if custom.xml relationship exists
    custom_rel = None
    max_id = 0
    for rel in root.findall(f'.//{{{RELS_NS}}}Relationship'):
        rel_id = rel.get('Id', '')
        if rel_id.startswith('rId'):
            try:
                num = int(rel_id[3:])
                max_id = max(max_id, num)
            except ValueError:
                pass
        
        if rel.get('Target') == 'docProps/custom.xml':
            custom_rel = rel
            break
    
    if custom_rel is None:
        # Add relationship for custom.xml
        rel = ET.SubElement(root, f'{{{RELS_NS}}}Relationship')
        rel.set('Id', f'rId{max_id + 1}')
        rel.set('Type', 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/custom-properties')
        rel.set('Target', 'docProps/custom.xml')
        tree.write(rels_path, xml_declaration=True, encoding='UTF-8')


def update_core_properties(temp_dir):
    """Update core.xml with Title property."""
    core_path = os.path.join(temp_dir, 'docProps', 'core.xml')
    
    if not os.path.exists(core_path):
        print("  Warning: core.xml not found")
        return
    
    tree = ET.parse(core_path)
    root = tree.getroot()
    
    title_elem = root.find(f'{{{DC_NS}}}title')
    if title_elem is not None:
        title_elem.text = DOC_TITLE
        print(f"  Set Title property: {DOC_TITLE}")
    else:
        # Create title element if it doesn't exist
        title_elem = ET.SubElement(root, f'{{{DC_NS}}}title')
        title_elem.text = DOC_TITLE
        print(f"  Created Title property: {DOC_TITLE}")
    
    tree.write(core_path, xml_declaration=True, encoding='UTF-8')


def find_first_heading_after_toc(body):
    """Find the index of the first Heading1 or content after TOC."""
    children = list(body)
    found_toc = False
    
    for i, child in enumerate(children):
        if child.tag == f'{{{W_NS}}}sdt':
            found_toc = True
            continue
        
        if found_toc and child.tag == f'{{{W_NS}}}p':
            style = get_para_style(child)
            text = get_text_content(child)
            if style.startswith('Heading') or style == 'Caption' or text.startswith('Table '):
                return i
    
    return None


def process_document(docx_path):
    """Main processing function."""
    temp_dir = tempfile.mkdtemp()
    
    try:
        with zipfile.ZipFile(docx_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
        
        document_path = os.path.join(temp_dir, 'word', 'document.xml')
        
        tree = ET.parse(document_path)
        root = tree.getroot()
        
        body = root.find(f'{{{W_NS}}}body')
        
        if body is None:
            print("Error: Could not find document body")
            return
        
        tables = body.findall(f'.//{{{W_NS}}}tbl')
        for tbl in tables:
            set_table_borders(tbl)
            set_header_row_bold(tbl)
            remove_cell_indent(tbl)
        
        fix_table_captions(body)
        
        remove_title_paragraph(body)
        
        add_page_break_before_toc(body)
        
        content_start_idx = find_first_heading_after_toc(body)
        
        if content_start_idx is not None:
            tot_elements = create_table_of_tables_section()
            for idx, elem in enumerate(tot_elements):
                body.insert(content_start_idx + idx, elem)
            print("  Added Table of Tables section with page breaks")
        
        tree.write(document_path, xml_declaration=True, encoding='UTF-8')
        
        update_custom_properties(temp_dir)
        update_core_properties(temp_dir)
        
        with zipfile.ZipFile(docx_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root_dir, dirs, files in os.walk(temp_dir):
                for file in files:
                    file_path = os.path.join(root_dir, file)
                    arcname = os.path.relpath(file_path, temp_dir)
                    zipf.write(file_path, arcname)
        
        print(f"Processed: {docx_path}")
        
    finally:
        shutil.rmtree(temp_dir)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <docx_file>")
        sys.exit(1)
    
    process_document(sys.argv[1])
