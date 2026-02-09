# Plan: L2 Header Selection Datamodel Additions

**Created**: 2026-02-03  
**Completed**: 2026-02-03  
**Status**: ✅ ARCHIVED (All tasks complete)  
**Estimated Effort**: 4-6 hours  
**Type**: Datamodel Enhancement  
**Related**: W-09-009 (PMR L2 Header Selection Rules), W-16 (L2 Header Selection Datamodel)

---

## Completion Summary

All 7 tasks completed and verified. Work item W-16 closed in `WORK_ITEMS.md`.

**Commit**: `7ab5916f` pushed to origin/main

**Deliverables Created**:
- ✅ `ue/link/lldp/protocols/link_negotiation_sm.ksy` - Link capability negotiation state machine
- ✅ `cornelis/config/address_vector.ksy` - Per-destination protocol configuration  
- ✅ `cornelis/protocols/l2_header_selection_sm.ksy` - L2 header selection decision logic
- ✅ `cornelis/config/peer_capability.ksy` - Per-peer capability state
- ✅ 3 metadata.yaml files for new directories
- ✅ W-16 added to WORK_ITEMS.md (now in Recently Closed)
- ✅ Section 2.7 added to packet_taxonomy_ue_plus_variants.md

---

## Objective

Add state machines and configuration models to support the L2 header selection decisions documented in W-09-009. Currently the datamodel has packet formats but lacks the decision logic models.

---

## Background

W-09-009 documented when PMR uses UE+ vs Ethernet headers:
- **UE+ (12B)**: Both endpoints support UE+, fabric-managed HMAC, link negotiated
- **Ethernet II (14B)**: Peer doesn't support UE+, RoCEv2, standard UE, Ethernet services

The datamodel needs state machines and configuration structures to model these decisions.

---

## Gap Analysis

| Component | Current State | Required |
|-----------|---------------|----------|
| UE+ packet format | ✅ `ue_plus.ksy` | Complete |
| Ethernet format | ✅ `ethernet/` | Complete |
| L2 type enum | ✅ `cornelis_l2_prefix.ksy` | Complete |
| Link negotiation TLV | ✅ `ue_link_negotiation_tlv.ksy` | Complete |
| Link negotiation SM | ❌ Missing | New file needed |
| Address Vector config | ❌ Missing | New file needed |
| L2 selection SM | ❌ Missing | New file needed |
| Peer capability state | ❌ Missing | New file needed |

---

## Tasks

### Task 1: Create Link Negotiation State Machine

**File**: `earlysim/datamodel/protocols/ue/link/lldp/protocols/link_negotiation_sm.ksy`

**Description**: Model the LLDP-based link capability negotiation process that determines if both endpoints support UE+.

**Content Structure**:
```yaml
meta:
  id: link_negotiation_sm
  title: UE Link Negotiation State Machine

x-protocol:
  protocol_type: "state_machine"
  state_machine:
    states:
      - INIT: Initial state, no negotiation
      - DISCOVERING: Sending/receiving LLDP TLVs
      - NEGOTIATING: Processing peer capabilities
      - UE_PLUS_ENABLED: Both peers support UE+
      - ETHERNET_ONLY: Peer doesn't support UE+
      - ERROR: Negotiation failed
    
    transitions:
      - from: INIT, to: DISCOVERING, trigger: link_up
      - from: DISCOVERING, to: NEGOTIATING, trigger: lldp_tlv_received
      - from: NEGOTIATING, to: UE_PLUS_ENABLED, trigger: peer_supports_ue_plus
      - from: NEGOTIATING, to: ETHERNET_ONLY, trigger: peer_no_ue_plus
      - from: *, to: INIT, trigger: link_down

    configuration:
      - lldp_tx_interval: LLDP transmission interval
      - negotiation_timeout: Max time to wait for peer
      - ue_version_required: Minimum UE version to accept

    state_variables:
      - local_capabilities: Our UE+ capabilities
      - peer_capabilities: Received peer capabilities
      - negotiation_result: Final negotiated mode
```

