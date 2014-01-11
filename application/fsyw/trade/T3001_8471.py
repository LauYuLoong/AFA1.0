# -*- coding: gbk -*-
##################################################################
#   ���մ���ƽ̨.���ղ�ѯ����
#=================================================================
#   �����ļ�:   T3001_8471.py
#   �޸�ʱ��:   2007-10-21
##################################################################
import TradeContext, AfaDBFunc, AfaLoggerFunc,AfaFlowControl
from types import *

def SubModuleMainFst( ):

    AfaLoggerFunc.tradeInfo('>>>��˰��������')
    if TradeContext.opflg=='0': 
        AfaLoggerFunc.tradeInfo('>>>����')
        if not Insert():
            return False
    elif TradeContext.opflg=='1': 
        AfaLoggerFunc.tradeInfo('>>>�޸�')
        if not Update():
            return False
    elif TradeContext.opflg=='2': 
        AfaLoggerFunc.tradeInfo('>>>ɾ��')
        if not Delete():
            return False
    else:
        return AfaFlowControl.ExitThisFlow('0001', 'δ����ò�������')    

    TradeContext.errorCode='0000'
    TradeContext.errorMsg='���״���ɹ�'
    return True


    
#����
def Insert():
    AfaLoggerFunc.tradeInfo( '********************�������ݱ�ʼ*******************' )
    try:
        if( TradeContext.existVariable( "busiNo" ) and len(TradeContext.busiNo)<=0):
            return AfaFlowControl.ExitThisFlow( 'A0027', '[��λ����]:����Ϊ��')
        if( TradeContext.existVariable( "hostIp" ) and len(TradeContext.hostIp)<=0):
            return AfaFlowControl.ExitThisFlow( 'A0027', '[������ַ]:����Ϊ��')
        if( TradeContext.existVariable( "upUser" ) and len(TradeContext.upUser)<=0):
            return AfaFlowControl.ExitThisFlow( 'A0027', '[�ϴ��û�]:����Ϊ��')
        if( TradeContext.existVariable( "upPwd" ) and len(TradeContext.upPwd)<=0):
            return AfaFlowControl.ExitThisFlow( 'A0027', '[�ϴ�����]:����Ϊ��')
        if( TradeContext.existVariable( "downUser" ) and len(TradeContext.downUser)<=0):
            return AfaFlowControl.ExitThisFlow( 'A0027', '[�����û�]:����Ϊ��')
        if( TradeContext.existVariable( "downPwd" ) and len(TradeContext.downPwd)<=0):
            return AfaFlowControl.ExitThisFlow( 'A0027', '[��������]:����Ϊ��')
        if( TradeContext.existVariable( "accDate" ) and len(TradeContext.accDate)<=0):
            return AfaFlowControl.ExitThisFlow( 'A0027', '[�������]:����Ϊ��')
        if( TradeContext.existVariable( "remain" ) and len(TradeContext.remain)<=0):
            return AfaFlowControl.ExitThisFlow( 'A0027', '[��������]:����Ϊ��')
        
        sqlstr      =   "insert into fs_businoconf(BUSINO,HOSTIP,UPUSER,UPPASSWD,UPLDIR,DOWNUSER,DOWNPASSWD,DOWNLDIR,UPRDIR,DOWNRDIR) values("
        sqlstr1     =   sqlstr
        sqlstr1     =   sqlstr1 + "'" + TradeContext.busiNo             + "',"
        sqlstr1     =   sqlstr1 + "'" + TradeContext.hostIp             + "',"
        sqlstr1     =   sqlstr1 + "'" + TradeContext.upUser             + "',"
        sqlstr1     =   sqlstr1 + "'" + TradeContext.upPwd              + "',"
        sqlstr1     =   sqlstr1 + "'/home/maps/afa/data/ahfs',"
        sqlstr1     =   sqlstr1 + "'" + TradeContext.downUser           + "',"
        sqlstr1     =   sqlstr1 + "'" + TradeContext.downPwd            + "',"
        sqlstr1     =   sqlstr1 + "'/home/maps/afa/data/ahfs',' ',' ')"
        
        
        AfaLoggerFunc.tradeInfo(sqlstr1)
        records = AfaDBFunc.InsertSqlCmt(sqlstr1)
        if( records == None or records <=0  ):
            AfaLoggerFunc.tradeFatal(sqlstr1)
            return AfaFlowControl.ExitThisFlow( 'A0002', '���ݿ�����쳣:'+AfaDBFunc.sqlErrMsg )            
        
        
        
        sqlstr      =   "insert into fs_remain(busino,date,this) values("
        sqlstr2     =   sqlstr
        sqlstr2     =   sqlstr2 + "'" + TradeContext.busiNo               + "',"
        sqlstr2     =   sqlstr2 + "'" + TradeContext.accDate              + "',"
        sqlstr2     =   sqlstr2 + "'" + TradeContext.remain               + "')"
        
        AfaLoggerFunc.tradeInfo(sqlstr2)
        records = AfaDBFunc.InsertSqlCmt(sqlstr2)
        if( records == None or records <=0  ):
            AfaLoggerFunc.tradeFatal(sqlstr2)
            return AfaFlowControl.ExitThisFlow( 'A0002', '���ݿ�����쳣:'+AfaDBFunc.sqlErrMsg )
        AfaLoggerFunc.tradeInfo( '********************�������ݱ����*******************' )
        return True
    
    except Exception, e:
        AfaLoggerFunc.tradeInfo(e)
        return AfaFlowControl.ExitThisFlow('9999', '�������쳣'+str(e))
        


