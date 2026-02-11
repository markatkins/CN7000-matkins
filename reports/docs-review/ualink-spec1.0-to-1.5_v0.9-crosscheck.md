# Full Crosscheck Review Report: UALink200 v1.0 Final vs. UALink v1.5 (Common + DLPL 200G)

## Document Information

| Field | Value |
|-------|-------|
| **Artifact 1** | `UALink200_Specification_v1.0_Final` — UALink_200 Rev 1.0, dated 4/1/2025 (5,974 lines, single document) |
| **Artifact 2a** | `UALink_Common_Specification_Draft_Rev1.5_v0.9` — UALink Common Spec Draft Rev 1.5 v0.9, dated 1/13/2026 (5,186 lines) |
| **Artifact 2b** | `UALink_1.5_DLPL_200G_NCB_RC` — UALink 200G Data Link and Physical Layers Version 1.5 (Release Candidate), dated 1/12/2026 (2,807 lines) |
| **Review Date** | 2026-02-11 |
| **Reviewer** | Crosscheck Analysis (developer-opus) |
| **Classification** | UALink Consortium Confidential |
| **Supersedes** | `ualink-spec1.0-to-1.5_v0.9-crosscheck.md` (Common-only review, 2026-02-10) |

---

## 1. Executive Summary

This report is the **full crosscheck** of UALink200 v1.0 Final against the complete v1.5 specification suite, which was split into two documents:
- **UALink Common Specification Draft Rev 1.5 v0.9** — Protocol, Transaction, Collectives, Security, Switch Requirements (Chapters 1-9)
- **UALink 200G Data Link and Physical Layers Version 1.5 RC** — Data Link and Physical Layer for 200G SerDes (Chapters 2-3 + Appendices)

The v1.0 specification was a single monolithic document. For v1.5, the UALink Consortium split it into a speed-independent "Common" specification and speed-specific "DLPL" specifications. This review covers both halves to provide complete coverage.

### Key Findings

**Common Spec Changes (from prior review — confirmed):**
1. **In-Network Collectives (INC)** — Entirely new Chapter 6 with Collective Primitives and Block Collectives (10 new UPLI commands)
2. **Security for Collectives** — New Section 8.6 with Accelerator-Switch link protection
3. **Multi-path routing security** — New Section 8.7
4. **PCRC (Payload CRC)** — New Section 8.5.15

**DLPL Spec Changes (NEW in this review):**
5. **Link Resiliency** — New Section 2.8 adds bonding of two physical layers to one DL with TDM, fault recovery, and reordering
6. **Link Folding** — New Section 2.9 adds power-saving lane folding/unfolding with DL PwrDn state
7. **Link Width Negotiation** — New DL control message (Section 2.4.3.3) for negotiating link width changes
8. **Tx Ready Notification** — New DL basic message (Section 2.4.2.6) for link unfolding coordination
9. **TL Backpressure** — New Rx Ingress Rules for handling TL backpressure (Section 2.6.6.2)
10. **DL-PL Interface** — New Appendix B with detailed signal-level interface specification
11. **Rapid Alignment Markers (RAMs)** — New Section 3.3.7 for fast alignment during link unfolding
12. **PMA Symbol Pair Demultiplexing** — New Section 3.3.8 requiring parallel alignment search

### Overall Assessment

| Dimension | v1.0 | v1.5 (Common + DLPL) | Delta |
|-----------|------|----------------------|-------|
| Total Lines | 5,974 | 7,993 (5,186 + 2,807) | +34% |
| Chapters | 10 | 9 (Common) + 3 (DLPL) + Appendices | Restructured |
| UPLI Commands | 12 | 22 | +10 new |
| DL States | 4 (Fault, Idle, NOP, Up) | 5 (+ PwrDn) | +1 new |
| DL Message Types | 7 | 9 | +2 new |
| PL Features | Basic RS/PCS/FEC | + Link Resiliency, Folding, RAMs | Major additions |

---

## 2. Specification Structure: v1.0 (Monolithic) vs. v1.5 (Split)

### 2.1 Document Mapping

