#!/bin/bash
target="https://www.jogossantacasa.pt/web/SCCartazResult/euroMilhoes"
gc=google-chrome

case $1 in
  --get-key)
  $gc --headless --dump-dom $target > ./landing_zone/page"_"`date +%Y_%m_%d`.html
  echo "Page saved"
  python3 ./python_modules/load_data.py
  echo "Data loaded"
  ;;
  --create-dw)
  python3 ./python_modules/create_dw.py
  exit
  ;;
  --help)
  echo ""
  echo "Made By: Ivo Xavier"
  echo ""
  echo " --get-key > Save webpage as html & Load Data to MySQL"
  echo ""
  echo " --create-dw > Create DataWarehouse on MySQL"
  ;;
esac