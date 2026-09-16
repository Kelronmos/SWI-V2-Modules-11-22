#!/usr/bin/env bash
set -euo pipefail

echo "=================================="
echo "SWI LOCAL NODE INFORMATION"
echo "=================================="

echo
echo "Computer:"
hostname

echo
echo "OS:"
sw_vers 2>/dev/null || uname -a

echo
echo "Architecture:"
uname -m

echo
echo "Processor:"
sysctl -n machdep.cpu.brand_string 2>/dev/null || true

echo
echo "Python:"
command -v python3 || true
python3 --version 2>/dev/null || true

echo
echo "Git:"
command -v git || true
git --version 2>/dev/null || true

echo
echo "Timestamp:"
date -Iseconds 2>/dev/null || date

echo
echo "=================================="
echo "LOCAL ONLY - NOT AN AUTHORIZATION"
echo "=================================="
