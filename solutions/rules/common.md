# Common Rules (All Formats)

These rules apply to all output formats (Markdown, DOCX, PPTX, PDF).

## Scale Specifications

| Scale | Max Endpoints | Per Rail (8 rails) |
|-------|---------------|-------------------|
| Small-Medium | ≤10K | ≤1.25K |
| Large | 10K-93K | 1.25K-11.6K |
| Hyperscalar | 100K-1.44M | 12.5K-180K |

- Always indicate max endpoints per rail assuming 8 rails
- Example: 1.44M/8 = 180K per rail

## Topology Rules

| Scale | Supported Topologies |
|-------|---------------------|
| Small-Medium | Fat-Tree or Fat-Tree Rail |
| Large | Fat-Tree Rail |
| Hyperscalar | Fat-Tree Rail |

- Megafly and Dragonfly are NOT supported for AI workloads (HPC only)

## Scale-Up Design Constraints

- **Cornelis does not currently have a scale-up NIC or embedded accelerator HFI**
- Scale-Up solutions assume third-party endpoint vendors connecting to Cornelis switches
- Scale-Up interoperability is **Homogeneous only** (no heterogeneous/island mode)
- This constraint applies to both Scale-Up AI (UALink) and Scale-Up HPC (UE/ULN)

## Feature Naming Conventions

| Feature | Correct Usage | Do NOT Use |
|---------|--------------|------------|
| FGAR | FGAR (do not expand in tables) | "Fine-Grained Adaptive Routing" |
| ECAR | Entropy Controlled Adaptive Routing | "Enhanced Congestion" |
| Dynamic Route Recovery | Dynamic Route Recovery | "Fast Route Recovery", "dynamic rerouting" |
| NSCC | NSCC (supports lossless and lossy) | "RTT-based" |
| RCCC | RCCC | "receiver credit control" |
| Collective Accel | Collective Accel (homogeneous/island only) | "RISC-V line-rate reduce" |

## Protocol/Feature Support Notation

- **ECN**: Include RoCE as supported alongside UE and Ethernet
- **Interoperability Mode**: For Heterogeneous, add "(island)" in parentheses

## Glossary Requirements

1. All acronyms used in tables MUST be defined in the glossary
2. Glossary entries must be alphabetically ordered
3. Format: `**ACRONYM** - Full expansion and brief description`

### Required Glossary Entries

All documents must include definitions for:
- bidi, CBFC, CMS, CSIG/CSIG+, ECAR, ECN, FGAR, LLR, NSCC, OPA
- PDS, RCCC, RMA, ROD, RoCE, RUD, RUDI, SDR, SES, UALink
- UE, UE+, ULN, UUD

## Toolchain Requirements

| Tool | Tested Version | Known Issues |
|------|---------------|--------------|
| Pandoc | 3.1.3 | `pandoc.Caption()` API unavailable; `--pdf-engine=typst` broken (use two-step process) |
| Typst | 0.14.2 | None known |
| Python | 3.x | Required for `docx-postprocess.py` and `pptx-postprocess.py` |

### Pandoc 3.1.3 Limitations
- `pandoc.Caption()` constructor does not exist — Lua filters must use table-based caption format: `{long = {...}, short = nil}`
- `--pdf-engine=typst` fails — must use two-step process: `pandoc → .typ` then `typst compile`
- PPTX layout selection is not exposed to Lua filters — layout remapping requires Python post-processing