| v1.0 Chapter | v1.5 Document | v1.5 Chapter | Status |
|-------------|---------------|-------------|--------|
| 1 - Introduction | Common | 1 - Introduction | UNCHANGED |
| 2 - UPLI Interface | Common | 2 - UPLI Interface | MODIFIED (INC commands) |
| 3 - RAS | Common | 3 - RAS | UNCHANGED |
| 4 - UPLI Reset | Common | 4 - UPLI Reset | MINOR CHANGES |
| 5 - Transaction Layer | Common | 5 - Transaction Layer | MODIFIED (INC compressed responses) |
| 6 - Data Link | **DLPL** | **2 - Data Link** | **MAJOR ADDITIONS** |
| 7 - Physical Layer | **DLPL** | **3 - Physical Layer** | **MAJOR ADDITIONS** |
| 8 - Manageability | Common | 7 - Manageability | RENUMBERED |
| 9 - Security | Common | 8 - Security | MODIFIED (collective security) |
| 10 - Switch Requirements | Common | 9 - Switch Requirements | RENUMBERED |
| *(none)* | Common | **6 - In-Network Collectives** | **ENTIRELY NEW** |
| *(none)* | **DLPL** | **Appendix A - DL CRC Example** | **NEW** |
| *(none)* | **DLPL** | **Appendix B - DL to PL Interface** | **NEW** |

### 2.2 DLPL Revision History

The DLPL spec's revision history (lines 260-269) documents the following additions beyond v1.0:

| ECN/ECR | Date | Description |
|---------|------|-------------|
| ECN DL Down Delay | 2025-09-17 | Programmable delay before DL Up -> DL Fault transition |
| ECR Link Resiliency | 2025-11-04 | Bonding two PLs to one DL |
| ECR Link Folding | 2025-11-04 | Power-saving lane folding |
| ECR Back Pressure from TL | 2025-09-30 | TL backpressure handling in DL Rx |
| ECR DL PL Interface | 2025-10-20 | Signal-level DL-PL interface spec |
| ECR CRC Example | 2025-09-22 | Informative CRC calculation example |
| Errata Batch 1 | — | 8 errata resolved (A103001-B103009) |
| Errata Batch 2 | — | 23 errata resolved (A103010-A103034) |

---

## 3. Data Link Layer Changes (DLPL Chapter 2 vs. v1.0 Chapter 6)

### 3.1 Core DL Parameters — Unchanged

| Parameter | v1.0 | v1.5 DLPL | Status |
|-----------|------|-----------|--------|
| DL Flit Size | 640 bytes | 640 bytes | UNCHANGED |
| Segments per Flit | 5 | 5 | UNCHANGED |
| TL Flit Size | 64 bytes | 64 bytes | UNCHANGED |
| Max TL Flits per DL Flit | ~9.8 (628B payload / 64B) | Same | UNCHANGED |
| CRC | 32-bit, IEEE 802.3 polynomial | 32-bit, IEEE 802.3 polynomial | UNCHANGED |
| CRC bit order | Reversed from 802.3 FCS (x0 first) | Reversed from 802.3 FCS (x0 first) | UNCHANGED |
| Flit Header | 3 bytes (24 bits) | 3 bytes (24 bits) | UNCHANGED |
| Segment Headers | 5 x 1 byte | 5 x 1 byte | UNCHANGED |
| DL overhead per Flit | 12 bytes (3 FH + 5 SH + 4 CRC) | 12 bytes | UNCHANGED |
| Effective TL payload | 628 bytes per 640B Flit | 628 bytes | UNCHANGED |
| Sequence Number | 9-bit (1-511, 0 reserved) | 9-bit (1-511, 0 reserved) | UNCHANGED |
| Max unacknowledged Flits | 255 | 255 | UNCHANGED |
| Replay Request copies | 3 | 3 | UNCHANGED |

### 3.2 DL Link States — NEW: DL PwrDn

| State | v1.0 | v1.5 DLPL | Status |
|-------|------|-----------|--------|
| DL Fault | Yes | Yes | UNCHANGED |
| DL Idle | Yes | Yes | **MODIFIED** — new transitions for Link Resiliency |
| DL NOP | Yes | Yes | **MODIFIED** — new transitions for Link Resiliency |
| DL Up | Yes | Yes | **MODIFIED** — programmable delay to DL Fault, PwrDn transitions |
| **DL PwrDn** | **No** | **Yes** | **NEW** — entered during Link Folding |

