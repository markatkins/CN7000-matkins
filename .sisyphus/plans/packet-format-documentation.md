# Packet Format Documentation - Detailed Header/Field Documentation

## TL;DR

> **Quick Summary**: Create a KSY parser utility that extracts field definitions from Kaitai Struct files and generates detailed header documentation with field tables and ASCII packet diagrams for PowerPoint reports.
> 
> **Deliverables**:
> - KSY parser utility (`utilities/ksy_parser/`)
> - ASCII packet diagram generator (RFC-style bit diagrams)
> - Updated technical report YAML files with field-level detail
> - Regenerated PPTX files with tables and diagrams
> 
> **Estimated Effort**: Medium
> **Parallel Execution**: YES - 2 waves
> **Critical Path**: Task 1 → Task 2 → Task 3 → Task 4 → Task 5

---

## Context

### Original Request
User wants detailed header and packet format documentation instead of just file statistics. The documentation should include:
- Field-level tables (name, bit offset, size, type, description)
- Visual bit diagrams (ASCII/RFC-style packet layouts)
- Content extracted directly from KSY files

### Interview Summary
**Key Discussions**:
- Detail level: Both field tables AND visual diagrams
- Source: Extract from KSY files (auto-generate)
- Priority: All protocols (UE, Ethernet, RoCE, Cornelis, UALink)

**Research Findings**:
- KSY files contain rich metadata in `seq` (fields), `instances` (computed), `doc` (descriptions)
- Extended metadata in `x-spec`, `x-packet`, `x-related-headers` sections
- Field types include: `u1`, `u2`, `u4`, `u8`, `b1`-`b24` (bit fields)
- Example: `bth.ksy` has 12-byte header with opcode, flags, pkey, dest_qp, psn fields

---

## Work Objectives

### Core Objective
Extract field definitions from KSY files and generate detailed documentation with field tables and ASCII packet diagrams for technical reports.

### Concrete Deliverables
- `utilities/ksy_parser/parser.py` - KSY file parser
- `utilities/ksy_parser/diagram.py` - ASCII packet diagram generator
- `utilities/ksy_parser/report.py` - YAML section generator
- `utilities/ksy_parser/__init__.py` - Module exports
- Updated `reports/packet_taxonomy/technical_report_*.yaml` files
- Regenerated `reports/packet_taxonomy/technical_report_*.pptx` files

### Definition of Done
- [x] `python -c "from utilities.ksy_parser import KsyParser"` succeeds
- [x] Parser extracts all fields from `bth.ksy` with correct sizes
- [x] ASCII diagram renders 12-byte BTH header correctly
- [x] Technical report YAML contains field tables for all protocols
- [x] PPTX files contain rendered field tables and diagrams

### Must Have
- Field extraction: name, type, size (bits/bytes), description
- Bit-level accuracy for packed fields (b1, b8, b24, etc.)
- ASCII diagram with bit positions (RFC 2360 style)
- Integration with existing pptx_helper CLI

### Must NOT Have (Guardrails)
- No modification to original KSY files
- No external dependencies beyond PyYAML (already used)
- No complex parsing - use YAML safe_load only
- No graphical diagrams (ASCII only for PPTX compatibility)

---

## Verification Strategy

### Test Decision
- **Infrastructure exists**: YES (pytest available)
- **User wants tests**: YES (TDD for parser)
- **Framework**: pytest

### TDD Approach
Each TODO follows RED-GREEN-REFACTOR:
1. Write failing test first
2. Implement minimum code to pass
3. Refactor while keeping green

---

## Execution Strategy

### Parallel Execution Waves

```
Wave 1 (Start Immediately):
├── Task 1: Create KSY parser module
└── Task 2: Create ASCII diagram generator

Wave 2 (After Wave 1):
├── Task 3: Create report section generator
└── Task 4: Update technical report YAML files

Wave 3 (After Wave 2):
└── Task 5: Regenerate PPTX files and verify

Critical Path: Task 1 → Task 3 → Task 4 → Task 5
Parallel Speedup: ~30% faster than sequential
```

### Dependency Matrix

| Task | Depends On | Blocks | Can Parallelize With |
|------|------------|--------|---------------------|
| 1 | None | 3, 4 | 2 |
| 2 | None | 3 | 1 |
| 3 | 1, 2 | 4 | None |
| 4 | 3 | 5 | None |
| 5 | 4 | None | None (final) |

---

## TODOs

