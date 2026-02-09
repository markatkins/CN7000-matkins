# Technical Report Improvements - UE Protocol

## TL;DR

> **Quick Summary**: Enhance UE technical reports with enumerations, detailed field definitions, state machines, and cross-references by creating a rules file and extending ksy_parser utilities to extract rich metadata from KSY files.
> 
> **Deliverables**:
> - Rules file: `.sisyphus/rules/technical-report-generation.md`
> - Enhanced ksy_parser: `utilities/ksy_parser/` (enums.py, state_machine.py, enhanced parser.py, report.py)
> - Updated report: `reports/packet_taxonomy/technical_report_ue.yaml`
> 
> **Estimated Effort**: Medium (3-5 days)
> **Parallel Execution**: YES - 2 waves
> **Critical Path**: Task 1 (Rules) → Task 3 (Parser) → Task 5 (Report Generator) → Task 7 (Update YAML)

---

## Context

### Original Request
Refine technical reports and their workflow. Create a rules file and update utilities to support technical report generation. Ensure enumerations, wire format diagrams, field definitions, cross-references, references, and state machines are included.

### Interview Summary
**Key Discussions**:
- Enumeration organization: Per-sublayer sections (matches current structure)
- State machine detail: Full detail (states + transitions + parameters + behavior)
- UE Spec references: Include all (section, table, page numbers)
- Scope: UE only first, then apply pattern to other protocols
- Implementation: Both rules file AND utility enhancements in parallel
- Content source: KSY files directly (not analysis docs)

**Research Findings**:
- KSY files have rich metadata: `x-spec`, `x-protocol`, `x-packet`, `enums` sections
- Current ksy_parser (98 lines) only extracts basic fields, not enums or metadata
- Golden reference: `earlysim/datamodel/protocols/ue/link/cbfc/cf_update.ksy` (294 lines with full metadata)
- Target quality: `analysis/packet_taxonomy/packet_taxonomy_ue_pds.md` (872 lines)

### Metis Review
**Identified Gaps** (addressed):
- Rules file scope: Defined as technical report generation standards only
- Enumeration granularity: Consolidated tables per sublayer + inline usage
- State machine detail: Full detail with configurable limits in rules
- Cross-reference format: Both inline links and separate section
- Utility location: Extend existing `utilities/ksy_parser/`
- Output format: YAML only (current format)
- Validation: Basic consistency checks only

---

## Work Objectives

### Core Objective
Create a sustainable workflow for generating comprehensive technical reports from KSY datamodel files, starting with UE protocol.

### Concrete Deliverables
1. `.sisyphus/rules/technical-report-generation.md` - Rules file defining standards
2. `utilities/ksy_parser/enums.py` - Enumeration extraction module
3. `utilities/ksy_parser/state_machine.py` - State machine extraction module
4. `utilities/ksy_parser/parser.py` - Enhanced to extract x-spec, x-protocol metadata
5. `utilities/ksy_parser/report.py` - Enhanced to generate new section types
6. `reports/packet_taxonomy/technical_report_ue.yaml` - Updated with new content

### Definition of Done
- [ ] `python -c "from utilities.ksy_parser import enums; print('OK')"` succeeds
- [ ] `python -c "from utilities.ksy_parser import state_machine; print('OK')"` succeeds
- [ ] Rules file exists and is valid markdown
- [ ] technical_report_ue.yaml contains enumeration tables
- [ ] technical_report_ue.yaml contains state machine sections
- [ ] technical_report_ue.yaml contains x-spec references
- [ ] Existing report content is preserved (regression check)

### Must Have
- Enumeration tables for all UE sublayers (PDS, SES, CMS, TSS, LLR, CBFC)
- State machine sections with states, transitions, and behavior
- UE Spec references (section, table, page) for all content
- Cross-references between related formats
- Backward compatibility with existing YAML structure

### Must NOT Have (Guardrails)
- Modifications to KSY files (read-only extraction)
- Other protocols (RoCE, Cornelis, Ethernet, UALink) - Phase 2
- HTML/PDF generation - separate task
- KSY validation/linting - separate task
- pktgen refactoring - minimal integration only
- Manual editing requirements for KSY files