**Finding F-3.2.1 (CHANGE — HIGH IMPACT):** The new DL PwrDn state (Section 2.7.1.5) is entered when Link Folding powers down a physical layer. In this state, the RS sends PwrDn Control Flits. The PL places Tx and Rx in low power state after 10 PwrDn Control Flits sent and 1 received. Transitions out of PwrDn go to DL Fault (for link width restoration or error conditions).

**Finding F-3.2.2 (CHANGE — MEDIUM IMPACT):** DL Up now has a **programmable delay** before transitioning to DL Fault on continuous fault indication: "between 0 and 10ms in 1ms steps, with a default of 5ms" (line 1528). This was not present in v1.0 and allows the system to ride through transient faults without dropping the link.

**Finding F-3.2.3 (CHANGE — MEDIUM IMPACT):** DL Idle now has additional transition conditions for Link Resiliency: it can transition to DL NOP if another DL "sub" state machine is in DL Up and specific conditions are met (first entry since PwrDn exit, successful Link Width Negotiation, or Link Folding Recovery).

### 3.3 DL Messages — NEW: Link Width Negotiation, Tx Ready Notification

| Message | v1.0 | v1.5 DLPL | Status |
|---------|------|-----------|--------|
| No-Op | Yes | Yes | UNCHANGED |
| TL Rate Notification | Yes | Yes | UNCHANGED |
| Device ID Request | Yes | Yes | UNCHANGED |
| Port Number Request | Yes | Yes | UNCHANGED |
| DL Channel On/Offline | Yes | Yes | UNCHANGED |
| **Link Width Negotiation** | **No** | **Yes** | **NEW** — Section 2.4.3.3 |
| **Tx Ready Notification** | **No** | **Yes** | **NEW** — Section 2.4.2.6 |
| UART Stream Transport | Yes | Yes | UNCHANGED |
| UART Stream Credit Update | Yes | Yes | UNCHANGED |
| UART Stream Reset Req/Rsp | Yes | Yes | UNCHANGED |

**Finding F-3.3.1 (CHANGE — HIGH IMPACT):** Link Width Negotiation (Table 2-10) is a new Control Message that enables negotiation of link width changes for Link Folding. Key features:
- Only Accelerators may initiate (not Switches)
- Supports full width and folded width (PL0 active or PL1 active)
- Priority bit for urgent thermal/power requests
- Conflict resolution rules: PL0 wins over PL1; smallest width with Priority wins; widest width without Priority wins
- Tx Ready Support bit advertises capability
- Response timeout: 1.0 us; decision pending re-request: 10ms

**Finding F-3.3.2 (CHANGE — MEDIUM IMPACT):** Tx Ready Notification (Table 2-8) is a new Basic Message sent when a PL transmitter being activated starts transmitting valid symbols during link unfolding. Used as a hint to enable CDR lock on the newly powered receiver.

### 3.4 Link Level Replay — MODIFIED

| Parameter | v1.0 | v1.5 DLPL | Status |
|-----------|------|-----------|--------|
| Explicit Flit Header format | Table in v1.0 Ch6 | Table 2-16 | UNCHANGED |
| Command Flit Header format | Table in v1.0 Ch6 | Table 2-17 | UNCHANGED |
| Rx_replay_limit default | 50 | 50 | UNCHANGED |
| Tx_ack_time_out | 10.24ms | 10.24ms | UNCHANGED |
| Replay Request Ignore Window | 12 Flits | 12 Flits | UNCHANGED |
| **TL Backpressure handling** | **Not specified** | **Section 2.6.6.2** | **NEW** |
| **Link Width Unfolding replay** | **Not specified** | **Section 2.6.6.11** | **NEW** |

