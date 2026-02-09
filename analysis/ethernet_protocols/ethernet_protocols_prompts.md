# Ethernet Protocols Session Prompts

**Document**: Session prompts for Ethernet datamodel work  
**Created**: 2026-01-28

---

## Session: 2026-01-28 (Ethernet Datamodel Review and RSS Hash Documentation)

### Session Summary

Completed Ethernet datamodel review (W-13-001 through W-13-009) and RSS hash algorithm documentation (W-13-011). Pushed 9 commits to origin/main.

### Prompt for New Session

```
Continue the PMR Packet Taxonomy Documentation project - Ethernet Datamodel.

Working directory: /home/matkins/CN7000/

**Session completed 2026-01-28:**

Pushed 16 commits to earlysim origin/main for Ethernet datamodel improvements:

| Commit | Work Item | Description |
|--------|-----------|-------------|
| 5163deec | W-13-001 | Added x-related-headers to all 6 ethernet .ksy files |
| ac03b79e | W-13-002 | Added x-spec metadata with IEEE/RFC references |
| ba8829c9 | W-13-003 | Added x-packet metadata with layer/size/constraints/usage |
| 0d94d0b7 | W-13-005 | Clarified vlan_802_1q.ksy header size (4-byte tag vs 6 bytes parsed) |
| 71777456 | W-13-007 | Added RoCE cross-reference to udp.ksy is_roce instance |
| b9e51104 | W-13-009 | Added reserved bits extraction and validation to tcp.ksy |
| c4d9ad6e | W-13-008 | Added dst_addr_hash and rss_hash_input_l3 to ipv6.ksy |
| 9939fa29 | W-13-006 | Updated ethernet/README.md with file list, protocol stack |
| f18cc8a5 | W-13-011 | RSS hash algorithm documentation (new rss/ directory) |
| 4cf0bf00 | W-13-012 | Clarified VLAN cross-ref description in ethernet_ii.ksy |
| 2a6c496f | W-13-013 | Added VLAN cross-ref to ipv4.ksy |
| 95d80292 | W-13-014 | Added VLAN cross-ref to ipv6.ksy |
| d87bece5 | W-13-015 | Added RSS cross-ref to tcp.ksy |
| 4ff530a5 | W-13-016 | Added RSS cross-ref to udp.ksy |
| a0273296 | W-13-017 | Fixed stale W-13-011 reference in ipv6.ksy |
| c2dfdfe9 | W-13-018 | Fixed README.md VLAN filename reference |
| 98d2461a | W-13-019 | Improved rss_hash_input_l4 doc in tcp.ksy and udp.ksy |
| 9dc6a627 | W-13-020, W-13-021 | Added Kaitai validation script, verified syntax |
| 48a3880f | W-13-010 | IEEE 802.3/LLC/SNAP frame support |

**Work Items Closed:**
- W-13-001: Ethernet x-related-headers cross-references
- W-13-002: Ethernet x-spec metadata
- W-13-003: Ethernet x-packet metadata
- W-13-004: Closed as not an issue (hardware max >= protocol max is correct)
- W-13-005: VLAN header size documentation
- W-13-006: Ethernet README.md update
- W-13-007: UDP is_roce cross-reference
- W-13-008: IPv6 dst_addr_hash instance
- W-13-009: TCP reserved bits extraction
- W-13-011: RSS hash algorithm documentation
- W-13-012: Clarified VLAN cross-ref description in ethernet_ii.ksy
- W-13-013: Added VLAN cross-ref to ipv4.ksy
- W-13-014: Added VLAN cross-ref to ipv6.ksy
- W-13-015: Added RSS cross-ref to tcp.ksy
- W-13-016: Added RSS cross-ref to udp.ksy
- W-13-017: Fixed stale W-13-011 reference in ipv6.ksy
- W-13-018: Fixed README.md VLAN filename reference
- W-13-019: Improved rss_hash_input_l4 doc consistency
- W-13-020: Verified hash_algorithm.ksy enum syntax with validation script
- W-13-021: Verified toeplitz_key.ksy type casting syntax with validation script
- W-13-010: IEEE 802.3/LLC/SNAP frame support for control-plane protocols

**RSS Hash Documentation (W-13-011):**

Created new `rss/` directory with comprehensive RSS hash documentation:
- `datamodel/protocols/ethernet/rss/hash_algorithm.ksy` - Algorithm selection (CRC32, XOR, Toeplitz)
- `datamodel/protocols/ethernet/rss/toeplitz_key.ksy` - 40-byte Toeplitz key format with CSR mapping
- `datamodel/protocols/ethernet/rss/hash_input.ksy` - Hash input formats (IPv4/IPv6 L3/L4 tuples)
- `datamodel/protocols/ethernet/rss/README.md` - RSS overview with CSR references

Updated ipv4.ksy and ipv6.ksy with RSS cross-references and improved rss_hash_input_l3 documentation.

**RSS CSR References:**
- Algorithm select: `rx_classify.pdp_hash_cfg` @ 0x3014
  - hash_func[1:0]: 0=CRC32, 1=XOR, 2=Toeplitz
  - hash_seed[31:8]: 24-bit seed (default 0x5A5A5A)
- Toeplitz key: `ethernet.rss_hash_key[0-9]` @ 0x4010-0x4034 (40 bytes)

**Toeplitz implementation location:**
- C code: `sim/hw/asics/pmr/device/hw/net/cn7000-pcie-ethernet.c` function `cn7000_eth_toeplitz_hash()`
- Original author: Charles Archer (commit 588c5c40, 2025-12-09)

**Kaitai Validation Script:**
- Location: `earlysim/datamodel/scripts/validate_ksy.py`
- Purpose: Validates .ksy files by stripping custom x-* keys and running ksc compiler
- Usage: `python validate_ksy.py --all datamodel/protocols/ethernet/`
- All 9 Ethernet and 9 RoCE files pass validation

**IEEE 802.3/LLC/SNAP Support (W-13-010):**

New files created for control-plane and discovery protocols:
- `link/ethernet_802_3.ksy` - IEEE 802.3 MAC frame (length field < 0x0600)
- `link/llc.ksy` - IEEE 802.2 Logical Link Control header
- `link/snap.ksy` - SNAP extension for EtherType over LLC

Use cases supported:
- Spanning Tree Protocol (STP) - LLC DSAP/SSAP = 0x42
- OSI protocols (IS-IS, CLNP, ES-IS) - LLC DSAP/SSAP = 0xFE
- IP over 802 networks (RFC 1042) - LLC + SNAP with EtherType

**Open Work Items:**

All W-13 Ethernet datamodel work items are now closed.

**Key tracking files:**
- `analysis/packet_taxonomy/packet_taxonomy.md` - Master work item index
- `analysis/ethernet_protocols/ethernet_protocols_issues.md` - Ethernet-specific issues
- `analysis/ethernet_protocols/ethernet_protocols_prompts.md` - Session prompts (this file)
```

---

## Previous Sessions

(No previous sessions recorded for Ethernet protocols work)
