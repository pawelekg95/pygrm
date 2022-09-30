#!/bin/bash
# Automatic documentation generator. Run it before final commit to generate latest documentation and pass CI pipeline

SCRIPT_DIR=$(dirname "$0")
ROOT_DIR=$(dirname "${SCRIPT_DIR}")
rm "${ROOT_DIR}"/docs/index.md
pdoc3 --html -o /tmp/html --force -c show_source_code=False "${ROOT_DIR}"/app
FILES=$(find /tmp/html -name '*.html')
for file in ${FILES}; do
  html2text "${file}" >> "${ROOT_DIR}"/docs/index.md
done

DATE=$(date '+%d/%m/%Y %H:%M:%S %Z')
echo -e "${DATE}" >> "${ROOT_DIR}"/docs/index.md
