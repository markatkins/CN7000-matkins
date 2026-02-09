# LNR Switch Performance Requirements Gap Analysis

**Document ID:** LNR-PERF-GAP-2026-01  
**Date:** 2026-01-23  
**Author:** AI Analysis Agent  
**Status:** Draft  

---

## 1. Executive Summary

This report presents a comprehensive gap analysis comparing the LNR (Lightning River) Switch performance requirements documented in the machine-processable datamodel (`datamodel/requirements/lnr/performance.yaml`) against the authoritative source document (`docs/references/requirements/Switch/CN7000 Switch Requirements.md`, §4 Performance Requirements).

### Key Findings

| Metric | Count |
|--------|-------|
| Requirements in Datamodel | 4 |
| Requirements in Source (§4) | 18+ |
| Identified Gaps | 23 |
| Resolved Conflicts | 3 |
| Resolved Ambiguities | 4 |
| Estimated New Requirements Needed | ~26 |

### Coverage Assessment

The current datamodel captures approximately **15-20%** of the performance requirements specified in the source document. Significant gaps exist in:

- UALink-specific performance requirements
- Congestion management (incast, FGAR, CSIG)
- Collective operations (AllReduce, AllToAll, AllGather, ReduceScatter)
- Industry benchmark compliance (GPCNeT, OSU, NCCL)
- Bandwidth ramp and efficiency requirements

---

## 2. Scope and Methodology

### 2.1 Scope

This analysis covers:

- **Source Document:** `docs/references/requirements/Switch/CN7000 Switch Requirements.md`
  - Section: §4 Performance Requirements (lines 1249-1950)
  - Subsections: §4.1 Overview, §4.2 Technical Analysis, §4.3 Requirements Tables
  
- **Datamodel:** `datamodel/requirements/lnr/performance.yaml`
  - Requirements: LNR-PERF-001 through LNR-PERF-004

### 2.2 Methodology

1. **Document Review:** Comprehensive reading of both source and datamodel
2. **Cross-Reference Mapping:** Alignment of datamodel requirements to source requirement IDs
3. **Gap Identification:** Requirements in source not captured in datamodel
4. **Conflict Detection:** Inconsistencies between source and datamodel values
5. **Ambiguity Analysis:** Unclear or incomplete requirement statements
6. **Stakeholder Clarification:** Resolution of conflicts and ambiguities through discussion

### 2.3 Reference Documents

| Document | Location | Purpose |
|----------|----------|---------|
| CN7000 Switch Requirements | `docs/references/requirements/Switch/CN7000 Switch Requirements.md` | Source of truth for requirements |
| LNR Performance YAML | `datamodel/requirements/lnr/performance.yaml` | Machine-processable requirements |
| Requirements AGENTS.md | `datamodel/requirements/AGENTS.md` | EARS methodology and ID allocation |
| LNR Landing Zone | `docs/references/LNR.md` | Architecture reference |

---

## 3. Cross-Reference Mapping

### 3.1 Existing Datamodel Requirements

| Datamodel ID | Source ID | Topic | Match Status |
|--------------|-----------|-------|--------------|
| LNR-PERF-001 | PERF-1A | Port-to-port latency ≤200ns | **MATCH** (datamodel authoritative) |
| LNR-PERF-002 | PERF-2A | 1.6 Tbps per port, 72 ports | **MATCH** (datamodel authoritative) |
| LNR-PERF-003 | PERF-6 | Adaptive routing within 1μs | Partial match |
| LNR-PERF-004 | N/A | CE base latency <1μs | **NEEDS UPDATE** - scope clarification |

### 3.2 Source Requirements Table (§4.3.1)

The source document defines 18 performance requirements (PERF-1A through PERF-18):

