#!/bin/bash
#Usage:
#------------------------------------------------------
#Filename:              startIntegModelServer.sh  
#Revision:              1.0
#Date:                  2018/07/27
#Author:                Jim
#Description:
#Notes:                
#------------------------------------------------------
Usage="Usage: $0 [stop|start]"
#[ $# -lt 2 ] && echo "${Usage}" && exit -1

#define alias time and bring into effect
alias dt='date +%Y-%m-%d" "%H:%M:%S'
shopt -s expand_aliases

export LANG=en_US.UTF-8


source /etc/profile
#当前脚本路径
cd `dirname $0`
scriptDir=`pwd`


echo "`dt`:当前脚本路径:${scriptDir}"


#停止服务
ps aux | grep python | grep manage.py | grep 0.0.0.0:8080 | awk '{print $2}' | xargs kill -9 > /dev/null 2>&1

rm -rf ./nohup.out

if [ "stop" = "$1" ];then
    state="stop"
else
    state="start"
    nohup python manage.py runserver 0.0.0.0:8080 &
    echo "`dt`:Start Succeed"
fi

pip freeze > ./requirements.txt
