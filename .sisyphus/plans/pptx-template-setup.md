# PowerPoint Template Setup for AI Generation

## TL;DR

> **Quick Summary**: Create a reusable Python module that enables OpenCode/AI to generate PowerPoint presentations using the Cornelis Networks corporate template, supporting progress reports and technical presentations.
> 
> **Deliverables**:
> - `templates/template-spec.md` - Complete template documentation
> - `utilities/pptx_helper/` - Python module with helpers for presentation generation
> - Example scripts demonstrating both use cases
> 
> **Estimated Effort**: Medium (4-6 hours)
> **Parallel Execution**: YES - 2 waves
> **Critical Path**: Task 1 (spec) → Task 2 (core module) → Tasks 3-5 (features)

---

## Context

### Original Request
User wants to enable OpenCode/AI to generate PowerPoint presentations using their existing Cornelis Networks template (`templates/Standard PPT Template_Light.potx`). Primary use cases are progress reports (open/closed items, status tracking) and technical presentations. Text and images are the priority; charts/graphs are secondary.

### Interview Summary
**Key Discussions**:
- Template is a .potx file (native PowerPoint template format)
- python-pptx library is available but has a quirk with .potx content type
- 39 slide layouts available in template
- Brand colors: Purple theme (#6400B9 primary)
- Fonts: Saira family

**Research Findings**:
- Template structure fully analyzed via XML inspection
- Key layouts identified for each use case (Layout 8 for content, Layout 13 for comparisons, Layout 30 for tables)
- .potx workaround: copy to temp .pptx before loading with python-pptx

### Metis Review
**Identified Gaps** (addressed):
- Input data format: Default to YAML (consistent with codebase patterns)
- Output location: User-specified per invocation
- Image handling: Pre-generated images only (v1 scope)
- CLI vs Library: Both (library-first with thin CLI wrapper)
- Error handling: Fail fast with clear messages
- Testing: Automated verification via pytest

---

## Work Objectives

### Core Objective
Create a Python module that loads the Cornelis .potx template and provides helper functions for generating progress reports and technical presentations programmatically.

### Concrete Deliverables
1. `templates/template-spec.md` - Documentation of all layouts, colors, fonts, usage examples
2. `utilities/pptx_helper/__init__.py` - Public API exports
3. `utilities/pptx_helper/core.py` - Template loading with .potx workaround
4. `utilities/pptx_helper/layouts.py` - Layout constants and mappings
5. `utilities/pptx_helper/colors.py` - Brand color constants
6. `utilities/pptx_helper/progress_report.py` - Progress report generation helpers
7. `utilities/pptx_helper/technical.py` - Technical presentation helpers
8. `utilities/pptx_helper/cli.py` - CLI entry point
9. `tests/test_pptx_helper.py` - Automated tests

### Definition of Done
- [ ] `python -c "from utilities.pptx_helper import create_presentation; print('OK')"` succeeds
- [ ] `pytest tests/test_pptx_helper.py` passes all tests
- [ ] Generated .pptx files can be re-opened with python-pptx without errors
- [ ] Example progress report generates with correct layout and branding

### Must Have
- Template loading with .potx workaround
- At least 5 key layouts supported (title, content, 2-column, image+content, table)
- Brand colors as constants
- Progress report slide helpers (status summary, item list)
- Technical presentation helpers (content slide, image slide)
- Automated tests that verify generation

### Must NOT Have (Guardrails)
- Chart/graph generation from data (out of scope for v1)
- Video/audio embedding
- Animations or transitions
- Support for all 39 layouts (limit to 5-7 most useful)
- Template editing capabilities
- Batch generation from multiple data sources
- Excel/CSV input parsing

---

## Verification Strategy (MANDATORY)

### Test Decision
- **Infrastructure exists**: YES (pytest available in Python environment)
- **User wants tests**: YES (automated verification)
- **Framework**: pytest

### Automated Verification Approach

All acceptance criteria are executable by agents via pytest or Python commands:

```python
# Verification pattern for all tasks
def test_feature():
    # Arrange
    from utilities.pptx_helper import some_function
    
    # Act
    result = some_function(input_data)
    
    # Assert
    assert result is not None
    assert expected_condition
```

---

## Execution Strategy

### Parallel Execution Waves

```
Wave 1 (Start Immediately):
└── Task 1: Create template-spec.md (no dependencies)

Wave 2 (After Wave 1):
├── Task 2: Core module (core.py, layouts.py, colors.py)
└── Task 3: Progress report helpers (depends: Task 2)
    Task 4: Technical presentation helpers (depends: Task 2)

Wave 3 (After Wave 2):
├── Task 5: CLI wrapper
└── Task 6: Tests and documentation

Critical Path: Task 1 → Task 2 → Task 3 → Task 6
```

### Dependency Matrix

| Task | Depends On | Blocks | Can Parallelize With |
|------|------------|--------|---------------------|
| 1 | None | 2, 3, 4 | None |
| 2 | 1 | 3, 4, 5 | None |
| 3 | 2 | 6 | 4 |
| 4 | 2 | 6 | 3 |
| 5 | 2 | 6 | 3, 4 |
| 6 | 3, 4, 5 | None | None (final) |

---

## TODOs

- [x] 1. Create Template Specification Document

  **What to do**:
  - Create `templates/template-spec.md` documenting:
    - All 39 slide layouts with names, indices, and placeholder mappings
    - Brand colors with hex and RGB values
    - Font specifications
    - Quick reference table for most useful layouts
    - Usage examples for progress reports and technical presentations
  - Include Python code snippets showing how to use each layout

  **Must NOT do**:
  - Include screenshots (text-only documentation)
  - Document every placeholder in detail (focus on commonly used ones)

  **Recommended Agent Profile**:
  - **Category**: `writing`
    - Reason: Documentation-focused task requiring clear technical writing
  - **Skills**: []
    - No special skills needed - straightforward documentation

  **Parallelization**:
  - **Can Run In Parallel**: NO (first task)
  - **Parallel Group**: Wave 1 (solo)
  - **Blocks**: Tasks 2, 3, 4
  - **Blocked By**: None (can start immediately)

  **References**:
  - `templates/Standard PPT Template_Light.potx` - The template file to document
  - Analysis output from this planning session showing all 39 layouts
  - Color scheme: "New Cornelis Brand" with primary #6400B9
  - Fonts: Saira Expanded SemiBold (headings), Saira (body)

  **Acceptance Criteria**:
  ```bash
  # File exists and has content
  test -f templates/template-spec.md && test -s templates/template-spec.md
  # Contains key sections
  grep -q "## Quick Reference" templates/template-spec.md
  grep -q "## Brand Colors" templates/template-spec.md
  grep -q "#6400B9" templates/template-spec.md
  grep -q "Saira" templates/template-spec.md
  ```

  **Commit**: YES
  - Message: `docs(templates): add PowerPoint template specification`
  - Files: `templates/template-spec.md`

---

- [x] 2. Create Core Module (Template Loading, Layouts, Colors)

  **What to do**:
  - Create directory structure: `utilities/pptx_helper/`
  - Create `utilities/pptx_helper/__init__.py` with public API exports
  - Create `utilities/pptx_helper/core.py` with:
    - `load_template()` function with .potx workaround (copy to temp .pptx)
    - `create_presentation()` factory function
    - `save_presentation(prs, output_path)` helper
    - Validation that template loaded correctly (check layout count)
  - Create `utilities/pptx_helper/layouts.py` with:
    - `LAYOUTS` dict mapping names to indices
    - `get_layout(prs, name)` helper function
    - Constants for key layouts: TITLE_SLIDE, CONTENT, TWO_COLUMN, IMAGE_CONTENT, TABLE
  - Create `utilities/pptx_helper/colors.py` with:
    - `CORNELIS_COLORS` dict with RGBColor objects
    - Individual constants: PRIMARY_PURPLE, DEEP_PURPLE, BRIGHT_PURPLE, etc.
  - Follow codebase patterns: type hints, docstrings, logging

  **Must NOT do**:
  - Add dependencies beyond python-pptx
  - Support all 39 layouts (only 5-7 key ones)
  - Implement presentation generation logic (that's Tasks 3-4)

  **Recommended Agent Profile**:
  - **Category**: `unspecified-low`
    - Reason: Straightforward Python module creation following established patterns
  - **Skills**: []
    - No special skills needed

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Wave 2 (sequential after Task 1)
  - **Blocks**: Tasks 3, 4, 5
  - **Blocked By**: Task 1

  **References**:
  - `templates/template-spec.md` - Layout indices and color values (created in Task 1)
  - `templates/Standard PPT Template_Light.potx` - Template file path
  - python-pptx documentation: https://python-pptx.readthedocs.io/

  **Pattern References** (from Metis analysis):
  - Follow Python patterns: dataclasses, type hints, docstrings with Usage/Design sections
  - Use `logging.getLogger(__name__)` for output
  - Use `pathlib.Path` for file handling

  **Acceptance Criteria**:
  ```bash
  # Module imports successfully
  python3 -c "from utilities.pptx_helper import load_template, create_presentation, save_presentation; print('Core imports OK')"
  
  # Template loads and has expected layouts
  python3 -c "
from utilities.pptx_helper import load_template
prs = load_template()
assert prs is not None, 'Template failed to load'
assert len(prs.slide_layouts) == 39, f'Expected 39 layouts, got {len(prs.slide_layouts)}'
print('Template validation OK')
"
  
  # Colors are defined correctly
  python3 -c "
from utilities.pptx_helper.colors import PRIMARY_PURPLE, CORNELIS_COLORS
from pptx.dml.color import RGBColor
assert PRIMARY_PURPLE == RGBColor(100, 0, 185), 'Primary purple incorrect'
print('Colors OK')
"
  
  # Layouts are mapped
  python3 -c "
from utilities.pptx_helper.layouts import LAYOUTS, CONTENT, TWO_COLUMN
assert 'content' in LAYOUTS or CONTENT is not None
print('Layouts OK')
"
  ```

  **Commit**: YES
  - Message: `feat(pptx_helper): add core module with template loading and constants`
  - Files: `utilities/pptx_helper/__init__.py`, `utilities/pptx_helper/core.py`, `utilities/pptx_helper/layouts.py`, `utilities/pptx_helper/colors.py`

---

- [x] 3. Create Progress Report Helpers

  **What to do**:
  - Create `utilities/pptx_helper/progress_report.py` with:
    - `add_title_slide(prs, title, subtitle, presenter_name, presenter_info)` - Cover slide
    - `add_status_summary_slide(prs, title, open_count, closed_count, notes)` - Overview
    - `add_item_list_slide(prs, title, items, item_type="open"|"closed")` - Bullet list of items
    - `add_comparison_slide(prs, title, left_title, left_items, right_title, right_items)` - Plan vs Actual
    - `add_section_header(prs, title, subtitle)` - Section divider
  - Each function should:
    - Use appropriate layout from layouts.py
    - Apply brand colors where appropriate
    - Return the created slide object
    - Have comprehensive docstring with example usage
  - Add exports to `__init__.py`

  **Must NOT do**:
  - Generate charts or graphs
  - Parse data from external files (just accept Python data structures)
  - Add complex formatting beyond what placeholders support

  **Recommended Agent Profile**:
  - **Category**: `unspecified-low`
    - Reason: Straightforward Python function implementation
  - **Skills**: []
    - No special skills needed

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Task 4)
  - **Blocks**: Task 6
  - **Blocked By**: Task 2

  **References**:
  - `utilities/pptx_helper/core.py` - Template loading functions (Task 2)
  - `utilities/pptx_helper/layouts.py` - Layout constants (Task 2)
  - `utilities/pptx_helper/colors.py` - Color constants (Task 2)
  - `templates/template-spec.md` - Layout usage guidance (Task 1)

  **Acceptance Criteria**:
  ```bash
  # Functions import successfully
  python3 -c "
from utilities.pptx_helper.progress_report import (
    add_title_slide, add_status_summary_slide, add_item_list_slide,
    add_comparison_slide, add_section_header
)
print('Progress report imports OK')
"
  
  # Generate a test progress report
  python3 -c "
from utilities.pptx_helper import create_presentation, save_presentation
from utilities.pptx_helper.progress_report import add_title_slide, add_status_summary_slide, add_item_list_slide
import tempfile
import os

prs = create_presentation()
add_title_slide(prs, 'Q4 Progress Report', 'Engineering Status', 'Test User', 'Engineer')
add_status_summary_slide(prs, 'Sprint Status', open_count=5, closed_count=12, notes='On track')
add_item_list_slide(prs, 'Open Items', ['Item A', 'Item B', 'Item C'], item_type='open')

output_path = os.path.join(tempfile.gettempdir(), 'test_progress.pptx')
save_presentation(prs, output_path)

# Verify by re-opening
from pptx import Presentation
prs2 = Presentation(output_path)
assert len(prs2.slides) == 3, f'Expected 3 slides, got {len(prs2.slides)}'
print(f'Progress report generated: {output_path}')
print('Progress report generation OK')
"
  ```

  **Commit**: YES (groups with Task 4)
  - Message: `feat(pptx_helper): add progress report and technical presentation helpers`
  - Files: `utilities/pptx_helper/progress_report.py`, `utilities/pptx_helper/technical.py`

---

- [x] 4. Create Technical Presentation Helpers

  **What to do**:
  - Create `utilities/pptx_helper/technical.py` with:
    - `add_content_slide(prs, title, bullets, subtitle=None)` - Standard content
    - `add_image_slide(prs, title, image_path, caption=None)` - Image with optional text
    - `add_image_content_slide(prs, title, content, image_path)` - Split layout
    - `add_table_slide(prs, title, headers, rows, description=None)` - Data table
    - `add_two_column_slide(prs, title, left_content, right_content)` - Comparison
    - `add_code_slide(prs, title, code, language=None)` - Code block (monospace)
  - Each function should:
    - Use appropriate layout from layouts.py
    - Handle image sizing/positioning appropriately
    - Return the created slide object
    - Have comprehensive docstring with example usage
  - Add exports to `__init__.py`

  **Must NOT do**:
  - Syntax highlighting for code (just monospace font)
  - Generate diagrams from data
  - Support video/audio embedding

  **Recommended Agent Profile**:
  - **Category**: `unspecified-low`
    - Reason: Straightforward Python function implementation
  - **Skills**: []
    - No special skills needed

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Task 3)
  - **Blocks**: Task 6
  - **Blocked By**: Task 2

  **References**:
  - `utilities/pptx_helper/core.py` - Template loading functions (Task 2)
  - `utilities/pptx_helper/layouts.py` - Layout constants (Task 2)
  - `utilities/pptx_helper/colors.py` - Color constants (Task 2)
  - `templates/template-spec.md` - Layout usage guidance (Task 1)
  - python-pptx image handling: https://python-pptx.readthedocs.io/en/latest/user/placeholders-using.html

  **Acceptance Criteria**:
  ```bash
  # Functions import successfully
  python3 -c "
from utilities.pptx_helper.technical import (
    add_content_slide, add_image_slide, add_image_content_slide,
    add_table_slide, add_two_column_slide, add_code_slide
)
print('Technical presentation imports OK')
"
  
  # Generate a test technical presentation
  python3 -c "
from utilities.pptx_helper import create_presentation, save_presentation
from utilities.pptx_helper.technical import add_content_slide, add_table_slide, add_two_column_slide
import tempfile
import os

prs = create_presentation()
add_content_slide(prs, 'Architecture Overview', ['Component A', 'Component B', 'Component C'])
add_table_slide(prs, 'Performance Metrics', 
    headers=['Metric', 'Target', 'Actual'],
    rows=[['Latency', '10ms', '8ms'], ['Throughput', '1000/s', '1200/s']])
add_two_column_slide(prs, 'Before vs After',
    left_content='Old approach:\n- Slow\n- Complex',
    right_content='New approach:\n- Fast\n- Simple')

output_path = os.path.join(tempfile.gettempdir(), 'test_technical.pptx')
save_presentation(prs, output_path)

# Verify by re-opening
from pptx import Presentation
prs2 = Presentation(output_path)
assert len(prs2.slides) == 3, f'Expected 3 slides, got {len(prs2.slides)}'
print(f'Technical presentation generated: {output_path}')
print('Technical presentation generation OK')
"
  ```

  **Commit**: YES (groups with Task 3)
  - Message: `feat(pptx_helper): add progress report and technical presentation helpers`
  - Files: `utilities/pptx_helper/progress_report.py`, `utilities/pptx_helper/technical.py`

