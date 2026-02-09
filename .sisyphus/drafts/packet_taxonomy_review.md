# Packet Taxonomy Review: Datamodel vs Documentation

## Summary

| Protocol | Datamodel Files | Datamodel Lines | Doc Last Updated | Status |
|----------|-----------------|-----------------|------------------|--------|
| UALink | 38 KSY | 6,023 | 2026-01-22 | **NEEDS UPDATE** |
| Ethernet | 12 KSY | 1,993 | 2026-01-23 | **NEEDS UPDATE** |
| RoCE | 9 KSY | 1,752 | 2026-01-23 | OK |
| UE | 100 KSY | 18,225 | Various | OK |
| Cornelis | 9 KSY | 1,957 | 2026-01-26 | OK |
| HSI | 22 KSY | N/A | 2026-01-23 | OK |

---

## 1. UALink (packet_taxonomy_ualink.md)

### Current State in Doc
- Last Updated: 2026-01-22
- Shows 38 packets across 5 layers
- Layer counts: UPLI 8, Transaction 9, Data Link 12, Physical 4, Security 5

### Datamodel Reality
- **38 KSY files** (matches doc)
- **6,023 total lines** (significant expansion since doc was written)
- **6 YAML reference files** in `reference/field_definitions/`:
  - tl_flit.yaml
  - dl_flit.yaml
  - flow_control_field.yaml
  - link_state.yaml
  - upli_request_channel.yaml
  - response_field.yaml (NEW - added in W-14-009)

### Changes Needed
1. **Update "Last Updated" date** to 2026-01-30
2. **Add YAML Reference Files section** documenting the 6 reference files
3. **Add note about W-14 work items** that expanded:
   - Security layer (W-14-004): 5 files expanded to ~1,660 lines
   - response_field.ksy (W-14-009): 52→310 lines with bit-level parsing
   - flit_header.ksy (W-14-010): 90→165 lines with top-level seq
   - data_half_flit.ksy (W-14-008): 40→142 lines
   - message_half_flit.ksy (W-14-008): 37→148 lines
4. **Add x-related-headers note** (W-14-007): All 37 KSY files now have cross-references

---

## 2. Ethernet (packet_taxonomy_ethernet.md)

### Current State in Doc
- Last Updated: 2026-01-23
- Shows 6 files: ethernet_ii, vlan_802_1q, ipv4, ipv6, udp, tcp
- Missing RSS and IEEE 802.3 files

### Datamodel Reality
- **12 KSY files** (doc shows only 6)
- **1,993 total lines**

**Files in datamodel:**
```
./link/ethernet_802_3.ksy    (NEW - W-13-010)
./link/ethernet_ii.ksy
./link/llc.ksy               (NEW - W-13-010)
./link/snap.ksy              (NEW - W-13-010)
./link/vlan_802_1q.ksy
./network/ipv4.ksy
./network/ipv6.ksy
./rss/hash_algorithm.ksy     (NEW - W-13-*)
./rss/hash_input.ksy         (NEW - W-13-*)
./rss/toeplitz_key.ksy       (NEW - W-13-*)
./transport/tcp.ksy
./transport/udp.ksy
```

### Changes Needed
1. **Update "Last Updated" date** to 2026-01-30
2. **Add Section 2.3: IEEE 802.3/LLC/SNAP** (W-13-010):
   - ethernet_802_3.ksy - MAC frame with length field
   - llc.ksy - IEEE 802.2 LLC header
   - snap.ksy - SNAP extension
3. **Add Section 7: RSS (Receive Side Scaling)**:
   - hash_algorithm.ksy - Hash algorithm definitions
   - hash_input.ksy - RSS hash input fields
   - toeplitz_key.ksy - Toeplitz hash key format
4. **Update file count** from 6 to 12
5. **Update Datamodel Files table** in Cross-References section

---

## 3. RoCE (packet_taxonomy_rocev2.md)

### Current State in Doc
- Last Updated: 2026-01-23
- Shows 9 files

### Datamodel Reality
- **9 KSY files** (matches doc)
- **1,752 total lines**

**Files:**
```
./protocols/qp_state_machine.ksy
./transport/aeth.ksy
./transport/atomicacketh.ksy
./transport/atomiceth.ksy
./transport/bth.ksy
./transport/deth.ksy
./transport/icrc.ksy
./transport/immdt.ksy
./transport/reth.ksy
```

### Status: OK
- File count matches
- No significant changes needed
- May want to update date if any minor changes were made

---

## 4. UE (packet_taxonomy_ue_*.md)

### Current State in Docs
- packet_taxonomy_ue_ses.md: 2026-01-23
- packet_taxonomy_ue_pds.md: 2026-01-23
- packet_taxonomy_ue_cms_tss.md: 2026-01-26
- packet_taxonomy_ue_link.md: 2026-01-23

### Datamodel Reality
- **100 KSY files total**
- **18,225 total lines**

**Breakdown:**
- transport/ses: 27 files
- transport/pds: 30 files
- transport/cms: 15 files
- transport/tss: 9 files
- link: 16 files

### Status: OK
- Comprehensive coverage
- Recent updates (2026-01-26 for CMS/TSS)
- No significant gaps identified

---

## 5. Cornelis (packet_taxonomy_cornelis.md)

### Current State in Doc
- Last Updated: 2026-01-26
- Shows UFH-16, UFH-32, UE+, CSIG+, VxLAN+, Collective L2, Scale-Up L2

### Datamodel Reality
- **9 KSY files** (matches doc)
- **1,957 total lines**

**Files:**
```
./encapsulation/vxlan_plus.ksy
./link/cornelis_l2_prefix.ksy
./link/ue_plus.ksy
./network/collective_l2.ksy
./network/scaleup_l2.ksy
./network/ufh_16.ksy
./network/ufh_32.ksy
./transport/csig_plus.ksy
./transport/pkey.ksy
```

### Status: OK
- Recently updated (2026-01-26)
- File count matches
- UFH-16/UFH-32 restructured in W-04-005/W-04-006

---

## 6. HSI (packet_taxonomy_hsi.md)

### Current State in Doc
- Last Updated: 2026-01-23
- Shows PMR HSI formats

### Datamodel Reality
- **22 KSY files** across hw/asics/pmr, hw/asics/lnr, hw/ip/cornelis

**PMR HSI (10 files):**
- host_interface/: command_queue_segment, event_notification, notification_entry, qw_violation_event, receive_notification, send_completion, sgl_entry
- host_interface/fsms/: desc_state_machine, segbuf_state_machine
- pcie/: descriptors

**PMR Ethernet (4 files):**
- ethernet/: eth_rx_buffer_desc, eth_rx_cqe, eth_tx_cqe, eth_tx_wqe

**PMR HDM (2 files):**
- hdm/: hdm_request, hdm_response

**LNR (2 files):**
- hostpath/: command_descriptor, notification_entry

**IP Blocks (4 files):**
- ce/: descriptors, fsms/ce_scheduler_fsm
- ec/: descriptors, fsms/ec_cmd_fsm

### Status: OK
- Core HSI formats documented
- May want to add Ethernet offload and HDM sections in future

---

## Recommended Actions

### Priority 1: Update packet_taxonomy_ethernet.md
- Add 6 missing files (802.3, LLC, SNAP, RSS)
- Most significant gap

### Priority 2: Update packet_taxonomy_ualink.md
- Add YAML reference files section
- Update with W-14 work item completions
- Note significant line count increases

### Priority 3: Minor date updates
- Update "Last Updated" dates on all files to reflect review
