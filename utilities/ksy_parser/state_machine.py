"""
KSY State Machine - Extract and format state machine definitions from Kaitai Struct files.

Provides utilities for:
- Extracting state machine definitions from x-protocol metadata
- Generating YAML table format for states
- Generating ASCII transition diagrams
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional


@dataclass
class State:
    """Represents a state in a state machine."""
    name: str
    description: str
    is_terminal: bool = False


@dataclass
class Transition:
    """Represents a transition between states."""
    from_state: str
    to_state: str
    trigger: str
    condition: Optional[str] = None
    action: Optional[str] = None
    spec_ref: Optional[str] = None


@dataclass
class StateMachine:
    """Represents a complete state machine definition."""
    name: str
    initial_state: str
    states: List[State]
    transitions: List[Transition]
    description: Optional[str] = None


def extract_state_machine(x_protocol: dict) -> Optional[StateMachine]:
    """
    Extract state machine definition from x-protocol metadata.
    
    Args:
        x_protocol: The x-protocol section from KSY data
        
    Returns:
        StateMachine object or None if no state machine defined
    """
    if not x_protocol:
        return None
    
    sm_data = x_protocol.get('state_machine')
    if not sm_data:
        return None
    
    # Extract states
    states = []
    for state_def in sm_data.get('states', []):
        states.append(State(
            name=state_def.get('name', ''),
            description=state_def.get('description', ''),
            is_terminal=state_def.get('is_terminal', False)
        ))
    
    # Extract transitions
    transitions = []
    for trans_def in sm_data.get('transitions', []):
        transitions.append(Transition(
            from_state=trans_def.get('from', ''),
            to_state=trans_def.get('to', ''),
            trigger=trans_def.get('trigger', ''),
            condition=trans_def.get('condition'),
            action=trans_def.get('action'),
            spec_ref=trans_def.get('spec_ref')
        ))
    
    # Get name from protocol description or generate from context
    name = x_protocol.get('description', 'State Machine')
    
    return StateMachine(
        name=name,
        initial_state=sm_data.get('initial_state', ''),
        states=states,
        transitions=transitions,
        description=x_protocol.get('description')
    )


def generate_state_table(sm: StateMachine) -> Dict[str, Any]:
    """
    Generate a YAML table structure for state machine states.
    
    Args:
        sm: StateMachine object
        
    Returns:
        Dict in YAML table format
    """
    rows = []
    for state in sm.states:
        terminal_marker = " (terminal)" if state.is_terminal else ""
        rows.append([state.name, state.description + terminal_marker])
    
    return {
        'type': 'table',
        'title': f"{sm.name} States",
        'headers': ['State', 'Description'],
        'rows': rows
    }


def generate_transition_table(sm: StateMachine) -> Dict[str, Any]:
    """
    Generate a YAML table structure for state machine transitions.
    
    Args:
        sm: StateMachine object
        
    Returns:
        Dict in YAML table format
    """
    rows = []
    for trans in sm.transitions:
        condition = trans.condition or "-"
        action = trans.action or "-"
        rows.append([trans.from_state, trans.to_state, trans.trigger, condition, action])
    
    return {
        'type': 'table',
        'title': f"{sm.name} Transitions",
        'headers': ['From', 'To', 'Trigger', 'Condition', 'Action'],
        'rows': rows
    }


def generate_transition_diagram(sm: StateMachine) -> str:
    """
    Generate an ASCII art transition diagram for a state machine.
    
    Args:
        sm: StateMachine object
        
    Returns:
        ASCII art string representing the state machine
    """
    if not sm.states:
        return ""
    
    lines = []
    lines.append(f"State Machine: {sm.name}")
    lines.append(f"Initial State: {sm.initial_state}")
    lines.append("")
    
    # Simple text-based representation
    for trans in sm.transitions:
        arrow = f"  {trans.from_state} --[{trans.trigger}]--> {trans.to_state}"
        lines.append(arrow)
    
    return "\n".join(lines)


def generate_state_machine_section(x_protocol: dict, title: str = "") -> List[Dict[str, Any]]:
    """
    Generate all state machine sections from x-protocol metadata.
    
    Args:
        x_protocol: The x-protocol section from KSY data
        title: Optional title override
        
    Returns:
        List of YAML section dicts (state table, transition table, diagram)
    """
    sm = extract_state_machine(x_protocol)
    if not sm:
        return []
    
    sections = []
    
    # Add state table
    state_table = generate_state_table(sm)
    if title:
        state_table['title'] = f"{title} States"
    sections.append(state_table)
    
    # Add transition table
    trans_table = generate_transition_table(sm)
    if title:
        trans_table['title'] = f"{title} Transitions"
    sections.append(trans_table)
    
    # Add ASCII diagram
    diagram = generate_transition_diagram(sm)
    if diagram:
        sections.append({
            'type': 'code_block',
            'title': f"{title or sm.name} Diagram",
            'language': '',
            'code': diagram
        })
    
    return sections
