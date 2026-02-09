# TOC Integration for Technical Presentations

## TL;DR

> **Quick Summary**: Integrate the existing navigation.py module into cli.py to add Table of Contents with hyperlinks and PowerPoint sections to technical presentations.
> 
> **Deliverables**:
> - Updated `utilities/pptx_helper/cli.py` with TOC generation
> - `--toc` CLI flag to enable TOC generation
> - PowerPoint sections for navigation pane
> 
> **Estimated Effort**: Quick (30 min)
> **Parallel Execution**: NO - single task
> **Critical Path**: Task 1 only

---

## Context

### Original Request
Complete the TOC integration into the CLI. The navigation.py module is already created with all necessary functions, but not yet integrated into cli.py.

### Existing Code
- `utilities/pptx_helper/navigation.py` (250 lines) - COMPLETE with:
  - `add_internal_hyperlink()` - Creates clickable links between slides
  - `add_section()` - Adds PowerPoint sections
  - `add_toc_slide()` - Creates Table of Contents with hyperlinks
  - `insert_slide_at_position()` - Moves slides via XML manipulation

### What Needs to Change in cli.py
1. Import navigation functions
2. Add `--toc` CLI argument
3. Modify `generate_technical_presentation()` to track section_header slides
4. After all slides created, generate TOC and insert at position 1
5. Create PowerPoint sections from section headers

---

## Work Objectives

### Core Objective
Enable TOC generation with hyperlinks and PowerPoint sections in technical presentations via a `--toc` flag.

### Concrete Deliverables
- `utilities/pptx_helper/cli.py` - Updated with TOC integration

### Definition of Done
- [ ] `python -m utilities.pptx_helper --type technical --data reports/packet_taxonomy/technical_report_ue.yaml --output test.pptx --toc` succeeds
- [ ] Generated PPTX has TOC slide at position 2 (after title)
- [ ] TOC entries are clickable hyperlinks to section headers
- [ ] PowerPoint navigation pane shows sections

### Must Have
- `--toc` flag to enable TOC generation
- TOC slide with hyperlinks to all section_header slides
- PowerPoint sections for navigation pane
- Backward compatibility (no TOC if flag not provided)

### Must NOT Have (Guardrails)
- Changes to navigation.py (already complete)
- Changes to other modules
- Breaking existing functionality

---

## Verification Strategy (MANDATORY)

### Test Decision
- **Infrastructure exists**: YES
- **User wants tests**: Manual verification
- **Framework**: Manual CLI testing

### Automated Verification

**For CLI integration** (using Bash):
```bash
# Generate presentation with TOC
python -m utilities.pptx_helper --type technical \
  --data reports/packet_taxonomy/technical_report_ue.yaml \
  --output /tmp/test_toc.pptx --toc -v
# Assert: Exit code 0

# Verify file created
test -f /tmp/test_toc.pptx
# Assert: Exit code 0

# Verify --toc flag exists in help
python -m utilities.pptx_helper --help | grep -q "\-\-toc"
# Assert: Exit code 0
```

---

## TODOs

### Task 1: Integrate Navigation into CLI

**What to do**:

1. **Add imports** at top of cli.py (after existing imports):
```python
from utilities.pptx_helper.navigation import (
    add_toc_slide,
    add_section,
    insert_slide_at_position,
)
```

2. **Add `--toc` argument** in `main()` function (after `--verbose` argument):
```python
parser.add_argument(
    '--toc',
    action='store_true',
    help='Generate Table of Contents with hyperlinks and PowerPoint sections'
)
```

3. **Update function signature** of `generate_technical_presentation()`:
```python
def generate_technical_presentation(data: Dict[str, Any], output_path: Path, dry_run: bool = False, add_toc: bool = False) -> None:
```

4. **Track section headers** - Add tracking variables after `prs = create_presentation()`:
```python
# Track section headers for TOC and PowerPoint sections
section_header_slides = []  # List of (title, slide) tuples
current_section_slides = []  # Slides in current section
all_section_groups = {}  # Dict[section_name, List[Slide]] for PowerPoint sections
current_section_name = None
```

5. **Modify the section processing loop** to track slides. Replace the entire `for section in data.get('sections', []):` loop with a version that:
   - Captures the slide object returned by each add_*_slide function
   - For section_header types, records (title, slide) in section_header_slides
   - Groups slides by section for PowerPoint sections

6. **Add TOC generation** after the loop, before `save_presentation()`:
```python
# Generate TOC and sections if requested
if add_toc and section_header_slides:
    # Create TOC entries from tracked section headers
    toc_entries = [(title, slide, 0) for title, slide in section_header_slides]
    
    # Add TOC slide (will be at end initially)
    toc_slide = add_toc_slide(prs, "Table of Contents", toc_entries)
    
    # Move TOC to position 1 (after title slide)
    insert_slide_at_position(prs, toc_slide, 1)
    
    # Create PowerPoint sections for navigation pane
    if all_section_groups:
        for section_name, slides in all_section_groups.items():
            slide_ids = [s.slide_id for s in slides]
            add_section(prs, section_name, slide_ids)
    
    logger.info(f"Added TOC with {len(toc_entries)} entries and {len(all_section_groups)} sections")
```

7. **Update the call** in `main()`:
```python
generate_technical_presentation(data, parsed_args.output, parsed_args.dry_run, parsed_args.toc)
```

