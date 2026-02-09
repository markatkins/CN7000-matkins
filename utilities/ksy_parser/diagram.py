"""ASCII packet diagram generator for RFC 2360-style bit diagrams."""

from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from utilities.ksy_parser.parser import KsyHeader, KsyField


class PacketDiagram:
    def __init__(self, header: "KsyHeader", width: int = 32):
        self.header = header
        self.width = width
    
    def render(self) -> str:
        lines = []
        lines.append(self._render_byte_ruler())
        lines.append(self._render_bit_ruler())
        lines.append(self._render_separator())
        
        current_bit = 0
        row_fields: List[tuple] = []
        
        for field in self.header.fields:
            remaining = field.size_bits
            field_start = current_bit % self.width
            
            while remaining > 0:
                row_pos = current_bit % self.width
                bits_left_in_row = self.width - row_pos
                bits_to_use = min(remaining, bits_left_in_row)
                
                row_fields.append((field.name, row_pos, bits_to_use))
                current_bit += bits_to_use
                remaining -= bits_to_use
                
                if current_bit % self.width == 0:
                    lines.append(self._render_field_row(row_fields))
                    lines.append(self._render_separator())
                    row_fields = []
        
        if row_fields:
            lines.append(self._render_field_row(row_fields))
            lines.append(self._render_separator())
        
        return '\n'.join(lines)
    
    def _render_byte_ruler(self) -> str:
        return " 0                   1                   2                   3"
    
    def _render_bit_ruler(self) -> str:
        return " " + " ".join(str(i % 10) for i in range(32))
    
    def _render_separator(self) -> str:
        return "+-" + "-+-" * 31 + "-+"
    
    def _render_field_row(self, fields_in_row: List[tuple]) -> str:
        row = [' '] * (self.width * 2)
        
        for name, start_bit, width_bits in fields_in_row:
            start_char = start_bit * 2
            end_char = start_char + width_bits * 2
            
            row[start_char] = '|'
            
            available_chars = width_bits * 2 - 1
            display_name = name[:available_chars] if len(name) > available_chars else name
            
            padding = available_chars - len(display_name)
            left_pad = padding // 2
            
            for i, char in enumerate(display_name):
                pos = start_char + 1 + left_pad + i
                if pos < end_char:
                    row[pos] = char
        
        row[-1] = '|'
        return ''.join(row)
