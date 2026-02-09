# CN7000 Solution and Feature Matrices

## Scale-Out Solutions

Table: Scale-Out AI Workload Solutions {#tbl:scale-out-ai}

| Feature Category | Sub-Feature | Small-Medium Scale | Large Scale | Hyperscalar |
|-----------------|-------------|-------------------|-------------|-------------|
| **Protocols** | Primary | UE+, UE, Ethernet | UE+, UE, Ethernet | UE+, UE, Ethernet |
| | Secondary | RoCE (interop) | RoCE (interop) | RoCE (interop) |
| | Dynamic Select | ✓ (UE+, UE, Ethernet, RoCE) | ✓ (UE+, UE, Ethernet, RoCE) | ✓ (UE+, UE, Ethernet, RoCE) |
| **Transports (UE)** | PDS Modes | RUD, ROD, RUDI, UUD | RUD, ROD, RUDI, UUD | RUD, ROD, RUDI, UUD |
| | SES | Tagged Send, RMA, Atomic, Deferrable Send | Tagged Send, RMA, Atomic, Deferrable Send | Tagged Send, RMA, Atomic, Deferrable Send |
| | CMS | NSCC, RCCC | NSCC, RCCC | NSCC, RCCC |
| **Scale** | Max Endpoints | ≤10K (≤1.25K/rail) | 10K-93K (1.25K-11.6K/rail) | 100K-1.44M (12.5K-180K/rail) |
| | Topology | Fat-Tree or Fat-Tree Rail | Fat-Tree Rail | Fat-Tree Rail |
| **Interoperability** | Mode | Homogeneous | Homogeneous or Heterogeneous (island) | Heterogeneous (island) |
| | Ethernet Compat | UE standard compliant | UE standard compliant | UE standard compliant |
| **Value-Add: Performance** | Link Behavior | Lossless (CBFC, LLR) | Lossless (CBFC, LLR) | Lossless (CBFC, LLR) |
| | Message Rate | 4B msgs/sec bidi | 4B msgs/sec bidi | 4B msgs/sec bidi |
| | Latency (hop) | ≤250ns | ≤250ns | ≤250ns |
| **Value-Add: Routing** | SDR/Packet Spray | ✓ | ✓ | ✓ |
| | FGAR | ✓ | ✓ | ✓ |
| | ECAR | ✓ | ✓ | ✓ |
| | Dynamic Route Recovery | ✓ | ✓ | ✓ |
| **Value-Add: Congestion Mgmt** | ECN | ✓ (UE, Ethernet, RoCE) | ✓ (UE, Ethernet, RoCE) | ✓ (UE, Ethernet, RoCE) |
| | NSCC | ✓ (lossless, lossy) | ✓ (lossless, lossy) | ✓ (lossless, lossy) |
| | RCCC | ✓ | ✓ | ✓ |
| | CSIG/CSIG+ | ✓ | ✓ | ✓ |
| **Value-Add: Collective Accel** | In-Network | ✓ (homogeneous/island) | ✓ (homogeneous/island) | ✓ (homogeneous/island) |

---

Table: Scale-Out HPC Workload Solutions {#tbl:scale-out-hpc}

| Feature Category | Sub-Feature | Small Scale | Medium Scale | Large Scale |
|-----------------|-------------|-------------|--------------|-------------|
| **Protocols** | Primary | OPA 16B, UE+, UE | OPA 16B, UE+, UE | OPA 16B, UE+, UE |
| | Secondary | Ethernet, RoCE | Ethernet, RoCE | Ethernet, RoCE |
| | Dynamic Select | ✓ (OPA, UE+, UE, Ethernet, RoCE) | ✓ (OPA, UE+, UE, Ethernet, RoCE) | ✓ (OPA, UE+, UE, Ethernet, RoCE) |
| **Transports (UE)** | PDS Modes | RUD, ROD, RUDI, UUD | RUD, ROD, RUDI, UUD | RUD, ROD, RUDI, UUD |
| | SES | Tagged Send, RMA, Atomic, Deferrable Send | Tagged Send, RMA, Atomic, Deferrable Send | Tagged Send, RMA, Atomic, Deferrable Send |
| | CMS | NSCC, RCCC | NSCC, RCCC | NSCC, RCCC |
| **Scale** | Max Endpoints | ≤5K (≤625/rail) | 5K-10K (625-1.25K/rail) | 10K-93K (1.25K-11.6K/rail) |
| | Topology | Fat-Tree or Fat-Tree Rail | Fat-Tree or Fat-Tree Rail | Fat-Tree Rail |
| **Interoperability** | Mode | Homogeneous | Homogeneous | Homogeneous or Heterogeneous (island) |
| | Ethernet Compat | UE standard compliant | UE standard compliant | UE standard compliant |
| | CN5000/CN6000 | No | No | No |
| **Value-Add: Performance** | Link Behavior | Lossless (CBFC, LLR) | Lossless (CBFC, LLR) | Lossless (CBFC, LLR) |
| | Message Rate | 4B msgs/sec bidi | 4B msgs/sec bidi | 4B msgs/sec bidi |
| | Latency (hop) | ≤250ns | ≤250ns | ≤250ns |
| **Value-Add: Routing** | SDR/Packet Spray | ✓ | ✓ | ✓ |
| | FGAR | ✓ | ✓ | ✓ |
| | ECAR | ✓ | ✓ | ✓ |
| | Dynamic Route Recovery | ✓ | ✓ | ✓ |
| **Value-Add: Congestion Mgmt** | ECN | ✓ (UE, Ethernet, RoCE) | ✓ (UE, Ethernet, RoCE) | ✓ (UE, Ethernet, RoCE) |
| | NSCC | ✓ (lossless, lossy) | ✓ (lossless, lossy) | ✓ (lossless, lossy) |
| | RCCC | ✓ | ✓ | ✓ |
| | CSIG/CSIG+ | ✓ | ✓ | ✓ |
| **Value-Add: Collective Accel** | In-Network | ✓ (homogeneous/island) | ✓ (homogeneous/island) | ✓ (homogeneous/island) |
| **Value-Add: Advanced Topo** | Megafly | Optional | Optional | ✓ |
| | Dragonfly | ✓ | ✓ | ✓ |

---

## Scale-Up Solutions

Table: Scale-Up AI Workload Solutions {#tbl:scale-up-ai}

| Feature Category | Sub-Feature | Pod/Rack Scale | Multi-Rack Scale |
|-----------------|-------------|----------------|------------------|
| **Protocols** | Primary | UALink 200G | UALink 200G |
| | Secondary | UE (ULN variant) | UE (ULN variant) |
| | Dynamic Select | N/A | N/A |
| **Transports (UALink)** | Semantics | Memory (load/store) | Memory (load/store) |
| | DL/TL | Fixed 680B payload, VC, LLR, CBFC | Fixed 680B payload, VC, LLR, CBFC |
| | Ordering | Same-address ordering | Same-address ordering |
| **Transports (UE/ULN)** | PDS Modes | ROD, RUD | ROD, RUD |
| | CMS | RCCC | RCCC |
| **Scale** | Max Endpoints | ≤1K accelerators | ≤1K accelerators |
| | Topology | Single-tier (1-hop) | Single-tier (1-4 racks) |
| | Cable Length | <4m per link | <4m per link |
| | RTT Target | <1μs | <1μs |
| **Interoperability** | Mode | Homogeneous | Homogeneous |
| | Standards | UALink Consortium spec | UALink Consortium spec |
| **Value-Add: Performance** | Link Behavior | Lossless (CBFC or PFC) | Lossless (CBFC or PFC) |
| | Message Rate | 4B msgs/sec bidi | 4B msgs/sec bidi |
| | Latency (RTT) | Sub-μs target | Sub-μs target |
| | Bandwidth/XPU | 1.6T (8x200G lanes) | 1.6T (8x200G lanes) |
| **Value-Add: Routing** | SDR/Packet Spray | N/A | N/A |
| | FGAR | N/A | N/A |
| | ECAR | N/A | N/A |
| | Dynamic Route Recovery | N/A | N/A |
| **Value-Add: Congestion Mgmt** | ECN | N/A | N/A |
| | NSCC | N/A | N/A |
| | RCCC | ✓ (UE/ULN) | ✓ (UE/ULN) |
| | CSIG/CSIG+ | N/A | N/A |
| | Flow Control | PFC or CBFC | PFC or CBFC |
| **Value-Add: Collective Accel** | In-Network | Optional | Optional |
| **Value-Add: Advanced Topo** | Megafly | No | No |
| | Dragonfly | No | No |

> **Note:** Cornelis does not currently have a scale-up NIC or embedded accelerator HFI. Scale-up solutions assume different endpoint vendors connecting to Cornelis switches.

---

Table: Scale-Up HPC Workload Solutions {#tbl:scale-up-hpc}

| Feature Category | Sub-Feature | Pod/Rack Scale | Multi-Rack Scale |
|-----------------|-------------|----------------|------------------|
| **Protocols** | Primary | UE (ULN) | UE (ULN) |
| | Secondary | OPA (homogeneous) | OPA (homogeneous) |
| | Dynamic Select | ✓ (OPA, UE, Ethernet, RoCE) | ✓ (OPA, UE, Ethernet, RoCE) |
| **Transports (UE/ULN)** | PDS Modes | ROD, RUD | ROD, RUD |
| | SES | RMA, Tagged Send | RMA, Tagged Send |
| | CMS | RCCC, NSCC | RCCC, NSCC |
| **Scale** | Max Endpoints | ≤1K compute nodes | ≤1K compute nodes |
| | Topology | Single-tier, all-to-all | Single-tier, 1-4 racks |
| | Cable Length | <4m | <4m |
| | RTT Target | <1μs | <1μs |
| **Interoperability** | Mode | Homogeneous | Homogeneous |
| | Standards | UE HPC profile | UE HPC profile |
| **Value-Add: Performance** | Link Behavior | Lossless (CBFC, LLR) | Lossless (CBFC, LLR) |
| | Message Rate | 4B msgs/sec bidi | 4B msgs/sec bidi |
| | Latency (RTT) | Sub-μs target | Sub-μs target |
| | Bandwidth/Node | 1.6T (aggregated) | 1.6T (aggregated) |
| **Value-Add: Routing** | SDR/Packet Spray | N/A | N/A |
| | FGAR | N/A | N/A |
| | ECAR | N/A | N/A |
| | Dynamic Route Recovery | N/A | N/A |
| **Value-Add: Congestion Mgmt** | ECN | ✓ | ✓ |
| | NSCC | ✓ (lossless, lossy) | ✓ (lossless, lossy) |
| | RCCC | ✓ | ✓ |
| | CSIG/CSIG+ | Optional | Optional |
| **Value-Add: Collective Accel** | In-Network | ✓ (homogeneous/island) | ✓ (homogeneous/island) |
| **Value-Add: Advanced Topo** | Megafly | No | No |
| | Dragonfly | No | No |

> **Note:** Cornelis does not currently have a scale-up NIC or embedded accelerator HFI. Scale-up solutions assume different endpoint vendors connecting to Cornelis switches.

---

## Feature Coexistence Rules

### **Scale-Out Mandatory Combinations:**

1. **UE+ Protocol** → Requires: CBFC + LLR + (NSCC or RCCC) + CSIG capability
2. **Large Scale Deployments** → Requires: FGAR + CSIG+ + Fat-Tree Rail topology
3. **Heterogeneous (island) Interop** → Requires: Standard UE (not UE+) + UE-compliant congestion control
4. **Dynamic Protocol Selection** → Requires: Homogeneous Cornelis deployment

### **Scale-Up Mandatory Combinations:**

1. **UALink (Scale-Up AI)** → Requires: CBFC (or PFC) + LLR + Single-tier topology + Memory semantics
2. **UE/ULN (Scale-Up HPC)** → Requires: RCCC + Sub-μs RTT + CBFC + Single-tier topology
3. **Collective Acceleration** → Requires: Homogeneous/island deployment

### **Mutually Exclusive Configurations:**

- **Scale-Out** ⊕ **Scale-Up** on same switch instance (different deployment models)
- **Dynamic protocol selection** ⊕ **Heterogeneous (island)** (dynamic selection only for homogeneous Cornelis)
- **Advanced Topologies (Megafly/Dragonfly)** ⊕ **Scale-Up** (Scale-Up uses single-tier only)
- **Advanced Topologies (Megafly/Dragonfly)** ⊕ **Scale-Out AI** (HPC only)

---

## Feature Applicability by Solution

Table: Feature Applicability by Solution {#tbl:feature-applicability}

| Feature Category | Sub-Feature | Scale-Out AI | Scale-Out HPC | Scale-Up AI | Scale-Up HPC |
|-----------------|-------------|--------------|---------------|-------------|--------------|
| **Protocols** | UE+, UE, Ethernet | ✓ | ✓ | — | ✓ (ULN) |
| | OPA 16B | — | ✓ | — | ✓ |
| | UALink | — | — | ✓ | — |
| | RoCE | ✓ (interop) | ✓ (interop) | — | ✓ (interop) |
| | Dynamic Select | ✓ | ✓ | — | ✓ |
| **Transports (UE)** | PDS Modes | ✓ | ✓ | ✓ (subset) | ✓ (subset) |
| | SES | ✓ | ✓ | — | ✓ (subset) |
| | CMS | ✓ | ✓ | ✓ (RCCC) | ✓ |
| **Transports (UALink)** | Memory Semantics | — | — | ✓ | — |
| **Scale** | >10K Endpoints | ✓ | ✓ | — | — |
| | ≤1K Endpoints | ✓ | ✓ | ✓ | ✓ |
| | Multi-tier Topology | ✓ | ✓ | — | — |
| | Single-tier Topology | ✓ | ✓ | ✓ | ✓ |
| **Interoperability** | Homogeneous | ✓ | ✓ | ✓ | ✓ |
| | Heterogeneous (island) | ✓ (Large+) | ✓ (Large) | — | — |
| **Value-Add: Performance** | Lossless (CBFC, LLR) | ✓ | ✓ | ✓ | ✓ |
| | 4B msgs/sec bidi | ✓ | ✓ | ✓ | ✓ |
| | ≤250ns hop latency | ✓ | ✓ | — | — |
| | Sub-μs RTT | — | — | ✓ | ✓ |
| **Value-Add: Routing** | SDR/Packet Spray | ✓ | ✓ | — | — |
| | FGAR | ✓ | ✓ | — | — |
| | ECAR | ✓ | ✓ | — | — |
| | Dynamic Route Recovery | ✓ | ✓ | — | — |
| **Value-Add: Congestion Mgmt** | ECN | ✓ | ✓ | — | ✓ |
| | NSCC | ✓ | ✓ | — | ✓ |
| | RCCC | ✓ | ✓ | ✓ | ✓ |
| | CSIG/CSIG+ | ✓ | ✓ | — | Optional |
| **Value-Add: Collective Accel** | In-Network | ✓ | ✓ | Optional | ✓ |
| **Value-Add: Advanced Topo** | Megafly | — | ✓ | — | — |
| | Dragonfly | — | ✓ | — | — |

---

## Key Differentiators by Solution Type

Table: Key Differentiators by Solution Type {#tbl:key-differentiators}

| Dimension | Scale-Out AI | Scale-Out HPC | Scale-Up AI | Scale-Up HPC |
|-----------|--------------|---------------|-------------|--------------|
| **Primary Goal** | Maximize GPU utilization, collective performance | Balanced latency/bandwidth/message rate | Ultra-low latency, memory semantics | Low-latency RDMA within pod |
| **Primary Protocol** | UE+, UE, Ethernet | OPA 16B, UE+, UE | UALink | UE (ULN) |
| **Packet Size** | Variable MTU | Variable MTU | Fixed 680B (UALink) | Variable MTU |
| **Max Scale** | 1.44M endpoints | 93K endpoints | ≤1K accelerators | ≤1K compute nodes |
| **Topology** | Fat-Tree, Fat-Tree Rail | Fat-Tree, Fat-Tree Rail, Megafly, Dragonfly | Single-tier | Single-tier |
| **Routing Complexity** | High (multi-tier, adaptive) | High (multi-tier, adaptive) | None (single-tier) | None (single-tier) |
| **Congestion Strategy** | NSCC + RCCC | NSCC + RCCC | RCCC (UE/ULN) | NSCC + RCCC |
| **Telemetry** | CSIG/CSIG+ | CSIG/CSIG+ | N/A | Optional |
| **Collective Offload** | ✓ (homogeneous/island) | ✓ (homogeneous/island) | Optional | ✓ (homogeneous/island) |
| **Interoperability** | Homogeneous or Heterogeneous (island) | Homogeneous or Heterogeneous (island) | Homogeneous | Homogeneous |

---

**References:**
- CN7000 Switch Requirements (Landing Zone)
- CN7000 HFI Requirements (Landing Zone)  
- UEC Transport Specifications (PDS, SES, CMS)
- UALink Consortium Specifications
- CN7000 Features Documentation

---

## Glossary

**bidi** - Bidirectional. Indicates that a metric (e.g., message rate) applies to both transmit and receive directions combined.

**CBFC** - Credit-Based Flow Control. A lossless flow control mechanism that uses credits to manage buffer space and prevent packet drops.

**CMS** - Congestion Management Service. UE transport layer service for congestion detection and response.

**CSIG/CSIG+** - Congestion Signaling. Telemetry mechanism for communicating congestion state (2B/4B/6B variants).

**ECAR** - Entropy Controlled Adaptive Routing. Routing algorithm that uses entropy-based path selection to balance load.

**ECN** - Explicit Congestion Notification. Standard mechanism for signaling network congestion to endpoints.

**FGAR** - Fine-Grained Adaptive Routing. Telemetry-based adaptive routing for optimal path selection.

**LLR** - Link-Level Retry. Mechanism for retransmitting corrupted or lost packets at the link layer.

**NSCC** - Network-Side Congestion Control. Congestion control mechanism supporting both lossless and lossy modes.

**OPA** - Omni-Path Architecture. Cornelis proprietary high-performance fabric protocol.

**PDS** - Packet Delivery Service. UE transport layer service defining delivery semantics (RUD, ROD, RUDI, UUD).

**RCCC** - Receiver Credit-based Congestion Control. Congestion control using receiver-side credit management.

**RMA** - Remote Memory Access. One-sided communication operations for direct memory access.

**ROD** - Reliable Ordered Delivery. PDS mode guaranteeing in-order packet delivery.

**RoCE** - RDMA over Converged Ethernet. Standard for RDMA operations over Ethernet networks.

**RUD** - Reliable Unordered Delivery. PDS mode guaranteeing delivery without ordering constraints.

**RUDI** - Reliable Unordered Delivery with Immediate data. RUD variant with immediate data support.

**SDR** - Source-based Deterministic Routing. Static routing determined at the source endpoint.

**SES** - Send/Event Service. UE transport layer service for messaging semantics (Tagged Send, RMA, Atomic).

**UALink** - Ultra Accelerator Link. Consortium-defined standard for accelerator interconnect with memory semantics.

**UE** - Ultra Ethernet. Industry-standard high-performance Ethernet protocol for HPC/AI workloads.

**UE+** - Ultra Ethernet Plus. Cornelis-enhanced UE with additional performance features.

**ULN** - Ultra Local Network. UE variant optimized for scale-up, low-latency deployments.

**UUD** - Unreliable Unordered Delivery. PDS mode with best-effort delivery semantics.