# -*- coding: gbk -*-
####################################################################
#    ��    ��:    Tvouh013.py
#    ˵    ��:    ƾ֤����.ƾ֤�������ϸ��ѯ����
#    ��    ��:    �м�ҵ����ƽ̨��AFA��--- UNIX: AIX 5.3
#    ��    ��:    ���ǽ�
#    ��    ˾:    ������ͬ�Ƽ�
#    ������ַ:    ����
#    ����ʱ��:    2008��6��16��
#    ά����¼:
####################################################################

import TradeContext, AfaLoggerFunc, AfaUtilTools, AfaFunc, AfaFlowControl, AfaDBFunc
from types import *
import VouhFunc,HostContext,VouhHostFunc

def main( ):

    AfaLoggerFunc.tradeInfo( 'ƾ֤�������ϸ��ѯ����['+TradeContext.TemplateCode+']����' )

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

        #=============��ȡ��������==========================
        HostContext.I1OTSB = TradeContext.sBesbNo         #������
        HostContext.I1SBNO = TradeContext.sBesbNo         #������
        HostContext.I1USID = TradeContext.sTellerNo       #��Ա��
        HostContext.I1WSNO = TradeContext.sWSNO           #�ն˺�
        if(not VouhHostFunc.CommHost('2001')):
            tradeExit(TradeContext.errorCode, TradeContext.errorMsg)
            raise AfaFlowControl.flowException( )
        if(TradeContext.errorCode == '0000'):
            SBNO = HostContext.O1SBCH
            AfaLoggerFunc.tradeInfo( SBNO )
        
        #=============��ȡ��Ա����==========================
        HostContext.I1TELR = TradeContext.sTellerNo       #��Ա��
        HostContext.I1SBNO = TradeContext.sBesbNo         #������
        HostContext.I1USID = TradeContext.sTellerNo       #��Ա��
        HostContext.I1WSNO = TradeContext.sWSNO           #�ն˺�
        if(not VouhHostFunc.CommHost('8809')):
            tradeExit(TradeContext.errorCode, TradeContext.errorMsg)
            raise AfaFlowControl.flowException( )
        if(TradeContext.errorCode == '0000'):
            TELLER = HostContext.O1TLRK
            AfaLoggerFunc.tradeInfo( TELLER )
            
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

        wheresql="t1.VOUHTYPE = t.VOUHTYPE AND (t.TELLERNO = '" + TradeContext.sTellerTailNo + "' or t.RIVTELLER = '"+ TradeContext.sTellerTailNo +"')\
                AND t.WORKDATE >='" + TradeContext.sStartDate + "' AND t.WORKDATE <='"+TradeContext.sEndDate+"' \
                and (substr(t1.BESBNO,1,6) = substr(t.BESBNO,1,6)) and TRANSTATUS = '0'"

        if(SBNO == '33' and TELLER == "10"):
            wheresql = wheresql + " AND ((t.VOUHSTATUS = '0' and t.EXSTATUS = ' ') \
                                        or (t.VOUHSTATUS = '1' and t.EXSTATUS = '0') \
                                        or (t.VOUHSTATUS = '2' and t.EXSTATUS = '0'))"

        elif(TELLER == "10"):
            wheresql = wheresql + " AND ((t.VOUHSTATUS = '2' and t.EXSTATUS = '0') \
                                        or (t.VOUHSTATUS = '2' and t.EXSTATUS = '3') \
                                        or (t.VOUHSTATUS = '0' and t.EXSTATUS = '2') \
                                        or (t.VOUHSTATUS = '3' and t.EXSTATUS = '2'))"

        #==============�������=====================
        if (TradeContext.existVariable("sSelBesbNo") and len(TradeContext.sSelBesbNo) <> 0 ):
            wheresql = wheresql + " and (substr(t.BESBNO,1,6) = substr('" + TradeContext.sSelBesbNo + "',1,6))"

        #==============��ƾ֤����=====================
        if (TradeContext.existVariable("sVouhType") and len(TradeContext.sVouhType) <> 0 ):
            wheresql = wheresql + " and t.VOUHTYPE = '" + TradeContext.sVouhType + "'"

        sqlStr = "SELECT TELLERNO,VOUHTYPE,STARTNO,ENDNO,VOUHNUM,VOUHNAME,VOUHSTATUS,WORKDATE \
                FROM ( \
                SELECT row_number() over() as rowid,t.TELLERNO,t.VOUHTYPE,t.STARTNO,t.ENDNO,t.VOUHNUM,t1.VOUHNAME,t.VOUHSTATUS,t.WORKDATE \
                FROM VOUH_MODIFY t,VOUH_PARAMETER t1 \
                WHERE " + wheresql + " \
                ) as tab1 \
                where tab1.rowid >= " + str(TradeContext.sStart)

        AfaLoggerFunc.tradeDebug(sqlStr);
        #��ѯ���ݿⲢ�����صĽ��ѹ����Ӧ������
        records = AfaDBFunc.SelectSql( sqlStr, int(TradeContext.arraySize))
        if( records == None ):
            VouhFunc.tradeExit('A005067', '��ѯ[ƾ֤�ǼǱ�]�����쳣!')
            raise AfaFlowControl.flowException( )
        elif( len( records ) == 0 ):
            VouhFunc.tradeExit('A005068', 'ƾ֤������!' )
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
            sVouhStatus = ''
            sWorkDate = ''

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
                sVouhStatus = sVouhStatus + strSplit + records[i][6]
                sWorkDate = sWorkDate + strSplit + records[i][7]

        TradeContext.tradeResponse.append( ['sVouhType',sVouhType] )
        TradeContext.tradeResponse.append( ['sVouhName',sVouhName] )
        TradeContext.tradeResponse.append( ['sStartNo',sStartNo] )
        TradeContext.tradeResponse.append( ['sEndNo',sEndNo] )
        TradeContext.tradeResponse.append( ['sVouhNum',sVouhNum] )
        TradeContext.tradeResponse.append( ['sVouhStatus',sVouhStatus] )
        TradeContext.tradeResponse.append( ['sWorkDate',sWorkDate] )
        TradeContext.tradeResponse.append( ['sTellerTailNo',TradeContext.sTellerTailNo] )
        TradeContext.tradeResponse.append( ['sTellerNo',TradeContext.sTellerNo] )              #ƾ֤�Ż�����201109 
        TradeContext.tradeResponse.append( ['sLstTrxDay',TradeContext.sLstTrxDay] )
        TradeContext.tradeResponse.append( ['sLstTrxTime',TradeContext.sLstTrxTime] )
        TradeContext.tradeResponse.append( ['sNum',str(total)] )
        TradeContext.tradeResponse.append( ['errorCode','0000'] )
        TradeContext.tradeResponse.append( ['errorMsg','���׳ɹ�'] )

        AfaFunc.autoPackData()
        #=============�����˳�====================
        AfaLoggerFunc.tradeInfo( 'ƾ֤�������ϸ��ѯ����['+TradeContext.TemplateCode+']�˳�' )
    except AfaFlowControl.flowException, e:
        AfaFlowControl.exitMainFlow( )
    except AfaFlowControl.accException:
        AfaFlowControl.exitMainFlow( )
    except Exception, e:
        AfaFlowControl.exitMainFlow(str(e))


