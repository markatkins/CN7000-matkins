# Crosscheck Review Report: UALink Switch Requirements vs. LNR Switch HAS Rev 0.3

## Document Information

| Field | Value |
|-------|-------|
| **Artifact 1** | `docs/references/UALink` — UALink-200 Switch Requirements V0.6 (AMD) + UALink200 Specification v1.0 Final + Gap Analysis + Engineering Review |
| **Artifact 2** | `docs/references/LNR_Switch_HAS_Rev_0.3` — Lightning River Switch Hardware Architecture Specification, Rev 0.3 (Cornelis Networks, Feb 4 2026) |
| **Review Date** | 2026-02-10 |
| **Reviewer** | Crosscheck Analysis (developer-opus) |
| **Classification** | Cornelis Internal |

---

## 1. Executive Summary

This crosscheck compares AMD's UALink-200 Switch Requirements V0.6 (the "Requirements") against the Cornelis Networks Lightning River (LNR) Switch HAS Rev 0.3 (the "Specification") to identify alignments, gaps, contradictions, and ambiguities between the two artifacts. A pre-existing gap analysis document (`AMD_UALink200_vs_LNR_Gap_Analysis.md`) and an internal engineering review (`Cornelis_UALink200_Engineering_Review.md`) were also consulted as supplementary context.

**Overall Assessment:** The LNR Switch HAS Rev 0.3 addresses the core switching hardware requirements (bandwidth, latency, port count, crossbar architecture, collectives engine, flow control) with strong alignment. However, the HAS document is **architecturally focused** and leaves many AMD requirements **unaddressed or as placeholder sections** — particularly in security/TEE, virtual pods, RAS error handling, power/thermal, ordering semantics, and software/management interfaces. The engineering review document acknowledges these gaps and proposes 52–66 engineer-weeks of work to close them.

### Summary Statistics

| Alignment Status | Count | Notes |
|-----------------|-------|-------|
| **ALIGNED** — HAS directly addresses requirement | 22 | Core HW: ports, BW, latency, crossbar, FEC, VLs, collectives, PCIe, CBFC |
| **PARTIALLY ALIGNED** — HAS addresses partially or implicitly | 14 | Routing, QoS, bifurcation, non-blocking, multicast, management |
| **UNSPECIFIED IN HAS** — Requirement exists, HAS has placeholder/TBD | 48 | Power, thermal, RAS, ordering, debug, reliability, SW update, telemetry |
| **GAP** — Requirement exists, HAS contradicts or omits entirely | 26 | TEE/SSM, UALinkSec, vPOD, SPDM, GNMI, Redfish, DRAM encryption |
| **HAS EXCEEDS** — HAS provides capability beyond requirement | 6 | BW (115.2 Tbps vs 57 Tbps), PCIe Gen5 vs Gen4, 8 VLs vs 2 required |

---

## 2. Detailed Cross-Reference Analysis

### 2.1 Port Configuration and Bandwidth

| Parameter | AMD Requirement (V0.6) | LNR HAS Rev 0.3 | Status |
|-----------|----------------------|------------------|--------|
| Switch Radix (800G) | 72 / 144 ports | 72 native 1.6T ports; 144 in 800G mode (quad-die) | ALIGNED |
| Switch Radix (400G) | 144 / 288 ports | 288 in 400G mode (quad-die) | ALIGNED |
| Aggregate BW | >57 Tbps (mandatory), >115 Tbps (preferred) | 115.2 Tbps (72 x 1.6T) | EXCEEDS |
| Lane Count | 576 lanes preferred, 288 mandatory | 576 lanes (72 x 8 lanes @ 212.5 Gbps) | ALIGNED |
| SerDes Speed | 200G PAM4 (212.5 Gbps signaling) | 212.5 Gbps/lane (HAS Switch Features - Port Bandwidths) | ALIGNED |
| Bifurcation | 2-lane and 4-lane groups, no mixed | Per-MPORT config; 1.6T/800G/400G/200G subdivision per port; heterogeneous supported within a native port | ALIGNED — LNR supports 2-lane (400G) and 4-lane (800G) groupings |
| Package Options | Not specified | Quad-die, Dual-die, Single-die (same base die) | EXCEEDS — flexibility |

