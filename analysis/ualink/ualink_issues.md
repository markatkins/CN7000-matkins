# UALink Datamodel Issues

**Document**: Issues identified during UALink datamodel review  
**Created**: 2026-01-29  
**Reviewer**: AI Analysis  
**Datamodel Directory**: `earlysim/datamodel/protocols/ualink/`  
**Reference Specifications**: UALink200 v1.0, UALink 1.5 DLPL

---

## Summary

The UALink datamodel is **production-quality** with excellent specification traceability. The `.ksy` files are authoritative and well-documented.

### Issue Status Summary

| Status | Count | Issues |
|--------|-------|--------|
| Closed | 11 | UAL-001 through UAL-011 |
| Open | 0 | None |

### Open Issues by Priority

| Priority | ID | Description | Work Item |
|----------|-----|-------------|-----------|
| ~~Medium~~ | ~~UAL-006~~ | ~~In-depth review of security layer expansion~~ | ~~W-14-006~~ (Closed) |
| ~~Medium~~ | ~~UAL-007~~ | ~~KSY files missing x-related-headers~~ | ~~W-14-007~~ (Closed) |
| ~~Low~~ | ~~UAL-008~~ | ~~Sparse half-flit definitions~~ | ~~W-14-008~~ (Closed) |
| ~~Low~~ | ~~UAL-009~~ | ~~Response field missing table references~~ | ~~W-14-009~~ (Closed) |
| ~~Low~~ | ~~UAL-010~~ | ~~Flit header missing top-level seq~~ | ~~W-14-010~~ (Closed) |
| ~~Low~~ | ~~UAL-011~~ | ~~Incomplete YAML reference coverage~~ | ~~W-14-011~~ (Closed)

---

## Issues

### UAL-001: DL Flit Segment Sizes in YAML Reference File (CRITICAL)

**File**: `reference/field_definitions/dl_flit.yaml`

**Problem**: The YAML reference file shows segment sizes WITHOUT headers, but the authoritative `.ksy` file (`datalink/dl_flit.ksy`) correctly includes headers in segment sizes.

**YAML (incorrect)**:
```yaml
fields:
  - name: flit_header
    bytes: 3
  - name: segment_0
    bytes: 128  # Missing 1-byte header
  - name: segment_1
    bytes: 128  # Missing 1-byte header
  - name: segment_2
    bytes: 128  # Missing 1-byte header
  - name: segment_3
    bytes: 124  # Missing 1-byte header
  - name: segment_4
    bytes: 120  # Missing 1-byte header
  - name: crc
    bytes: 4
  - name: padding
    bytes: 5   # Unexplained padding to reach 640
```

**KSY (correct)**:
```yaml
seq:
  - id: flit_header
    size: 3
  - id: segment_0
    size: 129  # 1 header + 128 payload
  - id: segment_1
    size: 129
  - id: segment_2
    size: 129
  - id: segment_3
    size: 125
  - id: segment_4
    size: 121
  - id: crc
    size: 4
# Total: 3 + 129 + 129 + 129 + 125 + 121 + 4 = 640 bytes
```

**Impact**: YAML reference file is misleading; could cause incorrect implementations if used as reference.

**Resolution**: Update `dl_flit.yaml` to match `.ksy` structure:
- Include segment headers in segment sizes (129, 129, 129, 125, 121)
- Remove unexplained `padding` field
- Add `sectors` field to each segment for clarity

**Status**: **CLOSED** (2026-01-29)

**Resolution**: Updated `dl_flit.yaml` to match authoritative `.ksy` structure:
- Changed segment sizes to include headers: segment_0=129, segment_1=129, segment_2=129, segment_3=125, segment_4=121
- Added `header_bytes: 1` and `payload_bytes` fields to each segment for clarity
- Removed erroneous `padding: 5` field (was placeholder for missing segment headers)
- Total now correctly sums to 640 bytes: 3 + 129 + 129 + 129 + 125 + 121 + 4 = 640

---

### UAL-002: Packet Count Discrepancy Between Metadata Files (MEDIUM)

**Files**: 
- `metadata.yaml` (line 96-97)
- `reference/packet_types.yaml` (line 176-177)

**Problem**: Inconsistent packet counts between files.

| File | total_packets | total_protocols |
|------|---------------|-----------------|
| `metadata.yaml` | 35 | 11 |
| `packet_types.yaml` | 38 | 11 |

**Impact**: Confusion about actual coverage; `packet_types.yaml` appears more accurate based on detailed enumeration.

**Resolution**: Update `metadata.yaml` to reflect accurate count of 38 packets.

