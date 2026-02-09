# State Machine Analysis - EarlySim Datamodel

**Date**: 2026-01-22  
**Scope**: `datamodel/` directory  
**Author**: AI Analysis

## Executive Summary

The EarlySim datamodel contains **7 state machine definitions** across multiple protocol domains and hardware components. The state machines vary significantly in quality and completeness, ranging from exemplary (QP State Machine, CCC State Machine) to skeletal (VC State Machine).

| State Machine | Domain | States | Transitions | Quality | Completeness |
|---------------|--------|--------|-------------|---------|--------------|
| QP State Machine | RoCE/RDMA | 7 | 17 | Exemplary | Complete |
| CCC State Machine | UE Transport/CMS | 4 | 8 | Exemplary | Complete |
| VC State Machine | UE Link/CBFC | 4 | 1 | Skeletal | Incomplete |
| UALink Link State | UALink Datalink | 5 | 6 | Good | Complete |
| Ethernet Queue State Machine | Ethernet HSI | 4 | 9 | Good | Complete |
| BME FSM | EC Hardware | 7 | 10 | Diagram Only | N/A |

---

## 1. RoCE/InfiniBand Queue Pair (QP) State Machine

**Location**: `datamodel/protocols/roce/protocols/qp_state_machine.ksy`  
**Feature**: 003-ue-packet-taxonomy  
**Spec Reference**: IB Architecture Specification Volume 1, Section 10.3; RoCEv2 Annex A17

### States (7)

| State | Description | Terminal |
|-------|-------------|----------|
| RESET | Initial state after QP creation. No resources allocated. | No |
| INIT | QP initialized with basic parameters. Can receive but not send. | No |
| RTR | Ready To Receive. Remote QP information configured. | No |
| RTS | Ready To Send. Fully operational for data transfer. | No |
| SQD | Send Queue Drained. Outstanding send WQEs completing. | No |
| SQE | Send Queue Error. Recoverable send error. | No |
| ERROR | Unrecoverable error. Must reset or destroy QP. | Yes |

### Transitions (17)

All transitions are fully documented with:
- Trigger (e.g., `ibv_modify_qp(IBV_QPS_INIT)`)
- Condition (e.g., "Valid QP attributes provided")
- Action (e.g., "Configure port, pkey_index, qkey")
- Spec reference (e.g., "IB Spec Section 10.3.1")

### Quality Assessment: **EXEMPLARY**

**Strengths**:
- Complete coverage of all 7 IB Spec states
- All 17 transitions documented with triggers, conditions, actions
- Full traceability to IB Architecture Specification
- QP type variations documented (RC, UC, UD)
- Error conditions enumerated with recovery paths
- ASCII state diagram included in documentation

**Deficiencies**: None identified.

---

## 2. CCC (Congestion Control Context) State Machine

**Location**: `datamodel/protocols/ue/transport/cms/protocols/ccc_state_machine.ksy`  
**Feature**: 003-ue-packet-taxonomy  
**Spec Reference**: UE Specification v1.0.1, Section 3.6.6, Figure 3-98, Page 362

### States (4)

| State | Description | Terminal |
|-------|-------------|----------|
| IDLE | No pending data. All data ACKed. CCC can be removed. | No |
| ACTIVE | Data to send but CC does not permit (window/credit exhausted). | No |
| READY | Data to send and CC permits. Scheduler can select PDCs. | No |
| PENDING | All data sent, waiting for ACKs. | No |

### Transitions (8)

| From | To | Trigger |
|------|-----|---------|
| IDLE | ACTIVE | new data arrives |
| ACTIVE | READY | congestion control permits sending |
| ACTIVE | PENDING | no data to send, last retransmit ACKed |
| READY | READY | data sent but more to send |
| READY | ACTIVE | congestion control no longer permits sending |
| READY | PENDING | all data sent |
| PENDING | IDLE | all data ACKed |
| PENDING | ACTIVE | retransmission needed |

### Quality Assessment: **EXEMPLARY**

**Strengths**:
- Complete coverage of Figure 3-98 from UE Spec
- All transitions documented with triggers, conditions, actions
- Line-level traceability to UE Spec (e.g., "Lines 9141-9166")
- Scheduling behavior documented
- CCC lifecycle (creation/destruction) documented
- Related protocols cross-referenced

**Deficiencies**: None identified.

---

