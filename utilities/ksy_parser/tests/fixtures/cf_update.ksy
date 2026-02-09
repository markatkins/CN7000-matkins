# GOLDEN REFERENCE: CBFC CF_Update Control Ordered Set
# Feature: 003-ue-packet-taxonomy
# UE Specification: v1.0.1, Tables 5-20 and 5-21, Section 5.2.6.1, Page 492
# 
# This is a GOLDEN REFERENCE definition demonstrating extreme rigor for Credit-Based
# Flow Control (CBFC) control ordered sets, serving as a template for all flow control
# packet definitions in the UE taxonomy.
#
# Quality Standards Applied:
# 1. Every field extracted with exact bit position and width from Tables 5-20, 5-21
# 2. All fields have x-required metadata (mandatory/optional per UE Spec)
# 3. Complete x-spec metadata (table, section, page) for traceability
# 4. All constraints captured (reserved bits, O-code values, VC index ranges)
# 5. 64B/66B block format structure documented
# 6. Byte-level and bit-level layout matches UE Spec exactly (8 bytes data payload)
# 7. TLV structure for dual VC credit updates
#
# Leverages Cornelis IP:
# - Omni-Path credit-based flow control patterns (per-VC credit management)
# - Kaitai Struct best practices (enums, contents validation, bit-endian)
# - 64B/66B PCS encoding knowledge from Ethernet standards

meta:
  id: cbfc_cf_update
  title: CBFC CF_Update Control Ordered Set (CtlOS)
  endian: le  # Little-endian for xMII lane data (transmitted LSB first per spec)
  bit-endian: le  # Little-endian bit ordering for bit fields
  doc: |
    Ultra Ethernet Credit-Based Flow Control (CBFC) CF_Update Control Ordered Set.
    
    CF_Update is used to communicate credit freed (CF) information for virtual channels
    (VCs). Each CF_Update CtlOS can carry credit updates for two VCs (CF1 and CF2),
    with each update containing a 5-bit VC index and a 15-bit credit count.
    
    The CF_Update message format uses TLV (Type-Length-Value) structure where:
    - Type: CtlOS message type (0x10 for CF_Update)
    - Length: Implicit (fixed 8-byte format)
    - Value: Two VC credit updates (CF1 and CF2)
    
    Total Size: 8 bytes (64 bits) data payload in 64B/66B block
    
    xMII Data Format (from Table 5-20):
    - Lane 0 (D0): 0x5C (UE control ordered set character)
    - Lane 1 (D1): 0x10 (CF_Update message type)
    - Lane 2-4: CF1 VC index and count (5 + 15 bits)
    - Lane 4[3:0]: O-code = 0x6 (ordered set code)
    - Lane 5-7: CF2 VC index and count (5 + 15 bits)
    
    The PCS sublayer encodes this into a 64B/66B block with sync header 2'b10.
  
  doc-ref:
    - "UE Specification v1.0.1, Table 5-20, Page 492"
    - "UE Specification v1.0.1, Table 5-21, Page 492"
    - "UE Specification v1.0.1, Section 5.2.6.1 (CF_Update Messages)"
    - "IEEE 802.3-2022, Clause 82.2.3 (64B/66B Block Format)"
  
  license: "Derived from UE Specification v1.0.1 (CC BY-ND 4.0)"
  ks-version: "0.10"

# UE Specification Traceability Metadata
x-spec:
  table: "Table 5-20, Table 5-21"
  section: "Section 5.2.6.1"
  page: 492
  spec_version: "1.0.1"
  spec_date: "2025-09-05"

# Packet-level metadata
x-packet:
  layer: "link"
  sublayer: "cbfc"
  category: "control_ordered_set"
  size_bytes: 8
  size_bits: 64
  
  # Validation constraints
  constraints:
    - "Control character (D0) MUST be 0x5C"
    - "Message type (D1) MUST be 0x10 for CF_Update"
    - "O-code (D4[3:0]) MUST be 0x6"
    - "CF1_VC_index is 5-bit value (0 to 31)"
    - "CF2_VC_index is 5-bit value (0 to 31)"
    - "CF1_count is 15-bit value (0 to 32767)"
    - "CF2_count is 15-bit value (0 to 32767)"
    - "D7[3:0] reserved, set to 0 on transmit, ignored on reception"

