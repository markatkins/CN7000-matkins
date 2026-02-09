# PMR Packet Taxonomy: Cornelis Proprietary Formats

**Parent Document**: [packet_taxonomy.md](packet_taxonomy.md)  
**Scope**: Cornelis Networks proprietary packet formats (UFH, CSIG+, VxLAN+, Collectives, Scale-Up)  
**Datamodel Directory**: `datamodel/protocols/cornelis/`  
**Last Updated**: 2026-01-26

---

## Table of Contents

1. [Overview](#1-overview)
2. [Link Layer](#2-link-layer)
   - [2.1 UE+ Header](#21-ue-header-12-bytes)
3. [Network Layer](#3-network-layer)
   - [3.1 UFH-16](#31-ufh-16-12-bytes)
   - [3.2 UFH-32](#32-ufh-32-12-bytes)
   - [3.3 Collective L2 (WIP)](#33-collective-l2-4-bytes-wip)
   - [3.4 Scale-Up L2 (WIP)](#34-scale-up-l2-4-bytes-wip)
4. [Transport Layer](#4-transport-layer)
   - [4.1 CSIG+ Telemetry](#41-csig-telemetry-4-bytes)
5. [Encapsulation](#5-encapsulation)
   - [5.1 VxLAN+](#51-vxlan-4-bytes)
6. [Cross-References](#6-cross-references)
7. [References](#7-references)

---

## 1. Overview

Cornelis Networks proprietary formats extend standard protocols with optimizations for high-performance computing and AI/ML workloads. These formats are designed for:

- **Efficiency**: Reduced header overhead for scale-up fabrics
- **Telemetry**: In-band network monitoring and diagnostics
- **Collectives**: Hardware-accelerated collective operations
- **Overlay**: Fabric-aware multi-tenant networking

### Format Summary

| Layer | Format | Size | Status | Description |
|-------|--------|------|--------|-------------|
| Link | UE+ Header | 12 bytes | Complete | Optimized L2 header |
| Network | UFH-16 | 12 bytes | Complete | 16-bit forwarding header |
| Network | UFH-32 | 12 bytes | Complete | 32-bit forwarding header |
| Network | Collective L2 | 4 bytes | **WIP** | HW-accelerated collectives |
| Network | Scale-Up L2 | 4 bytes | **WIP** | GPU cluster interconnect |
| Transport | CSIG+ | 4 bytes | Complete | In-band telemetry |
| Encapsulation | VxLAN+ | 4 bytes | Complete | Fabric-aware overlay |

---

## 2. Link Layer

### 2.1 UE+ Header (12 bytes)

**Datamodel**: `datamodel/protocols/cornelis/link/ue_plus.ksy`  
**Related Formats**: [UFH-16 (3.1)](#31-ufh-16-12-bytes) | [UFH-32 (3.2)](#32-ufh-32-12-bytes)  
**Work Item**: W-04-004 (updated 2026-01-26)

#### Wire Format

```
Byte 0:
  ┌─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┐
  │  7  │  6  │  5  │  4  │  3  │  2  │  1  │  0  │
  ├─────┴─────┼─────┴─────┼─────┴─────┴─────┴─────┤
  │   L2 (2)  │   V (2)   │       zyxm (4)        │
  └───────────┴───────────┴───────────────────────┘
  L2: CSR-configurable (avoids local MAC namespace conflicts)
  V:  Version
  zyxm: Local MAC indicator = 0b0010

Byte 1:
  ┌─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┐
  │  7  │  6  │  5  │  4  │  3  │  2  │  1  │  0  │
  ├─────┴─────┴─────┴─────┴─────┴─────┼─────┴─────┤
  │           Length (6)              │ RC[2:1]   │
  └───────────────────────────────────┴───────────┘

Byte 2:
  ┌─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┐
  │  7  │  6  │  5  │  4  │  3  │  2  │  1  │  0  │
  ├─────┼─────┴─────┴─────┴─────┼─────┴─────┴─────┤
  │RC[0]│        SC (4)         │    Hop (3)      │
  └─────┴───────────────────────┴─────────────────┘

Bytes 3-5: DLID/DMAC (24 bits)
  ┌─────────────────┬─────────────────┬─────────────────┐
  │    Byte 3       │    Byte 4       │    Byte 5       │
  │   [23:16]       │   [15:8]        │   [7:0]         │
  ├─────────────────┴─────────────────┴─────────────────┤
  │              DLID/DMAC (24 bits)                    │
  │         Destination Hierarchical MAC               │
  └─────────────────────────────────────────────────────┘

Bytes 6-7: Entropy (16 bits)
  ┌─────────────────┬─────────────────┐
  │    Byte 6       │    Byte 7       │
  ├─────────────────┴─────────────────┤
  │         Entropy (16 bits)         │
  └───────────────────────────────────┘

Byte 8: Reserved (8 bits)
  ┌─────────────────────────────────────┐
  │              Byte 8                 │
  ├─────────────────────────────────────┤
  │           Reserved (8)              │
  └─────────────────────────────────────┘

Bytes 9-11: SLID/SMAC (24 bits)
  ┌─────────────────┬─────────────────┬─────────────────┐
  │    Byte 9       │    Byte 10      │    Byte 11      │
  │   [23:16]       │   [15:8]        │   [7:0]         │
  ├─────────────────┴─────────────────┴─────────────────┤
  │              SLID/SMAC (24 bits)                    │
  │           Source Hierarchical MAC                  │
  └─────────────────────────────────────────────────────┘
```

#### Field Definitions

| Field | Bits | Byte.Bit | Description |
|-------|------|----------|-------------|
| L2 | 2 | 0[7:6] | L2 type identifier; CSR-configurable to avoid local MAC namespace conflicts |
| V | 2 | 0[5:4] | Version field |
| zyxm | 4 | 0[3:0] | Local MAC indicator; value = 0b0010 for UE+ |
| Length | 6 | 1[7:2] | Packet length (units TBD) |
| RC | 3 | 1[1:0], 2[7] | Routing Class; RC[2:1] in byte 1, RC[0] in byte 2 |
| SC | 4 | 2[6:3] | Service Class |
| Hop | 3 | 2[2:0] | Hop count (0-7) |
| DLID/DMAC | 24 | 3-5 | Destination Hierarchical MAC |
| Entropy | 16 | 6-7 | ECMP load balancing hash |
| Reserved | 8 | 8 | Reserved for future use |
| SLID/SMAC | 24 | 9-11 | Source Hierarchical MAC |

#### Terminology

| OPA Term | Cornelis Term | Description |
|----------|---------------|-------------|
| DLID | DMAC | Destination Hierarchical MAC (locally assigned) |
| SLID | SMAC | Source Hierarchical MAC (locally assigned) |
| LID | HMAC | Hierarchical MAC Address |
| HLID | HMAC | Hierarchical LID → Hierarchical MAC |

#### Next Header

The payload type is **not** part of the UE+ header. A 5-bit PDS-compatible next header indicator follows the UE+ header (exact format TBD).

#### HMAC Sub-Structure

The 24-bit Hierarchical MAC (HMAC) address format depends on the routing algorithm and network topology:

| Topology | Group | Switch-in-Group | Terminal | Total |
|----------|-------|-----------------|----------|-------|
| **No subdivision** | 12 bits (0-4095) | 6 bits (0-63) | 6 bits (0-63) | 24 bits |
| **x2 NIC subdivision** | 11 bits (0-2047) | 6 bits (0-63) | 7 bits (0-127) | 24 bits |
| **x8 NIC subdivision** | 9 bits (0-511) | 6 bits (0-63) | 9 bits (0-511) | 24 bits |

**No subdivision (12/6/6)**:
```
  ┌───────────────────────────────┬───────────────┬───────────────┐
  │         Group (12)            │ Switch (6)    │ Terminal (6)  │
  │        Bits 23:12             │ Bits 11:6     │ Bits 5:0      │
  └───────────────────────────────┴───────────────┴───────────────┘
```

**x2 NIC subdivision (11/6/7)**:
```
  ┌─────────────────────────────┬───────────────┬─────────────────┐
  │         Group (11)          │ Switch (6)    │  Terminal (7)   │
  │        Bits 23:13           │ Bits 12:7     │  Bits 6:0       │
  └─────────────────────────────┴───────────────┴─────────────────┘
```

**x8 NIC subdivision (9/6/9)**:
```
  ┌───────────────────────┬───────────────┬───────────────────────┐
  │      Group (9)        │ Switch (6)    │     Terminal (9)      │
  │     Bits 23:15        │ Bits 14:9     │      Bits 8:0         │
  └───────────────────────┴───────────────┴───────────────────────┘
```

---

## 3. Network Layer

### 3.1 UFH-16 (12 bytes)

**Datamodel**: `datamodel/protocols/cornelis/network/ufh_16_plus.ksy`  
**UE Standard**: `datamodel/protocols/ue/network/ufh_16.ksy`  
**Related Formats**: [UFH-32 (3.2)](#32-ufh-32-12-bytes)

UFH-16 overlays the Ethernet MAC Destination (bytes 0-5) and MAC Source (bytes 6-11) fields to provide efficient scale-up fabric forwarding with 16-bit addressing.

#### Wire Format

```
         MAC Destination (bytes 0-5)              MAC Source (bytes 6-11)
+-------+-------+-------+-------+-------+-------+-------+-------+-------+-------+-------+-------+
| Byte 0| Byte 1| Byte 2| Byte 3| Byte 4| Byte 5| Byte 6| Byte 7| Byte 8| Byte 9|Byte 10|Byte 11|
+-------+-------+-------+-------+-------+-------+-------+-------+-------+-------+-------+-------+
|Type|  |    Opaque (24-bit)    | Destination   |Opaque |Traffic|   Opaque      |    Source     |
|[7:4]  |                       | (16-bit BE)   |[7:4]  |Class  |   (16-bit)    |  (16-bit BE)  |
|SLAP   |                       |               |Z|Y|X|M|[7:0]  |               |               |
|[3:0]  |                       |               |[3:0]  |       |               |               |
+-------+-------+-------+-------+-------+-------+-------+-------+-------+-------+-------+-------+
```

#### Field Definitions

| Field | Byte(s) | Bits | Description |
|-------|---------|------|-------------|
| Type | 0 | [7:4] | Packet type for forwarding decisions |
| SLAP (dest) | 0 | [3:0] | Z,Y,X,M bits for MAC Dest; Z,Y,X=001 (constrained) |
| Opaque | 1-3 | 24 | Opaque to hardware |
| Destination | 4-5 | 16 | Destination endpoint address (big-endian) |
| Opaque | 6 | [7:4] | Opaque to hardware |
| SLAP (src) | 6 | [3:0] | Z,Y,X,M bits for MAC Src; Z,Y,X=001 (constrained) |
| Traffic Class | 7 | [7:0] | QoS / priority classification |
| Opaque | 8-9 | 16 | Opaque to hardware |
| Source | 10-11 | 16 | Source endpoint address (big-endian) |

**SLAP Field Constraint**: Z,Y,X bits MUST be 001. M bit may be 0 or 1. Valid values: 0x2 or 0x3.

#### UFH-16 Type Values

| Value | Type | Description |
|-------|------|-------------|
| 0 | Data | Data packet |
| 1 | Control | Control packet |
| 2 | Collective | Collective operation packet |
| 3 | Credit | Credit/flow control |
| 4 | Management | Management packet |
| 5-14 | Reserved | Reserved for future use |
| 15 | Extended | UFH-32 extension follows |

**Usage**: Scale-up fabric forwarding, intra-pod communication, medium cluster networking (up to 65536 endpoints).

---

### 3.2 UFH-32 (12 bytes)

**Datamodel**: `datamodel/protocols/cornelis/network/ufh_32_plus.ksy`  
**UE Standard**: `datamodel/protocols/ue/network/ufh_32.ksy`  
**Related Formats**: [UFH-16 (3.1)](#31-ufh-16-12-bytes)

UFH-32 overlays the Ethernet MAC Destination (bytes 0-5) and MAC Source (bytes 6-11) fields to provide efficient scale-up fabric forwarding with 32-bit addressing for large-scale deployments.

#### Wire Format

```
         MAC Destination (bytes 0-5)              MAC Source (bytes 6-11)
+-------+-------+-------+-------+-------+-------+-------+-------+-------+-------+-------+-------+
| Byte 0| Byte 1| Byte 2| Byte 3| Byte 4| Byte 5| Byte 6| Byte 7| Byte 8| Byte 9|Byte 10|Byte 11|
+-------+-------+-------+-------+-------+-------+-------+-------+-------+-------+-------+-------+
|Type|  |       |   Destination (32-bit BE)     |HopLim |Traffic|       Source (32-bit BE)      |
|[7:4]  |Opaque |                               |[7:4]  |Class  |                               |
|SLAP   |       |                               |Z|Y|X|M|[7:0]  |                               |
|[3:0]  |       |                               |[3:0]  |       |                               |
+-------+-------+-------+-------+-------+-------+-------+-------+-------+-------+-------+-------+
```

#### Field Definitions

| Field | Byte(s) | Bits | Description |
|-------|---------|------|-------------|
| Type | 0 | [7:4] | Packet type for forwarding decisions |
| SLAP (dest) | 0 | [3:0] | Z,Y,X,M bits for MAC Dest; Z,Y,X=001 (constrained) |
| Opaque | 1 | [7:0] | Opaque to hardware |
| Destination | 2-5 | 32 | Destination endpoint address (big-endian) |
| Hop Limit | 6 | [7:4] | TTL/hop count |
| SLAP (src) | 6 | [3:0] | Z,Y,X,M bits for MAC Src; Z,Y,X=001 (constrained) |
| Traffic Class | 7 | [7:0] | QoS / priority classification |
| Source | 8-11 | 32 | Source endpoint address (big-endian) |

**SLAP Field Constraint**: Z,Y,X bits MUST be 001. M bit may be 0 or 1. Valid values: 0x2 or 0x3.

#### UFH-32 Type Values

| Value | Type | Description |
|-------|------|-------------|
| 0 | Data | Data packet |
| 1 | Control | Control packet |
| 2 | Collective | Collective operation packet |
| 3 | Credit | Credit/flow control |
| 4 | Management | Management packet |
| 5 | Multicast | Multicast packet |
| 6 | Barrier | Barrier synchronization |
| 7 | Reduction | Reduction operation |
| 8-14 | Reserved | Reserved for future use |
| 15 | Vendor | Vendor-specific packet |

**Usage**: Large-scale scale-up fabric forwarding (4+ billion endpoints), multi-pod communication, extended collective operations.

---

### 3.3 Collective L2 (4 bytes, **WIP**)

> ⚠️ **Work In Progress**: This format is based on spec_version 0.1. 
> The specification is incomplete. See [W-08-001](packet_taxonomy.md#91-open-issues).

**Datamodel**: `datamodel/protocols/cornelis/network/collective_l2.ksy`  
**Spec Status**: Draft (v0.1)  
**Related Work Item**: W-08-001

#### Wire Format

```
Byte:    0       1       2       3
     +-------+-------+-------+-------+
     |op |flg| grp_id|  seq  |dt |cnt|
     +-------+-------+-------+-------+

Byte 0 Detail:
  Bit:  7 6 5 4 3 2 1 0
       |  op   | flags |
       |(4 bit)|(4 bit)|

Byte 3 Detail:
  Bit:  7 6 5 4 3 2 1 0
       |dtype  |cnt_exp|
       |(4 bit)|(4 bit)|
```

#### Field Definitions

| Field | Bits | Offset | Description | Constraints |
|-------|------|--------|-------------|-------------|
| operation | 4 | 0[7:4] | Collective operation type | Per enum below |
| flags | 4 | 0[3:0] | Operation flags | See below |
| group_id | 8 | 1 | Collective group ID | Pre-configured group |
| sequence | 8 | 2 | Sequence number | For ordering |
| data_type | 4 | 3[7:4] | Element data type | Per enum below |
| count_exponent | 4 | 3[3:0] | Element count (2^n) | 1 to 32768 elements |

#### Flags

| Bit | Name | Description |
|-----|------|-------------|
| 3 | in_place | In-place operation |
| 2 | completion | Completion notification required |
| 1 | tree | Tree-based topology (vs ring) |
| 0 | root | This node is root |

#### Collective Operations

| Value | Operation | Description |
|-------|-----------|-------------|
| 0 | Barrier | Barrier synchronization |
| 1 | Broadcast | Broadcast from root |
| 2 | Reduce | Reduce to root |
| 3 | All-reduce | Reduce + broadcast |
| 4 | Scatter | Scatter from root |
| 5 | Gather | Gather to root |
| 6 | All-gather | Gather + broadcast |
| 7 | All-to-all | All-to-all exchange |
| 8 | Scan | Prefix scan |
| 9 | Reduce-scatter | Reduce-scatter |
| 10-14 | Reserved | Reserved |
| 15 | Custom | Custom operation |

#### Data Types

| Value | Type | Size |
|-------|------|------|
| 0 | INT8 | 1 byte |
| 1 | INT16 | 2 bytes |
| 2 | INT32 | 4 bytes |
| 3 | INT64 | 8 bytes |
| 4 | UINT8 | 1 byte |
| 5 | UINT16 | 2 bytes |
| 6 | UINT32 | 4 bytes |
| 7 | UINT64 | 8 bytes |
| 8 | FLOAT16 | 2 bytes |
| 9 | FLOAT32 | 4 bytes |
| 10 | FLOAT64 | 8 bytes |
| 11 | BFLOAT16 | 2 bytes |
| 12-14 | Reserved | - |
| 15 | Custom | Variable |

#### Known Gaps

- [ ] Reduction operation encoding not fully specified
- [ ] Group configuration protocol not defined
- [ ] Multi-phase operation sequencing incomplete
- [ ] Error handling not specified

#### Protocol Behavior (Preliminary)

**Hardware Acceleration**: Collective L2 enables hardware-accelerated MPI collective operations at the fabric level.

**Use Cases**:
- MPI_Allreduce, MPI_Barrier, MPI_Bcast
- AI/ML gradient aggregation
- HPC synchronization primitives

---

### 3.4 Scale-Up L2 (4 bytes, **WIP**)

> ⚠️ **Work In Progress**: This format is based on spec_version 0.1. 
> The specification is incomplete. See [W-08-002](packet_taxonomy.md#91-open-issues).

**Datamodel**: `datamodel/protocols/cornelis/network/scaleup_l2.ksy`  
**Spec Status**: Draft (v0.1)  
**Related Work Item**: W-08-002

#### Wire Format

```
Byte:    0       1       2       3
     +-------+-------+-------+-------+
     |v|type |pr| src_node| dst_node|flg|ch |
     +-------+-------+-------+-------+

Byte 0 Detail:
  Bit:  7 6 5 4 3 2 1 0
       |ver|  type |pri|
       |(2)|(4 bit)|(2)|

Byte 3 Detail:
  Bit:  7 6 5 4 3 2 1 0
       | flags |channel|
       |(4 bit)|(4 bit)|
```

#### Field Definitions

| Field | Bits | Offset | Description | Constraints |
|-------|------|--------|-------------|-------------|
| version | 2 | 0[7:6] | Protocol version | Must be 0 |
| packet_type | 4 | 0[5:2] | Packet type | Per enum below |
| priority | 2 | 0[1:0] | Priority level | 0-3 (3=highest) |
| source_node | 8 | 1 | Source node ID | 0-255 |
| dest_node | 8 | 2 | Destination node ID | 0-255 |
| flags | 4 | 3[7:4] | Control flags | See below |
| channel | 4 | 3[3:0] | Virtual channel | 0-15 |

#### Flags

| Bit | Name | Description |
|-----|------|-------------|
| 3 | last | Last packet in transfer |
| 2 | first | First packet in transfer |
| 1 | gpu_direct | GPU-direct enabled |
| 0 | zero_copy | Zero-copy enabled |

#### Packet Types

| Value | Type | Description |
|-------|------|-------------|
| 0 | Data | Data transfer |
| 1 | Credit | Credit return |
| 2 | RDMA Read Req | RDMA read request |
| 3 | RDMA Read Resp | RDMA read response |
| 4 | RDMA Write | RDMA write |
| 5 | Atomic | Atomic operation |
| 6 | Completion | Completion notification |
| 7 | Flow Control | Flow control |
| 8-14 | Reserved | Reserved |
| 15 | Management | Management packet |

#### Known Gaps

- [ ] GPU-direct integration details not specified
- [ ] NVLink interoperability not defined
- [ ] Credit management protocol incomplete
- [ ] Multi-rail support not specified

#### Protocol Behavior (Preliminary)

**Scale-Up Domain**: Scale-Up L2 provides optimized networking within a tightly-coupled compute domain (up to 256 nodes).

**Use Cases**:
- GPU cluster interconnect
- AI/ML training clusters
- HPC scale-up networking

---

## 4. Transport Layer

### 4.1 CSIG+ Telemetry (4 bytes)

**Datamodel**: `datamodel/protocols/cornelis/transport/csig_plus.ksy`

CSIG+ (Cornelis Signal Plus) provides in-band network telemetry for monitoring and diagnostics.

#### Wire Format

```
Byte:    0       1       2       3
     +-------+-------+-------+-------+
     |ver|typ| flags |  telemetry_data |
     +-------+-------+-------+-------+

Byte 0 Detail:
  Bit:  7 6 5 4 3 2 1 0
       |version|  type |
       |(4 bit)|(4 bit)|
```

#### Field Definitions

| Field | Bits | Offset | Description | Constraints |
|-------|------|--------|-------------|-------------|
| version | 4 | 0[7:4] | CSIG+ version | Must be 0 |
| telemetry_type | 4 | 0[3:0] | Telemetry type | Per enum below |
| flags | 8 | 1 | Control flags | See below |
| telemetry_data | 16 | 2-3 | Type-specific data | Per type |

#### Flags

| Bit | Name | Description |
|-----|------|-------------|
| 7 | accumulate | Add hop data (vs replace) |
| 6 | report | Generate telemetry report |
| 5 | sink | Final hop for telemetry |
| 4 | source | Originating hop |
| 3-0 | type_flags | Type-specific flags |

#### Telemetry Types

| Value | Type | Data Format |
|-------|------|-------------|
| 0 | Latency | Accumulated latency (16-bit ns) |
| 1 | Queue Depth | Queue % (8-bit) + Queue ID (8-bit) |
| 2 | Congestion | ECN (2-bit) + Level (6-bit) + Rsvd (8-bit) |
| 3 | Path Trace | Switch ID (16-bit) |
| 4 | Timestamp | Truncated timestamp (16-bit) |
| 5-14 | Reserved | Reserved |
| 15 | Custom | Vendor-specific |

#### Protocol Behavior

**In-Band Telemetry**: CSIG+ enables per-hop telemetry collection without out-of-band management traffic.

**Use Cases**:
- Per-hop latency measurement
- Queue depth monitoring
- Congestion detection
- Path verification

**Reference**: Cornelis Networks CSIG+ Specification

---

## 5. Encapsulation

### 5.1 VxLAN+ (4 bytes)

**Datamodel**: `datamodel/protocols/cornelis/encapsulation/vxlan_plus.ksy`

VxLAN+ extends standard VxLAN (RFC 7348) with fabric-aware overlay networking features.

#### Wire Format

```
Byte:    0       1       2       3
     +-------+-------+-------+-------+
     | flags |vni_hi |vni_mid|vni_lo|pri|
     +-------+-------+-------+-------+

Byte 0 Detail:
  Bit:  7 6 5 4 3 2 1 0
       |I|P|B|O| rsvd  |
```

#### Field Definitions

| Field | Bits | Offset | Description | Constraints |
|-------|------|--------|-------------|-------------|
| flags.I | 1 | 0[7] | VNI valid | Must be 1 |
| flags.P | 1 | 0[6] | Policy applied | Informational |
| flags.B | 1 | 0[5] | BUM traffic | Broadcast/Unknown/Multicast |
| flags.O | 1 | 0[4] | OAM frame | Operations/Admin/Maintenance |
| flags.rsvd | 4 | 0[3:0] | Reserved | Must be 0 |
| vni_high | 8 | 1 | VNI bits [23:16] | - |
| vni_mid | 8 | 2 | VNI bits [15:8] | - |
| vni_low | 4 | 3[7:4] | VNI bits [7:4] | Low nibble |
| priority | 4 | 3[3:0] | Fabric priority | 0-15 |

**Note**: VNI bits [3:0] are always 0 in VxLAN+, giving effective VNI granularity of 16.

#### Computed Fields

| Field | Computation | Description |
|-------|-------------|-------------|
| vni | `(vni_high << 16) \| (vni_mid << 8) \| (vni_low & 0xF0)` | 24-bit VNI |
| priority | `vni_low & 0x0F` | 4-bit priority |

#### Protocol Behavior

**Fabric-Aware Overlay**: VxLAN+ integrates overlay networking with fabric QoS and policy.

**Use Cases**:
- Multi-tenant fabric isolation
- VM/container networking
- Data center interconnect

**Reference**: RFC 7348 (VxLAN), Cornelis Networks VxLAN+ Specification

---

## 6. Additional Cornelis Formats

### 6.1 Cornelis L2 Prefix (1 byte)

**Datamodel**: `datamodel/protocols/cornelis/link/cornelis_l2_prefix.ksy`

Single-byte prefix for encapsulated Ethernet frames over Cornelis fabric.

#### Wire Format

```
Byte:    0
     +-------+
     |L2|pr|flg|
     +-------+

Bit:  7 6 5 4 3 2 1 0
     |L2T|pri| flags |
     |(2)|(2)|  (4)  |
```

#### Field Definitions

| Field | Bits | Offset | Description | Constraints |
|-------|------|--------|-------------|-------------|
| l2_type | 2 | 0[7:6] | L2 frame type | 00=Ethernet, 10=UE+ |
| priority | 2 | 0[5:4] | Fabric priority | 0-3 |
| flags | 4 | 0[3:0] | Control flags | See below |

#### L2 Type Values

| Value | Type | Description |
|-------|------|-------------|
| 00 | Ethernet | Standard Ethernet frame follows |
| 01 | Reserved | Reserved |
| 10 | UE+ | UE+ header follows |
| 11 | Reserved | Reserved |

#### Flags

| Bit | Name | Description |
|-----|------|-------------|
| 3 | Reserved | Reserved |
| 2 | Multicast | Multicast indicator |
| 1 | Tagged | VLAN tagged indicator |
| 0 | Reserved | Reserved |

---

### 6.2 PKEY (Partition Key, 2 bytes)

**Datamodel**: `datamodel/protocols/cornelis/transport/pkey.ksy`

Partition key for multi-tenant traffic isolation.

#### Wire Format

```
Byte:    0       1
     +-------+-------+
     |M|pkey_hi|pkey_lo|
     +-------+-------+

Byte 0 Detail:
  Bit:  7 6 5 4 3 2 1 0
       |M| pkey[14:8] |
```

#### Field Definitions

| Field | Bits | Offset | Description | Constraints |
|-------|------|--------|-------------|-------------|
| membership | 1 | 0[7] | Membership type | 1=full, 0=limited |
| pkey_high | 7 | 0[6:0] | P_Key bits [14:8] | Upper 7 bits |
| pkey_low | 8 | 1 | P_Key bits [7:0] | Lower 8 bits |

#### Computed Fields

| Field | Computation | Description |
|-------|-------------|-------------|
| pkey | `(pkey_high << 8) \| pkey_low` | 15-bit partition key |

#### Membership Types

| Value | Type | Description |
|-------|------|-------------|
| 1 | Full | Can communicate with all members |
| 0 | Limited | Can only communicate with full members |

#### Reserved Values

- P_Key 0x0000: Invalid
- P_Key 0x7FFF: Default partition (full membership only)

---

## 7. Cross-References

### Related Documents

| Document | Content |
|----------|---------|
| [packet_taxonomy.md](packet_taxonomy.md) | Master index |
| [packet_taxonomy_ue_pds.md](packet_taxonomy_ue_pds.md) | UE+ PDS formats |
| [packet_taxonomy_ue_ses.md](packet_taxonomy_ue_ses.md) | UE+ SES formats |

### Datamodel Files

| File | Description |
|------|-------------|
| `link/ue_plus.ksy` | UE+ L2 header (12 bytes) |
| `network/ufh_16_plus.ksy` | UFH-16+ Cornelis extension (12 bytes) |
| `network/ufh_32_plus.ksy` | UFH-32+ Cornelis extension (12 bytes) |
| `network/collective_l2.ksy` | Collective L2 (4 bytes, WIP) |
| `network/scaleup_l2.ksy` | Scale-Up L2 (4 bytes, WIP) |
| `transport/csig_plus.ksy` | CSIG+ telemetry (4 bytes) |
| `encapsulation/vxlan_plus.ksy` | VxLAN+ (4 bytes) |
| `link/cornelis_l2_prefix.ksy` | L2 Prefix (1 byte) |
| `transport/pkey.ksy` | Partition Key (2 bytes) |

---

## 8. References

- CN7000 Packet Taxonomy
- Cornelis Networks CSIG+ Specification
- Cornelis Networks VxLAN+ Specification
- RFC 7348 (VxLAN)
- IEEE 802.1Q (VLAN)
