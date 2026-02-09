# Technical Report Generation Rules

This document defines standards for generating technical reports from KSY datamodel files.

---

## Scope

This document defines **HOW** to extract data from KSY datamodel files and format it into YAML sections. It is a **data extraction specification**.

**Use this file when**: Parsing KSY files, formatting YAML sections, understanding field mappings.

**For protocol-specific content requirements**: See [protocol-technical-reports.md](./protocol-technical-reports.md)

---

## Related Rules

| File | Purpose | When to Use |
|------|---------|-------------|
| [protocol-technical-reports.md](./protocol-technical-reports.md) | Protocol-specific content requirements | Deciding WHAT content each protocol report needs |
| This file | KSY extraction and YAML formatting | Deciding HOW to format extracted data |

### Precedence

When guidance conflicts:
1. **YAML syntax/format**: This file takes precedence
2. **Protocol-specific content**: `protocol-technical-reports.md` takes precedence
3. **Overflow handling**: Both files - follow the more restrictive guidance

---

## Required Sections

Every technical report MUST include the following sections in order:

### 1. Overview/Introduction
- Protocol context and purpose
- Delivery modes (if applicable)
- Relationships to other protocols/layers
- Size summary

### 2. Packet Variants (FRONT OF REPORT)
- Complete packet variant matrix showing all supported packet types
- Header stack for each variant (L2 → L3 → L4 → Transport → SES)
- Use cases for each variant
- Wire format diagrams for key variants

### 3. Header Overhead Summary (FRONT OF REPORT)
- Table showing header sizes by component for each variant
- Total overhead per variant
- Efficiency calculations (payload / total for reference payload size)
- Comparison with other protocols (e.g., RoCEv2)

### 4. Wire Format Diagrams
- ASCII art showing byte/bit layouts
- Use plain code blocks (no language tag)
- Show byte positions and bit fields
- Use ASCII box drawing characters

### 5. Field Definition Tables
- Complete field breakdown with constraints
- One table per header/packet type
- Enumerations INLINE with their associated field descriptions

### 6. Enumeration Tables
- All enumerations used by the protocol
- Organized per-sublayer (PDS, SES, CMS, TSS, LLR, CBFC)
- ALSO included inline with field definitions where enum is used

### 7. State Machine Sections
- States table with descriptions
- ASCII transition diagrams
- Parameters table (if applicable)
- Behavior rules as bullet lists

### 8. Cross-References
- Related formats table
- Links to related KSY files
- Inline references where appropriate

### 9. UE Spec References
- Section, table, and page numbers
- Spec version included

---

## Content Overflow Prevention (CRITICAL)

**ALL slides and content MUST fit within slide boundaries.** When generating YAML sections, consider overflow:

1. **Tables**: If >15 rows, add pagination markers (e.g., "Field Definitions (1/3)")
2. **Bullet Lists**: If >10 items, split at logical breakpoints
3. **Wire Diagrams**: Keep to 8 bytes per line maximum
4. **Code Blocks**: Truncate with "..." if >20 lines
5. **TOC**: Multi-column layout handled automatically by PPTX generator

**Note**: The PPTX generator (`utilities/pptx_helper`) handles some overflow automatically, but YAML authors should design for readability.

---

## Content Extraction Sources

### KSY Metadata Fields

| KSY Field | Content to Extract |
|-----------|-------------------|
| `meta.id` | Header/packet identifier |
| `meta.title` | Human-readable title |
| `x-spec.table` | UE Spec table reference |
| `x-spec.section` | UE Spec section reference |
| `x-spec.page` | UE Spec page number |
| `x-spec.spec_version` | Spec version (e.g., "1.0.1") |
| `x-spec.spec_date` | Spec date |
| `x-spec-ref` | Per-field spec references |
| `x-protocol.state_machine` | State machine definition |
| `x-protocol.usage_notes` | Protocol usage notes |
| `x-protocol.related_messages` | Related message types |
| `x-packet.layer` | Protocol layer (link, transport, etc.) |
| `x-packet.sublayer` | Sublayer (pds, ses, cms, tss, llr, cbfc) |
| `x-packet.category` | Packet category |
| `x-packet.size_bytes` | Total size in bytes |
| `x-packet.size_bits` | Total size in bits |
| `x-packet.constraints` | Validation constraints |
| `enums` | Enumeration definitions |
| `seq` | Field sequence definitions |
| `seq[].id` | Field name |
| `seq[].type` | Field type |
| `seq[].doc` | Field documentation |
| `seq[].x-required` | Required flag |
| `seq[].x-constraint` | Field constraint |
| `seq[].x-spec-ref` | Field-level spec reference |
| `instances` | Computed/derived fields |

