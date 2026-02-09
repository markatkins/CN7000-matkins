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
