# pdf-to-pptx-tool Architecture

## Overview

`pdf-to-pptx-tool` is a Python CLI tool that converts PDF documents to PowerPoint presentations. It follows modern Python development practices with strict type checking, comprehensive testing, and security scanning.

## Architecture Principles

### Separation of Concerns

The project follows a clean separation between:

1. **Core Logic** (`converter.py`) - Pure conversion logic, CLI-independent
2. **CLI Layer** (`cli.py`) - User interface and command handling
3. **Infrastructure** (`logging_config.py`) - Cross-cutting concerns

This separation enables:
- Reusability of core logic in other contexts
- Easier testing and maintenance
- Clear boundaries between concerns

### Type Safety First

- Python 3.14 with strict mypy checking (`strict = true`)
- All functions have complete type hints
- Uses modern typing features (`Path` from pathlib, type unions)
- Validates types at both runtime and static analysis time

### Agent-Friendly CLI Design

Following the "Agent-Friendly CLI Help" pattern:

- Self-documenting `--help` with inline examples
- Progressive complexity in examples (simple → advanced)
- Predictable output format (success to stdout, logs to stderr)
- Consistent exit codes (0=success, 1=error)
- Actionable error messages

## Project Structure

```
pdf-to-pptx-tool/
├── pdf_to_pptx_tool/          # Main package
│   ├── __init__.py            # Package metadata (__version__)
│   ├── cli.py                 # CLI entry point with Click commands
│   ├── converter.py           # Core PDF→PPTX conversion logic
│   ├── logging_config.py      # Multi-level verbosity logging
│   ├── completion.py          # Shell completion (bash/zsh/fish)
│   └── utils.py               # Utility functions
├── tests/                     # Test suite
│   ├── __init__.py
│   └── test_utils.py
├── pyproject.toml             # Project configuration (PEP 621)
├── Makefile                   # Development workflow
├── README.md                  # User documentation
├── CLAUDE.md                  # Development specification
└── references/                # Architecture documentation
    └── architecture.md        # This file
```

## Core Components

### 1. Converter Module (`converter.py`)

**Purpose**: Pure conversion logic without CLI dependencies.

**Key Function**: `convert_pdf_to_pptx(input_pdf, output_pptx, dpi=200)`

**Process Flow**:
```
1. Validate input file exists
   ↓
2. Convert PDF pages → PIL Images (using pdf2image)
   ↓
3. Create PowerPoint presentation (16:9 aspect ratio)
   ↓
4. For each image:
   - Save to temporary PNG
   - Add blank slide
   - Embed image (full-slide size)
   - Clean up temporary file
   ↓
5. Save PPTX file
```

**Error Handling**:
- `FileNotFoundError`: Input PDF doesn't exist
- `ValueError`: Input path is not a file
- `RuntimeError`: PDF conversion fails (e.g., corrupted PDF)
- All errors bubble up to CLI layer for user-friendly messages

**Design Decisions**:
- Uses temporary PNG files (simpler than in-memory buffers)
- 16:9 aspect ratio (modern presentation standard)
- Default 200 DPI (balance between quality and file size)
- Images sized to fill entire slide (no borders/padding)

### 2. CLI Module (`cli.py`)

**Purpose**: User interface layer using Click framework.

**Command Structure**:
```
pdf-to-pptx-tool [global options] <command> [command options]

Global Options:
  -v, --verbose    Multi-level verbosity (repeatable)
  --version        Show version
  --help           Show help

Commands:
  completion       Generate shell completion scripts
  convert          Convert PDF to PPTX
```

**Convert Command Design**:
```python
pdf-to-pptx-tool convert INPUT_PDF OUTPUT_PPTX [--dpi INT]
```

- **INPUT_PDF**: Positional argument (validated by Click: must exist, must be file)
- **OUTPUT_PPTX**: Positional argument (path where output will be written)
- **--dpi**: Optional flag with default value (200)

**Error Handling Strategy**:
```python
try:
    convert_pdf_to_pptx(...)
    click.echo("✓ Success message")  # stdout
except SpecificError as e:
    click.echo(f"✗ Error: {e}", err=True)  # stderr
    sys.exit(1)  # Non-zero exit code
```

