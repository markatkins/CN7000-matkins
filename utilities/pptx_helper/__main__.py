"""
Entry point for running pptx_helper as a module.

Usage:
    python -m utilities.pptx_helper --help
    python -m utilities.pptx_helper --type progress --data data.yaml --output report.pptx
"""

from utilities.pptx_helper.cli import main

if __name__ == '__main__':
    main()
