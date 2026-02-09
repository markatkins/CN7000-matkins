# CMS Documentation Plan

**Work Item**: W-05-003  
**Created**: 2026-01-26  
**Status**: In Progress (Option 3 selected)

---

## 1. Overview

The Congestion Management Sublayer (CMS) is a core component of the Ultra Ethernet Transport (UET) protocol, responsible for:
- Network signal-based congestion control (NSCC)
- Receiver-credit congestion control (RCCC)
- Transport flow control (TFC)
- Multipath path selection
- Telemetry integration (ECN, RTT, packet trimming)

This document outlines the plan for documenting CMS in the PMR Packet Taxonomy.

---

## 2. Current State

### 2.1 Existing Documentation

**File**: `analysis/packet_taxonomy/packet_taxonomy_ue_cms_tss.md`

**CMS Wire Formats Documented (5 files):**

| File | Size | Description | Status |
|------|------|-------------|--------|
| `ack_cc_state_nscc.ksy` | 8 bytes | NSCC congestion state | ✅ Documented |
| `ack_cc_state_rccc_tfc.ksy` | 8 bytes | RCCC/TFC credit state | ✅ Documented |
| `req_cc_state.ksy` | 8 bytes | Request CC state | ✅ Documented |
| `credit_cp_payload.ksy` | Variable | Credit CP payload | ✅ Documented |
| `credit_request_cp_payload.ksy` | Variable | Credit request payload | ✅ Documented |

### 2.2 Datamodel Files Not Yet Documented

**Directory**: `datamodel/protocols/ue/transport/cms/protocols/`

| File | Description | Status |
|------|-------------|--------|
| `ccc_state_machine.ksy` | CCC state machine | ❌ Not documented |
| `nscc_source.ksy` | NSCC source algorithm | ❌ Not documented |
| `nscc_destination.ksy` | NSCC destination algorithm | ❌ Not documented |
| `rccc_source.ksy` | RCCC source algorithm | ❌ Not documented |
| `rccc_destination.ksy` | RCCC destination algorithm | ❌ Not documented |
| `tfc_source.ksy` | TFC source algorithm | ❌ Not documented |
| `tfc_destination.ksy` | TFC destination algorithm | ❌ Not documented |
| `multipath_selection.ksy` | Multipath path selection | ❌ Not documented |

### 2.3 UE Spec Coverage Gap

The UE Specification Section 3.6 "Congestion Management Sublayer (CMS)" is extensive (~70 pages):

| Section | Topic | Documented? |
|---------|-------|-------------|
| 3.6.1 | UET CC Guidelines | ❌ No |
| 3.6.2 | Congestion Control Algorithms | ❌ No |
| 3.6.3 | CC Algorithm Design Targets | ❌ No |
| 3.6.4 | Telemetry and Network Switch Services | ❌ No |
| 3.6.5 | UET CC Protocol Operation Overview | ❌ No |
| 3.6.6 | Congestion Control Context (CCC) | ❌ No |
| 3.6.7 | CCC for ROD PDCs | ❌ No |
| 3.6.8 | Source Context | ❌ No |
| 3.6.9 | UET-CC Header Formats and Fields | ✅ Partial |
| 3.6.10 | Common CC Event Processing | ❌ No |
| 3.6.11 | Congestion Control Modes | ❌ No |
| 3.6.12 | Overall CCC Pseudocode | ❌ No |
| 3.6.13 | NSCC (Network Signal-based CC) | ❌ No |
| 3.6.14 | RCCC (Receiver-Credit CC) | ❌ No |
| 3.6.15 | TFC (Transport Flow Control) | ❌ No |
| 3.6.16 | Multipath Path Selection | ❌ No |
| 3.6.17 | Switch Configuration for UET CC | ❌ No |

---

## 3. Documentation Options

### Option 1: Comprehensive Documentation (High Effort)

