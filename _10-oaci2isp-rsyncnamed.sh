#!/bin/bash
clear
# Delete generated before list.
rm -rf /root/scripts/output/_11-oaciIDandDomains*

# Directory for zone files from the "old DNS".
if [ ! -d /root/scripts/output/named ]
then
	mkdir /root/scripts/output/named
fi
if [ ! -d /root/scripts/output/reverse_zones ]
then
	mkdir /root/scripts/output/reverse_zones
fi
if [ ! -f /root/scripts/billmanager/variables_bashvars.sh ]
then
	echo "Warning: /root/scripts/billmanager/variables_bashvars.sh missed. FIND IT."
	exit 7
else
	source variables_bashvars.sh
fi

synczone() {
echo "Rsync from current master DNS to the jumper:/root/scripts/output/named/ is running.."
rsync -avz --include='*.' --exclude='*' -f '- /*/' ${NS1}:/var/named/chroot/var/named/ /root/scripts/output/named/

# for name in $(find /root/scripts/output/named/ -type f)
# do
#        newname=$(echo "${name}" | sed 's/.$//g')
#        mv "${name}" "${newname}"
# done

echo "Rsync from /root/scripts/output/named/ to DNSmanager:/root/rsyncdst is running.."
echo "rm -rf /root/rsyncdst/*" | ssh ${DNSmgr} &>/dev/null
rsync -avz -q /root/scripts/output/named/ ${DNSmgr}:/root/rsyncdst/ &>/dev/null
echo "for file in /root/rsyncdst/*; do newname=\$(echo \$file | rev | cut -c 2- | rev); mv \$file \${newname}; done" | ssh ${DNSmgr} &>/dev/null

echo ""
echo "Rsync from current master DNS to the jumper:/root/scripts/output/reverse_zones/ is running.."
echo "rm -rf /root/rsyncdst_rev/*" | ssh ${DNSmgr} &>/dev/null
rsync -avz -r -q ${NS1}:/var/named/chroot/var/named/reverse_zones/* /root/scripts/output/reverse_zones/
/root/scripts/billmanager/_12-editPTRs.sh

echo "Rsync from /root/scripts/output/reverse_zones/ to DNSmanager:/root/rsyncdst_rev is running.."
echo "rm -rf /root/rsyncdst_rev/*" | ssh ${DNSmgr} &>/dev/null
rsync -avz -r -q /root/scripts/output/reverse_zones/* ${DNSmgr}:/root/rsyncdst_rev/
echo "for file in \$(find /root/rsyncdst_rev/ -maxdepth 1 -type f); do newname=\$(echo \${file,,} | rev | cut -c 2- | rev); mv \$file \${newname}; sed -i 's/reverse_zones/\/var\/named\/domains\/caravan.ru\/reverse_zones/g' \${newname}; done" | ssh ${DNSmgr}

echo "mkdir /var/named/domains/caravan.ru/reverse_zones" | ssh ${DNSmgr} 2>/dev/null
echo "chown named:named /var/named/domains/caravan.ru/reverse_zones" | ssh ${DNSmgr} 2>/dev/null
echo "rm -rf /root/rsyncdst_rev/*ba*" | ssh ${DNSmgr} 2>/dev/null
echo "for dirs in \$(find /root/rsyncdst_rev -maxdepth 1 -type d | sed '1d'); do cp -R \${dirs} /var/named/domains/caravan.ru/reverse_zones; done" | ssh ${DNSmgr}
echo "chown -R named:named /var/named/domains/caravan.ru/reverse_zones/*" | ssh ${DNSmgr} 2>/dev/null
}

usersdomains() {
echo "Generating list of OACI clientID and their domains"
./_11-oaciIDandDomains.py
# scp /root/scripts/output/_11-oaciIDandDomains* 10.10.20.26:/root/scripts/lab/variables_iddomainslist.py
cp /root/scripts/output/_11-oaciIDandDomains* /root/scripts/billmanager/variables_iddomainslist.py
}

if [ $# -eq 0 ]
then
	echo "You must pass the key to run script. Run ${0} -h to get info"
	exit 1
fi

echo "Before we start, check please, if it is correct variable?"
echo "If it is not, edit variables value in /root/scripts/billmanager/variables_bashvars.sh"
echo ""
echo "Current DNS private IP: ${NS1}"
echo "Current DNSmanager private IP: ${DNSmgr}"
ok=0
while [ $ok -eq 0 ]
do
	echo "Is it correct (y/n?)"
	read p
	if [ "${p}" == "yes" -o "${p}" == "y" ]
	then
		ok=1
		echo ""
		echo "OK, starting.."
		break
	fi
	if [ "${p}" == "no" -o "${p}" == "n" ]
	then
		ok=1
		echo ""
		echo "OK, edit /root/scripts/billmanager/variables_bashvars.sh"
	fi
	if [ "${p}" != "no" -o "${p}" != "n" -o "${p}" != "yes" -o "${p}" != "y" ]
	then
		echo "Incorrect input."
	fi
done
case $1 in
	-h)
		echo "-s    -- Running rsync to resync zones from old DNS to new DNS. You also be able to find, if there are any new zone files"
		echo "-o    -- Running oaci-parser that creates iddomainlist.py file with pairs accountID:domainnames"
		echo "-a    -- Running rsync first, next oaci-parser"
		echo "-h    -- Running this info"
	;;
	-s)
		synczone
		exit $?
	;;
	-o)
		usersdomains
		exit $?
	;;
	-a)
		synczone
		usersdomains
		exit $?
esac
echo "Gj. You can run /root/scripts/billmanager/_20-oaci2ispdomains.py now"
