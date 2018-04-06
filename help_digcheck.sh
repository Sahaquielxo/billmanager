#!/bin/bash
RES=1
while [ "${RES}" -ne 0 -a "${RES}" -le 5 ]
do
	if [ $(dig @$2 $1 | grep -c SOA) -eq 1 ]
	then 
		echo "     Zone found at $2"
		RES=0
	else
		echo "     Zone not found $2"
		RES=$(($RES + 1))
	fi
sleep 1
done