**Finding F-3.4.1 (CHANGE — MEDIUM IMPACT):** Section 2.6.6.2 adds new Rx Ingress Rules for TL backpressure. When the TL asserts backpressure and there is no room to store the DL Flit, the Flit is discarded and treated similarly to a CRC error (Rx_bad_crc_count incremented, Rx_ambiguous set if count >= 7). This is required for chiplet implementations where TL is on different silicon with UCIe replay. Non-chiplet implementations are "encouraged" to support this.

**Finding F-3.4.2 (CHANGE — LOW IMPACT):** Section 2.6.6.11 adds rules for replay during Link Width Unfolding: DL Flits created at folded width must be replayed at proportionately lower rate when operating at unfolded width (e.g., 50% rate via NOP insertion) to prevent receiver overflow.

### 3.5 Link Resiliency — ENTIRELY NEW (Section 2.8)

This is a major new feature not present in v1.0. Link Resiliency bonds two independent physical layers to a single DL.

| Feature | Description |
|---------|-------------|
| **Concept** | Two PLs bonded to one DL; TDM multiplexing in Tx, demultiplexing in Rx |
| **Applicability** | Optional; defined for links with 2+ lanes |
| **Tx ordering** | PL[A] first (lower-order lanes), then PL[B], round-robin |
| **Rx reordering** | Required to handle inter-PL skew; uses AM/RAM for alignment |
| **Skew budget** | Per IEEE 802.3: 200G serial SP6 = 145ns, at PCS receive = 152ns |
| **Skew variation** | 4ns (per 802.3) between any PL and any other PL |
| **Fault handling** | If one PL faults, DL continues on non-faulted PL; LLR replays lost Flits |
| **Fast recovery** | Faulted PL recovers without DL leaving DL Up (programmable timeout) |
| **Link down recovery** | Faulted PL goes through DL Fault -> DL Idle -> DL NOP -> DL Up |
| **DL "sub" state machines** | One per PL; DL is up if any sub-SM is in DL Up |
| **Tx mux latency** | Max 1/2 Flit time additional |

**Finding F-3.5.1 (CHANGE — CRITICAL IMPACT):** Link Resiliency fundamentally changes the DL architecture from a 1:1 DL-to-PL mapping to a 1:2 mapping. This affects:
- Replay buffer sizing (must cover RTT for both PLs)
- Error containment (PL ID mismatch or change triggers error)
- DL state machine (per-PL "sub" state machines with coordination rules)
- Flit sequencing (strict incremental monotonic order must be maintained across PLs)

### 3.6 Link Folding — ENTIRELY NEW (Section 2.9)

| Feature | Description |
|---------|-------------|
| **Concept** | Power-saving: fold link to half width by powering down one PL's SerDes |
| **Prerequisite** | Link Resiliency must be supported |
| **Initiation** | Only Accelerators may request (via Link Width Negotiation message) |
| **Folding sequence** | Negotiate -> Target enters DL PwrDn -> Initiator enters DL PwrDn -> PMD Tx/Rx low power |
| **Unfolding sequence** | Negotiate -> Signal PL to power up -> PL restores settings -> DL Fault -> DL Idle -> DL NOP -> DL Up |
| **Power-up target** | < 250us for Tx/Rx power-up and PL alignment lock |
| **RAMs during unfold** | Rapid Alignment Markers sent for fast alignment (128x more frequent than AMs) |
| **Folding recovery** | If active PL faults while folded, powered-down PL is powered up automatically |

**Finding F-3.6.1 (CHANGE — HIGH IMPACT):** Link Folding adds a complete power management subsystem to the DL. The < 250us power-up target (line 2137) is aggressive and requires that AN/LT not be re-run during unfold. The PL must save and restore Tx/Rx settings.

### 3.7 DL-PL Interface — ENTIRELY NEW (Appendix B)

Appendix B (lines 2656-2807) provides a detailed signal-level interface specification between DL and PL that was not present in v1.0.

| Signal Group | Key Signals | Description |
|-------------|-------------|-------------|
| **Tx DL->PL** | tx_dp_active, tx_dp_valid, tx_dp_data[511:0], tx_dp_flit_start, tx_dp_command[2:0], tx_dp_uerr, tx_dp_port_id[1:0] | DL drives data and control to PL |
| **Tx PL->DL** | tx_pd_ready, tx_pd_port_id[1:0], tx_pd_group_start, tx_pd_flit_start | PL flow-controls DL |
| **Rx PL->DL** | rx_pd_valid, rx_pd_data[511:0], rx_pd_flit_start, rx_pd_port_id[1:0], rx_pd_link_event[3:0], rx_pd_data_err, rx_pd_uerr | PL delivers data and events to DL |

