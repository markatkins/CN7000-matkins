# RoCE Datamodel Issues

**Document**: Issues identified during RoCE datamodel review  
**Created**: 2026-01-27  
**Source**: `earlysim/datamodel/protocols/roce/`  
**Reference**: InfiniBand Architecture Specification Volume 1, Release 1.4

---

## Summary

| ID | Severity | File | Issue | Status |
|----|----------|------|-------|--------|
| R-001 | Low | bth.ksy | `is_atomic` doc uses hex but code uses decimal - clarify | Closed |
| R-002 | Low | aeth.ksy | Section reference inconsistency - reference both 9.4 (format) and 9.7.5.1 (semantics) | Closed |

| R-003 | Medium | deth.ksy | Opcode format inconsistency (full vs operation codes) - standardized to operation codes | Closed |
| R-004 | Low | reth.ksy | Missing opcodes in x-related-headers - added opcodes [0x06, 0x0A, 0x0B, 0x0C] | Closed |
| R-005 | Low | README.md | Missing CNP and XRC transport types - CNP=Yes, XRC=No (W-12-012) | Closed |
| R-006 | Low | aeth.ksy | RNR timeout enum values 0x20-0x1f note - actually only 5 bits (0-31) so no reserved values needed | Cancelled |
| R-007 | Low | qp_state_machine.ksy | x-spec placement inconsistency - moved to root level | Closed |
| R-008 | Medium | (missing) | No XRCETH header for XRC transport | Closed (Not Required) |
| R-009 | Low | bth.ksy | Extended atomics (0x15, 0x16) not supported over RoCE | Closed |
| R-010 | Low | icrc.ksy | ICRC masking details incomplete for RoCEv2 - added detailed byte offsets per Linux rxe_icrc.c | Closed |
| R-011 | High | aeth.ksy | Syndrome bit layout WRONG: bit 7 reserved, bits [6:5]=ACK type, bits [4:0]=value; mask should be 0x1f not 0x3f; shift should be >>5 not >>6 | Closed |
| R-012 | Low | aeth.ksy | Missing opcodes [0x0D-0x12] in x-related-headers for bth.ksy reference | Closed |
| R-013 | Low | immdt.ksy | Missing opcodes [0x03, 0x05, 0x09, 0x0B] in x-related-headers for bth.ksy reference | Closed |
| R-014 | Low | atomiceth.ksy | Missing opcodes [0x13, 0x14] in x-related-headers for bth.ksy reference | Closed |
| R-015 | Low | atomicacketh.ksy | Missing opcodes [0x12] in x-related-headers for bth.ksy reference | Closed |
| R-016 | Low | deth.ksy | Missing opcodes [0x04, 0x05] in x-related-headers for bth.ksy reference | Closed |
| R-017 | Low | README.md | Missing protocols/ directory in file list | Closed |

---

## Issue Details

### R-001: BTH `is_atomic` Documentation Clarity (Low)

**File:** `bth.ksy`, lines 304-321

**Current:**
```yaml
is_atomic:
  value: operation >= 18 and operation <= 20
  doc: |
    True if this is an atomic operation (operation codes 0x12-0x14).
```

**Problem:** The doc says "operation codes 0x12-0x14" (hex) but the code uses decimal values 18-20. While mathematically equivalent, this can cause confusion.

**Recommendation:** Clarify in the doc that 0x12=18, 0x13=19, 0x14=20 decimal, or change the code to use hex literals for consistency:
```yaml
value: operation >= 0x12 and operation <= 0x14
```

---

### R-002: AETH Section Reference Inconsistency (Low)

**File:** `aeth.ksy`

**Current:**
- `x-spec.section`: "Section 9.7.5.1" (line 24)
- `doc` block: "Reference: InfiniBand Architecture Specification Vol 1, Section 9.4" (line 53)

**Problem:** Two different section references, but both are valid and cover different aspects:
- Section 9.4: AETH header format definition (field layout, bit positions, sizes)
- Section 9.7.5.1: ACK packet semantics (when AETH is used, syndrome interpretation, credit flow)

**Recommendation:** Reference both sections with clear distinction:

In `x-spec`:
```yaml
x-spec:
  spec_name: "InfiniBand Architecture Specification Volume 1"
  spec_version: "1.4"
  roce_annex: "A17"
  section: "Section 9.4"              # Primary: header format
  section_semantics: "Section 9.7.5.1"  # Secondary: ACK semantics
  table: "Table 46"
```

In doc block:
```
Reference: InfiniBand Architecture Specification Vol 1
  - Section 9.4: AETH header format (Table 46)
  - Section 9.7.5.1: ACK packet semantics and credit flow
```

---

### R-003: DETH Opcode Format Inconsistency (Medium)

**File:** `deth.ksy`

