#!/bin/sh
HOME=/home/zliu
echo "Starting download ${url}"
CURR_PATH=`cd $(dirname $0);pwd;`
cd $CURR_PATH
python crawler.py
git add ./data/*.csv
git commit -m "https://coronavirus.1point3acres.com/" >> git.log
git push >> git.log
