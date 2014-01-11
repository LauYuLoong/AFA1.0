# -*- coding: gbk -*-
###################################################################
#    文    件:    Tvouh002.py
#    说    明:    凭证管理-->凭证入库
#    环    境:    中间业务新平台（AFA）--- UNIX: AIX 5.3
#    作    者:    李亚杰
#    公    司:    北京赞同科技
#    创建地址:    安徽
#    创建时间:    2008年6月11日 
#    维护纪录:   
##################################################################
import TradeContext, AfaLoggerFunc, AfaUtilTools, AfaFunc, AfaFlowControl, AfaDBFunc
from types import *
import VouhFunc,VouhHostFunc,HostContext

#=============返回错误码,错误信息===================================
def tradeExit( code, msg ):
    TradeContext.errorCode, TradeContext.errorMsg=code, msg
    if code != '0000':
        return False
    return True

def main( ):
    AfaLoggerFunc.tradeInfo( '凭证入库['+TradeContext.TemplateCode+']进入' )

    #=============前台上送数据===================================
    #TradeContext.sBesbNo                                 机构号
    #TradeContext.sCur                                    货币代码
    #TradeContext.sTellerNo                               柜员号
    #TradeContext.sVouhType                               凭证种类
    #TradeContext.sVouhName                               凭证名称
    #TradeContext.sStartNo                                起始号码
    #TradeContext.sEndNo                                  终止号码
    #TradeContext.sRivTeller                              对方柜员
    #TradeContext.sVouhStatus                             凭证状态
    #TradeContext.sVouhNum                                凭证数量
    #TradeContext.sLstTrxDay                              最后交易日期
    #TradeContext.sLstTrxTime                             最后交易时间
    #TradeContext.sDepository                             库箱标志
    #TradeContext.sVouhName                               凭证名称
    
    try:
        
        #================拆包========================
        TradeContext.sVouhType = VouhFunc.DelSpace(TradeContext.sVouhType.split("|")) 
        TradeContext.sVouhName = VouhFunc.DelSpace(TradeContext.sVouhName.split("|"))
        TradeContext.sStartNo  = VouhFunc.DelSpace(TradeContext.sStartNo.split("|"))
        TradeContext.sEndNo    = VouhFunc.DelSpace(TradeContext.sEndNo.split("|"))
        TradeContext.sVouhNum  = VouhFunc.DelSpace(TradeContext.sVouhNum.split("|"))
        TradeContext.sNum      = len(TradeContext.sVouhType)
        
        #==================暂存==================================
        TradeContext.rVouhType = VouhFunc.AddSplit(TradeContext.sVouhType)
        TradeContext.rVouhName = VouhFunc.AddSplit(TradeContext.sVouhName)
        TradeContext.rStartNo  = VouhFunc.AddSplit(TradeContext.sStartNo)
        TradeContext.rEndNo    = VouhFunc.AddSplit(TradeContext.sEndNo)
        TradeContext.rVouhNum  = VouhFunc.AddSplit(TradeContext.sVouhNum)
        
        #=============初始化返回报文变量========================
        TradeContext.tradeResponse = []
        
        #=============生成流水号========================
        TradeContext.sVouhSerial = VouhFunc.GetVouhSerial( )

        #=============获取当前系统时间==========================
        TradeContext.sLstTrxDay  = AfaUtilTools.GetSysDate( )
        TradeContext.sLstTrxTime = AfaUtilTools.GetSysTime( )

        #=============置凭证操作状态及库箱标志====================
        TradeContext.sDepository  = '1' #库箱标志   1.分行管理库 2.支行管理库 3.网点管理库 4.柜员凭证箱
        TradeContext.sExDepos     = ' ' #原库箱标志
        TradeContext.sVouhStatus  = '0' #状态       0.已入未发 
        TradeContext.sExStatus    = ' ' #原状态
        TradeContext.sRivTeller   = '   '     #对方柜员
        TradeContext.sTransType    = '凭证入库'
        
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
            AfaLoggerFunc.tradeInfo( '柜员尾箱号：' + TradeContext.sTellerTailNo ) 
        #end   
            
        #判断是否回滚
        n=0
        
        for i in range(TradeContext.sNum):

            #=============定义变量==========================
            sFlagBack   = '0'     #入库凭证终止号码与库中凭证的起始号码是否存在连续关系,'1':是;'0':否
            sFlagFront  = '0'     #入库凭证起始号码与库中凭证的终止号码是否存在连续关系,'1':是;'0':否

            n=n+1
        
            #============= 判断入库的起始号码是否小于等于终止号码============================
            if(int(TradeContext.sStartNo[i]) > int(TradeContext.sEndNo[i]) ):
                tradeExit('A005066', '入库起始号码不能大于终止号码!')
                raise AfaFlowControl.flowException( )
            
            #凭证优化更改201108
            #============= 查询分行凭证库中的凭证号段============================
            #sqlStr = "select STARTNO,ENDNO,VOUHSTATUS from VOUH_REGISTER WHERE VOUHTYPE = '"\
            #+ TradeContext.sVouhType[i] + "' and BESBNO = '" + TradeContext.sBesbNo + "' and CUR = '" + TradeContext.sCur+"'"
            sqlStr = "select STARTNO,ENDNO ,VOUHSTATUS from VOUH_REGISTER where VOUHTYPE ='" + TradeContext.sVouhType[i] + "'" 
            sqlStr = sqlStr + " and VOUHSTATUS != '1' and BESBNO = '" + TradeContext.sBesbNo + "' and CUR = '" + TradeContext.sCur+"'"
            #end
             
            AfaLoggerFunc.tradeDebug(sqlStr)
            records = AfaDBFunc.SelectSql( sqlStr )
            AfaLoggerFunc.tradeInfo(records)
            
            if( records == None ):
                tradeExit('A005061', '查询[凭证登记表]操作异常!')
                raise AfaFlowControl.flowException( )
            elif( len( records ) == 0 ):    #如果数据库中无对应记录则直接插入
                sqlStr = "insert into VOUH_REGISTER \
                (BESBNO,TELLERNO,DEPOSITORY,CUR,VOUHTYPE,STARTNO,ENDNO,RIVTELLER,VOUHSTATUS,\
                VOUHNUM,LSTTRXDAY,LSTTRXTIME) \
                values \
                ('"+TradeContext.sBesbNo+"','"+TradeContext.sTellerTailNo+"',\
                '"+TradeContext.sDepository+"','"+TradeContext.sCur+"','"+TradeContext.sVouhType[i]+"',\
                '"+TradeContext.sStartNo[i]+"','"+TradeContext.sEndNo[i]+"','"+TradeContext.sRivTeller+"',\
                '"+TradeContext.sVouhStatus+"','"+TradeContext.sVouhNum[i]+"',\
                '"+TradeContext.sLstTrxDay+"','"+TradeContext.sLstTrxTime+"')"
                AfaLoggerFunc.tradeDebug(sqlStr)
                records = AfaDBFunc.InsertSql( sqlStr )
                if records == -1 :
                    AfaLoggerFunc.tradeInfo( '数据库回滚' )
                    AfaDBFunc.RollbackSql( )
                    tradeExit('A005062', '凭证入库失败,凭证数据库操作失败!')
                    raise AfaFlowControl.flowException( )
                else:
                    tradeExit('0000', '凭证入库成功')       
            else :
                #判断入库的凭证起止号码与已入库的凭证号码是否有交集,其中records[x][0]
                #为已入库的终止号码;records[x][1]为已入库的起始号码,判断为有交集的情况为:
                #1.入库的终止号码大于等于已入库的起始号码,并且小于等于已入库的终止号码;
                #2.入库的起始号码大于等于已入库的起始号码,并且小于等于已入库的终止号码;
                #3.入库的终止号码大于等于已入库的终止号码,并且入库的起始号码小于等于已入库的起始号码
                for x in range( len(records) ):
                    sTmpStartNo  = records[x][0]
                    sTmpEndNo    = records[x][1]
                    sTmpVouhStat = records[x][2]
                    if ((int(TradeContext.sEndNo[i])<=int(sTmpEndNo) and int(TradeContext.sEndNo[i])>=int(sTmpStartNo)) \
                    or (int(TradeContext.sStartNo[i])>=int(sTmpStartNo) and int(TradeContext.sStartNo[i])<=int(sTmpEndNo)) \
                    or ( int(TradeContext.sEndNo[i])>=int(sTmpEndNo) and int(TradeContext.sStartNo[i])<=int(sTmpStartNo))):
                        if( n > 1 ):
                            AfaLoggerFunc.tradeInfo( '数据库回滚' )
                            AfaDBFunc.RollbackSql( )
                        tradeExit('A005063', '凭证入库失败,凭证库中存在本次入库的凭证!')
                        raise AfaFlowControl.flowException( )
                    elif ((int(TradeContext.sEndNo[i]) == (int(sTmpStartNo)-1)) and sTmpVouhStat == '0'):
                        sFlagBack = '1'          #无交集且后连续,置后连续标识
                        sOperDelNo = records[x][0]
                        sOperEndNo = records[x][1]
                    elif ((int(TradeContext.sStartNo[i]) == (int(sTmpEndNo)+1)) and sTmpVouhStat == '0'):
                        sFlagFront = '1'         #无交集且前连续,置前连续标识
                        sOperStartNo = records[x][0]
                #输入的凭证号码与库中同类型凭证存在后连续关系,则与相应的记录进行归并
                if (  sFlagBack == '1' and sFlagFront == '0'):
                    sTmpVouhNum = str( int(sTmpEndNo) - int(TradeContext.sStartNo[i]) + 1 )
                    sqlStr = "update VOUH_REGISTER set \
                    STARTNO = '" + TradeContext.sStartNo[i] + "', \
                    VOUHNUM = '"+ sTmpVouhNum + "',\
                    TELLERNO = '" + TradeContext.sTellerTailNo + "',\
                    LSTTRXDAY = '"+ TradeContext.sLstTrxDay + "',\
                    LSTTRXTIME = '" + TradeContext.sLstTrxTime + "'\
                    where ENDNO = '" + sOperEndNo + "' AND VOUHSTATUS = '"+TradeContext.sVouhStatus+"' \
                    AND VOUHTYPE = '" + TradeContext.sVouhType[i]+ "' AND BESBNO = '" + TradeContext.sBesbNo+ "' \
                    AND CUR = '" + TradeContext.sCur+"'"
                    
                    AfaLoggerFunc.tradeDebug(sqlStr)
                    records = AfaDBFunc.UpdateSql( sqlStr )
                    if records == -1 :
                        AfaLoggerFunc.tradeInfo( '数据库回滚' )
                        #回滚
                        AfaDBFunc.RollbackSql( )
                        tradeExit('A005064', '凭证入库失败,凭证数据库操作异常!')
                        raise AfaFlowControl.flowException( )
                    elif records == 0 :
                        AfaLoggerFunc.tradeInfo( '数据库回滚' )
                        #回滚
                        AfaDBFunc.RollbackSql( )
                        tradeExit('A005062', '凭证入库失败,凭证数据库操作失败!')
                        raise AfaFlowControl.flowException( )
                    else:
                        tradeExit('0000', '凭证入库成功')
            
                #输入的凭证号码与库中同类型凭证存在前连续关系,则与相应的记录进行归并
                elif (  sFlagFront == '1' and sFlagBack == '0' ):
                    sTmpVouhNum = str( int(TradeContext.sEndNo[i]) - int(sOperStartNo) + 1 )
                    sqlStr = "update VOUH_REGISTER set \
                    ENDNO = '" + TradeContext.sEndNo[i] + "', \
                    VOUHNUM = '" + sTmpVouhNum + "',\
                    TELLERNO = '" + TradeContext.sTellerTailNo+ "',\
                    LSTTRXDAY = '" + TradeContext.sLstTrxDay + "',\
                    LSTTRXTIME = '" + TradeContext.sLstTrxTime + "'\
                    where STARTNO = '" + sOperStartNo + "' AND VOUHSTATUS = '"+TradeContext.sVouhStatus+"' \
                    AND VOUHTYPE = '" + TradeContext.sVouhType[i]+ "' AND BESBNO = '" + TradeContext.sBesbNo + "' \
                    AND CUR ='"+ TradeContext.sCur+"'"
                    AfaLoggerFunc.tradeDebug(sqlStr)
                    records = AfaDBFunc.UpdateSql( sqlStr )
                    if records == -1 :
                        AfaLoggerFunc.tradeInfo( '数据库回滚' )
                        #回滚
                        AfaDBFunc.RollbackSql( )
                        tradeExit('A005064', '凭证入库失败,凭证数据库操作异常!')
                        raise AfaFlowControl.flowException( )
                    elif records == 0 :
                        AfaLoggerFunc.tradeInfo( '数据库回滚' )
                        #回滚
                        AfaDBFunc.RollbackSql( )
                        tradeExit('A005062', '凭证入库失败,凭证数据库操作失败!')
                        raise AfaFlowControl.flowException( )
                    else:
                        tradeExit('0000', '凭证入库成功')
            
                #输入的凭证号码与库中同类型凭证存在前/后连续关系,则与相应的记录进行归并
                elif (  sFlagBack == '1' and sFlagFront == '1' ):
                    sTmpVouhNum = str( int(sOperEndNo) - int(sOperStartNo) + 1 )
                    sqlStr = "update VOUH_REGISTER set \
                    ENDNO = '" + sOperEndNo + "', VOUHNUM = '" + sTmpVouhNum + "',\
                    TELLERNO = '" + TradeContext.sTellerTailNo + "',\
                    LSTTRXDAY = '" + TradeContext.sLstTrxDay + "',\
                    LSTTRXTIME = '" + TradeContext.sLstTrxTime + "'\
                    where STARTNO = '" + sOperStartNo + "' AND VOUHSTATUS = '"+TradeContext.sVouhStatus+"' \
                    AND VOUHTYPE = '" + TradeContext.sVouhType[i]+ "' AND BESBNO = '" + TradeContext.sBesbNo + "' \
                    AND CUR = '"+ TradeContext.sCur+"'"
                    AfaLoggerFunc.tradeDebug(sqlStr)
                    records = AfaDBFunc.UpdateSql( sqlStr )
                    if records == -1 or records == 0 :
                        AfaLoggerFunc.tradeInfo( '数据库回滚' )
                        #回滚
                        AfaDBFunc.RollbackSql( )
                        tradeExit('A005062', '凭证入库失败,凭证数据库操作失败!')
                        raise AfaFlowControl.flowException( )
                    else:      #归并成功后,删除归并后其余一条
                        sqlDel = "delete from VOUH_REGISTER \
                        where STARTNO = '" + sOperDelNo + "' AND VOUHSTATUS = '"+TradeContext.sVouhStatus+"' \
                        AND VOUHTYPE = '" + TradeContext.sVouhType[i]+ "' AND BESBNO ='"+ TradeContext.sBesbNo+"' \
                        AND CUR = '"+ TradeContext.sCur+"'"
                        AfaLoggerFunc.tradeDebug(sqlDel)
                        record = AfaDBFunc.DeleteSql( sqlDel )
                        if record == -1 or record == 0 :
                            AfaLoggerFunc.tradeInfo( '数据库回滚' )
                            record = AfaDBFunc.RollbackSql( )
                            tradeExit('A005062', '凭证入库失败,凭证数据库操作失败!')
                            raise AfaFlowControl.flowException( )
                        else:
                            tradeExit('0000', '凭证入库成功')
            
                #输入的凭证号码与库中同类型凭证不存在任何连续关系,则直接插入
                else:
                    sqlStr = "insert into VOUH_REGISTER \
                    (BESBNO,TELLERNO,DEPOSITORY,CUR,VOUHTYPE,STARTNO,ENDNO,RIVTELLER,VOUHSTATUS,\
                    VOUHNUM,LSTTRXDAY,LSTTRXTIME) \
                    values \
                    ('" + TradeContext.sBesbNo + "','" + TradeContext.sTellerTailNo + "',\
                    '"+TradeContext.sDepository+ "','" + TradeContext.sCur+"','"+ TradeContext.sVouhType[i]+"',\
                    '" + TradeContext.sStartNo[i] + "','" + TradeContext.sEndNo[i] + "','" + TradeContext.sRivTeller +"',\
                    '"+TradeContext.sVouhStatus+"','" + TradeContext.sVouhNum[i] + "',\
                    '" + TradeContext.sLstTrxDay + "','" + TradeContext.sLstTrxTime + "')"
                    AfaLoggerFunc.tradeDebug(sqlStr)
                    records = AfaDBFunc.InsertSql( sqlStr )
                    if records == -1 :
                        AfaLoggerFunc.tradeInfo( '数据库回滚' )
                        AfaDBFunc.RollbackSql( )
                        tradeExit('A005062', '凭证入库失败,凭证数据库操作失败!')
                        raise AfaFlowControl.flowException( )
                    else:
                        tradeExit('0000', '凭证入库成功')
    

        AfaLoggerFunc.tradeInfo( '------------更新凭证变更登记表' )
        #更新凭证变更登记表
        VouhFunc.VouhModify()
        
        #数据库提交
        AfaLoggerFunc.tradeInfo( '------------数据库提交' )
        AfaDBFunc.CommitSql( )
        
        #主机记账
        AfaLoggerFunc.tradeInfo( '------------主机记账' )
        TradeContext.sOperSty = '0'
        VouhHostFunc.VouhCommHost()
        TradeContext.sTranStatus = '0'
        AfaLoggerFunc.tradeInfo( '=======================12'+TradeContext.errorCode )
        #TradeContext.errorCode = '0000'
        if(TradeContext.errorCode <> '0000'):
            tmpErrorCode= TradeContext.errorCode
            tmpErrorMsg = TradeContext.errorMsg
        
            #冲正
            
            #=============置凭证操作状态及库箱标志====================
            TradeContext.sDepository  = '1' #库箱标志   1.分行管理库 2.支行管理库 3.网点管理库 4.柜员凭证箱
            TradeContext.sExDepos     = '1' #原库箱标志
            TradeContext.sVouhStatus  = '9' #状态       0.已入未发 9.欲出库
            TradeContext.sExStatus    = '0' #原状态
            TradeContext.sRivTeller   = '   '     #对方柜员
            TradeContext.sTransType    = '冲正'
            TradeContext.sInTellerTailNo  = TradeContext.sTellerTailNo
            TradeContext.sInBesbNo    = TradeContext.sBesbNo

            #交易公共部分    
            VouhFunc.VouhTrans()
            AfaDBFunc.CommitSql( )
            
            sqlDel = "delete from VOUH_REGISTER where VOUHSTATUS = '9'"
            AfaLoggerFunc.tradeDebug(sqlDel)
            record = AfaDBFunc.DeleteSqlCmt( sqlDel )
            if record == -1 or record == 0 :
                tradeExit('A005062', '冲正失败,凭证数据库操作失败!')
                raise AfaFlowControl.flowException( )
            else:
                AfaLoggerFunc.tradeInfo( '============================自动冲正！' )
                
            TradeContext.sTranStatus = '1'
            if(not TradeContext.existVariable( "HostSerno" )):
                TradeContext.HostSerno = ''    
            
            #更新流水表
            VouhFunc.ModifyVouhModify()
            
            tradeExit(tmpErrorCode, tmpErrorMsg)
            raise AfaFlowControl.flowException( )
         
        #更新流水表
        VouhFunc.ModifyVouhModify()        
        
        TradeContext.tradeResponse.append( ['sVouhSerial',TradeContext.sVouhSerial] )
        TradeContext.tradeResponse.append( ['sVouhType',TradeContext.rVouhType] )
        TradeContext.tradeResponse.append( ['sVouhName',TradeContext.rVouhName] )
        TradeContext.tradeResponse.append( ['sStartNo',TradeContext.rStartNo] )
        TradeContext.tradeResponse.append( ['sEndNo',TradeContext.rEndNo] )
        TradeContext.tradeResponse.append( ['sVouhNum',TradeContext.rVouhNum] )
        TradeContext.tradeResponse.append( ['sLstTrxDay',TradeContext.sLstTrxDay] )
        TradeContext.tradeResponse.append( ['sLstTrxTime',TradeContext.sLstTrxTime] )
        TradeContext.tradeResponse.append( ['sNum',str(TradeContext.sNum)] )
        TradeContext.tradeResponse.append( ['errorCode','0000'] )
        TradeContext.tradeResponse.append( ['errorMsg','查询成功'] )
        
            
            #自动打包
        AfaFunc.autoPackData()

        #=============程序退出====================
        AfaLoggerFunc.tradeInfo( '凭证入库['+TradeContext.TemplateCode+']退出' )
    except AfaFlowControl.flowException, e:
        AfaLoggerFunc.tradeInfo( '数据库回滚' )
        AfaDBFunc.RollbackSql( )
        AfaFlowControl.exitMainFlow( )
    except AfaFlowControl.accException:
        AfaLoggerFunc.tradeInfo( '数据库回滚' )
        AfaDBFunc.RollbackSql( )
        AfaFlowControl.exitMainFlow( )
    except Exception, e:
        AfaLoggerFunc.tradeInfo( '数据库回滚' )
        AfaDBFunc.RollbackSql( )
        AfaFlowControl.exitMainFlow(str(e))

