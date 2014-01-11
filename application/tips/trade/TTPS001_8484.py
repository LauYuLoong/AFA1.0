# -*- coding: gbk -*-
###############################################################################
# Copyright (c) 2011,北京赞同科技发展有限公司.第三事业部
# All rights reserved.
#
# 文件名称：TPS001_8484.py
# 文件标识：
# 摘    要：财税库行.差错明细查询
#
# 当前版本：1.0
# 作    者：
# 完成日期：2011 年 7 月 26 日
#
# 取代版本：
# 原 作 者：李利君
# 完成日期：
###############################################################################
import TradeContext
TradeContext.sysType = 'tips'
import AfaDBFunc,AfaLoggerFunc,os,TipsFunc,AfaFlowControl
#import UtilTools，TradeContext, ConfigParser
def SubModuleMainFst( ):
    try:
        
        AfaLoggerFunc.tradeInfo( '进入差错明细查询['+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']'  )
        
        #明细写入文件
        #begin李利君优化20120611
        #mx_file_name = os.environ['AFAP_HOME'] + '/data/batch/tips/' + 'AH_ERROR_' + TradeContext.teller + '_'+TradeContext.workDate+'.txt'
        mx_file_name = os.environ['AFAP_HOME'] + '/tmp/' + 'AH_ERROR_' + TradeContext.teller + '_'+TradeContext.workDate+'.txt'
        #end
        
        TradeContext.tradeResponse.append(['fileName',  'AH_ERROR_' + TradeContext.teller +'_'+TradeContext.workDate+'.txt'])
        
        if (os.path.exists(mx_file_name) and os.path.isfile(mx_file_name)):
            #文件存在,先删除-再创建
            os.system("rm " + mx_file_name)
        
        #====获取清算信息=======   
        if not ChkLiquidStatus( ):
            return False
        
        
        #查询对账失败的交易明细
        sqlStr=''
        sqlStr=sqlStr + "SELECT BRNO,SERIALNO,DRACCNO,CRACCNO,TRADETYPE,TAXPAYNAME,AMOUNT,BANKSTATUS,CORPSTATUS,CHKFLAG,CORPCHKFLAG,REVTRANF,NOTE10 FROM TIPS_MAINTRANSDTL "
        sqlStr=sqlStr + " WHERE NOTE3 = '" + TradeContext.payBkCode.strip() + "' and WORKDATE = '" + TradeContext.date + "'"
        sqlStr=sqlStr + "and ((REVTRANF = '0' and BANKSTATUS = '0' and CORPSTATUS = '0' and ((CHKFLAG ='9' and CORPCHKFLAG ='9')or(CHKFLAG ='9' and CORPCHKFLAG ='0')or(CHKFLAG ='0' and CORPCHKFLAG ='9'))) "
        sqlStr=sqlStr + " or ( REVTRANF = '1' and BANKSTATUS != '0'))"
          
        AfaLoggerFunc.tradeInfo(sqlStr) 
           
        Records = AfaDBFunc.SelectSql( sqlStr )
           
        if( Records == None ):
            
            return TipsFunc.ExitThisFlow( 'A0027', '表操作异常:'+AfaDBFunc.sqlErrMsg )
            
        elif( len( Records )==0 ):
            
            return TipsFunc.ExitThisFlow( 'A0027', '没有满足条件的数据' )
        else:
            sfp = open(mx_file_name, "w")
            AfaLoggerFunc.tradeInfo('明细文件=['+mx_file_name+']')
            for i in range(0,len(Records)):
                A0 = str(Records[i][0]).strip()           #机构号
                A1 = str(Records[i][1]).strip()           #平台流水号     
                A2 = str(Records[i][2]).strip()           #借方账号   
                A3 = str(Records[i][3]).strip()           #贷方账号
                A4 = str(Records[i][4]).strip()           #交易类型
                A5 = str(Records[i][5]).strip()           #纳税人名称
                A6 = str(Records[i][6]).strip()           #交易金额
                A7 = str(Records[i][7]).strip()           #主机状态
                A8 = str(Records[i][8]).strip()           #企业状态
                A9 = str(Records[i][9]).strip()           #主机对账标志
                A10 = str(Records[i][10]).strip()         #企业对账标志
                A11 = str(Records[i][11]).strip()         #正反交易标志
                A12 = str(Records[i][12]).strip()         #清算金库名      
       
                sfp.write(A0 + '|' + A1 + '|' + A2 + '|' + A3 + '|' + A4 + '|' + A5 + '|' + A6 + '|' + A7 + '|' + A8 + '|' + A9 + '|' + A10 + '|' + A11 + '|' + A12 + '\n')
                
            sfp.close()                
        
        TradeContext.tradeResponse.append(['errorCode','0000'])
        TradeContext.tradeResponse.append(['errorMsg','交易成功'])
       
        AfaLoggerFunc.tradeInfo( '退出差错明细查询[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' )
    
        return True 
    
    except Exception, e:                  

        AfaFlowControl.exitMainFlow(str(e))      
                                              
#====获取清算信息==========    
def ChkLiquidStatus():
    AfaLoggerFunc.tradeInfo( '>>>获取清算信息' )
    
    sql ="SELECT PAYBKCODE,PAYEEBANKNO,TRECODE,TRENAME,PAYEEACCT,PAYBKNAME,STATUS FROM TIPS_LIQUIDATE_ADM WHERE "
    sql =sql + "BRNO = '" + TradeContext.brno + "'"
    
    AfaLoggerFunc.tradeInfo(sql)
    
    records = AfaDBFunc.SelectSql(sql)
    
    if( records == None ):
        AfaLoggerFunc.tradeFatal(sql)
        return TipsFunc.ExitThisFlow( 'A0002', '数据库操作异常:'+AfaDBFunc.sqlErrMsg )
    elif( len( records )==0 ):
        return  TipsFunc.ExitThisFlow( 'A0027', '本机构不是清算行，不可以进行对账差错查询' )
    else:
        if records[0][6]=='0':
            return TipsFunc.ExitThisFlow( 'A0027', '业务已停止，不可进行查询' )
        if records[0][6]=='2':
            return TipsFunc.ExitThisFlow( 'A0027', '业务已暂停，不可进行查询' )
        AfaLoggerFunc.tradeInfo('本机构的清算行号为'+ records[0][0])
        AfaLoggerFunc.tradeInfo('柜面送的清算行号为'+ TradeContext.payBkCode)
        if(records[0][0]!=TradeContext.payBkCode):
            return TipsFunc.ExitThisFlow( 'A0002', '清算行行号不正确，不允许做此交易')
            
    AfaLoggerFunc.tradeInfo( '>>>获取清算信息完成' )
    return True    
