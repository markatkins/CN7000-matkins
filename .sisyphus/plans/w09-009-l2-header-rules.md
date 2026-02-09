# Plan: W-09-009 PMR L2 Header Selection Rules

**Created**: 2026-02-03  
**Estimated Effort**: 30 minutes  
**Type**: Documentation

---

## Objective

Document the rules for when PMR uses standard Ethernet vs Cornelis UE+ header, then close W-09-009.

---

## Research Findings

From CN7000 HFI Requirements document (Section 3941-4015):

### UE+ Header Selection (12-byte Cornelis L2)
- Both endpoints must support UE+ (link negotiation + peer capability)
- Uses Hierarchical MAC (HMAC) addresses from fabric management
- Internal fabric traffic between CN7000 NICs
- No gateway conversion between UE+ and standard UE

### Standard Ethernet Selection (14-byte Ethernet II)
- Peer doesn't support UE+ (non-Cornelis or standard UE endpoints)
- Standard UE over UDP encapsulation
- RoCEv2 traffic (always Ethernet + IP + UDP)
- Standard Ethernet services (PTP, management, netdev)
- Non-managed Ethernet configuration

### Key Architecture Principle
- HFI does NOT operate in a "mode"
- Applications can use RoCE, UE, and UE+ simultaneously
- Selection is per-destination via Address Vector (AV)
- Software (libfabric) hides the distinction from applications

---

## Tasks

### Task 1: Add L2 Header Selection Rules to packet_taxonomy_ue_plus_variants.md

**File**: `analysis/packet_taxonomy/packet_taxonomy_ue_plus_variants.md`

**Action**: Add new section after the introduction (around line 40) documenting L2 header selection rules.

**Content to add**:

```markdown
---

## 2. L2 Header Selection Rules

This section documents when PMR uses the Cornelis UE+ header vs standard Ethernet.

### 2.1 Decision Matrix

| Condition | L2 Header | Network Header | Notes |
|-----------|-----------|----------------|-------|
| Both endpoints support UE+ | UE+ (12B) | UFH-16/32 | Fabric-managed HMAC addressing |
| Peer is standard UE endpoint | Ethernet II (14B) | IPv4/IPv6 + UDP | Standard UE encapsulation |
| Peer is RoCEv2 endpoint | Ethernet II (14B) | IPv4/IPv6 + UDP | RoCEv2 always uses Ethernet |
| Standard Ethernet traffic | Ethernet II (14B) | IPv4/IPv6 | PTP, management, netdev |
| Non-managed configuration | Ethernet II (14B) | IPv4/IPv6 | No fabric management |

### 2.2 UE+ Header Conditions

PMR uses the UE+ header (12-byte Cornelis L2) when **ALL** of the following are true:

1. **Link negotiates UE+ capability**: The physical link must negotiate support for UE+
2. **Peer supports UE+**: The destination endpoint must have UE+ capability
3. **Fabric management active**: Hierarchical MAC (HMAC) addresses are assigned
4. **Address Vector configured for UE+**: Software has configured the AV for UE+ mode

### 2.3 Standard Ethernet Conditions

PMR uses standard Ethernet II (14-byte) when **ANY** of the following are true:

1. **Peer doesn't support UE+**: Non-Cornelis endpoints or standard UE implementations
2. **RoCEv2 protocol**: RoCEv2 always uses Ethernet + IPv4/IPv6 + UDP encapsulation
3. **Standard UE encapsulation**: When using UDP-based UE transport per UE Spec
4. **Ethernet services**: PTP (IEEE 1588), management traffic, netdev interfaces
5. **Non-managed mode**: When fabric management is not configured

### 2.4 Simultaneous Protocol Support

**Key Architecture Principle** (HFI_ARCH_003):
> "The HFI shall support simultaneous use of UE+ and standard Ethernet packets"

- PMR does **NOT** operate in a single protocol "mode"
- An application can use RoCE, UE, and UE+ simultaneously
- Selection is **per-destination** based on Address Vector (AV) configuration
- Software (libfabric) hides the L2 header distinction from applications
- Neither HFI nor switch performs UE+ ↔ UE gateway conversion

### 2.5 Address Vector Role

The libfabric Address Vector (AV) determines L2 header selection:

| AV Configuration | L2 Header | Addressing |
|------------------|-----------|------------|
| UE+ peer (HMAC) | UE+ 12B | 24-bit Hierarchical MAC |
| Standard UE peer | Ethernet II 14B | 48-bit MAC + IPv4/IPv6 |
| RoCEv2 peer | Ethernet II 14B | 48-bit MAC + IPv4/IPv6 |

### 2.6 Reference

- CN7000 HFI Requirements, Section "Introduction" (UE+ definition)
- CN7000 HFI Requirements, HFI_ARCH_003 (simultaneous protocol support)
- CN7000 HFI Requirements, "Protocol Processing Units" section
```

---

### Task 2: Update WORK_ITEMS.md - Remove W-09-009 from Open

**File**: `analysis/packet_taxonomy/WORK_ITEMS.md`

**Action**: Remove W-09-009 section from "## 1. Open Work Items"

**Lines to remove** (approximately lines 22-33):
```markdown
### W-09-009: PMR Standard Ethernet vs UE+ Header Rules

| Field | Value |
|-------|-------|
| **Status** | Pending |
| **Priority** | Medium |
| **Category** | Architecture |
| **Created** | 2026-01-23 |

**Description**: Define rules for when PMR uses standard Ethernet vs Cornelis UE+ header.

---
```

---

### Task 3: Update WORK_ITEMS.md - Add W-09-009 to Closed Section

**File**: `analysis/packet_taxonomy/WORK_ITEMS.md`

**Action**: Add W-09-009 closure entry to "## 5. Recently Closed Work Items" section (after W-10-015 entry)

**Content to add**:

```markdown
### W-09-009: PMR L2 Header Selection Rules (2026-02-03)

Documented rules for when PMR uses standard Ethernet vs Cornelis UE+ header:
- **UE+ (12B)**: Both endpoints support UE+, fabric-managed HMAC addressing, link negotiated
- **Ethernet II (14B)**: Peer doesn't support UE+, RoCEv2, standard UE over UDP, Ethernet services
- **Key principle**: HFI supports simultaneous use of all protocols (HFI_ARCH_003)
- **Selection mechanism**: Per-destination via Address Vector (AV) configuration
- Added Section 2 "L2 Header Selection Rules" to `packet_taxonomy_ue_plus_variants.md`

```

---

### Task 4: Update Last Updated date

**File**: `analysis/packet_taxonomy/WORK_ITEMS.md`

**Action**: Update the "Last Updated" field in the header

**Change**: `**Last Updated**: 2026-02-03` → `**Last Updated**: 2026-02-03` (verify current)

---

## Verification

- [x] New Section 2 exists in `packet_taxonomy_ue_plus_variants.md`
- [x] Section includes decision matrix table
- [x] Section includes UE+ conditions list
- [x] Section includes Ethernet conditions list
- [x] Section includes simultaneous protocol support note
- [x] Section includes AV role explanation
- [x] W-09-009 removed from Open Work Items
- [x] W-09-009 added to Recently Closed section
- [x] Last Updated date is current

---

## Notes

- This closes the last "actionable" open work item
- W-11-009 (IB Spec 2.0 Review) remains open but is blocked on external spec access
- The L2 selection rules are derived from CN7000 HFI Requirements document
