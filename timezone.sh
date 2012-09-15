#!/usr/bin/sh

TIMEZONE=$(cat /etc/timezone)
cp -af /usr/share/zoneinfo/"$TIMEZONE" /etc/localtime