---

- [x] 5. Create CLI Wrapper

  **What to do**:
  - Create `utilities/pptx_helper/cli.py` with:
    - argparse-based CLI interface
    - `--template` option (defaults to Cornelis template)
    - `--output` option for output path
    - `--type` option: "progress" or "technical"
    - `--data` option: path to YAML file with content
    - `--dry-run` option to validate without generating
    - `--verbose` option for detailed output
  - Create example YAML files:
    - `examples/progress_report.yaml` - Sample progress report data
    - `examples/technical_presentation.yaml` - Sample technical data
  - Add `__main__.py` for `python -m utilities.pptx_helper` invocation

  **Must NOT do**:
  - Support JSON or other input formats (YAML only for v1)
  - Add complex validation beyond basic structure checks
  - Support batch generation

  **Recommended Agent Profile**:
  - **Category**: `unspecified-low`
    - Reason: Standard CLI implementation following codebase patterns
  - **Skills**: []
    - No special skills needed

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 3, 4)
  - **Blocks**: Task 6
  - **Blocked By**: Task 2

  **References**:
  - `utilities/pptx_helper/progress_report.py` - Progress report functions (Task 3)
  - `utilities/pptx_helper/technical.py` - Technical presentation functions (Task 4)
  - Codebase CLI pattern from `earlysim/docs/HAS/ETC/build_pdf.py` (argparse, --dry-run)

  **Acceptance Criteria**:
  ```bash
  # CLI help works
  python3 -m utilities.pptx_helper --help
  
  # Dry run validates without generating
  python3 -m utilities.pptx_helper --type progress --data examples/progress_report.yaml --dry-run
  
  # Generate from YAML
  python3 -m utilities.pptx_helper --type progress --data examples/progress_report.yaml --output /tmp/cli_test.pptx
  test -f /tmp/cli_test.pptx && echo "CLI generation OK"
  ```

  **Commit**: YES
  - Message: `feat(pptx_helper): add CLI interface and example YAML files`
  - Files: `utilities/pptx_helper/cli.py`, `utilities/pptx_helper/__main__.py`, `examples/progress_report.yaml`, `examples/technical_presentation.yaml`

