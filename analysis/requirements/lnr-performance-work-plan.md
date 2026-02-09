# LNR Switch Performance Requirements Work Plan

**Document ID:** LNR-PERF-WP-2026-01  
**Date:** 2026-01-23  
**Author:** AI Analysis Agent  
**Status:** Draft  
**Related:** `lnr-performance-gap-analysis.md`

---

## 1. Overview

This work plan addresses the gaps, conflicts, and ambiguities identified in the LNR Performance Requirements Gap Analysis. The plan is organized into six phases with prioritized work items.

### Summary Statistics

| Category | Count |
|----------|-------|
| Total Work Items | 27 |
| Critical Priority | 5 |
| High Priority | 15 |
| Medium Priority | 4 |
| Low Priority | 3 |
| Estimated New Requirements | ~26 (LNR-PERF-005 through LNR-PERF-030) |

---

## 2. Work Item Status Legend

| Status | Description |
|--------|-------------|
| `NOT_STARTED` | Work item not yet begun |
| `IN_PROGRESS` | Work item actively being worked |
| `BLOCKED` | Work item blocked by dependency or issue |
| `REVIEW` | Work item complete, awaiting review |
| `COMPLETE` | Work item finished and verified |

---

## 3. Phase 1: Update Existing Requirements

**Priority:** Critical  
**Objective:** Clarify and correct existing datamodel requirements

| Task ID | Description | Source Ref | Effort | Status | Assignee | Notes |
|---------|-------------|------------|--------|--------|----------|-------|
| WP-01 | Update LNR-PERF-004 statement to clarify CE base latency scope | CONF-03 | Low | `NOT_STARTED` | | Clarify: first byte from input to CE processing, or CE-to-CE, assuming simultaneous operand arrival and no congestion |

### WP-01 Details

**Current Statement (LNR-PERF-004):**
> "Hardware-accelerated collective operations with sub-microsecond latency"

**Proposed Statement:**
> "The switch shall provide hardware-accelerated collective operations where the base latency for the first byte of collective data to flow from an input port to a collective engine, or from one collective engine result to another collective engine, shall be less than 1 microsecond, assuming both operands arrive simultaneously and without encountering congestion."

**EARS Pattern:** Ubiquitous (The <system> shall <action>)

---

## 4. Phase 2: Fill Critical Gaps

**Priority:** Critical  
**Objective:** Add fundamental performance requirements missing from datamodel

| Task ID | Description | Source Ref | Effort | Status | Assignee | Notes |
|---------|-------------|------------|--------|--------|----------|-------|
| WP-02 | Add LNR-PERF-005: UALink latency | PERF-1B | Medium | `NOT_STARTED` | | Based on 72-port architecture |
| WP-03 | Add LNR-PERF-006: UALink bandwidth | PERF-2B | Medium | `NOT_STARTED` | | 800 Gbps @ 144 links, subdividable to 288/576 |
| WP-04 | Add LNR-PERF-007: Incast handling | PERF-3 | Medium | `NOT_STARTED` | | ≥95% egress BW under 32:1 incast |
| WP-05 | Add LNR-PERF-008: Message rate | PERF-10 | Medium | `NOT_STARTED` | | 4B msg/s bidirectional per port |

### WP-02 Details: UALink Latency (LNR-PERF-005)

**Proposed Requirement:**

```yaml
- id: "LNR-PERF-005"
  type: "non_functional"
  ears_pattern: "ubiquitous"
  statement: "The switch shall maintain port-to-port latency of 200 nanoseconds or less for UALink stations configured at 4x200Gbps (800 Gbps) with a 64-byte packet."
  rationale: "UALink performance must match native port latency characteristics to support scale-up AI/ML workloads."
  status: "proposed"
  
  source:
    document: "docs/references/requirements/Switch/CN7000 Switch Requirements.md"
    section: "§4.2.3 UALink Performance"
    original_id: "PERF-1B"
  
  verification:
    method: "perf_test"
    platform: "system"
    criteria: "Measured latency ≤200ns for 64B packets at 4x200Gbps UALink configuration"
  
  attributes:
    priority: "critical"
    stability: "stable"
    risk: "medium"
    competitive: "differentiator"
  
  tags: ["performance", "latency", "ualink"]
```

