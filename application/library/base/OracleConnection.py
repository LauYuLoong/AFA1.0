# -*- coding: gbk -*-
######################################################
#  Oracle���ݿ������ṩģ�飬��������е�Ψһʵ��(singleton)
#����������������������������������������������������������������
#                ��    �ߣ�    �� �� �� 
#                �޸�ʱ�䣺    20050602
######################################################

import cx_Oracle, os, ConfigParser

#    ģ���е�ȫ�ֱ��������ڶ����ʱ��ס���ݿ�����
connection = None
#print 'Initializing oracle connection......'

#    �ر����ӣ����ڳ���ʱΪ�������ݿ�����׼������
def closeConnection( ):
    global connection
    if( connection != None ):
        #print 'Closing oracle database connection......'
        connection.close( )
        connection = None
        
#    ��������ھʹ������ݿ����ӣ�����Ψһʵ��
def getConnection( ):
    global connection
    if( connection == None ):
        #print 'Creating oracle database connection......'
        config = ConfigParser.ConfigParser( )
        configFileName = os.environ['AFAP_HOME'] + '/conf/dbconnect.conf'
        config.readfp( open( configFileName ) )
        connection = cx_Oracle.connect( config.get( 'oracle', 'username' ), config.get( 'oracle', 'password' ), config.get( 'oracle', 'tnsentry' ) )
        print "getConnection  connection = ["+str(connection)+"]"
    return connection

#    �������ӣ���Ҫ����֮ǰ�ȹر����ݿ�����
def resetConnection( ):
    #print 'Resetting oracle database connection......'
    global connection
    connection = None