---

- [x] 6. Create Tests and Final Documentation

  **What to do**:
  - Create `tests/test_pptx_helper.py` with pytest tests:
    - `test_template_loads()` - Verify template loading
    - `test_layouts_defined()` - Verify layout constants
    - `test_colors_defined()` - Verify color constants
    - `test_progress_report_generation()` - End-to-end progress report
    - `test_technical_presentation_generation()` - End-to-end technical
    - `test_generated_pptx_valid()` - Re-open generated files
  - Update `utilities/pptx_helper/__init__.py` with complete docstring showing:
    - Quick start example
    - Available functions
    - Link to template-spec.md
  - Verify all acceptance criteria from previous tasks pass

  **Must NOT do**:
  - Visual verification tests (all tests must be automated)
  - Performance benchmarks
  - Integration with external systems

  **Recommended Agent Profile**:
  - **Category**: `unspecified-low`
    - Reason: Standard pytest test creation
  - **Skills**: []
    - No special skills needed

  **Parallelization**:
  - **Can Run In Parallel**: NO (final task)
  - **Parallel Group**: Wave 3 (solo)
  - **Blocks**: None (final)
  - **Blocked By**: Tasks 3, 4, 5

  **References**:
  - All files created in Tasks 1-5
  - pytest documentation: https://docs.pytest.org/

  **Acceptance Criteria**:
  ```bash
  # All tests pass
  pytest tests/test_pptx_helper.py -v
  
  # Module docstring exists
  python3 -c "
from utilities import pptx_helper
assert pptx_helper.__doc__ is not None
assert 'Quick start' in pptx_helper.__doc__ or 'Example' in pptx_helper.__doc__
print('Documentation OK')
"
  ```

  **Commit**: YES
  - Message: `test(pptx_helper): add comprehensive test suite`
  - Files: `tests/test_pptx_helper.py`, `utilities/pptx_helper/__init__.py`

