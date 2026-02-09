# Packet Taxonomy Datamodel Update Plan

**Document**: Plan for adding missing UE packet formats to the datamodel  
**Location**: `analysis/packet_taxonomy/`  
**Created**: 2026-01-23  
**Revised**: 2026-02-03  
**Status**: Revised - W-09-009 Completed

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Key Findings from UE Spec Review](#2-key-findings-from-ue-spec-review)
3. [Revised Gap Analysis](#3-revised-gap-analysis)
4. [Phase 1: Remaining Critical Formats](#4-phase-1-remaining-critical-formats)
5. [Phase 2: Supporting Formats](#5-phase-2-supporting-formats)
6. [Phase 3: Enumerations and References](#6-phase-3-enumerations-and-references)
7. [Work Items](#7-work-items)
8. [Implementation Schedule](#8-implementation-schedule)
9. [Appendix: UE Spec Reference Tables](#9-appendix-ue-spec-reference-tables)

---

## 1. Executive Summary

### Background

During the packet taxonomy documentation effort, a gap analysis identified several UE Specification packet formats that were believed to be missing from the datamodel. After detailed review of the UE Specification v1.0.1, several items were found to NOT require new datamodel files.

### Key Clarifications

| Original Assumption | Actual Finding |
|---------------------|----------------|
| UE defines a custom L2 header | **FALSE** - UE uses standard Ethernet II by default |
| Table 3-1 defines L2 header | **FALSE** - Table 3-1 is "Profile Requirements for Supporting libfabric Transactions" |
| Table 3-4 defines FEP address format | **FALSE** - Table 3-4 is "Profile Summary – SES header formats" |
| FEP has a custom address format | **FALSE** - FEP uses standard IPv4/IPv6 addresses (Fabric Address = FA) |
| Cornelis UE+ is standard UE | **FALSE** - Cornelis UE+ is proprietary value-add |

### Revised Scope

This plan now covers:
- Creation of PDCID format documentation (the one confirmed missing format)
- Updates to existing files (CP payload references)
- Documentation of the relationship between standard UE (Ethernet/IP) and Cornelis UE+ (proprietary)
- Future UFH headers (optional, being developed by UEC)

---

## 2. Key Findings from UE Spec Review

### 2.1 UE L2 Header - NOT A CUSTOM FORMAT

**Finding**: The UE Specification v1.0.1 does NOT define a custom L2 header. UE operates over standard Ethernet.

**Evidence from UE Spec**:
- Section 3.5.10.1: "Native IPv4, native IPv6, and UDP encapsulations are specified"
- The spec defines encapsulation options as:
  - Native IPv4 (Ethernet + IPv4 + UET)
  - Native IPv6 (Ethernet + IPv6 + UET)
  - UDP over IPv4 (Ethernet + IPv4 + UDP + UET)
  - UDP over IPv6 (Ethernet + IPv6 + UDP + UET)
- All use **standard Ethernet II headers** (14 bytes)

**Cornelis UE+ Header**:
- The `cornelis/link/ue_plus.ksy` is a **Cornelis Networks proprietary** 12-byte header
- It is a value-add optimization, NOT part of the UE standard
- PMR may use either standard Ethernet or Cornelis UE+ (rules defined in W-09-009, completed 2026-02-03)

**UFH Headers (Future)**:
- The UEC is currently developing UFH (Unified Forwarding Header) formats
- These are intended as optional alternatives to Ethernet II
- Should be considered optional until standardized

### 2.2 FEP Address Format - USES STANDARD IP

**Finding**: FEP addresses use standard IPv4 or IPv6 addresses. There is no custom FEP address wire format.

**Evidence from UE Spec**:
- Section 1.3: "A fabric address (FA) is either an IPv4 or IPv6 address, and a FEP is a logically addressable entity assigned a single FA"
- The addressing hierarchy is:
  1. **Fabric Address (FA)** = IPv4 or IPv6 address → selects a FEP
  2. **JobID** → identifies the job/application
  3. **PIDonFEP** → identifies the process on the FEP
  4. **Resource Index** → identifies the specific resource

**Libfabric Endpoint Address (Table 2-10)**:
- This is a **software API structure**, not a wire format
- Used by libfabric for endpoint management
- Does not require a `.ksy` datamodel file

### 2.3 PDCID Format - CONFIRMED NEEDED

**Finding**: PDCID (Packet Delivery Context Identifier) format IS defined in the spec and warrants documentation.

**Evidence from UE Spec**:
- Section 3.5.11.5: "Both the initiator and target allocate PDC Identifiers"
- PDCID is 16 bits, carried in `pds.spdcid` and `pds.dpdcid` fields
- During PDC establishment, `pds.dpdcid` is overloaded with `{pds.pdc_info, pds.psn_offset}`
- The `pds.pdc_info` field is 4 bits with specific encoding

---

## 3. Revised Gap Analysis

### Items Removed (Not Needed)

| Original Item | Reason Removed |
|---------------|----------------|
| W-09-001: UET L2 Header | UE uses standard Ethernet II; no custom L2 header defined |
| W-09-002: FEP Address Format | FEP uses standard IPv4/IPv6; no custom format defined |
| W-09-004: UET Network Header | UE uses standard IP headers; no custom network header |

### Items Retained (Still Needed)

| ID | Priority | Description | Status |
|----|----------|-------------|--------|
| W-09-003 | MEDIUM | Document PDCID format and pdc_info encoding | Pending |
| W-09-005 | MEDIUM | Create CP payload formats per Section 3.5.16.8 | Pending |
| W-09-006 | MEDIUM | Update `rud_rod_cp.ksy` with payload field and ACK reference | Pending |
| W-09-007 | LOW | Create `nack_codes.ksy` enumeration per Table 3-59 | Pending |
| W-09-008 | LOW | Create `next_header_types.ksy` enumeration per Table 3-16 | Pending |
| W-09-009 | MEDIUM | Define rules for when PMR uses standard Ethernet vs Cornelis UE+ | **CLOSED** (2026-02-03, commit `7ab5916f` pushed) |

### New Items Added

| ID | Priority | Description | Status |
|----|----------|-------------|--------|
| W-09-010 | LOW | Document UFH headers when UEC standardizes them (future) | Deferred |

---

## 4. Phase 1: Remaining Critical Formats

### 4.1 PDCID Format Documentation

**File**: `datamodel/protocols/ue/transport/pds/pdcid.ksy` (or add to existing PDS files)  
**UE Spec Reference**: Section 3.5.11.5, Section 3.5.8.2  
**Priority**: MEDIUM (downgraded from HIGH - format is simple)

#### Description

PDCID (Packet Delivery Context Identifier) is a 16-bit identifier used in PDS headers. During PDC establishment, the `dpdcid` field is overloaded with additional information.

#### PDCID Encoding

**Normal Operation** (after PDC established):
```
Bits:  15                                              0
      +------------------------------------------------+
      |                  PDCID (16 bits)               |
      +------------------------------------------------+
```

**During PDC Establishment** (`pds.flags.syn` = 1):
```
Bits:  15       12 11                                  0
      +----------+-------------------------------------+
      | pdc_info |          psn_offset (12 bits)      |
      |  (4 bits)|                                     |
      +----------+-------------------------------------+
```

#### pdc_info Field Encoding (4 bits)

| Bit | Name | Description |
|-----|------|-------------|
| 3 | mode | 0 = RUD, 1 = ROD |
| 2 | reserved | Reserved, must be 0 |
| 1:0 | tc | Traffic class (0-3) |

#### Implementation Notes

- PDCID = 0 is reserved and MUST NOT be used
- PDCIDs are locally unique at the FEP level
- {ip.src_addr, PDCID} must be globally unique
- Consider adding this as documentation to existing `rud_rod_request.ksy` rather than separate file

---

## 5. Phase 2: Supporting Formats

### 5.1 Control Packet Payload Formats

**Directory**: `datamodel/protocols/ue/transport/pds/cp_payloads/`  
**UE Spec Reference**: Section 3.5.16.8  
**Priority**: MEDIUM

#### Files to Create

| File | CP Subtype | UE Spec Reference |
|------|------------|-------------------|
| `probe_cp_payload.ksy` | Probe | Section 3.5.16.8.1 |
| `ack_request_cp_payload.ksy` | ACK Request | Section 3.5.16.8.2 |
| `close_cp_payload.ksy` | Close | Section 3.5.16.8.3 |
| `resync_cp_payload.ksy` | Resync | Section 3.5.16.8.4 |

#### Implementation Notes

- `credit_cp_payload.ksy` already exists (Table 3-64)
- `credit_request_cp_payload.ksy` already exists (Table 3-65)

### 5.2 Update rud_rod_cp.ksy

**File**: `datamodel/protocols/ue/transport/pds/rud_rod_cp.ksy`  
**Priority**: MEDIUM

#### Changes Required

1. Add `payload` field with reference to Section 3.5.16.8
2. Add note that spdcid/dpdcid are "Same as ACK" per UE Spec
3. Add cross-references to CP payload format files

---

## 6. Phase 3: Enumerations and References

### 6.1 NACK Codes Enumeration

**File**: `datamodel/protocols/ue/transport/pds/nack_codes.ksy`  
**UE Spec Reference**: Table 3-59, Section 3.5.12.7  
**Priority**: LOW

### 6.2 Next Header Types Enumeration

**File**: `datamodel/protocols/ue/transport/ses/next_header_types.ksy`  
**UE Spec Reference**: Table 3-16, Section 3.4.2.6  
**Priority**: LOW

---

## 7. Work Items

### Revised Work Items for packet_taxonomy.md

| ID | Priority | Category | Description | Status |
|----|----------|----------|-------------|--------|
| W-09-001 | - | Datamodel | ~~Create UET L2 header~~ | **CLOSED - Not Needed** (UE uses standard Ethernet) |
| W-09-002 | - | Datamodel | ~~Create FEP address format~~ | **CLOSED - Not Needed** (FEP uses standard IPv4/IPv6) |
| W-09-003 | MEDIUM | Datamodel | Document PDCID format and pdc_info encoding per Section 3.5.11.5 | Pending |
| W-09-004 | - | Datamodel | ~~Create UET network header~~ | **CLOSED - Not Needed** (UE uses standard IP) |
| W-09-005 | MEDIUM | Datamodel | Create CP payload formats per Section 3.5.16.8 | Pending |
| W-09-006 | MEDIUM | Datamodel | Update `rud_rod_cp.ksy` with payload field and ACK reference | Pending |
| W-09-007 | LOW | Datamodel | Create `nack_codes.ksy` enumeration per Table 3-59 | Pending |
| W-09-008 | LOW | Datamodel | Create `next_header_types.ksy` enumeration per Table 3-16 | Pending |
| W-09-009 | MEDIUM | Architecture | Define rules for when PMR uses standard Ethernet vs Cornelis UE+ | **CLOSED** (2026-02-03) |
| W-09-010 | LOW | Datamodel | Document UFH headers when UEC standardizes them | Deferred |

### Relationship to Existing Work Items

| Existing ID | Relationship |
|-------------|--------------|
| W-04-004 | Related - LID size in ue_plus.ksy (Cornelis proprietary, not UE standard) |
| W-07-003 | Related - ue_plus.ksy length field encoding (Cornelis proprietary) |

---

## 8. Implementation Schedule

### Revised Order

| Order | Work Item | Estimated Effort | Dependencies |
|-------|-----------|------------------|--------------|
| 1 | W-09-006 (Update rud_rod_cp.ksy) | 1 hour | None |
| 2 | W-09-003 (PDCID documentation) | 1 hour | None |
| 3 | W-09-005 (CP Payloads) | 2-3 hours | Section 3.5.16.8 |
| 4 | W-09-007 (NACK Codes) | 1 hour | Table 3-59 |
| 5 | W-09-008 (Next Header Types) | 1 hour | Table 3-16 |
| 6 | W-09-009 (L2 Selection Rules) | **COMPLETED** | Commit `7ab5916f` pushed to origin/main |

### Revised Total Estimated Effort

- Phase 1 (PDCID): 1 hour
- Phase 2 (CP Payloads, rud_rod_cp update): 3-4 hours
- Phase 3 (Enumerations): 2 hours
- **Total**: 6-7 hours (reduced from 11-17 hours)

---

## 9. Appendix: UE Spec Reference Tables

### Corrected Table References

| Table | Actual Title | Section | Used For |
|-------|--------------|---------|----------|
| Table 3-1 | Profile Requirements for Supporting libfabric Transactions | 3.3.1 | Profile compliance |
| Table 3-4 | Profile Summary – SES header formats | 3.3.5 | SES header requirements |
| Table 3-16 | Next Header Enumeration | 3.4.2.6 | next_header_types.ksy |
| Table 3-38 | CP Subtypes | 3.5.10.8 | rud_rod_cp.ksy |
| Table 3-59 | NACK Codes | 3.5.12.7 | nack_codes.ksy |
| Table 3-64 | Credit CP Payload | 3.5.16.6.1 | (exists) |
| Table 3-65 | Credit Request CP | 3.5.16.6.2 | (exists) |

### Key Sections for PDCID

| Section | Title | Content |
|---------|-------|---------|
| 3.5.8 | Packet Delivery Contexts (PDC) | PDC overview |
| 3.5.8.2 | PDC Establishment | PDCID allocation and syn flag |
| 3.5.11.5 | PDC Identifiers | PDCID format and pdc_info encoding |

---

## Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-01-23 | Claude AI | Initial draft |
| 2026-01-26 | Claude AI | Major revision after UE Spec review: Closed W-09-001, W-09-002, W-09-004 as not needed; UE uses standard Ethernet/IP, not custom headers; Cornelis UE+ is proprietary value-add |
| 2026-02-03 | Claude AI | Closed W-09-009: L2 header selection rules documented in `packet_taxonomy_ue_plus_variants.md` Section 2; datamodel support added via W-16 (link_negotiation_sm.ksy, address_vector.ksy, l2_header_selection_sm.ksy, peer_capability.ksy); commit `7ab5916f` pushed to origin/main |

---

## Approval

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Author | Claude AI | 2026-01-26 | - |
| Reviewer | matkins | | |
| Approver | | | |
