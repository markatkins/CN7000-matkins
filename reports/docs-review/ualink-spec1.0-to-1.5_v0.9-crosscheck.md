# Crosscheck Review Report: UALink200 Spec v1.0 Final vs. UALink Common Spec Draft Rev 1.5 v0.9

## Document Information

| Field | Value |
|-------|-------|
| **Artifact 1** | `docs/references/UALink/UALink200_Specification_v1.0_Final` — UALink_200 Rev 1.0, dated 4/1/2025 (5,974 lines) |
| **Artifact 2** | `docs/references/UALink/UALink_Common_Specification_Draft_Rev1.5_v0.9` — UALink Common Specification Draft Rev 1.5_v0.9, dated 1/13/2026 (5,186 lines) |
| **Review Date** | 2026-02-10 |
| **Reviewer** | Crosscheck Analysis (developer-opus) |
| **Classification** | UALink Consortium Confidential |

---

## 1. Executive Summary

This crosscheck compares the **UALink_200 Rev 1.0** specification (the "v1.0 Final", released April 2025) against the **UALink Common Specification Draft Rev 1.5 v0.9** (the "v1.5 Draft", dated January 2026) to identify all changes, additions, removals, and areas of concern between the two specification revisions.

**Key Finding:** The v1.5 Draft represents a **major structural and functional evolution** of the UALink specification. The most significant changes are:

1. **In-Network Collectives (INC)** — An entirely new Chapter 6 adds comprehensive INC support including Collective Primitives (ReadReduce, WriteMulticast, WriteFullMulticast, AtomicNRMulticast) and Block Collectives (BlockCollectiveAllocate, BlockCollectiveDeallocate, BlockCollectiveInvoke, BlockRead, BlockWriteFull).
2. **DL/PL Separation** — The Data Link Layer (Chapter 6 in v1.0) and Physical Layer (Chapter 7 in v1.0) have been **removed** from the Common specification and moved to separate companion specifications.
3. **Security Enhancements for Collectives** — New Section 8.6 adds security architecture for collective operations including Accelerator-Switch link protection, Switch Port Identifiers, and collective traffic detection.
4. **New UPLI Commands** — 10+ new command encodings added to support INC operations.
5. **Chapter Renumbering** — Security moves from Chapter 9 to Chapter 8; Switch Requirements moves from Chapter 10 to Chapter 9; Manageability moves from Chapter 8 to Chapter 7.

### Change Statistics

| Change Category | Count | Impact |
|----------------|-------|--------|
| **NEW** — Entirely new content | 14 | INC chapter, new commands, new switch structures, collective security |
| **MODIFIED** — Existing content changed | 18 | Command table, signal tables, TL compressed responses, security sections |
| **REMOVED** — Content removed from this spec | 2 | DL chapter, PL chapter (moved to separate specs) |
| **UNCHANGED** — Substantively identical | 12 | Core UPLI, addressing, coherency, topology, TL flit format basics |
| **TBD/INCOMPLETE** — Marked as incomplete | 3 | Reproducibility (6.5), Rounding Modes (6.6), some Block Collective details |

---

## 2. Structural Changes

### 2.1 Chapter Organization

| v1.0 Final Chapter | v1.5 Draft Chapter | Status |
|--------------------|---------------------|--------|
| 1 - Introduction | 1 - Introduction | UNCHANGED |
| 2 - UPLI Interface Definition | 2 - UPLI Interface Definition | MODIFIED (new commands, signals) |
| 3 - RAS | 3 - RAS | UNCHANGED (page refs shifted) |
| 4 - UPLI Interface Reset | 4 - UPLI Interface Reset | MODIFIED (minor) |
| 5 - Transaction Layer (TL) | 5 - Transaction Layer (TL) | MODIFIED (new compressed response types) |
| 6 - Data Link | *REMOVED* — moved to separate spec | **MAJOR REMOVAL** |
| 7 - Physical Layer | *REMOVED* — moved to separate spec | **MAJOR REMOVAL** |
| 8 - Manageability Requirements | 7 - Manageability Requirements | UNCHANGED |
| 9 - Security | 8 - Security | MODIFIED (new Section 8.6 for collectives) |
| 10 - UALink Switch Requirements | 9 - UALink Switch Requirements | MODIFIED (INC-related additions) |
| *(none)* | 6 - UALink In-Network Collectives | **ENTIRELY NEW** |

