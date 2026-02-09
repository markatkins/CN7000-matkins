# Protocol Technical Report Generation Rules

This document defines protocol-specific rules for generating technical reports from analysis documents and KSY datamodel files.

---

## Scope

This document defines **WHAT** content each protocol report must contain and how to generate PPTX presentations. It is a **content requirements specification**.

**Use this file when**: Determining required sections per protocol, generating PPTX, checking quality.

**For YAML formatting standards**: See [technical-report-generation.md](./technical-report-generation.md)

---

## Related Rules

| File | Purpose | When to Use |
|------|---------|-------------|
| [technical-report-generation.md](./technical-report-generation.md) | KSY extraction and YAML formatting | Deciding HOW to format extracted data |
| This file | Protocol-specific content requirements | Deciding WHAT content each protocol report needs |

### Precedence

When guidance conflicts:
1. **Protocol-specific content**: This file takes precedence
2. **YAML syntax/format**: `technical-report-generation.md` takes precedence
3. **Overflow handling**: Both files - follow the more restrictive guidance

---

## General Principles

### 1. Content Overflow Prevention (CRITICAL)

**ALL slides and content MUST fit within slide boundaries.** When content would overflow:

1. **Tables**: Split into multiple slides with pagination (e.g., "Field Definitions (1/3)")
2. **TOC**: Use multi-column layout (2-3 columns) and multiple slides if needed
3. **Bullet Lists**: Split at logical breakpoints, continue on next slide
4. **Wire Diagrams**: Scale font or split into multiple diagrams
5. **Code Blocks**: Truncate with "..." or split across slides

### 2. Source Documents

Each protocol report draws from:
- **Analysis Documents**: `analysis/packet_taxonomy/packet_taxonomy_{protocol}.md`
- **KSY Datamodel Files**: `earlysim/datamodel/protocols/{protocol}/`
- **Existing Rules**: `.sisyphus/rules/technical-report-generation.md`

### 3. Report Structure (All Protocols)

Every technical report MUST follow this section order:

1. **Title Slide** - Protocol name, version, date
2. **Table of Contents** - Multi-column with hyperlinks
3. **Overview** - Protocol purpose, context, key characteristics
4. **Packet Variants** - Complete variant matrix (if applicable)
5. **Header Overhead Summary** - Size breakdown by component
6. **Protocol Layers/Sublayers** - Organized by layer
7. **Wire Format Diagrams** - ASCII art for each packet type
8. **Field Definition Tables** - Complete field breakdown
9. **Enumeration Tables** - All enum values (inline with fields)
10. **State Machines** - States, transitions, behavior (if applicable)
11. **Cross-References** - Related formats and documents
12. **References** - Spec citations

---

## Protocol-Specific Rules

---

## UE+ (Ultra Ethernet Plus)

### Source Documents
- `analysis/packet_taxonomy/packet_taxonomy_ue_pds.md` - PDS formats
- `analysis/packet_taxonomy/packet_taxonomy_ue_ses.md` - SES formats
- `analysis/packet_taxonomy/packet_taxonomy_ue_cms_tss.md` - CMS/TSS formats
- `analysis/packet_taxonomy/packet_taxonomy_ue_link.md` - LLR/CBFC formats
- `analysis/packet_taxonomy/packet_taxonomy_ue_plus_variants.md` - Packet variants
- `analysis/packet_taxonomy/packet_taxonomy_ue_tagged_send_variants.md` - Tagged send variants

### Datamodel Directory
`earlysim/datamodel/protocols/ue/`

### Required Sections

#### 1. Overview
- UE+ protocol purpose and positioning vs RoCEv2
- Delivery modes (RUD, ROD, RUDI, UUD)
- Protocol stack diagram showing all sublayers
- Key differentiators from RoCEv2

#### 2. Packet Variants Matrix
Include ALL variants from `packet_taxonomy_ue_plus_variants.md`:

| Variant | Header Stack | Total Overhead | Use Case |
|---------|--------------|----------------|----------|
| UE Standard | Eth → IPv4 → UDP → PDS → SES(std) | 100B | Standard tagged send/recv |
| UE Small | Eth → IPv4 → UDP → PDS → SES(small) | 88B | Small messages (<256B) |
| UE + CSIG Compact | Eth → IPv4 → UDP → PDS → CC(8B) → SES | 108B | Congestion state |
| UE Encrypted | Eth → IPv4 → UDP → TSS → PDS → SES | 112B+16B | Secure domain |
| UE IPv6 | Eth → IPv6 → UDP → PDS → SES | 120B | IPv6 networks |

#### 3. Header Overhead Summary
Table showing size by component:

| Variant | L2 | L3 | L4 | TSS | PDS | CC | SES | Total | Auth |
|---------|----|----|----|----|-----|----|----|-------|------|
| Standard | 14B | 20B | 8B | - | 14B | - | 44B | 100B | - |

