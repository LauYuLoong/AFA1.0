#!/bin/bsh

AFA_USERNAME="maps"

#       检查中间业务定时调度CronServer是否存在
pids=`ps -ef | grep $AFA_USERNAME | grep "python CronServer.py" | grep -v grep | awk '{print $2}'`
if [ "$pids" ];then
        echo "关闭平台定时调度管理进程-CronServer:[ $pids ]"
        kill -9 $pids
fi

#	检查中间业务平台守护进程afapd是否存在
pids=`ps -ef | grep $AFA_USERNAME | grep "afapd" | grep -v grep | awk '{print $2}'`
if [ "$pids" ];then
	echo "关闭平台守护进程-afapd:[ $pids ]"
	kill -9 $pids
	sleep 1
	unlink afaipc/sync_fifo
fi

#	检查中间业务平台监听进程listener是否存在
pids=`ps -ef | grep $AFA_USERNAME | grep "listener" | grep -v grep | awk '{print $2}'`
if [ "$pids" ];then
	echo "关闭平台监听进程-listener:[ $pids ]"
	kill -9 $pids
	sleep 1
	unlink afaipc/service_fifo
	unlink afaipc/listener_unix
	unlink afaipc/monitor_unix
fi

#	检查中间业务平台日志服务LoggingServer是否存在
pids=`ps -ef | grep $AFA_USERNAME | grep "python LoggingServer.py" | grep -v grep | awk '{print $2}'`
if [ "$pids" ];then
	echo "关闭平台日志服务进程-LoggingServer:[ $pids ]"
	kill -9 $pids
fi

echo "成功关闭中间业务平台AFA"
