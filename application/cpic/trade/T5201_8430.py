# -*- coding: gbk -*-
##################################################################
#   �м�ҵ��ƽ̨.
#=================================================================
#   �����ļ�:   4201_8430.py
#   ����˵��:   [8430--6000112]�±���������
#   �޸�ʱ��:   2009-04-07
##################################################################
import TradeContext, AfaLoggerFunc, AfaUtilTools, AfaFunc, Party3Context,AfaAfeFunc,AfaFlowControl,AfaAhAdb
import AfaHostFunc
from types import *

def SubModuleDoFst( ):

    #begin  20091120  ������  ����
    #У�鱣�չ�˾�����ƾ֤�����Ƿ�Ϸ�
    if not AfaAhAdb.ADBCheckCert( ):
        return False
    #end

    AfaLoggerFunc.tradeInfo( '��ʼ�����ױ���' )
    #���״���
    TradeContext.tradeCode = TradeContext.TransCode
    #�û����/���յ���
    TradeContext.UserNo = TradeContext.CpicNo
    #��ַ
    if( TradeContext.existVariable( "Line" ) and len(TradeContext.Line.strip()) > 0):
        TradeContext.Address = TradeContext.Line
    #�绰
    if( TradeContext.existVariable( "DialNum" ) and len(TradeContext.DialNum.strip()) > 0):
        TradeContext.TelePhone = TradeContext.DialNum
    #�ʱ�
    if( TradeContext.existVariable( "Zip" ) and len(TradeContext.Zip.strip()) > 0):
        TradeContext.ZipCode = TradeContext.Zip
    #���֤����
    TradeContext.IdCode = TradeContext.GovtID

    #�������Ƿ�Ϊ������־
    #if( TradeContext.existVariable( "BenficType" ) ):
    #    if ( TradeContext.BenficType == "1"):
    #        TradeContext.BenficStr = "Y"
    #    else:
    #        TradeContext.BenficStr = "N"

    #AfaLoggerFunc.tradeDebug("BenficStr=[" + TradeContext.BenficStr + "]")

    #�ر�� 20091124 ���ݵ�λ�����ȡ���չ�˾��Ϣ
    AfaAhAdb.ADBGetInfoByUnitno()
    
    #����
    if( TradeContext.existVariable( "ProCode" ) ):
        if ( TradeContext.ProCode == '1'):
            #TradeContext.ProCodeStr = "EL5612"     #������B
            TradeContext.BenficStr = "N"           #��һ����������
            TradeContext.BenficName2 = "����"      #�ڶ�������-����
        elif ( TradeContext.ProCode == '2'):
            #TradeContext.ProCodeStr = "211610"     #���Ľ���������˺�����
            TradeContext.BenficStr = "Y"           #��һ����������
        else:
            TradeContext.BenficStr = ""

    AfaLoggerFunc.tradeDebug("BenficStr=[" + TradeContext.BenficStr + "]")
            

    return True
def SubModuleDoSnd():
    AfaLoggerFunc.tradeInfo('�����ѯ����[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']�������ͨѶ����' )
    try:
        Party3Context.unitno      = TradeContext.unitno
        Party3Context.ProCode = TradeContext.ProCode
        names = Party3Context.getNames( )
        for name in names:
            value = getattr( Party3Context, name )
            setattr( TradeContext, name, value )
            #AfaLoggerFunc.tradeInfo("�ֶ�����  ["+str(name)+"] =  "+str(value))
        if( TradeContext.errorCode == '0000' ):
        #    if( TradeContext.existVariable( "ProCodeStr" ) ):
        #        if (TradeContext.ProCodeStr == "EL5601"):            
        #            TradeContext.ProCode = "0"                      #������A
        #        elif (TradeContext.ProCodeStr == "EL5602"):
        #            TradeContext.ProCode = "1"                      #������B
        #        elif (TradeContext.ProCodeStr == "211610"):
        #            TradeContext.ProCode = "2"                      #���Ľ���������˺�����
            if not AfaAhAdb.AdbInsertQueDtl( ):
                raise AfaFlowControl.accException()
        AfaLoggerFunc.tradeInfo('�˳���ѯ�����������ͨѶ����' )
        return True
        
    except AfaFlowControl.flowException, e:
        AfaFlowControl.exitMainFlow( str(e) )
        
    except AfaFlowControl.accException:
        AfaFlowControl.exitMainFlow( )
        
    except Exception, e:
        AfaFlowControl.exitMainFlow(str(e))
