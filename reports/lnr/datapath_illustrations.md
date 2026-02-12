# LNR Data Path: Byte Alignment & Overhead Analysis

**Wire → MAC-PCS → MAC-Client → Crossbar**

Analysis of byte alignment, padding overhead, and storage efficiency for 64B, 72B,
and 128B Ethernet frames traversing the LNR switch receive data path.

---

## Table of Contents

- [Architectural Data Points](#architectural-data-points)
  - [Data Path Diagram (RX Direction)](#data-path-diagram-rx-direction)
- [Wire-Level Overhead (IEEE 802.3)](#wire-level-overhead-ieee-8023)
- [What Gets Stripped at Each Stage](#what-gets-stripped-at-each-stage)
- [Per-Packet Analysis](#per-packet-analysis)
  - [Definitions](#definitions)
  - [64-Byte Frame (Minimum Ethernet)](#64-byte-frame-minimum-ethernet)
  - [72-Byte Frame](#72-byte-frame)
  - [128-Byte Frame](#128-byte-frame)
- [Summary Table: End-to-End Byte Accounting](#summary-table-end-to-end-byte-accounting)
- [Key Takeaways](#key-takeaways)
- [References](#references)

---

## Architectural Data Points

Key interface widths, granularities, and alignment constraints extracted from the
Hill Creek (HLC) and LNR HAS documents.

| Stage | Interface Width | Granularity | Alignment | Source |
|-------|----------------|-------------|-----------|--------|
| **Wire (SerDes)** | 8 lanes × 212.5 Gbps PAM-4 | Bit-serial | N/A | HLC HAS `overview.md` |
| **PCS → MAC** | 1024 bits (128B) | 16 × 8B blocks | 8B block | HLC HAS `mac-client.md:370` |
| **MAC → MAC-Client RX** | 1024 bits (128B) | 16 × 8B blocks | 8B block | HLC HAS `mac-client.md:1256` |
| **MAC-Client RX → SoC (Rbuf)** | 2048 bits (256B) | 4 × 64B segments | 64B segment | HLC HAS `interfaces.md:117-119` |
| **Rbuf** | 2048 bits (256B) | 64B chunks | 64B aligned | LNR HAS `04_Major_Blocks.md` |
| **Gearbox (Rbuf→Xbar)** | 256B → 192B | 12B sub-channels | 12B | LNR HAS `04_Major_Blocks.md:365` |
| **Data Crossbar** | 192B channels (2×96B) | 8 × 12B sub-channels | 12B | LNR HAS `05_On_Chip_Networks.md` |
| **Lbuf** | 128B chunks | 128B credit unit | 128B aligned | LNR HAS `04_Major_Blocks.md:423` |
| **Gearbox (Xbar→Lbuf)** | 192B → 128B | — | 128B | LNR HAS `04_Major_Blocks.md:368` |
| **Lbuf → TBUF (via Xbar out)** | 192B (2×96B) | 12B blocks | 12B | HLC HAS `tbuf.md:200-208` |
| **Transfer Unit (BW metering)** | 16B | — | 16B | LNR HAS `06_Key_Functions.md:82` |

### Data Path Diagram (RX Direction)

```
Wire (8×212.5G PAM-4)
  │
  ▼
┌─────────────────────────────────────────────────────────────┐
│  SerDes RX  (8 lanes, 512 bits per lane per cycle)          │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  PCS  (256b/257b decode, FEC RS(544,514), lane alignment)   │
│  Strips: FEC parity, encoding overhead                      │
└─────────────────────────┬───────────────────────────────────┘
                          │  1024-bit (128B), 16 × 8B blocks
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  Ethernet MAC  (Alphawave IP)                               │
│  Strips: Preamble (7B), SFD (1B)                            │
│  Validates & strips: FCS (4B)                               │
│  Reports: mac_rx_pkt_err, PTP timestamps                    │
└─────────────────────────┬───────────────────────────────────┘
                          │  1024-bit (128B), 16 × 8B blocks
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  MAC-Client RX  (Cornelis IP, inside Hill Creek)            │
│  Width convert: 1024-bit → 2048-bit                         │
│  Segment align: packets → 4 × 64B segments                  │
│  Adds: ECC (8b per 8B word), control parity                 │
└─────────────────────────┬───────────────────────────────────┘
                          │  2048-bit (256B), 4 × 64B segments
                          │  + 256-bit ECC, 8-bit ctl parity
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  Rbuf  (in SoC, outside Hill Creek)                         │
│  Storage: 64B-aligned chunks, SECDED ECC                    │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  Gearbox  (256B → 192B)                                     │
│  Converts Rbuf format to crossbar channel format            │
└─────────────────────────┬───────────────────────────────────┘
                          │  192B (2 × 96B segments)
                          │  16 × 12B sub-channel locations
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  Data Crossbar                                              │
│  External: 192B channels @ 1.66 GHz                         │
│  Internal: 96B @ 3.33 GHz                                   │
│  Sub-channels: 8 × 12B per channel (576 effective radix)    │
│  Packet modes: 192B (small-pkt-optimized) or 128B (low-lat) │
└─────────────────────────┬───────────────────────────────────┘
                          │  192B → 128B (via gearbox)
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  Lbuf                                                       │
│  Storage: 128B-aligned chunks, 128B credit unit             │
└─────────────────────────┬───────────────────────────────────┘
                          │  128B → 192B (via gearbox)
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  TBUF  (inside Hill Creek, egress port)                     │
│  Input: 192B (2×96B), 12B granularity (switch crossbar)     │
│  Storage: 64B-aligned per-VL vFIFOs (96 total)              │
│  Output: 2048-bit (256B), 4 × 64B segments                  │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
                    MAC-Client TX → MAC → PCS → SerDes TX → Wire
```

---

## Wire-Level Overhead (IEEE 802.3)

Per IEEE 802.3, an Ethernet frame on the wire includes:

| Component | Bytes | Notes |
|-----------|-------|-------|
| Preamble | 7 | Alternating 10101010 pattern |
| SFD | 1 | Start Frame Delimiter (10101011) |
| **Frame** (DA+SA+Type+Payload+FCS) | Variable | This is the "packet size" being analyzed |
| FCS | 4 | Included in frame size; CRC-32 |
| IFG | 12 | Inter-Frame Gap (minimum) |

**Total wire overhead per frame**: 7 (preamble) + 1 (SFD) + 12 (IFG) = **20 bytes**
surrounding each frame.

> **Note**: The FCS (4B) is part of the frame itself. The MAC validates FCS and
> strips it before forwarding to the MAC-Client. So the "frame on wire" includes
> FCS, but the "packet delivered to SoC" does not.

---

## What Gets Stripped at Each Stage

| Stage | What's Removed | What's Added | Reference |
|-------|---------------|-------------|-----------|
| **PCS** | FEC overhead (RS(544,514) parity), 256b/257b encoding overhead | — | HLC HAS `overview.md:83-89` |
| **MAC** | Preamble (7B), SFD (1B), FCS (4B) validated & stripped | Error flags, PTP timestamps | HLC HAS `overview.md:62-64`, `mac-client.md:1187` |
| **MAC-Client RX** | Nothing removed | ECC (8b per 8B block), control parity, segment alignment padding | HLC HAS `interfaces.md:144-165`, `mac-client.md:1195-1198` |

---

## Per-Packet Analysis

### Definitions

- **Frame on wire** = DA(6) + SA(6) + EtherType(2) + Payload + FCS(4) = stated packet size
- **Wire occupancy** = Preamble(7) + SFD(1) + Frame + IFG(12) = Frame + 20
- **Post-MAC payload** = Frame − FCS(4) = the data delivered to MAC-Client
- **MAC interface** = 1024-bit (128B), 16 × 8B blocks, packed with SOP/EOP markers
- **HLC RX interface** = 2048-bit (256B), 4 × 64B segments, 64B-aligned
- **Rbuf storage** = 64B-aligned chunks with SECDED ECC
- **Crossbar transfer** = 192B (2 × 96B segments), 12B granularity
- **Lbuf storage** = 128B-aligned chunks

---

### 64-Byte Frame (Minimum Ethernet)

| Stage | Data Bytes | Overhead/Padding | Total Consumed | Efficiency |
|-------|-----------|-------------------|----------------|------------|
| **Wire** | 64 (incl. 4B FCS) | +20 (7 pre + 1 SFD + 12 IFG) | **84B** | 76.2% |
| **MAC output** | 60 (FCS stripped) | Packed in 8B blocks → 8 blocks (64B) | **64B** (8 × 8B blocks) | 93.8% |
| **MAC-Client RX → SoC** | 60 | Aligned to 64B segment → 4B pad | **64B** (1 segment) | 93.8% |
| **Rbuf** | 60 | 64B-aligned storage + 8B ECC per 8B word | **64B data + 8B ECC = 72B** | 83.3% |
| **Crossbar (12B mode)** | 60 | ⌈60/12⌉ = 5 × 12B blocks = 60B | **60B** (5 locations) | 100% |
| **Crossbar channel** | 60 | 5 of 16 locations used (192B channel) | **192B slot** | 31.3% |
| **Lbuf** | 60 | 128B-aligned → 68B pad | **128B** (1 credit unit) | 46.9% |
| **Transfer Units** | 60 | ⌈60/16⌉ = 4 TUs | **64B** (4 × 16B) | 93.8% |

**Key observations for 64B**:

- The minimum Ethernet frame (64B on wire, 60B post-FCS) fits in exactly **1 segment**
  at the HLC RX interface.
- At the crossbar, it uses only 5 of 16 available 12B locations per segment —
  **31.3% channel utilization**.
- In Lbuf, it wastes 68B of the 128B credit unit — **46.9% storage efficiency**.
- The MAC-Client can pack **2 × 64B packets per 1024-bit MAC word**
  (per HLC HAS `mac-client.md` Fig. packet-packing-64B).
- At the TBUF output (2048-bit), **4 × 64B packets fit per cycle** (4 segments).

---

### 72-Byte Frame

| Stage | Data Bytes | Overhead/Padding | Total Consumed | Efficiency |
|-------|-----------|-------------------|----------------|------------|
| **Wire** | 72 (incl. 4B FCS) | +20 | **92B** | 78.3% |
| **MAC output** | 68 (FCS stripped) | ⌈68/8⌉ = 9 blocks → 72B | **72B** (9 × 8B blocks) | 94.4% |
| **MAC-Client RX → SoC** | 68 | Spans 2 × 64B segments (68 > 64) → 60B pad in seg 1 | **128B** (2 segments) | 53.1% |
| **Rbuf** | 68 | 2 × 64B chunks + ECC | **128B data + 16B ECC = 144B** | 47.2% |
| **Crossbar (12B mode)** | 68 | ⌈68/12⌉ = 6 × 12B blocks = 72B | **72B** (6 locations) | 94.4% |
| **Crossbar channel** | 68 | 6 of 16 locations (spans into seg 1) | **192B slot** | 35.4% |
| **Lbuf** | 68 | 128B-aligned → 60B pad | **128B** (1 credit unit) | 53.1% |
| **Transfer Units** | 68 | ⌈68/16⌉ = 5 TUs | **80B** (5 × 16B) | 85.0% |

**Key observations for 72B**:

- At 68B post-FCS, this packet **just barely exceeds** the 64B segment boundary.
- This causes it to consume **2 segments** (128B) at the HLC RX interface for only
  68B of data — a significant efficiency cliff.
- At the MAC interface, it needs 9 × 8B blocks, which means it spans beyond one half
  of the 1024-bit word.
- The MAC-Client packing shows this: per HLC HAS `mac-client.md` Fig.
  packet-packing-65B, even 65B packets span two TBUF segments.
- Crossbar efficiency is slightly better (6 of 16 locations) but still under 40%.
- Lbuf fits in 1 credit unit (128B) since 68B < 128B.

---

### 128-Byte Frame

| Stage | Data Bytes | Overhead/Padding | Total Consumed | Efficiency |
|-------|-----------|-------------------|----------------|------------|
| **Wire** | 128 (incl. 4B FCS) | +20 | **148B** | 86.5% |
| **MAC output** | 124 (FCS stripped) | ⌈124/8⌉ = 16 blocks → 128B | **128B** (16 × 8B blocks, fills entire MAC word) | 96.9% |
| **MAC-Client RX → SoC** | 124 | Spans 2 × 64B segments → 4B pad in seg 1 | **128B** (2 segments) | 96.9% |
| **Rbuf** | 124 | 2 × 64B chunks + ECC | **128B data + 16B ECC = 144B** | 86.1% |
| **Crossbar (12B mode)** | 124 | ⌈124/12⌉ = 11 × 12B blocks = 132B | **132B** (11 locations) | 93.9% |
| **Crossbar channel** | 124 | 11 of 16 locations | **192B slot** | 64.6% |
| **Lbuf** | 124 | 128B-aligned → 4B pad | **128B** (1 credit unit) | 96.9% |
| **Transfer Units** | 124 | ⌈124/16⌉ = 8 TUs | **128B** (8 × 16B) | 96.9% |

**Key observations for 128B**:

- 124B post-FCS fills the MAC word almost perfectly (16 × 8B blocks = 128B, with 4B
  unused in last block).
- Per HLC HAS `mac-client.md` Fig. packet-packing-128B: one 128B packet fills an
  entire MAC cycle — **1 packet per MAC word**.
- At the HLC RX interface, it uses exactly 2 segments with only 4B wasted — excellent
  alignment.
- Crossbar uses 11 of 16 locations — **64.6% channel utilization**, much better than
  small packets.
- Lbuf: 124B fits in 1 credit unit (128B) with only 4B waste — near-perfect.

---

## Summary Table: End-to-End Byte Accounting

```
                          64B Frame       72B Frame       128B Frame
                          ─────────       ─────────       ──────────
Wire (with overhead)        84B             92B             148B
  Preamble+SFD              8B              8B               8B
  Frame (incl FCS)         64B             72B             128B
  IFG                      12B             12B              12B

Post-MAC (FCS stripped)    60B             68B             124B

MAC Interface (8B blks)    64B (8 blks)    72B (9 blks)    128B (16 blks)
  Blocks used/available    8/16            9/16            16/16

HLC RX (64B segments)      64B (1 seg)     128B (2 seg)    128B (2 seg)
  Segment efficiency       93.8%           53.1%           96.9%

Rbuf (64B aligned)         64B             128B            128B
  + ECC overhead           +8B             +16B            +16B

Crossbar (12B blocks)      60B (5 locs)    72B (6 locs)    132B (11 locs)
  Channel utilization      31.3%           35.4%           64.6%

Lbuf (128B aligned)        128B            128B            128B
  Storage efficiency       46.9%           53.1%           96.9%

Transfer Units (16B)       4 TUs (64B)     5 TUs (80B)     8 TUs (128B)
  BW meter efficiency      93.8%           85.0%           96.9%
```

---

## Key Takeaways

1. **The 64B segment boundary is the critical cliff**: A 72B frame (68B post-FCS)
   consumes **2× the HLC RX segments** compared to a 64B frame (60B post-FCS),
   despite being only 8 bytes larger. This is the single biggest efficiency drop in
   the entire pipeline.

2. **12B crossbar granularity is efficient for all sizes**: The crossbar's 12B
   sub-channel granularity means waste is at most 11B per packet (less than one
   block). This is a good design choice.

3. **128B Lbuf alignment penalizes small packets heavily**: A 60B packet wastes 53%
   of its Lbuf credit unit. This is the cost of the 128B credit-based flow control
   system.

4. **MAC-Client packing mitigates small-packet overhead**: The MAC-Client can pack
   up to 3 packets per 1024-bit MAC word, and the TBUF output delivers 4 × 64B
   segments per cycle. For 64B packets, this means up to **4 packets per TBUF
   cycle** — critical for small-packet throughput.

5. **Wire efficiency improves with packet size**: 76.2% for 64B → 78.3% for 72B →
   86.5% for 128B, due to the fixed 20B per-frame overhead (preamble + SFD + IFG).

---

## References

| Document | Location | Content |
|----------|----------|---------|
| HLC HAS `overview.md` | `earlysim/docs/HAS/HLC/overview.md` | Hill Creek overview, key capabilities, TX/RX data paths |
| HLC HAS `mac-client.md` | `earlysim/docs/HAS/HLC/mac-client.md` | MAC-Client TX/RX architecture, width conversion, packet packing |
| HLC HAS `interfaces.md` | `earlysim/docs/HAS/HLC/interfaces.md` | Signal definitions for all Hill Creek interfaces |
| HLC HAS `tbuf.md` | `earlysim/docs/HAS/HLC/tbuf.md` | TBUF architecture, crossbar/NIC interfaces, subdivision modes |
| LNR HAS `04_Major_Blocks.md` | `lnr/docs/has/04_Major_Blocks.md` | Rbuf, Lbuf, gearbox, MPORT interface details |
| LNR HAS `05_On_Chip_Networks.md` | `lnr/docs/has/05_On_Chip_Networks.md` | Data crossbar architecture, sub-channels, packet modes |
| LNR HAS `06_Key_Functions.md` | `lnr/docs/has/06_Key_Functions.md` | Transfer unit (16B), BW metering, reservation ring |
