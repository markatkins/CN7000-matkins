# W-14-007: Add x-related-headers Cross-References to KSY Files

## TL;DR

> **Quick Summary**: Add `x-related-headers` sections to KSY files that reference other packet definitions, improving navigation and discoverability across the 38-file UALink datamodel.
> 
> **Deliverables**:
> - Updated KSY files with `x-related-headers` sections
> - Consistent cross-referencing pattern across datamodel
> 
> **Estimated Effort**: Medium (2-3 hours)
> **Parallel Execution**: YES - files can be updated in parallel by layer
> **Critical Path**: Task 1 (analysis) → Tasks 2-6 (parallel updates) → Task 7 (commit)

---

## Context

### Original Request
W-14-007 from UALink datamodel review: KSY files don't have `x-related-headers` sections to cross-reference related files, making navigation between related packet definitions difficult.

### Background
The UALink datamodel has 38 .ksy files across 5 layers. Many files reference other files in documentation but don't formally link them. For example, `dl_flit.ksy` references `segment_header.ksy`, `flit_header.ksy`, and `crc.ksy` but doesn't have a machine-readable cross-reference.

### Proposed Pattern
```yaml
x-related-headers:
  - file: "segment_header.ksy"
    relationship: "contains"
    description: "Segment headers within DL Flit"
  - file: "flit_header.ksy"
    relationship: "contains"
    description: "Flit header at start of DL Flit"
```

---

## Work Objectives

### Core Objective
Add `x-related-headers` sections to all KSY files that have relationships with other packet definitions.

### Concrete Deliverables
- Updated KSY files with `x-related-headers` sections
- Consistent relationship vocabulary (contains, references, extends, uses)

### Definition of Done
- [ ] All files with cross-references have `x-related-headers` section
- [ ] Relationship types are consistent
- [ ] All referenced files exist
- [ ] YAML validation passes for all modified files

### Must Have
- `x-related-headers` section after `x-packet` section
- Consistent relationship vocabulary
- Bidirectional references where appropriate

### Must NOT Have (Guardrails)
- **MUST NOT** add references to non-existent files
- **MUST NOT** change any existing field definitions
- **MUST NOT** modify x-spec or x-packet sections
- **MUST NOT** add circular references without clear purpose

---

## Verification Strategy (MANDATORY)

### Test Decision
- **Infrastructure exists**: NO (this is datamodel, not code)
- **User wants tests**: Manual-only (YAML validation)
- **Framework**: None (YAML syntax validation only)

### Automated Verification

```bash
# Verify all modified files are valid YAML
for f in $(git -C earlysim status --porcelain | grep ".ksy" | awk '{print $2}'); do
  python3 -c "import yaml; yaml.safe_load(open('earlysim/$f'))" && echo "$f: VALID" || echo "$f: INVALID"
done

# Verify x-related-headers sections exist
grep -l "x-related-headers:" earlysim/datamodel/protocols/ualink/**/*.ksy | wc -l
```

---

## Execution Strategy

### Parallel Execution Waves

```
Wave 1 (Start Immediately):
└── Task 1: Analyze relationships and create mapping

Wave 2 (After Wave 1 - All in Parallel):
├── Task 2: Update UPLI layer files (8 files)
├── Task 3: Update Transaction layer files (9 files)
├── Task 4: Update Datalink layer files (12 files)
├── Task 5: Update Physical layer files (4 files)
└── Task 6: Update Security layer files (5 files)

Wave 3 (After Wave 2):
└── Task 7: Validate and commit changes

Critical Path: Task 1 → Any Task 2-6 → Task 7
Parallel Speedup: ~50% faster than sequential
```

### Relationship Vocabulary

| Relationship | Meaning | Example |
|--------------|---------|---------|
| `contains` | This packet contains instances of the referenced type | dl_flit → segment_header |
| `references` | This packet references fields/types from the other | request_field → status_codes |
| `extends` | This packet extends or specializes the other | command_header → flit_header |
| `uses` | This packet uses the referenced protocol/mechanism | tl_flit → compression |
| `part-of` | This packet is a component of the referenced type | segment_header → dl_flit |

---

## TODOs

- [ ] 1. Analyze Relationships and Create Mapping

  **What to do**:
  - Review all 38 KSY files
  - Identify cross-references in doc blocks and type references
  - Create relationship mapping table
  - Document in notepad for use by subsequent tasks

  **Output**: Relationship mapping in `.sisyphus/notepads/w-14-007-x-related-headers/relationships.md`

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: `[]`

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Wave 1 (alone)
  - **Blocks**: Tasks 2, 3, 4, 5, 6
  - **Blocked By**: None

  **References**:
  - All 38 .ksy files in `earlysim/datamodel/protocols/ualink/`

  **Acceptance Criteria**:
  - [ ] All 38 files reviewed
  - [ ] Relationship mapping created
  - [ ] Mapping documented in notepad

  **Commit**: NO

---

- [ ] 2. Update UPLI Layer Files (8 files)

  **What to do**:
  - Add `x-related-headers` to UPLI layer files based on mapping
  - Files: commands.ksy, request_channel.ksy, read_response_channel.ksy, write_response_channel.ksy, status_codes.ksy, originator_data_channel.ksy, protocols/flow_control.ksy, protocols/connection_handshake.ksy

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: `[]`

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 3, 4, 5, 6)
  - **Blocks**: Task 7
  - **Blocked By**: Task 1

  **References**:
  - `earlysim/datamodel/protocols/ualink/upli/*.ksy`
  - `earlysim/datamodel/protocols/ualink/upli/protocols/*.ksy`
  - Relationship mapping from Task 1

  **Acceptance Criteria**:
  - [ ] All UPLI files with relationships have x-related-headers
  - [ ] YAML validation passes

  **Commit**: NO (groups with Task 7)

