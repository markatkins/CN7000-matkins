# Work Item and Issue Tracking Rules

**Created**: 2026-02-03  
**Context**: CN7000 Packet Taxonomy work tracking conventions

---

## 1. Work Item ID Format

### Series-Based IDs (W-XX-YYY)
Use for related work items that form a logical group:

```
W-XX-YYY
│  │  └── Item number within series (001-999)
│  └───── Series number (01-99)
└──────── Work item prefix
```

**Examples**:
- W-09-003: UE Spec Clarifications series, item 3
- W-10-014: CMS Enumerations series, item 14
- W-14-007: UALink Expansion series, item 7

### Standalone IDs (W-XX)
Use for single items or new initiatives that may spawn a series:

```
W-XX
│  └── Item number (01-99)
└───── Work item prefix
```

**Examples**:
- W-15: UE+ to CN7000 PPT comparison
- W-16: L2 Header Selection Datamodel
- W-17: VLAN Protocol Coverage Verification

### When to Create a New Series vs Add to Existing

| Situation | Action |
|-----------|--------|
| New review of a protocol area | Create new series (W-XX) |
| Follow-on work from existing review | Add to existing series (W-XX-YYY) |
| Single standalone task | Use standalone ID (W-XX) |
| Task spawns multiple sub-items | Convert to series (W-XX-001, W-XX-002, ...) |

### Current Series Assignments

| Series | Description | Date Range |
|--------|-------------|------------|
| W-02 | Protocol Support Documentation | 2026-01-08 |
| W-03 | Terminology Clarifications | 2026-01-08 |
| W-04 | Datamodel Restructuring | 2026-01-10 |
| W-05 | MTU and Documentation | 2026-01-10 |
| W-06 | UFH Entropy | 2026-01-20 |
| W-07 | Datamodel Fixes | 2026-01-22 |
| W-08 | WIP Specs | 2026-01-23 |
| W-09 | UE Spec Clarifications | 2026-01-23 to 2026-01-26 |
| W-10 | CMS Enumerations | 2026-01-27 |
| W-11 | RoCE BTH/AETH Updates | 2026-01-27 |
| W-12 | RoCE Cross-References | 2026-01-27 to 2026-01-28 |
| W-13 | Ethernet Metadata/RSS | 2026-01-28 |
| W-14 | UALink Expansion | 2026-01-29 to 2026-01-30 |
| W-15 | PPT Comparison / UFH Reorganization | 2026-02-02 |
| W-16 | L2 Header Selection Datamodel | 2026-02-03 |
| W-17 | VLAN Protocol Coverage | 2026-02-03 |
| W-18 | VXLAN Protocol Coverage | 2026-02-03 |
| W-19 | UFH Rules for L2 Selection | 2026-02-03 |
| W-20 | Link Negotiation Review | 2026-02-03 |

---

## 2. Issue ID Formats by Protocol Area

### Protocol-Specific Prefixes

| Prefix | Protocol Area | Tracking Document |
|--------|---------------|-------------------|
| R-XXX | RoCE | `analysis/roce_protocols/RoCE_protocols_issues.md` |
| E-XXX | Ethernet | `analysis/ethernet_protocols/ethernet_protocols_issues.md` |
| UAL-XXX | UALink | `analysis/ualink/ualink_issues.md` |
| D-XXX | Datamodel Gaps | `analysis/packet_taxonomy/packet_taxonomy.md` Section 5.2 |
| Q-X | Specification Questions | `analysis/packet_taxonomy/packet_taxonomy.md` Section 5.3 |

### Issue vs Work Item

| Type | Purpose | ID Format | Tracking |
|------|---------|-----------|----------|
| **Issue** | Problem identified during review | R-XXX, E-XXX, UAL-XXX | Protocol-specific issue file |
| **Work Item** | Task to resolve issue or implement change | W-XX-YYY | WORK_ITEMS.md + packet_taxonomy.md |

**Flow**: Issue identified → Work item created to resolve → Work item closed with resolution

---

## 3. Required Fields for Work Items

### Minimum Required Fields

| Field | Description | Example |
|-------|-------------|---------|
| **ID** | Unique identifier | W-10-006 |
| **Status** | Current state | Open, Closed, Deferred |
| **Priority** | Importance level | High, Medium, Low |
| **Category** | Type of work | Datamodel, Documentation, Architecture, Investigation |
| **Description** | What needs to be done | "Expand nscc_source.ksy stub with NSCC algorithm" |
| **Created** | Date opened | 2026-01-27 |

### Additional Fields (when applicable)

| Field | When Used | Example |
|-------|-----------|---------|
| **Closed** | When resolved | 2026-01-27 |
| **Estimated Effort** | For planning | 2-3 hours |
| **Deferred** | When deferred | 2026-02-03 |
| **Deferral Reason** | Why deferred | "Requires SharePoint access" |
| **Resolution** | How resolved | "Created cc_type.ksy per Table 3-48" |
| **Commit** | Git commit hash | `af256ea7` |
| **Dependencies** | Blocking items | W-09-009 (completed) |
| **References** | Spec sections | UE Spec Section 3.6.13.3 |

### Work Item Template (for WORK_ITEMS.md)

