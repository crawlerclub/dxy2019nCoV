#!/bin/sh
#  @author:       Zhanliang Liu
#  @description:  get https://3g.dxy.cn/newh5/view/pneumonia hourly
HOME=/home/zliu
url="https://3g.dxy.cn/newh5/view/pneumonia"
echo "Starting download ${url}"
CURR_PATH=`cd $(dirname $0);pwd;`
cd $CURR_PATH
ts=`date +%Y%m%d%H%M`
echo $day >> git.log
wget ${url}  -O ../data/${ts}.html
git add ../data/${ts}.html
git commit -m "get data for ${ts}" >> git.log
git push >> git.log
