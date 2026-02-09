# Prompts Used for LNR Performance Requirements Analysis

**Document ID:** LNR-PERF-PROMPTS-2026-01  
**Date:** 2026-01-23  
**Purpose:** Document the prompts and responses used to generate the gap analysis and work plan

---

## Session Overview

This document records the prompts used during the AI-assisted analysis of LNR Switch Performance Requirements. The analysis compared the datamodel (`datamodel/requirements/lnr/performance.yaml`) against the source document (`docs/references/requirements/Switch/CN7000 Switch Requirements.md`, §4).

---

## Prompt 1: Initial Discovery

**User Prompt:**
> Where are the performance requirements for LNR and for PMR documented in the datamodel?

**Purpose:** Locate the machine-processable requirements files for both products.

**Key Findings:**
- LNR Performance: `earlysim/datamodel/requirements/lnr/performance.yaml`
- PMR Performance: `earlysim/datamodel/requirements/pmr/performance.yaml`
- Source documents referenced in metadata headers

---

## Prompt 2: Source Traceability

**User Prompt:**
> Are the original sources for the requirements documented?

**Purpose:** Verify traceability from datamodel to source documents.

**Key Findings:**
- Each YAML file includes `metadata.source_document` and `metadata.source_section`
- Each requirement includes `source.document`, `source.section`, and `source.original_id`
- Primary sources:
  - LNR: `docs/references/requirements/Switch/CN7000 Switch Requirements.md`
  - PMR: `docs/references/requirements/NIC/CN7000 HFI Requirements.md`

---

## Prompt 3: Landing Zone Documentation

**User Prompt:**
> Does early sim docs/references include landing zone documentation?

**Purpose:** Identify additional reference documentation for architecture context.

**Key Findings:**
- `docs/references/PMR.md` - PMR NIC Landing Zone
- `docs/references/LNR.md` - LNR Switch Landing Zone
- `docs/references/EC.md` - Electric Creek Common Component Landing Zone
- Landing zones provide architecture and interface specifications

---

## Prompt 4: Git History

**User Prompt:**
> who made the latest update to earlysim/docs/state_machine_taxonomy_review.md?

**Purpose:** Verify git repository location and access.

**Key Findings:**
- Git repository root: `/home/matkins/CN7000/earlysim`
- Last update by: Charles Archer <charles.archer@cornelisnetworks.com>
- Date: January 14, 2026

---

## Prompt 5: Gap Analysis Request

**User Prompt:**
> Please determine how well the LNR (Switch) Performance Requirements match those provided in the source document "CN7000 Switch Requirements.md". Identify gaps, conflicts, and ambiguities. Provide a plan to address the gaps, conflicts and ambiguities along with a Work List to track progress. Bear in mind the rules set forth in Be sure to provide references to the source document and the requirements documents; cross-reference them where they both address the same feature, parameter or performance metric. Please also identify key features described addressing performance requirements. This is in preparation of generating a report and work plan to close on LNR performance requirements. As part of the report, please track prompts used to generate the plan and the report. The report will be placed in analysis/requirements.

**Purpose:** Initiate comprehensive gap analysis.

**Key Findings:**
- Datamodel contains 4 requirements (LNR-PERF-001 to 004)
- Source contains 18+ requirements (PERF-1A to PERF-18)
- Coverage approximately 15-20%
- Identified 23 gaps, 3 conflicts, 4 ambiguities

---

## Prompt 6: Conflict Resolution (CONF-01, CONF-02)

**User Prompt:**
> For LNR-PERF-001 PERF-1A, continue to use what is in the datamodel, because the source is out-of-date; this will resolve CONF-01. For LNR-PERF-002 PERF-2A continue to use what is in the datamodel, because the source is out-of-date; this will resolve CONF-02.

**Purpose:** Resolve conflicts between datamodel and source document values.

