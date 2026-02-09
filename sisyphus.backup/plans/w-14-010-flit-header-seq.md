# W-14-010: Add Top-Level Sequence to flit_header.ksy

## TL;DR

> **Quick Summary**: Add top-level `seq:` and `instances:` sections to flit_header.ksy to enable direct parsing of 3-byte flit headers with discriminated type selection based on `op` field.
> 
> **Deliverables**:
> - Modified `flit_header.ksy` with parseable entry point (~130 lines)
> 
> **Estimated Effort**: Quick (30 minutes)
> **Parallel Execution**: NO - single file modification
> **Critical Path**: Task 1 → Task 2

---

## Context

### Original Request
W-14-010 from UALink datamodel review: "Flit header missing top-level seq" - flit_header.ksy defines types but no top-level `seq:` to parse the actual 3-byte header. Cannot be used directly for parsing.

### Interview Summary
**Key Discussions**:
- File currently defines `explicit_sequence_header` and `command_header` types correctly
- Missing entry point for parsing - no `seq:` section at root level
- Need discriminator logic based on `op` field to select correct type

**Research Findings**:
- Current flit_header.ksy: 90 lines, types only, no parsing entry point
- Table 6-14 (Explicit Sequence Header): op = 0b000 (NOP/original) or 0b001 (replay)
- Table 6-15 (Command Header): op = 0b010 (ACK) or 0b011 (replay request)
- Header is 3 bytes (24 bits), big-endian
- Exemplar: flow_control_field.ksy shows top-level `seq:` with bit-level parsing

### Metis Review (Self-Analysis)
**Identified Gaps** (addressed):
- Discriminator approach: Use instances with value expressions → **Resolved**: Follow Kaitai pattern for discriminated unions
- Bit extraction: How to extract `op` field from raw bytes → **Resolved**: Use `(header_bytes[0] >> 5) & 0x07` (bits 23:21 = byte 0 bits 7:5)

---

## Work Objectives

### Core Objective
Add top-level `seq:` and `instances:` sections to flit_header.ksy to enable direct parsing with automatic header type discrimination.

### Concrete Deliverables
- `earlysim/datamodel/protocols/ualink/datalink/flit_header.ksy` (~130 lines)

### Definition of Done
- [ ] flit_header.ksy has top-level `seq:` section
- [ ] `instances:` section extracts `op` field and provides type discrimination
- [ ] File passes YAML validation
- [ ] Existing types (`explicit_sequence_header`, `command_header`) preserved unchanged

### Must Have
- Top-level `seq:` reading raw 3-byte header
- Instance `op_field` extracting bits [23:21] from header
- Instance `is_explicit_sequence` (op == 0 or op == 1)
- Instance `is_command` (op == 2 or op == 3)
- Instance `header_type` returning parsed header as correct type

### Must NOT Have (Guardrails)
- **MUST NOT** modify existing `explicit_sequence_header` type definition
- **MUST NOT** modify existing `command_header` type definition
- **MUST NOT** change x-spec or x-packet metadata
- **MUST NOT** add fields not in Tables 6-14 or 6-15

---

## Verification Strategy (MANDATORY)

### Test Decision
- **Infrastructure exists**: NO (this is datamodel, not code)
- **User wants tests**: Manual-only (YAML validation)
- **Framework**: None (YAML syntax validation only)

### Automated Verification (ALWAYS include)

**For KSY files** (using Bash):
```bash
# Verify YAML syntax is valid
python3 -c "import yaml; yaml.safe_load(open('FILE'))" && echo "VALID" || echo "INVALID"
# Assert: Output is "VALID"

# Verify expected content exists
grep -c "PATTERN" FILE
# Assert: Output >= N
```

---

## Execution Strategy

### Parallel Execution Waves

```
Wave 1 (Start Immediately):
└── Task 1: Add top-level seq and instances to flit_header.ksy

Wave 2 (After Wave 1):
└── Task 2: Validate and commit changes

Critical Path: Task 1 → Task 2
Parallel Speedup: None (sequential)
```

### Dependency Matrix