**Finding F-3.7.1 (CHANGE — HIGH IMPACT):** The DL-PL interface is 512 bits wide (64 bytes) and TDM'd across ports. The TDM calendar changes based on Link Resiliency mode:
- Without Link Resiliency: 0,1,2,3 (4 ports) or 0,1 (2 ports) or 0 (1 port)
- With Link Resiliency: 0,2,1,3 (2 DLs) or 0,1 (1 DL) — interleaved for latency optimization

**Finding F-3.7.2 (OBSERVATION):** The rx_pd_link_event[3:0] signal provides a rich event vocabulary: NOP, Idle, Remote Fault, PwrDn, AM/RAM with PL ID 0/1/none, Bad Flit, Local Fault. This is the primary mechanism for the DL to track PL state.

---

## 4. Physical Layer Changes (DLPL Chapter 3 vs. v1.0 Chapter 7)

### 4.1 Core PL Parameters — Unchanged

| Parameter | v1.0 | v1.5 DLPL | Status |
|-----------|------|-----------|--------|
| 200G SerDes rate | 212.5 Gbps PAM4 | 212.5 Gbps PAM4 | UNCHANGED |
| 100G SerDes rate | 106.25 Gbps PAM4 | 106.25 Gbps PAM4 | UNCHANGED |
| Lane configurations | x1, x2, x4 | x1, x2, x4 | UNCHANGED |
| Station bandwidth | 800 Gbps | 800 Gbps | UNCHANGED |
| FEC | RS(544, 514) | RS(544, 514) | UNCHANGED |
| Code word size | 680 bytes (640B DL Flit + 40B FEC/encoding) | 680 bytes | UNCHANGED |
| DL Flit to codeword | 1:1 mapping | 1:1 mapping | UNCHANGED |
| 64B/66B encoding | Subset of 802.3 Clause 82 | Same subset | UNCHANGED |
| AN/LT | Unmodified from 802.3 | Unmodified from 802.3 | UNCHANGED |

### 4.2 Supported Rates and Clauses — Unchanged

**100G Serial (Table 3-1):**

| Rate | RS | FEC/PCS | PMA | Interleave |
|------|-----|---------|-----|------------|
| 100GBASE-KR1/CR1 | 81 | 82, 91 | 135 | 1-way |
| 200GBASE-KR2/CR2 | 117 | 119 | 120 | 2-way |
| 400GBASE-KR4/CR4 | 117 | 119 | 120 | 2-way |

**200G Serial (Table 3-2):**

| Rate | RS | PCS | PMA | 802.3 | UALink LL |
|------|-----|-----|-----|-------|-----------|
| 200GBASE-KR1/CR1 | 117 | 119 | 176 | 4-way | 2-way, 1-way |
| 400GBASE-KR2/CR2 | 117 | 119 | 176 | 4-way | 2-way |
| 800GBASE-KR4/CR4 | 170 | 172 | 176 | 4-way | — |

### 4.3 RS Changes — NEW Features

| Feature | v1.0 | v1.5 DLPL | Status |
|---------|------|-----------|--------|
| DL Flit Code Sequences | Data, Idle, Fault, AM | + Idle Start, Fault Start, PwrDn, PwrDn Start | **NEW** |
| PL ID in Control Flits | Not specified | Last 64B/66B block carries PL ID in D7 | **NEW** |
| Link Power Down | Not specified | RS sends PwrDn Control Flits; suspends fault signaling | **NEW** |
| Link Power Up | Not specified | RS sends RAMs; < 250us target; no AN/LT | **NEW** |
| Rapid Alignment Markers | Not specified | Section 3.3.7 — 128x more frequent than AMs | **NEW** |

