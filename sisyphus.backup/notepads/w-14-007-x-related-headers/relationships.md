# W-14-007: x-related-headers Relationship Mapping

## Relationship Vocabulary

| Relationship | Meaning | Example |
|--------------|---------|---------|
| `contains` | This packet contains instances of the referenced type | dl_flit → segment_header |
| `references` | This packet references fields/types from the other | request_field → status_codes |
| `extends` | This packet extends or specializes the other | command_header → flit_header |
| `uses` | This packet uses the referenced protocol/mechanism | tl_flit → compression |
| `part-of` | This packet is a component of the referenced type | segment_header → dl_flit |

---

## Layer: UPLI (8 files)

### commands.ksy
- **references** → `status_codes.ksy` (response status codes)
- **references** → `request_channel.ksy` (command opcodes used in requests)

### request_channel.ksy
- **references** → `commands.ksy` (ReqCmd field uses command opcodes)
- **references** → `originator_data_channel.ksy` (ReqNumBeats indicates data beats)
- **uses** → `../security/encryption.ksy` (ReqAuthTag for security)

### read_response_channel.ksy
- **references** → `status_codes.ksy` (RdRspStatus field)
- **uses** → `../security/encryption.ksy` (authentication)

### write_response_channel.ksy
- **references** → `status_codes.ksy` (WrRspStatus field)
- **uses** → `../security/encryption.ksy` (authentication)

### status_codes.ksy
- (No outgoing references - this is a leaf enumeration file)

### originator_data_channel.ksy
- **part-of** → `request_channel.ksy` (data beats follow requests)
- **uses** → `../security/encryption.ksy` (data encryption)

### protocols/flow_control.ksy
- **uses** → `request_channel.ksy` (credit management)
- **uses** → `read_response_channel.ksy` (credit management)
- **uses** → `write_response_channel.ksy` (credit management)

### protocols/connection_handshake.ksy
- **uses** → `../datalink/protocols/link_state.ksy` (link state during handshake)

---

## Layer: Transaction (9 files)

### tl_flit.ksy
- **contains** → `control_half_flit.ksy` (half-flit 0 or 1 can be control)
- **contains** → `data_half_flit.ksy` (half-flit 0 or 1 can be data)
- **contains** → `message_half_flit.ksy` (half-flit 0 or 1 can be message)
- **part-of** → `../datalink/dl_flit.ksy` (TL Flits pack into DL Flits)
- **uses** → `protocols/compression.ksy` (field compression)

### control_half_flit.ksy
- **contains** → `request_field.ksy` (control half-flit contains request fields)
- **contains** → `response_field.ksy` (control half-flit contains response fields)
- **contains** → `flow_control_field.ksy` (control half-flit contains FC/NOP)
- **part-of** → `tl_flit.ksy` (half-flit is part of TL Flit)

### message_half_flit.ksy
- **part-of** → `tl_flit.ksy` (half-flit is part of TL Flit)

### data_half_flit.ksy
- **part-of** → `tl_flit.ksy` (half-flit is part of TL Flit)
- **uses** → `../security/encryption.ksy` (data encryption)

### request_field.ksy
- **part-of** → `control_half_flit.ksy` (request field packed in control half-flit)
- **references** → `../upli/commands.ksy` (command opcodes)
- **uses** → `protocols/address_cache.ksy` (compressed requests use address cache)

### response_field.ksy
- **part-of** → `control_half_flit.ksy` (response field packed in control half-flit)
- **references** → `../upli/status_codes.ksy` (response status codes)

### flow_control_field.ksy
- **part-of** → `control_half_flit.ksy` (FC/NOP packed in control half-flit)
- **references** → `../upli/protocols/flow_control.ksy` (credit management)

### protocols/compression.ksy
- **uses** → `protocols/address_cache.ksy` (compression uses address cache)
- **references** → `request_field.ksy` (compressed request format)
- **references** → `response_field.ksy` (compressed response format)

### protocols/address_cache.ksy
- **uses** → `request_field.ksy` (cache entries for request addresses)

---

## Layer: Datalink (12 files)

### dl_flit.ksy
- **contains** → `flit_header.ksy` (3-byte header at start)
- **contains** → `segment_header.ksy` (5 segment headers, one per segment)
- **contains** → `crc.ksy` (4-byte CRC at end)
- **contains** → `../transaction/tl_flit.ksy` (up to 10 TL Flits packed)
- **uses** → `protocols/link_level_replay.ksy` (replay mechanism)

