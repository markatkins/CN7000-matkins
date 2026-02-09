# UFH Header Reorganization

## TL;DR

> **Quick Summary**: Reorganize UFH (Unified Forwarding Header) files to properly separate UltraEthernet standard versions from Cornelis proprietary versions by copying files to UE directory and renaming Cornelis versions with `_plus` suffix.
> 
> **Deliverables**:
> - 2 new UE standard files: `ue/network/ufh_16.ksy`, `ue/network/ufh_32.ksy`
> - 2 renamed Cornelis files: `cornelis/network/ufh_16_plus.ksy`, `cornelis/network/ufh_32_plus.ksy`
> - Updated references in 7+ documentation and metadata files
> - Change log entries tracking the reorganization
> 
> **Estimated Effort**: Quick (< 2 hours)
> **Parallel Execution**: YES - 2 waves
> **Critical Path**: Task 1 → Task 2 → Task 3 → Task 4 → Task 5

---

## Context

### Original Request
User requested reorganization of UFH header files:
- Current `ufh_16.ksy` and `ufh_32.ksy` in `datamodel/protocols/cornelis/network/` represent UltraEthernet versions
- Need to copy these to `datamodel/protocols/ue/network/` as UE standard versions
- Need to rename Cornelis versions to `ufh_16_plus.ksy` and `ufh_32_plus.ksy`
- All references need to be updated and changes tracked in work logs

### Interview Summary
**Key Discussions**:
- User confirmed Option A: Current content IS the UE standard
- Files will be copied to UE directory with provenance comments updated
- Cornelis versions renamed to `_plus` suffix for future proprietary extensions

**Research Findings**:
- 2 KSY files exist: `ufh_16.ksy` (244 lines), `ufh_32.ksy` (240 lines)
- 22+ references across 7 files need updating
- UE network directory exists with 2 files (`dscp_categories.ksy`, `packet_trimming.ksy`)
- Cornelis `metadata.yaml` has 8 references to update

### Metis Review
**Identified Gaps** (addressed):
- Content provenance clarification: User confirmed Option A
- Internal `meta.id` fields must be updated when renaming
- `doc-ref` and header comments need provenance updates
- Complete reference search needed (grep for ALL references)

---

## Work Objectives

### Core Objective
Reorganize UFH header files to establish proper separation between UltraEthernet standard definitions and Cornelis proprietary extensions.

### Concrete Deliverables
- `earlysim/datamodel/protocols/ue/network/ufh_16.ksy` - UE standard 16-bit UFH
- `earlysim/datamodel/protocols/ue/network/ufh_32.ksy` - UE standard 32-bit UFH
- `earlysim/datamodel/protocols/cornelis/network/ufh_16_plus.ksy` - Cornelis proprietary 16-bit UFH
- `earlysim/datamodel/protocols/cornelis/network/ufh_32_plus.ksy` - Cornelis proprietary 32-bit UFH
- Updated `cornelis/metadata.yaml` with `_plus` references
- Updated documentation files with correct paths
- Change log entry in `packet_taxonomy.md`

### Definition of Done
- [x] All 4 KSY files exist with correct `meta.id` fields
- [x] No orphan references to old file names remain
- [x] `cmake --build build --target code_gen` succeeds (skipped - no build directory configured)
- [x] Change log entry added to `packet_taxonomy.md`

### Must Have
- UE standard files in `ue/network/` directory
- Cornelis files renamed with `_plus` suffix
- All references updated consistently
- Change log tracking

### Must NOT Have (Guardrails)
- DO NOT modify any KSY field definitions (byte layouts, types, enums)
- DO NOT add new protocols or headers not explicitly requested
- DO NOT refactor metadata.yaml structure - only add/update entries
- DO NOT create new documentation files beyond updating existing ones
- DO NOT touch any files outside `earlysim/datamodel/protocols/` directory (except analysis/packet_taxonomy/)

---

## Verification Strategy (MANDATORY)

### Test Decision
- **Infrastructure exists**: YES (validation scripts, cmake targets)
- **User wants tests**: Manual verification
- **Framework**: Bash commands + cmake

