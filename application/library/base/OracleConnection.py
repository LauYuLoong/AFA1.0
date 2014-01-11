# -*- coding: gbk -*-
######################################################
#  Oracle数据库连接提供模块，管理进程中的唯一实例(singleton)
#＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
#                作    者：    陈 显 明 
#                修改时间：    20050602
######################################################

import cx_Oracle, os, ConfigParser

#    模块中的全局变量，用于多进程时记住数据库连接
connection = None
#print 'Initializing oracle connection......'

#    关闭连接，用于出错时为创建数据库连接准备环境
def closeConnection( ):
    global connection
    if( connection != None ):
        #print 'Closing oracle database connection......'
        connection.close( )
        connection = None
        
#    如果不存在就创建数据库连接，返回唯一实例
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

#    重置连接，需要调用之前先关闭数据库连接
def resetConnection( ):
    #print 'Resetting oracle database connection......'
    global connection
    connection = None


