# -*- coding: gbk -*-
################################################################################
#   农信银系统：往账.中心类操作模板(1.本地操作 2.中心操作).汇票挂失/解挂
#===============================================================================
#   交易文件:   TRCC003_8505.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  刘雨龙
#   修改时间:   2008-08-04
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc
import rccpsDBFunc,rccpsState,rccpsMap8505CTradeContext2Dbilbka_dict

from types import *
from rccpsConst import *

#=====================交易前处理(本地操作,中心前处理)===========================
def SubModuleDoFst():

    AfaLoggerFunc.tradeInfo('>>>进入汇票挂失/解挂操作')
    
    #====begin 蔡永贵 20110215 增加====
    #新票据号是16位，需要取后8位，版本号为02，同时要兼容老票据号8位，版本号为01
    if TradeContext.BILVER == '02':
        TradeContext.TMP_BILNO = TradeContext.BILNO[-8:]
    else:
        TradeContext.TMP_BILNO = TradeContext.BILNO
    #============end============
 
    #=====开始查询汇票信息====
    AfaLoggerFunc.tradeDebug('>>>开始查询汇票信息')
    bil_dict = {}
    if not rccpsDBFunc.getInfoBil(TradeContext.BILVER,TradeContext.BILNO,TradeContext.BILRS,bil_dict):
        return AfaFlowControl.ExitThisFlow('S999','查询汇票信息出错')

    AfaLoggerFunc.tradeDebug('>>>结束查询汇票信息')

    #=====判断现金或者转账汇票，只有现金汇票可以进行挂失====
    #if bil_dict['PAYWAY'] != '0':
    #    return AfaFlowControl.ExitThisFlow('S999','转账汇票不允许挂失/解挂')
        
    AfaLoggerFunc.tradeDebug('>>>判断汇票是否允许挂失')
    
    if bil_dict['REMBNKCO'] != TradeContext.SNDBNKCO:
        return AfaFlowControl.ExitThisFlow('S999','只能由签发行进行挂失操作')
    
    AfaLoggerFunc.tradeDebug('>>>判断签发行和挂失行是否一致')

    if bil_dict['SEAL'] == '':
        return AfaFlowControl.ExitThisFlow('S999','密押空错误')
    else:
        TradeContext.SEAL = bil_dict['SEAL']

    AfaLoggerFunc.tradeDebug('>>>结束密押判断')
    
    #=====查询数据库====
    records = {}
    ret = rccpsDBFunc.getTransBil(bil_dict['NOTE1'],bil_dict['NOTE2'],records)
    if( ret == False):
        return AfaFlowControl.ExitThisFlow('A099', '无此数据')

    if str(bil_dict['BILAMT']) == '':
        return AfaFlowControl.ExitThisFlow('S999','金额空错误')
    else:
        TradeContext.OCCAMT = str(bil_dict['BILAMT'])

    TradeContext.PYRACC  =  bil_dict['PYRACC']
    TradeContext.PYRNAM  =  bil_dict['PYRNAM']
    TradeContext.PYRADDR =  bil_dict['PYRADDR']
    TradeContext.PYEACC  =  bil_dict['PYEACC']
    TradeContext.PYENAM  =  bil_dict['PYENAM']
    TradeContext.PYEADDR =  bil_dict['PYEADDR']
    TradeContext.BILDAT  =  bil_dict['BILDAT']
    TradeContext.RCVBNKCO  =  bil_dict['PAYBNKCO']
    TradeContext.RCVBNKNM  =  bil_dict['PAYBNKNM']
    
    TradeContext.BBSSRC  =  records['BBSSRC']
    TradeContext.OPRNO   =  records['OPRNO']
    
        
    AfaLoggerFunc.tradeDebug('>>>开始判断汇票操作类型')

    #=====判断TRCCO汇票操作类型====
    if TradeContext.TRCCO == '2100102':
        #=====汇票挂失====
        if TradeContext.SNDBNKCO != bil_dict['REMBNKCO']:
            return AfaFlowControl.ExitThisFlow('S999','汇票必须由签发行进行挂失')
        #=====判断汇票状态是否 签发 或者 解挂 状态====
        if not (bil_dict['HPSTAT'] == PL_HPSTAT_SIGN or bil_dict['HPSTAT'] == PL_HPSTAT_DEHG):
            return AfaFlowControl.ExitThisFlow('S999','汇票当前状态[' + bil_dict['HPSTAT'] + ']不允许进行挂失')
        
        #=====添加OPRNO  PL_HPOPRNO_GS 挂失====
        TradeContext.OPRNO   =  PL_HPOPRNO_GS
    elif TradeContext.TRCCO == '2100104':
        #=====汇票解挂====
        if TradeContext.SNDBNKCO != bil_dict['REMBNKCO']:
            return AfaFlowControl.ExitThisFlow('S999','汇票必须由挂失行进行解挂')
        #=====判断汇票状态是否 挂失 状态====
        if not bil_dict['HPSTAT'] == PL_HPSTAT_HANG:
            return AfaFlowControl.ExitThisFlow('S999','汇票当前状态[' + bil_dict['HPSTAT'] + ']不允许进行解挂')
            
        #=====添加OPRNO  PL_HPOPRNO_JG 解挂====
        TradeContext.OPRNO   =  PL_HPOPRNO_JG
    else:
        return AfaFlowControl.ExitThisFlow('S999','汇票操作类型错误')

    AfaLoggerFunc.tradeDebug('>>>结束判断汇票操作类型')

    #=====PL_BILTYP_CASH  0  现金====
    if bil_dict['BILTYP'] == PL_BILTYP_CASH:
        #=====现金汇票====
        TradeContext.ROPRTPNO  =  ''
    else:
        #=====转账汇票====
        TradeContext.ROPRTPNO  =  '21'

    AfaLoggerFunc.tradeDebug('>>>结束判断汇票类型')
    
    #=====字典赋值====
    TradeContext.DCFLG = PL_DCFLG_DEB

    bilbka_dict = {}
    if not rccpsMap8505CTradeContext2Dbilbka_dict.map(bilbka_dict):
        return AfaFlowControl.ExitThisFlow('S999','字典赋值出错')

    AfaLoggerFunc.tradeDebug('>>>结束字典赋值')
    AfaLoggerFunc.tradeDebug('>>>开始登记汇票业务信息登记簿')

    #=====登记汇票业务信息登记簿====
    if not rccpsDBFunc.insTransBil(bilbka_dict):
        return AfaFlowControl.ExitThisFlow('S999','登记汇票业务信息登记簿出错')

    AfaDBFunc.CommitSql()
    
    AfaLoggerFunc.tradeDebug('>>>结束登记汇票业务信息登记簿')
    AfaLoggerFunc.tradeDebug('>>>开始发送农信银中心')

    TradeContext.TRANTYP   = '0'                #传输类型
    TradeContext.OPRTYPNO  = PL_TRCCO_HP        #业务属性 PL_TRCCO_HP 21 汇票
    
    #begin 20110614 曾照泰 修改 送往农信银中心的票号为8位
    TradeContext.BILNO = TradeContext.BILNO[-8:]
    #end
    
    return True


#=====================交易后处理================================================
def SubModuleDoSnd():

    AfaLoggerFunc.tradeDebug('>>>结束发送农信银中心')
    AfaLoggerFunc.tradeDebug('>>>开始状态变更')

    sstlog = {}

    sstlog['BJEDTE'] = TradeContext.BJEDTE
    sstlog['BSPSQN'] = TradeContext.BSPSQN
    sstlog['BCSTAT'] = PL_BCSTAT_SND
    sstlog['NOTE3']  = TradeContext.errorMsg

    if TradeContext.errorCode == '0000':
        sstlog['BDWFLG'] = PL_BDWFLG_SUCC
    else:
        sstlog['BDWFLG'] = PL_BDWFLG_FAIL

    #=====修改sstlog表中数据====
    if not rccpsState.setTransState(sstlog):
        return AfaFlowControl.ExitThisFlow(TradeContext.errorCode, TradeContext.errorMsg)
    else:
        #=====commit操作====
        AfaDBFunc.CommitSql()

    AfaLoggerFunc.tradeDebug('>>>结束状态变更')

    
    return True
    
