#!/usr/bin/env bash
# Test script to demonstrate multi-level verbosity logging
# This script shows how different verbosity levels affect output

set -e

echo "=================================="
echo "Multi-Level Verbosity Test Script"
echo "=================================="
echo ""

# Note: This script requires a sample PDF file to test the convert command
# For now, we'll test the CLI help and basic commands

echo "1. Testing WARNING level (no -v flag):"
echo "--------------------------------------"
echo "$ pdf-to-pptx-tool"
pdf-to-pptx-tool
echo ""

echo "2. Testing INFO level (-v flag):"
echo "--------------------------------------"
echo "$ pdf-to-pptx-tool -v"
pdf-to-pptx-tool -v 2>&1 | grep -E '^\[' || true
echo ""

echo "3. Testing DEBUG level (-vv flag):"
echo "--------------------------------------"
echo "$ pdf-to-pptx-tool -vv"
pdf-to-pptx-tool -vv 2>&1 | grep -E '^\[' || true
echo ""

echo "4. Testing TRACE level (-vvv flag):"
echo "--------------------------------------"
echo "$ pdf-to-pptx-tool -vvv"
pdf-to-pptx-tool -vvv 2>&1 | grep -E '^\[' || true
echo ""

echo "=================================="
echo "Test completed!"
echo ""
echo "Expected behavior:"
echo "  - No flag:  Only WARNING and ERROR messages"
echo "  - -v:       INFO, WARNING, and ERROR messages"
echo "  - -vv:      DEBUG, INFO, WARNING, and ERROR messages"
echo "  - -vvv:     DEBUG + library internals (pdf2image, PIL, pptx)"
echo "=================================="