---

- [ ] 3. Update Transaction Layer Files (9 files)

  **What to do**:
  - Add `x-related-headers` to Transaction layer files based on mapping
  - Files: tl_flit.ksy, control_half_flit.ksy, message_half_flit.ksy, data_half_flit.ksy, request_field.ksy, response_field.ksy, flow_control_field.ksy, protocols/compression.ksy, protocols/address_cache.ksy

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: `[]`

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 2, 4, 5, 6)
  - **Blocks**: Task 7
  - **Blocked By**: Task 1

  **References**:
  - `earlysim/datamodel/protocols/ualink/transaction/*.ksy`
  - `earlysim/datamodel/protocols/ualink/transaction/protocols/*.ksy`
  - Relationship mapping from Task 1

  **Acceptance Criteria**:
  - [ ] All Transaction files with relationships have x-related-headers
  - [ ] YAML validation passes

  **Commit**: NO (groups with Task 7)

---

- [ ] 4. Update Datalink Layer Files (12 files)

  **What to do**:
  - Add `x-related-headers` to Datalink layer files based on mapping
  - Files: dl_flit.ksy, flit_header.ksy, segment_header.ksy, crc.ksy, messages/basic_messages.ksy, messages/control_messages.ksy, messages/uart_messages.ksy, messages/vendor_defined.ksy, protocols/link_state.ksy, protocols/link_resiliency.ksy, protocols/link_level_replay.ksy, protocols/link_folding.ksy

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: `[]`

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 2, 3, 5, 6)
  - **Blocks**: Task 7
  - **Blocked By**: Task 1

  **References**:
  - `earlysim/datamodel/protocols/ualink/datalink/*.ksy`
  - `earlysim/datamodel/protocols/ualink/datalink/messages/*.ksy`
  - `earlysim/datamodel/protocols/ualink/datalink/protocols/*.ksy`
  - Relationship mapping from Task 1

  **Acceptance Criteria**:
  - [ ] All Datalink files with relationships have x-related-headers
  - [ ] YAML validation passes

  **Commit**: NO (groups with Task 7)

---

- [ ] 5. Update Physical Layer Files (4 files)

  **What to do**:
  - Add `x-related-headers` to Physical layer files based on mapping
  - Files: reconciliation_sublayer.ksy, control_ordered_sets.ksy, alignment_markers.ksy, protocols/link_training.ksy

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: `[]`

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 2, 3, 4, 6)
  - **Blocks**: Task 7
  - **Blocked By**: Task 1

  **References**:
  - `earlysim/datamodel/protocols/ualink/physical/*.ksy`
  - `earlysim/datamodel/protocols/ualink/physical/protocols/*.ksy`
  - Relationship mapping from Task 1

  **Acceptance Criteria**:
  - [ ] All Physical files with relationships have x-related-headers
  - [ ] YAML validation passes

  **Commit**: NO (groups with Task 7)

---

- [ ] 6. Update Security Layer Files (5 files)

  **What to do**:
  - Add `x-related-headers` to Security layer files based on mapping
  - Files: encryption.ksy, authentication.ksy, iv_format.ksy, protocols/key_derivation.ksy, protocols/key_rotation.ksy

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: `[]`

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 2, 3, 4, 5)
  - **Blocks**: Task 7
  - **Blocked By**: Task 1

  **References**:
  - `earlysim/datamodel/protocols/ualink/security/*.ksy`
  - `earlysim/datamodel/protocols/ualink/security/protocols/*.ksy`
  - Relationship mapping from Task 1

  **Acceptance Criteria**:
  - [ ] All Security files with relationships have x-related-headers
  - [ ] YAML validation passes

  **Commit**: NO (groups with Task 7)

---

- [ ] 7. Validate and Commit Changes

  **What to do**:
  - Run YAML validation on all modified files
  - Verify all referenced files exist
  - Update tracking files
  - Create commit

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: `["git-master"]`

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Wave 3 (final)
  - **Blocks**: None
  - **Blocked By**: Tasks 2, 3, 4, 5, 6

  **Tracking Files to Update**:
  - `/home/matkins/CN7000/analysis/ualink/ualink_issues.md` - Mark UAL-007 as CLOSED
  - `/home/matkins/CN7000/analysis/packet_taxonomy/packet_taxonomy.md` - Mark W-14-007 as Closed

  **Acceptance Criteria**:
  - [ ] All modified files pass YAML validation
  - [ ] All referenced files exist
  - [ ] Tracking files updated
  - [ ] Commit created

  **Commit**: YES
  - Message: `feat(ualink): add x-related-headers cross-references to KSY files`
  - Files: All modified .ksy files

---

## Success Criteria

### Verification Commands
```bash
# Count files with x-related-headers
grep -l "x-related-headers:" earlysim/datamodel/protocols/ualink/**/*.ksy | wc -l

# Verify all modified files are valid YAML
for f in earlysim/datamodel/protocols/ualink/**/*.ksy; do
  python3 -c "import yaml; yaml.safe_load(open('$f'))" || echo "INVALID: $f"
done
```

### Final Checklist
- [ ] Relationship mapping created
- [ ] All layers updated (UPLI, Transaction, Datalink, Physical, Security)
- [ ] All modified files pass YAML validation
- [ ] All referenced files exist
- [ ] Tracking files updated
- [ ] Commit created