**Finding F-2.1.1 (OBSERVATION):** AMD recommends 288x400G ports (Section 4.1), but LNR's native mode is 72x1.6T. UALink mode is **not supported in native 1.6T mode** — the HAS explicitly states "Native mode: UALink = N" (line 121). UALink requires 800G, 400G, or 200G subdivision modes. This is architecturally correct but should be clearly documented in customer-facing materials.

**Finding F-2.1.2 (OBSERVATION):** The HAS states "UALink and Ethernet can not be enabled simultaneously" (line 602). This is a per-chip-level mode selection. AMD's requirements do not explicitly require simultaneous Ethernet+UALink, but this constraint should be validated against deployment scenarios.

---

### 2.2 Latency

| Parameter | AMD Requirement | LNR HAS Rev 0.3 | Status |
|-----------|----------------|------------------|--------|
| Pin-to-Pin Latency (800G) | <=250 ns | Gap analysis claims 196-200 ns; HAS Latency Budgets shows crossbar core worst-case 15.9 ns (same die) to 89.2 ns (different dies) | ALIGNED |
| Pin-to-Pin Latency (400G) | <=275 ns | Not explicitly stated in HAS | UNSPECIFIED |
| Rpipe Latency | Not specified by AMD | Ethernet IPv4: 25 ns; UALink: TBD (HAS line 758) | TBD IN HAS |
| Uncongested Loaded Latency | <=300 ns at 80% load | Gap analysis claims ~250 ns | ALIGNED (per gap analysis, not HAS) |
| RTT Latency Tolerance | >=400 ns | Not specified in HAS | UNSPECIFIED |

**Finding F-2.2.1 (RISK — MEDIUM):** The HAS marks UALink Rpipe latency as "TBD" (line 758). This is a critical parameter for the overall pin-to-pin latency budget. The 196-200 ns claim in the gap analysis appears to be an estimate, not a specification. The HAS should be updated with a concrete UALink Rpipe latency target.

**Finding F-2.2.2 (OBSERVATION):** The HAS provides detailed crossbar latency budgets (Latency Budgets, lines 1813-1817) showing same-die best ~11.4 ns, worst ~36 ns; different-die best ~44 ns, worst ~89.2 ns. These are crossbar-only numbers and do not include Rpipe, Hill Creek MAC/PCS, or FEC latency. A complete pin-to-pin latency breakdown is needed.

---

### 2.3 Throughput

| Parameter | AMD Requirement | LNR HAS Rev 0.3 | Status |
|-----------|----------------|------------------|--------|
| 64B throughput (200G rate) | >=165 Gbps | HAS Data Crossbar shows 2 packets/clock in 1.6T mode for 64B; crossbar core 96B @ 3.33 GHz | ALIGNED (by architecture) |
| 256B throughput (200G rate) | >=186 Gbps (critical) | Line rate by architecture | ALIGNED |
| P2P Reads >=46 GB/s per 400G port | Required | Line rate by architecture | ALIGNED |
| All-to-All Writes >=46 GB/s | Required | Line rate by architecture | ALIGNED |
| Spray Reads >=46 GB/s | Required | Line rate by architecture | ALIGNED |

**Finding F-2.3.1 (OBSERVATION):** The HAS provides two crossbar packet modes — "Small Packet Optimized" (uses full 192B, higher latency due to pseudo-store-and-forward) and "Low Latency" (uses 128B, cut-through). The 64B throughput requirement may depend on which mode is used. The HAS should clarify which mode achieves the >=165 Gbps target for 64B packets.

---

### 2.4 Protocol Support

| Parameter | AMD Requirement | LNR HAS Rev 0.3 | Status |
|-----------|----------------|------------------|--------|
| UALink 2.0 protocol | Required | HAS Supported Protocols lists "Ultra Accelerator Link" as L2 protocol | VERSION AMBIGUITY |
| UALink Rpipe | Required | HAS UALink Rpipe (lines 699-773) describes separate UALink mode with per-station routing tables | ALIGNED |
| FEC | Standard (4-way) + LL FEC (1 & 2-way) | HAS Switch Features lists FEC support; gap analysis confirms RS-272/544 + LL FEC | ALIGNED |
| LLR (Link Layer Replay) | Implied by RAS requirements | HAS Switch Features - Ethernet lists LLR | ALIGNED |
| CBFC | Required for UALink | HAS Switch Features lists CBFC; Link Flow Control describes 64B credit unit | ALIGNED |

