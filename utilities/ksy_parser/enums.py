"""
KSY Enums - Extract and format enumeration definitions from Kaitai Struct files.

Provides utilities for:
- Extracting enum definitions from KSY data
- Generating YAML table format for enumerations
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional


@dataclass
class EnumValue:
    """Represents a single value in an enumeration."""
    value: int
    id: str
    doc: str


@dataclass
class EnumDef:
    """Represents an enumeration definition."""
    name: str
    values: List[EnumValue]


def extract_enums(ksy_data: dict) -> List[EnumDef]:
    """
    Extract enumeration definitions from KSY data.
    
    Args:
        ksy_data: Parsed KSY YAML data (dict)
        
    Returns:
        List of EnumDef objects
    """
    enums = []
    enums_section = ksy_data.get('enums', {})
    
    if not enums_section:
        return enums
    
    for enum_name, enum_values in enums_section.items():
        values = []
        for value, value_def in enum_values.items():
            # Handle both simple (string) and complex (dict) enum value definitions
            if isinstance(value_def, str):
                values.append(EnumValue(
                    value=int(value),
                    id=value_def,
                    doc=''
                ))
            elif isinstance(value_def, dict):
                values.append(EnumValue(
                    value=int(value),
                    id=value_def.get('id', str(value)),
                    doc=value_def.get('doc', '')
                ))
            else:
                values.append(EnumValue(
                    value=int(value),
                    id=str(value_def),
                    doc=''
                ))
        
        # Sort by value
        values.sort(key=lambda v: v.value)
        
        enums.append(EnumDef(
            name=enum_name,
            values=values
        ))
    
    return enums


def generate_enum_table(enum_def: EnumDef, title_prefix: str = "") -> Dict[str, Any]:
    """
    Generate a YAML table structure for an enumeration.
    
    Args:
        enum_def: EnumDef object to convert
        title_prefix: Optional prefix for the table title
        
    Returns:
        Dict in YAML table format for technical reports
    """
    # Format title: convert snake_case to Title Case
    formatted_name = enum_def.name.replace('_', ' ').title()
    title = f"{title_prefix}{formatted_name} Values" if title_prefix else f"{formatted_name} Values"
    
    rows = []
    for value in enum_def.values:
        # Format value as hex
        hex_value = f"0x{value.value:02X}"
        rows.append([hex_value, value.id, value.doc])
    
    return {
        'type': 'table',
        'title': title,
        'headers': ['Value', 'Name', 'Description'],
        'rows': rows
    }


def generate_enum_sections(ksy_data: dict, title_prefix: str = "") -> List[Dict[str, Any]]:
    """
    Generate all enumeration table sections from KSY data.
    
    Args:
        ksy_data: Parsed KSY YAML data
        title_prefix: Optional prefix for table titles
        
    Returns:
        List of YAML table dicts
    """
    enums = extract_enums(ksy_data)
    return [generate_enum_table(e, title_prefix) for e in enums]
