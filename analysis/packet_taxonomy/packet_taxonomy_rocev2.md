# PMR Packet Taxonomy: RoCEv2 Formats

**Parent Document**: [packet_taxonomy.md](packet_taxonomy.md)  
**Scope**: RDMA over Converged Ethernet v2 (RoCEv2) packet formats  
**Datamodel Directory**: `datamodel/protocols/roce/transport/`  
**Last Updated**: 2026-01-23

---

## Table of Contents

1. [Overview](#1-overview)
2. [RoCEv2 Packet Structure](#2-rocev2-packet-structure)
3. [Base Transport Header (BTH)](#3-base-transport-header-bth-12-bytes)
4. [Extended Transport Headers](#4-extended-transport-headers)
   - [4.1 RETH (RDMA Extended)](#41-reth-rdma-extended-transport-header-16-bytes)
   - [4.2 AETH (ACK Extended)](#42-aeth-ack-extended-transport-header-4-bytes)
   - [4.3 AtomicETH](#43-atomiceth-atomic-extended-transport-header-28-bytes)
   - [4.4 Other Headers](#44-other-headers)
5. [Packet Composition](#5-packet-composition)
6. [Cross-References](#6-cross-references)
7. [References](#7-references)

---

## 1. Overview

RoCEv2 (RDMA over Converged Ethernet v2) enables RDMA operations over standard Ethernet networks using UDP/IP encapsulation. PMR provides full hardware support for RoCEv2 operations.

### Key Characteristics

| Feature | Value |
|---------|-------|
| UDP Destination Port | 4791 (0x12B7) |
| Transport Types | RC, UC, RD, UD |
| Max PSN | 2^24 (16,777,216) |
| Max QP | 2^24 (16,777,216) |
| Atomic Size | 8 bytes (64-bit) |

### Transport Types

| Type | Value | Description |
|------|-------|-------------|
| RC | 0x00 | Reliable Connection |
| UC | 0x20 | Unreliable Connection |
| RD | 0x40 | Reliable Datagram |
| UD | 0x60 | Unreliable Datagram |

---

## 2. RoCEv2 Packet Structure

```
+-----------------------------------------------------------------------------+
| Ethernet II Header (14 bytes)                                               |
|   Dest MAC (6) | Source MAC (6) | EtherType (2) = 0x0800/0x86DD            |
+-----------------------------------------------------------------------------+
| IP Header (20 bytes IPv4 / 40 bytes IPv6)                                   |
|   Version, IHL, DSCP, ECN, Length, ID, Flags, TTL, Protocol=17, Checksum   |
|   Source IP, Dest IP                                                        |
+-----------------------------------------------------------------------------+
| UDP Header (8 bytes)                                                        |
|   Source Port (entropy) | Dest Port = 4791 | Length | Checksum             |
+-----------------------------------------------------------------------------+
| BTH - Base Transport Header (12 bytes)                                      |
|   Opcode | Flags | P-Key | Dest QP | A | PSN                               |
+-----------------------------------------------------------------------------+
| Extended Headers (optional, operation-dependent)                            |
|   RETH (16) | AETH (4) | AtomicETH (28) | ImmDt (4)                        |
+-----------------------------------------------------------------------------+
| Payload (0 - MTU bytes)                                                     |
+-----------------------------------------------------------------------------+
| ICRC (4 bytes)                                                              |
+-----------------------------------------------------------------------------+
```

### Header Sizes

| Component | Size | Notes |
|-----------|------|-------|
| Ethernet II | 14 bytes | + 4 bytes if VLAN tagged |
| IPv4 | 20 bytes | + options if present |
| IPv6 | 40 bytes | + extension headers |
| UDP | 8 bytes | Fixed |
| BTH | 12 bytes | Always present |
| RETH | 16 bytes | RDMA Read/Write |
| AETH | 4 bytes | ACK/Response |
| AtomicETH | 28 bytes | Atomic operations |
| ImmDt | 4 bytes | Immediate data |
| ICRC | 4 bytes | Always present |

---

## 3. Base Transport Header (BTH, 12 bytes)

**Datamodel**: `datamodel/protocols/roce/transport/bth.ksy`  
**Related Formats**: All RoCEv2 packets

The BTH is present in all RoCEv2 packets and follows the UDP header.

### Wire Format

```
Byte:    0       1       2       3       4       5       6       7
     +-------+-------+-------+-------+-------+-------+-------+-------+
     | opcode| flags |     p_key     | rsvd  |      dest_qp        →
     +-------+-------+-------+-------+-------+-------+-------+-------+
         8       9      10      11
     +-------+-------+-------+-------+
   → |A| rsvd |        psn          |
     +-------+-------+-------+-------+

Byte 1 (flags) Detail:
  Bit:  7 6 5 4 3 2 1 0
       |S|M|pad| tver  |
       |E| |cnt|       |
```

### Field Definitions

| Field | Bits | Offset | Description | Constraints |
|-------|------|--------|-------------|-------------|
| opcode | 8 | 0 | Operation code | See tables below |
| flags.SE | 1 | 1[7] | Solicited Event | Request completion notification |
| flags.M | 1 | 1[6] | Migration state | MigReq flag |
| flags.pad | 2 | 1[5:4] | Pad count | 0-3 bytes padding |
| flags.tver | 4 | 1[3:0] | Transport version | Must be 0 |
| p_key | 16 | 2-3 | Partition key | Bit 15 = membership type |
| rsvd | 8 | 4 | Reserved | Must be 0 |
| dest_qp | 24 | 5-7 | Destination QP | Target queue pair |
| ack_req | 1 | 8[7] | ACK request | Request ACK (reliable only) |
| rsvd | 7 | 8[6:0] | Reserved | Must be 0 |
| psn | 24 | 9-11 | Packet Sequence Number | 24-bit, wraps |

### Opcode Encoding

The opcode byte encodes both transport type and operation:

```
Opcode = (Transport Type << 5) | Operation
```

### Transport Types (Opcode bits [7:5])

| Value | Type | Description |
|-------|------|-------------|
| 0x00 | RC | Reliable Connection |
| 0x20 | UC | Unreliable Connection |
| 0x40 | RD | Reliable Datagram |
| 0x60 | UD | Unreliable Datagram |

### Operations (Opcode bits [4:0])

| Value | Operation | Extended Headers |
|-------|-----------|------------------|
| 0x00 | SEND_FIRST | None |
| 0x01 | SEND_MIDDLE | None |
| 0x02 | SEND_LAST | None |
| 0x03 | SEND_LAST_IMM | ImmDt |
| 0x04 | SEND_ONLY | None |
| 0x05 | SEND_ONLY_IMM | ImmDt |
| 0x06 | RDMA_WRITE_FIRST | RETH |
| 0x07 | RDMA_WRITE_MIDDLE | None |
| 0x08 | RDMA_WRITE_LAST | None |
| 0x09 | RDMA_WRITE_LAST_IMM | ImmDt |
| 0x0A | RDMA_WRITE_ONLY | RETH |
| 0x0B | RDMA_WRITE_ONLY_IMM | RETH + ImmDt |
| 0x0C | RDMA_READ_REQUEST | RETH |
| 0x0D | RDMA_READ_RESPONSE_FIRST | AETH |
| 0x0E | RDMA_READ_RESPONSE_MIDDLE | None |
| 0x0F | RDMA_READ_RESPONSE_LAST | AETH |
| 0x10 | RDMA_READ_RESPONSE_ONLY | AETH |
| 0x11 | ACK | AETH |
| 0x12 | ATOMIC_ACK | AETH + AtomicAckETH |
| 0x13 | CMP_SWAP | AtomicETH |
| 0x14 | FETCH_ADD | AtomicETH |

### Protocol Behavior

**Reliable Transports (RC, RD)**:
- PSN used for ordering and duplicate detection
- ACK request triggers acknowledgment
- Retransmission on timeout or NAK

**Unreliable Transports (UC, UD)**:
- No acknowledgments
- No retransmission
- PSN for duplicate detection only

**Reference**: InfiniBand Architecture Specification Vol 1, Section 9.2

---

## 4. Extended Transport Headers

### 4.1 RETH (RDMA Extended Transport Header, 16 bytes)

**Datamodel**: `datamodel/protocols/roce/transport/reth.ksy`  
**Related Formats**: [BTH (3)](#3-base-transport-header-bth-12-bytes)

Present in RDMA READ Request and RDMA WRITE First/Only packets.

#### Wire Format

```
Byte:    0       1       2       3       4       5       6       7
     +-------+-------+-------+-------+-------+-------+-------+-------+
     |                    virtual_address [63:0]                     |
     +-------+-------+-------+-------+-------+-------+-------+-------+
         8       9      10      11      12      13      14      15
     +-------+-------+-------+-------+-------+-------+-------+-------+
     |          r_key [31:0]         |       dma_length [31:0]       |
     +-------+-------+-------+-------+-------+-------+-------+-------+
```

#### Field Definitions

| Field | Bits | Offset | Description | Constraints |
|-------|------|--------|-------------|-------------|
| virtual_address | 64 | 0-7 | Remote virtual address | Target memory location |
| r_key | 32 | 8-11 | Remote key | Memory region authorization |
| dma_length | 32 | 12-15 | DMA length | Total bytes to transfer |

#### Protocol Behavior

**RDMA Write**:
- RETH specifies where to write data in remote memory
- Present in FIRST and ONLY packets
- Subsequent packets (MIDDLE, LAST) continue from computed offset

**RDMA Read**:
- RETH specifies where to read data from remote memory
- Response packets carry the requested data

**Reference**: InfiniBand Architecture Specification Vol 1, Section 9.3

---

### 4.2 AETH (ACK Extended Transport Header, 4 bytes)

**Datamodel**: `datamodel/protocols/roce/transport/aeth.ksy`  
**Related Formats**: [BTH (3)](#3-base-transport-header-bth-12-bytes)

Present in ACK, RDMA READ Response, and Atomic ACK packets.

#### Wire Format

```
Byte:    0       1       2       3
     +-------+-------+-------+-------+
     |syndrome|        msn          |
     +-------+-------+-------+-------+

Byte 0 (syndrome) Detail:
  Bit:  7 6 5 4 3 2 1 0
       |type | value     |
       |(2b) | (6 bits)  |
```

#### Field Definitions

| Field | Bits | Offset | Description | Constraints |
|-------|------|--------|-------------|-------------|
| syndrome | 8 | 0 | ACK type + value | See below |
| msn | 24 | 1-3 | Message Sequence Number | Message being ACK'd |

#### Syndrome Encoding

| Bits [7:6] | Type | Bits [5:0] Meaning |
|------------|------|-------------------|
| 00 | ACK | Credit count (0-31) |
| 01 | RNR NAK | RNR timeout value |
| 10 | Reserved | - |
| 11 | NAK | NAK error code |

#### NAK Error Codes

| Code | Name | Description |
|------|------|-------------|
| 0x00 | PSN_SEQ_ERROR | PSN sequence error |
| 0x01 | INVALID_REQUEST | Invalid request |
| 0x02 | REMOTE_ACCESS_ERROR | Remote access error |
| 0x03 | REMOTE_OP_ERROR | Remote operation error |
| 0x04 | INVALID_RD_REQUEST | Invalid RD request |

#### RNR Timeout Values

| Code | Timeout |
|------|---------|
| 0x00 | 655.36 ms |
| 0x01 | 0.01 ms |
| 0x02 | 0.02 ms |
| ... | ... |
| 0x1F | 491.52 ms |

#### Protocol Behavior

**Positive ACK**:
- Acknowledges successful receipt
- Credit count indicates receiver capacity

**RNR NAK**:
- Receiver Not Ready
- Sender should retry after timeout

**NAK**:
- Error condition
- Sender should handle error

**Reference**: InfiniBand Architecture Specification Vol 1, Section 9.4

---

### 4.3 AtomicETH (Atomic Extended Transport Header, 28 bytes)

**Datamodel**: `datamodel/protocols/roce/transport/atomiceth.ksy`  
**Related Formats**: [BTH (3)](#3-base-transport-header-bth-12-bytes) | [AETH (4.2)](#42-aeth-ack-extended-transport-header-4-bytes)

Present in atomic operation request packets (CMP_SWAP, FETCH_ADD).

#### Wire Format

```
Byte:    0       1       2       3       4       5       6       7
     +-------+-------+-------+-------+-------+-------+-------+-------+
     |                    virtual_address [63:0]                     |
     +-------+-------+-------+-------+-------+-------+-------+-------+
         8       9      10      11      12      13      14      15
     +-------+-------+-------+-------+-------+-------+-------+-------+
     |          r_key [31:0]         |     swap_or_add_data [63:0]  →
     +-------+-------+-------+-------+-------+-------+-------+-------+
        16      17      18      19      20      21      22      23
     +-------+-------+-------+-------+-------+-------+-------+-------+
   → |  (swap_or_add cont'd)         |       compare_data [63:0]    →
     +-------+-------+-------+-------+-------+-------+-------+-------+
        24      25      26      27
     +-------+-------+-------+-------+
   → |  (compare_data cont'd)        |
     +-------+-------+-------+-------+
```

#### Field Definitions

| Field | Bits | Offset | Description | Constraints |
|-------|------|--------|-------------|-------------|
| virtual_address | 64 | 0-7 | Remote virtual address | Must be 8-byte aligned |
| r_key | 32 | 8-11 | Remote key | Memory region authorization |
| swap_or_add_data | 64 | 12-19 | Swap/Add operand | See below |
| compare_data | 64 | 20-27 | Compare operand | CMP_SWAP only |

#### Operation Semantics

**Compare and Swap (CMP_SWAP)**:
```
if (*virtual_address == compare_data) {
    original = *virtual_address;
    *virtual_address = swap_or_add_data;
    return original;
}
```

**Fetch and Add (FETCH_ADD)**:
```
original = *virtual_address;
*virtual_address = original + swap_or_add_data;
return original;
```

#### Protocol Behavior

**Atomic Constraints**:
- Operations are always 8 bytes (64-bit)
- Address must be 8-byte aligned
- compare_data must be 0 for FETCH_ADD

**Response**:
- ATOMIC_ACK with AtomicAckETH containing original value

**Reference**: InfiniBand Architecture Specification Vol 1, Section 9.8

---

### 4.5 AtomicAckETH (Atomic Acknowledge ETH, 8 bytes)

**Datamodel**: `datamodel/protocols/roce/transport/atomicacketh.ksy`  
**Related Formats**: [AtomicETH (4.4)](#44-atomiceth-atomic-extended-transport-header-28-bytes) | [AETH (4.3)](#43-aeth-ack-extended-transport-header-4-bytes)

AtomicAckETH contains the original value from atomic operations.

#### Wire Format

```
Byte:    0       1       2       3       4       5       6       7
     +-------+-------+-------+-------+-------+-------+-------+-------+
     |                    original_data [63:0]                       |
     +-------+-------+-------+-------+-------+-------+-------+-------+
```

#### Field Definitions

| Field | Bits | Offset | Description | Constraints |
|-------|------|--------|-------------|-------------|
| original_data | 64 | 0-7 | Original remote data | Value before atomic op |

#### Protocol Behavior

**Usage**:
- Present in ATOMIC_ACK (0x12) response packets
- Contains value from remote memory before atomic operation

**For CMP_SWAP**: If original_data equals compare_data from request, swap succeeded  
**For FETCH_ADD**: Original value before add was applied

**Reference**: InfiniBand Architecture Specification Vol 1, Section 9.9

---

### 4.6 DETH (Datagram Extended Transport Header, 8 bytes)

**Datamodel**: `datamodel/protocols/roce/transport/deth.ksy`  
**Related Formats**: [BTH (3)](#3-base-transport-header-bth-12-bytes)

DETH provides source QP information for Unreliable Datagram (UD) packets.

#### Wire Format

```
Byte:    0       1       2       3       4       5       6       7
     +-------+-------+-------+-------+-------+-------+-------+-------+
     |           qkey [31:0]         |  rsvd |     src_qp [23:0]     |
     +-------+-------+-------+-------+-------+-------+-------+-------+
```

#### Field Definitions

| Field | Bits | Offset | Description | Constraints |
|-------|------|--------|-------------|-------------|
| qkey | 32 | 0-3 | Queue Key | Authorization key |
| reserved | 8 | 4 | Reserved | Must be 0 |
| src_qp | 24 | 5-7 | Source QP number | Sender QP |

#### Protocol Behavior

**Usage**:
- Present in UD transport type packets
- UD SEND_ONLY (0x64), UD SEND_ONLY_IMM (0x65)

**Q-Key**: Authorization key that must match destination UD QP configuration  
**Well-known Q-Key**: Bit 31 set indicates IB-defined management service key

**Reference**: InfiniBand Architecture Specification Vol 1, Section 9.5

---

### 4.7 ImmDt (Immediate Data, 4 bytes)

**Datamodel**: `datamodel/protocols/roce/transport/immdt.ksy`  
**Related Formats**: [BTH (3)](#3-base-transport-header-bth-12-bytes)

ImmDt carries 32-bit immediate data that generates receiver completion.

#### Wire Format

```
Byte:    0       1       2       3
     +-------+-------+-------+-------+
     |      immediate_data [31:0]    |
     +-------+-------+-------+-------+
```

#### Field Definitions

| Field | Bits | Offset | Description | Constraints |
|-------|------|--------|-------------|-------------|
| immediate_data | 32 | 0-3 | Immediate data value | Application-defined |

#### Protocol Behavior

**Usage**:
- Present in _IMM opcodes: SEND_LAST_IMM (0x03), SEND_ONLY_IMM (0x05), RDMA_WRITE_LAST_IMM (0x09), RDMA_WRITE_ONLY_IMM (0x0B)

**Completion**: Immediate data appears in receiver's CQ entry, enabling application signaling without additional round trips

**Reference**: InfiniBand Architecture Specification Vol 1, Section 9.6

---

### 4.8 ICRC (Invariant CRC, 4 bytes)

**Datamodel**: `datamodel/protocols/roce/transport/icrc.ksy`  
**Related Formats**: All RoCEv2 packets

ICRC provides end-to-end integrity check for RoCEv2 transport layer.

#### Wire Format

```
Byte:    0       1       2       3
     +-------+-------+-------+-------+
     |         crc_value [31:0]      |
     +-------+-------+-------+-------+
```

#### Field Definitions

| Field | Bits | Offset | Description | Constraints |
|-------|------|--------|-------------|-------------|
| crc_value | 32 | 0-3 | CRC-32 value | IEEE 802.3 polynomial |

#### CRC Parameters

| Parameter | Value | Description |
|-----------|-------|-------------|
| Polynomial | 0x04C11DB7 | CRC-32 (IEEE 802.3) |
| Polynomial (reflected) | 0xEDB88320 | For table-driven implementation |
| Initial value | 0xFFFFFFFF | All 1s |
| Final XOR | 0xFFFFFFFF | Inverts result |

#### ICRC Coverage

**Covered**: BTH (with masked fields), extended headers, payload, padding  
**Masked (0xFF)**: IP header, UDP header, BTH reserved fields, LRH if present

**Reference**: InfiniBand Architecture Specification Vol 1, Section 9.7; RoCEv2 Annex A17

---

## 5. Packet Composition

### Common Packet Formats

```
RoCEv2 Packet Composition:
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  SEND:        BTH + [Payload] + ICRC                            │
│  SEND_IMM:    BTH + ImmDt + [Payload] + ICRC                    │
│                                                                 │
│  RDMA Write:  BTH + RETH + [Payload] + ICRC (first/only)        │
│               BTH + [Payload] + ICRC (middle/last)              │
│                                                                 │
│  RDMA Read:   BTH + RETH + ICRC (request)                       │
│               BTH + AETH + [Payload] + ICRC (response)          │
│                                                                 │
│  Atomic:      BTH + AtomicETH + ICRC (request)                  │
│               BTH + AETH + AtomicAckETH + ICRC (response)       │
│                                                                 │
│  ACK/NAK:     BTH + AETH + ICRC                                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Header Size Summary by Operation

| Operation | BTH | Extended | Payload | ICRC | Min Total |
|-----------|-----|----------|---------|------|-----------|
| SEND_ONLY | 12 | 0 | 0+ | 4 | 16 |
| SEND_ONLY_IMM | 12 | 4 | 0+ | 4 | 20 |
| RDMA_WRITE_ONLY | 12 | 16 | 0+ | 4 | 32 |
| RDMA_READ_REQUEST | 12 | 16 | 0 | 4 | 32 |
| RDMA_READ_RESPONSE | 12 | 4 | 0+ | 4 | 20 |
| CMP_SWAP | 12 | 28 | 0 | 4 | 44 |
| FETCH_ADD | 12 | 28 | 0 | 4 | 44 |
| ACK | 12 | 4 | 0 | 4 | 20 |
| ATOMIC_ACK | 12 | 12 | 0 | 4 | 28 |

---

## 6. Cross-References

### Related Documents

| Document | Content |
|----------|---------|
| [packet_taxonomy.md](packet_taxonomy.md) | Master index |
| [packet_taxonomy_ue_pds.md](packet_taxonomy_ue_pds.md) | UE+ PDS (alternative transport) |

### Datamodel Files

| File | Description |
|------|-------------|
| `bth.ksy` | Base Transport Header (12 bytes) |
| `reth.ksy` | RDMA Extended Transport Header (16 bytes) |
| `aeth.ksy` | ACK Extended Transport Header (4 bytes) |
| `atomiceth.ksy` | Atomic Extended Transport Header (28 bytes) |
| `atomicacketh.ksy` | Atomic ACK ETH (8 bytes) |
| `deth.ksy` | Datagram Extended Transport Header (8 bytes) |
| `immdt.ksy` | Immediate Data (4 bytes) |
| `icrc.ksy` | Invariant CRC (4 bytes) |

---

## 7. References

- InfiniBand Architecture Specification Volume 1, Release 1.4
- RoCEv2 Annex A17 (IBTA)
- RFC 4391 (Transmission of IP Datagrams over InfiniBand)