Include efficiency comparison with RoCEv2.

#### 4. Sublayer Sections (in order)

**PDS (Packet Delivery Sublayer)**:
- PDS Type Values enumeration (0x00-0x0E)
- NACK Codes enumeration
- Prologue format (2 bytes)
- All request formats: RUD, ROD, RUDI, UUD
- All response formats: ACK, ACK_CC, ACK_CCX, NACK, NACK_CCX
- Control packet formats

**SES (Semantic Sublayer)**:
- SES Request Opcodes enumeration
- SES Response Opcodes enumeration
- Return Codes enumeration
- Atomic Opcodes and Datatypes
- Standard Request formats (SOM=1, SOM=0)
- Response formats
- Small Message format
- Extension formats (Rendezvous, Atomic, CAS)

**CMS (Congestion Management Sublayer)**:
- CC Type Values enumeration
- ACK CC State formats (NSCC, RCCC/TFC)
- Request CC State format
- CCC State Machine (states, transitions, behavior)

**TSS (Transport Security Sublayer)**:
- TSS Type Values enumeration
- Security Header format (12-16 bytes)
- IV construction methods
- Secure domain handling

**LLR (Link-Level Reliability)**:
- LLR CtlOS Types enumeration
- LLR_ACK, LLR_NACK formats
- LLR_INIT, LLR_INIT_ECHO formats
- LLR State Machine
- 64B/66B block format

**CBFC (Credit-Based Flow Control)**:
- CBFC Message Types enumeration
- CF_Update CtlOS format
- CC_Update Message format
- VC State Machine

#### 5. Wire Format Diagrams
Include ASCII diagrams for:
- PDS Prologue
- RUD/ROD Request (12 bytes)
- ACK/NACK (12 bytes)
- SES Standard Request SOM=1 (44 bytes)
- SES Small Message (32 bytes)
- LLR CtlOS (8 bytes)
- CF_Update CtlOS (8 bytes)

#### 6. State Machines
Include for:
- CCC (Congestion Control Context)
- LLR (Link-Level Reliability)
- VC (Virtual Channel)

Format:
```yaml
- type: table
  title: "CCC State Machine States"
  headers: ["State", "Description"]
  rows:
    - ["IDLE", "No pending data"]
    - ["ACTIVE", "Data pending, CC not permitting"]
```

#### 7. Spec References
All content must cite UE Spec v1.0.1 with:
- Table number
- Section number
- Page number

---

## RoCEv2 (RDMA over Converged Ethernet v2)

### Source Documents
- `analysis/packet_taxonomy/packet_taxonomy_rocev2.md`

### Datamodel Directory
`earlysim/datamodel/protocols/roce/`

### Required Sections

#### 1. Overview
- RoCEv2 purpose and InfiniBand heritage
- Transport types (RC, UC, RD, UD)
- UDP port 4791
- Key characteristics (24-bit PSN, 24-bit QP)

#### 2. Packet Variants Matrix

| Variant | Header Stack | Total Overhead | Use Case |
|---------|--------------|----------------|----------|
| RC SEND | Eth → IPv4 → UDP → BTH | 58B | Reliable send |
| RC RDMA_WRITE | Eth → IPv4 → UDP → BTH → RETH | 74B | Remote write |
| RC RDMA_READ | Eth → IPv4 → UDP → BTH → RETH | 74B | Remote read request |
| RC Atomic | Eth → IPv4 → UDP → BTH → AtomicETH | 86B | Atomic operations |
| UD SEND | Eth → IPv4 → UDP → BTH → DETH | 66B | Unreliable datagram |
| IPv6 variants | +20B for IPv6 header | +20B | IPv6 networks |

#### 3. Header Overhead Summary

| Variant | L2 | L3 | L4 | BTH | Ext | ICRC | Total |
|---------|----|----|----|----|-----|------|-------|
| RC SEND | 14B | 20B | 8B | 12B | - | 4B | 58B |
| RC WRITE | 14B | 20B | 8B | 12B | 16B | 4B | 74B |

#### 4. Transport Headers

**BTH (Base Transport Header, 12 bytes)**:
- Opcode encoding (transport type + operation)
- Transport Types enumeration
- Operations enumeration
- Field definitions with constraints

**RETH (RDMA Extended, 16 bytes)**:
- Virtual address (64-bit)
- R_Key (32-bit)
- DMA Length (32-bit)

**AETH (ACK Extended, 4 bytes)**:
- Syndrome encoding
- MSN (Message Sequence Number)

**AtomicETH (28 bytes)**:
- Virtual address
- R_Key
- Swap/Add data
- Compare data (for CAS)

**ImmDt (4 bytes)**:
- Immediate data field

