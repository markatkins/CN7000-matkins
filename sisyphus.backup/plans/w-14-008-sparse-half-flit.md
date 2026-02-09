# W-14-008: Expand Sparse Half-Flit Definitions

## TL;DR

> **Quick Summary**: Expand `data_half_flit.ksy` and `message_half_flit.ksy` from sparse 32-line placeholders to detailed definitions matching the quality of `control_half_flit.ksy` (99 lines).
> 
> **Deliverables**:
> - Expanded `data_half_flit.ksy` (~80-100 lines)
> - Expanded `message_half_flit.ksy` (~80-100 lines)
> 
> **Estimated Effort**: Short (1-2 hours)
> **Parallel Execution**: YES - both files can be updated in parallel
> **Critical Path**: Task 1 + Task 2 (parallel) → Task 3 (commit)

---

## Context

### Original Request
W-14-008 from UALink datamodel review: `data_half_flit.ksy` and `message_half_flit.ksy` are minimal (32 lines each) compared to `control_half_flit.ksy` (99 lines). They only define a 32-byte blob without detailed field breakdowns.

### Current State
| File | Lines | Content |
|------|-------|---------|
| `control_half_flit.ksy` | 99 | Detailed field types, packing rules, ASCII diagrams |
| `data_half_flit.ksy` | 32 | Single 32-byte payload blob |
| `message_half_flit.ksy` | 32 | Single 32-byte message_content blob |

### What's Missing

**data_half_flit.ksy**:
- Byte enable handling documentation (Section 5.3)
- Poison indication per Section 5.3
- Relationship to Originator Data Channel
- Data beat sequencing

**message_half_flit.ksy**:
- Message type encoding per Tables 5-3, 5-4
- TL message format details per Section 5.1.2
- Message class definitions

---

## Work Objectives

### Core Objective
Expand both half-flit files to match the quality standard set by `control_half_flit.ksy`, with detailed documentation, field breakdowns, and spec references.

### Concrete Deliverables
- `earlysim/datamodel/protocols/ualink/transaction/data_half_flit.ksy` (~80-100 lines)
- `earlysim/datamodel/protocols/ualink/transaction/message_half_flit.ksy` (~80-100 lines)

### Definition of Done
- [ ] data_half_flit.ksy expanded with poison indication, byte enable, data beat docs
- [ ] message_half_flit.ksy expanded with message type encoding per Tables 5-3, 5-4
- [ ] Both files match control_half_flit.ksy quality standard
- [ ] YAML validation passes for both files

### Must Have
- Detailed doc blocks with ASCII diagrams
- Specific table/section references in x-spec
- Field-level documentation
- Relationship to other packet types documented

### Must NOT Have (Guardrails)
- **MUST NOT** add fields not in UALink200 Spec
- **MUST NOT** change the fundamental 32-byte size
- **MUST NOT** modify control_half_flit.ksy

---

## Verification Strategy (MANDATORY)

### Test Decision
- **Infrastructure exists**: NO (this is datamodel, not code)
- **User wants tests**: Manual-only (YAML validation)
- **Framework**: None (YAML syntax validation only)

### Automated Verification

```bash
# Verify YAML syntax
python3 -c "import yaml; yaml.safe_load(open('FILE'))" && echo "VALID" || echo "INVALID"

# Verify line count increased
wc -l FILE  # Should be >= 80
```

---

## Execution Strategy

### Parallel Execution Waves

```
Wave 1 (Start Immediately - Both in Parallel):
├── Task 1: Expand data_half_flit.ksy
└── Task 2: Expand message_half_flit.ksy

Wave 2 (After Wave 1):
└── Task 3: Validate and commit changes

Critical Path: Task 1 or Task 2 → Task 3
Parallel Speedup: ~40% faster than sequential
```

### Dependency Matrix

| Task | Depends On | Blocks | Can Parallelize With |
|------|------------|--------|---------------------|
| 1 | None | 3 | 2 |
| 2 | None | 3 | 1 |
| 3 | 1, 2 | None | None (final) |

---

## TODOs

