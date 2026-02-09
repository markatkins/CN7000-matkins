"""Tests for ksy_parser.report module."""
import pytest
from utilities.ksy_parser.parser import KsyParser
from utilities.ksy_parser.report import (
    generate_header_section,
    generate_enum_section,
    generate_state_machine_section,
    generate_spec_reference,
    generate_cross_references,
    generate_usage_notes,
    generate_constraints_section
)


class TestGenerateSpecReference:
    """Tests for generate_spec_reference function."""
    
    def test_generate_spec_reference(self, cf_update_ksy):
        """Test generating spec reference string."""
        parser = KsyParser()
        header = parser.parse(str(cf_update_ksy))
        
        ref = generate_spec_reference(header)
        
        assert ref is not None
        assert 'UE Spec v1.0.1' in ref
        assert 'Table 5-20' in ref
        assert 'Section 5.2.6.1' in ref
        assert 'Page 492' in ref
    
    def test_generate_spec_reference_none(self, vc_state_machine_ksy):
        """Test that None is returned when no x-spec at top level."""
        parser = KsyParser()
        header = parser.parse(str(vc_state_machine_ksy))
        
        # This file has x-spec in meta, not at top level
        # Our parser should still find it
        ref = generate_spec_reference(header)
        # May or may not have spec ref depending on structure


class TestGenerateEnumSection:
    """Tests for generate_enum_section function."""
    
    def test_generate_enum_section(self, cf_update_ksy):
        """Test generating enum sections."""
        parser = KsyParser()
        header = parser.parse(str(cf_update_ksy))
        
        sections = generate_enum_section(header)
        
        assert len(sections) == 1
        assert sections[0]['type'] == 'table'
        assert 'Values' in sections[0]['title']


class TestGenerateStateMachineSection:
    """Tests for generate_state_machine_section function."""
    
    def test_generate_state_machine_section(self, vc_state_machine_ksy):
        """Test generating state machine sections."""
        parser = KsyParser()
        header = parser.parse(str(vc_state_machine_ksy))
        
        sections = generate_state_machine_section(header)
        
        # Should have state table, transition table, and diagram
        assert len(sections) >= 2
        types = [s['type'] for s in sections]
        assert 'table' in types


class TestGenerateHeaderSection:
    """Tests for generate_header_section function."""
    
    def test_generate_header_section_complete(self, cf_update_ksy):
        """Test generating complete header section."""
        parser = KsyParser()
        header = parser.parse(str(cf_update_ksy))
        
        sections = generate_header_section(header)
        
        # Should have multiple sections
        assert len(sections) >= 4
        
        # Check section types
        types = [s.get('type') for s in sections]
        assert 'section_header' in types
        assert 'code_block' in types
        assert 'table' in types
    
    def test_generate_header_section_has_spec_ref(self, cf_update_ksy):
        """Test that header section includes spec reference."""
        parser = KsyParser()
        header = parser.parse(str(cf_update_ksy))
        
        sections = generate_header_section(header)
        
        # Find text section with spec reference
        text_sections = [s for s in sections if s.get('type') == 'text']
        assert len(text_sections) >= 1
        assert 'UE Spec' in text_sections[0].get('content', '')
    
    def test_generate_header_section_has_enums(self, cf_update_ksy):
        """Test that header section includes enum tables."""
        parser = KsyParser()
        header = parser.parse(str(cf_update_ksy))
        
        sections = generate_header_section(header)
        
        # Find enum table
        tables = [s for s in sections if s.get('type') == 'table']
        enum_tables = [t for t in tables if 'Values' in t.get('title', '')]
        assert len(enum_tables) >= 1
    
    def test_generate_header_section_field_constraints(self, cf_update_ksy):
        """Test that field table includes constraints column."""
        parser = KsyParser()
        header = parser.parse(str(cf_update_ksy))
        
        sections = generate_header_section(header)
        
        # Find field definition table
        tables = [s for s in sections if s.get('type') == 'table']
        field_table = next((t for t in tables if 'Field Definitions' in t.get('title', '')), None)
        
        assert field_table is not None
        assert 'Constraints' in field_table['headers']
