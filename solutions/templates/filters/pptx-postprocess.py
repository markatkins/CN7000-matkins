#!/usr/bin/env python3
"""
Post-processor for pandoc-generated PPTX files.

This script remaps slide layout references from pandoc's default layout choices
to our preferred template layouts:

Pandoc uses:             We want:
"Title Slide"         -> "Title"
"Two Content"         -> "Title and Content - 2 Column"
"Comparison"          -> "Title and Content - 2 Column"
"Title and Content"   -> "title and 1 content"

IMPORTANT: We only rename layouts that pandoc created (fallback layouts),
not layouts that already exist in the template with the target name.
"""

import sys
import zipfile
import tempfile
import shutil
import os
import re
from xml.etree import ElementTree as ET

# XML namespaces for PPTX
PPTX_NS = {
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
}

RELS_NS = 'http://schemas.openxmlformats.org/package/2006/relationships'

for prefix, uri in PPTX_NS.items():
    ET.register_namespace(prefix, uri)
ET.register_namespace('', RELS_NS)

# Layout name mapping: current layout name -> desired layout name
LAYOUT_MAP = {
    'Title Slide': 'Title',
    'Two Content': 'Title and Content - 2 Column',
    'Comparison': 'Title and Content - 2 Column',
    'Title and Content': 'title and 1 content',
}


def get_layout_info(temp_dir):
    """Build maps of layout names to files and vice versa."""
    name_to_file = {}
    file_to_name = {}
    layouts_dir = os.path.join(temp_dir, 'ppt', 'slideLayouts')
    
    if not os.path.exists(layouts_dir):
        return name_to_file, file_to_name
    
    for filename in os.listdir(layouts_dir):
        if filename.endswith('.xml') and not filename.startswith('_'):
            filepath = os.path.join(layouts_dir, filename)
            try:
                tree = ET.parse(filepath)
                root = tree.getroot()
                
                cSld = root.find('.//{http://schemas.openxmlformats.org/presentationml/2006/main}cSld')
                if cSld is not None:
                    name = cSld.get('name', '')
                    if name:
                        name_to_file[name] = filename
                        file_to_name[filename] = name
            except ET.ParseError:
                continue
    
    return name_to_file, file_to_name


def get_slides_using_layout(temp_dir, layout_filename):
    """Find which slides use a specific layout."""
    slides_using = []
    slides_rels_dir = os.path.join(temp_dir, 'ppt', 'slides', '_rels')
    
    if not os.path.exists(slides_rels_dir):
        return slides_using
    
    for rels_file in os.listdir(slides_rels_dir):
        if not rels_file.endswith('.xml.rels'):
            continue
        
        rels_path = os.path.join(slides_rels_dir, rels_file)
        tree = ET.parse(rels_path)
        root = tree.getroot()
        
        for rel in root.findall(f'.//{{{RELS_NS}}}Relationship'):
            rel_type = rel.get('Type', '')
            if 'slideLayout' in rel_type:
                target = rel.get('Target', '')
                if os.path.basename(target) == layout_filename:
                    slides_using.append(rels_file.replace('.xml.rels', ''))
    
    return slides_using


def remap_slides_to_layout(temp_dir, slides, old_layout_file, new_layout_file):
    """Update slide relationships to point to a different layout."""
    slides_rels_dir = os.path.join(temp_dir, 'ppt', 'slides', '_rels')
    
    for slide in slides:
        rels_path = os.path.join(slides_rels_dir, f'{slide}.xml.rels')
        if not os.path.exists(rels_path):
            continue
        
        tree = ET.parse(rels_path)
        root = tree.getroot()
        
        modified = False
        for rel in root.findall(f'.//{{{RELS_NS}}}Relationship'):
            rel_type = rel.get('Type', '')
            if 'slideLayout' in rel_type:
                target = rel.get('Target', '')
                if os.path.basename(target) == old_layout_file:
                    new_target = target.replace(old_layout_file, new_layout_file)
                    rel.set('Target', new_target)
                    modified = True
        
        if modified:
            tree.write(rels_path, xml_declaration=True, encoding='UTF-8')


def delete_layout(temp_dir, layout_filename):
    """Delete a layout file and its relationships."""
    layout_path = os.path.join(temp_dir, 'ppt', 'slideLayouts', layout_filename)
    rels_path = os.path.join(temp_dir, 'ppt', 'slideLayouts', '_rels', f'{layout_filename}.rels')
    
    if os.path.exists(layout_path):
        os.remove(layout_path)
    if os.path.exists(rels_path):
        os.remove(rels_path)


