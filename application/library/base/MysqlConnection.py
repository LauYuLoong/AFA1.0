# -*- coding: gbk -*-
######################################################
#  DB2数据库连接提供模块，管理进程中的唯一实例(singleton)
#=====================================================
#                作    者：    陈 显 明 
#                修改时间：    20060913
######################################################
import MySQLdb

#    模块中的全局变量，用于多进程时记住数据库连接
connection = None

#    关闭连接，用于出错时为创建数据库连接准备环境
def closeConnection( ):
    global connection
    if( connection != None ):
        connection.close( )
        connection = None
        
#    如果不存在就创建数据库连接，返回唯一实例
def getConnection( ):
    global connection
    if( connection == None ):
        #connection = MySQLdb.connect( host="localhost", user="root", db="afa" ,unix_socket="/tmp/mysql.sock")
        connection = MySQLdb.connect( host="localhost", user="afa", passwd="afa", db="afa" ,unix_socket="/tmp/mysql.sock")
        connection.autocommit(1)
        #connection = MySQLdb.connect( host="localhost", user="afa", passwd="afa", db="afa" ,unix_socket="/tmp/mysql.sock")
    return connection

#    重置连接，需要调用之前先关闭数据库连接
def resetConnection( ):
    global connection
    connection = None



