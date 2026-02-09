# Packet Taxonomy Technical Report

## TL;DR

> **Quick Summary**: Create a comprehensive technical report documenting all protocols in `datamodel/protocols/`, following the exemplar format of `packet_taxonomy_ue_plus_variants.md`. Each protocol family gets detailed packet structures, variant matrices, state machines, and datamodel coverage. Reports are formatted as YAML for PowerPoint generation via `pptx_helper`.
> 
> **Deliverables**:
> - `reports/packet_taxonomy/technical_report.yaml` - Master technical report (YAML for PPTX)
> - `reports/packet_taxonomy/technical_report.pptx` - Generated PowerPoint
> - `reports/packet_taxonomy/technical_report_ue.yaml` - Ultra Ethernet protocols
> - `reports/packet_taxonomy/technical_report_ue.pptx` - Generated PowerPoint
> - `reports/packet_taxonomy/technical_report_ethernet.yaml` - Standard Ethernet protocols
> - `reports/packet_taxonomy/technical_report_ethernet.pptx` - Generated PowerPoint
> - `reports/packet_taxonomy/technical_report_roce.yaml` - RoCEv2 protocols
> - `reports/packet_taxonomy/technical_report_roce.pptx` - Generated PowerPoint
> - `reports/packet_taxonomy/technical_report_cornelis.yaml` - Cornelis proprietary protocols
> - `reports/packet_taxonomy/technical_report_cornelis.pptx` - Generated PowerPoint
> - `reports/packet_taxonomy/technical_report_ualink.yaml` - UALink protocols (reference)
> - `reports/packet_taxonomy/technical_report_ualink.pptx` - Generated PowerPoint
> 
> **Estimated Effort**: Large (10-14 hours)
> **Parallel Execution**: YES - 5 protocol reports can be written in parallel after Task 1
> **Critical Path**: Task 1 → Tasks 2-6 (parallel) → Task 7 → Task 8

---

## Context

### Original Request
Create a technical report of the packet taxonomy under `datamodel/protocols/`. The report should:
- Follow the exemplar format of `packet_taxonomy_ue_plus_variants.md`
- Include packet variant matrices
- Include detailed packet structures with wire diagrams
- Document rules and state machines
- Include datamodel coverage tables
- Include references to specifications
- Be convertible to PowerPoint via `pptx_helper` module

### Interview Summary
**Key Discussions**:
- Exemplar document: `analysis/packet_taxonomy/packet_taxonomy_ue_plus_variants.md` (652 lines)
- Output location: `reports/packet_taxonomy/` folder
- Coverage: All 5 protocol families (ue, ethernet, roce, cornelis, ualink)
- 174 KSY files total across all protocols

**Research Findings**:
- Existing analysis documents in `analysis/packet_taxonomy/packet_taxonomy_*.md` (12 files)
- Protocol subdirectory structure well-organized with `protocols/` subdirs for state machines
- KSY files contain `x-spec`, `x-packet`, `x-related-headers` metadata for cross-referencing

### Exemplar Document Structure (packet_taxonomy_ue_plus_variants.md)

The exemplar contains these sections:
1. **Overview** - Key characteristics, relationship diagrams
2. **L2 Header Selection Rules** - Decision matrix, conditions, datamodel support
3. **Header Building Blocks** - Tables of headers with sizes and datamodel files
4. **Packet Variant Matrix** - Tables showing header stacks, overhead, use cases
5. **Detailed Packet Structures** - ASCII wire diagrams with byte-level detail
6. **Header Types** - Enumerations and selection tables
7. **Telemetry/Extension Types** - Protocol-specific extensions
8. **Header Overhead Summary** - Efficiency calculations
9. **Datamodel Coverage** - File status tables with line counts
10. **References** - Internal documents, external specs, datamodel directories

---

## Work Objectives

### Core Objective
Generate comprehensive technical documentation for all protocols in `datamodel/protocols/`, providing detailed packet structures, variant matrices, state machine descriptions, and datamodel coverage following the established exemplar format.

### Concrete Deliverables