---

## Formatting Standards

### Field Definition Table Format

```yaml
- type: table
  title: "{Header Name} Field Definitions"
  headers: ["Field", "Bits", "Offset", "Type", "Description", "Constraints"]
  rows:
    - ["field_name", "8", "0", "u1", "Description text", "value == 0x5C"]
```

**Column Definitions:**
- **Field**: Field name from `seq[].id`
- **Bits**: Size in bits (from type or explicit size)
- **Offset**: Bit offset from start of header
- **Type**: Kaitai type (u1, u2, b5, etc.)
- **Description**: First line of `seq[].doc`
- **Constraints**: From `seq[].x-constraint` or `valid` clause

### Packet Variant Matrix Format

```yaml
- type: table
  title: "UE Packet Variant Matrix"
  headers: ["Variant", "Header Stack", "Total Overhead", "Use Case"]
  rows:
    - ["UE Standard", "Eth → IPv4 → UDP → PDS → SES(std)", "100B", "Standard tagged send/recv"]
    - ["UE Small", "Eth → IPv4 → UDP → PDS → SES(small)", "88B", "Small messages (<256B)"]
    - ["UE + CSIG Compact", "Eth → IPv4 → UDP → PDS → CC(8B) → SES", "108B", "Standard + congestion state"]
    - ["UE Encrypted", "Eth → IPv4 → UDP → TSS → PDS → SES", "112B+16B", "Secure domain traffic"]
```

### Header Overhead Summary Format

```yaml
- type: table
  title: "Header Overhead Summary"
  headers: ["Variant", "L2", "L3", "L4", "TSS", "PDS", "CC", "SES", "Total", "Auth Tag"]
  rows:
    - ["UE Standard", "14B", "20B", "8B", "-", "14B", "-", "44B", "100B", "-"]
    - ["UE Small", "14B", "20B", "8B", "-", "14B", "-", "32B", "88B", "-"]
    - ["UE Encrypted", "14B", "20B", "8B", "12B", "14B", "-", "44B", "112B", "16B"]
```

**Efficiency Calculation:**
```yaml
- type: table
  title: "Protocol Efficiency Comparison (4KB Payload)"
  headers: ["Protocol", "Overhead", "Efficiency"]
  rows:
    - ["UE Standard", "100B", "97.6%"]
    - ["UE Small", "88B", "97.9%"]
    - ["RoCEv2 (IPv4)", "58B", "98.6%"]
```

### Enumeration Table Format

```yaml
- type: table
  title: "{Enum Name} Values"
  headers: ["Value", "Name", "Description"]
  rows:
    - ["0x00", "reserved", "Reserved value"]
    - ["0x01", "tss", "Transport Security Sublayer"]
```

**Column Definitions:**
- **Value**: Numeric value in hex format (0x00)
- **Name**: Enum member `id`
- **Description**: Enum member `doc`

**Enumeration Organization:**
- Group enumerations by sublayer (PDS, SES, CMS, TSS, LLR, CBFC)
- Include consolidated reference tables per sublayer
- ALSO include inline with field definitions where enum is used

### Inline Enumeration with Field Definition

When a field uses an enumeration, include the enum values directly after the field table:

```yaml
- type: table
  title: "PDS Prologue Field Definitions"
  headers: ["Field", "Bits", "Offset", "Type", "Description", "Constraints"]
  rows:
    - ["type", "5", "0", "b5", "PDS packet type", "See PDS Type Values below"]
    - ["next_hdr", "4", "5", "b4", "SES header type", "See Next Header Types below"]

- type: table
  title: "PDS Type Values (type field)"
  headers: ["Value", "Name", "Description"]
  rows:
    - ["0x00", "reserved", "Reserved"]
    - ["0x01", "tss", "Transport Security Sublayer header follows"]
    - ["0x02", "rud_request", "Reliable Unordered Delivery request"]
```

