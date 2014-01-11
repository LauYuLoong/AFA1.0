# -*- coding: gbk -*-
######################################################
#  DB2���ݿ������ṩģ�飬��������е�Ψһʵ��(singleton)
#����������������������������������������������������������������
#                ��    �ߣ�    �� �� �� 
#                �޸�ʱ�䣺    20050602
######################################################

import DB2, os, ConfigParser

#=================ģ���е�ȫ�ֱ��������ڶ����ʱ��ס���ݿ�����===================
connection = None

#=================�ر����ӣ����ڳ���ʱΪ�������ݿ�����׼������===================
def closeConnection( ):

    global connection

    if( connection != None ):
        connection.close( )
        connection = None

#==================��������ھʹ������ݿ����ӣ�����Ψһʵ��===================
def getConnection( ):

    global connection

    if( connection == None ):

        config = ConfigParser.ConfigParser( )
        configFileName = os.environ['AFAP_HOME'] + '/conf/dbconnect.conf'
        config.readfp( open( configFileName ) )
        connection = DB2.connect(config.get('db2','tnsentry'),config.get('db2','username'),config.get('db2','password' ),0,1)
    return connection

#==================�������ӣ���Ҫ����֮ǰ�ȹر����ݿ�����====================
def resetConnection( ):

    global connection
    connection = None