### WP-03 Details: UALink Bandwidth (LNR-PERF-006)

**Proposed Requirement:**

```yaml
- id: "LNR-PERF-006"
  type: "non_functional"
  ears_pattern: "ubiquitous"
  statement: "The switch shall support 800 Gbps bandwidth per UALink station in each direction, with 144 total UALink stations when configured at 4x200Gbps, subdividable to 288 stations at 2x200Gbps (400 Gbps) or 576 stations at 1x200Gbps (200 Gbps)."
  rationale: "UALink subdivision enables flexible scale-up configurations for diverse AI/ML deployment scenarios."
  status: "proposed"
  
  source:
    document: "docs/references/requirements/Switch/CN7000 Switch Requirements.md"
    section: "§4.2.3 UALink Performance"
    original_id: "PERF-2B"
  
  verification:
    method: "perf_test"
    platform: "system"
    criteria: "Sustained 800 Gbps bidirectional per station at 4x200G; proportional bandwidth at subdivided configurations"
  
  attributes:
    priority: "critical"
    stability: "stable"
    risk: "medium"
    competitive: "differentiator"
  
  tags: ["performance", "bandwidth", "ualink", "subdivision"]
```

### WP-04 Details: Incast Handling (LNR-PERF-007)

**Proposed Requirement:**

```yaml
- id: "LNR-PERF-007"
  type: "non_functional"
  ears_pattern: "state_driven"
  statement: "While processing 32:1 incast traffic, the switch shall maintain at least 95% egress bandwidth."
  rationale: "Incast patterns are common in AI/ML training workloads and must not cause significant bandwidth degradation."
  status: "proposed"
  
  source:
    document: "docs/references/requirements/Switch/CN7000 Switch Requirements.md"
    section: "§4.3.1 Performance Requirements Table"
    original_id: "PERF-3"
  
  verification:
    method: "perf_test"
    platform: "system"
    criteria: "Measured egress bandwidth ≥95% of line rate under 32:1 incast pattern"
  
  attributes:
    priority: "critical"
    stability: "stable"
    risk: "high"
    competitive: "differentiator"
  
  tags: ["performance", "bandwidth", "congestion", "incast"]
```

### WP-05 Details: Message Rate (LNR-PERF-008)

**Proposed Requirement:**

```yaml
- id: "LNR-PERF-008"
  type: "non_functional"
  ears_pattern: "ubiquitous"
  statement: "The switch shall maintain 4 billion messages per second bidirectional per port."
  rationale: "High message rate is critical for HPC and AI/ML workloads with small message communication patterns."
  status: "proposed"
  
  source:
    document: "docs/references/requirements/Switch/CN7000 Switch Requirements.md"
    section: "§4.3.1 Performance Requirements Table"
    original_id: "PERF-10"
  
  verification:
    method: "perf_test"
    platform: "system"
    criteria: "Measured message rate ≥4B msg/s bidirectional with 64B packets"
  
  attributes:
    priority: "critical"
    stability: "stable"
    risk: "medium"
    competitive: "parity"
  
  tags: ["performance", "message-rate"]
```

---

## 5. Phase 3: Fill High-Priority Gaps

**Priority:** High  
**Objective:** Add important performance characteristics for competitive positioning