**Finding F-2.1.1 (OBSERVATION):** The revision history (line 446-449) explicitly states: "Moves DL/PL content out to separate specifications. Add support for In-Network-Collectives (INC)." This is the defining change of the v1.5 Draft.

**Finding F-2.1.2 (RISK — MEDIUM):** The removal of DL and PL chapters means the v1.5 Common spec is **not self-contained** for implementation. Implementors must now reference at least three documents: the Common spec, the DL spec, and the PL spec. The companion DL and PL specifications were not provided for this review. **Their availability and version alignment should be confirmed.**

---

## 3. Detailed Cross-Reference Analysis

### 3.1 Document Metadata and Scope

| Parameter | v1.0 Final | v1.5 Draft | Status |
|-----------|-----------|------------|--------|
| Title | "UALink_200 Rev 1.0" | "UALink Common Specification Draft Rev 1.5_v0.9" | **CHANGED** — renamed from "200" to "Common" |
| Copyright | (c) 2025 | (c) 2025-2026 | Updated |
| Release Date | 4/1/2025 | 1/13/2026 | 9 months later |
| Status | Final (1.0) | Draft (v0.9) | **v1.5 is still draft** |
| INC Support | "does not define or enable how to perform in-network, in-memory, or near-memory compute" (line 509) | INC fully specified in Chapter 6 | **MAJOR CHANGE** |
| DL/PL | Chapters 6-7 included | Removed to separate specs | **MAJOR CHANGE** |
| Total Lines | 5,974 | 5,186 | 13% smaller despite new INC chapter |

**Finding F-3.1.1 (CRITICAL OBSERVATION):** The v1.0 Final explicitly states (line 509): *"This version of the specification does not define or enable attaching devices to the Switches. It does not define or enable how to perform in-network, in-memory, or near-memory compute."* The v1.5 Draft **removes this limitation** and adds comprehensive INC support. This is the single most significant functional change between the two versions.

**Finding F-3.1.2 (OBSERVATION):** The naming change from "UALink_200" to "UALink Common Specification" suggests a restructuring of the specification suite. The "200" designation referred to the 200G SerDes speed; the "Common" designation suggests this spec now covers protocol-layer content common across multiple speed grades, with speed-specific DL/PL content in separate documents.

---

### 3.2 UPLI Interface (Chapter 2) — Commands

| Command | v1.0 Encoding | v1.5 Encoding | Status |
|---------|--------------|---------------|--------|
| Read | 00_0011b/03h | 00_0011b/03h | UNCHANGED |
| **ReadReduce** | *(not present)* | 00_0100b/04h | **NEW** — Collective Primitive |
| **BlockRead** | *(not present)* | 00_0101b/05h | **NEW** — Block Collective |
| Write | 10_1000b/28h | 10_1000b/28h | UNCHANGED |
| WriteFull | 10_1001b/29h | 10_1001b/29h | UNCHANGED |
| UPLI Write Message | 10_1010b/2Ah | 10_1010b/2Ah | UNCHANGED |
| **BlockCollectiveInvoke** | *(not present)* | 10_0000b/20h | **NEW** — Block Collective |
| **BlockCollectiveAllocate** | *(not present)* | 10_0001b/21h | **NEW** — Block Collective |
| **BlockCollectiveDeallocate** | *(not present)* | 10_0010b/22h | **NEW** — Block Collective |
| **BlockWriteFull** | *(not present)* | 10_0011b/23h | **NEW** — Block Collective |
| **WriteMulticast** | *(not present)* | 10_0110b/26h | **NEW** — Collective Primitive |
| **WriteFullMulticast** | *(not present)* | 10_0111b/27h | **NEW** — Collective Primitive |
| AtomicR | 11_0000b/30h | 11_0000b/30h | UNCHANGED |
| AtomicNR | 11_0010b/32h | 11_0010b/32h | UNCHANGED |
| **AtomicNRMulticast** | *(not present)* | 11_0011b/33h | **NEW** — Collective Primitive |