- [x] 1. Create KSY Parser Module

  **What to do**:
  - Create `utilities/ksy_parser/` directory
  - Implement `parser.py` with `KsyParser` class
  - Parse YAML structure to extract `seq` fields
  - Handle field types: `u1`, `u2`, `u4`, `u8`, `b1`-`b64`
  - Extract `doc` strings for descriptions
  - Parse `x-packet` metadata for header size
  - Create dataclasses: `KsyField`, `KsyHeader`

  **Must NOT do**:
  - Do not modify any KSY files
  - Do not use complex regex parsing
  - Do not add external dependencies

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Straightforward YAML parsing with well-defined structure
  - **Skills**: []
    - No special skills needed - standard Python

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Task 2)
  - **Blocks**: Tasks 3, 4
  - **Blocked By**: None

  **References**:

  **Pattern References**:
  - `earlysim/datamodel/protocols/roce/transport/bth.ksy` - Example KSY with `seq` fields, `instances`, `x-packet` metadata
  - `earlysim/datamodel/protocols/roce/transport/reth.ksy` - Simpler 16-byte header example
  - `earlysim/datamodel/protocols/ualink/datalink/flit_header.ksy` - Bit-field example with `b1`, `b3`, `b9`

  **Type References**:
  - KSY field types: `u1` (1 byte), `u2` (2 bytes), `u4` (4 bytes), `u8` (8 bytes)
  - KSY bit types: `b1` (1 bit), `b8` (8 bits), `b24` (24 bits)
  - `type: b24` means 24-bit field, `type: u4` means 4-byte field

  **Implementation Details**:
  ```python
  # Field size calculation
  TYPE_SIZES = {
      'u1': 8, 'u2': 16, 'u4': 32, 'u8': 64,  # bytes to bits
      's1': 8, 's2': 16, 's4': 32, 's8': 64,
  }
  # For 'bN' types, extract N as bit count
  # e.g., 'b24' -> 24 bits
  
  @dataclass
  class KsyField:
      name: str
      type_str: str
      size_bits: int
      offset_bits: int
      description: str
  
  @dataclass  
  class KsyHeader:
      id: str
      title: str
      size_bytes: int
      fields: List[KsyField]
      doc: str
  ```

  **Acceptance Criteria**:

  **TDD Tests**:
  - [ ] Test file: `tests/unit/test_ksy_parser.py`
  - [ ] Test: `test_parse_bth_header` - parses BTH, returns 12-byte header with 9 fields
  - [ ] Test: `test_parse_bit_fields` - correctly calculates bit sizes for b1, b8, b24
  - [ ] Test: `test_extract_description` - extracts doc strings from fields
  - [ ] `pytest tests/unit/test_ksy_parser.py` → PASS

  **Automated Verification**:
  ```bash
  python3 -c "
  from utilities.ksy_parser import KsyParser
  parser = KsyParser()
  header = parser.parse('earlysim/datamodel/protocols/roce/transport/bth.ksy')
  assert header.id == 'roce_bth'
  assert header.size_bytes == 12
  assert len(header.fields) >= 7
  print('Parser verification PASSED')
  "
  ```

  **Commit**: YES
  - Message: `feat(ksy_parser): add KSY file parser for field extraction`
  - Files: `utilities/ksy_parser/__init__.py`, `utilities/ksy_parser/parser.py`
  - Pre-commit: `pytest tests/unit/test_ksy_parser.py`

---

