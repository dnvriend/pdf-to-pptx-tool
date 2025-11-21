# pdf-to-pptx-tool - Project Specification

## Goal

Convert PDF documents into PowerPoint presentations with customizable quality settings, professional output format, and comprehensive debugging capabilities.

## What is pdf-to-pptx-tool?

`pdf-to-pptx-tool` is a professional command-line utility that converts PDF files to PowerPoint (PPTX) format. Each PDF page becomes a full-slide image in a 16:9 widescreen presentation. Built with modern Python tooling and best practices, it features multi-level verbosity logging, shell completion, and type-safe code.

## Technical Requirements

### Runtime

- Python 3.14+
- Installable globally with mise
- Cross-platform (macOS, Linux, Windows)

### Dependencies

- `click` - CLI framework
- `pdf2image` - PDF to image conversion
- `python-pptx` - PowerPoint file creation
- `Pillow` - Image processing
- `poppler` - System library for PDF rendering (external dependency)

### Development Dependencies

- `ruff` - Linting and formatting
- `mypy` - Type checking
- `pytest` - Testing framework
- `bandit` - Security linting
- `pip-audit` - Dependency vulnerability scanning
- `gitleaks` - Secret detection (requires separate installation)

## CLI Commands

### Main Command

```bash
pdf-to-pptx-tool [OPTIONS] COMMAND [ARGS]
```

**Global Options:**
- `-v, --verbose` - Enable verbose output (count flag: -v, -vv, -vvv)
  - `-v` (count=1): INFO level logging
  - `-vv` (count=2): DEBUG level logging
  - `-vvv` (count=3+): TRACE level (includes library internals for pdf2image, PIL, pptx)
- `--version` - Show version
- `--help` - Show help message

### convert - Convert PDF to PowerPoint

```bash
pdf-to-pptx-tool convert INPUT_PDF OUTPUT_PPTX [OPTIONS]
```

**Arguments:**
- `INPUT_PDF` - Path to input PDF file (required)
- `OUTPUT_PPTX` - Path to output PPTX file (required)

**Options:**
- `--dpi INTEGER` - Resolution for PDF page conversion (default: 200)
  - Range: 72-600 DPI
  - Higher DPI = better quality but larger files
  - Recommended: 200-300 for presentations
  - Examples: 72 (draft), 150 (web), 200 (default), 300 (print), 600 (high-res)

**Examples:**
```bash
# Basic conversion (200 DPI)
pdf-to-pptx-tool convert document.pdf slides.pptx

# High quality (300 DPI)
pdf-to-pptx-tool convert report.pdf presentation.pptx --dpi 300

# With verbose logging
pdf-to-pptx-tool -v convert input.pdf output.pptx

# Batch conversion
for pdf in *.pdf; do
  pdf-to-pptx-tool convert "$pdf" "${pdf%.pdf}.pptx"
done
```

**Output Format:**
- Aspect Ratio: 16:9 widescreen
- Slide Size: 10 inches × 5.625 inches
- Layout: One full-slide image per PDF page
- Image Format: PNG embedded in slides
- Compatibility: PowerPoint 2007+ (Windows/Mac/Online)

### completion - Generate Shell Completion

```bash
pdf-to-pptx-tool completion SHELL
```

**Arguments:**
- `SHELL` - Shell type: `bash`, `zsh`, or `fish` (required)

**Examples:**
```bash
# Bash
eval "$(pdf-to-pptx-tool completion bash)"

# Zsh
eval "$(pdf-to-pptx-tool completion zsh)"

# Fish
pdf-to-pptx-tool completion fish | source
```

## Project Structure

```
pdf-to-pptx-tool/
├── pdf_to_pptx_tool/
│   ├── __init__.py
│   ├── cli.py            # Click CLI entry point (group with subcommands)
│   ├── converter.py      # PDF to PPTX conversion logic
│   ├── completion.py     # Shell completion command
│   ├── logging_config.py # Multi-level verbosity logging
│   └── utils.py          # Utility functions
├── tests/
│   ├── __init__.py
│   └── test_utils.py
├── pyproject.toml        # Project configuration
├── README.md             # User documentation
├── CLAUDE.md             # This file
├── Makefile              # Development commands
├── LICENSE               # MIT License
├── .mise.toml            # mise configuration
├── .gitleaks.toml        # Gitleaks configuration
└── .gitignore
```

## Code Style

- Type hints for all functions
- Docstrings for all public functions
- Follow PEP 8 via ruff
- 100 character line length
- Strict mypy checking

## Development Workflow

