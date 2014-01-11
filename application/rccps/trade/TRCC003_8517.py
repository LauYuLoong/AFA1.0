# -*- coding: gbk -*-
################################################################################
#   农信银系统：往账.中心类操作(1.本地操作 2.中心操作).汇票查复书录入
#===============================================================================
#   交易文件:   TRCC003_8517.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  潘广通
#   修改时间:   2008-08-01
################################################################################

import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBFunc,rccpsGetFunc,os
import rccpsDBTrcc_hpcbka,rccpsDBTrcc_subbra,rccpsDBTrcc_bilbka,rccpsDBTrcc_bilinf,rccpsMap8517CTradeContext2Dhpcbka_dict

#=====================交易前处理(本地操作,中心前处理)===========================
def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo("进入汇票查复书录入 1.本地操作 ")
    
    #=====查询汇票查询查复登记簿====
    where_dict_hpcbka = {'BJEDTE':TradeContext.BOJEDT,'BSPSQN':TradeContext.BOSPSQ}
    res_hpcbka = rccpsDBTrcc_hpcbka.selectu(where_dict_hpcbka)
    if( res_hpcbka == None ):
        return AfaFlowControl.ExitThisFlow("S999", "查询汇票查询查复登记簿失败")
        
    if( len(res_hpcbka) == 0 ):
        return AfaFlowControl.ExitThisFlow("S999", "查询汇票查询查复登记簿结果为空")
        
    if( res_hpcbka['ISDEAL'] == PL_ISDEAL_ISDO ):
        return AfaFlowControl.ExitThisFlow("S999", "此笔查询已被查复过了")
    
#    #=====查询汇票业务登记簿====
#    where_dict_bilbka = {'BJEDTE':TradeContext.BOJEDT,'BSPSQN':TradeContext.BOSPSQ}
#    res_bilbka = rccpsDBTrcc_bilbka.selectu(where_dict_bilbka)
#    if( res_bilbka == None ):
#        return AfaFlowControl.ExitThisFlow("S999", "查询汇票业务失败")
#        
#    if( len(res_bilbka) == 0 ):
#        return AfaFlowControl.ExitThisFlow("S999", "查询汇票业务结果为空")
#        
#    #=====查询汇票信息登记簿====
#    where_dict_bilinf = {'BILVER':res_bilbka['BILVER'],'BILNO':res_bilbka['BILNO'],'BILRS':res_bilbka['BILRS']}
#    res_bilinf = rccpsDBTrcc_bilinf.selectu(where_dict_bilinf)
#    if( res_bilinf == None ):
#        return AfaFlowControl.ExitThisFlow("S999", "查询汇票信息失败")
#        
#    if( len(res_bilinf) == 0 ):
#        return AfaFlowControl.ExitThisFlow("S999", "查询汇票信息结果为空")
        
#    AfaLoggerFunc.tradeInfo("RCVSTLBIN="+TradeContext.RCVSTLBIN)
#    AfaLoggerFunc.tradeInfo("RCVBNKCO="+TradeContext.RCVBNKCO)
    AfaLoggerFunc.tradeInfo("RCVBNKNM="+TradeContext.RCVBNKNM)
    
    #=====登记汇票查复书信息====
    TradeContext.BRSFLG   = PL_BRSFLG_SND
#    TradeContext.BESBNO   = res_hpcbka['BESBNO']
#    TradeContext.BETELR   = res_hpcbka['BETELR']
#    TradeContext.BEAUUS   = res_hpcbka['BEAUUS']
    TradeContext.NCCWKDAT = TradeContext.NCCworkDate
    TradeContext.TRCCO    = '9900527'
    TradeContext.TRCDAT   = TradeContext.BJEDTE
    TradeContext.TRCNO    = TradeContext.SerialNo
#    TradeContext.SNDBNKCO = 
#    TradeContext.SNDBNKNM = 
    TradeContext.SNDMBRCO = TradeContext.SNDSTLBIN
    TradeContext.RCVMBRCO = TradeContext.RCVSTLBIN
#    TradeContext.RCVBNKCO = res_hpcbka['SNDBNKCO']
#    TradeContext.RCVBNKNM = res_hpcbka['SNDBNKNM']
    TradeContext.ORTRCCO  = '9900526'
    TradeContext.BILVER   = res_hpcbka['BILVER']
    TradeContext.BILNO    = res_hpcbka['BILNO']
    TradeContext.BILDAT   = res_hpcbka['BILDAT']
    TradeContext.PAYWAY   = res_hpcbka['PAYWAY']
    TradeContext.CUR      = res_hpcbka['CUR']
    TradeContext.BILAMT   = str(res_hpcbka['BILAMT'])
    TradeContext.PYRACC   = res_hpcbka['PYRACC']
    TradeContext.PYRNAM   = res_hpcbka['PYRNAM']
    TradeContext.PYEACC   = res_hpcbka['PYEACC']
    TradeContext.PYENAM   = res_hpcbka['PYENAM']
