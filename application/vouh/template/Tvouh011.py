# -*- coding: gbk -*-
####################################################################
#    ��    ��:    Tvouh011.py
#    ˵    ��:    ƾ֤����.��ѯƾ֤��潻��
#    ��    ��:    �м�ҵ����ƽ̨��AFA��--- UNIX: AIX 5.3
#    ��    ��:    ���ǽ�
#    ��    ˾:    ������ͬ�Ƽ�
#    ������ַ:    ����
#    ����ʱ��:    2008��6��16��
#    ά����¼:
#####################################################################
import TradeContext, AfaLoggerFunc, AfaUtilTools, AfaFunc,AfaFlowControl,AfaDBFunc
from types import *
import HostContext,VouhHostFunc,VouhFunc

def tradeExit( code, msg ):
    TradeContext.errorCode, TradeContext.errorMsg=code, msg
    if code != '0000':
        return False
    return True
    
def main( ):
    
    AfaLoggerFunc.tradeInfo( '��ѯƾ֤��潻��['+TradeContext.TemplateCode+']����' )
    
    #=============ǰ̨��������====================
    #TradeContext.sBesbNo           ������
    #TradeContext.sTellerNo         ��Ա��
    #TradeContext.sVouhType         ƾ֤����
    #TradeCoutext.sVouhStatus       ƾ֤״̬
    #TradeCoutext.sStartDate        ��ʼ����
    #TradeCoutext.sEndDate          ��ֹ����
    #TradeContext.sStart          ��ʼ��¼��
    #TradeContext.arraySize         ��ѯ����
    
    try:
        #=============��ʼ�����ر��ı���==================
        TradeContext.tradeResponse = []

        #=============��ȡ��ǰϵͳʱ��====================
        TradeContext.sLstTrxDay = AfaUtilTools.GetSysDate( )
        TradeContext.sLstTrxTime = AfaUtilTools.GetSysTime( ) 
        
        #beginƾ֤�Ż�����201109  
        #=============��ȡ��Աβ���===============================
        HostContext.I1SBNO = TradeContext.sBesbNo         #������
        HostContext.I1USID = TradeContext.sTellerNo       #��Ա��
        HostContext.I1WSNO = TradeContext.sWSNO           #�ն˺�
        HostContext.I1EDDT = TradeContext.sLstTrxDay      #��ֹ����
        HostContext.I1TELR = TradeContext.sTellerNo       #��Ա����
        
        if(not VouhHostFunc.CommHost('0104')):
            VouhFunc.tradeExit( TradeContext.errorCode, TradeContext.errorMsg )
            raise AfaFlowControl.flowException( )
        if(TradeContext.errorCode == '0000'):
            TradeContext.sTellerTailNobak = HostContext.O2CABO
            TradeContext.sTellerTailNo    = TradeContext.sTellerTailNobak[0]                 
            AfaLoggerFunc.tradeInfo( '���׹�Աβ��ţ�' + TradeContext.sTellerTailNo ) 
        #end   
        
        wheresql="substr(t1.BESBNO,1,6) = substr(t.BESBNO,1,6) AND t1.VOUHTYPE = t.VOUHTYPE AND t.VOUHSTATUS in ('0','2')"
        
        #==============�������=====================
        if (TradeContext.existVariable("sSelBesbNo") and len(TradeContext.sSelBesbNo) <> 0 ):
            wheresql = wheresql + " and t.BESBNO = '" + TradeContext.sSelBesbNo + "'"
            
        #==============��ƾ֤����=====================
        if (TradeContext.existVariable("sVouhType") and len(TradeContext.sVouhType) <> 0 ):
            wheresql = wheresql + " and t.VOUHTYPE = '" + TradeContext.sVouhType + "'"
        
        sqlStr = "SELECT TELLERNO,VOUHTYPE,STARTNO,ENDNO,VOUHNUM,VOUHNAME \
            FROM ( \
                    SELECT row_number() over() as rowid,t.TELLERNO,t.VOUHTYPE,t.STARTNO,t.ENDNO,t.VOUHNUM,t1.VOUHNAME \
                    FROM VOUH_REGISTER t,VOUH_PARAMETER t1 \
                    WHERE " + wheresql + " \
            ) as tab1 \
            where tab1.rowid >= " + str(TradeContext.sStart)
        
        AfaLoggerFunc.tradeDebug(sqlStr);
        #��ѯ���ݿⲢ�����صĽ��ѹ����Ӧ������
        records = AfaDBFunc.SelectSql( sqlStr, int(TradeContext.arraySize))
        if( records == None ):
            tradeExit('A005067', '��ѯ[ƾ֤�ǼǱ�]�����쳣!')
            raise AfaFlowControl.flowException( )
        elif( len( records ) == 0 ):
            tradeExit('A005068', 'ƾ֤������!' )
            raise AfaFlowControl.flowException( )
        else :
            record=AfaUtilTools.ListFilterNone( records )
            total=len( records )

            sTellerTailNo = ''
            sVouhType = ''
            sStartNo = ''
            sEndNo = ''
            sVouhNum = ''
            sVouhName = ''
            
            for i in range( 0, total ):
                if( i <> 0):
                    strSplit = '|'
                else:
                    strSplit = ''
                sTellerTailNo = sTellerTailNo + strSplit + records[i][0]
                sVouhType = sVouhType + strSplit + records[i][1]
                sStartNo = sStartNo + strSplit + records[i][2]
                sEndNo = sEndNo + strSplit + records[i][3]
                sVouhNum = sVouhNum + strSplit + records[i][4]
                sVouhName = sVouhName + strSplit + records[i][5]
                
        TradeContext.tradeResponse.append( ['sVouhType',sVouhType] )
        TradeContext.tradeResponse.append( ['sVouhName',sVouhName] )
        TradeContext.tradeResponse.append( ['sStartNo',sStartNo] )
        TradeContext.tradeResponse.append( ['sEndNo',sEndNo] )
        TradeContext.tradeResponse.append( ['sVouhNum',sVouhNum] )
        TradeContext.tradeResponse.append( ['sTellerTailNo',TradeContext.sTellerTailNo] ) 
        TradeContext.tradeResponse.append( ['sTellerNo',TradeContext.sTellerNo] )           #ƾ֤�Ż�����201109  ��Ա��������   
        TradeContext.tradeResponse.append( ['sLstTrxDay',TradeContext.sLstTrxDay] )
        TradeContext.tradeResponse.append( ['sLstTrxTime',TradeContext.sLstTrxTime] )
        TradeContext.tradeResponse.append( ['sNum',str(total)] )
        TradeContext.tradeResponse.append( ['errorCode','0000'] )
        TradeContext.tradeResponse.append( ['errorMsg','���׳ɹ�'] )

        AfaFunc.autoPackData()
        #=============�����˳�====================
        AfaLoggerFunc.tradeInfo( '��ѯƾ֤��潻��['+TradeContext.TemplateCode+']�˳�' )
    except AfaFlowControl.flowException, e:
        AfaFlowControl.exitMainFlow( )
    except AfaFlowControl.accException:
        AfaFlowControl.exitMainFlow( )
    except Exception, e:
        AfaFlowControl.exitMainFlow(str(e))

  
