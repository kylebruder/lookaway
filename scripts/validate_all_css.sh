#!/bin/bash
# Read all CSS classes in styles.css and check if any templates are in use.
# CSS file cannot be minimized. must run this from the base directory!

cat static/style.css | cut -d '.' -f 2 | cut -d '{' -f 1 | grep -v -e "  " -e '}' -e '^$' | 
while read i; do 
    scripts/css_validator.sh "$i" 
done
