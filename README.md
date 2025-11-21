# pdf-to-pptx-tool

[![Python Version](https://img.shields.io/badge/python-3.14+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Type checked: mypy](https://img.shields.io/badge/type%20checked-mypy-blue.svg)](https://github.com/python/mypy)
[![AI Generated](https://img.shields.io/badge/AI-Generated-blueviolet.svg)](https://www.anthropic.com/claude)
[![Built with Claude Code](https://img.shields.io/badge/Built_with-Claude_Code-5A67D8.svg)](https://www.anthropic.com/claude/code)

A tool that converts a pdf into a Powerpoint (pptx)

## Table of Contents

- [About](#about)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Multi-Level Verbosity Logging](#multi-level-verbosity-logging)
- [Shell Completion](#shell-completion)
- [Development](#development)
- [Testing](#testing)
- [Security](#security)
- [Contributing](#contributing)
- [License](#license)
- [Author](#author)

## About

`pdf-to-pptx-tool` is a Python CLI tool built with modern tooling and best practices.

## Features

- ✅ Type-safe with mypy strict mode
- ✅ Linted with ruff
- ✅ Tested with pytest
- 📊 Multi-level verbosity logging (-v/-vv/-vvv)
- 🐚 Shell completion for bash, zsh, and fish
- 🔒 Security scanning with bandit, pip-audit, and gitleaks
- ✅ Modern Python tooling (uv, mise, click)

## Installation

### Prerequisites

- Python 3.14 or higher
- [uv](https://github.com/astral-sh/uv) package manager

### Install from source

```bash
# Clone the repository
git clone https://github.com/dnvriend/pdf-to-pptx-tool.git
cd pdf-to-pptx-tool

# Install globally with uv
uv tool install .
```

### Install with mise (recommended for development)

```bash
cd pdf-to-pptx-tool
mise trust
mise install
uv sync
uv tool install .
```

### Verify installation

```bash
pdf-to-pptx-tool --version
```

## Usage

### Basic Usage

```bash
# Show help
pdf-to-pptx-tool --help

# Run the tool
pdf-to-pptx-tool

# Run with verbose output
pdf-to-pptx-tool -v      # INFO level
pdf-to-pptx-tool -vv     # DEBUG level
pdf-to-pptx-tool -vvv    # TRACE level (includes library internals)
```

## Multi-Level Verbosity Logging

The CLI supports progressive verbosity levels for debugging and troubleshooting. All logs output to stderr, keeping stdout clean for data piping.

### Logging Levels

| Flag | Level | Output | Use Case |
|------|-------|--------|----------|
| (none) | WARNING | Errors and warnings only | Production, quiet mode |
| `-v` | INFO | + High-level operations | Normal debugging |
| `-vv` | DEBUG | + Detailed info, full tracebacks | Development, troubleshooting |
| `-vvv` | TRACE | + Library internals | Deep debugging |

### Examples

```bash
# Quiet mode - only errors and warnings
pdf-to-pptx-tool

# INFO - see operations and progress
pdf-to-pptx-tool -v
# Output:
# [INFO] pdf-to-pptx-tool started
# [INFO] pdf-to-pptx-tool completed

# DEBUG - see detailed information
pdf-to-pptx-tool -vv
# Output:
# [INFO] pdf-to-pptx-tool started
# [DEBUG] Running with verbose level: 2
# [INFO] pdf-to-pptx-tool completed

# TRACE - see library internals (configure in logging_config.py)
pdf-to-pptx-tool -vvv
```

### Customizing Library Logging

To enable DEBUG logging for third-party libraries at TRACE level (-vvv), edit `pdf_to_pptx_tool/logging_config.py`:

```python
# Configure dependent library loggers at TRACE level (-vvv)
if verbose_count >= 3:
    logging.getLogger("requests").setLevel(logging.DEBUG)
    logging.getLogger("urllib3").setLevel(logging.DEBUG)
    # Add your project-specific library loggers here
```

## Shell Completion

The CLI provides native shell completion for bash, zsh, and fish shells.

### Supported Shells

| Shell | Version Requirement | Status |
|-------|-------------------|--------|
| **Bash** | ≥ 4.4 | ✅ Supported |
| **Zsh** | Any recent version | ✅ Supported |
| **Fish** | ≥ 3.0 | ✅ Supported |
| **PowerShell** | Any version | ❌ Not Supported |

### Installation

#### Quick Setup (Temporary)

```bash
# Bash - active for current session only
eval "$(pdf-to-pptx-tool completion bash)"

# Zsh - active for current session only
eval "$(pdf-to-pptx-tool completion zsh)"

# Fish - active for current session only
pdf-to-pptx-tool completion fish | source
```

#### Permanent Setup (Recommended)

```bash
# Bash - add to ~/.bashrc
echo 'eval "$(pdf-to-pptx-tool completion bash)"' >> ~/.bashrc
source ~/.bashrc

# Zsh - add to ~/.zshrc
echo 'eval "$(pdf-to-pptx-tool completion zsh)"' >> ~/.zshrc
source ~/.zshrc

# Fish - save to completions directory
mkdir -p ~/.config/fish/completions
pdf-to-pptx-tool completion fish > ~/.config/fish/completions/pdf-to-pptx-tool.fish
```

#### File-based Installation (Better Performance)

For better shell startup performance, generate completion scripts to files:

```bash
# Bash
pdf-to-pptx-tool completion bash > ~/.pdf-to-pptx-tool-complete.bash
echo 'source ~/.pdf-to-pptx-tool-complete.bash' >> ~/.bashrc

# Zsh
pdf-to-pptx-tool completion zsh > ~/.pdf-to-pptx-tool-complete.zsh
echo 'source ~/.pdf-to-pptx-tool-complete.zsh' >> ~/.zshrc

# Fish (automatic loading from completions directory)
mkdir -p ~/.config/fish/completions
pdf-to-pptx-tool completion fish > ~/.config/fish/completions/pdf-to-pptx-tool.fish
```

### Usage

Once installed, completion works automatically:

```bash
# Tab completion for commands
pdf-to-pptx-tool <TAB>
# Shows: completion

# Tab completion for options
pdf-to-pptx-tool --<TAB>
# Shows: --verbose --version --help

# Tab completion for shell types
pdf-to-pptx-tool completion <TAB>
# Shows: bash zsh fish
```

### Getting Help

```bash
# View completion installation instructions
pdf-to-pptx-tool completion --help
```

## Development

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/dnvriend/pdf-to-pptx-tool.git
cd pdf-to-pptx-tool

# Install dependencies
make install

# Show available commands
make help
```

### Available Make Commands

```bash
make install                 # Install dependencies
make format                  # Format code with ruff
make lint                    # Run linting with ruff
make typecheck               # Run type checking with mypy
make test                    # Run tests with pytest
make security-bandit         # Python security linter
make security-pip-audit      # Dependency vulnerability scanner
make security-gitleaks       # Secret/API key detection
make security                # Run all security checks
make check                   # Run all checks (lint, typecheck, test, security)
make pipeline                # Run full pipeline (format, lint, typecheck, test, security, build, install-global)
make build                   # Build package
make run ARGS="..."          # Run pdf-to-pptx-tool locally
make clean                   # Remove build artifacts
```

### Project Structure

```
pdf-to-pptx-tool/
├── pdf_to_pptx_tool/    # Main package
│   ├── __init__.py
│   ├── cli.py          # CLI entry point
│   └── utils.py        # Utility functions
├── tests/              # Test suite
│   ├── __init__.py
│   └── test_utils.py
├── pyproject.toml      # Project configuration
├── Makefile            # Development commands
├── README.md           # This file
├── LICENSE             # MIT License
└── CLAUDE.md           # Development documentation
```

## Testing

Run the test suite:

```bash
# Run all tests
make test

# Run tests with verbose output
uv run pytest tests/ -v

# Run specific test file
uv run pytest tests/test_utils.py

# Run with coverage
uv run pytest tests/ --cov=pdf_to_pptx_tool
```

## Security

The project includes lightweight security tools providing 80%+ coverage with fast scan times:

### Security Tools

| Tool | Purpose | Speed | Coverage |
|------|---------|-------|----------|
| **bandit** | Python code security linting | ⚡⚡ Fast | SQL injection, hardcoded secrets, unsafe functions |
| **pip-audit** | Dependency vulnerability scanning | ⚡⚡ Fast | Known CVEs in dependencies |
| **gitleaks** | Secret and API key detection | ⚡⚡⚡ Very Fast | Secrets in code and git history |

### Running Security Scans

```bash
# Run all security checks (~5-8 seconds)
make security

# Or run individually
make security-bandit       # Python security linting
make security-pip-audit    # Dependency CVE scanning
make security-gitleaks     # Secret detection
```

### Prerequisites

gitleaks must be installed separately:

```bash
# macOS
brew install gitleaks

# Linux
# See: https://github.com/gitleaks/gitleaks#installation
```

Security checks run automatically in `make check` and `make pipeline`.

### What's Protected

- ✅ AWS credentials (AKIA*, ASIA*, etc.)
- ✅ GitHub tokens (ghp_*, gho_*, etc.)
- ✅ API keys and secrets
- ✅ Private keys
- ✅ Slack tokens
- ✅ 100+ other secret types

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run the full pipeline (`make pipeline`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Code Style

- Follow PEP 8 guidelines
- Use type hints for all functions
- Write docstrings for public functions
- Format code with `ruff`
- Pass all linting and type checks

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

**Dennis Vriend**

- GitHub: [@dnvriend](https://github.com/dnvriend)

## Acknowledgments

- Built with [Click](https://click.palletsprojects.com/) for CLI framework
- Developed with [uv](https://github.com/astral-sh/uv) for fast Python tooling

---

**Generated with AI**

This project was generated using [Claude Code](https://www.anthropic.com/claude/code), an AI-powered development tool by [Anthropic](https://www.anthropic.com/). Claude Code assisted in creating the project structure, implementation, tests, documentation, and development tooling.

Made with ❤️ using Python 3.14
