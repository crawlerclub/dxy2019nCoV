#!/bin/sh
#  @author:       Zhanliang Liu
#  @description:  get http://2019ncov.nosugartech.com/data.json daily
HOME=/home/zliu
url="http://2019ncov.nosugartech.com/data.json"
echo "Starting download ${url}"
CURR_PATH=`cd $(dirname $0);pwd;`
cd $CURR_PATH
ts=`date +%Y%m%d`
echo $day >> git.log
wget ${url}  -O ../traffic/${ts}.json
git add ../traffic/${ts}.json
git commit -m "get data for ${ts}" >> git.log
git push >> git.log
