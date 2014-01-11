# -*- coding: gbk -*-
##################################################################
#   中间业务平台.
#=================================================================
#   程序文件:   YBT001_8614.py
#   程序说明:   当日单证重打
#   修改时间:   2010-08-03
##################################################################
import TradeContext, AfaLoggerFunc, AfaUtilTools, AfaFunc, Party3Context,AfaAfeFunc,AfaFlowControl,AfaDBFunc,AfaAhAdb,YbtFunc
import AfaHostFunc
from types import *

def SubModuleDoFst( ):

    #校验保险公司代码和凭证种类是否合法
    if not AfaAhAdb.ADBCheckCert( ):
        return False
    
    AfaLoggerFunc.tradeInfo( '初始化单证重打交易变量' )
    #交易代码
    TradeContext.tradeCode = TradeContext.TransCode
    
    try:
        #查询原缴费记录是否存在
        sql = ""
        sql = "select note9,amount,bankserno,agentserialno,tellerno,brno,draccno from afa_maintransdtl where agentserialno = '"+TradeContext.PreSerialno+"'"
        sql = sql + " and userno = '" + TradeContext.userno + "' and workdate = '" + TradeContext.workDate + "'"
        sql = sql + " and bankstatus = '0' and corpstatus = '0' and revtranf = '0'"
        
        AfaLoggerFunc.tradeInfo('当日单证重打查询语句'+ sql)
        
        records = AfaDBFunc.SelectSql( sql )
         
        if records==None:
            TradeContext.errorCode,TradeContext.errorMsg = "0001" ,"查询银保通数据库失败"
            raise AfaFlowControl.flowException( )
        
        elif(len(records) < 1):
            TradeContext.errorCode,TradeContext.errorMsg = "0001","无此交易，不能重打印"
            return False
        
        else:
            AfaLoggerFunc.tradeDebug("records=" + str(records))
            
        if(records[0][4] != TradeContext.tellerno):
            TradeContext.errorCode,TradeContext.errorMsg = "0001","原交易非本柜员所做，不能做此交易"
            return False
        
        if(records[0][5] != TradeContext.brno):
            TradeContext.errorCode,TradeContext.errorMsg = "0001","原交易非本网点所做，不能做此交易"
            return False
              
        if (TradeContext.policy!=records[0][0].split('|')[2].strip()):
            TradeContext.errorCode,TradeContext.errorMsg = "0001","保险单号不符，请重新输入"
            return False
            
        if (TradeContext.premium!=records[0][1].strip()):
            TradeContext.errorCode,TradeContext.errorMsg = "0001","交易金额不符，请重新输入"
            return False
        #投保单号
        TradeContext.applno = records[0][0].split('|')[1].strip()    
        #amount : "缴费金额"
        TradeContext.amount  = records[0][1].strip()
        
        #bankserno : "主机柜员流水号"
        TradeContext.hostserialno = records[0][2].strip()
        
        #agentSerialno: "中间业务流水号"
        TradeContext.agentserialno = records[0][3].strip()
        
        #draccno : 转账账号
        TradeContext.payacc = records[0][6].strip()
    
        return True        
    except Exception, e:
        AfaFlowControl.exitMainFlow(str(e))
    
   

def SubModuleDoSnd():
    AfaLoggerFunc.tradeInfo('进入单证重打交易[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']与第三方通信后处理' )
    
    try:
        names = Party3Context.getNames( )
       
        for name in names:
            value = getattr( Party3Context, name )
            if ( not name.startswith( '__' ) and type(value) is StringType or type(value) is ListType) :
                setattr( TradeContext, name, value )
            
        if(TradeContext.errorCode=='0000'):
            #第三方返回成功后更新原保单印刷号
            update_sql = "update afa_maintransdtl set "                                             
            update_sql = update_sql + " userno            = '" + TradeContext.userno1     + "'"       #user1新保单印刷号
            update_sql = update_sql + " where userno      = '" + TradeContext.userno      + "'"       #user原保单印刷号 
            update_sql = update_sql + " and workdate      = '" + TradeContext.workDate    + "'"       #日期  
            update_sql = update_sql + " and agentserialno = '" + TradeContext.PreSerialno + "'"       #缴费成功的中间业务流水号
            
            #更新并提交数据
            if  AfaDBFunc.UpdateSqlCmt(update_sql)<0:
                return AfaFlowControl.ExitThisFlow("A999","更新投保单号失败")
                
            #第三方返回成功后生成现金价值文件
            if not YbtFunc.createFile( ):
                return False

        AfaLoggerFunc.tradeInfo('退出单证重打[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']与第三方通讯后处理' )
        return True
    
    except Exception, e:
        AfaFlowControl.exitMainFlow(str(e))
