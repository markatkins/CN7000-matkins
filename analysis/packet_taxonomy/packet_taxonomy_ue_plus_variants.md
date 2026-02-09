# PMR Packet Taxonomy: UE+ Packet Variants

**Parent Document**: [packet_taxonomy.md](packet_taxonomy.md)  
**Scope**: UE+ (Cornelis Proprietary) packet variants based on UltraEthernet Specification  
**Datamodel Directories**: `datamodel/protocols/cornelis/`, `datamodel/protocols/ue/`  
**Reference**: CN7000 Packet Taxonomy.ppt, UE Specification v1.0.1  
**Last Updated**: 2026-02-03

---

## Table of Contents

1. [Overview](#1-overview)
2. [L2 Header Selection Rules](#2-l2-header-selection-rules)
3. [Header Building Blocks](#3-header-building-blocks)
4. [UE+ Packet Variant Matrix](#4-ue-packet-variant-matrix)
   - [4.1 Basic UE+ Packets](#41-basic-ue-packets-no-encryption)
   - [4.2 UE+ over IPv4 Packets](#42-ue-over-ipv4-packets-fep-mode)
   - [4.3 Encrypted UE+ Packets](#43-encrypted-ue-packets-tss)
5. [Detailed Packet Structures](#5-detailed-packet-structures)
   - [5.1 UE+ Standard Tagged Send](#51-ue-standard-tagged-send-som1)
   - [5.2 UE+ Small Message](#52-ue-small-message)
   - [5.3 UE+ with CSIG+ Telemetry](#53-ue-with-csig-telemetry)
   - [5.4 UE+ IPv4 (FEP Mode)](#54-ue-ipv4-fep-mode)
   - [5.5 UE+ Encrypted (TSS)](#55-ue-encrypted-tss)
   - [5.6 UE+ IPv4 Encrypted](#56-ue-ipv4-encrypted)
   - [5.7 UE+ with CSIG+ and TSS](#57-ue-with-csig-and-tss)
6. [SES Header Types](#6-ses-header-types)
7. [CSIG+ Telemetry Types](#7-csig-telemetry-types)
8. [Header Overhead Summary](#8-header-overhead-summary)
9. [Datamodel Coverage](#9-datamodel-coverage)
10. [References](#10-references)

---

## 1. Overview

This document describes UE+ packet variants - Cornelis Networks proprietary extensions to the UltraEthernet specification. UE+ packets use the Cornelis proprietary L2 header (`ue_plus.ksy`) combined with standard UE transport layers (PDS, SES, CMS, TSS) and optional Cornelis extensions (CSIG+).

### Key Characteristics

| Aspect | Description |
|--------|-------------|
| **L2 Header** | Cornelis proprietary 12-byte UE+ header with 24-bit HMAC addressing |
| **Transport** | Standard UE PDS/SES/CMS/TSS sublayers |
| **Telemetry** | Optional CSIG+ in-band telemetry (Cornelis proprietary) |
| **Security** | Optional TSS encryption (UE standard) |
| **FEP Mode** | IPv4/UDP encapsulation for Fabric Extension Profile |

### Relationship to UE Standard

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         UE+ (Cornelis Proprietary)                       │
├─────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────────────────────┐   │
│  │   UE+ L2    │ + │   CSIG+     │ + │   Standard UE Transport     │   │
│  │ (Cornelis)  │   │ (Cornelis)  │   │   (PDS/SES/CMS/TSS)         │   │
│  └─────────────┘   └─────────────┘   └─────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 2. L2 Header Selection Rules

This section documents when PMR uses the Cornelis UE+ header vs standard Ethernet.

### 2.1 Decision Matrix

| Condition | L2 Header | Network Header | Notes |
|-----------|-----------|----------------|-------|
| Both endpoints support UE+ | UE+ (12B) | UFH-16/32 | Fabric-managed HMAC addressing |
| Peer is standard UE endpoint | Ethernet II (14B) | IPv4/IPv6 + UDP | Standard UE encapsulation |
| Peer is RoCEv2 endpoint | Ethernet II (14B) | IPv4/IPv6 + UDP | RoCEv2 always uses Ethernet |
| Standard Ethernet traffic | Ethernet II (14B) | IPv4/IPv6 | PTP, management, netdev |
| Non-managed configuration | Ethernet II (14B) | IPv4/IPv6 | No fabric management |

### 2.2 UE+ Header Conditions

PMR uses the UE+ header (12-byte Cornelis L2) when **ALL** of the following are true:

1. **Link negotiates UE+ capability**: The physical link must negotiate support for UE+
2. **Peer supports UE+**: The destination endpoint must have UE+ capability
3. **Fabric management active**: Hierarchical MAC (HMAC) addresses are assigned
4. **Address Vector configured for UE+**: Software has configured the AV for UE+ mode

### 2.3 Standard Ethernet Conditions

PMR uses standard Ethernet II (14-byte) when **ANY** of the following are true:

1. **Peer doesn't support UE+**: Non-Cornelis endpoints or standard UE implementations
2. **RoCEv2 protocol**: RoCEv2 always uses Ethernet + IPv4/IPv6 + UDP encapsulation
3. **Standard UE encapsulation**: When using UDP-based UE transport per UE Spec
4. **Ethernet services**: PTP (IEEE 1588), management traffic, netdev interfaces
5. **Non-managed mode**: When fabric management is not configured

### 2.4 Simultaneous Protocol Support

**Key Architecture Principle** (HFI_ARCH_003):
> "The HFI shall support simultaneous use of UE+ and standard Ethernet packets"

- PMR does **NOT** operate in a single protocol "mode"
- An application can use RoCE, UE, and UE+ simultaneously
- Selection is **per-destination** based on Address Vector (AV) configuration
- Software (libfabric) hides the L2 header distinction from applications
- Neither HFI nor switch performs UE+ ↔ UE gateway conversion

### 2.5 Address Vector Role

The libfabric Address Vector (AV) determines L2 header selection:

| AV Configuration | L2 Header | Addressing |
|------------------|-----------|------------|
| UE+ peer (HMAC) | UE+ 12B | 24-bit Hierarchical MAC |
| Standard UE peer | Ethernet II 14B | 48-bit MAC + IPv4/IPv6 |
| RoCEv2 peer | Ethernet II 14B | 48-bit MAC + IPv4/IPv6 |

### 2.6 Reference

- CN7000 HFI Requirements, Section "Introduction" (UE+ definition)
- CN7000 HFI Requirements, HFI_ARCH_003 (simultaneous protocol support)
- CN7000 HFI Requirements, "Protocol Processing Units" section

### 2.7 Datamodel Support

The following datamodel files support L2 header selection:

| File | Purpose |
|------|---------|
| `ue/link/lldp/protocols/link_negotiation_sm.ksy` | Link capability negotiation state machine |
| `cornelis/config/address_vector.ksy` | Per-destination protocol configuration |
| `cornelis/protocols/l2_header_selection_sm.ksy` | L2 header selection decision logic |
| `cornelis/config/peer_capability.ksy` | Per-peer capability state |

These files model the **decision logic** for L2 header selection, complementing the existing packet format definitions. They enable:
- Simulation of link negotiation behavior
- Per-destination protocol selection via Address Vector
- Tracking of peer capabilities discovered via LLDP
- Decision tree evaluation for each packet

---

## 3. Header Building Blocks

### 3.1 Cornelis Proprietary Headers

| Header | Size | Datamodel | Description |
|--------|------|-----------|-------------|
| **UE+ L2** | 12 bytes | `cornelis/link/ue_plus.ksy` | Cornelis L2 header with 24-bit HMAC addressing |
| **CSIG+** | 4 bytes | `cornelis/transport/csig_plus.ksy` | In-band telemetry header |
| **UFH-16+** | 12 bytes | `cornelis/network/ufh_16_plus.ksy` | 16-bit forwarding (Cornelis extension) |
| **UFH-32+** | 12 bytes | `cornelis/network/ufh_32_plus.ksy` | 32-bit forwarding (Cornelis extension) |
| **VxLAN+** | 4 bytes | `cornelis/encapsulation/vxlan_plus.ksy` | Fabric-aware overlay |
| **PKEY** | 2 bytes | `cornelis/transport/pkey.ksy` | Partition key isolation |

### 3.2 UE Standard Headers

| Header | Size | Datamodel | Description |
|--------|------|-----------|-------------|
| **TSS** | 12-16 bytes | `ue/transport/tss/security_header.ksy` | Transport Security Sublayer |
| **PDS Prologue** | 24 bytes | `ue/transport/pds/prologue.ksy` | Packet Delivery Sublayer |
| **SES Standard** | 64 bytes | `ue/transport/ses/standard_request_som1.ksy` | Standard request header |
| **SES Small** | 32 bytes | `ue/transport/ses/small_message.ksy` | Small message header |
| **SES Response** | Variable | `ue/transport/ses/response.ksy` | Response header |

### 3.3 Standard Network Headers

| Header | Size | Datamodel | Description |
|--------|------|-----------|-------------|
| **Ethernet II** | 14 bytes | `ethernet/ethernet_ii.ksy` | Standard Ethernet frame |
| **IPv4** | 20+ bytes | `ethernet/ipv4.ksy` | Internet Protocol v4 |
| **IPv6** | 40 bytes | `ethernet/ipv6.ksy` | Internet Protocol v6 |
| **UDP** | 8 bytes | `ethernet/udp.ksy` | User Datagram Protocol |

---

## 4. UE+ Packet Variant Matrix

### 4.1 Basic UE+ Packets (No Encryption)

| Variant | Header Stack | Min Overhead | Max Overhead | Use Case |
|---------|--------------|--------------|--------------|----------|
| **UE+ Standard** | UE+ → PDS → SES(std) | 100 bytes | 100 bytes | Standard tagged send/recv |
| **UE+ Small** | UE+ → PDS → SES(small) | 68 bytes | 68 bytes | Small messages (<256B) |
| **UE+ Medium** | UE+ → PDS → SES(medium) | ~56 bytes | ~56 bytes | Optimized non-matching |
| **UE+ Response** | UE+ → PDS → SES(resp) | ~48 bytes | ~64 bytes | Response packets |
| **UE+ with CSIG+** | UE+ → CSIG+ → PDS → SES(std) | 104 bytes | 104 bytes | Standard + telemetry |
| **UE+ Small + CSIG+** | UE+ → CSIG+ → PDS → SES(small) | 72 bytes | 72 bytes | Small msg + telemetry |

### 4.2 UE+ over IPv4 Packets (FEP Mode)

| Variant | Header Stack | Min Overhead | Max Overhead | Use Case |
|---------|--------------|--------------|--------------|----------|
| **UE+ IPv4** | Eth → IPv4 → UDP → PDS → SES(std) | 130 bytes | 130 bytes | Fabric Extension Profile |
| **UE+ IPv4 Small** | Eth → IPv4 → UDP → PDS → SES(small) | 98 bytes | 98 bytes | FEP small messages |
| **UE+ IPv4 + CSIG+ Compact** | Eth → IPv4 → UDP → CSIG+(4B) → PDS → SES | 134 bytes | 134 bytes | FEP + compact telemetry |
| **UE+ IPv4 + CSIG+ Wide** | Eth → IPv4 → UDP → CSIG+(8B) → PDS → SES | 138 bytes | 138 bytes | FEP + extended telemetry |

### 4.3 Encrypted UE+ Packets (TSS)

| Variant | Header Stack | Min Overhead | Max Overhead | Use Case |
|---------|--------------|--------------|--------------|----------|
| **UE+ Encrypted** | UE+ → TSS → PDS → SES(std) | 112 bytes | 116 bytes | Secure domain traffic |
| **UE+ Encrypted Small** | UE+ → TSS → PDS → SES(small) | 80 bytes | 84 bytes | Secure small messages |
| **UE+ IPv4 Encrypted** | Eth → IPv4 → UDP → TSS → PDS → SES | 142 bytes | 146 bytes | Secure FEP traffic |
| **UE+ Encrypted + CSIG+** | UE+ → CSIG+ → TSS → PDS → SES | 116 bytes | 120 bytes | Secure + telemetry |

> **Note**: TSS header is 12 bytes when sp=0 (no SSI), 16 bytes when sp=1 (SSI present).
> All encrypted packets include a 16-byte AES-GCM authentication tag at the end.

---

## 5. Detailed Packet Structures

### 5.1 UE+ Standard Tagged Send (SOM=1)

**Use Case**: Standard tagged send/receive operations with full SES header.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        UE+ Standard Tagged Send (SOM=1)                      │
├─────────────────┬───────────────────┬─────────────────────┬─────────────────┤
│   UE+ L2 (12B)  │     PDS (24B)     │    SES Std (64B)    │    Payload      │
├─────────────────┼───────────────────┼─────────────────────┼─────────────────┤
│ Byte 0:         │ Byte 0:           │ Byte 0-1:           │                 │
│  L2[7:6]        │  type[4:0]        │  opcode[15:0]       │                 │
│  V[5:4]         │  flags[2:0]       │                     │                 │
│  zyxm[3:0]=0010 │                   │ Byte 2-9:           │                 │
│                 │ Byte 1-3:         │  tag[63:0]          │                 │
│ Byte 1:         │  psn[23:0]        │                     │                 │
│  Length[7:2]    │                   │ Byte 10-13:         │                 │
│  RC[1:0]        │ Byte 4-6:         │  src_id[31:0]       │   User Data     │
│                 │  ack_psn[23:0]    │                     │                 │
│ Byte 2:         │                   │ Byte 14-17:         │                 │
│  RC[0]          │ Byte 7:           │  length[31:0]       │                 │
│  SC[6:3]        │  next_hdr[3:0]=3  │                     │                 │
│  Hop[2:0]       │  flags2[3:0]      │ Byte 18-25:         │                 │
│                 │                   │  offset[63:0]       │                 │
│ Byte 3-5:       │ Byte 8-23:        │                     │                 │
│  DLID[23:0]     │  pdc_info         │ Byte 26-29:         │                 │
│                 │  (16 bytes)       │  rkey[31:0]         │                 │
│ Byte 6-7:       │                   │                     │                 │
│  Entropy[15:0]  │                   │ Byte 30-37:         │                 │
│                 │                   │  match_bits[63:0]   │                 │
│ Byte 8:         │                   │                     │                 │
│  Reserved       │                   │ Byte 38-63:         │                 │
│                 │                   │  context/extensions │                 │
│ Byte 9-11:      │                   │                     │                 │
│  SLID[23:0]     │                   │                     │                 │
└─────────────────┴───────────────────┴─────────────────────┴─────────────────┘

Total Header Overhead: 100 bytes (12 + 24 + 64)
Datamodel Files:
  - cornelis/link/ue_plus.ksy
  - ue/transport/pds/prologue.ksy
  - ue/transport/ses/standard_request_som1.ksy
```

### 5.2 UE+ Small Message

**Use Case**: Small messages under 256 bytes with reduced header overhead.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           UE+ Small Message                                  │
├─────────────────┬───────────────────┬─────────────────────┬─────────────────┤
│   UE+ L2 (12B)  │     PDS (24B)     │   SES Small (32B)   │    Payload      │
├─────────────────┼───────────────────┼─────────────────────┼─────────────────┤
│ Byte 0:         │ Byte 0:           │ Byte 0-1:           │                 │
│  L2|V|zyxm      │  type|flags       │  opcode[15:0]       │                 │
│                 │                   │                     │                 │
│ Byte 1:         │ Byte 1-3:         │ Byte 2-9:           │                 │
│  Length|RC      │  psn[23:0]        │  tag[63:0]          │                 │
│                 │                   │                     │                 │
│ Byte 2:         │ Byte 4-6:         │ Byte 10-13:         │  User Data      │
│  RC|SC|Hop      │  ack_psn[23:0]    │  src_id[31:0]       │  (< 256 bytes)  │
│                 │                   │                     │                 │
│ Byte 3-5:       │ Byte 7:           │ Byte 14-17:         │                 │
│  DLID[23:0]     │  next_hdr[3:0]=1  │  length[31:0]       │                 │
│                 │  (SMALL)          │                     │                 │
│ Byte 6-7:       │                   │ Byte 18-25:         │                 │
│  Entropy[15:0]  │ Byte 8-23:        │  match_bits[63:0]   │                 │
│                 │  pdc_info         │                     │                 │
│ Byte 8:         │                   │ Byte 26-31:         │                 │
│  Reserved       │                   │  reserved/context   │                 │
│                 │                   │                     │                 │
│ Byte 9-11:      │                   │                     │                 │
│  SLID[23:0]     │                   │                     │                 │
└─────────────────┴───────────────────┴─────────────────────┴─────────────────┘

Total Header Overhead: 68 bytes (12 + 24 + 32)
Datamodel Files:
  - cornelis/link/ue_plus.ksy
  - ue/transport/pds/prologue.ksy
  - ue/transport/ses/small_message.ksy
```

### 5.3 UE+ with CSIG+ Telemetry

**Use Case**: Standard traffic with in-band network telemetry for monitoring.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      UE+ with CSIG+ Telemetry                                │
├─────────────────┬───────────┬───────────────────┬───────────────┬───────────┤
│   UE+ L2 (12B)  │ CSIG+(4B) │     PDS (24B)     │  SES Std(64B) │  Payload  │
├─────────────────┼───────────┼───────────────────┼───────────────┼───────────┤
│ Byte 0:         │ Byte 0:   │ Byte 0:           │               │           │
│  L2|V|zyxm      │  Ver[7:4] │  type|flags       │   (same as    │           │
│                 │  Type[3:0]│                   │    4.1)       │           │
│ Byte 1:         │           │ Byte 1-3:         │               │           │
│  Length|RC      │ Byte 1:   │  psn[23:0]        │               │           │
│                 │  Flags    │                   │               │  User     │
│ Byte 2:         │  [7:0]    │ Byte 4-6:         │               │  Data     │
│  RC|SC|Hop      │           │  ack_psn[23:0]    │               │           │
│                 │ Byte 2-3: │                   │               │           │
│ Byte 3-5:       │  Telemetry│ Byte 7:           │               │           │
│  DLID[23:0]     │  Data     │  next_hdr=3       │               │           │
│                 │  [15:0]   │                   │               │           │
│ Byte 6-7:       │           │ Byte 8-23:        │               │           │
│  Entropy[15:0]  │           │  pdc_info         │               │           │
│                 │           │                   │               │           │
│ Byte 8:         │           │                   │               │           │
│  Reserved       │           │                   │               │           │
│                 │           │                   │               │           │
│ Byte 9-11:      │           │                   │               │           │
│  SLID[23:0]     │           │                   │               │           │
└─────────────────┴───────────┴───────────────────┴───────────────┴───────────┘

Total Header Overhead: 104 bytes (12 + 4 + 24 + 64)
Datamodel Files:
  - cornelis/link/ue_plus.ksy
  - cornelis/transport/csig_plus.ksy
  - ue/transport/pds/prologue.ksy
  - ue/transport/ses/standard_request_som1.ksy
```

### 5.4 UE+ IPv4 (FEP Mode)

**Use Case**: Fabric Extension Profile for routing UE traffic over IP networks.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        UE+ IPv4 (Fabric Extension Profile)                   │
├─────────┬─────────┬─────────┬───────────────────┬───────────────┬───────────┤
│Eth (14B)│IPv4(20B)│UDP (8B) │     PDS (24B)     │  SES Std(64B) │  Payload  │
├─────────┼─────────┼─────────┼───────────────────┼───────────────┼───────────┤
│ Byte 0-5│ Byte 0: │ Byte 0-1│ Byte 0:           │               │           │
│  DA[47:0│  Ver|IHL│  SrcPort│  type|flags       │   (same as    │           │
│         │         │  [15:0] │                   │    4.1)       │           │
│ Byte 6-1│ Byte 1: │         │ Byte 1-3:         │               │           │
│  SA[47:0│  TOS    │ Byte 2-3│  psn[23:0]        │               │           │
│         │         │  DstPort│                   │               │  User     │
│ Byte 12-│ Byte 2-3│  [15:0] │ Byte 4-6:         │               │  Data     │
│  Type   │  TotLen │  =4791  │  ack_psn[23:0]    │               │           │
│  [15:0] │         │  (RoCE) │                   │               │           │
│  =0x0800│ Byte 4-5│         │ Byte 7:           │               │           │
│  (IPv4) │  ID     │ Byte 4-5│  next_hdr=3       │               │           │
│         │         │  Length │                   │               │           │
│         │ Byte 6-7│         │ Byte 8-23:        │               │           │
│         │  Flags| │ Byte 6-7│  pdc_info         │               │           │
│         │  FragOff│  Chksum │                   │               │           │
│         │         │         │                   │               │           │
│         │ Byte 8: │         │                   │               │           │
│         │  TTL    │         │                   │               │           │
│         │         │         │                   │               │           │
│         │ Byte 9: │         │                   │               │           │
│         │  Proto  │         │                   │               │           │
│         │  =17(UDP│         │                   │               │           │
│         │         │         │                   │               │           │
│         │ Byte10-1│         │                   │               │           │
│         │  HdrChk │         │                   │               │           │
│         │         │         │                   │               │           │
│         │ Byte12-1│         │                   │               │           │
│         │  SrcAddr│         │                   │               │           │
│         │         │         │                   │               │           │
│         │ Byte16-1│         │                   │               │           │
│         │  DstAddr│         │                   │               │           │
└─────────┴─────────┴─────────┴───────────────────┴───────────────┴───────────┘

Total Header Overhead: 130 bytes (14 + 20 + 8 + 24 + 64)
Datamodel Files:
  - ethernet/ethernet_ii.ksy
  - ethernet/ipv4.ksy
  - ethernet/udp.ksy
  - ue/transport/pds/prologue.ksy
  - ue/transport/ses/standard_request_som1.ksy
```

### 5.5 UE+ Encrypted (TSS)

**Use Case**: Secure domain traffic with AES-GCM encryption.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        UE+ Encrypted (TSS, sp=1)                             │
├─────────────────┬───────────────────┬───────────────┬───────────┬───────────┤
│   UE+ L2 (12B)  │     TSS (16B)     │   PDS (24B)   │ SES (64B) │  Payload  │
├─────────────────┼───────────────────┼───────────────┼───────────┼───────────┤
│ Byte 0:         │ Byte 0:           │               │           │           │
│  L2|V|zyxm      │  type[4:0]=1      │               │           │           │
│                 │  sp[0]=1          │               │           │           │
│ Byte 1:         │  r[0]=0           │   (same as    │  (same as │           │
│  Length|RC      │  an[0]            │    above)     │   4.1)    │           │
│                 │                   │               │           │           │
│ Byte 2:         │ Byte 1-3:         │               │           │ Encrypted │
│  RC|SC|Hop      │  SDI[23:0]        │               │           │   Data    │
│                 │  (Secure Domain)  │               │           │           │
│ Byte 3-5:       │                   │               │           │           │
│  DLID[23:0]     │ Byte 4-7:         │               │           │           │
│                 │  SSI[31:0]        │               │           │           │
│ Byte 6-7:       │  (Source ID)      │               │           │           │
│  Entropy[15:0]  │                   │               │           │           │
│                 │ Byte 8-15:        │               │           │           │
│ Byte 8:         │  TSC[63:0]        │               │           │           │
│  Reserved       │  (Timestamp)      │               │           │           │
│                 │  [epoch|counter]  │               │           │           │
│ Byte 9-11:      │                   │               │           │           │
│  SLID[23:0]     │                   │               │           │           │
└─────────────────┴───────────────────┴───────────────┴───────────┴───────────┘
                                                                  ┌───────────┐
                                                                  │Auth Tag   │
                                                                  │  (16B)    │
                                                                  └───────────┘

Total Header Overhead: 116 bytes (12 + 16 + 24 + 64) + 16-byte auth tag
Datamodel Files:
  - cornelis/link/ue_plus.ksy
  - ue/transport/tss/security_header.ksy
  - ue/transport/pds/prologue.ksy
  - ue/transport/ses/standard_request_som1.ksy

IV Construction (per Table 3-91):
  IV = SSI[31:0] || TSC[63:0]  (when sp=1)
  IV = ip.src_addr[31:0] || TSC[63:0]  (when sp=0, FEP mode)
```

### 5.6 UE+ IPv4 Encrypted

**Use Case**: Secure Fabric Extension Profile traffic.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      UE+ IPv4 Encrypted (FEP + TSS)                          │
├─────────┬─────────┬─────────┬───────────┬───────────┬───────────┬───────────┤
│Eth (14B)│IPv4(20B)│UDP (8B) │ TSS (16B) │ PDS (24B) │ SES (64B) │  Payload  │
├─────────┼─────────┼─────────┼───────────┼───────────┼───────────┼───────────┤
│         │         │         │           │           │           │           │
│  (same  │  (same  │  (same  │  (same as │  (same as │  (same as │ Encrypted │
│  as 4.4)│  as 4.4)│  as 4.4)│   4.5)    │   above)  │   4.1)    │   Data    │
│         │         │         │           │           │           │           │
└─────────┴─────────┴─────────┴───────────┴───────────┴───────────┴───────────┘
                                                                  ┌───────────┐
                                                                  │Auth Tag   │
                                                                  │  (16B)    │
                                                                  └───────────┘

Total Header Overhead: 146 bytes (14 + 20 + 8 + 16 + 24 + 64) + 16-byte auth tag
```

### 5.7 UE+ with CSIG+ and TSS

**Use Case**: Secure traffic with telemetry monitoring.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    UE+ with CSIG+ and TSS (Full Stack)                       │
├─────────────────┬───────────┬───────────┬───────────┬───────────┬───────────┤
│   UE+ L2 (12B)  │ CSIG+(4B) │ TSS (16B) │ PDS (24B) │ SES (64B) │  Payload  │
├─────────────────┼───────────┼───────────┼───────────┼───────────┼───────────┤
│                 │           │           │           │           │           │
│  (same as 4.1)  │ (same as  │ (same as  │ (same as  │ (same as  │ Encrypted │
│                 │   4.3)    │   4.5)    │  above)   │   4.1)    │   Data    │
│                 │           │           │           │           │           │
└─────────────────┴───────────┴───────────┴───────────┴───────────┴───────────┘
                                                                  ┌───────────┐
                                                                  │Auth Tag   │
                                                                  │  (16B)    │
                                                                  └───────────┘

Total Header Overhead: 120 bytes (12 + 4 + 16 + 24 + 64) + 16-byte auth tag
```

---

## 6. SES Header Types

The `next_hdr` field in PDS identifies the SES header format (UE Spec Table 3-16):

| Value | Mnemonic | Size | Datamodel File | Description |
|-------|----------|------|----------------|-------------|
| 0x0 | UET_HDR_NONE | 0 | — | No SES header follows |
| 0x1 | UET_HDR_REQUEST_SMALL | 32B | `small_message.ksy`, `small_rma.ksy` | Small request format |
| 0x2 | UET_HDR_REQUEST_MEDIUM | Var | `optimized_non_matching.ksy` | Medium/optimized request |
| 0x3 | UET_HDR_REQUEST_STD | 64B | `standard_request_som1.ksy`, `standard_request_som0.ksy` | Standard request format |
| 0x4 | UET_HDR_RESPONSE | Var | `response.ksy` | Response (no data) |
| 0x5 | UET_HDR_RESPONSE_DATA | Var | `response_with_data.ksy` | Response with data |
| 0x6 | UET_HDR_RESPONSE_DATA_SMALL | Var | `optimized_response_with_data.ksy` | Small response with data |
| 0x7-0xF | Reserved | — | — | Reserved for future use |

### SES Header Selection by Operation

| Operation Type | SES Header | next_hdr |
|----------------|------------|----------|
| Tagged Send (large) | Standard Request | 0x3 |
| Tagged Send (small, <256B) | Small Message | 0x1 |
| Tagged Recv | Standard Request | 0x3 |
| RMA Write | Standard Request | 0x3 |
| RMA Read Request | Standard Request | 0x3 |
| RMA Read Response | Response with Data | 0x5 |
| Atomic (CAS/FAA) | Standard Request + Atomic Ext | 0x3 |
| Small RMA | Small RMA | 0x1 |
| Non-Matching | Optimized Non-Matching | 0x2 |

---

## 7. CSIG+ Telemetry Types

CSIG+ provides in-band telemetry with the following types (Cornelis proprietary):

| Type | Name | Data Format | Telemetry Data Bits | Use Case |
|------|------|-------------|---------------------|----------|
| 0 | Latency | Accumulated ns | [15:0] = nanoseconds | Per-hop latency measurement |
| 1 | Queue Depth | Occupancy + QID | [15:8] = %, [7:0] = QID | Queue monitoring |
| 2 | Congestion | ECN + Level | [15:14] = ECN, [13:8] = level | Congestion notification |
| 3 | Path Trace | Switch ID | [15:0] = switch_id | Path verification |
| 4 | Timestamp | Truncated time | [15:0] = timestamp | Timing correlation |
| 5-14 | Reserved | — | — | Future use |
| 15 | Custom | Vendor-defined | [15:0] = custom | Vendor extensions |

### CSIG+ Flags

| Bit | Name | Description |
|-----|------|-------------|
| 7 | Accumulate | Add hop data (vs replace) |
| 6 | Report | Generate telemetry report |
| 5 | Sink | Final hop for telemetry |
| 4 | Source | Originating hop |
| 3:0 | Type-specific | Varies by telemetry type |

---

## 8. Header Overhead Summary

### By Packet Variant

| Variant | L2 | Telemetry | Security | Transport | Total | Efficiency (4KB) |
|---------|-----|-----------|----------|-----------|-------|------------------|
| UE+ Standard | 12 | 0 | 0 | 88 | 100 | 97.6% |
| UE+ Small | 12 | 0 | 0 | 56 | 68 | 98.4% |
| UE+ + CSIG+ | 12 | 4 | 0 | 88 | 104 | 97.5% |
| UE+ Encrypted | 12 | 0 | 16+16 | 88 | 132 | 96.9% |
| UE+ IPv4 | 42 | 0 | 0 | 88 | 130 | 96.9% |
| UE+ IPv4 Encrypted | 42 | 0 | 16+16 | 88 | 162 | 96.2% |
| UE+ Full Stack | 12 | 4 | 16+16 | 88 | 136 | 96.8% |

> **Note**: Efficiency = Payload / (Payload + Overhead) for 4KB payload.
> Auth tag (16B) included in encrypted variants.

### Comparison with RoCEv2

| Protocol | Min Overhead | Max Overhead | 4KB Efficiency |
|----------|--------------|--------------|----------------|
| UE+ Standard | 100 bytes | 100 bytes | 97.6% |
| UE+ Small | 68 bytes | 68 bytes | 98.4% |
| RoCEv2 (IPv4) | 58 bytes | 78 bytes | 98.6% |
| RoCEv2 (IPv6) | 78 bytes | 98 bytes | 98.1% |

---

## 9. Datamodel Coverage

### Cornelis Proprietary Headers

| Header | File | Status | Lines |
|--------|------|--------|-------|
| UE+ L2 | `cornelis/link/ue_plus.ksy` | Complete | 394 |
| CSIG+ | `cornelis/transport/csig_plus.ksy` | Complete | 202 |
| UFH-16+ | `cornelis/network/ufh_16_plus.ksy` | Complete | 244 |
| UFH-32+ | `cornelis/network/ufh_32_plus.ksy` | Complete | 240 |
| VxLAN+ | `cornelis/encapsulation/vxlan_plus.ksy` | Complete | ~100 |
| PKEY | `cornelis/transport/pkey.ksy` | Complete | ~80 |
| Cornelis L2 Prefix | `cornelis/link/cornelis_l2_prefix.ksy` | Complete | ~60 |

### UE Standard Headers (Used by UE+)

| Header | File | Status |
|--------|------|--------|
| TSS Security | `ue/transport/tss/security_header.ksy` | Complete |
| PDS Prologue | `ue/transport/pds/prologue.ksy` | Complete |
| SES Standard Request | `ue/transport/ses/standard_request_som1.ksy` | Complete |
| SES Small Message | `ue/transport/ses/small_message.ksy` | Complete |
| SES Response | `ue/transport/ses/response.ksy` | Complete |
| SES Response with Data | `ue/transport/ses/response_with_data.ksy` | Complete |
| Next Header Types | `ue/transport/ses/next_header_types.ksy` | Complete |

### All SES Header Types

| Type | File | Status |
|------|------|--------|
| Standard Request (SOM=1) | `standard_request_som1.ksy` | Complete |
| Standard Request (SOM=0) | `standard_request_som0.ksy` | Complete |
| Small Message | `small_message.ksy` | Complete |
| Small RMA | `small_rma.ksy` | Complete |
| Optimized Non-Matching | `optimized_non_matching.ksy` | Complete |
| Response | `response.ksy` | Complete |
| Response with Data | `response_with_data.ksy` | Complete |
| Optimized Response with Data | `optimized_response_with_data.ksy` | Complete |
| Deferrable Send Request | `deferrable_send_request.ksy` | Complete |
| Rendezvous Extension | `rendezvous_extension.ksy` | Complete |
| Atomic Extension | `atomic_extension.ksy` | Complete |
| CAS Extension | `cas_extension.ksy` | Complete |
| Ready to Restart | `ready_to_restart.ksy` | Complete |

---

## 10. References

### Internal Documents

| Document | Description |
|----------|-------------|
| [packet_taxonomy.md](packet_taxonomy.md) | Master packet taxonomy index |
| [packet_taxonomy_cornelis.md](packet_taxonomy_cornelis.md) | Cornelis proprietary formats detail |
| [packet_taxonomy_ue_ses.md](packet_taxonomy_ue_ses.md) | UE SES sublayer formats |
| [packet_taxonomy_ue_pds.md](packet_taxonomy_ue_pds.md) | UE PDS sublayer formats |
| CN7000 Packet Taxonomy.ppt | Original PowerPoint reference |

### External Specifications

| Specification | Version | Sections |
|---------------|---------|----------|
| UE Specification | v1.0.1 | Table 3-16 (next_hdr), Table 3-90 (TSS), Section 3.5 (SES) |
| Cornelis UE+ Specification | 1.1 | UE+ L2 Header, CSIG+ Telemetry |

### Datamodel Directories

| Directory | Content |
|-----------|---------|
| `datamodel/protocols/cornelis/` | Cornelis proprietary headers |
| `datamodel/protocols/ue/` | UE standard headers |
| `datamodel/protocols/ethernet/` | Standard Ethernet/IP/UDP |

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-02-03 | Initial creation | Claude AI |