---

## Verification Strategy (MANDATORY)

### Test Decision
- **Infrastructure exists**: YES (pytest in utilities/)
- **User wants tests**: YES (TDD for utility modules)
- **Framework**: pytest

### If TDD Enabled

Each TODO follows RED-GREEN-REFACTOR:

**Task Structure:**
1. **RED**: Write failing test first
2. **GREEN**: Implement minimum code to pass
3. **REFACTOR**: Clean up while keeping green

**Test Setup Task:**
- Verify: `pytest utilities/ksy_parser/tests/ -v` runs

### Automated Verification (ALWAYS include)

**For utility modules** (using Bash pytest):
```bash
# Verify enums module
pytest utilities/ksy_parser/tests/test_enums.py -v
# Assert: All tests pass

# Verify state_machine module
pytest utilities/ksy_parser/tests/test_state_machine.py -v
# Assert: All tests pass

# Verify parser enhancements
pytest utilities/ksy_parser/tests/test_parser.py -v
# Assert: All tests pass
```

**For report generation** (using Bash):
```bash
# Verify enums in report
grep -c "PDS Type Values" reports/packet_taxonomy/technical_report_ue.yaml
# Assert: Returns >= 1

# Verify state machines in report
grep -c "state_machine" reports/packet_taxonomy/technical_report_ue.yaml
# Assert: Returns >= 10

# Verify x-spec references
grep -c "UE Spec v1.0.1" reports/packet_taxonomy/technical_report_ue.yaml
# Assert: Returns >= 20

# Verify regression (existing sections preserved)
grep -c "^- type: section_header" reports/packet_taxonomy/technical_report_ue.yaml
# Assert: Returns >= 15 (current count)
```

---

## Execution Strategy

### Parallel Execution Waves

```
Wave 1 (Start Immediately):
├── Task 1: Create rules file (no dependencies)
└── Task 2: Create test fixtures (no dependencies)

Wave 2 (After Wave 1):
├── Task 3: Enhance parser.py (depends: 2)
├── Task 4: Create enums.py (depends: 2)
└── Task 5: Create state_machine.py (depends: 2)

Wave 3 (After Wave 2):
└── Task 6: Enhance report.py (depends: 3, 4, 5)

Wave 4 (After Wave 3):
└── Task 7: Update technical_report_ue.yaml (depends: 6)

Critical Path: Task 2 → Task 3 → Task 6 → Task 7
Parallel Speedup: ~40% faster than sequential
```

### Dependency Matrix

| Task | Depends On | Blocks | Can Parallelize With |
|------|------------|--------|---------------------|
| 1 | None | 6 | 2 |
| 2 | None | 3, 4, 5 | 1 |
| 3 | 2 | 6 | 4, 5 |
| 4 | 2 | 6 | 3, 5 |
| 5 | 2 | 6 | 3, 4 |
| 6 | 3, 4, 5 | 7 | None |
| 7 | 6 | None | None (final) |

### Agent Dispatch Summary

| Wave | Tasks | Recommended Agents |
|------|-------|-------------------|
| 1 | 1, 2 | delegate_task(category="writing", ...) for rules; delegate_task(category="quick", ...) for fixtures |
| 2 | 3, 4, 5 | delegate_task(category="unspecified-low", ...) for each - parallel |
| 3 | 6 | delegate_task(category="unspecified-low", ...) |
| 4 | 7 | delegate_task(category="unspecified-high", ...) - large file update |

---

## TODOs

### Task 1: Create Rules File

**What to do**:
- Create `.sisyphus/rules/technical-report-generation.md`
- Define required sections for technical reports
- Define content extraction sources (KSY metadata fields)
- Define formatting standards (table columns, code block styles)
- Define UE Spec reference format
- Define enumeration table format
- Define state machine section format

**Must NOT do**:
- Define KSY authoring standards (separate concern)
- Define validation rules (separate task)

**Recommended Agent Profile**:
- **Category**: `writing`
  - Reason: Documentation/rules authoring task
