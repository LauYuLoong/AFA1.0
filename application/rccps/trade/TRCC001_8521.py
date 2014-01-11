# -*- coding: gbk -*-
##################################################################
#   农信银.查询打印业务.来张凭证打印
#=================================================================
#   程序文件:   TRCC001_8521.py
#   修改时间:   2008-06-05
##################################################################
#   修改人:     关彬捷
#   修改时间:   20080731
#   修改内容:   对于已被退汇的来账业务,
#               返回挂账状态的主机日期,主机流水号,待销账序号等
#               
##################################################################
#   修改人  ：  刘雨龙
#   修改时间：  2008-09-17
#   修改内容：  删除修改所留多余注释,
#               添加程序阅读必要注释,使程序更易读
#
##################################################################
import rccpsDBFunc,rccpsDBTrcc_trcbka,rccpsDBTrcc_sstlog,rccpsDBTrcc_bilinf,TradeContext,AfaLoggerFunc,AfaFlowControl,AfaUtilTools,AfaDBFunc
from types import *
from rccpsConst import *
import rccpsState

def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***农信银系统: 往账.本地类操作交易[RCC001_8521]进入***' )

    #=====判断输入接口值是否存在====
    if(not TradeContext.existVariable("OPRTYPNO")):
        return AfaFlowControl.ExitThisFlow('A099', '业务种类[OPRTYPNO]不存在')
    if(not TradeContext.existVariable("PRTFLG")):
        return AfaFlowControl.ExitThisFlow('A099', '打印标志[PRTFLG]不存在')
    if(not TradeContext.existVariable("BJEDTE")):
        return AfaFlowControl.ExitThisFlow('A099', '交易日期[BJEDTE]不存在')
    if(not TradeContext.existVariable("BSPSQN")):
        return AfaFlowControl.ExitThisFlow('A099', '报单序号[BSPSQN]不存在')

    #=====PL_TRCCO_HP 21 汇票====    
    if(TradeContext.OPRTYPNO==PL_TRCCO_HP):
        AfaLoggerFunc.tradeInfo("进入汇票处理")
        
        #=====查询数据库====
        records = {}
        ret = rccpsDBFunc.getTransBil(TradeContext.BJEDTE,TradeContext.BSPSQN,records)
        if( ret == False):
            return AfaFlowControl.ExitThisFlow('A099', '无此数据')
        
        AfaLoggerFunc.tradeInfo("结束数据库查询")
        
        #=====判断是否为签发机构====
        AfaLoggerFunc.tradeInfo("开始判断当前机构是否为交易机构")
        if( records['BESBNO'] != TradeContext.BESBNO ):
            return AfaFlowControl.ExitThisFlow('S999', '未查找到数据')
            
        AfaLoggerFunc.tradeInfo("结束判断当前机构是否为交易机构")
               
        #=====判断当前业务是否为来帐====
        AfaLoggerFunc.tradeInfo("开始判断当前业务是否为来帐")
        if( records['BRSFLG'] == PL_BRSFLG_SND ):
            return AfaFlowControl.ExitThisFlow('S999', '该笔业务为往账业务,请使用[8522 往账凭证补打]交易打印')
        
        AfaLoggerFunc.tradeInfo("结束判断当前业务是否为来帐")
        
        #=====判断当前状态====
        AfaLoggerFunc.tradeInfo("开始判断当前状态")
#        if( records['BCSTAT'] != PL_MBRTRCST_ACSUC and records['BCSTAT'] != PL_BCSTAT_AUTO ):
#            return AfaFlowControl.ExitThisFlow('A099', "当前状态["+records['BCSTAT']+"]不允许打印")
        #=====pgt 0925 将记账成功改为自动挂账，来帐没有记账，增加判断交易成功的判断====
