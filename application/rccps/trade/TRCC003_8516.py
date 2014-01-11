# -*- coding: gbk -*-
################################################################################
#   农信银系统：往账.中心类操作(1.本地操作 2.中心操作).汇票查询书录入
#===============================================================================
#   交易文件:   TRCC003_8516.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  潘广通
#   修改时间:   2008-08-01
################################################################################

import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBFunc,rccpsGetFunc,os
import rccpsDBTrcc_hpcbka,rccpsDBTrcc_subbra,rccpsDBTrcc_bilinf,rccpsDBTrcc_paybnk
import rccpsMap8516CTradeContext2Dhpcbka_dict

#=====================交易前处理(本地操作,中心前处理)===========================
def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo("进入汇票查询书录入 1.本地操作 ")
    
    #====begin 蔡永贵 20110215 增加====
    #新票据号是16位，需要取后8位，版本号为02，同时要兼容老票据号8位，版本号为01
    if TradeContext.BILVER == '02':
        TradeContext.TMP_BILNO = TradeContext.BILNO[-8:]
    else:
        TradeContext.TMP_BILNO = TradeContext.BILNO
    #============end============
    
    #=====查询汇票信息=====
#    where_dict_bilinf = {'BILVER':TradeContext.BILVER,'BILNO':TradeContext.BILNO,'BILRS':PL_BILRS_OUT}
#    res_bilinf = rccpsDBTrcc_bilinf.selectu(where_dict_bilinf)
#    if( res_bilinf == None ):
#        return AfaFlowControl.ExitThisFlow("S999", "查询汇票信息失败")
#        
#    if( len(res_bilinf) == 0 ):
#        return AfaFlowControl.ExitThisFlow("S999", "查询汇票信息为空")
        

#    #=====查询行名行号====
#    where_dict_paybnk = {'BANKBIN':TradeContext.BESBNO}
#    res_paybnk = rccpsDBTrcc_paybnk.selectu(where_dict_paybnk)
#    if( res_paybnk == None ):
#        return AfaFlowControl.ExitThisFlow("S999", "查询行名行号失败")
#        
#    if( len(res_paybnk) == 0 ):
#        return AfaFlowControl.ExitThisFlow("S999", "查询行名行号为空")
#        
    #=====登记查询书信息====
    AfaLoggerFunc.tradeInfo("开始登记查询书信息")
    
    TradeContext.BRSFLG      =  PL_BRSFLG_SND
    TradeContext.NCCWKDAT    =  TradeContext.NCCworkDate
    TradeContext.TRCNO       =  TradeContext.SerialNo
#    TradeContext.SNDBNKCO    =  TradeContext.BESBNO
#    TradeContext.SNDBNKNM    =  res_paybnk['BANKNAM']
#    TradeContext.RCVBNKCO    =  res_bilinf['PAYBNKCO']
#    TradeContext.RCVBNKNM    =  res_bilinf['PAYBNKNM']
    TradeContext.BOJEDT      =  ""
    TradeContext.BOSPSQ      =  ""
    TradeContext.ORTRCCO     =  ""
    #TradeContext.TRCDAT      =  TradeContext.BJEDTE
#    TradeContext.BILDAT      =  res_bilinf['BILDAT']
#    TradeContext.PAYWAY      =  res_bilinf['PAYWAY']
#    TradeContext.CUR         =  res_bilinf['CUR']
#    TradeContext.BILAMT      =  str(res_bilinf['BILAMT'])
#    TradeContext.PYRACC      =  res_bilinf['PYRACC']
#    TradeContext.PYRNAM      =  res_bilinf['PYRNAM']
#    TradeContext.PYEACC      =  res_bilinf['PYEACC']
#    TradeContext.PYENAM      =  res_bilinf['PYENAM']
    TradeContext.ISDEAL      =  PL_ISDEAL_UNDO
    TradeContext.PRCCO       =  ""
    TradeContext.SNDMBRCO    =  TradeContext.SNDSTLBIN
    TradeContext.RCVMBRCO    =  TradeContext.RCVSTLBIN

    hpcbka_insert_dict = {}
    if not rccpsMap8516CTradeContext2Dhpcbka_dict.map(hpcbka_insert_dict):
        return AfaFlowControl.ExitThisFlow("S999", "为汇票查询查复登记薄赋值失败")
        
    ret = rccpsDBTrcc_hpcbka.insertCmt(hpcbka_insert_dict)
    if( ret <= 0 ):
        return AfaFlowControl.ExitThisFlow("S999", "为汇票查询查复登记薄赋值异常")
    
    AfaLoggerFunc.tradeInfo("结束登记查询书信息")
        
    #=====为汇票查询书报文赋值====
    AfaLoggerFunc.tradeInfo("开始为汇票查询书报文赋值")
    #=====报文头====
    TradeContext.MSGTYPCO = 'SET008'
    TradeContext.SNDBRHCO = TradeContext.BESBNO
    TradeContext.SNDCLKNO = TradeContext.BETELR
    TradeContext.SNDTRDAT = TradeContext.BJEDTE
    TradeContext.SNDTRTIM = TradeContext.BJETIM
    TradeContext.MSGFLGNO = TradeContext.SNDSTLBIN + TradeContext.TRCDAT + TradeContext.SerialNo
    TradeContext.NCCWKDAT = TradeContext.NCCworkDate
    TradeContext.OPRTYPNO = '99'
    TradeContext.ROPRTPNO = '21'
    TradeContext.TRANTYP  = '0'
    #=====扩展数据====
    TradeContext.TRCCO    = '9900526'    
