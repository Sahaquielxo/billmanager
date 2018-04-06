#!/bin/bash

source bashvars.sh

> PTRlist.py

PTRfiles=( $(echo "find /var/named/chroot/var/named/reverse_zones/ -maxdepth 1 -type f" | ssh ${NS1} 2>/dev/null) )
for PTRfile in "${PTRfiles[@]}"
do
	lowercasePTRfile=$(echo "${PTRfile##*/}")
	echo "${lowercasePTRfile,,}" | sed 's/.$//g' >> variables_PTRlist.py
done

for file in $(find reverse_zones/ -maxdepth 1 -type f); do include=$(grep INCLUDE $file | awk '{print $2}' | sed 's/.$//g'); input=$(cat $include | awk 'NF{NF-=4};1'); sed -i.bak 's/.*INCLUDE.*//g' $file; echo "${input,,}\n" >> ${file}; laststr=$(tail -n1 ${file}); laststredit=$(echo "${laststr}" | sed 's/..$//g'); sed -i '$d' "${file}"; echo "${laststredit}" >> ${file}; done
