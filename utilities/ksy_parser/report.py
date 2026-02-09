"""
KSY Report Generator - Generate technical report sections from KSY data.

Provides utilities for:
- Generating header sections with field tables
- Generating enumeration sections
- Generating state machine sections
- Generating UE Spec reference text
- Generating cross-reference sections
"""

from typing import List, Dict, Any, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from utilities.ksy_parser.parser import KsyHeader

from utilities.ksy_parser.diagram import PacketDiagram
from utilities.ksy_parser.enums import extract_enums, generate_enum_table
from utilities.ksy_parser.state_machine import extract_state_machine, generate_state_table, generate_transition_table, generate_transition_diagram


def generate_spec_reference(header: "KsyHeader") -> Optional[str]:
    """
    Generate UE Spec reference text from x-spec metadata.
    
    Args:
        header: KsyHeader object with x_spec metadata
        
    Returns:
        Formatted reference string or None if no x-spec
    """
    if not header.x_spec:
        return None
    
    x_spec = header.x_spec
    parts = []
    
    # Get spec version
    version = x_spec.get('spec_version', '1.0.1')
    parts.append(f"UE Spec v{version}")
    
    # Add table reference
    if 'table' in x_spec:
        parts.append(x_spec['table'])
    
    # Add section reference
    if 'section' in x_spec:
        parts.append(x_spec['section'])
    
    # Add page reference
    if 'page' in x_spec:
        parts.append(f"Page {x_spec['page']}")
    
    return ", ".join(parts)


def generate_enum_section(header: "KsyHeader") -> List[Dict[str, Any]]:
    """
    Generate enumeration table sections from KSY header.
    
    Args:
        header: KsyHeader object with enums
        
    Returns:
        List of YAML table dicts for enumerations
    """
    if not header.enums or not header.raw_data:
        return []
    
    sections = []
    enums = extract_enums(header.raw_data)
    
    for enum_def in enums:
        table = generate_enum_table(enum_def)
        sections.append(table)
    
    return sections


def generate_state_machine_section(header: "KsyHeader") -> List[Dict[str, Any]]:
    """
    Generate state machine sections from KSY header.
    
    Args:
        header: KsyHeader object with x_protocol metadata
        
    Returns:
        List of YAML section dicts (state table, transition table, diagram)
    """
    if not header.x_protocol:
        return []
    
    sm = extract_state_machine(header.x_protocol)
    if not sm:
        return []
    
    sections = []
    
    # Use header title for naming
    title = header.title or header.id
    
    # Add state table
    state_table = generate_state_table(sm)
    state_table['title'] = f"{title} States"
    sections.append(state_table)
    
    # Add transition table if there are transitions
    if sm.transitions:
        trans_table = generate_transition_table(sm)
        trans_table['title'] = f"{title} Transitions"
        sections.append(trans_table)
    
    # Add ASCII diagram
    diagram = generate_transition_diagram(sm)
    if diagram:
        sections.append({
            'type': 'code_block',
            'title': f"{title} State Diagram",
            'language': '',
            'code': diagram
        })
    
    return sections


def generate_cross_references(header: "KsyHeader") -> List[Dict[str, Any]]:
    """
    Generate cross-reference sections from x-protocol metadata.
    
    Args:
        header: KsyHeader object with x_protocol metadata
        
    Returns:
        List of YAML section dicts for cross-references
    """
    if not header.x_protocol:
        return []
    
    related = header.x_protocol.get('related_messages', [])
    if not related:
        return []
    
    rows = []
    for msg in related:
        name = msg.get('name', '')
        desc = msg.get('description', '')
        ref = msg.get('reference', '')
        rows.append([name, desc, ref])
    
    return [{
        'type': 'table',
        'title': 'Related Formats',
        'headers': ['Format', 'Description', 'Reference'],
        'rows': rows
    }]


def generate_usage_notes(header: "KsyHeader") -> List[Dict[str, Any]]:
    """
    Generate usage notes section from x-protocol metadata.
    
    Args:
        header: KsyHeader object with x_protocol metadata
        
    Returns:
        List of YAML section dicts for usage notes
    """
    if not header.x_protocol:
        return []
    
    notes = header.x_protocol.get('usage_notes', [])
    if not notes:
        return []
    
    return [{
        'type': 'item_list',
        'title': 'Usage Notes',
        'items': notes,
        'item_type': 'closed'
    }]


def generate_constraints_section(header: "KsyHeader") -> List[Dict[str, Any]]:
    """
    Generate constraints section from x-packet metadata.
    
    Args:
        header: KsyHeader object with x_packet metadata
        
    Returns:
        List of YAML section dicts for constraints
    """
    if not header.x_packet:
        return []
    
    constraints = header.x_packet.get('constraints', [])
    if not constraints:
        return []
    
    return [{
        'type': 'item_list',
        'title': 'Validation Constraints',
        'items': constraints,
        'item_type': 'closed'
    }]


def generate_header_section(header: "KsyHeader") -> List[Dict[str, Any]]:
    """
    Generate complete header section with all available content.
    
    This is the main entry point for generating report sections from a KSY header.
    It includes:
    - Section header with title and size
    - UE Spec reference (if available)
    - Wire format diagram
    - Field definition table with constraints
    - Enumeration tables (if available)
    - State machine sections (if available)
    - Cross-references (if available)
    - Usage notes (if available)
    - Validation constraints (if available)
    
    Args:
        header: KsyHeader object
        
    Returns:
        List of YAML section dicts
    """
    sections = []
    
    # Section header
    sections.append({
        'type': 'section_header',
        'title': f"{header.title or header.id}",
        'subtitle': f"{header.size_bytes} bytes ({header.size_bytes * 8} bits)"
    })
    
    # UE Spec reference
    spec_ref = generate_spec_reference(header)
    if spec_ref:
        sections.append({
            'type': 'text',
            'content': f"Reference: {spec_ref}"
        })
    
    # Wire format diagram
    diagram = PacketDiagram(header)
    sections.append({
        'type': 'code_block',
        'title': f"{header.id} Packet Layout",
        'language': '',
        'code': diagram.render()
    })
    
    # Field definition table with enhanced columns
    rows = []
    for field in header.fields:
        constraint = field.x_constraint or ''
        rows.append([
            field.name,
            str(field.size_bits),
            str(field.offset_bits),
            field.type_str,
            field.description[:50] if field.description else '',
            constraint[:30] if constraint else ''
        ])
    
    sections.append({
        'type': 'table',
        'title': f"{header.id} Field Definitions",
        'headers': ['Field', 'Bits', 'Offset', 'Type', 'Description', 'Constraints'],
        'rows': rows
    })
    
    # Enumeration tables
    enum_sections = generate_enum_section(header)
    sections.extend(enum_sections)
    
    # State machine sections
    sm_sections = generate_state_machine_section(header)
    sections.extend(sm_sections)
    
    # Cross-references
    xref_sections = generate_cross_references(header)
    sections.extend(xref_sections)
    
    # Usage notes
    notes_sections = generate_usage_notes(header)
    sections.extend(notes_sections)
    
    # Validation constraints
    constraint_sections = generate_constraints_section(header)
    sections.extend(constraint_sections)
    
    return sections
