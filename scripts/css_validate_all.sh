#!/bin/bash
# Read all CSS classes in styles.css and check if any templates are in use.
# CSS file cannot be minimized. must run this from the base directory!

awk -v s="." 'index($0, s) == 1' static/style.css | cut -d '{' -f 1 | sed 's/[#$%*@.<>,]//g' | sed 's/ /\n/g'| 
while read i; do 
    echo $i
    scripts/css_validator.sh "$i" 
done