## 3. Virtual Channel (VC) State Machine

**Location**: `datamodel/protocols/ue/link/cbfc/protocols/vc_state_machine.ksy`  
**Feature**: 003-ue-packet-taxonomy  
**Spec Reference**: UE Specification v1.0.1, Section 5.2.6, Figure 5-10, Page 490

### States (4)

| State | Description | Terminal |
|-------|-------------|----------|
| DISABLED | DISABLED state | No |
| INITIALIZING | INITIALIZING state | No |
| ACTIVE | ACTIVE state | No |
| REMOVING | REMOVING state | Yes |

### Transitions (1)

| From | To | Trigger |
|------|-----|---------|
| DISABLED | INITIALIZING | start |

### Quality Assessment: **SKELETAL - INCOMPLETE**

**Deficiencies**:

1. **Missing Transitions**: Only 1 of expected ~6-8 transitions defined
   - Missing: INITIALIZING -> ACTIVE
   - Missing: ACTIVE -> REMOVING
   - Missing: ACTIVE -> DISABLED (error path)
   - Missing: REMOVING -> DISABLED
   - Missing: Any error transitions

2. **Placeholder Descriptions**: State descriptions are just the state name repeated (e.g., "DISABLED state")

3. **Missing Processing Details**: No `processing` arrays defining what happens in each state

4. **Missing Conditions**: Transition condition is just "true" - not meaningful

5. **Missing Actions**: Transition action is generic "Begin processing" - not specific

6. **No Error Handling**: No error states or error transitions defined

**Recommendation**: This state machine requires significant completion work to match the quality of the QP and CCC state machines. Reference UE Spec Section 5.2.6 and Figure 5-10 for the complete state machine definition.

---

## 4. UALink DL Link State Machine

**Location**: `datamodel/protocols/ualink/datalink/protocols/link_state.ksy`  
**Feature**: 024-add-ualink-to-topology  
**Spec Reference**: UALink200 Specification v1.0, Section 6.7, Figure 6-23, Page 177; UALink 1.5 DLPL Specification, Section 2.7, Figure 2-24

### States (5)

| State | Code | Description | Terminal |
|-------|------|-------------|----------|
| DL_FAULT | 0x00 | Reset state, link down | No |
| DL_IDLE | 0x01 | Link down, transmit Idle only | No |
| DL_NOP | 0x02 | Link down, transmit NOP DL Flits | No |
| DL_UP | 0x03 | Link up, transmit NOP or payload | No |
| DL_PWRDN | 0x04 | Power down state | No |

### Transitions (6)

| From | To | Trigger |
|------|-----|---------|
| DL_FAULT | DL_IDLE | RS not indicating fault |
| DL_IDLE | DL_NOP | F/W enable |
| DL_NOP | DL_UP | 10 NOP sent + 2 Flits received |
| DL_UP | DL_IDLE | Error/Timeout |
| DL_UP | DL_PWRDN | Link Width Negotiation |
| DL_PWRDN | DL_IDLE | Wake request |

### Quality Assessment: **GOOD**

**Strengths**:
- Complete state coverage from UALink spec
- State codes defined (0x00-0x04)
- ASCII state diagram in documentation
- Dual spec references (UALink200 and DLPL 1.5)
- Timing unit specified (microseconds)
- Enum definition for code generation

**Deficiencies**:

1. **Missing Error Transitions**: No explicit error transitions from DL_NOP or DL_IDLE states

2. **Missing DL_FAULT Entry Transitions**: No transitions showing how to enter DL_FAULT from other states (e.g., on RS fault indication)

3. **Incomplete Processing Details**: States lack `processing` arrays describing behavior

4. **Missing Timing Constraints**: No timeout values specified for transitions

**Recommendation**: Add error transitions and timeout specifications per UALink spec.

---

## 5. Ethernet Queue State Machine

**Location**: `datamodel/protocols/ethernet/queue_state_machine.yaml`  
**Feature**: 015-ethernet-nic-hsi  
**Spec Reference**: specs/015-ethernet-nic-hsi/spec.md, FR-031

### States (4)

| State | ID | Description | Terminal |
|-------|-----|-------------|----------|
| DISABLED | 0 | Queue not created or destroyed | No (initial) |
| ENABLED | 1 | Queue active and processing packets | No |
| QUIESCED | 2 | Queue drained, awaiting resume or destroy | No |
| ERROR | 3 | Queue in error state, requires reset | No |