#### 5. Opcode Tables
Complete opcode table showing:
- Opcode value (hex)
- Operation name
- Required extended headers
- Transport type applicability

#### 6. Wire Format Diagrams
- BTH (12 bytes)
- RETH (16 bytes)
- AETH (4 bytes)
- AtomicETH (28 bytes)
- Complete packet examples

#### 7. Spec References
Cite InfiniBand Architecture Specification Vol 1, relevant sections.

---

## Ethernet (Standard Protocols)

### Source Documents
- `analysis/packet_taxonomy/packet_taxonomy_ethernet.md`

### Datamodel Directory
`earlysim/datamodel/protocols/ethernet/`

### Required Sections

#### 1. Overview
- Standard Ethernet protocol stack
- Use cases: RoCEv2 encapsulation, offload, VxLAN+, management
- RSS (Receive Side Scaling) support

#### 2. Layer Organization

**Link Layer**:
- Ethernet II (14 bytes)
- VLAN 802.1Q (4 bytes)
- IEEE 802.3/LLC/SNAP

**Network Layer**:
- IPv4 (20 bytes minimum)
- IPv6 (40 bytes)

**Transport Layer**:
- UDP (8 bytes)
- TCP (20 bytes minimum)

#### 3. Field Definition Tables
For each header type:
- Field name, bits, offset, description
- Common values (EtherTypes, IP protocols, ports)

#### 4. EtherType Table

| Value | Protocol |
|-------|----------|
| 0x0800 | IPv4 |
| 0x86DD | IPv6 |
| 0x8100 | VLAN (802.1Q) |
| 0x88A8 | QinQ (802.1ad) |

#### 5. Wire Format Diagrams
- Ethernet II header
- VLAN tag
- IPv4 header
- IPv6 header
- UDP header
- TCP header

#### 6. RSS Section
- Hash algorithm selection
- Hash input formats
- Toeplitz hash key

---

## Cornelis (Proprietary Formats)

### Source Documents
- `analysis/packet_taxonomy/packet_taxonomy_cornelis.md`

### Datamodel Directory
`earlysim/datamodel/protocols/cornelis/`

### Required Sections

#### 1. Overview
- Cornelis proprietary extensions
- Design goals: efficiency, telemetry, collectives, overlay
- Format summary table with status (Complete/WIP)

#### 2. Format Status Matrix

| Layer | Format | Size | Status | Description |
|-------|--------|------|--------|-------------|
| Link | UE+ Header | 12B | Complete | Optimized L2 |
| Network | UFH-16 | 12B | Complete | 16-bit forwarding |
| Network | UFH-32 | 12B | Complete | 32-bit forwarding |
| Network | Collective L2 | 4B | **WIP** | HW collectives |
| Network | Scale-Up L2 | 4B | **WIP** | GPU interconnect |
| Transport | CSIG+ | 4B | Complete | In-band telemetry |
| Encap | VxLAN+ | 4B | Complete | Fabric overlay |

#### 3. UE+ Header Section
- Wire format diagram (12 bytes)
- Field definitions
- HMAC sub-structure (24-bit hierarchical MAC)
- Topology variants (no subdivision, x2, x8)

#### 4. UFH Sections
**UFH-16**:
- Wire format overlaying MAC fields
- Field definitions
- Addressing scheme

**UFH-32**:
- Extended addressing
- Field definitions

#### 5. CSIG+ Telemetry
- Telemetry data format
- Integration with packet flow

#### 6. VxLAN+ Encapsulation
- Fabric-aware overlay format
- Multi-tenant support

#### 7. Terminology Table

| OPA Term | Cornelis Term | Description |
|----------|---------------|-------------|
| DLID | DMAC | Destination Hierarchical MAC |
| SLID | SMAC | Source Hierarchical MAC |
| LID | HMAC | Hierarchical MAC Address |

---

## UALink (Reference Only)

### Source Documents
- `analysis/packet_taxonomy/packet_taxonomy_ualink.md`

### Datamodel Directory
`earlysim/datamodel/protocols/ualink/`

### Required Sections

#### 1. Overview (with Warning)
Include prominent warning:
> **Reference Only**: UALink is NOT currently supported by PMR. Included for future AI/ML accelerator interconnect reference.

- Protocol purpose (AI/ML accelerator interconnect)
- Layer summary (UPLI, Transaction, Data Link, Physical, Security)
- 38 packet definitions across all layers

#### 2. Protocol Stack Diagram
ASCII diagram showing all layers:
```
UPLI (Upper Protocol Layer Interface)
Transaction Layer
Data Link Layer
Physical Layer
Security Layer (Cross-cutting)
```

#### 3. Layer Summaries
For each layer, provide:
- Format count
- Key formats table
- Brief description

**UPLI Layer** (8 formats):
- Commands, Request/Response channels, Status codes