**YAML Data Files** (for pptx_helper):
- `reports/packet_taxonomy/technical_report.yaml` - Master index and overview
- `reports/packet_taxonomy/technical_report_ue.yaml` - Ultra Ethernet (103 files)
- `reports/packet_taxonomy/technical_report_ethernet.yaml` - Ethernet (12 files)
- `reports/packet_taxonomy/technical_report_roce.yaml` - RoCEv2 (9 files)
- `reports/packet_taxonomy/technical_report_cornelis.yaml` - Cornelis (12 files)
- `reports/packet_taxonomy/technical_report_ualink.yaml` - UALink (38 files)

**Generated PowerPoint Files**:
- `reports/packet_taxonomy/technical_report.pptx` - Master presentation
- `reports/packet_taxonomy/technical_report_ue.pptx` - Ultra Ethernet presentation
- `reports/packet_taxonomy/technical_report_ethernet.pptx` - Ethernet presentation
- `reports/packet_taxonomy/technical_report_roce.pptx` - RoCEv2 presentation
- `reports/packet_taxonomy/technical_report_cornelis.pptx` - Cornelis presentation
- `reports/packet_taxonomy/technical_report_ualink.pptx` - UALink presentation

### Definition of Done
- [ ] Each protocol report follows exemplar structure
- [ ] All 174 KSY files documented in coverage tables
- [ ] Packet variant matrices for each protocol family
- [ ] Detailed packet structures with ASCII wire diagrams
- [ ] State machines documented with state/transition tables
- [ ] Cross-references to specifications included
- [ ] Master index links all sub-reports
- [ ] All YAML files pass pptx_helper validation
- [ ] All PPTX files generated successfully
- [ ] All PPTX files load in python-pptx without errors

### Must Have
- Packet variant matrices (header stacks, overhead, use cases)
- Detailed packet structures with byte-level wire diagrams
- State machine documentation for all `protocols/` subdirectories
- Datamodel coverage tables with file status and line counts
- References to UE Spec, IB Spec, IEEE standards, UALink Spec
- Header building blocks tables

### Must NOT Have (Guardrails)
- Duplicate content from existing `analysis/packet_taxonomy/` files (reference them instead)
- Implementation details beyond packet format documentation
- Code snippets from KSY files (reference file paths instead)
- Speculation about undocumented features

---

## Verification Strategy (MANDATORY)

### Test Decision
- **Infrastructure exists**: YES (pptx_helper module with CLI)
- **User wants tests**: Automated via pptx_helper validation
- **Framework**: pptx_helper CLI with --dry-run and python-pptx validation

### Automated Verification (NO User Intervention)

**YAML Syntax Validation** (using Bash):
```bash
for f in reports/packet_taxonomy/technical_report*.yaml; do
  python -c "import yaml; yaml.safe_load(open('$f'))" && echo "$f: valid"
done
# Assert: All files pass YAML syntax validation
```

**pptx_helper Dry-Run Validation** (using Bash):
```bash
for f in reports/packet_taxonomy/technical_report*.yaml; do
  python -m utilities.pptx_helper --type technical --data "$f" --dry-run
done
# Assert: All files pass "Validation passed"
```

**PPTX Generation** (using Bash):
```bash
for f in reports/packet_taxonomy/technical_report*.yaml; do
  pptx="${f%.yaml}.pptx"
  python -m utilities.pptx_helper --type technical --data "$f" --output "$pptx"
done
# Assert: All PPTX files generated (exit code 0)
```

**PPTX Validation** (using Bash):
```bash
for f in reports/packet_taxonomy/technical_report*.pptx; do
  python -c "from pptx import Presentation; p = Presentation('$f'); print(f'$f: {len(p.slides)} slides')"
done
# Assert: Each PPTX has >= 10 slides
```

**File Existence Check** (using Bash):
```bash
ls -la reports/packet_taxonomy/technical_report*.yaml reports/packet_taxonomy/technical_report*.pptx
# Assert: 12 files exist (6 YAML + 6 PPTX)
```

**Line Count Verification** (using Bash):
```bash
wc -l reports/packet_taxonomy/technical_report*.yaml
# Assert: Each protocol report > 150 lines
# Assert: Master report > 80 lines
```

---

## Execution Strategy

### Parallel Execution Waves

```
Wave 1 (Start Immediately):
└── Task 1: Gather datamodel structure and metadata

Wave 2 (After Wave 1):
├── Task 2: Write UE technical report YAML
├── Task 3: Write Ethernet technical report YAML
├── Task 4: Write RoCE technical report YAML
├── Task 5: Write Cornelis technical report YAML
└── Task 6: Write UALink technical report YAML

Wave 3 (After Wave 2):
└── Task 7: Write master index YAML

Wave 4 (After Wave 3):
└── Task 8: Validate all YAML and generate all PPTX files
```