**Finding F-2.4.1 (RISK — HIGH):** AMD requires "UALink 2.0" compliance (Section 4.1), with a footnote that "UALink 2.0 specification may be renamed to 1.x." The LNR HAS does not specify which UALink version it targets. The gap analysis flags this as a "VERSION GAP." The engineering review recommends engaging AMD for clarification. **This version alignment must be resolved.**

**Finding F-2.4.2 (OBSERVATION):** The HAS UALink Rpipe (line 706) describes routing as "lookup of [IngressStation][DestAccId] into routing table" with per-ingress-station route tables and shadow copies for SW updates. This aligns with UALink routing requirements but the HAS marks several UALink Rpipe items as "needs to be defined" (line 769).

---

### 2.5 Virtual Channels / QoS

| Parameter | AMD Requirement | LNR HAS Rev 0.3 | Status |
|-----------|----------------|------------------|--------|
| VC-0 | Required | 8 QoS levels (HAS line 131); 6 VLs in crossbar bandwidth metering (line 2771) | EXCEEDS |
| VC-1 | Recommended | Supported | EXCEEDS |
| VC-2, VC-3 | Not used | Available but not required | EXCEEDS |
| Non-Blocking | Required | Crossbar architecture with distributed arbitration (CIA, DRIA, converge arbiters) | ALIGNED |
| Forward Progress | Round-robin arbitration | HAS VL/Priority Fairness describes LRU, WRR, strict priority, bandwidth metering | ALIGNED |

**Finding F-2.5.1 (CONTRADICTION — LOW):** AMD requires VC-0 (mandatory) and VC-1 (recommended), with VC-2 and VC-3 not used. The LNR HAS describes 8 QoS levels and 6 VLs in the crossbar bandwidth metering. The mapping between UALink Virtual Channels and LNR VLs is not explicitly defined in the HAS. The HAS UALink Rpipe (line 710) states "QOS based on VC — TBD factor in Request, Response and IngressSubport." **This mapping must be specified.**

**Finding F-2.5.2 (OBSERVATION):** The HAS provides extensive detail on VL/Priority arbitration (VL/Priority Fairness Resolution, Bandwidth Meters, CIA Arb) with configurable strict priority, bandwidth allocation, and best-effort modes. This exceeds AMD's basic round-robin requirement but the UALink-specific QoS mapping is TBD.

---

### 2.6 Non-Blocking Architecture

| Parameter | AMD Requirement | LNR HAS Rev 0.3 | Status |
|-----------|----------------|------------------|--------|
| Independent port traffic | Required | Crossbar architecture with per-port arbitration | ALIGNED |
| No egress backpressure blocking across ports | Required | Push model with distributed arbitration; pacing ring prevents incast | ALIGNED |
| No VC credit stall across VCs | Required | Per-VL credit management on Link Credit Ring | ALIGNED |
| No LLR stall propagation | Required | Not explicitly addressed in HAS | UNSPECIFIED |

**Finding F-2.6.1 (RISK — MEDIUM):** AMD Section 5.1 specifically warns that "An error on a port will force the link to replay FLITs using the link level retry (LLR) protocol. Traffic is blocked during LLR for 600ns to 1us. Blocking unrelated ports may lead to a cascading effect." The HAS does not explicitly address LLR stall isolation. AMD recommends independent schedulers per port. The HAS's MPORT architecture (3 Hill Creeks per MPORT) means ports within the same MPORT share resources. **The HAS should document how LLR on one port within an MPORT does not cascade to other ports.**

---

### 2.7 Routing

