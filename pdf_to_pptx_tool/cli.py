"""CLI entry point for pdf-to-pptx-tool.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import click

from pdf_to_pptx_tool.completion import completion_command
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
    """A tool that converts a pdf into a Powerpoint (pptx)"""
    # Setup logging based on verbosity count
    setup_logging(verbose)

    # If no subcommand is provided, run the default behavior
    if ctx.invoked_subcommand is None:
        logger.info("pdf-to-pptx-tool started")
        logger.debug("Running with verbose level: %d", verbose)

        greeting = get_greeting()
        click.echo(greeting)

        logger.info("pdf-to-pptx-tool completed")


# Add completion subcommand
main.add_command(completion_command)


if __name__ == "__main__":
    main()