### State Machine Section Format

**States Table:**
```yaml
- type: table
  title: "{Protocol} State Machine States"
  headers: ["State", "Description"]
  rows:
    - ["IDLE", "No pending data, all ACKed"]
    - ["ACTIVE", "Data to send but CC does not permit"]
```

**Transition Diagram:**
```yaml
- type: code_block
  title: "{Protocol} State Transitions"
  language: ""
  code: |
    IDLE ──[new data]──> ACTIVE ──[CC permits]──> READY
      ^                    ^                        │
      │                    │                        │
      │                    └──[CC exhausted]────────┘
      │                                             
      └──[all ACKed]──── PENDING <──[all sent]──────┘
```

**Parameters Table (if applicable):**
```yaml
- type: table
  title: "{Protocol} Parameters"
  headers: ["Parameter", "Type", "Description"]
  rows:
    - ["ack_request_interval", "uint32", "Packets between ACK requests"]
```

**Behavior Rules:**
```yaml
- type: item_list
  title: "{Protocol} Transmission Rules"
  items:
    - "Source assigns monotonically increasing PSN to each packet"
    - "ar flag SHOULD be set periodically"
  item_type: closed
```

### Bullet/Item List Section Types

The YAML parser accepts **both** `item_list` and `bullets` as section types. They are functionally equivalent.

**Format 1: `bullets` (preferred for new reports)**
```yaml
- type: bullets
  title: "Key Points"
  bullets:
    - "First point"
    - "Second point"
```

**Format 2: `item_list` (legacy, still supported)**
```yaml
- type: item_list
  title: "Key Points"
  items:
    - "First point"
    - "Second point"
  item_type: closed  # or "open" for ○ bullets
```

**Note**: `item_type: open` renders with ○ bullets, `item_type: closed` (default) renders with • bullets.

### Wire Format Diagram Format

```yaml
- type: code_block
  title: "{Header Name} Wire Format"
  language: ""
  code: |
    Byte:    0       1       2       3       4       5       6       7
         +-------+-------+-------+-------+-------+-------+-------+-------+
         |type |nxt|flg|       clear_psn_offset |         PSN [31:0]    →
         +-------+-------+-------+-------+-------+-------+-------+-------+
```

**Diagram Guidelines:**
- Show byte positions at top
- Use ASCII box drawing: `+`, `-`, `|`, `→`
- Label fields with names from `seq[].id`
- Show bit ranges for packed fields: `[7:3]`
- Use `→` for fields continuing to next line

### UE Spec Reference Format

**Standard Format:**
```
UE Spec v{version}, Table {table}, Section {section}, Page {page}
```

**Example:**
```
UE Spec v1.0.1, Table 5-20, Section 5.2.6.1, Page 492
```

**In YAML:**
```yaml
- type: text
  content: "Reference: UE Spec v1.0.1, Table 5-20, Section 5.2.6.1, Page 492"
```

### Cross-Reference Table Format

```yaml
- type: table
  title: "Related Formats"
  headers: ["Format", "Relationship", "KSY File"]
  rows:
    - ["CC_Update", "Credit consumed updates", "cc_update.ksy"]
    - ["CBFC TLV", "CBFC negotiation via LLDP", "cbfc_tlv.ksy"]
```

---

## Section Organization by Sublayer

### PDS (Packet Delivery Sublayer)
- PDS Type Values enumeration
- NACK Codes enumeration
- Prologue format
- RUD/ROD Request/ACK formats
- RUDI/UUD formats
- Control packet formats

### SES (Semantic Sublayer)
- SES Request Opcodes enumeration
- SES Response Opcodes enumeration
- Return Codes enumeration
- Atomic Opcodes enumeration
- Atomic Datatypes enumeration
- Standard Request formats
- Response formats
- Small Message format

### CMS (Congestion Management Sublayer)
- CC Type Values enumeration
- CC State formats (compact, wide)
- CCC State Machine

### TSS (Transport Security Sublayer)
- TSS Type Values enumeration
- TSS Header format
- Security context handling

### LLR (Link-Level Reliability)
- LLR CtlOS Types enumeration
- LLR ACK/NACK formats
- LLR Init/Init Echo formats
- LLR State Machine

