# Virtual Channel State Machine
# Feature: 003-ue-packet-taxonomy
# UE Specification: v1.0.1, Section 5.2.6, Figure 5-10, Page 490
#
# Virtual channel lifecycle state machine

meta:
  id: vc_state_machine
  title: Virtual Channel State Machine
  
  x-spec:
    section: "Section 5.2.6"
    figure: "Figure 5-10"
    page: 490
    description: "Virtual channel lifecycle state machine"
  
  x-protocol:
    protocol_type: "state_machine"
    layer: "link"
    sublayer: "cbfc"
    
    state_machine:
      initial_state: DISABLED
      
      states:
        - name: DISABLED
          description: "DISABLED state"
          is_terminal: false
        - name: INITIALIZING
          description: "INITIALIZING state"
          is_terminal: false
        - name: ACTIVE
          description: "ACTIVE state"
          is_terminal: false
        - name: REMOVING
          description: "REMOVING state"
          is_terminal: true
      
      transitions:
        - from: DISABLED
          to: INITIALIZING
          trigger: "start"
          condition: "true"
          action: "Begin processing"
          spec_ref: "Section 5.2.6"

doc: |
  Virtual Channel State Machine
  
  Virtual channel lifecycle state machine
  
  Reference: UE Specification v1.0.1, Section 5.2.6, Figure 5-10, Page 490