### Dependency Matrix

| Task | Depends On | Blocks | Can Parallelize With |
|------|------------|--------|---------------------|
| 1 | None | 2, 3, 4, 5, 6 | None |
| 2 | 1 | 7 | 3, 4, 5, 6 |
| 3 | 1 | 7 | 2, 4, 5, 6 |
| 4 | 1 | 7 | 2, 3, 5, 6 |
| 5 | 1 | 7 | 2, 3, 4, 6 |
| 6 | 1 | 7 | 2, 3, 4, 5 |
| 7 | 2, 3, 4, 5, 6 | 8 | None |
| 8 | 7 | None | None (final) |

---

## TODOs

- [x] 1. Gather Datamodel Structure and Metadata

  **What to do**:
  - List all KSY files in each protocol subdirectory
  - Extract `x-spec`, `x-packet`, `x-related-headers` metadata from key files
  - Identify all `protocols/` subdirectories containing state machines
  - Count files per subdirectory for coverage tables
  - Identify existing analysis documents to reference (not duplicate)

  **Must NOT do**:
  - Modify any datamodel files
  - Create new KSY files

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: File listing and metadata extraction
  - **Skills**: []
    - No special skills needed

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Wave 1
  - **Blocks**: Tasks 2-6
  - **Blocked By**: None

  **References**:
  - `earlysim/datamodel/protocols/` - All protocol directories
  - `analysis/packet_taxonomy/packet_taxonomy_ue_plus_variants.md` - Exemplar format

  **Acceptance Criteria**:
  ```bash
  # Verify data gathered for all 5 protocol families
  # Assert: File counts match expected (ue=103, ethernet=12, roce=9, cornelis=12, ualink=38)
  ```

  **Commit**: NO (data gathering only)

---

- [x] 2. Write Ultra Ethernet Technical Report YAML

  **What to do**:
  - Create `reports/packet_taxonomy/technical_report_ue.yaml`
  - Follow pptx_helper technical presentation YAML schema
  - Structure content per exemplar `packet_taxonomy_ue_plus_variants.md`
  - Document all 103 UE KSY files organized by sublayer:
    - transport/pds (14 files) - Packet Delivery Sublayer
    - transport/ses (15 files) - Semantic Sublayer
    - transport/cms (15 files) - Congestion Management
    - transport/tss (9 files) - Transport Security
    - link/llr (9 files) - Link Level Reliability
    - link/lldp (3 files) - Link Layer Discovery
    - link/cbfc (5 files) - Credit-Based Flow Control
    - network (4 files) - UFH headers, DSCP, trimming
    - physical (1 file) - Control ordered sets
  - Include packet variant matrices for PDS types, SES types
  - Include detailed packet structures for key formats
  - Document state machines in `protocols/` subdirectories
  - Include datamodel coverage table

  **Must NOT do**:
  - Duplicate content from `analysis/packet_taxonomy/packet_taxonomy_ue_*.md`
  - Include Cornelis-specific extensions (those go in cornelis report)

  **Recommended Agent Profile**:
  - **Category**: `writing`
    - Reason: Technical documentation creation
  - **Skills**: []
    - No special skills needed

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 3, 4, 5, 6)
  - **Blocks**: Task 7
  - **Blocked By**: Task 1

  **References**:
  - `earlysim/datamodel/protocols/ue/` - All UE KSY files
  - `analysis/packet_taxonomy/packet_taxonomy_ue_plus_variants.md` - Exemplar format
  - `analysis/packet_taxonomy/packet_taxonomy_ue_pds.md` - PDS reference
  - `analysis/packet_taxonomy/packet_taxonomy_ue_ses.md` - SES reference
  - `analysis/packet_taxonomy/packet_taxonomy_ue_cms_tss.md` - CMS/TSS reference
  - `analysis/packet_taxonomy/packet_taxonomy_ue_link.md` - Link layer reference
  - UE Specification v1.0.1

  **Acceptance Criteria**:
  ```bash
  # Verify YAML file exists with substantial content
  wc -l reports/packet_taxonomy/technical_report_ue.yaml
  # Assert: > 300 lines
  
  # Verify YAML syntax
  python -c "import yaml; yaml.safe_load(open('reports/packet_taxonomy/technical_report_ue.yaml'))"
  # Assert: Exit code 0
  
  # Verify KSY coverage
  grep -c "\.ksy" reports/packet_taxonomy/technical_report_ue.yaml
  # Assert: >= 100 references
  ```

  **Commit**: NO (local report)

