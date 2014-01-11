# -*- coding: gbk -*-
###################################################################
#    ��    ��:    Tvouh003.py
#    ˵    ��:    ƾ֤����-->ƾ֤����
#    ��    ��:    �м�ҵ����ƽ̨��AFA��--- UNIX: AIX 5.3
#    ��    ��:    ���ǽ�
#    ��    ˾:    ������ͬ�Ƽ�
#    ������ַ:    ����
#    ����ʱ��:    2008��6��4��
#    ά����¼:
##################################################################
import TradeContext, AfaLoggerFunc, AfaUtilTools, AfaFunc, AfaFlowControl, AfaDBFunc
from types import *
import VouhFunc,HostContext,VouhHostFunc

def main( ):
    AfaLoggerFunc.tradeInfo( 'ƾ֤����['+TradeContext.TemplateCode+']����' )
    
    
    #=============ǰ̨��������===================================
    #TradeContext.sBesbNo                                 ������
    #TradeContext.sBesbSty                                ��������
    #TradeContext.sCur                                    ���Ҵ���
    #TradeContext.sTellerNo                               ��Ա��
    #TradeContext.sVouhType                               ƾ֤����
    #TradeContext.sInBesbNo                               ���û�����
    #TradeContext.sInBesbSty                              ���û�������
    #TradeContext.sInTellerNo                             ���ù�Ա��
    #TradeContext.sStartNo                                ��ʼ����
    #TradeContext.sEndNo                                  ��ֹ����
    #TradeContext.sRivTeller                              �Է���Ա
    #TradeContext.sVouhStatus                             ƾ֤״̬
    #TradeContext.sVouhNum                                ƾ֤����
    #TradeContext.sLstTrxDay                              ���������
    #TradeContext.sLstTrxTime                             �����ʱ��
    #TradeContext.sDepository                             �����־

    try:
        #=============��ȡ��ǰϵͳʱ��==========================
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
            AfaLoggerFunc.tradeInfo( '���׻�������' )
            AfaLoggerFunc.tradeInfo( SBNO )
            
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
        
        #=============��ȡ���û�������==========================
        HostContext.I1OTSB = TradeContext.sInBesbNo       #���û�����
        HostContext.I1SBNO = TradeContext.sInBesbNo       #������
        HostContext.I1USID = TradeContext.sTellerNo       #��Ա��
        HostContext.I1WSNO = TradeContext.sWSNO           #�ն˺�
        if(not VouhHostFunc.CommHost('2001')):
            return VouhFunc.ExitThisFlow( TradeContext.errorCode, TradeContext.errorMsg )
        if(TradeContext.errorCode == '0000'):
            INSBNO = HostContext.O1SBCH
            AfaLoggerFunc.tradeInfo( '���û�������' )
            AfaLoggerFunc.tradeInfo( INSBNO )
            
        #beginƾ֤�Ż�����201109  
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
        TradeContext.sRivTeller = TradeContext.sInTellerTailNo
        
        #=============������ˮ��========================
        TradeContext.sVouhSerial = VouhFunc.GetVouhSerial( )
        
        #=============�������=============================================================
        #31������������ 32����Ӫҵ�� 33������� 40������/֧�� 50����/����/������
        #1.���й���� 2.֧�й���� 3.�������� 4.��Աƾ֤��
        if(SBNO=='33'):
            TradeContext.sExDepos     = '1' #ԭ�����־
        elif(SBNO=='31' or SBNO=='40' or SBNO=='32' or SBNO=='41'):
            TradeContext.sExDepos     = '2' #ԭ�����־
        elif(SBNO=='50'):
            TradeContext.sExDepos     = '3' #ԭ�����־
        else:
            VouhFunc.tradeExit('A005061', '�û�����Ա���ܽ��д˲���!')
            raise AfaFlowControl.flowException( )
        
        if(INSBNO=='33'):
            TradeContext.sDepository     = '1' #�����־
        elif(INSBNO=='31' or INSBNO=='40' or INSBNO=='32' or INSBNO=='41'):
            TradeContext.sDepository     = '2' #�����־
        elif(INSBNO=='50'):
            TradeContext.sDepository     = '3' #�����־
        else:
            VouhFunc.tradeExit('A005061', '�û�����Ա���ܽ��д˲���!')
            raise AfaFlowControl.flowException( )
            
        if(INSBNO=='33'): 
            TradeContext.sVouhStatus  = '0' #״̬       0.����δ��  2.�ѷ�δ��
            TradeContext.sExStatus    = '2' #ԭ״̬
        elif(SBNO=='33'):
            TradeContext.sVouhStatus  = '2' #״̬       0.����δ��  2.�ѷ�δ��
            TradeContext.sExStatus    = '0' #ԭ״̬
        else:
            TradeContext.sVouhStatus  = '2' #״̬       0.����δ��  2.�ѷ�δ��
            TradeContext.sExStatus    = '2' #ԭ״̬
            
        
        TradeContext.sTransType    = 'ƾ֤����'
        
        #================�ж��Ƿ������������===================================================
        if((SBNO =='33' and INSBNO=='50') or 
           (SBNO =='50' and INSBNO=='33') or
           (SBNO =='31' and INSBNO=='50') or
           (SBNO =='50' and INSBNO=='31') or
           (SBNO =='50' and INSBNO=='50') or
           (SBNO =='32' and INSBNO=='32') or
           (SBNO =='31' and INSBNO=='31') or
           (SBNO =='41' and INSBNO=='41') or
           (SBNO =='40' and INSBNO=='40')):
            VouhFunc.tradeExit('A005061', '�û�����Ա���ܽ��д˲���!')
            raise AfaFlowControl.flowException( )
            
        #================�ж��Ƿ�ͬ������===================================================
        if((SBNO =='31' and INSBNO=='40') or 
           (SBNO =='40' and INSBNO=='31') or
           (SBNO =='31' and INSBNO=='32') or
           (SBNO =='32' and INSBNO=='31') or
           (SBNO =='40' and INSBNO=='32') or
           (SBNO =='32' and INSBNO=='40') or
           (SBNO =='41' and INSBNO=='32') or
           (SBNO =='41' and INSBNO=='31') or
           (SBNO =='32' and INSBNO=='41') or
           (SBNO =='31' and INSBNO=='41')):
            VouhFunc.tradeExit('A005061', '�û�����Ա���ܽ��д˲���!')
            raise AfaFlowControl.flowException( )
            
        #================�ж����û����������ϼ��Ƿ��ǵ���ƾ֤�Ļ�����=========================
        if((SBNO =='40' and INSBNO=='50') or
           (SBNO =='32' and INSBNO=='50') or
           (SBNO =='41' and INSBNO=='50')):
            if(TradeContext.sBesbNo <> VouhFunc.SelectSBTPAC(TradeContext.sInBesbNo)):
                VouhFunc.tradeExit('A005061', '�û�����Ա���ܽ��д˲���!')
                raise AfaFlowControl.flowException( )
        
        #================�����ŵ������ϼ��Ƿ������û�����=====================================
        if((SBNO =='50' and INSBNO=='40') or
            (SBNO =='50' and INSBNO=='32') or
            (SBNO =='50' and INSBNO=='41')):
            if(TradeContext.sInBesbNo <> VouhFunc.SelectSBTPAC(TradeContext.sBesbNo)):
                VouhFunc.tradeExit('A005061', '�û�����Ա���ܽ��д˲���!')
                raise AfaFlowControl.flowException( )
                
        if((TradeContext.sBesbNo)[:6] <> (TradeContext.sInBesbNo)[:6]):
            VouhFunc.tradeExit('A005061', '�û�����Ա���ܽ��д˲���!')
            raise AfaFlowControl.flowException( )
            
        #���׹�������    
        AfaLoggerFunc.tradeInfo( TradeContext.sExDepos )
        VouhFunc.VouhTrans()

        #����ƾ֤����ǼǱ�
        VouhFunc.VouhModify()
        
        #���ݿ��ύ
        AfaDBFunc.CommitSql( )
        
        #��������
        AfaLoggerFunc.tradeInfo( '------------��������' )
        TradeContext.sOperSty = '2'
        VouhHostFunc.VouhCommHost()
        TradeContext.sTranStatus = '0'
        AfaLoggerFunc.tradeInfo( '=======================12'+TradeContext.errorCode )
        
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
            
            tmpTeller = TradeContext.sInTellerTailNo
            TradeContext.sInTellerTailNo = TradeContext.sTellerTailNo
            TradeContext.sTellerTailNo = tmpTeller
            
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

        #=============�����˳�=========================================
        AfaLoggerFunc.tradeInfo( 'ƾ֤����['+TradeContext.TemplateCode+']�˳�' )
    except AfaFlowControl.flowException, e:
        AfaFlowControl.exitMainFlow( )
    except AfaFlowControl.accException:
        AfaFlowControl.exitMainFlow( )
    except Exception, e:
        AfaFlowControl.exitMainFlow(str(e))