| Task ID | Description | Source Ref | Effort | Status | Assignee | Notes |
|---------|-------------|------------|--------|--------|----------|-------|
| WP-06 | Add LNR-PERF-009: Jitter requirements | PERF-4 | Medium | `NOT_STARTED` | | <5% normal load, <10% incast |
| WP-07 | Add LNR-PERF-010: Victim protection | PERF-5 | Medium | `NOT_STARTED` | | ≥95% BW for non-congested ports |
| WP-08 | Add LNR-PERF-011: CSIG support | PERF-7 | Medium | `NOT_STARTED` | | Ultra Ethernet congestion signaling |
| WP-09 | Add LNR-PERF-012: AllReduce large message BW | PERF-8A | Medium | `NOT_STARTED` | | 1.6Tb/s per port for ≥4MiB |
| WP-10 | Add LNR-PERF-013: Simultaneous AllReduce | PERF-8B | Medium | `NOT_STARTED` | | 800Gb/s each for 2 simultaneous |
| WP-11 | Add LNR-PERF-014: AllReduce benchmark latency | PERF-9 | Medium | `NOT_STARTED` | | ≤10μs for ≤1KB messages |
| WP-12 | Add LNR-PERF-015: Congested message rate | PERF-11 | Medium | `NOT_STARTED` | | ≥95% of peak under congestion |
| WP-13 | Add LNR-PERF-016: Bisection BW (static) | PERF-13 | Medium | `NOT_STARTED` | | ≥55% available |
| WP-14 | Add LNR-PERF-017: Bisection BW (FGAR) | PERF-14 | Medium | `NOT_STARTED` | | ≥85% available |
| WP-15 | Add LNR-PERF-018: Bandwidth ramp | §4.2.1 | Medium | `NOT_STARTED` | | 50%/90%/100% by packet size |
| WP-16 | Add LNR-PERF-019: Alternate config latency | PERF-1C | High | `NOT_STARTED` | | Table-based configurations |
| WP-17 | Add LNR-PERF-020: Subdivided port BW | PERF-2C | Medium | `NOT_STARTED` | | Proportional with adjustments |
| WP-18 | Add LNR-PERF-021/022: AllToAll performance | PERF-15A/B | Medium | `NOT_STARTED` | | 1.6Tb/s, ≥50% under congestion |
| WP-19 | Add LNR-PERF-023/024: AllGather performance | PERF-16A/B | Medium | `NOT_STARTED` | | 1.6Tb/s, ≥90% under congestion |
| WP-20 | Add LNR-PERF-025/026: ReduceScatter performance | PERF-17A/B | Medium | `NOT_STARTED` | | 1.6Tb/s, ≥90% under congestion |
| WP-21 | Add congestion concepts definitions | §4.2.2 | Medium | `NOT_STARTED` | | Root port, victim port, etc. |

---

## 6. Phase 4: Fill Medium-Priority Gaps

**Priority:** Medium  
**Objective:** Add benchmark compliance and efficiency requirements

| Task ID | Description | Source Ref | Effort | Status | Assignee | Notes |
|---------|-------------|------------|--------|--------|----------|-------|
| WP-22 | Add LNR-PERF-027: GPCNeT benchmark | PERF-12 | Medium | `NOT_STARTED` | | Latency/BW targets |
| WP-23 | Add LNR-PERF-028: ReduceScatter small msg | PERF-18 | Low | `NOT_STARTED` | | ≤10μs for ≤1KB |
| WP-24 | Add LNR-PERF-029: Speedup requirements | §4.2.1 | Medium | `NOT_STARTED` | | 50% crossbar speedup |
| WP-25 | Add LNR-PERF-030: Sawtooth efficiency | §4.2.9 | Medium | `NOT_STARTED` | | ≥90% average efficiency |

---

## 7. Phase 5: Source Document Updates

**Priority:** Low  
**Objective:** Align source document with authoritative datamodel values

| Task ID | Description | Source Ref | Effort | Status | Assignee | Notes |
|---------|-------------|------------|--------|--------|----------|-------|
| WP-26 | Update source PERF-1A latency | DEC-01 | Low | `NOT_STARTED` | | 195ns → 200ns |
| WP-27 | Update source PERF-2A port count | DEC-02 | Low | `NOT_STARTED` | | 64 → 72 ports |
| WP-28 | Update source UALink section | DEC-07 | Medium | `NOT_STARTED` | | 144/288/576 link configurations |

---

## 8. Dependencies

```
Phase 1 (WP-01)
    │
    ▼
Phase 2 (WP-02 to WP-05) ──────────────────┐
    │                                       │
    ▼                                       │
Phase 3 (WP-06 to WP-21)                   │
    │                                       │
    ▼                                       │
Phase 4 (WP-22 to WP-25)                   │
    │                                       │
    ▼                                       │
Phase 5 (WP-26 to WP-28) ◄─────────────────┘
```

**Notes:**
- Phase 1 must complete before Phase 2 (LNR-PERF-004 clarification informs collective requirements)
- Phases 2-4 can proceed in parallel within each phase
- Phase 5 depends on Phases 1-4 completion to ensure datamodel is stable before updating source

---

## 9. Validation Checklist

