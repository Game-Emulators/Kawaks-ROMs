#!/bin/sh

# Yaowen Xu 2021年2月1日

apt install curl -y
pip install beautifulsoup4
pip install requests
pip install lxml

python2 downld-step-1.py
sleep 360
python2 downld-step-2.py
bash download.sh