### CBFC (Credit-Based Flow Control)
- CBFC Message Types enumeration
- CF_Update format
- CC_Update format
- VC State Machine

---

## Validation Rules

### Required Metadata
- Every header MUST have `x-spec` with at least `table` and `section`
- Every field SHOULD have `doc` string
- Enumerations MUST have `doc` for each value

### Consistency Checks
- All cross-references MUST resolve to existing KSY files
- All enumeration references MUST be defined
- Field offsets MUST be sequential and non-overlapping

### Size Validation
- `x-packet.size_bytes` MUST match sum of field sizes
- `x-packet.size_bits` MUST equal `size_bytes * 8`

---

## Example: Complete Section

```yaml
sections:
  - type: section_header
    title: "CF_Update Control Ordered Set"
    subtitle: "8 bytes (64 bits)"

  - type: text
    content: |
      CF_Update is used to communicate credit freed (CF) information for virtual 
      channels (VCs). Each CF_Update CtlOS can carry credit updates for two VCs.
      
      Reference: UE Spec v1.0.1, Table 5-20, Section 5.2.6.1, Page 492

  - type: code_block
    title: "CF_Update Wire Format"
    language: ""
    code: |
      Byte:    0       1       2       3       4       5       6       7
           +-------+-------+-------+-------+-------+-------+-------+-------+
           | 0x5C  | 0x10  |CF1_VC |CF1_cnt|CF1_cnt| O=0x6 |CF2_VC |CF2_cnt|
           |       | type  |+cnt_hi|  mid  |lo+rsv |       |+cnt_hi|  mid  |
           +-------+-------+-------+-------+-------+-------+-------+-------+

  - type: table
    title: "CF_Update Field Definitions"
    headers: ["Field", "Bits", "Offset", "Type", "Description", "Constraints"]
    rows:
      - ["control_char", "8", "0", "u1", "UE control ordered set character", "value == 0x5C"]
      - ["message_type", "8", "8", "u1", "CtlOS Message Type (CF_Update)", "value == 0x10"]
      - ["cf1_vc_and_count_high", "8", "16", "u1", "CF1 VC index + count high bits", ""]
      - ["cf1_count_mid", "8", "24", "u1", "CF1 count middle bits", ""]
      - ["cf1_count_low_and_ocode", "8", "32", "u1", "CF1 count low + O-code", "(value & 0x0F) == 0x06"]
      - ["cf2_vc_and_count_high", "8", "40", "u1", "CF2 VC index + count high bits", ""]
      - ["cf2_count_mid", "8", "48", "u1", "CF2 count middle bits", ""]
      - ["cf2_count_low_and_reserved", "8", "56", "u1", "CF2 count low + reserved", ""]

  - type: table
    title: "CBFC Message Type Values"
    headers: ["Value", "Name", "Description"]
    rows:
      - ["0x10", "cf_update", "CF_Update CtlOS message (credit freed updates for 2 VCs)"]

  - type: table
    title: "Related Formats"
    headers: ["Format", "Relationship", "KSY File"]
    rows:
      - ["CC_Update", "Credit consumed updates (Ethernet packet format)", "cc_update.ksy"]
      - ["CBFC TLV", "CBFC negotiation via LLDP", "cbfc_tlv.ksy"]
```

---

## Generation Workflow

1. **Parse KSY file** using `yaml.safe_load()`
2. **Extract metadata** from `x-spec`, `x-packet`, `x-protocol`
3. **Extract fields** from `seq` with offsets calculated
4. **Extract enums** from `enums` section
5. **Extract state machine** from `x-protocol.state_machine` (if present)
6. **Generate sections** following formats above
7. **Add cross-references** from `x-protocol.related_messages`
8. **Validate** against rules above

---

## Quality Checklist

Before finalizing any YAML report:

- [ ] All required sections from this document included
- [ ] All tables have headers and consistent column counts
- [ ] All wire diagrams use ASCII box drawing characters
- [ ] All enumerations include value, name, description columns
- [ ] All spec references include table/section/page numbers
- [ ] Field offsets are sequential and non-overlapping
- [ ] `x-packet.size_bytes` matches sum of field sizes
- [ ] No content overflow on any section (see Overflow Prevention)

For protocol-specific checklists, see [protocol-technical-reports.md](./protocol-technical-reports.md#quality-checklist).
