# -*- coding: gbk -*-
################################################################################
#   农信银系统：往账.中心类操作(1.本地操作 2.中心操作).通存通兑查复书发送
#===============================================================================
#   交易文件:   TRCC003_8584.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  潘广通
#   修改时间:   2008-10-29
################################################################################

import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBFunc,rccpsGetFunc,os
import rccpsDBTrcc_hdcbka,rccpsDBTrcc_subbra,rccpsDBTrcc_wtrbka
import rccpsMap8512CTradeContext2Dhdcbka


#=====================交易前处理(本地操作,中心前处理)===========================
def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.中心类操作(1.本地操作).通存通兑查复书发送[TRC003_8584]进入***' )
    
    #=================查询原查复信息============================================  
    if not TradeContext.existVariable('ORQYDAT'):
        return AfaFlowControl.ExitThisFlow("S999", "原查询日期不能为空")
    
    if not TradeContext.existVariable('OQTNO'):
        return AfaFlowControl.ExitThisFlow("S999", "原查询号不能为空")
        
    AfaLoggerFunc.tradeInfo(">>>开始查询原查询书信息")
    
    hdcbka_dict = {}
    hdcbka_where_dict = {'BJEDTE':TradeContext.ORQYDAT,'BSPSQN':TradeContext.OQTNO}
    hdcbka_dict = rccpsDBTrcc_hdcbka.selectu(hdcbka_where_dict)
    if hdcbka_dict == None:
        return AfaFlowControl.ExitThisFlow("S999","数据库操作失败")
    if len(hdcbka_dict) > 0:
        if hdcbka_dict['ISDEAL']  == PL_ISDEAL_ISDO:        #PL_ISDEAL_ISDO  已查复或已处理
            return AfaFlowControl.ExitThisFlow("S999","该查询已被查复")
    
    AfaLoggerFunc.tradeInfo(">>>开始查询通存通兑原交易信息")
    wtrbka_dict = {}
    ret = rccpsDBFunc.getTransWtr(hdcbka_dict['BOJEDT'],hdcbka_dict['BOSPSQ'],wtrbka_dict)
    
    if not ret:
        return False
    
    AfaLoggerFunc.tradeInfo(">>>结束查询数据库信息")
    #=================登记查复书信息============================================
    AfaLoggerFunc.tradeInfo(">>>开始登记通存通兑业务查复书信息")
    
#    RCVBNKCO=TradeContext.RCVBNKCO 
    
#    TradeContext.RCVBNKCO = hdcbka_dict['SNDBNKCO']
#    TradeContext.RCVBNKNM = hdcbka_dict['SNDBNKNM']    注释于0724 by pgt
    TradeContext.NCCWKDAT = TradeContext.NCCworkDate
    TradeContext.ISDEAL   = PL_ISDEAL_ISDO            #查复标识为已处理
    TradeContext.BOJEDT   = TradeContext.ORQYDAT      #原交易日期
    TradeContext.BOSPSQ   = TradeContext.OQTNO        #原报单序号
    TradeContext.ORTRCCO  = hdcbka_dict['TRCCO']      #原交易码
    TradeContext.CUR      = hdcbka_dict['CUR']        #币种
    TradeContext.OCCAMT   = str(wtrbka_dict['OCCAMT']) #交易金额
    TradeContext.PYRACC   = wtrbka_dict['PYRACC']     #付款人账号
    TradeContext.PYEACC   = wtrbka_dict['PYEACC']     #收款人账号
    TradeContext.NOTE1    = hdcbka_dict['NOTE1']
    TradeContext.NOTE2    = hdcbka_dict['NOTE2']
    TradeContext.NOTE3    = hdcbka_dict['NOTE3']
    TradeContext.NOTE4    = hdcbka_dict['NOTE4']
    
    TradeContext.PRT_OROCCAMT = wtrbka_dict['OCCAMT']
    
    hdcbka_insert_dict = {}
    if not rccpsMap8512CTradeContext2Dhdcbka.map(hdcbka_insert_dict):
        return AfaFlowControl.ExitThisFlow("S999", "为汇兑业务查询查复登记簿赋值异常")
        
    ret = rccpsDBTrcc_hdcbka.insertCmt(hdcbka_insert_dict)
    
    if ret <= 0:
        return AfaFlowControl.ExitThisFlow("S999", "登记汇兑业务查复书信息异常")
    
    AfaLoggerFunc.tradeInfo(">>>结束登记汇兑业务查复书信息")
    
    
    
    #=================为汇兑查询书报文赋值======================================
    AfaLoggerFunc.tradeInfo(">>>开始为汇兑查复书报文赋值")
    
    TradeContext.TRCCO      = '9900512'
    TradeContext.MSGTYPCO   = 'SET008'
    TradeContext.SNDBRHCO   = TradeContext.BESBNO
    TradeContext.SNDCLKNO   = TradeContext.BETELR
    TradeContext.SNDTRDAT   = TradeContext.BJEDTE
    TradeContext.SNDTRTIM   = TradeContext.BJETIM
    TradeContext.MSGFLGNO   = TradeContext.SNDSTLBIN + TradeContext.TRCDAT + TradeContext.SerialNo
    TradeContext.ORMFN      = TradeContext.RCVSTLBIN + hdcbka_dict['TRCDAT'] + hdcbka_dict['TRCNO']
    TradeContext.NCCWKDAT   = TradeContext.NCCworkDate
    TradeContext.OPRTYPNO   = '99'
    TradeContext.ROPRTPNO   = '99'
    TradeContext.TRANTYP    = '0'
    TradeContext.TRCDAT     = TradeContext.TRCDAT
    TradeContext.TRCNO      = TradeContext.SerialNo
    TradeContext.ORTRCDAT   = wtrbka_dict['TRCDAT']
    TradeContext.ORTRCNO    = wtrbka_dict['TRCNO']
    TradeContext.ORSNDBNK   = wtrbka_dict['SNDBNKCO']
    TradeContext.ORRCVBNK   = wtrbka_dict['RCVBNKCO']
    TradeContext.ORTRCCO    = hdcbka_dict['TRCCO']
    TradeContext.ORCUR      = TradeContext.CUR
    TradeContext.OROCCAMT   = str(hdcbka_dict['OCCAMT'])
    TradeContext.ORQYDAT    = hdcbka_dict['TRCDAT']
    TradeContext.OQTSBNK    = hdcbka_dict['SNDBNKCO']
    TradeContext.OQTNO      = hdcbka_dict['TRCNO']
    
    AfaLoggerFunc.tradeInfo(">>>结束为汇兑查复书报文赋值")
    
    return True
    
    
    