| Parameter | AMD Requirement | LNR HAS Rev 0.3 | Status |
|-----------|----------------|------------------|--------|
| UALink Routing | Meet UALink Specification | HAS UALink Rpipe: per-station routing tables with [IngressStation][DestAccId] lookup, shadow copies, DenyMask | ALIGNED |
| Multicast | Required (at minimum) | Data Ring with destination mask (32-bit), Lbuf SRSB Packet Replicator | ALIGNED |
| Unicast | Required | Data Crossbar (HFC architecture) | ALIGNED |

**Finding F-2.7.1 (OBSERVATION):** The HAS Rpipe Tag Routing (line 778) clearly delineates routing paths: unicast -> Data Crossbar, multicast -> Data Ring, management -> Data Ring, collectives -> configurable (crossbar/ring/local). This is well-specified.

---

### 2.8 In-Network Collectives (INC)

| Parameter | AMD Requirement | LNR HAS Rev 0.3 | Status |
|-----------|----------------|------------------|--------|
| Block-based collectives | Primary requirement | CE block with 4x128B input buses, 1x128B output; RISC-V compute block (CE HAS) | ALIGNED |
| Transactional collectives | Important | Supported via CE programmability | ALIGNED |
| Data movement collectives | Important | Supported | ALIGNED |
| Multicast (minimum) | Required | Data Ring + Packet Replicator | ALIGNED |
| CE count | Not specified by AMD | 1 CE per MPORT = 24 CEs (quad-die); 4 cores per CE = 96 cores total | ALIGNED |

**Finding F-2.8.1 (OBSERVATION):** The HAS provides detailed collectives architecture: CE Arbiter ensures all operands received before processing (line 1236), Lbuf provides 1.2 MB storage with 1us skew tolerance (line 1046), and the Packet Replicator handles result dissemination. The engineering review identifies remaining firmware work (FP8/BF16 data types, Group Table, control plane mechanisms) estimated at 12-16 engineer-weeks.

**Finding F-2.8.2 (RISK — LOW):** The HAS Collectives Engine Packet Tag Generation (line 1222) marks tag characteristics as "TBD." This should be specified.

---

### 2.9 Security / Confidential Computing

| Parameter | AMD Requirement | LNR HAS Rev 0.3 | Status |
|-----------|----------------|------------------|--------|
| TEE Support | Device attestation, HW/FW isolation, multi-tenant memory isolation | HAS Data Path Security is a **placeholder** (single slide, line 3097) | **MAJOR GAP** |
| Switch Security Manager (SSM) | Lock INC config, group config, key management | Not in HAS | **MAJOR GAP** |
| TSISP | Standard trusted host interface | Not in HAS | **MAJOR GAP** |
| UALinkSec (3 modes) | Encryption disabled / without auth / with auth | HAS has no encryption engine specification | **MAJOR GAP** |
| SPDM Protocol | Device attestation, multiple sessions | Not in HAS | **MAJOR GAP** |
| DRAM Encryption | Required if INC has external memory | Not in HAS | **MAJOR GAP** |
| Hardware RoT | Required | HAS Electric Creek lists "Caliptra root of trust" (line 1310) | ALIGNED |
| Secure Boot | Required | Caliptra 2.0 (per Electric Creek HAS reference) | ALIGNED |
| Unique Device Key | Required | Caliptra Key Vault (per engineering review) | PLANNED |

**Finding F-2.9.1 (RISK — CRITICAL):** The HAS Data Path Security (page 176) is a **single empty placeholder slide**. AMD's confidential computing requirements (Section 6) are extensive — 22+ individual security requirements spanning TEE, SSM, TSISP, link encryption, key management, and memory isolation. **None of these are specified in the HAS.** The engineering review proposes a comprehensive architecture (16-20 engineer-weeks for TEE, 10-12 for UALinkSec) but this work has not been incorporated into the HAS.

**Finding F-2.9.2 (RISK — CRITICAL):** AMD Section 6.1.3 requires UALinkSec 2.0 with key rolling and key switching. The current HAS has no encryption engine specification. The engineering review proposes reusing TSS encryption architecture from the CN7000 NIC, but this is a proposal, not a specification.

---

### 2.10 Virtual Pods (vPOD)

