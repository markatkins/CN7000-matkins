# PMR Packet Taxonomy: UE Tagged-Send and IPv4 Variants

**Parent Document**: [packet_taxonomy.md](packet_taxonomy.md)  
**Scope**: Ultra Ethernet tagged-send operations and IPv4 encapsulation variants  
**Datamodel Directory**: `datamodel/protocols/ue/`  
**Last Updated**: 2026-02-02

---

## Table of Contents

1. [Overview](#1-overview)
2. [Protocol Stack](#2-protocol-stack)
3. [Packet Type Matrix](#3-packet-type-matrix)
4. [Tagged-Send Packet Variants](#4-tagged-send-packet-variants)
   - [4.1 UE Tagged Send (Standard)](#41-ue-tagged-send-standard-100b)
   - [4.2 UE Tagged Send with CSIG (Compact)](#42-ue-tagged-send-with-csig-compact-108b)
   - [4.3 UE Tagged Send with CSIG (Wide)](#43-ue-tagged-send-with-csig-wide-116b)
   - [4.4 UE IPv4 (Native, No UDP)](#44-ue-ipv4-native-no-udp-96b)
   - [4.5 UE IPv4 with CSIG](#45-ue-ipv4-with-csig-104b112b)
   - [4.6 UE IPv4 with Encryption (TSS)](#46-ue-ipv4-with-encryption-tss-116b16b)
   - [4.7 UE Small Message (Optimized)](#47-ue-small-message-optimized-88b)
   - [4.8 UE Rendezvous Send](#48-ue-rendezvous-send-132b)
   - [4.9 UE Deferrable Send](#49-ue-deferrable-send-100b)
5. [Wire Format Diagrams](#5-wire-format-diagrams)
6. [Header Size Summary](#6-header-size-summary)
7. [Cross-References](#7-cross-references)
8. [References](#8-references)

---

## 1. Overview

This document catalogs the complete set of Ultra Ethernet (UE) tagged-send packet variants and IPv4 encapsulation options. Tagged-send operations are the primary mechanism for two-sided messaging in UE, using match bits and initiator IDs for receive-side buffer selection.

### Key Packet Categories

| Category | Description | Primary Use Case |
|----------|-------------|------------------|
| Standard Tagged Send | Full SES header with match bits | General two-sided messaging |
| Small Message | Optimized 32B SES header | Single-packet low-latency sends |
| Rendezvous Send | Tagged send + rendezvous extension | Large message transfers |
| Deferrable Send | Tagged send with restart tokens | CCL-style unexpected messaging |
| IPv4 Native | Direct IPv4 encapsulation (no UDP) | Reduced header overhead |
| Encrypted (TSS) | TSS-protected payload | Secure communications |

### Delivery Modes

| Mode | Abbreviation | Reliability | Ordering | Typical Header |
|------|--------------|-------------|----------|----------------|
| Reliable Unordered Delivery | RUD | Yes | No | 12B PDS |
| Reliable Ordered Delivery | ROD | Yes | Yes | 12B PDS |
| Reliable Unordered Delivery Immediate | RUDI | Yes | No | 6B PDS |
| Unreliable Unordered Delivery | UUD | No | No | 6B PDS |

---

## 2. Protocol Stack

UE implements a layered protocol architecture where each sublayer adds specific functionality:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           Application Layer                              │
│                    (libfabric, MPI, SHMEM, etc.)                         │
├─────────────────────────────────────────────────────────────────────────┤
│                     SES - Semantic Sublayer (32-44B)                     │
│         Opcodes, match bits, initiator, buffer addressing                │
├─────────────────────────────────────────────────────────────────────────┤
│                     CMS - Congestion Management (8-16B)                  │
│              CC state: NSCC, RCCC/TFC credit management                  │
├─────────────────────────────────────────────────────────────────────────┤
│                     TSS - Transport Security (12-16B)                    │
│                  Encryption, authentication (optional)                   │
├─────────────────────────────────────────────────────────────────────────┤
│                     PDS - Packet Delivery Sublayer (6-12B)               │
│           RUD/ROD/RUDI/UUD, PSN, PDCID, ACK/NACK                         │
├─────────────────────────────────────────────────────────────────────────┤
│                        Network Layer (20-40B)                            │
│                         IPv4 (20B) / IPv6 (40B)                          │
├─────────────────────────────────────────────────────────────────────────┤
│                         Link Layer (14-18B)                              │
│                    Ethernet II (14B) + VLAN (4B opt)                     │
└─────────────────────────────────────────────────────────────────────────┘
```

### Encapsulation Options

| Encapsulation | Components | Total L2-L4 | Notes |
|---------------|------------|-------------|-------|
| UDP/IPv4 | Eth + IPv4 + UDP | 42B | Standard, ECMP via UDP src port |
| Native IPv4 | Eth + IPv4 + Entropy | 38B | 4B savings, entropy header for ECMP |
| UDP/IPv6 | Eth + IPv6 + UDP | 62B | IPv6 addressing |
| Native IPv6 | Eth + IPv6 + Entropy | 58B | IPv6 with entropy header |

---

## 3. Packet Type Matrix

### SES Header Formats (next_hdr values)

| next_hdr | Header Type | Size | Description |
|----------|-------------|------|-------------|
| 0x0 | Standard Header SOM=1 | 44B | Start of message (full addressing) |
| 0x1 | Standard Header SOM=0 | 16B | Continuation packet |
| 0x2 | Optimized Non-Matching | 32B | RMA without matching |
| 0x3 | Small Message/RMA | 32B | Single-packet optimized |
| 0x4 | Response | 16B | Standard response |
| 0x5 | Response with Data | 24B | Data-carrying response |
| 0x6 | Optimized Response | 16B | Optimized format |

### SES Request Opcodes (Table 3-17)

| Opcode | Value | Description | SES Header |
|--------|-------|-------------|------------|
| Tagged Send | 0x00 | Send with tag matching | Standard (44B) |
| RMA Write | 0x01 | Remote memory write | Standard (44B) |
| RMA Read | 0x02 | Remote memory read | Standard (44B) |
| Atomic Write | 0x03 | Atomic memory write | Standard + Atomic Ext |
| Atomic Read | 0x04 | Atomic memory read | Standard + Atomic Ext |
| Atomic CAS | 0x05 | Compare-and-swap | Standard + CAS Ext |
| Deferrable Send | 0x06 | Deferrable send | Deferrable (44B) |
| Ready to Restart | 0x07 | Restart notification | RTR (44B) |
| Small Message | 0x08 | Small message | Small (32B) |
| Small RMA Write | 0x09 | Small RMA write | Small (32B) |
| Small RMA Read | 0x0A | Small RMA read | Small (32B) |

---

## 4. Tagged-Send Packet Variants

### 4.1 UE Tagged Send (Standard, 100B)

Standard tagged-send packet using UDP/IPv4 encapsulation with RUD delivery.

**Encapsulation**: Ethernet II (14B) + IPv4 (20B) + UDP (8B) + PDS Prologue (2B) + PDS RUD (12B) + SES Standard SOM=1 (44B)

#### Wire Format

```
┌──────────┬──────────┬──────────┬──────────────┬──────────────┬──────────┬──────────┐
│ Ethernet │   IPv4   │   UDP    │ PDS Prologue │  PDS RUD/ROD │ SES Std  │   Data   │
│   14B    │   20B    │   8B     │     2B       │     12B      │   44B    │ Variable │
└──────────┴──────────┴──────────┴──────────────┴──────────────┴──────────┴──────────┘
```

**Total Header Size**: 100 bytes (before payload)

#### Component Breakdown

| Layer | Component | Size | Key Fields |
|-------|-----------|------|------------|
| L2 | Ethernet II | 14B | dst_mac, src_mac, ethertype=0x0800 |
| L3 | IPv4 | 20B | src_ip, dst_ip, protocol=17 (UDP) |
| L4 | UDP | 8B | src_port (entropy), dst_port=4791 |
| PDS | Prologue | 2B | type, next_hdr, flags |
| PDS | RUD Request | 12B | psn, spdcid, dpdcid, clear_psn_offset |
| SES | Standard SOM=1 | 44B | opcode=0x00, match_bits, initiator, buffer_offset |

**Datamodel Files**: 
- `datamodel/protocols/ethernet/link/ethernet_ii.ksy`
- `datamodel/protocols/ethernet/network/ipv4.ksy`
- `datamodel/protocols/ethernet/transport/udp.ksy`
- `datamodel/protocols/ue/transport/pds/prologue.ksy`
- `datamodel/protocols/ue/transport/pds/rud_rod_request.ksy`
- `datamodel/protocols/ue/transport/ses/standard_request_som1.ksy`

---

### 4.2 UE Tagged Send with CSIG (Compact, 108B)

Tagged-send with compact (8B) congestion control state for NSCC algorithm.

**Encapsulation**: Ethernet II (14B) + IPv4 (20B) + UDP (8B) + PDS Prologue (2B) + PDS RUD (12B) + CC State Compact (8B) + SES Standard SOM=1 (44B)

#### Wire Format

```
┌──────────┬──────────┬──────────┬──────────────┬──────────────┬──────────┬──────────┬──────────┐
│ Ethernet │   IPv4   │   UDP    │ PDS Prologue │  PDS RUD/ROD │ CC State │ SES Std  │   Data   │
│   14B    │   20B    │   8B     │     2B       │     12B      │    8B    │   44B    │ Variable │
└──────────┴──────────┴──────────┴──────────────┴──────────────┴──────────┴──────────┴──────────┘
```

**Total Header Size**: 108 bytes

#### CC State Compact Fields

| Field | Bits | Description |
|-------|------|-------------|
| cc_type | 4 | CC algorithm (0=NSCC, 1=CREDIT) |
| cc_flags | 4 | Reserved flags |
| sent_bytes | 24 | Bytes sent in current window |
| cwnd_bytes | 32 | Congestion window size |

**Datamodel Files**: 
- `datamodel/protocols/ue/transport/cms/cc_state_compact.ksy`

---

### 4.3 UE Tagged Send with CSIG (Wide, 116B)

Tagged-send with wide (16B) congestion control state for extended CC algorithms.

**Encapsulation**: Ethernet II (14B) + IPv4 (20B) + UDP (8B) + PDS Prologue (2B) + PDS RUD (12B) + CC State Wide (16B) + SES Standard SOM=1 (44B)

#### Wire Format

```
┌──────────┬──────────┬──────────┬──────────────┬──────────────┬──────────┬──────────┬──────────┐
│ Ethernet │   IPv4   │   UDP    │ PDS Prologue │  PDS RUD/ROD │ CC Wide  │ SES Std  │   Data   │
│   14B    │   20B    │   8B     │     2B       │     12B      │   16B    │   44B    │ Variable │
└──────────┴──────────┴──────────┴──────────────┴──────────────┴──────────┴──────────┴──────────┘
```

**Total Header Size**: 116 bytes

#### CC State Wide Fields

| Field | Bits | Description |
|-------|------|-------------|
| cc_type | 4 | CC algorithm type |
| cc_flags | 4 | Reserved flags |
| cc_state | 120 | Extended CC state (algorithm-specific) |

**Datamodel Files**: 
- `datamodel/protocols/ue/transport/cms/cc_state_wide.ksy`

---

### 4.4 UE IPv4 (Native, No UDP, 96B)

Native IPv4 encapsulation without UDP layer, using entropy header for ECMP.

**Encapsulation**: Ethernet II (14B) + IPv4 (20B) + UET Entropy (4B) + PDS Prologue (2B) + PDS RUD (12B) + SES Standard SOM=1 (44B)

#### Wire Format

```
┌──────────┬──────────┬──────────┬──────────────┬──────────────┬──────────┬──────────┐
│ Ethernet │   IPv4   │ Entropy  │ PDS Prologue │  PDS RUD/ROD │ SES Std  │   Data   │
│   14B    │   20B    │   4B     │     2B       │     12B      │   44B    │ Variable │
└──────────┴──────────┴──────────┴──────────────┴──────────────┴──────────┴──────────┘
```

**Total Header Size**: 96 bytes (4B savings vs UDP encapsulation)

#### Entropy Header Fields

| Field | Bits | Offset | Description |
|-------|------|--------|-------------|
| entropy | 16 | 0-1 | Flow hash for ECMP distribution |
| reserved | 16 | 2-3 | Must be 0 |

**IPv4 Protocol Field**: Uses protocol number 253 (experimental) or vendor-assigned value for UE native encapsulation.

**Datamodel Files**: 
- `datamodel/protocols/ue/transport/pds/entropy_header.ksy`

---

### 4.5 UE IPv4 with CSIG (104B/112B)

Native IPv4 with congestion control state (compact or wide).

**Encapsulation (Compact)**: Ethernet II (14B) + IPv4 (20B) + UET Entropy (4B) + PDS Prologue (2B) + PDS RUD (12B) + CC State Compact (8B) + SES Standard SOM=1 (44B)

#### Wire Format (Compact CC)

```
┌──────────┬──────────┬──────────┬──────────────┬──────────────┬──────────┬──────────┬──────────┐
│ Ethernet │   IPv4   │ Entropy  │ PDS Prologue │  PDS RUD/ROD │ CC State │ SES Std  │   Data   │
│   14B    │   20B    │   4B     │     2B       │     12B      │    8B    │   44B    │ Variable │
└──────────┴──────────┴──────────┴──────────────┴──────────────┴──────────┴──────────┴──────────┘
```

**Total Header Size**: 104B (compact) / 112B (wide)

---

### 4.6 UE IPv4 with Encryption (TSS, 116B+16B)

Encrypted tagged-send using Transport Security Sublayer (TSS).

**Encapsulation**: Ethernet II (14B) + IPv4 (20B) + UDP (8B) + PDS Prologue (2B) + TSS Header (12B) + PDS RUD (12B) + SES Standard SOM=1 (44B) + Auth Tag (16B)

#### Wire Format

```
┌──────────┬──────────┬──────────┬──────────────┬──────────┬──────────────┬──────────┬──────────┬──────────┐
│ Ethernet │   IPv4   │   UDP    │ PDS Prologue │   TSS    │  PDS RUD/ROD │ SES Std  │   Data   │ Auth Tag │
│   14B    │   20B    │   8B     │     2B       │   12B    │     12B      │   44B    │ Variable │   16B    │
└──────────┴──────────┴──────────┴──────────────┴──────────┴──────────────┴──────────┴──────────┴──────────┘
```

**Total Header Size**: 112B (before payload) + 16B auth tag (after payload)

#### TSS Header Fields

| Field | Bits | Description |
|-------|------|-------------|
| tss_type | 4 | TSS packet type |
| tss_flags | 4 | TSS flags |
| security_context_id | 32 | Security association identifier |
| sequence_number | 32 | Anti-replay sequence number |
| reserved | 24 | Reserved |

**Encryption Scope**: TSS encrypts from PDS header through payload; auth tag covers entire encrypted region.

**Datamodel Files**: 
- `datamodel/protocols/ue/transport/tss/tss_header.ksy`

---

### 4.7 UE Small Message (Optimized, 88B)

Optimized single-packet tagged-send using 32B SES small message header.

**Encapsulation**: Ethernet II (14B) + IPv4 (20B) + UDP (8B) + PDS Prologue (2B) + PDS RUD (12B) + SES Small Message (32B)

#### Wire Format

```
┌──────────┬──────────┬──────────┬──────────────┬──────────────┬──────────────┬──────────┐
│ Ethernet │   IPv4   │   UDP    │ PDS Prologue │  PDS RUD/ROD │  SES Small   │   Data   │
│   14B    │   20B    │   8B     │     2B       │     12B      │     32B      │ Variable │
└──────────┴──────────┴──────────┴──────────────┴──────────────┴──────────────┴──────────┘
```

**Total Header Size**: 88 bytes (12B savings vs standard)

#### SES Small Message Fields

| Field | Bits | Offset | Description |
|-------|------|--------|-------------|
| opcode | 6 | 0[7:2] | Operation code (0x08 for small message) |
| version | 2 | 0[1:0] | Protocol version |
| dc | 1 | 1[7] | Delivery Complete flag |
| ie | 1 | 1[6] | Initiator Error flag |
| rel | 1 | 1[5] | Relative addressing |
| hd | 1 | 1[4] | Header Data present |
| eom | 1 | 1[3] | End of Message (must be 1) |
| som | 1 | 1[2] | Start of Message (must be 1) |
| request_length | 14 | 2-3 | Request length (max 16383B) |
| ri_generation | 8 | 4 | Resource Index generation |
| job_id | 24 | 5-7 | Job Identifier |
| pid_on_fep | 12 | 8-9 | Process ID on FEP |
| resource_index | 12 | 10-11 | Resource Index |
| initiator | 32 | 12-15 | Initiator ID |
| match_bits | 64 | 16-23 | Match bits for receive matching |
| header_data | 64 | 24-31 | Completion header data |

**Constraints**: 
- Single-packet only (som=1, eom=1)
- Max payload: 16383 bytes
- No buffer_offset field (not needed for single packet)

**Datamodel Files**: 
- `datamodel/protocols/ue/transport/ses/small_message.ksy`

---

### 4.8 UE Rendezvous Send (132B)

Large message transfer using rendezvous protocol with eager data push.

**Encapsulation**: Ethernet II (14B) + IPv4 (20B) + UDP (8B) + PDS Prologue (2B) + PDS RUD (12B) + SES Standard SOM=1 (44B) + Rendezvous Extension (32B)

#### Wire Format

```
┌──────────┬──────────┬──────────┬──────────────┬──────────────┬──────────┬──────────────┬──────────┐
│ Ethernet │   IPv4   │   UDP    │ PDS Prologue │  PDS RUD/ROD │ SES Std  │ Rendezvous   │   Data   │
│   14B    │   20B    │   8B     │     2B       │     12B      │   44B    │     32B      │ Variable │
└──────────┴──────────┴──────────┴──────────────┴──────────────┴──────────┴──────────────┴──────────┘
```

**Total Header Size**: 132 bytes

#### Rendezvous Extension Fields

| Field | Bits | Offset | Description |
|-------|------|--------|-------------|
| eager_length | 32 | 0-3 | Bytes pushed with initial request |
| memory_key | 64 | 4-11 | Initiator memory key for RDMA Read |
| buffer_offset | 64 | 12-19 | Initiator buffer offset |
| remaining_length | 32 | 20-23 | Bytes remaining to pull |
| reserved | 64 | 24-31 | Reserved (must be 0) |

#### Protocol Flow

1. Initiator sends request with eager data + rendezvous extension
2. Target receives eager data, allocates buffer
3. Target issues RDMA Read using {memory_key, buffer_offset}
4. Target completes operation when all data received

**Datamodel Files**: 
- `datamodel/protocols/ue/transport/ses/rendezvous_extension.ksy`

---

### 4.9 UE Deferrable Send (100B)

CCL-style messaging with restart tokens for unexpected message handling.

**Encapsulation**: Ethernet II (14B) + IPv4 (20B) + UDP (8B) + PDS Prologue (2B) + PDS RUD (12B) + SES Deferrable (44B)

#### Wire Format

```
┌──────────┬──────────┬──────────┬──────────────┬──────────────┬──────────────┬──────────┐
│ Ethernet │   IPv4   │   UDP    │ PDS Prologue │  PDS RUD/ROD │SES Deferrable│   Data   │
│   14B    │   20B    │   8B     │     2B       │     12B      │     44B      │ Variable │
└──────────┴──────────┴──────────┴──────────────┴──────────────┴──────────────┴──────────┘
```

**Total Header Size**: 100 bytes

#### SES Deferrable Send Fields

| Field | Bits | Offset | Description |
|-------|------|--------|-------------|
| (standard prefix) | - | 0-15 | Same as Standard Request |
| initiator_restart_token | 32 | 16-19 | Initiator-defined restart token |
| target_restart_token | 32 | 20-23 | Target-allocated restart token (0 initially) |
| initiator | 32 | 24-27 | Initiator ID |
| match_bits | 64 | 28-35 | Match bits |
| header_data | 64 | 36-43 | Header data |

#### Protocol Flow

1. Initial send: target_restart_token = 0
2. If no buffer at target: Target sends RTR (Ready-to-Restart)
3. Initiator restarts with full restart_token from RTR
4. Restarted send MUST set ses.som = 1

**Key Difference from Standard**: buffer_offset replaced by restart_token (64 bits split into initiator/target portions)

**Datamodel Files**: 
- `datamodel/protocols/ue/transport/ses/deferrable_send_request.ksy`
- `datamodel/protocols/ue/transport/ses/ready_to_restart.ksy`

---

## 5. Wire Format Diagrams

### 5.1 UE Tagged Send (Standard) - Detailed

```
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                              UE Tagged Send (Standard) - 100B Header                         │
├──────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                              │
│  Byte:  0         6        12  14        34  42        44  46        58        102          │
│         │         │         │  │          │  │          │  │          │          │          │
│         ▼         ▼         ▼  ▼          ▼  ▼          ▼  ▼          ▼          ▼          │
│  ┌──────┬─────────┬─────────┬──┬──────────┬──┬──────────┬──┬──────────┬──────────┬────────┐ │
│  │Dst   │Src      │EType    │V │IPv4      │S │Dst       │L │UDP       │PDS       │SES     │ │
│  │MAC   │MAC      │0x0800   │e │Header    │r │Port      │e │Checksum  │Prologue  │Std     │ │
│  │      │         │         │r │          │c │4791      │n │          │+ RUD     │SOM=1   │ │
│  │6B    │6B       │2B       │4 │20B       │P │2B        │2 │2B        │14B       │44B     │ │
│  │      │         │         │  │          │t │          │B │          │          │        │ │
│  └──────┴─────────┴─────────┴──┴──────────┴──┴──────────┴──┴──────────┴──────────┴────────┘ │
│  │◄─────────── Ethernet ────────►│◄─────── IPv4 ───────►│◄── UDP ──►│◄─────── UE ────────►│ │
│  │              14B              │         20B          │    8B     │        58B          │ │
│                                                                                              │
└──────────────────────────────────────────────────────────────────────────────────────────────┘
```

### 5.2 UE IPv4 with Encryption (TSS) - Detailed

```
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                         UE IPv4 with Encryption (TSS) - 112B + 16B Auth                      │
├──────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                              │
│  ┌──────────┬──────────┬──────────┬──────────────┬──────────┬──────────────┬──────────┐     │
│  │ Ethernet │   IPv4   │   UDP    │ PDS Prologue │   TSS    │  PDS RUD     │ SES Std  │     │
│  │   14B    │   20B    │   8B     │     2B       │   12B    │    12B       │   44B    │     │
│  └──────────┴──────────┴──────────┴──────────────┴──────────┴──────────────┴──────────┘     │
│                                   │◄────────────── Encrypted ──────────────►│               │
│                                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────────┬──────────┐    │
│  │                              Payload (Variable)                           │ Auth Tag │    │
│  │                                                                           │   16B    │    │
│  └──────────────────────────────────────────────────────────────────────────┴──────────┘    │
│  │◄─────────────────────────── Authenticated ───────────────────────────────►│              │
│                                                                                              │
│  TSS Header Detail:                                                                          │
│  ┌────────┬────────┬────────────────────┬────────────────────┬────────────┐                 │
│  │tss_type│tss_flg │ security_ctx_id    │   sequence_number  │  reserved  │                 │
│  │  4b    │  4b    │       32b          │        32b         │    24b     │                 │
│  └────────┴────────┴────────────────────┴────────────────────┴────────────┘                 │
│                                                                                              │
└──────────────────────────────────────────────────────────────────────────────────────────────┘
```

### 5.3 UE Small Message - Detailed

```
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                              UE Small Message (Optimized) - 88B Header                       │
├──────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                              │
│  ┌──────────┬──────────┬──────────┬──────────────┬──────────────┬──────────────┐            │
│  │ Ethernet │   IPv4   │   UDP    │ PDS Prologue │  PDS RUD/ROD │  SES Small   │            │
│  │   14B    │   20B    │   8B     │     2B       │     12B      │     32B      │            │
│  └──────────┴──────────┴──────────┴──────────────┴──────────────┴──────────────┘            │
│                                                                                              │
│  SES Small Message Detail (32 bytes):                                                        │
│  ┌────────┬────────┬────────────┬──────────┬──────────┬──────────┬──────────┬──────────┐    │
│  │opcode  │flags   │req_length  │ri_gen    │job_id    │pid/res   │initiator │match_bits│    │
│  │+ver    │        │            │          │          │          │          │          │    │
│  │ 1B     │ 1B     │   2B       │  1B      │   3B     │   4B     │   4B     │   8B     │    │
│  └────────┴────────┴────────────┴──────────┴──────────┴──────────┴──────────┴──────────┘    │
│  ┌──────────────────┐                                                                        │
│  │   header_data    │                                                                        │
│  │       8B         │                                                                        │
│  └──────────────────┘                                                                        │
│                                                                                              │
│  Constraints: som=1, eom=1 (single packet only), max payload 16383B                          │
│                                                                                              │
└──────────────────────────────────────────────────────────────────────────────────────────────┘
```

### 5.4 UE IPv4 Native (No UDP) - Detailed

```
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                              UE IPv4 Native (No UDP) - 96B Header                            │
├──────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                              │
│  ┌──────────┬──────────┬──────────┬──────────────┬──────────────┬──────────┐                │
│  │ Ethernet │   IPv4   │ Entropy  │ PDS Prologue │  PDS RUD/ROD │ SES Std  │                │
│  │   14B    │   20B    │   4B     │     2B       │     12B      │   44B    │                │
│  └──────────┴──────────┴──────────┴──────────────┴──────────────┴──────────┘                │
│                                                                                              │
│  Entropy Header Detail (4 bytes):                                                            │
│  ┌────────────────────┬────────────────────┐                                                 │
│  │     entropy        │     reserved       │                                                 │
│  │       16b          │       16b          │                                                 │
│  └────────────────────┴────────────────────┘                                                 │
│                                                                                              │
│  IPv4 Protocol: 253 (experimental) or vendor-assigned for UE native                          │
│  Entropy field provides ECMP distribution equivalent to UDP source port                      │
│                                                                                              │
│  Savings vs UDP: 4 bytes (UDP 8B - Entropy 4B = 4B)                                          │
│                                                                                              │
└──────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 6. Header Size Summary

| Variant | Eth | IP | UDP/Ent | TSS | PDS | CC | SES | Total | Auth |
|---------|-----|----|---------|----|-----|----|----|-------|------|
| Tagged Send (Standard) | 14B | 20B | 8B | - | 14B | - | 44B | **100B** | - |
| Tagged Send + CSIG Compact | 14B | 20B | 8B | - | 14B | 8B | 44B | **108B** | - |
| Tagged Send + CSIG Wide | 14B | 20B | 8B | - | 14B | 16B | 44B | **116B** | - |
| IPv4 Native (No UDP) | 14B | 20B | 4B | - | 14B | - | 44B | **96B** | - |
| IPv4 Native + CSIG Compact | 14B | 20B | 4B | - | 14B | 8B | 44B | **104B** | - |
| IPv4 Native + CSIG Wide | 14B | 20B | 4B | - | 14B | 16B | 44B | **112B** | - |
| IPv4 + TSS Encryption | 14B | 20B | 8B | 12B | 14B | - | 44B | **112B** | 16B |
| Small Message | 14B | 20B | 8B | - | 14B | - | 32B | **88B** | - |
| Rendezvous Send | 14B | 20B | 8B | - | 14B | - | 76B | **132B** | - |
| Deferrable Send | 14B | 20B | 8B | - | 14B | - | 44B | **100B** | - |

**Notes**:
- PDS column includes 2B prologue + 12B RUD/ROD request
- SES Rendezvous = 44B standard + 32B rendezvous extension
- Auth tag (16B) is appended after payload, not included in header total
- IPv6 variants add 20B to IP column (40B vs 20B)

---

## 7. Cross-References

### Related Documents

| Document | Content |
|----------|---------|
| [packet_taxonomy.md](packet_taxonomy.md) | Master index |
| [packet_taxonomy_ue_ses.md](packet_taxonomy_ue_ses.md) | SES header field definitions |
| [packet_taxonomy_ue_pds.md](packet_taxonomy_ue_pds.md) | PDS header field definitions |
| [packet_taxonomy_ue_cms_tss.md](packet_taxonomy_ue_cms_tss.md) | CMS/TSS formats |
| [packet_taxonomy_ethernet.md](packet_taxonomy_ethernet.md) | Ethernet/IP/UDP formats |

### Datamodel Files

| File | Description |
|------|-------------|
| `transport/pds/prologue.ksy` | PDS prologue (2B) |
| `transport/pds/rud_rod_request.ksy` | RUD/ROD request (12B) |
| `transport/pds/entropy_header.ksy` | UET entropy header (4B) |
| `transport/ses/standard_request_som1.ksy` | SES standard SOM=1 (44B) |
| `transport/ses/small_message.ksy` | SES small message (32B) |
| `transport/ses/rendezvous_extension.ksy` | Rendezvous extension (32B) |
| `transport/ses/deferrable_send_request.ksy` | Deferrable send (44B) |
| `transport/ses/ready_to_restart.ksy` | Ready to restart (44B) |
| `transport/cms/cc_state_compact.ksy` | CC state compact (8B) |
| `transport/cms/cc_state_wide.ksy` | CC state wide (16B) |
| `transport/tss/tss_header.ksy` | TSS header (12B) |

---

## 8. References

- UE Specification v1.0.1, Chapter 3 (Transport Layer)
- UE Specification v1.0.1, Section 3.4 (SES) - Tables 3-8 through 3-17
- UE Specification v1.0.1, Section 3.5 (PDS) - Tables 3-33 through 3-42
- UE Specification v1.0.1, Section 3.6 (CMS) - Congestion Management
- UE Specification v1.0.1, Section 3.7 (TSS) - Transport Security
- UE Specification v1.0.1, Figure 3-14 (Small Message Format)
- UE Specification v1.0.1, Figure 3-15 (Rendezvous Extension)
- UE Specification v1.0.1, Figure 3-11 (Deferrable Send)
