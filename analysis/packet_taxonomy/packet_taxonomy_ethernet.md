# PMR Packet Taxonomy: Standard Ethernet Formats

**Parent Document**: [packet_taxonomy.md](packet_taxonomy.md)  
**Scope**: Standard Ethernet, VLAN, IPv4, IPv6, TCP, UDP formats  
**Datamodel Directory**: `datamodel/protocols/ethernet/`  
**Last Updated**: 2026-01-30

---

## Table of Contents

1. [Overview](#1-overview)
2. [Link Layer](#2-link-layer)
   - [2.1 Ethernet II](#21-ethernet-ii-14-bytes)
   - [2.2 VLAN 802.1Q](#22-vlan-8021q-4-bytes)
   - [2.3 IEEE 802.3/LLC/SNAP](#23-ieee-8023llcsnap)
3. [Network Layer](#3-network-layer)
   - [3.1 IPv4](#31-ipv4-20-bytes-minimum)
   - [3.2 IPv6](#32-ipv6-40-bytes)
4. [Transport Layer](#4-transport-layer)
   - [4.1 UDP](#41-udp-8-bytes)
   - [4.2 TCP](#42-tcp-20-bytes-minimum)
5. [Cross-References](#5-cross-references)
6. [References](#6-references)
7. [RSS (Receive Side Scaling)](#7-rss-receive-side-scaling)
   - [7.1 Hash Algorithm Selection](#71-hash-algorithm-selection-4-bytes)
   - [7.2 Hash Input Formats](#72-hash-input-formats-8-36-bytes)
   - [7.3 Toeplitz Hash Key](#73-toeplitz-hash-key-40-bytes)

---

## 1. Overview

This document covers 12 KSY datamodel files defining standard Ethernet formats used by PMR for:
- RoCEv2 encapsulation (UDP/IP/Ethernet)
- Standard Ethernet offload
- VxLAN+ overlay networking
- Management traffic
- Receive Side Scaling (RSS) for multi-queue distribution

---

## 2. Link Layer

### 2.1 Ethernet II (14 bytes)

**Datamodel**: `datamodel/protocols/ethernet/link/ethernet_ii.ksy`

#### Wire Format

```
Byte:    0       1       2       3       4       5       6       7
     +-------+-------+-------+-------+-------+-------+-------+-------+
     |              Destination MAC [47:0]                           |
     +-------+-------+-------+-------+-------+-------+-------+-------+
         8       9      10      11      12      13
     +-------+-------+-------+-------+-------+-------+
     |  (Dest cont'd)|        Source MAC [47:0]      |
     +-------+-------+-------+-------+-------+-------+
     |  (Source cont'd)              | EtherType     |
     +-------+-------+-------+-------+-------+-------+
```

#### Field Definitions

| Field | Bits | Offset | Description |
|-------|------|--------|-------------|
| dest_mac | 48 | 0-5 | Destination MAC address |
| src_mac | 48 | 6-11 | Source MAC address |
| ethertype | 16 | 12-13 | Protocol type |

#### Common EtherTypes

| Value | Protocol |
|-------|----------|
| 0x0800 | IPv4 |
| 0x86DD | IPv6 |
| 0x8100 | VLAN (802.1Q) |
| 0x88A8 | QinQ (802.1ad) |

**Note**: EtherType < 0x0600 indicates IEEE 802.3 frame with Length field (see Section 2.3).

---

### 2.2 VLAN 802.1Q (4 bytes)

**Datamodel**: `datamodel/protocols/ethernet/link/vlan_802_1q.ksy`

#### Wire Format

```
Byte:    0       1       2       3
     +-------+-------+-------+-------+
     |  TPID (0x8100)|PCP|D|  VID   |
     +-------+-------+-------+-------+

Bytes 0-1: TPID = 0x8100
Byte 2-3 Detail:
  Bit: 15 14 13 12 11 10 9 8 7 6 5 4 3 2 1 0
      | PCP  |D|         VID [11:0]         |
```

#### Field Definitions

| Field | Bits | Offset | Description |
|-------|------|--------|-------------|
| tpid | 16 | 0-1 | Tag Protocol ID (0x8100) |
| pcp | 3 | 2[7:5] | Priority Code Point (0-7) |
| dei | 1 | 2[4] | Drop Eligible Indicator |
| vid | 12 | 2[3:0], 3 | VLAN Identifier (0-4095) |

---

### 2.3 IEEE 802.3/LLC/SNAP

IEEE 802.3 frames use a Length field (< 0x0600) instead of EtherType, followed by LLC and optionally SNAP headers. Used for control-plane protocols (STP, CDP) and legacy protocol encapsulation.

#### 2.3.1 IEEE 802.3 MAC Frame (14 bytes)

**Datamodel**: `datamodel/protocols/ethernet/link/ethernet_802_3.ksy`

##### Wire Format

```
Byte:    0       1       2       3       4       5       6       7
     +-------+-------+-------+-------+-------+-------+-------+-------+
     |              Destination MAC [47:0]                           |
     +-------+-------+-------+-------+-------+-------+-------+-------+
         8       9      10      11      12      13
     +-------+-------+-------+-------+-------+-------+
     |  (Dest cont'd)|        Source MAC [47:0]      |
     +-------+-------+-------+-------+-------+-------+
     |  (Source cont'd)              |    Length     |
     +-------+-------+-------+-------+-------+-------+
```

##### Field Definitions

| Field | Bits | Offset | Description |
|-------|------|--------|-------------|
| dst_mac | 48 | 0-5 | Destination MAC address |
| src_mac | 48 | 6-11 | Source MAC address |
| length | 16 | 12-13 | LLC data length (must be < 0x0600) |

##### Key Constraints

- Length < 0x0600 (1536) distinguishes from Ethernet II EtherType
- Minimum frame: 64 bytes (with padding)
- Maximum frame: 1518 bytes (standard) or 9022 bytes (jumbo)

---

#### 2.3.2 LLC Header (3-4 bytes)

**Datamodel**: `datamodel/protocols/ethernet/link/llc.ksy`

##### Wire Format

```
Byte:    0       1       2       3 (optional)
     +-------+-------+-------+-------+
     |  DSAP |  SSAP | Control| Ext  |
     +-------+-------+-------+-------+

Byte 0 (DSAP) Detail:
  Bit: 7 6 5 4 3 2 1 0
      |   DSAP Address  |I/G|
      I/G: 0=Individual, 1=Group

Byte 1 (SSAP) Detail:
  Bit: 7 6 5 4 3 2 1 0
      |   SSAP Address  |C/R|
      C/R: 0=Command, 1=Response

Byte 2 (Control) Detail:
  Bits [1:0] = 11: U-format (1-byte control)
  Bits [1:0] = 00: I-format (2-byte control)
  Bits [1:0] = 01/10: S-format (2-byte control)
```

##### Field Definitions

| Field | Bits | Offset | Description |
|-------|------|--------|-------------|
| dsap | 8 | 0 | Destination Service Access Point |
| ssap | 8 | 1 | Source Service Access Point |
| control | 8 | 2 | Control field (first byte) |
| control_ext | 8 | 3 | Extended control (I/S-format only) |

##### Common LSAP Values

| Value | Protocol |
|-------|----------|
| 0x00 | Null LSAP |
| 0x42 | Spanning Tree Protocol (STP) |
| 0xAA | SNAP extension |
| 0xFE | OSI protocols (IS-IS, CLNP) |
| 0xF0 | NetBIOS |

---

#### 2.3.3 SNAP Extension (5 bytes)

**Datamodel**: `datamodel/protocols/ethernet/link/snap.ksy`

##### Wire Format

```
Byte:    0       1       2       3       4
     +-------+-------+-------+-------+-------+
     |         OUI [23:0]    | Protocol ID   |
     +-------+-------+-------+-------+-------+

OUI = 00:00:00 indicates Protocol ID is an EtherType value.
Other OUI values indicate vendor-specific protocol space.
```

##### Field Definitions

| Field | Bits | Offset | Description |
|-------|------|--------|-------------|
| oui | 24 | 0-2 | Organizationally Unique Identifier |
| protocol_id | 16 | 3-4 | Protocol identifier (EtherType when OUI=00:00:00) |

##### Common Protocol IDs (when OUI=00:00:00)

| Value | Protocol |
|-------|----------|
| 0x0800 | IPv4 |
| 0x0806 | ARP |
| 0x86DD | IPv6 |
| 0x809B | AppleTalk |

---

## 3. Network Layer

### 3.1 IPv4 (20 bytes minimum)

**Datamodel**: `datamodel/protocols/ethernet/network/ipv4.ksy`

#### Wire Format

```
Byte:    0       1       2       3       4       5       6       7
     +-------+-------+-------+-------+-------+-------+-------+-------+
     |Ver|IHL|  DSCP |ECN|     Total Length  |    Identification     |
     +-------+-------+-------+-------+-------+-------+-------+-------+
         8       9      10      11      12      13      14      15
     +-------+-------+-------+-------+-------+-------+-------+-------+
     |Flg|  Frag Offset  |  TTL  |Protocol |   Header Checksum     |
     +-------+-------+-------+-------+-------+-------+-------+-------+
        16      17      18      19
     +-------+-------+-------+-------+
     |         Source IP [31:0]      |
     +-------+-------+-------+-------+
        20      21      22      23
     +-------+-------+-------+-------+
     |       Destination IP [31:0]   |
     +-------+-------+-------+-------+
```

#### Field Definitions

| Field | Bits | Offset | Description |
|-------|------|--------|-------------|
| version | 4 | 0[7:4] | IP version (4) |
| ihl | 4 | 0[3:0] | Header length (words) |
| dscp | 6 | 1[7:2] | Differentiated Services |
| ecn | 2 | 1[1:0] | ECN bits |
| total_length | 16 | 2-3 | Total packet length |
| identification | 16 | 4-5 | Fragment ID |
| flags | 3 | 6[7:5] | DF, MF flags |
| frag_offset | 13 | 6[4:0], 7 | Fragment offset |
| ttl | 8 | 8 | Time to live |
| protocol | 8 | 9 | Next protocol |
| checksum | 16 | 10-11 | Header checksum |
| src_ip | 32 | 12-15 | Source IP |
| dst_ip | 32 | 16-19 | Destination IP |

#### Common Protocol Values

| Value | Protocol |
|-------|----------|
| 6 | TCP |
| 17 | UDP |

---

### 3.2 IPv6 (40 bytes)

**Datamodel**: `datamodel/protocols/ethernet/network/ipv6.ksy`

#### Wire Format

```
Byte:    0       1       2       3       4       5       6       7
     +-------+-------+-------+-------+-------+-------+-------+-------+
     |Ver| TC    |         Flow Label                |Payload Length |
     +-------+-------+-------+-------+-------+-------+-------+-------+
         8       9      10      11      12-23
     +-------+-------+-------+-------+-------+-------+-------+-------+
     |(PayLen)|Next H | Hop L |      Source Address [127:0]          |
     +-------+-------+-------+-------+-------+-------+-------+-------+
        24-39
     +-------+-------+-------+-------+-------+-------+-------+-------+
     |                  Destination Address [127:0]                  |
     +-------+-------+-------+-------+-------+-------+-------+-------+
```

#### Field Definitions

| Field | Bits | Offset | Description |
|-------|------|--------|-------------|
| version | 4 | 0[7:4] | IP version (6) |
| traffic_class | 8 | 0[3:0], 1[7:4] | Traffic class (DSCP+ECN) |
| flow_label | 20 | 1[3:0], 2-3 | Flow label |
| payload_length | 16 | 4-5 | Payload length |
| next_header | 8 | 6 | Next header type |
| hop_limit | 8 | 7 | Hop limit (TTL) |
| src_addr | 128 | 8-23 | Source address |
| dst_addr | 128 | 24-39 | Destination address |

---

## 4. Transport Layer

### 4.1 UDP (8 bytes)

**Datamodel**: `datamodel/protocols/ethernet/transport/udp.ksy`

#### Wire Format

```
Byte:    0       1       2       3       4       5       6       7
     +-------+-------+-------+-------+-------+-------+-------+-------+
     |   Source Port |    Dest Port  |     Length    |   Checksum    |
     +-------+-------+-------+-------+-------+-------+-------+-------+
```

#### Field Definitions

| Field | Bits | Offset | Description |
|-------|------|--------|-------------|
| src_port | 16 | 0-1 | Source port |
| dst_port | 16 | 2-3 | Destination port |
| length | 16 | 4-5 | UDP length |
| checksum | 16 | 6-7 | UDP checksum |

#### RoCEv2 Port

| Port | Protocol |
|------|----------|
| 4791 | RoCEv2 |

---

### 4.2 TCP (20 bytes minimum)

**Datamodel**: `datamodel/protocols/ethernet/transport/tcp.ksy`

#### Wire Format

```
Byte:    0       1       2       3       4       5       6       7
     +-------+-------+-------+-------+-------+-------+-------+-------+
     |   Source Port |    Dest Port  |        Sequence Number        |
     +-------+-------+-------+-------+-------+-------+-------+-------+
         8       9      10      11      12      13      14      15
     +-------+-------+-------+-------+-------+-------+-------+-------+
     |      Acknowledgment Number    |Offs|Rsvd|Flags|    Window     |
     +-------+-------+-------+-------+-------+-------+-------+-------+
        16      17      18      19
     +-------+-------+-------+-------+
     |   Checksum    | Urgent Ptr    |
     +-------+-------+-------+-------+
```

#### Field Definitions

| Field | Bits | Offset | Description |
|-------|------|--------|-------------|
| src_port | 16 | 0-1 | Source port |
| dst_port | 16 | 2-3 | Destination port |
| seq_num | 32 | 4-7 | Sequence number |
| ack_num | 32 | 8-11 | Acknowledgment number |
| data_offset | 4 | 12[7:4] | Header length (words) |
| reserved | 3 | 12[3:1] | Reserved |
| flags | 9 | 12[0], 13 | TCP flags |
| window | 16 | 14-15 | Window size |
| checksum | 16 | 16-17 | TCP checksum |
| urgent_ptr | 16 | 18-19 | Urgent pointer |

#### TCP Flags

| Bit | Flag | Description |
|-----|------|-------------|
| 8 | NS | ECN-nonce |
| 7 | CWR | Congestion Window Reduced |
| 6 | ECE | ECN-Echo |
| 5 | URG | Urgent |
| 4 | ACK | Acknowledgment |
| 3 | PSH | Push |
| 2 | RST | Reset |
| 1 | SYN | Synchronize |
| 0 | FIN | Finish |

---

## 5. Cross-References

### Related Documents

| Document | Content |
|----------|---------|
| [packet_taxonomy.md](packet_taxonomy.md) | Master index |
| [packet_taxonomy_rocev2.md](packet_taxonomy_rocev2.md) | RoCEv2 (uses UDP/IP) |

### Datamodel Files

| File | Description |
|------|-------------|
| `link/ethernet_ii.ksy` | Ethernet II (14 bytes) |
| `link/vlan_802_1q.ksy` | VLAN 802.1Q (4 bytes) |
| `link/ethernet_802_3.ksy` | IEEE 802.3 MAC Frame (14 bytes) |
| `link/llc.ksy` | LLC Header (3-4 bytes) |
| `link/snap.ksy` | SNAP Extension (5 bytes) |
| `network/ipv4.ksy` | IPv4 (20+ bytes) |
| `network/ipv6.ksy` | IPv6 (40 bytes) |
| `transport/udp.ksy` | UDP (8 bytes) |
| `transport/tcp.ksy` | TCP (20+ bytes) |
| `rss/hash_algorithm.ksy` | RSS Hash Algorithm Selection (4 bytes) |
| `rss/hash_input.ksy` | RSS Hash Input Formats (8-36 bytes) |
| `rss/toeplitz_key.ksy` | Toeplitz Hash Key (40 bytes) |

---

## 6. References

- IEEE 802.3 Ethernet Standard
- IEEE 802.1Q VLAN Standard
- RFC 791 (IPv4)
- RFC 8200 (IPv6)
- RFC 768 (UDP)
- RFC 793 (TCP)
- Microsoft RSS Specification

---

## 7. RSS (Receive Side Scaling)

Receive Side Scaling (RSS) enables multi-queue packet distribution by hashing packet headers to select receive queues. PMR supports three hash algorithms with configurable keys.

### 7.1 Hash Algorithm Selection (4 bytes)

**Datamodel**: `datamodel/protocols/ethernet/rss/hash_algorithm.ksy`

#### Wire Format

```
Byte:    0       1       2       3
     +-------+-------+-------+-------+
     |HF|Rsvd|       Hash Seed       |
     +-------+-------+-------+-------+

Byte 0 Detail:
  Bit: 7 6 5 4 3 2 1 0
      |  Reserved |HF |
      HF[1:0]: Hash Function Select
        0 = CRC32 (default)
        1 = XOR (testing only)
        2 = Toeplitz (production)
```

#### Field Definitions

| Field | Bits | Offset | Description |
|-------|------|--------|-------------|
| hash_func | 2 | 0[1:0] | Hash algorithm: 0=CRC32, 1=XOR, 2=Toeplitz |
| reserved | 6 | 0[7:2] | Reserved (must be zero) |
| hash_seed | 24 | 1-3 | Hash seed value (default: 0x5A5A5A) |

#### Algorithm Selection

| Value | Algorithm | Key Required | Use Case |
|-------|-----------|--------------|----------|
| 0 | CRC32 | No | Default at reset, good distribution |
| 1 | XOR | No | Testing/debugging only, poor distribution |
| 2 | Toeplitz | Yes (40 bytes) | Production, per Microsoft RSS spec |

#### CSR Reference

- Register: `rx_classify.pdp_hash_cfg` @ 0x3014

---

### 7.2 Hash Input Formats (8-36 bytes)

**Datamodel**: `datamodel/protocols/ethernet/rss/hash_input.ksy`

#### Wire Format

**IPv4 L3 Only (8 bytes)**:
```
Byte:    0       1       2       3       4       5       6       7
     +-------+-------+-------+-------+-------+-------+-------+-------+
     |         Source IPv4           |      Destination IPv4         |
     +-------+-------+-------+-------+-------+-------+-------+-------+
```

**IPv4 L3+L4 (12 bytes)**:
```
Byte:    0       1       2       3       4       5       6       7
     +-------+-------+-------+-------+-------+-------+-------+-------+
     |         Source IPv4           |      Destination IPv4         |
     +-------+-------+-------+-------+-------+-------+-------+-------+
         8       9      10      11
     +-------+-------+-------+-------+
     |  Src Port     |  Dst Port     |
     +-------+-------+-------+-------+
```

**IPv6 L3 Only (32 bytes)**:
```
Byte:    0-15                        16-31
     +-------------------------------+-------------------------------+
     |      Source IPv6 (16 bytes)   |   Destination IPv6 (16 bytes) |
     +-------------------------------+-------------------------------+
```

**IPv6 L3+L4 (36 bytes)**:
```
Byte:    0-15                        16-31                   32-35
     +-------------------------------+-------------------------------+-------+
     |      Source IPv6 (16 bytes)   |   Destination IPv6 (16 bytes) | Ports |
     +-------------------------------+-------------------------------+-------+
```

#### Field Definitions

| Hash Type | Size | Fields |
|-----------|------|--------|
| IPv4 L3 | 8 bytes | src_ip (4) + dst_ip (4) |
| IPv4 L4 | 12 bytes | src_ip (4) + dst_ip (4) + src_port (2) + dst_port (2) |
| IPv6 L3 | 32 bytes | src_ip (16) + dst_ip (16) |
| IPv6 L4 | 36 bytes | src_ip (16) + dst_ip (16) + src_port (2) + dst_port (2) |

#### Minimum Toeplitz Key Sizes

| Input Type | Input Size | Min Key Size |
|------------|------------|--------------|
| IPv4 L3 | 8 bytes | 12 bytes |
| IPv4 L4 | 12 bytes | 16 bytes |
| IPv6 L3 | 32 bytes | 36 bytes |
| IPv6 L4 | 36 bytes | 40 bytes |

---

### 7.3 Toeplitz Hash Key (40 bytes)

**Datamodel**: `datamodel/protocols/ethernet/rss/toeplitz_key.ksy`

#### Wire Format

```
Byte:    0       1       2       3       4       5       6       7
     +-------+-------+-------+-------+-------+-------+-------+-------+
     |                    Key Bytes 0-7 (CSR [0-1])                   |
     +-------+-------+-------+-------+-------+-------+-------+-------+
         8       9      10      11      12      13      14      15
     +-------+-------+-------+-------+-------+-------+-------+-------+
     |                    Key Bytes 8-15 (CSR [2-3])                  |
     +-------+-------+-------+-------+-------+-------+-------+-------+
        16      17      18      19      20      21      22      23
     +-------+-------+-------+-------+-------+-------+-------+-------+
     |                    Key Bytes 16-23 (CSR [4-5])                 |
     +-------+-------+-------+-------+-------+-------+-------+-------+
        24      25      26      27      28      29      30      31
     +-------+-------+-------+-------+-------+-------+-------+-------+
     |                    Key Bytes 24-31 (CSR [6-7])                 |
     +-------+-------+-------+-------+-------+-------+-------+-------+
        32      33      34      35      36      37      38      39
     +-------+-------+-------+-------+-------+-------+-------+-------+
     |                    Key Bytes 32-39 (CSR [8-9])                 |
     +-------+-------+-------+-------+-------+-------+-------+-------+
```

#### Field Definitions

| Field | Bits | Offset | Description |
|-------|------|--------|-------------|
| key | 320 | 0-39 | Toeplitz hash key (40 bytes) |

#### CSR Register Layout

| Register | Offset | Key Bytes |
|----------|--------|-----------|
| rss_hash_key[0] | 0x4010 | 0-3 |
| rss_hash_key[1] | 0x4014 | 4-7 |
| rss_hash_key[2] | 0x4018 | 8-11 |
| rss_hash_key[3] | 0x401C | 12-15 |
| rss_hash_key[4] | 0x4020 | 16-19 |
| rss_hash_key[5] | 0x4024 | 20-23 |
| rss_hash_key[6] | 0x4028 | 24-27 |
| rss_hash_key[7] | 0x402C | 28-31 |
| rss_hash_key[8] | 0x4030 | 32-35 |
| rss_hash_key[9] | 0x4034 | 36-39 |

#### Toeplitz Algorithm

```
hash = 0
for each bit i in input:
  if input_bit[i] == 1:
    hash ^= key[i : i+32]  // 32-bit window starting at bit i
return hash
```

Queue selection: `queue_id = hash_result % num_queues`
