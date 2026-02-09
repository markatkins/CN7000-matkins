# PMR Packet Taxonomy: UE+ CMS and TSS Formats

**Parent Document**: [packet_taxonomy.md](packet_taxonomy.md)  
**Scope**: Ultra Ethernet+ Congestion Management Sublayer (CMS) and Transport Security Sublayer (TSS)  
**Datamodel Directory**: `datamodel/protocols/ue/transport/cms/` and `datamodel/protocols/ue/transport/tss/`  
**Last Updated**: 2026-01-26

---

## Table of Contents

1. [Overview](#1-overview)
2. [CMS Formats](#2-cms-formats)
   - [2.1 ACK CC State - NSCC](#21-ack-cc-state---nscc-8-bytes)
   - [2.2 ACK CC State - RCCC/TFC](#22-ack-cc-state---rccctfc-8-bytes)
   - [2.3 Request CC State](#23-request-cc-state-8-bytes)
   - [2.4 CCC State Machine](#24-ccc-state-machine)
   - [2.5 NSCC Protocol](#25-nscc-protocol)
   - [2.6 RCCC Protocol](#26-rccc-protocol)
   - [2.7 TFC Protocol](#27-tfc-protocol)
   - [2.8 Multipath Selection](#28-multipath-selection)
3. [TSS Formats](#3-tss-formats)
   - [3.1 Security Header](#31-security-header-12-16-bytes)
4. [Cross-References](#4-cross-references)
5. [References](#5-references)

---

## 1. Overview

### Congestion Management Sublayer (CMS)

CMS provides congestion control mechanisms for Ultra Ethernet+. It supports multiple algorithms:

| Algorithm | Type | Description |
|-----------|------|-------------|
| NSCC | Network-Signaled | Destination signals congestion to source |
| RCCC | Credit-Based | Receiver-controlled credit flow |
| TFC | Credit-Based | Traffic-class flow control |

### Transport Security Sublayer (TSS)

TSS provides encryption and authentication for UE+ packets using AES-GCM.

| Feature | Description |
|---------|-------------|
| Encryption | AES-GCM (128/256-bit keys) |
| Authentication | GCM authentication tag |
| IV Construction | SSI + TSC or IP.src + TSC |
| Secure Domains | 24-bit domain identifier |

### CMS State Flow

```
CMS State Flow:
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  Request CC State ────────────────→ (carried in RUD/ROD_CC_REQ) │
│       │                                                         │
│       └──→ ACK CC State (NSCC) ───→ (carried in ACK_CC/ACK_CCX) │
│            ACK CC State (RCCC) ───→ (carried in ACK_CC/ACK_CCX) │
│                                                                 │
│  Credit CP Payload ───────────────→ (carried in CP type=7)      │
│  Credit Request CP Payload ───────→ (carried in CP type=8)      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. CMS Formats

**Datamodel Directory**: `datamodel/protocols/ue/transport/cms/`

### Format Summary

| Format | File | Size | Description |
|--------|------|------|-------------|
| ACK CC State (NSCC) | `ack_cc_state_nscc.ksy` | 8 bytes | NSCC congestion state |
| ACK CC State (RCCC/TFC) | `ack_cc_state_rccc_tfc.ksy` | 8 bytes | Credit-based CC state |
| Request CC State | `req_cc_state.ksy` | 8 bytes | Source CC state |
| Credit CP Payload | `credit_cp_payload.ksy` | Variable | Credit control packet |
| Credit Request | `credit_request_cp_payload.ksy` | Variable | Credit request |

---

### 2.1 ACK CC State - NSCC (8 bytes)

**Datamodel**: `datamodel/protocols/ue/transport/cms/ack_cc_state_nscc.ksy`  
**Related Formats**: [ACK_CC](packet_taxonomy_ue_pds.md#37-ack_cc-type-0x08-28-bytes)

Carried in `pds.ack_cc_state` when `pds.cc_type = CC_NSCC`.

#### Wire Format

```
Byte:    0       1       2       3       4       5       6       7
     +-------+-------+-------+-------+-------+-------+-------+-------+
     |    service_time     |r|rcv_cwnd|       rcvd_bytes            |
     |      [15:0]         |c| _pend  |         [23:0]              |
     +-------+-------+-------+-------+-------+-------+-------+-------+
         (cont'd)                      |        ooo_count           |
     +-------+-------+-------+-------+-------+-------+-------+-------+

Byte 2 Detail:
  Bit:  7 6 5 4 3 2 1 0
       |r|rcv_cwnd_pend |
       |c|   (7 bits)   |
```

#### Field Definitions

| Field | Bits | Offset | Description | Constraints |
|-------|------|--------|-------------|-------------|
| service_time | 16 | 0-1 | Destination service time | Units: 128 ns |
| rc | 1 | 2[7] | Restore cwnd flag | Boolean |
| rcv_cwnd_pend | 7 | 2[6:0] | Congestion level | 0-127 |
| rcvd_bytes | 24 | 3-5 | Received byte count | Units: 256 bytes, wraps |
| ooo_count | 16 | 6-7 | Out-of-order count | Instantaneous, 0xFFFF=invalid |

#### Field Notes

**service_time**:
- Units: 128 nanoseconds
- Accuracy target: ~500 ns
- 0x0000: Not valid (MUST be ignored)
- 0xFFFF: Exceeded 8.38848 ms

**rcvd_bytes**:
- Units: 256 bytes
- Wraps at 0xFFFFFF
- Cumulative per PDC

**ooo_count**:
- Instantaneous (not cumulative)
- Does not wrap
- 0xFFFF: Field invalid (destination doesn't calculate)

#### Protocol Behavior

**NSCC Algorithm**:
1. Destination measures service_time (MAC-to-MAC)
2. Destination tracks rcvd_bytes and ooo_count
3. Destination sets rcv_cwnd_pend based on congestion
4. Source adjusts cwnd based on received state

**Reference**: UE Spec v1.0.1, Table 3-74, Section 3.6.9.2, Page 366

---

### 2.2 ACK CC State - RCCC/TFC (8 bytes)

**Datamodel**: `datamodel/protocols/ue/transport/cms/ack_cc_state_rccc_tfc.ksy`  
**Related Formats**: [ACK_CC](packet_taxonomy_ue_pds.md#37-ack_cc-type-0x08-28-bytes)

Carried in `pds.ack_cc_state` when `pds.cc_type = CC_CREDIT`.

#### Wire Format

```
Byte:    0       1       2       3       4       5       6       7
     +-------+-------+-------+-------+-------+-------+-------+-------+
     |    credit_granted   |    credit_limit   |      reserved       |
     |       [15:0]        |       [15:0]      |       [31:0]        |
     +-------+-------+-------+-------+-------+-------+-------+-------+
```

#### Field Definitions

| Field | Bits | Offset | Description | Constraints |
|-------|------|--------|-------------|-------------|
| credit_granted | 16 | 0-1 | Credits granted | Units: packets or bytes |
| credit_limit | 16 | 2-3 | Maximum credits | Upper bound |
| reserved | 32 | 4-7 | Reserved | Must be 0 |

#### Protocol Behavior

**Credit-Based CC**:
- Receiver grants credits to sender
- Sender cannot exceed granted credits
- Prevents receiver buffer overflow

**Reference**: UE Spec v1.0.1, Table 3-75, Section 3.6.9.3

---

### 2.3 Request CC State (8 bytes)

**Datamodel**: `datamodel/protocols/ue/transport/cms/req_cc_state.ksy`  
**Related Formats**: [RUD Request](packet_taxonomy_ue_pds.md#31-rud-request-type-0x01-12-bytes)

Carried in RUD_CC_REQ and ROD_CC_REQ packets.

#### Wire Format

```
Byte:    0       1       2       3       4       5       6       7
     +-------+-------+-------+-------+-------+-------+-------+-------+
     |     sent_bytes      |    cwnd_bytes     |      reserved       |
     |       [15:0]        |       [15:0]      |       [31:0]        |
     +-------+-------+-------+-------+-------+-------+-------+-------+
```

#### Field Definitions

| Field | Bits | Offset | Description | Constraints |
|-------|------|--------|-------------|-------------|
| sent_bytes | 16 | 0-1 | Bytes sent | Units: 256 bytes |
| cwnd_bytes | 16 | 2-3 | Congestion window | Current cwnd |
| reserved | 32 | 4-7 | Reserved | Must be 0 |

#### Protocol Behavior

**Source State**:
- Communicates source congestion state to destination
- Enables destination to make informed decisions

**Reference**: UE Spec v1.0.1, Section 3.6.9.1

---

### 2.4 CCC State Machine

**Datamodel**: `datamodel/protocols/ue/transport/cms/protocols/ccc_state_machine.ksy`  
**UE Spec Reference**: Section 3.6.6, Figure 3-98, Page 362

The Congestion Control Context (CCC) State Machine controls when PDCs associated with a CCC can send data. It coordinates between the congestion control algorithm (NSCC, RCCC, or TFC) and the PDC scheduler.

#### States

| State | Description |
|-------|-------------|
| **IDLE** | No pending data, all ACKed. CCC can be removed. |
| **ACTIVE** | Data to send but CC does not permit (window/credit exhausted). |
| **READY** | Data to send and CC permits. Scheduler can select PDCs. |
| **PENDING** | All data sent, waiting for ACKs. |

#### State Diagram

```
IDLE ──[new data]──> ACTIVE ──[CC permits]──> READY
  ^                    ^                        │
  │                    │                        │
  │                    └──[CC exhausted]────────┘
  │                    │
  │                    └──[retransmit needed]───┐
  │                                             │
  └──[all ACKed]──── PENDING <──[all sent]──────┘
```

#### Key Behaviors

- Multiple PDCs can share a single CCC (same destination, same TC)
- CCC tracks aggregate bytes in flight across all associated PDCs
- NSCC uses congestion window (cwnd) to control sending
- RCCC/TFC use credit from destination to control sending
- Scheduler selects PDCs when CCC is in READY state

---

### 2.5 NSCC Protocol

**Datamodel**: 
- `datamodel/protocols/ue/transport/cms/protocols/nscc_source.ksy`
- `datamodel/protocols/ue/transport/cms/protocols/nscc_destination.ksy`

**UE Spec Reference**: Sections 3.6.13.3-3.6.13.9, Pages 381-390

Network Signal-based Congestion Control (NSCC) is a window-based algorithm that runs primarily at the source, using network signals (ECN, RTT) to adjust the congestion window.

#### NSCC Source States

| State | Description |
|-------|-------------|
| **IDLE** | No active flows |
| **SLOW_START** | Exponential window growth |
| **CONG_AVOID** | Linear window growth (congestion avoidance) |
| **FAST_RECOVERY** | Recovery after loss detection |

#### NSCC Destination States

| State | Description |
|-------|-------------|
| **IDLE** | No active flows |
| **MONITOR** | Monitoring incoming traffic |
| **SIGNAL_CONGESTION** | Signaling congestion to source |

#### Key Parameters

| Parameter | Description | UE Spec Reference |
|-----------|-------------|-------------------|
| cwnd | Congestion window (bytes) | Table 3-77 |
| ssthresh | Slow start threshold | Table 3-77 |
| target_qdelay | Target queuing delay | Section 3.6.13.3 |
| base_rtt | Base round-trip time | Section 3.6.13.3 |

#### Protocol Behavior

- Source adjusts cwnd based on ECN marks and RTT measurements
- Destination measures service_time and reports in ACK_CC
- Uses AIMD (Additive Increase, Multiplicative Decrease)
- Supports packet trimming for faster congestion detection

**Reference**: UE Spec v1.0.1, Section 3.6.13

---

### 2.6 RCCC Protocol

**Datamodel**: 
- `datamodel/protocols/ue/transport/cms/protocols/rccc_source.ksy`
- `datamodel/protocols/ue/transport/cms/protocols/rccc_destination.ksy`

**UE Spec Reference**: Sections 3.6.14.2-3.6.14.6, Pages 393-398

Receiver-Controlled Congestion Control (RCCC) is a credit-based algorithm where the destination controls the rate at which sources can send, providing explicit incast control.

#### RCCC Source States

| State | Description |
|-------|-------------|
| **IDLE** | No active flows |
| **RATE_CONTROL** | Sending at credit-controlled rate |
| **BACKOFF** | Backing off due to credit exhaustion |

#### RCCC Destination States

| State | Description |
|-------|-------------|
| **IDLE** | No active flows |
| **MONITOR_BUFFER** | Monitoring receive buffer usage |
| **REQUEST_REDUCTION** | Requesting sources to reduce rate |

#### Key Parameters

| Parameter | Description | UE Spec Reference |
|-----------|-------------|-------------------|
| credit | Available credit (bytes) | Table 3-79 |
| credit_target | Requested credit | Table 3-79 |
| max_wnd | Maximum window | Table 3-80 |

#### Protocol Behavior

- Destination grants credit to sources via Credit CP or ACK_CC
- Source cannot send more than granted credit
- Prevents receiver buffer overflow (incast control)
- Works best on non-blocking fat-tree topologies

**Reference**: UE Spec v1.0.1, Section 3.6.14

---

### 2.7 TFC Protocol

**Datamodel**: 
- `datamodel/protocols/ue/transport/cms/protocols/tfc_source.ksy`
- `datamodel/protocols/ue/transport/cms/protocols/tfc_destination.ksy`

**UE Spec Reference**: Section 3.6.15, Pages 398-404

Transport Flow Control (TFC) provides point-to-point flow control for managing receive buffer resources at the destination.

#### TFC Source States

| State | Description |
|-------|-------------|
| **IDLE** | No active flows |
| **FLOW_CONTROL** | Sending at flow-controlled rate |
| **THROTTLE** | Throttled due to buffer pressure |

#### TFC Destination States

| State | Description |
|-------|-------------|
| **IDLE** | No active flows |
| **MONITOR** | Monitoring buffer state |
| **SIGNAL_THROTTLE** | Signaling throttle to source |

#### Key Parameters

| Parameter | Description | UE Spec Reference |
|-----------|-------------|-------------------|
| tfc_credit | TFC credit (cells) | Section 3.6.15.2 |
| tfc_dest_cell_size | Destination cell size | Section 3.6.15.2 |
| tfc_pkt_overhead | Per-packet overhead | Section 3.6.15.2 |

#### Protocol Behavior

- Credit-based flow control at cell granularity
- Destination allocates buffer cells to sources
- Source consumes credit based on packet size + overhead
- Designed for point-to-point flow control

**Reference**: UE Spec v1.0.1, Section 3.6.15

---

### 2.8 Multipath Selection

**Datamodel**: `datamodel/protocols/ue/transport/cms/protocols/multipath_selection.ksy`  
**UE Spec Reference**: Section 3.6.16, Pages 404-409

Multipath path selection enables load balancing across multiple network paths using entropy-based ECMP.

#### States

| State | Description |
|-------|-------------|
| **IDLE** | No active path selection |
| **SELECT_PATH** | Selecting path for packet |
| **MONITOR_PATHS** | Monitoring path congestion |

#### Key Concepts

| Concept | Description |
|---------|-------------|
| **Entropy** | 16-bit value in UDP src_port or UET entropy header |
| **ECMP** | Equal-Cost Multi-Path routing |
| **Path Congestion** | Tracked per entropy value via ECN |

#### Protocol Behavior

- CMS assigns entropy value to each packet
- Switches use entropy for ECMP path selection
- Source tracks congestion per entropy value
- Congested paths avoided by changing entropy
- Supports per-packet or per-flow spraying

**Reference**: UE Spec v1.0.1, Section 3.6.16

---

## 3. TSS Formats

**Datamodel Directory**: `datamodel/protocols/ue/transport/tss/`

### Format Summary

| Format | File | Size | Description |
|--------|------|------|-------------|
| Security Header | `security_header.ksy` | 12-16 bytes | Encryption header |
| IV Construction | `iv_construction.ksy` | 12 bytes | Initialization vector |

---

### 3.1 Security Header (12-16 bytes)

**Datamodel**: `datamodel/protocols/ue/transport/tss/security_header.ksy`  
**Related Formats**: [PDS Prologue](packet_taxonomy_ue_pds.md#2-pds-prologue)

TSS header for AES-GCM encryption.

#### Wire Format (sp=1, 16 bytes)

```
Byte:    0       1       2       3       4       5       6       7
     +-------+-------+-------+-------+-------+-------+-------+-------+
     |type|sp|r|an|         sdi [23:0]        |      ssi [31:0]     |
     +-------+-------+-------+-------+-------+-------+-------+-------+
         8       9      10      11      12      13      14      15
     +-------+-------+-------+-------+-------+-------+-------+-------+
     |                        tsc [63:0]                             |
     |              epoch [15:0]  |        counter [47:0]            |
     +-------+-------+-------+-------+-------+-------+-------+-------+

Byte 0 Detail:
  Bit:  7 6 5 4 3 2 1 0
       |  type   |s|r|a|
       | (5 bit) |p| |n|
```

#### Wire Format (sp=0, 12 bytes)

```
Byte:    0       1       2       3       4       5       6       7
     +-------+-------+-------+-------+-------+-------+-------+-------+
     |type|sp|r|an|         sdi [23:0]        |      tsc [63:0]     →
     +-------+-------+-------+-------+-------+-------+-------+-------+
         8       9      10      11
     +-------+-------+-------+-------+
   → |    (tsc cont'd)               |
     +-------+-------+-------+-------+
```

#### Field Definitions

| Field | Bits | Offset | Description | Constraints |
|-------|------|--------|-------------|-------------|
| type | 5 | 0[7:3] | Header type | Must be 1 (UET_TSS) |
| sp | 1 | 0[2] | SSI present | 1=SSI included |
| reserved | 1 | 0[1] | Reserved | Must be 0 |
| an | 1 | 0[0] | Association number | Key association |
| sdi | 24 | 1-3 | Secure Domain ID | Domain identifier |
| ssi | 32 | 4-7 | Source Identifier | Present if sp=1 |
| tsc | 64 | 4-11 or 8-15 | Timestamp Counter | epoch(16) + counter(48) |

#### TSC Structure

| Field | Bits | Description |
|-------|------|-------------|
| epoch | 16 | Key epoch (upper 16 bits) |
| counter | 48 | Packet counter (lower 48 bits) |

#### IV Construction

The Initialization Vector for AES-GCM is constructed as:

| sp | IV Construction |
|----|-----------------|
| 1 | IV = SSI (32 bits) \|\| TSC (64 bits) = 96 bits |
| 0 | IV = IP.src_addr (32 bits) \|\| TSC (64 bits) = 96 bits |

#### Protocol Behavior

**Encryption**:
1. TSS header placed after PDS prologue
2. Payload encrypted with AES-GCM
3. Authentication tag appended

**Secure Domains**:
- SDI identifies the security domain
- Keys are per-domain
- AN selects active key (for rotation)

**Reference**: UE Spec v1.0.1, Table 3-90, Section 3.7.11, Page 441

---

## 4. Cross-References

### Related Documents

| Document | Content |
|----------|---------|
| [packet_taxonomy.md](packet_taxonomy.md) | Master index |
| [packet_taxonomy_ue_pds.md](packet_taxonomy_ue_pds.md) | PDS formats (carries CMS/TSS) |
| [packet_taxonomy_ue_ses.md](packet_taxonomy_ue_ses.md) | SES formats |

### Datamodel Files

#### CMS Wire Formats

| File | Description |
|------|-------------|
| `cms/ack_cc_state_nscc.ksy` | NSCC congestion state (8 bytes) |
| `cms/ack_cc_state_rccc_tfc.ksy` | RCCC/TFC credit state (8 bytes) |
| `cms/req_cc_state.ksy` | Request CC state (8 bytes) |
| `cms/credit_cp_payload.ksy` | Credit CP payload |
| `cms/credit_request_cp_payload.ksy` | Credit request payload |

#### CMS Protocol Definitions

| File | Description | UE Spec Section |
|------|-------------|-----------------|
| `cms/protocols/ccc_state_machine.ksy` | CCC state machine | 3.6.6 |
| `cms/protocols/nscc_source.ksy` | NSCC source algorithm | 3.6.13.3-3.6.13.6 |
| `cms/protocols/nscc_destination.ksy` | NSCC destination algorithm | 3.6.13.9 |
| `cms/protocols/rccc_source.ksy` | RCCC source algorithm | 3.6.14.2-3.6.14.4 |
| `cms/protocols/rccc_destination.ksy` | RCCC destination algorithm | 3.6.14.6 |
| `cms/protocols/tfc_source.ksy` | TFC source algorithm | 3.6.15 |
| `cms/protocols/tfc_destination.ksy` | TFC destination algorithm | 3.6.15 |
| `cms/protocols/multipath_selection.ksy` | Multipath path selection | 3.6.16 |

#### TSS Formats

| File | Description |
|------|-------------|
| `tss/security_header.ksy` | TSS security header (12-16 bytes) |
| `tss/iv_construction.ksy` | IV construction |

---

## 5. References

- UE Specification v1.0.1, Chapter 3 (Transport Layer)
- UE Specification v1.0.1, Section 3.6 (CMS)
  - Section 3.6.6: Congestion Control Context (CCC)
  - Section 3.6.13: NSCC (Network Signal-based CC)
  - Section 3.6.14: RCCC (Receiver-Credit CC)
  - Section 3.6.15: TFC (Transport Flow Control)
  - Section 3.6.16: Multipath Path Selection
- UE Specification v1.0.1, Section 3.7 (TSS)
- UE Specification v1.0.1, Tables 3-74, 3-75, 3-77, 3-78, 3-79, 3-80, 3-90
- CMS Documentation Plan: `analysis/ue_cms/CMS_DOCUMENTATION_PLAN.md`