#�޸�
def Update():
    AfaLoggerFunc.tradeInfo( '********************�޸����ݱ�ʼ*******************' )
    try:
        if( TradeContext.existVariable( "busiNo" ) and len(TradeContext.busiNo)<=0):
            return AfaFlowControl.ExitThisFlow( 'A0027', '[��λ����]:����Ϊ��')
        if( TradeContext.existVariable( "hostIp" ) and len(TradeContext.hostIp)<=0):
            return AfaFlowControl.ExitThisFlow( 'A0027', '[������ַ]:����Ϊ��')
        if( TradeContext.existVariable( "upUser" ) and len(TradeContext.upUser)<=0):
            return AfaFlowControl.ExitThisFlow( 'A0027', '[�ϴ��û�]:����Ϊ��')
        if( TradeContext.existVariable( "upPwd" ) and len(TradeContext.upPwd)<=0):
            return AfaFlowControl.ExitThisFlow( 'A0027', '[�ϴ�����]:����Ϊ��')
        if( TradeContext.existVariable( "downUser" ) and len(TradeContext.downUser)<=0):
            return AfaFlowControl.ExitThisFlow( 'A0027', '[�����û�]:����Ϊ��')
        if( TradeContext.existVariable( "downPwd" ) and len(TradeContext.downPwd)<=0):
            return AfaFlowControl.ExitThisFlow( 'A0027', '[��������]:����Ϊ��')
        if( TradeContext.existVariable( "accDate" ) and len(TradeContext.accDate)<=0):
            return AfaFlowControl.ExitThisFlow( 'A0027', '[�������]:����Ϊ��')
        if( TradeContext.existVariable( "remain" ) and len(TradeContext.remain)<=0):
            return AfaFlowControl.ExitThisFlow( 'A0027', '[��������]:����Ϊ��')
        sqlstr="UPDATE fs_businoconf SET "
        sqlstr1=   sqlstr
        sqlstr1=sqlstr1+"hostIp='"+ TradeContext.hostIp+"',"
        sqlstr1=sqlstr1+"upUser='"+ TradeContext.upUser+"',"
        sqlstr1=sqlstr1+"upPasswd='"+ TradeContext.upPwd+"',"
        sqlstr1=sqlstr1+"downUser='"+ TradeContext.downUser+"',"
        sqlstr1=sqlstr1+"downPasswd='"+ TradeContext.downPwd+"'"
        sqlstr1=sqlstr1+" WHERE "
        sqlstr1=sqlstr1+"busiNo = '"+ TradeContext.busiNo+"'"
                
        AfaLoggerFunc.tradeInfo(sqlstr1)
        records = AfaDBFunc.UpdateSqlCmt(sqlstr1)
                 
        if( records <=0  ):
            AfaLoggerFunc.tradeFatal(sqlstr1)
            return AfaFlowControl.ExitThisFlow( 'A0027', 'δ������Ϣ:'+AfaDBFunc.sqlErrMsg )
        if( records == None ):
            AfaLoggerFunc.tradeFatal(sqlstr1)
            return AfaFlowControl.ExitThisFlow( 'A0002', '���ݿ�����쳣:'+AfaDBFunc.sqlErrMsg )
        
        
        sqlstr="UPDATE fs_remain SET "
        sqlstr2=   sqlstr
        sqlstr2=sqlstr2+"date='"+ TradeContext.accDate+"',"
        sqlstr2=sqlstr2+"this='"+ TradeContext.remain+"'"
        sqlstr2=sqlstr2+" WHERE "
        sqlstr2=sqlstr2+"busiNo = '"+ TradeContext.busiNo+"'"
        
        AfaLoggerFunc.tradeInfo(sqlstr2)
        records = AfaDBFunc.UpdateSqlCmt(sqlstr2)
        
        if( records == None or records <=0  ):
            AfaLoggerFunc.tradeFatal(sqlstr2)
            return AfaFlowControl.ExitThisFlow( 'A0002', '���ݿ�����쳣:'+AfaDBFunc.sqlErrMsg )
        AfaLoggerFunc.tradeInfo( '********************�޸����ݱ����*******************' )
        return True
        
    except Exception, e:
        AfaLoggerFunc.tradeInfo(e)
        return AfaFlowControl.ExitThisFlow('9999', '�������쳣'+str(e))
        
        
#ɾ��
def Delete():
    try:
        if( TradeContext.existVariable( "busiNo" ) and len(TradeContext.busiNo)<=0):
            return AfaFlowControl.ExitThisFlow( 'A0027', '[��λ����]:����Ϊ��')
        
        sql="DELETE "
        sqlstr1=sql+" FROM fs_businoconf WHERE 1=1 "
        sqlstr1=sqlstr1+"AND busiNo='"+ TradeContext.busiNo+"'"
        
        AfaLoggerFunc.tradeInfo(sqlstr1)
        records = AfaDBFunc.DeleteSqlCmt(sqlstr1)
        if( records == None or records <=0 ):
            AfaLoggerFunc.tradeFatal(sqlstr1)
            return AfaFlowControl.ExitThisFlow( 'A0002', '���ݿ�����쳣:'+AfaDBFunc.sqlErrMsg )
            
        
        sql="DELETE "
        sqlstr2=sql+" FROM fs_remain WHERE 1=1 "
        sqlstr2=sqlstr2+"AND busiNo='"+ TradeContext.busiNo+"'"
        
        AfaLoggerFunc.tradeInfo(sqlstr2)
        records = AfaDBFunc.DeleteSqlCmt(sqlstr2)
        if( records == None or records <=0 ):
            AfaLoggerFunc.tradeFatal(sqlstr2)
            return AfaFlowControl.ExitThisFlow( 'A0002', '���ݿ�����쳣:'+AfaDBFunc.sqlErrMsg )
        return True
        
    except Exception, e:
        AfaLoggerFunc.tradeInfo(e)
        return AfaFlowControl.ExitThisFlow('9999', '�������쳣'+str(e))
    
