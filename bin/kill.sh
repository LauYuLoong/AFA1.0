#!/bin/bsh


#	����м�ҵ��ƽ̨�����Ƿ����
pids=`ps -ef | grep afa2 | grep "service" | grep -v grep | awk '{print $2}'`
if [ "$pids" ];then
	echo "ɱ��ƽ̨�ػ�����service��$pids��"
	kill -9 $pids
	sleep 1
fi


