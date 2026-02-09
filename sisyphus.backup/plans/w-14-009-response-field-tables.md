# W-14-009: Add Response Field Table References to response_field.ksy

## TL;DR

> **Quick Summary**: Expand response_field.ksy from sparse 52-line placeholder to full bit-level parsing (~250 lines) with Tables 5-30, 5-34, 5-35, 5-36, 5-37 from UALink200 Spec. Create companion response_field.yaml reference file.
> 
> **Deliverables**:
> - Expanded `response_field.ksy` with full bit-level Kaitai parsing for all response types
> - New `response_field.yaml` reference file following existing patterns
> 
> **Estimated Effort**: Short (1-2 hours)
> **Parallel Execution**: NO - sequential (YAML depends on KSY completion)
> **Critical Path**: Task 1 → Task 2 → Task 3

---

## Context

### Original Request
W-14-009 from UALink datamodel review: "Response field missing table refs" - response_field.ksy lacks specific table references (Tables 5-30, 5-34, 5-35) and has only placeholder types without bit-level parsing.

### Interview Summary
**Key Discussions**:
- User wants full field parsing (actual Kaitai `type: bN` entries, not just documentation)
- User wants all response types included (Tables 5-30, 5-34, 5-35, 5-36, 5-37)
- User wants YAML reference file created (none exists currently)

**Research Findings**:
- Current response_field.ksy: 52 lines, sparse placeholders with `size: N` only
- Exemplar request_field.ksy: 124 lines, detailed doc blocks, proper x-spec
- Table 5-30 (Uncompressed Response): 64 bits / 2 sectors, FTYPE=0x2
- Table 5-34 (Compressed Single-Beat Read): 32 bits / 1 sector, FTYPE=0x4
- Table 5-36 (Compressed Write/Multi-Beat Read): 32 bits / 1 sector, FTYPE=0x5
- Tables 5-35, 5-37 are usage restrictions (constraints, not fields)

### Metis Review
**Identified Gaps** (addressed):
- Size discrepancy: Spec says 64 bits (2 sectors) for uncompressed response, current ksy says 128 bits → **Resolved**: Spec is authoritative, use 64 bits (8 bytes)
- Restriction table handling: Tables 5-35, 5-37 are constraints → **Resolved**: Document in x-packet.constraints and doc-ref, not as parsed fields
- FTYPE discriminator: Whether to use switch-on pattern → **Resolved**: Use separate types (caller selects), matching request_field.ksy pattern

---

## Work Objectives

### Core Objective
Expand response_field.ksy with full bit-level Kaitai parsing for all UALink response field types per Tables 5-30, 5-34, 5-36, and document usage restrictions from Tables 5-35, 5-37.

### Concrete Deliverables
- `earlysim/datamodel/protocols/ualink/transaction/response_field.ksy` (~250 lines)
- `earlysim/datamodel/protocols/ualink/reference/field_definitions/response_field.yaml` (~60 lines)

### Definition of Done
- [ ] response_field.ksy contains bit-level parsing for all three response types
- [ ] All five tables (5-30, 5-34, 5-35, 5-36, 5-37) referenced in doc-ref
- [ ] Field names match spec exactly (FTYPE, VCHAN, TAG, POOL, etc.)
- [ ] response_field.yaml created following flow_control_field.yaml pattern
- [ ] Both files pass YAML validation

### Must Have
- Bit-level parsing using Kaitai `type: bN` syntax
- Exact field names from spec tables
- Page numbers for every field reference
- x-spec section with all table references
- x-packet.constraints for restriction tables

### Must NOT Have (Guardrails)
- **MUST NOT** add tables beyond 5-30, 5-34, 5-35, 5-36, 5-37
- **MUST NOT** modify request_field.ksy or any other .ksy files
- **MUST NOT** create runtime validation for restriction tables
- **MUST NOT** invent field names or abstractions not in spec
- **MUST NOT** create helper types or common headers not in spec
- **MUST NOT** use 128-bit size for uncompressed response (spec says 64 bits)

---

## Verification Strategy (MANDATORY)

### Test Decision
- **Infrastructure exists**: NO (this is datamodel, not code)
- **User wants tests**: Manual-only (YAML validation)
- **Framework**: None (YAML syntax validation only)

### Automated Verification (ALWAYS include)

Each TODO includes EXECUTABLE verification procedures:

