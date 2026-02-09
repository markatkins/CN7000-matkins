"""Tests for ksy_parser.enums module."""
import pytest
from utilities.ksy_parser.enums import extract_enums, EnumDef, EnumValue, generate_enum_table


class TestExtractEnums:
    """Tests for extract_enums function."""
    
    def test_extract_enums_from_ksy(self, cf_update_data):
        """Test extracting enums from KSY data."""
        enums = extract_enums(cf_update_data)
        
        assert len(enums) == 1
        assert enums[0].name == 'cbfc_message_type'
        assert len(enums[0].values) == 1
    
    def test_enum_value_extraction(self, cf_update_data):
        """Test that enum values are correctly extracted."""
        enums = extract_enums(cf_update_data)
        enum = enums[0]
        
        value = enum.values[0]
        assert value.value == 0x10
        assert value.id == 'cf_update'
        assert 'CF_Update' in value.doc
    
    def test_extract_enums_empty(self):
        """Test extracting enums from data with no enums."""
        enums = extract_enums({})
        assert enums == []
    
    def test_extract_enums_simple_format(self):
        """Test extracting enums in simple string format."""
        data = {
            'enums': {
                'test_enum': {
                    0: 'value_a',
                    1: 'value_b'
                }
            }
        }
        enums = extract_enums(data)
        
        assert len(enums) == 1
        assert len(enums[0].values) == 2
        assert enums[0].values[0].id == 'value_a'


class TestGenerateEnumTable:
    """Tests for generate_enum_table function."""
    
    def test_generate_table_format(self, cf_update_data):
        """Test that generated table has correct format."""
        enums = extract_enums(cf_update_data)
        table = generate_enum_table(enums[0])
        
        assert table['type'] == 'table'
        assert 'Values' in table['title']
        assert table['headers'] == ['Value', 'Name', 'Description']
        assert len(table['rows']) == 1
    
    def test_generate_table_hex_values(self, cf_update_data):
        """Test that values are formatted as hex."""
        enums = extract_enums(cf_update_data)
        table = generate_enum_table(enums[0])
        
        # First column should be hex
        assert table['rows'][0][0] == '0x10'
    
    def test_generate_table_with_prefix(self, cf_update_data):
        """Test generating table with title prefix."""
        enums = extract_enums(cf_update_data)
        table = generate_enum_table(enums[0], title_prefix="CBFC ")
        
        assert table['title'].startswith('CBFC ')