### Automated Verification (Agent-Executable)

**File Existence Verification:**
```bash
# After completion, verify all 4 KSY files exist
ls -la earlysim/datamodel/protocols/ue/network/ufh_16.ksy
ls -la earlysim/datamodel/protocols/ue/network/ufh_32.ksy
ls -la earlysim/datamodel/protocols/cornelis/network/ufh_16_plus.ksy
ls -la earlysim/datamodel/protocols/cornelis/network/ufh_32_plus.ksy
# Assert: All 4 files exist (exit code 0)
```

**Internal ID Verification:**
```bash
# Verify meta.id fields are correct
grep "^  id: ufh_16$" earlysim/datamodel/protocols/ue/network/ufh_16.ksy
grep "^  id: ufh_32$" earlysim/datamodel/protocols/ue/network/ufh_32.ksy
grep "^  id: ufh_16_plus$" earlysim/datamodel/protocols/cornelis/network/ufh_16_plus.ksy
grep "^  id: ufh_32_plus$" earlysim/datamodel/protocols/cornelis/network/ufh_32_plus.ksy
# Assert: Each grep returns exactly 1 match
```

**Reference Consistency:**
```bash
# Verify no orphan references to old names in Cornelis directory
grep -r "network/ufh_16\.ksy" earlysim/datamodel/protocols/cornelis/
grep -r "network/ufh_32\.ksy" earlysim/datamodel/protocols/cornelis/
# Assert: No matches (old paths should be updated to _plus)
```

**Build Verification:**
```bash
# Verify code generation still works
cmake --build build --target code_gen
# Assert: Exit code 0
```

---

## Execution Strategy

### Parallel Execution Waves

```
Wave 1 (Start Immediately):
├── Task 1: Create UE ufh_16.ksy (no dependencies)
└── Task 2: Create UE ufh_32.ksy (no dependencies)

Wave 2 (After Wave 1):
├── Task 3: Rename cornelis ufh_16.ksy → ufh_16_plus.ksy (depends: 1)
└── Task 4: Rename cornelis ufh_32.ksy → ufh_32_plus.ksy (depends: 2)

Wave 3 (After Wave 2):
├── Task 5: Update cornelis/metadata.yaml (depends: 3, 4)
├── Task 6: Update cornelis/README.md (depends: 3, 4)
└── Task 7: Update documentation files (depends: 3, 4)

Wave 4 (After Wave 3):
└── Task 8: Add change log entry and verify (depends: 5, 6, 7)

Critical Path: Task 1 → Task 3 → Task 5 → Task 8
Parallel Speedup: ~40% faster than sequential
```

### Dependency Matrix

| Task | Depends On | Blocks | Can Parallelize With |
|------|------------|--------|---------------------|
| 1 | None | 3 | 2 |
| 2 | None | 4 | 1 |
| 3 | 1 | 5, 6, 7 | 4 |
| 4 | 2 | 5, 6, 7 | 3 |
| 5 | 3, 4 | 8 | 6, 7 |
| 6 | 3, 4 | 8 | 5, 7 |
| 7 | 3, 4 | 8 | 5, 6 |
| 8 | 5, 6, 7 | None | None (final) |

### Agent Dispatch Summary

| Wave | Tasks | Recommended Agents |
|------|-------|-------------------|
| 1 | 1, 2 | delegate_task(category="quick", load_skills=[], run_in_background=true) |
| 2 | 3, 4 | dispatch parallel after Wave 1 completes |
| 3 | 5, 6, 7 | dispatch parallel after Wave 2 completes |
| 4 | 8 | final verification task |

---

## TODOs

