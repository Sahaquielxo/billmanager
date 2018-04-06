#!/bin/bash

prlctl set dnsmanager --device-del net0
prlctl set dnsmanager --device-del net1

prlctl set dnsmanager-slave --device-del net0
prlctl set dnsmanager-slave --device-del net1

prlctl set dnsmanager --device-add net --network Bridged --mac '00:18:51:7d:29:e0' --ipadd '212.24.37.249/255.255.255.240' --gw 212.24.37.241 --nameserver '185.48.236.55 217.23.129.4'
prlctl set dnsmanager-slave --device-add net --network Bridged --mac '001851BC1AB4' --ipadd '212.24.43.87/255.255.255.240' --gw 212.24.43.81 --nameserver '185.48.236.55 217.23.129.4'