**Finding F-3.2.1 (CHANGE — HIGH IMPACT):** The v1.5 Draft adds **10 new command encodings** to the ReqCmd field. These commands fall into two categories:
- **Collective Primitives** (4 commands): ReadReduce, WriteMulticast, WriteFullMulticast, AtomicNRMulticast — issued by Accelerators and replicated by the Switch
- **Block Collective Management** (3 commands): BlockCollectiveInvoke, BlockCollectiveAllocate, BlockCollectiveDeallocate — issued by Accelerators to manage Switch-side collective queues
- **Block Collective Data** (2 commands): BlockRead, BlockWriteFull — issued by the Switch to perform memory operations on behalf of Block Collectives

**Finding F-3.2.2 (OBSERVATION):** All new command encodings use previously reserved encoding space. No existing command encodings have been changed. This ensures backward compatibility at the encoding level.

**Finding F-3.2.3 (OBSERVATION):** The v1.5 Draft adds new ReqAttr usage tables: Table 2-4 "BlockRead, ReqAttr Usage" and Table 2-5 "ReadReduce, ReqAttr Usage" (lines 1181+). The ReadReduce ReqAttr carries an 8-bit Stochastic Seed value for stochastic rounding modes.

---

### 3.3 UPLI Interface — Signal Changes

| Signal | v1.0 Final | v1.5 Draft | Status |
|--------|-----------|------------|--------|
| ReqSrcPhysAccID[9:0] | Source Accelerator ID | Overloaded for ReadReduce: bits [6:0] = ReduceOpDataType, bits [9:7] = RoundingMode | **MODIFIED** for Collective Primitives |
| ReqDstPhysAccID[9:0] | Destination Accelerator ID | Overloaded for Collective Primitives: contains GroupID[9:0] | **MODIFIED** for Collective Primitives |
| RdRspTypeInfo[1:0] | *(not present or not documented)* | Indicates type of response (normal vs collective) | **NEW** |
| WrRspTypeInfo[1:0] | *(not present or not documented)* | Indicates type of response (normal vs collective) | **NEW** |

**Finding F-3.3.1 (CHANGE — HIGH IMPACT):** The ReqSrcPhysAccID and ReqDstPhysAccID fields are **overloaded** for Collective Primitive commands. For ReadReduce, the ReqSrcPhysAccID carries reduction operation parameters instead of the source accelerator ID. For all Collective Primitives, the ReqDstPhysAccID carries a GroupID instead of a destination accelerator ID. The Switch must restore the proper AccID values when replicating requests. **This overloading adds complexity to switch implementations and must be carefully handled to avoid routing errors.**

---

### 3.4 Transaction Layer (Chapter 5)

| Parameter | v1.0 Final | v1.5 Draft | Status |
|-----------|-----------|------------|--------|
| TL Flit Size | 64 bytes | 64 bytes | UNCHANGED |
| TL Half-Flit | 32 bytes | 32 bytes | UNCHANGED |
| Control Half-Flit types | Request, Response, FC/NOP, Message | Same + new compressed types for Block* and Multicast* | MODIFIED |
| Compressed Response types | Tables 5-34 through 5-37 | Tables 5-34 through 5-39 (expanded) | **MODIFIED** |

**Finding F-3.4.1 (CHANGE — MEDIUM IMPACT):** The v1.5 Draft adds new Compressed Response Field types:
- Table 5-34: Now includes "Compressed Response for Single Beat Read, AtomicR, **and ReadReduce** Field Signals"
- **Table 5-35 (NEW)**: "Compressed Response for Single Beat **BlockRead** Field Signals"
- Table 5-37: Now includes "Compressed Response for a Write, WriteFull, AtomicNR, **WriteMulticast, WriteFullMulticast, AtomicNRMulticast**, or for a Multi-Beat Read, AtomicR, **or ReadReduce** Request Field Signals"
- **Table 5-38 (NEW)**: "Compressed Response for a **BlockWrite, BlockWriteFull, or Multi-Beat BlockRead** Field Signals"

These additions expand the TL compressed response encoding to handle the new INC command types. Switch TL implementations must be updated to pack/unpack these new compressed response formats.

---

