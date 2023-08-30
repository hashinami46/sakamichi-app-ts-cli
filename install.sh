#!/bin/bash

sudo apt update && sudo apt upgrade -y
sudo apt install -y nodejs npm python3 git ffmpeg
sudo npm i -g n
sudo n latest -y

python3 -m ensurepip --upgrade
pip install -r requirements.txt
git clone https://github.com/Youjose/PyCriCodecs.git
cp -f .config/PyCriCodecs.setup.py PyCriCodecs/setup.py
cd PyCriCodecs && pip install . -v && cd ../ && rm -rf PyCriCodecs
