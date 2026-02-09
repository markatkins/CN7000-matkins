# UE Tagged-Send and IPv4 Variants Documentation

## TL;DR

> **Quick Summary**: Create comprehensive documentation for UE tagged-send packet variants and IPv4 encapsulations, including wire format diagrams and a comparison table to CN7000 Packet Taxonomy.ppt nomenclature.
> 
> **Deliverables**:
> - `analysis/packet_taxonomy/packet_taxonomy_ue_tagged_send_variants.md` - Full documentation with wire diagrams
> - Work item for CN7000 Packet Taxonomy.ppt comparison (tracked separately)
> 
> **Estimated Effort**: Medium (2-3 hours)
> **Parallel Execution**: NO - sequential (Task 2 depends on Task 1)
> **Critical Path**: Task 1 → Task 2 → Task 3

---

## Context

### Original Request
User requested:
1. Create formal document in `analysis/packet_taxonomy/` with wire format diagrams for each UE packet variant
2. Generate ASCII wire diagrams showing complete packet layouts
3. Create comparison table mapping UE+ packet types to CN7000 Packet Taxonomy.ppt nomenclature
4. Create work item for item 3 for future tracking

### Research Findings

**UE Datamodel Structure**:
- 100 KSY files in `datamodel/protocols/ue/`
- Key directories: `transport/ses/`, `transport/pds/`, `transport/cms/`, `transport/tss/`
- Existing taxonomy docs: `packet_taxonomy_ue_ses.md`, `packet_taxonomy_ue_pds.md`, `packet_taxonomy_ue_cms_tss.md`

**Packet Variants Identified**:
| Variant | Header Size | Key Components |
|---------|-------------|----------------|
| UE Standard Tagged Send | 100B | Eth+IPv4+UDP+PDS+SES |
| UE + CSIG Compact | 108B | + CC State (8B) |
| UE + CSIG Wide | 116B | + CC State Wide (16B) |
| UE IPv4 Native | 96B | Eth+IPv4+Entropy+PDS+SES |
| UE IPv4 + CSIG Compact | 104B | + CC State (8B) |
| UE IPv4 + CSIG Wide | 112B | + CC State Wide (16B) |
| UE + Encrypted | 116B+16B | + TSS Header + Auth Tag |
| UE Small Message | 88B | Smaller SES header (32B) |
| UE Rendezvous | 132B | + Rendezvous Extension (32B) |
| UE Deferrable | 100B | Special buffer_offset usage |

---

## Work Objectives

### Core Objective
Create comprehensive documentation for all UE tagged-send packet variants with wire format diagrams.

### Concrete Deliverables
1. `analysis/packet_taxonomy/packet_taxonomy_ue_tagged_send_variants.md` - Complete documentation
2. Work item file for CN7000 comparison table tracking

### Definition of Done
- [x] Document includes all 10+ packet variants
- [x] Each variant has ASCII wire format diagram
- [x] Header size summary table is complete
- [x] Cross-references to existing UE taxonomy docs
- [x] Work item created for comparison table

### Must Have
- Protocol stack overview diagram
- Packet type matrix (delivery modes, SES formats, opcodes)
- Wire format diagrams for each variant
- Field definitions tables
- Header size summary table
- Datamodel file mapping

### Must NOT Have (Guardrails)
- Do NOT duplicate content from existing packet_taxonomy_ue_*.md files
- Do NOT modify datamodel files
- Do NOT include response packet formats (already in packet_taxonomy_ue_ses.md)

---

## Verification Strategy (MANDATORY)

### Test Decision
- **Infrastructure exists**: N/A (documentation only)
- **User wants tests**: Manual-only
- **Framework**: grep verification

### Automated Verification

```bash
# Verify document exists and has key sections
grep -c "Tagged-Send\|IPv4 Variants" analysis/packet_taxonomy/packet_taxonomy_ue_tagged_send_variants.md
# Assert: >= 2

# Verify wire diagrams present
grep -c "┌──────────\|├──────────\|└──────────" analysis/packet_taxonomy/packet_taxonomy_ue_tagged_send_variants.md
# Assert: >= 10 (multiple diagrams)

# Verify header size table
grep -c "UE Standard\|UE + CSIG\|UE IPv4\|UE Small\|UE Rendezvous" analysis/packet_taxonomy/packet_taxonomy_ue_tagged_send_variants.md
# Assert: >= 5

# Verify cross-references
grep -c "packet_taxonomy_ue_ses.md\|packet_taxonomy_ue_pds.md" analysis/packet_taxonomy/packet_taxonomy_ue_tagged_send_variants.md
# Assert: >= 2

# Verify work item exists
ls -la analysis/packet_taxonomy/WORK_ITEMS.md || ls -la .sisyphus/work-items/
# Assert: file exists
```

---

## Execution Strategy

### Sequential Execution

```
Task 1: Create main documentation file
    ↓
Task 2: Add wire format diagrams (integrated in Task 1)
    ↓
Task 3: Create work item for comparison table
```