- [x] 2. Create ASCII Packet Diagram Generator

  **What to do**:
  - Implement `diagram.py` with `PacketDiagram` class
  - Generate RFC 2360-style ASCII bit diagrams
  - Support 32-bit wide diagrams (standard)
  - Show bit positions, field names, sizes
  - Handle fields that span multiple rows
  - Return diagram as multi-line string

  **Must NOT do**:
  - No graphical output (PNG, SVG)
  - No external diagram libraries
  - No Unicode box-drawing (ASCII only for PPTX)

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: String formatting task with clear output format
  - **Skills**: []
    - No special skills needed

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Task 1)
  - **Blocks**: Task 3
  - **Blocked By**: None

  **References**:

  **Pattern References**:
  - RFC 2360 packet diagram format (standard ASCII representation)
  - Example output format:
    ```
     0                   1                   2                   3
     0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |    Opcode     |     Flags     |            P_Key              |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |   Reserved    |              Destination QP                   |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |A|  Rsv  |              Packet Sequence Number                 |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    ```

  **Implementation Details**:
  ```python
  class PacketDiagram:
      def __init__(self, header: KsyHeader, width: int = 32):
          self.header = header
          self.width = width  # bits per row
      
      def render(self) -> str:
          lines = []
          lines.append(self._render_bit_ruler())
          lines.append(self._render_separator())
          
          bit_offset = 0
          for field in self.header.fields:
              # Render field, handling row wrapping
              ...
          
          return '\n'.join(lines)
      
      def _render_bit_ruler(self) -> str:
          # " 0                   1                   2                   3"
          # " 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1"
          ...
      
      def _render_separator(self) -> str:
          return "+-" + "-+-" * 31 + "-+"
  ```

  **Acceptance Criteria**:

  **TDD Tests**:
  - [ ] Test file: `tests/unit/test_packet_diagram.py`
  - [ ] Test: `test_render_bth_diagram` - renders 12-byte BTH as 3-row diagram
  - [ ] Test: `test_bit_ruler` - correct bit position labels
  - [ ] Test: `test_field_spanning` - fields spanning multiple rows render correctly
  - [ ] `pytest tests/unit/test_packet_diagram.py` → PASS

  **Automated Verification**:
  ```bash
  python3 -c "
  from utilities.ksy_parser import KsyParser, PacketDiagram
  parser = KsyParser()
  header = parser.parse('earlysim/datamodel/protocols/roce/transport/bth.ksy')
  diagram = PacketDiagram(header)
  output = diagram.render()
  assert '+-+-+-+-+-+-+-+-' in output
  assert 'Opcode' in output or 'opcode' in output
  print(output)
  print('Diagram verification PASSED')
  "
  ```

  **Commit**: YES
  - Message: `feat(ksy_parser): add ASCII packet diagram generator`
  - Files: `utilities/ksy_parser/diagram.py`
  - Pre-commit: `pytest tests/unit/test_packet_diagram.py`

---

- [x] 3. Create Report Section Generator

  **What to do**:
  - Implement `report.py` with `generate_header_section()` function
  - Generate YAML sections for technical reports
  - Create `type: table` sections with field details
  - Create `type: code_block` sections with ASCII diagrams
  - Support batch processing of multiple KSY files

  **Must NOT do**:
  - Do not modify existing YAML files directly (generate new content)
  - Do not change the existing YAML schema

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: YAML generation using existing patterns
  - **Skills**: []
    - No special skills needed

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Wave 2 (sequential)
  - **Blocks**: Task 4
  - **Blocked By**: Tasks 1, 2

  **References**:

  **Pattern References**:
  - `reports/packet_taxonomy/technical_report_ue.yaml` - Existing YAML structure with `type: table` sections
  - `utilities/pptx_helper/cli.py:183-190` - How `type: table` sections are processed

  **Output Format**:
  ```yaml
  - type: section_header
    title: "RoCE BTH - Base Transport Header"
    subtitle: "12 bytes (96 bits)"

  - type: code_block
    title: "BTH Packet Layout"
    language: ""
    code: |
       0                   1                   2                   3
       0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
      |    Opcode     |     Flags     |            P_Key              |
      ...

  - type: table
    title: "BTH Field Definitions"
    headers:
      - "Field"
      - "Bits"
      - "Offset"
      - "Type"
      - "Description"
    rows:
      - ["opcode", "8", "0", "u1", "Operation code (transport type + operation)"]
      - ["flags", "8", "8", "u1", "SE, MigReq, PadCount, TVer"]
      ...
  ```

  **Acceptance Criteria**:

  **TDD Tests**:
  - [ ] Test file: `tests/unit/test_report_generator.py`
  - [ ] Test: `test_generate_header_section` - generates valid YAML structure
  - [ ] Test: `test_table_has_all_fields` - table rows match header fields
  - [ ] `pytest tests/unit/test_report_generator.py` → PASS

  **Automated Verification**:
  ```bash
  python3 -c "
  import yaml
  from utilities.ksy_parser import KsyParser, generate_header_section
  parser = KsyParser()
  header = parser.parse('earlysim/datamodel/protocols/roce/transport/bth.ksy')
  sections = generate_header_section(header)
  assert len(sections) >= 2  # diagram + table
  assert any(s['type'] == 'table' for s in sections)
  assert any(s['type'] == 'code_block' for s in sections)
  print('Report generator verification PASSED')
  "
  ```

  **Commit**: YES
  - Message: `feat(ksy_parser): add report section generator for YAML output`
  - Files: `utilities/ksy_parser/report.py`
  - Pre-commit: `pytest tests/unit/test_report_generator.py`

---

