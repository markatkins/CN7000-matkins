# PMR Packet Taxonomy: UE+ PDS Formats

**Parent Document**: [packet_taxonomy.md](packet_taxonomy.md)  
**Scope**: Ultra Ethernet+ Packet Delivery Sublayer (PDS) packet formats  
**Datamodel Directory**: `datamodel/protocols/ue/transport/pds/`  
**Last Updated**: 2026-01-23

---

## Table of Contents

1. [Overview](#1-overview)
2. [PDS Prologue](#2-pds-prologue)
3. [PDS Packet Formats](#3-pds-packet-formats)
   - [3.1 RUD Request (Type 0x01)](#31-rud-request-type-0x01-12-bytes)
   - [3.2 ROD Request (Type 0x02)](#32-rod-request-type-0x02-12-bytes)
   - [3.3 RUDI Request (Type 0x04)](#33-rudi-request-type-0x04-6-bytes)
   - [3.4 RUDI Response (Type 0x05)](#34-rudi-response-type-0x05-6-bytes)
   - [3.5 UUD Request (Type 0x06)](#35-uud-request-type-0x06-6-bytes)
   - [3.6 ACK (Type 0x07)](#36-ack-type-0x07-12-bytes)
   - [3.7 ACK_CC (Type 0x08)](#37-ack_cc-type-0x08-28-bytes)
   - [3.8 ACK_CCX (Type 0x09)](#38-ack_ccx-type-0x09-44-bytes)
   - [3.9 NACK (Type 0x0A)](#39-nack-type-0x0a-12-bytes)
   - [3.10 NACK_CCX (Type 0x0C)](#310-nack_ccx-type-0x0c-28-bytes)
   - [3.11 RUD_CC_REQ / ROD_CC_REQ (Type 0x0D/0x0E)](#311-rud_cc_req--rod_cc_req-type-0x0d0x0e-28-bytes)
   - [3.12 Entropy Header](#312-entropy-header-4-bytes)
   - [3.13 Default SES Response](#313-default-ses-response-8-bytes)
   - [3.14 Control Packet (Type 0x0B)](#314-control-packet-type-0x0b-12-bytes)
4. [Cross-References](#4-cross-references)
5. [References](#5-references)

---

## 1. Overview

The Packet Delivery Sublayer (PDS) provides reliable and unreliable packet delivery services for Ultra Ethernet+. PDS sits between the network layer (UE+ L2 header) and the semantic layer (SES).

### Delivery Modes

| Mode | Type Values | Reliability | Ordering | Use Case |
|------|-------------|-------------|----------|----------|
| RUD | 0x01 | Reliable | Unordered | General RDMA |
| ROD | 0x02 | Reliable | Ordered | Streaming, multi-packet |
| RUDI | 0x04, 0x05 | Reliable | Unordered | Idempotent operations |
| UUD | 0x06 | Unreliable | Unordered | Best-effort traffic |

### Request/Response Relationships

```
PDS Request/Response Relationships:
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  UUD Request (0x06) ──────────────────────→ (no response)       │
│                                                                 │
│  RUDI Request (0x04) ─────────────────────→ RUDI Response (0x05)│
│                       └───────────────────→ NACK (0x0A)         │
│                                                                 │
│  RUD Request (0x01) ──┬───────────────────→ ACK (0x07)          │
│                       ├───────────────────→ ACK_CC (0x08)       │
│                       ├───────────────────→ ACK_CCX (0x09)      │
│                       ├───────────────────→ NACK (0x0A)         │
│                       └───────────────────→ NACK_CCX (0x0C)     │
│                                                                 │
│  ROD Request (0x02) ──┴───────────────────→ (same as RUD)       │
│                                                                 │
│  Control Packet (0x0B) ───────────────────→ (varies by subtype) │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. PDS Prologue

**Datamodel**: `datamodel/protocols/ue/transport/pds/prologue.ksy`

All PDS packets begin with a 2-byte prologue containing the packet type and flags.

```
+-------+-------+-------+-------+-------+-------+-------+-------+
| Byte 0                        | Byte 1                        |
+-------+-------+-------+-------+-------+-------+-------+-------+
| type[4:0] | next_hdr/ctl[3:0] | flags[6:0]                    |
+-------+-------+-------+-------+-------+-------+-------+-------+
```

### PDS Type Values

| PDS Type | Value | Description |
|----------|-------|-------------|
| Reserved | 0 | Reserved |
| TSS | 1 | Transport Security (encryption) |
| RUD Request | 2 | Reliable Unordered Delivery |
| ROD Request | 3 | Reliable Ordered Delivery |
| RUDI Request | 4 | Reliable Unordered Immediate |
| RUDI Response | 5 | RUDI response |
| UUD Request | 6 | Unreliable Unordered Delivery |
| ACK | 7 | Acknowledgment |
| ACK_CC | 8 | ACK with congestion control |
| ACK_CCX | 9 | ACK with extended CC |
| NACK | 10 | Negative acknowledgment |
| CP | 11 | Control packet |
| NACK_CCX | 12 | NACK with extended CC |
| RUD_CC_REQ | 13 | RUD with CC state |
| ROD_CC_REQ | 14 | ROD with CC state |

---

## 3. PDS Packet Formats

### Format Summary

| Type | Format | File | Size | Description |
|------|--------|------|------|-------------|
| 0x01 | RUD Request | `rud_rod_request.ksy` | 12 bytes | Reliable Unordered Delivery |
| 0x02 | ROD Request | `rud_rod_request.ksy` | 12 bytes | Reliable Ordered Delivery |
| 0x04 | RUDI Request | `rudi_request_response.ksy` | 6 bytes | Reliable Unordered Immediate |
| 0x05 | RUDI Response | `rudi_request_response.ksy` | 6 bytes | RUDI response |
| 0x06 | UUD Request | `uud_request.ksy` | 6 bytes | Unreliable Unordered Delivery |
| 0x07 | ACK | `rud_rod_ack.ksy` | 12 bytes | Acknowledgment |
| 0x08 | ACK_CC | `ack_cc.ksy` | 28 bytes | ACK with CC state |
| 0x09 | ACK_CCX | `ack_ccx.ksy` | 44 bytes | ACK with extended CC |
| 0x0A | NACK | `nack.ksy` | 12 bytes | Negative acknowledgment |
| 0x0B | CP | `rud_rod_cp.ksy` | 12 bytes | Control packet (10 subtypes) |
| 0x0C | NACK_CCX | `nack_ccx.ksy` | 28 bytes | NACK with extended CC |
| 0x0D | RUD_CC_REQ | `rud_rod_request_cc.ksy` | 28 bytes | RUD with CC state |
| 0x0E | ROD_CC_REQ | `rud_rod_request_cc.ksy` | 28 bytes | ROD with CC state |
| - | Entropy Header | `entropy_header.ksy` | 4 bytes | ECMP entropy (non-UDP) |
| - | Default SES | `rud_rod_default_ses.ksy` | 8 bytes | Default SES response |

---

### 3.1 RUD Request (Type 0x01, 12 bytes)

**Datamodel**: `datamodel/protocols/ue/transport/pds/rud_rod_request.ksy`  
**Related Formats**: [ROD Request (3.2)](#32-rod-request-type-0x02-12-bytes) | [ACK (3.6)](#36-ack-type-0x07-12-bytes) | [NACK (3.9)](#39-nack-type-0x0a-12-bytes)

#### Wire Format

```
Byte:    0       1       2       3       4       5       6       7
     +-------+-------+-------+-------+-------+-------+-------+-------+
     |type |nxt|flg|       clear_psn_offset |         PSN [31:0]    →
     +-------+-------+-------+-------+-------+-------+-------+-------+
         8       9      10      11
     +-------+-------+-------+-------+
   → |    spdcid     |    dpdcid     |
     +-------+-------+-------+-------+

Byte 0-1 Detail:
  Bit:  7 6 5 4 3 2 1 0 | 7 6 5 4 3 2 1 0
       |  type   |nxt_hdr| rsvd|r|a|s|rsvd|
       | (5 bits)|(4 bit)| (2) |t|r|y|(2) |
```

#### Field Definitions

| Field | Bits | Offset | Description | Constraints |
|-------|------|--------|-------------|-------------|
| type | 5 | 0[7:3] | PDS type = 0x01 (RUD) | Must be 0x01 |
| next_hdr | 4 | 0[2:0]+1[7] | SES header type | Per Table 3-16 |
| flags.rsvd | 2 | 1[6:5] | Reserved | Must be 0 |
| flags.retx | 1 | 1[4] | Retransmit indicator | 0=original, 1=retransmit |
| flags.ar | 1 | 1[3] | ACK request | 0=no ACK, 1=request ACK |
| flags.syn | 1 | 1[2] | PDC establishment | 0=normal, 1=SYN |
| flags.rsvd | 2 | 1[1:0] | Reserved | Must be 0 |
| clear_psn_offset | 16 | 2-3 | CLEAR_PSN relative to PSN | Unsigned offset |
| psn | 32 | 4-7 | Packet Sequence Number | 32-bit, wraps |
| spdcid | 16 | 8-9 | Source PDCID | Valid PDCID |
| dpdcid | 16 | 10-11 | Destination PDCID | See note below |

#### Field Notes

**PDCID Format** (Section 3.5.11.5):
- PDCID is 16 bits, carried in `spdcid` and `dpdcid` fields
- PDCID = 0 is reserved and MUST NOT be used by a PDC
- PDCIDs are locally unique at the FEP level
- `{ip.src_addr, PDCID}` MUST be globally unique
- Same PDCID MAY be reused for different destination FEPs
- Same PDCID MUST NOT be used simultaneously to same destination FEP

**dpdcid Interpretation** (depends on `syn` flag):
- `syn=0`: Destination PDCID for established PDC (16 bits)
- `syn=1`: `{pdc_info[3:0], psn_offset[11:0]}` for PDC establishment

**pdc_info Encoding** (4 bits, when `syn=1`, per Table 3-33):
| Bit | Name | Description |
|-----|------|-------------|
| 0 | use_rsv_pdc | 1=use PDC from reserved pool, 0=use global shared pool |
| 3:1 | reserved | Must be 0 |

**psn_offset** (12 bits, when `syn=1`):
- Numerical difference between PSN in this packet and Start_PSN on the PDC
- Used during PDC establishment to communicate starting sequence number
- Refer to Section 3.5.8.2 for details

**clear_psn_offset**: Computed as `CLEAR_PSN = PSN - clear_psn_offset`. Indicates the highest PSN that has been delivered to SES at the source.

#### Protocol Behavior

**Delivery Mode**: RUD (Reliable Unordered Delivery) provides reliable packet delivery without ordering guarantees. Packets may be delivered to SES out of order.

**State Machine**: RUD operates within the PDC (Packet Delivery Channel) state machine defined in Section 3.5.7.

**Transmission Rules**:
1. Source assigns monotonically increasing PSN to each packet
2. `ar` flag SHOULD be set periodically (per `ack_request_interval`)
3. `retx` flag set when retransmitting due to timeout or NACK
4. `syn` flag set only for first packet establishing new PDC

**Receiver Processing**:
1. Validate PDCID and PSN
2. If PSN is new: deliver to SES immediately (no ordering)
3. If PSN is duplicate: discard, optionally send ACK
4. If `ar=1`: generate ACK, ACK_CC, or ACK_CCX response

**Timing Constraints**:
- Retransmit timeout: Implementation-defined (typically RTT-based)
- ACK coalescing: Up to `ack_coalesce_count` packets

**Reference**: UE Spec v1.0.1, Table 3-33, Section 3.5.10.3, Page 256

---

### 3.2 ROD Request (Type 0x02, 12 bytes)

**Datamodel**: `datamodel/protocols/ue/transport/pds/rud_rod_request.ksy`  
**Related Formats**: [RUD Request (3.1)](#31-rud-request-type-0x01-12-bytes) | [ACK (3.6)](#36-ack-type-0x07-12-bytes) | [NACK (3.9)](#39-nack-type-0x0a-12-bytes)

#### Wire Format

Identical to RUD Request (Section 3.1) with `type = 0x02`.

#### Field Definitions

Same as RUD Request. Only `type` field differs.

#### Protocol Behavior

**Delivery Mode**: ROD (Reliable Ordered Delivery) provides reliable packet delivery with strict ordering guarantees. Packets are delivered to SES in PSN order.

**Key Difference from RUD**: ROD receiver MUST buffer out-of-order packets and deliver to SES only when all preceding PSNs have been received.

**Ordering Guarantee**:
- Receiver maintains expected PSN
- Out-of-order packets are buffered (not delivered)
- When gap is filled, buffered packets delivered in order
- Head-of-line blocking possible if packet lost

**Use Cases**:
- Multi-packet messages requiring in-order delivery
- Streaming data with ordering requirements
- Operations where partial delivery is not acceptable

**Reference**: UE Spec v1.0.1, Table 3-33, Section 3.5.10.3, Page 256

---

### 3.3 RUDI Request (Type 0x04, 6 bytes)

**Datamodel**: `datamodel/protocols/ue/transport/pds/rudi_request_response.ksy`  
**Related Formats**: [RUDI Response (3.4)](#34-rudi-response-type-0x05-6-bytes) | [NACK (3.9)](#39-nack-type-0x0a-12-bytes)

#### Wire Format

```
Byte:    0       1       2       3       4       5
     +-------+-------+-------+-------+-------+-------+
     |type |nxt|  flags  |         pkt_id [31:0]     |
     +-------+-------+-------+-------+-------+-------+

Byte 0-1 Detail:
  Bit:  7 6 5 4 3 2 1 0 | 7 6 5 4 3 2 1 0
       |  type   |nxt_hdr| rsvd|r|retx|rsvd|
       | (5 bits)|(4 bit)| (1) |m| (1)|(4) |
```

#### Field Definitions

| Field | Bits | Offset | Description | Constraints |
|-------|------|--------|-------------|-------------|
| type | 5 | 0[7:3] | PDS type = 0x04 (RUDI Request) | Must be 0x04 |
| next_hdr | 4 | 0[2:0]+1[7] | SES header type | Per Table 3-16 |
| flags.rsvd | 1 | 1[6] | Reserved | Must be 0 |
| flags.rsvd_m | 1 | 1[5] | Reserved (m for response) | Must be 0 for request |
| flags.retx | 1 | 1[4] | Retransmit indicator | 0=original, 1=retransmit |
| flags.rsvd | 4 | 1[3:0] | Reserved | Must be 0 |
| pkt_id | 32 | 2-5 | Packet Identifier | Locally unique |

#### Protocol Behavior

**Delivery Mode**: RUDI (Reliable Unordered Delivery with Idempotence) provides reliable delivery for idempotent operations without PDC context.

**Key Characteristics**:
- Uses packet ID instead of sequence number
- No PDC (Packet Delivery Context) required
- Idempotent: safe to retry without side effects
- Smaller header (6 bytes vs 12 bytes for RUD/ROD)

**Idempotence Guarantee**:
- Receiver tracks recently processed pkt_ids
- Duplicate pkt_ids are detected and response re-sent
- No state corruption from retransmissions

**Use Cases**:
- Small, self-contained operations
- Stateless request/response patterns
- Operations where retry is safe (reads, idempotent writes)

**Reference**: UE Spec v1.0.1, Table 3-39, Section 3.5.10.9, Page 262

---

### 3.4 RUDI Response (Type 0x05, 6 bytes)

**Datamodel**: `datamodel/protocols/ue/transport/pds/rudi_request_response.ksy`  
**Related Formats**: [RUDI Request (3.3)](#33-rudi-request-type-0x04-6-bytes)

#### Wire Format

Identical to RUDI Request with `type = 0x05` and `flags.m` valid.

#### Field Definitions

| Field | Bits | Offset | Description | Constraints |
|-------|------|--------|-------------|-------------|
| type | 5 | 0[7:3] | PDS type = 0x05 (RUDI Response) | Must be 0x05 |
| next_hdr | 4 | 0[2:0]+1[7] | SES header type | Per Table 3-16 |
| flags.rsvd | 1 | 1[6] | Reserved | Must be 0 |
| flags.m | 1 | 1[5] | ECN marked | 1 if request was ECN marked |
| flags.retx | 1 | 1[4] | Retransmit indicator | 0=original, 1=retransmit |
| flags.rsvd | 4 | 1[3:0] | Reserved | Must be 0 |
| pkt_id | 32 | 2-5 | Packet Identifier | Echoed from request |

#### Protocol Behavior

**Response Generation**:
1. Receiver processes RUDI Request
2. Generates RUDI Response with same pkt_id
3. Sets `m` flag if request packet was ECN marked

**Reference**: UE Spec v1.0.1, Table 3-39, Section 3.5.10.9, Page 262

---

### 3.5 UUD Request (Type 0x06, 6 bytes)

**Datamodel**: `datamodel/protocols/ue/transport/pds/uud_request.ksy`  
**Related Formats**: None (no response generated)

#### Wire Format

```
Byte:    0       1       2       3       4       5
     +-------+-------+-------+-------+-------+-------+
     |type |nxt|  flags  |         pkt_id [31:0]     |
     +-------+-------+-------+-------+-------+-------+

Byte 0-1 Detail:
  Bit:  7 6 5 4 3 2 1 0 | 7 6 5 4 3 2 1 0
       |  type   |nxt_hdr|     rsvd (7)    |
       | (5 bits)|(4 bit)|                 |
```

#### Field Definitions

| Field | Bits | Offset | Description | Constraints |
|-------|------|--------|-------------|-------------|
| type | 5 | 0[7:3] | PDS type = 0x06 (UUD) | Must be 0x06 |
| next_hdr | 4 | 0[2:0]+1[7] | SES header type | Per Table 3-16 |
| flags.rsvd | 7 | 1[6:0] | Reserved | Must be 0 |
| pkt_id | 32 | 2-5 | Packet Identifier | Locally unique |

#### Protocol Behavior

**Delivery Mode**: UUD (Unreliable Unordered Delivery) provides best-effort delivery with no reliability guarantees.

**Key Characteristics**:
- No ACKs or NACKs generated
- No retransmissions
- Packet loss is acceptable
- Lowest overhead delivery mode

**Use Cases**:
- Loss-tolerant traffic (video streaming, telemetry)
- High-frequency updates where latest value matters
- Multicast/broadcast scenarios

**Reference**: UE Spec v1.0.1, Table 3-42, Section 3.5.10.12, Page 265

---

### 3.6 ACK (Type 0x07, 12 bytes)

**Datamodel**: `datamodel/protocols/ue/transport/pds/rud_rod_ack.ksy`  
**Related Formats**: [RUD Request (3.1)](#31-rud-request-type-0x01-12-bytes) | [ACK_CC (3.7)](#37-ack_cc-type-0x08-28-bytes)

#### Wire Format

```
Byte:    0       1       2       3       4       5       6       7
     +-------+-------+-------+-------+-------+-------+-------+-------+
     |type |nxt|  flags  |   ack_psn_offset  |    probe_opaque     →
     +-------+-------+-------+-------+-------+-------+-------+-------+
         8       9      10      11
     +-------+-------+-------+-------+
   → |   cack_psn    |    spdcid     |    dpdcid     |
     +-------+-------+-------+-------+

Byte 0-1 Detail:
  Bit:  7 6 5 4 3 2 1 0 | 7 6 5 4 3 2 1 0
       |  type   |nxt_hdr| rsvd|m|r|p|req|rsvd|
       | (5 bits)|(4 bit)| (1) | |t| |   |(1) |
```

#### Field Definitions

| Field | Bits | Offset | Description | Constraints |
|-------|------|--------|-------------|-------------|
| type | 5 | 0[7:3] | PDS type = 0x07 (ACK) | Must be 0x07 |
| next_hdr | 4 | 0[2:0]+1[7] | SES header type | UET_HDR_NONE |
| flags.rsvd | 1 | 1[6] | Reserved | Must be 0 |
| flags.m | 1 | 1[5] | ECN marked | 1 if any ACK'd packet was ECN marked |
| flags.retx | 1 | 1[4] | Retransmit indicator | 0=original, 1=retransmit |
| flags.p | 1 | 1[3] | Probe response | 1 if responding to Probe CP |
| flags.req | 2 | 1[2:1] | Request type | 0=RUD, 1=ROD |
| flags.rsvd | 1 | 1[0] | Reserved | Must be 0 |
| ack_psn_offset | 16 | 2-3 | Offset from CACK_PSN to ACK_PSN | Signed |
| probe_opaque | 16 | 4-5 | Copied from Probe CP | Opaque value |
| cack_psn | 32 | 6-9 | Cumulative ACK PSN | Highest in-order PSN |
| spdcid | 16 | 10-11 | Source PDCID | Swapped from request |
| dpdcid | 16 | 12-13 | Destination PDCID | Swapped from request |

#### Protocol Behavior

**ACK Generation**:
1. Receiver tracks highest in-order PSN received (CACK_PSN)
2. ACK generated when `ar` flag set in request, or periodically
3. `m` flag set if any ACK'd packet had ECN marking

**Cumulative ACK**:
- `cack_psn` acknowledges all PSNs ≤ this value
- Sender can free buffers for acknowledged packets
- Enables sliding window flow control

**Reference**: UE Spec v1.0.1, Table 3-35, Section 3.5.10.5, Page 258

---

### 3.7 ACK_CC (Type 0x08, 32 bytes)

**Datamodel**: `datamodel/protocols/ue/transport/pds/ack_cc.ksy`  
**Related Formats**: [ACK (3.6)](#36-ack-type-0x07-12-bytes) | [ACK_CCX (3.8)](#38-ack_ccx-type-0x09-44-bytes) | [CMS Formats](packet_taxonomy_ue_cms_tss.md)

#### Wire Format

```
Byte:    0       1       2       3       4       5       6       7
     +-------+-------+-------+-------+-------+-------+-------+-------+
     |                    ACK Header (12 bytes)                      |
     +-------+-------+-------+-------+-------+-------+-------+-------+
         8       9      10      11      12      13      14      15
     +-------+-------+-------+-------+-------+-------+-------+-------+
     |  (ACK cont'd) |cc_typ|cc_flg|  mpr  | sack_psn_offset       →
     +-------+-------+-------+-------+-------+-------+-------+-------+
        16      17      18      19      20      21      22      23
     +-------+-------+-------+-------+-------+-------+-------+-------+
   → |              sack_bitmap [63:0]                               |
     +-------+-------+-------+-------+-------+-------+-------+-------+
        24      25      26      27      28      29      30      31
     +-------+-------+-------+-------+-------+-------+-------+-------+
     |                    ack_cc_state [63:0]                        |
     +-------+-------+-------+-------+-------+-------+-------+-------+
```

#### Field Definitions (CC Extension, bytes 12-31)

| Field | Bits | Offset | Description | Constraints |
|-------|------|--------|-------------|-------------|
| cc_type | 4 | 12[7:4] | CC algorithm type | Per Section 3.6.9 |
| cc_flags | 4 | 12[3:0] | CC flags | Reserved, must be 0 |
| mpr | 8 | 13 | Maximum PSN Range | Flow control window |
| sack_psn_offset | 16 | 14-15 | Offset to SACK base PSN | Signed |
| sack_bitmap | 64 | 16-23 | Selective ACK bitmap | 1=ACK'd, 0=not ACK'd |
| ack_cc_state | 64 | 24-31 | CC state (per cc_type) | See Section 3.6.9 |

#### CC Type Values

| Value | Name | Description |
|-------|------|-------------|
| 0x0 | CC_NSCC | Network-Signaled Congestion Control |
| 0x1 | CC_CREDIT | RCCC/TFC Credit-based CC |

#### Protocol Behavior

**Selective ACK (SACK)**:
- `sack_bitmap` covers 64 PSNs starting at `CACK_PSN + sack_psn_offset`
- Bit N = 1 means PSN (base + N) received
- Enables efficient loss recovery without full retransmit

**Congestion Control State**:
- `ack_cc_state` interpretation depends on `cc_type`
- For NSCC: Contains service_time, rcv_cwnd_pend, rcvd_bytes, ooo_count
- For CREDIT: Contains credit information

**Reference**: UE Spec v1.0.1, Table 3-36, Section 3.5.10.6, Page 259

---

### 3.8 ACK_CCX (Type 0x09, 44 bytes)

**Datamodel**: `datamodel/protocols/ue/transport/pds/ack_ccx.ksy`  
**Related Formats**: [ACK_CC (3.7)](#37-ack_cc-type-0x08-28-bytes)

#### Wire Format

ACK_CCX extends ACK_CC with additional 16 bytes for extended CC state.

```
Bytes 0-27:  ACK_CC header (28 bytes)
Bytes 28-43: Extended CC state (16 bytes)
```

#### Additional Fields (bytes 28-43)

| Field | Bits | Offset | Description |
|-------|------|--------|-------------|
| ack_ccx_state | 128 | 28-43 | Extended CC state |

#### Protocol Behavior

**Extended State**: ACK_CCX provides additional CC state for algorithms requiring more than 64 bits of feedback.

**Reference**: UE Spec v1.0.1, Table 3-37, Section 3.5.10.7, Page 260

---

### 3.9 NACK (Type 0x0A, 12 bytes)

**Datamodel**: `datamodel/protocols/ue/transport/pds/nack.ksy`  
**Related Formats**: [RUD Request (3.1)](#31-rud-request-type-0x01-12-bytes) | [NACK_CCX (3.10)](#310-nack_ccx-type-0x0c-28-bytes)

#### Wire Format

```
Byte:    0       1       2       3       4       5       6       7
     +-------+-------+-------+-------+-------+-------+-------+-------+
     |type |nxt|  flags  | nack_code |vendor_code|   nack_psn [31:0] →
     +-------+-------+-------+-------+-------+-------+-------+-------+
         8       9      10      11
     +-------+-------+-------+-------+
   → |    spdcid     |    dpdcid     |
     +-------+-------+-------+-------+

Byte 0-1 Detail:
  Bit:  7 6 5 4 3 2 1 0 | 7 6 5 4 3 2 1 0
       |  type   |nxt_hdr| rsvd|m|r|nt|rsvd|
       | (5 bits)|(4 bit)| (1) | |t|  |(3) |
```

#### Field Definitions

| Field | Bits | Offset | Description | Constraints |
|-------|------|--------|-------------|-------------|
| type | 5 | 0[7:3] | PDS type = 0x0A (NACK) | Must be 0x0A |
| next_hdr | 4 | 0[2:0]+1[7] | SES header type | UET_HDR_NONE |
| flags.rsvd | 1 | 1[6] | Reserved | Must be 0 |
| flags.m | 1 | 1[5] | ECN marked | 1 if request was ECN marked |
| flags.retx | 1 | 1[4] | Retransmit indicator | From request |
| flags.nt | 1 | 1[3] | NACK type | 0=RUD/ROD, 1=RUDI |
| flags.rsvd | 3 | 1[2:0] | Reserved | Must be 0 |
| nack_code | 8 | 2 | NACK reason code | Per Table 3-59 |
| vendor_code | 8 | 3 | Vendor-specific code | Optional |
| nack_psn | 32 | 4-7 | NACK'd PSN or pkt_id | Depends on nt flag |
| spdcid | 16 | 8-9 | Source PDCID | 0 if nt=1 or PDC failure |
| dpdcid | 16 | 10-11 | Destination PDCID | 0 if nt=1 |

#### NACK Codes (Table 3-59)

| Code | Name | Description |
|------|------|-------------|
| 0x00 | UET_NO_PKT_BUF | No packet buffer available |
| 0x01 | UET_TRIMMED | Packet was trimmed |
| 0x02 | UET_NO_PDC_AVAIL | No PDC resources available |
| 0x03 | UET_INV_DPDCID | Invalid destination PDCID |
| 0x04 | UET_PDC_HDR_MISMATCH | PDC header mismatch |
| 0x05 | UET_PSN_OOR_WINDOW | PSN outside expected window |
| 0x06 | UET_PSN_GAP | PSN gap detected (packet loss) |

#### Protocol Behavior

**NACK Generation**:
1. Receiver detects error condition (loss, resource exhaustion, etc.)
2. Generates NACK with appropriate nack_code
3. Sender receives NACK and takes corrective action

**Sender Response to NACK**:
- `UET_PSN_GAP`: Retransmit missing packets
- `UET_NO_PKT_BUF`: Back off, retry later
- `UET_NO_PDC_AVAIL`: PDC establishment failed, retry or abort

**Reference**: UE Spec v1.0.1, Table 3-40, Section 3.5.10.10, Page 263

---

### 3.10 NACK_CCX (Type 0x0C, 28 bytes)

**Datamodel**: `datamodel/protocols/ue/transport/pds/nack_ccx.ksy`  
**Related Formats**: [NACK (3.9)](#39-nack-type-0x0a-12-bytes)

#### Wire Format

NACK_CCX extends NACK with 16 bytes of CC state (similar to ACK_CC extension).

```
Bytes 0-11:  NACK header (12 bytes)
Bytes 12-27: CC extension (16 bytes)
```

#### Protocol Behavior

**Extended NACK**: NACK_CCX provides congestion control feedback along with the negative acknowledgment, enabling the sender to adjust its rate while handling the error.

**Reference**: UE Spec v1.0.1, Table 3-41, Section 3.5.10.11, Page 264

---

### 3.11 RUD_CC_REQ / ROD_CC_REQ (Type 0x0D/0x0E, 28 bytes)

**Datamodel**: `datamodel/protocols/ue/transport/pds/rud_rod_request_cc.ksy`  
**Related Formats**: [RUD Request (3.1)](#31-rud-request-type-0x01-12-bytes) | [ACK_CC (3.7)](#37-ack_cc-type-0x08-28-bytes) | [CMS Formats](packet_taxonomy_ue_cms_tss.md)

RUD/ROD Request with Congestion Control State extends the standard request with CC state.

#### Wire Format

```
Byte:    0       1       2       3       4       5       6       7
     +-------+-------+-------+-------+-------+-------+-------+-------+
     |type |nxt|flg|       clear_psn_offset |         PSN [31:0]    →
     +-------+-------+-------+-------+-------+-------+-------+-------+
         8       9      10      11      12      13      14      15
     +-------+-------+-------+-------+-------+-------+-------+-------+
   → |    spdcid     |    dpdcid     |       req_cc_state [127:0]   →
     +-------+-------+-------+-------+-------+-------+-------+-------+
        16      17      18      19      20      21      22      23
     +-------+-------+-------+-------+-------+-------+-------+-------+
   → |                    (req_cc_state cont'd)                      |
     +-------+-------+-------+-------+-------+-------+-------+-------+
        24      25      26      27
     +-------+-------+-------+-------+
   → |  (req_cc_state cont'd)        |
     +-------+-------+-------+-------+
```

#### Field Definitions

| Field | Bits | Offset | Description | Constraints |
|-------|------|--------|-------------|-------------|
| type | 5 | 0[7:3] | PDS type = 0x0D (RUD_CC) or 0x0E (ROD_CC) | Must be 0x0D or 0x0E |
| next_hdr | 4 | 0[2:0]+1[7] | SES header type | Per Table 3-16 |
| flags | 7 | 1[6:0] | Same as RUD/ROD Request | See Section 3.1 |
| clear_psn_offset | 16 | 2-3 | CLEAR_PSN relative to PSN | Unsigned offset |
| psn | 32 | 4-7 | Packet Sequence Number | 32-bit, wraps |
| spdcid | 16 | 8-9 | Source PDCID | Valid PDCID |
| dpdcid | 16 | 10-11 | Destination PDCID | Or {pdc_info, psn_offset} |
| req_cc_state | 128 | 12-27 | Request CC state | Per Section 3.6.9.1 |

#### Protocol Behavior

**CC State Contents**: The `req_cc_state` field contents depend on the congestion control algorithm:
- **NSCC**: Source congestion state (sent_bytes, cwnd_bytes)
- **RCCC/TFC**: Credit request information

**Use Cases**:
- Requests requiring congestion control feedback
- Used with NSCC, RCCC, or TFC algorithms
- Carries source congestion state to destination

**Reference**: UE Spec v1.0.1, Table 3-34, Section 3.5.10.4, Page 257

---

### 3.12 Entropy Header (4 bytes)

**Datamodel**: `datamodel/protocols/ue/transport/pds/entropy_header.ksy`  
**Related Formats**: [PDS Prologue (2)](#2-pds-prologue)

UET Entropy Header for path selection when UDP is not used.

#### Wire Format

```
Byte:    0       1       2       3
     +-------+-------+-------+-------+
     |     entropy [15:0]    |   reserved    |
     +-------+-------+-------+-------+
```

#### Field Definitions

| Field | Bits | Offset | Description | Constraints |
|-------|------|--------|-------------|-------------|
| entropy | 16 | 0-1 | Entropy value for ECMP | Flow hash |
| reserved | 16 | 2-3 | Reserved | Must be 0 |

#### Protocol Behavior

**Usage**:
- Present when using native IPv4 or IPv6 encapsulation (no UDP)
- MUST NOT be present when using UDP encapsulation
- Positioned at same location as UDP source port
- Enables consistent switch behavior for ECMP

**Reference**: UE Spec v1.0.1, Table 3-31, Section 3.5.10.1, Page 254

---

### 3.13 Default SES Response (8 bytes)

**Datamodel**: `datamodel/protocols/ue/transport/pds/rud_rod_default_ses.ksy`  
**Related Formats**: [Response](packet_taxonomy_ue_ses.md#23-response-16-bytes) | [ACK (3.6)](#36-ack-type-0x07-12-bytes)

Default SES Response generated by PDS for duplicate packets.

#### Wire Format

```
Byte:    0       1       2       3       4       5       6       7
     +-------+-------+-------+-------+-------+-------+-------+-------+
     |ls|opcode |v| ret_code|   message_id  | ri_gen|    job_id     |
     +-------+-------+-------+-------+-------+-------+-------+-------+

Byte 0-1 Detail:
  Bit:  7 6 5 4 3 2 1 0 | 7 6 5 4 3 2 1 0
       |list |  opcode |v| return_code   |
       | (2) | (6 bits)|r|   (6 bits)    |
```

#### Field Definitions

| Field | Bits | Offset | Description | Constraints |
|-------|------|--------|-------------|-------------|
| list | 2 | 0[7:6] | List indicator | Must be 0 (state not known) |
| opcode | 6 | 0[5:0] | Response opcode | UET_DEFAULT_RESPONSE or UET_NO_RESPONSE |
| version | 2 | 1[7:6] | Protocol version | Must be 0 |
| return_code | 6 | 1[5:0] | Return code | RC_NULL or RC_OKAY |
| message_id | 16 | 2-3 | Message ID | From duplicate request or 0 |
| ri_generation | 8 | 4 | Resource Index generation | Must be 0 |
| job_id | 24 | 5-7 | Job Identifier | From duplicate request or 0 |

#### Protocol Behavior

**Generation Triggers**:
- Duplicate PDS Request packet received
- ACK Request CP received for already-received PSN

**Purpose**:
- Reduces state storage requirements
- Alleviates need to store SES response for every packet
- Provides limited response information

**Reference**: UE Spec v1.0.1, Table 3-43, Section 3.5.10.13, Page 265

---

### 3.14 Control Packet (Type 0x0B, 12 bytes)

**Datamodel**: `datamodel/protocols/ue/transport/pds/rud_rod_cp.ksy`  
**Related Formats**: [RUD Request (3.1)](#31-rud-request-type-0x01-12-bytes) | [ACK (3.6)](#36-ack-type-0x07-12-bytes)

#### Wire Format

```
Byte:    0       1       2       3       4       5       6       7
     +-------+-------+-------+-------+-------+-------+-------+-------+
     |type |ctl|  flags  |   probe_opaque    |         PSN [31:0]  →
     +-------+-------+-------+-------+-------+-------+-------+-------+
         8       9      10      11
     +-------+-------+-------+-------+
   → |    spdcid     |    dpdcid     |
     +-------+-------+-------+-------+

Byte 0-1 Detail:
  Bit:  7 6 5 4 3 2 1 0 | 7 6 5 4 3 2 1 0
       |  type   |ctl_typ| rsvd|i|r|a|s|rsvd|
       | (5 bits)|(4 bit)| (1) |r|t|r|y|(2) |
```

#### Field Definitions

| Field | Bits | Offset | Description | Constraints |
|-------|------|--------|-------------|-------------|
| type | 5 | 0[7:3] | PDS type = 0x0B (CP) | Must be 0x0B |
| ctl_type | 4 | 0[2:0]+1[7] | Control packet subtype | 0-9 defined |
| flags.rsvd | 1 | 1[6] | Reserved | Must be 0 |
| flags.isrod | 1 | 1[5] | ROD indicator | 1=ROD, 0=RUD (for NOOP/Negotiation) |
| flags.retx | 1 | 1[4] | Retransmit indicator | 0=original, 1=retransmit |
| flags.ar | 1 | 1[3] | ACK request | 0=no ACK, 1=request ACK |
| flags.syn | 1 | 1[2] | PDC establishment | 0=normal, 1=SYN |
| flags.rsvd | 2 | 1[1:0] | Reserved | Must be 0 |
| probe_opaque | 16 | 2-3 | Opaque value for Probe | Echoed in ACK |
| psn | 32 | 4-7 | Packet Sequence Number | Some CPs consume PSN |
| spdcid | 16 | 8-9 | Source PDCID | Valid PDCID |
| dpdcid | 16 | 10-11 | Destination PDCID | Or {pdc_info, psn_offset} |

#### Control Packet Subtypes

| ctl_type | Name | Direction | Description |
|----------|------|-----------|-------------|
| 0 | NOOP | Either | No operation |
| 1 | ACK_REQUEST | Src→Dst | Request ACK for specific PSN |
| 2 | CLEAR_COMMAND | Init→Tgt | Clear guaranteed delivery state |
| 3 | CLEAR_REQUEST | Tgt→Init | Request initiator to send clear |
| 4 | CLOSE_COMMAND | Init→Tgt | PDC is being closed |
| 5 | CLOSE_REQUEST | Tgt→Init | Request initiator to close PDC |
| 6 | PROBE | Src→Dst | Request PDS ACK |
| 7 | CREDIT | Dst→Src | Carry CC credit |
| 8 | CREDIT_REQUEST | Src→Dst | Request credit |
| 9 | NEGOTIATION | Either | PDC negotiation |

#### Protocol Behavior

**PDC Lifecycle**:
- `CLOSE_COMMAND/REQUEST`: Graceful PDC teardown
- `CLEAR_COMMAND/REQUEST`: Clear delivery state without closing

**Flow Control**:
- `CREDIT/CREDIT_REQUEST`: Credit-based flow control
- `PROBE`: Solicit ACK for RTT measurement or liveness check

**Reference**: UE Spec v1.0.1, Table 3-38, Section 3.5.10.8, Page 261

---

## 4. Cross-References

### Related Documents

| Document | Content |
|----------|---------|
| [packet_taxonomy.md](packet_taxonomy.md) | Master index |
| [packet_taxonomy_ue_ses.md](packet_taxonomy_ue_ses.md) | SES formats (carried by PDS) |
| [packet_taxonomy_ue_cms_tss.md](packet_taxonomy_ue_cms_tss.md) | CMS/TSS formats (CC state details) |
| [packet_taxonomy_ue_link.md](packet_taxonomy_ue_link.md) | Link layer formats |

### Datamodel Files

| File | Description |
|------|-------------|
| `prologue.ksy` | PDS prologue (2 bytes) |
| `rud_rod_request.ksy` | RUD/ROD request (12 bytes) |
| `rudi_request_response.ksy` | RUDI request/response (6 bytes) |
| `uud_request.ksy` | UUD request (6 bytes) |
| `rud_rod_ack.ksy` | ACK (12 bytes) |
| `ack_cc.ksy` | ACK_CC (28 bytes) |
| `ack_ccx.ksy` | ACK_CCX (44 bytes) |
| `nack.ksy` | NACK (12 bytes) |
| `nack_ccx.ksy` | NACK_CCX (28 bytes) |
| `rud_rod_cp.ksy` | Control Packet (12 bytes) |
| `rud_rod_request_cc.ksy` | RUD/ROD Request with CC (28 bytes) |
| `entropy_header.ksy` | Entropy Header (4 bytes) |
| `rud_rod_default_ses.ksy` | Default SES Response (8 bytes) |

---

## 5. References

- UE Specification v1.0.1, Chapter 3 (Transport Layer)
- UE Specification v1.0.1, Section 3.5 (PDS)
- UE Specification v1.0.1, Tables 3-33 through 3-42