#=====================交易后处理================================================
def SubModuleDoSnd():
    #=================判断afe是否发送成功=======================================
    if TradeContext.errorCode != '0000':
        AfaLoggerFunc.tradeInfo('>>>AFE发送失败')
        return AfaFlowControl.ExitThisFlow(TradeContext.errorCode, TradeContext.errorMsg)
    
    AfaLoggerFunc.tradeInfo('>>>发送成功')
    update_wdict = {'BJEDTE':TradeContext.BOJEDT,'BSPSQN':TradeContext.BOSPSQ}
    update_dict  = {'ISDEAL':PL_ISDEAL_ISDO}                   #已查复
    ret = rccpsDBTrcc_hdcbka.update(update_dict,update_wdict)
    if (ret <= 0):
        AfaDBFunc.RollbackSql()
        return AfaFlowControl.ExitThisFlow("S999","更新原查询业务信息异常")

    AfaDBFunc.CommitSql()
    AfaLoggerFunc.tradeInfo(">>>Commit成功")
    
    #=====查询机构名====
    subbra_dict={'BESBNO':TradeContext.BESBNO}
    sub=rccpsDBTrcc_subbra.selectu(subbra_dict)
    if(sub==None):
        return AfaFlowControl.ExitThisFlow('A099','查询机构名失败' )
        
    if(len(sub)==0):
        return AfaFlowControl.ExitThisFlow('A099','没有相应的机构名' )

    #=====生成打印文本====
    AfaLoggerFunc.tradeInfo("开始生成打印文本")
    
    txt = """\
            
            
                               %(BESBNM)s通存通兑查复书
                               
        |-----------------------------------------------------------------------------|
        | 查复日期:     |      %(BJEDTE)s                                               |
        |-----------------------------------------------------------------------------|
        | 查复书号:     |      %(BSPSQN)s                                           |
        |-----------------------------------------------------------------------------|
        | 接收行行号:   |      %(RCVBNKCO)s                                             |
        |-----------------------------------------------------------------------------|
        | 原查询日期:   |      %(BOJEDT)s                                               |
        |-----------------------------------------------------------------------------|
        | 原查询书号:   |      %(BOSPSQ)s                                           |
        |-----------------------------------------------------------------------------|
        | 原金额:       |      %(OROCCAMT)-15.2f                                        |
        |-----------------------------------------------------------------------------|
        | 原币种:       |      人民币                                                 |
        |-----------------------------------------------------------------------------|
        | 查复内容:     |                                                             |
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

    file_name = 'rccps_' + TradeContext.BJEDTE + '_' + TradeContext.BSPSQN + '_' + '_8512'
    
    out_file = open(os.environ['AFAP_HOME'] + '/tmp/' + file_name,"wb")
    
    if out_file == None:
        return AfaFlowControl.ExitThisFlow("S999", "生成打印文件异常")
    
    print >> out_file,txt % {'BESBNM':(sub['BESBNM']).ljust(10,' '),\
                             'BJEDTE':(TradeContext.BJEDTE).ljust(8,' '),\
                             'BSPSQN':(TradeContext.BSPSQN).ljust(12,' '),\
                             'RCVBNKCO':(TradeContext.RCVBNKCO).ljust(10,' '),\
                             'BOJEDT':(TradeContext.BOJEDT).ljust(8,' '),\
                             'BOSPSQ':(TradeContext.BOSPSQ).ljust(12,' '),\
                             'OROCCAMT':(TradeContext.PRT_OROCCAMT),\
                             'CONT1':(TradeContext.CONT[:68]).ljust(68,' '),\
                             'CONT2':(TradeContext.CONT[68:138]).ljust(70,' '),\
                             'CONT3':(TradeContext.CONT[138:208]).ljust(70,' '),\
                             'CONT4':(TradeContext.CONT[208:]).ljust(70,' ')}
    
    out_file.close()
    
    TradeContext.PBDAFILE = file_name
    
    AfaLoggerFunc.tradeInfo("结束生成打印文本")
    
    
    return True