**References**:
- `ue/link/lldp/ue_link_negotiation_tlv.ksy` - TLV format
- UE Spec Section 5.3.2.1 - Link Negotiation

**Acceptance Criteria**:
- [x] File created with valid Kaitai syntax
- [x] States cover all negotiation outcomes
- [x] Transitions match UE Spec behavior
- [x] Cross-references to existing TLV file

**Status**: ✅ COMPLETE

---

### Task 2: Create Address Vector Configuration Model

**File**: `earlysim/datamodel/protocols/cornelis/config/address_vector.ksy`

**Description**: Model the libfabric Address Vector (AV) configuration that determines per-destination L2 header selection.

**Content Structure**:
```yaml
meta:
  id: address_vector_entry
  title: Address Vector Entry Configuration

doc: |
  Address Vector entry for per-destination protocol selection.
  
  The AV determines which L2 header to use for each destination:
  - UE+ peer (HMAC): Use UE+ 12-byte header
  - Standard UE peer: Use Ethernet II + IPv4/IPv6 + UDP
  - RoCEv2 peer: Use Ethernet II + IPv4/IPv6 + UDP

seq:
  - id: av_flags
    type: av_flags_t
    doc: Address vector flags
    
  - id: dest_addr
    type: dest_address_t
    doc: Destination address (format depends on protocol)
    
  - id: protocol_type
    type: u1
    enum: protocol_type_enum
    doc: Protocol selection for this destination

types:
  av_flags_t:
    seq:
      - id: ue_plus_capable
        type: b1
        doc: Destination supports UE+
      - id: hmac_valid
        type: b1
        doc: HMAC address is valid (fabric-managed)
      - id: ipv4_valid
        type: b1
        doc: IPv4 address is valid
      - id: ipv6_valid
        type: b1
        doc: IPv6 address is valid
      - id: reserved
        type: b4

  dest_address_t:
    seq:
      - id: hmac
        size: 3
        doc: 24-bit Hierarchical MAC (if ue_plus_capable)
      - id: mac48
        size: 6
        doc: 48-bit MAC address
      - id: ipv4
        size: 4
        doc: IPv4 address (if ipv4_valid)
      - id: ipv6
        size: 16
        doc: IPv6 address (if ipv6_valid)

enums:
  protocol_type_enum:
    0: ue_plus
    1: ue_standard
    2: rocev2
    3: ethernet
```

**References**:
- CN7000 HFI Requirements, HFI_ARCH_003
- libfabric fi_av(3) man page

**Acceptance Criteria**:
- [x] File created with valid Kaitai syntax
- [x] Covers all protocol types (UE+, UE, RoCEv2, Ethernet)
- [x] Address formats match each protocol's requirements
- [x] Flags enable per-destination selection

**Status**: ✅ COMPLETE

---

### Task 3: Create L2 Header Selection State Machine

**File**: `earlysim/datamodel/protocols/cornelis/protocols/l2_header_selection_sm.ksy`

**Description**: Model the decision logic for selecting UE+ vs Ethernet L2 header based on link state, peer capability, and AV configuration.