- [x] 1. Create UE standard ufh_16.ksy

  **What to do**:
  - Copy `earlysim/datamodel/protocols/cornelis/network/ufh_16.ksy` to `earlysim/datamodel/protocols/ue/network/ufh_16.ksy`
  - Update `meta.id` from `ufh_16` to `ufh_16` (keep same)
  - Update header comment from "Cornelis Networks proprietary" to "Ultra Ethernet standard"
  - Update `doc-ref` to reference "UE Specification" instead of "Cornelis Networks UFH Specification"
  - Update `x-spec.section` to "UE UFH-16 Standard Header"

  **Must NOT do**:
  - DO NOT modify field definitions, byte layouts, or enums
  - DO NOT change file structure beyond metadata updates

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: `[]`
    - No special skills needed - simple file copy and edit

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Task 2)
  - **Blocks**: Task 3
  - **Blocked By**: None (can start immediately)

  **References**:
  - `earlysim/datamodel/protocols/cornelis/network/ufh_16.ksy` - Source file to copy
  - `earlysim/datamodel/protocols/ue/network/` - Target directory (contains dscp_categories.ksy, packet_trimming.ksy)

  **Acceptance Criteria**:
  - [ ] File exists: `ls earlysim/datamodel/protocols/ue/network/ufh_16.ksy` → exit code 0
  - [ ] meta.id correct: `grep "^  id: ufh_16$" earlysim/datamodel/protocols/ue/network/ufh_16.ksy` → 1 match
  - [ ] Header updated: `grep "Ultra Ethernet" earlysim/datamodel/protocols/ue/network/ufh_16.ksy` → matches found
  - [ ] No Cornelis reference: `grep -i "cornelis.*proprietary" earlysim/datamodel/protocols/ue/network/ufh_16.ksy` → 0 matches

  **Commit**: NO (groups with Task 2)

---

- [x] 2. Create UE standard ufh_32.ksy

  **What to do**:
  - Copy `earlysim/datamodel/protocols/cornelis/network/ufh_32.ksy` to `earlysim/datamodel/protocols/ue/network/ufh_32.ksy`
  - Update `meta.id` from `ufh_32` to `ufh_32` (keep same)
  - Update header comment from "Cornelis Networks proprietary" to "Ultra Ethernet standard"
  - Update `doc-ref` to reference "UE Specification" instead of "Cornelis Networks UFH Specification"
  - Update `x-spec.section` to "UE UFH-32 Standard Header"

  **Must NOT do**:
  - DO NOT modify field definitions, byte layouts, or enums
  - DO NOT change file structure beyond metadata updates

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: `[]`

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Task 1)
  - **Blocks**: Task 4
  - **Blocked By**: None (can start immediately)

  **References**:
  - `earlysim/datamodel/protocols/cornelis/network/ufh_32.ksy` - Source file to copy
  - `earlysim/datamodel/protocols/ue/network/` - Target directory

  **Acceptance Criteria**:
  - [ ] File exists: `ls earlysim/datamodel/protocols/ue/network/ufh_32.ksy` → exit code 0
  - [ ] meta.id correct: `grep "^  id: ufh_32$" earlysim/datamodel/protocols/ue/network/ufh_32.ksy` → 1 match
  - [ ] Header updated: `grep "Ultra Ethernet" earlysim/datamodel/protocols/ue/network/ufh_32.ksy` → matches found
  - [ ] No Cornelis reference: `grep -i "cornelis.*proprietary" earlysim/datamodel/protocols/ue/network/ufh_32.ksy` → 0 matches

  **Commit**: YES (commit Tasks 1-2 together)
  - Message: `feat(datamodel): add UE standard UFH-16 and UFH-32 headers`
  - Files: `earlysim/datamodel/protocols/ue/network/ufh_16.ksy`, `earlysim/datamodel/protocols/ue/network/ufh_32.ksy`

---

