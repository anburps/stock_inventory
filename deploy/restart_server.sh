#!/bin/sh
sudo setenforce 0
sudo systemctl restart nginx
sudo supervisorctl stop invoice
sudo supervisorctl start invoice
sudo supervisorctl reload