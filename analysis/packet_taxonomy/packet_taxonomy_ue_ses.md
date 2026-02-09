# PMR Packet Taxonomy: UE+ SES Formats

**Parent Document**: [packet_taxonomy.md](packet_taxonomy.md)  
**Scope**: Ultra Ethernet+ Semantic Sublayer (SES) packet formats  
**Datamodel Directory**: `datamodel/protocols/ue/transport/ses/`  
**Last Updated**: 2026-01-23

---

## Table of Contents

1. [Overview](#1-overview)
2. [SES Opcodes](#2-ses-opcodes)
3. [SES Packet Formats](#3-ses-packet-formats)
   - [3.1 Standard Request SOM=1 (Table 3-8)](#31-standard-request-som1-table-3-8-44-bytes)
   - [3.2 Standard Request SOM=0 (Table 3-9)](#32-standard-request-som0-table-3-9-16-bytes)
   - [3.3 Response (Table 3-11)](#33-response-table-3-11-16-bytes)
   - [3.4 Response with Data (Table 3-12)](#34-response-with-data-table-3-12-24-bytes)
   - [3.5 Small Message (Figure 3-14)](#35-small-message-figure-3-14-32-bytes)
   - [3.6 Rendezvous Extension (Figure 3-15)](#36-rendezvous-extension-figure-3-15-32-bytes)
   - [3.7 Atomic Extension (Figure 3-16)](#37-atomic-extension-figure-3-16-8-bytes)
   - [3.8 Compare-and-Swap Extension (Figure 3-17)](#38-compare-and-swap-extension-figure-3-17-40-bytes)
   - [3.9 Deferrable Send Request (Figure 3-11)](#39-deferrable-send-request-figure-3-11-44-bytes)
   - [3.10 Ready to Restart (Figure 3-12)](#310-ready-to-restart-figure-3-12-44-bytes)
   - [3.11 Optimized Non-Matching (Table 3-10)](#311-optimized-non-matching-table-3-10-32-bytes)
   - [3.12 Optimized Response with Data (Table 3-13)](#312-optimized-response-with-data-table-3-13-16-bytes)
   - [3.13 Small RMA (Figure 3-14)](#313-small-rma-figure-3-14-32-bytes)
4. [Cross-References](#4-cross-references)
5. [References](#5-references)

---

## 1. Overview

The Semantic Sublayer (SES) provides the semantic meaning for Ultra Ethernet+ operations. SES headers are carried within PDS packets and define the operation type, addressing, and data transfer parameters.

### SES Header Types

| next_hdr Value | Header Type | Size | Description |
|----------------|-------------|------|-------------|
| 0x0 | Standard Header SOM=1 | 44 bytes | Start of message |
| 0x1 | Standard Header SOM=0 | 16 bytes | Continuation |
| 0x2 | Optimized Non-Matching | Variable | Optimized format |
| 0x3 | Small Message/RMA | 32 bytes | Single-packet optimized |
| 0x4 | Response | 16 bytes | Standard response |
| 0x5 | Response with Data | 24 bytes | Data-carrying response |
| 0x6 | Optimized Response | 16 bytes | Optimized format |

### Request/Response Relationships

```
SES Request/Response Relationships:
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  Standard Request ────┬───────────────────→ Response            │
│  (SOM=1, 44B)         └───────────────────→ Response w/Data     │
│       │                                                         │
│       └──→ Continuation (SOM=0, 16B)                            │
│                                                                 │
│  Small Message (32B) ─────────────────────→ Response            │
│                                                                 │
│  + Atomic Extension (8B) ─────────────────→ Response w/Data     │
│                                             (for fetching ops)  │
│                                                                 │
│  + Rendezvous Extension (32B) ────────────→ (target pulls data) │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. SES Opcodes

**Datamodel**: `datamodel/protocols/ue/transport/ses/opcodes.ksy`

### Request Opcodes (Table 3-17)

| Opcode | Value | Description |
|--------|-------|-------------|
| Tagged Send | 0x00 | Send with tag matching |
| RMA Write | 0x01 | Remote memory write |
| RMA Read | 0x02 | Remote memory read |
| Atomic Write | 0x03 | Atomic memory write |
| Atomic Read | 0x04 | Atomic memory read |
| Atomic CAS | 0x05 | Compare-and-swap |
| Deferrable Send | 0x06 | Deferrable send |
| Ready to Restart | 0x07 | Restart notification |
| Small Message | 0x08 | Small message (32B header) |
| Small RMA Write | 0x09 | Small RMA write |
| Small RMA Read | 0x0A | Small RMA read |
| Small Atomic Write | 0x0B | Small atomic write |
| Small Atomic Read | 0x0C | Small atomic read |
| Small Atomic CAS | 0x0D | Small atomic CAS |

### Response Opcodes (Table 3-18)

| Opcode | Value | Description |
|--------|-------|-------------|
| Response | 0x00 | Standard response |
| Response with Data | 0x01 | Response carrying data |
| Optimized Response | 0x02 | Optimized format |
| NACK | 0x03 | Negative acknowledgment |

---

## 3. SES Packet Formats

### Format Summary

| Table/Figure | Format | File | Size | Description |
|--------------|--------|------|------|-------------|
| Table 3-8 | Standard Request (SOM=1) | `standard_request_som1.ksy` | 44 bytes | Start of message |
| Table 3-9 | Standard Request (SOM=0) | `standard_request_som0.ksy` | 16 bytes | Continuation |
| Table 3-11 | Response | `response.ksy` | 16 bytes | Standard response |
| Table 3-12 | Response with Data | `response_with_data.ksy` | 24 bytes | Data-carrying response |
| Figure 3-14 | Small Message | `small_message.ksy` | 32 bytes | Single-packet optimized |
| Figure 3-15 | Rendezvous Extension | `rendezvous_extension.ksy` | 32 bytes | Large message protocol |
| Figure 3-16 | Atomic Extension | `atomic_extension.ksy` | 8 bytes | Atomic operations |

---

### 3.1 Standard Request SOM=1 (Table 3-8, 44 bytes)

**Datamodel**: `datamodel/protocols/ue/transport/ses/standard_request_som1.ksy`  
**Related Formats**: [Standard Request SOM=0 (3.2)](#32-standard-request-som0-table-3-9-16-bytes) | [Response (3.3)](#33-response-table-3-11-16-bytes)

#### Wire Format

```
Byte:    0       1       2       3       4       5       6       7
     +-------+-------+-------+-------+-------+-------+-------+-------+
     |rs|opcode |v|dc|ie|rl|hd|eo|so|    message_id     | ri_gen  →
     +-------+-------+-------+-------+-------+-------+-------+-------+
         8       9      10      11      12      13      14      15
     +-------+-------+-------+-------+-------+-------+-------+-------+
   → |      job_id [23:0]    |rsvd|pid_on_fep |rsvd| resource_idx  →
     +-------+-------+-------+-------+-------+-------+-------+-------+
        16      17      18      19      20      21      22      23
     +-------+-------+-------+-------+-------+-------+-------+-------+
   → |                    buffer_offset [63:0]                       |
     +-------+-------+-------+-------+-------+-------+-------+-------+
        24      25      26      27      28      29      30      31
     +-------+-------+-------+-------+-------+-------+-------+-------+
     |        initiator [31:0]       |   match_bits / memory_key    →
     +-------+-------+-------+-------+-------+-------+-------+-------+
        32      33      34      35      36      37      38      39
     +-------+-------+-------+-------+-------+-------+-------+-------+
   → |  (match_bits cont'd) [63:0]   |       header_data [63:0]     →
     +-------+-------+-------+-------+-------+-------+-------+-------+
        40      41      42      43
     +-------+-------+-------+-------+
   → | (hdr_data)    | request_length|
     +-------+-------+-------+-------+

Byte 0-1 Detail:
  Bit:  7 6 5 4 3 2 1 0 | 7 6 5 4 3 2 1 0
       |rsvd |  opcode |v|dc|ie|rl|hd|eo|so|
       | (2) | (6 bits)|r| | | | | | | |
```

#### Field Definitions

| Field | Bits | Offset | Description | Constraints |
|-------|------|--------|-------------|-------------|
| rsvd | 2 | 0[7:6] | Reserved | Must be 0 |
| opcode | 6 | 0[5:0] | Operation code | Per Table 3-17 |
| version | 2 | 1[7:6] | Protocol version | 0 for v1.0.1 |
| dc | 1 | 1[5] | Delivery Complete | Defer response until globally observable |
| ie | 1 | 1[4] | Initiator Error | Error at initiator |
| rel | 1 | 1[3] | Relative addressing | 0=absolute, 1=relative |
| hd | 1 | 1[2] | Header Data present | 1=header_data valid |
| eom | 1 | 1[1] | End of Message | 1=last packet |
| som | 1 | 1[0] | Start of Message | Must be 1 for this format |
| message_id | 16 | 2-3 | Message identifier | 0=reserved (invalid) |
| ri_generation | 8 | 4 | Resource Index generation | For buffer exhaustion recovery |
| job_id | 24 | 5-7 | Job Identifier | Matches VXLAN VNI size |
| rsvd | 4 | 8[7:4] | Reserved | Must be 0 |
| pid_on_fep | 12 | 8[3:0]+9 | Process ID on FEP | Target process |
| rsvd | 4 | 10[7:4] | Reserved | Must be 0 |
| resource_index | 12 | 10[3:0]+11 | Resource Index | Target resource |
| buffer_offset | 64 | 12-19 | Buffer offset | Or restart token for deferrable |
| initiator | 32 | 20-23 | Initiator ID | For tagged matching |
| match_bits | 64 | 24-31 | Match bits / Memory key | Dual-purpose field |
| header_data | 64 | 32-39 | Header data | Completion data (if hd=1) |
| request_length | 32 | 40-43 | Request length | Bytes to transfer |

#### Field Notes

**match_bits / memory_key Interpretation**:
- For tagged operations (sends): Match bits for receive queue matching
- For RMA operations (reads, writes): Memory key for authorization

**buffer_offset Special Uses**:
- For deferrable sends: Contains restart token (upper 32b initiator, lower 32b target)
- For FI_MR_VIRT_ADDR: Contains absolute virtual address

#### Protocol Behavior

**Message Framing**:
- `som=1, eom=1`: Single-packet message
- `som=1, eom=0`: First packet of multi-packet message
- Continuation packets use SOM=0 format (Table 3-9)

**Addressing Modes**:
- `rel=0` (Absolute): {JobID, PIDonFEP, resource_index} identifies target
- `rel=1` (Relative): Addressing relative to connection context

**Delivery Complete (dc)**:
- When `dc=1`: Response deferred until data globally observable
- Matches FI_DELIVERY_COMPLETE libfabric option

**Reference**: UE Spec v1.0.1, Table 3-8, Section 3.4.2.1, Page 158

---

### 3.2 Standard Request SOM=0 (Table 3-9, 16 bytes)

**Datamodel**: `datamodel/protocols/ue/transport/ses/standard_request_som0.ksy`  
**Related Formats**: [Standard Request SOM=1 (3.1)](#31-standard-request-som1-table-3-8-44-bytes)

#### Wire Format

```
Byte:    0       1       2       3       4       5       6       7
     +-------+-------+-------+-------+-------+-------+-------+-------+
     |rs|opcode |v|dc|ie|rl|hd|eo|so|    message_id     | ri_gen  →
     +-------+-------+-------+-------+-------+-------+-------+-------+
         8       9      10      11      12      13      14      15
     +-------+-------+-------+-------+-------+-------+-------+-------+
   → |      job_id [23:0]    |       message_offset [31:0]          |
     +-------+-------+-------+-------+-------+-------+-------+-------+
```

#### Field Definitions

| Field | Bits | Offset | Description | Constraints |
|-------|------|--------|-------------|-------------|
| rsvd | 2 | 0[7:6] | Reserved | Must be 0 |
| opcode | 6 | 0[5:0] | Operation code | Same as SOM=1 packet |
| version | 2 | 1[7:6] | Protocol version | 0 for v1.0.1 |
| dc | 1 | 1[5] | Delivery Complete | Same as SOM=1 |
| ie | 1 | 1[4] | Initiator Error | Error at initiator |
| rel | 1 | 1[3] | Relative addressing | Same as SOM=1 |
| hd | 1 | 1[2] | Header Data present | Ignored for SOM=0 |
| eom | 1 | 1[1] | End of Message | 1=last packet |
| som | 1 | 1[0] | Start of Message | Must be 0 for this format |
| message_id | 16 | 2-3 | Message identifier | Same as SOM=1 packet |
| ri_generation | 8 | 4 | Resource Index generation | Same as SOM=1 |
| job_id | 24 | 5-7 | Job Identifier | Same as SOM=1 |
| message_offset | 32 | 8-11 | Offset within message | Byte offset from start |

#### Protocol Behavior

**Continuation Packets**:
- Used for packets 2..N of multi-packet messages
- `message_offset` indicates position within overall message
- Target uses offset to place data correctly in buffer

**Packet Ordering**:
- ROD delivery: Packets delivered in PSN order
- RUD delivery: Packets may arrive out of order; target reassembles using message_offset

**Reference**: UE Spec v1.0.1, Table 3-9, Section 3.4.2.1, Page 159

---

### 3.3 Response (Table 3-11, 16 bytes)

**Datamodel**: `datamodel/protocols/ue/transport/ses/response.ksy`  
**Related Formats**: [Standard Request SOM=1 (3.1)](#31-standard-request-som1-table-3-8-44-bytes) | [Response with Data (3.4)](#34-response-with-data-table-3-12-24-bytes)

#### Wire Format

```
Byte:    0       1       2       3       4       5       6       7
     +-------+-------+-------+-------+-------+-------+-------+-------+
     | list|opcode |v| return_code |    message_id     | ri_gen  →
     +-------+-------+-------+-------+-------+-------+-------+-------+
         8       9      10      11      12      13      14      15
     +-------+-------+-------+-------+-------+-------+-------+-------+
   → |      job_id [23:0]    |       modified_length [31:0]         |
     +-------+-------+-------+-------+-------+-------+-------+-------+

Byte 0-1 Detail:
  Bit:  7 6 5 4 3 2 1 0 | 7 6 5 4 3 2 1 0
       |list |  opcode |v| return_code   |
       | (2) | (6 bits)|r|   (6 bits)    |
```

#### Field Definitions

| Field | Bits | Offset | Description | Constraints |
|-------|------|--------|-------------|-------------|
| list | 2 | 0[7:6] | List indicator | 0=expected, 1=unexpected |
| opcode | 6 | 0[5:0] | Response opcode | Per Table 3-18 |
| version | 2 | 1[7:6] | Protocol version | 0 for v1.0.1 |
| return_code | 6 | 1[5:0] | Return code | Per Table 3-19 |
| message_id | 16 | 2-3 | Message identifier | From original request |
| ri_generation | 8 | 4 | Resource Index generation | New generation on mismatch |
| job_id | 24 | 5-7 | Job Identifier | From original request |
| modified_length | 32 | 8-11 | Modified length | Bytes actually transferred |
| rsvd | 32 | 12-15 | Reserved | Must be 0 |

#### Return Codes (Table 3-19)

| Code | Name | Description |
|------|------|-------------|
| 0x00 | RC_OK | Success |
| 0x01 | RC_NO_MATCH | No matching buffer found |
| 0x02 | RC_BUFFER_TOO_SMALL | Target buffer too small |
| 0x03 | RC_AUTHORIZATION_FAILURE | Memory key mismatch |
| 0x04 | RC_INVALID_OPERATION | Invalid operation |
| 0x05 | RC_RESOURCE_EXHAUSTION | Resource exhaustion |
| 0x06 | RC_GENERATION_MISMATCH | RI generation mismatch |
| 0x07 | RC_TRUNCATED | Message truncated |

#### Protocol Behavior

**Response Generation**:
1. Target processes request
2. Generates response with appropriate return_code
3. `modified_length` indicates actual bytes transferred (may be < request_length)

**List Indicator**:
- `list=0`: Payload delivered to expected list (matched posted receive)
- `list=1`: Payload delivered to unexpected list (no matching receive)

**Reference**: UE Spec v1.0.1, Table 3-11, Section 3.4.2.5, Page 167

---

### 3.4 Response with Data (Table 3-12, 24 bytes)

**Datamodel**: `datamodel/protocols/ue/transport/ses/response_with_data.ksy`  
**Related Formats**: [Response (3.3)](#33-response-table-3-11-16-bytes)

#### Wire Format

```
Byte:    0       1       2       3       4       5       6       7
     +-------+-------+-------+-------+-------+-------+-------+-------+
     | list|opcode |v| return_code | response_msg_id   | rsvd    →
     +-------+-------+-------+-------+-------+-------+-------+-------+
         8       9      10      11      12      13      14      15
     +-------+-------+-------+-------+-------+-------+-------+-------+
   → |      job_id [23:0]    |read_req_msg_id|rs|payload_len      →
     +-------+-------+-------+-------+-------+-------+-------+-------+
        16      17      18      19      20      21      22      23
     +-------+-------+-------+-------+-------+-------+-------+-------+
   → |       modified_length [31:0]  |       message_offset [31:0]  |
     +-------+-------+-------+-------+-------+-------+-------+-------+
```

#### Field Definitions

| Field | Bits | Offset | Description | Constraints |
|-------|------|--------|-------------|-------------|
| list | 2 | 0[7:6] | List indicator | 0=expected, 1=unexpected |
| opcode | 6 | 0[5:0] | Response opcode | Per Table 3-18 |
| version | 2 | 1[7:6] | Protocol version | 0 for v1.0.1 |
| return_code | 6 | 1[5:0] | Return code | Per Table 3-19 |
| response_message_id | 16 | 2-3 | Response message ID | For this response |
| rsvd | 8 | 4 | Reserved | Must be 0 |
| job_id | 24 | 5-7 | Job Identifier | From original request |
| read_request_message_id | 16 | 8-9 | Original request msg ID | Links to request |
| rsvd | 2 | 10[7:6] | Reserved | Must be 0 |
| payload_length | 14 | 10[5:0]+11 | Payload in this packet | Max 16383 bytes |
| modified_length | 32 | 12-15 | Total bytes transferred | Across all packets |
| message_offset | 32 | 16-19 | Offset in response | For multi-packet responses |
| rsvd | 32 | 20-23 | Reserved | Must be 0 |

#### Protocol Behavior

**Use Cases**:
- RDMA Read responses (returning requested data)
- Fetching atomic responses (returning original value)

**Multi-Packet Responses**:
- `message_offset` indicates position within overall response
- `payload_length` indicates data in this specific packet
- `modified_length` is total across all response packets

**Reference**: UE Spec v1.0.1, Table 3-12, Section 3.4.2.5, Page 168

---

### 3.5 Small Message (Figure 3-14, 32 bytes)

**Datamodel**: `datamodel/protocols/ue/transport/ses/small_message.ksy`  
**Related Formats**: [Standard Request SOM=1 (3.1)](#31-standard-request-som1-table-3-8-44-bytes) | [Response (3.3)](#33-response-table-3-11-16-bytes)

#### Wire Format

```
Byte:    0       1       2       3       4       5       6       7
     +-------+-------+-------+-------+-------+-------+-------+-------+
     |opcode |v|dc|ie|rl|hd|eo|so|rs| request_length  | ri_gen  →
     +-------+-------+-------+-------+-------+-------+-------+-------+
         8       9      10      11      12      13      14      15
     +-------+-------+-------+-------+-------+-------+-------+-------+
   → |      job_id [23:0]    |rsvd|pid_on_fep |rsvd| resource_idx  →
     +-------+-------+-------+-------+-------+-------+-------+-------+
        16      17      18      19      20      21      22      23
     +-------+-------+-------+-------+-------+-------+-------+-------+
   → |        initiator [31:0]       |        match_bits [63:0]     →
     +-------+-------+-------+-------+-------+-------+-------+-------+
        24      25      26      27      28      29      30      31
     +-------+-------+-------+-------+-------+-------+-------+-------+
   → |  (match_bits cont'd)          |       header_data [63:0]     |
     +-------+-------+-------+-------+-------+-------+-------+-------+
```

#### Field Definitions

| Field | Bits | Offset | Description | Constraints |
|-------|------|--------|-------------|-------------|
| opcode | 6 | 0[7:2] | Operation code | Per Table 3-17 |
| version | 2 | 0[1:0] | Protocol version | 0 for v1.0.1 |
| dc | 1 | 1[7] | Delivery Complete | Defer response |
| ie | 1 | 1[6] | Initiator Error | Error at initiator |
| rel | 1 | 1[5] | Relative addressing | 0=absolute, 1=relative |
| hd | 1 | 1[4] | Header Data present | 1=header_data valid |
| eom | 1 | 1[3] | End of Message | Must be 1 (single packet) |
| som | 1 | 1[2] | Start of Message | Must be 1 (single packet) |
| rsvd | 2 | 1[1:0] | Reserved | Must be 0 |
| rsvd | 2 | 2[7:6] | Reserved | Must be 0 |
| request_length | 14 | 2[5:0]+3 | Request length | Max 16383 bytes |
| ri_generation | 8 | 4 | Resource Index generation | For buffer recovery |
| job_id | 24 | 5-7 | Job Identifier | Target job |
| rsvd | 4 | 8[7:4] | Reserved | Must be 0 |
| pid_on_fep | 12 | 8[3:0]+9 | Process ID on FEP | Target process |
| rsvd | 4 | 10[7:4] | Reserved | Must be 0 |
| resource_index | 12 | 10[3:0]+11 | Resource Index | Target resource |
| initiator | 32 | 12-15 | Initiator ID | For tagged matching |
| match_bits | 64 | 16-23 | Match bits | For tagged matching |
| header_data | 64 | 24-31 | Header data | Completion data |

#### Protocol Behavior

**Optimized Format**:
- 32 bytes vs 44 bytes for standard request
- Single-packet only (`som=1, eom=1` required)
- No buffer_offset (not needed for single packet)
- 14-bit request_length (max 16383 bytes)

**Use Cases**:
- Small tagged sends
- Single-packet messages with matching criteria
- Latency-sensitive operations

**Reference**: UE Spec v1.0.1, Figure 3-14, Section 3.4.2.3, Page 164

---

### 3.6 Rendezvous Extension (Figure 3-15, 32 bytes)

**Datamodel**: `datamodel/protocols/ue/transport/ses/rendezvous_extension.ksy`  
**Related Formats**: [Standard Request SOM=1 (3.1)](#31-standard-request-som1-table-3-8-44-bytes)

#### Wire Format

```
Byte:    0       1       2       3       4       5       6       7
     +-------+-------+-------+-------+-------+-------+-------+-------+
     |       eager_length [31:0]     |        memory_key [63:0]     →
     +-------+-------+-------+-------+-------+-------+-------+-------+
         8       9      10      11      12      13      14      15
     +-------+-------+-------+-------+-------+-------+-------+-------+
   → |  (memory_key cont'd)          |       buffer_offset [63:0]   →
     +-------+-------+-------+-------+-------+-------+-------+-------+
        16      17      18      19      20      21      22      23
     +-------+-------+-------+-------+-------+-------+-------+-------+
   → |  (buffer_offset cont'd)       |     remaining_length [31:0]  →
     +-------+-------+-------+-------+-------+-------+-------+-------+
        24      25      26      27      28      29      30      31
     +-------+-------+-------+-------+-------+-------+-------+-------+
   → | (remaining)   |              reserved [63:0]                  |
     +-------+-------+-------+-------+-------+-------+-------+-------+
```

#### Field Definitions

| Field | Bits | Offset | Description | Constraints |
|-------|------|--------|-------------|-------------|
| eager_length | 32 | 0-3 | Eager data length | Bytes pushed with request |
| memory_key | 64 | 4-11 | Initiator memory key | For target to pull data |
| buffer_offset | 64 | 12-19 | Initiator buffer offset | Start of remaining data |
| remaining_length | 32 | 20-23 | Remaining data length | Bytes to pull |
| rsvd | 64 | 24-31 | Reserved | Must be 0 |

#### Protocol Behavior

**Rendezvous Protocol**:
1. Initiator sends request with eager data + rendezvous extension
2. Target receives eager data, allocates buffer
3. Target issues RDMA Read to pull remaining data using {memory_key, buffer_offset}
4. Target completes operation when all data received

**Two-Sided Protocol**:
- Enables large message transfer without pre-registered buffers
- Target controls when/how to pull remaining data
- Reduces memory registration overhead

**Constraints**:
- MUST NOT be combined with atomic extension
- Placed on every packet using rendezvous opcode

**Reference**: UE Spec v1.0.1, Figure 3-15, Section 3.4.2.3, Page 165

---

### 3.7 Atomic Extension (Figure 3-16, 8 bytes)

**Datamodel**: `datamodel/protocols/ue/transport/ses/atomic_extension.ksy`  
**Related Formats**: [Standard Request SOM=1 (3.1)](#31-standard-request-som1-table-3-8-44-bytes) | [Response with Data (3.4)](#34-response-with-data-table-3-12-24-bytes)

#### Wire Format

```
Byte:    0       1       2       3       4       5       6       7
     +-------+-------+-------+-------+-------+-------+-------+-------+
     |atomic_opcode  |atomic_datatype| semantic_control  | reserved  |
     +-------+-------+-------+-------+-------+-------+-------+-------+
```

#### Field Definitions

| Field | Bits | Offset | Description | Constraints |
|-------|------|--------|-------------|-------------|
| atomic_opcode | 8 | 0 | Atomic operation | Per Table 3-21 |
| atomic_datatype | 8 | 1 | Data type | Per Table 3-22 |
| semantic_control | 16 | 2-3 | Semantic control | Per Table 3-23 |
| rsvd | 32 | 4-7 | Reserved | Must be 0 |

#### Atomic Opcodes (Table 3-21)

| Code | Name | Operation |
|------|------|-----------|
| 0x00 | MIN | Target = MIN(Target, Initiator) |
| 0x01 | MAX | Target = MAX(Target, Initiator) |
| 0x02 | SUM | Target = Target + Initiator |
| 0x03 | DIFF | Target = Target - Initiator |
| 0x04 | PROD | Target = Target * Initiator |
| 0x05 | LOR | Target = Target \|\| Initiator |
| 0x06 | LAND | Target = Target && Initiator |
| 0x07 | BOR | Target = Target \| Initiator |
| 0x08 | BAND | Target = Target & Initiator |
| 0x09 | LXOR | Logical XOR |
| 0x0A | BXOR | Target = Target ^ Initiator |
| 0x0B | READ | Initiator = Target |
| 0x0C | WRITE | Target = Initiator |
| 0x0D | CSWAP | Compare and swap if equal |
| 0x0E | CSWAP_NE | Compare and swap if not equal |
| 0x0F | CSWAP_LE | Compare and swap if ≤ |
| 0x10 | CSWAP_LT | Compare and swap if < |
| 0x11 | CSWAP_GE | Compare and swap if ≥ |
| 0x12 | CSWAP_GT | Compare and swap if > |
| 0x13 | MSWAP | Masked swap |
| 0x14 | INVAL | Invalidate cache |

#### Atomic Datatypes (Table 3-22)

| Code | Name | Size |
|------|------|------|
| 0x00 | INT8 | 1 byte |
| 0x01 | UINT8 | 1 byte |
| 0x02 | INT16 | 2 bytes |
| 0x03 | UINT16 | 2 bytes |
| 0x04 | INT32 | 4 bytes |
| 0x05 | UINT32 | 4 bytes |
| 0x06 | INT64 | 8 bytes |
| 0x07 | UINT64 | 8 bytes |
| 0x08 | FLOAT | 4 bytes |
| 0x09 | DOUBLE | 8 bytes |
| 0x0A | FLOAT_COMPLEX | 8 bytes |
| 0x0B | DOUBLE_COMPLEX | 16 bytes |
| 0x0E | FLOAT16 | 2 bytes |
| 0x0F | BFLOAT16 | 2 bytes |

#### Protocol Behavior

**Atomic Operations**:
- Always 8 bytes and must be naturally aligned
- Payload must be integral multiple of datatype size
- Fetching atomics return original value in Response with Data

**Constraints**:
- MUST NOT be combined with rendezvous extension
- Fetching atomics MUST NOT operate on more than one element

**Reference**: UE Spec v1.0.1, Figure 3-16, Section 3.4.2.4, Page 165

---

### 3.8 Compare-and-Swap Extension (Figure 3-17, 40 bytes)

**Datamodel**: `datamodel/protocols/ue/transport/ses/cas_extension.ksy`  
**Related Formats**: [Atomic Extension (3.7)](#37-atomic-extension-figure-3-16-8-bytes) | [Standard Request SOM=1 (3.1)](#31-standard-request-som1-table-3-8-44-bytes)

Compare-and-Swap Extension for dual-operand fetching atomics.

#### Wire Format

```
Byte:    0       1       2       3       4       5       6       7
     +-------+-------+-------+-------+-------+-------+-------+-------+
     |atomic_opcode  |atomic_datatype| semantic_control  | reserved  |
     +-------+-------+-------+-------+-------+-------+-------+-------+
         8       9      10      11      12      13      14      15
     +-------+-------+-------+-------+-------+-------+-------+-------+
     |                    compare/mask value [127:0]                 →
     +-------+-------+-------+-------+-------+-------+-------+-------+
        16      17      18      19      20      21      22      23
     +-------+-------+-------+-------+-------+-------+-------+-------+
   → |                    (compare/mask cont'd)                      |
     +-------+-------+-------+-------+-------+-------+-------+-------+
        24      25      26      27      28      29      30      31
     +-------+-------+-------+-------+-------+-------+-------+-------+
     |                       swap value [127:0]                      →
     +-------+-------+-------+-------+-------+-------+-------+-------+
        32      33      34      35      36      37      38      39
     +-------+-------+-------+-------+-------+-------+-------+-------+
   → |                       (swap value cont'd)                     |
     +-------+-------+-------+-------+-------+-------+-------+-------+
```

#### Field Definitions

| Field | Bits | Offset | Description | Constraints |
|-------|------|--------|-------------|-------------|
| atomic_opcode | 8 | 0 | Atomic operation | CSWAP*, MSWAP only |
| atomic_datatype | 8 | 1 | Data type | Per Table 3-22 |
| semantic_control | 16 | 2-3 | Semantic control | Per Table 3-23 |
| reserved | 32 | 4-7 | Reserved | Must be 0 |
| compare_mask_value | 128 | 8-23 | Compare/mask value | Low-order bytes used |
| swap_value | 128 | 24-39 | Swap value | Low-order bytes used |

#### Protocol Behavior

**Dual-Operand Atomics**:
- Compare-and-swap: compare_mask_value is compare value
- Swap-under-mask: compare_mask_value is mask value
- Payload length MUST be exactly 32 bytes
- Actual operation size determined by atomic_datatype (1-16 bytes)

**Reference**: UE Spec v1.0.1, Figure 3-17, Section 3.4.2.4, Page 166

---

### 3.9 Deferrable Send Request (Figure 3-11, 44 bytes)

**Datamodel**: `datamodel/protocols/ue/transport/ses/deferrable_send_request.ksy`  
**Related Formats**: [Ready to Restart (3.10)](#310-ready-to-restart-figure-3-12-44-bytes) | [Standard Request SOM=1 (3.1)](#31-standard-request-som1-table-3-8-44-bytes)

Deferrable Send Request for *CCL-style messaging with unexpected messages.

#### Wire Format

```
Byte:    0       1       2       3       4       5       6       7
     +-------+-------+-------+-------+-------+-------+-------+-------+
     |rs|opcode |v|dc|ie|rl|hd|eo|so|    message_id     | ri_gen  →
     +-------+-------+-------+-------+-------+-------+-------+-------+
         8       9      10      11      12      13      14      15
     +-------+-------+-------+-------+-------+-------+-------+-------+
   → |      job_id [23:0]    |rsvd|pid_on_fep |rsvd| resource_idx  →
     +-------+-------+-------+-------+-------+-------+-------+-------+
        16      17      18      19      20      21      22      23
     +-------+-------+-------+-------+-------+-------+-------+-------+
   → |    initiator_restart_token    |    target_restart_token       |
     +-------+-------+-------+-------+-------+-------+-------+-------+
        24      25      26      27      28      29      30      31
     +-------+-------+-------+-------+-------+-------+-------+-------+
     |        initiator [31:0]       |        match_bits [63:0]      →
     +-------+-------+-------+-------+-------+-------+-------+-------+
        32      33      34      35      36      37      38      39
     +-------+-------+-------+-------+-------+-------+-------+-------+
   → |  (match_bits cont'd)          |       header_data [63:0]      →
     +-------+-------+-------+-------+-------+-------+-------+-------+
        40      41      42      43
     +-------+-------+-------+-------+
   → | (hdr_data)    | request_length|
     +-------+-------+-------+-------+
```

#### Field Definitions

| Field | Bits | Offset | Description | Constraints |
|-------|------|--------|-------------|-------------|
| (standard fields) | - | 0-15 | Same as Standard Request | See Section 3.1 |
| initiator_restart_token | 32 | 16-19 | Initiator restart token | Defined by initiator |
| target_restart_token | 32 | 20-23 | Target restart token | 0 in initial request |
| initiator | 32 | 24-27 | Initiator ID | For matching |
| match_bits | 64 | 28-35 | Match bits | For matching |
| header_data | 64 | 36-43 | Header data | Completion data |

#### Protocol Behavior

**Deferrable Send Protocol**:
1. Initial send: target_restart_token = 0
2. If no buffer at target: Target sends RTR (Ready-to-Restart)
3. Restart with full restart_token from RTR
4. Restarted send MUST set ses.som = 1
5. Can restart with non-zero target_restart_token only once

**Key Difference**: buffer_offset replaced by restart_token (64 bits)

**Reference**: UE Spec v1.0.1, Figure 3-11, Section 3.4.3.4, Page 161

---

### 3.10 Ready to Restart (Figure 3-12, 44 bytes)

**Datamodel**: `datamodel/protocols/ue/transport/ses/ready_to_restart.ksy`  
**Related Formats**: [Deferrable Send (3.9)](#39-deferrable-send-request-figure-3-11-44-bytes)

Ready-to-Restart (RTR) response for deferrable send protocol.

#### Wire Format

```
Byte:    0       1       2       3       4       5       6       7
     +-------+-------+-------+-------+-------+-------+-------+-------+
     |  (standard header prefix - 12 bytes)                          |
     +-------+-------+-------+-------+-------+-------+-------+-------+
         8       9      10      11      12      13      14      15
     +-------+-------+-------+-------+-------+-------+-------+-------+
     |  (prefix cont'd)      |         buffer_offset [63:0]         →
     +-------+-------+-------+-------+-------+-------+-------+-------+
        16      17      18      19      20      21      22      23
     +-------+-------+-------+-------+-------+-------+-------+-------+
   → |  (buffer_offset cont'd)       |    initiator_restart_token    |
     +-------+-------+-------+-------+-------+-------+-------+-------+
        24      25      26      27      28      29      30      31
     +-------+-------+-------+-------+-------+-------+-------+-------+
     |    target_restart_token       |          reserved             |
     +-------+-------+-------+-------+-------+-------+-------+-------+
        32      33      34      35      36      37      38      39
     +-------+-------+-------+-------+-------+-------+-------+-------+
     |                       header_data [63:0]                      |
     +-------+-------+-------+-------+-------+-------+-------+-------+
        40      41      42      43
     +-------+-------+-------+-------+
     |       request_length          |
     +-------+-------+-------+-------+
```

#### Field Definitions

| Field | Bits | Offset | Description | Constraints |
|-------|------|--------|-------------|-------------|
| buffer_offset | 64 | 12-19 | Offset not captured | 0 to 2^32-2 |
| initiator_restart_token | 32 | 20-23 | Echo from deferrable send | From original request |
| target_restart_token | 32 | 24-27 | Allocated by target | 0 if not allocated |
| reserved | 32 | 28-31 | Reserved | Must be 0 |
| header_data | 64 | 32-39 | Header data | From original |
| request_length | 32 | 40-43 | Request length | For restart |

#### Protocol Behavior

**RTR Semantics**:
- Sent when deferrable send arrives but no buffer available
- Echoes initiator_restart_token from original send
- May allocate target_restart_token (or set to 0)
- buffer_offset indicates portion not captured

**Reference**: UE Spec v1.0.1, Figure 3-12, Section 3.4.3.4, Page 162

---

### 3.11 Optimized Non-Matching (Table 3-10, 32 bytes)

**Datamodel**: `datamodel/protocols/ue/transport/ses/optimized_non_matching.ksy`  
**Related Formats**: [Small Message (3.5)](#35-small-message-figure-3-14-32-bytes)

Optimized header for non-matching RMA operations.

#### Wire Format

```
Byte:    0       1       2       3       4       5       6       7
     +-------+-------+-------+-------+-------+-------+-------+-------+
     |opcode |v|dc|ie|rl|rs|eo|so|rs|rs| request_length  | ri_gen  →
     +-------+-------+-------+-------+-------+-------+-------+-------+
         8       9      10      11      12      13      14      15
     +-------+-------+-------+-------+-------+-------+-------+-------+
   → |      job_id [23:0]    |rsvd|pid_on_fep |rsvd| resource_idx  →
     +-------+-------+-------+-------+-------+-------+-------+-------+
        16      17      18      19      20      21      22      23
     +-------+-------+-------+-------+-------+-------+-------+-------+
   → |                    buffer_offset [63:0]                       |
     +-------+-------+-------+-------+-------+-------+-------+-------+
        24      25      26      27      28      29      30      31
     +-------+-------+-------+-------+-------+-------+-------+-------+
     |                       reserved (96 bits)                      |
     +-------+-------+-------+-------+-------+-------+-------+-------+
```

#### Field Definitions

| Field | Bits | Offset | Description | Constraints |
|-------|------|--------|-------------|-------------|
| opcode | 6 | 0[7:2] | Operation code | Per Table 3-17 |
| version | 2 | 0[1:0] | Protocol version | Must be 0 |
| (flags) | 8 | 1 | Control flags | som=eom=1 |
| request_length | 14 | 2-3[5:0] | Request length | Max 16383 bytes |
| ri_generation | 8 | 4 | RI generation | For recovery |
| job_id | 24 | 5-7 | Job ID | Target job |
| pid_on_fep | 12 | 8-9 | Process ID | Target process |
| resource_index | 12 | 10-11 | Resource index | RKEY/INDEX |
| buffer_offset | 64 | 12-19 | Buffer offset | Target offset |
| reserved | 96 | 20-31 | Reserved | Must be 0 |

#### Protocol Behavior

**Usage Criteria**:
- OPTIMIZED bit = 1 in memory region key
- RMA operation size ≤ MTU
- FI_REMOTE_CQ_DATA NOT set

**Eliminates**: initiator, match_bits, header_data, message_id

**Reference**: UE Spec v1.0.1, Table 3-10, Section 3.4.2.3, Page 163

---

### 3.12 Optimized Response with Data (Table 3-13, 16 bytes)

**Datamodel**: `datamodel/protocols/ue/transport/ses/optimized_response_with_data.ksy`  
**Related Formats**: [Response with Data (3.4)](#34-response-with-data-table-3-12-24-bytes)

Optimized response for single-packet data returns.

#### Wire Format

```
Byte:    0       1       2       3       4       5       6       7
     +-------+-------+-------+-------+-------+-------+-------+-------+
     |ls|opcode |v| ret_code|rs| payload_len | rsvd  |    job_id   →
     +-------+-------+-------+-------+-------+-------+-------+-------+
         8       9      10      11      12      13      14      15
     +-------+-------+-------+-------+-------+-------+-------+-------+
   → |  (job_id)     |      original_request_psn     |   reserved    |
     +-------+-------+-------+-------+-------+-------+-------+-------+
```

#### Field Definitions

| Field | Bits | Offset | Description | Constraints |
|-------|------|--------|-------------|-------------|
| list | 2 | 0[7:6] | List indicator | 0=expected, 1=unexpected |
| opcode | 6 | 0[5:0] | Response opcode | Per Table 3-18 |
| version | 2 | 1[7:6] | Protocol version | Must be 0 |
| return_code | 6 | 1[5:0] | Return code | Per Table 3-19 |
| payload_length | 14 | 2-3[5:0] | Payload length | Also modified_length |
| job_id | 24 | 5-7 | Job ID | From request |
| original_request_psn | 32 | 8-11 | Original PSN | For association |
| reserved | 32 | 12-15 | Reserved | Must be 0 |

#### Protocol Behavior

**Usage**:
- Response to optimized request headers
- Request length ≤ Payload MTU
- PSN used to associate response (no message_id)

**Reference**: UE Spec v1.0.1, Table 3-13, Section 3.4.2.5, Page 169

---

### 3.13 Small RMA (Figure 3-14, 32 bytes)

**Datamodel**: `datamodel/protocols/ue/transport/ses/small_rma.ksy`  
**Related Formats**: [Small Message (3.5)](#35-small-message-figure-3-14-32-bytes)

Small RMA header for single-packet RMA with matching.

#### Wire Format

Identical to Small Message (Section 3.5) with RMA opcodes (UET_WRITE, UET_READ).

#### Field Definitions

Same as Small Message. Only opcode values differ.

#### Protocol Behavior

**Usage**:
- Single-packet RMA operations
- With matching criteria
- Utilizes header_data
- No buffer_offset needed

**Reference**: UE Spec v1.0.1, Figure 3-14, Section 3.4.2.3, Page 164

---

## 4. Cross-References

### Related Documents

| Document | Content |
|----------|---------|
| [packet_taxonomy.md](packet_taxonomy.md) | Master index |
| [packet_taxonomy_ue_pds.md](packet_taxonomy_ue_pds.md) | PDS formats (carries SES) |
| [packet_taxonomy_ue_cms_tss.md](packet_taxonomy_ue_cms_tss.md) | CMS/TSS formats |

### Datamodel Files

| File | Description |
|------|-------------|
| `opcodes.ksy` | SES opcode definitions |
| `standard_request_som1.ksy` | Standard request SOM=1 (44 bytes) |
| `standard_request_som0.ksy` | Standard request SOM=0 (16 bytes) |
| `response.ksy` | Response (16 bytes) |
| `response_with_data.ksy` | Response with data (24 bytes) |
| `small_message.ksy` | Small message (32 bytes) |
| `rendezvous_extension.ksy` | Rendezvous extension (32 bytes) |
| `atomic_extension.ksy` | Atomic extension (8 bytes) |
| `cas_extension.ksy` | Compare-and-swap extension (40 bytes) |
| `deferrable_send_request.ksy` | Deferrable send request (44 bytes) |
| `ready_to_restart.ksy` | Ready to restart (44 bytes) |
| `optimized_non_matching.ksy` | Optimized non-matching (32 bytes) |
| `optimized_response_with_data.ksy` | Optimized response with data (16 bytes) |
| `small_rma.ksy` | Small RMA (32 bytes) |

---

## 5. References

- UE Specification v1.0.1, Chapter 3 (Transport Layer)
- UE Specification v1.0.1, Section 3.4 (SES)
- UE Specification v1.0.1, Tables 3-8 through 3-23
- UE Specification v1.0.1, Figures 3-14 through 3-16