### Transitions (9)

| Name | From | To | Trigger |
|------|------|-----|---------|
| create | DISABLED | ENABLED | CREATE_*_QUEUE command |
| destroy_from_enabled | ENABLED | DISABLED | DESTROY_QUEUE command |
| destroy_from_quiesced | QUIESCED | DISABLED | DESTROY_QUEUE command |
| quiesce | ENABLED | QUIESCED | MODIFY_QUEUE with quiesce=true |
| resume | QUIESCED | ENABLED | MODIFY_QUEUE with quiesce=false |
| error_from_enabled | ENABLED | ERROR | Fatal error |
| error_from_quiesced | QUIESCED | ERROR | Fatal error during drain |
| reset | ERROR | DISABLED | Queue reset |

### Quality Assessment: **GOOD**

**Strengths**:
- Complete transition matrix provided
- State properties defined (can_process_wqe, can_post_completion, buffer_refill_allowed)
- Error codes enumerated (DMA_FAILURE, PROTECTION_VIOLATION, etc.)
- Test scenarios defined for coverage
- pktgen integration configuration included
- Guards and actions documented for each transition

**Deficiencies**:

1. **Different Format**: Uses YAML format instead of Kaitai Struct (.ksy) - inconsistent with other state machines

2. **No Spec Traceability**: References internal spec (FR-031) but no external standard

3. **Missing Timing Constraints**: No timeout values for error detection or quiesce completion

4. **No State Codes**: States have IDs but no hex codes for hardware implementation

**Recommendation**: Consider converting to .ksy format for consistency, or document why YAML is preferred for this use case.

---

## 6. Block Move Engine (BME) FSM

**Location**: `datamodel/hw/ip/cornelis/ec/views/bme-fsm.puml`  
**Feature**: EC Hardware  
**Spec Reference**: None documented

### States (7)

| State | Description |
|-------|-------------|
| IDLE | Waiting for move request (o_move_busy = 0) |
| REQUEST | Arbitrating for CSR chain (o_move_busy = 1) |
| WAIT_GNT | Waiting for grant (o_move_busy = 1) |
| TRANSFER | Transferring data via CSR chain (o_move_busy = 1) |
| WAIT_ACK | Waiting for acknowledgment (o_move_busy = 1) |
| COMPLETE | Move complete (o_move_done = 1, o_move_busy = 0) |
| ERROR | Error occurred (o_move_error = 1, o_move_busy = 0) |

### Transitions (10)

| From | To | Trigger |
|------|-----|---------|
| IDLE | REQUEST | i_move_req |
| REQUEST | WAIT_GNT | arbitration |
| WAIT_GNT | TRANSFER | grant received |
| TRANSFER | WAIT_ACK | last data |
| WAIT_ACK | COMPLETE | ack received |
| COMPLETE | IDLE | done |
| IDLE | ERROR | error condition |
| REQUEST | ERROR | error condition |
| WAIT_GNT | ERROR | timeout |
| TRANSFER | ERROR | error condition |
| WAIT_ACK | ERROR | timeout |
| ERROR | IDLE | reset |

### Quality Assessment: **DIAGRAM ONLY**

**Strengths**:
- Clear visual representation
- Signal annotations (o_move_busy, o_move_done, o_move_error)
- Error paths from multiple states
- Reset recovery path

**Deficiencies**:

1. **No Machine-Readable Definition**: Only exists as PlantUML diagram, not as .ksy or .yaml

2. **No Spec Traceability**: No reference to hardware specification or MAS document

3. **No Timing Constraints**: Timeout values not specified

4. **No State Codes**: No hex codes for RTL implementation

5. **Incomplete Error Conditions**: "error condition" is vague - should enumerate specific errors

**Recommendation**: Create a corresponding .ksy or .yaml file with full state machine definition. The PlantUML diagram should be generated from the machine-readable definition, not maintained separately.

---

## Cross-Cutting Deficiencies

### 1. Format Inconsistency

State machines use three different formats:
- Kaitai Struct YAML (.ksy) - QP, CCC, VC, UALink
- Plain YAML (.yaml) - Ethernet Queue
- PlantUML only (.puml) - BME FSM

**Recommendation**: Standardize on Kaitai Struct YAML (.ksy) with `x-protocol` metadata for all state machines. Generate PlantUML diagrams from the .ksy definitions.

