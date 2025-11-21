---
name: skill-pdf-to-pptx-tool
description: A tool that converts a pdf into a Powerpoint (pptx)
---

<!--
⚠️ AGENT INSTRUCTIONS: This is a skeleton SKILL.md template
When details about this CLI tool become clearer, update this file with:

1. **When to use section**: Add 3-5 specific use cases (bullet points)
2. **Purpose section**: Expand the tool's purpose and capabilities
3. **When to Use This Skill**: Add specific scenarios and anti-patterns
4. **Installation**: Keep the standard installation instructions
5. **Quick Start**: Add 2-3 practical quick start examples
6. **Core Commands**: Add detailed documentation for each CLI command in collapsible sections
7. **Advanced Features**: Document advanced features like verbosity, shell completion, pipelines
8. **Troubleshooting**: Add common issues and solutions
9. **Best Practices**: Add 3-5 best practices for using the tool
10. **Resources**: Update with actual GitHub URL and documentation links

CRITICAL REQUIREMENTS:
- Keep description in frontmatter ≤ 50 characters (hard limit)
- Use progressive disclosure with <details> tags
- Include comprehensive examples in each section
- Provide troubleshooting guidance
- Keep always-visible content minimal (overview only)
- Put detailed info in expandable sections
- Use emojis for section summaries (📖 Core, ⚙️ Advanced, 🔧 Troubleshooting)
-->

# When to use
<!-- TODO: Add specific use cases when CLI functionality is known -->
- When you need to use pdf-to-pptx-tool CLI tool
- When you need comprehensive guidance on CLI commands
- When you need examples and troubleshooting

# pdf-to-pptx-tool Skill

## Purpose

<!-- TODO: Expand with specific tool capabilities -->
This skill provides access to the `pdf-to-pptx-tool` CLI tool. A tool that converts a pdf into a Powerpoint (pptx).

## When to Use This Skill

**Use this skill when:**
<!-- TODO: Add specific scenarios, e.g., -->
- You need to understand how to use pdf-to-pptx-tool
- You need comprehensive examples and patterns
- You need troubleshooting guidance

**Do NOT use this skill for:**
<!-- TODO: Add anti-patterns, e.g., -->
- Tasks unrelated to pdf-to-pptx-tool
- Quick syntax lookups (use slash commands instead)

## CLI Tool: pdf-to-pptx-tool

<!-- TODO: Add tool overview -->
The `pdf-to-pptx-tool` is a command-line interface tool that A tool that converts a pdf into a Powerpoint (pptx).

### Installation

```bash
# Clone and install
git clone https://github.com/dnvriend/pdf-to-pptx-tool.git
cd pdf-to-pptx-tool
uv tool install .
```

### Prerequisites

