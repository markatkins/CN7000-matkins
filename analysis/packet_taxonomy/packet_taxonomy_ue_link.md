# PMR Packet Taxonomy: UE+ Link Layer Formats

**Parent Document**: [packet_taxonomy.md](packet_taxonomy.md)  
**Scope**: Ultra Ethernet+ Link Layer Reliable (LLR) and Credit-Based Flow Control (CBFC)  
**Datamodel Directory**: `datamodel/protocols/ue/link/`  
**Last Updated**: 2026-01-23 (Phase 3 update)

---

## Table of Contents

1. [Overview](#1-overview)
2. [LLR Control Ordered Sets](#2-llr-control-ordered-sets)
   - [2.1 LLR_ACK CtlOS](#21-llr_ack-ctlos-8-bytes)
   - [2.2 LLR_NACK CtlOS](#22-llr_nack-ctlos-8-bytes)
   - [2.3 LLR_INIT CtlOS](#23-llr_init-ctlos-8-bytes)
   - [2.4 LLR_INIT_ECHO CtlOS](#24-llr_init_echo-ctlos-8-bytes)
3. [LLR Preamble Formats](#3-llr-preamble-formats)
   - [3.1 LLR Preamble MII](#31-llr-preamble-mii-8-bytes)
   - [3.2 LLR Preamble 64B/66B](#32-llr-preamble-64b66b-8-bytes)
4. [CBFC Formats](#4-cbfc-formats)
   - [4.1 CF_Update CtlOS](#41-cf_update-ctlos-8-bytes)
   - [4.2 CC_Update Message](#42-cc_update-message-8-bytes)
5. [LLDP TLV Formats](#5-lldp-tlv-formats)
   - [5.1 UE Link Negotiation TLV](#51-ue-link-negotiation-tlv)
   - [5.2 UE CBFC TLV](#52-ue-cbfc-tlv)
6. [Cross-References](#6-cross-references)
7. [References](#7-references)

---

## 1. Overview

### Link Layer Reliable (LLR)

LLR provides hop-by-hop reliability at the link layer using Control Ordered Sets (CtlOS) embedded in the 64B/66B encoding. LLR ensures reliable delivery between adjacent nodes without end-to-end retransmission.

| Feature | Description |
|---------|-------------|
| Sequence Numbers | 20-bit sequence space (0x00000 - 0xFFFFF) |
| ACK/NACK | Positive and negative acknowledgments |
| Initialization | LLR_INIT/LLR_INIT_ECHO handshake |
| Encoding | 64B/66B Control Ordered Sets |

### Credit-Based Flow Control (CBFC)

CBFC provides per-virtual-channel flow control using credit-based mechanisms. It prevents buffer overflow at receivers by controlling transmission based on available credits.

| Feature | Description |
|---------|-------------|
| Virtual Channels | Up to 32 VCs (5-bit index) |
| Credit Types | CF (Credit Freed), CC (Credit Consumed) |
| CF_Update | CtlOS format (frequent, low latency) |
| CC_Update | Ethernet packet format (less frequent) |

### Protocol Relationships

```
Link Layer Protocol Stack:
+------------------------------------------------------------------+
|                                                                  |
|  LLR (Link Layer Reliable)                                       |
|  ├── LLR_ACK CtlOS ────────→ Acknowledge received frames         |
|  ├── LLR_NACK CtlOS ───────→ Request retransmission              |
|  ├── LLR_INIT CtlOS ───────→ Initialize sequence state           |
|  └── LLR_INIT_ECHO CtlOS ──→ Confirm initialization              |
|                                                                  |
|  CBFC (Credit-Based Flow Control)                                |
|  ├── CF_Update CtlOS ──────→ Credit freed (frequent, CtlOS)      |
|  └── CC_Update Message ────→ Credit consumed (Ethernet packet)   |
|                                                                  |
|  LLDP Negotiation                                                |
|  ├── Link Negotiation TLV ─→ LLR/CBFC enable flags               |
|  └── CBFC TLV ─────────────→ VC configuration                    |
|                                                                  |
+------------------------------------------------------------------+
```

### 64B/66B Block Format

All LLR and CBFC CtlOS use 64B/66B encoding:

```
64B/66B Block Structure:
+--------+--------+--------+--------+--------+--------+--------+--------+--------+
| Sync   | D0     | D1     | D2     | D3     | D4     | D5     | D6     | D7     |
| Header | (Lane0)| (Lane1)| (Lane2)| (Lane3)| (Lane4)| (Lane5)| (Lane6)| (Lane7)|
+--------+--------+--------+--------+--------+--------+--------+--------+--------+
| 2 bits | 8 bits | 8 bits | 8 bits | 8 bits | 8 bits | 8 bits | 8 bits | 8 bits |
+--------+--------+--------+--------+--------+--------+--------+--------+--------+

Sync Header:
  2'b01 = Data block
  2'b10 = Control block (used for CtlOS)

Block Type Field (D0):
  0x4B = Control Ordered Set (LLR)
  0x5C = UE Control Ordered Set (CBFC)
```

---

## 2. LLR Control Ordered Sets

**Datamodel Directory**: `datamodel/protocols/ue/link/llr/`

### Format Summary

| Format | File | Type Code | Size | Description |
|--------|------|-----------|------|-------------|
| LLR_ACK | `llr_ack_ctlos.ksy` | 0x01 | 8 bytes | Frame acknowledgment |
| LLR_NACK | `llr_nack_ctlos.ksy` | 0x02 | 8 bytes | Negative acknowledgment |
| LLR_INIT | `llr_init_ctlos.ksy` | 0x03 | 8 bytes | Initialize sequence state |
| LLR_INIT_ECHO | `llr_init_echo_ctlos.ksy` | 0x04 | 8 bytes | Confirm initialization |

### LLR CtlOS Type Enumeration

| Value | Name | Description |
|-------|------|-------------|
| 0x01 | LLR_ACK | Frame acknowledgment |
| 0x02 | LLR_NACK | Negative acknowledgment |
| 0x03 | LLR_INIT | Initialize next_rx_seq state |
| 0x04 | LLR_INIT_ECHO | INIT received and processed |

---

### 2.1 LLR_ACK CtlOS (8 bytes)

**Datamodel**: `datamodel/protocols/ue/link/llr/llr_ack_ctlos.ksy`  
**Reference**: UE Spec v1.0.1, Tables 5-7 and 5-8, Section 5.1.4, Page 467

LLR_ACK acknowledges successful receipt of LLR frames.

#### Wire Format

```
64B/66B Block (Sync Header = 2'b10):
Byte:    0       1       2       3       4       5       6       7
     +-------+-------+-------+-------+-------+-------+-------+-------+
     | 0x4B  | 0x01  |ack_nack_seq   |seq_lo |  Rsvd |  Rsvd |  Rsvd |
     | (BTF) | (ACK) | [19:12]|[11:4]|+O-code|       |       |       |
     +-------+-------+-------+-------+-------+-------+-------+-------+
       D0      D1      D2      D3      D4      D5      D6      D7

D4 Detail:
  Bit:  7 6 5 4 3 2 1 0
       |ack_nack_seq| O-code |
       |   [3:0]    | (0x6)  |
```

#### Field Definitions

| Field | Bits | Offset | Description | Constraints |
|-------|------|--------|-------------|-------------|
| block_type | 8 | D0 | Block Type Field | MUST be 0x4B |
| ctlos_type | 8 | D1 | CtlOS message type | MUST be 0x01 |
| ack_nack_seq_high | 8 | D2 | Sequence bits [19:12] | Upper 8 bits |
| ack_nack_seq_mid | 8 | D3 | Sequence bits [11:4] | Middle 8 bits |
| ack_nack_seq_low | 4 | D4[7:4] | Sequence bits [3:0] | Lower 4 bits |
| ocode | 4 | D4[3:0] | Ordered set code | MUST be 0x6 |
| reserved | 24 | D5-D7 | Reserved | MUST be 0x00 |

#### Computed Fields

| Field | Formula | Description |
|-------|---------|-------------|
| ack_nack_seq | (D2 << 12) \| (D3 << 4) \| (D4 >> 4) | Complete 20-bit sequence number |

#### Protocol Behavior

**Transmission Timing**:
- Target spacing: 400-17296 bytes between CtlOS
- Minimum spacing in frame: 256 bytes from start
- Minimum spacing between CtlOS in same frame: 2048 bytes

**Usage**:
- Transmitted periodically to acknowledge received frames
- ack_nack_seq indicates most recently processed received frame
- Enables sender to free retransmit buffers

---

### 2.2 LLR_NACK CtlOS (8 bytes)

**Datamodel**: `datamodel/protocols/ue/link/llr/llr_nack_ctlos.ksy`  
**Reference**: UE Spec v1.0.1, Tables 5-7 and 5-8, Section 5.1.4, Page 467

LLR_NACK indicates frame loss or error, requesting retransmission.

#### Wire Format

```
64B/66B Block (Sync Header = 2'b10):
Byte:    0       1       2       3       4       5       6       7
     +-------+-------+-------+-------+-------+-------+-------+-------+
     | 0x4B  | 0x02  |ack_nack_seq   |seq_lo |  Rsvd |  Rsvd |  Rsvd |
     | (BTF) | (NACK)| [19:12]|[11:4]|+O-code|       |       |       |
     +-------+-------+-------+-------+-------+-------+-------+-------+
       D0      D1      D2      D3      D4      D5      D6      D7
```

#### Field Definitions

| Field | Bits | Offset | Description | Constraints |
|-------|------|--------|-------------|-------------|
| block_type | 8 | D0 | Block Type Field | MUST be 0x4B |
| ctlos_type | 8 | D1 | CtlOS message type | MUST be 0x02 |
| ack_nack_seq_high | 8 | D2 | Sequence bits [19:12] | Upper 8 bits |
| ack_nack_seq_mid | 8 | D3 | Sequence bits [11:4] | Middle 8 bits |
| ack_nack_seq_low | 4 | D4[7:4] | Sequence bits [3:0] | Lower 4 bits |
| ocode | 4 | D4[3:0] | Ordered set code | MUST be 0x6 |
| reserved | 24 | D5-D7 | Reserved | MUST be 0x00 |

#### Protocol Behavior

**NACK Triggers**:
- Sequence number gap detected
- CRC error on received frame
- Buffer overflow

**Retransmission**:
- Sender retransmits from ack_nack_seq forward
- Go-back-N or selective retransmit (implementation dependent)

---

### 2.3 LLR_INIT CtlOS (8 bytes)

**Datamodel**: `datamodel/protocols/ue/link/llr/llr_init_ctlos.ksy`  
**Reference**: UE Spec v1.0.1, Tables 5-7 and 5-8, Section 5.1.4, Page 467

LLR_INIT initializes the next_rx_seq state in the link partner.

#### Wire Format

```
64B/66B Block (Sync Header = 2'b10):
Byte:    0       1       2       3       4       5       6       7
     +-------+-------+-------+-------+-------+-------+-------+-------+
     | 0x4B  | 0x03  |  init_seq     |seq_lo |init_data      |  Rsvd |
     | (BTF) | (INIT)| [19:12]|[11:4]|+O-code| [7:0] |[15:8] |       |
     +-------+-------+-------+-------+-------+-------+-------+-------+
       D0      D1      D2      D3      D4      D5      D6      D7
```

#### Field Definitions

| Field | Bits | Offset | Description | Constraints |
|-------|------|--------|-------------|-------------|
| block_type | 8 | D0 | Block Type Field | MUST be 0x4B |
| ctlos_type | 8 | D1 | CtlOS message type | MUST be 0x03 |
| init_seq_high | 8 | D2 | Init sequence bits [19:12] | Upper 8 bits |
| init_seq_mid | 8 | D3 | Init sequence bits [11:4] | Middle 8 bits |
| init_seq_low | 4 | D4[7:4] | Init sequence bits [3:0] | Lower 4 bits |
| ocode | 4 | D4[3:0] | Ordered set code | MUST be 0x6 |
| init_data_low | 8 | D5 | Init data bits [7:0] | Lower byte |
| init_data_high | 8 | D6 | Init data bits [15:8] | Upper byte |
| reserved | 8 | D7 | Reserved | MUST be 0x00 |

#### Computed Fields

| Field | Formula | Description |
|-------|---------|-------------|
| init_seq | (D2 << 12) \| (D3 << 4) \| (D4 >> 4) | 20-bit init sequence |
| init_data | (D6 << 8) \| D5 | 16-bit init data |

#### Protocol Behavior

**Initialization Sequence**:
1. Station A sends LLR_INIT with init_seq
2. Station B receives, sets next_rx_seq = init_seq
3. Station B sends LLR_INIT_ECHO echoing init_seq and init_data
4. Station A receives echo, confirms initialization

**Usage**:
- Link initialization
- Link recovery after error
- Sequence number resynchronization

---

### 2.4 LLR_INIT_ECHO CtlOS (8 bytes)

**Datamodel**: `datamodel/protocols/ue/link/llr/llr_init_echo_ctlos.ksy`  
**Reference**: UE Spec v1.0.1, Tables 5-7 and 5-8, Section 5.1.4, Page 467

LLR_INIT_ECHO confirms receipt of LLR_INIT and readiness to receive frames.

#### Wire Format

```
64B/66B Block (Sync Header = 2'b10):
Byte:    0       1       2       3       4       5       6       7
     +-------+-------+-------+-------+-------+-------+-------+-------+
     | 0x4B  | 0x04  |  init_seq     |seq_lo |init_data      |  Rsvd |
     | (BTF) | (ECHO)| [19:12]|[11:4]|+O-code| [7:0] |[15:8] |       |
     +-------+-------+-------+-------+-------+-------+-------+-------+
       D0      D1      D2      D3      D4      D5      D6      D7
```

#### Field Definitions

Same as LLR_INIT except:

| Field | Bits | Offset | Description | Constraints |
|-------|------|--------|-------------|-------------|
| ctlos_type | 8 | D1 | CtlOS message type | MUST be 0x04 |

#### Protocol Behavior

**Echo Semantics**:
- init_seq and init_data are echoed from received LLR_INIT
- Confirms sequence state has been set
- Indicates station is ready to receive LLR frames

---

## 3. LLR Preamble Formats

**Datamodel Directory**: `datamodel/protocols/ue/link/llr/`

### 3.1 LLR Preamble MII (8 bytes)

**Datamodel**: `datamodel/protocols/ue/link/llr/llr_preamble_mii.ksy`  
**Reference**: UE Spec v1.0.1, Table 5-1, Section 5.1.2, Page 464

LLR preamble for MII (Media Independent Interface).

#### Wire Format

```
Byte:    0       1       2       3       4       5       6       7
     +-------+-------+-------+-------+-------+-------+-------+-------+
     |     Preamble (24 bits)        |  SFD  |  Sequence Number      |
     |        0x555555               |       |       (24 bits)       |
     +-------+-------+-------+-------+-------+-------+-------+-------+
                                                     | Control Flags |
     +-------+-------+-------+-------+-------+-------+-------+-------+
```

#### Field Definitions

| Field | Bits | Offset | Description | Constraints |
|-------|------|--------|-------------|-------------|
| preamble | 24 | 0-2 | Preamble pattern | Typically 0x555555 |
| sfd | 8 | 3 | Start Frame Delimiter | 0xD5 (std) or 0xDD (LLR) |
| sequence_number | 24 | 4-6 | tx_seq or rx_seq | Frame sequence |
| control_flags | 8 | 7 | LLR control flags | Implementation specific |

#### SFD Values

| Value | Name | Description |
|-------|------|-------------|
| 0xD5 | standard_sfd | Standard Ethernet SFD |
| 0xDD | llr_sfd | LLR frame SFD |

---

### 3.2 LLR Preamble 64B/66B (8 bytes)

**Datamodel**: `datamodel/protocols/ue/link/llr/llr_preamble_64b66b.ksy`  
**Reference**: UE Spec v1.0.1, Table 5-2, Section 5.1.2, Page 465

LLR preamble for 64B/66B PCS encoding.

#### Wire Format

```
64B/66B Block (Sync Header = 2'b01):
Byte:    0       1       2       3       4       5       6       7
     +-------+-------+-------+-------+-------+-------+-------+-------+
     |  Sequence Number (24 bits)    | Ctrl  |      Reserved         |
     |                               | Flags |      (32 bits)        |
     +-------+-------+-------+-------+-------+-------+-------+-------+
```

#### Field Definitions

| Field | Bits | Offset | Description | Constraints |
|-------|------|--------|-------------|-------------|
| sequence_number | 24 | 0-2 | LLR frame sequence | 24-bit sequence |
| control_flags | 8 | 3 | LLR control flags | Implementation specific |
| reserved | 32 | 4-7 | Reserved | MUST be 0 |

---

## 4. CBFC Formats

**Datamodel Directory**: `datamodel/protocols/ue/link/cbfc/`

### Format Summary

| Format | File | Size | Description |
|--------|------|------|-------------|
| CF_Update | `cf_update.ksy` | 8 bytes | Credit freed (CtlOS) |
| CC_Update | `cc_update.ksy` | 8 bytes | Credit consumed (Ethernet) |

---

### 4.1 CF_Update CtlOS (8 bytes)

**Datamodel**: `datamodel/protocols/ue/link/cbfc/cf_update.ksy`  
**Reference**: UE Spec v1.0.1, Tables 5-20 and 5-21, Section 5.2.6.1, Page 492

CF_Update communicates credit freed information for two virtual channels.

#### Wire Format

```
64B/66B Block (Sync Header = 2'b10):
Byte:    0       1       2       3       4       5       6       7
     +-------+-------+-------+-------+-------+-------+-------+-------+
     | 0x5C  | 0x10  |CF1_VC |CF1_cnt|CF1_cnt|CF2_VC |CF2_cnt|CF2_cnt|
     | (Ctrl)| (Type)|+cnt_hi| [10:3]|lo+Ocd |+cnt_hi| [10:3]|lo+Rsvd|
     +-------+-------+-------+-------+-------+-------+-------+-------+
       D0      D1      D2      D3      D4      D5      D6      D7

D2 Detail:
  Bit:  7 6 5 4 3 2 1 0
       |CF1_VC_idx |CF1_cnt|
       |   [4:0]   |[14:12]|

D4 Detail:
  Bit:  7 6 5 4 3 2 1 0
       |CF1_cnt| O-code |
       | [2:0] | (0x6)  |

D5 Detail:
  Bit:  7 6 5 4 3 2 1 0
       |CF2_VC_idx |CF2_cnt|
       |   [4:0]   |[14:12]|

D7 Detail:
  Bit:  7 6 5 4 3 2 1 0
       |CF2_cnt| Rsvd  |
       | [2:0] | (0x0) |
```

#### Field Definitions

| Field | Bits | Offset | Description | Constraints |
|-------|------|--------|-------------|-------------|
| control_char | 8 | D0 | UE control character | MUST be 0x5C |
| message_type | 8 | D1 | CF_Update type | MUST be 0x10 |
| cf1_vc_index | 5 | D2[7:3] | First VC index | 0-31 |
| cf1_count | 15 | D2[2:0], D3, D4[7:5] | First VC credit count | 0-32767 |
| ocode | 4 | D4[3:0] | Ordered set code | MUST be 0x6 |
| cf2_vc_index | 5 | D5[7:3] | Second VC index | 0-31 |
| cf2_count | 15 | D5[2:0], D6, D7[7:5] | Second VC credit count | 0-32767 |
| reserved | 4 | D7[3:0] | Reserved | Set to 0 |

#### Computed Fields

| Field | Formula | Description |
|-------|---------|-------------|
| cf1_vc_index | (D2 >> 3) & 0x1F | First VC index |
| cf1_count | ((D2 & 0x07) << 12) \| (D3 << 4) \| ((D4 >> 4) & 0x0E) | First VC credits |
| cf2_vc_index | (D5 >> 3) & 0x1F | Second VC index |
| cf2_count | ((D5 & 0x07) << 12) \| (D6 << 4) \| ((D7 >> 4) & 0x0E) | Second VC credits |

#### Protocol Behavior

**Credit Freed Updates**:
- Sent frequently via CtlOS (low latency)
- Each message updates credits for two VCs
- Credit counts represent R_VC_CF counter values
- Receiver uses credits to control sender transmission

---

### 4.2 CC_Update Message (8 bytes)

**Datamodel**: `datamodel/protocols/ue/link/cbfc/cc_update.ksy`  
**Reference**: UE Spec v1.0.1, Table 5-22, Section 5.2.6.2, Page 493

CC_Update communicates credit consumed information via Ethernet packet format.

#### Wire Format

```
Ethernet Packet Payload:
Byte:    0       1       2       3       4       5       6       7
     +-------+-------+-------+-------+-------+-------+-------+-------+
     | Type  |VC_idx |CC_cnt |CC_cnt |      Reserved (32 bits)       |
     |       |+CC_hi | [10:3]|  lo   |                               |
     +-------+-------+-------+-------+-------+-------+-------+-------+

Byte 1 Detail:
  Bit:  7 6 5 4 3 2 1 0
       | VC_index  |CC_cnt|
       |   [4:0]   |[14:12]|
```

#### Field Definitions

| Field | Bits | Offset | Description | Constraints |
|-------|------|--------|-------------|-------------|
| message_type | 8 | 0 | CC_Update type | Message identifier |
| vc_index | 5 | 1[7:3] | VC index | 0-31 |
| cc_counter | 15 | 1[2:0], 2, 3[7:4] | Credit consumed count | 0-32767 |
| reserved | 32 | 4-7 | Reserved | MUST be 0 |

#### Computed Fields

| Field | Formula | Description |
|-------|---------|-------------|
| vc_index | (byte1 >> 3) & 0x1F | VC index |
| cc_counter | ((byte1 & 0x07) << 12) \| (byte2 << 4) \| ((byte3 >> 4) & 0x0F) | Credit consumed |

#### Protocol Behavior

**Credit Consumed Updates**:
- Sent less frequently than CF_Update
- Uses Ethernet packet format (not CtlOS)
- Source to destination credit information
- Complements CF_Update for bidirectional credit tracking

---

## 5. LLDP TLV Formats

**Datamodel Directory**: `datamodel/protocols/ue/link/lldp/`

### 5.1 UE Link Negotiation TLV

**Datamodel**: `datamodel/protocols/ue/link/lldp/ue_link_negotiation_tlv.ksy`  
**Reference**: UE Spec v1.0.1, Section 5.3.2.1, Page 509

Negotiates UE-specific link parameters via LLDP.

#### Wire Format

```
LLDP TLV Format:
Byte:    0       1       2       3       4       5       6
     +-------+-------+-------+-------+-------+-------+-------+
     |Type|  Length |      OUI (24 bits)      |Subtype| Flags|
     | 7b |   9b    |                         |       |      |
     +-------+-------+-------+-------+-------+-------+-------+
         7
     +-------+
     |UE Ver |
     +-------+

Flags (Byte 5) Detail:
  Bit:  7 6 5 4 3 2 1 0
       |L|C|  Reserved  |
       |L|B|   (6b)     |
       |R|F|            |
       | |C|            |
```

#### Field Definitions

| Field | Bits | Offset | Description | Constraints |
|-------|------|--------|-------------|-------------|
| tlv_type | 7 | 0[7:1] | TLV type | MUST be 127 (Org Specific) |
| tlv_length | 9 | 0[0], 1 | TLV length | >= 4 |
| oui | 24 | 2-4 | UE Consortium OUI | Organization identifier |
| subtype | 8 | 5 | UE subtype | MUST be 1 (Link Negotiation) |
| llr_enabled | 1 | 6[7] | LLR enable flag | 0=disabled, 1=enabled |
| cbfc_enabled | 1 | 6[6] | CBFC enable flag | 0=disabled, 1=enabled |
| reserved | 6 | 6[5:0] | Reserved | MUST be 0 |
| ue_version | 8 | 7 | UE spec version | Version number |

---

### 5.2 UE CBFC TLV

**Datamodel**: `datamodel/protocols/ue/link/lldp/ue_cbfc_tlv.ksy`  
**Reference**: UE Spec v1.0.1, Section 5.3.2.2, Page 510

Advertises CBFC capabilities and configuration via LLDP.

#### Wire Format

```
LLDP TLV Format:
Byte:    0       1       2       3       4       5       6
     +-------+-------+-------+-------+-------+-------+-------+
     |Type|  Length |      OUI (24 bits)      |Subtype|Num VC|
     | 7b |   9b    |                         |       |      |
     +-------+-------+-------+-------+-------+-------+-------+
         7       8       9      10      11      12      13
     +-------+-------+-------+-------+-------+-------+-------+
     |Credit Pool Sz |    Lossless VCs (32 bits)     | Rsvd  |
     |    (16 bits)  |                               |(16b)  |
     +-------+-------+-------+-------+-------+-------+-------+
```

#### Field Definitions

| Field | Bits | Offset | Description | Constraints |
|-------|------|--------|-------------|-------------|
| tlv_type | 7 | 0[7:1] | TLV type | MUST be 127 (Org Specific) |
| tlv_length | 9 | 0[0], 1 | TLV length | >= 4 |
| oui | 24 | 2-4 | UE Consortium OUI | Organization identifier |
| subtype | 8 | 5 | UE subtype | MUST be 2 (CBFC) |
| num_vcs | 8 | 6 | Number of VCs | 1-32 |
| credit_pool_size | 16 | 7-8 | Total credit pool | > 0 |
| lossless_vcs | 32 | 9-12 | Lossless VC bitmap | Bit N = VC N lossless |
| reserved | 16 | 13-14 | Reserved | MUST be 0 |

---

## 6. UE Network Layer Formats

**Datamodel Directory**: `datamodel/protocols/ue/network/`

### 6.1 DSCP Categories

**Datamodel**: `datamodel/protocols/ue/network/dscp_categories.ksy`  
**Reference**: UE Spec v1.0.1, Tables 3-69, 3-70, Section 3.6.4.7, Page 351

DSCP (Differentiated Services Code Point) category mappings for UET traffic management.

#### DSCP Categories

| Category | Traffic Class | Priority | Description |
|----------|---------------|----------|-------------|
| DSCP_TRIMMABLE | TC_low | Low | Data packets eligible for trimming |
| DSCP_TRIMMED | TC_med | Medium | Packets that have been trimmed |
| DSCP_CONTROL | TC_high | High | Control packets (not trimmable) |

#### Requirements

- At least 2 DSCPs required (TRIMMABLE, CONTROL)
- 3 DSCPs recommended for trimming (TRIMMABLE, TRIMMED, CONTROL)
- Network operator configures specific DSCP values
- Multiple TRIMMABLE can map to same TRIMMED

---

### 6.2 Packet Trimming

**Datamodel**: `datamodel/protocols/ue/network/packet_trimming.ksy`  
**Reference**: UE Spec v1.0.1, Section 4.1, Table 4-1, Page 456

Network switch packet trimming mechanism for congestion management.

#### MIN_TRIM_SIZE Requirements (Table 4-1)

| Protocol | Components | Min Size |
|----------|------------|----------|
| UET/IP | Entropy (4B) + PDS (16B) | 20 bytes |
| UET/UDP/IP | UDP (8B) + PDS (16B) | 24 bytes |
| UET/IP over VXLAN | Full tunnel stack | 70 bytes |
| UET/UDP/IPv4 over VXLAN | Full tunnel stack | 74 bytes |
| UET/UDP/IPv6 over VXLAN | Full tunnel stack | 94 bytes |

#### Trimming Process

1. Packet with DSCP_TRIMMABLE fails buffer admission
2. Switch trims IP payload to >= MIN_TRIM_SIZE
3. Switch updates DSCP to DSCP_TRIMMED
4. Switch updates IP total length and checksums
5. Trimmed packet enqueued to DSCP_TRIMMED queue

#### Benefits

- Single RTT loss detection (vs timeout-based)
- Fast retransmission trigger
- Reduces buffer pressure (4KB packet → 20-94B header)

---

## 7. UE Physical Layer Formats

**Datamodel Directory**: `datamodel/protocols/ue/physical/`

### 7.1 Control Ordered Sets (CtlOS)

**Datamodel**: `datamodel/protocols/ue/physical/control_ordered_sets.ksy`  
**Reference**: UE Spec v1.0.1, Tables 5-28, 5-29, 5-30, Section 5.2.11, Page 510

Physical layer Control Ordered Set encoding for CBFC and LLR.

#### xMII Format (Table 5-28)

```
Lane:    0       1       2       3       4       5       6       7
     +-------+-------+-------+-------+-------+-------+-------+-------+
     | 0x5C  | Type  |  D2   |  D3   |D4+Ocd |  D5   |  D6   |  D7   |
     | (Ctrl)| (Msg) | (Data)| (Data)|{4b,6} | (Data)| (Data)| (Data)|
     +-------+-------+-------+-------+-------+-------+-------+-------+
```

#### 64B/66B Encoding (Table 5-30)

| Field | Value | Description |
|-------|-------|-------------|
| Sync Header | 2'b10 | Control block |
| Block Type | 0x4B | CtlOS block type |
| O-code | 0x6 | UE ordered set code |

#### Defined CtlOS Types (Table 5-29)

| Type | Name | Description |
|------|------|-------------|
| 0x01 | LLR_ACK | Frame acknowledgement |
| 0x02 | LLR_NACK | Frame negative acknowledgement |
| 0x03 | LLR_INIT | Initialize next_rx_seq state |
| 0x04 | LLR_INIT_ECHO | INIT received and processed |
| 0x10 | CF_Update | Credit freed update |

---

## 8. Cross-References

### Related Documents

| Document | Content |
|----------|---------|
| [packet_taxonomy.md](packet_taxonomy.md) | Master index |
| [packet_taxonomy_ue_pds.md](packet_taxonomy_ue_pds.md) | PDS formats |
| [packet_taxonomy_ue_ses.md](packet_taxonomy_ue_ses.md) | SES formats |
| [packet_taxonomy_ue_cms_tss.md](packet_taxonomy_ue_cms_tss.md) | CMS/TSS formats |

### Datamodel Files

| File | Description |
|------|-------------|
| `llr/llr_ack_ctlos.ksy` | LLR_ACK Control Ordered Set |
| `llr/llr_nack_ctlos.ksy` | LLR_NACK Control Ordered Set |
| `llr/llr_init_ctlos.ksy` | LLR_INIT Control Ordered Set |
| `llr/llr_init_echo_ctlos.ksy` | LLR_INIT_ECHO Control Ordered Set |
| `llr/llr_preamble_mii.ksy` | LLR Preamble MII format |
| `llr/llr_preamble_64b66b.ksy` | LLR Preamble 64B/66B format |
| `cbfc/cf_update.ksy` | CF_Update CtlOS |
| `cbfc/cc_update.ksy` | CC_Update Ethernet message |
| `lldp/ue_link_negotiation_tlv.ksy` | Link Negotiation TLV |
| `lldp/ue_cbfc_tlv.ksy` | CBFC Configuration TLV |
| `network/dscp_categories.ksy` | DSCP category mappings |
| `network/packet_trimming.ksy` | Packet trimming mechanism |
| `physical/control_ordered_sets.ksy` | Physical layer CtlOS encoding |

### Protocol State Machines

| File | Description |
|------|-------------|
| `llr/protocols/llr_transmit_sm.ksy` | LLR transmit state machine |
| `llr/protocols/llr_receive.ksy` | LLR receive state machine |
| `llr/protocols/ack_nack_transmit_sm.ksy` | ACK/NACK transmit state machine |
| `cbfc/protocols/vc_state_machine.ksy` | VC state machine |
| `cbfc/protocols/lossless_vc_init.ksy` | Lossless VC initialization |
| `cbfc/protocols/lossless_vc_removal.ksy` | Lossless VC removal |

---

## 9. References

- UE Specification v1.0.1, Chapter 5 (Link Layer)
- UE Specification v1.0.1, Section 5.1 (LLR)
- UE Specification v1.0.1, Section 5.2 (CBFC)
- UE Specification v1.0.1, Section 5.3 (LLDP)
- UE Specification v1.0.1, Tables 5-1 through 5-25
- IEEE 802.3-2022, Clause 82.2.3 (64B/66B Block Format)
