#!/bin/bash
# install_service.sh

sudo chmod +x /home/pi/light/light.py
cp /home/pi/light/light.service /etc/systemd/system/light.service
sudo systemctl enable light.service
sudo systemctl start light.service