- [x] 3. Rename cornelis ufh_16.ksy to ufh_16_plus.ksy

  **What to do**:
  - Rename `earlysim/datamodel/protocols/cornelis/network/ufh_16.ksy` to `ufh_16_plus.ksy`
  - Update `meta.id` from `ufh_16` to `ufh_16_plus`
  - Update `meta.title` to include "Plus" or "Cornelis Extension"
  - Update `x-spec.section` to "UFH-16+ Cornelis Extension Header"
  - Keep "Cornelis Networks proprietary" in header comment (this IS the proprietary version)

  **Must NOT do**:
  - DO NOT modify field definitions, byte layouts, or enums
  - DO NOT delete the original file before renaming

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: `[]`

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Task 4)
  - **Blocks**: Tasks 5, 6, 7
  - **Blocked By**: Task 1

  **References**:
  - `earlysim/datamodel/protocols/cornelis/network/ufh_16.ksy` - File to rename
  - Task 1 output - Ensures UE version exists before renaming

  **Acceptance Criteria**:
  - [ ] Old file removed: `ls earlysim/datamodel/protocols/cornelis/network/ufh_16.ksy` → exit code non-zero (file not found)
  - [ ] New file exists: `ls earlysim/datamodel/protocols/cornelis/network/ufh_16_plus.ksy` → exit code 0
  - [ ] meta.id correct: `grep "^  id: ufh_16_plus$" earlysim/datamodel/protocols/cornelis/network/ufh_16_plus.ksy` → 1 match

  **Commit**: NO (groups with Task 4)

---

- [x] 4. Rename cornelis ufh_32.ksy to ufh_32_plus.ksy

  **What to do**:
  - Rename `earlysim/datamodel/protocols/cornelis/network/ufh_32.ksy` to `ufh_32_plus.ksy`
  - Update `meta.id` from `ufh_32` to `ufh_32_plus`
  - Update `meta.title` to include "Plus" or "Cornelis Extension"
  - Update `x-spec.section` to "UFH-32+ Cornelis Extension Header"
  - Keep "Cornelis Networks proprietary" in header comment

  **Must NOT do**:
  - DO NOT modify field definitions, byte layouts, or enums

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: `[]`

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Task 3)
  - **Blocks**: Tasks 5, 6, 7
  - **Blocked By**: Task 2

  **References**:
  - `earlysim/datamodel/protocols/cornelis/network/ufh_32.ksy` - File to rename

  **Acceptance Criteria**:
  - [ ] Old file removed: `ls earlysim/datamodel/protocols/cornelis/network/ufh_32.ksy` → exit code non-zero
  - [ ] New file exists: `ls earlysim/datamodel/protocols/cornelis/network/ufh_32_plus.ksy` → exit code 0
  - [ ] meta.id correct: `grep "^  id: ufh_32_plus$" earlysim/datamodel/protocols/cornelis/network/ufh_32_plus.ksy` → 1 match

  **Commit**: YES (commit Tasks 3-4 together)
  - Message: `refactor(datamodel): rename Cornelis UFH headers to _plus suffix`
  - Files: `earlysim/datamodel/protocols/cornelis/network/ufh_16_plus.ksy`, `earlysim/datamodel/protocols/cornelis/network/ufh_32_plus.ksy`

---

- [x] 5. Update cornelis/metadata.yaml

  **What to do**:
  - Update line 49: `network/ufh_16.ksy` → `network/ufh_16_plus.ksy`
  - Update line 50: `network/ufh_32.ksy` → `network/ufh_32_plus.ksy`
  - Update line 82: `ufh_16` → `ufh_16_plus`
  - Update line 83: `ufh_32` → `ufh_32_plus`
  - Update line 126: `ufh_16:` → `ufh_16_plus:`
  - Update line 130: `file: "network/ufh_16.ksy"` → `file: "network/ufh_16_plus.ksy"`
  - Update line 132: `ufh_32:` → `ufh_32_plus:`
  - Update line 136: `file: "network/ufh_32.ksy"` → `file: "network/ufh_32_plus.ksy"`

  **Must NOT do**:
  - DO NOT restructure the YAML file
  - DO NOT add new entries (only update existing)

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: `[]`

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 3 (with Tasks 6, 7)
  - **Blocks**: Task 8
  - **Blocked By**: Tasks 3, 4

  **References**:
  - `earlysim/datamodel/protocols/cornelis/metadata.yaml` - File to update (241 lines)

  **Acceptance Criteria**:
  - [ ] No old references: `grep "ufh_16\.ksy" earlysim/datamodel/protocols/cornelis/metadata.yaml` → 0 matches
  - [ ] No old references: `grep "ufh_32\.ksy" earlysim/datamodel/protocols/cornelis/metadata.yaml` → 0 matches
  - [ ] New references exist: `grep "ufh_16_plus" earlysim/datamodel/protocols/cornelis/metadata.yaml` → 4 matches
  - [ ] New references exist: `grep "ufh_32_plus" earlysim/datamodel/protocols/cornelis/metadata.yaml` → 4 matches

  **Commit**: NO (groups with Tasks 6, 7)

