# Draft: UE Tagged-Send and IPv4 Variants Documentation

## Requirements (confirmed)
- Create formal document in `analysis/packet_taxonomy/packet_taxonomy_ue_tagged_send_variants.md`
- Include ASCII wire format diagrams for all packet variants
- Create comparison table mapping UE+ to CN7000 Packet Taxonomy.ppt nomenclature
- Create work item for future tracking of comparison table

## Technical Decisions
- Document will follow existing packet_taxonomy_ue_*.md format
- Wire diagrams will use ASCII art consistent with existing docs
- Comparison table will be a separate section in the document

## Research Findings
- UE datamodel has 100 KSY files across transport/ses, transport/pds, transport/cms, transport/tss
- Key packet types identified:
  - UE Standard Tagged Send (100B header)
  - UE + CSIG Compact (108B)
  - UE + CSIG Wide (116B)
  - UE IPv4 Native (96B)
  - UE IPv4 + CSIG (104B/112B)
  - UE + Encrypted (116B + 16B auth)
  - UE Small Message (88B)
  - UE Rendezvous (132B)
  - UE Deferrable (100B)

## Scope Boundaries
- INCLUDE: All tagged-send variants, IPv4 encapsulations, wire diagrams, header size summary
- EXCLUDE: Response packets (covered in packet_taxonomy_ue_ses.md), link layer details

## Content Prepared
- Full document content drafted (see plan for reference)
- Wire format diagrams designed
- Header size summary table created
