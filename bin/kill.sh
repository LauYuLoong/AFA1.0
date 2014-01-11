#!/bin/bsh


#	检查中间业务平台服务是否存在
pids=`ps -ef | grep afa2 | grep "service" | grep -v grep | awk '{print $2}'`
if [ "$pids" ];then
	echo "杀死平台守护进程service【$pids】"
	kill -9 $pids
	sleep 1
fi


