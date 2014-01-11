#!/bin/bsh

#清理AFA日志
#echo "开始清理AFA日志"
#tar cvf afalogback.tar log 1>/dev/null
#mv afalogback.tar $HOME/tmp/
#rm ./log/*
#echo "AFA日志清理完毕"

AFA_USERNAME="maps"

cd bin

#	检查中间业务平台日志服务LoggingServer是否存在
pids=`ps -ef | grep $AFA_USERNAME | grep "python LoggingServer.py" | grep -v grep | awk '{print $2}'`
if [ "$pids" ];then
	echo "中间业务平台日志服务 [ LoggingServer ] 已经启动。"
	exit -1
fi

#	检查中间业务平台守护进程afapd是否存在
pids=`ps -ef | grep $AFA_USERNAME | grep "afapd" | grep -v grep | awk '{print $2}'`
if [ "$pids" ];then
	echo "中间业务平台守护进程 [ afapd ] 已经启动。"
	exit -2
fi

#	检查中间业务平台监听进程listener是否存在
pids=`ps -ef | grep $AFA_USERNAME | grep "listener" | grep -v grep | awk '{print $2}'`
if [ "$pids" ];then
	echo "中间业务平台监听进程 [ listener ] 已经启动。"
	exit -3
fi

#	检查中间业务平台业务处理进程CronServer是否存在
pids=`ps -ef | grep $AFA_USERNAME | grep "CronService" | grep -v grep | awk '{print $2}'`
if [ "$pids" ];then
	echo "中间业务平台定时调度进程 [ CronServer ] 已经启动。"
	exit -4
fi

#	启动平台
python LoggingServer.py &

#       启动定时调度管理程序
python CronServer.py &

sleep 1
./afapd 100 &