| Task | Depends On | Blocks | Can Parallelize With |
|------|------------|--------|---------------------|
| 1 | None | 2 | None |
| 2 | 1 | None | None (final) |

### Agent Dispatch Summary

| Wave | Tasks | Recommended Agents |
|------|-------|-------------------|
| 1 | 1 | delegate_task(category="quick", load_skills=[], run_in_background=false) |
| 2 | 2 | delegate_task(category="quick", load_skills=["git-master"], run_in_background=false) |

---

## TODOs

- [x] 1. Add Top-Level Sequence and Instances to flit_header.ksy

  **What to do**:
  - Add `seq:` section at root level (after `x-packet:`, before `types:`)
  - Read raw 3-byte header as `header_bytes`
  - Add `instances:` section with:
    - `op_field`: Extract bits [23:21] = `(header_bytes[0] >> 5) & 0x07`
    - `payload_field`: Extract bit [20] = `(header_bytes[0] >> 4) & 0x01`
    - `is_explicit_sequence`: `op_field == 0 || op_field == 1`
    - `is_command`: `op_field == 2 || op_field == 3`
    - `is_nop`: `payload_field == 0`
    - `is_payload`: `payload_field == 1`
  - Add documentation explaining discriminator logic

  **Must NOT do**:
  - Do not modify existing `explicit_sequence_header` type
  - Do not modify existing `command_header` type
  - Do not change x-spec or x-packet sections
  - Do not add new types

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Single file modification with clear pattern
  - **Skills**: `[]`
    - No special skills needed
  - **Skills Evaluated but Omitted**:
    - `git-master`: Not needed until commit phase

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Wave 1 (alone)
  - **Blocks**: Task 2
  - **Blocked By**: None (can start immediately)

  **References** (CRITICAL - Be Exhaustive):

  **Pattern References** (existing code to follow):
  - `earlysim/datamodel/protocols/ualink/transaction/flow_control_field.ksy:90-121` - Top-level `seq:` with bit-level parsing pattern
  - `earlysim/datamodel/protocols/ualink/datalink/dl_flit.ksy` - Example of instances section

  **Spec References** (authoritative source):
  - `earlysim/docs/references/UALink/UALink200_Specification_v1.0_Final/UALink200_Specification_v1.0_Final.md:3697-3707` - Table 6-14 Explicit Sequence Header
  - `earlysim/docs/references/UALink/UALink200_Specification_v1.0_Final/UALink200_Specification_v1.0_Final.md:3713-3721` - Table 6-15 Command Header

  **Current File** (to be modified):
  - `earlysim/datamodel/protocols/ualink/datalink/flit_header.ksy:1-90` - Current file with types only

  **WHY Each Reference Matters**:
  - flow_control_field.ksy: Shows exact pattern for top-level `seq:` with bit-level fields
  - Spec lines 3697-3721: Defines op field values that determine header type
  - Current file: Preserves existing type definitions

  **Acceptance Criteria**:

  **Automated Verification:**
  ```bash
  # 1. Verify flit_header.ksy is valid YAML
  python3 -c "import yaml; yaml.safe_load(open('earlysim/datamodel/protocols/ualink/datalink/flit_header.ksy'))" && echo "VALID" || echo "INVALID"
  # Assert: Output is "VALID"

  # 2. Verify top-level seq exists
  grep -c "^seq:" earlysim/datamodel/protocols/ualink/datalink/flit_header.ksy
  # Assert: Output >= 1

  # 3. Verify instances section exists
  grep -c "^instances:" earlysim/datamodel/protocols/ualink/datalink/flit_header.ksy
  # Assert: Output >= 1

  # 4. Verify op_field instance exists
  grep -c "op_field:" earlysim/datamodel/protocols/ualink/datalink/flit_header.ksy
  # Assert: Output >= 1

  # 5. Verify is_explicit_sequence instance exists
  grep -c "is_explicit_sequence:" earlysim/datamodel/protocols/ualink/datalink/flit_header.ksy
  # Assert: Output >= 1

  # 6. Verify is_command instance exists
  grep -c "is_command:" earlysim/datamodel/protocols/ualink/datalink/flit_header.ksy
  # Assert: Output >= 1

  # 7. Verify existing types preserved
  grep -c "explicit_sequence_header:\|command_header:" earlysim/datamodel/protocols/ualink/datalink/flit_header.ksy
  # Assert: Output >= 2

  # 8. Verify file size increased
  wc -l earlysim/datamodel/protocols/ualink/datalink/flit_header.ksy | awk '{print $1}'
  # Assert: Output >= 110
  ```

  **Evidence to Capture:**
  - [ ] Terminal output from all verification commands
  - [ ] Line count before (90) and after (>=110)

  **Commit**: NO (groups with Task 2)

