# -*- coding: gbk -*-
################################################################################
#   农信银系统：往账.中心类操作(1.本地操作 2.中心操作).票据查复书发送
#===============================================================================
#   交易文件:   TRCC003_8515.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  关彬捷
#   修改时间:   2008-06-15
###############################################################################
#   修改者  :   刘雨龙
#   修改时间:   2008-07-21
#   功    能:   修改原交易中hpcbka汇票查询查复登记簿为pjcbka票据查询查复登记簿
#               修改查询原交易信息函数getTransTrc为rccpsDBTrcc_pjcbka.selectu
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBFunc,rccpsGetFunc
import rccpsDBTrcc_pjcbka,rccpsDBTrcc_subbra
import rccpsMap8515CTradeContext2Dpjcbka


#=====================交易前处理(本地操作,中心前处理)===========================
def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.中心类操作(1.本地操作).票据查复书发送[TRC003_8515]进入***' )
    
    #=================查询原交易信息============================================
    
    if not TradeContext.existVariable('BOSPSQ'):
        return AfaFlowControl.ExitThisFlow("S999", "原票据查询书号不能为空")
    
    if not TradeContext.existVariable('BOJEDT'):
        return AfaFlowControl.ExitThisFlow("S999", "原票据查询日期不能为空")
        
    AfaLoggerFunc.tradeInfo(">>>开始查询原查询书信息")
    
    pjcbka_dict = {}
    pjcbka_dict['BJEDTE']  =  TradeContext.BOJEDT
    pjcbka_dict['BSPSQN']  =  TradeContext.BOSPSQ
    ret = rccpsDBTrcc_pjcbka.selectu(pjcbka_dict)
    if ret == None:
        return  AfaFlowControl.ExitThisFlow('S999','查询票据查询查复业务登记簿异常') 
        
    TradeContext.OR_BJEDTE=ret['BJEDTE']
    TradeContext.OR_SNDBNKCO=ret['SNDBNKCO']
    
        
    AfaLoggerFunc.tradeInfo(">>>结束查询数据库信息")
    
    #=================登记查询书信息============================================
    AfaLoggerFunc.tradeInfo(">>>开始登记票据业务查询书信息")
    
    TradeContext.NCCWKDAT = TradeContext.NCCworkDate
    TradeContext.ISDEAL   = PL_ISDEAL_ISDO            #查复标识为未查复
    TradeContext.ORTRCCO  = ret['TRCCO']              #原交易代码
    TradeContext.BILNO    = ret['BILNO']              #票据号码
    TradeContext.BILDAT   = ret['BILDAT']             #票据日期
    TradeContext.BILPNAM  = ret['BILPNAM']            #出票人名称
    TradeContext.BILENDDT = ret['BILENDDT']           #票据截至日期
    TradeContext.BILAMT   = str(ret['BILAMT'])        #出票金额
    TradeContext.PYENAM   = ret['PYENAM']             #收款人名称
    TradeContext.HONBNKNM = ret['HONBNKNM']           #出票人名称
    TradeContext.OQTSBNK  = ret['SNDBNKCO']           #原发起行号
    TradeContext.OQTNO    = ret['TRCNO']              #原交易流水号
    TradeContext.ORQYDAT  = ret['BJEDTE']             #原查询日期
    
    #====begin 蔡永贵 20110215 增加====
    #新票据号是16位，需要取后8位，版本号为02，同时要兼容老票据号8位，版本号为01
    if len(TradeContext.BILNO) == 16:
        TradeContext.TMP_BILNO = TradeContext.BILNO[-8:]
    else:
        TradeContext.TMP_BILNO = TradeContext.BILNO
    #============end============
    
    #=====TradeContext向字典赋值操作====
    pjcbka_insert_dict = {}
    if not rccpsMap8515CTradeContext2Dpjcbka.map(pjcbka_insert_dict):
        return AfaFlowControl.ExitThisFlow("S999", "为票据业务查询查复登记簿赋值异常")
        
    #=====插入pjcbka票据查询查复登记簿====
    ret = rccpsDBTrcc_pjcbka.insertCmt(pjcbka_insert_dict)
    if ret <= 0:
        return AfaFlowControl.ExitThisFlow("S999", "登记票据业务查询书信息异常")

    AfaLoggerFunc.tradeInfo(">>>结束登记票据业务查询书信息")

    #=====刘雨龙 2008-07-21 新增更新原交易查询查复标志====
    pjcbka_update = {}
    pjcbka_set    = {}
    pjcbka_update['BJEDTE']  =  TradeContext.BOJEDT
    pjcbka_update['BSPSQN']  =  TradeContext.BOSPSQ
    pjcbka_set['ISDEAL']     =  TradeContext.ISDEAL
    ret = rccpsDBTrcc_pjcbka.updateCmt(pjcbka_set,pjcbka_update)
    if ret <= 0:
        return AfaFlowControl.ExitThisFlow("S999", "更新原票据查询书查询查复标识异常")
        
        
    
    #=================为票据查询书报文赋值======================================
    AfaLoggerFunc.tradeInfo(">>>开始为票据查询书报文赋值")
    
    TradeContext.SNDBRHCO   = TradeContext.BESBNO
    TradeContext.SNDCLKNO   = TradeContext.BETELR
    TradeContext.SNDTRDAT   = TradeContext.BJEDTE
    TradeContext.SNDTRTIM   = TradeContext.BJETIM
    #TradeContext.MSGFLGNO   = TradeContext.SNDSTLBIN + TradeContext.TRCDAT + TradeContext.SerialNo
    TradeContext.NCCWKDAT   = TradeContext.NCCworkDate
    TradeContext.OPRTYPNO   = '99'
    TradeContext.ROPRTPNO   = '20'
    TradeContext.TRANTYP    = '0'
    TradeContext.TRCNO      = TradeContext.SerialNo
    TradeContext.ORPYENAM   = TradeContext.PYENAM
    
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
            
       
                                         %(BESBNM)s票据查复书
                          
   |---------------------------------------------------------------------------------------|
   | 查复日期:               | %(BJEDTE)s                                                    |
   |---------------------------------------------------------------------------------------|
   | 票据查复书号:           | %(BSPSQN)s                                                |
   |---------------------------------------------------------------------------------------|
   | 发起行行号:             | %(SNDBNKCO)s                                                  |
   |---------------------------------------------------------------------------------------|
   | 接收行行号:             | %(RCVBNKCO)s                                                  |
   |---------------------------------------------------------------------------------------|
   | 票据日期:               | %(BILDAT)s                                                    |
   |---------------------------------------------------------------------------------------|
   | 票据到期日:             | %(BILENDDT)s                                                    |
   |---------------------------------------------------------------------------------------|
   | 票据号码:               | %(BILNO)s                                            |
   |---------------------------------------------------------------------------------------|
   | 出票人名称:             | %(BILPNAM)s|
   |---------------------------------------------------------------------------------------|
   | 收款人名称:             | %(PYENAM)s|
   |---------------------------------------------------------------------------------------|
   | 付款行名称:             | %(HONBNKNM)s|
   |---------------------------------------------------------------------------------------|
   | 原票据查询日期:         | %(BOJEDT)s                                                    |
   |---------------------------------------------------------------------------------------|
   | 原票据查询发起行行号:   | %(ORSNDBNKCO)s                                                  |
   |---------------------------------------------------------------------------------------|
   | 原票据查询书号:         | %(BOSPSQ)s                                                |
   |---------------------------------------------------------------------------------------|
   | 查复内容:               |                                                             |
   |---------------------------------------------------------------------------------------|
   |                                                                                       |
   |   %(CONT1)s                |
   |                                                                                       |
   |   %(CONT2)s              |
   |                                                                                       |
   |   %(CONT3)s              |
   |                                                                                       |
   |   %(CONT4)s              |
   |                                                                                       |
   |---------------------------------------------------------------------------------------|
   打印日期: %(BJEDTE)s      授权:                       记账:
    """
    
    file_name = 'rccps_' + TradeContext.BJEDTE + '_' + TradeContext.BSPSQN + '_8515'
    
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
                             'BILPNAM':(TradeContext.BILPNAM).ljust(60,' '),\
                             'PYENAM':(TradeContext.PYENAM).ljust(60,' '),\
                             'HONBNKNM':(TradeContext.HONBNKNM).ljust(60,' '),\
                             'BOJEDT':(TradeContext.OR_BJEDTE).ljust(8,' '),\
                             'ORSNDBNKCO':(TradeContext.OR_SNDBNKCO).ljust(10,' '),\
                             'BOSPSQ':(TradeContext.BOSPSQ).ljust(12,' '),\
                             'CONT1':(TradeContext.CONT[:68]).ljust(68,' '),\
                             'CONT2':(TradeContext.CONT[68:138]).ljust(70,' '),\
                             'CONT3':(TradeContext.CONT[138:208]).ljust(70,' '),\
                             'CONT4':(TradeContext.CONT[208:]).ljust(70,' ')}
    
    out_file.close
    
    TradeContext.PBDAFILE = file_name
    
    AfaLoggerFunc.tradeInfo("结束生成打印文本")
    
    
    return True
