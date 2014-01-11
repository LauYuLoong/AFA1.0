# -*- coding: gbk -*-
################################################################################
#   农信银系统：往账.中心类操作(1.本地操作 2.中心操作).票据查询书发送
#===============================================================================
#   交易文件:   TRCC003_8514.py
#   公司名称：  北京赞同科技有限公司
#   作    者：   戴智勇
#   修改时间:   2008-06-15
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBFunc,rccpsGetFunc
import rccpsDBTrcc_pjcbka,rccpsDBTrcc_subbra
import rccpsMap8514CTradeContext2Dpjcbka


#=====================交易前处理(本地操作,中心前处理)===========================
def SubModuleDoFst():
    
    #====begin 蔡永贵 20110215 增加====
    #新票据号是16位，需要取后8位，版本号为02，同时要兼容老票据号8位，版本号为01
    if len(TradeContext.BILNO) == 16:
        TradeContext.TMP_BILNO = TradeContext.BILNO[-8:]
    else:
        TradeContext.TMP_BILNO = TradeContext.BILNO
    #============end============
    
    #=================查询原交易信息============================================
    
    if not TradeContext.existVariable('BJEDTE'):
        return AfaFlowControl.ExitThisFlow("S999", "查询日期不能为空")
    
    if not TradeContext.existVariable('RCVBNKCO'):
        return AfaFlowControl.ExitThisFlow("S999", "接收行行号不能为空")
        
    #=================登记查询书信息============================================
    AfaLoggerFunc.tradeInfo(">>>开始登记票据业务查询书信息")
    
    TradeContext.NCCWKDAT = TradeContext.NCCworkDate
    TradeContext.ISDEAL   = PL_ISDEAL_UNDO            #查复标识为未查复
    
    pjcbka_insert_dict = {}
    if not rccpsMap8514CTradeContext2Dpjcbka.map(pjcbka_insert_dict):
        return AfaFlowControl.ExitThisFlow("S999", "为票据业务查询查复登记簿赋值异常")
        
    ret = rccpsDBTrcc_pjcbka.insertCmt(pjcbka_insert_dict)
    
    if ret <= 0:
        return AfaFlowControl.ExitThisFlow("S999", "登记票据业务查询书信息异常")
    
    AfaLoggerFunc.tradeInfo(">>>结束登记票据业务查询书信息")
    
    #=================为票据查询书报文赋值======================================
    AfaLoggerFunc.tradeInfo(">>>开始为票据查询书报文赋值")
    
    TradeContext.MSGTYPCO   = 'SET008'
    TradeContext.SNDBRHCO   = TradeContext.BESBNO
    TradeContext.SNDCLKNO   = TradeContext.BETELR
    TradeContext.SNDTRDAT   = TradeContext.BJEDTE
    TradeContext.SNDTRTIM   = TradeContext.BJETIM
    TradeContext.MSGFLGNO   = TradeContext.SNDSTLBIN + TradeContext.TRCDAT + TradeContext.SerialNo
    TradeContext.NCCWKDAT   = TradeContext.NCCworkDate
    TradeContext.OPRTYPNO   = '99'
    TradeContext.ROPRTPNO   = '20'
    TradeContext.TRANTYP    = '0'
    #TradeContext.TRCDAT     = TradeContext.BJEDTE
    TradeContext.TRCNO      = TradeContext.SerialNo
    #TradeContext.BILPNAM    = TradeContext.PYENAM
    #TradeContext.BILAMT   = str(TradeContext.BILAMT)
    
    AfaLoggerFunc.tradeInfo(">>>结束为票据查询书报文赋值")
    
    
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
    
    #=================生成打印文本=============================================
    AfaLoggerFunc.tradeInfo("开始生成打印文本")
    
    txt = """\
            
            
                               %(BESBNM)s票据查询书
                               
        |-----------------------------------------------------------------------------|
        | 查询日期:     | %(BJEDTE)s                                                    |
        |-----------------------------------------------------------------------------|
        | 票据查询书号: | %(BSPSQN)s                                                |
        |-----------------------------------------------------------------------------|
        | 发起行行号:   | %(SNDBNKCO)s                                                  |
        |-----------------------------------------------------------------------------|
        | 接收行行号:   | %(RCVBNKCO)s                                                  |
        |-----------------------------------------------------------------------------|
        | 票据日期:     | %(BILDAT)s                                                    |
        |-----------------------------------------------------------------------------|
        | 票据到期日:   | %(BILENDDT)s                                                    |
        |-----------------------------------------------------------------------------|
        | 票据号码:     | %(BILNO)s                                            |
        |-----------------------------------------------------------------------------|
        | 出票金额:     | %(BILAMT)s                                             |
        |-----------------------------------------------------------------------------|
        | 出票人名称:   | %(BILPNAM)s|
        |-----------------------------------------------------------------------------|
        | 付款行名称:   | %(HONBNKNM)s|
        |-----------------------------------------------------------------------------|
        | 查询内容:     |                                                             |
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
    
    file_name = 'rccps_' + TradeContext.BJEDTE + '_' + TradeContext.BSPSQN + '_8514'
    
    out_file = open(os.environ['AFAP_HOME'] + '/tmp/' + file_name,"wb")
    
    if out_file == None:
        return AfaFlowControl.ExitThisFlow("S999", "生成打印文件异常")
    
    print >> out_file,txt % {'BESBNM':(sub['BESBNM']).ljust(10,' '),\
                             'BJEDTE':(TradeContext.BJEDTE).ljust(8,' '),\
                             'BSPSQN':(TradeContext.BSPSQN).ljust(12,' '),\
                             'SNDBNKCO':(TradeContext.SNDBNKCO).ljust(10,' '),\
                             'RCVBNKCO':(TradeContext.RCVBNKCO).ljust(10,' '),\
                             'BILDAT':(TradeContext.BILDAT).ljust(8,' '),\
                             'BILENDDT':(TradeContext.BILENDDT).ljust(8,' '),\
                             'BILNO':(TradeContext.BILNO).ljust(16,' '),\
                             'BILAMT':(TradeContext.BILAMT).ljust(15,' '),\
                             'BILPNAM':(TradeContext.BILPNAM).ljust(60,' '),\
                             'HONBNKNM':(TradeContext.HONBNKNM).ljust(60,' '),\
                             'CONT1':(TradeContext.CONT[:68]).ljust(68,' '),\
                             'CONT2':(TradeContext.CONT[68:138]).ljust(70,' '),\
                             'CONT3':(TradeContext.CONT[138:208]).ljust(70,' '),\
                             'CONT4':(TradeContext.CONT[208:]).ljust(70,' ')}
    
    out_file.close
    
    TradeContext.PBDAFILE = file_name
    
    AfaLoggerFunc.tradeInfo("结束生成打印文本")
    
    return True
    
