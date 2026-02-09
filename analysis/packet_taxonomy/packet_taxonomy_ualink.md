# PMR Packet Taxonomy: UALink Protocol (Reference Only)

**Parent Document**: [packet_taxonomy.md](packet_taxonomy.md)  
**Scope**: Ultra Accelerator Link (UALink) protocol formats  
**Datamodel Directory**: `datamodel/protocols/ualink/`  
**Last Updated**: 2026-01-30

---

> ⚠️ **Reference Only**: UALink is defined in the datamodel but is **NOT currently supported by PMR**. It is included here for reference as it may be relevant for future AI/ML accelerator interconnect work.

---

## Table of Contents

1. [Overview](#1-overview)
2. [Protocol Layers](#2-protocol-layers)
3. [UPLI Layer](#3-upli-layer)
4. [Transaction Layer](#4-transaction-layer)
5. [Data Link Layer](#5-data-link-layer)
6. [Physical Layer](#6-physical-layer)
7. [Security Layer](#7-security-layer)
8. [Cross-References](#8-cross-references)
   - 8.5 [YAML Reference Files](#85-yaml-reference-files)
   - 8.6 [Recent Updates (W-14)](#86-recent-updates-w-14)
9. [References](#9-references)

---

## 1. Overview

UALink (Ultra Accelerator Link) is an AI/ML accelerator interconnect protocol with 38 packet definitions (6,023 total lines) across all OSI layers. It is designed for high-bandwidth, low-latency communication between AI accelerators (GPUs, TPUs, etc.).

### Layer Summary

| Layer | Count | Key Formats |
|-------|-------|-------------|
| UPLI (Upper Protocol Layer Interface) | 8 | commands.ksy, request_channel.ksy, status_codes.ksy |
| Transaction | 9 | tl_flit.ksy, control_half_flit.ksy, data_half_flit.ksy |
| Data Link | 12 | dl_flit.ksy, segment_header.ksy, crc.ksy, control_messages.ksy |
| Physical | 4 | alignment_markers.ksy, control_ordered_sets.ksy, link_training.ksy |
| Security | 5 | authentication.ksy, encryption.ksy, key_derivation.ksy |

---

## 2. Protocol Layers

```
UALink Protocol Stack:
┌─────────────────────────────────────────────────────────────────┐
│                    UPLI (Upper Protocol Layer Interface)        │
│                    Commands, Request/Response Channels          │
├─────────────────────────────────────────────────────────────────┤
│                    Transaction Layer                            │
│                    TL Flits, Flow Control                       │
├─────────────────────────────────────────────────────────────────┤
│                    Data Link Layer                              │
│                    DL Flits, Segments, CRC, Replay              │
├─────────────────────────────────────────────────────────────────┤
│                    Physical Layer                               │
│                    Alignment, Training, Ordered Sets            │
├─────────────────────────────────────────────────────────────────┤
│                    Security Layer (Cross-cutting)               │
│                    Authentication, Encryption, Key Management   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. UPLI Layer

**Datamodel Directory**: `datamodel/protocols/ualink/upli/`

The Upper Protocol Layer Interface provides the application-facing API for UALink operations.

### Formats

| Format | File | Description |
|--------|------|-------------|
| Commands | `commands.ksy` | UPLI command definitions |
| Request Channel | `request_channel.ksy` | Request channel format |
| Originator Data | `originator_data_channel.ksy` | Originator data channel |
| Read Response | `read_response_channel.ksy` | Read response channel |
| Write Response | `write_response_channel.ksy` | Write response channel |
| Status Codes | `status_codes.ksy` | Status code definitions |
| Connection Handshake | `protocols/connection_handshake.ksy` | Connection setup |
| Flow Control | `protocols/flow_control.ksy` | Flow control protocol |

---

## 4. Transaction Layer

**Datamodel Directory**: `datamodel/protocols/ualink/transaction/`

The Transaction Layer handles message framing and flow control.

### Formats

| Format | File | Description |
|--------|------|-------------|
| TL Flit | `tl_flit.ksy` | Transaction layer flit |
| Control Half Flit | `control_half_flit.ksy` | Control half flit |
| Data Half Flit | `data_half_flit.ksy` | Data half flit |
| Message Half Flit | `message_half_flit.ksy` | Message half flit |
| Request Field | `request_field.ksy` | Request field format |
| Response Field | `response_field.ksy` | Response field format |
| Flow Control Field | `flow_control_field.ksy` | Flow control field |
| Compression | `protocols/compression.ksy` | Data compression |
| Address Cache | `protocols/address_cache.ksy` | Address caching |

---

## 5. Data Link Layer

**Datamodel Directory**: `datamodel/protocols/ualink/datalink/`

The Data Link Layer provides reliable delivery with CRC protection and replay.

### Formats

| Format | File | Description |
|--------|------|-------------|
| DL Flit | `dl_flit.ksy` | Data link flit |
| Flit Header | `flit_header.ksy` | Flit header format |
| Segment Header | `segment_header.ksy` | Segment header |
| CRC | `crc.ksy` | CRC calculation |
| Control Messages | `messages/control_messages.ksy` | Control messages |
| Basic Messages | `messages/basic_messages.ksy` | Basic messages |
| UART Messages | `messages/uart_messages.ksy` | UART messages |
| Vendor Defined | `messages/vendor_defined.ksy` | Vendor extensions |
| Link Resiliency | `protocols/link_resiliency.ksy` | Link resiliency |
| Link Level Replay | `protocols/link_level_replay.ksy` | Replay protocol |
| Link State | `protocols/link_state.ksy` | Link state machine |
| Link Folding | `protocols/link_folding.ksy` | Link folding |

---

## 6. Physical Layer

**Datamodel Directory**: `datamodel/protocols/ualink/physical/`

The Physical Layer handles lane alignment and link training.

### Formats

| Format | File | Description |
|--------|------|-------------|
| Alignment Markers | `alignment_markers.ksy` | Lane alignment |
| Control Ordered Sets | `control_ordered_sets.ksy` | Control sequences |
| Reconciliation Sublayer | `reconciliation_sublayer.ksy` | RS sublayer |
| Link Training | `protocols/link_training.ksy` | Link training |

---

## 7. Security Layer

**Datamodel Directory**: `datamodel/protocols/ualink/security/`

The Security Layer provides authentication and encryption.

### Formats

| Format | File | Description |
|--------|------|-------------|
| Authentication | `authentication.ksy` | Authentication |
| Encryption | `encryption.ksy` | Encryption format |
| IV Format | `iv_format.ksy` | Initialization vector |
| Key Derivation | `protocols/key_derivation.ksy` | Key derivation |
| Key Rotation | `protocols/key_rotation.ksy` | Key rotation |

---

## 8. Cross-References

### Related Documents

| Document | Content |
|----------|---------|
| [packet_taxonomy.md](packet_taxonomy.md) | Master index |

### PMR Support Status

| Feature | Status |
|---------|--------|
| UALink Protocol | **NOT SUPPORTED** |
| Future Support | Under consideration for AI/ML workloads |

### 8.5 YAML Reference Files

YAML reference files exist in `reference/field_definitions/` for packets meeting specific criteria. Not all 38 KSY files require YAML references.

#### Coverage Criteria

| Criterion | Description | Rationale |
|-----------|-------------|-----------|
| Entry point packets | Top-level structures for parsing | Entry points need clear field summaries for parser initialization |
| Multi-variant formats | Structures with encoding variants | Variants are easier to compare in YAML table format |
| Cross-layer interfaces | Structures bridging protocol layers | Interface boundaries need explicit field-by-field documentation |
| High-complexity fields | Fields with many sub-fields/constraints | Complex structures benefit from human-readable summaries |

#### Current Coverage (6 files)

| File | Criterion | Description |
|------|-----------|-------------|
| `tl_flit.yaml` | Entry point | Transaction Layer Flit structure |
| `dl_flit.yaml` | Entry point | Data Link Flit structure |
| `response_field.yaml` | Multi-variant | 3 response field variants (uncompressed, compressed single-beat, compressed multi-beat) |
| `upli_request_channel.yaml` | Cross-layer | UPLI to Transaction Layer interface |
| `link_state.yaml` | Cross-layer | Link state protocol interface |
| `flow_control_field.yaml` | High-complexity | FC/NOP field details |

The remaining 32 KSY files are self-documenting through their `doc:` blocks and `x-spec` metadata.

### 8.6 Recent Updates (W-14)

W-14 work items completed significant expansions to the UALink datamodel.

#### W-14 Summary

| Work Item | File(s) | Before | After | Description |
|-----------|---------|--------|-------|-------------|
| W-14-004 | security/*.ksy (5 files) | ~270 | ~1,655 | Security layer expansion (Tables 9-1 through 9-7) |
| W-14-007 | 37 KSY files | 0 | 37 | x-related-headers cross-references added |
| W-14-008 | data_half_flit.ksy | 40 | 142 | Half-flit expansion (Table 5-2, Section 5.3) |
| W-14-008 | message_half_flit.ksy | 37 | 148 | Half-flit expansion (Tables 5-3, 5-4) |
| W-14-009 | response_field.ksy | 52 | 310 | Response field expansion (Tables 5-30, 5-34, 5-35) |
| W-14-010 | flit_header.ksy | 90 | 165 | Flit header expansion (top-level seq, discriminators) |
| W-14-011 | README.md | - | - | YAML coverage criteria documented |

#### Key Improvements

- **Security Layer**: Expanded from ~270 to ~1,655 lines with full encryption/authentication attributes per Tables 9-4 through 9-7
- **Cross-References**: All 37 applicable KSY files now have `x-related-headers` sections for navigation
- **Half-Flit Quality**: data_half_flit and message_half_flit now match control_half_flit exemplar quality
- **Response Field**: Full bit-level parsing for all 3 response variants
- **Flit Header**: Now parseable with top-level seq and discriminator instances

---

## 9. References

- UALink Specification (Ultra Accelerator Link)
- AI/ML Accelerator Interconnect Standards
