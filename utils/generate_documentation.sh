#!/bin/bash
# Automatic documentation generation. Run it before final commit to generate latest documentation

SCRIPT_DIR=$(dirname "$0")
ROOT_DIR=$(dirname "${SCRIPT_DIR}")
rm "${ROOT_DIR}"/docs/index.md
pdoc3 --html -o /tmp/html --force "${ROOT_DIR}"/app
FILES=$(find /tmp/html -name '*.html')
for file in ${FILES}; do
  html2text "${file}" >> "${ROOT_DIR}"/docs/index.md
done
