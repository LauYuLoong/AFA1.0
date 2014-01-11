# -*- coding: gbk -*-
################################################################################
#   农信银系统：往账.中心类操作(1.本地操作 2.中心操作).通存通兑查询书发送
#===============================================================================
#   交易文件:   TRCC003_8583.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  潘广通
#   修改时间:   2008-10-29
################################################################################

import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBFunc,rccpsGetFunc
import rccpsDBTrcc_hdcbka,rccpsDBTrcc_subbra,rccpsDBTrcc_wtrbka
import rccpsMap8583CTradeContext2Dhdcbka_dict

def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo("'***农信银系统：通存通兑往账交易.通存通兑查询书发送[8582] 进入")
    
    AfaLoggerFunc.tradeInfo("交易前处理(本地操作,中心前处理)")
    
    #=====查询原交易信息====
    AfaLoggerFunc.tradeInfo("查询原交易信息")
    if not TradeContext.existVariable('BOSPSQ'):
        return AfaFlowControl.ExitThisFlow('A099','没有原报单序号')
        
    if not TradeContext.existVariable('BOJEDT'):
        return AfaFlowControl.ExitThisFlow("A099", "没有原报单日期")
    
    #=====开始查询通存通兑业务登记簿====
    AfaLoggerFunc.tradeInfo("开始查询通存通兑业务登记簿")
    wtrbka_record = {}
    res = rccpsDBFunc.getTransWtr(TradeContext.BOJEDT,TradeContext.BOSPSQ,wtrbka_record)
    if( res == False ):
        return AfaFlowControl.ExitThisFlow('A099','查询原交易信息失败')
        
    #=====登记查询查复自由格式登记簿====
    AfaLoggerFunc.tradeInfo("登记查询查复登自由格式记簿")
    TradeContext.BRSFLG   = PL_BRSFLG_SND 
    TradeContext.NCCWKDAT = TradeContext.NCCworkDate
    TradeContext.TRCCO    = '9900511'
#    TradeContext.TRCDAT   = ''
    TradeContext.TRCNO    = TradeContext.SerialNo
#    TradeContext.SNDBNKCO = 
#    TradeContext.SNDBNKNM = 
#    TradeContext.RCVBNKCO = 
#    TradeContext.RCVBNKNM = 
#    TradeContext.BOJEDT   = 
#    TradeContext.BOSPSQ   = 
    TradeContext.ORTRCCO  = wtrbka_record['TRCCO']
    TradeContext.CUR      = wtrbka_record['CUR']
    TradeContext.OCCAMT   = str(wtrbka_record['OCCAMT'])
#    TradeContext.CONT     = 
    TradeContext.PYRACC   = wtrbka_record['PYRACC']
    TradeContext.PYEACC   = wtrbka_record['PYEACC']
    TradeContext.ISDEAL   = PL_ISDEAL_UNDO
#    TradeContext.PRCCO    = 

    #=====给插入字典赋值====
    AfaLoggerFunc.tradeInfo("给插入字典赋值")
    hdcbka_insert_dict = {}
    if not rccpsMap8583CTradeContext2Dhdcbka_dict.map(hdcbka_insert_dict):
        return AfaFlowControl.ExitThisFlow('A099','给插入字典赋值失败') 
    
    #=====登记数据库====
    AfaLoggerFunc.tradeInfo("登记数据库")
    res = rccpsDBTrcc_hdcbka.insertCmt(hdcbka_insert_dict)
    if( res == -1 ):
        return AfaFlowControl.ExitThisFlow('A099','给插入字典赋值失败') 
    
    #=====开始给查询书报文赋值====
    AfaLoggerFunc.tradeInfo("开始给查询书报文赋值")
    #====报文头====
    TradeContext.MSGTYPCO = 'SET008'
    TradeContext.RCVMBRCO = TradeContext.RCVSTLBIN
    TradeContext.SNDMBRCO = TradeContext.SNDSTLBIN
    TradeContext.SNDBRHCO = TradeContext.BESBNO
    TradeContext.SNDCLKNO = TradeContext.BETELR
    TradeContext.SNDTRDAT = TradeContext.BJEDTE
    TradeContext.SNDTRTIM = TradeContext.BJETIM
    TradeContext.MSGFLGNO = TradeContext.SNDSTLBIN + TradeContext.TRCDAT + TradeContext.SerialNo
    TradeContext.ORMFN    = wtrbka_record['SNDMBRCO'] + wtrbka_record['TRCDAT'] + wtrbka_record['TRCNO']
    TradeContext.NCCWKDAT = TradeContext.NCCworkDate
    TradeContext.OPRTYPNO = "99"
    TradeContext.ROPRTPNO = "30"
    TradeContext.TRANTYP  = "0"
    #=====业务要素集====
    TradeContext.TRCCO    = "9900511"
#    TradeContext.SNDBNKCO = ""
#    TradeContext.SNDBNKNM = ""
#    TradeContext.RCVBNKCO = ""
#    TradeContext.RCVBNKNM = ""
#    TradeContext.TRCDAT   = ""
#    TradeContext.TRCNO    = ""
    TradeContext.ORTRCCO  = wtrbka_record['TRCCO']
    TradeContext.ORTRCDAT = wtrbka_record['TRCDAT']
    TradeContext.ORTRCNO  = wtrbka_record['TRCNO']
    TradeContext.ORSNDBNK = wtrbka_record['SNDBNKCO']
    TradeContext.ORRCVBNK = wtrbka_record['RCVBNKCO']
    if( wtrbka_record['CUR'] == '01' ):
        TradeContext.ORCUR = 'CNY'
    else:
        TradeContext.ORCUR = wtrbka_record['CUR']
    TradeContext.OROCCAMT = str(wtrbka_record['OCCAMT'])
#    TradeContext.CONT     = ""

    AfaLoggerFunc.tradeInfo("交易前处理(本地操作,中心前处理) 退出")
    
    return True
    
def SubModuleDoSnd():
    AfaLoggerFunc.tradeInfo("交易后处理")
    
    #=====判断afe是否发送成功====
    AfaLoggerFunc.tradeInfo("判断afe是否发送成功")
    if TradeContext.errorCode != '0000':
        AfaLoggerFunc.tradeInfo("判断afe发送失败")
        return AfaFlowControl.ExitThisFlow(TradeContext.errorCode, TradeContext.errorMsg)
    
    AfaLoggerFunc.tradeInfo("判断afe发送成功")    
    #=====查询机构名====
    AfaLoggerFunc.tradeInfo("查询机构名")
    subbra_dict={'BESBNO':TradeContext.BESBNO}
    sub=rccpsDBTrcc_subbra.selectu(subbra_dict)
    if(sub==None):
        return AfaFlowControl.ExitThisFlow('A099','查询机构名失败' )
        
    if(len(sub)==0):
        return AfaFlowControl.ExitThisFlow('A099','没有相应的机构名' )
    
    #=================生成打印文本=============================================
    AfaLoggerFunc.tradeInfo("开始生成打印文本")
    
    txt = """\
            
            
                               %(BESBNM)s通存通兑查询书
                               
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
                             'OROCCAMT':float((TradeContext.OROCCAMT)),\
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
    
    AfaLoggerFunc.tradeInfo("交易后处理 退出")
    
    AfaLoggerFunc.tradeInfo("'***农信银系统：通存通兑往账交易.通存通兑查询书发送[8582] 退出")
    
    return True