**Must NOT do**:
- Modify navigation.py
- Change existing slide generation logic
- Break backward compatibility

**Recommended Agent Profile**:
- **Category**: `quick`
  - Reason: Single file modification with clear requirements
- **Skills**: []
  - No special skills needed

**Parallelization**:
- **Can Run In Parallel**: NO
- **Parallel Group**: N/A (single task)
- **Blocks**: None
- **Blocked By**: None

**References**:
- `utilities/pptx_helper/cli.py:32-39` - Current imports to extend
- `utilities/pptx_helper/cli.py:117-239` - `generate_technical_presentation()` to modify
- `utilities/pptx_helper/cli.py:262-316` - `main()` argument parsing
- `utilities/pptx_helper/navigation.py:106-170` - `add_toc_slide()` function
- `utilities/pptx_helper/navigation.py:59-91` - `add_section()` function
- `utilities/pptx_helper/navigation.py:204-249` - `insert_slide_at_position()` function

**Complete Modified cli.py Code**:

The key changes are:

```python
# === CHANGE 1: Add import after line 39 ===
from utilities.pptx_helper.navigation import (
    add_toc_slide,
    add_section,
    insert_slide_at_position,
)

# === CHANGE 2: Update function signature at line 117 ===
def generate_technical_presentation(data: Dict[str, Any], output_path: Path, dry_run: bool = False, add_toc: bool = False) -> None:

# === CHANGE 3: Add tracking after line 125 (after prs = create_presentation()) ===
    # Track section headers for TOC and PowerPoint sections
    section_header_slides = []  # List of (title, slide) tuples
    all_section_groups = {}  # Dict[section_name, List[Slide]]
    current_section_name = "Introduction"  # Default section for slides before first header
    current_section_slides = []

# === CHANGE 4: Modify the section loop (lines 136-236) ===
# Each section type needs to capture the slide and add to current_section_slides
# For section_header, also record in section_header_slides and start new section group

# === CHANGE 5: Add TOC generation before save_presentation (before line 238) ===
    # Generate TOC and sections if requested
    if add_toc and section_header_slides:
        # Finalize last section group
        if current_section_name and current_section_slides:
            all_section_groups[current_section_name] = current_section_slides
        
        # Create TOC entries
        toc_entries = [(title, slide, 0) for title, slide in section_header_slides]
        
        # Add TOC slide
        toc_slide = add_toc_slide(prs, "Table of Contents", toc_entries)
        
        # Move TOC to position 1 (after title slide)
        insert_slide_at_position(prs, toc_slide, 1)
        
        # Create PowerPoint sections
        for section_name, slides in all_section_groups.items():
            slide_ids = [s.slide_id for s in slides]
            add_section(prs, section_name, slide_ids)
        
        logger.info(f"Added TOC with {len(toc_entries)} entries and {len(all_section_groups)} sections")

# === CHANGE 6: Add --toc argument after line 315 ===
    parser.add_argument(
        '--toc',
        action='store_true',
        help='Generate Table of Contents with hyperlinks and PowerPoint sections'
    )

# === CHANGE 7: Update call at line 343 ===
            generate_technical_presentation(data, parsed_args.output, parsed_args.dry_run, parsed_args.toc)
```

**Acceptance Criteria**:
```bash
# Verify --toc flag in help
python -m utilities.pptx_helper --help | grep -q "toc"
# Assert: Exit code 0

# Generate UE report with TOC
python -m utilities.pptx_helper --type technical \
  --data reports/packet_taxonomy/technical_report_ue.yaml \
  --output /tmp/test_ue_toc.pptx --toc -v
# Assert: Exit code 0, logs show "Added TOC with N entries"

# Generate RoCE report with TOC
python -m utilities.pptx_helper --type technical \
  --data reports/packet_taxonomy/technical_report_roce.yaml \
  --output /tmp/test_roce_toc.pptx --toc -v
# Assert: Exit code 0

# Verify backward compatibility (no --toc flag)
python -m utilities.pptx_helper --type technical \
  --data reports/packet_taxonomy/technical_report_ue.yaml \
  --output /tmp/test_no_toc.pptx -v
# Assert: Exit code 0, no TOC added
```

**Commit**: YES
- Message: `feat(pptx_helper): add TOC generation with hyperlinks and PowerPoint sections`
- Files: `utilities/pptx_helper/cli.py`

---

## Commit Strategy

| After Task | Message | Files | Verification |
|------------|---------|-------|--------------|
| 1 | `feat(pptx_helper): add TOC generation with hyperlinks and PowerPoint sections` | `utilities/pptx_helper/cli.py` | CLI test with --toc |

---

## Success Criteria

### Verification Commands
```bash
# Generate with TOC
python -m utilities.pptx_helper --type technical \
  --data reports/packet_taxonomy/technical_report_ue.yaml \
  --output reports/packet_taxonomy/technical_report_ue.pptx --toc -v

# Verify file exists
ls -la reports/packet_taxonomy/technical_report_ue.pptx
```

### Final Checklist
- [ ] `--toc` flag works
- [ ] TOC slide has hyperlinks
- [ ] PowerPoint sections appear in navigation pane
- [ ] Backward compatibility maintained
- [ ] UE and RoCE reports generate successfully
