#!/bin/sh
#  @author:       Zhanliang Liu
#  @description:  get https://3g.dxy.cn/newh5/view/pneumonia hourly
HOME=/home/zliu
CURR_PATH=`cd $(dirname $0);pwd;`
cd $CURR_PATH
ts=`date +%Y%m%d%H%M`
python citycnt.py
echo "python citycnt.py" >> py.log
git add ../cities/${ts}.json
git commit -m "get cities for ${ts}" >> git.log
git push >> git.log