---

- [x] 3. Write Ethernet Technical Report YAML

  **What to do**:
  - Create `reports/packet_taxonomy/technical_report_ethernet.yaml`
  - Follow pptx_helper technical presentation YAML schema
  - Document all 12 Ethernet KSY files:
    - link (5 files) - Ethernet II, 802.3, VLAN, LLC, SNAP
    - network (2 files) - IPv4, IPv6
    - transport (2 files) - TCP, UDP
    - rss (3 files) - Hash algorithm, Toeplitz key, hash input
  - Include packet variant matrices for frame types
  - Include detailed packet structures for Ethernet II, VLAN, IPv4, IPv6
  - Document RSS hash algorithm selection
  - Include datamodel coverage table

  **Must NOT do**:
  - Include RoCE-specific content (that goes in roce report)

  **Recommended Agent Profile**:
  - **Category**: `writing`
    - Reason: Technical documentation creation
  - **Skills**: []
    - No special skills needed

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 2, 4, 5, 6)
  - **Blocks**: Task 7
  - **Blocked By**: Task 1

  **References**:
  - `earlysim/datamodel/protocols/ethernet/` - All Ethernet KSY files
  - `analysis/packet_taxonomy/packet_taxonomy_ethernet.md` - Existing analysis
  - IEEE 802.3, IEEE 802.1Q, RFC 791, RFC 8200, RFC 793, RFC 768

  **Acceptance Criteria**:
  ```bash
  wc -l reports/packet_taxonomy/technical_report_ethernet.yaml
  # Assert: > 150 lines
  
  python -c "import yaml; yaml.safe_load(open('reports/packet_taxonomy/technical_report_ethernet.yaml'))"
  # Assert: Exit code 0
  
  grep -c "\.ksy" reports/packet_taxonomy/technical_report_ethernet.yaml
  # Assert: >= 12 references
  ```

  **Commit**: NO (local report)

---

- [x] 4. Write RoCE Technical Report YAML

  **What to do**:
  - Create `reports/packet_taxonomy/technical_report_roce.yaml`
  - Follow pptx_helper technical presentation YAML schema
  - Document all 9 RoCE KSY files:
    - transport (8 files) - BTH, RETH, AETH, DETH, IMMDT, AtomicETH, AtomicAckETH, ICRC
    - protocols (1 file) - QP state machine
  - Include packet variant matrices for operation types
  - Include detailed packet structures for BTH, RETH, AETH, AtomicETH
  - Document QP state machine with state/transition table
  - Document operation validity matrix by transport type
  - Include datamodel coverage table

  **Must NOT do**:
  - Include UE-specific content

  **Recommended Agent Profile**:
  - **Category**: `writing`
    - Reason: Technical documentation creation
  - **Skills**: []
    - No special skills needed

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 2, 3, 5, 6)
  - **Blocks**: Task 7
  - **Blocked By**: Task 1

  **References**:
  - `earlysim/datamodel/protocols/roce/` - All RoCE KSY files
  - `analysis/packet_taxonomy/packet_taxonomy_rocev2.md` - Existing analysis
  - InfiniBand Architecture Specification v1.4

  **Acceptance Criteria**:
  ```bash
  wc -l reports/packet_taxonomy/technical_report_roce.yaml
  # Assert: > 150 lines
  
  python -c "import yaml; yaml.safe_load(open('reports/packet_taxonomy/technical_report_roce.yaml'))"
  # Assert: Exit code 0
  
  grep -c "\.ksy" reports/packet_taxonomy/technical_report_roce.yaml
  # Assert: >= 9 references
  ```

  **Commit**: NO (local report)

---

