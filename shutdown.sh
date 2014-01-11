#!/bin/bsh

AFA_USERNAME="maps"

#       ����м�ҵ��ʱ����CronServer�Ƿ����
pids=`ps -ef | grep $AFA_USERNAME | grep "python CronServer.py" | grep -v grep | awk '{print $2}'`
if [ "$pids" ];then
        echo "�ر�ƽ̨��ʱ���ȹ������-CronServer:[ $pids ]"
        kill -9 $pids
fi

#	����м�ҵ��ƽ̨�ػ�����afapd�Ƿ����
pids=`ps -ef | grep $AFA_USERNAME | grep "afapd" | grep -v grep | awk '{print $2}'`
if [ "$pids" ];then
	echo "�ر�ƽ̨�ػ�����-afapd:[ $pids ]"
	kill -9 $pids
	sleep 1
	unlink afaipc/sync_fifo
fi

#	����м�ҵ��ƽ̨��������listener�Ƿ����
pids=`ps -ef | grep $AFA_USERNAME | grep "listener" | grep -v grep | awk '{print $2}'`
if [ "$pids" ];then
	echo "�ر�ƽ̨��������-listener:[ $pids ]"
	kill -9 $pids
	sleep 1
	unlink afaipc/service_fifo
	unlink afaipc/listener_unix
	unlink afaipc/monitor_unix
fi

#	����м�ҵ��ƽ̨��־����LoggingServer�Ƿ����
pids=`ps -ef | grep $AFA_USERNAME | grep "python LoggingServer.py" | grep -v grep | awk '{print $2}'`
if [ "$pids" ];then
	echo "�ر�ƽ̨��־�������-LoggingServer:[ $pids ]"
	kill -9 $pids
fi

echo "�ɹ��ر��м�ҵ��ƽ̨AFA"