### 3.5 In-Network Collectives (Chapter 6) — ENTIRELY NEW

This is the largest addition in the v1.5 Draft, spanning approximately 550 lines (lines 3102-3642). It defines:

#### 3.5.1 Collective Types Defined

| Collective | Description | Implementation |
|-----------|-------------|----------------|
| BROADCAST | Copy data from Root Rank to all Ranks | Collective Primitives (WriteFullMulticast) or Block Collective |
| REDUCE | Reduce data from all Ranks to Root Rank | Collective Primitives (ReadReduce) or Block Collective |
| ALL-REDUCE | Reduce + Broadcast to all Ranks | Combination of REDUCE + BROADCAST |
| REDUCE-SCATTER | Reduce with scattered output | Repeated REDUCE operations |

#### 3.5.2 Collective Primitives

| Primitive | Base Command | Direction | Switch Action |
|-----------|-------------|-----------|---------------|
| ReadReduce | Read | Accel -> Switch -> All Ranks | Replicate read, reduce responses |
| WriteMulticast | Write | Accel -> Switch -> All Ranks | Replicate write to all group members |
| WriteFullMulticast | WriteFull | Accel -> Switch -> All Ranks | Replicate write to all group members |
| AtomicNRMulticast | AtomicNR | Accel -> Switch -> All Ranks | Replicate atomic to all group members |

#### 3.5.3 Block Collectives

| Operation | Command | Description |
|-----------|---------|-------------|
| BlockCollectiveAllocate | 10_0001b | Allocate entries in Switch Control Block Queue |
| BlockCollectiveDeallocate | 10_0010b | Deallocate entries from Switch Control Block Queue |
| BlockCollectiveInvoke | 10_0000b | Invoke a Block Collective with 64-byte Control Block |
| BlockRead | 00_0101b | Switch-issued read for Block Collective data |
| BlockWriteFull | 10_0011b | Switch-issued write for Block Collective results/status |

#### 3.5.4 Switch Structures Required for INC

| Structure | Description | Per-Port |
|-----------|-------------|----------|
| Group Table | 1024 entries, each with valid bit + bitmask (width = switch radix) | Yes |
| Accelerator ID Register | 10-bit register identifying attached Accelerator | Yes |
| Primitives INC Engine | Replication, tracking, response reduction logic | Yes |
| Control Block Queue | Implementation-specific depth, up to 64 Submission Queues | Yes |
| Block Collective Control Logic | Manages queue entries, issues BlockRead/BlockWriteFull | Yes |

**Finding F-3.5.1 (CHANGE — CRITICAL IMPACT):** The INC chapter imposes **substantial new hardware requirements on switches**. Every switch port must implement:
- A 1024-entry Group Table with bitmask width equal to the switch radix
- Collective Primitive replication and response reduction logic
- Block Collective Control Block Queues with Submission Queue management
- The ability to independently issue BlockRead and BlockWriteFull requests as an originator

This transforms the switch from a pure packet relay into an **active compute participant**. This is the most significant architectural change for switch implementations.

**Finding F-3.5.2 (RISK — MEDIUM):** The Block Collective Control Block is delivered as a 64-byte payload with the BlockCollectiveInvoke command. The Control Block format (Table 6-6, line 3477) contains parameters for the collective operation. Some parameters are marked with "[TBD: Green stuff above are parameters that can be wrong and should be checked]" (line 3499). **The Control Block format is not yet finalized.**

**Finding F-3.5.3 (RISK — LOW):** Sections 6.5 "Reproducibility" and 6.6 "Rounding Modes and Stochastic Rounding" are both marked "TBD" (lines 3634, 3642). These are important for numerical correctness of reduction operations.

---

### 3.6 Data Link Layer and Physical Layer — REMOVED

| v1.0 Chapter | Content | v1.5 Status |
|-------------|---------|-------------|
| 6 - Data Link | DL Flit format (640B), CRC, LLR, UART, pacing, link states | **REMOVED** — moved to separate DL spec |
| 7 - Physical Layer | RS, PCS/PMA, FEC, 100G/200G/400G/800G rates, LL FEC | **REMOVED** — moved to separate PL spec |