**Status**: **CLOSED** (2026-01-29)

**Resolution**: Updated `metadata.yaml` coverage statistics to match actual .ksy file count:
- `total_packets`: 35 → 38 (verified by counting .ksy files)
- Updated `by_layer` breakdown to match actual files:
  - upli: packets 8→6, protocols 2 (total 8 files)
  - transaction: packets 10→7, protocols 2 (total 9 files)
  - datalink: packets 13→8, protocols 4 (total 12 files)
  - physical: packets 4→3, protocols 1 (total 4 files)
  - security: packets 4→3, protocols 2 (total 5 files)
- Added explicit .ksy filename lists in comments for traceability
- Updated notes to clarify 38 = 27 packet formats + 11 protocols

---

### UAL-003: Missing KSY File Cross-References in YAML Reference Files (MEDIUM)

**Files**: All files in `reference/field_definitions/*.yaml`

**Problem**: YAML reference files don't cross-reference their corresponding `.ksy` files, making bidirectional traceability difficult.

**Current**:
```yaml
name: tl_flit
spec_ref: "UALink200 Section 5, Table 5-1"
layer: transaction
category: flit
```

**Recommended**:
```yaml
name: tl_flit
spec_ref: "UALink200 Section 5, Table 5-1"
ksy_file: "transaction/tl_flit.ksy"  # Add this
layer: transaction
category: flit
```

**Impact**: Difficult to navigate between reference documentation and authoritative definitions.

**Resolution**: Add `ksy_file` field to all YAML reference files:
- `tl_flit.yaml` → `transaction/tl_flit.ksy`
- `dl_flit.yaml` → `datalink/dl_flit.ksy`
- `flow_control_field.yaml` → `transaction/flow_control_field.ksy`
- `link_state.yaml` → `datalink/protocols/link_state.ksy`
- `upli_request_channel.yaml` → `upli/request_channel.ksy`

**Status**: **CLOSED** (2026-01-29)

**Resolution**: Added `ksy_file` field to all 5 YAML reference files:
- `tl_flit.yaml` → `ksy_file: "transaction/tl_flit.ksy"`
- `dl_flit.yaml` → `ksy_file: "datalink/dl_flit.ksy"`
- `flow_control_field.yaml` → `ksy_file: "transaction/flow_control_field.ksy"`
- `link_state.yaml` → `ksy_file: "datalink/protocols/link_state.ksy"`
- `upli_request_channel.yaml` → `ksy_file: "upli/request_channel.ksy"`

---

### UAL-004: Security Layer Definitions Sparse Compared to Other Layers (LOW)

**Files**: 
- `security/encryption.ksy`
- `security/iv_format.ksy`
- `security/authentication.ksy`

**Problem**: Security layer files are minimal (30-45 lines each) compared to other layers (100-300+ lines). Missing detailed field definitions from UALink200 Tables 9-4 through 9-7.

**Example** (`encryption.ksy` - only 43 lines):
```yaml
seq:
  - id: encryption_enabled
    type: b1
  - id: key_id
    type: b8
  - id: encrypted_payload
    size-eos: true
```

**Missing**:
- Key derivation parameters (Table 9-1)
- Authentication tag format details (Table 9-2)
- Encryption field layouts (Tables 9-4 through 9-7)
- Key rotation state machine

**Impact**: Security layer less useful for implementation reference compared to other layers.

**Resolution**: Expand security layer definitions to match detail level of UPLI/Transaction/DataLink layers. Reference Tables 9-1 through 9-7 in UALink200 Specification.

**Status**: **CLOSED** (2026-01-29)

**Resolution**: Expanded all 5 security layer files from ~270 lines total to ~1655 lines total:

| File | Before | After | Content Added |
|------|--------|-------|---------------|
| `encryption.ksy` | 43 | 464 | Tables 9-4 through 9-7 per-channel encryption/authentication attributes |
| `authentication.ksy` | 32 | 239 | Auth tag format, AAD structures, poison handling, integrity failure |
| `iv_format.ksy` | 39 | 209 | Table 9-3 IV format, per-stream IV state, TX/RX IV management |
| `key_derivation.ksy` | 75 | 355 | Figure 9-8 KDF state machine, context input, master/derived key structures |
| `key_rotation.ksy` | 81 | 388 | Figures 9-9, 9-11, 9-12 key swap flow, KeyRollMSG, TX/RX swap state |

Security layer now matches detail level of other UALink layers (UPLI, Transaction, Datalink).

---

### UAL-005: Spec Version Dates Need Verification (LOW)

**Files**: Various `.ksy` files

