# -*- coding: gbk -*-
###############################################################################
# Copyright (c) 2006,北京赞同科技发展有限公司.第三事业部
# All rights reserved.
#
# 文件名称：TTPS001_8457.py
# 文件标识：
# 摘    要：财税库行.对账查询
# 当前版本：1.0
# 作    者：
# 完成日期：2008年12月05日
#
# 取代版本：
# 原 作 者：
# 完成日期：
###############################################################################
import TradeContext, AfaDBFunc,AfaLoggerFunc,os,TipsFunc
import UtilTools
def SubModuleMainFst( ):
    AfaLoggerFunc.tradeInfo( '进入对账查询[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' )
    #检查机构状态,获取付款行号,收款行号
    if not TipsFunc.ChkBranchStatus():
        return TipsFunc.ExitThisFlow( 'A0027', '检查机构状态失败' )

    #合计        
    if not sumall():
        return False

    #明细写入文件
    mx_file_name = os.environ['AFAP_HOME'] + '/tmp/' + 'AH_' + TradeContext.teller + '.txt'
    TradeContext.tradeResponse.append(['fileName',  'AH_' + TradeContext.teller + '.txt'])
    
    if (os.path.exists(mx_file_name) and os.path.isfile(mx_file_name)):
        #文件存在,先删除-再创建
        os.system("rm " + mx_file_name)
    
    sfp = open(mx_file_name, "w")
    AfaLoggerFunc.tradeInfo('明细文件=['+mx_file_name+']')
    
    #明细
    sqlStr = ''
    sqlStr = sqlStr + "WHERE NOTE1 ='" +TradeContext.checkDate +"'"
    sqlStr = sqlStr + " AND NOTE2 = '" +TradeContext.checkNo   +"'"
    sqlStr = sqlStr + " AND NOTE3 ='"  + TradeContext.payBkCode.strip()  + "'"   
    sqlStr = sqlStr + " AND NOTE4 ='"  + TradeContext.payeeBankNo.strip()  + "'"
    ###################################################################################
    #guanbj 20091105 maps与tips的对账成功后即可查询对账结果
    #sqlStr=sqlStr+" AND CHKFLAG='0' and CORPCHKFLAG='0'"
    sqlStr=sqlStr+" AND CORPCHKFLAG='0'"
    ###################################################################################
    sqlStr=sqlStr+" ORDER BY SERIALNO"
    sqlStr_detail="SELECT WORKDATE,DRACCNO,TAXPAYNAME,SERIALNO,TAXPAYCODE,cast(AMOUNT as decimal(17,2)) FROM TIPS_MAINTRANSDTL  "
    sqlStr_detail=sqlStr_detail+sqlStr
    AfaLoggerFunc.tradeInfo(sqlStr_detail)
    Records = AfaDBFunc.SelectSql( sqlStr_detail )
    if( Records == None or Records <0):
        sfp.close()
        return TipsFunc.ExitThisFlow( 'A0027', '表操作异常:'+AfaDBFunc.sqlErrMsg )
    elif( len( Records )==0 ):
        sfp.close()
        return TipsFunc.ExitThisFlow( 'A0027', '没有满足条件的数据' )
    else:
        for i in range(0,len(Records)):
            A0 = str(Records[i][0]).strip()         #交易日期
            A1 = str(Records[i][1]).strip()         #帐号     
            A2 = str(Records[i][2]).strip()         #户名   
            A3 = str(Records[i][3]).strip()         #交易流水
            A4 = str(Records[i][4]).strip()         #纳税人编码
            A5 = str(Records[i][5]).strip()         #金额       

            sfp.write(A0 +  '|'  +  A1 +  '|'  +  A2 +  '|'  +  A3 +  '|'  +  A4 +  '|'  +  A5 +  '|' + '\n')
            
    sfp.close()                
    TradeContext.tradeResponse.append(['errorCode','0000'])
    TradeContext.tradeResponse.append(['errorMsg','交易成功'])

    AfaLoggerFunc.tradeInfo( '退出对账查询[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' )
    return True

#查询对账成功，差异笔数和金额
def sumall():       
    #成功总计
    AfaLoggerFunc.tradeInfo('查询对账成功笔数和金额')
    sumsql="SELECT count(*),sum(cast(amount as decimal(17,2))) "
    sumsql = sumsql + "FROM TIPS_MAINTRANSDTL  "
    sumsql = sumsql + "WHERE NOTE1 ='"+TradeContext.checkDate+"'"
    sumsql = sumsql + " AND NOTE2 = '"+TradeContext.checkNo+"'"
    ###################################################################################
    #guanbj 20091105 修改查询对账结果只查询maps与tips的对账成功的信息
    #sumsql = sumsql + " AND CHKFLAG='0' and CORPCHKFLAG='0'"
    sumsql=sumsql +" AND CORPCHKFLAG='0'"
    ###################################################################################
    sumsql = sumsql + " AND NOTE3='"  + TradeContext.payBkCode.strip()  + "'"   
    sumsql = sumsql + " AND NOTE4='"  + TradeContext.payeeBankNo.strip()  + "'"
    sumSucc=AfaDBFunc.SelectSql( sumsql)
    AfaLoggerFunc.tradeInfo(sumsql)
    AfaLoggerFunc.tradeInfo("成功总计"+repr(sumSucc))
    if( sumSucc == None ):
        # None 查询失败
        return TipsFunc.ExitThisFlow( 'A0025', '数据库操作错误 统计成功笔数出错!'+AfaDBFunc.sqlErrMsg  )
    if sumSucc[0][0] == 0:
        return TipsFunc.ExitThisFlow( 'A0027', '没有满足条件的数据' )

    sumSucc=UtilTools.ListFilterNone(sumSucc,0)
    TradeContext.tradeResponse.append( ['sSum', str(sumSucc[0][0])] )  
    TradeContext.tradeResponse.append( ['sAmt', str(sumSucc[0][1])] )

    return True
    