**Finding F-3.6.1 (CHANGE — HIGH IMPACT):** The removal of DL and PL chapters reduces the v1.5 Common spec by approximately 1,500 lines of content. However, the DL and PL specifications are **not included in this review**. Key parameters that were in v1.0 and are now in separate specs include:
- DL Flit size: 640 bytes
- DL-to-TL Flit mapping: 10 TL Flits per DL Flit
- CRC protection scheme
- Link Level Replay (LLR) protocol
- FEC types: RS-544, RS-272, 1-way/2-way/4-way interleave
- SerDes rates: 100G, 200G per lane
- Lane widths: x1, x2, x4

**These parameters are still normative but must now be referenced from the companion specifications.**

---

### 3.7 Manageability (Chapter 7 in v1.5 / Chapter 8 in v1.0)

| Parameter | v1.0 Final | v1.5 Draft | Status |
|-----------|-----------|------------|--------|
| System Node management | Section 8.1 | Section 7.1 | RENUMBERED, content unchanged |
| Switch management | Section 8.2 | Section 7.2 | RENUMBERED, content unchanged |
| Pod Controller | Section 8.3 | Section 7.3 | RENUMBERED, content unchanged |
| Virtual Pods | Section 8.4 | Section 7.4 | RENUMBERED, content unchanged |
| Workflows | Section 8.5 | Section 7.5 | RENUMBERED, content unchanged |

**Finding F-3.7.1 (OBSERVATION):** The Manageability chapter is substantively unchanged between v1.0 and v1.5. It has been renumbered from Chapter 8 to Chapter 7 due to the removal of DL/PL chapters and insertion of the INC chapter.

---

### 3.8 Security (Chapter 8 in v1.5 / Chapter 9 in v1.0)

| Parameter | v1.0 Final | v1.5 Draft | Status |
|-----------|-----------|------------|--------|
| Security model | Section 9.3 | Section 8.3 | RENUMBERED, content unchanged |
| AES-GCM encryption | Section 9.5 | Section 8.5 | RENUMBERED, content largely unchanged |
| Switch requirements | Section 9.5.14 | Section 8.5.14 | RENUMBERED, content unchanged |
| Key Derivation (KDF) | Section 9.5.15 | *(not present as separate section)* | **MOVED** — KDF now in Section 8.5.9.2 |
| **Collective Security** | *(not present)* | **Section 8.6** | **ENTIRELY NEW** |
| **Multi-path routing** | *(not present)* | **Section 8.7** | **ENTIRELY NEW** |
| **Spec version compat** | *(not present)* | **Section 8.8** | **ENTIRELY NEW** |
| PCRC (Payload CRC) | *(not present)* | Section 8.5.15 (Figures 11-12) | **NEW** — PCRC generation/verification |
| KDF specification | KMAC256 per SP800-56 | KMAC256 per SP800-56 + detailed context tables | **ENHANCED** |

**Finding F-3.8.1 (CHANGE — HIGH IMPACT):** Section 8.6 "Security during collective operations" (lines 4814-5030) is entirely new and adds:
- **Switch Port Identifier** (8.6.1): Switch ID + Port Number for identifying switch endpoints in collective security
- **Accelerator-Switch link protection** (8.6.2): Separate encryption/authentication scheme for the Accelerator-to-Switch link segment during collectives
- **Ordering Requirements** (8.6.3): Ordering constraints for collective traffic with security enabled
- **Key States** (8.6.4.1): Key state machine for accelerator-switch link protection keys
- **Collective traffic detection** (8.6.5): Mechanism for switches to identify collective vs. unicast traffic
- **Integrity failure handling** (8.6.7): Error handling for security failures on collective traffic

**Finding F-3.8.2 (CHANGE — MEDIUM IMPACT):** Section 8.7 "Allowing multi-path routing with authentication and encryption enabled" (lines 5032-5087) is new and addresses the challenge of maintaining security ordering when traffic may take multiple paths through the network. This includes a new IV format for multi-path routing (Table 29).

**Finding F-3.8.3 (CHANGE — MEDIUM IMPACT):** Section 8.5.15 "Datapath protection" (lines 4790-4812) adds PCRC (Payload CRC) generation and verification during encryption/decryption flows (Figures 11-12). This provides an additional layer of data integrity protection within the security pipeline.

