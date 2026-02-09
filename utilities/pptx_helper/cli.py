"""
Command-line interface for Cornelis PowerPoint generation.

Usage:
    python -m utilities.pptx_helper --type progress --data data.yaml --output report.pptx
    python -m utilities.pptx_helper --type technical --data data.yaml --output tech.pptx
    python -m utilities.pptx_helper --help

Design:
    Provides a CLI wrapper around the pptx_helper module for generating
    presentations from YAML data files. Supports both progress reports
    and technical presentations.
"""

import argparse
import logging
import sys
from pathlib import Path
from typing import Any, Dict

import yaml

from utilities.pptx_helper import create_presentation, save_presentation
from utilities.pptx_helper.progress_report import (
    add_title_slide as add_progress_title,
    add_status_summary_slide,
    add_item_list_slide,
    add_comparison_slide,
    add_section_header as add_progress_section,
)
from utilities.pptx_helper.progress_report import add_status_summary_slide, add_comparison_slide
from utilities.pptx_helper.technical import (
    add_content_slide,
    add_image_slide,
    add_image_content_slide,
    add_table_slide,
    add_two_column_slide,
    add_code_slide,
)
from utilities.pptx_helper.navigation import (
    add_toc_slides,
    add_section,
    insert_slides_at_position,
)

logger = logging.getLogger(__name__)