**Current (line 13):**
```yaml
opcodes: [0x65]
```

**Current (lines 55-57):**
```
Used with UD transport type opcodes:
  - UD SEND_ONLY (0x64)
  - UD SEND_ONLY_IMM (0x65)
```

**Problem:** Uses full opcodes (transport_type << 5 | operation) while other files use operation codes only. For example:
- `bth.ksy` x-related-headers uses operation codes: `opcodes: [0x06, 0x0A, 0x0B, 0x0C]`
- `deth.ksy` uses full opcodes: `opcodes: [0x65]`

**Recommendation:** Standardize on operation codes (0x04, 0x05) with transport type noted separately, consistent with BTH documentation style:
```yaml
opcodes: [0x04, 0x05]  # SEND_ONLY, SEND_ONLY_IMM (UD transport only)
```

---

### R-004: RETH Missing Opcodes in x-related-headers (Low)

**File:** `reth.ksy`, lines 7-17

**Current:**
```yaml
x-related-headers:
  - file: "bth.ksy"
    description: "Base Transport Header - precedes RETH in all packets"
```

**Problem:** No opcodes listed for when RETH is used, unlike BTH which lists opcodes for each related header.

**Recommendation:** Add opcodes to the bth.ksy reference:
```yaml
x-related-headers:
  - file: "bth.ksy"
    description: "Base Transport Header - precedes RETH in all packets"
    opcodes: [0x06, 0x0A, 0x0B, 0x0C]  # RDMA_WRITE_FIRST, RDMA_WRITE_ONLY, RDMA_WRITE_ONLY_IMM, RDMA_READ_REQUEST
```

---

### R-005: README.md Missing CNP and XRC Transport Types (Low)

**File:** `README.md`, lines 35-41

**Current:**
```markdown
| Type | Code | Description |
|------|------|-------------|
| RC (Reliable Connection) | 0 | Connection-oriented, reliable, in-order |
| UC (Unreliable Connection) | 1 | Connection-oriented, unreliable |
| RD (Reliable Datagram) | 2 | Connectionless, reliable |
| UD (Unreliable Datagram) | 3 | Connectionless, unreliable |
```

**Problem:** Missing CNP (4) and XRC (5) which are documented in `bth.ksy`.

**Recommendation:** Add CNP and XRC to the transport types table:
```markdown
| CNP (Congestion Notification) | 4 | ECN-based congestion notification |
| XRC (Extended Reliable Connection) | 5 | RC with shared receive queue |
```

---

### R-006: AETH RNR Timeout Enum - CANCELLED

**File:** `aeth.ksy`, lines 149-181

**Original concern:** The `rnr_timeout_values` enum defines values 0x00-0x1f (0-31), and values 0x20-0x3f might be reserved.

**Resolution:** Per IB Spec Vol 1 v1.4, the RNR timeout field is only 5 bits [4:0], so values 0-31 (0x00-0x1f) are the complete range. There are no reserved values 0x20-0x3f because the field is only 5 bits.

**Status:** CANCELLED - not an issue.

---

### R-007: QP State Machine x-spec Placement Inconsistency (Low)

**File:** `qp_state_machine.ksy`, lines 36-39

**Current:**
```yaml
meta:
  id: qp_state_machine
  title: RoCE/InfiniBand Queue Pair State Machine

# Cross-references...
x-related-headers:
  ...
  
  x-spec:  # Nested inside meta block
    section: "IB Arch Vol 1, Section 10.3"
```

**Problem:** `x-spec` is nested inside the `meta:` block, unlike transport files where it's at root level after `x-related-headers`.

**Recommendation:** Move `x-spec` to root level for consistency with transport files:
```yaml
meta:
  id: qp_state_machine
  ...

x-related-headers:
  ...

x-spec:
  spec_name: "InfiniBand Architecture Specification Volume 1"
  spec_version: "1.4"
  section: "Section 10.3"
  ...
```

---

### R-008: Missing XRCETH Header for XRC Transport (Medium) - CLOSED (Not Required)

**File:** (not needed)

**Original Problem:** XRC transport type (5) is documented in BTH, but there's no XRCETH (XRC Extended Transport Header) file.

**Decision:** PMR does NOT support XRC (Extended Reliable Connection) transport.

**Rationale:** PMR does not implement shared receive queues, which are required for XRC. Therefore:
- XRCETH header is not needed in the datamodel
- XRC transport type (5) is documented in bth.ksy for packet classification only
- XRC packets should be rejected by PMR

**Resolution:**
- Updated `roce/README.md` to show XRC PMR Support = "No"
- Updated `bth.ksy` x-packet.pmr_support to document XRC exclusion
- Updated `bth.ksy` is_xrc instance doc to note PMR does not support XRC