#    TradeContext.CONT     = res_hpcbka['CONT']
    TradeContext.ISDEAL   = PL_ISDEAL_ISDO
    TradeContext.PRCCO    = ""
    TradeContext.BILENDDT = ""
    
    TradeContext.PRT_BILAMT = res_hpcbka['BILAMT']
    
    #====begin 蔡永贵 20110215 增加====
    #新票据号是16位，需要取后8位，版本号为02，同时要兼容老票据号8位，版本号为01
    if len(TradeContext.BILNO) == 16:
        TradeContext.TMP_BILNO = TradeContext.BILNO[-8:]
    else:
        TradeContext.TMP_BILNO = TradeContext.BILNO
    #============end============

    hpcbka_insert_dict = {}
    if not rccpsMap8517CTradeContext2Dhpcbka_dict.map(hpcbka_insert_dict):
        return AfaFlowControl.ExitThisFlow("S999", "为汇票查询查复登记薄赋值失败")
        
    ret = rccpsDBTrcc_hpcbka.insertCmt(hpcbka_insert_dict)
    if( ret <= 0 ):
        return AfaFlowControl.ExitThisFlow("S999", "为汇票查询查复登记薄赋值异常")
    
    AfaLoggerFunc.tradeInfo("结束登记查询书信息")
    
    #=====给查复报文赋值====
    AfaLoggerFunc.tradeInfo("开始为汇票查复书报文赋值")
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
#    TradeContext.TRCCO    = 
#    TradeContext.SNDBNKCO = 
#    TradeContext.SNDBNKNM = 
#    TradeContext.RCVBNKCO = 
#    TradeContext.RCVBNKNM = 
#    TradeContext.TRCDAT   = 
#    TradeContext.TRCNO    = 
#    TradeContext.BILDAT   = 
#    TradeContext.BILNO    = 
#    TradeContext.BILVER   = 
#    TradeContext.PAYWAY   = 
#    TradeContext.CUR      = 
#    TradeContext.BILAMT   = 
#    TradeContext.PYRACC   = 
#    TradeContext.PYRNAM   = 
#    TradeContext.PYEACC   = 
#    TradeContext.PYENAM   = 
#    TradeContext.CONT     = 
    TradeContext.ORQYDAT  = TradeContext.BOJEDT
    TradeContext.OQTSBNK  = res_hpcbka['SNDBNKCO']
    TradeContext.OQTNO    = res_hpcbka['TRCNO']
    
    AfaLoggerFunc.tradeInfo("结束为汇票查询书报文赋值")
    
    return True
    
    
#===================================================================
def SubModuleDoSnd(): 
    AfaLoggerFunc.tradeInfo("进入交易后处理")
    #=====判断afe是否发送成功====
    if TradeContext.errorCode != '0000':
        return AfaFlowControl.ExitThisFlow(TradeContext.errorCode, TradeContext.errorMsg)
        
    AfaLoggerFunc.tradeInfo('>>>发送成功')    
    
    #=====更新汇票查询查复登记簿中的查复标识====
    update_where_dict = {'BJEDTE':TradeContext.BOJEDT,'BSPSQN':TradeContext.BOSPSQ}
    update_dict = {'ISDEAL':PL_ISDEAL_ISDO}
    ret = rccpsDBTrcc_hpcbka.update(update_dict,update_where_dict)
    if( ret <= 0 ):
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
        
    AfaLoggerFunc.tradeInfo("开始生成打印文本")
    
    txt = """\
            
            
                               %(BESBNM)s汇票查复书
                               
        |-----------------------------------------------------------------------------|
        | 查复日期:     | %(BJEDTE)s                                                    |
        |-----------------------------------------------------------------------------|
        | 汇票查复书号: | %(BSPSQN)s                                                |
        |-----------------------------------------------------------------------------|
        | 发起行行号:   | %(SNDBNKCO)s                                                  |
        |-----------------------------------------------------------------------------|
        | 接收行行号:   | %(RCVBNKCO)s                                                  |
        |-----------------------------------------------------------------------------|
        | 出票日期:     | %(BILDAT)s                                                    |
        |-----------------------------------------------------------------------------|
        | 汇票金额:     | %(BILAMT)-15.2f                                             |
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
        | 查复内容:     |                                                             |
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
    
    file_name = 'rccps_' + TradeContext.BJEDTE + '_' + TradeContext.BSPSQN + '_8517'
    
    out_file = open(os.environ['AFAP_HOME'] + '/tmp/' + file_name,"wb")
    
    if out_file == None:
        return AfaFlowControl.ExitThisFlow("S999", "生成打印文件异常")

    print >> out_file,txt % {'BESBNM':(sub['BESBNM']).ljust(10,' '),\
                             'BJEDTE':(TradeContext.BJEDTE).ljust(8,' '),\
                             'BSPSQN':(TradeContext.BSPSQN).ljust(12,' '),\
                             'SNDBNKCO':(TradeContext.SNDBNKCO).ljust(10,' '),\
                             'RCVBNKCO':(TradeContext.RCVBNKCO).ljust(10,' '),\
                             'BILDAT':(TradeContext.BILDAT).ljust(8,' '),\
                             'BILAMT':(TradeContext.PRT_BILAMT),\
                             'BILNO':(TradeContext.BILNO).ljust(16,' '),\
                             'PYRACC':(TradeContext.PYRACC).ljust(32,' '),\
                             'PYRNAM':(TradeContext.PYRNAM).ljust(60,' '),\
                             'PYEACC':(TradeContext.PYEACC).ljust(32,' '),\
                             'PYENAM':(TradeContext.PYENAM).ljust(60,' '),\
                             'CONT1':(TradeContext.CONT[:68]).ljust(68,' '),\
                             'CONT2':(TradeContext.CONT[68:138]).ljust(70,' '),\
                             'CONT3':(TradeContext.CONT[138:208]).ljust(70,' '),\
                             'CONT4':(TradeContext.CONT[208:]).ljust(70,' ')}
    
    out_file.close
    
    TradeContext.PBDAFILE = file_name
    
    AfaLoggerFunc.tradeInfo("结束生成打印文本")
    
    AfaLoggerFunc.tradeInfo("结束交易后处理")
    
    return True