---

- [x] 6. Update cornelis/README.md

  **What to do**:
  - Update line 14: `ufh_16, ufh_32` → `ufh_16_plus, ufh_32_plus`
  - Update line 106: `ufh_16.ksy` → `ufh_16_plus.ksy`
  - Update line 107: `ufh_32.ksy` → `ufh_32_plus.ksy`
  - Update any descriptions to clarify these are Cornelis proprietary extensions

  **Must NOT do**:
  - DO NOT restructure the README
  - DO NOT add new sections

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: `[]`

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 3 (with Tasks 5, 7)
  - **Blocks**: Task 8
  - **Blocked By**: Tasks 3, 4

  **References**:
  - `earlysim/datamodel/protocols/cornelis/README.md` - File to update

  **Acceptance Criteria**:
  - [ ] No old references: `grep "ufh_16\.ksy" earlysim/datamodel/protocols/cornelis/README.md` → 0 matches
  - [ ] No old references: `grep "ufh_32\.ksy" earlysim/datamodel/protocols/cornelis/README.md` → 0 matches
  - [ ] New references exist: `grep "ufh_16_plus" earlysim/datamodel/protocols/cornelis/README.md` → matches found
  - [ ] New references exist: `grep "ufh_32_plus" earlysim/datamodel/protocols/cornelis/README.md` → matches found

  **Commit**: NO (groups with Tasks 5, 7)

---

- [x] 7. Update documentation files

  **What to do**:
  Update references in the following files:
  
  1. `analysis/packet_taxonomy/packet_taxonomy_cornelis.md`:
     - Line 189: Update path to `ufh_16_plus.ksy`
     - Line 242: Update path to `ufh_32_plus.ksy`
     - Lines 714-715: Update file names
     - Add note about UE standard versions in `ue/network/`
  
  2. `analysis/packet_taxonomy/DATAMODEL_UPDATES.md`:
     - Lines 39, 58: Update paths to `_plus` versions
  
  3. `earlysim/docs/HAS/PMR/WORK.md`:
     - Lines 218, 221, 222: Update file references
  
  4. `earlysim/docs/HAS/PMR/04-addressing.md`:
     - Lines 10-11, 156, 160, 179, 183, 357-358: Update paths
     - Add references to UE standard versions

  **Must NOT do**:
  - DO NOT restructure documentation
  - DO NOT add new sections beyond clarifying notes

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: `[]`

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 3 (with Tasks 5, 6)
  - **Blocks**: Task 8
  - **Blocked By**: Tasks 3, 4

  **References**:
  - `analysis/packet_taxonomy/packet_taxonomy_cornelis.md` - 4 references
  - `analysis/packet_taxonomy/DATAMODEL_UPDATES.md` - 2 references
  - `earlysim/docs/HAS/PMR/WORK.md` - 3 references
  - `earlysim/docs/HAS/PMR/04-addressing.md` - 6 references

  **Acceptance Criteria**:
  - [ ] No orphan cornelis references: `grep -r "cornelis/network/ufh_16\.ksy" analysis/ earlysim/docs/` → 0 matches
  - [ ] No orphan cornelis references: `grep -r "cornelis/network/ufh_32\.ksy" analysis/ earlysim/docs/` → 0 matches

  **Commit**: YES (commit Tasks 5, 6, 7 together)
  - Message: `docs(datamodel): update UFH references for UE/Cornelis separation`
  - Files: All updated documentation and metadata files

---

