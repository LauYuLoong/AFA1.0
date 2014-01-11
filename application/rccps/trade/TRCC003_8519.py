# -*- coding: gbk -*-
################################################################################
#   农信银系统：往账.中心类操作(1.本地操作 2.中心操作).特约电子汇兑查复书发送
#===============================================================================
#   交易文件:   TRCC003_8519.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  戴智勇
#   修改时间:   2008-06-15
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBFunc,rccpsGetFunc
import rccpsDBTrcc_hdcbka,rccpsDBTrcc_subbra
import rccpsMap8519CTradeContext2Dhdcbka


#=====================交易前处理(本地操作,中心前处理)===========================
def SubModuleDoFst():
    #=================查询原查复信息============================================
    
    if not TradeContext.existVariable('ORQYDAT'):
        return AfaFlowControl.ExitThisFlow("S999", "原查询日期不能为空")
    
    if not TradeContext.existVariable('OQTNO'):
        return AfaFlowControl.ExitThisFlow("S999", "原查询号不能为空")
        
    #=====刘雨龙 20080701 修改查询函数====
    #=====使用错误函数，应该查询 查询查复登记簿 中关于特约汇兑查询的信息====
    AfaLoggerFunc.tradeInfo(">>>开始查询原查询书信息")
    hdcbka = {}
    hdcbka['BJEDTE']   =  TradeContext.ORQYDAT     #查询日期
    hdcbka['BSPSQN']   =  TradeContext.OQTNO       #报单序号

    hdcbka_dict = rccpsDBTrcc_hdcbka.selectu(hdcbka)

    if hdcbka_dict == None:
        return AfaFlowControl.ExitThisFlow('S999','查询数据库出错')
    if len(hdcbka_dict) <= 0:
        return AfaFlowControl.ExitThisFlow('S999','数据库中无相应记录')


    #=====刘雨龙 20080702 增加判断是否已查复====
    if hdcbka_dict['ISDEAL'] == PL_ISDEAL_ISDO:
        return AfaFlowControl.ExitThisFlow('S999','报单序号['+TradeContext.OQTNO+']该笔业务已查复')

    #=====刘雨龙 20080725 增加判断是否来账====
    if hdcbka_dict['BRSFLG'] != PL_BRSFLG_RCV:
        return AfaFlowControl.ExitThisFlow('S999','报单序号['+TradeContext.OQTNO+']该笔业务不为来账查询书')

    #=====刘雨龙 20080722 增加判断原交易代码是否为:特约汇兑查询书 9900522====
    if hdcbka_dict['TRCCO'] != '9900522':
        return AfaFlowControl.ExitThisFlow('S999','报单序号['+TradeContext.OQTNO+']该笔业务不为特约汇兑查询书')

    AfaLoggerFunc.tradeInfo(">>>开始查询原交易信息")
    trcbka_dict = {}
    ret = rccpsDBFunc.getTransTrc(hdcbka_dict['BOJEDT'],hdcbka_dict['BOSPSQ'],trcbka_dict)
    
    if not ret:
        return AfaFlowControl.ExitThisFlow('S999','查询原交易信息失败') 
    
    AfaLoggerFunc.tradeInfo(">>>结束查询数据库信息")
    #=================登记查复书信息============================================
    AfaLoggerFunc.tradeInfo(">>>开始登记特约电子汇兑业务查复书信息")
    
    #TradeContext.RCVBNKCO = hdcbka_dict['SNDBNKCO']
    #TradeContext.RCVBNKNM = hdcbka_dict['SNDBNKNM']
    TradeContext.NCCWKDAT = TradeContext.NCCworkDate
    TradeContext.ISDEAL   = PL_ISDEAL_ISDO            #查复标识为已处理
    
    #=====刘雨龙 20080701 增加数据库内容====
    TradeContext.CUR      = trcbka_dict['CUR']        #币种
    TradeContext.ORTRCCO  = hdcbka_dict['TRCCO']      #原交易代码
    TradeContext.OCCAMT   = trcbka_dict['OCCAMT']     #交易金额
    TradeContext.PYRACC   = trcbka_dict['PYRACC']     #付款人账号
    TradeContext.PYEACC   = trcbka_dict['PYEACC']     #收款人账号
    TradeContext.NOTE1    = hdcbka_dict['NOTE1']      #备注1
    TradeContext.NOTE2    = hdcbka_dict['NOTE2']      #备注2
    TradeContext.NOTE3    = hdcbka_dict['NOTE3']      #备注3
    TradeContext.NOTE4    = hdcbka_dict['NOTE4']      #备注4
    TradeContext.BRSFLG   = PL_BRSFLG_SND             #往来标志
    
    hdcbka_insert_dict = {}
    if not rccpsMap8519CTradeContext2Dhdcbka.map(hdcbka_insert_dict):
        return AfaFlowControl.ExitThisFlow("S999", "为特约电子汇兑业务查询查复登记簿赋值异常")
  
    #关彬捷 20080728 BJEDTE和BSPSQN在map函数中已赋值
    #hdcbka_insert_dict['BJEDTE']  =  TradeContext.BJEDTE
    #hdcbka_insert_dict['BSPSQN']  =  TradeContext.BSPSQN
    
    #=====潘广通 20080729 生成打印表格中的数据====
    TradeContext.OR_SNDBNKCO = trcbka_dict['SNDBNKCO']
    TradeContext.OR_TRCDAT   = trcbka_dict['TRCDAT']
    TradeContext.OR_TRCNO    = trcbka_dict['TRCNO']
    TradeContext.OR_OCCAMT   = trcbka_dict['OCCAMT']
        
    ret = rccpsDBTrcc_hdcbka.insertCmt(hdcbka_insert_dict)
    
    if ret <= 0:
        return AfaFlowControl.ExitThisFlow("S999", "登记特约电子汇兑业务查复书信息异常")
    
    AfaLoggerFunc.tradeInfo(">>>结束登记特约电子汇兑业务查复书信息")
    
    #=================为特约电子汇兑查复书报文赋值======================================
    AfaLoggerFunc.tradeInfo(">>>开始为特约电子汇兑查复书报文赋值")
    
    TradeContext.MSGTYPCO   = 'SET008'
    TradeContext.SNDBRHCO   = TradeContext.BESBNO
    TradeContext.SNDCLKNO   = TradeContext.BETELR
    TradeContext.SNDTRDAT   = TradeContext.BJEDTE
    TradeContext.SNDTRTIM   = TradeContext.BJETIM
    #TradeContext.MSGFLGNO   = TradeContext.SNDSTLBIN + TradeContext.TRCDAT + TradeContext.SerialNo
    TradeContext.ORMFN      = hdcbka_dict['SNDMBRCO'] + hdcbka_dict['TRCDAT'] + hdcbka_dict['TRCNO']
    TradeContext.NCCWKDAT   = TradeContext.NCCworkDate
    TradeContext.OPRTYPNO   = '99'
    TradeContext.ROPRTPNO   = '99'
    TradeContext.TRANTYP    = '0'
    TradeContext.TRCDAT     = TradeContext.TRCDAT
    TradeContext.TRCNO      = TradeContext.SerialNo
    TradeContext.ORTRCDAT   = hdcbka_dict['TRCDAT']
    TradeContext.ORTRCNO    = hdcbka_dict['TRCNO']
    TradeContext.ORSNDBNK   = hdcbka_dict['SNDBNKCO']
    TradeContext.ORRCVBNK   = hdcbka_dict['RCVBNKCO']
    TradeContext.ORTRCCO    = hdcbka_dict['TRCCO']
    TradeContext.ORCUR      = trcbka_dict['CUR']
    TradeContext.OROCCAMT   = str(trcbka_dict['OCCAMT'])
    TradeContext.ORQYDAT    = hdcbka_dict['BJEDTE']
    TradeContext.OQTSBNK    = hdcbka_dict['SNDBNKCO']

    #=====刘雨龙 20080701 新增收/付款人名称====
    TradeContext.PYENAM     = trcbka_dict['PYENAM']       #收款人名称
    TradeContext.PYRNAM     = trcbka_dict['PYRNAM']       #付款人名称
    TradeContext.OROQTNO    = hdcbka_dict['TRCNO']        #原特约查询交易流水号
    TradeContext.BOJEDT     = hdcbka_dict['BJEDTE']
    TradeContext.BOSPSQ     = hdcbka_dict['BSPSQN']
    
    
    AfaLoggerFunc.tradeInfo(">>>结束为特约电子汇兑查复书报文赋值")
    
   
    return True