**Finding F-3.8.4 (CHANGE — LOW IMPACT):** Section 8.5.9.2 "Key Derivation Function" (lines 4255-4292) is enhanced with detailed context value tables (Table 7) and IV construction tables (Table 8) that were not present in v1.0.

---

### 3.9 Switch Requirements (Chapter 9 in v1.5 / Chapter 10 in v1.0)

| Parameter | v1.0 Final | v1.5 Draft | Status |
|-----------|-----------|------------|--------|
| Overview | Section 10.1 | Section 9.1 | RENUMBERED, content identical |
| Bifurcation | Section 10.2 | Section 9.2 | RENUMBERED, content identical |
| Lossless delivery | Section 10.3 | Section 9.3 | RENUMBERED, content identical |
| Non-blocking | Section 10.4 | Section 9.4 | RENUMBERED, content identical |
| Forward progress | Section 10.5 | Section 9.5 | RENUMBERED, content identical |
| Ordering & VCs | Section 10.6 | Section 9.6 | RENUMBERED, content identical |
| Routing Table | Section 10.7 | Section 9.7 | RENUMBERED, content identical |
| Routing Table Instances | Section 10.7.1 | Section 9.7.1 | RENUMBERED, content identical |
| Egress port reachability | Section 10.7.2 | Section 9.7.2 | RENUMBERED, content identical |
| Configuration | Section 10.8 | Section 9.8 | RENUMBERED, content identical |
| Latency goals | Section 10.9.2 | Section 9.9.2 | RENUMBERED, content identical |
| Performance goals | Section 10.9.3 | Section 9.9.3 | RENUMBERED, content identical |

**Finding F-3.9.1 (OBSERVATION):** The Switch Requirements chapter is **substantively identical** between v1.0 and v1.5, with only chapter/section renumbering. Notably, the switch requirements chapter does **not** explicitly reference the new INC requirements from Chapter 6. The INC-related switch requirements (Group Table, Primitives INC Engine, Control Block Queue) are defined within Chapter 6 itself rather than in the Switch Requirements chapter.

**Finding F-3.9.2 (RISK — LOW):** The switch latency goals remain identical: 128-lane <200ns, 256-lane <250ns, 512-lane <300ns. These goals do not account for the additional latency that INC processing (collective primitive replication, response reduction, block collective management) may introduce. **The spec should clarify whether these latency goals apply only to unicast forwarding or also to collective operations.**

---

### 3.10 Core Protocol — Unchanged Elements

The following elements are confirmed **unchanged** between v1.0 and v1.5:

| Element | Value | Confirmed |
|---------|-------|-----------|
| Max Accelerators per Pod | 1024 (10-bit AccID) | Yes |
| Max Lanes per Station | 4 | Yes |
| Bifurcation modes | x4, x2, x1 | Yes |
| Max bandwidth per Station | 800 Gbps | Yes |
| Signaling rate | 212.5 GT/s | Yes |
| UPLI channels | 4 (Req, RdRsp, WrRsp, OrigData) | Yes |
| TL Flit size | 64 bytes | Yes |
| Max Request size | 256 bytes (4 beats) | Yes |
| 256-byte boundary rule | Requests shall not cross | Yes |
| Coherency model | I/O coherency, no snoops | Yes |
| Address translation | Implementation-specific | Yes |
| Credit-based flow control | Per-channel credits | Yes |

---

## 4. Contradictions and Inconsistencies

### C-1: v1.0 INC Exclusion vs. v1.5 INC Inclusion
- **v1.0** (line 509): "This version of the specification does not define or enable how to perform in-network, in-memory, or near-memory compute."
- **v1.5**: Chapter 6 fully defines INC with Collective Primitives and Block Collectives.
- **Assessment:** Not a contradiction — this is an intentional evolution. The v1.0 statement is version-scoped. However, implementations targeting v1.0 compliance will **not** support INC, and implementations targeting v1.5 **must** support INC. The transition path for existing v1.0 implementations should be documented.

