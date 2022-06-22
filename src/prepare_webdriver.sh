#!/bin/bash

# This script is used to set webdriver for the tests.
# Howewer, it is not used at server.

# Google Chrome installation
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt -y install ./google-chrome-stable_current_amd64.deb

# Webdriver installation
wget https://chromedriver.storage.googleapis.com/102.0.5005.61/chromedriver_linux64.zip
sudo apt install unzip
sudo unzip chromedriver_linux64.zip /bin/

# Deleting the downloaded files
rm -rf chromedriver_linux64.zip google-chrome-stable_current_amd64.deb
