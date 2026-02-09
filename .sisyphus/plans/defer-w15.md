# Plan: Defer W-15 Work Item

**Created**: 2026-02-03  
**Estimated Effort**: 5 minutes  
**Type**: Documentation update

---

## Objective

Move W-15 (UE+ to CN7000 Packet Taxonomy.ppt Comparison Table) from Open to Deferred status in `analysis/packet_taxonomy/WORK_ITEMS.md`.

**Reason for deferral**: Requires access to CN7000 Packet Taxonomy.ppt which is on SharePoint and not accessible programmatically.

---

## Tasks

### Task 1: Move W-15 to Deferred Section

**File**: `analysis/packet_taxonomy/WORK_ITEMS.md`

**Action**: 
1. Cut the entire W-15 section (lines 22-55) from "## 1. Open Work Items"
2. Paste into "## 2. Deferred Work Items" section (after line 97)
3. Update the status field from `Open` to `Deferred`
4. Add deferral reason

**Updated W-15 entry**:

```markdown
### W-15: UE+ to CN7000 Packet Taxonomy.ppt Comparison Table

| Field | Value |
|-------|-------|
| **Status** | Deferred |
| **Priority** | Medium |
| **Category** | Documentation |
| **Estimated Effort** | 2-4 hours |
| **Created** | 2026-02-02 |
| **Deferred** | 2026-02-03 |
| **Deferral Reason** | Requires SharePoint access to CN7000 Packet Taxonomy.ppt |

**Description**: Create a comparison table mapping UE+ packet types (as documented in `packet_taxonomy_ue_plus_variants.md`) to the nomenclature used in CN7000 Packet Taxonomy.ppt.

**Expected Deliverable**: A new section in `packet_taxonomy_ue_plus_variants.md` with a comparison table containing:

| UE Spec Name | CN7000 PPT Name | Key Differences | Notes |
|--------------|-----------------|-----------------|-------|
| UE Tagged Send (Standard) | TBD | TBD | TBD |
| UE + CSIG Compact | TBD | TBD | TBD |
| UE + CSIG Wide | TBD | TBD | TBD |
| UE IPv4 Native | TBD | TBD | TBD |
| UE + Encrypted (TSS) | TBD | TBD | TBD |
| UE Small Message | TBD | TBD | TBD |
| UE Rendezvous Send | TBD | TBD | TBD |
| UE Deferrable Send | TBD | TBD | TBD |

**Dependencies**:
- Requires access to CN7000 Packet Taxonomy.ppt (internal document)
- `packet_taxonomy_ue_plus_variants.md` must be complete ✅

**References**:
- CN7000 Packet Taxonomy.ppt (SharePoint: OPA Engineering Documentation/Projects/CN7000/General/Landing Zone/)
- UltraEthernet Specification v1.0.1
- `analysis/packet_taxonomy/packet_taxonomy_ue_plus_variants.md`

**To Undefer**: Download CN7000 Packet Taxonomy.ppt to local repo or provide packet type nomenclature from the PPT.
```

---

## Verification

- [x] W-15 no longer appears in Section 1 (Open Work Items)
- [x] W-15 appears in Section 2 (Deferred Work Items)
- [x] Status field shows "Deferred"
- [x] Deferral date and reason are documented

---

## Notes

- Also corrected file reference from `packet_taxonomy_ue_tagged_send_variants.md` to `packet_taxonomy_ue_plus_variants.md` (the actual file name)
- Added SharePoint path to references for future retrieval