#        if( records['BCSTAT'] != PL_BCSTAT_HANG and records['BCSTAT'] != PL_BCSTAT_AUTO and records['BDWFLG'] != PL_BDWFLG_SUCC ):
#            return AfaFlowControl.ExitThisFlow('A099', "当前状态["+records['BCSTAT']+"]不允许打印")
        if not ((records['BCSTAT'] == PL_BCSTAT_HANG and records['BDWFLG'] == PL_BDWFLG_SUCC) or (records['BCSTAT'] == PL_BCSTAT_AUTO and records['BDWFLG'] == PL_BDWFLG_SUCC)):
            return AfaFlowControl.ExitThisFlow('A099', "当前状态["+records['BCSTAT']+"]["+records['BDWFLG']+"]不允许打印")
            
        AfaLoggerFunc.tradeInfo("结束判断当前状态")
        
        #=====判断打印状态====
        AfaLoggerFunc.tradeInfo("开始判断当前业务的打印状态")
        if(TradeContext.PRTFLG == "0" and int(records['PRTCNT']) > 0):   #打印，打印次数大于0
            return AfaFlowControl.ExitThisFlow('A099','打印次数大于1，请选择补打' )
        
        if(TradeContext.PRTFLG == "1" and int(records['PRTCNT']) == 0):  #补打，打印次数为0
            return AfaFlowControl.ExitThisFlow('A099','打印次数为0，请选择打印' ) 
            
        AfaLoggerFunc.tradeInfo("结束判断当前业务的打印状态")
        
        #=====查询汇票信息登记簿====
        AfaLoggerFunc.tradeInfo("开始查询汇票信息登记簿")
        bilinf_record = {}
        ret = rccpsDBFunc.getInfoBil(records['BILVER'],records['BILNO'],records['BILRS'],bilinf_record)
        if( ret == False ):
            return AfaFlowControl.ExitThisFlow('S999','查询汇票信息登记簿失败' ) 
        AfaLoggerFunc.tradeInfo("结束查询汇票信息登记簿")
        
        #=====输出接口====
        AfaLoggerFunc.tradeInfo("开始向输出接口赋值")
        TradeContext.PRTDAT     = AfaUtilTools.GetHostDate()     #打印日期
        TradeContext.PRTTIM     = AfaUtilTools.GetSysTime()      #打印时间
        TradeContext.BJEDTE     = records['BJEDTE']              #交易日期
        TradeContext.BSPSQN     = records['BSPSQN']              #报单序号
        TradeContext.BJETIM     = records['BJETIM']              #交易时间
        TradeContext.TRCCO      = records['TRCCO']               #交易代码
        TradeContext.OPRATTNO   = records['OPRATTNO']            #业务熟悉
        TradeContext.TRCDAT     = records['TRCDAT']              #委托日期
        TradeContext.TRCNO      = records['TRCNO']               #交易流水号          
        TradeContext.OCCAMT     = str(bilinf_record['BILAMT'])	 #交易金额        
        TradeContext.BILNO      = records['BILNO']               #汇票号码            
        TradeContext.PYRACC     = bilinf_record['PYRACC']        #付款人账号  
        TradeContext.PYRNAM     = bilinf_record['PYRNAM']        #付款人名称      
        TradeContext.PYRADDR    = bilinf_record['PYRADDR']       #付款人地址      
        TradeContext.PYEACC     = bilinf_record['PYEACC']        #收款人账号      
        TradeContext.PYENAM     = bilinf_record['PYENAM']        #收款人名称      
        TradeContext.PYEADDR    = bilinf_record['PYEADDR']       #收款人地址  
        TradeContext.SEAL       = bilinf_record['SEAL']          #汇票密压            
        TradeContext.TRDT       = records['TRDT']                #主机日期
        TradeContext.TLSQ       = records['TLSQ']                #主机流水号
        TradeContext.ACC1       = records['SBAC']                #借方账号
        TradeContext.ACC2       = records['RBAC']                #贷方账号
        TradeContext.ACC3       = ""                             #备用账号
        TradeContext.DASQ       = records['DASQ']                #销账序号
        TradeContext.SNDBNKCO   = records['SNDBNKCO']            #发送行号
        TradeContext.SNDBNKNM   = records['SNDBNKNM']            #发送行名
        TradeContext.RCVBNKCO   = records['RCVBNKCO']            #接收行号
        TradeContext.RCVBNKNM   = records['RCVBNKNM']            #接收行名
        TradeContext.USE        = bilinf_record['USE']           #用途
        TradeContext.REMARK     = bilinf_record['REMARK']        #备注
        TradeContext.PRTCNT     = str(int(records['PRTCNT'])+1)  #打印次数
        TradeContext.CUR        = bilinf_record['CUR']           #币种
        TradeContext.OPRNO      = records['OPRNO']               #业务类型
        TradeContext.RMNAMT     = str(bilinf_record['RMNAMT'])   #结余余额
        TradeContext.OCCAMT1    = str(bilinf_record['OCCAMT'])   #实际结算金额
        TradeContext.PAYBNKCO   = bilinf_record['PAYBNKCO']      #代理兑付行行号
        TradeContext.PAYBNKNM   = bilinf_record['PAYBNKNM']      #代理兑付行行名
        
        AfaLoggerFunc.tradeInfo("结束向输出结构赋值")
        
        #=====更新打印标志====
        AfaLoggerFunc.tradeInfo("开始更新打印标志")
        
        update_dict={'PRTCNT':records['PRTCNT']+1} 
        where_dict={'BJEDTE':records['BJEDTE'],'BSPSQN':records['BSPSQN'],'BCSTAT':records['BCSTAT']}
        
        rownum=rccpsDBTrcc_sstlog.update(update_dict,where_dict)
        if(rownum<=0):
            AfaDBFunc.RollbackSql()
            return AfaFlowControl.ExitThisFlow('A099','更新打印次数失败' )        	
        
        AfaDBFunc.CommitSql()
        
        AfaLoggerFunc.tradeInfo("结束更新打印标志")         
        AfaLoggerFunc.tradeInfo("结束汇票处理")
        
    #=====PL_TRCCO_HD 20 汇兑====
    elif(TradeContext.OPRTYPNO==PL_TRCCO_HD):
        AfaLoggerFunc.tradeInfo("进入汇兑处理")
        
        #=====查询数据库====
        records = {}
        ret = rccpsDBFunc.getTransTrc(TradeContext.BJEDTE,TradeContext.BSPSQN,records)
        if(ret==False):
            return AfaFlowControl.ExitThisFlow('A099','无此数据' )
            
        #=====判断是否为签发机构====
        AfaLoggerFunc.tradeInfo("开始判断当前机构是否为交易机构")
        if( records['BESBNO'] != TradeContext.BESBNO ):
            return AfaFlowControl.ExitThisFlow('S999', '为查找到数据')
            
        AfaLoggerFunc.tradeInfo("结束判断当前机构是否为交易机构")
        
        #=====刘雨龙 20080702 判断当前业务是否为来账业务====
        if records['BRSFLG'] == PL_BRSFLG_SND:
            return AfaFlowControl.ExitThisFlow('S999','报单序号['+TradeContext.BSPSQN+']该笔业务为往账业务，不允许打印')
        
        #=====判断当前状态====
        #=====pgt 0925 增加判断交易成功的判断====
