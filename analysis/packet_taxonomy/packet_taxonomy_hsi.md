# PMR Packet Taxonomy: Host-Software Interface (HSI) Formats

**Parent Document**: [packet_taxonomy.md](packet_taxonomy.md)  
**Scope**: PMR NIC Host-Software Interface formats (Command Queue, Notifications, SGL)  
**Datamodel Directory**: `datamodel/hw/asics/pmr/interfaces/host_interface/`  
**Last Updated**: 2026-01-23

---

## Table of Contents

1. [Overview](#1-overview)
2. [Command Queue Formats](#2-command-queue-formats)
   - [2.1 Command Queue Segment](#21-command-queue-segment-64-bytes)
3. [Notification Queue Formats](#3-notification-queue-formats)
   - [3.1 Receive Notification](#31-receive-notification-64-bytes)
   - [3.2 Send Completion](#32-send-completion-64-bytes)
   - [3.3 Event Notification](#33-event-notification-64-bytes)
4. [Scatter-Gather Formats](#4-scatter-gather-formats)
   - [4.1 SGL Entry](#41-sgl-entry-32-bytes)
5. [Data Flow](#5-data-flow)
6. [Cross-References](#6-cross-references)
7. [References](#7-references)

---

## 1. Overview

The Host-Software Interface (HSI) defines the data structures used for communication between host software (libfabric provider) and the PMR NIC hardware. All HSI structures are 64-byte aligned for efficient PCIe transfers.

### HSI Components

| Component | Direction | Description |
|-----------|-----------|-------------|
| Command Queue | Host → NIC | Work requests (send, recv, RDMA) |
| Notification Queue | NIC → Host | Completions and events |
| Doorbell | Host → NIC | Queue advancement signals |

### Data Flow

```
HSI Data Flow:
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  Host → NIC:  Command Queue Segment + SGL Entry(s)              │
│               Doorbell (notify NIC of new work)                 │
│                                                                 │
│  NIC → Host:  Receive Notification (incoming message)           │
│               Send Completion (outgoing complete)               │
│               Event Notification (error/async)                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Format Summary

| Format | Size | Type | Description |
|--------|------|------|-------------|
| Command Queue Segment | 64 bytes | Command | Work request descriptor |
| Receive Notification | 64 bytes | Notification | Received message info |
| Send Completion | 64 bytes | Notification | Send operation complete |
| Event Notification | 64 bytes | Notification | Async error/event |
| SGL Entry | 32 bytes | Data | Scatter-gather list entry |

---

## 2. Command Queue Formats

### 2.1 Command Queue Segment (64 bytes)

**Datamodel**: `command_queue_segment.ksy`  
**Related Formats**: [SGL Entry (4.1)](#41-sgl-entry-32-bytes)

Command Queue Segments describe work requests submitted by the host.

#### Wire Format

```
Byte:    0       1       2       3       4       5       6       7
     +-------+-------+-------+-------+-------+-------+-------+-------+
     | opcode| flags |   payload_len |          reserved             |
     +-------+-------+-------+-------+-------+-------+-------+-------+
         8       9      10      11      12      13      14      15
     +-------+-------+-------+-------+-------+-------+-------+-------+
     |                         tag [63:0]                            |
     +-------+-------+-------+-------+-------+-------+-------+-------+
        16      17      18      19      20      21      22      23
     +-------+-------+-------+-------+-------+-------+-------+-------+
     |                        dest [63:0]                            |
     +-------+-------+-------+-------+-------+-------+-------+-------+
        24      25      26      27      28      29      30      31
     +-------+-------+-------+-------+-------+-------+-------+-------+
     |                      metadata [63:0]                          |
     +-------+-------+-------+-------+-------+-------+-------+-------+
        32-63: Inline Data or SGL Entry (32 bytes)
     +-------+-------+-------+-------+-------+-------+-------+-------+
```

#### Field Definitions

| Field | Bits | Offset | Description | Constraints |
|-------|------|--------|-------------|-------------|
| opcode | 8 | 0 | Operation code | See encoding below |
| flags | 8 | 1 | Operation flags | See flags below |
| payload_len | 16 | 2-3 | Payload length | Bytes to transfer |
| reserved | 32 | 4-7 | Reserved | Must be 0 |
| tag | 64 | 8-15 | Tag value | For tagged operations |
| dest | 64 | 16-23 | Destination | Endpoint or address |
| metadata | 64 | 24-31 | Metadata | Operation context |
| data | 256 | 32-63 | Inline/SGL | Data or SGL entry |

#### Opcode Encoding

```
Opcode byte:
  Bits [7:4]: Family
    0x1 = MSG (message operations)
    0x2 = TAGGED (tagged message operations)
    0x3 = RMA (remote memory access)
    0x4 = ATOMIC (atomic operations)
  
  Bits [3:2]: Variant
    0x0 = SEND
    0x1 = RECV
    0x2 = INJECT
  
  Bit [1]: Reserved (must be 0)
  
  Bit [0]: Data Source
    0 = INLINE (data in segment)
    1 = SGL (scatter-gather list)
```

#### Flags

| Bit | Name | Description |
|-----|------|-------------|
| 7 | FENCE | Wait for prior operations |
| 6 | COMPLETION | Generate completion |
| 5 | INJECT | Inline inject (no completion) |
| 4 | REMOTE_CQ | Remote completion queue |
| 3-0 | Reserved | Must be 0 |

#### Protocol Behavior

**Command Submission**:
1. Host writes Command Queue Segment to command queue
2. Host writes Doorbell to notify NIC
3. NIC processes command and generates completion

**Data Modes**:
- **Inline**: Data in bytes 32-63 (up to 32 bytes)
- **SGL**: SGL Entry in bytes 32-63 points to data

---

## 3. Notification Queue Formats

All notification formats are 64 bytes with a prime marker in byte 63 for validity detection.

### 3.1 Receive Notification (64 bytes)

**Datamodel**: `receive_notification.ksy`  
**Related Formats**: [Send Completion (3.2)](#32-send-completion-64-bytes)

Generated when a message is received.

#### Wire Format

```
Byte:    0       1       2       3       4       5       6       7
     +-------+-------+-------+-------+-------+-------+-------+-------+
     | type  | flags |    status     |          src_id               |
     +-------+-------+-------+-------+-------+-------+-------+-------+
         8       9      10      11      12      13      14      15
     +-------+-------+-------+-------+-------+-------+-------+-------+
     |                         tag [63:0]                            |
     +-------+-------+-------+-------+-------+-------+-------+-------+
        16      17      18      19      20      21      22      23
     +-------+-------+-------+-------+-------+-------+-------+-------+
     |      total_length     |buf_id_0|buf_id_1|buf_off|  reserved   |
     +-------+-------+-------+-------+-------+-------+-------+-------+
        24-62: Inline Data (up to 35 bytes)
     +-------+-------+-------+-------+-------+-------+-------+-------+
        63: marker
     +-------+-------+-------+-------+-------+-------+-------+-------+
```

#### Field Definitions

| Field | Bits | Offset | Description | Constraints |
|-------|------|--------|-------------|-------------|
| type | 8 | 0 | Notification type | 0x00 for receive |
| flags | 8 | 1 | Flags | FI_INLINE, continuation |
| status | 16 | 2-3 | Completion status | 0 = success |
| src_id | 32 | 4-7 | Source endpoint ID | Sender identifier |
| tag | 64 | 8-15 | Tag value | For tagged receives |
| total_length | 32 | 16-19 | Payload length | Bytes received |
| buffer_id_0 | 16 | 20-21 | First buffer ID | Receive buffer |
| buffer_id_1 | 16 | 22-23 | Second buffer ID | Continuation |
| buffer_offset | 16 | 24-25 | Offset in buffer | Start position |
| reserved | 16 | 26-27 | Reserved | Must be 0 |
| inline_data | 280 | 28-62 | Inline payload | Up to 35 bytes |
| marker | 8 | 63 | Prime marker | 1-13 for validity |

#### Protocol Behavior

**Receive Processing**:
1. NIC receives message
2. NIC writes Receive Notification to notification queue
3. Host polls notification queue for completions
4. Host processes received data from buffer or inline

---

### 3.2 Send Completion (64 bytes)

**Datamodel**: `send_completion.ksy`  
**Related Formats**: [Receive Notification (3.1)](#31-receive-notification-64-bytes)

Generated when a send operation completes.

#### Wire Format

```
Byte:    0       1       2       3       4       5       6       7
     +-------+-------+-------+-------+-------+-------+-------+-------+
     | type  | flags |    status     |          reserved_0           |
     +-------+-------+-------+-------+-------+-------+-------+-------+
         8       9      10      11      12      13      14      15
     +-------+-------+-------+-------+-------+-------+-------+-------+
     |                      op_context [63:0]                        |
     +-------+-------+-------+-------+-------+-------+-------+-------+
        16      17      18      19      20-62: reserved
     +-------+-------+-------+-------+-------+-------+-------+-------+
     |      bytes_sent       |              reserved_1               |
     +-------+-------+-------+-------+-------+-------+-------+-------+
        63: marker
     +-------+-------+-------+-------+-------+-------+-------+-------+
```

#### Field Definitions

| Field | Bits | Offset | Description | Constraints |
|-------|------|--------|-------------|-------------|
| type | 8 | 0 | Notification type | 0x01 for send |
| flags | 8 | 1 | Completion flags | Operation-specific |
| status | 16 | 2-3 | Completion status | 0 = success |
| reserved_0 | 32 | 4-7 | Reserved | Must be 0 |
| op_context | 64 | 8-15 | Operation context | From command |
| bytes_sent | 32 | 16-19 | Bytes transferred | Actual count |
| reserved_1 | 344 | 20-62 | Reserved | Must be 0 |
| marker | 8 | 63 | Prime marker | 1-13 for validity |

---

### 3.3 Event Notification (64 bytes)

**Datamodel**: `event_notification.ksy`  
**Related Formats**: [Receive Notification (3.1)](#31-receive-notification-64-bytes)

Generated for asynchronous events and errors.

#### Wire Format

```
Byte:    0       1       2       3       4       5       6       7
     +-------+-------+-------+-------+-------+-------+-------+-------+
     | type  |evt_typ|    status     |  endpoint_id  |  reserved_0   |
     +-------+-------+-------+-------+-------+-------+-------+-------+
         8       9      10      11      12      13      14      15
     +-------+-------+-------+-------+-------+-------+-------+-------+
     |                      event_data [63:0]                        |
     +-------+-------+-------+-------+-------+-------+-------+-------+
        16      17      18      19      20      21      22      23
     +-------+-------+-------+-------+-------+-------+-------+-------+
     |                      timestamp [63:0]                         |
     +-------+-------+-------+-------+-------+-------+-------+-------+
        24-62: reserved_1
     +-------+-------+-------+-------+-------+-------+-------+-------+
        63: marker
     +-------+-------+-------+-------+-------+-------+-------+-------+
```

#### Field Definitions

| Field | Bits | Offset | Description | Constraints |
|-------|------|--------|-------------|-------------|
| type | 8 | 0 | Notification type | 0x02 for event |
| event_type | 8 | 1 | Event category | See enum below |
| status | 16 | 2-3 | Status/severity | Bits [1:0] = severity |
| endpoint_id | 16 | 4-5 | Affected endpoint | Source of event |
| reserved_0 | 16 | 6-7 | Reserved | Must be 0 |
| event_data | 64 | 8-15 | Event-specific data | Per event_type |
| timestamp | 64 | 16-23 | Event timestamp | CPU cycles |
| reserved_1 | 312 | 24-62 | Reserved | Must be 0 |
| marker | 8 | 63 | Prime marker | 1-13 for validity |

#### Event Types

| Code | Name | event_data Meaning |
|------|------|-------------------|
| 0x01 | RXPOOL_EXHAUSTED | Dropped packet count |
| 0x02 | HELD_BUFFER_THRESHOLD | Current held count |
| 0x03 | CREDIT_STARVATION | Starvation duration (cycles) |
| 0x04 | INVALID_DESCRIPTOR | Descriptor offset |
| 0x05 | PROTECTION_VIOLATION | Faulting address |
| 0x06 | PCIE_ERROR | PCIe error code |

#### Severity Levels

| Value | Level | Description |
|-------|-------|-------------|
| 0x00 | Info | Informational |
| 0x01 | Warning | Warning condition |
| 0x02 | Error | Error condition |
| 0x03 | Fatal | Fatal error |

#### Protocol Behavior

**Event Handling**:
1. NIC detects anomalous condition
2. NIC writes Event Notification to notification queue
3. Host processes event (log, counter, notify application)

---

## 4. Scatter-Gather Formats

### 4.1 SGL Entry (32 bytes)

**Datamodel**: `sgl_entry.ksy`  
**Related Formats**: [Command Queue Segment (2.1)](#21-command-queue-segment-64-bytes)

Scatter-gather list entry for indirect data or inline data.

#### Wire Format

```
Byte:    0       1       2       3       4       5       6       7
     +-------+-------+-------+-------+-------+-------+-------+-------+
     |                   physical_address [63:0]                     |
     |                   (or inline_data QW0)                        |
     +-------+-------+-------+-------+-------+-------+-------+-------+
         8       9      10      11      12      13      14      15
     +-------+-------+-------+-------+-------+-------+-------+-------+
     |                     memory_key [63:0]                         |
     |                   (or inline_data QW1)                        |
     +-------+-------+-------+-------+-------+-------+-------+-------+
        16      17      18      19      20      21      22      23
     +-------+-------+-------+-------+-------+-------+-------+-------+
     |                      reserved [63:0]                          |
     |                   (or inline_data QW2)                        |
     +-------+-------+-------+-------+-------+-------+-------+-------+
        24      25      26      27      28      29      30      31
     +-------+-------+-------+-------+-------+-------+-------+-------+
     |                    length_flags [63:0]                        |
     |        length[31:0]        |I|        reserved[30:0]          |
     +-------+-------+-------+-------+-------+-------+-------+-------+
```

#### Field Definitions

| Field | Bits | Offset | Description | Constraints |
|-------|------|--------|-------------|-------------|
| physical_address | 64 | 0-7 | DMA address / inline QW0 | 64-byte aligned (indirect) |
| memory_key | 64 | 8-15 | Memory region key / inline QW1 | Valid MR key (indirect) |
| reserved | 64 | 16-23 | Reserved / inline QW2 | 0 for indirect |
| length | 32 | 24-27 | Data length | Bytes (indirect only) |
| inline_flag | 1 | 28[0] | Inline indicator | Bit 32 of length_flags |
| reserved_flags | 31 | 28-31 | Reserved | Must be 0 |

#### Interpretation

**Indirect Mode (bit 32 = 0)**:
- `physical_address`: DMA source address (64-byte aligned)
- `memory_key`: 64-bit protection domain key
- `length`: Bytes to transfer

**Inline Mode (bit 32 = 1)**:
- Bytes 0-23 contain up to 24 bytes of inline data
- `length` field indicates actual inline data size

#### Protocol Behavior

**Memory Key**:
- 64-bit key (larger than libibverbs 32-bit lkey)
- Provider maintains lkey → memory_key mapping
- Hardware validates key against registered memory regions

---

## 5. Data Flow

### Command Submission Flow

```
1. Host prepares Command Queue Segment
   - Set opcode, flags, payload_len
   - Set tag, dest, metadata
   - Add inline data or SGL entry

2. Host writes segment to command queue
   - Write to next available slot
   - Maintain producer index

3. Host writes Doorbell
   - Notify NIC of new work
   - Include updated producer index

4. NIC processes command
   - Read segment from command queue
   - Execute operation (send, recv, RDMA)
   - Generate completion notification
```

### Completion Processing Flow

```
1. NIC completes operation
   - Write notification to notification queue
   - Set prime marker for validity

2. Host polls notification queue
   - Check marker for new entries
   - Read notification type

3. Host processes notification
   - Receive: Extract data, update buffers
   - Send: Free resources, notify application
   - Event: Log, handle error condition

4. Host advances consumer index
   - Update notification queue consumer
   - Free processed entries
```

---

## 6. Additional HSI Formats

### 6.1 Notification Entry (64 bytes)

**Datamodel**: `notification_entry.ksy`

Common header for all notification types with prime marker validity detection.

#### Wire Format

```
Byte:    0       1       2       3       4-62                    63
     +-------+-------+-------+-------+---------------------------+-------+
     | type  | flags |    status     |   type_specific_data      |marker |
     +-------+-------+-------+-------+---------------------------+-------+
```

#### Field Definitions

| Field | Bits | Offset | Description |
|-------|------|--------|-------------|
| type | 8 | 0 | Notification type (0=recv, 1=send, 2=event) |
| flags | 8 | 1 | Flags (bit 0=FI_INLINE, bit 1=continuation) |
| status | 16 | 2-3 | Completion status (0=success) |
| type_specific_data | 472 | 4-62 | Type-specific fields |
| marker | 8 | 63 | Prime marker (1-13) |

#### Prime Marker Polling

- Provider polls byte 63 of next expected entry
- Marker cycles 1→2→...→13→1
- Queue depth MUST NOT be multiple of 13
- Single cache miss fetches entire 64-byte entry

---

### 6.2 QW Violation Event (64 bytes)

**Datamodel**: `qw_violation_event.ksy`

Event generated when software writes to command queue BAR with incorrect size/alignment.

#### Wire Format

```
Byte:    0       1       2       3       4       5       6       7
     +-------+-------+-------+-------+-------+-------+-------+-------+
     |evt_typ|vio_typ|  endpoint_id  |       size_or_offset          |
     +-------+-------+-------+-------+-------+-------+-------+-------+
         8       9      10      11      12      13      14      15
     +-------+-------+-------+-------+-------+-------+-------+-------+
     |                      bar_offset [63:0]                        |
     +-------+-------+-------+-------+-------+-------+-------+-------+
        16      17      18      19      20      21      22      23
     +-------+-------+-------+-------+-------+-------+-------+-------+
     |                      timestamp [63:0]                         |
     +-------+-------+-------+-------+-------+-------+-------+-------+
        24-62                                                   63
     +-------------------------------------------------------+-------+
     |                      reserved (39 bytes)              |marker |
     +-------------------------------------------------------+-------+
```

#### Field Definitions

| Field | Bits | Offset | Description |
|-------|------|--------|-------------|
| event_type | 8 | 0 | Always 0x10 (QW_VIOLATION) |
| violation_type | 8 | 1 | 0x01=SUB_QW, 0x02=UNALIGNED |
| endpoint_id | 16 | 2-3 | Endpoint where violation occurred |
| size_or_offset | 32 | 4-7 | Write size (SUB_QW) or misalignment (UNALIGNED) |
| bar_offset | 64 | 8-15 | BAR offset of violating write |
| timestamp | 64 | 16-23 | NIC timestamp |
| reserved | 312 | 24-62 | Reserved |
| marker | 8 | 63 | Prime marker |

---

### 6.3 PCIe Descriptors (64 bytes)

**Datamodel**: `pcie/descriptors.ksy`

Phase 1 command and notification descriptors for PCIe interface.

#### Command Descriptor

```
Byte:    0       1       2       3       4       5       6       7
     +-------+-------+-------+-------+-------+-------+-------+-------+
     |                      opcode [63:0]                            |
     |  OP   | FLAGS |              reserved                         |
     +-------+-------+-------+-------+-------+-------+-------+-------+
         8-15                16-19   20-23   24-55           56-63
     +-------+-------+-------+-------+-------+-------+-------+-------+
     |   packet_addr [63:0]  |pkt_len| rsvd  |  metadata (32B)| rsvd |
     +-------+-------+-------+-------+-------+-------+-------+-------+
```

| Field | Bits | Offset | Description |
|-------|------|--------|-------------|
| opcode | 64 | 0-7 | Operation (bits 7:0) + flags (bits 15:8) |
| packet_addr | 64 | 8-15 | Physical address of packet |
| packet_length | 32 | 16-19 | Packet length (max 9216) |
| metadata | 256 | 24-55 | Reserved for future use |

#### Notification Descriptor

```
Byte:    0       1       2       3       4       5       6       7
     +-------+-------+-------+-------+-------+-------+-------+-------+
     |                      status [63:0]                            |
     | TYPE  | FLAGS |              reserved                         |
     +-------+-------+-------+-------+-------+-------+-------+-------+
         8-15                16-19   20-23   24-55           56-63
     +-------+-------+-------+-------+-------+-------+-------+-------+
     |   packet_addr [63:0]  |pkt_len|err_cd |  metadata (32B)| rsvd |
     +-------+-------+-------+-------+-------+-------+-------+-------+
```

| Field | Bits | Offset | Description |
|-------|------|--------|-------------|
| status | 64 | 0-7 | Type (bits 7:0) + flags (bits 15:8) |
| packet_addr | 64 | 8-15 | Packet address |
| packet_length | 32 | 16-19 | Packet length |
| error_code | 32 | 20-23 | Error code (0=success) |
| metadata | 256 | 24-55 | Reserved for future use |

---

## 7. Cross-References

### Related Documents

| Document | Content |
|----------|---------|
| [packet_taxonomy.md](packet_taxonomy.md) | Master index |
| [packet_taxonomy_ue_pds.md](packet_taxonomy_ue_pds.md) | UE+ PDS (wire protocol) |

### Datamodel Files

| File | Description |
|------|-------------|
| `command_queue_segment.ksy` | Command Queue Segment (64 bytes) |
| `receive_notification.ksy` | Receive Notification (64 bytes) |
| `send_completion.ksy` | Send Completion (64 bytes) |
| `event_notification.ksy` | Event Notification (64 bytes) |
| `notification_entry.ksy` | Generic Notification Entry |
| `sgl_entry.ksy` | SGL Entry (32 bytes) |
| `qw_violation_event.ksy` | QW Violation Event |
| `pcie/descriptors.ksy` | PCIe Phase 1 Descriptors |

---

## 8. References

- specs/021-command-queue-hsi/spec.md
- specs/021-command-queue-hsi/data-model.md
- PMR Hardware Architecture Specification
