# UALink 1.5 Datamodel Update — Work Plan

## Table of Contents

- [TL;DR](#tldr)
- [Context](#context)
  - [Original Request](#original-request)
  - [Interview Summary](#interview-summary)
  - [Metis Review](#metis-review)
- [Work Objectives](#work-objectives)
  - [Core Objective](#core-objective)
  - [Concrete Deliverables](#concrete-deliverables)
  - [Definition of Done](#definition-of-done)
  - [Must Have](#must-have)
  - [Must NOT Have (Guardrails)](#must-not-have-guardrails)
- [Verification Strategy](#verification-strategy)
  - [Test Decision](#test-decision)
  - [Agent-Executed QA Scenarios](#agent-executed-qa-scenarios-mandatory--all-tasks)
  - [Spec Version String Rules](#spec-version-string-rules-from-metis-g1)
- [Execution Strategy](#execution-strategy)
  - [Parallel Execution Waves](#parallel-execution-waves)
  - [Dependency Matrix](#dependency-matrix)
- [TODOs](#todos)
  - [Phase 0: Prerequisites & KSY Structural Fix](#phase-0-prerequisites--ksy-structural-fix)
  - [Phase 1: Metadata & Version Alignment](#phase-1-metadata--version-alignment)
  - [Phase 2: Field-Level Verification](#phase-2-field-level-verification-5-parallel-tasks)
  - [Phase 2 Validation Gate](#phase-2-validation-gate)
  - [Phase 3: In-Network Collectives](#phase-3-in-network-collectives-new-files)
  - [Phase 4: RAS & Error Handling](#phase-4-ras--error-handling-new-files)
  - [Phase 5: Collective Security](#phase-5-collective-security-updated--new-files)
  - [Phase 6: Final Constraints, Counts & Documentation](#phase-6-final-constraints-counts--documentation)
- [Commit Strategy](#commit-strategy)
- [Success Criteria](#success-criteria)
  - [Verification Commands](#verification-commands)
  - [Final Checklist](#final-checklist)

## TL;DR

> **Quick Summary**: Update the UALink datamodel (38 existing KSY files + 13 new files = 51 total) to match UALink specification v1.5. **STATUS: COMPLETE — All phases implemented and pushed.** The reference specs are the Source of Truth. First fix KSY structural issue (move doc/doc-ref from meta to type level per Kaitai Struct spec), then covers metadata alignment, field verification of all existing files, creation of new Collectives/RAS/Security files, and documentation updates.
> 
> **Deliverables**:
> - Structural fix: doc/doc-ref moved to type level in all 38 existing KSY files (per KSY spec)
> - Updated metadata, constraints, README, and reference files for v1.5
> - All 38 existing KSY files verified and updated with v1.5 spec references
> - ~8 new KSY files for In-Network Collectives (collectives/)
> - ~3 new KSY files for RAS error handling (ras/)
> - ~2 updated + ~2 new KSY files for Collective Security (security/)
> - Updated CMakeLists.txt, final coverage counts, documentation
> 
> **Estimated Effort**: Large (7 phases including Phase 0 structural fix, ~20 work items)
> **Parallel Execution**: YES — 4 waves
> **Critical Path**: Phase 0 → Phase 1 → Phase 2 → Phase 3 → Phase 6

---

## Context

### Original Request
```
/crosscheck earlysim/docs/references/UALink/*1.5* earlysim/datamodel/protocols/ualink
where the references are the SoT. Develop a plan for updating the datamodel.
Let's be clear that this is to update the datamodel to match version 1.5 of the
UALink specifications.
```

### Interview Summary
**Key Discussions**:
- All 6 phases in a single plan
- Validate with `validate_ksy.py` after each phase
- Phase 2 organized as one work item per layer (5 items)
- No unit tests beyond `validate_ksy.py`

**Research Findings**:
- Common Spec v1.5 adds: Ch3 RAS, Ch6 INC (10 new UPLI commands, 8 tables), Ch7 Manageability, Ch8.6 Collective Security (4 tables), Ch8.7 Multi-path routing, Ch9 Switch Requirements
- DLPL Spec v1.5 adds: Tx Ready Notification, Link Width Negotiation, TL Backpressure, Link Resiliency, Link Folding, RAMs, PMA Symbol Pair Demux, DL-PL Interface
- Core DL parameters UNCHANGED: flit header, segment header, CRC, 5 DL states
- 2 new DL message types confirmed
- Existing `link_resiliency.ksy` and `link_folding.ksy` need structural expansion (not just metadata)
- Existing `basic_messages.ksy` may already anticipate Tx Ready Notification

### Metis Review
**Identified Gaps** (addressed):
- Spec version string rules: Resolved — use `"1.5"` for `ualink_spec_version` in metadata.yaml; per-file x-spec tracks source spec
- Phase 1 coverage counts: Deferred to Phase 6 (counts unknown until Phases 3-5 complete)
- `link_resiliency.ksy`/`link_folding.ksy` treatment: Flagged as structural expansion in Phase 2
- Naming convention: Use `collectives/` (plural, matching spec chapter title "In-Network Collectives")
- Phase 5 file placement: New collective security files go in `security/` (same layer)
- Existing security files may need updates rather than new files for KDF/IV changes

---

## Work Objectives

### Core Objective
Bring the UALink datamodel into full alignment with UALink specification v1.5, ensuring every KSY file has correct spec references, all new v1.5 content is modeled, and metadata/constraints reflect the current spec state.

### Concrete Deliverables
- Updated `metadata.yaml`, `constraints.yaml`, `README.md`, `packet_types.yaml`
- Updated 6 `reference/field_definitions/*.yaml` files
- Updated 38 existing KSY files with v1.5 spec references
- Structurally expanded `link_resiliency.ksy`, `link_folding.ksy`, `basic_messages.ksy`, `control_messages.ksy`
- New `collectives/` directory with ~8 KSY files
- New `ras/` directory with ~3 KSY files
- Updated/new security KSY files for collective security
- Updated `CMakeLists.txt`

### Definition of Done
- [x] All KSY files have `doc` and `doc-ref` at type level (not inside `meta:`) per Kaitai Struct spec
- [x] `python earlysim/datamodel/scripts/validate_ksy.py --all earlysim/datamodel/protocols/ualink/` → exit code 0 (51/51 PASS)
- [x] All KSY files have valid `x-spec.spec_version` and `x-spec.section` or `x-spec.table`
- [x] `metadata.yaml` coverage counts match actual file counts
- [x] No `spec_version: "1.0"` references remain in metadata.yaml or constraints.yaml

### Must Have
- Every new KSY file follows the exemplar pattern (≥50 lines, all x-* metadata)
- Every spec table/figure referenced in the plan is traceable to a KSY file
- Validation passes after each phase

### Must NOT Have (Guardrails)
- **G1**: No changes outside `earlysim/datamodel/protocols/ualink/`
- **G2**: Phase 2 metadata-only changes for most files (exception: link_resiliency, link_folding, basic_messages, control_messages)
- **G3**: No speculative types or helpers — model ONLY what's in the referenced spec table/figure
- **G4**: No unit tests beyond `validate_ksy.py`
- **G5**: No YAML reference files for new KSY files unless they meet documented criteria (entry points, multi-variant, cross-layer, high-complexity)
- **G6**: constraints.yaml contains ONLY values directly stated in specifications
- **G7**: No changes to other protocol datamodels (ue/, ethernet/, roce/, cornelis/)

---

## Verification Strategy

> **UNIVERSAL RULE: ZERO HUMAN INTERVENTION**
>
> ALL tasks in this plan MUST be verifiable WITHOUT any human action.

### Test Decision
- **Infrastructure exists**: YES (`earlysim/datamodel/scripts/validate_ksy.py`)
- **Automated tests**: validate_ksy.py after each phase
- **Framework**: Python script + ksc (kaitai-struct-compiler)

### Agent-Executed QA Scenarios (MANDATORY — ALL tasks)

**Verification Tool by Deliverable Type:**

| Type | Tool | How Agent Verifies |
|------|------|-------------------|
| YAML files | Bash (python) | `python -c "import yaml; yaml.safe_load(open(...))"` |
| KSY files | Bash (validate_ksy.py) | `python validate_ksy.py --all <dir>` → exit 0 |
| Directory structure | Bash (ls) | `ls -d <dir>` → exists |
| File counts | Bash (find/wc) | `find <dir> -name '*.ksy' | wc -l` → expected count |
| Metadata consistency | Bash (python) | Custom python one-liner checking counts |

### Spec Version String Rules (from Metis G1)
```
- metadata.yaml: ualink_spec_version → "1.5"
- Per-file x-spec.spec_version:
  - UPLI files (Common Spec sourced): "1.5" (tables renumbered in v1.5)
  - Transaction files (Common Spec sourced): "1.5"
  - Data Link files (DLPL sourced): "1.5"
  - Physical files (DLPL sourced): "1.5"
  - Security files (Common Spec sourced): "1.5"
  - New collectives files (Common Spec Ch6): "1.5"
  - New RAS files (Common Spec Ch3): "1.5"
- Per-file x-spec.spec_date:
  - Common Spec sourced: "2026-01-13"
  - DLPL sourced: "2026-01-12"
```

---

## Execution Strategy

### Parallel Execution Waves

```
Wave 0 (Start Immediately):
└── Task 0: Phase 0 — Verify Build Environment & Fix doc/doc-ref Placement (38 files)

Wave 1 (After Wave 0):
└── Task 1: Phase 1 — Metadata & Version Alignment

Wave 2 (After Wave 1):
├── Task 2: Phase 2a — UPLI Layer Verification
├── Task 3: Phase 2b — Transaction Layer Verification
├── Task 4: Phase 2c — Data Link Layer Verification (includes structural expansion)
├── Task 5: Phase 2d — Physical Layer Verification
└── Task 6: Phase 2e — Security Layer Verification

Wave 3 (After Wave 2):
├── Task 7: Phase 3 — In-Network Collectives (new files)
├── Task 8: Phase 4 — RAS & Error Handling (new files)
└── Task 9: Phase 5 — Collective Security (new + updated files)

Wave 4 (After Wave 3):
└── Task 10: Phase 6 — Final Constraints, Counts & Documentation

Critical Path: Task 0 → Task 1 → Task 4 → Task 7 → Task 10
```

### Dependency Matrix

| Task | Depends On | Blocks | Can Parallelize With |
|------|------------|--------|---------------------|
| 0 | None | 1-10 | None (must be first — structural fix) |
| 1 | 0 | 2-6 | None (must follow Task 0) |
| 2 | 1 | 7 | 3, 4, 5, 6 |
| 3 | 1 | 7 | 2, 4, 5, 6 |
| 4 | 1 | 7 | 2, 3, 5, 6 |
| 5 | 1 | 7 | 2, 3, 4, 6 |
| 6 | 1 | 9 | 2, 3, 4, 5 |
| 7 | 2, 3, 4 | 10 | 8, 9 |
| 8 | 1 | 10 | 7, 9 |
| 9 | 6 | 10 | 7, 8 |
| 10 | 7, 8, 9 | None | None (must be last) |

---

## TODOs

### Phase 0: Prerequisites & KSY Structural Fix

- [x] 0. Verify Build Environment & Fix doc/doc-ref Placement in All 38 KSY Files

  **What to do**:

  **Step 1: Verify build tools**
  - Verify `ksc` (kaitai-struct-compiler) is available: `which ksc`
  - Verify `validate_ksy.py` runs: `python earlysim/datamodel/scripts/validate_ksy.py --help`
  - Verify git submodule initialized: `ls earlysim/datamodel/protocols/ualink/metadata.yaml`
  - If `ksc` not found, install or note as blocker

  **Step 2: Fix doc/doc-ref placement in ALL 38 existing KSY files (STRUCTURAL FIX)**

  Per the [Kaitai Struct KSY Style Guide](https://doc.kaitai.io/ksy_style_guide.html), `doc` and `doc-ref` are **type-level keys** — they MUST be siblings of `meta:`, NOT nested inside it. Currently all 38 UALink KSY files have `doc` and `doc-ref` incorrectly nested inside the `meta:` section, which causes `ksc` to reject them with `/meta/doc-ref: error: unknown key found`.

  **The fix**: For each of the 38 KSY files, move `doc:` and `doc-ref:` from inside `meta:` to the type level (between `meta:` and the next top-level key like `x-spec:`).

  **Before** (WRONG — current state in all 38 files):
  ```yaml
  meta:
    id: ualink_crc
    title: UALink DL CRC
    endian: be
    bit-endian: be
    doc: |
      UALink DL CRC-32 from UALink200 Specification Section 6.
      CRC covers the entire DL Flit except the CRC field itself.
    doc-ref:
      - "UALink200 Specification v1.0, Section 6"
    ks-version: "0.10"
  ```

  **After** (CORRECT — per Kaitai Struct spec):
  ```yaml
  meta:
    id: ualink_crc
    title: UALink DL CRC
    endian: be
    bit-endian: be
    ks-version: "0.10"

  doc: |
    UALink DL CRC-32 from UALink200 Specification Section 6.
    CRC covers the entire DL Flit except the CRC field itself.

  doc-ref:
    - "UALink200 Specification v1.0, Section 6"
  ```

  **Key rules for the transformation**:
  1. `meta:` retains ONLY: `id`, `title`, `endian`, `bit-endian`, `license`, `ks-version` (and `imports` if present)
  2. `doc:` moves to type level, immediately after `meta:` block (with blank line separator)
  3. `doc-ref:` moves to type level, immediately after `doc:` (with blank line separator)
  4. `doc:` content (the actual text) must NOT change — preserve exact wording
  5. `doc-ref:` list items must NOT change — preserve exact references
  6. Indentation changes: `doc:` and `doc-ref:` go from 2-space indent (inside meta) to 0-space indent (type level)
  7. For files with `license:` inside `meta:`, keep `license:` inside `meta:` (it IS a valid meta key)
  8. Preserve all other keys (`x-spec`, `x-packet`, `x-related-headers`, `x-protocol`, `seq`, `types`, `enums`, `instances`) unchanged

  **Two structural patterns exist across the 38 files**:

  **Pattern A** (~20 files, e.g. `crc.ksy`, `basic_messages.ksy`, `segment_header.ksy`):
  Short `doc` string, no `license` in meta. `doc-ref` at low line number (line 9-10).
  ```yaml
  meta:
    id: ...
    title: ...
    endian: be
    bit-endian: be
    doc: |
      Short description (1-3 lines)
    doc-ref:
      - "..."
    ks-version: "0.10"
  ```

  **Pattern B** (~18 files, e.g. `request_channel.ksy`, `tl_flit.ksy`, `encryption.ksy`):
  Long multi-paragraph `doc`, has `license` in meta. `doc-ref` at higher line number (line 35-80).
  ```yaml
  meta:
    id: ...
    title: ...
    endian: be
    bit-endian: be
    doc: |
      Long multi-paragraph description (10-40 lines)
    doc-ref:
      - "..."
      - "..."
    license: "..."
    ks-version: "0.10"
  ```

  **Files to fix** (all 38):
  - `upli/commands.ksy`, `upli/request_channel.ksy`, `upli/originator_data_channel.ksy`, `upli/read_response_channel.ksy`, `upli/write_response_channel.ksy`, `upli/status_codes.ksy`, `upli/protocols/connection_handshake.ksy`, `upli/protocols/flow_control.ksy`
  - `transaction/tl_flit.ksy`, `transaction/control_half_flit.ksy`, `transaction/data_half_flit.ksy`, `transaction/message_half_flit.ksy`, `transaction/request_field.ksy`, `transaction/response_field.ksy`, `transaction/flow_control_field.ksy`, `transaction/protocols/compression.ksy`, `transaction/protocols/address_cache.ksy`
  - `datalink/dl_flit.ksy`, `datalink/flit_header.ksy`, `datalink/segment_header.ksy`, `datalink/crc.ksy`, `datalink/messages/basic_messages.ksy`, `datalink/messages/control_messages.ksy`, `datalink/messages/uart_messages.ksy`, `datalink/messages/vendor_defined.ksy`, `datalink/protocols/link_state.ksy`, `datalink/protocols/link_resiliency.ksy`, `datalink/protocols/link_folding.ksy`, `datalink/protocols/link_level_replay.ksy`
  - `physical/alignment_markers.ksy`, `physical/control_ordered_sets.ksy`, `physical/reconciliation_sublayer.ksy`, `physical/protocols/link_training.ksy`
  - `security/encryption.ksy`, `security/iv_format.ksy`, `security/authentication.ksy`, `security/protocols/key_derivation.ksy`, `security/protocols/key_rotation.ksy`

  **Step 3: Run baseline validation**
  - Run: `python earlysim/datamodel/scripts/validate_ksy.py --all earlysim/datamodel/protocols/ualink/`
  - This MUST now pass (exit code 0) since `doc-ref` is no longer inside `meta:`

  **Must NOT do**:
  - Do not change the TEXT CONTENT of any `doc:` or `doc-ref:` values — only move their YAML position
  - Do not change any `seq:`, `types:`, `enums:`, `instances:`, `x-spec`, `x-packet`, or other keys
  - Do not update spec version references yet (that's Phase 1 and Phase 2 scope)
  - Do not install packages without user approval

  **Recommended Agent Profile**:
  - **Category**: `deep`
    - Reason: 38 files to transform with two structural patterns; must be meticulous to avoid breaking YAML structure
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Sequential (must be first)
  - **Blocks**: All other tasks
  - **Blocked By**: None

  **References**:

  **Pattern References**:
  - `earlysim/datamodel/protocols/ualink/datalink/crc.ksy` — Pattern A exemplar (short doc, no license, doc-ref at line 9)
  - `earlysim/datamodel/protocols/ualink/upli/request_channel.ksy` — Pattern B exemplar (long doc, has license, doc-ref at line 58)
  - `earlysim/datamodel/protocols/ualink/transaction/tl_flit.ksy` — Pattern B exemplar (long doc, has license, doc-ref at line 52)

  **Documentation References**:
  - [Kaitai Struct KSY Style Guide §2](https://doc.kaitai.io/ksy_style_guide.html#type) — Order of sections: `meta` → `doc` → `doc-ref` → `seq` → `instances` → `types`/`enums`
  - [Kaitai Struct KSY Style Guide §3](https://doc.kaitai.io/ksy_style_guide.html#meta) — Valid meta keys: `id`, `title`, `application`, `file-extension`, `xref`, `tags`, `license`, `ks-version`, `imports`, `encoding`, `endian`, `bit-endian`

  **Tool References**:
  - `earlysim/datamodel/scripts/validate_ksy.py` — Validation script (strips x-* keys, then runs ksc)

  **Acceptance Criteria**:

  ```
  Scenario: All 38 KSY files have doc/doc-ref at type level (not inside meta)
    Tool: Bash (python)
    Steps:
      1. For each of 38 KSY files:
         python -c "
         import yaml
         with open('<file>') as f:
             data = yaml.safe_load(f.read())
         # doc and doc-ref should be top-level keys, NOT inside meta
         assert 'doc' not in data.get('meta', {}), '<file>: doc still inside meta'
         assert 'doc-ref' not in data.get('meta', {}), '<file>: doc-ref still inside meta'
         # doc and doc-ref should exist at type level
         assert 'doc' in data, '<file>: doc missing from type level'
         assert 'doc-ref' in data, '<file>: doc-ref missing from type level'
         print('PASS: <file>')
         "
    Expected Result: All 38 files pass
    Evidence: Command output captured

  Scenario: doc/doc-ref content preserved (no text changes)
    Tool: Bash (git diff)
    Steps:
      1. git diff --stat → shows exactly 38 files changed
      2. For a sample of 3 files (crc.ksy, request_channel.ksy, tl_flit.ksy):
         Verify git diff shows only indentation/position changes, not content changes
    Expected Result: Only structural moves, no content modifications
    Evidence: git diff output captured

  Scenario: Baseline validation passes after fix
    Tool: Bash (validate_ksy.py)
    Steps:
      1. python earlysim/datamodel/scripts/validate_ksy.py --all earlysim/datamodel/protocols/ualink/
    Expected Result: Exit code 0 — ALL 38 files pass
    Evidence: Validation output captured (should show 0 failures)
  ```

  **Commit**: YES
  - Message: `fix(ualink): move doc/doc-ref from meta section to type level per KSY spec`
  - Files: All 38 `*.ksy` files under `earlysim/datamodel/protocols/ualink/`
  - Pre-commit: `python earlysim/datamodel/scripts/validate_ksy.py --all earlysim/datamodel/protocols/ualink/`

---

### Phase 1: Metadata & Version Alignment

- [x] 1. Update metadata.yaml, constraints.yaml, README.md, packet_types.yaml, and field_definitions/

  **What to do**:

  **metadata.yaml** (update version strings and layer definitions ONLY):
  - Change `ualink_spec_version: "1.0"` → `"1.5"` (line 8)
  - Change `ualink_spec_date: "2025-04-08"` → `"2026-01-13"` (line 9)
  - Update comment on line 94 from "Based on UALink200 Specification v1.0" → "Based on UALink 1.5 Specification"
  - Add new layers to `layers:` section:
    - `collectives: { sublayers: [primitives, block_collectives, management] }`
    - `ras: { sublayers: [error_types, error_handling, drop_mode] }`
  - DO NOT update `coverage:` counts yet (deferred to Phase 6)

  **constraints.yaml**:
  - Update header comment: "Source: UALink200 Specification v1.0" → "Source: UALink 1.5 Specification"
  - Update `version_compatibility.ualink200_base.version`: `"1.0"` → `"1.5"`
  - Update `version_compatibility.ualink200_base.description` to reflect v1.5 scope
  - Add new constraint sections (values from spec):
    - `collectives_layer:` — max_accelerators_per_pod: 1024, group_table_entries: 1024, submission_queues_max: 64, control_block_entries_max: 128, buffer_alignment_bytes: 256, transfer_length_multiple_bytes: 256
    - `ras_layer:` — error_types: [upli_control, upli_data, upli_protocol, switch_core_control, switch_core_data, link_down], handling_mechanisms: [tl_drop_mode, originator_drop_mode, completer_drop_mode, isolation_mode]
    - `switch_requirements:` — routing_table_key_bits: 10, max_stations: 64, ports_per_station: 4, bifurcation_modes: ["1x4", "2x2", "4x1"], latency_goals_ns: {128_lane: 200, 256_lane: 250, 512_lane: 300}
    - `manageability:` — max_accelerators_per_pod: 1024, pod_controller_required: true
  - Add DL PwrDn and Link Resiliency parameters to `datalink_layer:`
    - `dl_pwrdn_control_flits_before_low_power: 10`
    - `link_resiliency_optional: true`
    - `link_folding_optional: true`
    - `link_width_negotiation_response_timeout_us: 1.0`
    - `link_width_negotiation_decision_pending_timeout_ms: 10`

  **README.md**:
  - Update header: `**UALink Specification**: v1.0 (UALink200), v1.5 (DLPL)` → `**UALink Specification**: v1.5 (Common + DLPL)`
  - Update Specification References table to show v1.5 entries:
    - `UALink_Common_Specification | v1.5 Draft Rev 0.9`
    - `UALink_1.5_DLPL_200G | v1.5 RC`
  - Add `collectives/` and `ras/` to directory structure listing
  - DO NOT update coverage table counts yet (deferred to Phase 6)

  **packet_types.yaml**:
  - Update header comment: "Source: UALink200 Specification v1.0" → "Source: UALink 1.5 Specification"
  - Add placeholder sections for new layers (exact files TBD in Phases 3-5):
    - `collectives: { primitives: [], block_collectives: [], management: [] }`
    - `ras: { error_types: [], error_handling: [] }`
  - DO NOT update summary counts yet (deferred to Phase 6)
  - Update all existing `spec_ref` values from "UALink200" to "UALink 1.5" prefix

  **field_definitions/*.yaml** (6 files):
  - `tl_flit.yaml`: Update `spec_ref: "UALink200 Section 5, Table 5-1"` → `"UALink 1.5 Common Spec Section 5, Table 5-1"`
  - `dl_flit.yaml`: Update `spec_ref: "UALink200 Section 6, UALink 1.5 DLPL"` → `"UALink 1.5 DLPL Section 2"`
  - `response_field.yaml`: Update all `spec_ref` and `spec_table` values to v1.5 references
  - `upli_request_channel.yaml`: Update `spec_ref: "UALink200 Table 2-2"` → `"UALink 1.5 Common Spec Table 2-2"`
  - `link_state.yaml`: Update `spec_ref: "UALink200 Section 6.7"` → `"UALink 1.5 DLPL Section 2.7"`
  - `flow_control_field.yaml`: Update `spec_ref: "UALink200 Table 5-38"` → `"UALink 1.5 Common Spec Table 5-38"`

  **Must NOT do**:
  - Do not update coverage counts in metadata.yaml (deferred to Phase 6)
  - Do not update summary counts in packet_types.yaml (deferred to Phase 6)
  - Do not update coverage table in README.md (deferred to Phase 6)
  - Do not modify any KSY files

  **Recommended Agent Profile**:
  - **Category**: `unspecified-low`
  - **Skills**: []
    - No specialized skills needed — straightforward YAML/Markdown edits

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Wave 1 (solo)
  - **Blocks**: Tasks 2-6 (all Phase 2 tasks)
  - **Blocked By**: Task 0

  **References**:

  **Pattern References**:
  - `earlysim/datamodel/protocols/ualink/metadata.yaml` — Current metadata (lines 8-9 for version, ~line 30 for layers, ~line 80 for coverage)
  - `earlysim/datamodel/protocols/ualink/constraints.yaml` — Current constraints (line 3 for comment, line 119 for version_compatibility)
  - `earlysim/datamodel/protocols/ualink/README.md` — Current README (line 3 for version, lines 13-20 for coverage, lines 22-36 for directory structure, lines 48-49 for spec refs)
  - `earlysim/datamodel/protocols/ualink/reference/packet_types.yaml` — Current packet types (line 3 for comment, lines 175-178 for summary)

  **Spec References**:
  - `earlysim/docs/references/UALink/UALink_Common_Specification_Draft_Rev1.5_v0.9/UALink_Common_Specification_Draft_Rev1.5_v0.9.md` — Common Spec (Ch3 RAS, Ch6 INC, Ch7 Manageability, Ch9 Switch Requirements for constraint values)
  - `earlysim/docs/references/UALink/UALink_1.5_DLPL_200G_NCB_RC/UALink_1.5_DLPL_200G_NCB_RC.md` — DLPL Spec (§2.4.3.3 for Link Width Negotiation timeout values, §2.9 for Link Folding parameters)

  **Acceptance Criteria**:

  ```
  Scenario: YAML files are valid
    Tool: Bash (python)
    Steps:
      1. python -c "import yaml; yaml.safe_load(open('earlysim/datamodel/protocols/ualink/metadata.yaml'))"
      2. python -c "import yaml; yaml.safe_load(open('earlysim/datamodel/protocols/ualink/constraints.yaml'))"
      3. python -c "import yaml; yaml.safe_load(open('earlysim/datamodel/protocols/ualink/reference/packet_types.yaml'))"
      4. For each file in reference/field_definitions/*.yaml: yaml.safe_load
    Expected Result: No exceptions
    Evidence: Command output captured

  Scenario: Version strings updated
    Tool: Bash (grep)
    Steps:
      1. grep 'ualink_spec_version' metadata.yaml → contains "1.5"
      2. grep -c '"1.0"' metadata.yaml → 0 (no remaining v1.0 references in version fields)
      3. grep 'version:' constraints.yaml → version_compatibility shows "1.5"
    Expected Result: All v1.0 version references replaced
    Evidence: grep output captured

  Scenario: New layers defined
    Tool: Bash (grep)
    Steps:
      1. grep 'collectives:' metadata.yaml → exists in layers section
      2. grep 'ras:' metadata.yaml → exists in layers section
      3. grep 'collectives_layer:' constraints.yaml → exists
      4. grep 'ras_layer:' constraints.yaml → exists
    Expected Result: New layer definitions present
    Evidence: grep output captured

  Scenario: KSY validation still passes (no regression)
    Tool: Bash (validate_ksy.py)
    Steps:
      1. python earlysim/datamodel/scripts/validate_ksy.py --all earlysim/datamodel/protocols/ualink/
    Expected Result: Exit code 0
    Evidence: Validation output captured
  ```

  **Commit**: YES
  - Message: `feat(ualink): update metadata and references for UALink spec v1.5`
  - Files: `metadata.yaml`, `constraints.yaml`, `README.md`, `reference/packet_types.yaml`, `reference/field_definitions/*.yaml`
  - Pre-commit: `python earlysim/datamodel/scripts/validate_ksy.py --all earlysim/datamodel/protocols/ualink/`

---

### Phase 2: Field-Level Verification (5 parallel tasks)

- [x] 2. Phase 2a — UPLI Layer Verification (8 KSY files)

  **What to do**:
  - Read each of the 8 UPLI KSY files and compare against UALink 1.5 Common Spec Chapter 2
  - Update `x-spec` metadata: table numbers, section numbers, page numbers, spec_version → "1.5", spec_date → "2026-01-13"
  - Update `doc-ref` strings (now at type level after Task 0 fix) to reference v1.5
  - Update `x-spec-ref` annotations on individual fields
  - For `commands.ksy`: Verify all 12 existing opcodes still valid in v1.5 Table 2-6. Add 10 new INC command opcodes (ReadReduce 04h, WriteMulticast 26h, WriteFullMulticast 27h, AtomicNRMulticast 33h, BlockCollectiveInvoke 20h, BlockCollectiveAllocate 21h, BlockCollectiveDeallocate 22h, BlockRead 05h, BlockWriteFull 23h, BlockWrite — verify exact opcode). This IS a structural change.
  - For other UPLI files: Verify field definitions match v1.5 tables (likely unchanged)

  **Must NOT do**:
  - Do not change field definitions (seq:, types:, instances:) UNLESS the spec table shows a change
  - Do not add new files — new collectives UPLI commands go in existing commands.ksy

  **Recommended Agent Profile**:
  - **Category**: `deep`
  - **Skills**: []
    - Reason: Requires careful cross-referencing between spec tables and KSY files

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 3, 4, 5, 6)
  - **Blocks**: Task 7 (Phase 3)
  - **Blocked By**: Task 1

  **References**:

  **Pattern References**:
  - `earlysim/datamodel/protocols/ualink/upli/commands.ksy` — Command opcodes (221 lines, Table 2-6)
  - `earlysim/datamodel/protocols/ualink/upli/request_channel.ksy` — Request channel (338 lines, Table 2-2) — EXEMPLAR for field patterns

  **Spec References**:
  - Common Spec Chapter 2 (UPLI Interface) — Tables 2-1 through 2-6
  - Common Spec Chapter 6 (INC) — New command opcodes for collectives

  **Files to verify**:
  - `upli/commands.ksy` — Table 2-6 (STRUCTURAL CHANGE: add 10 new opcodes)
  - `upli/request_channel.ksy` — Table 2-2
  - `upli/originator_data_channel.ksy` — Table 2-3
  - `upli/read_response_channel.ksy` — Table 2-4
  - `upli/write_response_channel.ksy` — Table 2-5
  - `upli/status_codes.ksy` — Table 2-7
  - `upli/protocols/connection_handshake.ksy` — Section 2.8
  - `upli/protocols/flow_control.ksy` — Section 2.9

  **Acceptance Criteria**:

  ```
  Scenario: UPLI KSY files have v1.5 spec references
    Tool: Bash (python)
    Steps:
      1. For each of 8 UPLI KSY files:
         python -c "import yaml; d=yaml.safe_load(open('<file>')); assert d['x-spec']['spec_version']=='1.5', f'Wrong version in <file>'"
    Expected Result: All 8 files have spec_version "1.5"
    Evidence: Command output

  Scenario: commands.ksy has new INC opcodes
    Tool: Bash (grep)
    Steps:
      1. grep -c 'read_reduce\|write_multicast\|write_full_multicast\|atomic_nr_multicast\|block_collective_invoke\|block_collective_allocate\|block_collective_deallocate\|block_read\|block_write_full' upli/commands.ksy
    Expected Result: Count >= 9 (all new opcodes present)
    Evidence: grep output

  Scenario: KSY validation passes
    Tool: Bash (validate_ksy.py)
    Steps:
      1. python validate_ksy.py --all earlysim/datamodel/protocols/ualink/upli/
    Expected Result: Exit code 0
    Evidence: Validation output
  ```

  **Commit**: YES (standalone — one commit per layer for easy revert)
  - Message: `feat(ualink/upli): verify UPLI layer against UALink 1.5 spec`
  - Files: `upli/*.ksy`

---

- [x] 3. Phase 2b — Transaction Layer Verification (9 KSY files)

  **What to do**:
  - Read each of the 9 Transaction KSY files and compare against UALink 1.5 Common Spec Chapter 5
  - Update `x-spec` metadata: table numbers, section numbers, page numbers, spec_version → "1.5", spec_date → "2026-01-13"
  - Update `doc-ref` strings (now at type level after Task 0 fix) and `x-spec-ref` annotations
  - Verify field definitions match v1.5 tables (likely unchanged — core TL parameters confirmed unchanged)

  **Must NOT do**:
  - Do not change field definitions unless spec table shows a change
  - Do not add new types for INC compressed responses (those are Phase 3 scope)

  **Recommended Agent Profile**:
  - **Category**: `deep`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 2, 4, 5, 6)
  - **Blocks**: Task 7
  - **Blocked By**: Task 1

  **References**:
  - `earlysim/datamodel/protocols/ualink/transaction/request_field.ksy` — Tables 5-29, 5-31 (133 lines)
  - `earlysim/datamodel/protocols/ualink/transaction/response_field.ksy` — Tables 5-30, 5-34, 5-36 (317 lines)
  - Common Spec Chapter 5 (Transaction Layer) — Tables 5-1 through 5-38

  **Files to verify**:
  - `transaction/tl_flit.ksy`, `transaction/control_half_flit.ksy`, `transaction/data_half_flit.ksy`, `transaction/message_half_flit.ksy`, `transaction/request_field.ksy`, `transaction/response_field.ksy`, `transaction/flow_control_field.ksy`, `transaction/protocols/compression.ksy`, `transaction/protocols/address_cache.ksy`

  **Acceptance Criteria**:
  ```
  Scenario: Transaction KSY files have v1.5 spec references
    Tool: Bash (python)
    Steps:
      1. For each of 9 Transaction KSY files: assert x-spec.spec_version == "1.5"
    Expected Result: All 9 files updated
    Evidence: Command output

  Scenario: KSY validation passes
    Tool: Bash (validate_ksy.py)
    Steps:
      1. python validate_ksy.py --all earlysim/datamodel/protocols/ualink/transaction/
    Expected Result: Exit code 0
  ```

  **Commit**: YES (standalone — one commit per layer for easy revert)
  - Message: `feat(ualink/transaction): verify Transaction layer against UALink 1.5 spec`

---

- [x] 4. Phase 2c — Data Link Layer Verification (12 KSY files) — STRUCTURAL CHANGES

  **What to do**:
  - Read each of the 12 Data Link KSY files and compare against UALink 1.5 DLPL Spec Chapter 2
  - Update `x-spec` metadata: spec_version → "1.5", spec_date → "2026-01-12", update section/table/page to DLPL references
  - **STRUCTURAL CHANGES required for these files**:
    - `basic_messages.ksy`: Add Tx Ready Notification (mtype=0b001, Table 2-8) — new enum value + field layout
    - `control_messages.ksy`: Add Link Width Negotiation (mtype=0b000, Table 2-10) — new enum value + field layout with Priority, Channel.TargetState, Channel.Command, Channel.Response, Tx Ready Support fields
    - `protocols/link_state.ksy`: Update transitions for Link Resiliency (per-PL "sub" state machines), add programmable DL Up→Fault delay (0-10ms), update state diagram
    - `protocols/link_resiliency.ksy`: MAJOR EXPANSION — currently ~89 lines with generic refs. Expand with: Table 2-19 skew budget, TDM mux/demux, reordering, DL "sub" state machines, fault handling, fast recovery, link down recovery (§2.8)
    - `protocols/link_folding.ksy`: MAJOR EXPANSION — currently ~98 lines with generic refs. Expand with: Link Width Negotiation integration, PwrDn sequence, unfolding sequence, folding recovery, RAM coordination (§2.9)
    - `protocols/link_level_replay.ksy`: Add TL Backpressure rules (§2.6.6.2) and Link Width Unfolding replay rules (§2.6.6.11)
  - For remaining files (dl_flit.ksy, flit_header.ksy, segment_header.ksy, crc.ksy, uart_messages.ksy, vendor_defined.ksy): Metadata-only updates (core formats confirmed unchanged)

  **Must NOT do**:
  - Do not change dl_flit.ksy, flit_header.ksy, segment_header.ksy, crc.ksy field definitions (confirmed unchanged)
  - Do not create DL-PL Interface files (Appendix B is informative, not normative)

  **Recommended Agent Profile**:
  - **Category**: `deep`
  - **Skills**: []
    - Reason: Most complex Phase 2 task — requires structural expansion of 6 files

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 2, 3, 5, 6)
  - **Blocks**: Task 7
  - **Blocked By**: Task 1

  **References**:

  **Pattern References**:
  - `earlysim/datamodel/protocols/ualink/datalink/protocols/link_state.ksy` — State machine exemplar (209 lines)
  - `earlysim/datamodel/protocols/ualink/datalink/messages/basic_messages.ksy` — Basic message pattern (70 lines)
  - `earlysim/datamodel/protocols/ualink/datalink/messages/control_messages.ksy` — Control message pattern (62 lines)

  **Spec References**:
  - DLPL Spec §2.4.2.6 — Tx Ready Notification (Table 2-8)
  - DLPL Spec §2.4.3.3 — Link Width Negotiation (Table 2-10, pages 33-36)
  - DLPL Spec §2.6.6.2 — TL Backpressure rules
  - DLPL Spec §2.6.6.11 — Link Width Unfolding replay rules
  - DLPL Spec §2.7.1 — DL Link States (5 states, programmable delay)
  - DLPL Spec §2.8 — Link Resiliency (Table 2-19, Figures 2-23 through 2-39)
  - DLPL Spec §2.9 — Link Folding (Figures 2-40 through 2-48)

  **Acceptance Criteria**:
  ```
  Scenario: Data Link KSY files have v1.5 spec references
    Tool: Bash (python)
    Steps:
      1. For each of 12 DL KSY files: assert x-spec.spec_version == "1.5"
    Expected Result: All 12 files updated

  Scenario: New DL message types present
    Tool: Bash (grep)
    Steps:
      1. grep 'tx_ready_notification' basic_messages.ksy → found
      2. grep 'link_width_negotiation' control_messages.ksy → found
    Expected Result: Both new message types defined

  Scenario: Link Resiliency expanded
    Tool: Bash (wc)
    Steps:
      1. wc -l protocols/link_resiliency.ksy → >= 150 lines (was ~89)
    Expected Result: File substantially expanded

  Scenario: Link Folding expanded
    Tool: Bash (wc)
    Steps:
      1. wc -l protocols/link_folding.ksy → >= 150 lines (was ~98)
    Expected Result: File substantially expanded

  Scenario: KSY validation passes
    Tool: Bash (validate_ksy.py)
    Steps:
      1. python validate_ksy.py --all earlysim/datamodel/protocols/ualink/datalink/
    Expected Result: Exit code 0
  ```

  **Commit**: YES (standalone — one commit per layer for easy revert)
  - Message: `feat(ualink/datalink): verify and expand Data Link layer for UALink 1.5 DLPL spec`

---

- [x] 5. Phase 2d — Physical Layer Verification (4 KSY files)

  **What to do**:
  - Read each of the 4 Physical KSY files and compare against UALink 1.5 DLPL Spec Chapter 3
  - Update `x-spec` metadata: spec_version → "1.5", spec_date → "2026-01-12", update to DLPL section/table/page
  - For `alignment_markers.ksy`: Add Rapid Alignment Markers (RAMs) content from §3.3.7 — RAM period (Table 3-5), am_next_count variable, alignment lock rules. This IS a structural change.
  - For `control_ordered_sets.ksy`: Add new flit code sequences (Idle Start, Fault Start, PwrDn, PwrDn Start) from §3.3. This IS a structural change.
  - For `reconciliation_sublayer.ksy`: Add PL ID signaling, Link Resiliency transmit alignment (§3.8)
  - For `protocols/link_training.ksy`: Add PMA Symbol Pair Demux requirement (§3.3.8)

  **Must NOT do**:
  - Do not create separate RAM KSY file — RAMs use same format as AMs, add to alignment_markers.ksy

  **Recommended Agent Profile**:
  - **Category**: `deep`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 2, 3, 4, 6)
  - **Blocks**: Task 7
  - **Blocked By**: Task 1

  **References**:
  - DLPL Spec §3.3.7 — Rapid Alignment Markers (Table 3-5, Figure 3-3)
  - DLPL Spec §3.3.8 — PMA Symbol Pair Demultiplexing
  - DLPL Spec §3.8 — Link Resiliency at PL Level

  **Acceptance Criteria**:
  ```
  Scenario: Physical KSY files have v1.5 spec references
    Tool: Bash (python)
    Steps:
      1. For each of 4 Physical KSY files: assert x-spec.spec_version == "1.5"

  Scenario: RAM content added to alignment_markers.ksy
    Tool: Bash (grep)
    Steps:
      1. grep -i 'rapid_alignment\|ram_period\|am_next_count' physical/alignment_markers.ksy → found

  Scenario: New flit code sequences in control_ordered_sets.ksy
    Tool: Bash (grep)
    Steps:
      1. grep -i 'idle_start\|fault_start\|pwrdn' physical/control_ordered_sets.ksy → found

  Scenario: KSY validation passes
    Tool: Bash (validate_ksy.py)
    Steps:
      1. python validate_ksy.py --all earlysim/datamodel/protocols/ualink/physical/
    Expected Result: Exit code 0
  ```

  **Commit**: YES (standalone — one commit per layer for easy revert)
  - Message: `feat(ualink/physical): verify and expand Physical layer for UALink 1.5 DLPL spec`

---

- [x] 6. Phase 2e — Security Layer Verification (5 KSY files)

  **What to do**:
  - Read each of the 5 Security KSY files and compare against UALink 1.5 Common Spec Chapter 8
  - Update `x-spec` metadata: spec_version → "1.5", spec_date → "2026-01-13"
  - For `encryption.ksy`: Verify encryption modes, add PCRC reference (§8.5.15)
  - For `iv_format.ksy`: Verify IV format fields. Note: §8.6.4.3 adds NEW IV formats for collective security — these will be added in Phase 5
  - For `protocols/key_derivation.ksy`: Verify KDF. Note: §8.5.9.2 has enhanced KDF context — verify if existing file covers this or needs expansion. §8.6.4.2 adds collective-specific KDF — Phase 5 scope
  - For `authentication.ksy`: Verify auth tag format
  - For `protocols/key_rotation.ksy`: Verify key rotation states

  **Must NOT do**:
  - Do not add collective security content yet (Phase 5 scope)
  - Do not add multi-path routing IV format yet (Phase 5 scope)

  **Recommended Agent Profile**:
  - **Category**: `deep`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 2-5)
  - **Blocks**: Task 9 (Phase 5)
  - **Blocked By**: Task 1

  **References**:
  - `earlysim/datamodel/protocols/ualink/security/encryption.ksy` — 483 lines, Tables 9-4 through 9-7
  - `earlysim/datamodel/protocols/ualink/security/iv_format.ksy` — 216 lines, Table 9-3
  - Common Spec Chapter 8 (Security) — §8.5.15 PCRC, §8.5.9.2 Enhanced KDF

  **Acceptance Criteria**:
  ```
  Scenario: Security KSY files have v1.5 spec references
    Tool: Bash (python)
    Steps:
      1. For each of 5 Security KSY files: assert x-spec.spec_version == "1.5"

  Scenario: KSY validation passes
    Tool: Bash (validate_ksy.py)
    Steps:
      1. python validate_ksy.py --all earlysim/datamodel/protocols/ualink/security/
    Expected Result: Exit code 0
  ```

  **Commit**: YES (standalone — one commit per layer for easy revert)
  - Message: `feat(ualink/security): verify Security layer against UALink 1.5 spec`

---

### Phase 2 Validation Gate

After ALL Phase 2 tasks complete:
```bash
python earlysim/datamodel/scripts/validate_ksy.py --all earlysim/datamodel/protocols/ualink/
# Assert: exit code 0 — ALL 38 files pass
```

---

### Phase 3: In-Network Collectives (New Files)

- [x] 7. Create Collectives KSY files (~8 new files)

  **What to do**:
  - Create `earlysim/datamodel/protocols/ualink/collectives/` directory
  - Create the following KSY files following the exemplar pattern from `upli/request_channel.ksy`:

  **Packet Format Files** (~5 files):
  1. `collectives/collective_primitives.ksy` — Collective Primitive request/response flows (§6.2, Table 6-1, Figures 6-6/6-7). Fields: ReadReduce, WriteMulticast, WriteFullMulticast, AtomicNRMulticast request formats. Response reduction rules (Table 6-1).
  2. `collectives/block_collective_allocate.ksy` — BlockCollectiveAllocate request/response (§6.3.2, Table 6-2, Figures 6-9/6-10). Fields: Submission Queue Number [7:2], Number of Queue Entries [14:8], Status Buffer Address.
  3. `collectives/block_collective_deallocate.ksy` — BlockCollectiveDeallocate request/response (§6.3.3, Table 6-3, Figures 6-11/6-12). Fields: Submission Queue Number [7:2], Status Buffer Address.
  4. `collectives/block_collective_invoke.ksy` — BlockCollectiveInvoke request/response (§6.3.4, Tables 6-4/6-5, Figures 6-13/6-14/6-15). Fields: Submission Queue Number [7:2], Base Address [56:12], Status Buffer fields (V0, V1, IStatus, W, BStatus, AccID, FailAddress).
  5. `collectives/block_collective_control_block.ksy` — Block Collective Control Block format (§6.3.7, Tables 6-6/6-7/6-8). Fields: BTYPE (8b), CTYPE (8b), LEN (24b), ROPDT (8b), RMODE (8b), I_OFF (24b), O_OFF (24b), S_OFF (24b), XSIZE (32b), YSIZE (32b), SSIZE (32b), SSEED (32b). Enums: Collective Type (Table 6-7: BROADCAST, REDUCE, ALL-REDUCE, strided/non-strided variants).

  **Protocol/State Machine Files** (~2 files):
  6. `collectives/protocols/collective_primitive_flow.ksy` — Collective Primitive request/response flow state machine (§6.2.2, Figures 6-6/6-7). States: IDLE, REQUEST_SENT, REDUCING, RESPONSE_COMPLETE.
  7. `collectives/protocols/block_collective_flow.ksy` — Block Collective invocation flow state machine (§6.3.9, Figures 6-20 through 6-25). States: IDLE, ALLOCATED, INVOKED, INPUT_READ, COMPUTING, OUTPUT_WRITE, STATUS_UPDATE, COMPLETE.

  **Reference File** (~1 file):
  8. `collectives/group_table.ksy` — Group Table structure (§6.2.1). Fields: GroupID[9:0] → Group Accelerator Mask (1024-bit bitmask). This is a switch structure, not a packet, but models the key data structure.

  **For each new file, MUST include**:
  - Header comment with "EXEMPLARY QUALITY" and Feature: 024-add-ualink-to-topology
  - meta: id (ualink_collectives_*), title, endian: be, bit-endian: be, license, ks-version: "0.10"
  - doc: (multi-paragraph, at TYPE LEVEL — sibling of meta, NOT inside meta)
  - doc-ref: (at TYPE LEVEL — sibling of meta, NOT inside meta)
  - x-spec: table, section, page, spec_version: "1.5", spec_date: "2026-01-13"
  - x-packet: layer: "collectives", sublayer, category
  - x-related-headers: cross-references to upli/commands.ksy and other relevant files
  - enums: with hex values, id, doc, x-required
  - seq: with per-field id, type, doc, x-required, x-constraint, x-spec-ref
  - Minimum 50 lines per file

  **Must NOT do**:
  - Do not model TBD sections (§6.5 Reproducibility, §6.6 Rounding Modes)
  - Do not create speculative helper types
  - Do not create YAML reference files unless file meets documented criteria

  **Recommended Agent Profile**:
  - **Category**: `deep`
  - **Skills**: []
    - Reason: Largest phase — entirely new content requiring careful spec reading

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 3 (with Tasks 8, 9)
  - **Blocks**: Task 10 (Phase 6)
  - **Blocked By**: Tasks 2, 3, 4 (Phase 2a-c must complete for cross-references)

  **References**:

  **Pattern References**:
  - `earlysim/datamodel/protocols/ualink/upli/request_channel.ksy` — EXEMPLAR for packet format files (339 lines)
  - `earlysim/datamodel/protocols/ualink/datalink/protocols/link_state.ksy` — EXEMPLAR for state machine files (209 lines)
  - `earlysim/datamodel/protocols/ualink/upli/commands.ksy` — Pattern for enum-heavy files (221 lines)

  **Spec References**:
  - Common Spec §6.1-6.4 — Full INC chapter (lines 3150-3632)
  - Common Spec Tables 6-1 through 6-8 — All field definitions
  - Common Spec Figures 6-1 through 6-26 — All diagrams

  **Acceptance Criteria**:
  ```
  Scenario: Collectives directory exists with expected files
    Tool: Bash (ls/find)
    Steps:
      1. ls -d earlysim/datamodel/protocols/ualink/collectives/ → exists
      2. find earlysim/datamodel/protocols/ualink/collectives/ -name '*.ksy' | wc -l → >= 7
    Expected Result: Directory exists with >= 7 KSY files

  Scenario: All new files have valid structure
    Tool: Bash (python)
    Steps:
      1. For each new KSY file:
         python -c "import yaml; d=yaml.safe_load(open('<file>')); assert 'meta' in d; assert 'x-spec' in d; assert d['x-spec']['spec_version']=='1.5'"
    Expected Result: All files have required sections

  Scenario: All new files meet minimum quality
    Tool: Bash (wc)
    Steps:
      1. For each new KSY file: wc -l → >= 50 lines
    Expected Result: No stub files

  Scenario: KSY validation passes
    Tool: Bash (validate_ksy.py)
    Steps:
      1. python validate_ksy.py --all earlysim/datamodel/protocols/ualink/collectives/
    Expected Result: Exit code 0
  ```

  **Commit**: YES
  - Message: `feat(ualink): add In-Network Collectives datamodel (UALink 1.5 Chapter 6)`
  - Files: `collectives/*.ksy`, `collectives/protocols/*.ksy`

---

### Phase 4: RAS & Error Handling (New Files)

- [x] 8. Create RAS KSY files (~3 new files)

  **What to do**:
  - Create `earlysim/datamodel/protocols/ualink/ras/` directory
  - Create the following KSY files:

  1. `ras/error_types.ksy` — RAS error type enumeration (§3.1.2). Enums: upli_control_error, upli_data_error, upli_protocol_error, switch_core_control_error, switch_core_data_error, link_down_error. Include sub-types for UPLI control errors (ReqVldParity, RdRspVldParity, etc. — 16 sub-types from §3.1.2).
  2. `ras/error_handling.ksy` — Error handling mechanisms (§3.1.3). Enums: tl_drop_mode, originator_drop_mode, completer_drop_mode, isolation_mode. Document Watch Dog Timers, Completion Timeout Responses.
  3. `ras/protocols/error_recovery.ksy` — Error recovery state machine (§3.1.4, Figures 3-1 through 3-11). States: NORMAL, UPLI_DATA_ERROR, UPLI_CONTROL_ERROR, TL_DROP_MODE, ISOLATION_MODE, LINK_DOWN, RECOVERY. Transitions from Figures 3-2 through 3-11.

  **Must NOT do**:
  - Do not model implementation-specific error handling details
  - Do not add error injection mechanisms (those are switch debug features, not protocol)

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 3 (with Tasks 7, 9)
  - **Blocks**: Task 10
  - **Blocked By**: Task 1

  **References**:
  - Common Spec §3.1 — Full RAS chapter (lines 1837-2059)
  - Common Spec Figures 3-1 through 3-11 — Error flow diagrams
  - `earlysim/datamodel/protocols/ualink/datalink/protocols/link_state.ksy` — State machine exemplar

  **Acceptance Criteria**:
  ```
  Scenario: RAS directory exists with expected files
    Tool: Bash (ls/find)
    Steps:
      1. ls -d earlysim/datamodel/protocols/ualink/ras/ → exists
      2. find earlysim/datamodel/protocols/ualink/ras/ -name '*.ksy' | wc -l → >= 3

  Scenario: KSY validation passes
    Tool: Bash (validate_ksy.py)
    Steps:
      1. python validate_ksy.py --all earlysim/datamodel/protocols/ualink/ras/
    Expected Result: Exit code 0
  ```

  **Commit**: YES
  - Message: `feat(ualink): add RAS error handling datamodel (UALink 1.5 Chapter 3)`

---

### Phase 5: Collective Security (Updated + New Files)

- [x] 9. Update existing and create new Security files for collective security (~4 files)

  **What to do**:

  **Update existing files** (2 files):
  - `security/iv_format.ksy`: Add collective security IV formats from Tables 27-28 (§8.6.4.3) and multi-path routing IV format from Table 29 (§8.7). Add new types for accelerator-switch IV and switch-accelerator IV with fields: Source ID (10b), Destination ID (10b), Source Port Num (8b), Destination Port Num (8b), Stream ID (2b), Counter (32b).
  - `security/protocols/key_derivation.ksy`: Add collective-specific KDF context from Tables 25-26 (§8.6.4.2). Add new types for accelerator-switch KDF context and switch-accelerator KDF context with fields: Padded Source ID (16b), Padded Destination ID (16b), Source Port Number (8b), Epoch Counter Value (32b).

  **Create new files** (2 files):
  1. `security/collective_security.ksy` — Collective security architecture (§8.6). Fields: Switch Port Identifier (Switch ID 10b, Port Number 10b), Neighbor Information (DevID, DevType, PortNum), INC Master Key (32B), TX/RX Key Material. Enums: key_state (from §8.6.4.1). Document: crypto engine per switch port, GroupTable security, routing table locking.
  2. `security/multipath_routing.ksy` — Multi-path routing security (§8.7, Table 29). Fields: Phase (4 epochs), Epoch (512 transactions), Epoch Counter (2b), Sequence Number (9b). IV format for multipath with Counter (21b), Epoch number (2b), Sequence number (9b). Tag management: 512-bit vector per epoch per source accelerator.

  **Must NOT do**:
  - Do not modify encryption.ksy or authentication.ksy (no changes needed for collective security)
  - Do not add SPDM/TEE/SSM implementation details (those are switch firmware, not protocol format)

  **Recommended Agent Profile**:
  - **Category**: `deep`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 3 (with Tasks 7, 8)
  - **Blocks**: Task 10
  - **Blocked By**: Task 6 (Phase 2e — Security verification must complete first)

  **References**:
  - `earlysim/datamodel/protocols/ualink/security/iv_format.ksy` — Existing IV format (216 lines, Table 9-3) — EXEMPLAR
  - `earlysim/datamodel/protocols/ualink/security/protocols/key_derivation.ksy` — Existing KDF (359 lines)
  - Common Spec §8.6 — Collective Security (lines 4814-5031, Tables 25-28)
  - Common Spec §8.7 — Multi-path Routing (lines 5032-5086, Table 29)

  **Acceptance Criteria**:
  ```
  Scenario: New security files exist
    Tool: Bash (ls)
    Steps:
      1. ls earlysim/datamodel/protocols/ualink/security/collective_security.ksy → exists
      2. ls earlysim/datamodel/protocols/ualink/security/multipath_routing.ksy → exists

  Scenario: IV format updated with collective formats
    Tool: Bash (grep)
    Steps:
      1. grep -i 'collective\|accelerator_switch\|switch_accelerator' security/iv_format.ksy → found

  Scenario: KSY validation passes
    Tool: Bash (validate_ksy.py)
    Steps:
      1. python validate_ksy.py --all earlysim/datamodel/protocols/ualink/security/
    Expected Result: Exit code 0
  ```

  **Commit**: YES
  - Message: `feat(ualink): add collective security and multi-path routing (UALink 1.5 §8.6-8.7)`

---

### Phase 6: Final Constraints, Counts & Documentation

- [x] 10. Update CMakeLists.txt, finalize coverage counts, update packet_types.yaml

  **What to do**:

  **CMakeLists.txt**:
  - Add install() targets for `collectives/` and `ras/` directories
  - Verify GLOB_RECURSE pattern picks up new files

  **metadata.yaml** (finalize counts):
  - Update `coverage.total_packets` to actual count of packet KSY files
  - Update `coverage.total_protocols` to actual count of protocol KSY files
  - Update `coverage.by_layer` with actual per-layer counts including collectives and ras

  **packet_types.yaml** (finalize):
  - Populate `collectives:` section with actual file names from Phase 3
  - Populate `ras:` section with actual file names from Phase 4
  - Add new security files from Phase 5 to `security:` section
  - Update `protocols:` section with new protocol files
  - Update `summary:` counts

  **README.md** (finalize):
  - Update coverage table with actual counts
  - Verify directory structure listing includes all new directories

  **constraints.yaml** (verify):
  - Verify all constraint values match spec (spot-check against Common Spec §9 and DLPL)

  **Must NOT do**:
  - Do not modify any KSY files
  - Do not add documentation beyond what's needed for accuracy

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Wave 4 (solo, final)
  - **Blocks**: None (final task)
  - **Blocked By**: Tasks 7, 8, 9 (all Phase 3-5 tasks)

  **References**:
  - `earlysim/datamodel/protocols/ualink/CMakeLists.txt` — Current build config
  - All files created/modified in Phases 1-5

  **Acceptance Criteria**:
  ```
  Scenario: CMakeLists.txt covers new directories
    Tool: Bash (grep)
    Steps:
      1. grep 'collectives' earlysim/datamodel/protocols/ualink/CMakeLists.txt → found
      2. grep 'ras' earlysim/datamodel/protocols/ualink/CMakeLists.txt → found

  Scenario: metadata.yaml counts are consistent
    Tool: Bash (python)
    Steps:
      1. python -c "
         import yaml, glob
         with open('earlysim/datamodel/protocols/ualink/metadata.yaml') as f:
             m = yaml.safe_load(f)
         actual = len(glob.glob('earlysim/datamodel/protocols/ualink/**/*.ksy', recursive=True))
         declared = m['coverage']['total_packets'] + m['coverage']['total_protocols']
         assert actual == declared, f'MISMATCH: {actual} files vs {declared} declared'
         print(f'PASS: {actual} KSY files match declared count')
         "
    Expected Result: Counts match

  Scenario: All KSY files have valid x-spec metadata
    Tool: Bash (python)
    Steps:
      1. python -c "
         import yaml, glob, sys
         errors = []
         for f in sorted(glob.glob('earlysim/datamodel/protocols/ualink/**/*.ksy', recursive=True)):
             with open(f) as fh:
                 data = yaml.safe_load(fh.read())
             xspec = data.get('x-spec', {})
             if not xspec.get('spec_version'):
                 errors.append(f'{f}: missing x-spec.spec_version')
             if not xspec.get('section') and not xspec.get('table'):
                 errors.append(f'{f}: missing x-spec.section or x-spec.table')
         if errors:
             for e in errors: print(e)
             sys.exit(1)
         count = len(glob.glob('earlysim/datamodel/protocols/ualink/**/*.ksy', recursive=True))
         print(f'PASS: All {count} KSY files have valid x-spec metadata')
         "
    Expected Result: All files pass

  Scenario: Full validation passes
    Tool: Bash (validate_ksy.py)
    Steps:
      1. python earlysim/datamodel/scripts/validate_ksy.py --all earlysim/datamodel/protocols/ualink/
    Expected Result: Exit code 0
    Evidence: Final validation output
  ```

  **Commit**: YES
  - Message: `feat(ualink): finalize UALink 1.5 datamodel update — counts, CMake, documentation`

---

## Commit Strategy

> **11 fine-grained commits** — structural fix first, then one per layer in Phase 2 for easy selective revert.
> To back out a specific layer's changes: `git revert <commit-hash>`

| # | After Task | Message | Commit Hash | Files | Verification |
|---|------------|---------|-------------|-------|--------------|
| 1 | 0 | `fix(ualink): move doc/doc-ref from meta section to type level per KSY spec` | `0c63aca8` | All 38 *.ksy files | validate_ksy.py |
| 2 | 1 | `feat(ualink): update metadata and references for UALink spec v1.5` | `6e017e68` | metadata.yaml, constraints.yaml, README.md, reference/ | validate_ksy.py |
| 3 | 2 | `feat(ualink/upli): verify UPLI layer against UALink 1.5 spec` | `85df6d4f` | upli/*.ksy (8 files) | validate_ksy.py |
| 4 | 3 | `feat(ualink/transaction): verify Transaction layer against UALink 1.5 spec` | `f39a037f` | transaction/*.ksy (9 files) | validate_ksy.py |
| 5 | 4 | `feat(ualink/datalink): verify and expand Data Link layer for UALink 1.5 DLPL spec` | `133eda62` | datalink/*.ksy (12 files) | validate_ksy.py |
| 6 | 5 | `feat(ualink/physical): verify and expand Physical layer for UALink 1.5 DLPL spec` | `b8629388` | physical/*.ksy (4 files) | validate_ksy.py |
| 7 | 6 | `feat(ualink/security): verify Security layer against UALink 1.5 spec` | `e79efd8c` | security/*.ksy (5 files) | validate_ksy.py |
| 8 | 7 | `feat(ualink): add In-Network Collectives datamodel (UALink 1.5 Chapter 6)` | `4c618a8e` | collectives/*.ksy (8 new files) | validate_ksy.py |
| 9 | 8 | `feat(ualink): add RAS error handling datamodel (UALink 1.5 Chapter 3)` | `88c36009` | ras/*.ksy (3 new files) | validate_ksy.py |
| 10 | 9 | `feat(ualink): add collective security and multi-path routing (UALink 1.5 §8.6-8.7)` | `3571084f` | security/*.ksy (4 files) | validate_ksy.py |
| 11 | 10 | `feat(ualink): finalize UALink 1.5 datamodel update — counts, CMake, documentation` | `f8b5f0d7` | CMakeLists.txt, metadata.yaml, packet_types.yaml, README.md | validate_ksy.py + count check |

---

## Success Criteria

### Verification Commands
```bash
# Full validation
python earlysim/datamodel/scripts/validate_ksy.py --all earlysim/datamodel/protocols/ualink/
# Expected: exit code 0

# File count (51 KSY files, up from 38)
find earlysim/datamodel/protocols/ualink/ -name '*.ksy' | wc -l
# Expected: 51

# No remaining v1.0 version references in metadata
grep -r 'spec_version.*1\.0' earlysim/datamodel/protocols/ualink/metadata.yaml earlysim/datamodel/protocols/ualink/constraints.yaml
# Expected: empty output

# All KSY files have v1.5 spec_version
python -c "
import yaml, glob
for f in sorted(glob.glob('earlysim/datamodel/protocols/ualink/**/*.ksy', recursive=True)):
    with open(f) as fh:
        d = yaml.safe_load(fh.read())
    v = d.get('x-spec', {}).get('spec_version', 'MISSING')
    if v != '1.5':
        print(f'FAIL: {f} has spec_version={v}')
print('CHECK COMPLETE')
"
# Expected: No FAIL lines
```

### Final Checklist
- [x] All "Must Have" present (v1.5 references, new collectives/ras/security files, validation passes)
- [x] All "Must NOT Have" absent (no changes outside ualink/, no speculative types, no TBD sections modeled)
- [x] All KSY files pass validate_ksy.py (51/51 PASS)
- [x] metadata.yaml counts match actual file counts (51 total)
- [x] All new files follow exemplar pattern (≥50 lines, all x-* metadata)
