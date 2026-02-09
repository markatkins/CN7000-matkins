# Packet Taxonomy Datamodel Updates
**Last Updated**: 2026-02-03

**Document**: History of datamodel updates made during packet taxonomy documentation  
**Location**: `analysis/packet_taxonomy/`  
**Repository**: `earlysim` (datamodel files in `datamodel/protocols/`)  
**Maintainers**: matkins, Claude AI assistant

---

## Table of Contents

1. [Overview](#1-overview)
2. [Update History](#2-update-history)
3. [Pending Updates](#3-pending-updates)

---

## 1. Overview

This document tracks all updates made to the `earlysim` datamodel `.ksy` files as a result of the packet taxonomy documentation effort. Updates are made when discrepancies are found between the datamodel and the authoritative specifications (UE Spec, HAS, etc.).

### Update Categories

| Category | Description |
|----------|-------------|
| **Fix** | Corrects an error in the datamodel (wrong field size, type, etc.) |
| **Enhancement** | Adds missing fields, documentation, or metadata |
| **Restructure** | Changes the overall structure of a format |

---

## 2. Update History

### 2.1 UFH-16 Restructuring (2026-01-20)

| Field | Value |
|-------|-------|
| **File** | `datamodel/protocols/cornelis/network/ufh_16.ksy` |
| **Work Item** | W-04-005 |
| **Category** | Restructure |
| **Author** | matkins |
| **Commit** | (part of matkins-packet-tax branch, merged in PR #18) |

**Issue**: Datamodel showed 12-bit destination address, should be 16-bit per HAS.

**Resolution**: UFH-16 restructured to 12-byte Ethernet MAC overlay format:
- 16-bit destination address (bytes 4-5)
- 16-bit source address (bytes 10-11)
- Added SLAP field constraints (Z,Y,X=001)

---

### 2.2 UFH-32 Restructuring (2026-01-20)

| Field | Value |
|-------|-------|
| **File** | `datamodel/protocols/cornelis/network/ufh_32.ksy` |
| **Work Item** | W-04-006 |
| **Category** | Restructure |
| **Author** | matkins |
| **Commit** | (part of matkins-packet-tax branch, merged in PR #18) |

**Issue**: Datamodel showed 16-bit destination address, should be 32-bit per HAS.

**Resolution**: UFH-32 restructured to 12-byte Ethernet MAC overlay format:
- 32-bit destination address (bytes 2-5)
- 32-bit source address (bytes 8-11)
- Added SLAP field constraints (Z,Y,X=001)

---

### 2.2a UFH Header Reorganization (2026-02-02)

| Field | Value |
|-------|-------|
| **Files** | `datamodel/protocols/ue/network/ufh_16.ksy`, `datamodel/protocols/ue/network/ufh_32.ksy` (new UE standard), `datamodel/protocols/cornelis/network/ufh_16_plus.ksy`, `datamodel/protocols/cornelis/network/ufh_32_plus.ksy` (renamed Cornelis) |
| **Work Item** | W-15-001 |
| **Category** | Restructure |
| **Author** | Claude AI (edit), matkins (commit/push) |
| **Commits** | `d5cfb7e2` - "feat(datamodel): add UE standard UFH-16 and UFH-32 headers", `1d4e0ce4` - "refactor(datamodel): rename Cornelis UFH headers to _plus suffix", `c78222d8` - "docs(datamodel): update UFH references for UE/Cornelis separation" |

**Issue**: UFH headers in `cornelis/network/` represented UE standard versions but were labeled as Cornelis proprietary.

**Resolution**: Separated UE standard from Cornelis proprietary versions:
- Created `ue/network/ufh_16.ksy` and `ufh_32.ksy` as UE standard versions (provenance updated to "Ultra Ethernet standard")
- Renamed `cornelis/network/ufh_16.ksy` → `ufh_16_plus.ksy` and `ufh_32.ksy` → `ufh_32_plus.ksy`
- Updated `meta.id` fields to `ufh_16_plus` and `ufh_32_plus`
- Updated `x-spec.section` to "UFH-16+ Cornelis Extension Header" and "UFH-32+ Cornelis Extension Header"
- Updated all references in metadata.yaml, README.md, and documentation files

---

### 2.3 ACK_CC ack_cc_state Field Size (2026-01-23)

| Field | Value |
|-------|-------|
| **File** | `datamodel/protocols/ue/transport/pds/ack_cc.ksy` |
| **Work Item** | W-07-001 |
| **Category** | Fix |
| **Author** | Claude AI (edit), matkins (commit/push) |
| **Commit** | `114b7cbd` - "fix(datamodel): correct ack_cc_state to 64-bit per UE Spec Table 3-36" |

**Issue**: `ack_cc_state` field was defined as 32-bit (`u4`) but UE Spec Table 3-36 specifies 64-bit (8 bytes).

**Resolution**: 
- Changed `ack_cc_state` from `type: u4` to `type: u8`
- Updated total header size from 28 bytes to 32 bytes
- Updated all size references and wire format documentation in the file
- Updated `packet_taxonomy_ue_pds.md` and `packet_taxonomy.md` to reflect correct size

**Diff Summary**:
```diff
-  size_bytes: 28
-  size_bits: 224
+  size_bytes: 32
+  size_bits: 256

-  # Byte 24-27: ACK CC State (32 bits)
+  # Byte 24-31: ACK CC State (64 bits)
   - id: ack_cc_state
-    type: u4
+    type: u8
```

---

### 2.4 RUD/ROD Request PDCID Documentation (2026-01-26)

| Field | Value |
|-------|-------|
| **File** | `datamodel/protocols/ue/transport/pds/rud_rod_request.ksy` |
| **Work Item** | W-09-003 |
| **Category** | Enhancement |
| **Author** | Claude AI (edit), matkins (commit/push) |
| **Commit** | `319c0565` - "docs(datamodel): add PDCID format and pdc_info encoding documentation" |

**Issue**: PDCID format and pdc_info encoding were not fully documented in the datamodel.

**Resolution**: 
- Added comprehensive PDCID constraints per Section 3.5.11.5:
  - PDCID = 0 is reserved and MUST NOT be used
  - PDCIDs are locally unique at FEP level
  - {ip.src_addr, PDCID} MUST be globally unique
  - Same PDCID MAY be reused for different destination FEPs
  - Same PDCID MUST NOT be used simultaneously to same dest FEP
- Added pdc_info encoding per Table 3-33:
  - Bit 0: `use_rsv_pdc` (1=reserved pool, 0=shared pool)
  - Bits 3:1: reserved (must be 0)
- Added psn_offset description for PDC establishment
- Added `x-pdc-info-encoding` metadata for tooling
- Updated `packet_taxonomy_ue_pds.md` with correct encoding

**Note**: Initial documentation incorrectly showed pdc_info as containing mode and traffic class fields. This was corrected to match UE Spec Table 3-33 which only defines bit 0 as `use_rsv_pdc` with bits 3:1 reserved.

---

### 2.5 RUD/ROD CP Payload Field (2026-01-26)

| Field | Value |
|-------|-------|
| **File** | `datamodel/protocols/ue/transport/pds/rud_rod_cp.ksy` |
| **Work Item** | W-09-005, W-09-006 |
| **Category** | Enhancement |
| **Author** | Claude AI (edit), matkins (commit) |
| **Commit** | `3cc80cc4` - "docs(datamodel): add CP payload field and references to rud_rod_cp.ksy" |

**Issue**: Control Packet payload field was not documented, and spdcid/dpdcid "Same as ACK" note was missing.

**Resolution**: 
- Added `payload` field with complete CP type table per Table 3-66:
  - NOOP: no payload
  - ACK Request: message_id (32 bits) or 0x0
  - Clear Command/Request: PSN values (32 bits)
  - Close Command/Request: no payload
  - Probe: SACK bitmap base PSN (32 bits)
  - Credit: credit_cp_payload (32 bits)
  - Credit Request: credit_request_cp_payload (32 bits)
  - Negotiation: reserved (256 bits)
- Added `x-payload-by-type` metadata for code generation tooling
- Added note that spdcid/dpdcid are "Same as ACK" per Table 3-38
- Corrected path references to `ue/transport/cms/credit_cp_payload.ksy` and `ue/transport/cms/credit_request_cp_payload.ksy`
- Updated header to show variable total size (12 bytes header + 0-32 bytes payload)

**Note**: W-09-005 (CP payload formats) was closed because existing `credit_cp_payload.ksy` and `credit_request_cp_payload.ksy` files are sufficient for the complex payloads; other CP payloads are simple 32-bit values adequately documented inline.

---

### 2.6 PDS NACK Codes Enumeration (2026-01-26)

| Field | Value |
|-------|-------|
| **File** | `datamodel/protocols/ue/transport/pds/nack_codes.ksy` |
| **Work Item** | W-09-007 |
| **Category** | Enhancement |
| **Author** | Claude AI (create), matkins (commit/push) |
| **Commit** | `af256ea7` - "feat(datamodel): add NACK codes and next header type enumerations" |

**Issue**: NACK codes enumeration was not available in the datamodel for code generation and validation.

**Resolution**: 
- Created new `nack_codes.ksy` file with complete NACK code enumeration per Table 3-59
- Documented all NACK codes (0x01-0x1A, 0xFD-0xFF) with:
  - Mnemonic identifiers (e.g., `uet_trimmed`, `uet_no_pdc_avail`)
  - Error types: NORMAL, PDC_ERR, PDC_FATAL
  - Source actions: RETX (retransmit), RETRY (new PDC), FAIL (report error)
  - Section references for each code
- Added `nack_error_type` and `nack_source_action` helper enumerations
- Added `x-spec` and `x-packet` metadata for tooling
- Noted reserved ranges (0x0C, 0x1B-0xFC)

---

### 2.7 SES Next Header Types Enumeration (2026-01-26)

| Field | Value |
|-------|-------|
| **File** | `datamodel/protocols/ue/transport/ses/next_header_types.ksy` |
| **Work Item** | W-09-008 |
| **Category** | Enhancement |
| **Author** | Claude AI (create), matkins (commit/push) |
| **Commit** | `af256ea7` - "feat(datamodel): add NACK codes and next header type enumerations" |

**Issue**: Next header type enumeration was not available in the datamodel for SES header parsing.

**Resolution**: 
- Created new `next_header_types.ksy` file with complete next_hdr enumeration per Table 3-16
- Documented all next_hdr values (0x0-0x6 defined, 0x7-0xF reserved):
  - 0x0: UET_HDR_NONE - No header follows
  - 0x1: UET_HDR_REQUEST_SMALL - Small request (Figure 3-13)
  - 0x2: UET_HDR_REQUEST_MEDIUM - Medium request (Figure 3-14)
  - 0x3: UET_HDR_REQUEST_STD - Standard request (Figures 3-9 to 3-12)
  - 0x4: UET_HDR_RESPONSE - Response (Figure 3-18)
  - 0x5: UET_HDR_RESPONSE_DATA - Response with data (Figure 3-19)
  - 0x6: UET_HDR_RESPONSE_DATA_SMALL - Small response with data (Figure 3-20)
- Added `-x-figure` and `-x-ksy-file` metadata for cross-referencing
- Added `x-spec` and `x-packet` metadata for tooling

---

### 2.8 UE+ Header Restructuring (2026-01-26)

| Field | Value |
|-------|-------|
| **File** | `datamodel/protocols/cornelis/link/ue_plus.ksy` |
| **Work Item** | W-04-004 |
| **Category** | Restructure |
| **Author** | Claude AI (rewrite), matkins (commit/push) |
| **Commit** | `63a59be6` - "fix(datamodel): restructure UE+ header with correct 24-bit HMAC addressing" |

**Issue**: UE+ header had incorrect field layout:
- LID fields were 16-bit, should be 24-bit (DLID/DMAC, SLID/SMAC)
- Length field was 9-bit split, should be 6-bit
- Version field was 1-bit, should be 2-bit
- RC field was 4-bit, should be 3-bit split across bytes 1-2
- Hop count was 8-bit, should be 3-bit
- Type/EtherType field (16-bit) should not be in UE+ header
- Missing reserved byte (byte 8)

**Resolution**: Complete rewrite of `ue_plus.ksy` with correct layout:

| Byte | Fields | Bits |
|------|--------|------|
| 0 | L2[7:6], V[5:4], zyxm[3:0] | 2+2+4 |
| 1 | Length[7:2], RC[1:0] (RC bits 2:1) | 6+2 |
| 2 | RC[7] (RC bit 0), SC[6:3], Hop[2:0] | 1+4+3 |
| 3-5 | DLID/DMAC (24-bit Hierarchical MAC) | 24 |
| 6-7 | Entropy | 16 |
| 8 | Reserved | 8 |
| 9-11 | SLID/SMAC (24-bit Hierarchical MAC) | 24 |

**Additional changes**:
- Added terminology mapping (OPA → Cornelis): DLID→DMAC, SLID→SMAC, LID→HMAC
- Added HMAC sub-structure documentation for 3 topology configurations:
  - No subdivision (12/6/6): Group/Switch/Terminal
  - x2 NIC subdivision (11/6/7)
  - x8 NIC subdivision (9/6/9)
- Added note that 5-bit PDS-compatible next header follows UE+ header (not part of it)
- Added `x-hmac-formats` metadata for topology configurations
- Updated HAS `04-addressing.md` and `05-packet-formats.md` to match

**Related**: W-07-003 (9-bit length encoding) is now superseded by this change; the Length field is now 6 bits (units TBD).

---

### 2.9 MTU Values Update (2026-01-26)

| Field | Value |
|-------|-------|
| **Files** | Multiple HAS and datamodel files |
| **Work Item** | W-05-002 |
| **Category** | Fix |
| **Author** | Claude AI (edit), matkins (commit/push) |
| **Commit** | `7b9c1a72` - "docs(mtu): update MTU values to correct hardware and protocol limits" |

**Issue**: MTU values in documentation and datamodel were incorrect:
- Hardware max was documented as 9216 bytes, should be 10240 bytes
- UE+ typical was 4096 bytes, should be 8192 bytes
- RoCEv2 max was 9000 bytes, should be 4096 bytes
- Missing distinction between UE Payload MTU and UE+ packet size
- Missing RoCEv2 MTU derivation rules

**Resolution**: 

Updated HAS documentation:
- `05-packet-formats.md` Section 5.9.1: Complete rewrite with correct MTU values, UE Payload MTU table (per UE Spec Section 3.4.1.11), UE+ vs UE Payload MTU distinction, header overhead relationship, RoCEv2 MTU derivation rules
- `03-architecture.md`: Updated Max MTU from 9216 to 10240 bytes

Updated datamodel files (9216 → 10240):
- `hw/asics/pmr/interfaces/ethernet/eth_tx_wqe.ksy`
- `hw/ip/cornelis/ec/descriptors.ksy`
- `hw/asics/pmr/interfaces/pcie/descriptors.ksy`

**Key values**:
- Hardware maximum: 10240 bytes
- UE+ typical payload: 8192 bytes (Cornelis software limit)
- UE Payload MTU (per UE Spec): 1024, 2048, 4096 (required), 8192 bytes
- RoCEv2 maximum: 4096 bytes (IB spec limit)
- Standard Ethernet: 1500 bytes
- Jumbo Ethernet: 9000 bytes

---

## 3. Pending Updates

The following datamodel issues have been identified but not yet resolved:

| Work Item | File | Issue | Priority |
|-----------|------|-------|----------|
| W-07-003 | `ue_plus.ksy` | Length field units TBD (now 6 bits per W-04-004) | Low |
| W-08-001 | `collective_l2.ksy` | Marked as WIP (spec_version 0.1); specification incomplete | Low |
| W-08-002 | `scaleup_l2.ksy` | Marked as WIP (spec_version 0.1); specification incomplete | Low |

---

## 4. Update Process

When making datamodel updates:

1. **Identify discrepancy** - Compare datamodel against authoritative spec
2. **Create work item** - Add to `packet_taxonomy.md` Work List (W-XX-XXX)
3. **Make edit** - Update the `.ksy` file with correct values
4. **Update documentation** - Update relevant `packet_taxonomy_*.md` files
5. **Commit** - Use conventional commit format: `fix(datamodel): description`
6. **Record here** - Add entry to this document with commit hash
7. **Close work item** - Move from Open Issues to Closed Issues in `packet_taxonomy.md`

### Commit Message Format

```
fix(datamodel): brief description

Detailed explanation of what was wrong and what was fixed.
Reference to specification (e.g., "per UE Spec Table 3-36").

Closes W-XX-XXX.
```

### 2.10 CMS Enumerations and Expansions (2026-01-27)

| Field | Value |
|-------|-------|
| **Work Items** | W-10-001 through W-10-006, W-10-014 |
| **Category** | Enhancement |
| **Author** | Claude AI (edit), matkins (commit/push) |

**Changes**:
- Created `ue/transport/cms/cc_type.ksy` - CC_TYPE enumeration per Table 3-48 (CC_NSCC=0, CC_CREDIT=1, reserved 2-13, proprietary 14-15)
- Created `ue/transport/cms/ccx_type.ksy` - CCX_TYPE enumeration per Table 3-49 (all reserved)
- Added preprocessing algorithm references to CMS .ksy files (Sections 3.6.10.3, 3.6.10.4)
- Added Credit CP protocol constraints to `credit_cp_payload.ksy` (pds.psn=0x0, pds.flags.ar=0)
- Added API function references to `ccc_state_machine.ksy` (Section 3.6.8.1)
- Expanded `nscc_source.ksy` stub with NSCC source algorithm (Sections 3.6.13.3-3.6.13.6, Table 3-76)
- Fixed `ack_cc_state_rccc_tfc.ksy` to 8 bytes (64 bits) with 24-bit reserved field

---

### 2.11 RoCE BTH/AETH Updates (2026-01-27)

| Field | Value |
|-------|-------|
| **Work Items** | W-11-001 through W-11-008 |
| **Category** | Enhancement |
| **Author** | Claude AI (edit), matkins (commit/push) |

**Changes**:
- Updated `bth.ksy` `is_atomic` docs with operation codes 0x12-0x14 and transport type restrictions
- Added `is_ack` (0x11) and `is_atomic_ack` (0x12) instances to `bth.ksy`
- Added CNP (4, 0x80) and XRC (5, 0xA0) transport types to `bth.ksy` enum
- Documented FECN (bit 7) and BECN (bit 6) in `bth.ksy` reserved field with ICRC masking note
- Added operation validity matrix by transport type to `bth.ksy` (IB Spec Table 38)
- Fixed `aeth.ksy` syndrome bit layout per IB Spec v1.4 (bit 7 reserved, bits [6:5]=ACK type, bits [4:0]=value)
- Added `x-related-headers` cross-references to all 9 RoCE files
- Added `x-spec` and `x-packet` metadata to all RoCE transport files

---

### 2.12 RoCE Cross-References (2026-01-27 to 2026-01-28)

| Field | Value |
|-------|-------|
| **Work Items** | W-12-001 through W-12-018 |
| **Category** | Enhancement |
| **Author** | Claude AI (edit), matkins (commit/push) |

**Changes**:
- Standardized opcode format across files (hex vs decimal)
- Added missing opcodes to x-related-headers in aeth.ksy, immdt.ksy, atomiceth.ksy, atomicacketh.ksy, deth.ksy
- Documented PMR transport type support: CNP=Yes (ECN), XRC=No (no shared receive queues)
- Clarified extended atomics (MASKED_CMP_SWAP, MASKED_FETCH_ADD) implemented over UE/UE+ not RoCE
- Added ICRC masking details per Annex A17
- Updated roce/README.md with protocols/ directory and transport type support

---

### 2.13 Ethernet Metadata and RSS (2026-01-28)

| Field | Value |
|-------|-------|
| **Work Items** | W-13-001 through W-13-021 |
| **Category** | Enhancement |
| **Author** | Claude AI (edit/create), matkins (commit/push) |

**Changes**:
- Added x-related-headers, x-spec, x-packet metadata to all 6 Ethernet .ksy files
- Created `ethernet_802_3.ksy`, `llc.ksy`, `snap.ksy` for IEEE 802.3 frame format support
- Created RSS hash algorithm documentation: `rss/hash_algorithm.ksy`, `rss/toeplitz_key.ksy`, `rss/hash_input.ksy`, `rss/README.md`
- Updated ipv4.ksy and ipv6.ksy with RSS cross-references
- Added dst_addr_hash instance to ipv6.ksy for RSS hash symmetry
- Added reserved bits extraction to tcp.ksy
- Updated ethernet/README.md with complete file list

---

### 2.14 UALink Expansion (2026-01-29 to 2026-01-30)

| Field | Value |
|-------|-------|
| **Work Items** | W-14-001 through W-14-011 |
| **Category** | Enhancement |
| **Author** | Claude AI (edit/create), matkins (commit/push) |

**Changes**:
- Fixed `dl_flit.yaml` segment sizes to match authoritative `dl_flit.ksy`
- Updated `metadata.yaml` packet count from 35 to 38
- Added `ksy_file` cross-references to all YAML reference files
- Expanded security layer files (1660 lines across 5 files):
  - `encryption.ksy` (Tables 9-4 through 9-7)
  - `authentication.ksy` (Tables 9-8 through 9-12)
  - `iv_format.ksy` (Table 9-3)
  - `key_derivation.ksy` (Figure 9-8)
  - `key_rotation.ksy` (Figures 9-9, 9-11, 9-12)
- Added `x-related-headers` cross-references to 37 KSY files across all 5 layers
- Expanded `data_half_flit.ksy` (40→142 lines) and `message_half_flit.ksy` (37→148 lines)
- Expanded `response_field.ksy` (52→310 lines) with full bit-level parsing
- Expanded `flit_header.ksy` (90→165 lines) with header type discrimination
- Documented YAML reference coverage criteria in README.md

See `analysis/ualink/ualink_issues.md` for detailed issue tracking.
