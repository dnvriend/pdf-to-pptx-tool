"""CLI entry point for pdf-to-pptx-tool.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import sys
from pathlib import Path

import click

from pdf_to_pptx_tool.completion import completion_command
from pdf_to_pptx_tool.converter import convert_pdf_to_pptx
from pdf_to_pptx_tool.logging_config import get_logger, setup_logging
from pdf_to_pptx_tool.utils import get_greeting

logger = get_logger(__name__)


@click.group(invoke_without_command=True)
@click.option(
    "-v",
    "--verbose",
    count=True,
    help="Enable verbose output (use -v for INFO, -vv for DEBUG, -vvv for TRACE)",
)
@click.version_option(version="0.1.0")
@click.pass_context
def main(ctx: click.Context, verbose: int) -> None:
    """Convert PDF documents to PowerPoint presentations.

    Transform PDF files into professional PowerPoint presentations with
    customizable quality settings. Each PDF page becomes a full-slide
    image in 16:9 widescreen format.

    \b
    Examples:
        # Convert with default quality (200 DPI)
        pdf-to-pptx-tool convert document.pdf slides.pptx

        # High quality for print (300 DPI)
        pdf-to-pptx-tool convert report.pdf presentation.pptx --dpi 300

        # With verbose logging
        pdf-to-pptx-tool -v convert input.pdf output.pptx

    \b
    Commands:
        convert     Convert PDF to PowerPoint with customizable DPI
        completion  Generate shell completion scripts for bash/zsh/fish
    """
    # Setup logging based on verbosity count
    setup_logging(verbose)

    # If no subcommand is provided, run the default behavior
    if ctx.invoked_subcommand is None:
        logger.info("pdf-to-pptx-tool started")
        logger.debug("Running with verbose level: %d", verbose)

        greeting = get_greeting()
        click.echo(greeting)

        logger.info("pdf-to-pptx-tool completed")


@click.command(name="convert")
@click.argument("input_pdf", type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.argument("output_pptx", type=click.Path(dir_okay=False, path_type=Path))
@click.option(
    "--dpi",
    type=int,
    default=200,
    show_default=True,
    help="Resolution for PDF page conversion",
)
@click.pass_context
def convert_command(ctx: click.Context, input_pdf: Path, output_pptx: Path, dpi: int) -> None:
    """Convert a PDF file to PowerPoint (PPTX) format.

    INPUT_PDF: Path to the input PDF file to convert

    OUTPUT_PPTX: Path where the output PPTX file will be saved

    This command converts each page of the PDF to a high-resolution image
    and embeds it in a PowerPoint slide with 16:9 aspect ratio.

    Examples:

    \b
        # Basic conversion
        pdf-to-pptx-tool convert input.pdf output.pptx

    \b
        # Convert with higher DPI for better quality
        pdf-to-pptx-tool convert input.pdf output.pptx --dpi 300

    \b
        # Convert with verbose output to see progress
        pdf-to-pptx-tool -v convert input.pdf output.pptx

    \b
    Output Format:
        Creates a PowerPoint presentation (.pptx) with:
        - One slide per PDF page
        - 16:9 aspect ratio (10" x 5.625")
        - Images sized to fill the entire slide
    """
    # Get verbosity from parent context
    verbose = ctx.parent.params.get("verbose", 0) if ctx.parent else 0
    setup_logging(verbose)

    logger.info("Starting PDF to PPTX conversion")
    logger.debug("Input: %s, Output: %s, DPI: %d", input_pdf, output_pptx, dpi)

    try:
        convert_pdf_to_pptx(str(input_pdf), str(output_pptx), dpi=dpi)
        click.echo(f"✓ Successfully converted {input_pdf} to {output_pptx}")
        logger.info("Conversion completed successfully")
    except FileNotFoundError as e:
        logger.error("File not found: %s", str(e))
        logger.debug("Full traceback:", exc_info=True)
        click.echo(f"✗ Error: {e}", err=True)
        sys.exit(1)
    except ValueError as e:
        logger.error("Invalid input: %s", str(e))
        logger.debug("Full traceback:", exc_info=True)
        click.echo(f"✗ Error: {e}", err=True)
        sys.exit(1)
    except RuntimeError as e:
        logger.error("Runtime error: %s", str(e))
        logger.debug("Full traceback:", exc_info=True)
        click.echo(f"✗ Error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        logger.error("Unexpected error during conversion: %s", type(e).__name__)
        logger.error("Error message: %s", str(e))
        logger.debug("Full traceback:", exc_info=True)
        click.echo(f"✗ Unexpected error: {e}", err=True)
        sys.exit(1)


# Add subcommands
main.add_command(completion_command)
main.add_command(convert_command)


if __name__ == "__main__":
    main()
