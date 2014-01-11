# -*- coding: gbk -*-
##################################################################
#             网络通讯发送和接收指定长度数据封装模块
#================================================================
#                作    者：    陈 显 明 
#                修改时间：    20070522
##################################################################
import time

#    用以控制循环传输数据的次数，避免进入死循环
#MAX_TRANSFER_RETRIES = 8

#    从网络接收指定长度的数据
def receiveNumBytes( connection, num, timeout = 65 ):
    #retries = 0
    baseTimeValue, totalTimeSpent = 1, 0
    result = connection.recv( num )    #    接收数据长度
    while( len( result ) < num ):
        #    睡眠一段时间，等待网络上的数据就绪
        time.sleep( baseTimeValue )
        totalTimeSpent = totalTimeSpent + baseTimeValue
        baseTimeValue = baseTimeValue * 2

        result = result + connection.recv( num - len( result ) )
        #retries = retries + 1
        #if( retries == MAX_TRANSFER_RETRIES ): raise StandardError, "接收网络数据超时"
        if( ( ( totalTimeSpent + baseTimeValue ) > timeout ) and ( len( result ) < num ) ): raise StandardError, "接收网络数据超时"
    if( len( result ) != num ):
        print '接收数据异常:  (', len( result ), "<", num, ")"
        return None
    return result

#    通过网络发送指定缓冲区中的所有内容
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
            #    睡眠一段时间，等待网络上的数据就绪
            time.sleep( baseTimeValue )
            totalTimeSpent = totalTimeSpent + baseTimeValue
            baseTimeValue = baseTimeValue * 2

            sent = connection.send( sendData[sentsofar:] )
            sentsofar = sentsofar + sent
            left = left - sent
            #retries = retries + 1
            #if( retries == MAX_TRANSFER_RETRIES ): raise StandardError, "发送网络数据超时"
            if( ( ( totalTimeSpent + baseTimeValue ) > timeout ) and ( left > 0 ) ): raise StandardError, "发送网络数据超时"