- [x] 5. Write Cornelis Technical Report YAML

  **What to do**:
  - Create `reports/packet_taxonomy/technical_report_cornelis.yaml`
  - Follow pptx_helper technical presentation YAML schema
  - Document all 12 Cornelis KSY files:
    - link (2 files) - UE+, L2 prefix
    - network (4 files) - UFH-16+, UFH-32+, collective_l2, scaleup_l2
    - transport (2 files) - CSIG+, pkey
    - config (2 files) - address_vector, peer_capability
    - protocols (1 file) - L2 header selection SM
    - encapsulation (1 file) - VxLAN+
  - Include packet variant matrices for UE+ variants
  - Include detailed packet structures for UE+, UFH-16+, UFH-32+, CSIG+
  - Document L2 header selection state machine
  - Document HMAC addressing formats
  - Include datamodel coverage table

  **Must NOT do**:
  - Duplicate UE+ variants content from `packet_taxonomy_ue_plus_variants.md` (reference it)

  **Recommended Agent Profile**:
  - **Category**: `writing`
    - Reason: Technical documentation creation
  - **Skills**: []
    - No special skills needed

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 2, 3, 4, 6)
  - **Blocks**: Task 7
  - **Blocked By**: Task 1

  **References**:
  - `earlysim/datamodel/protocols/cornelis/` - All Cornelis KSY files
  - `analysis/packet_taxonomy/packet_taxonomy_cornelis.md` - Existing analysis
  - `analysis/packet_taxonomy/packet_taxonomy_ue_plus_variants.md` - UE+ variants
  - Cornelis UE+ Specification

  **Acceptance Criteria**:
  ```bash
  wc -l reports/packet_taxonomy/technical_report_cornelis.yaml
  # Assert: > 150 lines
  
  python -c "import yaml; yaml.safe_load(open('reports/packet_taxonomy/technical_report_cornelis.yaml'))"
  # Assert: Exit code 0
  
  grep -c "\.ksy" reports/packet_taxonomy/technical_report_cornelis.yaml
  # Assert: >= 12 references
  ```

  **Commit**: NO (local report)

---

- [x] 6. Write UALink Technical Report YAML

  **What to do**:
  - Create `reports/packet_taxonomy/technical_report_ualink.yaml`
  - Follow pptx_helper technical presentation YAML schema
  - Document all 38 UALink KSY files:
    - upli (8 files) - Upper Protocol Layer Interface
    - transaction (9 files) - Transaction Layer flits
    - datalink (12 files) - Data Link Layer
    - physical (4 files) - Physical Layer
    - security (5 files) - Encryption/Authentication
  - Include packet variant matrices for flit types
  - Include detailed packet structures for TL flit, DL flit, segment header
  - Document state machines:
    - link_training.ksy
    - link_state.ksy
    - link_resiliency.ksy
    - link_level_replay.ksy
    - link_folding.ksy
    - key_derivation.ksy
    - key_rotation.ksy
    - flow_control.ksy
    - connection_handshake.ksy
    - compression.ksy
    - address_cache.ksy
  - Include datamodel coverage table
  - Note: UALink is reference only (not PMR-supported)

  **Must NOT do**:
  - Imply PMR supports UALink

  **Recommended Agent Profile**:
  - **Category**: `writing`
    - Reason: Technical documentation creation
  - **Skills**: []
    - No special skills needed

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 2, 3, 4, 5)
  - **Blocks**: Task 7
  - **Blocked By**: Task 1

  **References**:
  - `earlysim/datamodel/protocols/ualink/` - All UALink KSY files
  - `analysis/packet_taxonomy/packet_taxonomy_ualink.md` - Existing analysis
  - `analysis/ualink/ualink_issues.md` - UALink issues
  - UALink 200 Specification v1.0

  **Acceptance Criteria**:
  ```bash
  wc -l reports/packet_taxonomy/technical_report_ualink.yaml
  # Assert: > 200 lines
  
  python -c "import yaml; yaml.safe_load(open('reports/packet_taxonomy/technical_report_ualink.yaml'))"
  # Assert: Exit code 0
  
  grep -c "\.ksy" reports/packet_taxonomy/technical_report_ualink.yaml
  # Assert: >= 38 references
  ```

  **Commit**: NO (local report)

---