**Scope**:
- Document all CMS algorithms with pseudocode
- Add state machine diagrams for NSCC, RCCC, TFC
- Document telemetry mechanisms (ECN, RTT, trimming)
- Add traffic class mapping tables (DSCP to TC)
- Document multipath selection algorithms
- Create detailed protocol interaction diagrams

**Pros**:
- Self-contained documentation
- No need to reference external specs
- Useful for implementation teams

**Cons**:
- High effort (2-3 days)
- Risk of divergence from UE Spec
- Maintenance burden as spec evolves

**Estimated Effort**: 2-3 days

---

### Option 2: Reference-Based Documentation (Medium Effort)

**Scope**:
- Keep current wire format documentation
- Add references to UE Spec sections for algorithm details
- Document key parameters and configuration options
- Add summary tables for each algorithm
- Create overview diagrams

**Pros**:
- Moderate effort
- Maintains UE Spec as authoritative source
- Provides useful summaries

**Cons**:
- Requires access to UE Spec for full details
- May not be sufficient for implementation

**Estimated Effort**: 4-8 hours

---

### Option 3: Datamodel-Focused Documentation (Low Effort) ✅ SELECTED

**Scope**:
- Document the 8 protocol `.ksy` files not yet covered
- Add cross-references to UE Spec sections
- Keep algorithm details in UE Spec (authoritative source)
- Focus on wire formats and state structures

**Pros**:
- Low effort
- Avoids duplication with UE Spec
- Datamodel files capture implementation-relevant details
- Incremental approach - can expand later

**Cons**:
- Algorithm details not in taxonomy docs
- Requires UE Spec for full understanding

**Estimated Effort**: 2-4 hours

---

### Option 4: Defer (No Effort)

**Scope**:
- Mark W-05-003 as "Spec Update" - waiting for implementation needs
- Document only when needed for specific implementation work

**Pros**:
- No immediate effort
- CMS may change as PMR implementation progresses

**Cons**:
- Documentation gap remains
- May slow down future implementation work

**Estimated Effort**: None

---

## 4. Selected Approach: Option 3

### 4.1 Rationale

Option 3 (Datamodel-Focused) was selected because:

1. **UE Spec is authoritative**: The UE Specification is the authoritative source for algorithm details. Duplicating pseudocode risks divergence.

2. **Datamodel captures wire formats**: The `.ksy` files capture the wire formats and state structures needed for implementation.

3. **Incremental approach**: Additional documentation can be added as implementation needs arise.

4. **Maintenance**: Less documentation to maintain as the spec evolves.

### 4.2 Implementation Plan

**Step 1**: Read and analyze the 8 protocol `.ksy` files

**Step 2**: Add new section to `packet_taxonomy_ue_cms_tss.md`:
- Section 2.4: CCC State Machine
- Section 2.5: NSCC Protocol
- Section 2.6: RCCC Protocol
- Section 2.7: TFC Protocol
- Section 2.8: Multipath Selection

**Step 3**: For each protocol file, document:
- Purpose and scope
- Key state variables
- UE Spec reference (section, table, figure)
- Related datamodel files

**Step 4**: Update cross-references and datamodel file list

**Step 5**: Update tracking documents (packet_taxonomy.md, DATAMODEL_UPDATES.md)

### 4.3 Deliverables

1. Updated `packet_taxonomy_ue_cms_tss.md` with protocol documentation
2. Updated `packet_taxonomy.md` with W-05-003 closure
3. This plan file for future reference

---

## 5. References

- UE Specification v1.0.1, Section 3.6 (Congestion Management Sublayer)
- `datamodel/protocols/ue/transport/cms/` - CMS datamodel files
- `analysis/packet_taxonomy/packet_taxonomy_ue_cms_tss.md` - Current CMS documentation

---

## 6. Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-01-26 | Initial plan created | Claude AI |
| 2026-01-26 | Option 3 selected and implementation started | Claude AI |
