# -*- coding: gbk -*-
######################################################
#  DB2���ݿ������ṩģ�飬��������е�Ψһʵ��(singleton)
#=====================================================
#                ��    �ߣ�    �� �� �� 
#                �޸�ʱ�䣺    20060913
######################################################
import MySQLdb

#    ģ���е�ȫ�ֱ��������ڶ����ʱ��ס���ݿ�����
connection = None

#    �ر����ӣ����ڳ���ʱΪ�������ݿ�����׼������
def closeConnection( ):
    global connection
    if( connection != None ):
        connection.close( )
        connection = None
        
#    ��������ھʹ������ݿ����ӣ�����Ψһʵ��
def getConnection( ):
    global connection
    if( connection == None ):
        #connection = MySQLdb.connect( host="localhost", user="root", db="afa" ,unix_socket="/tmp/mysql.sock")
        connection = MySQLdb.connect( host="localhost", user="afa", passwd="afa", db="afa" ,unix_socket="/tmp/mysql.sock")
        connection.autocommit(1)
        #connection = MySQLdb.connect( host="localhost", user="afa", passwd="afa", db="afa" ,unix_socket="/tmp/mysql.sock")
    return connection

#    �������ӣ���Ҫ����֮ǰ�ȹر����ݿ�����
def resetConnection( ):
    global connection
    connection = None