### Dependency Matrix

| Task | Depends On | Blocks | Can Parallelize With |
|------|------------|--------|---------------------|
| 1 | None | 2, 3 | None |
| 2 | 1 | 3 | None |
| 3 | 1, 2 | None | None |

---

## TODOs

- [x] 1. Create packet_taxonomy_ue_tagged_send_variants.md

  **What to do**:
  - Create new file `analysis/packet_taxonomy/packet_taxonomy_ue_tagged_send_variants.md`
  - Include all sections from the draft content:
    1. Overview
    2. Protocol Stack diagram
    3. Packet Type Matrix (delivery modes, SES formats, opcodes)
    4. Tagged-Send Packet Variants (10 variants with descriptions)
    5. Wire Format Diagrams (ASCII art for each variant)
    6. Header Size Summary table
    7. Cross-References
    8. References

  **Must NOT do**:
  - Do NOT duplicate content from existing packet_taxonomy_ue_*.md files
  - Do NOT modify datamodel files

  **Recommended Agent Profile**:
  - **Category**: `writing`
    - Reason: Documentation creation with technical content
  - **Skills**: `[]`
    - No special skills needed

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Sequential
  - **Blocks**: Task 2, Task 3
  - **Blocked By**: None

  **References** (CRITICAL - Be Exhaustive):

  **Pattern References** (existing documentation to follow):
  - `analysis/packet_taxonomy/packet_taxonomy_ue_ses.md:1-200` - SES format documentation pattern
  - `analysis/packet_taxonomy/packet_taxonomy_ue_pds.md:1-150` - PDS format documentation pattern
  - `analysis/packet_taxonomy/packet_taxonomy_ethernet.md:39-103` - Wire format diagram style

  **Source Files** (datamodel to document):
  - `earlysim/datamodel/protocols/ue/transport/ses/standard_request_som1.ksy` - 44B SES header
  - `earlysim/datamodel/protocols/ue/transport/ses/small_message.ksy` - 32B small header
  - `earlysim/datamodel/protocols/ue/transport/pds/rud_rod_request.ksy` - 12B PDS header
  - `earlysim/datamodel/protocols/ue/transport/pds/entropy_header.ksy` - 4B entropy header
  - `earlysim/datamodel/protocols/ue/transport/tss/security_header.ksy` - TSS encryption
  - `earlysim/datamodel/protocols/ue/transport/cms/ack_cc_state_nscc.ksy` - CC state

  **Draft Content**:
  - `.sisyphus/drafts/ue-tagged-send-variants.md` - Contains research findings

  **WHY Each Reference Matters**:
  - `packet_taxonomy_ue_ses.md` - Follow existing SES documentation format
  - `standard_request_som1.ksy` - Source of truth for 44B header fields
  - `small_message.ksy` - Source of truth for 32B header fields
  - `rud_rod_request.ksy` - Source of truth for PDS header fields

  **Acceptance Criteria**:

  ```bash
  # Verify document exists
  test -f analysis/packet_taxonomy/packet_taxonomy_ue_tagged_send_variants.md
  # Assert: file exists

  # Verify key sections present
  grep -c "## 1. Overview\|## 2. Protocol Stack\|## 3. Packet Type Matrix\|## 4. Tagged-Send" analysis/packet_taxonomy/packet_taxonomy_ue_tagged_send_variants.md
  # Assert: >= 4

  # Verify wire diagrams present (box-drawing characters)
  grep -c "┌\|├\|└" analysis/packet_taxonomy/packet_taxonomy_ue_tagged_send_variants.md
  # Assert: >= 20

  # Verify all 10 variants documented
  grep -c "UE Standard\|UE + CSIG Compact\|UE + CSIG Wide\|UE IPv4\|UE + Encrypted\|UE Small\|UE Rendezvous\|UE Deferrable" analysis/packet_taxonomy/packet_taxonomy_ue_tagged_send_variants.md
  # Assert: >= 8
  ```

  **Evidence to Capture:**
  - [x] grep output showing section headers (8 sections found)
  - [x] grep output showing wire diagram characters (56 chars found)
  - [x] grep output showing variant names (18 mentions found)

  **Commit**: YES
  - Message: `docs(taxonomy): add UE tagged-send and IPv4 variants documentation`
  - Files: `analysis/packet_taxonomy/packet_taxonomy_ue_tagged_send_variants.md`

---