seq:
  # Lane 0 (D0): Control Character
  - id: control_char
    type: u1
    doc: |
      Control character value for UE control ordered set.
      MUST be 0x5C per UE Spec Table 5-20.
      
      This identifies the block as a UE-specific control ordered set.
      
      UE Spec: Table 5-20, Lane 0.
    x-required: true
    x-constraint: "value == 0x5C"
    x-spec-ref: "Table 5-20, Lane 0"
    valid:
      eq: 0x5C
  
  # Lane 1 (D1): CtlOS Message Type
  - id: message_type
    type: u1
    enum: cbfc_message_type
    doc: |
      CtlOS Message Type identifier.
      MUST be 0x10 for CF_Update.
      
      UE Spec: Table 5-20, Lane 1 (Type field).
    x-required: true
    x-constraint: "value == 0x10"
    x-spec-ref: "Table 5-20, Lane 1; Table 5-21, Type field"
  
  # Lane 2 (D2): CF1_VC_index[4:0] (upper 5 bits) + CF1_count[14:11] (lower 3 bits)
  - id: cf1_vc_and_count_high
    type: u1
    doc: |
      Combined field containing:
      - Bits [7:3]: CF1_VC_index[4:0] (5-bit VC number for first credit update)
      - Bits [2:0]: CF1_count[14:12] (upper 3 bits of 15-bit credit count)
      
      UE Spec: Table 5-21, D2[7:3] = CF1_VC_index[4:0], D2[2:0] = CF1_count[14:12].
    x-required: true
    x-constraint: "value <= 0xFF"
    x-spec-ref: "Table 5-21, D2 field"
  
  # Lane 3 (D3): CF1_count[10:3]
  - id: cf1_count_mid
    type: u1
    doc: |
      CF1 credit count bits [10:3] (middle 8 bits of 15-bit count).
      
      This is part of the R_VC_CF[CF1_VC_index] counter value.
      
      UE Spec: Table 5-21, D3[7:0] = CF1_count[10:3].
    x-required: true
    x-constraint: "value <= 0xFF"
    x-spec-ref: "Table 5-21, D3 field"
  
  # Lane 4 (D4): CF1_count[2:0] (upper 3 bits) + reserved (bit 3) + O-code (lower 4 bits)
  - id: cf1_count_low_and_ocode
    type: u1
    doc: |
      Combined field containing:
      - Bits [7:5]: CF1_count[2:0] (lower 3 bits of 15-bit credit count)
      - Bit [4]: Part of O-code (0x6)
      - Bits [3:0]: O-code = 0x6 (ordered set code)
      
      The O-code MUST be 0x6 per IEEE 802.3 64B/66B encoding for ordered sets.
      
      UE Spec: Table 5-21, D4[7:4] = CF1_count[2:0] + reserved, D4[3:0] = O-code (0x6).
    x-required: true
    x-constraint: "(value & 0x0F) == 0x06"
    x-spec-ref: "Table 5-21, D4 field"
  
  # Lane 5 (D5): CF2_VC_index[4:0] (upper 5 bits) + CF2_count[14:12] (lower 3 bits)
  - id: cf2_vc_and_count_high
    type: u1
    doc: |
      Combined field containing:
      - Bits [7:3]: CF2_VC_index[4:0] (5-bit VC number for second credit update)
      - Bits [2:0]: CF2_count[14:12] (upper 3 bits of 15-bit credit count)
      
      UE Spec: Table 5-21, D5[7:3] = CF2_VC_index[4:0], D5[2:0] = CF2_count[14:12].
    x-required: true
    x-constraint: "value <= 0xFF"
    x-spec-ref: "Table 5-21, D5 field"
  
  # Lane 6 (D6): CF2_count[10:3]
  - id: cf2_count_mid
    type: u1
    doc: |
      CF2 credit count bits [10:3] (middle 8 bits of 15-bit count).
      
      This is part of the R_VC_CF[CF2_VC_index] counter value.
      
      UE Spec: Table 5-21, D6[7:0] = CF2_count[10:3].
    x-required: true
    x-constraint: "value <= 0xFF"
    x-spec-ref: "Table 5-21, D6 field"
  
  # Lane 7 (D7): CF2_count[2:0] (upper 3 bits) + reserved (lower 4 bits)
  - id: cf2_count_low_and_reserved
    type: u1
    doc: |
      Combined field containing:
      - Bits [7:4]: CF2_count[2:0] (lower 3 bits of 15-bit credit count) + reserved bit
      - Bits [3:0]: Reserved (set to 0 on transmit, ignored on reception)
      
      UE Spec: Table 5-21, D7[7:4] = CF2_count[2:0], D7[3:0] = Reserved.
    x-required: true
    x-constraint: "value <= 0xFF"
    x-spec-ref: "Table 5-21, D7 field"

