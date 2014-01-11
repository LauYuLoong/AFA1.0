# -*- coding: gbk -*-
###################################################################
#    ��    ��:    Tvouh005.py
#    ˵    ��:    ƾ֤����-->ƾ֤���⳷��
#    ��    ��:    �м�ҵ����ƽ̨��AFA��--- UNIX: AIX 5.3
#    ��    ��:    ���ǽ�
#    ��    ˾:    ������ͬ�Ƽ�
#    ������ַ:    ����
#    ����ʱ��:    2008��6��11�� 
#    ά����¼:   
##################################################################
import TradeContext, AfaLoggerFunc, AfaUtilTools, AfaFunc, AfaFlowControl, AfaDBFunc, VouhHostFunc
from types import *
import VouhFunc,HostContext

def main( ):
    AfaLoggerFunc.tradeInfo( 'ƾ֤���⳷��['+TradeContext.TemplateCode+']����' )

    #=============ǰ̨��������===================================
    #TradeContext.sBesbNo                                 ������
    #TradeContext.sBesbSty                                ��������
    #TradeContext.sCur                                    ���Ҵ���
    #TradeContext.sTellerNo                               ��Ա��
    #TradeContext.sVouhType                               ƾ֤����
    #TradeContext.sStartNo                                ��ʼ����
    #TradeContext.sEndNo                                  ��ֹ����
    #TradeContext.sRivTeller                              �Է���Ա
    #TradeContext.sVouhStatus                             ƾ֤״̬
    #TradeContext.sVouhNum                                ƾ֤����
    #TradeContext.sLstTrxDay                              ���������
    #TradeContext.sLstTrxTime                             �����ʱ��
    #TradeContext.sDepository                             �����־
    #TradeContext.sVouhName                               ƾ֤����

    try:
        #================���========================
        TradeContext.sVouhType = VouhFunc.DelSpace(TradeContext.sVouhType.split("|"))
        TradeContext.sVouhName = VouhFunc.DelSpace(TradeContext.sVouhName.split("|"))
        TradeContext.sStartNo  = VouhFunc.DelSpace(TradeContext.sStartNo.split("|"))
        TradeContext.sEndNo    = VouhFunc.DelSpace(TradeContext.sEndNo.split("|"))
        TradeContext.sVouhNum  = VouhFunc.DelSpace(TradeContext.sVouhNum.split("|"))
        TradeContext.sNum      = len(TradeContext.sVouhType)
        
        #==================�ݴ�==================================
        TradeContext.rVouhType = VouhFunc.AddSplit(TradeContext.sVouhType)
        TradeContext.rVouhName = VouhFunc.AddSplit(TradeContext.sVouhName)
        TradeContext.rStartNo  = VouhFunc.AddSplit(TradeContext.sStartNo)
        TradeContext.rEndNo    = VouhFunc.AddSplit(TradeContext.sEndNo)
        TradeContext.rVouhNum  = VouhFunc.AddSplit(TradeContext.sVouhNum)
    
        #=============��ʼ�����ر��ı���========================
        TradeContext.tradeResponse = []
        
        #=============������ˮ��========================
        TradeContext.sVouhSerial = VouhFunc.GetVouhSerial( )

        #=============��ȡ��ǰϵͳʱ��==========================
        TradeContext.sLstTrxDay  = AfaUtilTools.GetSysDate( )
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

        #=============��ƾ֤����״̬�������־====================
        TradeContext.sDepository  = '1' #�����־   1.���й���� 2.֧�й���� 3.�������� 4.��Աƾ֤��
        TradeContext.sExDepos     = ' ' #ԭ�����־
        TradeContext.sVouhStatus  = '0' #״̬       0.����δ�� 1.�ѳ���
        TradeContext.sExStatus    = '1' #ԭ״̬
        TradeContext.sRivTeller   = '   '     #�Է���Ա
        TradeContext.sTransType    = 'ƾ֤���⳷��'
        TradeContext.sInTellerTailNo  = TradeContext.sTellerTailNo
        TradeContext.sInBesbNo    = TradeContext.sBesbNo
        

        #���׹�������    
        VouhFunc.VouhTrans()

        #����ƾ֤����ǼǱ�
        VouhFunc.VouhModify()
        
        #���ݿ��ύ
        AfaDBFunc.CommitSql( )
        
        #��������
        AfaLoggerFunc.tradeInfo( '------------��������' )
        TradeContext.sOperSty = '0'
        VouhHostFunc.VouhCommHost()
        TradeContext.sTranStatus = '0'
        AfaLoggerFunc.tradeInfo( '=======================12'+TradeContext.errorCode )
        #TradeContext.errorCode = '0000'
        if(TradeContext.errorCode <> '0000'):
            tmpErrorCode= TradeContext.errorCode
            tmpErrorMsg = TradeContext.errorMsg
        
            #����
            
            #=============��ƾ֤����״̬�������־====================
            tmpDepos = TradeContext.sDepository
            TradeContext.sDepository = TradeContext.sExDepos
            TradeContext.sExDepos = tmpDepos

            tmpStatus = TradeContext.sVouhStatus
            TradeContext.sVouhStatus = TradeContext.sExStatus
            TradeContext.sExStatus = tmpStatus

            TradeContext.sRivTeller   = '   '     #�Է���Ա
            TradeContext.sTransType    = '����'
            

            #���׹�������    
            VouhFunc.VouhTrans()
            AfaDBFunc.CommitSql( )
            
            TradeContext.sTranStatus = '1'
            if(not TradeContext.existVariable( "HostSerno" )):
                TradeContext.HostSerno = ''    
            
            #������ˮ��
            VouhFunc.ModifyVouhModify()
            
            AfaLoggerFunc.tradeInfo( '============================�Զ�������' )

            
            VouhFunc.tradeExit(tmpErrorCode, tmpErrorMsg)
            raise AfaFlowControl.flowException( )
        
        #������ˮ��
        VouhFunc.ModifyVouhModify() 
        
        TradeContext.tradeResponse.append( ['sVouhSerial',TradeContext.sVouhSerial] )
        TradeContext.tradeResponse.append( ['sVouhType',TradeContext.rVouhType] )
        TradeContext.tradeResponse.append( ['sVouhName',TradeContext.rVouhName] )
        TradeContext.tradeResponse.append( ['sStartNo',TradeContext.rStartNo] )
        TradeContext.tradeResponse.append( ['sEndNo',TradeContext.rEndNo] )
        TradeContext.tradeResponse.append( ['sVouhNum',TradeContext.rVouhNum] )
        TradeContext.tradeResponse.append( ['sLstTrxDay',TradeContext.sLstTrxDay] )
        TradeContext.tradeResponse.append( ['sLstTrxTime',TradeContext.sLstTrxTime] )
        TradeContext.tradeResponse.append( ['sNum',str(TradeContext.sNum)] )
        TradeContext.tradeResponse.append( ['errorCode','0000'] )
        TradeContext.tradeResponse.append( ['errorMsg','���׳ɹ�'] )

        #�Զ����
        AfaFunc.autoPackData()

        #=============�����˳�====================
        AfaLoggerFunc.tradeInfo( 'ƾ֤���⳷��['+TradeContext.TemplateCode+']�˳�' )
    except AfaFlowControl.flowException, e:
        AfaFlowControl.exitMainFlow( )
    except AfaFlowControl.accException:
        AfaFlowControl.exitMainFlow( )
    except Exception, e:
        AfaFlowControl.exitMainFlow(str(e))