**Transaction Layer** (9 formats):
- TL Flit, Control/Data half flits, Flow control

**Data Link Layer** (12 formats):
- DL Flit, Segments, CRC, Control messages, Replay

**Physical Layer** (4 formats):
- Alignment markers, Control ordered sets, Link training

**Security Layer** (5 formats):
- Authentication, Encryption, Key derivation/rotation

#### 4. PMR Support Status Table

| Feature | Status |
|---------|--------|
| UALink Protocol | **NOT SUPPORTED** |
| Future Support | Under consideration |

---

## YAML Report Format

### Section Types

```yaml
# Section header (creates TOC entry)
- type: section_header
  title: "Section Title"
  subtitle: "Optional subtitle"

# Text content
- type: text
  content: |
    Multi-line text content.
    Can include markdown-style formatting.

# Bullet list (Format 1: preferred for new reports)
- type: bullets
  title: "List Title"
  bullets:
    - "First item"
    - "Second item"

# Bullet list (Format 2: legacy, still supported)
- type: item_list
  title: "List Title"
  items:
    - "First item"
    - "Second item"
  item_type: closed  # or "open" for ○ bullets

# Table
- type: table
  title: "Table Title"
  headers: ["Col1", "Col2", "Col3"]
  rows:
    - ["val1", "val2", "val3"]

# Code block (wire diagrams)
- type: code_block
  title: "Wire Format"
  language: ""
  code: |
    +-------+-------+-------+
    | Field1| Field2| Field3|
    +-------+-------+-------+
```

**Note**: Both `bullets` and `item_list` are valid section types. They are functionally equivalent - the YAML parser handles both. See [technical-report-generation.md](./technical-report-generation.md#bulletitem-list-section-types) for details.

### Naming Conventions

- Report files: `reports/packet_taxonomy/technical_report_{protocol}.yaml`
- Output files: `reports/packet_taxonomy/technical_report_{protocol}.pptx`
- Protocol names: `ue`, `roce`, `ethernet`, `cornelis`, `ualink`

---

## Generation Workflow

1. **Read analysis document** for protocol
2. **Extract content** following protocol-specific rules above
3. **Generate YAML** following section types
4. **Validate** YAML structure
5. **Generate PPTX** with `--toc` flag:
   ```bash
   python -m utilities.pptx_helper --type technical \
     --data reports/packet_taxonomy/technical_report_{protocol}.yaml \
     --output reports/packet_taxonomy/technical_report_{protocol}.pptx \
     --toc -v
   ```

---

## Adding New Protocols

When adding a new protocol to the technical report system:

### 1. Create Analysis Document
- Location: `analysis/packet_taxonomy/packet_taxonomy_{protocol}.md`
- Include: Overview, packet formats, field definitions, enumerations

### 2. Create KSY Datamodel (if applicable)
- Location: `earlysim/datamodel/protocols/{protocol}/`
- Follow KSY metadata standards in [technical-report-generation.md](./technical-report-generation.md)

### 3. Add Protocol Section to This File
Copy this template and fill in:

```markdown
## {Protocol Name}

### Source Documents
- `analysis/packet_taxonomy/packet_taxonomy_{protocol}.md`

### Datamodel Directory
`earlysim/datamodel/protocols/{protocol}/`

### Required Sections

#### 1. Overview
- Protocol purpose and context
- Key characteristics

#### 2. Packet Variants Matrix
| Variant | Header Stack | Total Overhead | Use Case |
|---------|--------------|----------------|----------|

#### 3. Header Overhead Summary
| Variant | L2 | L3 | L4 | ... | Total |
|---------|----|----|----|----|-------|

#### 4. Wire Format Diagrams
- List key formats to diagram

#### 5. Field Definition Tables
- List headers requiring field tables

#### 6. Spec References
- Cite specification with version, section, page
```

### 4. Generate YAML Report
- Location: `reports/packet_taxonomy/technical_report_{protocol}.yaml`
- Follow YAML format in [technical-report-generation.md](./technical-report-generation.md)

### 5. Generate PPTX
```bash
python -m utilities.pptx_helper --type technical \
  --data reports/packet_taxonomy/technical_report_{protocol}.yaml \
  --output reports/packet_taxonomy/technical_report_{protocol}.pptx \
  --toc -v
```

---

## Quality Checklist

Before finalizing any protocol report:

- [ ] All sections from protocol-specific rules included
- [ ] No content overflow on any slide
- [ ] TOC fits on slide(s) with multi-column layout
- [ ] All tables have headers and consistent column counts
- [ ] All wire diagrams use ASCII box drawing
- [ ] All enumerations include value, name, description
- [ ] All spec references include table/section/page
- [ ] Cross-references link to related formats
- [ ] State machines include states, transitions, behavior
- [ ] Packet variants matrix is complete
- [ ] Header overhead summary includes all components