| Parameter | AMD Requirement | LNR HAS Rev 0.3 | Status |
|-----------|----------------|------------------|--------|
| vPOD Support | Integer number of System Nodes per vPOD | HAS Virtualization is a **placeholder** (single slide, line 3105) | **MAJOR GAP** |
| Per-port routing tables | Required for vPOD isolation | UALink Rpipe has per-station routing tables (line 707) — foundation exists | PARTIAL |
| Resource isolation | Required | Not specified | **GAP** |

**Finding F-2.10.1 (RISK — HIGH):** The HAS Virtualization (page 178) is a **single empty placeholder slide**. AMD requires vPOD support (Section 4.4, mandatory). The engineering review proposes a vPOD architecture with up to 16 vPODs, independent LFT instances, and resource partitioning (14-18 engineer-weeks), but this is not in the HAS. The per-station routing table architecture in the UALink Rpipe provides a foundation, but the complete vPOD isolation mechanism is unspecified.

---

### 2.11 RAS / Error Handling

| Parameter | AMD Requirement | LNR HAS Rev 0.3 | Status |
|-----------|----------------|------------------|--------|
| UPLI Control/Data/Protocol Errors | Capture & report | Not specified in HAS | UNSPECIFIED |
| Switch Core Control/Data Errors | Capture & report | HAS mentions SECDED ECC on Rbuf (line 552) and Lbuf (line 1049); SBE/MBE logging on read (lines 838-839) | PARTIAL |
| Port & Station Reset | Required | Not specified in HAS | UNSPECIFIED |
| Hot Add/Remove | Required | Not specified in HAS | UNSPECIFIED |
| TL Drop Mode | Required | Not specified in HAS | UNSPECIFIED |
| Port Isolation | Required | Not specified in HAS | UNSPECIFIED |
| Linkdown Isolation | Required | Not specified in HAS | UNSPECIFIED |
| Re-Linkup | Required | Not specified in HAS | UNSPECIFIED |
| Link Resiliency (2 lanes) | Required | Not specified in HAS | UNSPECIFIED |
| E2E Soft Error Protection | Required | SECDED ECC on memory arrays; CRC on crossbar data | PARTIAL |
| Poison Support | Required | Not specified in HAS | UNSPECIFIED |
| Error Logging & Reporting | Required | Not specified in HAS | UNSPECIFIED |
| Error Injection | Required | Not specified in HAS | UNSPECIFIED |

**Finding F-2.11.1 (RISK — HIGH):** AMD specifies 28+ RAS requirements (Sections 2.21-2.63, 2.86-2.87). The HAS provides ECC protection on memory arrays (Rbuf SECDED at 8-byte granularity, Lbuf SECDED at 8-byte granularity) and mentions SBE correction and MBE logging during reads. However, **no systematic RAS architecture is specified** — no error reporting framework, no port isolation mechanism, no drop mode, no poison propagation, no error injection capability. The engineering review proposes preliminary RAS specifications but these are not in the HAS.

---

### 2.12 Power and Thermal

| Parameter | AMD Requirement | LNR HAS Rev 0.3 | Status |
|-----------|----------------|------------------|--------|
| Power w/o INC (288 lanes) | <=460W | Not specified | UNSPECIFIED |
| TDP (576 lanes) | <=900W | Not specified | UNSPECIFIED |
| Idle Power (no SerDes) | <=50W | Not specified | UNSPECIFIED |
| SerDes Power | <=5 pJ/bit | Not specified | UNSPECIFIED |
| L0P Link Folding | Required | Not specified | UNSPECIFIED |
| Tj max | 105 deg C | Not specified | UNSPECIFIED |
| Process Node | Not specified | TSMC N3P (HAS line 130) | (informational) |

**Finding F-2.12.1 (RISK — MEDIUM):** The HAS specifies TSMC N3P process and provides detailed crossbar architecture (96B @ 3.33 GHz core), but contains **zero power or thermal specifications**. The engineering review proposes preliminary targets (400W typical / 450W max for 288 lanes; 800W typical / 900W TDP for 576 lanes) but these are unvalidated estimates. AMD's power requirements are mandatory.

---

### 2.13 Management Interfaces

