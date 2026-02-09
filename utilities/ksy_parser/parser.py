"""
KSY Parser - Extract field definitions from Kaitai Struct files.

Parses .ksy YAML files and extracts field definitions including:
- Field name, type, size in bits, offset
- Documentation strings
- Header metadata from x-packet section
- UE Spec references from x-spec section
- Protocol metadata from x-protocol section
- Enumeration definitions
- Instance (computed) fields
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
import yaml


TYPE_SIZES = {
    'u1': 8, 'u2': 16, 'u4': 32, 'u8': 64,
    's1': 8, 's2': 16, 's4': 32, 's8': 64,
}


@dataclass
class KsyField:
    """Represents a field in a KSY sequence."""
    name: str
    type_str: str
    size_bits: int
    offset_bits: int
    description: str
    x_required: Optional[bool] = None
    x_constraint: Optional[str] = None
    x_spec_ref: Optional[str] = None
    enum_type: Optional[str] = None


@dataclass
class KsyInstance:
    """Represents a computed/derived field in KSY instances."""
    name: str
    value: str
    description: str


@dataclass
class KsyHeader:
    """Represents a parsed KSY header/packet definition."""
    id: str
    title: str
    size_bytes: int
    fields: List[KsyField]
    doc: str
    # Extended metadata
    x_spec: Optional[Dict[str, Any]] = None
    x_packet: Optional[Dict[str, Any]] = None
    x_protocol: Optional[Dict[str, Any]] = None
    enums: Optional[Dict[str, Dict]] = None
    instances: Optional[List[KsyInstance]] = None
    raw_data: Optional[Dict[str, Any]] = None


class KsyParser:
    """Parser for Kaitai Struct (.ksy) YAML files."""
    
    def parse(self, filepath: str) -> KsyHeader:
        """Parse a KSY file and return a KsyHeader object."""
        with open(filepath) as f:
            data = yaml.safe_load(f)
        
        meta = data.get('meta', {})
        header_id = meta.get('id', '')
        title = meta.get('title', '')
        
        # Extract x-packet metadata
        x_packet = data.get('x-packet', {})
        size_bytes = x_packet.get('size_bytes', 0)
        
        # Extract x-spec metadata (can be at top level or in meta)
        x_spec = data.get('x-spec', meta.get('x-spec', None))
        
        # Extract x-protocol metadata (can be at top level or in meta)
        x_protocol = data.get('x-protocol', meta.get('x-protocol', None))
        
        # Parse fields from seq
        fields = []
        offset_bits = 0
        for field_def in data.get('seq', []):
            name = field_def.get('id', '')
            type_str = str(field_def.get('type', ''))
            size_bits = self._get_type_size(type_str, field_def)
            doc = self._extract_doc(field_def.get('doc', ''))
            
            # Extract extended field metadata
            x_required = field_def.get('x-required')
            x_constraint = field_def.get('x-constraint')
            x_spec_ref = field_def.get('x-spec-ref')
            enum_type = field_def.get('enum')
            
            fields.append(KsyField(
                name=name,
                type_str=type_str,
                size_bits=size_bits,
                offset_bits=offset_bits,
                description=doc,
                x_required=x_required,
                x_constraint=x_constraint,
                x_spec_ref=x_spec_ref,
                enum_type=enum_type
            ))
            offset_bits += size_bits
        
        if size_bytes == 0:
            size_bytes = (offset_bits + 7) // 8
        
        # Parse enums
        enums = data.get('enums', None)
        
        # Parse instances
        instances = None
        if 'instances' in data:
            instances = []
            for inst_name, inst_def in data['instances'].items():
                value = str(inst_def.get('value', ''))
                doc = self._extract_doc(inst_def.get('doc', ''))
                instances.append(KsyInstance(
                    name=inst_name,
                    value=value,
                    description=doc
                ))
        
        return KsyHeader(
            id=header_id,
            title=title,
            size_bytes=size_bytes,
            fields=fields,
            doc=data.get('doc', '') or '',
            x_spec=x_spec,
            x_packet=x_packet if x_packet else None,
            x_protocol=x_protocol,
            enums=enums,
            instances=instances,
            raw_data=data
        )
    
    def _get_type_size(self, type_str: str, field_def: dict) -> int:
        """Determine the size in bits for a field type."""
        if type_str in TYPE_SIZES:
            return TYPE_SIZES[type_str]
        if type_str.startswith('b') and type_str[1:].isdigit():
            return int(type_str[1:])
        if 'size' in field_def:
            size_val = field_def['size']
            if isinstance(size_val, int):
                return size_val * 8
            return 0
        return 0
    
    def _extract_doc(self, doc) -> str:
        """Extract the first line of documentation."""
        if not doc:
            return ''
        if not isinstance(doc, str):
            doc = str(doc)
        lines = doc.strip().split('\n')
        return lines[0].strip() if lines else ''
    
    def _extract_full_doc(self, doc) -> str:
        """Extract the full documentation string."""
        if not doc:
            return ''
        if not isinstance(doc, str):
            doc = str(doc)
        return doc.strip()