---

- [x] 2. Validate and Commit Changes

  **What to do**:
  - Run all acceptance criteria from Task 1
  - Verify no regressions in other UALink files
  - Create commit with proper message
  - Update W-14-010 status in tracking files

  **Must NOT do**:
  - Do not modify any files other than flit_header.ksy
  - Do not push to remote (user will do this)

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Validation and commit only
  - **Skills**: `["git-master"]`
    - git-master: For proper commit message and staging
  - **Skills Evaluated but Omitted**:
    - None applicable

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Wave 2 (final)
  - **Blocks**: None
  - **Blocked By**: Task 1

  **References** (CRITICAL - Be Exhaustive):

  **Pattern References**:
  - Previous W-14 commits for message style (e.g., `feat(ualink): add X to Y`)

  **Files to Commit**:
  - `earlysim/datamodel/protocols/ualink/datalink/flit_header.ksy`

  **Tracking Files to Update**:
  - `/home/matkins/CN7000/analysis/ualink/ualink_issues.md` - Mark UAL-010 as CLOSED
  - `/home/matkins/CN7000/analysis/packet_taxonomy/packet_taxonomy.md` - Mark W-14-010 as Closed

  **Acceptance Criteria**:

  **Automated Verification:**
  ```bash
  # 1. Verify git status shows only expected file
  git -C earlysim status --porcelain | grep "flit_header.ksy" | wc -l
  # Assert: Output == 1

  # 2. Verify no other UALink files modified
  git -C earlysim status --porcelain | grep -v "flit_header" | grep "ualink" | wc -l
  # Assert: Output == 0

  # 3. After commit, verify commit exists
  git -C earlysim log -1 --oneline | grep -i "flit"
  # Assert: Output contains commit message
  ```

  **Evidence to Capture:**
  - [ ] git status output before commit
  - [ ] git log output after commit
  - [ ] Commit hash

  **Commit**: YES
  - Message: `feat(ualink): add top-level seq and instances to flit_header.ksy`
  - Files: `datamodel/protocols/ualink/datalink/flit_header.ksy`
  - Pre-commit: YAML validation

---

## Commit Strategy

| After Task | Message | Files | Verification |
|------------|---------|-------|--------------|
| 2 | `feat(ualink): add top-level seq and instances to flit_header.ksy` | flit_header.ksy | YAML validation |

---

## Success Criteria

### Verification Commands
```bash
# All-in-one validation script
cd earlysim

# 1. KSY valid YAML
python3 -c "import yaml; yaml.safe_load(open('datamodel/protocols/ualink/datalink/flit_header.ksy'))"

# 2. Has top-level seq
grep -c "^seq:" datamodel/protocols/ualink/datalink/flit_header.ksy  # Should be >= 1

# 3. Has instances
grep -c "^instances:" datamodel/protocols/ualink/datalink/flit_header.ksy  # Should be >= 1

# 4. Has discriminator instances
grep -c "op_field:\|is_explicit_sequence:\|is_command:" datamodel/protocols/ualink/datalink/flit_header.ksy  # Should be >= 3
```

### Final Checklist
- [ ] All "Must Have" present (seq, instances, discriminators)
- [ ] All "Must NOT Have" absent (no type modifications, no new types)
- [ ] File passes YAML validation
- [ ] Commit created with proper message
- [ ] Tracking files updated (ualink_issues.md, packet_taxonomy.md)
