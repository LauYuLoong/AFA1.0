# -*- coding: gbk -*-
################################################################################
#   ����ҵ��ϵͳ�����ز�����
#===============================================================================
#   �����ļ�:   T001000_8400.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  XZH
#   �޸�ʱ��:   2008-06-10
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,os
from types import *


#=====================���ص�λ��Ϣ������========================================
def TrxMain():
    

    AfaLoggerFunc.tradeInfo('**********���ص�λ��Ϣ(8400)��ʼ**********')


    TradeContext.fileSum1 = 0
    TradeContext.fileSum2 = 0


    #����������Ϣ
    if not GetBatchBusiInfo():
        return False


    #����ʵʱ��Ϣ
    if not GetRealBusiInfo():
        return False


    #ͳ�������ļ�����
    sFileNum = 0
    sFileNum = TradeContext.fileSum1 + TradeContext.fileSum2
    if ( sFileNum <= 0 ):
        return ExitSubTrade( '9000', 'û���κε�λ��Ϣ' )

    #���صĵ�λ����
    TradeContext.tradeResponse.append(['fileSum', str(sFileNum)])


    AfaLoggerFunc.tradeInfo('**********���ص�λ��Ϣ(8400)����**********')

    #����
    TradeContext.tradeResponse.append(['errorCode', '0000'])
    TradeContext.tradeResponse.append(['errorMsg',  '���׳ɹ�'])
    return True


#��ȡ������λ��Ϣ
def GetBatchBusiInfo():

    try:
        AfaLoggerFunc.tradeInfo('����������λ��Ϣ')
    
        rm_cmd_str = "rm " + os.environ['AFAP_HOME'] + "/tmp/*" + TradeContext.I1SBNO + ".plist"
        os.system(rm_cmd_str)
    
        #ͳ�Ƹû��������ж��ٸ�ҵ�����(����)
        sql = "SELECT DISTINCT(APPNO),APPNAME FROM ABDT_UNITINFO WHERE STATUS = '1' AND AGENTTYPE IN ('3','4')" 
        sql = sql + " AND (AGENTMODE='0' OR (AGENTMODE='1' AND SUBSTR(BRNO,1,4)='" + TradeContext.I1SBNO[:4]
        sql = sql + "') OR (AGENTMODE='2' AND BRNO='" + TradeContext.I1SBNO + "'))"

        AfaLoggerFunc.tradeInfo(sql)

        records = AfaDBFunc.SelectSql( sql )
        if( records==None):
             return ExitSubTrade( '9000', '���ص�λ����������쳣1' )
                
        elif( len(records) == 0 ):
            AfaLoggerFunc.tradeInfo('û�з����κε�λ��Ϣ')
            return True

        else:
            TradeContext.fileSum1 = len(records)     #��Ҫ���ض��ٸ��ļ�����

            AfaLoggerFunc.tradeInfo('ʵʱ��λ��Ϣ�ļ�����=' + str(TradeContext.fileSum1))

            #����ҵ������ļ�
            filename1 = os.environ['AFAP_HOME'] + "/tmp/BAPPNO_" + TradeContext.I1SBNO + ".plist"

            AfaLoggerFunc.tradeInfo('�ļ���=' + filename1)

            fp1 = open(filename1,'w')
            fp1.write("TITLE = ҵ�����\n")

            for i in range(0,int(TradeContext.fileSum1)):

                fp1.write("ITEM  = " + AfaUtilTools.lrtrim(records[i][0]) + " | " + AfaUtilTools.lrtrim(records[i][1]) + " |\n")

                #����һ���̶����ļ�����ΪappNo+��������.plist
                filename = os.environ['AFAP_HOME'] + "/tmp/B" + AfaUtilTools.lrtrim(records[i][0]) + TradeContext.I1SBNO + ".plist"
                fp = open(filename,'w')
                fp.write("TITLE = ��λ����\n")

                #����appNo��ѯ��Ӧ��Ϣ
                sql1 = "SELECT BUSINO,BUSINAME FROM ABDT_UNITINFO WHERE "
                sql1 = sql1 + "APPNO=" + "'" + records[i][0] + "'"                 #ҵ����
                sql1 = sql1 + " AND STATUS='1'"                                    #״̬(0:ע��,1:����)
                sql1 = sql1 + " AND AGENTTYPE IN ('1','2','3','4') AND (AGENTMODE='0' OR (AGENTMODE='1' AND SUBSTR(BRNO,1,4)='" + TradeContext.I1SBNO[:4] + "') OR (AGENTMODE='2' AND BRNO='" + TradeContext.I1SBNO + "'))"

                try:
                    AfaLoggerFunc.tradeInfo(sql1)
                    
                    records1 = AfaDBFunc.SelectSql( sql1 )
                        
                    if( records1==None):
                        fp.close()
                        fp1.close()
                        return ExitSubTrade( '9000', '���ص�λ����������쳣2' )

                    else:
                        TradeContext.busiSum = len(records1)

                        for j in range(0,int(TradeContext.busiSum)):
                            fp.write("ITEM = " + AfaUtilTools.lrtrim(records1[j][0]) + " | " + AfaUtilTools.lrtrim(records1[j][1]) + " |\n")

                        fp.close()

                except Exception,e:
                    AfaLoggerFunc.tradeInfo(e)
                    fp.close()
                    fp1.close()
                    return ExitSubTrade( '9000', '���ص�λ����������쳣3' )

        return True
        
    except Exception,e:
        AfaLoggerFunc.tradeInfo(e)
        fp1.close()
        return ExitSubTrade( '9999', '����ҵ������쳣' )


	
