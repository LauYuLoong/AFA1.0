# -*- coding: gbk -*-
###################################################################
#    ��    ��:    Tvouh007.py
#    ˵    ��:    ƾ֤����-->ƾ֤�Ͻ�
#    ��    ��:    �м�ҵ����ƽ̨��AFA��--- UNIX: AIX 5.3
#    ��    ��:    ���ǽ�
#    ��    ˾:    ������ͬ�Ƽ�
#    ������ַ:    ����
#    ����ʱ��:    2008��6��11�� 
#    ά����¼:   
##################################################################
import TradeContext,  AfaUtilTools, AfaFunc, AfaFlowControl, AfaDBFunc
from types import *
import AfaLoggerFunc,VouhFunc,HostContext,VouhHostFunc

def main( ):
    AfaLoggerFunc.tradeInfo( 'ƾ֤�Ͻ����['+TradeContext.TemplateCode+']����' )

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
        #=====================��ȡ��������===============================
        #TradeContext.sBesbSty = VouhFunc.SelectBesbSty(TradeContext.sBesbNo)
        
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
        
        #=============��ȡ���ù�Աβ���===============================
        HostContext.I1SBNO = TradeContext.sBesbNo           #������  �������ͽ��׻����� 
        #HostContext.I1USID = TradeContext.sInTellerNo      #��Ա��
        HostContext.I1USID = '999996'                       #��Ա��  ��Ա�����Զ���Ա
        HostContext.I1WSNO = TradeContext.sWSNO             #�ն˺�
        HostContext.I1EDDT = TradeContext.sLstTrxDay        #��ֹ����
        HostContext.I1TELR = TradeContext.sInTellerNo       #��Ա����
        
        if(not VouhHostFunc.CommHost('0104')):
            VouhFunc.tradeExit( TradeContext.errorCode, TradeContext.errorMsg )
            raise AfaFlowControl.flowException( )
        if(TradeContext.errorCode == '0000'):
            TradeContext.sInTellerTailNobak = HostContext.O2CABO
            TradeContext.sInTellerTailNo    = TradeContext.sInTellerTailNobak[0]                 
            AfaLoggerFunc.tradeInfo( '���ù�Աβ��ţ�' + TradeContext.sInTellerTailNo ) 
        #end 
        
        #=============��ʼ�����ر��ı���========================
        TradeContext.tradeResponse = []
        TradeContext.sRivTeller = TradeContext.sInTellerTailNo

        #=============��ƾ֤����״̬�������־====================
        TradeContext.sExDepos  = '4' #ԭ�����־   1.���й���� 2.֧�й���� 3.�������� 4.��Աƾ֤��
        if(SBNO=='31' or SBNO=='40' or SBNO=='32'):
            TradeContext.sDepository = '2' #�����־
        elif(SBNO=='50'):
            TradeContext.sDepository = '3' #�����־
        else:
            VouhFunc.tradeExit('A005061', '�û�����Ա���ܽ��д˲���!')
            raise AfaFlowControl.flowException( )
        
        TradeContext.sVouhStatus  = '2' #״̬       2.�ѷ�δ��3.����δ��     
        TradeContext.sExStatus    = '3' #ԭ״̬     3.����δ��ʱ������ƾ֤�Ͻɣ��Ͻɺ�Ϊ2.�ѷ�δ��
        TradeContext.sTransType    = 'ƾ֤�Ͻ�'
        TradeContext.sInBesbNo    = TradeContext.sBesbNo
        
        tellerNo = TradeContext.sTellerTailNo
        TradeContext.sTellerTailNo = TradeContext.sInTellerTailNo
        TradeContext.sInTellerTailNo = tellerNo
        
        if(SBNO <> '31' and SBNO <> '32' and SBNO <> '40' and SBNO <> '50' ):
            tradeExit( 'A0001', '�û�����Ա���ܽ��д˲���!' )
            raise AfaFlowControl.flowException( )

        #���׹�������    
        VouhFunc.VouhTrans()

        #����ƾ֤����ǼǱ�
        VouhFunc.VouhModify()
       
        #���ݿ��ύ
        AfaDBFunc.CommitSql( )
        
        TradeContext.sInTellerTailNo = TradeContext.sTellerTailNo
        TradeContext.sTellerTailNo = tellerNo
        
        #��������
        AfaLoggerFunc.tradeInfo( '------------��������' )
        TradeContext.sOperSty = '3'
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
            
            tmpBesbNo = TradeContext.sInBesbNo
            TradeContext.sInBesbNo = TradeContext.sBesbNo
            TradeContext.sBesbNo = tmpBesbNo

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
        AfaLoggerFunc.tradeInfo( 'ƾ֤�Ͻ�['+TradeContext.TemplateCode+']�˳�' )
    except AfaFlowControl.flowException, e:
        AfaFlowControl.exitMainFlow( )
    except AfaFlowControl.accException:
        AfaFlowControl.exitMainFlow( )
    except Exception, e:
        AfaFlowControl.exitMainFlow(str(e))