### 3. Logging Configuration (`logging_config.py`)

**Purpose**: Centralized logging with multi-level verbosity.

**Verbosity Levels**:

| Flag | Level | Output | Use Case |
|------|-------|--------|----------|
| (none) | WARNING | Errors/warnings only | Production, quiet mode |
| `-v` | INFO | + Operations | Normal debugging |
| `-vv` | DEBUG | + Detailed info | Development |
| `-vvv` | TRACE | + Library internals | Deep debugging |

**Design**:
- All logs go to stderr (keeps stdout clean for data piping)
- Simple format: `[LEVEL] message`
- Configurable library logging at TRACE level
- `force=True` ensures configuration overrides

**Usage Pattern**:
```python
from pdf_to_pptx_tool.logging_config import get_logger

logger = get_logger(__name__)
logger.info("Operation started")
logger.debug("Detailed info: %s", details)
```

### 4. Completion Module (`completion.py`)

**Purpose**: Generate shell completion scripts for bash/zsh/fish.

**Supported Shells**:
- Bash ≥ 4.4
- Zsh (any recent version)
- Fish ≥ 3.0

**Implementation**:
- Uses Click's built-in `shell_completion` module
- Generates completion scripts programmatically
- Includes installation instructions in help text

## Library Dependencies

### Production Dependencies

#### 1. **click** (≥8.1.7)
- **Purpose**: CLI framework
- **Why chosen**:
  - Industry standard for Python CLIs
  - Excellent decorator-based API
  - Built-in shell completion support
  - Type-safe with modern Python
- **Features used**:
  - Command groups (`@click.group`)
  - Arguments with validation (`click.Path`)
  - Options with defaults
  - Context passing

#### 2. **pdf2image** (≥1.17.0)
- **Purpose**: Convert PDF pages to PIL images
- **Why chosen**:
  - Most reliable PDF → image conversion
  - Handles complex PDFs correctly
  - Good DPI control
- **Dependencies**: Requires `poppler` system library
  - macOS: `brew install poppler`
  - Linux: `apt-get install poppler-utils`
- **Alternative considered**: PyMuPDF (fitz) - more complex API

#### 3. **python-pptx** (≥1.0.2)
- **Purpose**: Create and manipulate PowerPoint files
- **Why chosen**:
  - Pure Python (no Office required)
  - Mature, stable API
  - Excellent documentation
  - Supports modern PPTX features
- **Features used**:
  - Presentation creation
  - Slide layouts
  - Image embedding
  - Dimension control (16:9 aspect ratio)

#### 4. **pillow** (≥11.0.0)
- **Purpose**: Image processing (used by pdf2image)
- **Why chosen**:
  - Standard Python imaging library
  - Required dependency for pdf2image
  - Handles PNG saving for temporary files
- **Features used**:
  - Image format conversion
  - Image saving (PNG)

### Development Dependencies

#### 5. **ruff** (≥0.8.0)
- **Purpose**: Linting and formatting
- **Why chosen**:
  - Fast (10-100x faster than flake8/black)
  - All-in-one (linter + formatter)
  - Modern Python support
- **Configuration**:
  - Line length: 100 characters
  - Target: Python 3.14
  - Selected rules: E, F, I, N, W, UP

#### 6. **mypy** (≥1.7.0)
- **Purpose**: Static type checking
- **Configuration**: Strict mode enabled
  - `disallow_untyped_defs = true`
  - `disallow_any_generics = true`
  - `warn_return_any = true`
  - `strict = true`

#### 7. **pytest** (≥7.4.0)
- **Purpose**: Testing framework
- **Why chosen**:
  - Industry standard
  - Excellent fixture system
  - Rich plugin ecosystem

#### 8. **bandit** (≥1.7.0)
- **Purpose**: Security linting
- **Checks**: SQL injection, hardcoded secrets, unsafe functions
- **Configuration**: Skip B101 (assert_used in tests)

#### 9. **pip-audit** (≥2.6.0)
- **Purpose**: Dependency vulnerability scanning
- **Checks**: Known CVEs in dependencies

