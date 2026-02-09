# Ethernet Datamodel Issues

**Document**: Issues identified during Ethernet datamodel review  
**Created**: 2026-01-28  
**Source**: `earlysim/datamodel/protocols/ethernet/`  
**References**: IEEE 802.3, IEEE 802.1Q, RFC 791, RFC 768, RFC 793, RFC 8200

---

## Summary

| ID | Severity | File | Issue | Status |
|----|----------|------|-------|--------|
| E-001 | Medium | All 6 files | Missing x-related-headers cross-references | Closed |
| E-002 | Low | All 6 files | Missing x-spec metadata for specification traceability | Closed |
| E-003 | Low | All 6 files | Missing x-packet metadata for layer/category/constraints | Closed |
| E-004 | Medium | ethernet_ii.ksy | Max frame size 9216 vs PMR hardware max 10240 | Closed (Not an issue) |
| E-005 | Low | vlan_802_1q.ksy | Header size documentation confusing (4 vs 6 bytes) | Closed |
| E-006 | Low | README.md | Outdated placeholder status, missing file list | Closed |
| E-007 | Low | udp.ksy | Missing RoCE cross-reference for port 4791 | Closed |
| E-008 | Low | ipv6.ksy | Missing dst_addr_hash instance for RSS symmetry | Closed |
| E-009 | Low | tcp.ksy | Reserved bits not extracted as instance | Closed |
| E-010 | Medium | link/*.ksy | IEEE 802.3 frame format support | Closed |
| E-011 | Medium | ipv4.ksy, ipv6.ksy | RSS hash algorithm documentation | Closed |
| E-012 | Low | ethernet_ii.ksy | VLAN cross-reference description could be clearer | Closed |
| E-013 | Low | ipv4.ksy | Missing VLAN cross-reference | Closed |
| E-014 | Low | ipv6.ksy | Missing VLAN cross-reference | Closed |
| E-015 | Low | tcp.ksy | Missing RSS cross-reference | Closed |
| E-016 | Low | udp.ksy | Missing RSS cross-reference | Closed |
| E-017 | Low | ipv6.ksy | Stale W-13-011 reference in comment | Closed |
| E-018 | Low | README.md | Incorrect VLAN file reference in protocol stack | Closed |
| E-019 | Low | tcp.ksy, udp.ksy | rss_hash_input_l4 documentation inconsistency | Closed |
| E-020 | Medium | hash_algorithm.ksy | Enum reference syntax verification needed | Closed |
| E-021 | Medium | toeplitz_key.ksy | Type casting syntax verification needed | Closed |

---

## Issue Details

### E-001: Missing Cross-References (x-related-headers) - All Files (Medium)

**Files affected:** All 6 .ksy files in ethernet/

**Problem:** None of the ethernet files have `x-related-headers` sections to cross-reference related files, unlike the RoCE datamodel which has comprehensive cross-references between all transport headers.

**Impact:** Makes it difficult to understand protocol relationships and packet structure.

**Recommendation:** Add x-related-headers to establish relationships:

```yaml
# ethernet_ii.ksy
x-related-headers:
  - file: "vlan_802_1q.ksy"
    description: "802.1Q VLAN tag - inserted after src_mac when ether_type=0x8100"
  - file: "../network/ipv4.ksy"
    description: "IPv4 header - payload when ether_type=0x0800"
  - file: "../network/ipv6.ksy"
    description: "IPv6 header - payload when ether_type=0x86DD"

# vlan_802_1q.ksy
x-related-headers:
  - file: "ethernet_ii.ksy"
    description: "Ethernet II frame - VLAN tag follows src_mac"
  - file: "../network/ipv4.ksy"
    description: "IPv4 header - payload when inner ether_type=0x0800"
  - file: "../network/ipv6.ksy"
    description: "IPv6 header - payload when inner ether_type=0x86DD"

# ipv4.ksy
x-related-headers:
  - file: "../link/ethernet_ii.ksy"
    description: "Ethernet II frame - encapsulates IPv4"
  - file: "../transport/tcp.ksy"
    description: "TCP header - payload when protocol=6"
  - file: "../transport/udp.ksy"
    description: "UDP header - payload when protocol=17"

# ipv6.ksy
x-related-headers:
  - file: "../link/ethernet_ii.ksy"
    description: "Ethernet II frame - encapsulates IPv6"
  - file: "../transport/tcp.ksy"
    description: "TCP header - payload when next_header=6"
  - file: "../transport/udp.ksy"
    description: "UDP header - payload when next_header=17"

# tcp.ksy
x-related-headers:
  - file: "../network/ipv4.ksy"
    description: "IPv4 header - encapsulates TCP (protocol=6)"
  - file: "../network/ipv6.ksy"
    description: "IPv6 header - encapsulates TCP (next_header=6)"

# udp.ksy
x-related-headers:
  - file: "../network/ipv4.ksy"
    description: "IPv4 header - encapsulates UDP (protocol=17)"
  - file: "../network/ipv6.ksy"
    description: "IPv6 header - encapsulates UDP (next_header=17)"
  - file: "../../roce/transport/bth.ksy"
    description: "RoCEv2 BTH - payload when dst_port=4791"
```

---

### E-002: Missing x-spec Metadata - All Files (Low)

**Files affected:** All 6 .ksy files in ethernet/

**Problem:** No `x-spec` metadata blocks for specification traceability, unlike RoCE files which reference IB Spec sections and tables.

**Current state:** Files have RFC/IEEE references in doc blocks but not in structured metadata.

**Recommendation:** Add x-spec blocks:

```yaml
# ethernet_ii.ksy
x-spec:
  spec_name: "IEEE 802.3"
  spec_version: "2022"
  section: "Section 3.1.1"
  description: "MAC frame format"

# vlan_802_1q.ksy
x-spec:
  spec_name: "IEEE 802.1Q"
  spec_version: "2022"
  section: "Section 9"
  table: "Table 9-2"
  description: "VLAN tag format"

# ipv4.ksy
x-spec:
  spec_name: "RFC 791"
  spec_version: "1981"
  section: "Section 3.1"
  description: "Internet Header Format"

# ipv6.ksy
x-spec:
  spec_name: "RFC 8200"
  spec_version: "2017"
  section: "Section 3"
  description: "IPv6 Header Format"

# tcp.ksy
x-spec:
  spec_name: "RFC 793"
  spec_version: "1981"
  section: "Section 3.1"
  description: "Header Format"
  related_rfcs: ["RFC 7323", "RFC 3168"]

# udp.ksy
x-spec:
  spec_name: "RFC 768"
  spec_version: "1980"
  section: "Format"
  description: "User Datagram Header Format"
```

---

### E-003: Missing x-packet Metadata - All Files (Low)

**Files affected:** All 6 .ksy files in ethernet/

**Problem:** No `x-packet` metadata blocks for layer/category/constraints, unlike RoCE files which have comprehensive packet metadata.

**Recommendation:** Add x-packet blocks with layer, size, and constraints:

```yaml
# Example for ethernet_ii.ksy
x-packet:
  layer: "link"
  sublayer: "ethernet"
  category: "frame_header"
  size_bytes: 14
  size_bits: 112
  
  constraints:
    - "Minimum frame size: 64 bytes (with padding)"
    - "Maximum frame size: 10240 bytes (PMR hardware limit)"
    - "EtherType >= 0x0600 distinguishes from IEEE 802.3 length field"
  
  usage:
    - "Encapsulates all higher-layer protocols"
    - "Provides MAC addressing for local delivery"
    - "EtherType identifies payload protocol"
```

---

### E-004: Maximum Frame Size - CLOSED (Not an Issue)

**File:** `ethernet_ii.ksy`, lines 13-14

**Current:**
```
Frame size constraints (FR-030):
- Minimum: 64 bytes (with padding)
- Maximum: 9216 bytes (jumbo frames)
```

**Original concern:** The 9216 byte maximum appears to conflict with PMR hardware max of 10240 bytes.

**Resolution:** This is NOT a conflict. It is acceptable (and correct) for hardware to support a maximum MTU larger than what individual protocols specify. The key requirements are:
1. Hardware max >= protocol max (satisfied: 10240 >= 9216)
2. Hardware must support the maximum MTU of any protocol it claims to support
3. Individual protocols may document smaller limits than hardware supports

The 9216 byte value in `ethernet_ii.ksy` correctly documents the typical jumbo frame maximum for standard Ethernet, which is a protocol-level constraint independent of PMR hardware capabilities.

**Status:** CLOSED - Not an issue.

---

### E-005: vlan_802_1q.ksy Header Size Inconsistency (Low)

**File:** `vlan_802_1q.ksy`, lines 23-37 and 72-79

**Current seq section:**
```yaml
seq:
  - id: tpid
    type: u2        # 2 bytes
  - id: tci
    type: u2        # 2 bytes
  - id: ether_type
    type: u2        # 2 bytes = 6 bytes total
```

**Current instances:**
```yaml
header_size:
  value: 4
  doc: VLAN tag size in bytes (TPID + TCI)

full_header_size:
  value: 6
  doc: Full VLAN header including inner EtherType
```

**Problem:** The `seq` section parses 6 bytes (TPID + TCI + ether_type), but `header_size` says 4 bytes. This is technically correct (the VLAN tag itself is 4 bytes), but confusing because:
1. The file parses more than just the VLAN tag
2. The inner EtherType is part of the original Ethernet II header, not the VLAN tag

**Recommendation:** Clarify documentation:
```yaml
header_size:
  value: 4
  doc: |
    VLAN tag size in bytes (TPID + TCI only).
    Note: This file also parses the inner EtherType (2 bytes) for convenience,
    which is technically part of the encapsulated frame, not the VLAN tag.

total_parsed_size:
  value: 6
  doc: Total bytes parsed by this file (TPID + TCI + inner EtherType)
```

Or restructure to only parse the 4-byte VLAN tag and leave EtherType parsing to the caller.

---

### E-006: README.md Outdated (Low)

**File:** `README.md`

**Current:**
```markdown
## Status

Placeholder - to be implemented
```

**Problem:** The README says "Placeholder - to be implemented" but 6 .ksy files are already implemented. Also missing actual file list. Additionally lists "IEEE 802.3 frames" and "Common application protocols" which are not implemented.

**Recommendation:** Update README (revised 2026-01-28):
- Remove placeholder status
- Remove "IEEE 802.3 frames" (deferred per W-13-010)
- Remove "Common application protocols" (not implemented)
- Add protocol stack diagram
- Add file tables with sizes and descriptions
- Update references to match x-spec metadata

```markdown
# Ethernet Protocol Taxonomy

Kaitai Struct definitions for standard Ethernet protocol headers.

## Overview

This taxonomy defines packet formats for standard Ethernet protocols used by PMR for:
- Standard Ethernet NIC functionality
- RoCEv2 encapsulation (UDP port 4791)
- RSS hash computation
- Checksum offload

## Protocol Stack

+------------------+
|   Application    |
+------------------+
| TCP (tcp.ksy)    |  Transport Layer
| UDP (udp.ksy)    |
+------------------+
| IPv4 (ipv4.ksy)  |  Network Layer
| IPv6 (ipv6.ksy)  |
+------------------+
| VLAN (vlan.ksy)  |  Link Layer (optional)
| Ethernet II      |
+------------------+

## Files

### Link Layer (link/)

| File | Size | Description |
|------|------|-------------|
| ethernet_ii.ksy | 14 bytes | Ethernet II (DIX) frame header |
| vlan_802_1q.ksy | 4 bytes | IEEE 802.1Q VLAN tag |

### Network Layer (network/)

| File | Size | Description |
|------|------|-------------|
| ipv4.ksy | 20-60 bytes | IPv4 header (RFC 791) |
| ipv6.ksy | 40 bytes | IPv6 fixed header (RFC 8200) |

### Transport Layer (transport/)

| File | Size | Description |
|------|------|-------------|
| tcp.ksy | 20-60 bytes | TCP header (RFC 793) |
| udp.ksy | 8 bytes | UDP header (RFC 768) |

## References

- IEEE 802.3-2022 - Ethernet
- IEEE 802.1Q-2022 - VLAN Tagging
- RFC 791 - Internet Protocol (IPv4)
- RFC 8200 - Internet Protocol, Version 6 (IPv6)
- RFC 793 - Transmission Control Protocol (TCP)
- RFC 768 - User Datagram Protocol (UDP)
```

### Transport Layer (transport/)

| File | Size | Description |
|------|------|-------------|
| tcp.ksy | 20-60 bytes | TCP header (RFC 793) |
| udp.ksy | 8 bytes | UDP header (RFC 768) |

## References

- IEEE 802.3 - Ethernet
- IEEE 802.1Q - VLAN Tagging
- RFC 791 - IPv4
- RFC 8200 - IPv6
- RFC 793 - TCP
- RFC 768 - UDP
```

---

### E-007: Missing RoCE Cross-Reference in UDP (Low)

**File:** `udp.ksy`, lines 68-70

**Current:**
```yaml
is_roce:
  value: dst_port == 4791
  doc: True if RoCEv2 traffic
```

**Problem:** References RoCEv2 but doesn't cross-reference the RoCE datamodel files. When `is_roce` is true, the UDP payload is a RoCEv2 packet starting with BTH.

**Recommendation:** Add x-related-headers reference:
```yaml
x-related-headers:
  - file: "../network/ipv4.ksy"
    description: "IPv4 header - encapsulates UDP (protocol=17)"
  - file: "../network/ipv6.ksy"
    description: "IPv6 header - encapsulates UDP (next_header=17)"
  - file: "../../roce/transport/bth.ksy"
    description: "RoCEv2 Base Transport Header - UDP payload when dst_port=4791"
```

And update the is_roce doc:
```yaml
is_roce:
  value: dst_port == 4791
  doc: |
    True if RoCEv2 traffic (IANA assigned port).
    When true, UDP payload contains RoCEv2 packet starting with BTH.
    See: roce/transport/bth.ksy
```

---

### E-008: IPv6 Missing dst_addr_hash Instance (Low)

**File:** `ipv6.ksy`, lines 91-101

**Current:** Has `src_addr_hash` instance but no `dst_addr_hash`.

```yaml
src_addr_hash:
  value: >-
    ((src_addr[0].as<u8> << 56) | ... ) ^
    ((src_addr[8].as<u8> << 56) | ... )
  doc: Source address hash (XOR of high/low 64 bits)
```

**Problem:** For RSS hash computation, both source and destination address hashes are typically needed. The file has `src_addr_hash` but no corresponding `dst_addr_hash`.

**Recommendation:** Add `dst_addr_hash` instance:
```yaml
dst_addr_hash:
  value: >-
    ((dst_addr[0].as<u8> << 56) | (dst_addr[1].as<u8> << 48) |
     (dst_addr[2].as<u8> << 40) | (dst_addr[3].as<u8> << 32) |
     (dst_addr[4].as<u8> << 24) | (dst_addr[5].as<u8> << 16) |
     (dst_addr[6].as<u8> << 8)  | dst_addr[7].as<u8>) ^
    ((dst_addr[8].as<u8> << 56) | (dst_addr[9].as<u8> << 48) |
     (dst_addr[10].as<u8> << 40) | (dst_addr[11].as<u8> << 32) |
     (dst_addr[12].as<u8> << 24) | (dst_addr[13].as<u8> << 16) |
     (dst_addr[14].as<u8> << 8)  | dst_addr[15].as<u8>)
  doc: Destination address hash (XOR of high/low 64 bits)

rss_hash_input_l3:
  value: src_addr_hash ^ dst_addr_hash
  doc: L3 hash input for RSS (XOR of address hashes)
```

---

### E-009: TCP Reserved Bits Not Extracted (Low)

**File:** `tcp.ksy`, lines 34-36

**Current:**
```yaml
- id: data_offset_reserved_flags
  type: u2
  doc: Data offset (4 bits) + Reserved (3 bits) + Flags (9 bits)
```

**Problem:** The reserved bits (3 bits between data offset and flags) are mentioned in doc but not extracted as an instance. Per RFC 793, these must be zero. Extracting them allows validation.

**Recommendation:** Add reserved instance and validation:
```yaml
# Extract reserved bits (bits 11-9)
reserved:
  value: (data_offset_reserved_flags >> 9) & 0x07
  doc: Reserved bits (3 bits, must be zero per RFC 793)

is_valid_reserved:
  value: reserved == 0
  doc: True if reserved bits are zero (valid per RFC 793)
```

---

### E-010: IEEE 802.3 Frame Format Support (Medium) - CLOSED

**Files:** `link/ethernet_802_3.ksy`, `link/llc.ksy`, `link/snap.ksy`

**Original Problem:** Only Ethernet II (DIX) format was implemented. IEEE 802.3 uses a length field instead of EtherType when the value is < 1536 (0x0600).

**Decision:** Support IEEE 802.3 frame format because it is still used for control-plane/discovery/L2 control traffic for Ethernet.

**Resolution:** Implemented Option 1 - created separate files for IEEE 802.3 and LLC:

1. **New files created:**
   - `ethernet_802_3.ksy` - IEEE 802.3 MAC frame with length field
   - `llc.ksy` - IEEE 802.2 Logical Link Control header
   - `snap.ksy` - SNAP extension for EtherType over LLC

2. **Updated files:**
   - `ethernet_ii.ksy` - Added cross-reference to 802.3, added `is_ethernet_ii` and `is_ieee_802_3` disambiguation instances
   - `vlan_802_1q.ksy` - Added cross-references to 802.3 and LLC
   - `README.md` - Updated protocol stack diagram, file list, and references

3. **Use cases supported:**
   - Spanning Tree Protocol (STP) - LLC DSAP/SSAP = 0x42
   - OSI protocols (IS-IS, CLNP, ES-IS) - LLC DSAP/SSAP = 0xFE
   - IP over 802 networks (RFC 1042) - LLC + SNAP with EtherType
   - NetBIOS - LLC DSAP/SSAP = 0xF0

4. **Validation:** All 12 Ethernet .ksy files pass validation with `validate_ksy.py`

**Status:** CLOSED - Commit 48a3880f, pushed to origin/main (2026-01-28).

---

### E-011: RSS Hash Algorithm Documentation (Medium) - CLOSED

**Files affected:** `ipv4.ksy`, `ipv6.ksy`, new `rss/` directory

**Original concern:** Both files used simple XOR for RSS hash computation without documenting that production RSS uses Toeplitz hash.

**Resolution:** Created comprehensive RSS hash documentation:

1. **New `rss/` directory** with 4 files:
   - `hash_algorithm.ksy` - Algorithm selection (CRC32, XOR, Toeplitz) with CSR mapping
   - `toeplitz_key.ksy` - 40-byte Toeplitz key format with CSR mapping
   - `hash_input.ksy` - Hash input formats for IPv4/IPv6 L3/L4 tuples
   - `README.md` - RSS overview with CSR references and implementation notes

2. **Updated `ipv4.ksy` and `ipv6.ksy`**:
   - Added RSS cross-references in x-related-headers
   - Updated rss_hash_input_l3 doc to clarify XOR is for illustration only
   - Added references to rss/ directory for production RSS documentation

3. **CSR References documented**:
   - Algorithm select: `rx_classify.pdp_hash_cfg` @ 0x3014
   - Toeplitz key: `ethernet.rss_hash_key[0-9]` @ 0x4010-0x4034

4. **Implementation reference**:
   - C code: `sim/hw/asics/pmr/device/hw/net/cn7000-pcie-ethernet.c`
   - Function: `cn7000_eth_toeplitz_hash()`

**Status:** CLOSED - Commit f18cc8a5, pushed to origin/main.

---

## Second Review Issues (2026-01-28)

The following issues were identified during a second review of the Ethernet datamodel after the initial fixes were applied.

---

### E-012: ethernet_ii.ksy VLAN Cross-Reference Description (Low) - CLOSED

**File:** `ethernet_ii.ksy`, x-related-headers

**Found:** Second review, 2026-01-28

**Issue:** The VLAN cross-reference description could be clearer about the relationship between ether_type=0x8100 and the inner ether_type in the VLAN tag.

**Resolution:** Updated description to clarify that when ether_type=0x8100, the VLAN tag follows and its inner ether_type field identifies the payload protocol.

**Status:** CLOSED - Commit 4cf0bf00, pushed to origin/main.

---

### E-013: ipv4.ksy Missing VLAN Cross-Reference (Low) - CLOSED

**File:** `ipv4.ksy`, x-related-headers

**Found:** Second review, 2026-01-28

**Issue:** ipv4.ksy references ethernet_ii.ksy but not vlan_802_1q.ksy. IPv4 can be encapsulated in VLAN-tagged frames (inner ether_type=0x0800).

**Resolution:** Added x-related-headers reference to vlan_802_1q.ksy with ether_type=0x0800.

**Status:** CLOSED - Commit 2a6c496f, pushed to origin/main.

---

### E-014: ipv6.ksy Missing VLAN Cross-Reference (Low) - CLOSED

**File:** `ipv6.ksy`, x-related-headers

**Found:** Second review, 2026-01-28

**Issue:** ipv6.ksy references ethernet_ii.ksy but not vlan_802_1q.ksy. IPv6 can be encapsulated in VLAN-tagged frames (inner ether_type=0x86DD).

**Resolution:** Added x-related-headers reference to vlan_802_1q.ksy with ether_type=0x86DD.

**Status:** CLOSED - Commit 95d80292, pushed to origin/main.

---

### E-015: tcp.ksy Missing RSS Cross-Reference (Low) - CLOSED

**File:** `tcp.ksy`, x-related-headers

**Found:** Second review, 2026-01-28

**Issue:** tcp.ksy only references ipv4.ksy and ipv6.ksy. It should also reference RSS files since TCP ports are used in L3+L4 hash computation.

**Resolution:** Added x-related-headers reference to rss/hash_input.ksy.

**Status:** CLOSED - Commit d87bece5, pushed to origin/main.

---

### E-016: udp.ksy Missing RSS Cross-Reference (Low) - CLOSED

**File:** `udp.ksy`, x-related-headers

**Found:** Second review, 2026-01-28

**Issue:** udp.ksy references RoCE BTH but not RSS files, even though UDP ports are used in L3+L4 hash computation.

**Resolution:** Added x-related-headers reference to rss/hash_input.ksy.

**Status:** CLOSED - Commit 4ff530a5, pushed to origin/main.

---

### E-017: ipv6.ksy Stale W-13-011 Reference (Low) - CLOSED

**File:** `ipv6.ksy`, lines 141-143

**Found:** Second review, 2026-01-28

**Issue:** The comment referenced "W-13-011 for discussion" but W-13-011 is now closed and the RSS documentation is in the rss/ directory.

**Resolution:** Updated comment to reference "rss/ directory for documentation" instead of the closed work item.

**Status:** CLOSED - Commit a0273296, pushed to origin/main.

---

### E-018: README.md Incorrect VLAN File Reference (Low) - CLOSED

**File:** `README.md`, line 25

**Found:** Second review, 2026-01-28

**Issue:** The protocol stack diagram showed "VLAN (vlan.ksy)" but the actual file is named `vlan_802_1q.ksy`.

**Resolution:** Updated to "VLAN (802.1Q)" to use consistent abbreviation matching the IEEE standard name.

**Status:** CLOSED - Commit c2dfdfe9, pushed to origin/main.

---

### E-019: tcp.ksy and udp.ksy rss_hash_input_l4 Documentation Inconsistency (Low) - CLOSED

**Files:** `tcp.ksy`, `udp.ksy`

**Found:** Second review, 2026-01-28

**Issue:** Unlike ipv4.ksy and ipv6.ksy which have detailed documentation about production RSS using Toeplitz, the tcp.ksy and udp.ksy files had minimal documentation for rss_hash_input_l4.

**Resolution:** Updated both files with expanded documentation matching the style used in ipv4.ksy and ipv6.ksy. Now clarifies that XOR is for illustration only and references rss/ directory for production RSS documentation.

**Status:** CLOSED - Commit 98d2461a, pushed to origin/main.

---

### E-020: hash_algorithm.ksy Enum Reference Syntax (Medium) - CLOSED

**File:** `hash_algorithm.ksy`, lines 126-135

**Found:** Second review, 2026-01-28

**Issue:** The `algorithm::crc32` enum reference syntax needed verification with the Kaitai Struct compiler.

**Resolution:** Created `datamodel/scripts/validate_ksy.py` validation script that:
1. Strips custom x-* metadata keys (not recognized by ksc)
2. Runs ksc compiler on stripped content
3. Reports pass/fail status

Validation confirmed the enum syntax is correct. The `algorithm::crc32` syntax compiles successfully and generates proper Python code:
```python
self._m_is_crc32 = self.hash_func == TestEnum.Algorithm.crc32
```

All 9 Ethernet .ksy files pass validation.

**Status:** CLOSED - Commit 9dc6a627, pushed to origin/main.

---

### E-021: toeplitz_key.ksy Type Casting Syntax (Medium) - CLOSED

**File:** `toeplitz_key.ksy`, lines 157-215

**Found:** Second review, 2026-01-28

**Issue:** The `.as<u4>` type casting syntax for byte array elements needed verification with the Kaitai Struct compiler.

**Resolution:** Used `datamodel/scripts/validate_ksy.py` validation script to verify compilation.

Validation confirmed the type casting syntax is correct. The `.as<u4>` syntax compiles successfully and generates proper Python code using `KaitaiStream.byte_array_index()`:
```python
self._m_segment_0 = ((KaitaiStream.byte_array_index(self.key, 0) << 24 | 
                      KaitaiStream.byte_array_index(self.key, 1) << 16) | 
                      KaitaiStream.byte_array_index(self.key, 2) << 8) | 
                      KaitaiStream.byte_array_index(self.key, 3)
```

All 9 Ethernet .ksy files pass validation.

**Status:** CLOSED - Commit 9dc6a627, pushed to origin/main.

---

## Work Items Created

These issues are tracked in `analysis/packet_taxonomy/packet_taxonomy.md` as work items W-13-001 through W-13-011.

---

## References

- IEEE 802.3-2022 - Ethernet
- IEEE 802.1Q-2022 - VLAN Tagging
- RFC 791 - Internet Protocol (IPv4)
- RFC 8200 - Internet Protocol, Version 6 (IPv6)
- RFC 793 - Transmission Control Protocol (TCP)
- RFC 768 - User Datagram Protocol (UDP)
- `earlysim/datamodel/protocols/ethernet/README.md`