**Problem**: Some files use different `spec_date` values that should be verified against actual specification release dates.

| File | spec_date | Spec Version |
|------|-----------|--------------|
| `segment_header.ksy` | 2026-01-06 | DLPL 1.5 |
| `tl_flit.ksy` | 2025-03-01 | UALink200 1.0 |
| `dl_flit.ksy` | 2025-03-01 | UALink200 1.0 |

**Assessment**: Different dates are acceptable since different spec versions have different release dates. However, dates should be verified against actual UALink Consortium release dates.

**Impact**: Minor - documentation accuracy.

**Resolution**: Verify spec_date values against official UALink Consortium release dates. Update if incorrect.

**Status**: **CLOSED** (2026-01-30)

**Resolution**: Updated all spec_date values to official release dates:
- UALink 200 v1.0 Final: `2025-04-08` (per official press release)
- DLPL 1.5 Release Candidate: `2026-01-12` (per revision history)

Files updated:
- 37 .ksy files: `2025-03-01` → `2025-04-08` (UALink 200 v1.0)
- 1 .ksy file (`segment_header.ksy`): `2026-01-06` → `2026-01-12` (DLPL 1.5 RC)
- `metadata.yaml`: Updated `ualink_spec_date` and `dlpl_spec_date`

---

### UAL-007: KSY Files Missing x-related-headers Cross-References (MEDIUM)

**Files**: All 38 `.ksy` files in `datamodel/protocols/ualink/`

**Problem**: KSY files don't have `x-related-headers` sections to cross-reference related files. This makes navigation between related packet definitions difficult.