def process_pptx(pptx_path):
    """Main processing function."""
    temp_dir = tempfile.mkdtemp()
    
    try:
        # Extract PPTX
        with zipfile.ZipFile(pptx_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
        
        # Build layout maps
        name_to_file, file_to_name = get_layout_info(temp_dir)
        print(f"Found {len(name_to_file)} layouts in PPTX")
        
        # Process each mapping
        print("\nProcessing layout mappings:")
        for source_name, target_name in LAYOUT_MAP.items():
            if source_name not in name_to_file:
                print(f"  '{source_name}': not found in PPTX, skipping")
                continue
            
            source_file = name_to_file[source_name]
            
            if target_name in name_to_file:
                # Target layout already exists - remap slides and delete source
                target_file = name_to_file[target_name]
                slides = get_slides_using_layout(temp_dir, source_file)
                
                if slides:
                    print(f"  '{source_name}' -> '{target_name}': remapping {len(slides)} slides to existing layout")
                    remap_slides_to_layout(temp_dir, slides, source_file, target_file)
                
                # Delete the pandoc fallback layout
                print(f"    Deleting unused fallback layout: {source_file}")
                delete_layout(temp_dir, source_file)
            else:
                # Target doesn't exist - just rename the source
                print(f"  '{source_name}' -> '{target_name}': renaming layout")
                layout_path = os.path.join(temp_dir, 'ppt', 'slideLayouts', source_file)
                tree = ET.parse(layout_path)
                root = tree.getroot()
                cSld = root.find('.//{http://schemas.openxmlformats.org/presentationml/2006/main}cSld')
                if cSld is not None:
                    cSld.set('name', target_name)
                    tree.write(layout_path, xml_declaration=True, encoding='UTF-8')
        
        # Update Content_Types.xml to remove deleted layouts
        update_content_types(temp_dir, name_to_file)
        
        # Update slideMaster relationships
        update_slide_master_rels(temp_dir, name_to_file)
        
        # Repack PPTX
        with zipfile.ZipFile(pptx_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root_dir, dirs, files in os.walk(temp_dir):
                for file in files:
                    file_path = os.path.join(root_dir, file)
                    arcname = os.path.relpath(file_path, temp_dir)
                    zipf.write(file_path, arcname)
        
        print(f"\nProcessed: {pptx_path}")
        
    finally:
        shutil.rmtree(temp_dir)


def update_content_types(temp_dir, original_name_to_file):
    """Remove deleted layouts from [Content_Types].xml."""
    ct_path = os.path.join(temp_dir, '[Content_Types].xml')
    if not os.path.exists(ct_path):
        return
    
    CT_NS = 'http://schemas.openxmlformats.org/package/2006/content-types'
    ET.register_namespace('', CT_NS)
    
    tree = ET.parse(ct_path)
    root = tree.getroot()
    
    # Find layouts that no longer exist
    layouts_dir = os.path.join(temp_dir, 'ppt', 'slideLayouts')
    existing_layouts = set(f for f in os.listdir(layouts_dir) if f.endswith('.xml') and not f.startswith('_'))
    
    # Remove overrides for deleted layouts
    to_remove = []
    for override in root.findall(f'.//{{{CT_NS}}}Override'):
        part_name = override.get('PartName', '')
        if '/slideLayouts/' in part_name:
            layout_file = os.path.basename(part_name)
            if layout_file not in existing_layouts:
                to_remove.append(override)
    
    for elem in to_remove:
        root.remove(elem)
    
    if to_remove:
        tree.write(ct_path, xml_declaration=True, encoding='UTF-8')
        print(f"  Removed {len(to_remove)} entries from [Content_Types].xml")


def update_slide_master_rels(temp_dir, original_name_to_file):
    """Remove deleted layouts from slideMaster relationships."""
    rels_path = os.path.join(temp_dir, 'ppt', 'slideMasters', '_rels', 'slideMaster1.xml.rels')
    if not os.path.exists(rels_path):
        return
    
    ET.register_namespace('', RELS_NS)
    
    tree = ET.parse(rels_path)
    root = tree.getroot()
    
    # Find layouts that no longer exist
    layouts_dir = os.path.join(temp_dir, 'ppt', 'slideLayouts')
    existing_layouts = set(f for f in os.listdir(layouts_dir) if f.endswith('.xml') and not f.startswith('_'))
    
    # Remove relationships for deleted layouts
    to_remove = []
    for rel in root.findall(f'.//{{{RELS_NS}}}Relationship'):
        target = rel.get('Target', '')
        if 'slideLayout' in target:
            layout_file = os.path.basename(target)
            if layout_file not in existing_layouts:
                to_remove.append(rel)
    
    for elem in to_remove:
        root.remove(elem)
    
    if to_remove:
        tree.write(rels_path, xml_declaration=True, encoding='UTF-8')
        print(f"  Removed {len(to_remove)} entries from slideMaster1.xml.rels")


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <pptx_file>")
        sys.exit(1)
    
    process_pptx(sys.argv[1])