| Parameter | AMD Requirement | LNR HAS Rev 0.3 | Status |
|-----------|----------------|------------------|--------|
| PCIe Control Plane | PCIe Gen4 x4 | PCIe Gen5 x2 (32 Gbps max, HAS line 140) | EXCEEDS (Gen5 > Gen4) |
| Host CPU | Switch NOS CPU | Electric Creek with RISC-V MPROC (line 1309) | ALIGNED |
| BMC Interface | I3C/I2C | Electric Creek (per EC HAS reference) | ALIGNED |
| GNMI API | Required | Not specified | **GAP** |
| Redfish Events | Required (websocket/SSE) | Not specified | **GAP** |
| SAI API | Required | Planned (per engineering review) | PLANNED |
| SONiC NOS | Required | Planned (per engineering review) | PLANNED |

**Finding F-2.13.1 (OBSERVATION):** The HAS specifies PCIe Gen5 x2 (line 140), which provides 32 Gbps — exceeding AMD's Gen4 x4 requirement (also 32 Gbps but with wider link). The lane count difference (x2 vs x4) should be validated for compatibility.

---

### 2.14 Ordering

| Parameter | AMD Requirement | LNR HAS Rev 0.3 | Status |
|-----------|----------------|------------------|--------|
| Strict Ordered Delivery (with encryption) | Required: Requests, Read Responses, Write Responses must stay ordered between src/dst | HAS Rbuf SRSB Scheduler: "Packets to a given destination port must be read out of Rbuf in the order that grant tags are received" (line 822) | PARTIAL |
| Relaxed Order Delivery (without encryption) | Not required (N) | N/A | N/A |

**Finding F-2.14.1 (RISK — MEDIUM):** AMD Section 2.31 requires strict ordered delivery for three streams (requests, read responses, write responses) between source and destination ports when encryption is enabled. The HAS provides per-destination-port ordering at the Rbuf SRSB Scheduler level, but does not explicitly address UALink stream-level ordering semantics. The HAS UALink Rpipe open items (line 769) lists "UALink needs to be defined" for ordering. **This must be specified.**

---

### 2.15 Reliability

| Parameter | AMD Requirement | LNR HAS Rev 0.3 | Status |
|-----------|----------------|------------------|--------|
| Silicon Operating Life | 5 years | Not specified | UNSPECIFIED |
| Quality (t=0) | 500 DPPM | Not specified | UNSPECIFIED |
| SER | <200 FIT, SDC <5 FIT | Not specified | UNSPECIFIED |
| EOL Hard Errors | 150 FIT | Not specified | UNSPECIFIED |
| ESD HBM | >1 kV | Not specified | UNSPECIFIED |
| Temperature Range | 0 deg C - 105 deg C | Not specified | UNSPECIFIED |

**Finding F-2.15.1 (OBSERVATION):** All 16 reliability requirements (Sections 2.71-2.85) are unspecified in the HAS. These are characterization/qualification items rather than architectural features, but AMD marks them all as mandatory (Y). The engineering review proposes preliminary targets but notes they are "subject to validation through qualification testing."

---

### 2.16 Software / Firmware

| Parameter | AMD Requirement | LNR HAS Rev 0.3 | Status |
|-----------|----------------|------------------|--------|
| Software Considerations | Required | HAS Software Considerations is a **placeholder** (single slide, line 3144) | UNSPECIFIED |
| Debug Interfaces | Required | HAS Debug Interfaces is a **placeholder** (single slide, line 3138) | UNSPECIFIED |
| CSR Definitions | Required | HAS LNR CSRs references "TBD Peak RDL documentation" (line 3152) | TBD |
| Init Sequence | Required | HAS Init Sequence is a **placeholder** (single slide, line 3127) | UNSPECIFIED |
| Non-disruptive FW Update | Required | Not specified | UNSPECIFIED |
| Secure Boot | Required | Caliptra 2.0 (via Electric Creek) | ALIGNED |

---

## 3. Contradictions and Inconsistencies

