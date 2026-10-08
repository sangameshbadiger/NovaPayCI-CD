#!/bin/bash

exec > /var/log/novapay-user-data.log 2>&1

echo "NovaPay user-data started"

dnf update -y
dnf install -y nginx

systemctl enable nginx
systemctl start nginx

echo "<h1>NovaPay Digital Bank</h1>" > /usr/share/nginx/html/index.html

echo "NovaPay user-data completed"