**Content Structure**:
```yaml
meta:
  id: l2_header_selection_sm
  title: L2 Header Selection State Machine

doc: |
  L2 Header Selection Decision Logic
  
  Determines whether to use UE+ (12-byte) or Ethernet II (14-byte) header
  for each packet based on:
  1. Link negotiation result (UE+ capable?)
  2. Peer capability (supports UE+?)
  3. Address Vector configuration (per-destination)
  4. Protocol type (RoCEv2 always uses Ethernet)

x-protocol:
  protocol_type: "state_machine"
  state_machine:
    description: "Per-packet L2 header selection"
    
    inputs:
      - link_state: Current link negotiation state
      - av_entry: Address Vector entry for destination
      - packet_type: Type of packet being sent
      
    decision_tree:
      - condition: "packet_type == ROCEV2"
        result: ETHERNET_II
        reason: "RoCEv2 always uses Ethernet + IP + UDP"
        
      - condition: "packet_type == ETHERNET_SERVICE"
        result: ETHERNET_II
        reason: "PTP, management, netdev use standard Ethernet"
        
      - condition: "link_state != UE_PLUS_ENABLED"
        result: ETHERNET_II
        reason: "Link did not negotiate UE+ capability"
        
      - condition: "!av_entry.ue_plus_capable"
        result: ETHERNET_II
        reason: "Destination does not support UE+"
        
      - condition: "!av_entry.hmac_valid"
        result: ETHERNET_II
        reason: "No fabric-managed HMAC for destination"
        
      - condition: "av_entry.protocol_type == UE_STANDARD"
        result: ETHERNET_II
        reason: "AV configured for standard UE over UDP"
        
      - condition: "default"
        result: UE_PLUS
        reason: "All conditions met for UE+ header"

    outputs:
      - l2_header_type: UE_PLUS | ETHERNET_II
      - addressing_mode: HMAC_24 | MAC_48
      - encapsulation: NONE | IPV4_UDP | IPV6_UDP

x-related-files:
  - path: "../link/ue_plus.ksy"
    description: "UE+ header format"
  - path: "../../ethernet/ethernet_ii.ksy"
    description: "Ethernet II header format"
  - path: "../config/address_vector.ksy"
    description: "Address Vector configuration"
  - path: "../../ue/link/lldp/protocols/link_negotiation_sm.ksy"
    description: "Link negotiation state machine"
```

**References**:
- W-09-009 documentation in `packet_taxonomy_ue_plus_variants.md`
- CN7000 HFI Requirements, HFI_ARCH_003

**Acceptance Criteria**:
- [x] File created with valid Kaitai syntax
- [x] Decision tree covers all W-09-009 conditions
- [x] Cross-references to related files
- [x] Documents simultaneous protocol support principle

**Status**: ✅ COMPLETE

---

### Task 4: Create Peer Capability State Model

**File**: `earlysim/datamodel/protocols/cornelis/config/peer_capability.ksy`

**Description**: Model the per-peer capability state tracked by the NIC.

**Content Structure**:
```yaml
meta:
  id: peer_capability
  title: Peer Capability State

doc: |
  Per-peer capability state maintained by the NIC.
  
  Tracks what each peer supports based on:
  - LLDP negotiation results
  - Fabric management information
  - Runtime discovery

seq:
  - id: peer_id
    type: u4
    doc: Peer identifier (index into peer table)
    
  - id: capabilities
    type: capability_flags_t
    doc: Peer capability flags
    
  - id: ue_version
    type: u1
    doc: Peer's UE specification version
    
  - id: hmac_address
    size: 3
    doc: Peer's HMAC address (if fabric-managed)
    
  - id: last_updated
    type: u8
    doc: Timestamp of last capability update

types:
  capability_flags_t:
    seq:
      - id: ue_plus_supported
        type: b1
        doc: Peer supports UE+ protocol
      - id: llr_supported
        type: b1
        doc: Peer supports Link Layer Retry
      - id: cbfc_supported
        type: b1
        doc: Peer supports Credit-Based Flow Control
      - id: tss_supported
        type: b1
        doc: Peer supports Transport Security
      - id: fabric_managed
        type: b1
        doc: Peer has fabric-assigned HMAC
      - id: rocev2_supported
        type: b1
        doc: Peer supports RoCEv2
      - id: reserved
        type: b2
```

**References**:
- `ue/link/lldp/ue_link_negotiation_tlv.ksy` - Capability TLV
- CN7000 HFI Requirements

**Acceptance Criteria**:
- [x] File created with valid Kaitai syntax
- [x] Covers all relevant peer capabilities
- [x] Includes fabric management state (HMAC)
- [x] Timestamp for staleness detection

**Status**: ✅ COMPLETE

---

### Task 5: Create Directory Structure and Metadata