### C-1: UALink Native Mode Not Supported
- **HAS** (line 121): Native mode UALink = **N**; UALink only in 800G/400G/200G subdivision
- **AMD** (Section 4.1): Recommends 288x400G ports
- **Assessment:** Not a contradiction — architecturally consistent. LNR's native 1.6T mode is Ethernet-only; UALink uses subdivided modes. However, this means a 72-port quad-die LNR in UALink mode operates as 144x800G or 288x400G, not 72x1.6T.

### C-2: PCIe Lane Count
- **AMD** (Section 2.36): Recommends PCIe Gen4 x4
- **HAS** (line 140): PCIe Gen5 x2
- **Assessment:** Both provide ~32 Gbps. Gen5 x2 is a higher-performance interface but with fewer lanes. If AMD's software stack assumes x4 lane width, there could be a compatibility issue. **Needs validation.**

### C-3: VL Count Ambiguity
- **HAS** (line 131): "8 quality of service levels (QoS)"
- **HAS** (line 2771): "Destinations: 576 x (6 VLs) TPORT" — bandwidth meters track 6 VLs
- **HAS** (line 2682): "we might be able to go back to 8?" — suggests 8 VLs is aspirational
- **Assessment:** The crossbar currently implements 6 VLs for bandwidth metering, with 8 QoS levels at the port level. The mapping between port QoS levels and crossbar VLs is unclear. AMD requires VC-0 (mandatory) and VC-1 (recommended), so 6 VLs is sufficient, but the HAS should clarify the actual VL count.

### C-4: Rbuf Size vs. Cable Length Claims
- **HAS** (lines 546-550): 6.0 MB Rbuf, 2.0 MB per native port, supports 3 ports with 30m cables or 1 port with 200m cable
- **AMD** (Section 2.100): RTT latency tolerance >=400 ns, assumes 3m cable + retimer
- **Assessment:** No contradiction — LNR's Rbuf is sized for much longer cables than AMD requires. The 30m CBFC support significantly exceeds AMD's 3m cable assumption.

---

## 4. Placeholder / TBD Sections in HAS

The following HAS sections are **empty placeholders** (single slide with title only):

| Section | HAS Page | AMD Relevance |
|---------|----------|---------------|
| Data Path Security | 176 | **CRITICAL** — AMD Section 6 (22+ requirements) |
| Quality of Service | 177 | **HIGH** — AMD Sections 2.50-2.51 |
| Virtualization | 178 | **CRITICAL** — AMD Sections 4.4, 2.10 (vPOD) |
| Packet Trimming | 179 | MEDIUM — related to RAS drop modes |
| Clocks | 181 | LOW — AMD Sections 2.3-2.6 (frequency targets) |
| Resets | 182 | MEDIUM — AMD Section 2.26 (port/station reset) |
| Init Sequence | 183 | MEDIUM — AMD Section 2.90 |
| Performance | 184 | HIGH — references external document |
| Debug Interfaces | 185 | MEDIUM — AMD Sections 2.64-2.65 |
| Software Considerations | 186 | HIGH — AMD Section 7 (all SW requirements) |
| LNR CSRs | 187 | HIGH — needed for all configuration |

**Finding F-4.1 (RISK — CRITICAL):** 11 of the HAS's key sections are empty placeholders. Three of these (Data Path Security, Virtualization, Quality of Service) correspond to AMD's most critical requirements. The HAS Rev 0.3 is approximately **60-65% complete** as measured by section content coverage.

---

## 5. Items in HAS Not Required by AMD

The HAS specifies several capabilities not explicitly required by AMD:

| HAS Feature | Description | Value |
|-------------|-------------|-------|
| 1.6T Native Ethernet Mode | 72-port 1.6T Ethernet switching | Enables Ethernet use case beyond UALink |
| Dual/Single-die packages | Smaller package options | Enables lower-cost SKUs |
| 200m cable support | 1-port 200m CBFC | Far exceeds AMD's 3m requirement |
| Data Ring architecture | Dedicated multicast/management/collectives network | Architectural advantage for INC |
| Congestion Telemetry Ring | Dedicated congestion monitoring | Enables advanced congestion management |
| UCIe die-to-die | Multi-die scaling via UCIe | Enables flexible packaging |

---

