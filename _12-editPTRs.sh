#!/bin/bash

for file in $(find /root/scripts/output/reverse_zones/ -maxdepth 1 -type f)
do 
	include=$(grep INCLUDE $file | awk '{print $2}' | sed 's/.$//g')
# Remove last 4 columns from file: "; rr = N"
	input=$(cat /root/scripts/output/${include} | awk 'NF{NF-=4};1')
# Replace "$INCLUDE..." string with ""
	sed -i.bak 's/.*INCLUDE.*//g' $file
	echo "${input,,}\n" >> ${file}
# Delete chars "\n" from the end of the last line ($laststredit var)
	laststr=$(tail -n1 ${file})
	laststredit=$(echo "${laststr}" | sed 's/..$//g')
	sed -i '$d' "${file}"
	echo "${laststredit}" >> ${file}
done