- [x] 2. Verify wire format diagrams are complete

  **What to do**:
  - Review the created document
  - Ensure each of the 10 packet variants has a wire format diagram
  - Verify diagrams show:
    - Byte offsets
    - Field names
    - Field sizes
    - Total header size

  **Must NOT do**:
  - Do NOT create separate diagram files
  - Do NOT use non-ASCII characters outside box-drawing set

  **Recommended Agent Profile**:
  - **Category**: `writing`
    - Reason: Documentation review and refinement
  - **Skills**: `[]`
    - No special skills needed

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Sequential
  - **Blocks**: Task 3
  - **Blocked By**: Task 1

  **References**:
  - `analysis/packet_taxonomy/packet_taxonomy_ue_tagged_send_variants.md` - Document to verify

  **Acceptance Criteria**:

  ```bash
  # Count wire diagrams (each starts with ┌──────────)
  grep -c "┌──────────┬" analysis/packet_taxonomy/packet_taxonomy_ue_tagged_send_variants.md
  # Assert: >= 4 (main diagrams)

  # Verify header size summary table exists
  grep -c "Header Size Summary\|Total Header" analysis/packet_taxonomy/packet_taxonomy_ue_tagged_send_variants.md
  # Assert: >= 1
  ```

  **Commit**: NO (grouped with Task 1 if changes needed)

---

- [x] 3. Create work item for CN7000 Packet Taxonomy.ppt comparison

  **What to do**:
  - Create a work item file to track the comparison table task
  - Include:
    - Description of the comparison needed
    - Reference to CN7000 Packet Taxonomy.ppt
    - Expected deliverable format
    - Priority and estimated effort

  **Must NOT do**:
  - Do NOT create the comparison table itself (deferred)
  - Do NOT modify the main documentation file

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Simple file creation
  - **Skills**: `[]`
    - No special skills needed

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Sequential
  - **Blocks**: None
  - **Blocked By**: Task 1, Task 2

  **References**:
  - User request for comparison table
  - CN7000 Packet Taxonomy.ppt (external reference)

  **Acceptance Criteria**:

  ```bash
  # Verify work item file exists
  test -f analysis/packet_taxonomy/WORK_ITEMS.md || test -f analysis/ualink/ualink_issues.md
  # Assert: one of these exists

  # Verify work item content
  grep -c "CN7000 Packet Taxonomy\|comparison table\|UE+" analysis/packet_taxonomy/WORK_ITEMS.md 2>/dev/null || echo "0"
  # Assert: >= 1 if file exists
  ```

  **Work Item Content**:
  ```markdown
  ## W-15: UE+ to CN7000 Packet Taxonomy.ppt Comparison Table

  **Status**: Open
  **Priority**: Medium
  **Estimated Effort**: 2-4 hours

  ### Description
  Create a comparison table mapping UE+ packet types (as documented in 
  packet_taxonomy_ue_tagged_send_variants.md) to the nomenclature used in 
  CN7000 Packet Taxonomy.ppt.

  ### Expected Deliverable
  A table in packet_taxonomy_ue_tagged_send_variants.md with columns:
  - UE Spec Name
  - CN7000 PPT Name
  - Key Differences
  - Notes

  ### Dependencies
  - Requires access to CN7000 Packet Taxonomy.ppt
  - packet_taxonomy_ue_tagged_send_variants.md must be complete

  ### References
  - CN7000 Packet Taxonomy.ppt (internal document)
  - UltraEthernet Specification v1.0.1
  ```

  **Commit**: YES
  - Message: `docs(taxonomy): add work item for CN7000 comparison table`
  - Files: `analysis/packet_taxonomy/WORK_ITEMS.md`

---

## Commit Strategy

| After Task | Message | Files | Verification |
|------------|---------|-------|--------------|
| 1 | `docs(taxonomy): add UE tagged-send and IPv4 variants documentation` | packet_taxonomy_ue_tagged_send_variants.md | grep sections |
| 3 | `docs(taxonomy): add work item for CN7000 comparison table` | WORK_ITEMS.md | grep content |

---

## Success Criteria

### Verification Commands
```bash
# Main document verification
grep -c "Tagged-Send\|Wire Format\|Header Size" analysis/packet_taxonomy/packet_taxonomy_ue_tagged_send_variants.md
# Expected: >= 3

# Wire diagrams verification
grep -c "┌──────────" analysis/packet_taxonomy/packet_taxonomy_ue_tagged_send_variants.md
# Expected: >= 4

# Work item verification
grep -c "W-15\|CN7000 Packet Taxonomy" analysis/packet_taxonomy/WORK_ITEMS.md
# Expected: >= 1
```

### Final Checklist
- [x] packet_taxonomy_ue_tagged_send_variants.md exists with all sections
- [x] Wire format diagrams present for all major variants
- [x] Header size summary table complete
- [x] Cross-references to existing UE taxonomy docs
- [x] Work item created for CN7000 comparison table
- [x] Both files committed (N/A - analysis/ not in git repo)

---

## Document Content Reference

The full document content has been prepared and is available in:
- `.sisyphus/drafts/ue-tagged-send-variants.md` - Research findings
- This plan's Task 1 references - Complete document structure

Key sections to include:
1. Overview (packet categories, delivery modes)
2. Protocol Stack (ASCII diagram)
3. Packet Type Matrix (SES formats, opcodes)
4. Tagged-Send Packet Variants (10 variants with field tables)
5. Wire Format Diagrams (4 detailed ASCII diagrams)
6. Header Size Summary (comparison table)
7. Cross-References (related docs, datamodel files)
8. References (UE Spec sections)
