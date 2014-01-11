# -*- coding: gbk -*-
################################################################################
#   农信银系统：往账.中心类操作(1.本地操作 2.中心操作).汇兑查询书发送
#===============================================================================
#   交易文件:   TRCC003_8511.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  关彬捷
#   修改时间:   2008-06-15
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBFunc,rccpsGetFunc
import rccpsDBTrcc_hdcbka,rccpsDBTrcc_subbra
import rccpsMap8511CTradeContext2Dhdcbka


#=====================交易前处理(本地操作,中心前处理)===========================
def SubModuleDoFst():
    #=================查询原交易信息============================================
    
    if not TradeContext.existVariable('BOJEDT'):
        return AfaFlowControl.ExitThisFlow("S999", "原交易日期不能为空")
    
    if not TradeContext.existVariable('BOSPSQ'):
        return AfaFlowControl.ExitThisFlow("S999", "原报单序号不能为空")
        
    AfaLoggerFunc.tradeInfo(">>>开始查询原汇兑业务交易信息")
    
    trcbka_dict = {}
    ret = rccpsDBFunc.getTransTrc(TradeContext.BOJEDT,TradeContext.BOSPSQ,trcbka_dict)
    
    if not ret:
        return False
    
    AfaLoggerFunc.tradeInfo(">>>开始查询原汇兑业务交易信息")
    #=================登记查询书信息============================================
    AfaLoggerFunc.tradeInfo(">>>开始登记汇兑业务查询书信息")
    
    #TradeContext.RCVBNKCO = trcbka_dict['RCVBNKCO']
    #TradeContext.RCVBNKNM = trcbka_dict['RCVBNKNM']
    TradeContext.NCCWKDAT = TradeContext.NCCworkDate
    TradeContext.ISDEAL   = PL_ISDEAL_UNDO            #查复标识为未查复
    
    #=====刘雨龙 20080701 新增汇兑业务查询查复登记簿信息====
    TradeContext.TRCNO    = TradeContext.SerialNo       #交易流水号
    TradeContext.ORTRCCO    = trcbka_dict['TRCCO']      #原交易代码
    TradeContext.CUR      = trcbka_dict['CUR']          #原币种
    TradeContext.OCCAMT   = str(trcbka_dict['OCCAMT'])  #原交易金额
    TradeContext.PYRACC   = trcbka_dict['PYRACC']       #原付款人账号
    TradeContext.PYEACC   = trcbka_dict['PYEACC']       #原收款人账号
    #TradeContext.PRCCO    = trcbka_dict['PRCCO']        #中心返回代码   关彬捷 删除 20080728
    TradeContext.NOTE1    = trcbka_dict['NOTE1']        #备注1
    TradeContext.NOTE2    = trcbka_dict['NOTE2']        #备注2
    TradeContext.NOTE3    = trcbka_dict['NOTE3']        #备注3
    TradeContext.NOTE4    = trcbka_dict['NOTE4']        #备注4
    
    TradeContext.PRT_OROCCAMT = trcbka_dict['OCCAMT']
    
    hdcbka_insert_dict = {}
    if not rccpsMap8511CTradeContext2Dhdcbka.map(hdcbka_insert_dict):
        return AfaFlowControl.ExitThisFlow("S999", "为汇兑业务查询查复登记簿赋值异常")
        
    ret = rccpsDBTrcc_hdcbka.insertCmt(hdcbka_insert_dict)
    
    if ret <= 0:
        return AfaFlowControl.ExitThisFlow("S999", "登记汇兑业务查询书信息异常")
    
    AfaLoggerFunc.tradeInfo(">>>结束登记汇兑业务查询书信息")
    
    #=====赋值给打印表单中的变量====
    TradeContext.OROCCAMT=str(trcbka_dict['OCCAMT'])
    TradeContext.ORSNDBNKCO=trcbka_dict['SNDBNKCO']
    TradeContext.ORRCVBNKCO=trcbka_dict['RCVBNKCO']
    
    
    #=================为汇兑查询书报文赋值=====================================
    AfaLoggerFunc.tradeInfo(">>>开始为汇兑查询书报文赋值")
    
    TradeContext.TRCCO      = '9900511'
    TradeContext.MSGTYPCO   = 'SET008'
    TradeContext.SNDBRHCO   = TradeContext.BESBNO
    TradeContext.SNDCLKNO   = TradeContext.BETELR
    TradeContext.SNDTRDAT   = TradeContext.BJEDTE
    TradeContext.SNDTRTIM   = TradeContext.BJETIM
    TradeContext.MSGFLGNO   = TradeContext.SNDSTLBIN + TradeContext.TRCDAT + TradeContext.SerialNo
    TradeContext.ORMFN      = trcbka_dict['SNDMBRCO'] + trcbka_dict['TRCDAT'] + trcbka_dict['TRCNO']
    TradeContext.NCCWKDAT   = TradeContext.NCCworkDate
    TradeContext.OPRTYPNO   = '99'
    TradeContext.ROPRTPNO   = '20'
    TradeContext.TRANTYP    = '0'
    TradeContext.TRCDAT     = TradeContext.TRCDAT
    TradeContext.TRCNO      = TradeContext.SerialNo
    TradeContext.ORTRCDAT   = trcbka_dict['TRCDAT']
    TradeContext.ORTRCNO    = trcbka_dict['TRCNO']
    TradeContext.ORSNDBNK   = trcbka_dict['SNDBNKCO']
    TradeContext.ORRCVBNK   = trcbka_dict['RCVBNKCO']
    TradeContext.ORCUR      = trcbka_dict['CUR']
    TradeContext.OROCCAMT   = str(trcbka_dict['OCCAMT'])
    
    AfaLoggerFunc.tradeInfo(">>>结束为汇兑查询书报文赋值")
    
    
    return True