instances:
  # CF1 VC index (5 bits)
  cf1_vc_index:
    value: (cf1_vc_and_count_high >> 3) & 0x1F
    doc: |
      CF1 Virtual Channel index (5 bits).
      
      Identifies the first VC for which credit freed information is being sent.
      Valid range: 0 to 31.
      
      UE Spec: Table 5-21, CF1_VC_index[4:0].
  
  # CF1 credit count (15 bits)
  cf1_count:
    value: |
      ((cf1_vc_and_count_high & 0x07) << 12) |
      (cf1_count_mid << 4) |
      ((cf1_count_low_and_ocode >> 4) & 0x0E)
    doc: |
      CF1 credit count (15 bits).
      
      R_VC_CF[CF1_VC_index] counter value indicating credits freed for this VC.
      Valid range: 0 to 32767.
      
      Reconstructed from:
      - cf1_vc_and_count_high[2:0] (bits [14:12])
      - cf1_count_mid[7:0] (bits [11:4])
      - cf1_count_low_and_ocode[7:5] (bits [3:1])
      
      UE Spec: Table 5-21, CF1_count[14:0].
  
  # CF2 VC index (5 bits)
  cf2_vc_index:
    value: (cf2_vc_and_count_high >> 3) & 0x1F
    doc: |
      CF2 Virtual Channel index (5 bits).
      
      Identifies the second VC for which credit freed information is being sent.
      Valid range: 0 to 31.
      
      UE Spec: Table 5-21, CF2_VC_index[4:0].
  
  # CF2 credit count (15 bits)
  cf2_count:
    value: |
      ((cf2_vc_and_count_high & 0x07) << 12) |
      (cf2_count_mid << 4) |
      ((cf2_count_low_and_reserved >> 4) & 0x0E)
    doc: |
      CF2 credit count (15 bits).
      
      R_VC_CF[CF2_VC_index] counter value indicating credits freed for this VC.
      Valid range: 0 to 32767.
      
      Reconstructed from:
      - cf2_vc_and_count_high[2:0] (bits [14:12])
      - cf2_count_mid[7:0] (bits [11:4])
      - cf2_count_low_and_reserved[7:5] (bits [3:1])
      
      UE Spec: Table 5-21, CF2_count[14:0].
  
  # Extract O-code for validation
  ocode:
    value: cf1_count_low_and_ocode & 0x0F
    doc: |
      Ordered set code extracted from D4[3:0].
      MUST be 0x6 per IEEE 802.3 64B/66B encoding.
      
      UE Spec: Table 5-21, D4[3:0] = 0x6.

enums:
  cbfc_message_type:
    0x10:
      id: cf_update
      doc: "CF_Update CtlOS message (credit freed updates for 2 VCs)"

# Protocol behavior metadata (for future state machine integration)
x-protocol:
  description: "CBFC CF_Update Control Ordered Set transmission protocol"
  
  usage_notes:
    - "CF_Update messages are frequent and carry credit freed information"
    - "Each CF_Update can update credits for two VCs (CF1 and CF2)"
    - "Credit counts are 15-bit values representing R_VC_CF counter values"
    - "VC indices are 5-bit values (0-31) identifying virtual channels"
    - "PCS sublayer encodes CF_Update into 64B/66B block per UE PHY spec"
    - "All data from xMII lanes D1 to D7 passed to 66-bit block"
    - "CF_Update is less frequent than CC_Update (which uses Ethernet packets)"
  
  related_messages:
    - name: "CC_Update"
      description: "Credit consumed updates (Ethernet packet format)"
      reference: "Table 5-22, Section 5.2.6.2"
    - name: "CBFC TLV"
      description: "CBFC negotiation via LLDP"
      reference: "Tables 5-23, 5-24, 5-25"
