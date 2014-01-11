# -*- coding: gbk -*-
##################################################################
#   ��˰���к�������.��ѯά����ģ��.
#=================================================================
#   �����ļ�:   TPS001.py
#   �޸�ʱ��:   2008-5-2 10:24 
##################################################################
import TradeContext, AfaLoggerFunc, UtilTools, TipsFunc
from types import *

def main( ):
    AfaLoggerFunc.tradeInfo('==========�����ѯά����ģ��['+TradeContext.TemplateCode+']==========')
    try:
        #=============��ʼ�����ر��ı���====================
        TradeContext.tradeResponse=[]
        
        #=============��ȡ��ǰϵͳʱ��====================
        AfaLoggerFunc.tradeInfo('>>>��ȡ��ǰϵͳʱ��')
        if not (TradeContext.existVariable( "workDate" ) and len(TradeContext.workDate)>0):
            TradeContext.workDate = UtilTools.GetSysDate( )
        TradeContext.workTime=UtilTools.GetSysTime( )
        TradeContext.sysId      ='AG2010'
        TradeContext.busiNo     ='00000000000001'
        
        #��ʹ��ת��������
        TradeContext.__respFlag__="0"
    
        #=============����ӿ�1====================
        subModuleExistFlag=0
        subModuleName = 'T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode
        try:
            subModuleHandle=__import__( subModuleName )
        except Exception, e:
            AfaLoggerFunc.tradeInfo( e)
        else:
            AfaLoggerFunc.tradeInfo( 'ִ��['+subModuleName+']ģ��' )
            subModuleExistFlag=1
            if not subModuleHandle.SubModuleMainFst( ) :
                raise TipsFunc.flowException( )

        #=============�Զ����====================
        TipsFunc.autoPackData()

        AfaLoggerFunc.tradeInfo('==========�˳���ѯά����ģ��['+TradeContext.TemplateCode+']==========')
        
    except TipsFunc.flowException, e:
        TipsFunc.exitMainFlow( )
        
    except Exception, e:
        TipsFunc.exitMainFlow(str(e))