### C-2: Switch as Pure Relay vs. Active Compute
- **v1.0** (Section 10.1 / line 5887): "A UALink Switch shall not be required to decode the contents of these Requests or Responses beyond that necessary to deliver the Requests and Responses, nor shall the Switch track any Request/Response state."
- **v1.5** (Section 9.1 / line 5099): Contains the **identical statement**.
- **v1.5** (Chapter 6): Requires switches to implement Group Tables, Primitives INC Engines, Control Block Queues, and issue BlockRead/BlockWriteFull requests.
- **Assessment:** **CONTRADICTION.** The Switch Requirements chapter (Section 9.1) still states the switch need not decode request contents or track state, but Chapter 6 requires exactly that for INC operations. The Switch Requirements overview should be updated to acknowledge INC requirements. The statement may be intended to apply only to unicast forwarding, but this is not clarified.

### C-3: Typo in v1.5 Configuration Section
- **v1.5** (Section 9.8, line 5167): "For each port, whether or not Authentication is enabled, whichjjjjjjjjjjjjjjjjjj affects TL flit packing and unpacking."
- **Assessment:** Obvious keyboard artifact ("jjjjjjjjjjjjjjjjjj"). This is a draft quality issue.

---

## 5. TBD / Incomplete Sections in v1.5 Draft

| Section | Content | Status |
|---------|---------|--------|
| 6.5 Reproducibility | "TBD." | **INCOMPLETE** — Critical for numerical correctness |
| 6.6 Rounding Modes and Stochastic Rounding | "TBD." | **INCOMPLETE** — Required for ReadReduce operations |
| 6.3.7 Block Collective Control Block | "[TBD: Green stuff above are parameters that can be wrong and should be checked]" | **INCOMPLETE** — Control Block format not finalized |
| 6.3.6 Address Masking | "[Figure here showing the entire process?]" | **INCOMPLETE** — Missing figure |
| 6.3.9 Block Collective Request/Response Flows | "[Add words here for passing through the other signals in the Req Channel?]" | **INCOMPLETE** — Missing text |

**Finding F-5.1 (RISK — HIGH):** The Reproducibility section (6.5) is critical for AI/ML workloads where deterministic results across runs are required. Without a reproducibility guarantee, different invocations of the same collective operation may produce different results due to floating-point non-associativity. This must be resolved before the spec is finalized.

**Finding F-5.2 (RISK — HIGH):** The Rounding Modes section (6.6) is required for the ReadReduce Collective Primitive, which carries a RoundingMode[2:0] field. Without this section, the semantics of the rounding mode values are undefined.

---

## 6. Impact Assessment for LNR Switch Implementation

| v1.5 Change | LNR HAS Rev 0.3 Impact | Effort Estimate |
|-------------|------------------------|-----------------|
| New INC commands (10 commands) | Rpipe must parse and route new command types; new command encodings in TL pack/unpack | Medium |
| Group Table (1024 entries per port) | New per-MPORT structure; bitmask width = switch radix | Medium |
| Primitives INC Engine | New per-MPORT logic for request replication and response reduction | High |
| Block Collective Control Block Queue | New per-MPORT queue structure with Submission Queue management | High |
| Switch-originated BlockRead/BlockWriteFull | Switch must act as request originator, not just relay | High |
| Collective security (Section 8.6) | Switch Port Identifier, Accel-Switch link protection, collective traffic detection | High |
| Multi-path routing security (Section 8.7) | New IV format for multi-path routing | Medium |
| PCRC (Section 8.5.15) | Additional CRC in security pipeline | Low |
| DL/PL separation | No direct impact on switch core; DL/PL IP unchanged | None |

**Finding F-6.1 (OBSERVATION):** The LNR HAS Rev 0.3 already includes a Collectives Engine (CE) with RISC-V compute blocks, which is architecturally aligned with the v1.5 INC requirements. However, the specific command encodings, Group Table structure, Block Collective Control Block Queue, and response reduction logic defined in v1.5 Chapter 6 must be validated against the LNR CE architecture.

**Finding F-6.2 (OBSERVATION):** The LNR HAS describes collectives as using the Data Ring for multicast and the Collectives Engine for reduction. The v1.5 spec's Collective Primitives (which use the switch to replicate requests and reduce responses) map well to this architecture. The Block Collectives (which require the switch to independently issue reads and writes) may require additional logic in the LNR MPORT to act as a request originator.

