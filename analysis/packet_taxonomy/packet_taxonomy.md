# PMR (CN7000) Packet Format Taxonomy

**Document**: Master index for PMR NIC ASIC packet format documentation  
**Generated**: 2026-01-14  
**Last Reviewed**: 2026-02-03  
**Source**: `datamodel/` directory in EarlySim repository  
**Reference**: `docs/HAS/PMR/05-packet-formats.md`

---

## Table of Contents

1. [Overview](#1-overview)
2. [Protocol Stack Summary](#2-protocol-stack-summary)
3. [Document Index](#3-document-index)
4. [Quick Reference](#4-quick-reference)
5. [Work List](#9-work-list)
6. [References](#10-references)

---

## 1. Overview

PMR (Prism River) is Cornelis Networks' 1.6 Tbps NIC ASIC (CN7000 product family). It supports multiple wire protocols with per-packet protocol selection on a single physical port.

### Supported Protocols

| Protocol | Version | Status | Description |
|----------|---------|--------|-------------|
| Ultra Ethernet+ | 1.0.1 | Full | Optimized UE with Cornelis extensions |
| RoCEv2 | v2 | Full | RDMA over Converged Ethernet |
| Standard Ethernet | IEEE 802.3 | Full | Traditional Ethernet with offloads |
| Cornelis Proprietary | 1.0.0 | Full | UFH, CSIG+, VxLAN+, Collectives |

### Header Efficiency Comparison

| Protocol Stack | Total Headers | Efficiency (4KB payload) |
|----------------|---------------|--------------------------|
| UE+ (small msg) | ~20 bytes | 99.5% |
| UE+ (standard) | ~40 bytes | 99.0% |
| RoCEv2 (IPv4) | ~58 bytes | 98.6% |
| RoCEv2 (IPv6) | ~78 bytes | 98.1% |

---

## 2. Protocol Stack Summary

```
+-----------------------------------------------------------------------------+
|                           Application Layer                                  |
|                    (Libfabric, Verbs, Sockets, DPDK)                         |
+-----------------------------------------------------------------------------+
|                           Transport Layer                                    |
|  +------------------+  +------------------+  +------------------+            |
|  |   UE Transport   |  |     RoCEv2       |  |    TCP/UDP       |            |
|  |   (SES/PDS/CMS)  |  |   (BTH/RETH)     |  |                  |            |
|  +------------------+  +------------------+  +------------------+            |
+-----------------------------------------------------------------------------+
|                           Network Layer                                      |
|  +------------------+  +------------------+  +------------------+            |
|  |   UFH-16/32      |  |   IPv4/IPv6      |  |   IPv4/IPv6      |            |
|  |   (Cornelis)     |  |   + UDP          |  |                  |            |
|  +------------------+  +------------------+  +------------------+            |
+-----------------------------------------------------------------------------+
|                            Link Layer                                        |
|  +------------------+  +------------------+  +------------------+            |
|  |      UE+         |  |   Ethernet II    |  |   Ethernet II    |            |
|  |   (12 bytes)     |  |   (14 bytes)     |  |   (14 bytes)     |            |
|  +------------------+  +------------------+  +------------------+            |
+-----------------------------------------------------------------------------+
|                          Physical Layer                                      |
|                    Hill Creek (212.5G x8 PAM4 SerDes)                        |
+-----------------------------------------------------------------------------+
      Ultra Ethernet+           RoCEv2              Standard Ethernet
```

---

## 3. Document Index

This taxonomy is organized into sub-documents by protocol layer and type.

### Ultra Ethernet+ (UE+) Formats

| Document | Scope | Formats | Datamodel Directory |
|----------|-------|---------|---------------------|
| [packet_taxonomy_ue_pds.md](packet_taxonomy_ue_pds.md) | PDS (Packet Delivery Sublayer) | RUD, ROD, RUDI, UUD, ACK, NACK, CP | `ue/transport/pds/` |
| [packet_taxonomy_ue_ses.md](packet_taxonomy_ue_ses.md) | SES (Semantic Sublayer) | Standard Request, Response, Small Message, Atomic, Rendezvous | `ue/transport/ses/` |
| [packet_taxonomy_ue_cms_tss.md](packet_taxonomy_ue_cms_tss.md) | CMS + TSS | Congestion Control, Security Headers | `ue/transport/cms/`, `ue/transport/tss/` |
| [packet_taxonomy_ue_link.md](packet_taxonomy_ue_link.md) | Link Layer | LLR, CBFC, LLDP TLVs | `ue/link/` |
| [packet_taxonomy_ue_tagged_send_variants.md](packet_taxonomy_ue_tagged_send_variants.md) | Tagged-Send Variants | UE Standard, CSIG, IPv4, TSS, Small, Rendezvous, Deferrable | `ue/transport/` |

### Other Protocol Formats

| Document | Scope | Formats | Datamodel Directory |
|----------|-------|---------|---------------------|
| [packet_taxonomy_rocev2.md](packet_taxonomy_rocev2.md) | RoCEv2 | BTH, RETH, AETH, AtomicETH, DETH | `roce/transport/` |
| [packet_taxonomy_cornelis.md](packet_taxonomy_cornelis.md) | Cornelis Proprietary | UFH-16, UFH-32, CSIG+, VxLAN+, Collective L2 | `cornelis/` |
| [packet_taxonomy_hsi.md](packet_taxonomy_hsi.md) | Host-Software Interface | Command Queue, Notifications, SGL | `hw/asics/pmr/interfaces/` |
| [packet_taxonomy_ualink.md](packet_taxonomy_ualink.md) | UALink (Reference Only) | UPLI, Transaction, Data Link, Physical | `ualink/` |

### Document Relationships

```
                          packet_taxonomy.md (this document)
                                    |
          +-------------------------+-------------------------+
          |                         |                         |
    UE+ Transport              Other Protocols           Infrastructure
          |                         |                         |
    +-----+-----+             +-----+-----+                   |
    |     |     |             |     |     |                   |
   PDS   SES  CMS/TSS      RoCEv2 Cornelis              HSI  UALink
    |     |     |             |     |                    |   (ref only)
  Link   ...   ...           ...   ...                  ...
```

---

## 4. Quick Reference

### UE+ PDS Types

| Type | Value | Size | Document Section |
|------|-------|------|------------------|
| RUD Request | 0x01 | 12 bytes | [PDS 3.1](packet_taxonomy_ue_pds.md#31-rud-request-type-0x01-12-bytes) |
| ROD Request | 0x02 | 12 bytes | [PDS 3.2](packet_taxonomy_ue_pds.md#32-rod-request-type-0x02-12-bytes) |
| RUDI Request | 0x04 | 6 bytes | [PDS 3.3](packet_taxonomy_ue_pds.md#33-rudi-request-type-0x04-6-bytes) |
| RUDI Response | 0x05 | 6 bytes | [PDS 3.4](packet_taxonomy_ue_pds.md#34-rudi-response-type-0x05-6-bytes) |
| UUD Request | 0x06 | 6 bytes | [PDS 3.5](packet_taxonomy_ue_pds.md#35-uud-request-type-0x06-6-bytes) |
| ACK | 0x07 | 12 bytes | [PDS 3.6](packet_taxonomy_ue_pds.md#36-ack-type-0x07-12-bytes) |
| ACK_CC | 0x08 | 32 bytes | [PDS 3.7](packet_taxonomy_ue_pds.md#37-ack_cc-type-0x08-32-bytes) |
| ACK_CCX | 0x09 | 44 bytes | [PDS 3.8](packet_taxonomy_ue_pds.md#38-ack_ccx-type-0x09-44-bytes) |
| NACK | 0x0A | 12 bytes | [PDS 3.9](packet_taxonomy_ue_pds.md#39-nack-type-0x0a-12-bytes) |
| CP | 0x0B | 12 bytes | [PDS 3.10](packet_taxonomy_ue_pds.md#310-control-packet-type-0x0b-12-bytes) |
| NACK_CCX | 0x0C | 28 bytes | [PDS 3.11](packet_taxonomy_ue_pds.md#311-nack_ccx-type-0x0c-28-bytes) |

### UE+ SES Formats

| Format | Size | Document Section |
|--------|------|------------------|
| Standard Request (SOM=1) | 44 bytes | [SES 2.1](packet_taxonomy_ue_ses.md#21-standard-request-som1-44-bytes) |
| Standard Request (SOM=0) | 16 bytes | [SES 2.2](packet_taxonomy_ue_ses.md#22-standard-request-som0-16-bytes) |
| Response | 16 bytes | [SES 2.3](packet_taxonomy_ue_ses.md#23-response-16-bytes) |
| Response with Data | 24 bytes | [SES 2.4](packet_taxonomy_ue_ses.md#24-response-with-data-24-bytes) |
| Small Message | 32 bytes | [SES 2.5](packet_taxonomy_ue_ses.md#25-small-message-32-bytes) |
| Rendezvous Extension | 32 bytes | [SES 2.6](packet_taxonomy_ue_ses.md#26-rendezvous-extension-32-bytes) |
| Atomic Extension | 8 bytes | [SES 2.7](packet_taxonomy_ue_ses.md#27-atomic-extension-8-bytes) |

### UE+ Link Layer Formats

| Format | Size | Document Section |
|--------|------|------------------|
| LLR_ACK CtlOS | 8 bytes | [Link 2.1](packet_taxonomy_ue_link.md#21-llr_ack-ctlos-8-bytes) |
| [packet_taxonomy_ue_tagged_send_variants.md](packet_taxonomy_ue_tagged_send_variants.md) | Tagged-Send Variants | UE Standard, CSIG, IPv4, TSS, Small, Rendezvous, Deferrable | `ue/transport/` |
| LLR_NACK CtlOS | 8 bytes | [Link 2.2](packet_taxonomy_ue_link.md#22-llr_nack-ctlos-8-bytes) |
| [packet_taxonomy_ue_tagged_send_variants.md](packet_taxonomy_ue_tagged_send_variants.md) | Tagged-Send Variants | UE Standard, CSIG, IPv4, TSS, Small, Rendezvous, Deferrable | `ue/transport/` |
| LLR_INIT CtlOS | 8 bytes | [Link 2.3](packet_taxonomy_ue_link.md#23-llr_init-ctlos-8-bytes) |
| [packet_taxonomy_ue_tagged_send_variants.md](packet_taxonomy_ue_tagged_send_variants.md) | Tagged-Send Variants | UE Standard, CSIG, IPv4, TSS, Small, Rendezvous, Deferrable | `ue/transport/` |
| LLR_INIT_ECHO CtlOS | 8 bytes | [Link 2.4](packet_taxonomy_ue_link.md#24-llr_init_echo-ctlos-8-bytes) |
| [packet_taxonomy_ue_tagged_send_variants.md](packet_taxonomy_ue_tagged_send_variants.md) | Tagged-Send Variants | UE Standard, CSIG, IPv4, TSS, Small, Rendezvous, Deferrable | `ue/transport/` |
| CF_Update CtlOS | 8 bytes | [Link 4.1](packet_taxonomy_ue_link.md#41-cf_update-ctlos-8-bytes) |
| [packet_taxonomy_ue_tagged_send_variants.md](packet_taxonomy_ue_tagged_send_variants.md) | Tagged-Send Variants | UE Standard, CSIG, IPv4, TSS, Small, Rendezvous, Deferrable | `ue/transport/` |
| CC_Update Message | 8 bytes | [Link 4.2](packet_taxonomy_ue_link.md#42-cc_update-message-8-bytes) |
| [packet_taxonomy_ue_tagged_send_variants.md](packet_taxonomy_ue_tagged_send_variants.md) | Tagged-Send Variants | UE Standard, CSIG, IPv4, TSS, Small, Rendezvous, Deferrable | `ue/transport/` |

### RoCEv2 Headers

| Header | Size | Document Section |
|--------|------|------------------|
| BTH | 12 bytes | [RoCEv2 2.1](packet_taxonomy_rocev2.md#21-bth-base-transport-header-12-bytes) |
| RETH | 16 bytes | [RoCEv2 2.2](packet_taxonomy_rocev2.md#22-reth-rdma-extended-transport-header-16-bytes) |
| AETH | 4 bytes | [RoCEv2 2.3](packet_taxonomy_rocev2.md#23-aeth-ack-extended-transport-header-4-bytes) |
| AtomicETH | 28 bytes | [RoCEv2 2.4](packet_taxonomy_rocev2.md#24-atomiceth-atomic-extended-transport-header-28-bytes) |

### Cornelis Proprietary

| Format | Size | Document Section |
|--------|------|------------------|
| UFH-16 | 12 bytes | [Cornelis 2.1](packet_taxonomy_cornelis.md#21-ufh-16-unified-forwarding-header-16-bit-addressing-12-bytes) |
| UFH-32 | 12 bytes | [Cornelis 2.2](packet_taxonomy_cornelis.md#22-ufh-32-unified-forwarding-header-32-bit-addressing-12-bytes) |
| CSIG+ | Variable | [Cornelis 3.1](packet_taxonomy_cornelis.md#31-csig-telemetry-header) |
| VxLAN+ | Variable | [Cornelis 4.1](packet_taxonomy_cornelis.md#41-vxlan-extended-vxlan-overlay) |

---

## 5. Work List

This section tracks issues requiring follow-up investigation or specification updates.

### 5.1 Open Issues

| ID | Priority | Category | Description | Status | Opened | Closed |
|----|----------|----------|-------------|--------|--------|--------|
| W-06-001 | Medium | Datamodel | UFH-32 lacks 16-bit entropy field; per-packet ECMP not supported; switch must derive entropy from Src+Dest hash. Note: UFH entropy fields might use the UE Entropy Header (see `ue/transport/pds/entropy_header.ksy`, UE Spec Table 3-31, Section 3.5.10.1) | Deferred | 2026-01-20 | - |
| W-07-001 | Low | Datamodel | `ack_cc.ksy` shows `ack_cc_state` as 32-bit (4 bytes) but UE Spec Table 3-36 shows 64-bit (8 bytes); verify field size | Closed | 2026-01-22 | 2026-01-23 |
| W-07-002 | Low | Documentation | `collective_l2.ksy` and `scaleup_l2.ksy` marked as "work_in_progress" with spec_version 0.1; specifications incomplete | Closed | 2026-01-22 | 2026-01-27 |
| W-07-003 | Low | Datamodel | `ue_plus.ksy` Length field units TBD (now 6 bits per W-04-004 restructuring) | Investigation | 2026-01-22 | - |
| W-04-004 | High | Datamodel | `ue_plus.ksy` complete restructuring: 24-bit HMAC addresses, correct field layout | Closed | 2026-01-10 | 2026-01-26 |
| W-05-002 | Medium | Specification | MTU values: Verify maximum MTU for each protocol | Closed | 2026-01-10 | 2026-01-26 |
| W-05-003 | Medium | Documentation | CMS detailed formats: Need comprehensive documentation | Closed | 2026-01-10 | 2026-01-26 |
| W-03-002 | Low | Terminology | PDP vs PDS naming: UML uses both terms inconsistently. **Tracked in:** `earlysim/docs/HAS/PMR/WORK.md` | Spec Update | 2026-01-08 | - |
| W-03-006 | Low | Terminology | SES vs SE: "SES Processing Groups" vs "Semantic Engines". **Tracked in:** `earlysim/docs/HAS/PMR/WORK.md` | Spec Update | 2026-01-08 | - |
| W-08-001 | Low | Datamodel | `collective_l2.ksy` marked as WIP (spec_version 0.1); specification incomplete | Spec Update | 2026-01-23 | - |
| W-08-002 | Low | Datamodel | `scaleup_l2.ksy` marked as WIP (spec_version 0.1); specification incomplete | Spec Update | 2026-01-23 | - |
| W-09-001 | - | Datamodel | ~~Create UE L2 header~~ - UE uses standard Ethernet II; no custom L2 header | Closed | 2026-01-23 | 2026-01-26 |
| W-09-002 | - | Datamodel | ~~Create FEP address format~~ - FEP uses standard IPv4/IPv6 addresses | Closed | 2026-01-23 | 2026-01-26 |
| W-09-003 | Medium | Datamodel | Document PDCID format and pdc_info encoding per Section 3.5.11.5 | Closed | 2026-01-23 | 2026-01-26 |
| W-09-004 | - | Datamodel | ~~Create UET network header~~ - UE uses standard IP headers | Closed | 2026-01-23 | 2026-01-26 |
| W-09-005 | Medium | Datamodel | Create CP payload formats per Section 3.5.16.8 | Closed | 2026-01-23 | 2026-01-26 |
| W-09-006 | Medium | Datamodel | Update `rud_rod_cp.ksy` with payload field and note spdcid/dpdcid "Same as ACK" | Closed | 2026-01-23 | 2026-01-26 |
| W-09-007 | Low | Datamodel | Create `nack_codes.ksy` enumeration per Table 3-59 | Closed | 2026-01-23 | 2026-01-26 |
| W-09-008 | Low | Datamodel | Create `next_header_types.ksy` enumeration per Table 3-16 | Closed | 2026-01-23 | 2026-01-26 |
| W-09-009 | Medium | Architecture | Define rules for when PMR uses standard Ethernet vs Cornelis UE+ header | Closed | 2026-01-23 | 2026-02-03 |
| W-09-010 | Low | Datamodel | Document UFH headers when UEC standardizes them (future, optional) | Deferred | 2026-01-26 | - |
| W-10-001 | Low | Datamodel | Create `cc_type.ksy` enumeration per Table 3-48 (CC_NSCC, CC_CREDIT) | Closed | 2026-01-27 | 2026-01-27 |
| W-10-002 | Low | Datamodel | Create `ccx_type.ksy` enumeration per Table 3-49 (all reserved) | Closed | 2026-01-27 | 2026-01-27 |
| W-10-003 | Low | Datamodel | Add preprocessing algorithm references to CMS .ksy files (Sections 3.6.10.3, 3.6.10.4) | Closed | 2026-01-27 | 2026-01-27 |
| W-10-004 | Low | Datamodel | Add Credit CP protocol constraints to `credit_cp_payload.ksy` (pds.psn=0x0, pds.flags.ar=0) | Closed | 2026-01-27 | 2026-01-27 |
| W-10-005 | Low | Datamodel | Add API function references to `ccc_state_machine.ksy` (Section 3.6.8.1: AllocateCCC, OnACK, OnNACK, etc.) | Closed | 2026-01-27 | 2026-01-27 |
| W-10-006 | Low | Datamodel | Expand `nscc_source.ksy` stub with NSCC source algorithm (Sections 3.6.13.3-3.6.13.6, Table 3-76) | Closed | 2026-01-27 | 2026-01-27 |
| W-11-001 | Low | Datamodel | Update `bth.ksy` `is_atomic` docs with operation codes 0x12-0x14 and transport type restrictions (RC/RD/XRC only) | Closed | 2026-01-27 | 2026-01-27 |
| W-11-002 | Low | Datamodel | Add `is_ack` (0x11) and `is_atomic_ack` (0x12) instances to `bth.ksy` with IB Spec references | Closed | 2026-01-27 | 2026-01-27 |
| W-11-003 | Medium | Datamodel | Add CNP (4, 0x80) and XRC (5, 0xA0) transport types to `bth.ksy` enum and opcode documentation | Closed | 2026-01-27 | 2026-01-27 |
| W-11-004 | Medium | Datamodel | Document FECN (bit 7) and BECN (bit 6) in `bth.ksy` reserved field with ICRC masking note; added `fecn` and `becn` instances | Closed | 2026-01-27 | 2026-01-27 |
| W-10-007 | Low | Datamodel | Expand `nscc_destination.ksy` stub with NSCC destination algorithm (Section 3.6.13.9) | Deferred | 2026-01-27 | - |
| W-10-008 | Low | Datamodel | Expand `rccc_source.ksy` stub with RCCC source algorithm (Sections 3.6.14.2-3.6.14.4) | Deferred | 2026-01-27 | - |
| W-10-009 | Low | Datamodel | Expand `rccc_destination.ksy` stub with RCCC destination algorithm (Sections 3.6.14.5-3.6.14.6) | Deferred | 2026-01-27 | - |
| W-10-010 | Low | Datamodel | Expand `tfc_source.ksy` stub with TFC source behavior (Section 3.6.15) | Deferred | 2026-01-27 | - |
| W-10-011 | Low | Datamodel | Expand `tfc_destination.ksy` stub with TFC destination behavior (Section 3.6.15) | Deferred | 2026-01-27 | - |
| W-10-012 | Low | Datamodel | Expand `multipath_selection.ksy` stub with multipath algorithms (Section 3.6.16) | Deferred | 2026-01-27 | - |
| W-10-013 | Medium | Investigation | Investigate CC_TYPE (14-15) and CCX_TYPE (14-15) proprietary extensions as Cornelis value-add for congestion management. UE Spec reserves these for vendor-specific CC algorithms. | Investigation | 2026-01-27 | - |
| W-10-014 | Medium | Datamodel | Fix `ack_cc_state_rccc_tfc.ksy` to 8 bytes (64 bits) with 24-bit reserved field (Bytes 3-5) to match ACK_CC pds.ack_cc_state field size. Update `cc_type.ksy` CC_CREDIT size reference. | Closed | 2026-01-27 | 2026-01-27 |
| W-10-015 | Low | Review | In-depth review of expanded `nscc_source.ksy` against UE Spec 1.0.1 Sections 3.6.13.1-3.6.13.7. Verify configuration parameters (Table 3-76), state variables (Table 3-77), algorithm pseudocode accuracy. Follow-on to W-10-006. | Closed | 2026-01-27 | 2026-02-03 |
| W-11-001 | Low | Datamodel | Update `bth.ksy` `is_atomic` documentation to note it includes requests (CMP_SWAP, FETCH_ADD) and response (ATOMIC_ACK); add note that atomics only supported on RC, RD, XRC transport types | Closed | 2026-01-27 | 2026-01-27 |
| W-11-002 | Low | Datamodel | Add `is_ack` (operation 0x11) and `is_atomic_ack` (operation 0x12) instances to `bth.ksy` | Closed | 2026-01-27 | 2026-01-27 |
| W-11-003 | Medium | Datamodel | Add CNP (value=4, base=0x80) and XRC (value=5, base=0xA0) transport types to `bth.ksy` enum and opcode documentation | Closed | 2026-01-27 | 2026-01-27 |
| W-11-004 | Medium | Datamodel | Document FECN (bit 7) and BECN (bit 6) in `bth.ksy` reserved field; add note that these must be masked during ICRC calculation | Closed | 2026-01-27 | 2026-01-27 |
| W-11-005 | Medium | Datamodel | Add operation validity matrix by transport type to `bth.ksy` (e.g., atomics only on RC/RD/XRC, SEND on all types) | Closed | 2026-01-27 | 2026-01-27 |
| W-11-006 | Low | Datamodel | Fix `aeth.ksy` credit_count documentation - syndrome bits [5:0] description says 6 bits but credit is only 5 bits (0x1f mask) | Closed | 2026-01-27 | 2026-01-27 |
| W-11-007 | Low | Datamodel | Add cross-references between all RoCE transport header files (bth, reth, aeth, deth, immdt, atomiceth, atomicacketh, icrc) | Closed | 2026-01-27 | 2026-01-27 |
| W-11-008 | Low | Datamodel | Add `x-spec` metadata blocks to RoCE files for consistency with CMS datamodel style | Closed | 2026-01-27 | 2026-01-27 |
| W-11-009 | Medium | Investigation | Obtain and review InfiniBand Architecture Specification Release 2.0 (announced Nov 2025). Compare with Release 1.4 for RoCEv2-relevant changes. Contact IBTA at administration@infinibandta.org for access. | Pending | 2026-01-27 | - |
| W-12-001 | Low | Datamodel | `bth.ksy` `is_atomic` doc uses hex (0x12-0x14) but code uses decimal (18-20) - clarify or use hex literals | Closed | 2026-01-27 | 2026-01-27 |
| W-12-002 | Low | Datamodel | `aeth.ksy` section reference inconsistency: reference both Section 9.4 (header format) and Section 9.7.5.1 (ACK semantics) | Closed | 2026-01-27 | 2026-01-27 |
| W-12-003 | Medium | Datamodel | `deth.ksy` uses full opcodes (0x64, 0x65) while other files use operation codes - standardize format | Closed | 2026-01-27 | 2026-01-27 |
| W-12-004 | Low | Datamodel | `reth.ksy` missing opcodes in x-related-headers for bth.ksy reference | Closed | 2026-01-27 | 2026-01-27 |
| W-12-005 | Low | Documentation | `roce/README.md` missing CNP (4) and XRC (5) transport types - added with TBD status, see W-12-012 | Closed | 2026-01-27 | 2026-01-27 |
| W-12-012 | Medium | Datamodel | PMR transport type support: CNP=Yes (ECN congestion control), XRC=No (no shared receive queues). Updated README.md and bth.ksy. | Closed | 2026-01-27 | 2026-01-28 |
| W-12-006 | Low | Datamodel | `aeth.ksy` rnr_timeout_values enum - CANCELLED: field is 5 bits [4:0] so 0-31 is complete range, no reserved values | Cancelled | 2026-01-27 | 2026-01-27 |
| W-12-007 | Low | Datamodel | `qp_state_machine.ksy` x-spec nested in meta block - move to root level for consistency | Closed | 2026-01-27 | 2026-01-27 |
| W-12-008 | Medium | Datamodel | Missing XRCETH header - CLOSED: PMR does not support XRC, XRCETH not required | Closed | 2026-01-27 | 2026-01-28 |
| W-12-009 | Low | Datamodel | Extended atomics (MASKED_CMP_SWAP 0x15, MASKED_FETCH_ADD 0x16) NOT supported over RoCE - implemented over UE/UE+ instead. Standard atomics (CMP_SWAP, FETCH_ADD) supported. | Closed | 2026-01-27 | 2026-01-28 |
| W-12-010 | Low | Datamodel | `icrc.ksy` ICRC masking details incomplete for RoCEv2 - add specific byte offsets per Annex A17 | Closed | 2026-01-27 | 2026-01-27 |
| W-12-011 | High | Datamodel | `aeth.ksy` syndrome bit layout WRONG per IB Spec v1.4: bit 7 reserved, bits [6:5]=ACK type (not [7:6]), bits [4:0]=value (not [5:0]); revert mask to 0x1f, fix ack_type shift to >>5. W-11-006 was incorrect. | Closed | 2026-01-27 | 2026-01-27 |
| W-12-013 | Low | Datamodel | `aeth.ksy` missing opcodes [0x0D-0x12] in x-related-headers for bth.ksy reference (RDMA_READ_RESPONSE_*, ACKNOWLEDGE, ATOMIC_ACKNOWLEDGE) | Closed | 2026-01-28 | 2026-01-28 |
| W-12-014 | Low | Datamodel | `immdt.ksy` missing opcodes [0x03, 0x05, 0x09, 0x0B] in x-related-headers for bth.ksy reference (SEND_LAST_IMM, SEND_ONLY_IMM, RDMA_WRITE_LAST_IMM, RDMA_WRITE_ONLY_IMM) | Closed | 2026-01-28 | 2026-01-28 |
| W-12-015 | Low | Datamodel | `atomiceth.ksy` missing opcodes [0x13, 0x14] in x-related-headers for bth.ksy reference (CMP_SWAP, FETCH_ADD) | Closed | 2026-01-28 | 2026-01-28 |
| W-12-016 | Low | Datamodel | `atomicacketh.ksy` missing opcodes [0x12] in x-related-headers for bth.ksy reference (ATOMIC_ACKNOWLEDGE) | Closed | 2026-01-28 | 2026-01-28 |
| W-12-017 | Low | Datamodel | `deth.ksy` missing opcodes [0x04, 0x05] in x-related-headers for bth.ksy reference (SEND_ONLY, SEND_ONLY_IMM for UD transport) | Closed | 2026-01-28 | 2026-01-28 |
| W-12-018 | Low | Documentation | `roce/README.md` missing protocols/ directory in file list (contains qp_state_machine.ksy) | Closed | 2026-01-28 | 2026-01-28 |
| W-13-001 | Medium | Datamodel | Ethernet: All 6 .ksy files missing x-related-headers cross-references | Closed | 2026-01-28 | 2026-01-28 |
| W-13-002 | Low | Datamodel | Ethernet: All 6 .ksy files missing x-spec metadata for specification traceability | Closed | 2026-01-28 | 2026-01-28 |
| W-13-003 | Low | Datamodel | Ethernet: All 6 .ksy files missing x-packet metadata for layer/category/constraints | Closed | 2026-01-28 | 2026-01-28 |
| W-13-004 | Medium | Datamodel | `ethernet_ii.ksy` max frame size 9216 - NOT A CONFLICT: hardware max (10240) >= protocol max (9216) is correct; protocols may have smaller limits than hardware supports | Closed | 2026-01-28 | 2026-01-28 |
| W-13-005 | Low | Datamodel | `vlan_802_1q.ksy` header_size documentation confusing (4 bytes tag vs 6 bytes parsed) | Closed | 2026-01-28 | 2026-01-28 |
| W-13-006 | Low | Documentation | `ethernet/README.md` outdated placeholder status, missing file list | Closed | 2026-01-28 | 2026-01-28 |
| W-13-007 | Low | Datamodel | `udp.ksy` is_roce instance missing cross-reference to roce/transport/bth.ksy | Closed | 2026-01-28 | 2026-01-28 |
| W-13-008 | Low | Datamodel | `ipv6.ksy` missing dst_addr_hash instance for RSS hash symmetry with src_addr_hash | Closed | 2026-01-28 | 2026-01-28 |
| W-13-009 | Low | Datamodel | `tcp.ksy` reserved bits (3 bits) not extracted as instance for validation | Closed | 2026-01-28 | 2026-01-28 |
| W-13-010 | Medium | Datamodel | IEEE 802.3 frame format support: Created ethernet_802_3.ksy, llc.ksy, snap.ksy. Updated ethernet_ii.ksy and vlan_802_1q.ksy with cross-references. | Closed | 2026-01-28 | 2026-01-28 |
| W-13-011 | Medium | Datamodel | RSS hash algorithm documentation: Created rss/ directory with hash_algorithm.ksy, toeplitz_key.ksy, hash_input.ksy, README.md. Updated ipv4.ksy and ipv6.ksy with RSS cross-references. | Closed | 2026-01-28 | 2026-01-28 |
| W-13-012 | Low | Datamodel | `ethernet_ii.ksy` VLAN cross-reference description clarified to explain inner ether_type relationship | Closed | 2026-01-28 | 2026-01-28 |
| W-13-013 | Low | Datamodel | `ipv4.ksy` added VLAN cross-reference (can be encapsulated in VLAN-tagged frames) | Closed | 2026-01-28 | 2026-01-28 |
| W-13-014 | Low | Datamodel | `ipv6.ksy` added VLAN cross-reference (can be encapsulated in VLAN-tagged frames) | Closed | 2026-01-28 | 2026-01-28 |
| W-13-015 | Low | Datamodel | `tcp.ksy` added RSS cross-reference (TCP ports used in L3+L4 hash) | Closed | 2026-01-28 | 2026-01-28 |
| W-13-016 | Low | Datamodel | `udp.ksy` added RSS cross-reference (UDP ports used in L3+L4 hash) | Closed | 2026-01-28 | 2026-01-28 |
| W-13-017 | Low | Datamodel | `ipv6.ksy` fixed stale W-13-011 reference - now references rss/ directory | Closed | 2026-01-28 | 2026-01-28 |
| W-13-018 | Low | Documentation | `ethernet/README.md` protocol stack updated "vlan.ksy" to "VLAN (802.1Q)" | Closed | 2026-01-28 | 2026-01-28 |
| W-13-019 | Low | Datamodel | `tcp.ksy` and `udp.ksy` rss_hash_input_l4 doc updated to match ipv4/ipv6 RSS documentation style | Closed | 2026-01-28 | 2026-01-28 |
| W-13-020 | Medium | Datamodel | `hash_algorithm.ksy` enum reference syntax (algorithm::crc32) verified with validate_ksy.py script | Closed | 2026-01-28 | 2026-01-28 |
| W-13-021 | Medium | Datamodel | `toeplitz_key.ksy` type casting syntax (.as<u4>) verified with validate_ksy.py script | Closed | 2026-01-28 | 2026-01-28 |
| W-14-001 | High | Datamodel | UALink: `dl_flit.yaml` segment sizes don't include headers (128 vs 129 bytes); unexplained 5-byte padding. Fix to match authoritative `dl_flit.ksy`. See `analysis/ualink/ualink_issues.md` UAL-001. | Closed | 2026-01-29 | 2026-01-29 |
| W-14-002 | Medium | Datamodel | UALink: Packet count mismatch - `metadata.yaml` shows 35 packets, `packet_types.yaml` shows 38. Update `metadata.yaml` to 38. See `analysis/ualink/ualink_issues.md` UAL-002. | Closed | 2026-01-29 | 2026-01-29 |
| W-14-003 | Medium | Datamodel | UALink: YAML reference files missing `ksy_file` cross-references. Add to all files in `reference/field_definitions/*.yaml`. See `analysis/ualink/ualink_issues.md` UAL-003. | Closed | 2026-01-29 | 2026-01-29 |
| W-14-004 | Low | Datamodel | UALink: Security layer files sparse (30-45 lines) compared to other layers (100-300+ lines). Expand with Tables 9-1 through 9-7 details. See `analysis/ualink/ualink_issues.md` UAL-004. | Closed | 2026-01-29 | 2026-01-29 |
| W-14-005 | Low | Documentation | UALink: Verify spec_date values against official UALink Consortium release dates. See `analysis/ualink/ualink_issues.md` UAL-005. | Closed | 2026-01-29 | 2026-01-30 |
| W-14-006 | Medium | Review | UALink: Security layer expansion verified against UALink200 Spec Section 9. All 5 files (1660 lines) pass verification: encryption.ksy (Tables 9-4-9-7), authentication.ksy (Tables 9-8-9-12), iv_format.ksy (Table 9-3), key_derivation.ksy (Figure 9-8), key_rotation.ksy (Figures 9-9, 9-11, 9-12). No corrections required. See `analysis/ualink/ualink_issues.md` UAL-006. | Closed | 2026-01-29 | 2026-01-30 |
| W-14-007 | Medium | Datamodel | UALink: KSY files missing `x-related-headers` cross-references. Added sections to 37 KSY files across all 5 layers (UPLI 7, Transaction 9, Datalink 12, Physical 4, Security 5) with relationship vocabulary (contains, references, uses, part-of). See `analysis/ualink/ualink_issues.md` UAL-007. | Closed | 2026-01-30 | 2026-01-30 |
| W-14-008 | Low | Datamodel | UALink: `data_half_flit.ksy` and `message_half_flit.ksy` expanded to exemplar quality. data_half_flit: 40→142 lines (poison, byte enable, data beat). message_half_flit: 37→148 lines (Tables 5-3, 5-4, Section 5.1.2). See `analysis/ualink/ualink_issues.md` UAL-008. | Closed | 2026-01-30 | 2026-01-30 |
| W-14-009 | Low | Documentation | UALink: `response_field.ksy` expanded from 52 to 310 lines with full bit-level parsing for Tables 5-30, 5-34, 5-35, 5-36, 5-37. Created response_field.yaml. See `analysis/ualink/ualink_issues.md` UAL-009. | Closed | 2026-01-30 | 2026-01-30 |
| W-14-010 | Low | Datamodel | UALink: `flit_header.ksy` expanded from 90 to 165 lines with top-level seq and instances for header type discrimination. See `analysis/ualink/ualink_issues.md` UAL-010. | Closed | 2026-01-30 | 2026-01-30 |
| W-14-011 | Low | Documentation | UALink: Documented YAML reference coverage criteria in README.md. 4 criteria: entry point, multi-variant, cross-layer, high-complexity. 6 YAML files exist by design; remaining 32 KSY files are self-documenting. See `analysis/ualink/ualink_issues.md` UAL-011. | Closed | 2026-01-30 | 2026-01-30 |

### 5.2 Datamodel Gaps

| ID | Priority | Description | Target Location | Status | Opened | Closed |
|----|----------|-------------|-----------------|--------|--------|--------|
| D-001 | High | PMR CSR definitions missing from datamodel | `datamodel/hw/asics/pmr/csrs/*.rdl` | Spec Update | 2026-01-10 | - |
| D-002 | Medium | PMR block hierarchy YAML incomplete | `datamodel/hw/asics/pmr/blocks.yaml` | Spec Update | 2026-01-10 | - |
| D-003 | Medium | PMR interface contracts missing | `datamodel/views/contracts/pmr-*.puml` | Spec Update | 2026-01-10 | - |

### 5.3 Specification Clarifications Needed

| ID | Priority | Question | Context | Status | Opened | Closed |
|----|----------|----------|---------|--------|--------|--------|
| Q1 | Medium | Lightweight Interface Scope | What features should be reduced in lightweight mode? | Investigation | 2026-01-10 | - |
| Q2 | Medium | Tag Table Sizing | Should HW tag table size be per-endpoint configurable? | Investigation | 2026-01-10 | - |
| Q3 | Medium | Multi-Packet Eager Messages | Should hardware support multi-packet eager messages? | Investigation | 2026-01-10 | - |
| Q4 | Low | RoCE Work Queue Implementation | Confirm RoCE WQ/CQ are software-implemented | Investigation | 2026-01-10 | - |

### 5.4 Closed Issues

| ID | Priority | Category | Description | Resolution | Opened | Closed |
|----|----------|----------|-------------|------------|--------|--------|
| W-05-001 | Medium | Documentation | UE taxonomy reference | Documented in `05-packet-formats.md` | 2026-01-08 | 2026-01-10 |
| W-02-005 | Medium | Documentation | Protocol support documentation | Documented UE+, RoCEv2, Ethernet | 2026-01-08 | 2026-01-10 |
| W-02-006 | Medium | Documentation | Cornelis Collective Reduction Protocol | Documented in HAS 2.5.4 | 2026-01-08 | 2026-01-10 |
| W-03-001 | Medium | Architecture | Semantic Engine count | Confirmed 64 (8x8) in UML and HAS | 2026-01-08 | 2026-01-10 |
| W-17-005 | Low | Documentation | Port subdivision note | Added to HAS Ch17 | 2026-01-11 | 2026-01-11 |
| W-17-006 | Medium | Documentation | MPORT interface documentation | Documented 256B @ 1.66 GHz | 2026-01-11 | 2026-01-11 |
| W-04-005 | High | Datamodel | `ufh_16.ksy` address size: Datamodel shows 12-bit dest, should be 16-bit | UFH-16 restructured to 12-byte Ethernet MAC overlay with 16-bit destination (bytes 4-5) and 16-bit source (bytes 10-11) | 2026-01-10 | 2026-01-20 |
| W-04-006 | High | Datamodel | `ufh_32.ksy` address size: Datamodel shows 16-bit dest, should be 32-bit | UFH-32 restructured to 12-byte Ethernet MAC overlay with 32-bit destination (bytes 2-5) and 32-bit source (bytes 8-11) | 2026-01-10 | 2026-01-20 |
| W-07-001 | Low | Datamodel | `ack_cc.ksy` shows `ack_cc_state` as 32-bit (4 bytes) but UE Spec Table 3-36 shows 64-bit (8 bytes) | Updated `ack_cc.ksy` to use 64-bit (u8) for ack_cc_state; total size now 32 bytes | 2026-01-22 | 2026-01-23 |
| W-09-001 | - | Datamodel | Create UE L2 header | NOT NEEDED: UE uses standard Ethernet II; no custom L2 header defined in UE Spec | 2026-01-23 | 2026-01-26 |
| W-09-002 | - | Datamodel | Create FEP address format | NOT NEEDED: FEP uses standard IPv4/IPv6 addresses (FA = Fabric Address) | 2026-01-23 | 2026-01-26 |
| W-09-003 | Medium | Datamodel | Document PDCID format and pdc_info encoding | Added PDCID format documentation to rud_rod_request.ksy and packet_taxonomy_ue_pds.md; pdc_info encoding: use_rsv_pdc(1), rsvd(3) per Table 3-33 | 2026-01-23 | 2026-01-26 |
| W-09-004 | - | Datamodel | Create UET network header | NOT NEEDED: UE uses standard IP headers; no custom network header defined | 2026-01-23 | 2026-01-26 |
| W-09-005 | Medium | Datamodel | Create CP payload formats per Section 3.5.16.8 | Existing credit_cp_payload.ksy and credit_request_cp_payload.ksy sufficient; other CP payloads documented inline in rud_rod_cp.ksy | 2026-01-23 | 2026-01-26 |
| W-09-006 | Medium | Datamodel | Update rud_rod_cp.ksy with payload field | Added payload field with CP type table (Table 3-66), x-payload-by-type metadata, "Same as ACK" note, corrected path references | 2026-01-23 | 2026-01-26 |
| W-09-007 | Low | Datamodel | Create nack_codes.ksy enumeration per Table 3-59 | Created `ue/transport/pds/nack_codes.ksy` with all NACK codes (0x01-0x1A, 0xFD-0xFF), error types (NORMAL, PDC_ERR, PDC_FATAL), and source actions (RETX, RETRY, FAIL) | 2026-01-23 | 2026-01-26 |
| W-09-008 | Low | Datamodel | Create next_header_types.ksy enumeration per Table 3-16 | Created `ue/transport/ses/next_header_types.ksy` with all next_hdr values (0x0-0x6 defined, 0x7-0xF reserved), figure references, and ksy file mappings | 2026-01-23 | 2026-01-26 |
| W-04-004 | High | Datamodel | UE+ header restructuring: 24-bit HMAC, correct field layout | Complete rewrite of `ue_plus.ksy`: 24-bit DLID/DMAC and SLID/SMAC, L2=2/V=2/zyxm=4/Length=6/RC=3/SC=4/Hop=3/Reserved=8, removed Type field, added HMAC sub-structure for 3 topologies, updated HAS docs | 2026-01-10 | 2026-01-26 |
| W-05-002 | Medium | Specification | MTU values verification | Hardware max=10240, UE+ typical=8192, RoCEv2 max=4096. Updated HAS docs and datamodel files (eth_tx_wqe.ksy, ec/descriptors.ksy, pcie/descriptors.ksy) | 2026-01-10 | 2026-01-26 |
| W-05-003 | Medium | Documentation | CMS detailed formats documentation | Option 3 (datamodel-focused) implemented: documented 8 CMS protocol .ksy files (CCC state machine, NSCC source/dest, RCCC source/dest, TFC source/dest, multipath selection). Created plan file at `analysis/ue_cms/CMS_DOCUMENTATION_PLAN.md`. | 2026-01-10 | 2026-01-26 |
| W-07-002 | Low | Documentation | `collective_l2.ksy` and `scaleup_l2.ksy` marked WIP | Superseded by W-08-001 and W-08-002 which track each file separately | 2026-01-22 | 2026-01-27 |
| W-10-001 | Low | Datamodel | Create `cc_type.ksy` enumeration per Table 3-48 | Created `ue/transport/cms/cc_type.ksy` with CC_NSCC (0), CC_CREDIT (1), reserved (2-13), proprietary (14-15) | 2026-01-27 | 2026-01-27 |
| W-10-002 | Low | Datamodel | Create `ccx_type.ksy` enumeration per Table 3-49 | Created `ue/transport/cms/ccx_type.ksy` with all reserved values (0-13 future, 14-15 proprietary) | 2026-01-27 | 2026-01-27 |
| W-10-003 | Low | Datamodel | Add preprocessing algorithm references to CMS .ksy files | Added Section 3.6.10.3 to ack_cc_state_nscc.ksy, Section 3.6.10.4 to ack_cc_state_rccc_tfc.ksy, Figure 3-99 to req_cc_state.ksy | 2026-01-27 | 2026-01-27 |
| W-10-004 | Low | Datamodel | Add Credit CP protocol constraints to credit_cp_payload.ksy | Added pds.psn=0x0, pds.flags.ar=0 constraints, Sections 3.6.14.6 and 3.6.15.2 references | 2026-01-27 | 2026-01-27 |
| W-10-005 | Low | Datamodel | Add API function references to ccc_state_machine.ksy | Added Section 3.6.8.1 abstract PDS-CMS API: lifecycle (AllocateCCC, DeallocateCCC), events (OnACK, OnNACK, OnInferredLoss, OnNewData, OnCreditUpdate, OnSend), queries (GetSendParams, GetEagerEstimate) | 2026-01-27 | 2026-01-27 |
| W-11-005 | Medium | Datamodel | Add operation validity matrix by transport type to `bth.ksy` | Added IB Spec Table 38 operation validity matrix to doc block; added `is_valid_for_rc/uc/rd/ud/xrc`, `is_valid_operation`, and `invalid_operation_reason` instances | 2026-01-27 | 2026-01-27 |
| W-11-006 | Low | Datamodel | Fix `aeth.ksy` syndrome mask from 0x1f to 0x3f | Updated `credit_count`, `rnr_timeout`, `nak_code` instances to use 0x3f mask (6 bits per IB Spec); updated syndrome field documentation | 2026-01-27 | 2026-01-27 |
| W-11-007 | Low | Datamodel | Add `x-related-headers` cross-references to RoCE files | Added cross-references to all 9 RoCE files: bth, reth, aeth, deth, immdt, atomiceth, atomicacketh, icrc, qp_state_machine | 2026-01-27 | 2026-01-27 |
| W-11-008 | Low | Datamodel | Add `x-spec` and `x-packet` metadata to RoCE transport files | Added IB Spec 1.4 traceability metadata to all 8 transport files with section/table references, constraints, and usage notes | 2026-01-27 | 2026-01-27 |

### 5.5 Change Log

| Date | Change | Details |
|------|--------|---------|
| 2026-01-14 | Initial creation | Document created with PMR packet taxonomy |
| 2026-01-20 | Review and update | Added UALink section (reference only, not PMR-supported); Added change log; Updated datamodel file counts; No new .ksy files since initial creation |
| 2026-01-20 | UFH format details | Added detailed UFH-16 and UFH-32 format documentation in Section 6.2 (wire diagrams, field tables, type enumerations) |
| 2026-01-20 | UFH restructuring | UFH-16 and UFH-32 restructured to 12-byte Ethernet MAC overlays; UFH-16 now 16-bit addressing, UFH-32 now 32-bit addressing; Added SLAP field constraints (Z,Y,X=001); Updated datamodel .ksy files; Closed W-04-005 and W-04-006 |
| 2026-01-22 | Datamodel review | Added W-07-001 (ack_cc_state size mismatch), W-07-002 (collective/scaleup specs incomplete), W-07-003 (ue_plus length encoding); Identified 30+ packet formats requiring expansion |
| 2026-01-22 | Phase 1 expansion | Expanded PDS formats (3.3.1-3.3.11): RUD, ROD, RUDI, UUD, ACK, ACK_CC, ACK_CCX, NACK, NACK_CCX, Control Packet with wire diagrams, field tables, protocol behavior, and cross-references. Expanded SES formats (3.5.1-3.5.7): Standard Request SOM=1/SOM=0, Response, Response with Data, Small Message, Rendezvous Extension, Atomic Extension. Added request/response relationship diagrams. Total ~1200 lines added. |
| 2026-01-23 | Phase 2 document split | Restructured monolithic document into sub-documents: packet_taxonomy_ue_pds.md (PDS formats), packet_taxonomy_ue_ses.md (SES formats), packet_taxonomy_ue_cms_tss.md (CMS/TSS formats), packet_taxonomy_ue_link.md (Link Layer formats), packet_taxonomy_rocev2.md (RoCEv2 formats), packet_taxonomy_cornelis.md (Cornelis proprietary), packet_taxonomy_hsi.md (HSI formats), packet_taxonomy_ualink.md (UALink reference). Master document converted to index with quick reference tables. Added W-08-001 and W-08-002 for WIP specs. |
| [packet_taxonomy_ue_tagged_send_variants.md](packet_taxonomy_ue_tagged_send_variants.md) | Tagged-Send Variants | UE Standard, CSIG, IPv4, TSS, Small, Rendezvous, Deferrable | `ue/transport/` |
| 2026-01-23 | Phase 3 gap closure | Documented 27 previously missing formats: PDS (entropy_header, rud_rod_default_ses, rud_rod_request_cc), SES (cas_extension, deferrable_send_request, optimized_non_matching, optimized_response_with_data, ready_to_restart, small_rma), UE Network (dscp_categories, packet_trimming), UE Physical (control_ordered_sets), RoCEv2 (atomicacketh, deth, immdt, icrc), Cornelis (cornelis_l2_prefix, pkey), Standard Ethernet (ethernet_ii, vlan_802_1q, ipv4, ipv6, tcp, udp), HSI (notification_entry, qw_violation_event, pcie/descriptors). Created new packet_taxonomy_ethernet.md sub-document. |
| 2026-01-23 | Datamodel gap analysis | Identified missing UE Spec formats not in datamodel: UET L2 Header (Table 3-1), FEP Address (Table 3-4), PDCID (Table 3-5), UET Network Header (Table 3-3), CP payloads (Section 3.5.16.8), enumerations (Tables 3-16, 3-59). Created DATAMODEL_UPDATE_PLAN.md with 9 new work items (W-09-001 through W-09-009). Clarified: standard UE L2 goes in ue/link/, Cornelis UE+ is value-add variant, PMR L2 selection rules TBD. |
| 2026-01-26 | Plan revision after UE Spec review | Closed W-09-001, W-09-002, W-09-004 as NOT NEEDED after detailed UE Spec review: UE uses standard Ethernet II (no custom L2 header), FEP uses standard IPv4/IPv6 (no custom address format), UE uses standard IP headers (no custom network header). Table 3-1 is "Profile Requirements", not L2 header. Table 3-4 is "SES header formats", not FEP address. Cornelis UE+ is proprietary value-add, not UE standard. Added W-09-010 for future UFH headers (deferred). Updated DATAMODEL_UPDATE_PLAN.md with revised scope. |
| 2026-01-26 | Phase 2 datamodel updates | Closed W-09-003 (PDCID format in rud_rod_request.ksy), W-09-005 (CP payloads - existing files sufficient), W-09-006 (rud_rod_cp.ksy payload field). Commits: 319c0565 (rud_rod_request.ksy), 3cc80cc4 (rud_rod_cp.ksy). |
| 2026-01-26 | Phase 3 enumeration files | Created `nack_codes.ksy` (W-09-007) with all PDS NACK codes per Table 3-59 including error types and source actions. Created `next_header_types.ksy` (W-09-008) with SES next header enumeration per Table 3-16 including figure references and ksy file mappings. |
| 2026-01-26 | UE+ header restructuring | Complete rewrite of `ue_plus.ksy` (W-04-004): 24-bit HMAC addresses (DLID/DMAC, SLID/SMAC), correct field layout (L2=2, V=2, zyxm=4, Length=6, RC=3 split, SC=4, Hop=3, Reserved=8), removed Type field (next header follows UE+ header), added HMAC sub-structure documentation for 3 topologies (no subdivision 12/6/6, x2 NIC 11/6/7, x8 NIC 9/6/9), updated HAS 04-addressing.md and 05-packet-formats.md. W-07-003 updated to track Length field units (now 6 bits). |
| 2026-01-26 | MTU values update | Closed W-05-002: Updated MTU documentation with correct values. Hardware max=10240 bytes, UE+ typical=8192 bytes, RoCEv2 max=4096 bytes. Added UE Payload MTU vs UE+ packet size distinction, header overhead relationship, RoCEv2 MTU derivation rules. Updated HAS 03-architecture.md and 05-packet-formats.md. Updated datamodel files: eth_tx_wqe.ksy, ec/descriptors.ksy, pcie/descriptors.ksy (9216→10240). |
| 2026-01-26 | CMS documentation | Closed W-05-003: Implemented Option 3 (datamodel-focused) from CMS documentation plan. Added sections 2.4-2.8 to packet_taxonomy_ue_cms_tss.md documenting 8 CMS protocol .ksy files: CCC state machine, NSCC source/destination, RCCC source/destination, TFC source/destination, multipath selection. Created plan file at `analysis/ue_cms/CMS_DOCUMENTATION_PLAN.md`. |
| 2026-01-27 | Work item cleanup | Closed W-07-002 (superseded by W-08-001 and W-08-002 which track collective_l2.ksy and scaleup_l2.ksy separately). Updated W-03-002 and W-03-006 to note they are tracked in `earlysim/docs/HAS/PMR/WORK.md`. |
| 2026-01-27 | CMS datamodel review | Reviewed 5 CMS .ksy files against UE Spec 1.0.1. All field sizes and layouts verified accurate. Created `cc_type.ksy` (W-10-001, Table 3-48) and `ccx_type.ksy` (W-10-002, Table 3-49) enumeration files. Added preprocessing algorithm references (W-10-003) to ack_cc_state_nscc.ksy (Section 3.6.10.3) and ack_cc_state_rccc_tfc.ksy (Section 3.6.10.4). Added protocol constraints (W-10-004) to credit_cp_payload.ksy (pds.psn=0x0, pds.flags.ar=0). |
| 2026-01-27 | CMS protocols review | Reviewed 8 CMS protocol .ksy files in `cms/protocols/`. `ccc_state_machine.ksy` is HIGH QUALITY with accurate state machine from Figure 3-98. Other 7 files are STUBS needing expansion: nscc_source (W-10-006), nscc_destination (W-10-007), rccc_source (W-10-008), rccc_destination (W-10-009), tfc_source (W-10-010), tfc_destination (W-10-011), multipath_selection (W-10-012). Added W-10-005 for ccc_state_machine API references. Stub items deferred. |
| 2026-01-27 | CCC state machine API | Closed W-10-005: Added abstract PDS-CMS API (Section 3.6.8.1) to `ccc_state_machine.ksy`. Documented 8 API functions: lifecycle (AllocateCCC, DeallocateCCC), events (OnACK, OnNACK, OnInferredLoss, OnNewData, OnCreditUpdate, OnSend), queries (GetSendParams, GetEagerEstimate). Added doc-ref and updated doc block. Commit: 6043d306, pushed to origin/main. |
| 2026-01-27 | CC_CREDIT size fix | Closed W-10-014: Fixed `ack_cc_state_rccc_tfc.ksy` from 5 bytes to 8 bytes (64 bits) to match ACK_CC pds.ack_cc_state field size. Added 24-bit reserved field (Bytes 3-5) between credit and ooo_count. Updated `cc_type.ksy` CC_CREDIT documentation and size reference. Table 3-75 defines 40 bits but pds.ack_cc_state is always 64 bits. Commit: 2b3916ca, pushed to origin/main. |
| 2026-01-27 | NSCC source expansion | Closed W-10-006: Expanded `nscc_source.ksy` from 53-line stub to ~580-line comprehensive algorithm documentation. Removed incorrect TCP-style state machine. Added: 20 configuration parameters (Table 3-76), 16 state variables (Table 3-77), 6 algorithm functions (OnACK, OnNACK, OnInferredLoss, OnSend, CanSend, AckRequest), 11 internal functions (calculate_rtt, fulfill_adjustment, fair_increase, proportional_increase, multiplicative_decrease, quick_adapt, fast_increase, update_base_rtt, apply_cwnd_penalty, update_delay, get_avg_delay), ECN/delay decision matrix, pseudocode. Created W-10-015 for follow-on review. |
| 2026-01-27 | BTH datamodel updates | Closed W-11-001 through W-11-004: Enhanced `bth.ksy` with comprehensive RoCEv2 transport type and congestion control documentation. W-11-001: Updated `is_atomic` docs with operation codes 0x12-0x14 and transport type restrictions (RC/RD/XRC only). W-11-002: Added `is_ack` (0x11) and `is_atomic_ack` (0x12) instances with IB Spec references. W-11-003: Added CNP (4, 0x80) and XRC (5, 0xA0) transport types to enum and all opcode documentation. W-11-004: Documented FECN (bit 7) and BECN (bit 6) in reserved field with ICRC masking note; added `fecn` and `becn` instances. File grew from 197 to 305 lines. |
| 2026-01-27 | RoCE datamodel enhancements | Closed W-11-005, W-11-007, W-11-008: Comprehensive RoCE datamodel improvements. W-11-005: Added operation validity matrix (IB Spec Table 38) to `bth.ksy` doc block with `is_valid_operation` and `invalid_operation_reason` instances. W-11-006: Initially changed mask to 0x3f but this was INCORRECT - see later fix. W-11-007: Added `x-related-headers` cross-references to all 9 RoCE files (8 transport + qp_state_machine). W-11-008: Added `x-spec` and `x-packet` metadata blocks to all 8 RoCE transport files with IB Spec 1.4 references. Created W-11-009 for IB Spec Release 2.0 review (announced Nov 2025). |
| 2026-01-27 | RoCE datamodel review | Comprehensive review of all 9 RoCE .ksy files. Identified 10 issues (R-001 through R-010) documented in `analysis/roce_protocols/RoCE_protocols_issues.md`. Created work items W-12-001 through W-12-010. Key findings: opcode format inconsistencies (full vs operation codes), missing XRCETH header for XRC transport, extended atomics not documented, ICRC masking details incomplete. Two items require investigation (W-12-008 XRC support, W-12-009 extended atomics). |
| 2026-01-27 | AETH syndrome fix | Closed W-11-006, W-12-001, W-12-002, W-12-011. Critical fix to `aeth.ksy` syndrome field per IB Spec Vol 1 v1.4: bit 7 reserved (must be 0), bits [6:5] = ACK type, bits [4:0] = value. Reverted mask from 0x3f to 0x1f, fixed ack_type shift from >>6 to >>5. Added `reserved_bit` and `is_unlimited_credits` instances. Updated x-spec to reference both Section 9.4 (format) and Section 9.7.5.1 (semantics). Fixed `bth.ksy` `is_atomic` to use hex literals (0x12-0x14) with decimal equivalents in doc. Commit: 53ad6809, pushed to origin/main. |
| 2026-01-27 | README CNP/XRC update | Closed W-12-005: Added CNP (4) and XRC (5) transport types to `roce/README.md` with PMR Support column showing TBD status. Created W-12-012 to track decision on CNP/XRC support. Commit: c2b130f7, pushed to origin/main. |
| 2026-01-27 | QP state machine x-spec | Closed W-12-007: Moved `x-spec` from nested inside `x-related-headers` to root level in `qp_state_machine.ksy` for consistency with transport files. Expanded metadata format. Commit: bec54ad5, pushed to origin/main. |
| 2026-01-27 | DETH opcode format | Closed W-12-003: Standardized `deth.ksy` from full opcodes (0x64, 0x65) to operation codes (0x04, 0x05) for consistency with other RoCE files. Added transport_type field and updated doc to show both formats. Commit: 5837af2b, pushed to origin/main. |
| 2026-01-27 | RETH opcodes | Closed W-12-004: Added opcodes [0x06, 0x0A, 0x0B, 0x0C] to `reth.ksy` x-related-headers for bth.ksy reference. Commit: 0065a1e8, pushed to origin/main. |
| 2026-01-27 | ICRC masking details | Closed W-12-010: Added detailed ICRC masking byte offsets to `icrc.ksy` verified against Linux kernel rxe_icrc.c. Documented IPv4/IPv6/UDP/BTH field masks, calculation algorithm, and added masking constant instances. Commit: 35f74447, pushed to origin/main. |
| 2026-01-28 | RoCE x-related-headers opcodes | Closed W-12-013 through W-12-018: Added missing opcodes to x-related-headers for bth.ksy reference in all RoCE transport files. W-12-013: aeth.ksy [0x0D-0x12] (5edecc5c). W-12-014: immdt.ksy [0x03,0x05,0x09,0x0B] (8d0e31cc). W-12-015: atomiceth.ksy [0x13,0x14] (ebe482ec). W-12-016: atomicacketh.ksy [0x12] (ef187ab8). W-12-017: deth.ksy [0x04,0x05] (fb9c7d46). W-12-018: README.md protocols/ directory (86b901b7). All pushed to origin/main. |
| 2026-01-28 | Ethernet datamodel review | Created W-13-001 through W-13-010 for Ethernet datamodel issues. Key findings: missing x-related-headers cross-references (all files), missing x-spec/x-packet metadata, ethernet_ii.ksy max frame size conflict (9216 vs PMR 10240), vlan_802_1q.ksy header size confusion, README.md outdated, udp.ksy missing RoCE cross-ref, ipv6.ksy missing dst_addr_hash, tcp.ksy reserved bits not extracted, IEEE 802.3 format not implemented. Issues documented in `analysis/ethernet_protocols/ethernet_protocols_issues.md`. |
| 2026-01-28 | Ethernet datamodel updates | Closed W-13-001 through W-13-004. W-13-001: Added x-related-headers to all 6 ethernet .ksy files (5163deec). W-13-002: Added x-spec metadata with IEEE/RFC references (ac03b79e). W-13-003: Added x-packet metadata with layer/size/constraints/usage (ba8829c9). W-13-004: Closed as not an issue - hardware max (10240) >= protocol max (9216) is correct. All pushed to origin/main. |
| 2026-01-28 | VLAN header size clarification | Closed W-13-005: Clarified vlan_802_1q.ksy header size confusion. Renamed header_size→vlan_tag_size (4 bytes), full_header_size→total_parsed_size (6 bytes). Added doc explaining VLAN tag is 4 bytes but file parses 6 bytes including inner EtherType for convenience. Commit: 0d94d0b7, pushed to origin/main. |
| 2026-01-28 | UDP RoCE cross-reference | Closed W-13-007: Updated udp.ksy is_roce instance doc to reference x-related-headers cross-reference to roce/transport/bth.ksy. Added note about IANA port 4791 and BTH payload. Commit: 71777456, pushed to origin/main. |
| 2026-01-28 | TCP reserved bits | Closed W-13-009: Added reserved bits extraction (bits 11-9) and is_valid_reserved validation instance to tcp.ksy. Reserved bits must be zero per RFC 793. Commit: b9e51104, pushed to origin/main. |
| 2026-01-28 | IPv6 RSS hash instances | Closed W-13-008: Added dst_addr_hash and rss_hash_input_l3 instances to ipv6.ksy for RSS hash symmetry. Added note referencing W-13-011 for Toeplitz hash discussion. Commit: c4d9ad6e, pushed to origin/main. |
| 2026-01-28 | Ethernet README update | Closed W-13-006: Updated ethernet/README.md - removed placeholder status, added protocol stack diagram, file tables with sizes/descriptions, updated references. Added TBD note for IEEE 802.3 LLC/SNAP support (W-13-010). Commit: 9939fa29, pushed to origin/main. |
| 2026-01-28 | RSS hash documentation | Closed W-13-011: Created new rss/ directory with comprehensive RSS hash documentation. Files: hash_algorithm.ksy (algorithm selection: CRC32, XOR, Toeplitz), toeplitz_key.ksy (40-byte key format with CSR mapping), hash_input.ksy (IPv4/IPv6 L3/L4 tuple formats), README.md (overview with CSR references). Updated ipv4.ksy and ipv6.ksy with RSS cross-references and improved rss_hash_input_l3 documentation. Commit: f18cc8a5, pushed to origin/main. |
| 2026-01-28 | Ethernet second review | Second review of Ethernet datamodel after initial fixes. Created W-13-012 through W-13-021 for 10 additional issues: missing VLAN cross-references in ipv4/ipv6 (E-013, E-014), missing RSS cross-references in tcp/udp (E-015, E-016), stale W-13-011 comment reference (E-017), README VLAN filename mismatch (E-018), rss_hash_input_l4 doc inconsistency (E-019), and two Medium-priority Kaitai syntax verification items (E-020 enum syntax, E-021 type casting). Issues documented in `analysis/ethernet_protocols/ethernet_protocols_issues.md`. |
| 2026-01-28 | Ethernet second review fixes | Closed W-13-012 through W-13-017: W-13-012 clarified VLAN cross-ref in ethernet_ii.ksy (4cf0bf00). W-13-013 added VLAN cross-ref to ipv4.ksy (2a6c496f). W-13-014 added VLAN cross-ref to ipv6.ksy (95d80292). W-13-015 added RSS cross-ref to tcp.ksy (d87bece5). W-13-016 added RSS cross-ref to udp.ksy (4ff530a5). W-13-017 fixed stale W-13-011 reference in ipv6.ksy (a0273296). All pushed to origin/main. |
| 2026-01-28 | Ethernet second review fixes (cont.) | Closed W-13-018 and W-13-019: W-13-018 fixed README.md VLAN filename reference (c2dfdfe9). W-13-019 improved rss_hash_input_l4 doc in tcp.ksy and udp.ksy to match ipv4/ipv6 style (98d2461a). Both pushed to origin/main. |
| 2026-01-28 | Kaitai validation script | Closed W-13-020 and W-13-021: Created `datamodel/scripts/validate_ksy.py` to validate .ksy files by stripping custom x-* keys and running ksc compiler. Verified all 9 Ethernet and 9 RoCE files pass validation. Confirmed enum syntax (algorithm::crc32) and type casting (.as<u4>) are valid. Commit: 9dc6a627, pushed to origin/main. |
| 2026-01-29 | UALink ksy_file cross-references | Closed W-14-003: Added `ksy_file` field to all 5 UALink YAML reference files in `reference/field_definitions/` for bidirectional traceability to authoritative .ksy definitions. Files: tl_flit.yaml, dl_flit.yaml, flow_control_field.yaml, link_state.yaml, upli_request_channel.yaml. Commit: d8a0777e, pushed to origin/main. |
| 2026-01-29 | UALink dl_flit.yaml segment sizes | Closed W-14-001: Fixed `dl_flit.yaml` segment sizes to include headers (129, 129, 129, 125, 121 bytes). Added `header_bytes` and `payload_bytes` fields for clarity. Removed erroneous 5-byte `padding` field. Total now correctly sums to 640 bytes matching authoritative `dl_flit.ksy`. Commit: a129dfd9, pushed to origin/main. |
| 2026-01-29 | UALink metadata.yaml packet count | Closed W-14-002: Fixed `metadata.yaml` packet count from 35 to 38 (verified by counting actual .ksy files). Updated `by_layer` breakdown: upli 6+2=8, transaction 7+2=9, datalink 8+4=12, physical 3+1=4, security 3+2=5. Total: 27 packet formats + 11 protocols = 38 .ksy files. Commit: 6e596fa4, pushed to origin/main. |
| 2026-01-29 | UALink security layer expansion | Closed W-14-004: Expanded all 5 security layer .ksy files from ~270 lines to ~1655 lines. Added Tables 9-4 through 9-7 encryption/authentication attributes, Table 9-3 IV format, Figures 9-8/9-9/9-11/9-12 key derivation and rotation state machines. Security layer now matches detail level of other UALink layers. Commit: c2aec1ee, pushed to origin/main. |
| 2026-01-30 | UALink spec_date verification | Closed W-14-005: Updated all spec_date values to official release dates. UALink 200 v1.0 Final: 2025-04-08 (37 files). DLPL 1.5 RC: 2026-01-12 (1 file). Updated metadata.yaml with correct dates. Commit: 9ef353b1, pushed to origin/main. |
| 2026-01-28 | IEEE 802.3 frame support | Closed W-13-010: Added IEEE 802.3/LLC/SNAP frame support for control-plane and discovery protocols. New files: ethernet_802_3.ksy (MAC frame with length field), llc.ksy (IEEE 802.2 LLC header), snap.ksy (SNAP extension). Updated ethernet_ii.ksy with disambiguation instances, vlan_802_1q.ksy with cross-references, README.md with protocol stack and file list. All 12 Ethernet files pass validation. Commit: 48a3880f, pushed to origin/main. |
| 2026-01-28 | RoCE CNP/XRC support decision | Closed W-12-008 and W-12-012: PMR supports CNP (transport type 4) for ECN-based congestion control. PMR does NOT support XRC (transport type 5) - no shared receive queues. Updated roce/README.md PMR Support column (CNP=Yes, XRC=No). Updated bth.ksy with pmr_support metadata and is_xrc note. XRCETH header not required. Commit: 53fb207b, pushed to origin/main. |
| 2026-01-28 | RoCE extended atomics exclusion | Closed W-12-009: Extended/masked atomics (MASKED_CMP_SWAP 0x15, MASKED_FETCH_ADD 0x16) NOT supported over RoCE - will be implemented over UE/UE+ instead. Standard 64-bit atomics (CMP_SWAP, FETCH_ADD) remain supported. Updated roce/README.md and bth.ksy with exclusion documentation. Commit: dd2e1f5b, pushed to origin/main. |
| 2026-01-29 | UALink datamodel review | Comprehensive review of UALink datamodel (48 files). Overall quality: PRODUCTION-QUALITY with excellent spec traceability. Created 5 work items (W-14-001 through W-14-005). Key issues: DL Flit YAML segment sizes incorrect (W-14-001, Critical), packet count mismatch (W-14-002, Medium), missing KSY cross-references in YAML (W-14-003, Medium). Issues documented in `analysis/ualink/ualink_issues.md`. |
| 2026-01-30 | UALink half-flit expansion | Closed W-14-008: Expanded sparse half-flit definitions to exemplar quality. `data_half_flit.ksy`: 40→142 lines (poison indication per Section 5.3, byte enable relationship, data beat sequencing, ASCII diagram). `message_half_flit.ksy`: 37→148 lines (message type encoding per Tables 5-3/5-4, TL message format per Section 5.1.2, ASCII diagram). Both files now match `control_half_flit.ksy` exemplar pattern. Commit: 61030281, pushed to origin/main. |
| 2026-01-30 | UALink YAML coverage criteria | Closed W-14-011: Documented YAML reference coverage criteria in `ualink/README.md`. 4 criteria: (1) Entry point packets (tl_flit, dl_flit), (2) Multi-variant formats (response_field), (3) Cross-layer interfaces (upli_request_channel, link_state), (4) High-complexity fields (flow_control_field). 6 YAML files exist by design; remaining 32 KSY files are self-documenting. Commit: 51d8c469, pushed to origin/main. |
| 2026-02-02 | UFH header reorganization | Separated UE standard UFH headers from Cornelis proprietary versions. Created `ue/network/ufh_16.ksy` and `ufh_32.ksy` for UE standard. Renamed Cornelis versions to `ufh_16_plus.ksy` and `ufh_32_plus.ksy`. Updated all references in metadata.yaml, README.md, packet_taxonomy_cornelis.md, DATAMODEL_UPDATES.md, HAS/PMR/WORK.md, and HAS/PMR/04-addressing.md. Commits: d5cfb7e2, 1d4e0ce4, c78222d8, pushed to origin/main. |

---

## 6. References

### Internal Documents
- `docs/HAS/PMR/05-packet-formats.md` - PMR HAS Chapter 5
- `docs/HAS/PMR/WORK.md` - PMR HAS Work Tracking (authoritative source for W-03-002, W-03-006)
- `.specify/memory/constitution.md` - Project Constitution

### Sub-Documents
- [packet_taxonomy_ue_pds.md](packet_taxonomy_ue_pds.md) - UE+ PDS formats
- [packet_taxonomy_ue_ses.md](packet_taxonomy_ue_ses.md) - UE+ SES formats
- [packet_taxonomy_ue_cms_tss.md](packet_taxonomy_ue_cms_tss.md) - UE+ CMS/TSS formats
- [packet_taxonomy_ue_link.md](packet_taxonomy_ue_link.md) - UE+ Link Layer formats
| [packet_taxonomy_ue_tagged_send_variants.md](packet_taxonomy_ue_tagged_send_variants.md) | Tagged-Send Variants | UE Standard, CSIG, IPv4, TSS, Small, Rendezvous, Deferrable | `ue/transport/` |
- [packet_taxonomy_rocev2.md](packet_taxonomy_rocev2.md) - RoCEv2 formats
- [packet_taxonomy_cornelis.md](packet_taxonomy_cornelis.md) - Cornelis proprietary formats
- [packet_taxonomy_hsi.md](packet_taxonomy_hsi.md) - Host-Software Interface formats
- [packet_taxonomy_ualink.md](packet_taxonomy_ualink.md) - UALink reference (not PMR-supported)
- [packet_taxonomy_ethernet.md](packet_taxonomy_ethernet.md) - Standard Ethernet formats

### Issue Tracking Documents
- [RoCE_protocols_issues.md](../roce_protocols/RoCE_protocols_issues.md) - RoCE datamodel issues (R-001 through R-017)
- [ethernet_protocols_issues.md](../ethernet_protocols/ethernet_protocols_issues.md) - Ethernet datamodel issues (E-001 through E-010)

### Datamodel Locations
- `datamodel/protocols/ue/` - Ultra Ethernet protocols (94 .ksy files)
- `datamodel/protocols/roce/` - RoCEv2 protocols (8 .ksy files)
- `datamodel/protocols/ethernet/` - Standard Ethernet (6 .ksy files)
- `datamodel/protocols/cornelis/` - Cornelis proprietary (9 .ksy files)
- `datamodel/protocols/ualink/` - UALink protocols (38 .ksy files) - NOT supported by PMR
- `datamodel/hw/asics/pmr/` - PMR ASIC definitions

### External Specifications
- [Ultra Ethernet Specification v1.0.1](https://ultraethernet.org/)
- [InfiniBand Architecture Specification](https://www.infinibandta.org/)
- IEEE 802.3 Ethernet Standard
- UALink Specification (Ultra Accelerator Link)
| 2026-01-30 | UALink security layer review | Closed W-14-006: In-depth review of W-14-004 security layer expansion against UALink200 Spec Section 9. All 5 files (1660 lines) verified: encryption.ksy (Tables 9-4-9-7), authentication.ksy (Tables 9-8-9-12), iv_format.ksy (Table 9-3), key_derivation.ksy (Figure 9-8), key_rotation.ksy (Figures 9-9, 9-11, 9-12). No corrections required. Review-only task (no code changes). Findings documented in `.sisyphus/notepads/w-14-006-security-layer-review/findings.md`. |
| 2026-01-30 | UALink response_field expansion | Closed W-14-009: Expanded response_field.ksy from 52 to 310 lines with full bit-level parsing. Added uncompressed_response (Table 5-30), compressed_response_single_beat (Table 5-34), compressed_response_write_multibeat (Table 5-36). Added x-packet.constraints for Tables 5-35 and 5-37 restrictions. Created response_field.yaml reference file (139 lines). Commit: 1f8f4a35, pushed to origin/main. |
| 2026-01-30 | UALink flit_header top-level seq | Closed W-14-010: Expanded flit_header.ksy from 90 to 165 lines with top-level seq and instances for header type discrimination. Added op_field, payload_field, is_explicit_sequence, is_command, is_ack, is_replay_request, is_original, is_replay, is_nop, is_payload instances. Commit: 6c622561, pushed to origin/main. |
| 2026-01-30 | UALink x-related-headers | Closed W-14-007: Added x-related-headers cross-reference sections to 37 KSY files across all 5 layers. UPLI (7): commands, request_channel, read_response_channel, write_response_channel, originator_data_channel, flow_control, connection_handshake. Transaction (9): tl_flit, control_half_flit, message_half_flit, data_half_flit, request_field, response_field, flow_control_field, compression, address_cache. Datalink (12): dl_flit, flit_header, segment_header, crc, basic_messages, control_messages, uart_messages, vendor_defined, link_state, link_resiliency, link_level_replay, link_folding. Physical (4): reconciliation_sublayer, control_ordered_sets, alignment_markers, link_training. Security (5): encryption, authentication, iv_format, key_derivation, key_rotation. Relationship vocabulary: contains, references, uses, part-of. Commit: 51dbf9ed, pushed to origin/main. |