### flit_header.ksy
- **part-of** → `dl_flit.ksy` (header is part of DL Flit)
- **references** → `protocols/link_level_replay.ksy` (sequence numbers for replay)

### segment_header.ksy
- **part-of** → `dl_flit.ksy` (segment headers are part of DL Flit)
- **references** → `../transaction/tl_flit.ksy` (indicates TL Flit presence)

### crc.ksy
- **part-of** → `dl_flit.ksy` (CRC is part of DL Flit)

### messages/basic_messages.ksy
- **part-of** → `dl_flit.ksy` (DL messages in alternative sectors)
- **references** → `segment_header.ksy` (DLAltSector indicates message presence)

### messages/control_messages.ksy
- **part-of** → `dl_flit.ksy` (DL messages in alternative sectors)
- **uses** → `protocols/link_state.ksy` (link state control)

### messages/uart_messages.ksy
- **part-of** → `dl_flit.ksy` (DL messages in alternative sectors)

### messages/vendor_defined.ksy
- **part-of** → `dl_flit.ksy` (DL messages in alternative sectors)

### protocols/link_state.ksy
- **uses** → `flit_header.ksy` (state transitions via flit commands)
- **uses** → `protocols/link_resiliency.ksy` (state recovery)

### protocols/link_resiliency.ksy
- **uses** → `protocols/link_level_replay.ksy` (replay for recovery)
- **uses** → `protocols/link_state.ksy` (state management)

### protocols/link_level_replay.ksy
- **references** → `flit_header.ksy` (sequence numbers in header)
- **references** → `dl_flit.ksy` (replay buffer stores flits)

### protocols/link_folding.ksy
- **uses** → `dl_flit.ksy` (folding affects flit transmission)
- **uses** → `../physical/reconciliation_sublayer.ksy` (RS interface)

---

## Layer: Physical (4 files)

### reconciliation_sublayer.ksy
- **uses** → `../datalink/dl_flit.ksy` (RS receives flits from DL)
- **uses** → `control_ordered_sets.ksy` (RS handles ordered sets)
- **uses** → `alignment_markers.ksy` (RS handles alignment)

### control_ordered_sets.ksy
- **uses** → `protocols/link_training.ksy` (ordered sets during training)
- **part-of** → `reconciliation_sublayer.ksy` (ordered sets via RS)

### alignment_markers.ksy
- **part-of** → `reconciliation_sublayer.ksy` (alignment via RS)
- **uses** → `protocols/link_training.ksy` (alignment during training)

### protocols/link_training.ksy
- **uses** → `control_ordered_sets.ksy` (training sequences)
- **uses** → `alignment_markers.ksy` (lane alignment)
- **uses** → `../datalink/protocols/link_state.ksy` (state transitions)

---

## Layer: Security (5 files)

### encryption.ksy
- **uses** → `iv_format.ksy` (IV for AES-GCM)
- **uses** → `protocols/key_derivation.ksy` (key material)
- **references** → `../upli/request_channel.ksy` (encrypted fields)
- **references** → `../upli/read_response_channel.ksy` (encrypted fields)
- **references** → `../upli/write_response_channel.ksy` (encrypted fields)
- **references** → `../upli/originator_data_channel.ksy` (encrypted fields)

### authentication.ksy
- **uses** → `encryption.ksy` (AES-GCM provides authentication)
- **uses** → `iv_format.ksy` (IV for authentication)

### iv_format.ksy
- **part-of** → `encryption.ksy` (IV used in encryption)
- **part-of** → `authentication.ksy` (IV used in authentication)

### protocols/key_derivation.ksy
- **uses** → `protocols/key_rotation.ksy` (key rotation triggers derivation)

### protocols/key_rotation.ksy
- **uses** → `protocols/key_derivation.ksy` (rotation derives new keys)
- **uses** → `../datalink/protocols/link_state.ksy` (rotation during link state)

---

## Summary Statistics

| Layer | Files | With Relationships |
|-------|-------|-------------------|
| UPLI | 8 | 7 (status_codes.ksy is leaf) |
| Transaction | 9 | 9 |
| Datalink | 12 | 12 |
| Physical | 4 | 4 |
| Security | 5 | 5 |
| **Total** | **38** | **37** |

Note: `status_codes.ksy` is a leaf enumeration file with no outgoing relationships.
It will still receive incoming references from other files.
