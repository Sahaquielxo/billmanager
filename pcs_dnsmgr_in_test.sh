#!/bin/bash

prlctl set dnsmanager --device-del net0
prlctl set dnsmanager-slave --device-del net0

prlctl set dnsmanager --device-add net --network Bridged --ipadd '212.24.37.248/255.255.255.240' --gw 212.24.37.241 --nameserver '185.48.236.55 217.23.129.4'
prlctl set dnsmanager --device-add net --ipadd '10.10.20.24/255.255.0.0'
prlctl set dnsmanager --device-set net1 --type routed

prlctl set dnsmanager-slave --device-add net --network Bridged --ipadd '212.24.43.88/255.255.255.240' --gw 212.24.43.81 --nameserver '185.48.236.55 217.23.129.4'
prlctl set dnsmanager-slave --device-add net --ipadd '10.10.20.25/255.255.0.0'
prlctl set dnsmanager-slave --device-set net1 --type routed

