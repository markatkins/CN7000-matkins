# CN7000

Top-level workspace for the Cornelis Networks CN7000 high-performance networking platform.

## Product Overview

CN7000 is Cornelis Networks' next-generation networking platform targeting HPC and AI
workloads. The platform comprises the CN7000 NIC (codename PMR / Prism River, 1.6 Tbps)
and the LNR (Lightning River) switch ASIC, supporting Ultra Ethernet (UE), RoCE, and
standard Ethernet protocols.

This repository is the top-level workspace aggregating hardware design, functional
simulation, architecture analysis, and documentation.

## Repository Structure

| Directory | Description | Entry Point |
|-----------|-------------|-------------|
| `earlysim/` | CN7000 functional simulator (NIC + LNR switch) with QEMU-based device emulation, libfabric integration, SONiC management, and end-to-end cluster simulation. **Git submodule.** | [earlysim/README.md](earlysim/README.md) |
| `hlc/` | Hill Creek ASIC (HLC) hardware design and verification. **Git submodule.** | [hlc/README.md](hlc/README.md) |
| `analysis/` | Architecture analysis covering packet taxonomy, state machines, protocol reviews (UALink, RoCE, Ethernet, UE CMS), and requirements gap analysis. | [analysis/](analysis/) |
| `solutions/` | CN7000 solution and feature matrix documentation pipeline. Generates PPTX, DOCX, and PDF from markdown source using pandoc with custom filters. | [solutions/solutions.md](solutions/solutions.md) |
| `utilities/` | Shared Python tools: `ksy_parser` (Kaitai Struct YAML parser with report generation) and `pptx_helper` (PowerPoint generation from YAML data). | [utilities/](utilities/) |
| `reports/` | Generated technical reports (packet taxonomy protocol reports). | [reports/](reports/) |
| `templates/` | Cornelis-branded document templates (PowerPoint, specification). | [templates/](templates/) |
| `examples/` | Example YAML data files for report and presentation generation. | [examples/](examples/) |
| `tests/` | Top-level tests for shared utilities. | [tests/](tests/) |
| `prompts/` | AI prompt templates for architecture review workflows. | [prompts/](prompts/) |
| `AGENTS/` | AI assistant configuration and entry points. | [AGENTS/start_here.md](AGENTS/start_here.md) |

## Submodules

This repository uses git submodules for the two primary development workstreams.

### earlysim

Full-stack functional simulator encompassing QEMU device models, libfabric provider,
kernel driver, RISC-V Collectives Engine firmware, LNR switch simulator, and
SONiC/OpenBMC management infrastructure. Contains build system, data models, tests,
and cluster launch scripts.

See [earlysim/README.md](earlysim/README.md) for full documentation.

### hlc

Hill Creek ASIC (HLC) hardware design and verification.

See [hlc/README.md](hlc/README.md).

### Initializing Submodules

After cloning, initialize and fetch all submodule content:

```bash
git submodule update --init --recursive
```

## Key Technologies

**Languages and build:**

- CMake 3.20+
- Python 3.11+ (uv-managed)
- C11 / C++17
- SystemVerilog (IEEE 1800-2017)
- RISC-V

**Frameworks and tools:**

- QEMU
- libfabric
- Kaitai Struct
- SystemRDL
- SONiC
- OpenBMC
- pandoc

## Getting Started

- **Simulator quick start**: See [earlysim/README.md](earlysim/README.md) for
  dependencies, build instructions, and cluster launch.
- **Solutions document pipeline**: Run [solutions/build.sh](solutions/build.sh) to
  generate PPTX/DOCX/PDF solution documents from markdown source.
- **Hill Creek ASIC**: See [hlc/README.md](hlc/README.md) for HLC hardware design
  entry points.

## License

Proprietary — Cornelis Networks
