# -*- coding: gbk -*-
################################################################
#   ͨ�������ļ��������ݿ������ṩģ�飬��������е�Ψһʵ��(singleton)
#==============================================================
#                ��    �ߣ�    �� �� �� 
#                �޸�ʱ�䣺    20060305
################################################################
import os, ConfigParser

#    ��ȡ�����ļ��е����ݿ�ʵ��ģ����Ϣ
config = ConfigParser.ConfigParser( )
configFileName = os.environ['AFAP_HOME'] + '/conf/dbconnect.conf'
config.readfp( open( configFileName ) )
dbModName = config.get( 'dbconnection', 'moduleName' )

#    �������ݿ�ʵ��ģ��
#print "Importing connection implementation module '",dbModName,"'......"
dbMod = __import__( dbModName )

#    ����������ͬʱ�ʹ���ʵ�ʵ����ݿ�����,�Ա㾡�緢�����ݿ����Ӳ��ϵ�����
try:
    dbMod.getConnection( )
except:
    print "===================================\n��ȡ���ݿ�����ʧ�ܣ��������ݿ�����Ƿ��Ѿ�����\n==================================="