**Files**:
- `earlysim/datamodel/protocols/cornelis/config/metadata.yaml`
- `earlysim/datamodel/protocols/cornelis/protocols/metadata.yaml`
- `earlysim/datamodel/protocols/ue/link/lldp/protocols/metadata.yaml`

**Description**: Create metadata files for new directories and update existing metadata.

**Acceptance Criteria**:
- [x] Directory structure created
- [x] Metadata files list all new KSY files
- [x] Cross-references documented

**Status**: ✅ COMPLETE

**Files Created**:
- `cornelis/config/metadata.yaml`
- `cornelis/protocols/metadata.yaml`
- `ue/link/lldp/protocols/metadata.yaml`

---

### Task 6: Update WORK_ITEMS.md

**File**: `analysis/packet_taxonomy/WORK_ITEMS.md`

**Action**: Add new work item for this datamodel enhancement and track completion.

**New Work Item**:
```markdown
### W-16: L2 Header Selection Datamodel

| Field | Value |
|-------|-------|
| **Status** | Open |
| **Priority** | Medium |
| **Category** | Datamodel |
| **Created** | 2026-02-03 |

**Description**: Add state machines and configuration models to support L2 header selection decisions (W-09-009).

**Deliverables**:
- [ ] `ue/link/lldp/protocols/link_negotiation_sm.ksy`
- [ ] `cornelis/config/address_vector.ksy`
- [ ] `cornelis/protocols/l2_header_selection_sm.ksy`
- [ ] `cornelis/config/peer_capability.ksy`
- [ ] Directory metadata files

**Dependencies**:
- W-09-009 (completed - provides requirements)
```

**Acceptance Criteria**:
- [x] W-16 added to Open Work Items
- [x] All deliverables listed
- [x] Dependencies documented

**Status**: ✅ COMPLETE (W-16 now in Recently Closed section)

---

### Task 7: Update packet_taxonomy_ue_plus_variants.md

**File**: `analysis/packet_taxonomy/packet_taxonomy_ue_plus_variants.md`

**Action**: Add reference to new datamodel files in Section 2 (L2 Header Selection Rules).

**Content to add** (after Section 2.6 Reference):
```markdown
### 2.7 Datamodel Support

The following datamodel files support L2 header selection:

| File | Purpose |
|------|---------|
| `ue/link/lldp/protocols/link_negotiation_sm.ksy` | Link capability negotiation state machine |
| `cornelis/config/address_vector.ksy` | Per-destination protocol configuration |
| `cornelis/protocols/l2_header_selection_sm.ksy` | L2 header selection decision logic |
| `cornelis/config/peer_capability.ksy` | Per-peer capability state |
```

**Acceptance Criteria**:
- [x] Section 2.7 added
- [x] All new files referenced
- [x] Table format consistent with document

**Status**: ✅ COMPLETE

---

## Verification

- [x] All 4 new KSY files created
- [x] All files pass Kaitai syntax validation
- [x] Directory metadata files created
- [x] W-16 work item added to WORK_ITEMS.md
- [x] Section 2.7 added to packet_taxonomy_ue_plus_variants.md
- [x] Cross-references between files are correct
- [x] Files follow existing datamodel conventions

---

## File Summary

| New File | Location | Purpose |
|----------|----------|---------|
| `link_negotiation_sm.ksy` | `ue/link/lldp/protocols/` | Link negotiation state machine |
| `address_vector.ksy` | `cornelis/config/` | AV configuration model |
| `l2_header_selection_sm.ksy` | `cornelis/protocols/` | L2 selection decision logic |
| `peer_capability.ksy` | `cornelis/config/` | Peer capability state |

---

## Notes

- These files model the **decision logic**, not the packet formats (which already exist)
- The state machines use the `x-protocol.state_machine` schema pattern established in the codebase
- Files should follow the conventions in `earlysim/datamodel/AGENTS.md`
- This work enables future simulation of L2 header selection behavior
