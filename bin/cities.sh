#!/bin/sh
#  @author:       Zhanliang Liu
#  @description:  get https://3g.dxy.cn/newh5/view/pneumonia hourly
HOME=/home/zliu
CURR_PATH=`cd $(dirname $0);pwd;`
cd $CURR_PATH
python citycnt.py >> py.log
git add ../cities/*.json
git commit -m "get cities" 
git push >> git_cities.log