**Finding F-4.3.1 (CHANGE — HIGH IMPACT):** The RS now supports 8 types of Flit Code Sequences (up from 4 in v1.0):
1. Data Flit (unchanged)
2. Idle Flit (unchanged)
3. Fault Flit (unchanged)
4. AM Flit (unchanged)
5. **Idle Start Flit** (NEW — indicates AM/RAM timing to PCS)
6. **Fault Start Flit** (NEW — indicates AM/RAM timing during fault)
7. **PwrDn Flit** (NEW — block type 0xFF, all data 0x00)
8. **PwrDn Start Flit** (NEW — PwrDn with AM timing indication)

**Finding F-4.3.2 (CHANGE — HIGH IMPACT):** Rapid Alignment Markers (Section 3.3.7) are a significant PCS addition:
- Use same format as 802.3 Clause 119.2.4.4 AMs
- UP0 for Lane 0 XOR'd with am_next_count (indicates RAMs until next AM)
- 128x more frequent than AMs: 32 CW period at 200G x1 (819 ns)
- Required for Link Folding unfold sequence
- Alignment lock rules: parallel search for RAM and AM lock, transition from RAM lock to AM lock when two RAMs agree on AM placement

### 4.4 PCS Changes

| Feature | v1.0 | v1.5 DLPL | Status |
|---------|------|-----------|--------|
| AM frequency (100G) | Every 4,096 Flits | Every 4,096 Flits | UNCHANGED |
| AM frequency (200G) | Every 4,096 Flits | Every 4,096 Flits | UNCHANGED |
| AM frequency (400G) | Every 8,192 Flits | Every 8,192 Flits | UNCHANGED |
| AM frequency (800G) | Every 16,384 Flits | Every 16,384 Flits | UNCHANGED |
| Rate matching | Every 1024 CW | Every 1024 CW | UNCHANGED |
| **PMA Symbol Pair Demux** | **Not specified** | **Section 3.3.8 — parallel search** | **NEW** |

**Finding F-4.4.1 (CHANGE — MEDIUM IMPACT):** Section 3.3.8 requires PMA to consider all 20 possible symbol pair alignments **in parallel** (not serial). This reduces symbol alignment time from ~6ms (serial search) to ~300us (3 AM intervals). This is a new requirement for PMA implementations.

### 4.5 Link Resiliency at PL Level (Section 3.8)

| Feature | Description |
|---------|-------------|
| **Transmit Alignment** | PL[A] and PL[B] codewords staggered by 50%; PL[A] first |
| **AM synchronization** | AMs occur at same time + 50% stagger offset |
| **PL ID** | PL[A] = 0, PL[B] = 1; transmitted in AM/RAM Control Flits |
| **PL ID signaling** | RS indicates PL ID to DL when FEC-corrected AM codeword received |

---

## 5. Common Spec Changes (Summary — from prior review)

The following changes were identified in the prior Common-only crosscheck and are confirmed here for completeness:

### 5.1 In-Network Collectives (Chapter 6) — ENTIRELY NEW

- **Collective Primitives**: ReadReduce (04h), WriteMulticast (26h), WriteFullMulticast (27h), AtomicNRMulticast (33h)
- **Block Collective Management**: BlockCollectiveInvoke (20h), BlockCollectiveAllocate (21h), BlockCollectiveDeallocate (22h)
- **Block Collective Data**: BlockRead (05h), BlockWriteFull (23h)
- **Switch Structures**: Group Table (1024 entries/port), Primitives INC Engine, Control Block Queue (up to 64 Submission Queues)
- **TBD Sections**: Reproducibility (6.5), Rounding Modes (6.6), some Control Block parameters

### 5.2 Security Enhancements (Chapter 8)

- **Section 8.6**: Security during collective operations (Switch Port ID, Accel-Switch link protection, key states, collective traffic detection)
- **Section 8.7**: Multi-path routing with authentication/encryption
- **Section 8.5.15**: PCRC (Payload CRC) in security pipeline
- **Section 8.5.9.2**: Enhanced KDF with detailed context/IV tables

### 5.3 Switch Requirements (Chapter 9)

- Substantively identical to v1.0 Chapter 10 (renumbered only)
- **Contradiction C-2** (from prior review): Section 9.1 still states switches need not decode request contents, but Chapter 6 INC requires exactly that