---

## Commit Strategy

| After Task | Message | Files | Verification |
|------------|---------|-------|--------------|
| 1 | `docs(templates): add PowerPoint template specification` | `templates/template-spec.md` | grep checks |
| 2 | `feat(pptx_helper): add core module with template loading and constants` | `utilities/pptx_helper/*.py` | python import tests |
| 3+4 | `feat(pptx_helper): add progress report and technical presentation helpers` | `progress_report.py`, `technical.py` | generation tests |
| 5 | `feat(pptx_helper): add CLI interface and example YAML files` | `cli.py`, `__main__.py`, `examples/*.yaml` | CLI tests |
| 6 | `test(pptx_helper): add comprehensive test suite` | `tests/test_pptx_helper.py` | pytest |

---

## Success Criteria

### Verification Commands
```bash
# All imports work
python3 -c "from utilities.pptx_helper import create_presentation, save_presentation"

# All tests pass
pytest tests/test_pptx_helper.py -v

# CLI works
python3 -m utilities.pptx_helper --help

# End-to-end: Generate a presentation
python3 -m utilities.pptx_helper --type progress --data examples/progress_report.yaml --output /tmp/final_test.pptx
```

### Final Checklist
- [x] Template specification document exists and is comprehensive
- [x] Core module loads template without errors
- [x] Progress report helpers generate valid slides
- [x] Technical presentation helpers generate valid slides
- [x] CLI accepts YAML input and generates output
- [x] All pytest tests pass (15/15)
- [x] Generated .pptx files can be re-opened without errors
- [x] No chart/graph generation included (scope boundary)
- [x] No dependencies added beyond python-pptx and pyyaml

**Status**: COMPLETE (verified 2026-02-03)