**Status:** CLOSED (Not Required) - Commit 53fb207b, pushed to origin/main (2026-01-28).

---

### R-009: Extended Atomics Not Supported Over RoCE (Low) - CLOSED

**File:** `bth.ksy`, `README.md`

**Original Problem:** Only CMP_SWAP (0x13) and FETCH_ADD (0x14) are documented. IB Spec 1.3+ added extended atomics:
- MASKED_CMP_SWAP (0x15)
- MASKED_FETCH_ADD (0x16)

**Decision:** PMR does NOT support extended/masked atomics over RoCE. These operations will be implemented over UE/UE+ instead.

**PMR RoCE Atomic Support:**
- **Supported:** CMP_SWAP (0x13), FETCH_ADD (0x14) - standard 64-bit atomics
- **NOT Supported:** MASKED_CMP_SWAP (0x15), MASKED_FETCH_ADD (0x16) - extended atomics

**Resolution:**
- Updated `roce/README.md` with note about extended atomics exclusion
- Updated `bth.ksy` pmr_support metadata with atomic support details
- Updated `bth.ksy` is_atomic instance doc to list supported vs not supported operations
- Updated is_atomic transport type restrictions to reflect XRC not supported

**Status:** CLOSED - Commit dd2e1f5b, pushed to origin/main.

---

### R-011: AETH Syndrome Field Bit Layout Incorrect (High)

**File:** `aeth.ksy`

**Current (WRONG):**
```yaml
doc: |
  Syndrome field (8 bits)
  Encodes ACK type and additional information:
    - Bits [7:6]: ACK type (2 bits)      # WRONG
      00 = ACK (positive acknowledgment)
      01 = RNR NAK (Receiver Not Ready)
      10 = Reserved
      11 = NAK (Negative acknowledgment)
    - Bits [5:0]: Meaning depends on ACK type (6 bits, values 0-63)  # WRONG

ack_type:
  value: (syndrome >> 6) & 0x03   # WRONG shift
  
credit_count:
  value: syndrome & 0x3f          # WRONG mask (was incorrectly "fixed" from 0x1f)
```

**Correct (per IB Spec Vol 1, v1.4):**
```yaml
doc: |
  Syndrome field (8 bits)
  Encodes ACK type and additional information:
    - Bit 7: Reserved (must be 0)
    - Bits [6:5]: ACK type (2 bits)
      00 = ACK (positive acknowledgment)
      01 = RNR NAK (Receiver Not Ready)
      10 = Reserved
      11 = NAK (Negative acknowledgment)
    - Bits [4:0]: Value depends on ACK type (5 bits, values 0-31)
      For ACK:     Credit count (C CCCC)
      For RNR NAK: Timer value (T TTTT)
      For NAK:     NAK code (N NNNN)

ack_type:
  value: (syndrome >> 5) & 0x03   # Correct: shift by 5, mask 2 bits
  
credit_count:
  value: syndrome & 0x1f          # Correct: 5 bits (0-31)
```

**Problem:** W-11-006 incorrectly "fixed" the mask from 0x1f to 0x3f based on misreading the bit layout. The original 0x1f mask was correct for bits [4:0]. The documentation incorrectly stated bits [7:6] for ACK type when it should be bits [6:5].

**Impact:** High - incorrect parsing of AETH syndrome field will cause:
- Wrong ACK type detection
- Wrong credit count values
- Wrong RNR timeout values
- Wrong NAK codes

**Recommendation:** Revert mask to 0x1f, fix ack_type shift to >> 5, update all documentation.

**Note:** This supersedes the closure of W-11-006. W-11-006 must be reopened and corrected.

---

### R-010: ICRC Masking Details Incomplete for RoCEv2 (Low)

**File:** `icrc.ksy`

**Current (lines 69-73):**
```
Fields masked/replaced during ICRC calculation:
  - IP header fields: replaced with 0xFF
  - UDP header: replaced with 0xFF
  - BTH reserved fields: replaced with 0xFF
  - LRH (Link Route Header) if present: replaced with 0xFF
```

**Problem:** The description is generic. For RoCEv2 specifically, the exact bytes/offsets that are masked should be documented.

**Recommendation:** Add RoCEv2-specific masking details:
```
RoCEv2 ICRC Masking (per Annex A17):
  - IPv4: TTL, Header Checksum, Source IP (bytes 8-9, 10-11, 12-15)
  - IPv6: Hop Limit, Source Address (byte 7, bytes 8-23)
  - UDP: Checksum (bytes 6-7)
  - BTH: Reserved byte (byte 4)
```

---

### R-012: AETH Missing Opcodes in x-related-headers (Low)

**File:** `aeth.ksy`

**Problem:** The `x-related-headers` section for bth.ksy does not list the opcodes that use AETH.

