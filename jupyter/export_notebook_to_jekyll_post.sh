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
HTML_OUTPUT_PATH="../jekyll/_posts/en/$NOTEBOOK_NAME.html"
GENERATED_HTML="articles/$NOTEBOOK_NAME/$NOTEBOOK_NAME.html"
NOTEBOOK_ASSET_PATH="articles/$NOTEBOOK_NAME/article_assets/"
JEKYLL_ASSET_PATH="../jekyll/assets/posts/$NOTEBOOK_NAME/"

# Check if the notebook exists
if [ ! -f "$NOTEBOOK_PATH" ]; then
    echo "Error: Notebook '$NOTEBOOK_PATH' does not exist."
    exit 1
fi

# Run the jupyter nbconvert command
jupyter nbconvert "$NOTEBOOK_PATH" --to html \
    --template exclude_text_outputs \
    --TemplateExporter.exclude_input=True \
    --TagRemovePreprocessor.enabled=True \
    --TagRemovePreprocessor.remove_cell_tags="['exclude']" \
    --TagRemovePreprocessor.remove_all_outputs_tags="['exclude']" \
    --no-prompt

# Check if the generated HTML file exists
if [ ! -f "$GENERATED_HTML" ]; then
    echo "Error: Generated HTML file '$GENERATED_HTML' not found."
    exit 1
fi

# Check if the final HTML output exists
if [ ! -f "$HTML_OUTPUT_PATH" ]; then
    echo "Error: Expected HTML output '$HTML_OUTPUT_PATH' not found."
    exit 1
fi

# Transform
sed -i '' "s|'https://cdn.plot.ly/plotly-2.35.2.min'|'/js/plotly'|g" $GENERATED_HTML
sed -i '' 's/\(<h[1-6][^>]*>\)\(.*\)<a class="anchor-link" href="\([^"]*\)">¶<\/a>/\1<a class="anchor-link" href="\3">\2<\/a>/g' $GENERATED_HTML

# Copy Assets
mkdir -p "$NOTEBOOK_ASSET_PATH"
mkdir -p "$JEKYLL_ASSET_PATH"
cp -r "$NOTEBOOK_ASSET_PATH" "$JEKYLL_ASSET_PATH"
sed -i ''  "s|article_assets/|/assets/posts/${NOTEBOOK_NAME}/|g" $GENERATED_HTML

# Clean up content between {% raw %} and {% endraw %}
sed -i '' '/{% raw %}/,/{% endraw %}/{
/{% raw %}/!{
/{% endraw %}/!d
}
}' "$HTML_OUTPUT_PATH"

# Insert the generated HTML file contents after {% raw %}
sed -i '' "/{% raw %}/r $GENERATED_HTML" "$HTML_OUTPUT_PATH"

# Remove Temporal
rm -rf $GENERATED_HTML

# Notify the user
echo "Conversion, cleanup, and insertion completed for notebook: $NOTEBOOK_NAME"