## Design Patterns

### 1. CLI-Independent Core

**Pattern**: Core logic has no Click dependencies.

**Benefits**:
- Can import `converter.py` in other projects
- Easier unit testing (no CLI mocking)
- Clear separation of concerns

**Example**:
```python
# Can use in any context
from pdf_to_pptx_tool.converter import convert_pdf_to_pptx

convert_pdf_to_pptx("input.pdf", "output.pptx", dpi=300)
```

### 2. Agent-Friendly CLI Help

**Pattern**: Self-documenting help with inline examples.

**Implementation**:
```python
def command():
    """Brief description.

    Long description.

    Examples:

    \b
        # Comment explaining use case
        command --option value

    \b
    Output Format:
        Description of what command returns
    """
```

**Benefits**:
- AI agents can self-correct by reading help
- Users get immediate usage guidance
- Examples show common patterns

### 3. Multi-Level Verbosity

**Pattern**: Progressive logging levels via repeated flags.

**Mapping**:
```python
verbose_count = 0  # WARNING (quiet)
verbose_count = 1  # INFO (-v)
verbose_count = 2  # DEBUG (-vv)
verbose_count = 3  # TRACE (-vvv)
```

**Benefits**:
- Users control detail level
- Development vs. production distinction
- Standard Unix pattern

### 4. Makefile-Driven Development

**Pattern**: Common tasks encapsulated in Makefile.

**Key Targets**:
```makefile
make install          # Set up environment
make format           # Auto-format code
make lint             # Check code quality
make typecheck        # Run mypy
make test             # Run tests
make security         # Run all security checks
make pipeline         # Full CI/CD pipeline
make run ARGS="..."   # Run locally
```

**Benefits**:
- Consistent workflow across projects
- Easy onboarding
- CI/CD compatibility

## Conversion Process Deep Dive

### Step-by-Step Flow

**1. Input Validation**:
```python
input_path = Path(input_pdf)
if not input_path.exists():
    raise FileNotFoundError(...)
if not input_path.is_file():
    raise ValueError(...)
```

**2. PDF → Images Conversion**:
```python
images = convert_from_path(str(input_path), dpi=dpi)
```
- Uses `pdftoppm` from poppler under the hood
- Returns list of PIL Image objects
- DPI controls resolution (higher = better quality, larger file)

**3. PowerPoint Creation**:
```python
prs = Presentation()
prs.slide_width = Inches(10)      # 16:9 aspect ratio
prs.slide_height = Inches(5.625)   # (10 / 16) * 9
```

**4. Image Embedding Loop**:
```python
for i, image in enumerate(images, 1):
    # Save temporary PNG
    temp_path = f"temp_page_{i}.png"
    image.save(temp_path, "PNG")

    # Add blank slide
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # Embed image (full-slide)
    slide.shapes.add_picture(
        temp_path,
        left=Inches(0),
        top=Inches(0),
        width=prs.slide_width,
        height=prs.slide_height
    )

    # Cleanup
    Path(temp_path).unlink(missing_ok=True)
```

**5. Save PPTX**:
```python
prs.save(output_pptx)
```

### Why Temporary Files?

**Alternative considered**: In-memory buffer with `BytesIO`.

**Decision**: Use temporary PNG files.

**Rationale**:
- `python-pptx` requires file paths (not file-like objects)
- Simpler error handling
- Minimal performance impact (already I/O bound on PDF conversion)
- Files cleaned up immediately after use (`missing_ok=True` for safety)

### Aspect Ratio Choice

**Selected**: 16:9 (10" × 5.625")

**Rationale**:
- Modern presentation standard
- Matches most projectors/screens
- Google Slides/modern PowerPoint default
- Better for full-bleed images

**Alternative**: 4:3 (traditional) - less common now.

## Security Considerations

### 1. Input Validation

**File Existence**: Validated before processing.
```python
click.Path(exists=True, dir_okay=False)
```

**Path Traversal**: Click validates paths, no manual string manipulation.

### 2. Temporary File Handling