- [x] 4. Update Technical Report YAML Files

  **What to do**:
  - Create script to batch-process KSY files by protocol
  - Generate detailed sections for each header type
  - Update `technical_report_ue.yaml` with UE header details
  - Update `technical_report_ethernet.yaml` with Ethernet/IP/TCP/UDP details
  - Update `technical_report_roce.yaml` with BTH, RETH, AETH details
  - Update `technical_report_cornelis.yaml` with OPA/OPX header details
  - Update `technical_report_ualink.yaml` with UALink header details
  - Preserve existing structure, add new detailed sections

  **Must NOT do**:
  - Do not remove existing content
  - Do not change file statistics sections (keep for reference)
  - Do not process all 100+ KSY files (select key headers only)

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
    - Reason: Multiple files to update with careful content integration
  - **Skills**: []
    - No special skills needed

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Wave 2 (after Task 3)
  - **Blocks**: Task 5
  - **Blocked By**: Task 3

  **References**:

  **KSY Files to Process** (key headers per protocol):

  **RoCE (6 headers)**:
  - `earlysim/datamodel/protocols/roce/transport/bth.ksy` - Base Transport Header
  - `earlysim/datamodel/protocols/roce/transport/reth.ksy` - RDMA Extended Transport Header
  - `earlysim/datamodel/protocols/roce/transport/aeth.ksy` - ACK Extended Transport Header
  - `earlysim/datamodel/protocols/roce/transport/deth.ksy` - Datagram Extended Transport Header
  - `earlysim/datamodel/protocols/roce/transport/atomiceth.ksy` - Atomic Extended Transport Header
  - `earlysim/datamodel/protocols/roce/transport/immdt.ksy` - Immediate Data

  **UALink (8 headers)**:
  - `earlysim/datamodel/protocols/ualink/datalink/flit_header.ksy` - DL Flit Header
  - `earlysim/datamodel/protocols/ualink/datalink/dl_flit.ksy` - DL Flit
  - `earlysim/datamodel/protocols/ualink/datalink/segment_header.ksy` - Segment Header
  - `earlysim/datamodel/protocols/ualink/transaction/tl_flit.ksy` - TL Flit
  - `earlysim/datamodel/protocols/ualink/transaction/message_half_flit.ksy` - Message Half Flit
  - `earlysim/datamodel/protocols/ualink/transaction/data_half_flit.ksy` - Data Half Flit
  - `earlysim/datamodel/protocols/ualink/transaction/control_half_flit.ksy` - Control Half Flit
  - `earlysim/datamodel/protocols/ualink/transaction/flow_control_field.ksy` - Flow Control Field

  **Cornelis (6 headers)**:
  - `earlysim/datamodel/protocols/cornelis/network/ufh_16_plus.ksy` - UFH 16+ Header
  - `earlysim/datamodel/protocols/cornelis/network/ufh_32_plus.ksy` - UFH 32+ Header
  - `earlysim/datamodel/protocols/cornelis/link/cornelis_l2_prefix.ksy` - L2 Prefix
  - `earlysim/datamodel/protocols/cornelis/link/ue_plus.ksy` - UE+ Header
  - `earlysim/datamodel/protocols/cornelis/transport/csig_plus.ksy` - CSIG+ Header
  - `earlysim/datamodel/protocols/cornelis/transport/pkey.ksy` - Partition Key

  **UE Link Layer (10 headers)**:
  - `earlysim/datamodel/protocols/ue/link/llr/llr_preamble_64b66b.ksy` - LLR Preamble
  - `earlysim/datamodel/protocols/ue/link/llr/llr_ack_ctlos.ksy` - LLR ACK
  - `earlysim/datamodel/protocols/ue/link/llr/llr_nack_ctlos.ksy` - LLR NACK
  - `earlysim/datamodel/protocols/ue/link/cbfc/cf_update.ksy` - Credit Flow Update
  - `earlysim/datamodel/protocols/ue/link/cbfc/cc_update.ksy` - Congestion Control Update
  - `earlysim/datamodel/protocols/ue/link/lldp/ue_link_negotiation_tlv.ksy` - Link Negotiation TLV
  - `earlysim/datamodel/protocols/ue/link/lldp/ue_cbfc_tlv.ksy` - CBFC TLV
  - (Select additional key headers from UE transport/session layers)

  **Target Files**:
  - `reports/packet_taxonomy/technical_report_roce.yaml`
  - `reports/packet_taxonomy/technical_report_ualink.yaml`
  - `reports/packet_taxonomy/technical_report_cornelis.yaml`
  - `reports/packet_taxonomy/technical_report_ue.yaml`
  - `reports/packet_taxonomy/technical_report_ethernet.yaml`

  **Acceptance Criteria**:

  **Automated Verification**:
  ```bash
  # Verify YAML files are valid
  for f in reports/packet_taxonomy/technical_report_*.yaml; do
    python3 -c "import yaml; yaml.safe_load(open('$f'))" && echo "$f: VALID"
  done

  # Verify new sections exist
  grep -l "BTH Field Definitions" reports/packet_taxonomy/technical_report_roce.yaml && echo "RoCE BTH: FOUND"
  grep -l "Flit Header" reports/packet_taxonomy/technical_report_ualink.yaml && echo "UALink Flit: FOUND"
  ```

  **Commit**: YES
  - Message: `docs(reports): add detailed header format documentation to technical reports`
  - Files: `reports/packet_taxonomy/technical_report_*.yaml`
  - Pre-commit: `python3 -c "import yaml; [yaml.safe_load(open(f)) for f in __import__('glob').glob('reports/packet_taxonomy/*.yaml')]"`