| Source ID | Description | Datamodel Coverage |
|-----------|-------------|-------------------|
| PERF-1A | Native port latency ≤195ns | LNR-PERF-001 (≤200ns) |
| PERF-1B | UALink station latency ≤196ns | **GAP** |
| PERF-1C | Alternate configuration latency table | **GAP** |
| PERF-2A | Native port bandwidth 1.6Tb/s | LNR-PERF-002 |
| PERF-2B | UALink station bandwidth 800Gb/s | **GAP** |
| PERF-2C | Subdivided port bandwidth | **GAP** |
| PERF-3 | Incast handling ≥95% @ 32:1 | **GAP** |
| PERF-4 | Jitter <5% normal load | **GAP** |
| PERF-5 | Victim protection ≥95% | **GAP** |
| PERF-6 | FGAR within 1 RTT | LNR-PERF-003 (partial) |
| PERF-7 | Ultra Ethernet CSIG | **GAP** |
| PERF-8A | AllReduce large message BW | **GAP** |
| PERF-8B | Simultaneous AllReduce | **GAP** |
| PERF-9 | AllReduce small message latency | **GAP** |
| PERF-10 | Message rate 4B msg/s | **GAP** |
| PERF-11 | Congested message rate | **GAP** |
| PERF-12 | GPCNeT benchmark | **GAP** |
| PERF-13 | Bisection BW (static) | **GAP** |
| PERF-14 | Bisection BW (FGAR) | **GAP** |
| PERF-15A/B | AllToAll performance | **GAP** |
| PERF-16A/B | AllGather performance | **GAP** |
| PERF-17A/B | ReduceScatter performance | **GAP** |
| PERF-18 | ReduceScatter small message | **GAP** |

---

## 4. Gap Analysis

### 4.1 Critical Gaps

These gaps represent fundamental performance requirements that must be captured in the datamodel.

| Gap ID | Source ID | Description | Source Reference |
|--------|-----------|-------------|------------------|
| GAP-01 | PERF-1B | UALink latency ≤196ns for 4x200Gbps station | §4.3.1, line 1873 |
| GAP-02 | PERF-2B | UALink bandwidth 800Gb/s per station | §4.3.1, line 1876 |
| GAP-03 | PERF-3 | Incast handling: ≥95% egress BW under 32:1 | §4.3.1, line 1878 |
| GAP-04 | PERF-10 | Message rate: 4B msg/s bidirectional per port | §4.3.1, line 1886 |

### 4.2 High-Priority Gaps

These gaps represent important performance characteristics for competitive positioning.

| Gap ID | Source ID | Description | Source Reference |
|--------|-----------|-------------|------------------|
| GAP-05 | PERF-1C | Latency for alternate configurations (table) | §4.3.1, line 1874 |
| GAP-06 | PERF-2C | Subdivided port bandwidth adjustments | §4.3.1, line 1877 |
| GAP-07 | PERF-4 | Jitter: <5% variation under normal load | §4.3.1, line 1879 |
| GAP-08 | PERF-5 | Victim protection: ≥95% BW for non-congested ports | §4.3.1, line 1880 |
| GAP-09 | PERF-7 | Ultra Ethernet CSIG congestion management | §4.3.1, line 1882 |
| GAP-10 | PERF-8A | AllReduce: 1.6Tb/s per port for ≥4MiB messages | §4.3.1, line 1883 |
| GAP-11 | PERF-8B | Simultaneous AllReduce: 800Gb/s each | §4.3.1, line 1884 |
| GAP-12 | PERF-9 | AllReduce latency: ≤10μs for ≤1KB messages | §4.3.1, line 1885 |
| GAP-13 | PERF-11 | Congested message rate: ≥95% of peak | §4.3.1, line 1887 |
| GAP-14 | PERF-13 | Bisection BW (static): ≥55% available | §4.3.1, line 1889 |
| GAP-15 | PERF-14 | Bisection BW (FGAR): ≥85% available | §4.3.1, line 1890 |
| GAP-16 | PERF-15A/B | AllToAll: 1.6Tb/s, ≥50% under congestion | §4.3.1, lines 1891-1892 |
| GAP-17 | PERF-16A/B | AllGather: 1.6Tb/s, ≥90% under congestion | §4.3.1, lines 1893-1894 |
| GAP-18 | PERF-17A/B | ReduceScatter: 1.6Tb/s, ≥90% under congestion | §4.3.1, lines 1895-1896 |
| GAP-19 | §4.2.1 | Bandwidth ramp: 50%/90%/100% by packet size | §4.2.1, lines 1337-1340 |

### 4.3 Medium-Priority Gaps

These gaps represent benchmark compliance and efficiency requirements.

| Gap ID | Source ID | Description | Source Reference |
|--------|-----------|-------------|------------------|
| GAP-20 | PERF-12 | GPCNeT benchmark targets | §4.3.1, line 1888 |
| GAP-21 | PERF-18 | ReduceScatter latency: ≤10μs for ≤1KB | §4.3.1, line 1897 |
| GAP-22 | §4.2.1 | Crossbar speedup: 50% target | §4.2.1, lines 1386-1398 |
| GAP-23 | §4.2.9 | Sawtooth efficiency: ≥90% average | §4.2.9, lines 1787-1817 |