#=====================交易后处理================================================
def SubModuleDoSnd():
    #=================判断afe是否发送成功=======================================
    if TradeContext.errorCode != '0000':
        return AfaFlowControl.ExitThisFlow(TradeContext.errorCode, TradeContext.errorMsg)
    
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
            
            
                               %(BESBNM)s电子汇兑查询书
                               
        |-----------------------------------------------------------------------------|
        | 查询日期:     |      %(BJEDTE)s                                               |
        |-----------------------------------------------------------------------------|
        | 查询书号:     |      %(BSPSQN)s                                           |
        |-----------------------------------------------------------------------------|
        | 发起行行号:   |      %(SNDBNKCO)s                                             |
        |-----------------------------------------------------------------------------|
        | 接收行行号:   |      %(RCVBNKCO)s                                             |
        |-----------------------------------------------------------------------------|
        | 原交易金额:   |      %(OROCCAMT)-15.2f                                        |
        |-----------------------------------------------------------------------------|
        | 原发起行行号: |      %(ORSNDBNKCO)s                                             |
        |-----------------------------------------------------------------------------|
        | 原接收行行号: |      %(ORRCVBNKCO)s                                             |
        |-----------------------------------------------------------------------------|
        | 查询内容:     |                                                             |
        |-----------------------------------------------------------------------------|
        |                                                                             |
        |     %(CONT1)s    |
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
    
    file_name = 'rccps_' + TradeContext.BJEDTE + '_' + TradeContext.BSPSQN + '_8511'
    
    out_file = open(os.environ['AFAP_HOME'] + '/tmp/' + file_name,"wb")
    
    if out_file == None:
        return AfaFlowControl.ExitThisFlow("S999", "生成打印文件异常")
    
    print >> out_file,txt % {'BESBNM':(sub['BESBNM']).ljust(10,' '),\
                             'BJEDTE':(TradeContext.BJEDTE).ljust(8,' '),\
                             'BSPSQN':(TradeContext.BSPSQN).ljust(12,' '),\
                             'SNDBNKCO':(TradeContext.SNDBNKCO).ljust(10,' '),\
                             'RCVBNKCO':(TradeContext.RCVBNKCO).ljust(10,' '),\
                             'OROCCAMT':(TradeContext.PRT_OROCCAMT),\
                             'ORSNDBNKCO':(TradeContext.SNDBNKCO).ljust(10,' '),\
                             'ORRCVBNKCO':(TradeContext.RCVBNKCO).ljust(10,' '),\
                             'CONT1':(TradeContext.CONT[:68]).ljust(68,' '),\
                             'CONT2':(TradeContext.CONT[68:138]).ljust(70,' '),\
                             'CONT3':(TradeContext.CONT[138:208]).ljust(70,' '),\
                             'CONT4':(TradeContext.CONT[208:]).ljust(70,' ')}
    
    out_file.close
    
    TradeContext.PBDAFILE = file_name
    
    AfaLoggerFunc.tradeInfo("结束生成打印文本")
    
    
    AfaLoggerFunc.tradeInfo('发送成功')
    
    return True
    
