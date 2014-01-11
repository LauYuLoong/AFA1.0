# -*- coding: gbk -*-
################################################################################
#   中间业务平台.公共方法类
#===============================================================================
#   程序文件:   AfaFunc.py
#   修改时间:   2006-09-26
################################################################################
import exceptions,TradeContext,AfaDBFunc,TradeException,AfaUtilTools,ConfigParser,Party3Context,AfaLoggerFunc,AfaFlowControl,os,time,socket,UtilTools
from types import *

#=======================根据指定的配置文件,section名获取相应配置================
def GetConfigInfo( configFileName = '', sectionName='' ):

    AfaLoggerFunc.tradeInfo( '>>>获取配置信息' )

    result=[]
    try:
        config = ConfigParser.ConfigParser( )
        config.readfp( open( configFileName ) )
        tmpResult = config.options( sectionName )

        for i in range( 0, len( tmpResult ) ):
            result.append( config.get( sectionName, tmpResult[i] ) )

    except Exception, e:
        AfaLoggerFunc.tradeFatal( str(e) )
        return 0
        
    return result


#=======================获取平台流水号DB2=======================================
def GetSerialno( seqName="BUSI_ONLINE_SEQ" ):

    AfaLoggerFunc.tradeInfo( '获取平台流水号' )

    sqlStr = "SELECT NEXTVAL FOR " + seqName + " FROM SYSIBM.SYSDUMMY1"
    records = AfaDBFunc.SelectSql( sqlStr )
    if records == None :
        TradeContext.errorCode = 'A0025'
        TradeContext.errorMsg = AfaDBFunc.sqlErrMsg
        return -1

    #左补"0"(8位)
    TradeContext.agentSerialno=str( records[0][0] ).rjust( 8, '0' )

    return str( records[0][0] )