After completing each phase, run the following validation:

```bash
# Validate requirements schema and EARS compliance
cmake --build build --target validate-requirements

# Generate traceability matrix
cmake --build build --target generate-traceability

# Run contract tests
ctest --test-dir build -R requirements
```

### Acceptance Criteria

| Phase | Validation | Criteria |
|-------|------------|----------|
| Phase 1 | Schema validation | LNR-PERF-004 passes EARS validation |
| Phase 2 | Schema validation | LNR-PERF-005 to 008 pass validation |
| Phase 3 | Schema validation | LNR-PERF-009 to 026 pass validation |
| Phase 4 | Schema validation | LNR-PERF-027 to 030 pass validation |
| Phase 5 | Manual review | Source document aligned with datamodel |
| All | Traceability | All new requirements traced to source |

---

## 10. Effort Estimates

| Phase | Work Items | Estimated Effort | Notes |
|-------|------------|------------------|-------|
| Phase 1 | 1 | 2 hours | Statement clarification |
| Phase 2 | 4 | 8 hours | New critical requirements |
| Phase 3 | 16 | 32 hours | New high-priority requirements |
| Phase 4 | 4 | 8 hours | New medium-priority requirements |
| Phase 5 | 3 | 4 hours | Source document updates |
| **Total** | **28** | **54 hours** | |

---

## 11. Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| EARS pattern mismatch | Medium | Low | Run validation after each requirement |
| Source document conflicts | Low | Medium | Stakeholder review before Phase 5 |
| Missing verification criteria | Medium | Medium | Reference source VM-* methods |
| ID allocation conflicts | Low | Low | Check AGENTS.md allocation status |

---

## 12. Appendix: Requirement ID Allocation

Per `datamodel/requirements/AGENTS.md`, the LNR PERF category allocation:

| Current | Next Available | Reserved Range |
|---------|----------------|----------------|
| LNR-PERF-001 to 004 | LNR-PERF-005 | LNR-PERF-001 to LNR-PERF-199 |

**Planned Allocation:**

| ID Range | Phase | Description |
|----------|-------|-------------|
| LNR-PERF-005 to 008 | Phase 2 | Critical gaps |
| LNR-PERF-009 to 026 | Phase 3 | High-priority gaps |
| LNR-PERF-027 to 030 | Phase 4 | Medium-priority gaps |

---

## 13. Appendix: Source Verification Methods

The source document defines verification methods that should be referenced:

| Method ID | Description | Applicable Requirements |
|-----------|-------------|------------------------|
| VM-LAT-1 | Measure port-to-port latency | LNR-PERF-001, 005, 019 |
| VM-LAT-2 | Measure latency variation | LNR-PERF-009 |
| VM-BW-1 | Verify bandwidth | LNR-PERF-002, 006, 018, 020 |
| VM-BW-2 | Verify bisection BW (static) | LNR-PERF-016 |
| VM-BW-3 | Verify bisection BW (FGAR) | LNR-PERF-017 |
| VM-CONG-1 | Test incast bandwidth | LNR-PERF-007 |
| VM-CONG-2 | Validate victim protection | LNR-PERF-010 |
| VM-CONG-3 | Test FGAR operation | LNR-PERF-003 |
| VM-CONG-4 | Verify CSIG implementation | LNR-PERF-011 |
| VM-COLL-1 | Measure AllReduce bandwidth | LNR-PERF-012, 013 |
| VM-COLL-2 | Measure AllReduce latency | LNR-PERF-014 |
| VM-COLL-3 | Measure AllToAll bandwidth | LNR-PERF-021, 022 |
| VM-COLL-4 | Measure AllGather bandwidth | LNR-PERF-023, 024 |
| VM-COLL-5 | Measure ReduceScatter bandwidth | LNR-PERF-025, 026 |
| VM-COLL-6 | Measure ReduceScatter latency | LNR-PERF-028 |
| VM-MSG-1 | Verify message rate | LNR-PERF-008 |
| VM-MSG-2 | Test congested message rate | LNR-PERF-015 |
| VM-GPCNET-1 | Execute GPCNeT benchmark | LNR-PERF-027 |

---

**Document History:**

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-01-23 | AI Analysis Agent | Initial draft |