### 2. Missing State Machines

Based on the protocol taxonomy, the following state machines are likely missing:

| Expected State Machine | Domain | Evidence |
|------------------------|--------|----------|
| PDC State Machine | UE Transport/PDS | Referenced in CCC state machine |
| LLR State Machine | UE Link/LLR | LLR protocol exists but no state machine |
| NSCC/RCCC/TFC State Machines | UE Transport/CMS | Referenced as "related_protocols" in CCC |
| TSS State Machine | UE Transport/TSS | Security protocol likely has states |

### 3. Missing Timing Constraints

Only the UALink state machine specifies a timing unit (`x-timing-unit: us`). Other state machines lack:
- Timeout values for transitions
- Minimum/maximum state durations
- Timing requirements for error detection

### 4. Missing Code Generation Integration

The Ethernet Queue state machine includes `pktgen_integration` configuration, but other state machines lack:
- Code generation targets
- Output format specifications
- Validation test generation

### 5. Incomplete Error Handling

Several state machines have incomplete error handling:
- VC State Machine: No error states or transitions
- UALink: Missing some error entry paths
- BME FSM: Vague "error condition" triggers

---

## Recommendations

### Priority 1: Complete VC State Machine

The VC State Machine is critically incomplete. Actions:
1. Review UE Spec Section 5.2.6 and Figure 5-10
2. Add all missing transitions
3. Add meaningful state descriptions
4. Add processing details for each state
5. Add error handling

### Priority 2: Create Machine-Readable BME FSM

The BME FSM exists only as a diagram. Actions:
1. Create `datamodel/hw/ip/cornelis/ec/protocols/bme_state_machine.ksy`
2. Define all states with codes
3. Define all transitions with triggers, conditions, actions
4. Add spec reference to EC MAS document
5. Update PlantUML to be generated from .ksy

### Priority 3: Add Missing State Machines

Create state machine definitions for:
1. PDC State Machine (UE Transport/PDS)
2. LLR State Machine (UE Link/LLR)
3. NSCC/RCCC/TFC State Machines (UE Transport/CMS)

### Priority 4: Standardize Format

1. Convert Ethernet Queue state machine to .ksy format
2. Establish template for state machine .ksy files
3. Add code generation targets to all state machines

### Priority 5: Add Timing Constraints

For all state machines:
1. Add `x-timing-unit` metadata
2. Specify timeout values for transitions
3. Document timing requirements from specifications

---

## Appendix: State Machine Quality Checklist

Use this checklist when creating or reviewing state machine definitions:

