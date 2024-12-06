#!/bin/bash

# Check if both variables are passed
if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Usage: $0 <notebook_name> <language>"
    exit 1
fi

# Assign variables
NOTEBOOK_NAME=$1
LANGUAGE=$2

# Construct paths
NOTEBOOK_PATH="articles/$NOTEBOOK_NAME/$NOTEBOOK_NAME.ipynb"
TRANSLATION_OUTPUT_PATH="articles/$NOTEBOOK_NAME/translations/${LANGUAGE}.json"
NOTEBOOK_OUTPUT_PATH="articles/$NOTEBOOK_NAME/translations/${NOTEBOOK_NAME}_${LANGUAGE}.ipynb"

# Check if jq is installed
if ! command -v jq &> /dev/null; then
    echo "Error: jq is not installed. Install jq and try again."
    exit 1
fi

# Check if the input files exist
if [ ! -f "$TRANSLATION_OUTPUT_PATH" ]; then
    echo "Error: Translation file '$TRANSLATION_OUTPUT_PATH' does not exist."
    exit 1
fi

if [ ! -f "$NOTEBOOK_PATH" ]; then
    echo "Error: Notebook file '$NOTEBOOK_PATH' does not exist."
    exit 1
fi

# Read translated JSON into a jq-compatible structure
TRANSLATED_MAP=$(jq -n --slurpfile translated "$TRANSLATION_OUTPUT_PATH" '
  reduce ($translated[0][] | {id, text}) as $item ({}; .[$item.id] = $item.text)
')

# Update notebook file by matching ids
jq --argjson translations "$TRANSLATED_MAP" '
  .cells |= map(
    if .id and (.id | in($translations)) then
      .source = $translations[.id]
    else
      .
    end
  )
' "$NOTEBOOK_PATH" > "$NOTEBOOK_OUTPUT_PATH"

echo "Updated notebook saved to $NOTEBOOK_OUTPUT_PATH"
sed -i '' "s/lang: en/lang: ${LANGUAGE}/g" "$NOTEBOOK_OUTPUT_PATH"

bash scripts/export_notebook_to_jekyll_post.sh ${NOTEBOOK_NAME} ${LANGUAGE}

rm "$NOTEBOOK_OUTPUT_PATH"
