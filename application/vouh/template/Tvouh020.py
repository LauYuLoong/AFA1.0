# -*- coding: gbk -*-

####################################################################
#    ��    ��:    Tvouh020.py
#    ˵    ��:    ƾ֤����.��ѯ��ϸ���׸�����ˮ��
#    ��    ��:    �м�ҵ����ƽ̨��AFA��--- UNIX: AIX 5.3
#    ��    ��:    ���ǽ�
#    ��    ˾:    ������ͬ�Ƽ�
#    ������ַ:    ����
#    ����ʱ��:    2008��6��15��
#    ά����¼:
####################################################################

import TradeContext, AfaLoggerFunc, AfaUtilTools, AfaFunc,AfaFlowControl,AfaDBFunc
from types import *
#import AfaLoggerFunc

def tradeExit( code, msg ):
    TradeContext.errorCode, TradeContext.errorMsg=code, msg
    if code != '0000':
        return False
    return True

def main( ):
    
    AfaLoggerFunc.tradeInfo( '��ѯ��ϸ���׸�����ˮ��['+TradeContext.TemplateCode+']����' )
    
    #=============ǰ̨��������====================
    #TradeContext.oVouhSerial           ԭ��ˮ�� 
    #TradeContext.sVouhType             ƾ֤����
    #TradeContext.sStartNo              ��ʼ����
    #TradeContext.sEndNo                ��ֹ���� 
    #TradeContext.sVouhNum              ƾ֤����
    
    try:
        #=============��ʼ�����ر��ı���==================
        TradeContext.tradeResponse = []

        #=============��ȡ��ǰϵͳʱ��====================
        TradeContext.sLstTrxDay = AfaUtilTools.GetSysDate( )
        TradeContext.sLstTrxTime = AfaUtilTools.GetSysTime( ) 
        
        #����ǰ̨�����ƾ֤������в�ѯ������ǰ̨
        sqlStr = "select distinct t.VOUHTYPE,t1.VOUHNAME,t.TELLERNO,t.STARTNO,t.ENDNO,t.VOUHNUM FROM VOUH_MODIFY t,VOUH_PARAMETER t1 \
                 where VOUHSERIAL='"+TradeContext.sVouhSerial+"' AND t.VOUHTYPE = t1.VOUHTYPE AND substr(t.BESBNO,1,6) = substr(t1.BESBNO,1,6) \
                 AND TRANSTYPE not like '%����' AND TRANSTATUS = '0'"

        AfaLoggerFunc.tradeDebug(sqlStr);
        #��ѯ���ݿⲢ�����صĽ��ѹ����Ӧ������
        records = AfaDBFunc.SelectSql( sqlStr )
        if( records == None ):
            tradeExit('A005067', '��ѯ[ƾ֤����ǼǱ�]�����쳣!')
            raise AfaFlowControl.flowException( )
        elif( len( records ) == 0 ):
            tradeExit('A005068', 'ƾ֤������!' )
            raise AfaFlowControl.flowException( )
        else :
            record=AfaUtilTools.ListFilterNone( records )
            total=len( records )
            
            sVouhType = ''
            sVouhName = ''
            sTellerNo = ''
            sStartNo = ''
            sEndNo = ''
            sVouhNum = ''
            
            for i in range( 0, total ):
                if( i <> 0):
                    strSplit = '|'
                else:
                    strSplit = ''
                sVouhType = sVouhType + strSplit + records[i][0]
                sVouhName = sVouhName + strSplit + records[i][1]
                sTellerNo = sTellerNo + strSplit + records[i][2]
                sStartNo = sStartNo + strSplit + records[i][3]
                sEndNo = sEndNo + strSplit + records[i][4]
                sVouhNum = sVouhNum + strSplit + records[i][5]
                
        TradeContext.tradeResponse.append( ['oVouhSerial',TradeContext.sVouhSerial] )
        TradeContext.tradeResponse.append( ['sVouhType',sVouhType] )
        TradeContext.tradeResponse.append( ['sVouhName',sVouhName] )
        TradeContext.tradeResponse.append( ['oTellerNo',sTellerNo] )
        TradeContext.tradeResponse.append( ['sStartNo',sStartNo] )
        TradeContext.tradeResponse.append( ['sEndNo',sEndNo] )
        TradeContext.tradeResponse.append( ['sVouhNum',sVouhNum] )
        TradeContext.tradeResponse.append( ['sLstTrxDay',TradeContext.sLstTrxDay] )
        TradeContext.tradeResponse.append( ['sLstTrxTime',TradeContext.sLstTrxTime] )
        TradeContext.tradeResponse.append( ['sNum',str(total)] )
        TradeContext.tradeResponse.append( ['errorCode','0000'] )
        TradeContext.tradeResponse.append( ['errorMsg','���׳ɹ�'] )

        AfaFunc.autoPackData()
        #=============�����˳�====================
        AfaLoggerFunc.tradeInfo( '��ѯ��ϸ���׸�����ˮ��['+TradeContext.TemplateCode+']�˳�' )
    except AfaFlowControl.flowException, e:
        AfaFlowControl.exitMainFlow( )
    except AfaFlowControl.accException:
        AfaFlowControl.exitMainFlow( )
    except Exception, e:
        AfaFlowControl.exitMainFlow(str(e))

  
