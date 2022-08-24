#!/bin/bash

# This script is used to set webdriver for the tests.
# Howewer, it is not used at server.

exit_code=0

# Google Chrome installation
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
check=$?

if [[ $check -eq 0 ]]; then
  echo "Starting installation process. Password may be required."
  sudo apt -y install ./google-chrome-stable_current_amd64.deb

  # Webdriver installation
  wget https://chromedriver.storage.googleapis.com/102.0.5005.61/chromedriver_linux64.zip
  check=$?

  if [[ $check -eq 0 ]]; then
    sudo apt install unzip
    sudo unzip chromedriver_linux64.zip /bin/

    # Deleting the downloaded files
    rm -rf chromedriver_linux64.zip google-chrome-stable_current_amd64.deb
  else
    echo "Unable to download chromedriver."
    result=2
  fi
else
  echo "Unable to download Google Chrome."
  result=1
fi

exit $result