- **Skills**: []
  - No special skills needed

**Parallelization**:
- **Can Run In Parallel**: YES
- **Parallel Group**: Wave 1 (with Task 2)
- **Blocks**: Task 6
- **Blocked By**: None (can start immediately)

**References**:
- `analysis/packet_taxonomy/packet_taxonomy_ue_pds.md` - Target quality example
- `earlysim/datamodel/protocols/ue/link/cbfc/cf_update.ksy` - KSY metadata structure
- `reports/packet_taxonomy/technical_report_ue.yaml` - Current report structure

**Acceptance Criteria**:
```bash
# Verify file exists
test -f .sisyphus/rules/technical-report-generation.md
# Assert: Exit code 0

# Verify required sections
grep -c "## Required Sections" .sisyphus/rules/technical-report-generation.md
# Assert: Returns 1

# Verify enumeration format defined
grep -c "Enumeration" .sisyphus/rules/technical-report-generation.md
# Assert: Returns >= 1

# Verify state machine format defined
grep -c "State Machine" .sisyphus/rules/technical-report-generation.md
# Assert: Returns >= 1
```

**Commit**: YES
- Message: `docs(rules): add technical report generation standards`
- Files: `.sisyphus/rules/technical-report-generation.md`

---

### Task 2: Create Test Fixtures

**What to do**:
- Create `utilities/ksy_parser/tests/` directory
- Create `utilities/ksy_parser/tests/__init__.py`
- Create `utilities/ksy_parser/tests/fixtures/` directory
- Copy sample KSY files as test fixtures:
  - `cf_update.ksy` (has enums, x-spec, x-protocol)
  - `rud_rod_request.ksy` (has field definitions)
  - A protocol state machine KSY file
- Create `utilities/ksy_parser/tests/conftest.py` with pytest fixtures

**Must NOT do**:
- Modify original KSY files
- Create complex test infrastructure

**Recommended Agent Profile**:
- **Category**: `quick`
  - Reason: Simple file creation and copying
- **Skills**: []
  - No special skills needed

**Parallelization**:
- **Can Run In Parallel**: YES
- **Parallel Group**: Wave 1 (with Task 1)
- **Blocks**: Tasks 3, 4, 5
- **Blocked By**: None (can start immediately)

**References**:
- `earlysim/datamodel/protocols/ue/link/cbfc/cf_update.ksy` - Enum example
- `earlysim/datamodel/protocols/ue/link/cbfc/protocols/vc_state_machine.ksy` - State machine example

**Acceptance Criteria**:
```bash
# Verify test directory exists
test -d utilities/ksy_parser/tests
# Assert: Exit code 0

# Verify fixtures exist
test -f utilities/ksy_parser/tests/fixtures/cf_update.ksy
# Assert: Exit code 0

# Verify conftest exists
test -f utilities/ksy_parser/tests/conftest.py
# Assert: Exit code 0

# Verify pytest can discover tests
cd utilities/ksy_parser && python -m pytest --collect-only tests/
# Assert: Exit code 0
```

**Commit**: YES
- Message: `test(ksy_parser): add test fixtures and conftest`
- Files: `utilities/ksy_parser/tests/`

---

### Task 3: Enhance parser.py to Extract Full Metadata

