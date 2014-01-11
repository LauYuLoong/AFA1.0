# -*- coding: gbk -*-
##################################################################
#             ����ͨѶ���ͺͽ���ָ���������ݷ�װģ��
#================================================================
#                ��    �ߣ�    �� �� �� 
#                �޸�ʱ�䣺    20070522
##################################################################
import time

#    ���Կ���ѭ���������ݵĴ��������������ѭ��
#MAX_TRANSFER_RETRIES = 8

#    ���������ָ�����ȵ�����
def receiveNumBytes( connection, num, timeout = 65 ):
    #retries = 0
    baseTimeValue, totalTimeSpent = 1, 0
    result = connection.recv( num )    #    �������ݳ���
    while( len( result ) < num ):
        #    ˯��һ��ʱ�䣬�ȴ������ϵ����ݾ���
        time.sleep( baseTimeValue )
        totalTimeSpent = totalTimeSpent + baseTimeValue
        baseTimeValue = baseTimeValue * 2

        result = result + connection.recv( num - len( result ) )
        #retries = retries + 1
        #if( retries == MAX_TRANSFER_RETRIES ): raise StandardError, "�����������ݳ�ʱ"
        if( ( ( totalTimeSpent + baseTimeValue ) > timeout ) and ( len( result ) < num ) ): raise StandardError, "�����������ݳ�ʱ"
    if( len( result ) != num ):
        print '���������쳣:  (', len( result ), "<", num, ")"
        return None
    return result

#    ͨ�����緢��ָ���������е���������
def sendAllData( connection, sendData, timeout = 65 ):
    if hasattr( connection, "sendall" ):
        connection.sendall( sendData )
    else:
        #retries = 0
        baseTimeValue, totalTimeSpent = 1, 0

        sent = connection.send( sendData[0:] )
        sentsofar = sent
        left = len( sendData ) - sent
        while left > 0:
            #    ˯��һ��ʱ�䣬�ȴ������ϵ����ݾ���
            time.sleep( baseTimeValue )
            totalTimeSpent = totalTimeSpent + baseTimeValue
            baseTimeValue = baseTimeValue * 2

            sent = connection.send( sendData[sentsofar:] )
            sentsofar = sentsofar + sent
            left = left - sent
            #retries = retries + 1
            #if( retries == MAX_TRANSFER_RETRIES ): raise StandardError, "�����������ݳ�ʱ"
            if( ( ( totalTimeSpent + baseTimeValue ) > timeout ) and ( left > 0 ) ): raise StandardError, "�����������ݳ�ʱ"