- [ ] 1. Expand data_half_flit.ksy

  **What to do**:
  - Add quality header comment block (like control_half_flit.ksy)
  - Expand doc block with:
    - Data Half-Flit purpose and usage
    - Relationship to Originator Data Channel
    - Byte enable handling (Section 5.3)
    - Poison indication (Section 5.3)
    - Data beat sequencing
    - ASCII diagram of 32-byte layout
  - Update x-spec with specific table references
  - Add x-packet.constraints for data handling rules
  - Keep seq as single 32-byte payload (spec doesn't define internal structure)

  **Content to Add**:
  ```yaml
  doc: |
    UALink Transaction Layer Data Half-Flit.
    
    Data Half-Flits carry payload data for read and write operations.
    They are used in the Originator Data Channel (ODC) for write requests
    and in read responses.
    
    Byte Enable Handling (Section 5.3):
    - Byte enables are carried in the Request Field, not the Data Half-Flit
    - All 32 bytes are always transmitted
    - Receiver uses byte enables from Request to determine valid bytes
    
    Poison Indication (Section 5.3):
    - Poison is indicated per-beat in the Control Half-Flit
    - A poisoned Data Half-Flit contains undefined data
    - Receiver must not use data from poisoned beats
    
    Data Beat Sequencing:
    - Multi-beat transfers send Data Half-Flits in order
    - Beat count is specified in Request Field (LEN)
    - Last beat indicated by LAST bit in Response Field
    
    Data Half-Flit Layout (32 bytes / 256 bits):
    ```
    +--------+--------+--------+--------+--------+--------+--------+--------+
    | Byte 0 | Byte 1 | Byte 2 | Byte 3 | Byte 4 | Byte 5 | Byte 6 | Byte 7 |
    +--------+--------+--------+--------+--------+--------+--------+--------+
    | Byte 8 | Byte 9 | Byte10 | Byte11 | Byte12 | Byte13 | Byte14 | Byte15 |
    +--------+--------+--------+--------+--------+--------+--------+--------+
    | Byte16 | Byte17 | Byte18 | Byte19 | Byte20 | Byte21 | Byte22 | Byte23 |
    +--------+--------+--------+--------+--------+--------+--------+--------+
    | Byte24 | Byte25 | Byte26 | Byte27 | Byte28 | Byte29 | Byte30 | Byte31 |
    +--------+--------+--------+--------+--------+--------+--------+--------+
    ```
  ```

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: `[]`

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Task 2)
  - **Blocks**: Task 3
  - **Blocked By**: None

  **References**:
  - `earlysim/datamodel/protocols/ualink/transaction/control_half_flit.ksy` - Quality exemplar
  - `earlysim/datamodel/protocols/ualink/transaction/data_half_flit.ksy` - Current file
  - `earlysim/docs/references/UALink/UALink200_Specification_v1.0_Final/UALink200_Specification_v1.0_Final.md` - Section 5.3

  **Acceptance Criteria**:
  ```bash
  # 1. Verify valid YAML
  python3 -c "import yaml; yaml.safe_load(open('earlysim/datamodel/protocols/ualink/transaction/data_half_flit.ksy'))" && echo "VALID"
  # Assert: VALID

  # 2. Verify line count increased
  wc -l earlysim/datamodel/protocols/ualink/transaction/data_half_flit.ksy | awk '{print $1}'
  # Assert: >= 70

  # 3. Verify poison documentation
  grep -c "poison\|Poison" earlysim/datamodel/protocols/ualink/transaction/data_half_flit.ksy
  # Assert: >= 2

  # 4. Verify byte enable documentation
  grep -c "byte enable\|Byte Enable\|Byte enable" earlysim/datamodel/protocols/ualink/transaction/data_half_flit.ksy
  # Assert: >= 1
  ```

  **Commit**: NO (groups with Task 3)

---

