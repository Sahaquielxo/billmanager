#!/bin/bash

OLDIP='212.24.37.248'
NEWIP='212.24.37.249'
OLDSLAVEIP='212.24.43.88'
NEWSLAVEIP='212.24.43.87'

sed -i.bak "s/$OLDIP/$NEWIP/g" /usr/local/mgr5/etc/ihttpd.conf
sed -i.bak "s/$OLDIP/$NEWIP/g;s/$OLDSLAVEIP/$NEWSLAVEIP/g" /etc/named.conf