- [x] 7. Write Master Index YAML

  **What to do**:
  - Create `reports/packet_taxonomy/technical_report.yaml`
  - Include overview of all protocol families
  - Include summary statistics (174 KSY files, 5 families)
  - Include links to all sub-reports (reference PPTX filenames)
  - Include cross-protocol comparison table

  **Must NOT do**:
  - Duplicate detailed content from sub-reports

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Index creation
  - **Skills**: []
    - No special skills needed

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Wave 3
  - **Blocks**: Task 8
  - **Blocked By**: Tasks 2, 3, 4, 5, 6

  **References**:
  - All 5 sub-reports created in Tasks 2-6
  - `.sisyphus/rules/packet-taxonomy-reporting.md` - Reporting rules

  **Acceptance Criteria**:
  ```bash
  # Verify all 6 YAML files exist
  ls reports/packet_taxonomy/technical_report*.yaml | wc -l
  # Assert: 6 files
  
  # Verify YAML syntax
  python -c "import yaml; yaml.safe_load(open('reports/packet_taxonomy/technical_report.yaml'))"
  # Assert: Exit code 0
  
  # Verify master index references all sub-reports
  grep -c "technical_report_" reports/packet_taxonomy/technical_report.yaml
  # Assert: >= 5 references
  ```

  **Commit**: NO (local reports)

---

- [x] 8. Validate All YAML and Generate All PPTX Files

  **What to do**:
  - Validate all 6 YAML files with pptx_helper --dry-run
  - Fix any validation errors
  - Generate all 6 PPTX files
  - Verify all PPTX files load correctly with python-pptx

  **Must NOT do**:
  - Skip validation
  - Generate PPTX without dry-run validation first

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: CLI command execution and validation
  - **Skills**: []
    - No special skills needed

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Wave 4 (final)
  - **Blocks**: None
  - **Blocked By**: Task 7

  **References**:
  - `utilities/pptx_helper/cli.py` - CLI interface
  - All 6 YAML files from Tasks 2-7

  **Acceptance Criteria**:
  ```bash
  # Dry-run validation for all files
  for f in reports/packet_taxonomy/technical_report*.yaml; do
    python -m utilities.pptx_helper --type technical --data "$f" --dry-run
  done
  # Assert: All pass "Validation passed"
  
  # Generate all PPTX files
  for f in reports/packet_taxonomy/technical_report*.yaml; do
    pptx="${f%.yaml}.pptx"
    python -m utilities.pptx_helper --type technical --data "$f" --output "$pptx"
  done
  # Assert: All exit code 0
  
  # Verify all PPTX files exist and are valid
  for f in reports/packet_taxonomy/technical_report*.pptx; do
    python -c "from pptx import Presentation; p = Presentation('$f'); print(f'$f: {len(p.slides)} slides')"
  done
  # Assert: Each file has >= 10 slides
  
  # Verify file counts
  ls reports/packet_taxonomy/technical_report*.yaml | wc -l
  # Assert: 6 YAML files
  ls reports/packet_taxonomy/technical_report*.pptx | wc -l
  # Assert: 6 PPTX files
  ```

  **Commit**: NO (local reports)

---

## YAML Template for pptx_helper Technical Presentations

Each protocol report YAML should follow this structure:

