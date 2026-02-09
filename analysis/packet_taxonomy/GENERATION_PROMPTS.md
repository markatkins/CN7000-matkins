# Packet Taxonomy Documentation Generation Prompts

**Document**: Record of prompts used to generate the PMR Packet Taxonomy documentation  
**Location**: `analysis/packet_taxonomy/`  
**Generated**: 2026-01-14 through 2026-01-23  
**Sessions**: Multiple Claude sessions over ~10 days

---

## Table of Contents

1. [Overview](#1-overview)
2. [Phase 1: Initial Creation](#2-phase-1-initial-creation)
3. [Phase 2: Document Restructuring](#3-phase-2-document-restructuring)
4. [Phase 3: Gap Closure](#4-phase-3-gap-closure)
5. [Continuation Prompts](#5-continuation-prompts)

---

## 1. Overview

The packet taxonomy documentation was created iteratively across multiple sessions. The work progressed through three main phases:

| Phase | Date | Focus | Output |
|-------|------|-------|--------|
| Phase 1 | 2026-01-14 to 2026-01-22 | Initial creation, PDS/SES expansion | Monolithic `packet_taxonomy.md` |
| Phase 2 | 2026-01-23 | Document restructuring | 9 sub-documents |
| Phase 3 | 2026-01-23 | Gap closure | 27 additional formats documented |

---

## 2. Phase 1: Initial Creation

### 2.1 Initial Document Creation (2026-01-14)

**Prompt**:
```
Create a packet taxonomy document for the PMR NIC ASIC that catalogs all packet 
formats from the datamodel directory. Include:
- Protocol stack overview
- Format summary tables
- Wire diagrams for each format
- Field definitions with bit positions
- Cross-references to datamodel .ksy files
```

**Result**: Initial `packet_taxonomy.md` with overview, protocol stack, and basic format tables.

### 2.2 PDS Format Expansion (2026-01-22)

**Prompt**:
```
Expand the PDS packet formats in packet_taxonomy.md with detailed documentation 
for each format type. For each format include:
- Wire diagram showing byte layout
- Field table with bits, offset, description, constraints
- Protocol behavior section
- Cross-references to related formats
- UE Spec references (table, section, page)

Start with RUD Request (Type 0x01) and work through all PDS types.
```

**Result**: Detailed documentation for 11 PDS formats (RUD, ROD, RUDI, UUD, ACK, ACK_CC, ACK_CCX, NACK, NACK_CCX, Control Packet).

### 2.3 SES Format Expansion (2026-01-22)

**Prompt**:
```
Continue expanding packet_taxonomy.md with SES (Semantic Sublayer) formats.
Document each SES header type with the same level of detail as PDS:
- Wire diagrams
- Field tables
- Protocol behavior
- Request/response relationships

Include Standard Request SOM=1/SOM=0, Response, Response with Data, 
Small Message, Rendezvous Extension, and Atomic Extension.
```

**Result**: Detailed documentation for 7 SES formats with request/response relationship diagrams.

---

## 3. Phase 2: Document Restructuring

### 3.1 Document Split Planning (2026-01-23)

**Prompt**:
```
The packet_taxonomy.md document has grown to 1887 lines and is becoming unwieldy.
Split it into multiple sub-documents organized by protocol layer:

1. packet_taxonomy_ue_pds.md - PDS formats
2. packet_taxonomy_ue_ses.md - SES formats  
3. packet_taxonomy_ue_cms_tss.md - CMS and TSS formats
4. packet_taxonomy_ue_link.md - Link Layer (LLR, CBFC, LLDP)
5. packet_taxonomy_rocev2.md - RoCEv2 formats
6. packet_taxonomy_cornelis.md - Cornelis proprietary (UFH, CSIG+, VxLAN+)
7. packet_taxonomy_hsi.md - Host-Software Interface
8. packet_taxonomy_ualink.md - UALink reference

Convert the master document to an index with quick reference tables.
```

**Result**: 9 sub-documents created, master document converted to index.

### 3.2 Sub-Document Creation

**Prompt for each sub-document**:
```
Create packet_taxonomy_[layer].md with:
- Parent document reference
- Scope statement
- Datamodel directory reference
- Table of contents
- Overview section
- Detailed format sections (wire diagrams, field tables, protocol behavior)
- Cross-references section
- References section

Follow the same format as the existing expanded PDS/SES documentation.
```

### 3.3 Link Layer Documentation (2026-01-23)

**Prompt**:
```
Create packet_taxonomy_ue_link.md with LLR and CBFC formats from:
- earlysim/datamodel/protocols/ue/link/llr/*.ksy
- earlysim/datamodel/protocols/ue/link/cbfc/*.ksy
- earlysim/datamodel/protocols/ue/link/lldp/*.ksy

Document LLR_ACK, LLR_NACK, LLR_INIT, LLR_INIT_ECHO, LLR Preambles,
CF_Update, CC_Update, and LLDP TLVs.
```

**Result**: Complete Link Layer documentation with 10 formats.

---

## 4. Phase 3: Gap Closure

### 4.1 Gap Analysis (2026-01-23)

**Prompt**:
```
Verify that all packet formats have been expanded and documented in the same 
manner. If not, determine the remaining.
```

**Result**: Gap analysis identifying 27 undocumented formats across 9 categories.

### 4.2 Phase 3 Implementation (2026-01-23)

**Prompt**:
```
Please proceed with Phase 3 implementation to document the remaining gaps.
```

**Result**: Documentation of all 27 missing formats:

**PDS Formats** (added to `packet_taxonomy_ue_pds.md`):
- entropy_header (4 bytes)
- rud_rod_default_ses (8 bytes)
- rud_rod_request_cc (28 bytes)

**SES Formats** (added to `packet_taxonomy_ue_ses.md`):
- cas_extension (40 bytes)
- deferrable_send_request (44 bytes)
- optimized_non_matching (32 bytes)
- optimized_response_with_data (16 bytes)
- ready_to_restart (44 bytes)
- small_rma (32 bytes)

**UE Network/Physical** (added to `packet_taxonomy_ue_link.md`):
- dscp_categories
- packet_trimming
- control_ordered_sets

**RoCEv2** (added to `packet_taxonomy_rocev2.md`):
- atomicacketh (8 bytes)
- deth (8 bytes)
- immdt (4 bytes)
- icrc (4 bytes)

**Cornelis** (added to `packet_taxonomy_cornelis.md`):
- cornelis_l2_prefix (1 byte)
- pkey (2 bytes)

**Standard Ethernet** (new `packet_taxonomy_ethernet.md`):
- ethernet_ii (14 bytes)
- vlan_802_1q (4 bytes)
- ipv4 (20+ bytes)
- ipv6 (40 bytes)
- tcp (20+ bytes)
- udp (8 bytes)

**HSI** (added to `packet_taxonomy_hsi.md`):
- notification_entry (64 bytes)
- qw_violation_event (64 bytes)
- pcie/descriptors (64 bytes)

---

## 5. Continuation Prompts

### 5.1 Session Continuation

When continuing work across sessions, the following prompt was used:

**Prompt**:
```
Continue Phase 2 of the PMR Packet Taxonomy documentation project.

Working directory: /home/matkins/CN7000/analysis/

Completed sub-documents:
- packet_taxonomy_ue_pds.md
- packet_taxonomy_ue_ses.md
- packet_taxonomy_cornelis.md
- packet_taxonomy_rocev2.md
- packet_taxonomy_hsi.md
- packet_taxonomy_ualink.md
- packet_taxonomy_ue_cms_tss.md

Remaining tasks:
1. Create packet_taxonomy_ue_link.md with LLR and CBFC formats from:
   - earlysim/datamodel/protocols/ue/link/llr/*.ksy
   - earlysim/datamodel/protocols/ue/link/cbfc/*.ksy
   - earlysim/datamodel/protocols/ue/link/lldp/*.ksy

2. Refactor packet_taxonomy.md into a master index document with:
   - Overview and protocol stack summary
   - Document index table linking to all sub-documents
   - Consolidated Work List (add W-08-001 for collective_l2.ksy WIP, W-08-002 for scaleup_l2.ksy WIP)
   - Consolidated Change Log with entry for Phase 2 document split

3. Update change log with date 2026-01-23 documenting the Phase 2 restructuring.

Follow the same format as existing sub-documents (wire diagrams, field tables, protocol behavior, cross-references).
```

### 5.2 System Reminder (Automatic)

The system automatically injected continuation reminders:

```
[SYSTEM REMINDER - TODO CONTINUATION]

Incomplete tasks remain in your todo list. Continue working on the next pending task.

- Proceed without asking for permission
- Mark each task complete when finished
- Do not stop until all tasks are done

[Status: X/Y completed, Z remaining]
```

### 5.3 File Organization (2026-01-23)

**Prompt**:
```
In order to maintain better organization of the analysis directory, please move 
the packet taxonomy documents to analysis/packet_taxonomy
```

**Result**: All 10 documents moved to `analysis/packet_taxonomy/` subdirectory.

---

## 6. Documentation Standards

The following standards were applied consistently across all documents:

### Wire Diagram Format
```
Byte:    0       1       2       3       4       5       6       7
     +-------+-------+-------+-------+-------+-------+-------+-------+
     | field1| field2|     field3    |         field4 [31:0]         |
     +-------+-------+-------+-------+-------+-------+-------+-------+
```

### Field Table Format
| Field | Bits | Offset | Description | Constraints |
|-------|------|--------|-------------|-------------|
| field_name | bit_count | byte[bit_range] | Description | Must be X |

### Section Structure
1. Overview with feature summary table
2. Format sections with wire diagram, field table, protocol behavior
3. Cross-references to related documents and datamodel files
4. References to specifications

### Datamodel Traceability
- Every format references its `.ksy` datamodel file
- UE Spec table/section/page references included
- Related formats cross-linked

---

## 7. Final Statistics

| Metric | Value |
|--------|-------|
| Total documents | 10 |
| Total size | ~214 KB |
| Formats documented | ~80 |
| Datamodel files referenced | ~168 |
| Work sessions | ~5 |
| Calendar days | 10 (2026-01-14 to 2026-01-23) |