#��ȡʵʱ��λ��Ϣ
def GetRealBusiInfo():

    try:
        AfaLoggerFunc.tradeInfo('����ʵʱ��λ��Ϣ')

        #ͳ�Ƹû��������ж��ٸ�ҵ�����(ʵʱ)
        sql = "SELECT DISTINCT(APPNO),APPNAME FROM ABDT_UNITINFO WHERE AGENTTYPE IN ('1','2')" 
        sql = sql + " AND (AGENTMODE='0' OR (AGENTMODE='1' AND SUBSTR(BRNO,1,4)='" + TradeContext.I1SBNO[:4]
        sql = sql + "') OR (AGENTMODE='2' AND BRNO='" + TradeContext.I1SBNO + "'))"

        AfaLoggerFunc.tradeInfo(sql)

        records = AfaDBFunc.SelectSql( sql )
        if( records==None):
             return ExitSubTrade( '9000', '����ʵʱ��λ����������쳣1' )

        elif( len(records) == 0 ):
            AfaLoggerFunc.tradeInfo('û�з����κ�ʵʱ��λ��Ϣ')
            return True

        else:
            TradeContext.fileSum2 = len(records)     #��Ҫ���ض��ٸ��ļ�����

            AfaLoggerFunc.tradeInfo('ʵʱ��λ��Ϣ�ļ�����=' + str(TradeContext.fileSum2))

            #����ҵ������ļ�
            filename1 = os.environ['AFAP_HOME'] + "/tmp/RAPPNO_" + TradeContext.I1SBNO + ".plist"

            AfaLoggerFunc.tradeInfo('�ļ���=' + filename1)

            fp1 = open(filename1,'w')
            fp1.write("TITLE = ҵ�����\n")

            for i in range(0,int(TradeContext.fileSum2)):

                fp1.write("ITEM  = " + AfaUtilTools.lrtrim(records[i][0]) + " | " + AfaUtilTools.lrtrim(records[i][1]) + " |\n")

                #����һ���̶����ļ�����ΪappNo+��������.plist
                filename = os.environ['AFAP_HOME'] + "/tmp/R" + AfaUtilTools.lrtrim(records[i][0]) + TradeContext.I1SBNO + ".plist"
                fp = open(filename,'w')
                fp.write("TITLE = ��λ����\n")

                #����appNo��ѯ��Ӧ��Ϣ
                sql1 = "SELECT BUSINO,BUSINAME FROM ABDT_UNITINFO WHERE "
                sql1 = sql1 + "APPNO=" + "'" + records[i][0] + "'"                  #ҵ����
                sql1 = sql1 + " AND STATUS='1'"                                    #״̬(0:ע��,1:����)
                sql1 = sql1 + " AND AGENTTYPE IN ('1','2') AND (AGENTMODE='0' OR (AGENTMODE='1' AND SUBSTR(BRNO,1,4)='" + TradeContext.I1SBNO[:4] + "') OR (AGENTMODE='2' AND BRNO='" + TradeContext.I1SBNO + "'))"

                try:
                    AfaLoggerFunc.tradeInfo(sql1)

                    records1 = AfaDBFunc.SelectSql( sql1 )
                    
                    if( records1==None):
                        fp.close()
                        fp1.close()
                        return ExitSubTrade( '9000', '����ʵʱ��λ����������쳣2' )

                    else:
                        TradeContext.busiSum = len(records1)

                        for j in range(0,int(TradeContext.busiSum)):
                            fp.write("ITEM = " + AfaUtilTools.lrtrim(records1[j][0]) + " | " + AfaUtilTools.lrtrim(records1[j][1]) + " |\n")

                        fp.close()

                except Exception,e:
                    AfaLoggerFunc.tradeInfo(e)
                    fp.close()
                    fp1.close()
                    return ExitSubTrade( '9000', '����ʵʱ��λ����������쳣3' )

        return True

    except Exception,e:
        AfaLoggerFunc.tradeInfo(e)
        fp1.close()
        return ExitSubTrade( '9999', '����ʵʱҵ������쳣' )



def ExitSubTrade( errorCode, errorMsg ):

    if( len( errorCode )!=0 ):
        TradeContext.tradeResponse.append(['errorCode', errorCode])
        TradeContext.tradeResponse.append(['errorMsg',  errorMsg])

    if( errorCode.isdigit( )==True and long( errorCode )==0 ):
        return True

    else:
        return False