**Creation**: Uses predictable names (`temp_page_{i}.png`) in current directory.

**Cleanup**: Always cleaned up with `unlink(missing_ok=True)`.

**Risk**: Low (files exist briefly, cleaned up on error too via `finally`).

### 3. Dependency Security

**Scanning**: `pip-audit` checks for known CVEs.

**Frequency**: Run on every `make pipeline` and CI/CD.

**Current Status**: No known vulnerabilities.

### 4. Secret Detection

**Tool**: `gitleaks` scans code and git history.

**Coverage**: AWS keys, GitHub tokens, API keys, private keys.

**Configuration**: `.gitleaks.toml` with custom rules.

## Performance Characteristics

### Bottlenecks

1. **PDF → Image conversion** (dominant cost)
   - CPU-bound (poppler rendering)
   - Scales with: page count, DPI, PDF complexity

2. **Image → PPTX embedding** (secondary cost)
   - I/O-bound (writing PNG, reading into PPTX)
   - Scales with: page count, DPI

3. **Temporary file I/O** (minimal cost)
   - Fast on modern SSDs
   - Could use tmpfs/RAM disk for marginal gains

### Scalability

**Typical Performance** (18-page PDF at 200 DPI):
- Conversion: ~30-60 seconds
- Output size: ~70-75 MB
- Memory usage: ~500 MB peak

**DPI Impact**:
- 200 DPI: Good quality, reasonable file size (default)
- 300 DPI: High quality, 2-3x larger files, 2x slower
- 150 DPI: Lower quality, smaller files, faster

**Parallelization**: Not implemented (complexity vs. benefit trade-off).

## Testing Strategy

### Current Coverage

1. **Unit Tests** (`tests/test_utils.py`)
   - Tests utility functions
   - Fast, isolated

2. **Integration Tests** (manual)
   - Test full conversion flow
   - Verify output quality

### Future Enhancements

1. **Converter Tests**:
   - Mock pdf2image for fast tests
   - Test error handling paths
   - Validate PPTX structure

2. **CLI Tests**:
   - Test command parsing
   - Test exit codes
   - Test error messages

3. **Fixtures**:
   - Sample PDFs (1-page, multi-page, complex)
   - Expected outputs for comparison

## Development Workflow

### 1. Local Development

```bash
# Clone and setup
git clone https://github.com/dnvriend/pdf-to-pptx-tool.git
cd pdf-to-pptx-tool
make install

# Develop
# ... make changes ...

# Test locally
make run ARGS="convert test.pdf output.pptx"

# Run checks
make check  # lint, typecheck, test, security

# Format and full pipeline
make pipeline  # format, lint, typecheck, test, security, build, install
```

### 2. Pre-Commit Workflow

Recommended checks before commit:
```bash
make check  # or make pipeline for full flow
```

### 3. CI/CD Integration

GitHub Actions (recommended):
```yaml
- name: Run Pipeline
  run: make pipeline
```

All checks must pass before merge.

## Extension Points

### 1. Custom Slide Layouts

**Current**: Uses blank slide layout (index 6).

**Extension**: Support different layouts:
```python
def convert_pdf_to_pptx(
    input_pdf: str,
    output_pptx: str,
    dpi: int = 200,
    slide_layout_idx: int = 6  # Add parameter
) -> None:
    # ...
    slide = prs.slides.add_slide(prs.slide_layouts[slide_layout_idx])
```

### 2. Custom Aspect Ratios

**Current**: Hardcoded 16:9.

**Extension**: Add aspect ratio option:
```python
def convert_pdf_to_pptx(
    input_pdf: str,
    output_pptx: str,
    dpi: int = 200,
    aspect_ratio: str = "16:9"  # Add parameter
) -> None:
    if aspect_ratio == "16:9":
        prs.slide_width = Inches(10)
        prs.slide_height = Inches(5.625)
    elif aspect_ratio == "4:3":
        prs.slide_width = Inches(10)
        prs.slide_height = Inches(7.5)
```

### 3. Batch Conversion

**Current**: Single file conversion.