---

## 6. Contradictions and Inconsistencies

### C-1: Switch Requirements vs. INC (from prior review — confirmed)
- **Common Section 9.1**: "A UALink Switch shall not be required to decode the contents of these Requests or Responses beyond that necessary to deliver the Requests and Responses, nor shall the Switch track any Request/Response state."
- **Common Chapter 6**: Requires switches to implement Group Tables, INC Engines, Control Block Queues, and issue BlockRead/BlockWriteFull.
- **Assessment:** CONTRADICTION. Must be resolved.

### C-2: Typo in Common Section 9.8 (from prior review — confirmed)
- Line 5167: "whichjjjjjjjjjjjjjjjjjj affects TL flit packing"
- **Assessment:** Draft quality issue.

### C-3: DLPL Section 2.7.1.5 Cross-Reference Error
- Line 1541: "see 6.4.3.3" — This references a section number from the v1.0 monolithic spec. Should be "see 2.4.3.3" in the DLPL document.
- **Assessment:** Broken cross-reference from spec split.

### C-4: DLPL Section 2.8.1 Numbering Error
- Line 79: Table of Contents shows "7 Link State and Errors" but the actual section is "2.7 Link State and Errors"
- Line 84: Table of Contents shows "3 Link Resiliency" but the actual section is "2.8 Link Resiliency"
- Line 91: Table of Contents shows "9 Link Folding Operation" but the actual section is "2.9 Link Folding Operation"
- **Assessment:** Table of Contents numbering errors — likely OCR/conversion artifacts.

---

## 7. TBD / Incomplete Sections

### Common Spec TBDs

| Section | Content | Impact |
|---------|---------|--------|
| 6.5 Reproducibility | "TBD." | **HIGH** — numerical correctness |
| 6.6 Rounding Modes | "TBD." | **HIGH** — ReadReduce semantics |
| 6.3.7 Block Collective Control Block | "[TBD: parameters that can be wrong]" | **MEDIUM** — format not finalized |

### DLPL Spec TBDs

| Section | Content | Impact |
|---------|---------|--------|
| None identified | DLPL appears complete (Release Candidate status) | — |

**Finding F-7.1 (OBSERVATION):** The DLPL spec is at **Release Candidate** status (v1.0 RC, dated 2026-01-12), while the Common spec is at **Draft v0.9** status. The DLPL spec appears more mature with no TBD sections identified.

---

## 8. Impact Assessment for LNR Switch Implementation

### 8.1 DLPL-Specific Impacts

| v1.5 DLPL Change | LNR HAS Rev 0.3 Impact | Effort |
|-----------------|------------------------|--------|
| Link Resiliency (2 PLs bonded) | Hill Creek MAC must support TDM mux/demux, per-PL state machines, reordering | **HIGH** |
| Link Folding (DL PwrDn) | Hill Creek must support PwrDn state, Link Width Negotiation, SerDes power management | **HIGH** |
| Link Width Negotiation message | New DL control message in Hill Creek DL | **MEDIUM** |
| Tx Ready Notification message | New DL basic message in Hill Creek DL | **LOW** |
| TL Backpressure in DL Rx | Hill Creek DL Rx must handle backpressure from TL (relevant for UCIe die-to-die) | **MEDIUM** |
| DL-PL Interface (Appendix B) | Informative but useful for Hill Creek DL-PL integration | **LOW** |
| Rapid Alignment Markers | Hill Creek PCS must support RAM generation and lock | **MEDIUM** |
| PMA parallel symbol pair search | Hill Creek PMA must search 20 alignments in parallel | **LOW** |
| Programmable DL Up->Fault delay | Hill Creek DL state machine needs configurable timer (0-10ms) | **LOW** |

### 8.2 Combined Impact Summary

| Category | Common Spec | DLPL Spec | Total |
|----------|-------------|-----------|-------|
| **Critical** | INC (10 commands, switch structures) | Link Resiliency | 2 |
| **High** | Collective Security, TBD sections | Link Folding, DL-PL Interface | 4 |
| **Medium** | Multi-path security, PCRC | Link Width Negotiation, TL Backpressure, RAMs | 5 |
| **Low** | Typos, latency goals | Tx Ready, PMA parallel search, DL delay timer | 4 |