#=======================判断应用系统状态========================================
def ChkSysStatus( ):


    AfaLoggerFunc.tradeInfo( '>>>判断应用系统状态' )


    #=======================变量值的有效性校验==========================
    if( not TradeContext.existVariable( "sysId" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '应用系统标识[sysId]值不存在!' )
    else:
        TradeContext.sysId=AfaUtilTools.Lfill( TradeContext.sysId, 6, '0' )
        
        
    #=======================网点级别检查========================================
    #if(not GetBranchInfo(TradeContext.brno)):
    #    return False
    #else:
    #    if( int(TradeContext.__branchType__) != 3):
    #        return AfaFlowControl.ExitThisFlow( '0001', '非营业网点，不允许做此交易' )
    

    #=======================系统标识============================================
    sqlStr = "SELECT * FROM AFA_SYSTEM WHERE SYSID = '" + TradeContext.sysId + "'"

    AfaLoggerFunc.tradeInfo( sqlStr )

    records = AfaDBFunc.SelectSql( sqlStr )
    if( records == None ):
        return AfaFlowControl.ExitThisFlow( 'A0002', '应用系统状态表操作异常:'+AfaDBFunc.sqlErrMsg )

    elif( len( records )!=0 ):
        AfaUtilTools.ListFilterNone( records )

        #=======================判断系统状态====================================
        if( records[0][5]=="0" ):
            return AfaFlowControl.ExitThisFlow( 'A0004', '该应用系统处于关闭状态,不能做交易' )
                
        elif( records[0][5]=="2" ):
            return AfaFlowControl.ExitThisFlow( 'A0005', '该应用系统处于暂停状态,不能做交易' )
                
        elif( records[0][5]=="3" ):
            return AfaFlowControl.ExitThisFlow( 'A0005', '该应用系统处于未启用状态,不能做交易' )

        #=======================设置全局变量====================================

        #系统英文简称
        TradeContext.sysEName = records[0][1]
        
        #系统中文名称
        TradeContext.sysCName = records[0][2]

        #系统类型(0-总行应用 1-分行应用 2-支行应用)
        TradeContext.__type__ = records[0][6]


        #单笔交易额度(当额度为0时表示不限制额度)
        if(len(records[0][7])==0):
            TradeContext.__sysMaxAmount__ = '0'
        else:
            TradeContext.__sysMaxAmount__ = records[0][7]

        AfaLoggerFunc.tradeInfo( '::::::系统单笔额度  =' + TradeContext.__sysMaxAmount__ )

        #日累计交易额度(当额度为0时表示不限制额度)
        if(len(records[0][8])==0):
            TradeContext.__sysTotalamount__ = '0'
        else:
            TradeContext.__sysTotalamount__ = records[0][8]

        AfaLoggerFunc.tradeInfo( '::::::系统累计额度  =' + TradeContext.__sysTotalamount__ )

        #检查交易额度(1-系统 2-渠道)
        if(not ChkAmtStatus('1')):
            return False
                
        #渠道管理模式(0-按总行控制 1-按分行控制 2-按支行控制)
        TradeContext.__channelMode__ = records[0][9]
        AfaLoggerFunc.tradeInfo( '::::::渠道管理模式  =' + TradeContext.__channelMode__ )

        #缴费介质管理模式(0-按总行控制 1-按分行控制 2-按支行控制)
        TradeContext.__actnoMode__ = records[0][10]
        AfaLoggerFunc.tradeInfo( '::::::介质管理模式  =' + TradeContext.__actnoMode__ )


        #获取摘要代码(帐务核心系统需要)(默认=258)
        if( not GetSummaryInfo( ) ):
            return False
            
        return True
        
    else:
     
        return AfaFlowControl.ExitThisFlow( 'A0003', '无系统参数信息' )


#=======================判断商户状态============================================
def ChkUnitStatus( ):

    AfaLoggerFunc.tradeInfo( '>>>判断单位状态' )
        
    #=======================变量值的有效性校验==================================
    if( not TradeContext.existVariable( "unitno" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '单位代码[unitno]值不存在!' )
            

    #=======================单位信息============================================
    sqlStr = "SELECT * FROM AFA_UNITADM WHERE SYSID = '" + TradeContext.sysId + "' AND UNITNO = '" + TradeContext.unitno + "' "

    AfaLoggerFunc.tradeInfo( sqlStr )

    records = AfaDBFunc.SelectSql( sqlStr )
    if( records == None ):
        return AfaFlowControl.ExitThisFlow( 'A0002', '单位信息表操作异常:'+AfaDBFunc.sqlErrMsg )

    elif( len( records ) != 0 ):
        AfaUtilTools.ListFilterNone( records )

        #=======================设置全局变量====================================

        #单位名称
        TradeContext.unitName = records[0][2]

        #单位简称
        TradeContext.unitSName = records[0][3]

        #=======================判断单位状态====================================
        if( records[0][4]=="0" ):
            return AfaFlowControl.ExitThisFlow( 'A0004', '该单位处于关闭状态,不能做交易' )

        elif( records[0][4]=="2" ):
            return AfaFlowControl.ExitThisFlow( 'A0005', '该单位处于暂停状态,不能做交易' )

        elif( records[0][4]=="3" ):
            return AfaFlowControl.ExitThisFlow( 'A0005', '该单位处于未启用状态,不能做交易' )


        #业务模式(0-无分支机构 1-有分支机构,业务参数按商户单位控制 2-有分支机构,业务参数按商户分支单位控制
        TradeContext.__busiMode__ = records[0][5]
        AfaLoggerFunc.tradeInfo( '::::::业务模式  =' + TradeContext.__busiMode__ )

        
        #账户模式(0-无分账户 1-有分账户,按总商户清算 2-有分账户,按商户分支单位清算)
        TradeContext.__accMode__ = records[0][6]
        AfaLoggerFunc.tradeInfo( '::::::账户模式  =' + TradeContext.__accMode__ )

        
        #=======================业务模式========================================
        if( TradeContext.__busiMode__ != "2" ):
            
            #判断服务时间
            if( len(records[0][12]) == 0 ):
                records[0][12]='000000'
                
            if( len(records[0][13]) == 0 ):
                records[0][13]='000000'

            if( long( TradeContext.workTime )<long( records[0][12] ) or long( TradeContext.workTime )>long( records[0][13] ) ):
                return AfaFlowControl.ExitThisFlow( 'A0007', "超过该业务开放时间,请在每天["+records[0][12]+"->"+records[0][13]+"]做此业务" )


            #收取模式(0-不收费 1-模式一(逐笔收费) 2-模式二(汇总收费))
            TradeContext.__feeFlag__ = records[0][14]
            AfaLoggerFunc.tradeInfo( '::::::费用收取模式  =' + TradeContext.__feeFlag__ )

            
            #拆分特征码(1-签到校验标志 2-日终校验标志 3-对帐校验标志 4-响应码使用标志 5-子表使用标志 6-扩展模式 7-密钥使用标志)
            TradeContext.__agentEigen__ = records[0][25]

            AfaLoggerFunc.tradeInfo( '::::::签到校验标志  =' + TradeContext.__agentEigen__[0] )
            AfaLoggerFunc.tradeInfo( '::::::日终校验标志  =' + TradeContext.__agentEigen__[1] )
            AfaLoggerFunc.tradeInfo( '::::::对帐校验标志  =' + TradeContext.__agentEigen__[2] )
            AfaLoggerFunc.tradeInfo( '::::::响应码使用标志=' + TradeContext.__agentEigen__[3] )
            AfaLoggerFunc.tradeInfo( '::::::子表使用标志  =' + TradeContext.__agentEigen__[4] )
            AfaLoggerFunc.tradeInfo( '::::::扩展模式      =' + TradeContext.__agentEigen__[5] )
            AfaLoggerFunc.tradeInfo( '::::::密钥使用标志  =' + TradeContext.__agentEigen__[6] )
            
            #判断是否是签到签退交易
            if( not TradeContext.existVariable( "__signFlag__" ) ):
                
                #检查签到标志
                if( TradeContext.__agentEigen__[0]=='1' and records[0][26]=="0" ):
                    return AfaFlowControl.ExitThisFlow( 'A0008', '该单位还没有签到,不能做此交易' )

            else:
                if TradeContext.__signFlag__ == '1' :
                    
                    #签到
                    return SignIn( )
                        
                else:
                
                    #签退
                    return SignOut( )


            #检查日终标志(0-未做 1-已做)
            if( TradeContext.__agentEigen__[1]=='1' and records[0][27]=="1" ):
                return AfaFlowControl.ExitThisFlow( 'A0009', '该单位已做日终操作,不能做此交易' )
                    
            #检查对帐标志(0：未做 1-已对主机帐 2-第三方对帐成功 3-第三方对帐失败)
            if( TradeContext.__agentEigen__[2]=='1' and long(records[0][29])>=1 ):
                return AfaFlowControl.ExitThisFlow( 'A0010', '该单位已做对帐操作,不能做此交易' )


            #响应码转换标志
            TradeContext.__respFlag__ = TradeContext.__agentEigen__[3]


            #密钥使用标志
            TradeContext.__keyFlag__ = TradeContext.__agentEigen__[6]


            #密钥使用标志
            if ( TradeContext.__keyFlag__=='1' ):
                if( not GetKeyInfo( ) ):
                    return False

            #收费使用标志
            if ( TradeContext.__feeFlag__=='1' ):
                if( not GetFeeInfo( ) ):
                    return False
                    
        #=======================账户模式========================================
        if( TradeContext.__accMode__ != "2" ):
            
            #银行商户代码(商户号)
            TradeContext.bankUnitno = records[0][7]
            
            #主办分行号
            if(len(records[0][8])>0):
                TradeContext.mainZoneno = records[0][8]
                
            #主办网点号
            if(len(records[0][9])>0):
                TradeContext.mainBrno = records[0][9]


            #银行编码(商户给银行分配的编码)
            TradeContext.bankno       = records[0][15]
            
            #单位账号(accno1)
            TradeContext.__agentAccno__  = records[0][16]
            TradeContext.__agentAccno1__ = records[0][17]
            TradeContext.__agentAccno2__ = records[0][18]
            TradeContext.__agentAccno3__ = records[0][19]
            TradeContext.__agentAccno4__ = records[0][20]
            TradeContext.__agentAccno5__ = records[0][21]

        #=======================分支机构/分账户=================================
        if(TradeContext.__busiMode__ == '2' or TradeContext.__accMode__ == '2' ):
            #判断商户分支单位信息状态
            if( not ChkSubUnitStatus( ) ):
                return False

        else:
            if( not TradeContext.existVariable( "subUnitno" ) ):
                TradeContext.subUnitno='00000000'

        return True
        
    else:

        return AfaFlowControl.ExitThisFlow( 'A0003', '无单位信息' )



#=======================判断分支单位信息状态====================================
def ChkSubUnitStatus( ):

    AfaLoggerFunc.tradeInfo( '>>>判断子单位信息状态' )

    #=======================变量值的有效性校验==================================
    if( not TradeContext.existVariable( "subUnitno" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '分支单位代码[subUnitno]值不存在!' )

    #=======================子单位信息==========================================
    sqlStr = "SELECT * FROM AFA_SUBUNITADM WHERE SYSID = '" + TradeContext.sysId + "' AND UNITNO = '" + TradeContext.unitno + "' AND SUBUNITNO = '" + TradeContext.subUnitno + "' "

    AfaLoggerFunc.tradeInfo( sqlStr )

    subRecords = AfaDBFunc.SelectSql( sqlStr )
        
    if(subRecords == None ):
        return AfaFlowControl.ExitThisFlow( 'A0002', '子单位信息表操作异常:'+AfaDBFunc.sqlErrMsg )

    elif( len( subRecords )!=0 ):

        AfaUtilTools.ListFilterNone( subRecords )

        #单位名称
        TradeContext.subUnitName = subRecords[0][3]
        
        #单位简称
        TradeContext.subUnitSName = subRecords[0][4]

        #=======================业务模式========================================
        if(TradeContext.__busiMode__ == '2' ):
            
            #判断分支单位状态
            if( subRecords[0][5]=="0" ):
                return AfaFlowControl.ExitThisFlow( 'A0004', '该子单位处于关闭状态,不能做交易' )
                    
            elif( subRecords[0][5]=="2" ):
                return AfaFlowControl.ExitThisFlow( 'A0005', '该子单位处于暂停状态,不能做交易' )
                    
            elif( subRecords[0][5]=="3" ):
                return AfaFlowControl.ExitThisFlow( 'A0005', '该子单位处于未启用状态,不能做交易' )
                    
            #判断服务时间
            if( len(subRecords[0][8])==0 ):
                subRecords[0][8]='000000'
                
            if( len(subRecords[0][9])==0 ):
                subRecords[0][9]='000000'

            if( long( TradeContext.workTime )<long( subRecords[0][8] ) or long( TradeContext.workTime )>long( subRecords[0][9] ) ):
                return AfaFlowControl.ExitThisFlow( 'A0007', "超过该业务开放时间,请在每天["+subRecords[0][8]+"->"+subRecords[0][9]+"]做此业务" )


            #收取模式(0-不收费 1-模式一(逐笔收费) 2-模式二(汇总收费))
            TradeContext.__feeFlag__ = subRecords[0][10]
            
            
            #拆分特征码(1-签到校验标志 2-日终校验标志 3-对帐校验标志 4-响应码使用标志 5-子表使用标志 6-扩展模式 7-密钥使用标志)
            TradeContext.__agentEigen__ = subRecords[0][24]

            AfaLoggerFunc.tradeInfo( '::::::签到校验标志  =' + TradeContext.__agentEigen__[0] )
            AfaLoggerFunc.tradeInfo( '::::::日终校验标志  =' + TradeContext.__agentEigen__[1] )
            AfaLoggerFunc.tradeInfo( '::::::对帐校验标志  =' + TradeContext.__agentEigen__[2] )
            AfaLoggerFunc.tradeInfo( '::::::响应码使用标志=' + TradeContext.__agentEigen__[3] )
            AfaLoggerFunc.tradeInfo( '::::::子表使用标志  =' + TradeContext.__agentEigen__[4] )
            AfaLoggerFunc.tradeInfo( '::::::扩展模式      =' + TradeContext.__agentEigen__[5] )
            AfaLoggerFunc.tradeInfo( '::::::密钥使用标志  =' + TradeContext.__agentEigen__[6] )
            
            #判断是否是签到签退交易
            if( not TradeContext.existVariable( "__signFlag__" ) ):
                
                #检查签到标志
                if( TradeContext.__agentEigen__[0]=='1' and subRecords[0][25]=="0" ):
                    return AfaFlowControl.ExitThisFlow( 'A0008', '该子单位还没有签到,不能做此交易' )
                        
            else:
                if TradeContext.__signFlag__ == '1' :
                    
                    #签到
                    return SignIn( )
                        
                else:
                
                    #签退
                    return SignOut( )
                        
                        
            #检查日终标志
            if( TradeContext.__agentEigen__[1]=='1' and subRecords[0][26]=="1" ):
                return AfaFlowControl.ExitThisFlow( 'A0009', '该子单位已做日终操作,不能做此交易' )
                    
            #检查对帐标志
            if( TradeContext.__agentEigen__[2]=='1' and subRecords[0][28]=="1" ):
                return AfaFlowControl.ExitThisFlow( 'A0010', '该子单位已做对帐操作,不能做此交易' )
                    
            #响应码转换标志
            TradeContext.__respFlag__ = TradeContext.__agentEigen__[3]

            #密钥使用标志
            TradeContext.__keyFlag__ = TradeContext.__agentEigen__[6]


            #获取密钥使用标志
            if ( TradeContext.__keyFlag__=='1' ):
                if( not GetKeyInfo( ) ):
                    return False


            #获取收费使用标志
            if ( TradeContext.__feeFlag__=='1' ):
                if( not GetFeeInfo( ) ):
                    return False
                    
        #=======================账户模式========================================
        if(TradeContext.__accMode__ == '2' ):
            
            #主办分行号
            if(len(subRecords[0][12])>0):
                TradeContext.mainZoneno = subRecords[0][12]
                
            #主办网点号
            if(len(subRecords[0][13])>0):
                TradeContext.mainBrno = subRecords[0][13]
                
            #商户编码(银行给商户分配的编码)
            TradeContext.bankUnitno = subRecords[0][14]

            #银行编码(商户给银行分配的编码)
            TradeContext.bankno = subRecords[0][11]

            #单位账号
            TradeContext.__agentAccno__  = subRecords[0][15]
            TradeContext.__agentAccno1__ = subRecords[0][16]
            TradeContext.__agentAccno2__ = subRecords[0][17]
            TradeContext.__agentAccno3__ = subRecords[0][18]
            TradeContext.__agentAccno4__ = subRecords[0][19]
            TradeContext.__agentAccno5__ = subRecords[0][20]

        return True

    else:
        return AfaFlowControl.ExitThisFlow( 'A0002', '无子单位信息' )


#=======================应用签到================================================
def SignIn( ):
    
    ret=SignMode( '1' )
        
    if( ret < 1 ):
        return AfaFlowControl.ExitThisFlow( 'A0052', '签到失败' )
            
    return True


#=======================应用签退================================================
def SignOut( ):

    ret=SignMode( '0' )
        
    if( ret < 1 ):
        return AfaFlowControl.ExitThisFlow( 'A0052', '签退失败' )
            
    return True


#=======================应用签到/退=============================================
def SignMode( flag ):
    
    if(TradeContext.__busiMode__ != '2'):
        sql="UPDATE AFA_UNITADM SET LOGINSTATUS='"    + flag + "' WHERE SYSID='" + TradeContext.sysId + "' AND UNITNO='" + TradeContext.unitno + "'"
        
    else:
        sql="UPDATE AFA_SUBUNITADM SET LOGINSTATUS='" + flag + "' WHERE SYSID='" + TradeContext.sysId + "' AND UNITNO='" + TradeContext.unitno + "' AND SUBUNITNO='" + TradeContext.subUnitno+"'"

    return AfaDBFunc.UpdateSqlCmt( sql )


#=======================判断交易状态============================================
def ChkTradeStatus( ):

    AfaLoggerFunc.tradeInfo( '>>>判断交易状态' )
        
    #=======================变量值的有效性校验==================================
    if( not TradeContext.existVariable( "TransCode" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '交易代码[TransCode]值不存在!' )

    #系统标识
    sqlStr = "SELECT * FROM AFA_TRADEADM WHERE SYSID='" + TradeContext.sysId

    #单位代码=
    sqlStr = sqlStr + "' AND UNITNO='" + TradeContext.unitno

    #业务模式
    if(TradeContext.__busiMode__ == '2' ):
        #子单位代码
        sqlStr = sqlStr + "' AND SUBUNITNO='" + TradeContext.subUnitno

    #交易代码
    sqlStr = sqlStr + "' AND TRXCODE='" + TradeContext.TransCode + "'"

    #渠道代码
    sqlStr = sqlStr + "' AND CHANNELCODE='" + TradeContext.channelCode + "' OR CHANNELCODE='" + "00000" + "'"

    #地区号
    sqlStr = sqlStr + "' AND ZONENO='"   + TradeContext.zoneno    + "' OR ZONENO='"   + "00000" + "'"

    #网点号
    sqlStr = sqlStr + "' AND BRNO='"     + TradeContext.brno      + "' OR BRNO='"     + "00000" + "'"

    #柜员号
    sqlStr = sqlStr + "' AND TELLERNO='" + TradeContext.tellerno  + "' OR TELLERNO='" + "00000" + "'"

    AfaLoggerFunc.tradeInfo( sqlStr )

    records = AfaDBFunc.SelectSql( sqlStr )
        
    if( records == None ):
        return AfaFlowControl.ExitThisFlow( 'A0002', '交易信息管理表操作异常:'+AfaDBFunc.sqlErrMsg )

    elif( len( records )!=0 ):
        AfaUtilTools.ListFilterNone( records )
        
        #判断交易状态
        if( records[0][7]=="0" ):
            return AfaFlowControl.ExitThisFlow( 'A0004', '该交易处于未启用状态,不能做此交易' )
                
        elif( records[0][7]=="2" ):
            return AfaFlowControl.ExitThisFlow( 'A0005', '该交易处于关闭状态,不能做此交易' )

        elif( records[0][7]=="3" ):
            return AfaFlowControl.ExitThisFlow( 'A0006', '该交易处于停用状态,不能做此交易' )

        #判断服务时间
        if( long( TradeContext.workTime )<long( records[0][5] ) or long( TradeContext.workTime )>long( records[0][6] ) ):
            return AfaFlowControl.ExitThisFlow( 'A0007', "超过该交易开放时间,请在每天["+records[0][5]+"->"+records[0][6]+"]做此业务" )

        return True

    else:
        return AfaFlowControl.ExitThisFlow( 'A0007', '无此权限,不能做此交易' )


################################################################################
# 函数名:    ChkChannelStatus
# 参数:      无
# 返回值：    True  校验成功    False 校验失败
# 函数说明：  查询渠道信息表获取渠道的配置信息，一般为查询缴费或者取消交易使用    
################################################################################
def ChkChannelStatus( ):

    AfaLoggerFunc.tradeInfo( '>>>判断渠道状态' )
        
    #=======================变量值的有效性校验==================================
    if( not TradeContext.existVariable( "channelCode" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '渠道代码[channelCode]值不存在!' )
            
    #系统标识
    sqlStr = "SELECT * FROM AFA_CHANNELADM WHERE SYSID='" + TradeContext.sysId
    
    #单位代码
    sqlStr = sqlStr + "' AND UNITNO='" + TradeContext.unitno
    
    #业务模式
    if(TradeContext.__busiMode__ == '2' ):
        
        #子单位代码
        sqlStr = sqlStr + "' AND SUBUNITNO='" + TradeContext.subUnitno
        
    #业务方式
    sqlStr = sqlStr + "' AND AGENTFLAG='" + TradeContext.agentFlag

    #业务地区号
    if(TradeContext.__channelMode__ == '0' ):
        sqlStr = sqlStr + "' AND ZONENO='" + '00000'
    else:
        sqlStr = sqlStr + "' AND ZONENO='" + TradeContext.zoneno

        if(TradeContext.__channelMode__ == '2' ):

            #业务支行号
            sqlStr = sqlStr + "' AND ZHNO='" + TradeContext.zhno

    #渠道代码
    sqlStr = sqlStr + "' AND CHANNELCODE='" + TradeContext.channelCode + "'"

    AfaLoggerFunc.tradeInfo( sqlStr )

    records = AfaDBFunc.SelectSql( sqlStr )
    if( records == None ):
        return AfaFlowControl.ExitThisFlow( 'A0002', '渠道信息表操作异常:'+AfaDBFunc.sqlErrMsg )

    elif( len( records )!=0 ):
        AfaUtilTools.ListFilterNone( records )

        #=======================判断业务状态====================================
        if( records[0][14]=="0" ):
            return AfaFlowControl.ExitThisFlow( 'A0004', '该业务渠道处于未启用状态,不能做此交易' )

        elif( records[0][14]=="2" ):
            return AfaFlowControl.ExitThisFlow( 'A0005', '该业务渠道处于关闭状态,不能做此交易' )
                
        elif( records[0][14]=="3" ):
            return AfaFlowControl.ExitThisFlow( 'A0006', '该业务渠道处于停用状态,不能做此交易' )


        #=======================外围系统网点号/出纳员号=========================
        if( TradeContext.channelCode != '005' ):
            if(len(records[0][7])==0):
                return AfaFlowControl.ExitThisFlow( 'A0006', '外围系统行所号为空,不能做此交易' )
            else:
                TradeContext.__agentBrno__=records[0][7]

            if(len(records[0][8])==0):
                return AfaFlowControl.ExitThisFlow( 'A0006', '外围系统出纳员号为空,不能做此交易' )
            else:
                TradeContext.__agentTeller__=records[0][8]

                
        #渠道单笔交易额度
        if(len(records[0][9])==0):
            TradeContext.__chanlMaxAmount__ = '0'
        else:
            TradeContext.__chanlMaxAmount__=records[0][9]
            
        AfaLoggerFunc.tradeInfo( '::::::渠道单笔额度  =' + TradeContext.__chanlMaxAmount__ )

        #渠道日累计交易额度
        if(len(records[0][10])==0):
            TradeContext.__chanlTotalAmount__ = '0'
        else:
            TradeContext.__chanlTotalAmount__=records[0][10]
            
        AfaLoggerFunc.tradeInfo( '::::::渠道累计额度  =' + TradeContext.__chanlTotalAmount__ )

        #检查渠道交易额度
        if(not ChkAmtStatus('2')):
            return False

                
        #发票保存标志
        TradeContext.__billSaveCtl__=records[0][11]
        AfaLoggerFunc.tradeInfo( '::::::发票保存标志  =' + TradeContext.__billSaveCtl__ )

        #自动冲帐标志
        TradeContext.__autoRevTranCtl__=records[0][12]
        AfaLoggerFunc.tradeInfo( '::::::自动冲帐标志  =' + TradeContext.__autoRevTranCtl__ )

        #异常交易检测标志
        TradeContext.__errChkCtl__=records[0][13]
        AfaLoggerFunc.tradeInfo( '::::::异常检测标志  =' + TradeContext.__errChkCtl__ )

        #自动检查帐户类型
        TradeContext.__autoChkAcct__=records[0][15]
        AfaLoggerFunc.tradeInfo( '::::::异常检测标志  =' + TradeContext.__autoChkAcct__ )


        if( TradeContext.channelCode != "005" ):
            
            #外围发起的交易,如果没有上送网点柜员号,从表中获取
            
            #网点号
            if( not TradeContext.existVariable( "brno" ) or len( TradeContext.brno ) == 0 ):
                TradeContext.brno=TradeContext.__agentBrno__
                
            #柜员号
            if( not TradeContext.existVariable( "tellerno" ) or len( TradeContext.tellerno ) == 0 ):
                TradeContext.tellerno  = TradeContext.__agentTeller__
                TradeContext.cashTelno = TradeContext.__agentTeller__


        #异常交易检测
        if( TradeContext.__errChkCtl__ == '1' and ( not ( TradeContext.existVariable( 'revTranF' ) and TradeContext.revTranF == '1' ) ) ):

            iRetCode = ChkAbnormal( )
            if( iRetCode == -1 ):
                TradeContext.errorCode, TradeContext.errorMsg='A0035', '检测异常交易失败'+AfaDBFunc.sqlErrMsg
                return False

            if( iRetCode == 1 ):
                TradeContext.errorCode, TradeContext.errorMsg='A0036', '这类业务存在异常交易,请使用异常交易进行处理'
                return False


        #如果需要自动检查帐户类型,调用相应函数,只有正交易作此判断
        if( TradeContext.existVariable('revTranF') and TradeContext.revTranF=='0' and TradeContext.existVariable('accno') and TradeContext.__autoChkAcct__=='1' ):
            if ( GetAccType( TradeContext.accno ) == 0 ):
                TradeContext.errorCode, TradeContext.errorMsg='A0037', '没有对应的帐户种类信息'
                return False

        return True
        
    else:
        return AfaFlowControl.ExitThisFlow( 'A0003', '无渠道配置信息' )


################################################################################
# 函数名:    ChkAbnormal
# 参数:      无
# 返回值：    0  无异常交易    1  有异常交易    -1  查询流水表检测异常失败
# 函数说明：  按柜员查询流水表中的主机异常交易 
################################################################################
def ChkAbnormal( ):

    AfaLoggerFunc.tradeInfo( '>>>查询流水表中的异常交易' )

    #业务方式(01-代收 02-代付 03-批扣 04-批付)
    if (TradeContext.agentFlag=='01' or TradeContext.agentFlag=='03'):
        sqlStr = "SELECT COUNT(*) FROM AFA_MAINTRANSDTL WHERE WORKDATE='"
        sqlStr = sqlStr + TradeContext.workDate + "' AND SYSID='" + TradeContext.sysId
        sqlStr = sqlStr + "' AND ZONENO='"+TradeContext.zoneno+"' AND BRNO='"+TradeContext.brno
        sqlStr = sqlStr + "' AND TELLERNO='"+TradeContext.tellerno+"' AND REVTRANF='0' AND (BANKSTATUS='2' OR (BANKSTATUS='0' AND CORPSTATUS IN ('1', '2','3')))"
       
    else:
        sqlStr = "SELECT COUNT(*) FROM AFA_MAINTRANSDTL WHERE WORKDATE='"
        sqlStr = TradeContext.workDate + "' AND SYSID='" + TradeContext.sysId
        sqlStr = sqlStr + "' AND ZONENO='"+TradeContext.zoneno+"' AND BRNO='"+TradeContext.brno
        sqlStr = sqlStr + "' AND TELLERNO='"+TradeContext.tellerno+"' AND REVTRANF='0' AND (CORPSTATUS='2' OR (CORPSTATUS='0' AND BANKSTATUS IN ('1', '2','3')))"


    #单位代码
    sqlStr = sqlStr + " AND UNITNO='" + TradeContext.unitno

    #业务模式
    if(TradeContext.__busiMode__ == '2' ):
        #子单位代码
        sqlStr = sqlStr + "' AND SUBUNITNO='" + TradeContext.subUnitno
        
    #渠道代码
    sqlStr = sqlStr + "' AND CHANNELCODE='" + TradeContext.channelCode + "'"

    AfaLoggerFunc.tradeInfo( sqlStr )

    result=AfaDBFunc.SelectSql( sqlStr )
    if( result == None ):
        #查询流水表检测异常失败
        return -1
        
    if( result[0][0]!=0 ):
        #有异常交易
        return 1
        
    else:
        #无异常交易
        return 0


################################################################################
# 函数名:    GetAccType
# 参数:      卡账号
# 返回值：    0  失败    1  成功
# 函数说明：  自动判断账户类型
################################################################################
def GetAccType( card ):

    AfaLoggerFunc.tradeInfo( '>>>获取账户类型' )
        
    cardlen=len( card )
    i=2
    #比较函数
    def signCompare( x, card ):
        if not x[i] or card[( x[i+1]-1 ):( x[i+1]-1+x[i+2] )]==x[i]:
            return 1
        else:
            return 0
    sqlstr = "SELECT SEQNO,ACCLEN,EIGENSTR1,STARTBIT1,LEN1,EIGENSTR2,STARTBIT2,LEN2,EIGENSTR3,STARTBIT3,LEN3,"
    sqlstr = sqlstr + "EIGENSTR4,STARTBIT4,LEN4,EIGENSTR5,STARTBIT5,LEN5,"
    sqlstr = sqlstr + "ACCTYPE FROM AFA_ACCTINFO WHERE ACCLEN="+str(cardlen)+" ORDER BY SEQNO"

    AfaLoggerFunc.tradeInfo( sqlstr )
    
    a = AfaDBFunc.SelectSql( sqlstr )
    if a:
        for i in range( i, len( a[0] )-1, 3 ):                                  #注意i会多加一次后才会失败
            for x in a:
                a=[x for x in a if signCompare( x, card )]                      #在a中循环筛取符合条件的元素，并重新放在a中    
        if len( a )<1: 
            TradeContext.errorCode, TradeContext.errorMsg='A0020', '无法判断该账号类型,请检查输入账号'
            return 0                                                            #如果为[] 则返回0
        elif len( a )==1:                                                       #如果只有一条符合记录 则返回该条记录的acctype
            TradeContext.accType=a[0][17]
            return 1
        else:                                                                    #处理包含有子类的情况
            for i in range( i, 2, -3 ):
                    for x in a:
                        if x[i]:
                            a=[x]
            TradeContext.accType=a[0][17]
            return 1
    else:
        TradeContext.errorCode, TradeContext.errorMsg='A0025', '无对应账号类型,请检查输入账号:['+AfaDBFunc.sqlErrMsg+']'
        return 0


################################################################################
# 函数名:    ChkActStatus
# 参数:      无
# 返回值：    0  失败    1  成功
# 函数说明：  校验缴费介质的合法性
################################################################################
def ChkActStatus( ):

    AfaLoggerFunc.tradeInfo( '>>>校验缴费介质的合法性' )

    #=======================变量值的有效性校验==================================
    if( not TradeContext.existVariable( "accType" ) or len(TradeContext.accType)==0 ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '缴费介质代码[accType]值不存在!' )
            
    #系统标识
    sqlStr = "SELECT * FROM AFA_ACTNOADM WHERE SYSID='" + TradeContext.sysId
    
    #单位代码
    sqlStr = sqlStr + "' AND UNITNO='" + TradeContext.unitno
    
    #业务模式
    if(TradeContext.__busiMode__ == '2' ):
        
        #子单位代码
        sqlStr = sqlStr + "' AND SUBUNITNO='" + TradeContext.subUnitno
        
    #业务方式
    sqlStr = sqlStr + "' AND AGENTFLAG='" + TradeContext.agentFlag
    

    #=======================缴费介质管理模式====================================
   
    #地区号
    if(TradeContext.__actnoMode__ == '0' ):
        sqlStr = sqlStr + "' AND ZONENO='" + "00000"
    else:
        sqlStr = sqlStr + "' AND ZONENO='" + TradeContext.zoneno

        #业务支行号
        if(TradeContext.__actnoMode__ == '2' ):
            sqlStr = sqlStr + "' AND ZHNO='" + TradeContext.zhno

    #渠道代码
    sqlStr = sqlStr + "' AND CHANNELCODE='" + TradeContext.channelCode
    
    
    #缴费介质代码
    sqlStr = sqlStr + "' AND ACTTYPECODE='" + TradeContext.accType + "'"


    AfaLoggerFunc.tradeInfo( sqlStr )


    records = AfaDBFunc.SelectSql( sqlStr )
    if( records == None ):
        return AfaFlowControl.ExitThisFlow( 'A0002', '缴费介质信息表操作异常:'+AfaDBFunc.sqlErrMsg )
            
    elif( len( records )!=0 ):
        AfaUtilTools.ListFilterNone( records )
            
        #判断业务状态
        if( records[0][10]=="0" ):
            return AfaFlowControl.ExitThisFlow( 'A0004', '该缴费介质没有开通,不能做此交易' )
                
        TradeContext.__chkAccPwdCtl__= records[0][8]
        TradeContext.__enpAccPwdCtl__= records[0][9]
        
        return True

    else:
        return AfaFlowControl.ExitThisFlow( 'A0003', '没有开通相应的缴费介质' )




################################################################################
# 函数名:    ChkAmtStatus
# 参数:      chkType:1.按应用系统统计检查;2.按应用系统的渠道统计检查
# 返回值：    False  失败    True  成功
# 函数说明：  检查应用系统当日发生额度
################################################################################
def ChkAmtStatus(chkType=''):

    if(not TradeContext.existVariable( "revTranF" ) or TradeContext.revTranF!='0'):
        return True

    AfaLoggerFunc.tradeInfo( '>>>额度校验' )

    #检查系统单笔交易额度
    if (chkType=='1'):
        if (long(TradeContext.__sysMaxAmount__)>0 and long(float(TradeContext.amount)*100)>long(TradeContext.__sysMaxAmount__)) :
            return AfaFlowControl.ExitThisFlow( 'A0004', '交易金额不能大于系统定义的单笔最大交易金额[' + TradeContext.__sysMaxAmount__ + ']' )
                
    #检查系统渠道单笔交易额度
    elif (chkType=='2'):
        if(long(TradeContext.__chanlMaxAmount__)>0 and long(float(TradeContext.amount)*100)>long(TradeContext.__chanlMaxAmount__) ):
            return AfaFlowControl.ExitThisFlow( 'A0004', '交易金额不能大于系统渠道定义的单笔最大交易金额[' + TradeContext.__chanlMaxAmount__ + ']' )


    #=======================检查系统日累计交易额度==============================
    if (chkType=='1' and long(TradeContext.__sysTotalamount__)>0):
        sqlStr = "SELECT SUM(CAST(AMOUNT AS DECIMAL(17,2))) FROM AFA_MAINTRANSDTL WHERE SYSID = '" + TradeContext.sysId + "' AND REVTRANF = '0' "

        AfaLoggerFunc.tradeInfo( sqlStr )

        records = AfaDBFunc.SelectSql( sqlStr )
            
        if( records == None ):
            return AfaFlowControl.ExitThisFlow( 'A0002', '流水表表操作异常:'+AfaDBFunc.sqlErrMsg )
                
        records=AfaUtilTools.ListFilterNone( records )
            
        if( type(records[0][0]) is StringType ):
            records[0][0]=0

        if(long(TradeContext.__sysTotalamount__)<long(records[0][0])+long(float(TradeContext.amount)*100)):
            return AfaFlowControl.ExitThisFlow( 'A0004', '交易金额不能大于系统定义的日交易额度[' + TradeContext.__sysTotalamount__ + ']' )


    #=======================检查渠道日累计交易额度==============================
    elif (chkType=='2' and long(TradeContext.__chanlTotalAmount__)>0):
        
        sqlStr = "SELECT SUM(CAST(AMOUNT AS DECIMAL(17,2))) FROM AFA_MAINTRANSDTL WHERE SYSID = '" + TradeContext.sysId + "' AND REVTRANF = '0"
        
        
        #单位代码
        sqlStr = sqlStr + "' AND UNITNO = '" + TradeContext.unitno
        
        
        #业务模式
        if(TradeContext.__busiMode__ == '2' ):
            #子单位代码
            sqlStr = sqlStr + "' AND SUBUNITNO = '" + TradeContext.subUnitno
        
            
        #业务方式
        sqlStr = sqlStr + "' AND AGENTFLAG = '" + TradeContext.agentFlag
        
        
        #业务地区号
        if(TradeContext.__channelMode__ == '0' ):
            sqlStr = sqlStr + "' AND ZONENO = '" + '00000'
        else:
            sqlStr = sqlStr + "' AND ZONENO = '" + TradeContext.zoneno
            
            if(TradeContext.__channelMode__ == '2' ):
                #业务支行号
                sqlStr = sqlStr + "' AND ZHNO = '" + TradeContext.zhno

        #渠道代码
        sqlStr = sqlStr + "' AND CHANNELCODE = '" + TradeContext.channelCode + "'"
        
        
        AfaLoggerFunc.tradeInfo( sqlStr )


        records = AfaDBFunc.SelectSql( sqlStr )
            
            
        if( records == None ):
            return AfaFlowControl.ExitThisFlow( 'A0002', '流水表表操作异常:'+AfaDBFunc.sqlErrMsg )
              
                
        records=AfaUtilTools.ListFilterNone( records )
        if( type(records[0][0]) is StringType ):
            records[0][0]=0


        if(long(TradeContext.__chanlTotalAmount__)<long(records[0][0])+long(float(TradeContext.amount)*100)):
            return AfaFlowControl.ExitThisFlow( 'A0004', '交易金额不能大于系统渠道定义的日交易额度[' + TradeContext.__chanlTotalAmount__ + ']' )


    return True

################################################################################
# 函数名:    RespCodeMsg
# 参数:      outcode:外部响应码
# 返回值：    0  失败    1  成功
# 函数说明：  根据外部响应码获取外部响应信息
################################################################################
def RespCodeMsg( outcode ):

    AfaLoggerFunc.tradeInfo( '>>>转帐主机响应码' )

    sqlStr="SELECT * FROM AFA_RESPCODE WHERE SYSID='HOST' AND ORESPCODE='" + outcode + "'"
    
    AfaLoggerFunc.tradeInfo( sqlStr )

    records=AfaDBFunc.SelectSql( sqlStr )
    if( records == None ):
        return AfaFlowControl.ExitThisFlow( 'A0002', '响应码信息表操作异常:'+AfaDBFunc.sqlErrMsg )
            
    elif( len( records ) != 0 ):
        AfaUtilTools.ListFilterNone( records )
        TradeContext.__irespCode__=records[0][3]
        AfaLoggerFunc.tradeInfo( '主机返回码:['+outcode+']['+TradeContext.__irespCode__+']' )
        return records[0][5]

    else:
        return AfaFlowControl.ExitThisFlow( 'A0003', '响应码信息表没有相应记录' )

    return True

################################################################################
# 函数名:    GetRespMsg
# 参数:      outcode:外部响应码
# 返回值：    0  失败    1  成功
# 函数说明：  根据外部响应码获取外部响应信息
################################################################################
def GetRespMsg( outcode ):

    AfaLoggerFunc.tradeInfo( '>>>转帐外部响应码' )
        
    AfaLoggerFunc.tradeInfo( '>>>入口=' + outcode)

    sqlStr="SELECT IRESPCODE,RESPMSG FROM AFA_RESPCODE WHERE SYSID='" + TradeContext.sysId + "' AND UNITNO = '" + TradeContext.unitno + "' AND ORESPCODE='" + outcode + "'"

    AfaLoggerFunc.tradeInfo( sqlStr )

    records=AfaDBFunc.SelectSql( sqlStr )
        
    if( records == None ):
        return AfaFlowControl.ExitThisFlow( 'A0002', '响应码信息表操作异常:'+AfaDBFunc.sqlErrMsg )
            
    elif( len( records )!=0 ):
        AfaUtilTools.ListFilterNone( records )

        TradeContext.errorCode = records[0][0]
        TradeContext.errorMsg  = records[0][1]
        AfaLoggerFunc.tradeInfo( '返回码:['+outcode+']['+TradeContext.errorCode+']['+TradeContext.errorMsg+']' )

    else:

        TradeContext.errorCode=outcode
        TradeContext.errorMsg ='未知错误'

        AfaLoggerFunc.tradeInfo( '未找到响应码信息，返回码:['+TradeContext.errorCode+'][未知错误]' )

    return True

################################################################################
# 函数名:    GetTradeName
# 参数:      fileName:文件名
# 返回值：    0  失败    temp  变量数组
# 函数说明：  读取文件中的变量名
################################################################################
def GetTradeName( fileName ):

    temp=[]
    try:
        testFile=open( fileName, 'r' )
        for y in testFile.readlines( ):
            temp.append( y.replace( '\n', '' ) )
        testFile.close( )
        return temp
    except Exception, e:
        AfaLoggerFunc.tradeError(str(e))
        return 0



################################################################################
# 函数名:    autoPackData
# 参数:      无
# 返回值：    True 成功
# 函数说明：  自动打包
################################################################################
def autoPackData( ):

    AfaLoggerFunc.tradeInfo( '>>>自动打包' )

    #抛出监控数据
    SendUpdData()

    if( not TradeContext.existVariable( "tradeResponse" ) or not TradeContext.tradeResponse ):
        
        TradeContext.tradeResponse=[]
        
        #平台内部报文
        names = TradeContext.getNames( )
        for name in names:
            if ( not name.startswith( '__' ) and name != 'tradeResponse' ) :
                value = getattr( TradeContext, name )
                if( type( value ) is StringType ) :
                    TradeContext.tradeResponse.append( [name, value] )
                elif( type( value ) is ListType ) :
                    for elem in value:
                        if type(elem) is not str :
                            AfaLoggerFunc.tradeInfo( 'autoPackData  [value is not sting]')
                            continue
                        TradeContext.tradeResponse.append( [name, elem] )
                           
        #第三方返回报文
        names = Party3Context.getNames( )
        for name in names:
            if ( name.startswith( 'dn_' ) ) :
                value = getattr( Party3Context, name )
                if( type( value ) is StringType ) :
                    TradeContext.tradeResponse.append( [name, value] )
                elif( type( value ) is ListType ) :
                    for elem in value:
                        TradeContext.tradeResponse.append( [name, elem] )
        
    else:
        return False
        
    return True



#=======================查询类变量值的有效性校验==========================
def Query_ChkVariableExist( ):

    AfaLoggerFunc.tradeInfo( '>>>查询类变量值的有效性校验' )
        
    if( not TradeContext.existVariable( "sysId" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '系统标识[sysId]值不存在!' )

    if( not TradeContext.existVariable( "agentFlag" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '业务方式[agentFlag]值不存在!' )


    if( not TradeContext.existVariable( "channelCode" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '渠道代码[channelCode]值不存在!' )

    if( TradeContext.channelCode == '005' ):
        if( not TradeContext.existVariable( "zoneno" ) ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '分行号[zoneno]值不存在!' )

        if( not TradeContext.existVariable( "brno" ) ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '行所号[brno]值不存在!' )

        if( not TradeContext.existVariable( "tellerno" ) ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '行所号[tellerno]值不存在!' )

    return True

#=======================缴费类变量值的有效性校验==========================
def Pay_ChkVariableExist( ):

    AfaLoggerFunc.tradeInfo( '>>>缴费类变量值的有效性校验' )
        
    if( not TradeContext.existVariable( "sysId" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '系统标识[sysId]值不存在!' )


    if( not TradeContext.existVariable( "agentFlag" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '业务方式[agentFlag]值不存在!' )


    if( not TradeContext.existVariable( "channelCode" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '渠道代码[channelCode]值不存在!' )


    if( TradeContext.channelCode == '005' ):
        if( not TradeContext.existVariable( "zoneno" ) ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '分行号号[zoneno]值不存在!' )
                
        if( not TradeContext.existVariable( "brno" ) ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '行所号[brno]值不存在!' )
                
        if( not TradeContext.existVariable( "tellerno" ) ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '柜员号[tellerno]值不存在!' )
                
        if( not TradeContext.existVariable( "cashTelno" ) ):
            TradeContext.cashTelno = TradeContext.tellerno

    if( not TradeContext.existVariable( "operno" ) ):
        TradeContext.operno='00000'
        
        
    if( not TradeContext.existVariable( "zhno" ) or len( TradeContext.zhno ) == 0 ):
        TradeContext.zhno='00000'


    if( not TradeContext.existVariable( "amount" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '金额[amount]值不存在!' )


    if( not TradeContext.existVariable( "userno" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '用户号[userno]值不存在!' )


    if( not TradeContext.existVariable( "accno" ) ):
        TradeContext.accType='000'


    TradeContext.revTranF='0'

    return True



#=======================取消交易变量值的有效性校验==========================
def Cancel_ChkVariableExist( ):

    AfaLoggerFunc.tradeInfo( '>>>取消交易变量值的有效性校验' )
        
    if( not TradeContext.existVariable( "sysId" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '系统标识[sysId]值不存在!' )


    if( not TradeContext.existVariable( "agentFlag" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '代理业务方式[agentFlag]值不存在!' )


    if( not TradeContext.existVariable( "channelCode" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '渠道代码[channelCode]值不存在!' )

    if( TradeContext.channelCode == '005' ):
        if( not TradeContext.existVariable( "zoneno" ) ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '分行号[zoneno]值不存在!' )
                
        if( not TradeContext.existVariable( "brno" ) ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '行所号[brno]值不存在!' )

        if( not TradeContext.existVariable( "tellerno" ) ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '柜员号[tellerno]值不存在!' )
                
        if( not TradeContext.existVariable( "cashTelno" ) ):
            TradeContext.cashTelno = TradeContext.tellerno


    if( not TradeContext.existVariable( "operno" ) ):
        TradeContext.operno='00000'

        
    if( not TradeContext.existVariable( "zhno" ) or len( TradeContext.zhno ) == 0 ):
        TradeContext.zhno='00000'


    if( not TradeContext.existVariable( "amount" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '金额[amount]值不存在!' )

            
    if( not TradeContext.existVariable( "preAgentSerno" ) and not TradeContext.existVariable( "preChannelSerno" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '原交易流水号[preAgentSerno或preChannelSerno]值不存在!' )


    if( not TradeContext.existVariable( "userno" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '用户号[userno]值不存在!' )


    if( not TradeContext.existVariable( "accno" ) ):
        TradeContext.accno=''
        TradeContext.accType='000'
        
        
    TradeContext.revTranF='1'
    
    
    return True

#===============校验反交易数据完整性,根据流水号比对用户号/帐号/交易金额=========
def ChkRevInfo( ):

    AfaLoggerFunc.tradeInfo( '>>>校验反交易数据完整性' )
        
    sqlstr = "SELECT REVTRANF,USERNO,CRACCNO,DRACCNO,AMOUNT,AGENTFLAG,ACCTYPE,TELLERNO,CASHTELNO,"
    sqlstr = sqlstr + "SUBUSERNO,SUBAMOUNT,USERNAME,VOUHTYPE,TERMID,"
    sqlstr = sqlstr + "VOUHNO,VOUHDATE,BANKSERNO,CORPSERNO,CORPTIME,NOTE1,NOTE2,NOTE3,NOTE4,NOTE5,NOTE6,"
    sqlstr = sqlstr + "NOTE7,NOTE8,NOTE9,NOTE10,AGENTSERIALNO,CURRTYPE,CURRFLAG FROM AFA_MAINTRANSDTL WHERE "
    
    iSernoFlag = 0
    if ( TradeContext.existVariable( "preAgentSerno" ) and len(TradeContext.preAgentSerno)>0 ) :
        sqlstr = sqlstr + " AGENTSERIALNO='"+TradeContext.preAgentSerno+"' AND "
        iSernoFlag = 1

    if ( TradeContext.existVariable( "preChannelSerno" ) and len(TradeContext.preChannelSerno)>0 ) :
        sqlstr = sqlstr + " CHANNELSERNO='"+TradeContext.preChannelSerno+"' AND "
        iSernoFlag = 2


    sqlstr = sqlstr + " WORKDATE='"+TradeContext.workDate+ "' AND BANKSTATUS='0' AND CORPSTATUS='0' "
    
    if ( iSernoFlag == 0 ):
        return AfaFlowControl.ExitThisFlow( 'A0025', '原中间业务流水号和企业流水号不能同时为空' )
            
    
    AfaLoggerFunc.tradeInfo( sqlstr )


    tmp = AfaDBFunc.SelectSql( sqlstr )
    if tmp == None :
        return AfaFlowControl.ExitThisFlow( 'A0025', AfaDBFunc.sqlErrMsg )
            
            
    elif len( tmp ) == 0 :
        return AfaFlowControl.ExitThisFlow( 'A0045', '未发现原交易' )


    tmp=AfaUtilTools.ListFilterNone( tmp )

    temp=tmp[0]
    if temp[0]!='0':                    #校验反交易标志
        return AfaFlowControl.ExitThisFlow( 'A0020', '无匹配信息反交易标志有误' )
            
            
    if temp[7]!=TradeContext.tellerno:  #校验柜员号
        return AfaFlowControl.ExitThisFlow( 'A0020', '柜员号不匹配' )
            
            
    if temp[8]!=TradeContext.cashTelno: #校验出纳员号
        return AfaFlowControl.ExitThisFlow( 'A0020', '出纳员号不匹配' )
            
            
    if temp[1]!=TradeContext.userno:    #校验用户号
        return AfaFlowControl.ExitThisFlow( 'A0020', '用户号不匹配' )       


    if temp[4]!=TradeContext.amount:    #校验金额
        return AfaFlowControl.ExitThisFlow( 'A0020', '金额不匹配' )
            
            
    TradeContext.__crAccno__  = temp[2]         #贷方账号
    TradeContext.__drAccno__  = temp[3]         #借方账号
    TradeContext.accType      = temp[6]         #账户类型
    TradeContext.subUserno    = temp[9]         #附加用户号
    TradeContext.subAmount    = temp[10]        #附加金额
    TradeContext.userName     = temp[11]        #用户名称
    TradeContext.vouhType     = temp[12]        #凭证种类
    TradeContext.termId       = temp[13]        #终端号
    TradeContext.vouhno       = temp[14]        #凭证号
    TradeContext.vouhDate     = temp[15]        #凭证日期
    TradeContext.bankSerno    = temp[16]        #银行流水
    TradeContext.corpSerno    = temp[17]        #企业流水
    TradeContext.corpTime     = temp[18]        #企业时间戳
    TradeContext.note1        = temp[19]        #备注1
    TradeContext.note2        = temp[20]        #备注2
    TradeContext.note3        = temp[21]        #备注3
    TradeContext.note4        = temp[22]        #备注4
    TradeContext.note5        = temp[23]        #备注5
    TradeContext.note6        = temp[24]        #备注6
    TradeContext.note7        = temp[25]        #备注7
    TradeContext.note8        = temp[26]        #备注8
    TradeContext.note9        = temp[27]        #备注9
    TradeContext.note10       = temp[28]        #备注10

    if ( iSernoFlag == 2 ):
        TradeContext.preAgentSerno= temp[29]    #原中间业务流水号

    TradeContext.currType     = temp[30]        #币种
    TradeContext.currFlag     = temp[31]        #钞汇标志

    return True



################################################################################
# 函数名:    GetBranchInfo
# 参数:      branchno
# 返回值：    False  失败;    成功返回list
# 函数说明：  获取行所信息
################################################################################
def GetBranchInfo(branchno=''):

    AfaLoggerFunc.tradeInfo( '>>>查询获取行所信息' )

    sqlStr="SELECT UPBRANCHNO,BRANCHCODE,TYPE,BRANCHNAMES,BRANCHNAME FROM AFA_BRANCH WHERE BRANCHNO='" + branchno + "'"

    AfaLoggerFunc.tradeInfo( sqlStr )

    records=AfaDBFunc.SelectSql( sqlStr )
        
    if( records == None ):
        return AfaFlowControl.ExitThisFlow( 'A0002', '查询机构号失败:'+AfaDBFunc.sqlErrMsg )
            
    elif ( len( records )==0):
        return AfaFlowControl.ExitThisFlow( 'A0002', '无法找到相应的机构号' )
            
    elif ( len( records )>1):
        return AfaFlowControl.ExitThisFlow( 'A0002', '查到多条机构号' )
            
    else:
        AfaUtilTools.ListFilterNone( records )
        TradeContext.__mngZoneno__   = records[0][0]
        TradeContext.__branchCode__  = records[0][1]
        TradeContext.__branchType__  = records[0][2]
        TradeContext.__branchNames__ = records[0][3]
        TradeContext.__branchName__  = records[0][4]
        
        AfaLoggerFunc.tradeInfo('管辖机构号:['+TradeContext.__mngZoneno__+']')

    return True


################################################################################
# 函数名:    GetSummaryInfo
# 参数:      无
# 返回值：    False  失败;    成功返回 True
# 函数说明：  获取主机摘要信息
################################################################################
def GetSummaryInfo( ):

    AfaLoggerFunc.tradeInfo( '>>>查询摘要代码信息' )

    sqlStr="SELECT SUMNO,SUMNAME FROM AFA_SUMMARY WHERE SYSID='" + TradeContext.sysId + "'"

    AfaLoggerFunc.tradeInfo( sqlStr )

    records=AfaDBFunc.SelectSql( sqlStr )

    if( records == None ):
        return AfaFlowControl.ExitThisFlow( 'A0002', '查询摘要代码信息失败:' + AfaDBFunc.sqlErrMsg )
            
    elif ( len( records )==0 ):
        TradeContext.__summaryCode__='258'
        TradeContext.__summaryName__='默认'

    elif ( len( records )>1):
        return AfaFlowControl.ExitThisFlow( 'A0002', '查到多条摘要代码信息' )

    else:
        AfaUtilTools.ListFilterNone( records )
        TradeContext.__summaryCode__=records[0][0]
        TradeContext.__summaryName__=records[0][1]

    AfaLoggerFunc.tradeInfo('>>>摘要代码:['+TradeContext.__summaryCode__+']')
    AfaLoggerFunc.tradeInfo('>>>摘要名称:['+TradeContext.__summaryName__+']')

    return True



################################################################################
# 函数名:    GetKeyInfo
# 参数:      无
# 返回值：    False  失败;    成功返回 True
# 函数说明：  获取密钥信息
################################################################################
def GetKeyInfo( ):

    AfaLoggerFunc.tradeInfo('>>>获取KEY信息')

    sqlStr = "SELECT KEY1,KEY2 FROM AFA_KEYADM WHERE SYSID='" + TradeContext.sysId + "' AND UNITNO='" + TradeContext.unitno +"'"


    if ( TradeContext.__busiMode__ == '2' ):
         sqlStr =  sqlStr + " AND SUBUNITNO='" + TradeContext.subUnitno +"'"
         
         
    AfaLoggerFunc.tradeInfo( sqlStr )


    records=AfaDBFunc.SelectSql( sqlStr )
    
    
    if( records == None ):
        return AfaFlowControl.ExitThisFlow( 'A0002', '查询密钥信息失败:' + AfaDBFunc.sqlErrMsg )
            
    elif ( len( records )==0 ):
        return AfaFlowControl.ExitThisFlow( 'A0002', '没有发现密钥信息' )

    elif ( len( records )>1):
        return AfaFlowControl.ExitThisFlow( 'A0002', '查到多条密钥信息' )

    else:
        AfaUtilTools.ListFilterNone( records )
        TradeContext.initKey = records[0][0]
        TradeContext.commKey = records[0][1]

    AfaLoggerFunc.tradeInfo('>>>initKey:[' + TradeContext.initKey + ']')

    AfaLoggerFunc.tradeInfo('>>>commKey:[' + TradeContext.commKey + ']')

    return True
    
    

################################################################################
# 函数名:    GetFeeInfo
# 参数:      无
# 返回值：    False  失败;    成功返回 True
# 函数说明：  获取费用信息
################################################################################
def GetFeeInfo( ):


    AfaLoggerFunc.tradeInfo('>>>获取费用信息')


    sqlStr = "SELECT FEEFLAG,AMOUNT FROM AFA_FEEADM WHERE SYSID='" + TradeContext.sysId + "' AND UNITNO='" + TradeContext.unitno +"'"


    if ( TradeContext.__busiMode__ == '2' ):
         sqlStr =  sqlStr + " AND SUBUNITNO='" + TradeContext.subUnitno +"'"


    AfaLoggerFunc.tradeInfo( sqlStr )


    records=AfaDBFunc.SelectSql( sqlStr )


    if( records == None ):
        return AfaFlowControl.ExitThisFlow( 'A0002', '查询费用信息失败:' + AfaDBFunc.sqlErrMsg )


    elif ( len( records )==0 ):
        return AfaFlowControl.ExitThisFlow( 'A0002', '无费用信息' )


    elif ( len( records )>1):
        return AfaFlowControl.ExitThisFlow( 'A0002', '查到多条费用信息' )


    else:
        AfaUtilTools.ListFilterNone( records )
            
        if ( records[0][0] == '1' ):
            TradeContext.__feeAmount__ = records[0][1]

            AfaLoggerFunc.tradeInfo('>>>逐笔收费:[' + TradeContext.__feeAmount__ + ']')
                
        else:
            AfaLoggerFunc.tradeInfo('>>>汇总收费:该模式目前不支持]')

        return True
    
    
    
################################################################################
# 函数名:    ChkMainbrno
# 参数:      psSysid,psUnitid,psSubUnitid,psBrno 业务代码，商户代码，分支商户代码，交易网点号
# 返回值：    False  失败;    成功返回list
# 函数说明：  判断psBrno是否为业务psSysid,psUnitid,psSubUnitid的主办网点
################################################################################
def ChkMainbrno(psSysid,psUnitid,psSubUnitid,psBrno):

    AfaLoggerFunc.tradeInfo( '>>>检查是否为主办行' )


    #系统标识
    sqlStr = "SELECT BRNO,BUSIMODE,ACCMODE FROM AFA_UNITADM WHERE SYSID = '" + psSysid + "' AND "
    
    
    #单位代码
    sqlStr = sqlStr + "UNITNO = '" + psUnitid + "'"    
    

    AfaLoggerFunc.tradeInfo( sqlStr )


    records=AfaDBFunc.SelectSql( sqlStr )
    if( records == None ):
        return AfaFlowControl.ExitThisFlow( 'A0002', '查询分行号失败:'+AfaDBFunc.sqlErrMsg )
            
            
    elif ( len( records )==0):
        return AfaFlowControl.ExitThisFlow( 'A0002', '无法找到相应的分行号或管辖分行号' )
            
            
    elif ( len( records )>1):
        return AfaFlowControl.ExitThisFlow( 'A0002', '查到多条分行号或管辖分行号记录' )
            
            
    else:
        if(records[0][1]=='2' or records[0][2]=='2'):
            
            #系统标识
            sqlStr = "SELECT BRNO FROM AFA_SUBUNITADM WHERE SYSID = '" + psSysid + "' AND "

            #单位代码
            sqlStr = sqlStr + "UNITNO = '" + psUnitid + "' AND SUBUNITNO = '" + psSubUnitid + "'"

            AfaLoggerFunc.tradeInfo( sqlStr )

            subrecords=AfaDBFunc.SelectSql( sqlStr )
            if( subrecords == None ):
                return AfaFlowControl.ExitThisFlow( 'A0002', '查询分行号失败:' + AfaDBFunc.sqlErrMsg )
                    
                    
            elif ( len( subrecords )==0):
                return AfaFlowControl.ExitThisFlow( 'A0002', '无法找到相应的分行号或管辖分行号' )
                    
                    
            elif ( len( subrecords )>1):
                return AfaFlowControl.ExitThisFlow( 'A0002', '查到多条分行号或管辖分行号记录' )
                    
                    
            else:
                AfaUtilTools.ListFilterNone( subrecords )
                if(psBrno==subrecords[0][0]):
                    return True
                    
        else:
            AfaUtilTools.ListFilterNone( records )
                
            if(psBrno==records[0][0]):
                return True
            
    return False    


################################################################################
# 函数名:    SendUpdData
# 返回值：   False-失败; True-成功
# 函数说明：  
################################################################################
def SendUpdData( ):

    try:

        AfaLoggerFunc.tradeInfo( '>>>抛出监控数据' )

        #拼装广播信息
        sndBuf = "oid=1.3.6.1.4.1.26350.1.6.6.6.6" + "|"


        #交易代码
        if( TradeContext.existVariable( "TemplateCode" ) and TradeContext.existVariable( "TransCode" ) ):
            #交易标识
            sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.1.1=" + TradeContext.TemplateCode + '-' + TradeContext.TransCode + "|"
        else:
            return False


        #系统编码
        if ( TradeContext.existVariable( "sysId" ) ):
            sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.1="  + TradeContext.sysId + "|"

            if (TradeContext.sysId=="RCC01"):
                TradeContext.sysCName = "农信银"

            elif (TradeContext.sysId=="AG2008"):
                TradeContext.sysCName = "非税收入"

        elif ( TradeContext.existVariable( "sysType" ) ):
            sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.1="  + TradeContext.sysType + "|"

            if (TradeContext.sysType=="abdt"):
                TradeContext.sysCName = "批量处理"

            elif (TradeContext.sysType=="vouh"):
                TradeContext.sysCName = "凭证管理"

        else:
            sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.1="  + "AG0000" + "|"      
            TradeContext.sysCName = "公共系统"


        #系统名称
        if( TradeContext.existVariable( "sysCName" ) ):
            sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.2="  + TradeContext.sysCName + "|"      
        else:
            sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.2="  + "" + "|"     



        #交易代码
        sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.3=" + TradeContext.TemplateCode + '-' + TradeContext.TransCode + "|"


        #交易名称
        if( TradeContext.existVariable( "TransName" ) ):
            sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.4="  + TradeContext.TransName + "|"      
        else:
            sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.4="  + "" + "|"


            
        #流水号
        if( TradeContext.existVariable( "agentSerialno" ) ):
            sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.5="  + TradeContext.agentSerialno + "|"     
             
        elif( TradeContext.existVariable( "BSPSQN" ) ):
            sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.5="  + TradeContext.BSPSQN + "|"     

        elif( TradeContext.existVariable( "SerialNo" ) ):
            sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.5="  + TradeContext.SerialNo + "|"     

        else:
            sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.5="  + "00000000" + "|"



        #交易日期
        if( TradeContext.existVariable( "workDate" ) ):
            sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.6="  + TradeContext.workDate + "|"      
        else:
            sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.6="  + UtilTools.GetSysDate( ) + "|"



        #交易时间
        if( TradeContext.existVariable( "workTime" ) ):
            sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.7="  + TradeContext.workTime + "|"      
        else:
            sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.7="  + UtilTools.GetSysTime( ) + "|"
            


        #机构号
        if( TradeContext.existVariable( "brno" ) ):
            sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.8="  + TradeContext.brno + "|"     
            
        elif ( TradeContext.existVariable( "BESBNO" ) ):
            sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.8="  + TradeContext.BESBNO + "|"     

        elif ( TradeContext.existVariable( "I1SBNO" ) ):
            sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.8="  + TradeContext.I1SBNO + "|"     

        else:
            sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.8="  + "0000000000" + "|"
            


        #柜员号
        if( TradeContext.existVariable( "tellerno" ) ):
            sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.9="  + TradeContext.tellerno + "|"      
            
        elif ( TradeContext.existVariable( "BETELR" ) ):
            sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.9="  + TradeContext.BETELR + "|"    

        elif ( TradeContext.existVariable( "I1USID" ) ):
            sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.9="  + TradeContext.I1USID + "|"    

        else:
            sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.9="  + "" + "|"


        #渠道编码
        if( TradeContext.existVariable( "channelCode" ) ):
            if TradeContext.channelCode=="001":
                sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.10="  + "自助终端"  + "|"   
                
            elif TradeContext.channelCode=="002":
                sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.10="  + "ATM"       + "|"   
                
            elif TradeContext.channelCode=="003":
                sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.10="  + "电话银行"  + "|"   
                
            elif TradeContext.channelCode=="004":
                sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.10="  + "网上银行"  + "|"   
                
            elif TradeContext.channelCode=="005":
                sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.10="  + "柜面"      + "|"   
                
            elif TradeContext.channelCode=="006":
                sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.10="  + "人工坐席"  + "|"   
                
            elif TradeContext.channelCode=="007":
                sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.10="  + "手机银行"  + "|"   
                
            elif TradeContext.channelCode=="008":
                sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.10="  + "企业"      + "|"   
                
            elif TradeContext.channelCode=="009":
                sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.10="  + "短信平台"  + "|"   
                
            elif TradeContext.channelCode=="010":
                sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.10="  + "POS"       + "|"   
                
            else:
                sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.10="  + ""          + "|"   
                
        else:
            sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.10="      + ""          + "|"


        #缴费介质
        if( TradeContext.existVariable( "accType" ) ):
            if TradeContext.accType=="000":
                sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.11="  + "现金"      + "|"      
                
            elif TradeContext.accType=="001":
                sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.11="  + "活期账号"  + "|"   
                
            elif TradeContext.accType=="002":
                sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.11="  + "借记卡"    + "|"   

            elif TradeContext.accType=="003":
                sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.11="  + "贷记卡"    + "|"   

            elif TradeContext.accType=="004":
                sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.11="  + "单位账号"  + "|"   

            elif TradeContext.accType=="005":
                sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.11="  + "公务卡"    + "|"   

            else:
                sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.11="  + ""          + "|"  

        else:
            sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.11="      + ""          + "|"



        #账号
        if( TradeContext.existVariable( "accno" ) ):
            sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.12="  + TradeContext.accno + "|"      
        else:
            sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.12="  + ""                 + "|"      



        #缴费金额
        if( TradeContext.existVariable( "amount" ) ):
            sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.13="  + TradeContext.amount + "|"      
        else:
            sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.13="  + "" + "|"
            

        #返回代码
        if( TradeContext.existVariable( "errorCode" ) ):
            sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.14="  + TradeContext.errorCode + "|"

        elif( TradeContext.existVariable( "tradeResponse" ) ):
            tmpErrorCode = ""
            for varlist in TradeContext.tradeResponse:
                if varlist[0] == 'errorCode':
                    tmpErrorCode = varlist[1]
                    break
            sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.14="  + tmpErrorCode + "|"
        else:
            sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.14="  + "" + "|"


        #返回信息
        if( TradeContext.existVariable( "errorMsg" ) ):
            sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.15="  + TradeContext.errorMsg + "|"      


        elif( TradeContext.existVariable( "tradeResponse" ) ):
            tmpErrorMsg = ""
            for varlist in TradeContext.tradeResponse:
                if varlist[0] == 'errorMsg':
                    tmpErrorMsg = varlist[1]
                    break
            sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.15="  + tmpErrorMsg + "|"
        else:
            sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.15="  + "" + "|"

        host     = "10.0.130.30"
        lhost    = "10.0.130.30"
        textport = "20089"

        #创建套接字
        sockfd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            port = int(textport)
    
        except ValueError:
            port = socket.getservbyname(textport, 'udp')

        #邦定IP
        sockfd.bind((lhost, 0))
            
        #创建连接
        sockfd.connect((host, port))
    
        #发送消息
        sockfd.sendall(sndBuf)
    
        #关闭连接(0-断开接收通道 1-断开发送通道 3-同时断开发送通道和接收通道)
        sockfd.close()
    
        return True
        
    except Exception, e:
        AfaLoggerFunc.tradeError(str(e))
        return False