def load_yaml_data(data_path: Path) -> Dict[str, Any]:
    """Load and parse YAML data file."""
    with open(data_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def generate_progress_report(data: Dict[str, Any], output_path: Path, dry_run: bool = False) -> None:
    """Generate a progress report presentation from YAML data."""
    if dry_run:
        logger.info("Dry run: validating progress report data...")
        _validate_progress_data(data)
        logger.info("Validation passed. Would generate presentation.")
        return
    
    prs = create_presentation()
    
    # Add title slide
    presenter = data.get('presenter', {})
    add_progress_title(
        prs,
        title=data.get('title', 'Progress Report'),
        subtitle=data.get('subtitle', ''),
        presenter_name=presenter.get('name', ''),
        presenter_info=presenter.get('info', '')
    )
    
    # Process sections
    for section in data.get('sections', []):
        section_type = section.get('type', '')
        
        if section_type == 'status_summary':
            add_status_summary_slide(
                prs,
                title=section.get('title', 'Status'),
                open_count=section.get('open_count', 0),
                closed_count=section.get('closed_count', 0),
                notes=section.get('notes', ''),
                subtitle=section.get('subtitle', '')
            )
        
        elif section_type == 'item_list':
            add_item_list_slide(
                prs,
                title=section.get('title', 'Items'),
                items=section.get('items', []),
                item_type=section.get('item_type', 'open'),
                subtitle=section.get('subtitle', '')
            )
        
        elif section_type == 'comparison':
            add_comparison_slide(
                prs,
                title=section.get('title', 'Comparison'),
                left_title=section.get('left_title', 'Left'),
                left_items=section.get('left_items', []),
                right_title=section.get('right_title', 'Right'),
                right_items=section.get('right_items', [])
            )
        
        elif section_type == 'section_header':
            add_progress_section(
                prs,
                title=section.get('title', ''),
                subtitle=section.get('subtitle', '')
            )
        
        else:
            logger.warning(f"Unknown section type: {section_type}")
    
    save_presentation(prs, output_path)
    logger.info(f"Progress report saved to: {output_path}")


def generate_technical_presentation(data: Dict[str, Any], output_path: Path, dry_run: bool = False, add_toc: bool = False) -> None:
    """Generate a technical presentation from YAML data."""
    if dry_run:
        logger.info("Dry run: validating technical presentation data...")
        _validate_technical_data(data)
        logger.info("Validation passed. Would generate presentation.")
        return
    
    prs = create_presentation()
    
    # Track section headers for TOC and PowerPoint sections
    section_header_slides = []  # List of (title, slide) tuples
    all_section_groups = {}  # Dict[section_name, List[Slide]]
    current_section_name = "Introduction"
    current_section_slides = []
    
    presenter = data.get('presenter', {})
    add_progress_title(
        prs,
        title=data.get('title', 'Technical Presentation'),
        subtitle=data.get('subtitle', ''),
        presenter_name=presenter.get('name', ''),
        presenter_info=presenter.get('info', '')
    )
    
    for section in data.get('sections', []):
        section_type = section.get('type', '')
        
        if section_type == 'content':
            add_content_slide(
                prs,
                title=section.get('title', ''),
                bullets=section.get('bullets', []),
                subtitle=section.get('subtitle', '')
            )
        
        elif section_type == 'bullets':
            add_content_slide(
                prs,
                title=section.get('title', ''),
                bullets=section.get('bullets', []),
                subtitle=section.get('subtitle', '')
            )
        
        elif section_type in ('item_list', 'bullet_list'):
            items = section.get('items', [])
            item_type = section.get('item_type', 'closed')
            if item_type == 'open':
                items = [f"○ {item}" if not item.startswith(('○', '●', '•', '-')) else item for item in items]
            add_content_slide(
                prs,
                title=section.get('title', ''),
                bullets=items,
                subtitle=section.get('subtitle', '')
            )
        
        elif section_type == 'image':
            add_image_slide(
                prs,
                title=section.get('title', ''),
                image_path=section.get('image_path', ''),
                caption=section.get('caption', '')
            )
        
        elif section_type == 'image_content':
            add_image_content_slide(
                prs,
                title=section.get('title', ''),
                content=section.get('content', ''),
                image_path=section.get('image_path', '')
            )
        
        elif section_type == 'table':
            add_table_slide(
                prs,
                title=section.get('title', ''),
                headers=section.get('headers', []),
                rows=section.get('rows', []),
                description=section.get('description', '')
            )
        
        elif section_type == 'two_column':
            add_two_column_slide(
                prs,
                title=section.get('title', ''),
                left_content=section.get('left_content', ''),
                right_content=section.get('right_content', '')
            )
        
        elif section_type in ('code', 'code_block'):
            add_code_slide(
                prs,
                title=section.get('title', ''),
                code=section.get('code', ''),
                language=section.get('language', '')
            )
        
        elif section_type == 'section_header':
            # Save previous section group before starting new one
            if current_section_name and current_section_slides:
                all_section_groups[current_section_name] = current_section_slides.copy()
            
            slide = add_progress_section(
                prs,
                title=section.get('title', ''),
                subtitle=section.get('subtitle', '')
            )
            
            # Track for TOC
            section_header_slides.append((section.get('title', ''), slide))
            
            # Start new section group
            current_section_name = section.get('title', '')
            current_section_slides = [slide]
        
        elif section_type == 'status_summary':
            add_status_summary_slide(
                prs,
                title=section.get('title', 'Status'),
                open_count=section.get('open_count', 0),
                closed_count=section.get('closed_count', 0),
                notes=section.get('notes', ''),
                subtitle=section.get('subtitle', '')
            )
        
        elif section_type == 'comparison':
            add_comparison_slide(
                prs,
                title=section.get('title', 'Comparison'),
                left_title=section.get('left_title', 'Left'),
                left_items=section.get('left_items', []),
                right_title=section.get('right_title', 'Right'),
                right_items=section.get('right_items', [])
            )
        
        else:
            logger.warning(f"Unknown section type: {section_type}")
    
    # Generate TOC and sections if requested
    if add_toc and section_header_slides:
        # Finalize last section group
        if current_section_name and current_section_slides:
            all_section_groups[current_section_name] = current_section_slides
        
        # Create TOC entries
        toc_entries = [(title, slide, 0) for title, slide in section_header_slides]
        
        # Add TOC slide(s) - may create multiple slides for large TOCs
        toc_slides = add_toc_slides(prs, "Table of Contents", toc_entries)
        
        # Move TOC slides to position 1 (after title slide)
        insert_slides_at_position(prs, toc_slides, 1)
        
        # Create PowerPoint sections
        for section_name, slides in all_section_groups.items():
            slide_ids = [s.slide_id for s in slides]
            add_section(prs, section_name, slide_ids)
        
        logger.info(f"Added TOC with {len(toc_entries)} entries across {len(toc_slides)} slide(s) and {len(all_section_groups)} sections")
    
    save_presentation(prs, output_path)
    logger.info(f"Technical presentation saved to: {output_path}")


def _validate_progress_data(data: Dict[str, Any]) -> None:
    """Validate progress report data structure."""
    if 'title' not in data:
        raise ValueError("Missing required field: title")
    
    for i, section in enumerate(data.get('sections', [])):
        if 'type' not in section:
            raise ValueError(f"Section {i} missing required field: type")


def _validate_technical_data(data: Dict[str, Any]) -> None:
    """Validate technical presentation data structure."""
    if 'title' not in data:
        raise ValueError("Missing required field: title")
    
    for i, section in enumerate(data.get('sections', [])):
        if 'type' not in section:
            raise ValueError(f"Section {i} missing required field: type")


def main(args=None):
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Generate PowerPoint presentations from YAML data using Cornelis template.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  %(prog)s --type progress --data report.yaml --output report.pptx
  %(prog)s --type technical --data tech.yaml --output presentation.pptx
  %(prog)s --type progress --data report.yaml --dry-run

See examples/ directory for sample YAML files.
        '''
    )
    
    parser.add_argument(
        '--type', '-t',
        choices=['progress', 'technical'],
        required=True,
        help='Type of presentation to generate'
    )
    
    parser.add_argument(
        '--data', '-d',
        type=Path,
        required=True,
        help='Path to YAML data file'
    )
    
    parser.add_argument(
        '--output', '-o',
        type=Path,
        default=Path('output.pptx'),
        help='Output path for generated presentation (default: output.pptx)'
    )
    
    parser.add_argument(
        '--template',
        type=Path,
        default=None,
        help='Path to custom template file (default: Cornelis template)'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Validate data without generating presentation'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )
    
    parser.add_argument(
        '--toc',
        action='store_true',
        help='Generate Table of Contents with hyperlinks and PowerPoint sections'
    )
    
    parsed_args = parser.parse_args(args)
    
    # Configure logging
    log_level = logging.DEBUG if parsed_args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(levelname)s: %(message)s'
    )
    
    # Validate input file exists
    if not parsed_args.data.exists():
        logger.error(f"Data file not found: {parsed_args.data}")
        sys.exit(1)
    
    # Load data
    try:
        data = load_yaml_data(parsed_args.data)
    except Exception as e:
        logger.error(f"Failed to load YAML data: {e}")
        sys.exit(1)
    
    # Generate presentation
    try:
        if parsed_args.type == 'progress':
            generate_progress_report(data, parsed_args.output, parsed_args.dry_run)
        else:
            generate_technical_presentation(data, parsed_args.output, parsed_args.dry_run, getattr(parsed_args, 'toc', False))
    except Exception as e:
        logger.error(f"Failed to generate presentation: {e}")
        if parsed_args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)
    
    if not parsed_args.dry_run:
        print(f"Presentation generated: {parsed_args.output}")


if __name__ == '__main__':
    main()
