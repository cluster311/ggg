#!/bin/sh

version_file='ggg/settings.py'
line_to_replace="$(grep -Po 'VERSION = ([^;]+)' $version_file)"
echo "LINE TO REPLACE: $line_to_replace"
old_version="$(echo "$line_to_replace" | cut -d"'" -f 2)"
echo "OLD VERSION: $old_version"
new_version="$(echo $old_version | awk -F. -v OFS=. 'NF==1{print ++$NF}; NF>1{if(length($NF+1)>length($NF))$(NF-1)++; $NF=sprintf("%0*d", length($NF), ($NF+1)%(10^length($NF))); print}')"
echo "NEW VERSION: $new_version"
new_line="VERSION = '$new_version'"
echo "NEW LINE: $new_line"

sed -i '/'"${line_to_replace}"'/s/.*/'"${new_line}"'/' $version_file