```markdown
### W-XX-YYY: Title

| Field | Value |
|-------|-------|
| **Status** | Open |
| **Priority** | Medium |
| **Category** | Datamodel |
| **Created** | YYYY-MM-DD |
| **Estimated Effort** | X-Y hours |

**Description**: What needs to be done.

**Deliverables**:
- [ ] Deliverable 1
- [ ] Deliverable 2

**References**:
- Spec Section X.Y.Z
- Related file: `path/to/file.ksy`
```

---

## 4. Status Values and Transitions

### Status Definitions

| Status | Meaning |
|--------|---------|
| **Open** | Active work item, not yet started or in progress |
| **Closed** | Work completed, verified, committed |
| **Deferred** | Postponed due to external dependency or lower priority |
| **Pending** | Waiting on external input (e.g., spec access, decision) |
| **Investigation** | Research needed before work can proceed |
| **Spec Update** | Requires specification change (tracked in HAS/PMR/WORK.md) |
| **Cancelled** | No longer needed (document reason) |

### Valid Transitions

```
Open ──────┬──→ Closed (work completed)
           ├──→ Deferred (postponed)
           ├──→ Pending (waiting on input)
           ├──→ Investigation (needs research)
           └──→ Cancelled (no longer needed)

Deferred ──┬──→ Open (unblocked, resuming)
           └──→ Cancelled (no longer relevant)

Pending ───┬──→ Open (input received)
           └──→ Deferred (input delayed)

Investigation ─→ Open (research complete, work defined)
```

### Criteria for Status Transitions

| Transition | Criteria |
|------------|----------|
| Open → Closed | All deliverables complete, verified, committed (if applicable) |
| Open → Deferred | External blocker identified, or deprioritized with reason |
| Open → Pending | Waiting on specific external input (document what) |
| Open → Cancelled | Determined unnecessary (document why) |
| Deferred → Open | Blocker resolved or priority increased |

---

## 5. Document Locations and Responsibilities

### Where to Track Different Items

| Item Type | Primary Location | Secondary Location |
|-----------|------------------|-------------------|
| **Active Open Items** | `analysis/packet_taxonomy/WORK_ITEMS.md` Section 1 | - |
| **Deferred Items** | `analysis/packet_taxonomy/WORK_ITEMS.md` Section 2 | - |
| **Recently Closed** | `analysis/packet_taxonomy/WORK_ITEMS.md` Section 5 | - |
| **Complete History** | `analysis/packet_taxonomy/packet_taxonomy.md` Section 5 | - |
| **File Modifications** | `analysis/packet_taxonomy/DATAMODEL_UPDATES.md` | - |
| **Protocol-Specific Issues** | `analysis/<protocol>/<protocol>_issues.md` | - |
| **Datamodel Gaps** | `analysis/packet_taxonomy/packet_taxonomy.md` Section 5.2 | WORK_ITEMS.md Section 3 |
| **Spec Questions** | `analysis/packet_taxonomy/packet_taxonomy.md` Section 5.3 | WORK_ITEMS.md Section 4 |
| **HAS-Tracked Items** | `docs/HAS/PMR/WORK.md` | Reference in packet_taxonomy.md |

### Update Workflow

1. **New work item identified**:
   - Add to `WORK_ITEMS.md` Section 1 (Open Work Items)
   - Add to `packet_taxonomy.md` Section 5.1 (Open Issues)

2. **Work item closed**:
   - Move from Section 1 to Section 5 in `WORK_ITEMS.md`
   - Update status in `packet_taxonomy.md` Section 5.1
   - Add entry to `packet_taxonomy.md` Section 5.5 (Change Log)
   - If file modified, add entry to `DATAMODEL_UPDATES.md`

3. **Work item deferred**:
   - Move from Section 1 to Section 2 in `WORK_ITEMS.md`
   - Update status and add deferral reason in `packet_taxonomy.md`

---

## 6. Priority Guidelines

### Priority Definitions

| Priority | Criteria |
|----------|----------|
| **High** | Blocks other work, architectural decision, data correctness issue |
| **Medium** | Important enhancement, documentation gap, cross-reference missing |
| **Low** | Nice-to-have, future consideration, minor documentation improvement |

### Priority Assignment Examples

| Priority | Example Work Items |
|----------|-------------------|
| High | W-04-004 (UE+ restructure), W-12-011 (AETH syndrome fix), W-19 (UFH rules) |
| Medium | W-09-003 (PDCID docs), W-13-010 (IEEE 802.3 support), W-11-009 (IB Spec review) |
| Low | W-09-010 (UFH UEC standardization), W-10-007 to W-10-012 (algorithm stubs) |

---

## 7. Category Definitions

| Category | Description | Examples |
|----------|-------------|----------|
| **Datamodel** | Changes to .ksy files | Field fixes, new files, restructuring |
| **Documentation** | Documentation updates | README, HAS chapters, taxonomy docs |
| **Architecture** | Design decisions | L2 selection rules, link negotiation |
| **Investigation** | Research tasks | Spec reviews, proprietary extensions |
| **Terminology** | Naming consistency | PDP vs PDS, SES vs SE |
| **Review** | Verification tasks | In-depth review of existing files |
| **Spec Update** | Requires spec change | Tracked in HAS/PMR/WORK.md |

---

## Usage

When creating or updating work items:

1. Assign appropriate ID (series or standalone)
2. Fill in all required fields
3. Set correct status and priority
4. Add to appropriate tracking document(s)
5. Update related documents when status changes
6. Include commit hash when work is committed