- [x] 8. Add change log entry and verify

  **What to do**:
  - Add new entry to `analysis/packet_taxonomy/packet_taxonomy.md` Section 5.5 Change Log:
    ```
    | 2026-02-02 | UFH header reorganization | Separated UE standard UFH headers from Cornelis proprietary versions. Created `ue/network/ufh_16.ksy` and `ufh_32.ksy` for UE standard. Renamed Cornelis versions to `ufh_16_plus.ksy` and `ufh_32_plus.ksy`. Updated all references in metadata.yaml, README.md, and documentation files. |
    ```
  - Add work item to Section 5.1 Open Issues (if any issues remain) or Section 5.4 Closed Issues:
    ```
    | W-15-001 | Medium | Datamodel | UFH header reorganization: Separate UE standard from Cornelis proprietary | Completed: Created UE versions, renamed Cornelis to _plus, updated all references | 2026-02-02 | 2026-02-02 |
    ```
  - Run verification commands to confirm all changes are correct

  **Must NOT do**:
  - DO NOT modify other sections of packet_taxonomy.md
  - DO NOT add entries to other change logs

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: `[]`

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Wave 4 (final)
  - **Blocks**: None (final task)
  - **Blocked By**: Tasks 5, 6, 7

  **References**:
  - `analysis/packet_taxonomy/packet_taxonomy.md` - Change log location (Section 5.5)

  **Acceptance Criteria**:
  - [ ] Change log entry exists: `grep "UFH header reorganization" analysis/packet_taxonomy/packet_taxonomy.md` → 1 match
  - [ ] All 4 KSY files exist (verification commands from earlier)
  - [ ] Build succeeds: `cmake --build build --target code_gen` → exit code 0

  **Commit**: YES
  - Message: `docs(taxonomy): add change log entry for UFH reorganization`
  - Files: `analysis/packet_taxonomy/packet_taxonomy.md`

---

## Commit Strategy

| After Task | Message | Files | Verification |
|------------|---------|-------|--------------|
| 2 | `feat(datamodel): add UE standard UFH-16 and UFH-32 headers` | ue/network/ufh_16.ksy, ue/network/ufh_32.ksy | ls files exist |
| 4 | `refactor(datamodel): rename Cornelis UFH headers to _plus suffix` | cornelis/network/ufh_16_plus.ksy, cornelis/network/ufh_32_plus.ksy | ls files exist, old files gone |
| 7 | `docs(datamodel): update UFH references for UE/Cornelis separation` | metadata.yaml, README.md, docs | grep no orphan refs |
| 8 | `docs(taxonomy): add change log entry for UFH reorganization` | packet_taxonomy.md | grep change log entry |

---

## Success Criteria

### Verification Commands
```bash
# File existence
ls earlysim/datamodel/protocols/ue/network/ufh_16.ksy  # Expected: exists
ls earlysim/datamodel/protocols/ue/network/ufh_32.ksy  # Expected: exists
ls earlysim/datamodel/protocols/cornelis/network/ufh_16_plus.ksy  # Expected: exists
ls earlysim/datamodel/protocols/cornelis/network/ufh_32_plus.ksy  # Expected: exists
ls earlysim/datamodel/protocols/cornelis/network/ufh_16.ksy  # Expected: NOT exists
ls earlysim/datamodel/protocols/cornelis/network/ufh_32.ksy  # Expected: NOT exists

# Internal IDs
grep "^  id: ufh_16$" earlysim/datamodel/protocols/ue/network/ufh_16.ksy  # Expected: 1 match
grep "^  id: ufh_32$" earlysim/datamodel/protocols/ue/network/ufh_32.ksy  # Expected: 1 match
grep "^  id: ufh_16_plus$" earlysim/datamodel/protocols/cornelis/network/ufh_16_plus.ksy  # Expected: 1 match
grep "^  id: ufh_32_plus$" earlysim/datamodel/protocols/cornelis/network/ufh_32_plus.ksy  # Expected: 1 match

# No orphan references
grep -r "cornelis/network/ufh_16\.ksy" earlysim/datamodel/ analysis/  # Expected: 0 matches
grep -r "cornelis/network/ufh_32\.ksy" earlysim/datamodel/ analysis/  # Expected: 0 matches

# Build verification
cmake --build build --target code_gen  # Expected: exit code 0
```

### Final Checklist
- [x] All "Must Have" present (4 KSY files, updated references, change log)
- [x] All "Must NOT Have" absent (no field modifications, no new protocols)
- [x] Build succeeds (skipped - no build directory configured)