#        if records['BCSTAT'] != PL_BCSTAT_HANG and records['BCSTAT'] != PL_BCSTAT_AUTO and records['BCSTAT'] != PL_BCSTAT_QTR and records['BDWFLG'] != PL_BDWFLG_SUCC :
#            return AfaFlowControl.ExitThisFlow('A099',"当前状态[" + records['BCSTAT'] + "]不允许打印")
        if not ((records['BCSTAT'] == PL_BCSTAT_HANG and records['BDWFLG'] == PL_BDWFLG_SUCC) or (records['BCSTAT'] == PL_BCSTAT_AUTO and records['BDWFLG'] == PL_BDWFLG_SUCC) or (records['BCSTAT'] == PL_BCSTAT_QTR and records['BDWFLG'] == PL_BDWFLG_SUCC)):
            return AfaFlowControl.ExitThisFlow('A099',"当前状态[" + records['BCSTAT'] + "]["+records['BDWFLG']+"]不允许打印")
                
        if(TradeContext.PRTFLG == "0" and int(records['PRTCNT']) > 0):   #打印，打印次数大于0
            return AfaFlowControl.ExitThisFlow('A099','打印次数大于1，请选择补打' )
        
        if(TradeContext.PRTFLG == "1" and int(records['PRTCNT']) == 0):  #补打，打印次数为0
            return AfaFlowControl.ExitThisFlow('A099','打印次数未0，请选择打印' )
        
        AfaLoggerFunc.tradeInfo("判断打印标志结束")
        
        #=====输出接口====
        TradeContext.PRTDAT   =  AfaUtilTools.GetHostDate()     #打印日期
        TradeContext.PRTTIM   =  AfaUtilTools.GetSysTime()      #打印时间
        TradeContext.BJEDTE   =  records['BJEDTE']              #交易日期
        TradeContext.BSPSQN   =  records['BSPSQN']              #交易序号
        TradeContext.BJETIM   =  records['BJETIM']              #交易时间
        TradeContext.TRCCO    =  records['TRCCO']               #业务类型
        TradeContext.OPRATTNO =  records['OPRATTNO']            #业务属性
        TradeContext.TRCDAT   =  records['TRCDAT']              #委托日期
        TradeContext.TRCNO    =  records['TRCNO']               #交易流水号
        TradeContext.OCCAMT   =  str(records['OCCAMT'])         #交易金额
        TradeContext.BILNO    =  records['BILNO']               #汇票号码
        TradeContext.PYRACC   =  records['PYRACC']              #付款人账号
        TradeContext.PYRNAM   =  records['PYRNAM']              #付款人名称
        TradeContext.PYRADDR  =  records['PYRADDR']             #付款人地址
        TradeContext.PYEACC   =  records['PYEACC']              #收款人账号
        TradeContext.PYENAM   =  records['PYENAM']              #收款人名称
        TradeContext.PYEADDR  =  records['PYEADDR']             #收款人地址
        TradeContext.SEAL     =  records['SEAL']                #汇票密压
        
        #=====PL_BCSTAT_QTR  80 退汇====
        if records['BCSTAT'] == PL_BCSTAT_QTR:
            #=====退汇业务,返回挂账状态的状态详细信息====
            stat_dict = {}
            if not rccpsState.getTransStateSet(records['BJEDTE'],records['BSPSQN'],PL_BCSTAT_HANG,PL_BDWFLG_SUCC,stat_dict):
                return AfaFlowControl.ExitThisFlow('A099','查询交易自动挂账状态异常' )
            
            TradeContext.TRDT = stat_dict['TRDT']               #主机日期
            TradeContext.TLSQ = stat_dict['TLSQ']               #主机流水号
            TradeContext.ACC1 = stat_dict['SBAC']               #借方账号
            TradeContext.ACC2 = stat_dict['RBAC']               #贷方账号
            TradeContext.ACC3 = ""                              #备用账号
            TradeContext.DASQ = stat_dict['DASQ']               #销账序号
        else:
            #=====非退汇业务,返回当前状态的状态详细信息====
            TradeContext.TRDT = records['TRDT']	                #主机日期
            TradeContext.TLSQ = records['TLSQ']	                #主机流水号
            TradeContext.ACC1 = records['SBAC']                 #借方账号
            TradeContext.ACC2 = records['RBAC']                 #贷方账号
            TradeContext.ACC3 = ""                              #备用账号
            TradeContext.DASQ = records['DASQ']                 #销账序号
            
        TradeContext.SNDBNKCO = records['SNDBNKCO']             #发送行号
        TradeContext.SNDBNKNM = records['SNDBNKNM']             #发送行名
        TradeContext.RCVBNKCO = records['RCVBNKCO']             #接收行号
        TradeContext.RCVBNKNM = records['RCVBNKNM']             #接收行名
        TradeContext.USE      = records['USE']                  #用途
        TradeContext.REMARK   = records['REMARK']               #备注
        TradeContext.PRTCNT   = str(int(records['PRTCNT'])+1)   #打印次数
        TradeContext.OPRNO    = records['OPRNO']                #业务类型
        TradeContext.CUR      = records['CUR']                  #币种
        TradeContext.OCCAMT   = str(records['OCCAMT'])          #业务属性
        
        #=====更新打印标志====
        AfaLoggerFunc.tradeInfo("开始更新打印标志")
        
        update_dict={'PRTCNT':records['PRTCNT']+1}        
        where_dict={'BJEDTE':records['BJEDTE'],'BSPSQN':records['BSPSQN'],'BCSTAT':records['BCSTAT']}
        
        rownum=rccpsDBTrcc_sstlog.update(update_dict,where_dict)
        if(rownum<=0):
            AfaDBFunc.RollbackSql()
            return AfaFlowControl.ExitThisFlow('A099','更新打印次数失败' )        	
        
        AfaDBFunc.CommitSql()
    else:
        return AfaFlowControl.ExitThisFlow('A099','业务类型错')
        
    TradeContext.errorCode="0000"
    TradeContext.errorMsg="查询成功"
    
    AfaLoggerFunc.tradeInfo( '***农信银系统: 往账.本地类操作交易[RCC001_8521]退出***' )

    return True