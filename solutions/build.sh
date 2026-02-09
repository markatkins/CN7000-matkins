#!/bin/bash

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INPUT_FILE="${SCRIPT_DIR}/solutions.md"
OUTPUT_DIR="${SCRIPT_DIR}/output"
TEMPLATES_DIR="${SCRIPT_DIR}/templates"
FILTERS_DIR="${TEMPLATES_DIR}/filters"

WORD_TEMPLATE="${TEMPLATES_DIR}/Standard_Tech Doc Word Template.dotx"
PPTX_TEMPLATE="${TEMPLATES_DIR}/custom-reference.pptx"

mkdir -p "${OUTPUT_DIR}"

build_docx() {
    echo "Building DOCX..."
    pandoc "${INPUT_FILE}" \
        --from markdown \
        --to docx \
        --reference-doc="${WORD_TEMPLATE}" \
        --lua-filter="${FILTERS_DIR}/docx-format.lua" \
        --toc \
        --toc-depth=3 \
        --shift-heading-level-by=-1 \
        -M title="CN7000 Solution and Feature Matrices" \
        -o "${OUTPUT_DIR}/solutions.docx"
    
    echo "Post-processing DOCX..."
    python3 "${FILTERS_DIR}/docx-postprocess.py" "${OUTPUT_DIR}/solutions.docx"
    
    echo "Created: ${OUTPUT_DIR}/solutions.docx"
}

build_pdf() {
    echo "Building PDF via Typst..."
    # Two-step process: pandoc -> typst source, then typst -> pdf
    local TEMP_TYP=$(mktemp --suffix=.typ)
    
    pandoc "${INPUT_FILE}" \
        --from markdown \
        --to typst \
        --lua-filter="${FILTERS_DIR}/typst-compat.lua" \
        --toc \
        --toc-depth=3 \
        -o "${TEMP_TYP}"
    
    typst compile "${TEMP_TYP}" "${OUTPUT_DIR}/solutions.pdf"
    
    rm -f "${TEMP_TYP}"
    echo "Created: ${OUTPUT_DIR}/solutions.pdf"
}

build_pptx() {
    echo "Building PPTX..."
    pandoc "${INPUT_FILE}" \
        --from markdown \
        --to pptx \
        --reference-doc="${PPTX_TEMPLATE}" \
        --lua-filter="${FILTERS_DIR}/pptx-tables.lua" \
        --slide-level=3 \
        -o "${OUTPUT_DIR}/solutions.pptx"
    
    echo "Post-processing PPTX (layout remapping)..."
    python3 "${FILTERS_DIR}/pptx-postprocess.py" "${OUTPUT_DIR}/solutions.pptx"
    
    echo "Created: ${OUTPUT_DIR}/solutions.pptx"
}

show_help() {
    echo "Usage: $0 [command]"
    echo ""
    echo "Commands:"
    echo "  all     Build all formats (docx, pdf, pptx)"
    echo "  docx    Build Word document only"
    echo "  pdf     Build PDF only (requires typst)"
    echo "  pptx    Build PowerPoint only"
    echo "  clean   Remove output directory"
    echo "  help    Show this help message"
    echo ""
    echo "If no command is specified, 'all' is assumed."
}

clean() {
    echo "Cleaning output directory..."
    rm -rf "${OUTPUT_DIR}"
    echo "Done."
}

case "${1:-all}" in
    all)
        build_docx
        build_pdf
        build_pptx
        echo ""
        echo "All builds complete!"
        ;;
    docx)
        build_docx
        ;;
    pdf)
        build_pdf
        ;;
    pptx)
        build_pptx
        ;;
    clean)
        clean
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "Unknown command: $1"
        show_help
        exit 1
        ;;
esac