#    TradeContext.BILDAT   = res_bilinf['BILDAT']
#    TradeContext.BILAMT   = str(res_bilinf['BILAMT'])
    
    #=====给前台接口赋值====
    TradeContext.BILENDDT = ""  #先这么放着
    
    AfaLoggerFunc.tradeInfo("结束为汇票查询书报文赋值")
    
    return True
    
#=====================交易后处理================================================
def SubModuleDoSnd(): 
    AfaLoggerFunc.tradeInfo("进入交易后处理")
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
            
            
                               %(BESBNM)s汇票查询书
                               
        |-----------------------------------------------------------------------------|
        | 查询日期:     | %(BJEDTE)s                                                    |
        |-----------------------------------------------------------------------------|
        | 查询书号:     | %(BSPSQN)s                                                |
        |-----------------------------------------------------------------------------|
        | 发起行行号:   | %(SNDBNKCO)s                                                  |
        |-----------------------------------------------------------------------------|
        | 接收行行号:   | %(RCVBNKCO)s                                                  |
        |-----------------------------------------------------------------------------|
        | 出票日期:     | %(BILDAT)s                                                    |
        |-----------------------------------------------------------------------------|
        | 汇票金额:     | %(BILAMT)s                                             |
        |-----------------------------------------------------------------------------|
        | 汇票号码:     | %(BILNO)s                                            |
        |-----------------------------------------------------------------------------|
        | 付款人账号:   | %(PYRACC)s                            |
        |-----------------------------------------------------------------------------|
        | 付款人名称:   | %(PYRNAM)s|
        |-----------------------------------------------------------------------------|
        | 收款人账号:   | %(PYEACC)s                            |
        |-----------------------------------------------------------------------------|
        | 收款人名称:   | %(PYENAM)s|
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
    
    file_name = 'rccps_' + TradeContext.BJEDTE + '_' + TradeContext.BSPSQN + '_8516'
    
    out_file = open(os.environ['AFAP_HOME'] + '/tmp/' + file_name,"wb")
    
    if out_file == None:
        return AfaFlowControl.ExitThisFlow("S999", "生成打印文件异常")
    AfaLoggerFunc.tradeInfo(">>>>>>开始赋值")
    print >> out_file,txt % {'BESBNM':(sub['BESBNM']).ljust(10,' '),\
                             'BJEDTE':(TradeContext.BJEDTE).ljust(8,' '),\
                             'BSPSQN':(TradeContext.BSPSQN).ljust(12,' '),\
                             'SNDBNKCO':(TradeContext.SNDBNKCO).ljust(10,' '),\
                             'RCVBNKCO':(TradeContext.RCVBNKCO).ljust(10,' '),\
                             'BILDAT':(TradeContext.BILDAT).ljust(8,' '),\
                             'BILAMT':(TradeContext.BILAMT).ljust(15,' '),\
                             'BILNO':(TradeContext.BILNO).ljust(16,' '),\
                             'PYRACC':(TradeContext.PYRACC).ljust(32,' '),\
                             'PYRNAM':(TradeContext.PYRNAM).ljust(60,' '),\
                             'PYEACC':(TradeContext.PYEACC).ljust(32,' '),\
                             'PYENAM':(TradeContext.PYENAM).ljust(60,' '),\
                             'CONT1':(TradeContext.CONT[:68]).ljust(68,' '),\
                             'CONT2':(TradeContext.CONT[68:138]).ljust(70,' '),\
                             'CONT3':(TradeContext.CONT[138:208]).ljust(70,' '),\
                             'CONT4':(TradeContext.CONT[208:]).ljust(70,' ')}
    AfaLoggerFunc.tradeInfo(">>>>>>结束赋值")
    out_file.close
    
    TradeContext.PBDAFILE = file_name
    
    AfaLoggerFunc.tradeInfo("结束生成打印文本")
    
    AfaLoggerFunc.tradeInfo("结束交易后处理")
    
    return True