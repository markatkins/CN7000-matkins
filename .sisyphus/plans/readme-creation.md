# Create Root README.md for CN7000 Repository

## TL;DR

> **Quick Summary**: Create a concise, navigation-hub-style README.md at the CN7000 repository root that orients internal Cornelis Networks engineers to the repo structure, provides brief product context, and links to detailed documentation in submodules.
> 
> **Deliverables**:
> - `/home/matkins/CN7000/README.md` — New file (~100-140 lines)
> 
> **Estimated Effort**: Quick
> **Parallel Execution**: NO — single task
> **Critical Path**: Task 1 (only task)

---

## Context

### Original Request
Create an informative README.md for the main CN7000 repository, which currently has no root README.

### Interview Summary
**Key Discussions**:
- **Audience**: Internal Cornelis Networks engineers
- **Detail level**: Concise overview + links (~100-150 lines), not duplicating earlysim/README.md
- **Product context**: Include brief CN7000 product overview (NIC + switch for HPC/AI, UE protocol)
- **Scope**: Cover ALL top-level directories (earlysim, hlc, analysis, reports, solutions, utilities, templates, etc.)

**Research Findings**:
- No root README.md currently exists
- `earlysim/README.md` is comprehensive (621 lines with architecture diagrams, tutorials, build instructions)
- `hlc/README.md` is minimal (3 lines: "Hill Creek ASIC (HLC)")
- `AGENTS/start_here.md` exists as AI agent entry point (18 lines)
- `.gitmodules` defines `earlysim` and `hlc` as git submodules pointing to `cornelisnetworks/earlysim.git` and `cornelisnetworks/hlc.git`
- Top-level directories verified: `AGENTS/`, `analysis/`, `earlysim/`, `examples/`, `hlc/`, `prompts/`, `reports/`, `solutions/`, `templates/`, `tests/`, `utilities/`
- License: Proprietary — Cornelis Networks (from earlysim/README.md)
- `solutions/` is a complete document generation pipeline (Markdown → PPTX/DOCX/PDF via pandoc with custom Lua filters)
- `utilities/` contains two Python packages: `pptx_helper` and `ksy_parser`
- `analysis/` has 7 subdirectories covering packet taxonomy, state machines, UALink, RoCE, Ethernet, UE CMS, and requirements

### Metis Review
**Identified Gaps** (addressed):
- `.sisyphus/` and `sisyphus.backup/` directories: Resolved — omit from README (tooling artifacts, not project content)
- Empty `reports/` directory: Resolved — include with note "Generated technical reports (packet taxonomy)"
- `prompts/` directory: Resolved — include briefly as "AI prompt templates for architecture review"
- Product terminology: Resolved — use CN7000 as primary name, mention PMR/LNR codenames parenthetically
- Prerequisites section: Resolved — defer entirely to submodule READMEs (link only)
- `AGENTS/` directory: Resolved — include briefly, relevant for engineers using AI tools

---

## Work Objectives

### Core Objective
Create a single README.md file at the repository root that serves as a navigation hub for internal engineers, providing product context and directory-level orientation with links to detailed documentation.

### Concrete Deliverables
- `/home/matkins/CN7000/README.md` — New markdown file, 80-150 lines

### Definition of Done
- [x] File exists at `/home/matkins/CN7000/README.md`
- [x] Line count between 80 and 150
- [x] Starts with H1 title
- [x] All top-level directories mentioned
- [x] Links to `earlysim/README.md` for simulator details
- [x] No ASCII architecture diagrams (box-drawing characters)
- [x] No build instructions (cmake, dnf install, apt install)
- [x] No content duplicated from earlysim/README.md
- [x] All relative links point to existing files/directories
- [x] License section present

### Must Have
- H1 title with repository name
- Brief product overview (CN7000 NIC + LNR switch, HPC/AI, Ultra Ethernet)
- Directory structure table covering ALL top-level directories
- Submodule callout (earlysim and hlc are git submodules)
- Key technologies summary
- Links to detailed documentation in submodules
- License footer (Proprietary — Cornelis Networks)