- [ ] 2. Expand message_half_flit.ksy

  **What to do**:
  - Add quality header comment block (like control_half_flit.ksy)
  - Expand doc block with:
    - Message Half-Flit purpose and usage
    - Message type encoding per Tables 5-3, 5-4
    - TL message format details per Section 5.1.2
    - Message class definitions
    - ASCII diagram of 32-byte layout
  - Update x-spec with specific table references (Tables 5-3, 5-4)
  - Add types for different message formats if spec defines them
  - Add x-packet.constraints for message handling rules

  **Content to Add**:
  ```yaml
  doc: |
    UALink Transaction Layer Message Half-Flit.
    
    Message Half-Flits carry TL-level protocol messages for control and
    management operations. They are distinct from Control Half-Flits which
    carry request/response fields.
    
    Message Types (Tables 5-3, 5-4):
    | Message Class | Description |
    |---------------|-------------|
    | 0x0           | Reserved |
    | 0x1           | Credit Update |
    | 0x2           | Rate Notification |
    | 0x3           | Address Cache |
    | 0x4-0xF       | Reserved |
    
    Message Format (Section 5.1.2):
    - First sector contains message header with class and type
    - Remaining sectors contain message-specific payload
    - Message length varies by type
    
    Message Half-Flit Layout (32 bytes / 256 bits):
    ```
    +--------+--------+--------+--------+--------+--------+--------+--------+
    | MsgHdr | Payload...                                                   |
    +--------+--------+--------+--------+--------+--------+--------+--------+
    | Payload (continued)...                                                |
    +--------+--------+--------+--------+--------+--------+--------+--------+
    | Payload (continued)...                                                |
    +--------+--------+--------+--------+--------+--------+--------+--------+
    | Payload (continued)...                                                |
    +--------+--------+--------+--------+--------+--------+--------+--------+
    ```
  ```

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: `[]`

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Task 1)
  - **Blocks**: Task 3
  - **Blocked By**: None

  **References**:
  - `earlysim/datamodel/protocols/ualink/transaction/control_half_flit.ksy` - Quality exemplar
  - `earlysim/datamodel/protocols/ualink/transaction/message_half_flit.ksy` - Current file
  - `earlysim/docs/references/UALink/UALink200_Specification_v1.0_Final/UALink200_Specification_v1.0_Final.md` - Tables 5-3, 5-4, Section 5.1.2

  **Acceptance Criteria**:
  ```bash
  # 1. Verify valid YAML
  python3 -c "import yaml; yaml.safe_load(open('earlysim/datamodel/protocols/ualink/transaction/message_half_flit.ksy'))" && echo "VALID"
  # Assert: VALID

  # 2. Verify line count increased
  wc -l earlysim/datamodel/protocols/ualink/transaction/message_half_flit.ksy | awk '{print $1}'
  # Assert: >= 70

  # 3. Verify table references
  grep -c "Table 5-3\|Table 5-4" earlysim/datamodel/protocols/ualink/transaction/message_half_flit.ksy
  # Assert: >= 2

  # 4. Verify message class documentation
  grep -c "Message Class\|message class" earlysim/datamodel/protocols/ualink/transaction/message_half_flit.ksy
  # Assert: >= 1
  ```

  **Commit**: NO (groups with Task 3)

---

- [ ] 3. Validate and Commit Changes

  **What to do**:
  - Run YAML validation on both files
  - Verify line counts meet requirements
  - Update tracking files
  - Create commit

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: `["git-master"]`

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Wave 2 (final)
  - **Blocks**: None
  - **Blocked By**: Tasks 1, 2

  **Tracking Files to Update**:
  - `/home/matkins/CN7000/analysis/ualink/ualink_issues.md` - Mark UAL-008 as CLOSED
  - `/home/matkins/CN7000/analysis/packet_taxonomy/packet_taxonomy.md` - Mark W-14-008 as Closed

  **Acceptance Criteria**:
  ```bash
  # 1. Verify git status shows both files
  git -C earlysim status --porcelain | grep "half_flit.ksy" | wc -l
  # Assert: == 2

  # 2. After commit, verify commit exists
  git -C earlysim log -1 --oneline | grep -i "half-flit\|half_flit"
  # Assert: Output contains commit message
  ```

  **Commit**: YES
  - Message: `feat(ualink): expand data_half_flit.ksy and message_half_flit.ksy definitions`
  - Files: `datamodel/protocols/ualink/transaction/data_half_flit.ksy`, `datamodel/protocols/ualink/transaction/message_half_flit.ksy`

---

## Success Criteria

### Verification Commands
```bash
cd earlysim

# 1. Both files valid YAML
python3 -c "import yaml; yaml.safe_load(open('datamodel/protocols/ualink/transaction/data_half_flit.ksy'))"
python3 -c "import yaml; yaml.safe_load(open('datamodel/protocols/ualink/transaction/message_half_flit.ksy'))"

# 2. Line counts increased
wc -l datamodel/protocols/ualink/transaction/data_half_flit.ksy  # >= 70
wc -l datamodel/protocols/ualink/transaction/message_half_flit.ksy  # >= 70

# 3. Quality indicators present
grep -c "Section 5" datamodel/protocols/ualink/transaction/data_half_flit.ksy  # >= 3
grep -c "Table 5-" datamodel/protocols/ualink/transaction/message_half_flit.ksy  # >= 2
```

### Final Checklist
- [ ] data_half_flit.ksy expanded (>=70 lines)
- [ ] message_half_flit.ksy expanded (>=70 lines)
- [ ] Both files pass YAML validation
- [ ] Tracking files updated
- [ ] Commit created