- Python 3.14+
- [uv](https://github.com/astral-sh/uv) package manager

### Quick Start

<!-- TODO: Add 2-3 practical quick start examples when commands are known -->
```bash
# Example 1: Basic usage
pdf-to-pptx-tool --help

# Example 2: Show version
pdf-to-pptx-tool --version
```

## Progressive Disclosure

<details>
<summary><strong>📖 Core Commands (Click to expand)</strong></summary>

<!-- TODO: Add detailed command documentation for each CLI command -->
<!-- Template for each command:

### command-name - Brief Description

Detailed explanation of what this command does.

**Usage:**
```bash
pdf-to-pptx-tool command-name ARGUMENT [OPTIONS]
```

**Arguments:**
- `ARGUMENT`: Description of argument
- `--option VALUE` / `-o VALUE`: Description of option
- `-v/-vv/-vvv`: Verbosity (INFO/DEBUG/TRACE)

**Examples:**
```bash
# Example 1: Basic usage
pdf-to-pptx-tool command-name "example"

# Example 2: With options
pdf-to-pptx-tool command-name "example" --option value

# Example 3: Pipeline usage
pdf-to-pptx-tool command-name "example" --json | jq '.'
```

**Output:**
Description of what this command returns.

---

Repeat for each command...
-->

### help - Show Help Information

Display help information for CLI commands.

**Usage:**
```bash
pdf-to-pptx-tool --help
pdf-to-pptx-tool COMMAND --help
```

**Examples:**
```bash
# General help
pdf-to-pptx-tool --help

# Command help
pdf-to-pptx-tool command --help

# Version info
pdf-to-pptx-tool --version
```

</details>

<details>
<summary><strong>⚙️  Advanced Features (Click to expand)</strong></summary>

<!-- TODO: Add advanced features documentation -->

### Multi-Level Verbosity Logging

Control logging detail with progressive verbosity levels. All logs output to stderr.

**Logging Levels:**

| Flag | Level | Output | Use Case |
|------|-------|--------|----------|
| (none) | WARNING | Errors and warnings only | Production, quiet mode |
| `-v` | INFO | + High-level operations | Normal debugging |
| `-vv` | DEBUG | + Detailed info, full tracebacks | Development, troubleshooting |
| `-vvv` | TRACE | + Library internals | Deep debugging |

**Examples:**
```bash
# INFO level - see operations
pdf-to-pptx-tool command -v

# DEBUG level - see detailed info
pdf-to-pptx-tool command -vv

# TRACE level - see all internals
pdf-to-pptx-tool command -vvv
```

---

### Shell Completion

Native shell completion for bash, zsh, and fish.

**Installation:**
```bash
# Bash (add to ~/.bashrc)
eval "$(pdf-to-pptx-tool completion bash)"

# Zsh (add to ~/.zshrc)
eval "$(pdf-to-pptx-tool completion zsh)"

# Fish (save to completions)
pdf-to-pptx-tool completion fish > ~/.config/fish/completions/pdf-to-pptx-tool.fish
```

---

### Pipeline Composition

<!-- TODO: Add pipeline examples when commands support --json and --stdin -->
Compose commands with Unix pipes for powerful workflows.

**Examples:**
```bash
# Example pipeline workflows will be added when CLI commands are implemented
pdf-to-pptx-tool command --json | jq '.'
```

</details>

<details>
<summary><strong>🔧 Troubleshooting (Click to expand)</strong></summary>

### Common Issues

**Issue: Command not found**
```bash
# Verify installation
pdf-to-pptx-tool --version

# Reinstall if needed
cd pdf-to-pptx-tool
uv tool install . --reinstall
```

<!-- TODO: Add command-specific troubleshooting when functionality is known -->

**Issue: General errors**
- Try with verbose flag: `-vv` to see detailed error information
- Check that all prerequisites are installed
- Ensure you're using Python 3.14+

### Getting Help

```bash
# Show help
pdf-to-pptx-tool --help

# Command-specific help
pdf-to-pptx-tool COMMAND --help
```

</details>

## Exit Codes

- `0`: Success
- `1`: Client error (invalid arguments, validation failed)
- `2`: Server error (API error, network issue)
- `3`: Network error (connection failed, timeout)

## Output Formats

<!-- TODO: Update with actual output formats when commands are implemented -->

**Default Output:**
- Human-readable formatted output
- Varies by command

**JSON Output (`--json` flag):**
- Machine-readable structured data
- Perfect for pipelines and processing
- Available on commands that support structured output

## Best Practices

<!-- TODO: Add command-specific best practices -->
1. **Use verbosity progressively**: Start with `-v`, increase to `-vv`/`-vvv` only if needed
2. **Check help first**: Use `--help` to understand command options
3. **Leverage shell completion**: Install completion for better CLI experience

## Resources

- **GitHub**: https://github.com/dnvriend/pdf-to-pptx-tool
- **Python Package Index**: https://pypi.org/project/pdf-to-pptx-tool/
- **Documentation**: <!-- TODO: Add documentation URL if available -->
