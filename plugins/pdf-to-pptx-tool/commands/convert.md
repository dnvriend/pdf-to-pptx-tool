---
description: Convert PDF to PowerPoint with custom DPI
argument-hint: input.pdf output.pptx
---

Convert a PDF file to PowerPoint (PPTX) format with each page as a slide.

## Usage

```bash
pdf-to-pptx-tool convert INPUT_PDF OUTPUT_PPTX [--dpi DPI]
```

## Arguments

- `INPUT_PDF`: Path to input PDF file (required)
- `OUTPUT_PPTX`: Path to output PPTX file (required)
- `--dpi DPI`: Resolution for conversion (default: 200)
- `-v/-vv/-vvv`: Verbosity (INFO/DEBUG/TRACE)

## Examples

```bash
# Basic conversion
pdf-to-pptx-tool convert document.pdf slides.pptx

# High quality conversion
pdf-to-pptx-tool convert report.pdf presentation.pptx --dpi 300

# With verbose logging
pdf-to-pptx-tool -vv convert input.pdf output.pptx
```

## Output

Creates a PowerPoint (.pptx) with:
- One slide per PDF page
- 16:9 aspect ratio (10" x 5.625")
- Images sized to fill entire slide