**Extension**: Add batch command:
```python
@click.command(name="convert-batch")
@click.argument("input_dir", type=click.Path(exists=True, file_okay=False))
@click.argument("output_dir", type=click.Path(file_okay=False))
def convert_batch_command(input_dir: Path, output_dir: Path) -> None:
    """Convert all PDFs in directory."""
    # ...
```

### 4. Progress Bars

**Current**: Log messages only.

**Extension**: Add progress bars with `tqdm`:
```python
from tqdm import tqdm

for i, image in enumerate(tqdm(images, desc="Adding slides"), 1):
    # ...
```

### 5. Template Support

**Current**: Creates new presentation from scratch.

**Extension**: Use template PPTX:
```python
def convert_pdf_to_pptx(
    input_pdf: str,
    output_pptx: str,
    dpi: int = 200,
    template_pptx: str | None = None  # Add parameter
) -> None:
    if template_pptx:
        prs = Presentation(template_pptx)
    else:
        prs = Presentation()
    # ...
```

## Known Limitations

### 1. Requires poppler

**Issue**: `pdf2image` depends on poppler system library.

**Impact**: Users must install separately (not pure Python).

**Mitigation**: Clear error messages, installation instructions in README.

### 2. Large File Sizes

**Issue**: High DPI creates large PPTX files (70+ MB for 18 pages).

**Cause**: Full-resolution PNG images embedded per slide.

**Mitigation**:
- Default 200 DPI balances quality and size
- Users can adjust with `--dpi` flag
- Consider image compression in future

### 3. No Text Extraction

**Issue**: PDF text becomes rasterized (images only).

**Impact**: Text not searchable or editable in PPTX.

**Rationale**: Text extraction is complex (layout, fonts, formatting).

**Future**: Could add OCR or text layer extraction.

### 4. Memory Usage

**Issue**: All images loaded into memory during conversion.

**Impact**: Large PDFs (100+ pages) may use significant RAM.

**Mitigation**: Process scales linearly, cleanup after each slide.

**Future**: Streaming approach (one page at a time).

## Troubleshooting Guide

### Issue: "poppler not found"

**Symptom**: `pdf2image` fails with poppler error.

**Solution**:
```bash
# macOS
brew install poppler

# Ubuntu/Debian
sudo apt-get install poppler-utils

# Verify
which pdftoppm
```

### Issue: "Out of memory"

**Symptom**: Conversion fails on large PDFs.

**Solution**: Lower DPI or split PDF:
```bash
pdf-to-pptx-tool convert large.pdf output.pptx --dpi 150
```

### Issue: Slow conversion

**Symptom**: Takes very long to convert.

**Causes**: High DPI, complex PDF, many pages.

**Solutions**:
- Use lower DPI (`--dpi 150`)
- Check PDF complexity (vector vs. raster)
- Split large PDFs into smaller chunks

### Issue: Poor image quality

**Symptom**: Blurry or pixelated slides.

**Solution**: Increase DPI:
```bash
pdf-to-pptx-tool convert input.pdf output.pptx --dpi 300
```

**Trade-off**: Larger file, slower conversion.

## References

### Documentation

- [Click Documentation](https://click.palletsprojects.com/)
- [python-pptx Documentation](https://python-pptx.readthedocs.io/)
- [pdf2image Documentation](https://github.com/Belval/pdf2image)
- [Pillow Documentation](https://pillow.readthedocs.io/)

### Standards

- [PEP 621 - Project Metadata](https://peps.python.org/pep-0621/)
- [PEP 8 - Style Guide](https://peps.python.org/pep-0008/)
- [PEP 484 - Type Hints](https://peps.python.org/pep-0484/)

### Tools

- [ruff](https://github.com/astral-sh/ruff)
- [mypy](https://github.com/python/mypy)
- [bandit](https://github.com/PyCQA/bandit)
- [pip-audit](https://github.com/pypa/pip-audit)
- [gitleaks](https://github.com/gitleaks/gitleaks)

---

**Document Version**: 1.0
**Last Updated**: 2025-11-21
**Author**: Dennis Vriend

**Note**: This documentation was created with assistance from AI coding tools and reviewed by humans.
