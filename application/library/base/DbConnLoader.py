# -*- coding: gbk -*-
################################################################
#   通过配置文件载入数据库连接提供模块，管理进程中的唯一实例(singleton)
#==============================================================
#                作    者：    陈 显 明 
#                修改时间：    20060305
################################################################
import os, ConfigParser

#    读取配置文件中的数据库实现模块信息
config = ConfigParser.ConfigParser( )
configFileName = os.environ['AFAP_HOME'] + '/conf/dbconnect.conf'
config.readfp( open( configFileName ) )
dbModName = config.get( 'dbconnection', 'moduleName' )

#    载入数据库实现模块
#print "Importing connection implementation module '",dbModName,"'......"
dbMod = __import__( dbModName )

#    进程启动的同时就创建实际的数据库连接,以便尽早发现数据库连接不上的问题
try:
    dbMod.getConnection( )
except:
    print "===================================\n获取数据库连接失败，请检查数据库服务是否已经启动\n==================================="