**For KSY/YAML files** (using Bash):
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
└── Task 1: Expand response_field.ksy with full bit-level parsing

Wave 2 (After Wave 1):
└── Task 2: Create response_field.yaml reference file

Wave 3 (After Wave 2):
└── Task 3: Validate both files and update metadata if needed

Critical Path: Task 1 → Task 2 → Task 3
Parallel Speedup: None (sequential dependency)
```

### Dependency Matrix

| Task | Depends On | Blocks | Can Parallelize With |
|------|------------|--------|---------------------|
| 1 | None | 2, 3 | None |
| 2 | 1 | 3 | None |
| 3 | 1, 2 | None | None (final) |

### Agent Dispatch Summary

| Wave | Tasks | Recommended Agents |
|------|-------|-------------------|
| 1 | 1 | delegate_task(category="quick", load_skills=[], run_in_background=false) |
| 2 | 2 | delegate_task(category="quick", load_skills=[], run_in_background=false) |
| 3 | 3 | delegate_task(category="quick", load_skills=[], run_in_background=false) |

---

## TODOs

- [x] 1. Expand response_field.ksy with Full Bit-Level Parsing

  **What to do**:
  - Replace current sparse types with full Kaitai bit-level parsing
  - Add `uncompressed_response` type (64 bits) per Table 5-30:
    - ftype: b4 [63:60] = 0x2
    - vchan: b2 [59:58]
    - tag: b11 [57:47]
    - pool: b1 [46]
    - len: b2 [45:44]
    - offset: b2 [43:42]
    - status: b4 [41:38]
    - rd_wr: b1 [37]
    - last: b1 [36]
    - srcaccid: b10 [35:26]
    - dstaccid: b10 [25:16]
    - spare: b16 [15:0]
  - Add `compressed_response_single_beat` type (32 bits) per Table 5-34:
    - ftype: b4 [31:28] = 0x4
    - vchan: b2 [27:26]
    - tag: b11 [25:15]
    - pool: b1 [14]
    - dstaccid: b10 [13:4]
    - offset: b2 [3:2]
    - last: b1 [1]
    - spare: b1 [0]
  - Add `compressed_response_write_multibeat` type (32 bits) per Table 5-36:
    - ftype: b4 [31:28] = 0x5
    - vchan: b2 [27:26]
    - tag: b11 [25:15]
    - pool: b1 [14]
    - dstaccid: b10 [13:4]
    - len: b2 [3:2]
    - rd_wr: b1 [1]
    - spare: b1 [0]
  - Update x-spec with all table references (5-30, 5-34, 5-35, 5-36, 5-37)
  - Update doc-ref with specific page numbers
  - Add x-packet.constraints for Tables 5-35 and 5-37 restrictions
  - Follow request_field.ksy quality standard for documentation

  **Must NOT do**:
  - Do not add any tables beyond 5-30, 5-34, 5-35, 5-36, 5-37
  - Do not modify any other .ksy files
  - Do not create helper types or abstractions
  - Do not use 128-bit size (spec says 64 bits for uncompressed)

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Single file modification with clear spec-driven content
  - **Skills**: `[]`
    - No special skills needed - straightforward file editing
  - **Skills Evaluated but Omitted**:
    - `git-master`: Not needed until commit phase

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Wave 1 (alone)
  - **Blocks**: Tasks 2, 3
  - **Blocked By**: None (can start immediately)

  **References** (CRITICAL - Be Exhaustive):

  **Pattern References** (existing code to follow):
  - `earlysim/datamodel/protocols/ualink/transaction/request_field.ksy:1-124` - EXEMPLARY quality standard for documentation style, x-spec format, doc-ref entries
  - `earlysim/datamodel/protocols/ualink/transaction/flow_control_field.ksy` - Bit-level parsing pattern with `type: bN`

  **Spec References** (authoritative source):
  - `earlysim/docs/references/UALink/UALink200_Specification_v1.0_Final/UALink200_Specification_v1.0_Final.md:2838-2862` - Table 5-30 Uncompressed Response (64 bits)
  - `earlysim/docs/references/UALink/UALink200_Specification_v1.0_Final/UALink200_Specification_v1.0_Final.md:2924-2939` - Table 5-34 Compressed Single-Beat Read (32 bits)
  - `earlysim/docs/references/UALink/UALink200_Specification_v1.0_Final/UALink200_Specification_v1.0_Final.md:2943-2948` - Table 5-35 Usage Restrictions
  - `earlysim/docs/references/UALink/UALink200_Specification_v1.0_Final/UALink200_Specification_v1.0_Final.md:2953-2968` - Table 5-36 Compressed Write/Multi-Beat Read (32 bits)
  - `earlysim/docs/references/UALink/UALink200_Specification_v1.0_Final/UALink200_Specification_v1.0_Final.md:2972-2977` - Table 5-37 Usage Restrictions

  **Current File** (to be modified):
  - `earlysim/datamodel/protocols/ualink/transaction/response_field.ksy:1-52` - Current sparse placeholder

  **WHY Each Reference Matters**:
  - request_field.ksy: Shows exact documentation style, x-spec format, and quality bar to match
  - flow_control_field.ksy: Shows Kaitai bit-level parsing syntax (`type: bN`)
  - Spec lines 2838-2977: Authoritative field definitions with exact names, sizes, positions

  **Acceptance Criteria**:

  **Automated Verification:**
  ```bash
  # 1. Verify response_field.ksy is valid YAML
  python3 -c "import yaml; yaml.safe_load(open('earlysim/datamodel/protocols/ualink/transaction/response_field.ksy'))" && echo "VALID" || echo "INVALID"
  # Assert: Output is "VALID"

  # 2. Verify all five tables are referenced in doc-ref
  grep -E "Table 5-(30|34|35|36|37)" earlysim/datamodel/protocols/ualink/transaction/response_field.ksy | wc -l
  # Assert: Output >= 5

  # 3. Verify bit-level parsing exists (type: bN entries)
  grep -c "type: b" earlysim/datamodel/protocols/ualink/transaction/response_field.ksy
  # Assert: Output >= 20

  # 4. Verify spec field names are used
  grep -E "(ftype|vchan|tag|pool|srcaccid|dstaccid|status|offset|last|rd_wr|len|spare)" earlysim/datamodel/protocols/ualink/transaction/response_field.ksy | wc -l
  # Assert: Output >= 15

  # 5. Verify three response types exist
  grep -c "uncompressed_response\|compressed_response_single_beat\|compressed_response_write_multibeat" earlysim/datamodel/protocols/ualink/transaction/response_field.ksy
  # Assert: Output >= 3

  # 6. Verify file size increased significantly
  wc -l earlysim/datamodel/protocols/ualink/transaction/response_field.ksy | awk '{print $1}'
  # Assert: Output >= 200
  ```

  **Evidence to Capture:**
  - [ ] Terminal output from all verification commands
  - [ ] Line count before (52) and after (>=200)

  **Commit**: NO (groups with Task 3)

---

- [x] 2. Create response_field.yaml Reference File

  **What to do**:
  - Create new file `earlysim/datamodel/protocols/ualink/reference/field_definitions/response_field.yaml`
  - Follow flow_control_field.yaml pattern exactly
  - Include all fields from all three response types
  - Group fields by response type using YAML structure
  - Add ksy_file cross-reference

  **Must NOT do**:
  - Do not deviate from flow_control_field.yaml pattern
  - Do not add fields not in the spec
  - Do not create nested structures beyond what pattern shows

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Single file creation with clear pattern to follow
  - **Skills**: `[]`
    - No special skills needed
  - **Skills Evaluated but Omitted**:
    - None applicable

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Wave 2 (alone)
  - **Blocks**: Task 3
  - **Blocked By**: Task 1 (needs to know final field names)

  **References** (CRITICAL - Be Exhaustive):

  **Pattern References** (existing code to follow):
  - `earlysim/datamodel/protocols/ualink/reference/field_definitions/flow_control_field.yaml:1-30` - EXACT pattern to follow for structure, fields, encoding format

  **Source References** (field definitions):
  - Task 1 output: response_field.ksy (use field names from completed Task 1)

  **WHY Each Reference Matters**:
  - flow_control_field.yaml: Defines exact YAML structure, field format, required attributes

  **Acceptance Criteria**:

  **Automated Verification:**
  ```bash
  # 1. Verify file exists
  test -f earlysim/datamodel/protocols/ualink/reference/field_definitions/response_field.yaml && echo "EXISTS" || echo "MISSING"
  # Assert: Output is "EXISTS"

  # 2. Verify valid YAML
  python3 -c "import yaml; yaml.safe_load(open('earlysim/datamodel/protocols/ualink/reference/field_definitions/response_field.yaml'))" && echo "VALID" || echo "INVALID"
  # Assert: Output is "VALID"

  # 3. Verify ksy_file reference exists
  grep -c "ksy_file:" earlysim/datamodel/protocols/ualink/reference/field_definitions/response_field.yaml
  # Assert: Output >= 1

  # 4. Verify fields section exists with multiple entries
  grep -c "^  - name:" earlysim/datamodel/protocols/ualink/reference/field_definitions/response_field.yaml
  # Assert: Output >= 10

  # 5. Verify spec_ref exists
  grep -c "spec_ref:" earlysim/datamodel/protocols/ualink/reference/field_definitions/response_field.yaml
  # Assert: Output >= 1
  ```

  **Evidence to Capture:**
  - [ ] Terminal output from all verification commands
  - [ ] File content matches flow_control_field.yaml structure

  **Commit**: NO (groups with Task 3)

---

- [x] 3. Validate and Commit Changes

  **What to do**:
  - Run all acceptance criteria from Tasks 1 and 2
  - Verify no regressions in other UALink files
  - Create single commit with both files
  - Update W-14-009 status in work item tracker (if exists)

  **Must NOT do**:
  - Do not modify any files other than response_field.ksy and response_field.yaml
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
  - **Parallel Group**: Wave 3 (final)
  - **Blocks**: None
  - **Blocked By**: Tasks 1, 2

  **References** (CRITICAL - Be Exhaustive):

  **Pattern References**:
  - Previous W-14 commits for message style (e.g., `feat(ualink): add Table X-Y references to Z`)

  **Files to Commit**:
  - `earlysim/datamodel/protocols/ualink/transaction/response_field.ksy`
  - `earlysim/datamodel/protocols/ualink/reference/field_definitions/response_field.yaml`

  **Acceptance Criteria**:

  **Automated Verification:**
  ```bash
  # 1. Verify git status shows only expected files
  git -C earlysim status --porcelain | grep -E "response_field\.(ksy|yaml)" | wc -l
  # Assert: Output == 2

  # 2. Verify no other UALink files modified
  git -C earlysim status --porcelain | grep -v "response_field" | grep "ualink" | wc -l
  # Assert: Output == 0

  # 3. After commit, verify commit exists
  git -C earlysim log -1 --oneline | grep -i "response"
  # Assert: Output contains commit message
  ```

  **Evidence to Capture:**
  - [ ] git status output before commit
  - [ ] git log output after commit
  - [ ] Commit hash

  **Commit**: YES
  - Message: `feat(ualink): add Tables 5-30, 5-34, 5-35, 5-36, 5-37 to response_field.ksy`
  - Files: `datamodel/protocols/ualink/transaction/response_field.ksy`, `datamodel/protocols/ualink/reference/field_definitions/response_field.yaml`
  - Pre-commit: YAML validation (python3 -c "import yaml; ...")

---

## Commit Strategy

| After Task | Message | Files | Verification |
|------------|---------|-------|--------------|
| 3 | `feat(ualink): add Tables 5-30, 5-34, 5-35, 5-36, 5-37 to response_field.ksy` | response_field.ksy, response_field.yaml | YAML validation |

---

## Success Criteria

### Verification Commands
```bash
# All-in-one validation script
cd earlysim

# 1. KSY valid YAML
python3 -c "import yaml; yaml.safe_load(open('datamodel/protocols/ualink/transaction/response_field.ksy'))"

# 2. YAML valid YAML
python3 -c "import yaml; yaml.safe_load(open('datamodel/protocols/ualink/reference/field_definitions/response_field.yaml'))"

# 3. Tables referenced
grep -c "Table 5-3" datamodel/protocols/ualink/transaction/response_field.ksy  # Should be >= 5

# 4. Bit parsing exists
grep -c "type: b" datamodel/protocols/ualink/transaction/response_field.ksy  # Should be >= 20

# 5. YAML has fields
grep -c "^  - name:" datamodel/protocols/ualink/reference/field_definitions/response_field.yaml  # Should be >= 10
```

### Final Checklist
- [ ] All "Must Have" present (bit-level parsing, exact field names, page numbers, x-spec, constraints)
- [ ] All "Must NOT Have" absent (no extra tables, no other file modifications, no invented names)
- [ ] Both files pass YAML validation
- [ ] Commit created with proper message