---

## 9. Risk Summary

| Priority | Finding | Category | Impact |
|----------|---------|----------|--------|
| **P0** | C-1: Switch Requirements contradicts INC | Spec Consistency | Implementor confusion |
| **P0** | F-5.1 (prior): Reproducibility TBD | Numerical Correctness | Non-deterministic AI results |
| **P0** | F-5.2 (prior): Rounding Modes TBD | Protocol Completeness | ReadReduce undefined |
| **P1** | F-3.5.1: Link Resiliency major DL architecture change | Implementation | Significant Hill Creek rework |
| **P1** | F-3.6.1: Link Folding < 250us power-up target | Implementation | Aggressive timing requirement |
| **P1** | F-4.3.2: RAMs require new PCS alignment logic | Implementation | New PCS feature |
| **P1** | F-3.4.1: TL Backpressure in DL Rx | Implementation | Required for UCIe chiplet |
| **P2** | C-3: Broken cross-reference in DLPL 2.7.1.5 | Draft Quality | Minor |
| **P2** | C-4: ToC numbering errors in DLPL | Draft Quality | Minor |
| **P2** | F-7.1: Common spec less mature than DLPL | Spec Maturity | Common is v0.9 Draft vs DLPL RC |

---

## 10. Recommendations

### For Specification Authors (UALink Consortium)

1. **Fix C-1:** Update Common Section 9.1 to acknowledge INC switch requirements.
2. **Complete Common TBDs:** Sections 6.5 (Reproducibility) and 6.6 (Rounding Modes) are blocking.
3. **Fix C-3:** Update DLPL Section 2.7.1.5 cross-reference from "6.4.3.3" to "2.4.3.3".
4. **Fix C-4:** Correct Table of Contents numbering in DLPL.
5. **Fix C-2:** Remove typo in Common Section 9.8.

### For LNR Switch Implementation (Cornelis Networks)

6. **Prioritize Link Resiliency assessment:** This is the most architecturally significant DLPL change. Evaluate Hill Creek MAC/DL architecture for 2-PL bonding, TDM, and reordering support.
7. **Assess Link Folding feasibility:** Determine if Hill Creek SerDes supports < 250us power-up without AN/LT re-run. Evaluate DL PwrDn state machine integration.
8. **Plan for RAM support in PCS:** Rapid Alignment Markers require new PCS logic for generation, lock, and transition to AM lock.
9. **Validate TL Backpressure path:** If LNR uses UCIe die-to-die (confirmed in HAS), the TL backpressure handling in DL Rx is mandatory.
10. **Track Common spec maturity:** The Common spec (v0.9 Draft) is less mature than the DLPL spec (RC). Monitor for changes in INC, Security, and Switch Requirements chapters before finalizing implementation.

---

## 11. Conclusion

The v1.5 specification suite represents a **substantial evolution** from v1.0 across both the protocol layer (Common spec) and the link/physical layer (DLPL spec).

**Common Spec** adds In-Network Collectives as the headline feature, transforming the switch from a passive relay to an active compute participant. This is the most impactful change for switch ASIC architecture.

**DLPL Spec** adds Link Resiliency and Link Folding as the headline features, enabling fault-tolerant operation and power management at the link level. These features add significant complexity to the DL state machine (new DL PwrDn state, per-PL "sub" state machines, reordering logic) and PCS (Rapid Alignment Markers, parallel symbol pair search).

The core protocol parameters (DL Flit size, TL Flit size, CRC, sequence numbering, FEC, SerDes rates) are **unchanged**, ensuring backward compatibility at the physical and data link layers. All new features are additive.

For the LNR Switch, the combined impact of INC (from Common) and Link Resiliency/Folding (from DLPL) represents the two largest implementation efforts. The DLPL changes primarily affect the Hill Creek MAC/PCS IP, while the Common changes primarily affect the LNR switch core (Rpipe, Collectives Engine, security pipeline).

---

*End of Full Crosscheck Review Report*
