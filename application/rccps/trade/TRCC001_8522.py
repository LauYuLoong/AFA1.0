# -*- coding: gbk -*-
##################################################################
#   农信银.查询打印业务.往账凭证打印
#=================================================================
#   程序文件:   TRCC001_8522.py
#   修改时间:   2008-06-11
#   作者：      潘广通
##################################################################
#   修改人  ：  刘雨龙
#   修改时间：  2008-09-17
#   修改内容：  删除修改所留多余注释,
#               添加程序阅读必要注释,使程序更易读
#
##################################################################
#   修改人  ：  潘广通
#   修改时间：  2008-10-24
#   修改内容：  添加通存通兑部分
##################################################################
import TradeContext,AfaLoggerFunc,AfaFlowControl,AfaUtilTools,rccpsDBFunc,AfaDBFunc,rccpsDBTrcc_sstlog
from types import *
from rccpsConst import *
import rccpsMap8522DTrans2CTradeContext,rccpsMap8522DInfo2CTradeContext,rccpsMap8522DTransTrc2CTradeContext,rccpsMap8522Drecords2CTradeContext
import rccpsDBTrcc_bilbka,rccpsDBTrcc_sstlog,rccpsDBTrcc_trcbka,rccpsDBTrcc_wtrbka

def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***农信银系统: 往账.本地类操作交易[RCC001_8522]进入***' )
    
    #=====判断接口是否存在====
    if( not TradeContext.existVariable( "BJEDTE" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '交易日期[BJEDTE]不存在')        
    if( not TradeContext.existVariable( "BSPSQN" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '报单序号[BSPSQN]不存在')       
    if( not TradeContext.existVariable( "OPRTYPNO" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '业务种类[OPRTYPNO]不存在')       
    if( not TradeContext.existVariable( "BCURSQ" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '当前处理编号[BCURSQ]不存在')
        
    #=====查询历史状态表得到主机日期和主机流水号====
    
    where_sql={'BJEDTE':TradeContext.BJEDTE,'BSPSQN':TradeContext.BSPSQN,'BCURSQ':TradeContext.BCURSQ}
    
    ret=rccpsDBTrcc_sstlog.selectu(where_sql)
    if(ret==None):
        return AfaFlowControl.ExitThisFlow('A099', '查询历史状态表失败')
    if(len(ret)==0):
        return AfaFlowControl.ExitThisFlow('A099', '查询历史状态表结果为空')
    if(ret['TRDT']=="" or ret['TLSQ']==""):
        return AfaFlowControl.ExitThisFlow('A099', '此序号状态非成功的账务状态')
             
    #=====PL_TRCCO_HP 21 汇票====
    if(TradeContext.OPRTYPNO==PL_TRCCO_HP):
        AfaLoggerFunc.tradeInfo("进入汇票处理")

        records1={}
        #=====查询汇票业务登记簿====
        bilbka_where_dict = {'BJEDTE':TradeContext.BJEDTE,'BSPSQN':TradeContext.BSPSQN} 
        res_bilbka = rccpsDBTrcc_bilbka.selectu(bilbka_where_dict)  
        if( res_bilbka == None):
            return AfaFlowControl.ExitThisFlow('S999', '查询汇票交易登记簿失败')          
        if( len(res_bilbka) == 0 ):
            return AfaFlowControl.ExitThisFlow('S999', '查询汇票交易登记簿结果为空')
            
        #=====查询状态明细表====
        sstlog_where_dict = {'BJEDTE':TradeContext.BJEDTE,'BSPSQN':TradeContext.BSPSQN,'BCURSQ':TradeContext.BCURSQ}
        res_sstlog = rccpsDBTrcc_sstlog.selectu(sstlog_where_dict)
        if( res_sstlog == None):
            return AfaFlowControl.ExitThisFlow('S999', '查询历史状态登记簿失败')            
        if( len(res_sstlog) == 0):
            return AfaFlowControl.ExitThisFlow('S999', '查询历史状态登记簿结果为空')
            
        #=====给resords1赋值,字典相加赋值到新的字典====
        records1.update(res_bilbka)
        records1.update(res_sstlog)
        
        #=====判断是否为签发机构====
        AfaLoggerFunc.tradeInfo("开始判断当前机构是否为交易机构")

        if( records1['BESBNO'] != TradeContext.BESBNO ):
            return AfaFlowControl.ExitThisFlow('S999', '为查找到数据')
            
        AfaLoggerFunc.tradeInfo("结束判断当前机构是否为交易机构")   
        
        #=====判断是否为往账业务====
        if records1['BRSFLG'] != PL_BRSFLG_SND:
            return AfaFlowControl.ExitThisFlow('S999','报单序号['+TradeContext.BSPSQN+']该笔业务为来账业务，不允许打印')
        
#        #=====判断汇票状态，如果是撤销则不让打印====
#        if(records1['HPSTAT'] == PL_HPSTAT_CANC ):
#            return AfaFlowControl.ExitThisFlow('S999','此汇票为撤销状态，不允许打印')
        
        #=====判断当前状态====
        #=====PL_BCSTAT_ACC  20 记账====
        #=====PL_BCSTAT_HCAC 21 抹账====
        if(records1['BCSTAT']!=PL_BCSTAT_ACC and records1['BCSTAT']!=PL_BCSTAT_HCAC):
            return AfaFlowControl.ExitThisFlow('A009',"当前状态[" + records1['BCSTAT'] + "]不允许打印")
                
        records2={}
        #=====查询汇票信息登记簿====
        res=rccpsDBFunc.getInfoBil(records1['BILVER'],records1['BILNO'],records1['BILRS'],records2)
        if(res==False):
            return AfaFlowControl.ExitThisFlow('D003','汇票信息登记簿中无记录')    
        
        #=====输出接口====
        rccpsMap8522DTrans2CTradeContext.map(records1)
        rccpsMap8522DInfo2CTradeContext.map(records2)
        
        TradeContext.PRTDAT  =  AfaUtilTools.GetHostDate()          #打印日期
        TradeContext.PRTTIM  =  AfaUtilTools.GetSysTime()           #打印时间
        TradeContext.PRTCNT  =  str(int(TradeContext.PRTCNT)+1)     #打印次数
        TradeContext.BCSTAT  =  ret['BCSTAT']                       #当前状态
        TradeContext.BDWFLG  =  ret['BDWFLG']                       #流转处理标识
        TradeContext.TRDT    =  ret['TRDT']                         #主机日期
        TradeContext.TLSQ    =  ret['TLSQ']                         #主机流水
        TradeContext.OCCAMT  =  str(TradeContext.OCCAMT)            #交易金额
        TradeContext.BILAMT  =  str(TradeContext.BILAMT)            #出票金额
        TradeContext.RMNAMT  =  str(TradeContext.RMNAMT)            #结余金额
                
        #=====更新打印标志====
        AfaLoggerFunc.tradeInfo("开始更新打印标志")
        
        update_dict={'PRTCNT':TradeContext.PRTCNT}
        where_dict={'BJEDTE':TradeContext.BJEDTE,'BSPSQN':TradeContext.BSPSQN,'BCSTAT':TradeContext.BCSTAT}
        
        rownum=rccpsDBTrcc_sstlog.update(update_dict,where_dict)
        if(rownum<=0):
            AfaDBFunc.RollbackSql()
            return AfaFlowControl.ExitThisFlow('S999','修改数据库打印次数失败')
        else:
            AfaLoggerFunc.tradeDebug('>>>commit 成功')
        
        AfaDBFunc.CommitSql()
               
        TradeContext.errorCode="0000"
        TradeContext.errorMsg="查询成功"
       
    #=====PL_TRCCO_HD 20 汇兑====
    elif(TradeContext.OPRTYPNO==PL_TRCCO_HD):
        AfaLoggerFunc.tradeInfo("进入汇兑处理")

        records={}
        #=====查询汇兑登记簿====
        trcbka_where_dict = {'BJEDTE':TradeContext.BJEDTE,'BSPSQN':TradeContext.BSPSQN}
        res_trcbka = rccpsDBTrcc_trcbka.selectu(trcbka_where_dict)
        if( res_trcbka == None ):
            return AfaFlowControl.ExitThisFlow('S999', '查询汇兑登记簿异常')
            
        if( len(res_trcbka) == 0 ):
            return AfaFlowControl.ExitThisFlow('S999', '查询汇兑登记簿结果为空')
            
        #=====查询历史状态表====
        sstlog_where_dict = {'BJEDTE':TradeContext.BJEDTE,'BSPSQN':TradeContext.BSPSQN,'BCURSQ':TradeContext.BCURSQ}
        res_sstlog = rccpsDBTrcc_sstlog.selectu(sstlog_where_dict)
        if( res_sstlog == None):
            return AfaFlowControl.ExitThisFlow('S999', '查询历史状态登记簿失败')            
        if( len(res_sstlog) == 0):
            return AfaFlowControl.ExitThisFlow('S999', '查询历史状态登记簿结果为空')
            
        #=====给records赋值,字典相加赋值到新的字典====
        records.update(res_trcbka)
        records.update(res_sstlog)
        
        #=====判断是否为签发机构====
        AfaLoggerFunc.tradeInfo("开始判断当前机构是否为交易机构")
        if( records['BESBNO'] != TradeContext.BESBNO ):
            return AfaFlowControl.ExitThisFlow('S999', '非签发机构')
            
        AfaLoggerFunc.tradeInfo("结束判断当前机构是否为交易机构")
        
        #=====判断是否为往账业务====
        if records['BRSFLG'] != PL_BRSFLG_SND:
            return AfaFlowControl.ExitThisFlow('S999','报单序号['+TradeContext.BSPSQN+']该笔业务为来账业务，不允许打印')
        
        #=====判断当前状态====
        #=====PL_BCSTAT_ACC  20 记账====
        #=====PL_BCSTAT_HCAC 21 抹账====
        if not (records['BCSTAT']==PL_BCSTAT_ACC or records['BCSTAT'] == PL_BCSTAT_HCAC):
            return AfaFlowControl.ExitThisFlow('A009',"当前状态[" + records1['BCSTAT'] + "]不允许打印")
        
        rccpsMap8522DTransTrc2CTradeContext.map(records)
        
        #=====输出接口====
        TradeContext.PRTDAT  = AfaUtilTools.GetHostDate()       #打印日期
        TradeContext.PRTTIM  = AfaUtilTools.GetSysTime()        #打印时间
        TradeContext.PRTCNT  = str(int(TradeContext.PRTCNT)+1)  #打印次数
        TradeContext.OCCAMT  = str(TradeContext.OCCAMT)         #交易金额
        TradeContext.BILAMT  = str(TradeContext.COMAMT)	        #出票金额
        TradeContext.BCSTAT  = ret['BCSTAT']                    #当前状态
        TradeContext.BDWFLG  = ret['BDWFLG']                    #流转处理标识
        TradeContext.TRDT    = ret['TRDT']                      #主机日期
        TradeContext.TLSQ    = ret['TLSQ']                      #主机流水号
        
        #=====更新打印标志====
        AfaLoggerFunc.tradeInfo("开始更新打印标志")
        update_dict={'PRTCNT':TradeContext.PRTCNT}
        where_dict={'BJEDTE':TradeContext.BJEDTE,'BSPSQN':TradeContext.BSPSQN,'BCSTAT':TradeContext.BCSTAT}
        rownum=rccpsDBTrcc_sstlog.update(update_dict,where_dict)
        if(rownum<=0):
            AfaDBFunc.RollbackSql()
            return AfaFlowControl.ExitThisFlow('S999','修改数据库打印次数失败')
        
        AfaDBFunc.CommitSql()
        TradeContext.errorCode="0000"
        TradeContext.errorMsg="查询成功"
    
    #=====30 通存通兑====
    elif( TradeContext.OPRTYPNO == PL_TRCCO_TCTD ):
        AfaLoggerFunc.tradeInfo("进入通存通兑处理")
        
        records = {}
        #=====查询交易信息====
        AfaLoggerFunc.tradeInfo("查询交易信息")
        wtrbka_where_dict = {'BJEDTE':TradeContext.BJEDTE,'BSPSQN':TradeContext.BSPSQN}
        res_wtrbka = rccpsDBTrcc_wtrbka.selectu(wtrbka_where_dict)
        if( len(res_wtrbka) == 0 ):
            return AfaFlowControl.ExitThisFlow('A009','查询交易信息结果为空')
        if( res_wtrbka == None ):
            return AfaFlowControl.ExitThisFlow('A009','查询交易信息失败')
            
        #=====查询交易的历史状态====    
        AfaLoggerFunc.tradeInfo("查询交易的历史状态")
        sstlog_where_dict = {'BJEDTE':TradeContext.BJEDTE,'BSPSQN':TradeContext.BSPSQN,'BCURSQ':TradeContext.BCURSQ}
        res_sstlog = rccpsDBTrcc_sstlog.selectu(sstlog_where_dict)
        if( len(res_sstlog) == 0 ):
            return AfaFlowControl.ExitThisFlow('A009','查询交易历史状态结果为空')
        if( res_sstlog == None ):
            return AfaFlowControl.ExitThisFlow('A009','查询交易历史状态失败')
            
        #=====给records字典赋值，字典相加，赋值到新的字典====
        records.update(res_wtrbka)
        records.update(res_sstlog)
        
        #=====判断是否为签发机构====
        AfaLoggerFunc.tradeInfo("判断是否为签发机构")
        if( records['BESBNO'] != TradeContext.BESBNO ):
            return AfaFlowControl.ExitThisFlow('A009','此机构不是签发机构')
        
        #=====判断此交易是否为往账====
        AfaLoggerFunc.tradeInfo("判断此交易是否为往账")
        if( records['BRSFLG'] != PL_BRSFLG_SND ):
            return AfaFlowControl.ExitThisFlow('A009','此交易不是往账交易')
            
        #=====判断交易状态====
        AfaLoggerFunc.tradeInfo("判断此交易状态")
        if not ( records['BCSTAT'] == PL_BCSTAT_ACC or records['BCSTAT'] == PL_BCSTAT_HCAC or records['BCSTAT'] == PL_BCSTAT_CANCEL or records['BCSTAT'] == PL_BCSTAT_CANC):
            return AfaFlowControl.ExitThisFlow('A009','此状态不允许打印')
        
        if(records['BCSTAT'] == PL_BCSTAT_CANCEL or records['BCSTAT'] == PL_BCSTAT_CANC):
            if(records['TRDT'] == "" or records['TLSQ'] == ""):
                return AfaFlowControl.ExitThisFlow('A009','此笔业务没有产生产生账务')
            
            
        rccpsMap8522Drecords2CTradeContext.map(records)
        
        #=====输出接口====
        AfaLoggerFunc.tradeInfo("给输出接口赋值")
        TradeContext.PRTDAT  = AfaUtilTools.GetHostDate()
        TradeContext.PRTTIM  = AfaUtilTools.GetSysTime() 
        TradeContext.PRTCNT  = str(int(records['PRTCNT'])+1) 
        TradeContext.USE     = ""
        TradeContext.BILAMT  = str(records['OCCAMT']) 
        TradeContext.BCSTAT  = ret['BCSTAT']                    #当前状态
        TradeContext.BDWFLG  = ret['BDWFLG']                    #流转处理标识
        TradeContext.TRDT    = ret['TRDT']                      #主机日期
        TradeContext.TLSQ    = ret['TLSQ']                      #主机流水号    
        TradeContext.REMARK  = ""
        TradeContext.DASQ    = records['DASQ']                  #销账序号
        TradeContext.BNKBKNO = records['BNKBKNO']               #存折号码
        TradeContext.CHSHTP  = records['CHRGTYP']               #手续费收取方式
        if(records['TRCCO'] in ('3000002','30000102')):         #卡折标志
            TradeContext.PYITYP = records['PYETYP']
        else:
            TradeContext.PYITYP = records['PYRTYP']

        #=====更新打印标志====        
        AfaLoggerFunc.tradeInfo("开始更新打印标志")
        update_dict={'PRTCNT':str(int(records['PRTCNT'])+1)}
        where_dict={'BJEDTE':TradeContext.BJEDTE,'BSPSQN':TradeContext.BSPSQN,'BCURSQ':TradeContext.BCURSQ}
        rownum=rccpsDBTrcc_sstlog.update(update_dict,where_dict)
        if(rownum<=0):
            AfaDBFunc.RollbackSql()
            return AfaFlowControl.ExitThisFlow('S999','修改数据库打印次数失败')
        
        AfaDBFunc.CommitSql()
        TradeContext.errorCode="0000"
        TradeContext.errorMsg="查询成功"
         
    else:
        return AfaFlowControl.ExitThisFlow('A009','业务种类非法')

    AfaLoggerFunc.tradeInfo( '***农信银系统: 往账.本地类操作交易[RCC001_8522]退出***' )
    return True
