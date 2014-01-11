# -*- coding: gbk -*-
##################################################################
#   ���մ���ƽ̨.��ģ��.
#=================================================================
#   �����ļ�:   3001.py
#   �޸�ʱ��:   2008-12-05 
##################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaFlowControl,AfaFunc,HostContext,AfaDBFunc,zzywHostFunc
from types import *

def main( ):
    
    AfaLoggerFunc.tradeInfo('=======����ҵ������ģ�忪ʼ=======')

    try:
        #=============��ʼ�����ر��ı���====================
        TradeContext.tradeResponse=[]
        
        #=============��ȡ��ǰϵͳʱ��====================
        TradeContext.workDate=AfaUtilTools.GetSysDate( )
        TradeContext.workTime=AfaUtilTools.GetSysTime( )

        
        HostContext.I1SBNO = TradeContext.PDSBNO
        #HostContext.I1USID = TradeContext.PDUSID
        HostContext.I1AUUS = TradeContext.PDAUUS
        HostContext.I1AUPS = TradeContext.PDAUPS
        HostContext.I1WSNO = TradeContext.PDWSNO
        HostContext.I1ACCN = TradeContext.JXACCT
        AfaLoggerFunc.tradeInfo(HostContext.I1ACCN)
        #HostContext.I1CCNO = TradeContext.ccno
       
        
        #����������
        zzywHostFunc.CommHost()
        AfaLoggerFunc.tradeInfo('����ͨѶ����')

        if( HostContext.O1MGID !='AAAAAAA'):
            AfaLoggerFunc.tradeInfo('-----test1-------------')
            TradeContext.bodyl=''
            TradeContext.errorCode = HostContext.O1MGID
            TradeContext.errorMsg  = HostContext.O1INFO
            AfaLoggerFunc.tradeInfo(TradeContext.errorCode)
            AfaLoggerFunc.tradeInfo(TradeContext.errorMsg)
            
            TradeContext.bodyl    ='243'
            TradeContext.CICS     =''                  
            TradeContext.INFCOD   ='E'                 
            TradeContext.Appcode  =''                  
            TradeContext.RETNO    ='0000'              
            TradeContext.PDTRCD   ='831030'            
            TradeContext.PDTRSQ   =''                  
            TradeContext.PDWSNO   =''                  
            TradeContext.JXACCT   =''                  
            TradeContext.JXCESQ   =''                  
            TradeContext.INFPAD0  =''                  
            TradeContext.INFPAD1  =''                  
            TradeContext.INFPAD2  =''                  
            TradeContext.PDTRDT  =''
            TradeContext.PDTRTM   =''                  
            TradeContext.PDTLSQ   =''
            TradeContext.PAMGID   =TradeContext.errorCode
            TradeContext.BEERTX   =HostContext.O1INFO                 
            AfaLoggerFunc.tradeInfo(HostContext.O1INFO)
            TradeContext.RecNum   =''  
            TradeContext.JXCKFG   =''
            TradeContext.JXTRCU   =''
        else:    
            AfaLoggerFunc.tradeInfo('-----test2-------------')
            TradeContext.JXTRCU   = HostContext.O1NXLN
            TradeContext.JXCKFG   = HostContext.O1MGNO
            AfaLoggerFunc.tradeInfo(HostContext.O1MGNO)
            TradeContext.CICS     =''
            TradeContext.INFCOD   ='N'
            TradeContext.Appcode  =''
            TradeContext.RETNO    ='0000'
            TradeContext.PDTRCD   ='831030'
            TradeContext.PDTRSQ   =''
            TradeContext.PDWSNO   =''
            TradeContext.JXACCT   =''
            TradeContext.JXCESQ   =''
            TradeContext.INFPAD0  =''
            TradeContext.INFPAD1  =''
            TradeContext.INFPAD2  =''
            TradeContext.PDTRTM   =''
            TradeContext.BEERTX   =''
            TradeContext.RecNum   = HostContext.O1ACUR
            
            
            TradeContext.bodyl   =str(int(TradeContext.RecNum)*51+243)
            AfaLoggerFunc.tradeInfo(TradeContext.bodyl) 
            
            if( HostContext.O1ACUR == '00' and HostContext.O1MGNO != '1' ):
                TradeContext.errorCode = '0001'
                TradeContext.errorMsg = "�޲�������"
                AfaLoggerFunc.tradeInfo(TradeContext.errorCode)
                AfaLoggerFunc.tradeInfo(TradeContext.errorMsg)
                TradeContext.PAMGID   =TradeContext.errorCode

            else:
                TradeContext.JXSGDT  = HostContext.O2ORDT 
                #TradeContext.JXCATP  = HostContext.O2SMCD
                
                #ת��ժҪ����Ϊ����
                TMP_O2SMCD = []
                for i in xrange(0,len(HostContext.O2SMCD)):
                    sum_sql = "select text from craba where smcd = '" + HostContext.O2SMCD[i] + "'"
                    sum_record = AfaDBFunc.SelectSql(sum_sql)
                    if sum_record == None:
                        TMP_O2SMCD.append("δ֪")
                    elif len(sum_record) <= 0:
                        TMP_O2SMCD.append("δ֪")
                    else:
                        TMP_O2SMCD.append(sum_record[0][0])
                TradeContext.JXCATP  = TMP_O2SMCD

                TradeContext.JXBDST  = HostContext.O2AMCD
                TradeContext.JXTRAM  = HostContext.O2TRAM
                TradeContext.JXACBL  = HostContext.O2ACBL
                TradeContext.JXCAUS  = HostContext.O2USID
                AfaLoggerFunc.tradeInfo(TradeContext.JXSGDT)
                AfaLoggerFunc.tradeInfo(TradeContext.JXCATP)
                AfaLoggerFunc.tradeInfo(TradeContext.JXBDST)
                AfaLoggerFunc.tradeInfo(TradeContext.JXTRAM)
                AfaLoggerFunc.tradeInfo(TradeContext.JXACBL)
                AfaLoggerFunc.tradeInfo(TradeContext.JXCAUS)
                
                # TradeContext.ordt  = HostContext.O2SBSQ
                # TradeContext.ordt  = HostContext.O2VLDT
                # TradeContext.ordt  = HostContext.O2PERD
                # TradeContext.ordt  = HostContext.O2ITCD
                # TradeContext.ordt  = HostContext.O2CYNO
                # TradeContext.ordt  = HostContext.O2INRT
                                  
                                  
        #=============�Զ����====================
        AfaFunc.autoPackData()
                              
        AfaLoggerFunc.tradeInfo('=======����ҵ������ģ�����=======')
                              
    except AfaFlowControl.flowException, e:
        #�����쳣             
        AfaFlowControl.exitMainFlow( )
                              
    except AfaFlowControl.accException:
        #�����쳣
        AfaFlowControl.exitMainFlow( )
            
    except Exception, e:
        #Ĭ���쳣
        AfaFlowControl.exitMainFlow( str( e ) )

