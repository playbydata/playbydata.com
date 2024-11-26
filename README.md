# playbydata.com
Play by Data Landing Page and Blogging


jupyter nbconvert my_notebook.ipynb --to html \
    --TagRemovePreprocessor.enabled=True \
    --TagRemovePreprocessor.remove_cell_tags="['exclude']" \
    --TagRemovePreprocessor.remove_all_outputs_tags="['exclude']" \
    --no-input  # Optional: Exclude all inputs

jupyter nbconvert articles/2024-11-29-findingnflwinners/2024-11-29-findingnflwinners.ipynb --to html --template exclude_text_outputs  --TemplateExporter.exclude_input=True  --TagRemovePreprocessor.enabled=True  --TagRemovePreprocessor.remove_cell_tags="['exclude']" --TagRemovePreprocessor.remove_all_outputs_tags="['exclude']" --no-prompt

sed -i '' '/{% raw %}/,/{% endraw %}/{
/{% raw %}/!{
/{% endraw %}/!d
}
}' ../jekyll/_posts/en/2024-11-29-findingnflwinners.html



sed -i '' '/{% raw %}/r articles/2024-11-29-findingnflwinners/2024-11-29-findingnflwinners.html' ../jekyll/_posts/en/2024-11-29-findingnflwinners.html