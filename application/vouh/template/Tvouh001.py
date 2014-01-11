# -*- coding: gbk -*-
###################################################################
#    文    件:    Tvouh001.py
#    说    明:    凭证管理-->凭证中心参数维护
#    环    境:    中间业务新平台（AFA）--- UNIX: AIX 5.3
#    作    者:    李亚杰
#    公    司:    北京赞同科技
#    创建地址:    安徽
#    创建时间:    2008年6月12日
#    维护纪录:
##################################################################
import TradeContext, AfaLoggerFunc, AfaUtilTools, AfaFunc, AfaFlowControl, AfaDBFunc
from types import *
import VouhFunc,HostContext,VouhHostFunc

#=============返回错误码,错误信息===================================
def tradeExit( code, msg ):
    TradeContext.errorCode, TradeContext.errorMsg=code, msg
    if code != '0000':
        return False
    return True

def main():
    AfaLoggerFunc.tradeInfo( '凭证中心参数维护['+TradeContext.TemplateCode+']进入' )
    
    #=============前台上送数据===================================
    #TradeContext.sBesbNo                                 机构号
    #TradeContext.sTellerNo                               柜员号
    #TradeContext.opeType                                 操作类型
    #TradeContext.sVouhType                               凭证种类
    #TradeContext.sVouhName                               凭证名称
    #TradeContext.sNum                                    重复次数
    

    #=============获取当前系统时间==========================
    TradeContext.sLstTrxDay  = AfaUtilTools.GetSysDate( )
    TradeContext.sLstTrxTime = AfaUtilTools.GetSysTime( )
        
    try:        
        #=============获取机构类型==========================
        HostContext.I1OTSB = TradeContext.sBesbNo         #机构号
        HostContext.I1SBNO = TradeContext.sBesbNo         #机构号
        HostContext.I1USID = TradeContext.sTellerNo       #柜员号
        HostContext.I1WSNO = TradeContext.sWSNO           #终端号
        
        if(not VouhHostFunc.CommHost('2001')):
            VouhFunc.tradeExit( TradeContext.errorCode, TradeContext.errorMsg )
            raise AfaFlowControl.flowException( )
        if(TradeContext.errorCode == '0000'):
            SBNO = HostContext.O1SBCH
            AfaLoggerFunc.tradeInfo( SBNO )
            
        #begin凭证优化更改LLJ  201109     
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
            TradeContext.sTellerTailNo    = TradeContext.sTellerTailNobak[0]                 #柜员尾箱号TradeContext.sTellerTailNo
            AfaLoggerFunc.tradeInfo( '柜员尾箱号：' + TradeContext.sTellerTailNo )   
        #end 
        
        #=============初始化返回报文变量========================
        TradeContext.tradeResponse = []
        
        #================拆包========================
        if(TradeContext.existVariable("sVouhType")):
            TradeContext.sVouhType = VouhFunc.DelSpace(TradeContext.sVouhType.split("|"))
            TradeContext.sNum = len(TradeContext.sVouhType)
        if(TradeContext.existVariable("sVouhName")):
            TradeContext.sVouhName  = VouhFunc.DelSpace(TradeContext.sVouhName.split("|"))
        AfaLoggerFunc.tradeInfo( '=================='+str(TradeContext.sNum) )
        
        #===========检查操作类型是否存在===========
        # 1 新增,2 删除, 3 修改, 4 查询
        if( not TradeContext.existVariable( "opeType" ) ):
            tradeExit( 'A005060', '操作类型[opeType]值不存在!' )
            raise AfaFlowControl.flowException( )

        if TradeContext.opeType == '1': #新增
        
            if(SBNO <> '33' and SBNO <> '02' ):
                tradeExit( 'A0001', '该机构柜员不能进行此操作!' )
                raise AfaFlowControl.flowException( )
        
            n=0
        
            for i in range(TradeContext.sNum):
                n=n+1
                #==========检查该凭证种类信息是否已经存在============
                sqlStr = "select VOUHTYPE from VOUH_PARAMETER \
                     where VOUHTYPE = '" + TradeContext.sVouhType[i] + "'\
                     and BESBNO = '" + TradeContext.sBesbNo + "'"
                AfaLoggerFunc.tradeInfo( 'sql = ' + sqlStr )
                records = AfaDBFunc.SelectSql( sqlStr )
                if( records == None ):
                    if(n>1):
                        AfaLoggerFunc.tradeInfo( '数据库回滚' )
                        AfaDBFunc.RollbackSql( )
                    tradeExit( 'A005052', '查询[凭证参数维护表]操作异常!' )
                    raise AfaFlowControl.flowException( )
                elif( len( records )!=0 ):
                    if(n>1):
                        AfaLoggerFunc.tradeInfo( '数据库回滚' )
                        AfaDBFunc.RollbackSql( )
                    tradeExit( 'A005053', '凭证种类已存在!' )
                    raise AfaFlowControl.flowException( )
                    
                #==========检查该凭证名称信息是否已经存在============
                sqlStr = "select VOUHNAME from VOUH_PARAMETER \
                     where trim(VOUHNAME) = trim('" + TradeContext.sVouhName[i] + "')\
                     and BESBNO = '" + TradeContext.sBesbNo + "'"
                AfaLoggerFunc.tradeInfo( 'sql = ' + sqlStr )
                records = AfaDBFunc.SelectSql( sqlStr )
                if( records == None ):
                    if(n>1):
                        AfaLoggerFunc.tradeInfo( '数据库回滚' )
                        AfaDBFunc.RollbackSql( )
                    tradeExit( 'A005052', '查询[凭证参数维护表]操作异常!' )
                    raise AfaFlowControl.flowException( )
                elif( len( records )!=0 ):
                    if(n>1):
                        AfaLoggerFunc.tradeInfo( '数据库回滚' )
                        AfaDBFunc.RollbackSql( )
                    tradeExit( 'A005053', '凭证名称已存在!' )
                    raise AfaFlowControl.flowException( )
                
                #=============初始化返回报文变量====================
                TradeContext.tradeResponse=[]
                sqlStr = "INSERT INTO VOUH_PARAMETER (BESBNO,VOUHTYPE,VOUHNAME,TELLERNO,ACTIVEDATE,STATUS) VALUES ('"+TradeContext.sBesbNo+"','"+\
                TradeContext.sVouhType[i]+"','"+TradeContext.sVouhName[i]+"','"+TradeContext.sTellerTailNo+"','"+TradeContext.sLstTrxDay+"','1')"
                
                AfaLoggerFunc.tradeInfo( sqlStr )
                records = AfaDBFunc.InsertSql( sqlStr )
                
                if records < 0 :
                    AfaLoggerFunc.tradeInfo( '数据库回滚' )
                    AfaDBFunc.RollbackSql( )
                    tradeExit( 'A005054', '新增[凭证号码表]基本信息失败!' )
                    raise AfaFlowControl.flowException( )
            #数据库提交
            AfaLoggerFunc.tradeInfo( '------------数据库提交' )
            AfaDBFunc.CommitSql( )
            
            TradeContext.tradeResponse.append( ['sNum',str(TradeContext.sNum)] )
            TradeContext.tradeResponse.append( ['sLstTrxDay',TradeContext.sLstTrxDay] )
            TradeContext.tradeResponse.append( ['sLstTrxTime',TradeContext.sLstTrxTime] )
            TradeContext.tradeResponse.append( ['errorCode','0000'] )
            TradeContext.tradeResponse.append( ['errorMsg','交易成功'] )

        if TradeContext.opeType == '3':  #删除
            
            if(SBNO <> '33' and SBNO <> '02' ):
                tradeExit( 'A0001', '该机构柜员不能进行此操作!' )
                raise AfaFlowControl.flowException( )
                
            n = 0
            for i in range(TradeContext.sNum):
                n=n+1
                sqlStr = "select * from VOUH_REGISTER \
                     where VOUHTYPE = '" + TradeContext.sVouhType[i]+ "' \
                     and VOUHSTATUS <> '6' \
                     and BESBNO = '"+TradeContext.sBesbNo+"'"
                records = AfaDBFunc.SelectSql( sqlStr )
                AfaLoggerFunc.tradeDebug(sqlStr)
                if( records == None ):
                    if(n>1):
                        AfaLoggerFunc.tradeInfo( '数据库回滚' )
                        AfaDBFunc.RollbackSql( )
                    tradeExit( 'A005060', '查询[凭证登记表]操作异常!'  )
                    raise AfaFlowControl.flowException( )
                elif( len( records ) > 0 ):
                    if(n>1):
                        AfaLoggerFunc.tradeInfo( '数据库回滚' )
                        AfaDBFunc.RollbackSql( )
                    tradeExit( 'A005061', '不能删除存在有效凭证的凭证参数!' )
                    raise AfaFlowControl.flowException( )
                sqlStr = "DELETE  FROM  VOUH_PARAMETER WHERE VOUHTYPE = '" + TradeContext.sVouhType[i]+ "'\
                     and BESBNO = '" + TradeContext.sBesbNo+ "'"
                
                AfaLoggerFunc.tradeDebug(sqlStr)
                records = AfaDBFunc.DeleteSql( sqlStr )
                if records == -1:
                    AfaLoggerFunc.tradeInfo( '数据库回滚' )
                    AfaDBFunc.RollbackSql( )
                    tradeExit( 'A005055', '删除[凭证参数维护表]操作异常!' )
                    raise AfaFlowControl.flowException( )
                if records == 0:
                    AfaLoggerFunc.tradeInfo( '数据库回滚' )
                    AfaDBFunc.RollbackSql( )
                    tradeExit( 'A005056', '[凭证参数维护表]内无对应记录可被删除!' )
                    raise AfaFlowControl.flowException( )
                
            #数据库提交
            AfaLoggerFunc.tradeInfo( '------------数据库提交' )
            AfaDBFunc.CommitSql( )
            
            TradeContext.tradeResponse.append( ['sNum',str(TradeContext.sNum)] )
            TradeContext.tradeResponse.append( ['sLstTrxDay',TradeContext.sLstTrxDay] )
            TradeContext.tradeResponse.append( ['sLstTrxTime',TradeContext.sLstTrxTime] )
            TradeContext.tradeResponse.append( ['errorCode','0000'] )
            TradeContext.tradeResponse.append( ['errorMsg','交易成功'] )

        if TradeContext.opeType == '2':#修改
        
            if(SBNO <> '33' and SBNO <> '02' ):
                tradeExit( 'A0001', '该机构柜员不能进行此操作!' )
                raise AfaFlowControl.flowException( )
                
            n=0     
            #==============修改凭证参数维护表=====================
            for i in range(TradeContext.sNum):
                n=n+1

                #==========检查该凭证名称信息是否已经存在============
                sqlStr = "select VOUHNAME from VOUH_PARAMETER \
                     where trim(VOUHNAME) = trim('" + TradeContext.sVouhName[i] + "')\
                     and BESBNO = '" + TradeContext.sBesbNo + "'"
                AfaLoggerFunc.tradeInfo( 'sql = ' + sqlStr )
                records = AfaDBFunc.SelectSql( sqlStr )
                if( records == None ):
                    if(n>1):
                        AfaLoggerFunc.tradeInfo( '数据库回滚' )
                        AfaDBFunc.RollbackSql( )
                    tradeExit( 'A005052', '查询[凭证参数维护表]操作异常!' )
                    raise AfaFlowControl.flowException( )
                elif( len( records )!=0 ):
                    if(n>1):
                        AfaLoggerFunc.tradeInfo( '数据库回滚' )
                        AfaDBFunc.RollbackSql( )
                    tradeExit( 'A005053', '凭证名称已存在!' )
                    raise AfaFlowControl.flowException( )
                
                sqlStr = "UPDATE VOUH_PARAMETER set \
                  VOUHNAME = '"+ TradeContext.sVouhName[i] + "'"
                sqlStr = sqlStr +" WHERE VOUHTYPE = '" + TradeContext.sVouhType[i] + "'\
                and BESBNO = '" + TradeContext.sBesbNo+ "'"
                
                records = AfaDBFunc.UpdateSql( sqlStr )
                if records==-1 :
                    AfaLoggerFunc.tradeInfo( '数据库回滚' )
                    AfaDBFunc.RollbackSql( )
                    tradeExit( 'A005057', '更新[凭证参数维护表]信息异常!' )
                    raise AfaFlowControl.flowException( )
                elif records==0 :
                    AfaLoggerFunc.tradeInfo( '数据库回滚' )
                    AfaDBFunc.RollbackSql( )
                    tradeExit( 'A005058', '修改[凭证参数维护表]基本信息失败!' )
                    raise AfaFlowControl.flowException( )
            #数据库提交
            AfaLoggerFunc.tradeInfo( '------------数据库提交' )
            AfaDBFunc.CommitSql( )
            
            TradeContext.tradeResponse.append( ['sNum',str(TradeContext.sNum)] )
            TradeContext.tradeResponse.append( ['sLstTrxDay',TradeContext.sLstTrxDay] )
            TradeContext.tradeResponse.append( ['sLstTrxTime',TradeContext.sLstTrxTime] )
            TradeContext.tradeResponse.append( ['errorCode','0000'] )
            TradeContext.tradeResponse.append( ['errorMsg','交易成功'] )

        if TradeContext.opeType == '4':#查询
              
            TradeContext.tradeResponse=[]
            sqlStr = "SELECT VOUHTYPE,VOUHNAME,BESBNO FROM VOUH_PARAMETER WHERE (SUBSTR(BESBNO,1,6) = '"+ (TradeContext.sBesbNo)[:6] +"' \
                    or BESBNO ='3400008887')"
            if (len(TradeContext.sVouhType)!=0 and len(TradeContext.sVouhType[0])!=0):
                sqlStr = sqlStr + " AND VOUHTYPE = '" + TradeContext.sVouhType[0] + "' AND STATUS = '1'"
            
            AfaLoggerFunc.tradeInfo( 'sqlStr = ' + sqlStr )
            records = AfaDBFunc.SelectSql( sqlStr )
            if( records == None ):
                TradeContext.tradeResponse.append( ['retCount','0'] )
                tradeExit( 'A005052', '查询[凭证参数维护表]操作异常!'  )
                raise AfaFlowControl.flowException( )
            elif( len( records )==0 ):
                TradeContext.tradeResponse.append( ['retCount','0'] )
                tradeExit( 'A005059', '查询[凭证参数维护表]基本信息不存在!' )
                raise AfaFlowControl.flowException( )
            else:
                records=AfaUtilTools.ListFilterNone( records )

                sTotal=len( records )
                sVouhType = ''
                sVouhName = ''
                sBESBNO = ''
                for i in range( 0, len( records ) ):
                    if( i <> 0):
                        strSplit = '|'
                    else:
                        strSplit = ''
                    sVouhType = sVouhType + strSplit + records[i][0]
                    sVouhName = sVouhName + strSplit + records[i][1]
                    sBESBNO = sBESBNO + strSplit + records[i][2]
                
                TradeContext.tradeResponse.append( ['sVouhType',sVouhType] )
                TradeContext.tradeResponse.append( ['sVouhName',sVouhName] )
                TradeContext.tradeResponse.append( ['sBESBNO',sBESBNO] )
                TradeContext.tradeResponse.append( ['sLstTrxDay',TradeContext.sLstTrxDay] )
                TradeContext.tradeResponse.append( ['sLstTrxTime',TradeContext.sLstTrxTime] )
                TradeContext.tradeResponse.append( ['sTotal',str(sTotal)] )
                TradeContext.tradeResponse.append( ['errorCode','0000'] )
                TradeContext.tradeResponse.append( ['errorMsg','查询成功'] )

                tradeExit('0000', '查询成功')

        #自动打包
        AfaFunc.autoPackData()

        #=============程序退出=========================================
        AfaLoggerFunc.tradeInfo( '凭证中心参数维护['+TradeContext.TemplateCode+']退出' )
    except AfaFlowControl.flowException, e:
        AfaFlowControl.exitMainFlow( )
    except AfaFlowControl.accException:
        AfaFlowControl.exitMainFlow( )
    except Exception, e:
        AfaFlowControl.exitMainFlow(str(e))