#=====================交易后处理================================================
def SubModuleDoSnd():
    #=================判断afe是否发送成功=======================================
    if TradeContext.errorCode != '0000':
        return AfaFlowControl.ExitThisFlow(TradeContext.errorCode, TradeContext.errorMsg)
    
    AfaLoggerFunc.tradeInfo('发送成功')
    #=====刘雨龙 20080702 新增修改原记录状态为 已查复 ====
    hdcbka_where_dict = {}
    hdcbka_where_dict['BJEDTE'] = TradeContext.BOJEDT
    hdcbka_where_dict['BSPSQN'] = TradeContext.BOSPSQ

    hdcbka_update_dict = {}
    hdcbka_update_dict['ISDEAL']  = PL_ISDEAL_ISDO

    ret = rccpsDBTrcc_hdcbka.update(hdcbka_update_dict,hdcbka_where_dict)
    if ret == None:
        return AfaFlowControl.ExitThisFlow('S999','数据库操作错误')
    if ret <= 0:
        if not AfaDBFunc.RollbackSql( ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            AfaLoggerFunc.tradeError(">>>Rollback异常")
        return AfaFlowControl.ExitThisFlow("S999","更新系统状态异常")

    if not AfaDBFunc.CommitSql( ):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow("S999","Commit异常")
    AfaLoggerFunc.tradeInfo(">>>Commit成功")

    #=====查询机构名====
    subbra_dict={'BESBNO':TradeContext.BESBNO}
    sub=rccpsDBTrcc_subbra.selectu(subbra_dict)
    if(sub==None):
        return AfaFlowControl.ExitThisFlow('A099','查询机构名失败' )
        
    if(len(sub)==0):
        return AfaFlowControl.ExitThisFlow('A099','没有相应的机构名' )
    
    #=================生成打印文本=============================================
    AfaLoggerFunc.tradeInfo("开始生成打印文本")
    
    txt = """\
            
            
                               %(BESBNM)s全国特约电子汇兑查复书
                               
        |-----------------------------------------------------------------------------|
        | 查复日期:             |      %(BJEDTE)s                                       |
        |-----------------------------------------------------------------------------|
        | 特约汇兑查复书号:     |      %(BSPSQN)s                                   |
        |-----------------------------------------------------------------------------|
        | 发起行行号:           |      %(SNDBNKCO)s                                     |
        |-----------------------------------------------------------------------------|
        | 接收行行号:           |      %(RCVBNKCO)s                                     |
        |-----------------------------------------------------------------------------|
        | 原特约查询发起行行号: |      %(ORSNDBNKCO)s                                     |
        |-----------------------------------------------------------------------------|
        | 原特约查询日期:       |      %(BOJEDT)s                                       |
        |-----------------------------------------------------------------------------|
        | 原金额:               |      %(OROCCAMT)-15.2f                         |
        |-----------------------------------------------------------------------------|
        | 原委托日期:           |      %(ORTRCDAT)s                                       |
        |-----------------------------------------------------------------------------|
        | 原特约查询交易流水号: |      %(ORTRCNO)s                                   |
        |-----------------------------------------------------------------------------|
        | 查询内容:             |                                                     |
        |-----------------------------------------------------------------------------|
        |                                                                             |
        |   %(CONT1)s      |
        |                                                                             |
        |   %(CONT2)s    |
        |                                                                             |
        |   %(CONT3)s    |
        |                                                                             |
        |   %(CONT4)s    |
        |                                                                             |
        |-----------------------------------------------------------------------------|
        打印日期: %(BJEDTE)s      授权:                       记账:
    """
    
    file_name = 'rccps_' + TradeContext.BJEDTE + '_' + TradeContext.BSPSQN + '_8519'
    
    out_file = open(os.environ['AFAP_HOME'] + '/tmp/' + file_name,"wb")
    
    if out_file == None:
        return AfaFlowControl.ExitThisFlow("S999", "生成打印文件异常")
    
    print >> out_file,txt % {'BESBNM':(sub['BESBNM']).ljust(10,' '),\
                             'BJEDTE':(TradeContext.BJEDTE).ljust(8,' '),\
                             'BSPSQN':(TradeContext.BSPSQN).ljust(12,' '),\
                             'SNDBNKCO':(TradeContext.SNDBNKCO).ljust(10,' '),\
                             'RCVBNKCO':(TradeContext.RCVBNKCO).ljust(10,' '),\
                             'ORSNDBNKCO':(TradeContext.OR_SNDBNKCO).ljust(10,' '),\
                             'BOJEDT':(TradeContext.ORQYDAT).ljust(8,' '),\
                             'OROCCAMT':(TradeContext.OR_OCCAMT),\
                             'ORTRCDAT':(TradeContext.OR_TRCDAT).ljust(8,' '),\
                             'ORTRCNO':(TradeContext.OR_TRCNO).ljust(12,' '),\
                             'CONT1':(TradeContext.CONT[:68]).ljust(68,' '),\
                             'CONT2':(TradeContext.CONT[68:138]).ljust(70,' '),\
                             'CONT3':(TradeContext.CONT[138:208]).ljust(70,' '),\
                             'CONT4':(TradeContext.CONT[208:]).ljust(70,' ')}
    
    out_file.close
    
    TradeContext.PBDAFILE = file_name
    
    AfaLoggerFunc.tradeInfo("结束生成打印文本")
    
    return True
    
