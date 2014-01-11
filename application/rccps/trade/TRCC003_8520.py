# -*- coding: gbk -*-
################################################################################
#   农信银系统：往账.中心类操作(1.本地操作 2.中心操作).特约汇兑自由格式书发送
#===============================================================================
#   交易文件:   TRCC003_8520.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  刘雨龙
#   修改时间:   2008-07-02
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc
import rccpsDBFunc,rccpsGetFunc
import rccpsDBTrcc_hdcbka,rccpsDBTrcc_subbra
import rccpsMap8520CTradeContext2Dhdcbka

from types import *
from rccpsConst import *
#=====================交易前处理(本地操作,中心前处理)===========================
def SubModuleDoFst():
    #=================汇兑自由格式书检查============================================
    if not TradeContext.existVariable('RCVBNKCO'):
        return AfaFlowControl.ExitThisFlow("S999", "接收行行号不能为空")
        
    #=================登记汇兑自由格式书信息============================================
    AfaLoggerFunc.tradeInfo(">>>开始登记汇兑业务查询书信息")
    
    TradeContext.NCCWKDAT = TradeContext.NCCworkDate
    #=====刘雨龙 20080701 增加汇兑业务查询查复登记簿信息====
    TradeContext.TRCNO    = TradeContext.SerialNo        #交易流水号
    
    hdcbka_insert_dict = {}
    if not rccpsMap8520CTradeContext2Dhdcbka.map(hdcbka_insert_dict):
        return AfaFlowControl.ExitThisFlow("S999", "为汇兑业务查询查复登记簿赋值异常")
        
    ret = rccpsDBTrcc_hdcbka.insertCmt(hdcbka_insert_dict)
    
    if ret <= 0:
        return AfaFlowControl.ExitThisFlow("S999", "登记汇兑业务自由格式信息异常")
    
    AfaLoggerFunc.tradeInfo(">>>结束登记汇兑业务查询书信息")
    
    
    
    #=================为汇兑查询书报文赋值======================================
    AfaLoggerFunc.tradeInfo(">>>开始为汇兑查询书报文赋值")
    
    TradeContext.MSGTYPCO   = 'SET008'
    TradeContext.SNDBRHCO   = TradeContext.BESBNO
    TradeContext.SNDCLKNO   = TradeContext.BETELR
    TradeContext.SNDTRDAT   = TradeContext.BJEDTE
    TradeContext.SNDTRTIM   = TradeContext.BJETIM
    #TradeContext.MSGFLGNO   = TradeContext.SNDSTLBIN + TradeContext.TRCDAT + TradeContext.SerialNo
    TradeContext.ORMFN      = hdcbka_insert_dict['SNDMBRCO'] + hdcbka_insert_dict['TRCDAT'] + hdcbka_insert_dict['TRCNO']
    TradeContext.OPRTYPNO   = '99'
    TradeContext.ROPRTPNO   = '20'
    TradeContext.TRANTYP    = '0'
    
    
    AfaLoggerFunc.tradeInfo(">>>结束为汇兑自由格式书报文赋值")
    
    
    return True


#=====================交易后处理================================================
def SubModuleDoSnd():
    #=================判断afe是否发送成功=======================================
    if TradeContext.errorCode != '0000':
        return AfaFlowControl.ExitThisFlow(TradeContext.errorCode, TradeContext.errorMsg)
    
    AfaLoggerFunc.tradeInfo('发送成功')
    
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
            
            
                               %(BESBNM)s全国特约电子汇兑自由格式书
                               
        |-----------------------------------------------------------------------------|
        | 日期:                  |      %(BJEDTE)s                                      |
        |-----------------------------------------------------------------------------|
        | 特约汇兑自由格式书号:  |      %(BSPSQN)s                                  |
        |-----------------------------------------------------------------------------|
        | 发起行行号:            |      %(SNDBNKCO)s                                    |
        |-----------------------------------------------------------------------------|
        | 接收行行号:            |      %(RCVBNKCO)s                                    |
        |-----------------------------------------------------------------------------|
        | 内容:                  |                                                    |
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
    
    file_name = 'rccps_' + TradeContext.BJEDTE + '_' + TradeContext.BSPSQN + '_8520'
    
    out_file = open(os.environ['AFAP_HOME'] + '/tmp/' + file_name,"wb")
    
    if out_file == None:
        return AfaFlowControl.ExitThisFlow("S999", "生成打印文件异常")
    
    print >> out_file,txt % {'BESBNM':(sub['BESBNM']).ljust(10,' '),\
                             'BJEDTE':(TradeContext.BJEDTE).ljust(8,' '),\
                             'BSPSQN':(TradeContext.BSPSQN).ljust(12,' '),\
                             'SNDBNKCO':(TradeContext.SNDBNKCO).ljust(10,' '),\
                             'RCVBNKCO':(TradeContext.RCVBNKCO).ljust(10,' '),\
                             'CONT1':(TradeContext.CONT[:68]).ljust(68,' '),\
                             'CONT2':(TradeContext.CONT[68:138]).ljust(70,' '),\
                             'CONT3':(TradeContext.CONT[138:208]).ljust(70,' '),\
                             'CONT4':(TradeContext.CONT[208:]).ljust(70,' ')}
    
    out_file.close
    
    TradeContext.PBDAFILE = file_name
    
    AfaLoggerFunc.tradeInfo("结束生成打印文本")
    
    return True
    
