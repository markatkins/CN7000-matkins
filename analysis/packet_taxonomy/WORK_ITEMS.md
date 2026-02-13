# Packet Taxonomy Work Items

**Document**: Active work tracking for packet taxonomy documentation  
**Location**: `analysis/packet_taxonomy/`  
**Last Updated**: 2026-02-03

---

## Table of Contents

1. [Open Work Items](#1-open-work-items)
2. [Deferred Work Items](#2-deferred-work-items)
3. [Datamodel Gaps](#3-datamodel-gaps)
4. [Specification Questions](#4-specification-questions)
5. [Recently Closed](#5-recently-closed)
6. [Archive Reference](#6-archive-reference)

---

## 1. Open Work Items

### W-17: VLAN Protocol Coverage Verification

| Field | Value |
|-------|-------|
| **Status** | Open |
| **Priority** | Medium |
| **Category** | Datamodel Review |
| **Created** | 2026-02-03 |
| **Estimated Effort** | 2-3 hours |

**Description**: Verify that VLAN (IEEE 802.1Q) is properly described in all protocols that need it.

**Current Coverage**:
- ✅ `ethernet/link/vlan_802_1q.ksy` - Core VLAN tag format
- ✅ `ethernet/link/ethernet_ii.ksy` - VLAN tag detection
- ✅ `ethernet/link/ethernet_802_3.ksy` - VLAN reference
- ✅ `cornelis/link/cornelis_l2_prefix.ksy` - VLAN indicator flag
- ✅ `ethernet/network/ipv4.ksy`, `ipv6.ksy` - VLAN cross-references

**Gaps to Investigate**:
- [ ] UE+ packets over VLAN-tagged Ethernet - is this supported?
- [ ] RoCEv2 over VLAN - verify datamodel coverage
- [ ] UFH headers with VLAN - does UFH replace or coexist with VLAN?
- [ ] VxLAN+ inner VLAN handling
- [ ] Document VLAN interaction with each L2 header type in `l2_header_selection_sm.ksy`

**Deliverables**:
- Updated datamodel files with VLAN cross-references where missing
- Section in `packet_taxonomy_ue_plus_variants.md` documenting VLAN interactions

---

### W-18: VXLAN Protocol Coverage Verification

| Field | Value |
|-------|-------|
| **Status** | Open |
| **Priority** | Medium |
| **Category** | Datamodel Review |
| **Created** | 2026-02-03 |
| **Estimated Effort** | 3-4 hours |

**Description**: Verify that VXLAN is properly described in all protocols that need it.

**Current Coverage**:
- ✅ `cornelis/encapsulation/vxlan_plus.ksy` - Cornelis VxLAN+ (4-byte proprietary)
- ✅ `ethernet/transport/udp.ksy` - VXLAN port (4789)
- ✅ `ue/network/packet_trimming.ksy` - VXLAN overhead calculations

**Gaps to Investigate**:
- [ ] Create standard `ethernet/encapsulation/vxlan.ksy` (RFC 7348) - currently only VxLAN+ exists
- [ ] Document when to use VxLAN+ vs standard VXLAN
- [ ] RoCEv2 over VXLAN encapsulation
- [ ] UE over VXLAN (FEP mode tunneling)
- [ ] VXLAN GPE (Generic Protocol Extension) for UE
- [ ] Add VXLAN to L2 header selection decision tree

**Deliverables**:
- `ethernet/encapsulation/vxlan.ksy` - Standard VXLAN header (RFC 7348)
- Updated `l2_header_selection_sm.ksy` with VXLAN encapsulation decisions
- Documentation of VxLAN+ vs VXLAN selection rules

---

### W-19: UFH Rules for L2 Header Selection

| Field | Value |
|-------|-------|
| **Status** | Open |
| **Priority** | High |
| **Category** | Architecture |
| **Created** | 2026-02-03 |
| **Estimated Effort** | 4-6 hours |

**Description**: Include UFH (Unified Forwarding Header) rules in L2 header selection. Differentiate between scale-out vs scale-up use cases and when to use UE+ versions vs UE standard versions.

**Current State**:
- `ue/network/ufh_16.ksy`, `ufh_32.ksy` - UE standard UFH headers
- `cornelis/network/ufh_16_plus.ksy`, `ufh_32_plus.ksy` - Cornelis extensions
- `cornelis/network/scaleup_l2.ksy` - Scale-up specific header
- `cornelis/protocols/l2_header_selection_sm.ksy` - Does NOT include UFH selection

**Scale-out vs Scale-up Differentiation**:

| Topology | Header | Addressing | Use Case |
|----------|--------|------------|----------|
| Scale-out | UFH-32 | 32-bit fabric addresses | Large HPC clusters, multi-rack |
| Scale-up | UFH-16 | 16-bit local addresses | Single-rack, GPU interconnect |
| Scale-up | scaleup_l2 | Node IDs | Proprietary scale-up domain |

**UE+ vs UE Standard Selection**:

| Condition | Header Version | Reason |
|-----------|----------------|--------|
| Both endpoints Cornelis | UFH-16+/32+ | Proprietary extensions available |
| Mixed vendor fabric | UFH-16/32 (UE standard) | Interoperability required |
| UEC-standardized fabric | UFH-16/32 (UE standard) | Compliance with UE Spec |

**Deliverables**:
- [ ] Update `l2_header_selection_sm.ksy` with UFH selection decision tree
- [ ] Create `cornelis/protocols/ufh_selection_sm.ksy` - UFH-16 vs UFH-32 selection
- [ ] Document scale-out vs scale-up topology detection
- [ ] Add UFH selection to `packet_taxonomy_ue_plus_variants.md` Section 2

**Dependencies**:
- W-09-009 (completed - provides L2 selection framework)
- W-16 (completed - provides base state machines)

---

### W-20: Link Negotiation Review for Multi-Protocol Support

| Field | Value |
|-------|-------|
| **Status** | Open |
| **Priority** | High |
| **Category** | Architecture Review |
| **Created** | 2026-02-03 |
| **Estimated Effort** | 6-8 hours |

**Description**: Review link negotiation as it relates to UE, Ethernet, UE+, and UALink. Assess whether the current `link_negotiation_sm.ksy` is appropriate for configuring L2 header type selection.

**Current State**:
- `ue/link/lldp/protocols/link_negotiation_sm.ksy` - LLDP-based UE+ negotiation
- `ue/link/lldp/ue_link_negotiation_tlv.ksy` - UE Link Negotiation TLV
- `ue/link/lldp/ue_cbfc_tlv.ksy` - CBFC capability TLV
- 38 UALink protocol files in `ualink/` - separate link layer

**Protocols to Review**:

| Protocol | Link Negotiation Method | Current Coverage |
|----------|------------------------|------------------|
| UE+ | LLDP with UE TLVs | ✅ `link_negotiation_sm.ksy` |
| Standard UE | LLDP with UE TLVs | ✅ Same as UE+ |
| Ethernet | Auto-negotiation (IEEE 802.3) | ❌ Not modeled |
| RoCEv2 | DCBX (PFC, ETS) | ❌ Not modeled |
| UALink | UALink-specific (UPLI handshake) | ❌ Not integrated |

**Review Questions**:
1. Should `link_negotiation_sm.ksy` be extended or should separate SMs exist per protocol?
2. How does UALink link training (`ualink/physical/protocols/link_training.ksy`) interact with L2 selection?
3. Is DCBX negotiation needed for RoCEv2 L2 selection?
4. How does Ethernet auto-negotiation affect UFH vs Ethernet II selection?
5. Should link negotiation output feed directly into `l2_header_selection_sm.ksy`?

**Deliverables**:
- [ ] Architecture document: Link negotiation strategy for multi-protocol support
- [ ] Update or create link negotiation state machines as needed:
  - [ ] `ethernet/link/protocols/autoneg_sm.ksy` - Ethernet auto-negotiation (if needed)
  - [ ] `roce/link/protocols/dcbx_sm.ksy` - DCBX for RoCEv2 (if needed)
  - [ ] Integration with `ualink/datalink/protocols/link_state.ksy`
- [ ] Update `l2_header_selection_sm.ksy` inputs to include all negotiation results
- [ ] Update `peer_capability.ksy` with protocol-specific capability flags

**References**:
- UE Spec Section 5.3.2.1 - Link Negotiation
- IEEE 802.3 Clause 28 - Auto-Negotiation
- IEEE 802.1Qbb - Priority-based Flow Control (PFC)
- UALink Spec - Link Training

---

### W-11-009: IB Spec 2.0 Review

| Field | Value |
|-------|-------|
| **Status** | Pending |
| **Priority** | Medium |
| **Category** | Investigation |
| **Created** | 2026-01-27 |

**Description**: Obtain and review InfiniBand Architecture Specification Release 2.0 (announced Nov 2025). Compare with Release 1.4 for RoCEv2-relevant changes. Contact IBTA at administration@infinibandta.org for access.

---


### W-21: Collective Acceleration Packet Format Definitions

| Field | Value |
|-------|-------|
| **Status** | Open |
| **Priority** | High |
| **Category** | Datamodel |
| **Created** | 2026-02-09 |
| **Estimated Effort** | 8-12 hours |

**Description**: Define comprehensive packet format KSY files for collective acceleration operations. The current datamodel has a single `collective_l2.ksy` header (4 bytes) but lacks the full set of packet formats needed for hardware-accelerated collectives via the Collectives Engine (CE).

**Current Coverage**:
- ✅ `cornelis/network/collective_l2.ksy` - 4-byte collective L2 header (op, flags, group_id, sequence, dtype, count)
- ✅ `hw/ip/cornelis/ce/descriptors.ksy` - CE command/completion descriptors (host-side, opcodes 0x20-0x2C)
- ✅ `hw/ip/cornelis/ce/fsms/ce_scheduler_fsm.ksy` - CE firmware dispatch model
- ✅ `ue/network/ufh_32.ksy` - UFH-32 collective/multicast/barrier/reduction type enums
- ✅ `ue/network/ufh_16.ksy` - UFH-16 collective type enum
- ✅ `cornelis/network/ufh_16_plus.ksy`, `ufh_32_plus.ksy` - Cornelis UFH extensions with collective types

**Gaps to Address**:
- [ ] Collective data packet format (payload carrying reduction operands)
- [ ] Collective control packet format (tree setup, group management, completion signals)
- [ ] Collective ACK/NACK format (reliability for collective operations)
- [ ] Reduction operation header extensions (reduction operator enum: SUM, MIN, MAX, AND, OR, XOR, etc.)
- [ ] Tree topology descriptor (parent/child relationships, fan-in/fan-out)
- [ ] Ring topology descriptor (predecessor/successor, ring direction)
- [ ] Collective completion/notification packet format
- [ ] Barrier synchronization packet format (arrival, release phases)
- [ ] Multi-phase collective sequence definitions (e.g., allreduce = reduce + broadcast)
- [ ] CE-to-network interface packet format (how CE cores inject/receive collective packets)
- [ ] Integration with `collective_l2.ksy` — extend or create companion formats

**Relationship to Existing Work**:
- `collective_l2.ksy` defines the L2 header but not the full packet stack
- CE descriptors (`hw/ip/cornelis/ce/descriptors.ksy`) define host→CE commands, not CE→network packets
- UFH headers reference collective types but don't define the collective payload formats
- CE firmware dispatch model shows reduce_handler and command_handler states but packet formats for these are undefined

**Deliverables**:
- [ ] `cornelis/network/collective_data.ksy` - Collective data packet (reduction operands)
- [ ] `cornelis/network/collective_control.ksy` - Collective control packet (setup, teardown, completion)
- [ ] `cornelis/network/collective_ack.ksy` - Collective reliability (ACK/NACK)
- [ ] `cornelis/network/collective_barrier.ksy` - Barrier synchronization packets
- [ ] `cornelis/network/collective_topology.ksy` - Tree/ring topology descriptors
- [ ] `cornelis/network/collective_sequences/` - Multi-phase collective sequence definitions
- [ ] Update `collective_l2.ksy` with cross-references to new formats
- [ ] Update `ufh_32_plus.ksy` and `ufh_16_plus.ksy` with collective next-header references
- [ ] Documentation in `packet_taxonomy_ue_plus_variants.md` Section on collective packet flows

**References**:
- `datamodel/protocols/cornelis/network/collective_l2.ksy` - Existing collective L2 header
- `datamodel/hw/ip/cornelis/ce/descriptors.ksy` - CE command descriptors
- `datamodel/hw/ip/cornelis/ce/fsms/ce_scheduler_fsm.ksy` - CE firmware dispatch model
- CN7000 Packet Taxonomy (internal)
- MPI Standard (collective operation semantics)
- NCCL/RCCL (GPU collective patterns for reference)

**Sub-Items**:

#### W-21-001: HAS vs Datamodel Collective Review and Alignment Plan

| Field | Value |
|-------|-------|
| **Status** | Open |
| **Priority** | High |
| **Category** | Review / Alignment |
| **Estimated Effort** | 4-6 hours |

**Description**: Review all HAS references to collective operations against the datamodel, determine which source is correct where they diverge, and produce an alignment plan for updates.

**Scope**: The HAS references collectives across multiple chapters but Chapter 16 (Collectives Engine) is **missing** (tracked as W-16-CE-001 in `earlysim/docs/HAS/PMR/WORK.md`). Meanwhile, the datamodel has `collective_l2.ksy` and CE descriptors that may not match what the HAS prose describes. This sub-item reconciles the two.

**HAS Chapters Referencing Collectives** (all must be reviewed):

| Chapter | Section | Content | Key Claims to Verify |
|---------|---------|---------|---------------------|
| Ch 2 (Overview) | §2 Collective Protocol | Protocol overview | In-network reduction, tree-based aggregation, VLEN=1024 |
| Ch 3 (Architecture) | §3 CE block | CE parameters, data path | 4 cores, AX45MPV, 128KB ILM+DLM, S2V/V2S streaming |
| Ch 4 (Addressing) | §4 Multicast/Collective | Tree addressing | Multicast LID range 0xC00000-0xFFFFFE, parent/child/root |
| Ch 5 (Packet Formats) | §5 Collective L2 Header | Header format | Points to `datamodel/cornelis/network/collective_l2.ksy` (path wrong — missing `protocols/`) |
| Ch 6 (Programming) | §6 Collective Operations | Programming model | CE firmware, allreduce/reduce/broadcast/barrier |
| Ch 8 (HDM) | §8 CE Interface | HDM port for CE | 1 CE port, 32 GB/s, descriptor fetch + operand DMA |
| Ch 15 (CTU) | §15 Small-Data Collectives | CTU vs CE tradeoff | CE ~500ns latency, CTU for <256B, CE for >1KB |
| Ch 16 (TX Path) | §16 CE TX Path | CE egress | Dedicated VL (VL5), CE priority, ~1.6 GHz |
| Ch 17 (RX Path) | §17 CE RX Path | CE ingress, steering | Opcode 0x20-0x2C, CE queue, PTAG variant TBD |
| Ch 24 (Errors) | §24 CE Errors | Error codes 0x0400-0x04FF | CE freeze mode, firmware exceptions |

**Datamodel Files to Review Against HAS**:

| File | What to Check |
|------|---------------|
| `protocols/cornelis/network/collective_l2.ksy` | Does 4-byte header match HAS Ch 5 description? Are op/flags/group_id/sequence/dtype/count fields documented in HAS? |
| `hw/ip/cornelis/ce/descriptors.ksy` | Do CE opcodes 0x20-0x2C match HAS Ch 17 steering range? Are all descriptor fields documented? |
| `hw/ip/cornelis/ce/fsms/ce_scheduler_fsm.ksy` | Does firmware dispatch model match HAS Ch 3 CE description? |
| `protocols/ue/network/ufh_32.ksy` | Do UFH collective/multicast/barrier/reduction enums match HAS? |
| `protocols/cornelis/network/ufh_16_plus.ksy`, `ufh_32_plus.ksy` | Do Cornelis UFH collective types match HAS? |
| `hw/ip/cornelis/ce/views/*.puml` | Do CE behavioral diagrams match HAS Ch 3 architecture? |

**Authority Resolution** (per AGENTS.md hierarchy):
- **Datamodel is authoritative** for packet formats, descriptor layouts, and field definitions
- **HAS is authoritative** for architectural intent, programming model, and system-level behavior
- **Where they conflict**: Determine which reflects the intended design, update the other
- **Where both are incomplete**: Flag as gap requiring CE architecture team input

**Deliverables**:
- [ ] Comparison table: HAS claim → Datamodel state → Match/Mismatch/Gap
- [ ] List of HAS corrections needed (wrong paths, stale claims, missing details)
- [ ] List of datamodel gaps (formats described in HAS but not in datamodel)
- [ ] List of items requiring CE architecture team input (neither source definitive)
- [ ] Alignment plan with prioritized updates (which to fix first)
- [ ] Cross-reference to existing work items (W-16-CE-001 in HAS WORK.md, W-05-* in has-datamodel-comparison.md)

**Known Issues Already Identified**:
- HAS Ch 5 references `datamodel/cornelis/network/collective_l2.ksy` — path is wrong (missing `protocols/` prefix), tracked as systemic issue in `has-datamodel-comparison.md`
- HAS Ch 16 (Collectives Engine) is entirely missing (W-16-CE-001)
- CE PTAG variant format is TBD (noted in Ch 17 RX path)
- Collective tree addressing details deferred (W-04-001 in HAS WORK.md)
- HAS Ch 3 says AX45MPV but CE descriptors.ksy says AX46MPV — need to determine which is correct

**Dependencies**:
- W-19 (UFH rules — collective packets use UFH headers)
- CE architecture documents (`earlysim/docs/HAS/CE/`)
- `earlysim/datamodel/protocols/working/reviews/has-datamodel-comparison.md` (existing HAS vs datamodel review)

---

**Dependencies**:
- W-19 (UFH rules — collective packets use UFH headers)
- W-21-001 (HAS review — determines what's correct before building new formats)
- CE architecture documents (`earlysim/docs/HAS/CE/`)

---

## 2. Deferred Work Items

### W-15: UE+ to CN7000 Packet Taxonomy.ppt Comparison Table

| Field | Value |
|-------|-------|
| **Status** | Deferred |
| **Priority** | Medium |
| **Category** | Documentation |
| **Estimated Effort** | 2-4 hours |
| **Created** | 2026-02-02 |
| **Deferred** | 2026-02-03 |
| **Deferral Reason** | Requires SharePoint access to CN7000 Packet Taxonomy.ppt |

**Description**: Create a comparison table mapping UE+ packet types (as documented in `packet_taxonomy_ue_plus_variants.md`) to the nomenclature used in CN7000 Packet Taxonomy.ppt.

**Expected Deliverable**: A new section in `packet_taxonomy_ue_plus_variants.md` with a comparison table containing:

| UE Spec Name | CN7000 PPT Name | Key Differences | Notes |
|--------------|-----------------|-----------------|-------|
| UE Tagged Send (Standard) | TBD | TBD | TBD |
| UE + CSIG Compact | TBD | TBD | TBD |
| UE + CSIG Wide | TBD | TBD | TBD |
| UE IPv4 Native | TBD | TBD | TBD |
| UE + Encrypted (TSS) | TBD | TBD | TBD |
| UE Small Message | TBD | TBD | TBD |
| UE Rendezvous Send | TBD | TBD | TBD |
| UE Deferrable Send | TBD | TBD | TBD |

**Dependencies**:
- Requires access to CN7000 Packet Taxonomy.ppt (internal document)
- `packet_taxonomy_ue_plus_variants.md` must be complete ✅

**References**:
- CN7000 Packet Taxonomy.ppt (SharePoint: OPA Engineering Documentation/Projects/CN7000/General/Landing Zone/)
- UltraEthernet Specification v1.0.1
- `analysis/packet_taxonomy/packet_taxonomy_ue_plus_variants.md`

**To Undefer**: Download CN7000 Packet Taxonomy.ppt to local repo or provide packet type nomenclature from the PPT.

---

### W-06-001: UFH-32 Entropy Field

| Field | Value |
|-------|-------|
| **Status** | Deferred |
| **Priority** | Medium |
| **Category** | Datamodel |
| **Created** | 2026-01-20 |

**Description**: UFH-32 lacks 16-bit entropy field; per-packet ECMP not supported; switch must derive entropy from Src+Dest hash. Note: UFH entropy fields might use the UE Entropy Header (see `ue/transport/pds/entropy_header.ksy`, UE Spec Table 3-31, Section 3.5.10.1).

---

### W-07-003: ue_plus.ksy Length Field Units

| Field | Value |
|-------|-------|
| **Status** | Investigation |
| **Priority** | Low |
| **Category** | Datamodel |
| **Created** | 2026-01-22 |

**Description**: `ue_plus.ksy` Length field units TBD (now 6 bits per W-04-004 restructuring).

---

### W-09-010: UFH Headers UEC Standardization

| Field | Value |
|-------|-------|
| **Status** | Deferred |
| **Priority** | Low |
| **Category** | Datamodel |
| **Created** | 2026-01-26 |

**Description**: Document UFH headers when UEC standardizes them (future, optional).

---

### W-10-007: nscc_destination.ksy Expansion

| Field | Value |
|-------|-------|
| **Status** | Deferred |
| **Priority** | Low |
| **Category** | Datamodel |
| **Created** | 2026-01-27 |

**Description**: Expand `nscc_destination.ksy` stub with NSCC destination algorithm (Section 3.6.13.9).

---

### W-10-008: rccc_source.ksy Expansion

| Field | Value |
|-------|-------|
| **Status** | Deferred |
| **Priority** | Low |
| **Category** | Datamodel |
| **Created** | 2026-01-27 |

**Description**: Expand `rccc_source.ksy` stub with RCCC source algorithm (Sections 3.6.14.2-3.6.14.4).

---

### W-10-009: rccc_destination.ksy Expansion

| Field | Value |
|-------|-------|
| **Status** | Deferred |
| **Priority** | Low |
| **Category** | Datamodel |
| **Created** | 2026-01-27 |

**Description**: Expand `rccc_destination.ksy` stub with RCCC destination algorithm (Sections 3.6.14.5-3.6.14.6).

---

### W-10-010: tfc_source.ksy Expansion

| Field | Value |
|-------|-------|
| **Status** | Deferred |
| **Priority** | Low |
| **Category** | Datamodel |
| **Created** | 2026-01-27 |

**Description**: Expand `tfc_source.ksy` stub with TFC source behavior (Section 3.6.15).

---

### W-10-011: tfc_destination.ksy Expansion

| Field | Value |
|-------|-------|
| **Status** | Deferred |
| **Priority** | Low |
| **Category** | Datamodel |
| **Created** | 2026-01-27 |

**Description**: Expand `tfc_destination.ksy` stub with TFC destination behavior (Section 3.6.15).

---

### W-10-012: multipath_selection.ksy Expansion

| Field | Value |
|-------|-------|
| **Status** | Deferred |
| **Priority** | Low |
| **Category** | Datamodel |
| **Created** | 2026-01-27 |

**Description**: Expand `multipath_selection.ksy` stub with multipath algorithms (Section 3.6.16).

---

### W-10-013: CC_TYPE Proprietary Extensions

| Field | Value |
|-------|-------|
| **Status** | Investigation |
| **Priority** | Medium |
| **Category** | Investigation |
| **Created** | 2026-01-27 |

**Description**: Investigate CC_TYPE (14-15) and CCX_TYPE (14-15) proprietary extensions as Cornelis value-add for congestion management. UE Spec reserves these for vendor-specific CC algorithms.

---

## 3. Datamodel Gaps

| ID | Priority | Description | Target Location | Status |
|----|----------|-------------|-----------------|--------|
| D-001 | High | PMR CSR definitions missing from datamodel | `datamodel/hw/asics/pmr/csrs/*.rdl` | Spec Update |
| D-002 | Medium | PMR block hierarchy YAML incomplete | `datamodel/hw/asics/pmr/blocks.yaml` | Spec Update |
| D-003 | Medium | PMR interface contracts missing | `datamodel/views/contracts/pmr-*.puml` | Spec Update |

---

## 4. Specification Questions

| ID | Priority | Question | Context | Status |
|----|----------|----------|---------|--------|
| Q1 | Medium | Lightweight Interface Scope | What features should be reduced in lightweight mode? | Investigation |

**Note**: Q2-Q4 from original list have been resolved or superseded.

---

## 5. Recently Closed

### W-16: L2 Header Selection Datamodel (2026-02-03)

Added state machines and configuration models to support L2 header selection decisions:
- `ue/link/lldp/protocols/link_negotiation_sm.ksy` - Link capability negotiation state machine
- `cornelis/config/address_vector.ksy` - Per-destination protocol configuration
- `cornelis/protocols/l2_header_selection_sm.ksy` - L2 header selection decision logic
- `cornelis/config/peer_capability.ksy` - Per-peer capability state
- 3 metadata.yaml files for new directories
- **Commit**: `7ab5916f` pushed to origin/main

### W-10-015: nscc_source.ksy In-Depth Review (2026-02-03)

Completed in-depth review of `nscc_source.ksy` against UE Spec 1.0.1 Sections 3.6.13.1-3.6.13.7:
- **Configuration Parameters (Table 3-76)**: 20/20 verified correct
- **State Variables (Table 3-77)**: 16/16 verified correct
- **Algorithm Functions (Section 3.6.13.5)**: 6/6 pseudocode matches spec
- **Internal Functions (Section 3.6.13.6)**: 11/11 pseudocode matches spec
- **Overall Assessment**: PASS - datamodel is accurate and complete
- Minor gap: Section 3.6.13.7 (Probe CP guidance) not documented (informational only)

### W-09-009: PMR L2 Header Selection Rules (2026-02-03)

Documented rules for when PMR uses standard Ethernet vs Cornelis UE+ header:
- **UE+ (12B)**: Both endpoints support UE+, fabric-managed HMAC addressing, link negotiated
- **Ethernet II (14B)**: Peer doesn't support UE+, RoCEv2, standard UE over UDP, Ethernet services
- **Key principle**: HFI supports simultaneous use of all protocols (HFI_ARCH_003)
- **Selection mechanism**: Per-destination via Address Vector (AV) configuration
- Added Section 2 "L2 Header Selection Rules" to `packet_taxonomy_ue_plus_variants.md`
- **Datamodel**: W-16 added supporting state machines and config models
- **Commit**: `7ab5916f` pushed to origin/main

### W-14 Series: UALink Datamodel Expansion (2026-01-29 to 2026-01-30)

Completed comprehensive UALink datamodel expansion:
- W-14-001 through W-14-011: All closed
- Security layer expansion (1660 lines across 5 files)
- Cross-references added to 37 KSY files
- Half-flit and response field expansions
- YAML reference coverage documented

See `analysis/ualink/ualink_issues.md` for full details.

### W-13 Series: Ethernet Metadata and RSS (2026-01-28)

Completed Ethernet datamodel enhancements:
- W-13-001 through W-13-021: All closed
- Added x-related-headers, x-spec, x-packet metadata
- Created IEEE 802.3 frame format support
- Created RSS hash algorithm documentation

### W-12 Series: RoCE Cross-References (2026-01-27 to 2026-01-28)

Completed RoCE datamodel cross-referencing:
- W-12-001 through W-12-018: All closed (W-12-006 cancelled)
- Standardized opcode format across files
- Added missing opcodes to x-related-headers
- Documented PMR transport type support

### W-11 Series: RoCE BTH/AETH Updates (2026-01-27)

Completed RoCE transport header updates:
- W-11-001 through W-11-008: All closed
- Added operation validity matrix
- Fixed AETH syndrome bit layout
- Added x-spec metadata to all files

### W-10-015: nscc_source.ksy In-Depth Review (2026-02-03)

Completed in-depth review of `nscc_source.ksy` against UE Spec 1.0.1 Sections 3.6.13.1-3.6.13.7:
- **Configuration Parameters (Table 3-76)**: 20/20 verified correct
- **State Variables (Table 3-77)**: 16/16 verified correct
- **Algorithm Functions (Section 3.6.13.5)**: 6/6 pseudocode matches spec
- **Internal Functions (Section 3.6.13.6)**: 11/11 pseudocode matches spec
- **Overall Assessment**: PASS - datamodel is accurate and complete
- Minor gap: Section 3.6.13.7 (Probe CP guidance) not documented (informational only)

### W-10 Series: CMS Enumerations (2026-01-27)

Completed CMS enumeration and documentation:
- W-10-001 through W-10-006, W-10-014: All closed
- Created cc_type.ksy and ccx_type.ksy
- Added preprocessing algorithm references
- Expanded nscc_source.ksy

---

## 6. Archive Reference

**Complete work item history is maintained in**: `packet_taxonomy.md` Section 5 (Work List)

This includes:
- Full details of all closed items (Section 5.4)
- Change log with dates (Section 5.5)
- Original issue descriptions and resolutions

**Datamodel update history is maintained in**: `DATAMODEL_UPDATES.md`

This includes:
- Detailed commit information
- Before/after diffs
- Specification references

---

## 7. Status Reports

### 2026-02-03: Full History Status Report

Generated comprehensive status report covering all packet taxonomy work from 2026-01-10 to 2026-02-03.

**Deliverables**:
- `reports/packet_taxonomy/status_report/status_report.yaml` - YAML data file (182 lines)
- `reports/packet_taxonomy/status_report/status_report.pptx` - PowerPoint presentation (22 slides)

**Report Contents**:
- Executive summary with 94% completion rate (83 closed, 5 open, 13 deferred)
- Protocol coverage: 174 KSY files across 5 families (UE 103, UALink 38, Ethernet 12, Cornelis 12, RoCE 9)
- Work item series completion status (W-09 through W-16)
- Open items by priority (2 High, 3 Medium)
- Deferred items summary with reasons
- File modifications (created vs modified)
- Non-protocol file changes
- Next steps and recommendations

**Generation**: `python -m utilities.pptx_helper --type progress --data reports/packet_taxonomy/status_report/status_report.yaml --output reports/packet_taxonomy/status_report/status_report.pptx`
