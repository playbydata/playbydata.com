#!/bin/bash

# Check if a variable is passed
if [ -z "$1" ]; then
    echo "Usage: $0 <notebook_name>"
    exit 1
fi

# Notebook name passed as the first argument
NOTEBOOK_NAME=$1

# Construct paths
NOTEBOOK_PATH="articles/$NOTEBOOK_NAME/$NOTEBOOK_NAME.ipynb"
ENGLISH_TRANSLATION_OUTPUT_PATH="articles/$NOTEBOOK_NAME/translations/en.json"

# Use jq to filter and transform the JSON structure
jq '
.cells
| map(
    select(
        .cell_type == "markdown" and (.metadata.tags | not or (. | contains(["exclude"]) | not))
    )
    | {
        id: .id,
        text: .source
    }
)
' "$NOTEBOOK_PATH" > "$ENGLISH_TRANSLATION_OUTPUT_PATH"