---

## 7. Risk Summary

| Priority | Finding | Category | Impact |
|----------|---------|----------|--------|
| **P0** | C-2: Switch Requirements overview contradicts INC requirements | Spec Consistency | Implementor confusion |
| **P0** | F-5.1: Reproducibility section TBD | Numerical Correctness | Non-deterministic AI results |
| **P0** | F-5.2: Rounding Modes section TBD | Protocol Completeness | ReadReduce semantics undefined |
| **P1** | F-3.5.2: Block Collective Control Block format not finalized | Protocol Completeness | Cannot implement Block Collectives |
| **P1** | F-3.6.1: Companion DL/PL specs not reviewed | Spec Completeness | Cannot verify DL/PL alignment |
| **P1** | F-3.8.1: Collective security adds major switch requirements | Security | Switch must implement Accel-Switch link protection |
| **P2** | F-3.1.2: Naming change from "200" to "Common" | Versioning | Potential confusion with v1.0 references |
| **P2** | C-3: Typo in Section 9.8 | Draft Quality | Minor |
| **P2** | F-3.9.2: Latency goals don't address INC operations | Performance | Unclear latency expectations for collectives |

---

## 8. Recommendations

### For Specification Authors (UALink Consortium)

1. **Resolve C-2:** Update Section 9.1 (Switch Requirements Overview) to acknowledge that switches supporting INC must decode collective command types and maintain collective state. Consider adding a "Switch INC Requirements" subsection to Chapter 9.

2. **Complete TBD Sections:** Prioritize Sections 6.5 (Reproducibility) and 6.6 (Rounding Modes) — these are blocking for INC implementation.

3. **Finalize Block Collective Control Block:** Remove TBD markers from Section 6.3.7 and validate all parameter definitions.

4. **Add INC Latency Goals:** Extend Section 9.9.2 to include latency goals for Collective Primitive and Block Collective operations.

5. **Fix Typo:** Section 9.8, line 5167 — remove "jjjjjjjjjjjjjjjjjj".

### For LNR Switch Implementation (Cornelis Networks)

6. **Validate CE Architecture Against v1.5 INC:** Confirm that the LNR Collectives Engine architecture supports the specific Collective Primitive and Block Collective flows defined in Chapter 6, including Group Table structure, response reduction logic, and Block Collective Control Block Queue.

7. **Plan for New Command Encodings:** Update Rpipe and TL pack/unpack logic to handle the 10 new command encodings.

8. **Assess Collective Security Impact:** The new Section 8.6 requirements for Accelerator-Switch link protection during collectives may require additional encryption/decryption engines or key management logic in the switch.

9. **Obtain Companion DL/PL Specs:** Request the separate DL and PL specifications referenced by the v1.5 Common spec to ensure alignment with the LNR Hill Creek implementation.

---

## 9. Conclusion

The UALink Common Specification Draft Rev 1.5 v0.9 represents a **transformative evolution** from UALink_200 Rev 1.0. The addition of In-Network Collectives fundamentally changes the role of the UALink switch from a passive packet relay to an active compute participant. This aligns with the industry trend toward offloading collective communication operations to network hardware for AI/ML workloads.

The core protocol (UPLI, TL, addressing, coherency) remains **backward compatible** — all v1.0 command encodings are preserved, and the new commands use previously reserved encoding space. However, v1.5-compliant switches must implement substantially more hardware (Group Tables, INC Engines, Control Block Queues) than v1.0-compliant switches.

The v1.5 Draft is **approximately 85% complete**, with critical TBD sections in Reproducibility, Rounding Modes, and Block Collective Control Block format. The separation of DL/PL into companion specifications is a clean architectural decision but requires those companion specs to be available and version-aligned.

**For the LNR Switch:** The existing Collectives Engine architecture in the LNR HAS Rev 0.3 provides a strong foundation for v1.5 INC compliance, but specific validation against the Chapter 6 requirements is needed, particularly for Block Collective Control Block Queue management and the new collective security requirements in Section 8.6.

---

*End of Crosscheck Review Report*
