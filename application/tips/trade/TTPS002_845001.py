# -*- coding: gbk -*-
##################################################################
#   �м�ҵ��ƽ̨.��˰���к�������.���ʽɷѽ���
#=================================================================
#   �����ļ�:   TTPS002_845001.py
#   �޸�ʱ��:   2008-5-2 16:02
##################################################################
import TradeContext, AfaLoggerFunc,Party3Context,TipsFunc,AfaFlowControl
import HostContext,HostComm,os
from types import *
from tipsConst import *

def SubModuleDoFst( ):
    try:
        AfaLoggerFunc.tradeInfo('����ɷѽ���['+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']ǰ����' )
        
        #begin 20101130 ���������� �����տ�������ƣ����ں���Ǽ���ˮ
        TradeContext.note10 = TradeContext.payeeName
        #end
        
        #=============�ж�Ӧ��״̬====================
        if not TipsFunc.ChkAppStatus( ) :
            return False
        #====��ȡ������Ϣ=======
        if not TipsFunc.ChkLiquidStatus():
            return False
            
        #TradeContext.tradeType='T' #ת���ཻ��
        if( not TradeContext.existVariable( "corpTime" ) ):
            return TipsFunc.ExitThisFlow( 'A0001', 'ί������[corpTime]ֵ������!' )
        if( not TradeContext.existVariable( "corpSerno" ) ):
            return TipsFunc.ExitThisFlow( 'A0001', '������.������ˮ��[corpSerno]ֵ������!' )
        
        #��������Ƿ����
        AfaLoggerFunc.tradeInfo('>>>��������Ƿ����')
        if (TradeContext.corpTime!=TradeContext.workDate ):
            AfaLoggerFunc.tradeInfo('�ѹ��ڣ��������ϡ����Ĺ�������:'+TradeContext.corpTime+'ϵͳ��������:'+TradeContext.workDate)
            return TipsFunc.ExitThisFlow( 'A0002', '�������ڲ���,����')

      
        #====����Ƿ�ǩԼ��=======
        if not TipsFunc.ChkCustSign():
            return False
        #====��ѯ�տ��ʺ�=======
        if not TipsFunc.SelectAcc():
            return False

        #begin 20100721 ����������
        AfaLoggerFunc.tradeInfo( '--->ԭ�к�[' + TradeContext.brno + ']' )
        #====��ѯ�������к�======
        if not QueryBrnoInfo( ):
            return False
        #end

        #====��ȡժҪ����=======
        #if not AfaFlowControl.GetSummaryCode():
        #    return False
        
        #ժҪ����
        TradeContext.summary_code = 'TIP'
        TradeContext.teller = TIPS_TELLERNO_AUTO                    #�Զ���Ա
        
        
        #ת�����(��ԪΪ��λ->�Է�Ϊ��λ)
        #AfaLoggerFunc.tradeInfo('ת��ǰ���(��ԪΪ��λ)=' + TradeContext.amount)
        #TradeContext.amount=str(long((float(TradeContext.amount))*100 + 0.1))
        #AfaLoggerFunc.tradeInfo('ת������(�Է�Ϊ��λ)=' + TradeContext.amount)
       
        #��ʼ��
        TradeContext.catrFlag = '1'         #�ֽ�ת�˱�־
        TradeContext.__agentEigen__ = '0'   #�ӱ��־
        TradeContext.tradeType = '7'        #��������
        
       
        AfaLoggerFunc.tradeInfo('�˳��ɷѽ���['+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']ǰ����' )
        return True
    except Exception, e:
        TipsFunc.exitMainFlow(str(e)) 
def SubModuledoSnd():
    try:
        return Party3Context.dn_detail
    except Exception, e:
        TipsFunc.exitMainFlow(str(e))

#20100721 ���������ӣ���ѯ�������к�
def QueryBrnoInfo():
    try:
        AfaLoggerFunc.tradeInfo( '--->�������˺�[' + TradeContext.accno + ']' )
        AfaLoggerFunc.tradeInfo( '--->�տ����˺�[' + TradeContext.payeeAcct + ']' )
        #ͨѶ�����
        HostContext.I1TRCD = '8810'                        #����������
        HostContext.I1SBNO = TIPS_SBNO_QS                  #�ý��׵ķ������
        HostContext.I1USID = TIPS_TELLERNO_AUTO            #���׹�Ա��
        HostContext.I1AUUS = ''                            #��Ȩ��Ա
        HostContext.I1AUPS = ''                            #��Ȩ��Ա����
        HostContext.I1WSNO = '10.12.5.189'                 #�ն˺�
        HostContext.I1ACNO = TradeContext.accno            #�跽�ʺ�
        HostContext.I1CYNO = '01'                          #����
        HostContext.I1CFFG = '1'                           #����У���־(0-��Ҫ,1-����Ҫ)
        HostContext.I1PSWD = ''                            #����
        HostContext.I1CETY = ''                            #ƾ֤����
        HostContext.I1CCSQ = ''                            #ƾ֤����
        HostContext.I1CTFG = ''                            #�����־

        HostTradeCode = "8810".ljust(10,' ')
        HostComm.callHostTrade( os.environ['AFAP_HOME'] + '/conf/hostconf/AH8810.map', HostTradeCode, "0002" )
        if( HostContext.host_Error ):
            AfaLoggerFunc.tradeInfo('>>>��������ʧ��=[' + str(HostContext.host_ErrorType) + ']:' +  HostContext.host_ErrorMsg)
            return TipsFunc.ExitThisFlow( '9001', HostContext.host_ErrorMsg )
        else:
            if ( HostContext.O1MGID == 'AAAAAAA' ):
                TradeContext.brno             = HostContext.O1OPNT
                AfaLoggerFunc.tradeInfo( '----->��������[' + TradeContext.brno + ']' )

            else:
                return TipsFunc.ExitThisFlow( HostContext.O1MGID, HostContext.O1INFO )

    except Exception, e:
        AfaLoggerFunc.tradeInfo(e)
        return AfaFlowControl.ExitThisFlow('9999', '�������쳣'+str(e))
    return True
