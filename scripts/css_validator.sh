#!/bin/bash
# Search for CSS classes in the templates directories
class=$1
lines=`grep -r $class templates/ */templates/*/ | wc -l`
#printf '=%.0s' {1..80}
#echo -e "\n"
#echo searching directories: 
#echo -e "\n"
#echo templates/ */templates/*/
#echo -e "\n"
#printf '=%.0s' {1..80}
#echo -e "\n"
echo -e "\n"
if [ $lines == 0 ]
then
    echo $class was not found in any lines.
else
    echo $class was found in $lines lines.
fi
echo -e "\n"