### Must NOT Have (Guardrails)
- ASCII architecture diagrams (those belong in earlysim/README.md)
- Build instructions, dependency lists, or installation steps
- Duplicated content from earlysim/README.md
- More than 2 sentences about any single directory
- Technology deep-dives (don't explain UE protocol, Kaitai Struct, etc.)
- HTML tags in markdown
- Descriptions of hlc/ beyond what its own README says
- References to `.sisyphus/` or `sisyphus.backup/` directories

---

## Verification Strategy (MANDATORY)

> **UNIVERSAL RULE: ZERO HUMAN INTERVENTION**
>
> ALL verification is executed by the agent using tools. No human action permitted.

### Test Decision
- **Infrastructure exists**: N/A (documentation task)
- **Automated tests**: None (documentation)
- **Framework**: N/A

### Agent-Executed QA Scenarios (MANDATORY)

All verification is command-based, executed by the implementing agent.

---

## Execution Strategy

### Single Task — No Parallelization Needed

This is a single-file creation task. One task, one wave.

```
Wave 1 (Start Immediately):
└── Task 1: Create README.md
```

---

## TODOs

- [x] 1. Create `/home/matkins/CN7000/README.md`

  **What to do**:
  - Create a new markdown file at the repository root
  - Structure with these sections (in order):
    1. **H1 Title**: `# CN7000` (or `# CN7000 — Cornelis Networks Architecture Repository`)
    2. **Product Overview** (2-3 sentences): CN7000 is Cornelis Networks' next-generation networking platform for HPC and AI workloads. Mention the CN7000 NIC (codename PMR/Prism River, 1.6 Tbps) and LNR (Lightning River) switch. Mention Ultra Ethernet (UE) protocol support. Note this repo is the top-level workspace aggregating hardware design, functional simulation, analysis, and documentation.
    3. **Repository Structure** (markdown table): One row per top-level directory with columns: Directory, Description, Entry Point (link). Cover: `earlysim/`, `hlc/`, `analysis/`, `solutions/`, `utilities/`, `reports/`, `templates/`, `examples/`, `tests/`, `prompts/`, `AGENTS/`
    4. **Submodules**: Note that `earlysim` and `hlc` are git submodules. Include the `git submodule update --init --recursive` command for cloning.
    5. **Key Technologies** (bullet list): CMake 3.20+, Python 3.11+ (uv-managed), C11/C++17, SystemVerilog, RISC-V, QEMU, libfabric, Kaitai Struct, SystemRDL, SONiC, OpenBMC, pandoc
    6. **Getting Started**: 2-3 bullet points linking to earlysim/README.md for simulator quick start, solutions/build.sh for solutions pipeline, hlc/README.md for HLC
    7. **License**: "Proprietary — Cornelis Networks"
  - Use verified directory descriptions:
    - `earlysim/` — CN7000 functional simulator (NIC + LNR switch) with QEMU-based device emulation, libfabric integration, SONiC management, and end-to-end cluster simulation. **Git submodule.**
    - `hlc/` — Hill Creek ASIC (HLC) hardware design and verification. **Git submodule.**
    - `analysis/` — Architecture analysis covering packet taxonomy, state machines, protocol reviews (UALink, RoCE, Ethernet, UE CMS), and requirements gap analysis.
    - `solutions/` — CN7000 solution and feature matrix documentation pipeline. Generates PPTX, DOCX, and PDF from markdown source using pandoc with custom filters.
    - `utilities/` — Shared Python tools: `ksy_parser` (Kaitai Struct YAML parser with report generation) and `pptx_helper` (PowerPoint generation from YAML data).
    - `reports/` — Generated technical reports (packet taxonomy protocol reports).
    - `templates/` — Cornelis-branded document templates (PowerPoint, specification).
    - `examples/` — Example YAML data files for report and presentation generation.
    - `tests/` — Top-level tests for shared utilities.
    - `prompts/` — AI prompt templates for architecture review workflows.
    - `AGENTS/` — AI assistant configuration and entry points.

  **Must NOT do**:
  - Do NOT include ASCII box-drawing architecture diagrams
  - Do NOT include build instructions (cmake commands, dnf/apt install)
  - Do NOT duplicate content from earlysim/README.md
  - Do NOT describe hlc/ beyond "Hill Creek ASIC (HLC) hardware design and verification"
  - Do NOT reference `.sisyphus/` or `sisyphus.backup/` directories
  - Do NOT use HTML tags
  - Do NOT exceed 150 lines

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Single-file documentation creation with clear specifications. No complex logic or multi-file coordination.
  - **Skills**: []
    - No specialized skills needed — this is a markdown file creation task.
  - **Skills Evaluated but Omitted**:
    - `frontend-ui-ux`: No UI/UX work involved
    - `git-master`: No git operations needed (file creation only, commit separately if requested)

  **Parallelization**:
  - **Can Run In Parallel**: NO (single task)
  - **Parallel Group**: N/A
  - **Blocks**: Nothing
  - **Blocked By**: None (can start immediately)

  **References** (CRITICAL):

  **Pattern References** (existing files to follow):
  - `AGENTS/start_here.md` — Terse, navigational style to emulate for the README
  - `earlysim/README.md` — Comprehensive README to link to (NOT duplicate)
  - `hlc/README.md` — Minimal README showing what hlc/ contains

  **Content References** (verified facts to use):
  - `.gitmodules` — Confirms earlysim and hlc are submodules pointing to `cornelisnetworks/earlysim.git` and `cornelisnetworks/hlc.git`
  - `solutions/solutions.md` — CN7000 solution/feature matrices content (confirms solutions/ purpose)
  - `utilities/ksy_parser/parser.py` — Confirms ksy_parser is a Kaitai Struct YAML parser
  - `earlysim/README.md:1-5` — Product description: "A comprehensive functional simulator for the Cornelis Networks CN7000 NIC and LNR switch"
  - `earlysim/README.md:616` — License: "Proprietary - Cornelis Networks"

  **WHY Each Reference Matters**:
  - `AGENTS/start_here.md`: Shows the terse, navigational tone appropriate for a root-level orientation document
  - `.gitmodules`: Source of truth for submodule URLs — ensures accurate submodule section
  - `earlysim/README.md`: The detailed README we're linking to — must not duplicate its content
  - `solutions/solutions.md`: Confirms the solutions directory contains CN7000 feature matrices, not generic docs

  **Acceptance Criteria**:

  > **AGENT-EXECUTABLE VERIFICATION ONLY** — No human action permitted.

  **Agent-Executed QA Scenarios (MANDATORY):**

  ```
  Scenario: README.md exists at correct location
    Tool: Bash
    Preconditions: Task 1 completed
    Steps:
      1. test -f /home/matkins/CN7000/README.md
      2. Assert: exit code is 0
    Expected Result: File exists
    Evidence: Command output captured

  Scenario: Line count within bounds (80-150)
    Tool: Bash
    Preconditions: README.md exists
    Steps:
      1. wc -l /home/matkins/CN7000/README.md
      2. Assert: line count >= 80 AND <= 150
    Expected Result: Line count in range
    Evidence: wc output captured

  Scenario: Starts with H1 title
    Tool: Bash
    Preconditions: README.md exists
    Steps:
      1. head -1 /home/matkins/CN7000/README.md
      2. Assert: first line starts with "# "
    Expected Result: H1 header present
    Evidence: head output captured

  Scenario: All required directories mentioned
    Tool: Bash
    Preconditions: README.md exists
    Steps:
      1. For each directory in [earlysim, hlc, analysis, solutions, utilities, templates, examples, tests, prompts, AGENTS, reports]:
         grep -q "$dir" /home/matkins/CN7000/README.md
      2. Assert: all greps return exit code 0
    Expected Result: All 11 directories mentioned
    Evidence: grep results captured

  Scenario: Links to earlysim README
    Tool: Bash
    Preconditions: README.md exists
    Steps:
      1. grep -q "earlysim/README.md" /home/matkins/CN7000/README.md
      2. Assert: exit code is 0
    Expected Result: Link to earlysim/README.md present
    Evidence: grep output captured

  Scenario: No ASCII architecture diagrams
    Tool: Bash
    Preconditions: README.md exists
    Steps:
      1. grep -c "┌\|└\|│\|├" /home/matkins/CN7000/README.md
      2. Assert: count is 0
    Expected Result: No box-drawing characters
    Evidence: grep count captured

  Scenario: No build instructions
    Tool: Bash
    Preconditions: README.md exists
    Steps:
      1. grep -c "cmake --build\|cmake \.\.\|dnf install\|apt install\|sudo dnf\|sudo apt" /home/matkins/CN7000/README.md
      2. Assert: count is 0
    Expected Result: No build/install commands
    Evidence: grep count captured

  Scenario: License section present
    Tool: Bash
    Preconditions: README.md exists
    Steps:
      1. grep -qi "proprietary\|license" /home/matkins/CN7000/README.md
      2. Assert: exit code is 0
    Expected Result: License mentioned
    Evidence: grep output captured

  Scenario: All relative links valid
    Tool: Bash
    Preconditions: README.md exists
    Steps:
      1. Extract all relative links from markdown: grep -oP '\]\((?!http)([^)]+)\)' README.md
      2. For each link, verify: test -e /home/matkins/CN7000/$link
      3. Assert: all links resolve to existing files/directories
    Expected Result: Zero broken links
    Evidence: Link validation output captured

  Scenario: Submodule instructions present
    Tool: Bash
    Preconditions: README.md exists
    Steps:
      1. grep -q "git submodule" /home/matkins/CN7000/README.md
      2. Assert: exit code is 0
    Expected Result: Submodule clone instructions present
    Evidence: grep output captured
  ```

  **Evidence to Capture:**
  - [x] All bash verification outputs in terminal
  - [x] Each evidence captured as command output (no screenshots needed for text file)

  **Commit**: YES
  - Message: `docs: add root README.md with repository overview and navigation`
  - Files: `README.md`
  - Pre-commit: Acceptance criteria verification commands above

---

## Commit Strategy

| After Task | Message | Files | Verification |
|------------|---------|-------|--------------|
| 1 | `docs: add root README.md with repository overview and navigation` | `README.md` | All 10 QA scenarios pass |

---

## Success Criteria

### Verification Commands
```bash
# File exists
test -f /home/matkins/CN7000/README.md && echo "PASS" || echo "FAIL"

# Line count 80-150
lines=$(wc -l < /home/matkins/CN7000/README.md); [ "$lines" -ge 80 ] && [ "$lines" -le 150 ] && echo "PASS: $lines lines" || echo "FAIL: $lines lines"

# Starts with H1
head -1 /home/matkins/CN7000/README.md | grep -q "^# " && echo "PASS" || echo "FAIL"

# No ASCII diagrams
grep -c '┌\|└\|│\|├' /home/matkins/CN7000/README.md | grep -q "^0$" && echo "PASS" || echo "FAIL"

# No build instructions
grep -c 'cmake --build\|cmake \.\.\|dnf install\|apt install' /home/matkins/CN7000/README.md | grep -q "^0$" && echo "PASS" || echo "FAIL"

# All directories mentioned
for d in earlysim hlc analysis solutions utilities templates examples tests prompts AGENTS reports; do grep -q "$d" /home/matkins/CN7000/README.md && echo "PASS: $d" || echo "FAIL: $d"; done

# License present
grep -qi "proprietary" /home/matkins/CN7000/README.md && echo "PASS" || echo "FAIL"
```

### Final Checklist
- [x] All "Must Have" sections present
- [x] All "Must NOT Have" items absent
- [x] Line count within 80-150 range
- [x] All relative links valid
- [x] All 10 QA scenarios pass
