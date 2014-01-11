# -*- coding: gbk -*-
##################################################################
#   �м�ҵ��ƽ̨.
#=================================================================
#   �����ļ�:   TZJYW0001_8650.py
#   ����˵��:   [��ѯ�м�ҵ����ˮ��]
#   ԭ �� �ߣ�  LLJ
#   �޸�ʱ��:   2012��6��
##################################################################
import TradeContext, AfaLoggerFunc, AfaUtilTools, AfaFunc, Party3Context,AfaAfeFunc,AfaFlowControl,AfaDBFunc
import AfaHostFunc
from types import *
        
def TrxMain():
    AfaLoggerFunc.tradeInfo('��ѯ�м�ҵ����ˮ��[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']����' )
    
    try:
        
        #ֻ��ѯ����δ���˵��ѳɹ�������
        sql = ""
        sql = sql + "select AGENTSERIALNO from afa_maintransdtl where "
        sql = sql + " workdate = '" + TradeContext.workdate + "'"
        sql = sql + " and  bankstatus    = '0' and corpstatus = '0' and revtranf = '0' and chkflag='9'and corpchkflag='9'"
        
        #������������ͨҵ��
        if((TradeContext.sysId =='AG2011' or TradeContext.sysId =='AG2013') and  TradeContext.existVariable( "printNo" ) and len(TradeContext.printNo.strip()) > 0  ):
            if ( not (TradeContext.existVariable( "unitno" ) and len(TradeContext.unitno.strip()) > 0) ):
                TradeContext.errorCode,TradeContext.errorMsg = '0001', "��ѯ�������㣬��������ȷ�ĵ�λ���"
                raise AfaFlowControl.flowException( )
                
            sql = sql + " and sysid = '" + TradeContext.sysId+ "'"           
            sql = sql + " and  unitno  = '" + TradeContext.unitno + "'"  
            sql = sql + " and  userno  = '" + TradeContext.printNo.strip() + "'"        #����ӡˢ��
            
            
        #���ս���ҵ��    
        if(TradeContext.sysId =='AG2017' and TradeContext.existVariable( "punishNo" ) and len(TradeContext.punishNo.strip()) > 0):
            sql = sql + " and sysid = '" + TradeContext.sysId+ "'"
            sql = sql + " and  unitno  = '0001'"                                        #0001
            sql = sql + " and  userno  = '" + TradeContext.punishNo.strip() + "'"       #������������
            
        #��������
        if(TradeContext.sysId =='AG2018'and TradeContext.existVariable( "userno" ) and len(TradeContext.userno.strip()) > 0):
            
            sql = sql + " and sysid = '" + TradeContext.sysId + "'"
            sql = sql + " and  unitno  = '00000001'"                                    #00000001
            sql = sql + " and  userno  = '" + TradeContext.userno.strip() + "'"         #�û����
            
        if(TradeContext.existVariable( "bankserno" ) and len(TradeContext.bankserno.strip()) > 0):
            
            sql = sql + " and  bankserno  = '" + TradeContext.bankserno.strip() + "'"    #������ˮ��            
        
        AfaLoggerFunc.tradeInfo('��ѯ�м�ҵ����ˮ�ţ�'+ sql)
        
        results = AfaDBFunc.SelectSql( sql )
        
        if results == None:
            TradeContext.errorCode,TradeContext.errorMsg = "0001" ,"��ѯ�м�ҵ����ˮ���쳣"
            return False
        
        if(len(results) == 0):
            TradeContext.errorCode,TradeContext.errorMsg = "0001","�޴˽���,��ѯ�м�ҵ����ˮ��ʧ��"
            return False
            
        else:
            TradeContext.agentSerialno  = results[0][0]                        #�м�ҵ����ˮ��
            AfaLoggerFunc.tradeInfo(TradeContext.agentSerialno)       
            
        TradeContext.errorCode,TradeContext.errorMsg = '0000', "���׳ɹ�"
        AfaLoggerFunc.tradeInfo('�м�ҵ����ˮ�Ų�ѯ����[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']�˳�' )
        return True
    
    except Exception, e:
        AfaFlowControl.exitMainFlow(str(e))