- [ ] All states from specification are defined
- [ ] All transitions from specification are defined
- [ ] Each state has meaningful description
- [ ] Each state has `processing` array (what happens in state)
- [ ] Each state has `is_terminal` flag
- [ ] Each transition has `trigger` (what causes it)
- [ ] Each transition has `condition` (when it's valid)
- [ ] Each transition has `action` (what happens)
- [ ] Each transition has `spec_ref` (traceability)
- [ ] Error states and transitions are defined
- [ ] Timing constraints are specified
- [ ] State codes are defined (for hardware)
- [ ] Spec traceability metadata (`x-spec`) is complete
- [ ] ASCII or PlantUML diagram is included in `doc`
- [ ] Code generation configuration is included

---

## Work List

### Critical Priority (Blocking)

| ID | Task | State Machine | Effort | Status |
|----|------|---------------|--------|--------|
| WL-SM-001 | Complete VC State Machine - add missing transitions (INITIALIZING->ACTIVE, ACTIVE->REMOVING, REMOVING->DISABLED, error paths) | VC State Machine | Medium | Open |
| WL-SM-002 | Add meaningful state descriptions to VC State Machine (replace placeholder text) | VC State Machine | Low | Open |
| WL-SM-003 | Add processing details to VC State Machine states | VC State Machine | Medium | Open |
| WL-SM-004 | Add error states and error transitions to VC State Machine | VC State Machine | Medium | Open |

### High Priority (Significant Gaps)

| ID | Task | State Machine | Effort | Status |
|----|------|---------------|--------|--------|
| WL-SM-005 | Create machine-readable BME FSM definition (`datamodel/hw/ip/cornelis/ec/protocols/bme_state_machine.ksy`) | BME FSM | Medium | Open |
| WL-SM-006 | Add state codes (hex values) to BME FSM for RTL implementation | BME FSM | Low | Open |
| WL-SM-007 | Add spec traceability to BME FSM (reference EC MAS document) | BME FSM | Low | Open |
| WL-SM-008 | Enumerate specific error conditions in BME FSM (replace vague "error condition") | BME FSM | Medium | Open |
| WL-SM-009 | Add missing error transitions to UALink Link State (DL_NOP->DL_FAULT, DL_IDLE->DL_FAULT) | UALink Link State | Low | Open |
| WL-SM-010 | Add DL_FAULT entry transitions from all states on RS fault indication | UALink Link State | Low | Open |

### Medium Priority (Completeness)

| ID | Task | State Machine | Effort | Status |
|----|------|---------------|--------|--------|
| WL-SM-011 | Create PDC State Machine definition (referenced in CCC state machine) | New - PDC | High | Open |
| WL-SM-012 | Create LLR State Machine definition (LLR protocol exists but no state machine) | New - LLR | High | Open |
| WL-SM-013 | Create NSCC State Machine definition (referenced as related protocol in CCC) | New - NSCC | High | Open |
| WL-SM-014 | Create RCCC State Machine definition (referenced as related protocol in CCC) | New - RCCC | High | Open |
| WL-SM-015 | Create TFC State Machine definition (referenced as related protocol in CCC) | New - TFC | High | Open |
| WL-SM-016 | Add timeout values to UALink Link State transitions | UALink Link State | Low | Open |
| WL-SM-017 | Add processing arrays to UALink Link State states | UALink Link State | Medium | Open |

### Low Priority (Standardization)

| ID | Task | State Machine | Effort | Status |
|----|------|---------------|--------|--------|
| WL-SM-018 | Convert Ethernet Queue State Machine from .yaml to .ksy format | Ethernet Queue | Medium | Open |
| WL-SM-019 | Add hex state codes to Ethernet Queue State Machine | Ethernet Queue | Low | Open |
| WL-SM-020 | Add timing constraints to Ethernet Queue State Machine | Ethernet Queue | Low | Open |
| WL-SM-021 | Add `x-timing-unit` metadata to all state machines | All | Low | Open |
| WL-SM-022 | Add code generation configuration to QP State Machine | QP State Machine | Low | Open |
| WL-SM-023 | Add code generation configuration to CCC State Machine | CCC State Machine | Low | Open |
| WL-SM-024 | Add code generation configuration to UALink Link State | UALink Link State | Low | Open |
| WL-SM-025 | Create state machine .ksy template file for consistency | Infrastructure | Medium | Open |
| WL-SM-026 | Update PlantUML BME FSM to be generated from .ksy definition | BME FSM | Low | Blocked by WL-SM-005 |

### Documentation

| ID | Task | State Machine | Effort | Status |
|----|------|---------------|--------|--------|
| WL-SM-027 | Document why Ethernet Queue uses .yaml format (if intentional) or convert | Ethernet Queue | Low | Open |
| WL-SM-028 | Add TSS State Machine if security protocol requires state tracking | New - TSS | Medium | Open |

---

## Work List Summary

| Priority | Open | Blocked | Total |
|----------|------|---------|-------|
| Critical | 4 | 0 | 4 |
| High | 6 | 0 | 6 |
| Medium | 7 | 0 | 7 |
| Low | 10 | 1 | 11 |
| **Total** | **27** | **1** | **28** |

### Effort Estimates

| Effort | Count | Description |
|--------|-------|-------------|
| Low | 12 | < 1 hour, straightforward additions |
| Medium | 11 | 1-4 hours, requires spec review |
| High | 5 | 4+ hours, new state machine creation |

### Dependencies

```
WL-SM-026 (Generate PlantUML from .ksy)
    └── Blocked by: WL-SM-005 (Create BME FSM .ksy)
```

---

## References

| Document | Location |
|----------|----------|
| IB Architecture Specification | External (InfiniBand Trade Association) |
| UE Specification v1.0.1 | External (Ultra Ethernet Consortium) |
| UALink200 Specification v1.0 | External (UALink Consortium) |
| UALink 1.5 DLPL Specification | External (UALink Consortium) |
| Ethernet NIC HSI Spec | `specs/015-ethernet-nic-hsi/spec.md` |
| EC MAS Document | `hw/design/ec_mas/` |
