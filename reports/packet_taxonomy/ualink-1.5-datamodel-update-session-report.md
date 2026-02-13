# UALink 1.5 Datamodel Update — Session Report

## Table of Contents

- [1. Session Summary](#1-session-summary)
  - [What Was Requested](#what-was-requested)
  - [What Was Completed](#what-was-completed)
  - [Implementation Status](#implementation-status)
- [2. Reference Specifications (Source of Truth)](#2-reference-specifications-source-of-truth)
  - [UALink Common Specification Draft Rev 1.5 v0.9](#ualink-common-specification-draft-rev-15-v09)
  - [UALink 200G DL/PL 1.5 RC](#ualink-200g-dlpl-15-rc)
  - [Specification Structure Change (v1.0 → v1.5)](#specification-structure-change-v10--v15)
- [3. Current Datamodel State](#3-current-datamodel-state)
  - [Location](#location)
  - [Inventory](#inventory)
  - [Layer Breakdown](#layer-breakdown)
  - [Version Metadata](#version-metadata)
  - [Key Configuration Files](#key-configuration-files)
- [4. Crosscheck Findings](#4-crosscheck-findings)
  - [Overall Assessment](#overall-assessment)
  - [Critical Gaps (G1-G5)](#critical-gaps-g1-g5)
  - [Common Spec Changes (Confirmed)](#common-spec-changes-confirmed)
  - [DLPL Spec Changes](#dlpl-spec-changes-new-in-full-crosscheck)
  - [Field-Level Verification Items (V1-V14)](#field-level-verification-items-v1-v14)
  - [Metadata/Constraints Updates (M1-M10)](#metadataconstraints-updates-m1-m10)
- [5. Update Plan (6 Phases)](#5-update-plan-6-phases)
- [6. Risk Assessment](#6-risk-assessment)
- [7. Background Agent Results](#7-background-agent-results-not-retrieved)
- [8. Files Read During Analysis](#8-files-read-during-analysis)
- [9. Related Reports](#9-related-reports)
- [10. Implementation Results](#10-implementation-results)
  - [Commit Log](#commit-log)
  - [Final Metrics](#final-metrics)
- [11. Explicit Constraints (Verbatim from User)](#11-explicit-constraints-verbatim-from-user)
- [12. Technical Notes](#12-technical-notes)

**Date**: 2026-02-12
**Author**: Packet Taxonomy Team (developer-opus)
**Classification**: Cornelis Networks Engineering — Internal
**Status**: COMPLETE — All 6 phases implemented and pushed (11 commits, 51 KSY files)

---

## 1. Session Summary

This report captures the complete state of the UALink 1.5 datamodel crosscheck and update planning session. The goal is to update the UALink datamodel (Kaitai Struct .ksy files) to match version 1.5 of the UALink specifications.

### What Was Requested

```
/crosscheck earlysim/docs/references/UALink/*1.5* earlysim/datamodel/protocols/ualink
where the references are the SoT. Develop a plan for updating the datamodel.
Let's be clear that this is to update the datamodel to match version 1.5 of the
UALink specifications.
```

### What Was Completed

1. **Crosscheck Report Delivered** — Comprehensive gap analysis comparing UALink 1.5 specs against the existing datamodel
2. **6-Phase Update Plan** — Prioritized plan for bringing the datamodel to 1.5 alignment
3. **Risk Assessment** — 5 identified risks with mitigation recommendations
4. **Background Agent Analysis** — 3 deep-dive agents completed (results regenerated during execution)
5. **Full Implementation** — All 6 phases executed: 11 commits, 51 KSY files (38 updated + 13 new), all validated
6. **Push Complete** — All commits pushed to earlysim submodule remote

### Implementation Status

All 6 phases have been completed:

| Phase | Description | Status |
|-------|-------------|--------|
| Phase 0 | KSY structural fix (doc/doc-ref placement) | ✅ Complete |
| Phase 1 | Metadata & version alignment | ✅ Complete |
| Phase 2 | Field-level verification (5 layers) | ✅ Complete |
| Phase 3 | In-Network Collectives (8 new files) | ✅ Complete |
| Phase 4 | RAS & Error Handling (3 new files) | ✅ Complete |
| Phase 5 | Collective Security (2 new + 2 updated) | ✅ Complete |
| Phase 6 | Final counts, CMake, documentation | ✅ Complete |

---

## 2. Reference Specifications (Source of Truth)

### UALink Common Specification Draft Rev 1.5 v0.9

- **Path**: `earlysim/docs/references/UALink/UALink_Common_Specification_Draft_Rev1.5_v0.9/`
- **File**: `UALink_Common_Specification_Draft_Rev1.5_v0.9.md` (~5,186 lines, ~245+ pages)
- **Metadata**: `UALink_Common_Specification_Draft_Rev1.5_v0.9_meta.json`
- **Date**: 2026-01-13
- **Scope**: Protocol, Transaction, Collectives, Security, Switch Requirements (Chapters 1-9)
- **Copyright**: 2025-2026 Ultra Accelerator Link Consortium

### UALink 200G DL/PL 1.5 RC

- **Path**: `earlysim/docs/references/UALink/UALink_1.5_DLPL_200G_NCB_RC/`
- **File**: `UALink_1.5_DLPL_200G_NCB_RC.md` (~2,807 lines, ~106+ pages)
- **Metadata**: `UALink_1.5_DLPL_200G_NCB_RC_meta.json` (full TOC with page coordinates)
- **Date**: 2026-01-12
- **Scope**: Data Link and Physical Layer for 200G SerDes (Chapters 2-3 + Appendices)
- **Copyright**: 2025 Ultra Accelerator Link Consortium

### Specification Structure Change (v1.0 → v1.5)

The v1.0 specification was a single monolithic document (UALink200 v1.0 Final, 5,974 lines). For v1.5, the UALink Consortium split it into:
- A speed-independent **Common** specification
- Speed-specific **DLPL** specifications (200G NCB is the first)

---

## 3. Current Datamodel State

### Location

`earlysim/datamodel/protocols/ualink/`

### Inventory

| Category | Before (v1.0) | After (v1.5) | Description |
|----------|---------------|--------------|-------------|
| KSY packet definitions | 27 | 36 | Kaitai Struct format files |
| KSY protocol FSMs | 11 | 15 | State machine definitions |
| **Total KSY files** | **38** | **51** | Across 7 layers |
| YAML reference files | 7 | 7 | Field definitions, packet types, metadata |

### Layer Breakdown

| Layer | KSY Files | Key Files |
|-------|-----------|-----------|
| UPLI (Upper Protocol Layer Interface) | 8 (6 formats + 2 protocols) | `commands.ksy`, `request_channel.ksy`, `status_codes.ksy` |
| Transaction | 9 (7 formats + 2 protocols) | `tl_flit.ksy`, `control_half_flit.ksy`, `request_field.ksy` |
| Data Link | 12 (4 headers + 4 messages + 4 protocols) | `dl_flit.ksy`, `flit_header.ksy`, `segment_header.ksy` |
| Physical | 4 (3 formats + 1 protocol) | `alignment_markers.ksy`, `control_ordered_sets.ksy` |
| Security | 7 (5 formats + 2 protocols) | `encryption.ksy`, `collective_security.ksy`, `multipath_routing.ksy` |
| **Collectives** (NEW) | **8** (5 formats + 2 protocols + 1 table) | `collective_primitives.ksy`, `block_collective_invoke.ksy` |
| **RAS** (NEW) | **3** (2 formats + 1 protocol) | `error_types.ksy`, `error_handling.ksy`, `error_recovery.ksy` |

### Version Metadata

From `metadata.yaml` (updated):
- `ualink_spec_version: "1.5"` — ✅ updated from "1.0"
- `dlpl_spec_version: "1.5"` — already correct
- Total KSY files: 51 (was 38)

### Key Configuration Files

| File | Purpose |
|------|---------|
| `metadata.yaml` | Spec versions, layer definitions, coverage statistics |
| `constraints.yaml` | Architectural constraints (topology, ordering, limits) |
| `README.md` | Datamodel documentation |
| `reference/packet_types.yaml` | Packet type registry |
| `reference/field_definitions/*.yaml` | 6 field definition files |

---

## 4. Crosscheck Findings

### Overall Assessment

| Dimension | v1.0 (Current) | v1.5 (Target) | Delta |
|-----------|----------------|---------------|-------|
| Total Spec Lines | 5,974 | 7,993 (5,186 + 2,807) | +34% |
| Chapters | 10 | 9 (Common) + 3 (DLPL) + Appendices | Restructured |
| UPLI Commands | 12 | 22 | +10 new |
| DL States | 4 (Fault, Idle, NOP, Up) | 5 (+ PwrDn) | +1 new |

### Critical Gaps (G1-G5)

| # | Gap | Spec Reference | New Files Needed | Priority |
|---|-----|----------------|-----------------|----------|
| G1 | In-Network Collectives (entirely missing) | Common Spec §6 (~30 pages) | ~11 new KSY | P0 |
| G2 | RAS Error Types/Handling | Common Spec §3 (~15 pages) | ~3 new KSY | P1 |
| G3 | Collective Security | Common Spec §8.6 (~10 pages) | ~3 new KSY | P1 |
| G4 | Switch Requirements | Common Spec §9 (~5 pages) | Constraints only | P2 |
| G5 | Manageability Requirements | Common Spec §7 (~5 pages) | Constraints only | P2 |

### Common Spec Changes (Confirmed)

1. **In-Network Collectives (INC)** — Entirely new Chapter 6 with Collective Primitives and Block Collectives (10 new UPLI commands)
2. **Security for Collectives** — New Section 8.6 with Accelerator-Switch link protection
3. **Multi-path routing security** — New Section 8.7
4. **PCRC (Payload CRC)** — New Section 8.5.15

### DLPL Spec Changes (New in Full Crosscheck)

5. **Link Resiliency** — New Section 2.8: bonding of two physical layers to one DL with TDM, fault recovery, and reordering
6. **Link Folding** — New Section 2.9: power-saving lane folding/unfolding with DL PwrDn state
7. **Link Width Negotiation** — New DL control message (Section 2.4.3.3) for negotiating link width changes
8. **Tx Ready Notification** — New DL basic message (Section 2.4.2.6) for link unfolding coordination
9. **TL Backpressure** — New Rx Ingress Rules for handling TL backpressure (Section 2.6.6.2)
10. **DL-PL Interface** — New Appendix B with detailed signal-level interface specification
11. **Rapid Alignment Markers (RAMs)** — New Section 3.3.7 for fast alignment during link unfolding
12. **PMA Symbol Pair Demultiplexing** — New Section 3.3.8 requiring parallel alignment search

### Field-Level Verification Items (V1-V14)

These require comparing existing KSY fields against 1.5 spec tables:

| # | Item | Affected Files |
|---|------|---------------|
| V1 | UPLI command opcodes (12 → 22) | `upli/commands.ksy` |
| V2 | Request channel fields | `upli/request_channel.ksy` |
| V3 | Transaction request field layout | `transaction/request_field.ksy` |
| V4 | Transaction response field layout | `transaction/response_field.ksy` |
| V5 | Flit header bit assignments | `datalink/flit_header.ksy` |
| V6 | Segment header encoding | `datalink/segment_header.ksy` |
| V7 | Control message types | `datalink/messages/control_messages.ksy` |
| V8 | Basic message types | `datalink/messages/basic_messages.ksy` |
| V9 | Link state transitions (new PwrDn) | `datalink/protocols/link_state.ksy` |
| V10 | Encryption field widths | `security/encryption.ksy` |
| V11 | Authentication tag format | `security/authentication.ksy` |
| V12 | IV format changes | `security/iv_format.ksy` |
| V13 | Physical layer alignment markers | `physical/alignment_markers.ksy` |
| V14 | Control ordered sets | `physical/control_ordered_sets.ksy` |

### Metadata/Constraints Updates (M1-M10)

| # | Item | Target File |
|---|------|------------|
| M1 | Spec version "1.0" → "1.5" | `metadata.yaml` |
| M2 | Add `collectives` layer | `metadata.yaml` |
| M3 | Add `ras` layer | `metadata.yaml` |
| M4 | Update packet count (38 → ~55) | `metadata.yaml` |
| M5 | Add RAS constraints | `constraints.yaml` |
| M6 | Add switch constraints | `constraints.yaml` |
| M7 | Add manageability constraints | `constraints.yaml` |
| M8 | Add collectives constraints | `constraints.yaml` |
| M9 | Update README for new layers | `README.md` |
| M10 | Register new packet types | `reference/packet_types.yaml` |

---

## 5. Update Plan (6 Phases)

### Phase 1: Metadata & Version Alignment (P0)

**Scope**: Update metadata, constraints, README, and packet type registry.

**Files to modify**:
- `metadata.yaml`: version "1.0" → "1.5", add `collectives` and `ras` layers
- `constraints.yaml`: add RAS, switch, manageability, collectives sections
- `README.md`: update for new layers and spec references
- `reference/packet_types.yaml`: register new packet types

**Estimated effort**: Small

### Phase 2: Field-Level Verification (P0)

**Scope**: Verify all 38 existing KSY files against 1.5 spec tables. Update `x-spec` metadata references (section numbers changed between v1.0 and v1.5).

**Key files**:
- `upli/request_channel.ksy`
- `transaction/request_field.ksy`, `response_field.ksy`
- `security/encryption.ksy`
- `datalink/flit_header.ksy`
- All message KSY files

**Estimated effort**: Medium-Large (14 verification items across 38 files)

### Phase 3: In-Network Collectives (P0)

**Scope**: Create ~11 new KSY files under new `collectives/` directory.

**New files**:
- `collective_primitives.ksy`
- `broadcast.ksy`
- `reduce.ksy`
- `all_reduce.ksy`
- `reduce_scatter.ksy`
- `block_collective_allocate.ksy`
- `block_collective_deallocate.ksy`
- `block_collective_invoke.ksy`
- `block_collective_control_block.ksy`
- Plus 2 protocol FSMs

**Estimated effort**: Large (entirely new chapter, ~30 pages of spec)

### Phase 4: RAS & Error Handling (P1)

**Scope**: Create ~3 new KSY files under `ras/` directory.

**Source**: Common Spec §3 (~15 pages)

**Estimated effort**: Medium

### Phase 5: Collective Security (P1)

**Scope**: Create ~3 new KSY files under `security/`.

**Source**: Common Spec §8.6 (~10 pages)

**Estimated effort**: Medium

### Phase 6: Constraints & Documentation (P2)

**Scope**: Add architectural constraints from Chapters 7 and 9. Update CMakeLists.txt for new directories.

**Estimated effort**: Small

### Recommended Execution Order

```
Phase 1 → Phase 2 → Phase 3 → Phase 5 → Phase 4 → Phase 6
```

### Post-Update Results

| Metric | Before | Target | Actual |
|--------|--------|--------|--------|
| KSY files | 38 | ~55 | **51** |
| Protocol FSMs | 11 | ~16 | **15** |
| Layers | 5 | 7 | **7** (+ collectives, ras) |
| Spec version | 1.0 | 1.5 | **1.5** |

---

## 6. Risk Assessment

| # | Risk | Impact | Mitigation |
|---|------|--------|------------|
| R1 | Spec is Draft (v0.9) — fields may change before final | High | Track spec revisions; use `x-spec-status: draft` metadata |
| R2 | OCR conversion artifacts in spec markdown | Medium | Cross-reference with PDF when field values seem wrong |
| R3 | Collectives chapter is entirely new — no existing patterns to follow | Medium | Study UE CMS patterns as closest analog; follow existing KSY conventions |
| R4 | Section number remapping (v1.0 → v1.5) affects all `x-spec` references | Medium | Systematic search-and-replace with verification |
| R5 | DLPL spec is separate document — dual-source maintenance | Low | Clear metadata tracking which spec each file references |

---

## 7. Background Agent Results

Three explore agents completed deep analysis during the initial planning session. Results were not retrieved in that session due to token limits, but equivalent analysis was regenerated during execution by the Sisyphus work agents.

| Agent ID | Task | Status | Used During Execution |
|----------|------|--------|----------------------|
| `bg_6a7d9bb4` | Deep analysis of UALink 1.5 Common Spec | Completed | Regenerated by Phase 2-5 agents |
| `bg_b66436e8` | Deep analysis of all 38 datamodel KSY files | Completed | Regenerated by Phase 0-2 agents |
| `bg_0ba84e8f` | Deep analysis of UALink 1.5 DLPL 200G NCB RC | Completed | Regenerated by Phase 2c-2d agents |

---

## 8. Files Read During Analysis

### Reference Spec Files
- `earlysim/docs/references/UALink/UALink_Common_Specification_Draft_Rev1.5_v0.9/UALink_Common_Specification_Draft_Rev1.5_v0.9_meta.json`
- `earlysim/docs/references/UALink/UALink_1.5_DLPL_200G_NCB_RC/UALink_1.5_DLPL_200G_NCB_RC_meta.json`
- First 200 lines of both spec markdown files (table of contents extracted)

### Datamodel Files
- `earlysim/datamodel/protocols/ualink/metadata.yaml`
- `earlysim/datamodel/protocols/ualink/constraints.yaml`
- `earlysim/datamodel/protocols/ualink/README.md`
- `earlysim/datamodel/protocols/ualink/reference/packet_types.yaml`

---

## 9. Related Reports

| Report | Path | Relationship |
|--------|------|-------------|
| UALink v1.0-to-1.5 Crosscheck (Common-only) | `reports/docs-review/ualink-spec1.0-to-1.5_v0.9-crosscheck.md` | Predecessor — Common spec only, superseded by full crosscheck |
| UALink HAS Crosscheck | `reports/docs-review/ualink-has-crosscheck.md` | Related — HAS alignment review |
| UALink Technical Report | `reports/packet_taxonomy/technical_report/technical_report_ualink.yaml` | Current state — documents existing 38 KSY files |
| Status Report | `reports/packet_taxonomy/status_report/status_report.yaml` | Overall project status — W-14 series covers UALink expansion |

---

## 10. Implementation Results

### Commit Log

All 11 commits were made in the `earlysim` submodule and pushed to remote:

| # | Commit Hash | Message | Phase |
|---|-------------|---------|-------|
| 1 | `0c63aca8` | `fix(ualink): move doc/doc-ref from meta section to type level per KSY spec` | Phase 0 |
| 2 | `6e017e68` | `feat(ualink): update metadata and references for UALink spec v1.5` | Phase 1 |
| 3 | `85df6d4f` | `feat(ualink/upli): verify UPLI layer against UALink 1.5 spec` | Phase 2a |
| 4 | `f39a037f` | `feat(ualink/transaction): verify Transaction layer against UALink 1.5 spec` | Phase 2b |
| 5 | `133eda62` | `feat(ualink/datalink): verify and expand Data Link layer for UALink 1.5 DLPL spec` | Phase 2c |
| 6 | `b8629388` | `feat(ualink/physical): verify and expand Physical layer for UALink 1.5 DLPL spec` | Phase 2d |
| 7 | `e79efd8c` | `feat(ualink/security): verify Security layer against UALink 1.5 spec` | Phase 2e |
| 8 | `4c618a8e` | `feat(ualink): add In-Network Collectives datamodel (UALink 1.5 Chapter 6)` | Phase 3 |
| 9 | `88c36009` | `feat(ualink): add RAS error handling datamodel (UALink 1.5 Chapter 3)` | Phase 4 |
| 10 | `3571084f` | `feat(ualink): add collective security and multi-path routing (UALink 1.5 §8.6-8.7)` | Phase 5 |
| 11 | `f8b5f0d7` | `feat(ualink): finalize UALink 1.5 datamodel update — counts, CMake, documentation` | Phase 6 |

### Final Metrics

| Metric | Value |
|--------|-------|
| Total KSY files | 51 (38 existing + 13 new) |
| New files created | 13 (8 collectives, 3 RAS, 2 security) |
| Existing files updated | 38 (all with v1.5 metadata + structural fix) |
| Validation result | 51/51 PASS |
| New UPLI opcodes added | 10 (INC commands) |
| Major file expansions | `link_resiliency.ksy` (92→253 lines), `link_folding.ksy` (101→243 lines) |
| New directories | `collectives/`, `collectives/protocols/`, `ras/`, `ras/protocols/` |

---

## 11. Explicit Constraints (Verbatim from User)

- "the references are the SoT" — Reference specifications are the Source of Truth
- "Let's be clear that this is to update the datamodel to match version 1.5 of the UALink specifications" — The goal is datamodel alignment to 1.5, not the other way around

---

## 12. Technical Notes

- The `earlysim/` directory is a **git submodule** — must be initialized with `git submodule update --init --recursive`
- KSY files use Kaitai Struct YAML format with custom `x-spec` metadata extensions
- Reference YAMLs define field definitions with bit positions, widths, and spec section references
- The spec markdown files are very large — use `offset`/`limit` parameters when reading
- Both spec markdown files are OCR-converted from PDF (via the `_meta.json` files which contain page-level TOC with polygon coordinates)
