# Packet Taxonomy Reporting Rules

**Created**: 2026-02-03  
**Context**: CN7000 Packet Taxonomy work tracking and status reporting

---

## 1. Document Sources for Status Reports

When generating status reports for packet taxonomy work, use **ALL** tracking documents:

| Document | Location | Content |
|----------|----------|---------|
| **WORK_ITEMS.md** | `analysis/packet_taxonomy/WORK_ITEMS.md` | Active open/deferred items, recently closed |
| **packet_taxonomy.md** | `analysis/packet_taxonomy/packet_taxonomy.md` | Master index with **full work history** (Section 5: Work List) |
| **DATAMODEL_UPDATES.md** | `analysis/packet_taxonomy/DATAMODEL_UPDATES.md` | File modification history with commit references |
| **RoCE_protocols_issues.md** | `analysis/roce_protocols/RoCE_protocols_issues.md` | RoCE datamodel issues (R-001+) |
| **ethernet_protocols_issues.md** | `analysis/ethernet_protocols/ethernet_protocols_issues.md` | Ethernet datamodel issues (E-001+) |
| **ualink_issues.md** | `analysis/ualink/ualink_issues.md` | UALink datamodel issues (UAL-001+) |

**CRITICAL**: The master work item history is in `packet_taxonomy.md` Section 5, which includes work items from W-02 onwards. Do NOT rely solely on `WORK_ITEMS.md` which only tracks active items.

---

## 2. Status Report Content Requirements

### Protocol Coverage
- Break down by subdirectories of `datamodel/protocols/`:
  - `ue/` (Ultra Ethernet) - with sublayers: transport/pds, transport/ses, transport/cms, transport/tss, link/llr, link/lldp, link/cbfc, network, physical
  - `ethernet/` - with sublayers: link, network, transport, rss
  - `roce/` - with sublayers: transport, protocols
  - `cornelis/` - with sublayers: link, network, transport, config, protocols, encapsulation
  - `ualink/` (reference only) - with sublayers: upli, transaction, datalink, physical, security
- Include file counts per subdirectory
- Document modifications made to each protocol area

### Work Item Series Organization
Organize work items by:

1. **Series Grouping** (W-02, W-03, W-04, ... W-20):
   - W-02: Protocol Support Documentation
   - W-03: Terminology Clarifications
   - W-04: Datamodel Restructuring
   - W-05: MTU and Documentation
   - W-06 to W-08: Deferred/WIP Items
   - W-09: UE Spec Clarifications
   - W-10: CMS Enumerations
   - W-11: RoCE BTH/AETH Updates
   - W-12: RoCE Cross-References
   - W-13: Ethernet Metadata/RSS
   - W-14: UALink Expansion
   - W-15 to W-16: Recent Work
   - W-17 to W-20: Open Items

2. **Modification Type**:
   - Datamodel Fixes: Field sizes, layouts, restructuring
   - Datamodel Enhancements: Cross-references, metadata, enumerations
   - Documentation: Protocol coverage, MTU values, format descriptions
   - Architecture: L2 header selection, link negotiation
   - Terminology: Naming consistency (PDP vs PDS, SES vs SE)
   - Investigation: Spec reviews, proprietary extensions

### Complete History Requirement
- **ALWAYS** include ALL work items from the beginning (W-02+)
- Do NOT limit to recent work items only
- Include status indicators: [CLOSED], [DEFERRED], [OPEN], [SPEC UPDATE], [INVESTIGATION], [CANCELLED]

### Additional Tracked Items
- **Datamodel Gaps**: D-001 to D-003 (CSR definitions, block hierarchy, interface contracts)
- **Specification Questions**: Q1-Q4 (Lightweight Interface, Tag Table, Eager Messages, RoCE WQ)

---

## 3. File Location Rules

### Local-Only Directories (NOT tracked in git)
- `analysis/` - All analysis and issue tracking documents
- `reports/` - Generated status reports
- `.sisyphus/` - Work plans, rules, session state

**No commits needed** for files in these directories.

### Git-Tracked Directories
- `earlysim/datamodel/protocols/` - KSY datamodel files
- `earlysim/docs/HAS/` - Hardware Architecture Specification
- `earlysim/datamodel/scripts/` - Validation scripts

---

## 4. PowerPoint Generation

### Tool
Use `utilities/pptx_helper` module with YAML data files.

### CLI Commands
```bash
# Validate YAML syntax
python -c "import yaml; yaml.safe_load(open('reports/packet_taxonomy/status_report.yaml'))"

# Dry-run validation
python -m utilities.pptx_helper --type progress --data reports/packet_taxonomy/status_report.yaml --dry-run

# Generate presentation
python -m utilities.pptx_helper --type progress --data reports/packet_taxonomy/status_report.yaml --output reports/packet_taxonomy/status_report.pptx

# Verify slide count
python -c "from pptx import Presentation; p = Presentation('reports/packet_taxonomy/status_report.pptx'); print(f'Slides: {len(p.slides)}')"
```

### YAML Structure
Follow `pptx_helper` progress report schema:
- `title`, `subtitle`, `presenter` (name, info)
- `sections` array with slide types:
  - `section_header`: Visual dividers
  - `status_summary`: Open/closed counts
  - `item_list`: Bullet lists with item_type (open/closed)
  - `comparison`: Two-column side-by-side

### Output Location
- YAML: `reports/packet_taxonomy/status_report.yaml`
- PPTX: `reports/packet_taxonomy/status_report.pptx`

---

## 5. KSY File Counts (as of 2026-02-03)

| Protocol | Total | Subdirectories |
|----------|-------|----------------|
| ue/ | 103 | transport (pds 14, ses 15, cms 15, tss 9, sequences 12), link (llr 9, lldp 3, cbfc 5), network 4, physical 1 |
| ualink/ | 38 | upli 8, transaction 9, datalink 12, physical 4, security 5 |
| ethernet/ | 12 | link 5, network 2, transport 2, rss 3 |
| cornelis/ | 12 | link 2, network 4, transport 2, config 2, protocols 1, encapsulation 1 |
| roce/ | 9 | transport 8, protocols 1 |
| **Total** | **174** | |

---

## Usage

When asked to generate a packet taxonomy status report:

1. Read ALL source documents listed in Section 1
2. Count KSY files by subdirectory (verify against Section 5)
3. Extract complete work item history (W-02 through W-20)
4. Organize by series AND modification type
5. Include D-001 to D-003 and Q1-Q4
6. Generate YAML following Section 4 structure
7. Validate and generate PPTX