**Example** (`dl_flit.ksy` references these in documentation but doesn't formally link):
- `segment_header.ksy`
- `flit_header.ksy`
- `crc.ksy`

**Current**: No `x-related-headers` section
```yaml
x-packet:
  layer: "datalink"
  sublayer: "flits"
  category: "flit"
```

**Recommended**:
```yaml
x-packet:
  layer: "datalink"
  sublayer: "flits"
  category: "flit"

x-related-headers:
  - file: "segment_header.ksy"
    relationship: "contains"
    description: "Segment headers within DL Flit"
  - file: "flit_header.ksy"
    relationship: "contains"
    description: "Flit header at start of DL Flit"
  - file: "crc.ksy"
    relationship: "contains"
    description: "CRC-32 at end of DL Flit"
```

**Impact**: Difficult to navigate between related packet definitions; reduces discoverability.

**Resolution**: Add `x-related-headers` section to all KSY files that reference other packet types.

**Status**: **CLOSED** (2026-01-30)

**Resolution**: Added `x-related-headers` sections to 37 KSY files across all 5 layers:
- UPLI (7 files): commands, request_channel, read_response_channel, write_response_channel, originator_data_channel, flow_control, connection_handshake
- Transaction (9 files): tl_flit, control_half_flit, message_half_flit, data_half_flit, request_field, response_field, flow_control_field, compression, address_cache
- Datalink (12 files): dl_flit, flit_header, segment_header, crc, basic_messages, control_messages, uart_messages, vendor_defined, link_state, link_resiliency, link_level_replay, link_folding
- Physical (4 files): reconciliation_sublayer, control_ordered_sets, alignment_markers, link_training
- Security (5 files): encryption, authentication, iv_format, key_derivation, key_rotation

Relationship vocabulary: contains, references, uses, part-of
Commit: 16601541

---

### UAL-008: Sparse Half-Flit Definitions (LOW)

**Files**:
- `transaction/data_half_flit.ksy` (32 lines)
- `transaction/message_half_flit.ksy` (32 lines)

**Problem**: These files are minimal compared to `control_half_flit.ksy` (99 lines). They only define a 32-byte blob without detailed field breakdowns.

**Current** (`data_half_flit.ksy`):
```yaml
seq:
  - id: payload
    size: 32
    doc: "Data payload (32 bytes / 256 bits)"
    x-required: true
```

**Missing for Data Half-Flit**:
- Byte enable handling documentation
- Poison indication per Section 5.3
- Relationship to Originator Data Channel

**Missing for Message Half-Flit**:
- Message type encoding per Tables 5-3, 5-4
- TL message format details per Section 5.1.2

**Impact**: Less useful for implementation reference compared to other half-flit types.

**Resolution**: Expand definitions to include:
1. `data_half_flit.ksy`: Add poison indication, byte enable relationship, data beat sequencing
2. `message_half_flit.ksy`: Add message type encoding per Tables 5-3, 5-4

**Status**: **CLOSED** (2026-01-30)

**Resolution**: Expanded both half-flit files to match `control_half_flit.ksy` exemplar quality:

| File | Before | After | Content Added |
|------|--------|-------|---------------|
| `data_half_flit.ksy` | 40 | 142 | Field footprint table (Table 5-2), poison indication (Section 5.3), byte enable relationship (originator_data_channel.ksy), data beat sequencing, ASCII wire diagram |
| `message_half_flit.ksy` | 37 | 148 | Field footprint table (Table 5-2), message type encoding (Tables 5-3, 5-4), TL message format details (Section 5.1.2), ASCII wire diagram |

Both files now include:
- Header comment block with quality standards
- Expanded `doc:` block with field tables and ASCII diagrams
- Updated `x-spec` with specific table/section references
- Updated `x-packet` with constraints
- Updated `x-related-headers` with cross-references
- `seq:` remains as 32-byte blob (not bit-level parsing, matching exemplar pattern)

Commit: 61030281, pushed to origin/main

---

### UAL-009: Response Field Missing Specific Table References (LOW)

**File**: `transaction/response_field.ksy`

**Problem**: References "Section 5" generically but doesn't cite specific tables for each response format.

**Current**:
```yaml
x-spec:
  section: "Section 5"
  page: 131
```

**Should Reference**:
- Table 5-30: Uncompressed Response Field (Page 131)
- Table 5-34: Compressed Response Field Single-Beat (Page 135)
- Table 5-35: Compressed Response Field Multi-Beat (Page 136)

**Impact**: Reduced specification traceability for response field formats.

**Resolution**: Update `x-spec` to include all relevant tables:
```yaml
x-spec:
  tables: "Tables 5-30, 5-34, 5-35"
  section: "Section 5.9"
  page: 131
```

**Status**: **CLOSED** (2026-01-30)

**Resolution**: Expanded response_field.ksy from 52 to 310 lines with full bit-level parsing:
- Added `uncompressed_response` type (64 bits / 2 sectors) per Table 5-30
- Added `compressed_response_single_beat` type (32 bits / 1 sector) per Table 5-34
- Added `compressed_response_write_multibeat` type (32 bits / 1 sector) per Table 5-36
- Added x-packet.constraints for Tables 5-35 and 5-37 restrictions
- Created `response_field.yaml` reference file (139 lines)
- Commit: 1f8f4a35

---

### UAL-010: Flit Header Missing Top-Level Sequence (LOW)

**File**: `datalink/flit_header.ksy`

**Problem**: Defines types (`explicit_sequence_header`, `command_header`) but no top-level `seq:` to parse the actual 3-byte header. Cannot be used directly for parsing.

**Current**: Only defines types, no parsing entry point
```yaml
types:
  explicit_sequence_header:
    seq:
      - id: payload
        type: b1
      # ...
  command_header:
    seq:
      - id: payload
        type: b1
      # ...
# No top-level seq: section
```

**Recommended**: Add discriminated parsing based on `op` field:
```yaml
seq:
  - id: header_bytes
    size: 3
    doc: "Raw 3-byte flit header"

instances:
  op_field:
    value: "(header_bytes[0] >> 4) & 0x07"
    doc: "Operation field determines header type"
  
  is_explicit_sequence:
    value: "op_field == 0 || op_field == 1"
    
  is_command:
    value: "op_field == 2 || op_field == 3"
```

**Impact**: File cannot be used directly for parsing flit headers.

**Resolution**: Add top-level `seq:` with conditional parsing or instances for header type discrimination.

**Status**: **CLOSED** (2026-01-30)

**Resolution**: Expanded flit_header.ksy from 90 to 165 lines with:
- Top-level `seq:` reading raw 3-byte header
- `instances:` section with discriminator logic:
  - `op_field`: Extract bits [23:21] for header type
  - `payload_field`: Extract bit [20] for NOP/payload
  - `is_explicit_sequence`: op == 0 or 1
  - `is_command`: op == 2 or 3
  - `is_ack`, `is_replay_request`, `is_original`, `is_replay`, `is_nop`, `is_payload`
- Existing types preserved unchanged
- Commit: 6c622561

---

### UAL-011: Incomplete YAML Reference File Coverage (LOW)

**Files**: `reference/field_definitions/` directory

**Problem**: Only 5 YAML reference files exist for 38 KSY files. Coverage is incomplete.

**Current Coverage** (5 files):
- `dl_flit.yaml` ✓
- `tl_flit.yaml` ✓
- `flow_control_field.yaml` ✓
- `link_state.yaml` ✓
- `upli_request_channel.yaml` ✓

**Missing** (examples of key files without YAML references):
- `segment_header.yaml`
- `flit_header.yaml`
- `request_field.yaml`
- `response_field.yaml`
- `control_half_flit.yaml`
- All security layer files

**Impact**: Inconsistent reference documentation; some packet types have YAML summaries, others don't.

**Resolution**: Either:
1. Create YAML reference files for all 38 KSY files (comprehensive)
2. Document that YAML files are only for key packet formats and list criteria (minimal)

**Recommendation**: Option 2 - document the criteria for which packets get YAML reference files.

**Status**: **CLOSED** (2026-01-30)

**Resolution**: Documented YAML reference coverage criteria in `ualink/README.md`:

**Criteria for YAML Reference Files:**
1. **Entry point packets** - Top-level structures for parsing (tl_flit, dl_flit)
2. **Multi-variant formats** - Structures with encoding variants (response_field)
3. **Cross-layer interfaces** - Structures bridging protocol layers (upli_request_channel, link_state)
4. **High-complexity fields** - Fields with many sub-fields/constraints (flow_control_field)

**Current Coverage (6 files, not 5):**
- `tl_flit.yaml` - Entry point
- `dl_flit.yaml` - Entry point
- `response_field.yaml` - Multi-variant (added in W-14-009)
- `upli_request_channel.yaml` - Cross-layer
- `link_state.yaml` - Cross-layer
- `flow_control_field.yaml` - High-complexity

The remaining 32 KSY files are self-documenting through their `doc:` blocks and `x-spec` metadata.

Commit: 51d8c469, pushed to origin/main

---

## Verification Checklist

| Check | Status | Notes |
|-------|--------|-------|
| All layers covered (UPLI, TL, DL, PL, Security) | PASS | 38 files across 5 layers |
| Spec references present | PASS | x-spec metadata in all .ksy files |
| Field constraints documented | PASS | x-constraint annotations present |
| State machines defined | PASS | x-protocol.state_machine schema used |
| Enumerations complete | PASS | All opcodes/status codes defined |
| Wire formats documented | PASS | ASCII diagrams in doc blocks |
| Cross-file references (YAML→KSY) | PASS | Fixed in UAL-003 |
| Cross-file references (KSY→KSY) | PASS | Added x-related-headers to 37 files (UAL-007 CLOSED) |
| Size calculations correct | PASS | Fixed in UAL-001 |
| Half-flit detail level | PASS | data/message expanded to exemplar quality (UAL-008 CLOSED) |
| Table references complete | PASS | response_field has all tables (UAL-009 CLOSED) |
| Parseable structures | PASS | flit_header.ksy now has top-level seq (UAL-010 CLOSED) |
| YAML reference coverage | PASS | Criteria documented, 6/38 files by design (UAL-011 CLOSED) |

---

## Recommendations

### Completed (Closed)

1. **UAL-001**: ~~Fix `dl_flit.yaml` segment sizes~~ - CLOSED (W-14-001)
2. **UAL-002**: ~~Update `metadata.yaml` packet count to 38~~ - CLOSED (W-14-002)
3. **UAL-003**: ~~Add `ksy_file` cross-references to YAML files~~ - CLOSED (W-14-003)
4. **UAL-004**: ~~Expand security layer definitions~~ - CLOSED (W-14-004)
5. **UAL-005**: ~~Verify spec dates against official releases~~ - CLOSED (W-14-005)

### Open Issues (Medium Priority)

6. ~~**UAL-006**: In-depth review of W-14-004 security layer expansion (W-14-006)~~ - CLOSED (Verified, no corrections)
7. ~~**UAL-007**: Add `x-related-headers` cross-references to KSY files (W-14-007)~~ - CLOSED (37 files updated)

### Open Issues (Low Priority)

8. ~~**UAL-008**: Expand sparse half-flit definitions (W-14-008)~~ - CLOSED (data_half_flit 40→142, message_half_flit 37→148)
9. ~~**UAL-009**: Add specific table references to response_field.ksy (W-14-009)~~ - CLOSED
10. ~~**UAL-010**: Add top-level seq to flit_header.ksy (W-14-010)~~ - CLOSED
11. ~~**UAL-011**: Document YAML reference file coverage criteria (W-14-011)~~ - CLOSED (criteria in README.md)

---

## References

- UALink200 Specification v1.0 (UALink Consortium)
- UALink 1.5 DLPL Specification (UALink Consortium)
- `earlysim/datamodel/protocols/ualink/README.md`
- `earlysim/datamodel/protocols/ualink/metadata.yaml`