**Missing opcodes:**
- 0x0D: RDMA_READ_RESPONSE_FIRST
- 0x0E: RDMA_READ_RESPONSE_MIDDLE
- 0x0F: RDMA_READ_RESPONSE_LAST
- 0x10: RDMA_READ_RESPONSE_ONLY
- 0x11: ACKNOWLEDGE
- 0x12: ATOMIC_ACKNOWLEDGE

**Recommendation:** Add opcodes to x-related-headers:
```yaml
x-related-headers:
  - file: "bth.ksy"
    description: "Base Transport Header - precedes AETH"
    opcodes: [0x0D, 0x0E, 0x0F, 0x10, 0x11, 0x12]
```

---

### R-013: ImmDt Missing Opcodes in x-related-headers (Low)

**File:** `immdt.ksy`

**Problem:** The `x-related-headers` section for bth.ksy does not list the opcodes that use ImmDt.

**Missing opcodes:**
- 0x03: SEND_LAST_IMM
- 0x05: SEND_ONLY_IMM
- 0x09: RDMA_WRITE_LAST_IMM
- 0x0B: RDMA_WRITE_ONLY_IMM

**Recommendation:** Add opcodes to x-related-headers:
```yaml
x-related-headers:
  - file: "bth.ksy"
    description: "Base Transport Header - precedes ImmDt"
    opcodes: [0x03, 0x05, 0x09, 0x0B]
```

---

### R-014: AtomicETH Missing Opcodes in x-related-headers (Low)

**File:** `atomiceth.ksy`

**Problem:** The `x-related-headers` section for bth.ksy does not list the opcodes that use AtomicETH.

**Missing opcodes:**
- 0x13: CMP_SWAP (Compare and Swap)
- 0x14: FETCH_ADD (Fetch and Add)

**Recommendation:** Add opcodes to x-related-headers:
```yaml
x-related-headers:
  - file: "bth.ksy"
    description: "Base Transport Header - precedes AtomicETH"
    opcodes: [0x13, 0x14]
```

---

### R-015: AtomicAckETH Missing Opcodes in x-related-headers (Low)

**File:** `atomicacketh.ksy`

**Problem:** The `x-related-headers` section for bth.ksy does not list the opcodes that use AtomicAckETH.

**Missing opcodes:**
- 0x12: ATOMIC_ACKNOWLEDGE

**Recommendation:** Add opcodes to x-related-headers:
```yaml
x-related-headers:
  - file: "bth.ksy"
    description: "Base Transport Header - precedes AtomicAckETH"
    opcodes: [0x12]
```

---

### R-016: DETH Missing Opcodes in x-related-headers (Low)

**File:** `deth.ksy`

**Problem:** The `x-related-headers` section for bth.ksy does not list the opcodes that use DETH.

**Missing opcodes:**
- 0x04: SEND_ONLY (UD transport)
- 0x05: SEND_ONLY_IMM (UD transport)

**Note:** These are operation codes (not full opcodes). For UD transport (type 3), full opcodes would be 0x64 and 0x65.

**Recommendation:** Add opcodes to x-related-headers:
```yaml
x-related-headers:
  - file: "bth.ksy"
    description: "Base Transport Header - precedes DETH"
    opcodes: [0x04, 0x05]  # Operation codes for UD SEND_ONLY, SEND_ONLY_IMM
```

---

### R-017: README.md Missing protocols/ Directory (Low)

**File:** `README.md`

**Problem:** The file list in README.md does not include the `protocols/` directory which contains `qp_state_machine.ksy`.

**Current file list:**
```markdown
## Files

| File | Description |
|------|-------------|
| bth.ksy | Base Transport Header |
| reth.ksy | RDMA Extended Transport Header |
| aeth.ksy | ACK Extended Transport Header |
| deth.ksy | Datagram Extended Transport Header |
| immdt.ksy | Immediate Data |
| atomiceth.ksy | Atomic Extended Transport Header |
| atomicacketh.ksy | Atomic Acknowledge Extended Transport Header |
| icrc.ksy | Invariant CRC |
```

**Recommendation:** Add protocols/ directory:
```markdown
## Files

### Transport Headers (transport/)

| File | Description |
|------|-------------|
| bth.ksy | Base Transport Header |
| ... |

### Protocol State Machines (protocols/)

| File | Description |
|------|-------------|
| qp_state_machine.ksy | Queue Pair State Machine |
```

---

## Work Items Created

These issues are tracked in `analysis/packet_taxonomy/packet_taxonomy.md` as work items W-12-001 through W-12-018.

---

## References

- InfiniBand Architecture Specification Volume 1, Release 1.4
- RoCEv2 Annex A17 (IBTA)
- `earlysim/datamodel/protocols/roce/README.md`