**Decisions Made:**
- **DEC-01:** Datamodel authoritative for latency (≤200ns vs source's 195ns)
- **DEC-02:** Datamodel authoritative for port count (72 ports vs source's 64 ports)
- Source document to be updated in Phase 5 of work plan

---

## Prompt 7: Clarifications (CONF-03, Phase 6, UALink)

**User Prompt:**
> Question 1: Let's clarify LNR-PERF-004 to indicate that this is the base latency of collective data in the switch, which includes the data path and the collective engine. This is not a statement of packet or message latency, but rather a statement regarding the worst-case time for the first byte of a collective message to flow from an input and be processed by a collective engine, or for a byte to flow from one collective engine result to another collective engine and be processed. This assumes that both operands arrive simultaneously and without encountering congestion.... Note, the stricter requirement in the source is referencing a specific benchmark and is still a requirement in that context. Question 2. Phase 6 should be part of the work plan. Question 3. The UALink station bandwidth requirement in the data model should reflect the native 1.6Tb/s 72-port architecture, which is 8x200G. This means that the UALink 800 Gbps requirement should support 144 links at 800 Gbps. It is subdividable to 2x200G and 1x200G with 288 links and 576 links, respectively.

**Purpose:** Clarify collective latency scope, confirm Phase 6 inclusion, define UALink architecture.

**Decisions Made:**
- **DEC-03:** LNR-PERF-004 and PERF-9 have different scope - both valid
  - LNR-PERF-004: CE base latency (hardware/architecture)
  - PERF-9: Benchmark latency (system-level)
- **DEC-07:** UALink architecture based on 72-port native:
  - 144 links @ 800 Gbps (4x200G)
  - 288 links @ 400 Gbps (2x200G)
  - 576 links @ 200 Gbps (1x200G)
- Phase 5 (source document updates) confirmed in work plan

---

## Prompt 8: Ambiguity Resolution

**User Prompt:**
> For AMB-04, RTT is defined as Round Trip Time. For AMB-01, I don't see a reference to cut-through routing in the source. There is no need to change the wording of "cut-through forwarding" in the requirement, because it is intended to measure the latency of the first byte of through the switch when cut-through routing is done, or at least a pseudo-store-and-forward. The requirement is not enforced for packets that must be processed in a store-and-forward mode. For AMB-02, congestion concepts can and should be defined later in the datamodel performance requirements

**Purpose:** Resolve remaining ambiguities.

**Decisions Made:**
- **AMB-01 (RESOLVED):** "Cut-through forwarding" wording is correct; measures first-byte latency; not enforced for store-and-forward packets
- **AMB-02 (RESOLVED):** Congestion concepts to be defined in datamodel (added as WP-21)
- **AMB-04 (RESOLVED):** RTT = Round Trip Time (standard networking term)

---

## Prompt 9: Report Generation

**User Prompt:**
> Please generate the report.

**Purpose:** Create final deliverables.

**Deliverables Created:**
1. `analysis/requirements/lnr-performance-gap-analysis.md` - Main analysis report
2. `analysis/requirements/lnr-performance-work-plan.md` - Detailed work plan
3. `analysis/requirements/prompts/lnr-performance-analysis.md` - This document

---

## Summary of Key Decisions

| Decision ID | Topic | Decision | Prompt |
|-------------|-------|----------|--------|
| DEC-01 | Latency target | Datamodel authoritative (≤200ns) | Prompt 6 |
| DEC-02 | Port count | Datamodel authoritative (72 ports) | Prompt 6 |
| DEC-03 | Collective latency | Different scope - both valid | Prompt 7 |
| DEC-04 | Cut-through wording | No change needed | Prompt 8 |
| DEC-05 | Congestion definition | Define later in datamodel | Prompt 8 |
| DEC-06 | RTT definition | RTT = Round Trip Time | Prompt 8 |
| DEC-07 | UALink architecture | 72-port native, subdividable | Prompt 7 |

---

## Analysis Statistics

| Metric | Value |
|--------|-------|
| Total Prompts | 9 |
| Conflicts Identified | 3 |
| Conflicts Resolved | 3 |
| Ambiguities Identified | 4 |
| Ambiguities Resolved | 4 |
| Gaps Identified | 23 |
| Work Items Created | 28 |
| New Requirements Planned | ~26 |

---

**Document History:**

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-01-23 | AI Analysis Agent | Initial draft |
