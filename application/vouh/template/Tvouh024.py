# -*- coding: gbk -*-

####################################################################
#    文    件:    Tvouh024.py
#    说    明:    凭证管理.打印报表
#    环    境:    中间业务新平台（AFA）--- UNIX: AIX 5.3
#    作    者:    李亚杰
#    公    司:    北京赞同科技
#    创建地址:    安徽
#    创建时间:    2008年6月15日
#    维护纪录:
####################################################################

import TradeContext, AfaLoggerFunc, AfaUtilTools, AfaFunc, AfaFlowControl, AfaDBFunc
from types import *
import AfaLoggerFunc,VouhFunc,binascii,HostContext,VouhHostFunc,os


def tradeExit( code, msg ):
    TradeContext.errorCode, TradeContext.errorMsg=code, msg
    if code != '0000':
        return False
    return True

def main( ):
    
    AfaLoggerFunc.tradeInfo( '打印报表['+TradeContext.TemplateCode+']进入' )
    
    #=============前台上送数据====================
    #TradeContext.sTellerNo          柜员号 
    #TradeContext.sWorkDate          交易日期
    #TrddeContext.sBesbNo            机构号

    
    
    try:
        #=============获取机构类型==========================
        HostContext.I1OTSB = TradeContext.sBesbNo         #机构号
        HostContext.I1SBNO = TradeContext.sBesbNo         #机构号
        HostContext.I1USID = TradeContext.sTellerNo       #柜员号
        HostContext.I1WSNO = TradeContext.sWSNO           #终端号
        if(not VouhHostFunc.CommHost('2001')):
            tradeExit(TradeContext.errorCode, TradeContext.errorMsg)
            raise AfaFlowControl.flowException( )
        if(TradeContext.errorCode == '0000'):
            SBNO = HostContext.O1SBCH
            AfaLoggerFunc.tradeInfo( SBNO )
        
        #=============获取柜员级别==========================
        HostContext.I1TELR = TradeContext.sTellerNo       #柜员号
        HostContext.I1SBNO = TradeContext.sBesbNo         #机构号
        HostContext.I1USID = TradeContext.sTellerNo       #柜员号
        HostContext.I1WSNO = TradeContext.sWSNO           #终端号
        if(not VouhHostFunc.CommHost('8809')):
            tradeExit(TradeContext.errorCode, TradeContext.errorMsg)
            raise AfaFlowControl.flowException( )
        if(TradeContext.errorCode == '0000'):
            TELLER = HostContext.O1TLRK
            AfaLoggerFunc.tradeInfo( TELLER )
        
        #=============初始化返回报文变量==================
        TradeContext.tradeResponse = []
        
        #=================获取机构名称==============================
        #begin 20100920 蔡永贵修改 避免机构不存在时查询结果为空而抛出错误
        #TradeContext.sBesbName = VouhFunc.SelectBesbName(TradeContext.sBesbNo)
        if not VouhFunc.SelectBesbName(TradeContext.sBesbNo):
            raise AfaFlowControl.flowException( )
        else:
            TradeContext.sBesbName = VouhFunc.SelectBesbName(TradeContext.sBesbNo)
        #end

        #=====================获取机构类型===============================
        #TradeContext.sBesbSty = VouhFunc.SelectBesbSty(TradeContext.sBesbNo)
        #AfaLoggerFunc.tradeInfo('================='+TradeContext.sBesbSty)

        #=============获取当前系统时间====================
        TradeContext.sLstTrxDay = AfaUtilTools.GetSysDate( )
        TradeContext.sLstTrxTime = AfaUtilTools.GetSysTime( ) 
        
        #begin凭证优化更改201109  
        #=============获取柜员尾箱号===============================
        HostContext.I1SBNO = TradeContext.sBesbNo         #机构号
        HostContext.I1USID = TradeContext.sTellerNo       #柜员号
        HostContext.I1WSNO = TradeContext.sWSNO           #终端号
        HostContext.I1EDDT = TradeContext.sLstTrxDay      #终止日期
        HostContext.I1TELR = TradeContext.sTellerNo       #柜员代号
        
        if(not VouhHostFunc.CommHost('0104')):
            VouhFunc.tradeExit( TradeContext.errorCode, TradeContext.errorMsg )
            raise AfaFlowControl.flowException( )
        if(TradeContext.errorCode == '0000'):
            TradeContext.sTellerTailNobak = HostContext.O2CABO
            TradeContext.sTellerTailNo    = TradeContext.sTellerTailNobak[0]                 
            AfaLoggerFunc.tradeInfo( '交易柜员尾箱号：' + TradeContext.sTellerTailNo ) 
        #end   
        
        vouh = []
        count1 = 0
        count2 = 0
        count3 = 0
        AfaLoggerFunc.tradeInfo(TradeContext.sTellerTailNo)
        sqlStr = "select VOUHTYPE,VOUHNAME from VOUH_PARAMETER where substr(BESBNO,1,6) = '" + (TradeContext.sBesbNo)[:6] + "' order by VOUHTYPE"
        AfaLoggerFunc.tradeInfo(sqlStr)
        records = AfaDBFunc.SelectSql( sqlStr )
        if( records == None ):
            tradeExit('A005067', '查询[凭证参数表]操作异常!')
            raise AfaFlowControl.flowException( )
        elif( len( records ) == 0 ):
            tradeExit('A005068', '凭证不存在!' )
            raise AfaFlowControl.flowException( )
        else :
            for i in range(len(records)):
                num1 = 0
                num2 = 0
                num3 = 0
                if(SBNO == '33' and TELLER == "10"):
                    
                    #查询凭证领用数
                    sqlStr = "select SUM(CAST(VOUHNUM AS DECIMAL(25))) from VOUH_MODIFY \
                            where WORKDATE = '" + TradeContext.sWorkDate + "' \
                            and VOUHTYPE = '" + records[i][0] + "' \
                            and TELLERNO = '" + TradeContext.sTellerTailNo + "' \
                            and BESBNO = '" + TradeContext.sBesbNo + "' \
                            and TRANSTATUS = '0' \
                            and VOUHSTATUS = '0'"
                    res1 = AfaDBFunc.SelectSql( sqlStr )
                    AfaLoggerFunc.tradeInfo('sql1 = '+sqlStr)
                    if( res1 == None ):
                        tradeExit('A005067', '查询[凭证表]操作异常!')
                        raise AfaFlowControl.flowException( )
                    elif( len( res1 ) == 0 ):
                        num1 = 0
                    else :
                        num1 = res1[0][0]
                        if(num1 == None):
                            num1 = 0
                        AfaLoggerFunc.tradeInfo(num1)  
                          
                    #查询凭证付出数
                    sqlStr = "select SUM(CAST(VOUHNUM AS DECIMAL(25))) from VOUH_MODIFY \
                            where WORKDATE = '" + TradeContext.sWorkDate + "' \
                            and TELLERNO = '" + TradeContext.sTellerTailNo + "' \
                            and VOUHTYPE = '" + records[i][0] + "' \
                            and BESBNO = '" + TradeContext.sBesbNo + "' \
                            and TRANSTATUS = '0' \
                            and VOUHSTATUS in ('1','2')"
                    res2 = AfaDBFunc.SelectSql( sqlStr )
                    AfaLoggerFunc.tradeInfo('sql2 = '+sqlStr)
                    if( res2 == None ):
                        tradeExit('A005067', '查询[凭证表]操作异常!')
                        raise AfaFlowControl.flowException( )
                    elif( len( res2 ) == 0 ):
                        num2 = 0
                    else :
                        num2 = res2[0][0]
                        if(num2 == None):
                            num2 = 0
                        AfaLoggerFunc.tradeInfo(num2)  
                         
                    #查询凭证余数
                    sqlStr = "select SUM(CAST(VOUHNUM AS DECIMAL(25))) from VOUH_REGISTER \
                            where VOUHTYPE = '" + records[i][0] + "' \
                            and TELLERNO = '" + TradeContext.sTellerTailNo + "' \
                            and BESBNO = '" + TradeContext.sBesbNo + "' \
                            and VOUHSTATUS = '0'"
                    res3 = AfaDBFunc.SelectSql( sqlStr )
                    AfaLoggerFunc.tradeInfo('sql3 = '+sqlStr)
                    if( res3 == None ):
                        tradeExit('A005067', '查询[凭证表]操作异常!')
                        raise AfaFlowControl.flowException( )
                    elif( len( res3 ) == 0 ):
                        num3 = 0
                    else :
                        num3 = res3[0][0]
                        if(num3 == None):
                            num3 = 0
                        AfaLoggerFunc.tradeInfo(num3)  
                          
                elif(TELLER == "10"):
                    
                    #查询凭证领用数
                    sqlStr = "select SUM(CAST(VOUHNUM AS DECIMAL(25))) from VOUH_MODIFY \
                            where WORKDATE = '" + TradeContext.sWorkDate + "' \
                            and VOUHTYPE = '" + records[i][0] + "' \
                            and (TELLERNO = '" + TradeContext.sTellerTailNo + "' \
                            or RIVTELLER = '" + TradeContext.sTellerTailNo + "') \
                            and BESBNO = '" + TradeContext.sBesbNo + "' \
                            and TRANSTATUS = '0' \
                            and VOUHSTATUS = '2'"
                    res1 = AfaDBFunc.SelectSql( sqlStr )
                    AfaLoggerFunc.tradeInfo('sql1 = '+sqlStr)
                    if( res1 == None ):
                        tradeExit('A005067', '查询[凭证表]操作异常!')
                        raise AfaFlowControl.flowException( )
                    elif( len( res1 ) == 0 ):
                        num1 = 0
                    else :
                        num1 = res1[0][0]
                        if(num1 == None):
                            num1 = 0
                            
                    #查询凭证付出数
                    sqlStr = "select SUM(CAST(VOUHNUM AS DECIMAL(25))) from VOUH_MODIFY \
                            where WORKDATE = '" + TradeContext.sWorkDate + "' \
                            and TELLERNO = '" + TradeContext.sTellerTailNo + "' \
                            and BESBNO = '" + TradeContext.sBesbNo + "' \
                            and VOUHTYPE = '" + records[i][0] + "' \
                            and TRANSTATUS = '0' \
                            and EXSTATUS = '2' \
                            and VOUHSTATUS in ('0','3')"
                    res2 = AfaDBFunc.SelectSql( sqlStr )
                    AfaLoggerFunc.tradeInfo('sql2 = '+sqlStr)
                    if( res2 == None ):
                        tradeExit('A005067', '查询[凭证表]操作异常!')
                        raise AfaFlowControl.flowException( )
                    elif( len( res2 ) == 0 ):
                        num2 = 0
                    else :
                        num2 = res2[0][0]
                        if(num2 == None):
                            num2 = 0
                            
                    #查询凭证余数
                    sqlStr = "select SUM(CAST(VOUHNUM AS DECIMAL(25))) from VOUH_REGISTER \
                            where VOUHTYPE = '" + records[i][0] + "' \
                            and TELLERNO = '" + TradeContext.sTellerTailNo + "' \
                            and BESBNO = '" + TradeContext.sBesbNo + "' \
                            and VOUHSTATUS = '2'"
                    res3 = AfaDBFunc.SelectSql( sqlStr )
                    AfaLoggerFunc.tradeInfo('sql3 = '+sqlStr)
                    if( res3 == None ):
                        tradeExit('A005067', '查询[凭证表]操作异常!')
                        raise AfaFlowControl.flowException( )
                    elif( len( res3 ) == 0 ):
                        num3 = 0
                    else :
                        num3 = res3[0][0]
                        if(num3 == None):
                            num3 = 0
                            
                elif(TELLER == "20"):
                    
                    #查询凭证领用数
                    sqlStr = "select SUM(CAST(VOUHNUM AS DECIMAL(25))) from VOUH_MODIFY \
                            where WORKDATE = '" + TradeContext.sWorkDate + "' \
                            and VOUHTYPE = '" + records[i][0] + "' \
                            and substr(BESBNO,1,6) = '" + (TradeContext.sBesbNo)[:6] + "' \
                            and BESBNO = '" + TradeContext.sBesbNo + "' \
                            and TRANSTATUS = '0' \
                            and VOUHSTATUS = '2'"
                    res1 = AfaDBFunc.SelectSql( sqlStr )
                    AfaLoggerFunc.tradeInfo('sql1 = '+sqlStr)
                    if( res1 == None ):
                        tradeExit('A005067', '查询[凭证表]操作异常!')
                        raise AfaFlowControl.flowException( )
                    elif( len( res1 ) == 0 ):
                        num1 = 0
                    else :
                        num1 = res1[0][0]
                        if(num1 == None):
                            num1 = 0
                            
                    #查询凭证付出数
                    sqlStr = "select SUM(CAST(VOUHNUM AS DECIMAL(25))) from VOUH_MODIFY \
                            where WORKDATE = '" + TradeContext.sWorkDate + "' \
                            and substr(BESBNO,1,6) = '" + (TradeContext.sBesbNo)[:6] + "' \
                            and BESBNO = '" + TradeContext.sBesbNo + "' \
                            and VOUHTYPE = '" + records[i][0] + "' \
                            and TRANSTATUS = '0' \
                            and EXSTATUS = '3' \
                            and VOUHSTATUS in ('2','4','5','6')"
                    res2 = AfaDBFunc.SelectSql( sqlStr )
                    AfaLoggerFunc.tradeInfo('sql2 = '+sqlStr)
                    if( res2 == None ):
                        tradeExit('A005067', '查询[凭证表]操作异常!')
                        raise AfaFlowControl.flowException( )
                    elif( len( res2 ) == 0 ):
                        num2 = 0
                    else :
                        num2 = res2[0][0]
                        if(num2 == None):
                            num2 = 0
                            
                    #查询凭证余数
                    sqlStr = "select SUM(CAST(VOUHNUM AS DECIMAL(25))) from VOUH_REGISTER \
                            where VOUHTYPE = '" + records[i][0] + "' \
                            and substr(BESBNO,1,6) = '" + (TradeContext.sBesbNo)[:6] + "' \
                            and BESBNO = '" + TradeContext.sBesbNo + "' \
                            and VOUHSTATUS in ('2','3')"
                    res3 = AfaDBFunc.SelectSql( sqlStr )
                    AfaLoggerFunc.tradeInfo('sql3 = '+sqlStr)
                    if( res3 == None ):
                        tradeExit('A005067', '查询[凭证表]操作异常!')
                        raise AfaFlowControl.flowException( )
                    elif( len( res3 ) == 0 ):
                        num3 = 0
                    else :
                        num3 = res3[0][0]
                        if(num3 == None):
                            num3 = 0
                            
                else:
                    
                    #查询凭证领用数
                    sqlStr = "select SUM(CAST(VOUHNUM AS DECIMAL(25))) from VOUH_MODIFY \
                            where WORKDATE = '" + TradeContext.sWorkDate + "' \
                            and VOUHTYPE = '" + records[i][0] + "' \
                            and (TELLERNO = '" + TradeContext.sTellerTailNo + "' \
                            or RIVTELLER = '" + TradeContext.sTellerTailNo + "') \
                            and BESBNO = '" + TradeContext.sBesbNo + "' \
                            and TRANSTATUS = '0' \
                            and VOUHSTATUS = '3'"
                    res1 = AfaDBFunc.SelectSql( sqlStr )
                    AfaLoggerFunc.tradeInfo('sql1 = '+sqlStr)
                    if( res1 == None ):
                        tradeExit('A005067', '查询[凭证表]操作异常!')
                        raise AfaFlowControl.flowException( )
                    elif( len( res1 ) == 0 ):
                        num1 = 0
                    else :
                        num1 = res1[0][0]
                        if(num1 == None):
                            num1 = 0
                            
                    #查询凭证付出数
                    sqlStr = "select SUM(CAST(VOUHNUM AS DECIMAL(25))) from VOUH_MODIFY \
                            where WORKDATE = '" + TradeContext.sWorkDate + "' \
                            and TELLERNO = '" + TradeContext.sTellerTailNo + "' \
                            and BESBNO = '" + TradeContext.sBesbNo + "' \
                            and VOUHTYPE = '" + records[i][0] + "' \
                            and TRANSTATUS = '0' \
                            and EXSTATUS = '3' \
                            and VOUHSTATUS in ('2','4','5','6')"
                    res2 = AfaDBFunc.SelectSql( sqlStr )
                    AfaLoggerFunc.tradeInfo('sql2 = '+sqlStr)
                    if( res2 == None ):
                        tradeExit('A005067', '查询[凭证表]操作异常!')
                        raise AfaFlowControl.flowException( )
                    elif( len( res2 ) == 0 ):
                        num2 = 0
                    else :
                        num2 = res2[0][0]
                        if(num2 == None):
                            num2 = 0
                            
                    #查询凭证余数
                    sqlStr = "select SUM(CAST(VOUHNUM AS DECIMAL(25))) from VOUH_REGISTER \
                            where VOUHTYPE = '" + records[i][0] + "' \
                            and TELLERNO = '" + TradeContext.sTellerTailNo + "' \
                            and BESBNO = '" + TradeContext.sBesbNo + "' \
                            and VOUHSTATUS = '3'"
                    res3 = AfaDBFunc.SelectSql( sqlStr )
                    AfaLoggerFunc.tradeInfo('sql3 = '+sqlStr)
                    if( res3 == None ):
                        tradeExit('A005067', '查询[凭证表]操作异常!')
                        raise AfaFlowControl.flowException( )
                    elif( len( res3 ) == 0 ):
                        num3 = 0
                    else :
                        num3 = res3[0][0]
                        if(num3 == None):
                            num3 = 0
                    
                vouh.append([records[i][0],records[i][1],str(num1),str(num2),str(num3)])
                
                count1 = count1 + num1
                count2 = count2 + num2
                count3 = count3 + num3

        
        rBankFile= os.environ['AFAP_HOME'] + '/data/vouh/vouhtmp.txt'
      

        #创建业务报表文件
        bFp = open(rBankFile, "w")
        AfaLoggerFunc.tradeInfo('-----' + TradeContext.sBesbNo)
        AfaLoggerFunc.tradeInfo('-----' + TradeContext.sBesbName)
        AfaLoggerFunc.tradeInfo('-----' + TradeContext.sTellerTailNo)
        AfaLoggerFunc.tradeInfo('-----' + TradeContext.sWorkDate)
        
        #写入标题
        bFp.write('\n                          **************** 代理业务凭证余额表 ****************                         \n\n')
        bFp.write('              机构号码:' + TradeContext.sBesbNo + '        机构名称: ' + TradeContext.sBesbName +  '\n')
        bFp.write('              柜员号码:' + TradeContext.sTellerTailNo +  '            日期:' + TradeContext.sWorkDate +  '\n')
        bFp.write('    ------------------------------------------------------------------------------------------------------\n')
        bFp.write('    |   序号   | 凭证种类 |          凭证姓名            |   收方发生额  |   付方发生额  |      余额     |\n')
        bFp.write('    |----------|----------|------------------------------|---------------|---------------|---------------|\n')
            
        AfaLoggerFunc.tradeInfo('------------test5')
        for i in range( len( vouh ) ):

            wbuffer = '    |'
            wbuffer = wbuffer + str(i+1).ljust(10,' ') + '|'
            wbuffer = wbuffer +(vouh[i][0].strip()).ljust(10, ' ') + '|'
            wbuffer = wbuffer +(vouh[i][1].strip()).ljust(30, ' ') + '|'
            wbuffer = wbuffer +(vouh[i][2].strip()).rjust(15, ' ') + '|'
            wbuffer = wbuffer +(vouh[i][3].strip()).rjust(15, ' ') + '|'
            wbuffer = wbuffer +(vouh[i][4].strip()).rjust(15, ' ') + '|'

            #写入报表文件
            bFp.write(wbuffer + '\n')
            bFp.write('    |----------|----------|------------------------------|---------------|---------------|---------------|\n')
        
        bFp.write('    |   合计   |          |                              |' + str(count1).rjust(15,' ') + '|' + str(count2).rjust(15,' ') + '|' + str(count3).rjust(15,' ')+ '|\n')
        bFp.write('    ------------------------------------------------------------------------------------------------------\n')
        #关闭文件
        bFp.close()
        
        TradeContext.tradeResponse.append( ['sBesbNo',TradeContext.sBesbNo] )
        TradeContext.tradeResponse.append( ['sTellerTailNo',TradeContext.sTellerTailNo] )
        TradeContext.tradeResponse.append( ['sTellerNo',TradeContext.sTellerNo] )             #凭证优化更改201109 
        TradeContext.tradeResponse.append( ['sLstTrxDay',TradeContext.sLstTrxDay] )
        TradeContext.tradeResponse.append( ['sLstTrxTime',TradeContext.sLstTrxTime] )
        TradeContext.tradeResponse.append( ['sFileName','vouhtmp.txt'] )
        TradeContext.tradeResponse.append( ['errorCode','0000'] )
        TradeContext.tradeResponse.append( ['errorMsg','交易成功'] )
        AfaFunc.autoPackData()
        #=============程序退出====================
        AfaLoggerFunc.tradeInfo( '打印报表['+TradeContext.TemplateCode+']退出' )
    except AfaFlowControl.flowException, e:
        AfaFlowControl.exitMainFlow( )
    except AfaFlowControl.accException:
        AfaFlowControl.exitMainFlow( )
    except Exception, e:
        AfaFlowControl.exitMainFlow(str(e))

  