```yaml
title: "PMR Packet Taxonomy: [Protocol] Technical Report"
subtitle: "[Protocol description]"

presenter:
  name: "Packet Taxonomy Team"
  info: "Cornelis Networks Engineering"

sections:
  # Section 1: Overview
  - type: section_header
    title: "Overview"
    subtitle: "[Protocol] Key Characteristics"

  - type: content
    title: "Protocol Summary"
    bullets:
      - "Key characteristic 1"
      - "Key characteristic 2"

  - type: table
    title: "Protocol Parameters"
    headers: ["Parameter", "Value", "Notes"]
    rows:
      - ["Param 1", "Value 1", "Note 1"]

  # Section 2: Protocol Architecture
  - type: section_header
    title: "Protocol Architecture"
    subtitle: "Layer Structure and Components"

  - type: content
    title: "Layer Diagram"
    bullets:
      - "Layer relationships described"

  # Section 3: Header Building Blocks
  - type: section_header
    title: "Header Building Blocks"
    subtitle: "Packet Header Components"

  - type: table
    title: "Header Formats"
    headers: ["Header", "Size", "Datamodel File", "Description"]
    rows:
      - ["Header1", "N bytes", "path/to/file.ksy", "Description"]

  # Section 4: Packet Variant Matrix
  - type: section_header
    title: "Packet Variant Matrix"
    subtitle: "Header Combinations and Use Cases"

  - type: table
    title: "Packet Variants"
    headers: ["Variant", "Header Stack", "Overhead", "Use Case"]
    rows:
      - ["Variant1", "H1 + H2 + H3", "N bytes", "Use case"]

  # Section 5: Detailed Packet Structures
  - type: section_header
    title: "Detailed Packet Structures"
    subtitle: "Wire Format Diagrams"

  - type: code
    title: "Packet Structure: [Name]"
    language: "text"
    code: |
      +--------+--------+--------+
      | Field1 | Field2 | Field3 |
      +--------+--------+--------+

  # Section 6: State Machines and Rules
  - type: section_header
    title: "State Machines and Rules"
    subtitle: "Protocol Behavior"

  - type: table
    title: "State Machine: [Name]"
    headers: ["State", "Event", "Next State", "Action"]
    rows:
      - ["State1", "Event1", "State2", "Action1"]

  # Section 7: Header Overhead Summary
  - type: section_header
    title: "Header Overhead Summary"
    subtitle: "Efficiency Analysis"

  - type: table
    title: "Overhead Comparison"
    headers: ["Variant", "Overhead", "4KB Efficiency"]
    rows:
      - ["Variant1", "N bytes", "XX.X%"]

  # Section 8: Datamodel Coverage
  - type: section_header
    title: "Datamodel Coverage"
    subtitle: "KSY File Status"

  - type: table
    title: "File Coverage"
    headers: ["File", "Status", "Lines", "Description"]
    rows:
      - ["file.ksy", "Complete", "NNN", "Description"]

  # Section 9: References
  - type: section_header
    title: "References"
    subtitle: "Specifications and Documents"

  - type: item_list
    title: "External Specifications"
    items:
      - "Specification 1"
      - "Specification 2"
    item_type: "closed"

  - type: item_list
    title: "Datamodel Directories"
    items:
      - "datamodel/protocols/[protocol]/"
    item_type: "closed"
```

### pptx_helper Slide Types for Technical Presentations

| Type | Purpose | Key Fields |
|------|---------|------------|
| `section_header` | Visual divider | title, subtitle |
| `content` | Bullet points | title, bullets, subtitle |
| `table` | Data tables | title, headers, rows, description |
| `code` | Code/diagrams | title, code, language |
| `two_column` | Side-by-side | title, left_content, right_content |
| `image` | Images | title, image_path, caption |
| `image_content` | Image + text | title, content, image_path |

---

## Success Criteria

### Verification Commands
```bash
# All YAML files exist
ls -la reports/packet_taxonomy/technical_report*.yaml

# All PPTX files exist
ls -la reports/packet_taxonomy/technical_report*.pptx

# YAML line counts
wc -l reports/packet_taxonomy/technical_report*.yaml

# YAML validation
for f in reports/packet_taxonomy/technical_report*.yaml; do
  python -c "import yaml; yaml.safe_load(open('$f'))" && echo "$f: valid"
done

# PPTX validation
for f in reports/packet_taxonomy/technical_report*.pptx; do
  python -c "from pptx import Presentation; p = Presentation('$f'); print(f'$f: {len(p.slides)} slides')"
done

# KSY coverage
for f in reports/packet_taxonomy/technical_report_*.yaml; do
  echo "$f: $(grep -c '\.ksy' $f) KSY references"
done
```

### Final Checklist
- [ ] Master index YAML created at `reports/packet_taxonomy/technical_report.yaml`
- [ ] Master index PPTX generated at `reports/packet_taxonomy/technical_report.pptx`
- [ ] UE report YAML created with >= 100 KSY references
- [ ] UE report PPTX generated with >= 20 slides
- [ ] Ethernet report YAML created with >= 12 KSY references
- [ ] Ethernet report PPTX generated with >= 10 slides
- [ ] RoCE report YAML created with >= 9 KSY references
- [ ] RoCE report PPTX generated with >= 10 slides
- [ ] Cornelis report YAML created with >= 12 KSY references
- [ ] Cornelis report PPTX generated with >= 10 slides
- [ ] UALink report YAML created with >= 38 KSY references
- [ ] UALink report PPTX generated with >= 15 slides
- [ ] All YAML files pass pptx_helper validation
- [ ] All PPTX files load in python-pptx without errors
- [ ] Packet variant matrices included in each report
- [ ] Detailed packet structures with ASCII diagrams included
- [ ] State machines documented where applicable
- [ ] Datamodel coverage tables included
- [ ] References to specifications included
- [ ] Total coverage: 174 KSY files documented
