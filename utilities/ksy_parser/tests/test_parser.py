"""Tests for ksy_parser.parser module."""
import pytest
from utilities.ksy_parser.parser import KsyParser, KsyHeader, KsyField


class TestKsyParser:
    """Tests for KsyParser class."""
    
    def test_parse_basic_fields(self, cf_update_ksy):
        """Test that basic fields are extracted."""
        parser = KsyParser()
        header = parser.parse(str(cf_update_ksy))
        
        assert header.id == 'cbfc_cf_update'
        assert header.title == 'CBFC CF_Update Control Ordered Set (CtlOS)'
        assert header.size_bytes == 8
        assert len(header.fields) == 8
    
    def test_parse_x_spec(self, cf_update_ksy):
        """Test that x-spec metadata is extracted."""
        parser = KsyParser()
        header = parser.parse(str(cf_update_ksy))
        
        assert header.x_spec is not None
        assert header.x_spec.get('table') == 'Table 5-20, Table 5-21'
        assert header.x_spec.get('section') == 'Section 5.2.6.1'
        assert header.x_spec.get('page') == 492
        assert header.x_spec.get('spec_version') == '1.0.1'
    
    def test_parse_x_packet(self, cf_update_ksy):
        """Test that x-packet metadata is extracted."""
        parser = KsyParser()
        header = parser.parse(str(cf_update_ksy))
        
        assert header.x_packet is not None
        assert header.x_packet.get('layer') == 'link'
        assert header.x_packet.get('sublayer') == 'cbfc'
        assert header.x_packet.get('size_bytes') == 8
    
    def test_parse_x_protocol(self, cf_update_ksy):
        """Test that x-protocol metadata is extracted."""
        parser = KsyParser()
        header = parser.parse(str(cf_update_ksy))
        
        assert header.x_protocol is not None
        assert 'usage_notes' in header.x_protocol
        assert 'related_messages' in header.x_protocol
    
    def test_parse_enums(self, cf_update_ksy):
        """Test that enums are extracted."""
        parser = KsyParser()
        header = parser.parse(str(cf_update_ksy))
        
        assert header.enums is not None
        assert 'cbfc_message_type' in header.enums
    
    def test_parse_instances(self, cf_update_ksy):
        """Test that instances are extracted."""
        parser = KsyParser()
        header = parser.parse(str(cf_update_ksy))
        
        assert header.instances is not None
        assert len(header.instances) == 5
        instance_names = [i.name for i in header.instances]
        assert 'cf1_vc_index' in instance_names
        assert 'cf1_count' in instance_names
    
    def test_parse_field_metadata(self, cf_update_ksy):
        """Test that field-level metadata is extracted."""
        parser = KsyParser()
        header = parser.parse(str(cf_update_ksy))
        
        # Find control_char field
        control_char = next((f for f in header.fields if f.name == 'control_char'), None)
        assert control_char is not None
        assert control_char.x_required == True
        assert control_char.x_constraint == 'value == 0x5C'
        assert control_char.x_spec_ref == 'Table 5-20, Lane 0'
    
    def test_parse_state_machine_ksy(self, vc_state_machine_ksy):
        """Test parsing a state machine KSY file."""
        parser = KsyParser()
        header = parser.parse(str(vc_state_machine_ksy))
        
        assert header.id == 'vc_state_machine'
        # x-protocol is in meta for this file
        assert header.x_protocol is not None
        assert 'state_machine' in header.x_protocol