### 4.4 Conceptual Gaps

The source document defines congestion concepts (§4.2.2) that should be captured in the datamodel:

| Concept | Definition | Source Reference |
|---------|------------|------------------|
| Root Port | Egress port with credits but multiple competing ingress ports | §4.2.2, line 1410 |
| Victim Port | Egress port with no credits due to back pressure | §4.2.2, line 1412 |
| Starved Flow | Flow blocked by a victim, not common to the root | §4.2.2, line 1413 |
| Congesting Flow | Flow saturating target link at 90-100% capacity | §4.2.2, line 1414 |
| Victim Flow | Latency-sensitive flow sharing congested resource | §4.2.2, line 1415 |
| Elephant Flow | Large, long-running stream consuming disproportionate resources | §4.2.2, line 1416 |

---

## 5. Conflict Resolution

Three conflicts were identified and resolved through stakeholder discussion.

### 5.1 CONF-01: Latency Target (RESOLVED)

| Attribute | Datamodel | Source | Resolution |
|-----------|-----------|--------|------------|
| Latency | ≤200ns | ≤195ns | **Datamodel authoritative** |
| Rationale | - | - | Source document is out-of-date |

### 5.2 CONF-02: Port Count (RESOLVED)

| Attribute | Datamodel | Source | Resolution |
|-----------|-----------|--------|------------|
| Port Count | 72 ports | 64 ports | **Datamodel authoritative** |
| Rationale | - | - | Source document is out-of-date |

### 5.3 CONF-03: Collective Latency Scope (RESOLVED)

| Attribute | LNR-PERF-004 | Source PERF-9 | Resolution |
|-----------|--------------|---------------|------------|
| Metric | CE base latency | Benchmark latency | **Different scope - both valid** |
| Target | <1μs | ≤10μs for ≤1KB | Both requirements needed |
| Scope | First byte through CE | End-to-end NCCL operation | Clarify LNR-PERF-004 scope |

**LNR-PERF-004 Clarification:**
- Measures: Time for first byte of collective data to flow from input to CE processing, OR from one CE result to another CE for processing
- Conditions: Both operands arrive simultaneously, no congestion
- This is a hardware/architecture requirement, distinct from benchmark requirements

---

## 6. Ambiguity Resolution

Four ambiguities were identified and resolved.

| ID | Topic | Issue | Resolution |
|----|-------|-------|------------|
| AMB-01 | LNR-PERF-001 "cut-through forwarding" | No packet size specified | **No change needed** - measures first-byte latency; not enforced for store-and-forward |
| AMB-02 | LNR-PERF-003 "congestion is detected" | No definition | **Deferred** - congestion concepts to be defined in datamodel (WP-20) |
| AMB-03 | LNR-PERF-004 "sub-microsecond" | Vague target | **Clarified** - CE base latency scope documented |
| AMB-04 | PERF-6 "within 1 RTT" | RTT undefined | **Resolved** - RTT = Round Trip Time (standard networking term) |

---

## 7. Key Decisions

| Decision ID | Topic | Decision | Rationale |
|-------------|-------|----------|-----------|
| DEC-01 | Latency target | Datamodel authoritative (≤200ns) | Source out-of-date |
| DEC-02 | Port count | Datamodel authoritative (72 ports) | Source out-of-date |
| DEC-03 | Collective latency | Different scope - both valid | LNR-PERF-004 = CE base latency; PERF-9 = benchmark latency |
| DEC-04 | Cut-through wording | No change needed | Measures first-byte latency; not enforced for store-and-forward |
| DEC-05 | Congestion definition | Define later in datamodel | Add as work item WP-20 |
| DEC-06 | RTT definition | RTT = Round Trip Time | Standard networking term |
| DEC-07 | UALink architecture | 72-port native, subdividable | 144 links @ 800G, 288 @ 400G, 576 @ 200G |

---

## 8. UALink Architecture Clarification

The datamodel should reflect the native 72-port 1.6 Tbps architecture with UALink subdivision support:

| Configuration | Port Speed | Lane Config | Total Links | Notes |
|---------------|------------|-------------|-------------|-------|
| Native | 1.6 Tbps | 8x200G | 72 | Base architecture |
| UALink 4-lane | 800 Gbps | 4x200G | 144 | 2:1 subdivision |
| UALink 2-lane | 400 Gbps | 2x200G | 288 | 4:1 subdivision |
| UALink 1-lane | 200 Gbps | 1x200G | 576 | 8:1 subdivision |

This differs from the source document which specifies 64 native ports. The datamodel's 72-port architecture is authoritative.

---

## 9. Key Performance Features

The source document identifies the following key performance features that should be reflected in the datamodel:

### 9.1 Port-to-Port Performance
- Base latency ≤200ns (cut-through, RS-544 FEC) - **In datamodel**
- 1.6 Tbps sustained bidirectional per port - **In datamodel**
- 4 billion messages/second bidirectional per port - **GAP**
- Jitter <5% under normal load, <10% under incast - **GAP**

### 9.2 Congestion Management
- FGAR (Fine-Grained Adaptive Routing) with telemetry - **Partial in datamodel**
- Ultra Ethernet CSIG support - **GAP**
- Incast handling (≥95% at 32:1, ≥90% at 64:1) - **GAP**
- Victim port protection - **GAP**

### 9.3 Collective Operations
- AllReduce, AllToAll, AllGather, ReduceScatter - **GAP**
- 1.6 Tbps per port for large messages (≥4MiB) - **GAP**
- ≤10μs latency for small messages (≤1KB) - **GAP**
- Simultaneous collective support - **GAP**
- CE base latency <1μs - **In datamodel (needs clarification)**

### 9.4 UALink Performance
- 800 Gbps per station (4x200G) at 144 links - **GAP**
- Subdividable to 400 Gbps (288 links) and 200 Gbps (576 links) - **GAP**
- ≤196ns latency (512-lane switch: <300ns spec) - **GAP**

### 9.5 Industry Benchmarks
- GPCNeT compliance - **GAP**
- OSU/IMB benchmark targets - **GAP**
- NCCL test targets - **GAP**

---

## 10. Recommendations

### 10.1 Immediate Actions (Critical)

1. **Update LNR-PERF-004** to clarify CE base latency scope
2. **Add UALink requirements** (LNR-PERF-005, LNR-PERF-006)
3. **Add incast handling** (LNR-PERF-007)
4. **Add message rate** (LNR-PERF-008)

### 10.2 Short-Term Actions (High Priority)

1. Add remaining performance requirements (LNR-PERF-009 through LNR-PERF-026)
2. Add congestion concept definitions to datamodel
3. Ensure all requirements follow EARS methodology

### 10.3 Medium-Term Actions

1. Add benchmark compliance requirements
2. Add efficiency requirements (speedup, sawtooth)
3. Update source document to align with datamodel (latency, port count, UALink architecture)

### 10.4 Validation

After implementing the work plan:
1. Run `cmake --build build --target validate-requirements`
2. Generate traceability matrix
3. Review for completeness against source document

---

## 11. Appendices

### Appendix A: Work Plan Reference

See companion document: `lnr-performance-work-plan.md`

### Appendix B: Prompts Used

See companion document: `prompts/lnr-performance-analysis.md`

### Appendix C: Source Document Line References

| Section | Lines | Content |
|---------|-------|---------|
| §4 Overview | 1249-1295 | Performance overview and targets |
| §4.2.1 Port-to-Port | 1300-1404 | Latency, bandwidth, message rate, jitter, speedup |
| §4.2.2 Congestion | 1406-1466 | Congestion concepts, incast, FGAR, CSIG |
| §4.2.3 UALink | 1522-1559 | UALink-specific performance |
| §4.2.4 Collectives | 1560-1599 | Collective operations acceleration |
| §4.2.5 Benchmarks | 1600-1688 | Industry standard benchmarks |
| §4.2.6 Subdivision | 1689-1738 | Subdivision performance considerations |
| §4.2.7 Speed Change | 1740-1762 | Speed change considerations |
| §4.2.8 Store-and-Forward | 1763-1785 | Store-and-forward considerations |
| §4.2.9 Sawtooth | 1787-1851 | Crossbar bandwidth efficiency |
| §4.2.10 L3 Router | 1852-1865 | L3 router support considerations |
| §4.3.1 Requirements Table | 1866-1898 | Performance requirements table |
| §4.3.2 Verification Table | 1928-1950 | Verification methods table |

---

**Document History:**

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-01-23 | AI Analysis Agent | Initial draft |
