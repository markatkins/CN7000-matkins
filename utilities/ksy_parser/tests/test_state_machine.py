"""Tests for ksy_parser.state_machine module."""
import pytest
from utilities.ksy_parser.state_machine import (
    extract_state_machine, 
    StateMachine, 
    State, 
    Transition,
    generate_state_table,
    generate_transition_table,
    generate_transition_diagram
)


class TestExtractStateMachine:
    """Tests for extract_state_machine function."""
    
    def test_extract_state_machine(self, vc_state_machine_data):
        """Test extracting state machine from x-protocol."""
        x_protocol = vc_state_machine_data.get('meta', {}).get('x-protocol')
        sm = extract_state_machine(x_protocol)
        
        assert sm is not None
        assert sm.initial_state == 'DISABLED'
        assert len(sm.states) == 4
    
    def test_extract_states(self, vc_state_machine_data):
        """Test that states are correctly extracted."""
        x_protocol = vc_state_machine_data.get('meta', {}).get('x-protocol')
        sm = extract_state_machine(x_protocol)
        
        state_names = [s.name for s in sm.states]
        assert 'DISABLED' in state_names
        assert 'INITIALIZING' in state_names
        assert 'ACTIVE' in state_names
        assert 'REMOVING' in state_names
    
    def test_extract_transitions(self, vc_state_machine_data):
        """Test that transitions are correctly extracted."""
        x_protocol = vc_state_machine_data.get('meta', {}).get('x-protocol')
        sm = extract_state_machine(x_protocol)
        
        assert len(sm.transitions) >= 1
        trans = sm.transitions[0]
        assert trans.from_state == 'DISABLED'
        assert trans.to_state == 'INITIALIZING'
        assert trans.trigger == 'start'
    
    def test_extract_none_when_no_state_machine(self):
        """Test that None is returned when no state machine."""
        sm = extract_state_machine({})
        assert sm is None
        
        sm = extract_state_machine(None)
        assert sm is None


class TestGenerateStateTables:
    """Tests for state table generation functions."""
    
    def test_generate_state_table(self, vc_state_machine_data):
        """Test generating state table."""
        x_protocol = vc_state_machine_data.get('meta', {}).get('x-protocol')
        sm = extract_state_machine(x_protocol)
        table = generate_state_table(sm)
        
        assert table['type'] == 'table'
        assert 'States' in table['title']
        assert table['headers'] == ['State', 'Description']
        assert len(table['rows']) == 4
    
    def test_generate_transition_table(self, vc_state_machine_data):
        """Test generating transition table."""
        x_protocol = vc_state_machine_data.get('meta', {}).get('x-protocol')
        sm = extract_state_machine(x_protocol)
        table = generate_transition_table(sm)
        
        assert table['type'] == 'table'
        assert 'Transitions' in table['title']
        assert 'From' in table['headers']
        assert 'To' in table['headers']
        assert 'Trigger' in table['headers']
    
    def test_generate_transition_diagram(self, vc_state_machine_data):
        """Test generating ASCII transition diagram."""
        x_protocol = vc_state_machine_data.get('meta', {}).get('x-protocol')
        sm = extract_state_machine(x_protocol)
        diagram = generate_transition_diagram(sm)
        
        assert 'DISABLED' in diagram
        assert 'INITIALIZING' in diagram
        assert '--[' in diagram  # Arrow format
