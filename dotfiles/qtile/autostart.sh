#!/bin/sh

# Network & removable media system tray applets
nm-applet &
blueman-applet &
udiskie -t &

xss-lock -- xlock &

/run/current-system/profile/libexec/polkit-gnome-authentication-agent-1 &
