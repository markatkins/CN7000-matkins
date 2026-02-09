# W-14-011: Document YAML Reference File Coverage Criteria

## TL;DR

> **Quick Summary**: Document the criteria for which KSY files get YAML reference files, rather than creating YAML files for all 38 KSY files. Currently 6/38 files have YAML references.
> 
> **Deliverables**:
> - Updated `reference/field_definitions/README.md` documenting coverage criteria
> - Clear guidelines for when to create YAML reference files
> 
> **Estimated Effort**: Quick (30 minutes)
> **Parallel Execution**: NO - single documentation task
> **Critical Path**: Task 1 → Task 2

---

## Context

### Original Request
W-14-011 from UALink datamodel review: Only 6 YAML reference files exist for 38 KSY files. Coverage is incomplete. The recommendation was to document criteria rather than create all 38 YAML files.

### Current Coverage (6 files)
| YAML File | KSY File | Rationale |
|-----------|----------|-----------|
| `dl_flit.yaml` | `datalink/dl_flit.ksy` | Core DL structure |
| `tl_flit.yaml` | `transaction/tl_flit.ksy` | Core TL structure |
| `flow_control_field.yaml` | `transaction/flow_control_field.ksy` | Key field type |
| `link_state.yaml` | `datalink/protocols/link_state.ksy` | Protocol state machine |
| `upli_request_channel.yaml` | `upli/request_channel.ksy` | UPLI interface |
| `response_field.yaml` | `transaction/response_field.ksy` | Key field type (added W-14-009) |

### Missing (32 files without YAML)
- All security layer files (5)
- All physical layer files (4)
- Most datalink files (10)
- Most transaction files (6)
- Most UPLI files (7)

### Decision
Option 2 from UAL-011: Document criteria for which packets get YAML reference files rather than creating all 38.

---

## Work Objectives

### Core Objective
Create documentation explaining the criteria for YAML reference file coverage, making it clear which KSY files warrant YAML summaries and why.

### Concrete Deliverables
- `earlysim/datamodel/protocols/ualink/reference/field_definitions/README.md`

### Definition of Done
- [ ] README.md created with coverage criteria
- [ ] Existing files documented with rationale
- [ ] Guidelines for adding new YAML files
- [ ] Tracking files updated

### Must Have
- Clear criteria for when to create YAML reference files
- Rationale for existing coverage
- Guidelines for contributors

### Must NOT Have (Guardrails)
- **MUST NOT** create YAML files for all 38 KSY files
- **MUST NOT** remove existing YAML files
- **MUST NOT** change existing YAML file content

---

## Verification Strategy (MANDATORY)

### Test Decision
- **Infrastructure exists**: NO (this is documentation)
- **User wants tests**: None (documentation only)
- **Framework**: None

### Automated Verification

```bash
# Verify README exists
test -f earlysim/datamodel/protocols/ualink/reference/field_definitions/README.md && echo "EXISTS"

# Verify content
grep -c "criteria\|Criteria" earlysim/datamodel/protocols/ualink/reference/field_definitions/README.md
```

---

## Execution Strategy

### Parallel Execution Waves

```
Wave 1 (Start Immediately):
└── Task 1: Create README.md with coverage criteria

Wave 2 (After Wave 1):
└── Task 2: Update tracking files and commit

Critical Path: Task 1 → Task 2
```

---

## TODOs