---

- [x] 5. Regenerate PPTX Files and Verify

  **What to do**:
  - Run pptx_helper CLI to regenerate all technical report PPTX files
  - Verify tables render with field definitions
  - Verify code blocks render with ASCII diagrams
  - Count slides and verify increase from new content

  **Must NOT do**:
  - Do not manually edit PPTX files
  - Do not skip any protocol report

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Simple regeneration and verification
  - **Skills**: []
    - No special skills needed

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Wave 3 (final)
  - **Blocks**: None
  - **Blocked By**: Task 4

  **References**:

  **Commands**:
  ```bash
  cd /home/matkins/CN7000
  for f in reports/packet_taxonomy/technical_report*.yaml; do
      pptx="${f%.yaml}.pptx"
      echo "Generating: $pptx"
      python -m utilities.pptx_helper --type technical --data "$f" --output "$pptx"
  done
  ```

  **Acceptance Criteria**:

  **Automated Verification**:
  ```bash
  # Regenerate all PPTX files
  cd /home/matkins/CN7000
  for f in reports/packet_taxonomy/technical_report*.yaml; do
      pptx="${f%.yaml}.pptx"
      python -m utilities.pptx_helper --type technical --data "$f" --output "$pptx"
  done

  # Verify PPTX files exist and have content
  python3 -c "
  from pptx import Presentation
  import glob

  for f in glob.glob('reports/packet_taxonomy/technical_report_*.pptx'):
      prs = Presentation(f)
      table_count = sum(1 for slide in prs.slides for shape in slide.shapes if shape.has_table)
      print(f'{f}: {len(prs.slides)} slides, {table_count} tables')
      assert table_count > 0, f'No tables in {f}'
  print('All PPTX files verified')
  "
  ```

  **Commit**: YES
  - Message: `docs(reports): regenerate PPTX files with detailed header documentation`
  - Files: `reports/packet_taxonomy/technical_report_*.pptx`
  - Pre-commit: None (binary files)

---

## Commit Strategy

| After Task | Message | Files | Verification |
|------------|---------|-------|--------------|
| 1 | `feat(ksy_parser): add KSY file parser` | `utilities/ksy_parser/*.py` | pytest |
| 2 | `feat(ksy_parser): add ASCII diagram generator` | `utilities/ksy_parser/diagram.py` | pytest |
| 3 | `feat(ksy_parser): add report section generator` | `utilities/ksy_parser/report.py` | pytest |
| 4 | `docs(reports): add detailed header documentation` | `reports/packet_taxonomy/*.yaml` | yaml.safe_load |
| 5 | `docs(reports): regenerate PPTX files` | `reports/packet_taxonomy/*.pptx` | pptx verification |

---

## Success Criteria

### Verification Commands
```bash
# Parser works
python3 -c "from utilities.ksy_parser import KsyParser; print('OK')"

# Diagram renders
python3 -c "from utilities.ksy_parser import PacketDiagram; print('OK')"

# YAML files valid
python3 -c "import yaml, glob; [yaml.safe_load(open(f)) for f in glob.glob('reports/packet_taxonomy/*.yaml')]"

# PPTX files have tables
python3 -c "
from pptx import Presentation
import glob
for f in glob.glob('reports/packet_taxonomy/technical_report_*.pptx'):
    prs = Presentation(f)
    tables = sum(1 for s in prs.slides for sh in s.shapes if sh.has_table)
    assert tables > 10, f'{f} has only {tables} tables'
print('All verified')
"
```

### Final Checklist
- [x] All KSY parser tests pass
- [x] ASCII diagrams render correctly for all header types
- [x] Technical report YAML files contain field-level documentation
- [x] PPTX files contain tables with field definitions
- [x] PPTX files contain code blocks with ASCII diagrams