**What to do**:
- Add `x-spec` extraction (table, section, page, spec_version)
- Add `x-spec-ref` extraction (per-field spec references)
- Add `x-protocol` extraction (state_machine, usage_notes, related_messages)
- Add `x-packet` extraction (layer, sublayer, category, constraints)
- Add `instances` extraction (computed fields)
- Update `KsyHeader` dataclass with new fields
- Handle missing metadata gracefully (return None, don't fail)

**Must NOT do**:
- Extract enums (Task 4)
- Extract state machines (Task 5)
- Modify KSY files

**Recommended Agent Profile**:
- **Category**: `unspecified-low`
  - Reason: Straightforward Python enhancement
- **Skills**: []
  - No special skills needed

**Parallelization**:
- **Can Run In Parallel**: YES
- **Parallel Group**: Wave 2 (with Tasks 4, 5)
- **Blocks**: Task 6
- **Blocked By**: Task 2

**References**:
- `utilities/ksy_parser/parser.py:40-77` - Current parse() method to enhance
- `earlysim/datamodel/protocols/ue/link/cbfc/cf_update.ksy:60-85` - x-spec, x-packet structure
- `earlysim/datamodel/protocols/ue/link/cbfc/cf_update.ksy:274-294` - x-protocol structure

**Acceptance Criteria**:
```bash
# Create test file
cat > /tmp/test_parser.py << 'EOF'
from utilities.ksy_parser.parser import KsyParser
parser = KsyParser()
header = parser.parse('utilities/ksy_parser/tests/fixtures/cf_update.ksy')
assert header.x_spec is not None, "x_spec not extracted"
assert header.x_spec.get('table') is not None, "x_spec.table not extracted"
assert header.x_packet is not None, "x_packet not extracted"
print("PASS: parser extracts full metadata")
EOF
python /tmp/test_parser.py
# Assert: Prints "PASS: parser extracts full metadata"
```

**Commit**: YES
- Message: `feat(ksy_parser): extract x-spec, x-protocol, x-packet metadata`
- Files: `utilities/ksy_parser/parser.py`

---

### Task 4: Create enums.py Module

**What to do**:
- Create `utilities/ksy_parser/enums.py`
- Implement `extract_enums(ksy_data: dict) -> List[EnumDef]`
- Implement `EnumDef` dataclass (name, values: List[EnumValue])
- Implement `EnumValue` dataclass (value, id, doc)
- Implement `generate_enum_table(enum_def: EnumDef) -> dict` (YAML table format)
- Handle enums defined in separate files (resolve references)
- Create `utilities/ksy_parser/tests/test_enums.py`

**Must NOT do**:
- Modify KSY files
- Handle circular references (out of scope)

**Recommended Agent Profile**:
- **Category**: `unspecified-low`
  - Reason: Straightforward Python module creation
- **Skills**: []
  - No special skills needed

**Parallelization**:
- **Can Run In Parallel**: YES
- **Parallel Group**: Wave 2 (with Tasks 3, 5)
- **Blocks**: Task 6
- **Blocked By**: Task 2

**References**:
- `earlysim/datamodel/protocols/ue/link/cbfc/cf_update.ksy:268-273` - Enum definition example
- `analysis/packet_taxonomy/packet_taxonomy_ue_pds.md:88-106` - Target enum table format

**Acceptance Criteria**:
```bash
# Verify module imports
python -c "from utilities.ksy_parser.enums import extract_enums, EnumDef, generate_enum_table; print('OK')"
# Assert: Prints "OK"

# Run unit tests
pytest utilities/ksy_parser/tests/test_enums.py -v
# Assert: All tests pass

# Verify enum extraction
python -c "
import yaml
from utilities.ksy_parser.enums import extract_enums
with open('utilities/ksy_parser/tests/fixtures/cf_update.ksy') as f:
    data = yaml.safe_load(f)
enums = extract_enums(data)
assert len(enums) >= 1, 'No enums extracted'
print(f'PASS: Extracted {len(enums)} enums')
"
# Assert: Prints "PASS: Extracted N enums"
```

**Commit**: YES
- Message: `feat(ksy_parser): add enums extraction module`
- Files: `utilities/ksy_parser/enums.py`, `utilities/ksy_parser/tests/test_enums.py`

---

### Task 5: Create state_machine.py Module

**What to do**:
- Create `utilities/ksy_parser/state_machine.py`
- Implement `extract_state_machine(x_protocol: dict) -> Optional[StateMachine]`
- Implement `StateMachine` dataclass (name, states, transitions, parameters, behavior)
- Implement `State` dataclass (name, description)
- Implement `Transition` dataclass (from_state, to_state, trigger, action)
- Implement `generate_state_table(sm: StateMachine) -> dict` (YAML table format)
- Implement `generate_transition_diagram(sm: StateMachine) -> str` (ASCII art)
- Create `utilities/ksy_parser/tests/test_state_machine.py`

**Must NOT do**:
- Modify KSY files
- Generate PlantUML (ASCII only)

**Recommended Agent Profile**:
- **Category**: `unspecified-low`
  - Reason: Straightforward Python module creation
- **Skills**: []
  - No special skills needed

**Parallelization**:
- **Can Run In Parallel**: YES
- **Parallel Group**: Wave 2 (with Tasks 3, 4)
- **Blocks**: Task 6
- **Blocked By**: Task 2

**References**:
- `earlysim/datamodel/protocols/ue/link/cbfc/protocols/vc_state_machine.ksy` - State machine KSY example
- `analysis/packet_taxonomy/packet_taxonomy_ue_cms_tss.md:240-258` - Target state machine format

**Acceptance Criteria**:
```bash
# Verify module imports
python -c "from utilities.ksy_parser.state_machine import extract_state_machine, StateMachine, generate_state_table; print('OK')"
# Assert: Prints "OK"

# Run unit tests
pytest utilities/ksy_parser/tests/test_state_machine.py -v
# Assert: All tests pass
```

**Commit**: YES
- Message: `feat(ksy_parser): add state machine extraction module`
- Files: `utilities/ksy_parser/state_machine.py`, `utilities/ksy_parser/tests/test_state_machine.py`

---

### Task 6: Enhance report.py to Generate New Section Types

**What to do**:
- Import enums and state_machine modules
- Add `generate_enum_section(header: KsyHeader) -> List[dict]`
- Add `generate_state_machine_section(header: KsyHeader) -> List[dict]`
- Add `generate_spec_reference(header: KsyHeader) -> str`
- Add `generate_cross_references(header: KsyHeader) -> List[dict]`
- Update `generate_header_section()` to include new content
- Follow rules file standards for formatting
- Create `utilities/ksy_parser/tests/test_report.py`

**Must NOT do**:
- Generate HTML/PDF
- Modify existing section types (additive only)

**Recommended Agent Profile**:
- **Category**: `unspecified-low`
  - Reason: Python enhancement with clear patterns
- **Skills**: []
  - No special skills needed

**Parallelization**:
- **Can Run In Parallel**: NO
- **Parallel Group**: Wave 3 (sequential)
- **Blocks**: Task 7
- **Blocked By**: Tasks 3, 4, 5

**References**:
- `utilities/ksy_parser/report.py:9-43` - Current generate_header_section()
- `.sisyphus/rules/technical-report-generation.md` - Formatting standards (from Task 1)
- `reports/packet_taxonomy/technical_report_ue.yaml` - Target output format

**Acceptance Criteria**:
```bash
# Verify new functions exist
python -c "
from utilities.ksy_parser.report import generate_enum_section, generate_state_machine_section, generate_spec_reference
print('OK')
"
# Assert: Prints "OK"

# Run unit tests
pytest utilities/ksy_parser/tests/test_report.py -v
# Assert: All tests pass

# Verify output format
python -c "
from utilities.ksy_parser.parser import KsyParser
from utilities.ksy_parser.report import generate_header_section
parser = KsyParser()
header = parser.parse('utilities/ksy_parser/tests/fixtures/cf_update.ksy')
sections = generate_header_section(header)
types = [s.get('type') for s in sections]
assert 'table' in types, 'No table sections'
print(f'PASS: Generated {len(sections)} sections')
"
# Assert: Prints "PASS: Generated N sections"
```

**Commit**: YES
- Message: `feat(ksy_parser): add enum and state machine report generation`
- Files: `utilities/ksy_parser/report.py`, `utilities/ksy_parser/tests/test_report.py`

---

### Task 7: Update technical_report_ue.yaml with New Content

**What to do**:
- Backup existing file
- Parse all UE KSY files from `earlysim/datamodel/protocols/ue/`
- Generate enumeration sections for each sublayer (PDS, SES, CMS, TSS, LLR, CBFC)
- Generate state machine sections for protocol files
- Add UE Spec references to existing sections
- Add cross-reference sections
- Preserve existing content structure
- Validate output YAML is valid

**Must NOT do**:
- Remove existing content
- Change existing section order
- Process non-UE protocols

**Recommended Agent Profile**:
- **Category**: `unspecified-high`
  - Reason: Large file update requiring careful integration
- **Skills**: []
  - No special skills needed

**Parallelization**:
- **Can Run In Parallel**: NO
- **Parallel Group**: Wave 4 (final)
- **Blocks**: None (final task)
- **Blocked By**: Task 6

**References**:
- `reports/packet_taxonomy/technical_report_ue.yaml` - Current report (2060 lines)
- `earlysim/datamodel/protocols/ue/` - All UE KSY files
- `.sisyphus/rules/technical-report-generation.md` - Formatting standards

**Acceptance Criteria**:
```bash
# Verify YAML is valid
python -c "import yaml; yaml.safe_load(open('reports/packet_taxonomy/technical_report_ue.yaml')); print('YAML valid')"
# Assert: Prints "YAML valid"

# Verify enums added
grep -c "PDS Type Values\|NACK Codes\|SES Request Opcodes" reports/packet_taxonomy/technical_report_ue.yaml
# Assert: Returns >= 3

# Verify state machines added
grep -c "State Machine\|States\|Transitions" reports/packet_taxonomy/technical_report_ue.yaml
# Assert: Returns >= 10

# Verify UE Spec references
grep -c "UE Spec v1.0.1" reports/packet_taxonomy/technical_report_ue.yaml
# Assert: Returns >= 20

# Verify regression (existing sections preserved)
grep -c "^- type: section_header" reports/packet_taxonomy/technical_report_ue.yaml
# Assert: Returns >= 15

# Verify file size reasonable (< 10MB)
test $(stat -f%z reports/packet_taxonomy/technical_report_ue.yaml 2>/dev/null || stat -c%s reports/packet_taxonomy/technical_report_ue.yaml) -lt 10000000
# Assert: Exit code 0
```

**Commit**: YES
- Message: `feat(reports): add enumerations, state machines, and spec refs to UE technical report`
- Files: `reports/packet_taxonomy/technical_report_ue.yaml`

---

## Commit Strategy

| After Task | Message | Files | Verification |
|------------|---------|-------|--------------|
| 1 | `docs(rules): add technical report generation standards` | `.sisyphus/rules/technical-report-generation.md` | File exists |
| 2 | `test(ksy_parser): add test fixtures and conftest` | `utilities/ksy_parser/tests/` | pytest --collect-only |
| 3 | `feat(ksy_parser): extract x-spec, x-protocol, x-packet metadata` | `utilities/ksy_parser/parser.py` | pytest test_parser.py |
| 4 | `feat(ksy_parser): add enums extraction module` | `utilities/ksy_parser/enums.py`, tests | pytest test_enums.py |
| 5 | `feat(ksy_parser): add state machine extraction module` | `utilities/ksy_parser/state_machine.py`, tests | pytest test_state_machine.py |
| 6 | `feat(ksy_parser): add enum and state machine report generation` | `utilities/ksy_parser/report.py`, tests | pytest test_report.py |
| 7 | `feat(reports): add enumerations, state machines, and spec refs to UE technical report` | `reports/packet_taxonomy/technical_report_ue.yaml` | grep validation |

---

## Success Criteria

### Verification Commands
```bash
# All tests pass
pytest utilities/ksy_parser/tests/ -v

# Report is valid YAML
python -c "import yaml; yaml.safe_load(open('reports/packet_taxonomy/technical_report_ue.yaml'))"

# Enums present
grep -c "PDS Type Values" reports/packet_taxonomy/technical_report_ue.yaml | xargs test 1 -le

# State machines present
grep -c "state_machine" reports/packet_taxonomy/technical_report_ue.yaml | xargs test 10 -le

# Spec references present
grep -c "UE Spec v1.0.1" reports/packet_taxonomy/technical_report_ue.yaml | xargs test 20 -le
```

### Final Checklist
- [ ] All "Must Have" present
- [ ] All "Must NOT Have" absent
- [ ] All tests pass
- [ ] YAML is valid
- [ ] Existing content preserved
- [ ] Rules file complete
