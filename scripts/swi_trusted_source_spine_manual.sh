#!/usr/bin/env bash
# Independent second-eye structural inspection.
# Deliberately does NOT import the Python inspector.
set -u

echo "=========================================="
echo "SWI TRUSTED-SOURCE SPINE INSPECTION (MANUAL)"
echo "=========================================="

FAIL=0

check() {
    NAME="$1"
    COMMAND="$2"

    if eval "$COMMAND" >/dev/null 2>&1; then
        printf "PASS   %-28s\n" "$NAME"
    else
        printf "FAIL   %-28s\n" "$NAME"
        FAIL=1
    fi
}

check "SWI HEADER" \
  "grep -Riq 'SWI' docs evidence 2>/dev/null"

for FIELD in \
  source_id \
  source_type \
  publisher \
  reference \
  provenance \
  trusted_for \
  policy_version \
  policy_status \
  policy_scope \
  jurisdiction \
  evidence \
  boundary
do
    check "$FIELD" \
      "grep -Riq \"$FIELD\" docs evidence 2>/dev/null"
done

check "STANDARD != LAW" \
  "grep -Riq 'STANDARD != LAW' docs evidence 2>/dev/null"

check "SOURCE != AUTHORIZATION" \
  "grep -Riq 'SOURCE != AUTHORIZATION' docs evidence 2>/dev/null"

check "API != AUTHORIZATION" \
  "grep -Riq 'API != AUTHORIZATION' docs evidence 2>/dev/null"

check "VPN != AUTHORIZATION" \
  "grep -Riq 'VPN != AUTHORIZATION' docs evidence 2>/dev/null"

check "SIGNATURE != AUTHORITY" \
  "grep -Riq 'SIGNATURE != AUTHORITY' docs evidence 2>/dev/null"

check "CI AUTHORITY BOUNDARY" \
  "grep -Riq 'CI_GREEN != PRODUCTION_AUTHORIZATION\\|No automatic green authority' docs evidence 2>/dev/null"

echo
echo "=========================================="

if [ "$FAIL" -ne 0 ]; then
    echo "SPINE BREAK"
    echo "HALT"
    echo "GREEN: NO"
    echo "BINDING: NO"
    echo "AUTHORIZATION: NO"
    exit 1
fi

echo "STRUCTURAL SPINE CHECK PASSED"
echo "GREEN: STRUCTURAL ONLY"
echo "AUTHORITY: NOT PROVEN"
echo "PRODUCTION AUTHORIZATION: NOT PROVEN"
exit 0