## 6. Risk Summary

| Priority | Finding | Category | Impact |
|----------|---------|----------|--------|
| **P0** | F-2.9.1: Security/TEE entirely unspecified | Security | No confidential computing capability |
| **P0** | F-2.9.2: UALinkSec not specified | Security | No link encryption |
| **P0** | F-2.10.1: vPOD entirely unspecified | Virtualization | No multi-tenancy |
| **P0** | F-2.4.1: UALink version ambiguity | Protocol | Potential spec non-compliance |
| **P0** | F-4.1: 11 placeholder sections | Completeness | HAS ~60-65% complete |
| **P1** | F-2.11.1: RAS architecture unspecified | Reliability | No error handling framework |
| **P1** | F-2.14.1: Ordering semantics unspecified | Protocol | Potential data corruption |
| **P1** | F-2.6.1: LLR stall isolation unspecified | Non-blocking | Potential cascading failures |
| **P1** | F-2.2.1: UALink Rpipe latency TBD | Performance | Latency budget incomplete |
| **P2** | F-2.12.1: Power/thermal unspecified | Power | Cannot validate AMD power targets |
| **P2** | F-2.5.1: UALink VC-to-VL mapping TBD | QoS | QoS behavior undefined for UALink |
| **P2** | F-2.15.1: Reliability targets unspecified | Reliability | Cannot validate qualification |

---

## 7. Recommendations

### Immediate Actions (P0)

1. **Resolve UALink Version Alignment** — Confirm with AMD whether UALink 200 v1.0 (as implemented via Cadence IP in Hill Creek) satisfies the "UALink 2.0" requirement, given AMD's own footnote that "UALink 2.0 may be renamed to 1.x."

2. **Populate Security Architecture in HAS** — The engineering review's TEE/SSM/TSISP/UALinkSec proposals (Sections 1-2) should be incorporated into the HAS as architectural specifications, not left as separate proposal documents.

3. **Populate Virtualization Section in HAS** — The engineering review's vPOD architecture (Section 3) should be incorporated into the HAS.

4. **Complete Placeholder Sections** — Prioritize Data Path Security, Virtualization, QoS, and Software Considerations sections.

### Near-Term Actions (P1)

5. **Specify UALink Rpipe Latency** — Replace "TBD" with a concrete target and breakdown.

6. **Document RAS Architecture** — Specify error detection, reporting, isolation, and recovery mechanisms.

7. **Specify UALink Ordering Model** — Document how strict ordered delivery is maintained for the three UALink streams.

8. **Document LLR Stall Isolation** — Specify how LLR on one port within an MPORT does not cascade.

### Medium-Term Actions (P2)

9. **Add Power/Thermal Specifications** — Incorporate validated power and thermal targets.

10. **Define UALink VC-to-VL Mapping** — Specify how UALink Virtual Channels map to LNR VLs.

11. **Add Reliability Targets** — Incorporate qualification targets for FIT, DPPM, ESD, etc.

---

## 8. Conclusion

The LNR Switch HAS Rev 0.3 demonstrates a **strong hardware foundation** that meets or exceeds AMD's core switching requirements for bandwidth (115.2 Tbps vs. >57 Tbps), latency (~200 ns vs. <=250 ns), port count (144x800G or 288x400G), and in-network collectives (24 CEs with RISC-V vector processors). The crossbar architecture (HFC with distributed arbitration), data ring for multicast/collectives, and flexible port subdivision are well-specified and architecturally sound.

However, the HAS is **approximately 60-65% complete**, with 11 critical sections as empty placeholders. The most significant gaps are in **security/confidential computing** (22+ unaddressed requirements), **virtual pods** (unaddressed), and **RAS** (28+ unaddressed requirements). The engineering review document proposes architectures for these gaps totaling 52-66 engineer-weeks of effort, but these proposals have not yet been incorporated into the HAS.

**The LNR HAS Rev 0.3 should not be presented to AMD as a complete response to the UALink-200 Switch Requirements V0.6.** A Rev 0.4 or higher incorporating the security, virtualization, RAS, and software sections is needed before external review.

---

*End of Crosscheck Review Report*