```bash
# Install dependencies
make install

# Run linting
make lint

# Format code
make format

# Type check
make typecheck

# Run tests
make test

# Security scanning
make security-bandit       # Python security linting
make security-pip-audit    # Dependency CVE scanning
make security-gitleaks     # Secret detection
make security              # Run all security checks

# Run all checks (includes security)
make check

# Full pipeline (includes security)
make pipeline
```

## Security

The template includes three lightweight security tools:

1. **bandit** - Python code security linting
   - Detects: SQL injection, hardcoded secrets, unsafe functions
   - Speed: ~2-3 seconds

2. **pip-audit** - Dependency vulnerability scanning
   - Detects: Known CVEs in dependencies
   - Speed: ~2-3 seconds

3. **gitleaks** - Secret and API key detection
   - Detects: AWS keys, GitHub tokens, API keys, private keys
   - Speed: ~1 second
   - Requires: `brew install gitleaks` (macOS)

All security checks run automatically in `make check` and `make pipeline`.

## Multi-Level Verbosity Logging

The template includes a centralized logging system with progressive verbosity levels.

### Implementation Pattern

1. **logging_config.py** - Centralized logging configuration
   - `setup_logging(verbose_count)` - Configure logging based on -v count
   - `get_logger(name)` - Get logger instance for module
   - Maps verbosity to Python logging levels (WARNING/INFO/DEBUG)

2. **CLI Integration** - Add to every CLI command
   ```python
   from pdf_to_pptx_tool.logging_config import get_logger, setup_logging

   logger = get_logger(__name__)

   @click.command()
   @click.option("-v", "--verbose", count=True, help="...")
   def command(verbose: int):
       setup_logging(verbose)  # First thing in command
       logger.info("Operation started")
       logger.debug("Detailed info")
   ```

3. **Logging Levels**
   - **0 (no -v)**: WARNING only - production/quiet mode
   - **1 (-v)**: INFO - high-level operations
   - **2 (-vv)**: DEBUG - detailed debugging
   - **3+ (-vvv)**: TRACE - enable library internals

4. **Best Practices**
   - Always log to stderr (keeps stdout clean for piping)
   - Use structured messages with placeholders: `logger.info("Found %d items", count)`
   - Call `setup_logging()` first in every command
   - Use `get_logger(__name__)` at module level
   - For TRACE level, enable third-party library loggers in `logging_config.py`

5. **Customizing Library Logging**
   Edit `logging_config.py` to add project-specific libraries:
   ```python
   if verbose_count >= 3:
       logging.getLogger("requests").setLevel(logging.DEBUG)
       logging.getLogger("urllib3").setLevel(logging.DEBUG)
   ```

## Shell Completion

The template includes shell completion for bash, zsh, and fish following the Click Shell Completion Pattern.

### Implementation

1. **completion.py** - Separate module for completion command
   - Uses Click's `BashComplete`, `ZshComplete`, `FishComplete` classes
   - Generates shell-specific completion scripts
   - Includes installation instructions in help text

2. **CLI Integration** - Added as subcommand
   ```python
   from pdf_to_pptx_tool.completion import completion_command

   @click.group(invoke_without_command=True)
   def main(ctx: click.Context):
       # Default behavior when no subcommand
       if ctx.invoked_subcommand is None:
           # Main command logic here
           pass

   # Add completion subcommand
   main.add_command(completion_command)
   ```

3. **Usage Pattern** - User-friendly command
   ```bash
   # Generate completion script
   pdf-to-pptx-tool completion bash
   pdf-to-pptx-tool completion zsh
   pdf-to-pptx-tool completion fish

   # Install (eval or save to file)
   eval "$(pdf-to-pptx-tool completion bash)"
   ```

4. **Supported Shells**
   - **Bash** (≥ 4.4) - Uses bash-completion
   - **Zsh** (any recent) - Uses zsh completion system
   - **Fish** (≥ 3.0) - Uses fish completion system
   - **PowerShell** - Not supported by Click

5. **Installation Methods**
   - **Temporary**: `eval "$(pdf-to-pptx-tool completion bash)"`
   - **Permanent**: Add eval to ~/.bashrc or ~/.zshrc
   - **File-based** (recommended): Save to dedicated completion file

### Adding More Commands

The CLI uses `@click.group()` for extensibility. To add new commands:

1. Create new command module in `pdf_to_pptx_tool/`
2. Import and add to CLI group:
   ```python
   from pdf_to_pptx_tool.new_command import new_command
   main.add_command(new_command)
   ```

3. Completion will automatically work for new commands and their options

## Installation Methods

### Global installation with mise

```bash
cd /path/to/pdf-to-pptx-tool
mise use -g python@3.14
uv sync
uv tool install .
```

After installation, `pdf-to-pptx-tool` command is available globally.

### Local development

```bash
uv sync
uv run pdf-to-pptx-tool [args]
```
