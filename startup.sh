#!/bin/bsh

#����AFA��־
#echo "��ʼ����AFA��־"
#tar cvf afalogback.tar log 1>/dev/null
#mv afalogback.tar $HOME/tmp/
#rm ./log/*
#echo "AFA��־�������"

AFA_USERNAME="maps"

cd bin

#	����м�ҵ��ƽ̨��־����LoggingServer�Ƿ����
pids=`ps -ef | grep $AFA_USERNAME | grep "python LoggingServer.py" | grep -v grep | awk '{print $2}'`
if [ "$pids" ];then
	echo "�м�ҵ��ƽ̨��־���� [ LoggingServer ] �Ѿ�������"
	exit -1
fi

#	����м�ҵ��ƽ̨�ػ�����afapd�Ƿ����
pids=`ps -ef | grep $AFA_USERNAME | grep "afapd" | grep -v grep | awk '{print $2}'`
if [ "$pids" ];then
	echo "�м�ҵ��ƽ̨�ػ����� [ afapd ] �Ѿ�������"
	exit -2
fi

#	����м�ҵ��ƽ̨��������listener�Ƿ����
pids=`ps -ef | grep $AFA_USERNAME | grep "listener" | grep -v grep | awk '{print $2}'`
if [ "$pids" ];then
	echo "�м�ҵ��ƽ̨�������� [ listener ] �Ѿ�������"
	exit -3
fi

#	����м�ҵ��ƽ̨ҵ�������CronServer�Ƿ����
pids=`ps -ef | grep $AFA_USERNAME | grep "CronService" | grep -v grep | awk '{print $2}'`
if [ "$pids" ];then
	echo "�м�ҵ��ƽ̨��ʱ���Ƚ��� [ CronServer ] �Ѿ�������"
	exit -4
fi

#	����ƽ̨
python LoggingServer.py &

#       ������ʱ���ȹ������
python CronServer.py &

sleep 1
./afapd 100 &

