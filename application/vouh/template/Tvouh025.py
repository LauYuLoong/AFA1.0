# -*- coding: gbk -*-
###################################################################
#    ��    ��:    Tvouh025.py
#    ˵    ��:    ƾ֤����-->ƾ֤��Ա����
#    ��    ��:    �м�ҵ����ƽ̨��AFA��--- UNIX: AIX 5.3
#    ��    ��:    ���ǽ�
#    ��    ˾:    ������ͬ�Ƽ�
#    ������ַ:    ����
#    ����ʱ��:    2008��6��11�� 
#    ά����¼:   
##################################################################
import TradeContext, AfaLoggerFunc, AfaUtilTools, AfaFunc, AfaFlowControl, AfaDBFunc
from types import *
import AfaLoggerFunc,VouhFunc,binascii,HostContext,VouhHostFunc


def main( ):
    AfaLoggerFunc.tradeInfo( 'ƾ֤��Ա����['+TradeContext.TemplateCode+']����' )

    #=============ǰ̨��������===================================
    #TradeContext.sBesbNo                                 ������
    #TradeContext.sBesbSty                                ��������
    #TradeContext.sCur                                    ���Ҵ���
    #TradeContext.sTellerNo                               ��Ա��
    #TradeContext.sRivTeller                              �Է���Ա
    #TradeContext.sLstTrxDay                              ���������
    #TradeContext.sLstTrxTime                             �����ʱ��
    
    try: 
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
        
        #=============��ʼ�����ر��ı���========================
        TradeContext.tradeResponse = []
        TradeContext.sRivTeller = TradeContext.sInTellerNo
        
        #=============������ˮ��========================
        TradeContext.sVouhSerial = VouhFunc.GetVouhSerial( )

        #=============��ȡ��ǰϵͳʱ��==========================
        TradeContext.sLstTrxDay  = AfaUtilTools.GetSysDate( )
        TradeContext.sLstTrxTime = AfaUtilTools.GetSysTime( )

        TradeContext.sTransType    = 'ƾ֤��Ա����'
        
        #================�ж϶Է���Ա�Ƿ���ƾ֤==================================
        if(len(TradeContext.sInTellerNo) == 0):
            VouhFunc.tradeExit('A005061', '�Է���Ա����Ϊ��!')
            raise AfaFlowControl.flowException( )
        
        #if(TELLER == '01' or TELLER == '02' or TELLER == '03'):
        #    VouhFunc.tradeExit('A005061', '�ù�Ա���ܽ��д˲���!')
        #    raise AfaFlowControl.flowException( )
            
        sqlStr = "select * from VOUH_REGISTER where TELLERNO = '" + TradeContext.sInTellerNo + "' and VOUHSTATUS = '3'"
        
        records = AfaDBFunc.SelectSql( sqlStr )
        AfaLoggerFunc.tradeDebug(sqlStr)
        if records==-1 :
            VouhFunc.tradeExit( 'A005057', '��ѯ[ƾ֤�ǼǱ�]��Ϣ�쳣!' )
            raise AfaFlowControl.flowException( )
        elif len(records) > 0 :
            VouhFunc.tradeExit( 'A005058', '['+TradeContext.sInTellerNo+']��Ա���ܽ���!' )
            raise AfaFlowControl.flowException( )
        
        #================�жϹ�Ա�Ƿ���ƾ֤==================================
        
        #if((TradeContext.sTellerNo)[4:] == '01' or (TradeContext.sTellerNo)[4:] == '02' or (TradeContext.sTellerNo)[4:] == '03'):
        #    VouhFunc.tradeExit('A005061', '�ù�Ա���ܽ��д˲���!')
        #    raise AfaFlowControl.flowException( )
            
        sqlStr = "select * from VOUH_REGISTER where TELLERNO = '" + TradeContext.sTellerNo + "' and VOUHSTATUS = '3'"
        
        records = AfaDBFunc.SelectSql( sqlStr )
        AfaLoggerFunc.tradeDebug(sqlStr)
        if records==-1 :
            VouhFunc.tradeExit( 'A005057', '��ѯ[ƾ֤�ǼǱ�]��Ϣ�쳣!' )
            raise AfaFlowControl.flowException( )
        elif records==0 :
            VouhFunc.tradeExit( 'A005058', '��ƾ֤!' )
            raise AfaFlowControl.flowException( )
        
        #======================��Ա����=====================================
        sqlStr = "update VOUH_REGISTER set TELLERNO = '" + TradeContext.sInTellerNo + "' where TELLERNO = '" + TradeContext.sTellerNo + "' and VOUHSTATUS = '3'"
        
        records = AfaDBFunc.UpdateSqlCmt( sqlStr )
        AfaLoggerFunc.tradeDebug(sqlStr)
        if records==-1 :
            VouhFunc.tradeExit( 'A005057', '����[ƾ֤�ǼǱ�]��Ϣ�쳣!' )
            raise AfaFlowControl.flowException( )
        elif records==0 :
            VouhFunc.tradeExit( 'A005058', '�޸�[ƾ֤�ǼǱ�]������Ϣʧ��!' )
            raise AfaFlowControl.flowException( )

        #����ƾ֤����ǼǱ�
        VouhFunc.VouhModify()
        #���ݿ��ύ
        AfaDBFunc.CommitSql( )
        
        #==================��ѯ����ƾ֤��ϸ==================================
	#=====���ǽ�  20080812  �޸�ƾ֤��ѯ����,����ƾ֤״̬Ϊ'3'�����====
        #sqlStr = "select distinct t.VOUHTYPE,t1.VOUHNAME,t.STARTNO,t.ENDNO,t.VOUHNUM FROM VOUH_REGISTER t,VOUH_PARAMETER t1 \
        #         where t.VOUHTYPE = t1.VOUHTYPE AND substr(t.BESBNO,1,6) = substr(t1.BESBNO,1,6) \
        #         AND t.TELLERNO = '" + TradeContext.sInTellerNo + "'"

        sqlStr = "select distinct t.VOUHTYPE,t1.VOUHNAME,t.STARTNO,t.ENDNO,t.VOUHNUM FROM VOUH_REGISTER t,VOUH_PARAMETER t1 \
                 where t.VOUHTYPE = t1.VOUHTYPE AND substr(t.BESBNO,1,6) = substr(t1.BESBNO,1,6) \
                 AND t.VOUHSTATUS = '3' AND t.TELLERNO = '" + TradeContext.sInTellerNo + "'"

        AfaLoggerFunc.tradeDebug(sqlStr);
        #��ѯ���ݿⲢ�����صĽ��ѹ����Ӧ������
        records = AfaDBFunc.SelectSql( sqlStr )
        if( records == None ):
            VouhFunc.tradeExit('A005067', '��ѯ[ƾ֤��]�����쳣!')
            raise AfaFlowControl.flowException( )
        elif( len( records ) == 0 ):
            VouhFunc.tradeExit('A005068', 'ƾ֤������!' )
            raise AfaFlowControl.flowException( )
        else :
            record=AfaUtilTools.ListFilterNone( records )
            total=len( records )
            
            sVouhType = ''
            sVouhName = ''
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
                sStartNo = sStartNo + strSplit + records[i][2]
                sEndNo = sEndNo + strSplit + records[i][3]
                sVouhNum = sVouhNum + strSplit + records[i][4]
                
        TradeContext.tradeResponse.append( ['sVouhType',sVouhType] )
        TradeContext.tradeResponse.append( ['sVouhName',sVouhName] )
        TradeContext.tradeResponse.append( ['sTellerNo',TradeContext.sTellerNo] )
        TradeContext.tradeResponse.append( ['sInTellerNo',TradeContext.sInTellerNo] )
        TradeContext.tradeResponse.append( ['sStartNo',sStartNo] )
        TradeContext.tradeResponse.append( ['sEndNo',sEndNo] )
        TradeContext.tradeResponse.append( ['sVouhNum',sVouhNum] )
        TradeContext.tradeResponse.append( ['sNum',str(total)] )
        TradeContext.tradeResponse.append( ['sVouhSerial',TradeContext.sVouhSerial] )
        TradeContext.tradeResponse.append( ['sLstTrxDay',TradeContext.sLstTrxDay] )
        TradeContext.tradeResponse.append( ['sLstTrxTime',TradeContext.sLstTrxTime] )
        TradeContext.tradeResponse.append( ['errorCode','0000'] )
        TradeContext.tradeResponse.append( ['errorMsg','���׳ɹ�'] )

        #�Զ����
        AfaFunc.autoPackData()

        #=============�����˳�====================
        AfaLoggerFunc.tradeInfo( 'ƾ֤��Ա����['+TradeContext.TemplateCode+']�˳�' )
    except AfaFlowControl.flowException, e:
        AfaFlowControl.exitMainFlow( )
    except AfaFlowControl.accException:
        AfaFlowControl.exitMainFlow( )
    except Exception, e:
        AfaFlowControl.exitMainFlow(str(e))