- [ ] 1. Create README.md with Coverage Criteria

  **What to do**:
  - Create `reference/field_definitions/README.md`
  - Document the purpose of YAML reference files
  - Define criteria for when to create YAML files
  - List existing files with rationale
  - Provide guidelines for contributors

  **Content Structure**:
  ```markdown
  # UALink YAML Reference Files

  ## Purpose

  YAML reference files provide human-readable summaries of key packet formats
  for quick reference. They complement the authoritative `.ksy` files but are
  NOT required for all packet types.

  ## Coverage Criteria

  YAML reference files are created for KSY files that meet ONE OR MORE of:

  1. **Core Layer Structures**: Top-level flit formats (TL Flit, DL Flit)
  2. **Key Field Types**: Fields that appear in multiple contexts (request, response, flow control)
  3. **Complex State Machines**: Protocol state machines with multiple states/transitions
  4. **High-Reference Interfaces**: Interfaces frequently referenced by implementers

  ## When NOT to Create YAML Files

  - Simple wrapper types (e.g., half-flit containers)
  - Internal protocol details rarely referenced directly
  - Types fully documented in parent structures
  - Security layer (sensitive, refer to spec directly)

  ## Current Coverage

  | File | KSY Source | Criteria Met |
  |------|------------|--------------|
  | dl_flit.yaml | datalink/dl_flit.ksy | Core Layer Structure |
  | tl_flit.yaml | transaction/tl_flit.ksy | Core Layer Structure |
  | flow_control_field.yaml | transaction/flow_control_field.ksy | Key Field Type |
  | response_field.yaml | transaction/response_field.ksy | Key Field Type |
  | link_state.yaml | datalink/protocols/link_state.ksy | Complex State Machine |
  | upli_request_channel.yaml | upli/request_channel.ksy | High-Reference Interface |

  ## Adding New YAML Files

  Before creating a new YAML reference file:

  1. Verify the KSY file meets at least one coverage criterion
  2. Ensure the YAML adds value beyond the KSY documentation
  3. Include `ksy_file` cross-reference field
  4. Follow existing file format patterns

  ## Authoritative Source

  The `.ksy` files in `datamodel/protocols/ualink/` are ALWAYS authoritative.
  YAML reference files are supplementary documentation only.
  ```

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: `[]`

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Wave 1 (alone)
  - **Blocks**: Task 2
  - **Blocked By**: None

  **References**:
  - Existing YAML files in `earlysim/datamodel/protocols/ualink/reference/field_definitions/`
  - UAL-011 description in `analysis/ualink/ualink_issues.md`

  **Acceptance Criteria**:
  ```bash
  # 1. Verify file exists
  test -f earlysim/datamodel/protocols/ualink/reference/field_definitions/README.md && echo "EXISTS"
  # Assert: EXISTS

  # 2. Verify criteria section exists
  grep -c "Coverage Criteria\|coverage criteria" earlysim/datamodel/protocols/ualink/reference/field_definitions/README.md
  # Assert: >= 1

  # 3. Verify current coverage documented
  grep -c "dl_flit.yaml\|tl_flit.yaml\|flow_control_field.yaml" earlysim/datamodel/protocols/ualink/reference/field_definitions/README.md
  # Assert: >= 3

  # 4. Verify line count reasonable
  wc -l earlysim/datamodel/protocols/ualink/reference/field_definitions/README.md | awk '{print $1}'
  # Assert: >= 40
  ```

  **Commit**: NO (groups with Task 2)

---

- [ ] 2. Update Tracking Files and Commit

  **What to do**:
  - Update ualink_issues.md: Mark UAL-011 as CLOSED
  - Update packet_taxonomy.md: Mark W-14-011 as Closed
  - Create commit

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: `["git-master"]`

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Wave 2 (final)
  - **Blocks**: None
  - **Blocked By**: Task 1

  **Tracking Files to Update**:
  - `/home/matkins/CN7000/analysis/ualink/ualink_issues.md` - Mark UAL-011 as CLOSED
  - `/home/matkins/CN7000/analysis/packet_taxonomy/packet_taxonomy.md` - Mark W-14-011 as Closed

  **Acceptance Criteria**:
  ```bash
  # 1. Verify git status shows README
  git -C earlysim status --porcelain | grep "README.md" | wc -l
  # Assert: >= 1

  # 2. After commit, verify commit exists
  git -C earlysim log -1 --oneline | grep -i "yaml\|reference\|coverage"
  # Assert: Output contains commit message
  ```

  **Commit**: YES
  - Message: `docs(ualink): document YAML reference file coverage criteria`
  - Files: `datamodel/protocols/ualink/reference/field_definitions/README.md`

---

## Success Criteria

### Verification Commands
```bash
cd earlysim

# 1. README exists
test -f datamodel/protocols/ualink/reference/field_definitions/README.md && echo "EXISTS"

# 2. Has criteria section
grep -c "Criteria" datamodel/protocols/ualink/reference/field_definitions/README.md

# 3. Documents all 6 existing files
grep -c ".yaml" datamodel/protocols/ualink/reference/field_definitions/README.md  # >= 6
```

### Final Checklist
- [ ] README.md created with coverage criteria
- [ ] All 6 existing YAML files documented
- [ ] Guidelines for contributors included
- [ ] Tracking files updated
- [ ] Commit created
