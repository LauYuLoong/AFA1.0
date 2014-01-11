# -*- coding: gbk -*-
################################################################################
#   农信银系统：往账.本地类操作模板(1.本地操作).交易名称
#===============================================================================
#   交易文件:   TRCC001_8535.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  刘雨龙
#   修改时间:   2008-07-11
#   功    能：  业务清单查询打印
#               01-汇兑往帐             02-汇兑来账
#               03-本行汇票             04-解付他行
#               05-退汇往帐             06-退汇来账
#               07-查询书               08-查复书
#               09-票据查询书           10-票据查复书
#               11-汇票查询书           12-汇票查复书
#               13-自由格式书           14-通存通兑来账
#               15-通存通兑往账
###############################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc
import rccpsDBFunc,rccpsDBTrcc_trcbka,rccpsDBTrcc_subbra,rccpsDBTrcc_spbsta,rccpsDBTrcc_bilbka
import rccpsDBTrcc_hdcbka,rccpsDBTrcc_pjcbka,rccpsDBTrcc_bilinf,rccpsDBTrcc_hpcbka,rccpsDBTrcc_wtrbka
from types import *
from rccpsConst import *

#=====================个性化处理(本地操作)======================================
def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.本地类操作交易[TRC001_8535]进入***' )
    
    #=====判断业务类型是否存在====
    if not (TradeContext.existVariable( "TRCCO" ) and len(TradeContext.TRCCO) != 0):
        return AfaFlowControl.ExitThisFlow('S999','业务类型[TRCCO]不存在或为空')

    #=====取交易时间====
    TradeContext.BJEDTE = AfaUtilTools.GetSysDate( )

    #=====通过机构号查询机构名称====
    ret    = {}
    subbra = {'BESBNO':TradeContext.BESBNO}
    
    ret = rccpsDBTrcc_subbra.selectu(subbra)
    if ret == None:
        return AfaFlowControl.ExitThisFlow('S999','数据库操作失败')
    if len(ret) <= 0:
        if TradeContext.TRCCO not in ('14','15'):
            return AfaFlowControl.ExitThisFlow('S999','数据库中无机构号['+TradeContext.BESBNO+']')
        else:
            TradeContext.BESBNM = TradeContext.BESBNO
    else:
        TradeContext.BESBNM  = ret['BESBNM'] 

    #=====判断业务类型  01  汇兑往账====
    if TradeContext.TRCCO == '01':
        AfaLoggerFunc.tradeInfo('>>>汇兑往账清单打印操作')
        
        #=====组织查询语句====
        sql = "BJEDTE >= '" + TradeContext.STRDAT + "'"
        sql = sql + " AND BJEDTE <= '" + TradeContext.ENDDAT + "'"
        sql = sql + " AND BESBNO =  '" + TradeContext.BESBNO + "'"
        sql = sql + " AND BRSFLG = '"  + PL_BRSFLG_SND + "'"
        sql = sql + " AND TRCCO IN ('2000001','2000002','2000003','2000009') "

        #=====多笔查询====
        ordersql = "ORDER BY TRCCO ASC"
        records = rccpsDBTrcc_trcbka.selectm(1,0,sql,ordersql)
        
        if records == None:
            return AfaFlowControl.ExitThisFlow('A099','数据库操作失败' )
        if len(records) == 0:
            return AfaFlowControl.ExitThisFlow('A099','无满足条件记录' )

        #=====开始组织返回文件====
        filename="rccps_"+TradeContext.BETELR+"_"+AfaUtilTools.GetSysDate()+"_"+TradeContext.TransCode
        try:
            fpath=os.environ["AFAP_HOME"]+"/tmp/"
            f=open(fpath+filename,"w")
        except IOError:
            return AfaFlowControl.ExitThisFlow('S999','打开文件失败') 

        #=====写文件头====
        filecontext = "\n\n\n"
        filecontext = filecontext + "                                                  " + TradeContext.BESBNM + "电子汇兑往帐清单\n" 
        filecontext = filecontext + "起止日期：" + TradeContext.STRDAT + "~" + TradeContext.ENDDAT + "\n"
        filecontext = filecontext + "序号 业务种类　报单序号  　报单日期 发起行行号 接收行行号　金额      付款人账号　　　　　　　　　　"
        filecontext = filecontext + "收款人账号　　　　　　　　　　业务状态\n"
        filecontext = filecontext + "=================================================================================================================\n"
        f.write(filecontext+"\n")

        #=====循环组织文件数据====
        for i in range(0,len(records)):
            #=====通过报单序号和日期取状态====
            bcstat      = {}
            bcstat_dict = {'BJEDTE':records[i]['BJEDTE'],'BSPSQN':records[i]['BSPSQN']}
            bcstat     = rccpsDBTrcc_spbsta.selectu(bcstat_dict)
            if bcstat == None:
                return AfaFlowControl.ExitThisFlow('S999','数据库操作失败')
            if len(bcstat) <= 0:
                return AfaFlowControl.ExitThisFlow('S999','通过报单序号取业务状态失败')
                 
            #=====写文件====
            filecontext=str(i+1).ljust(4) +  records[i]['TRCCO'].ljust(10) + records[i]['BSPSQN'].ljust(13) \
                       + records[i]['BJEDTE'].ljust(9)    + records[i]['SNDBNKCO'].ljust(11)      \
                       + records[i]['RCVBNKCO'].ljust(11) + str(records[i]['OCCAMT']).ljust(11)   \
                       + records[i]['PYRACC'].ljust(30)   + records[i]['PYEACC'].ljust(34)        \
                       + bcstat['BCSTAT']
            f.write(filecontext+"\n")

        #=====添加打印日期等====       
        filecontext = "-----------------------------------------------------------------------------------------------------------------\n"
        filecontext = filecontext +  "    打印日期:" + TradeContext.BJEDTE + "                           授权：　　　　　　　　　　　记账：  \n"
        f.write(filecontext)

        f.close()
        AfaLoggerFunc.tradeInfo(">>>生成文件结束")
    #=====02 汇兑来帐====
    elif TradeContext.TRCCO == '02':
        AfaLoggerFunc.tradeInfo('>>>汇兑来账清单打印操作')
        
        #=====组织查询语句====
        sql = "BJEDTE >= '" + TradeContext.STRDAT + "'"
        sql = sql + " AND BJEDTE <= '" + TradeContext.ENDDAT + "'"
        sql = sql + " AND BESBNO =  '" + TradeContext.BESBNO + "'"
        sql = sql + " AND BRSFLG = '"  + PL_BRSFLG_RCV + "'"
        sql = sql + " AND TRCCO IN ('2000001','2000002','2000003','2000009')"

        #=====多笔查询====
        ordersql = "ORDER BY TRCCO ASC"
        records = rccpsDBTrcc_trcbka.selectm(1,0,sql,ordersql)
        if records == None:
            return AfaFlowControl.ExitThisFlow('A099','数据库操作失败' )
        if len(records) == 0:
            return AfaFlowControl.ExitThisFlow('A099','无满足条件记录' )

        #=====开始组织返回文件====
        filename="rccps_"+TradeContext.BETELR+"_"+AfaUtilTools.GetSysDate()+"_"+TradeContext.TransCode
        try:
            fpath=os.environ["AFAP_HOME"]+"/tmp/"
            f=open(fpath+filename,"w")
        except IOError:
            return AfaFlowControl.ExitThisFlow('S999','打开文件失败') 

        #=====写文件头====
        filecontext = "\n\n\n"
        filecontext = filecontext + "                                                  " + TradeContext.BESBNM + "电子汇兑来帐清单\n" 
        filecontext = filecontext + "起止日期：" + TradeContext.STRDAT + "~" + TradeContext.ENDDAT + "\n"
        filecontext = filecontext + "序号 汇票类别　报单序号  　出票日期 汇票号码  金额      申请人账号　　　　　　　　　　"
        filecontext = filecontext + "收款人账号　　　　　　　　　　业务状态\n"
        filecontext = filecontext + "=================================================================================================================\n"
        f.write(filecontext+"\n")

        #=====循环组织文件数据====
        for i in range(0,len(records)):
            #=====通过报单序号和日期取状态====
            bcstat      = {}
            bcstat_dict = {'BJEDTE':records[i]['BJEDTE'],'BSPSQN':records[i]['BSPSQN']}
            bcstat     = rccpsDBTrcc_spbsta.selectu(bcstat_dict)
            if bcstat == None:
                return AfaFlowControl.ExitThisFlow('S999','数据库操作失败')
            if len(bcstat) <= 0:
                return AfaFlowControl.ExitThisFlow('S999','通过报单序号取业务状态失败')
                 
            #=====写文件====
            filecontext=str(i+1).ljust(4) +  records[i]['TRCCO'].ljust(10) + records[i]['BSPSQN'].ljust(13) \
                       + records[i]['BJEDTE'].ljust(9)    + records[i]['SNDBNKCO'].ljust(11)      \
                       + records[i]['RCVBNKCO'].ljust(11) + str(records[i]['OCCAMT']).ljust(11)   \
                       + records[i]['PYRACC'].ljust(30)   + records[i]['PYEACC'].ljust(34)        \
                       + bcstat['BCSTAT']
            f.write(filecontext+"\n")

        #=====添加打印日期等====       
        filecontext = "-----------------------------------------------------------------------------------------------------------------\n"
        filecontext = filecontext +  "    打印日期:" + TradeContext.BJEDTE + "                           授权：　　　　　　　　　　　记账：  \n"
        f.write(filecontext)

        f.close()
        AfaLoggerFunc.tradeInfo(">>>生成文件结束")
    #====03 本行汇票签发====
    elif TradeContext.TRCCO == '03':
        AfaLoggerFunc.tradeInfo('>>>本行汇票签发清单打印操作')
        
        #====组织查询语句====
        sql = "BJEDTE >= '" + TradeContext.STRDAT + "'"
        sql = sql + " AND BJEDTE <= '" + TradeContext.ENDDAT + "'"
        sql = sql + " AND BESBNO =  '" + TradeContext.BESBNO + "'"
        sql = sql + " AND BRSFLG = '"  + PL_BRSFLG_SND + "'"
        sql = sql + " AND BILRS = '" + PL_BILRS_INN + "' AND HPSTAT = '" + PL_HPSTAT_SIGN + "'"

        #=====多笔查询====
        records = rccpsDBTrcc_bilbka.selectm(1,0,sql,"")
        if records == None:
            return AfaFlowControl.ExitThisFlow('A099','数据库操作失败' )
        if len(records) == 0:
            return AfaFlowControl.ExitThisFlow('A099','无满足条件记录' )

        #=====开始组织返回文件====
        filename="rccps_"+TradeContext.BETELR+"_"+AfaUtilTools.GetSysDate()+"_"+TradeContext.TransCode
        try:
            fpath=os.environ["AFAP_HOME"]+"/tmp/"
            f=open(fpath+filename,"w")
        except IOError:
            return AfaFlowControl.ExitThisFlow('S999','打开文件失败') 

        #=====写文件头====
        filecontext = "\n\n\n"
        filecontext = filecontext + "                                                  " + TradeContext.BESBNM + "本行汇票签发清单\n" 
        filecontext = filecontext + "起止日期：" + TradeContext.STRDAT + "~" + TradeContext.ENDDAT + "\n"
        filecontext = filecontext + "序号 汇票类别　报单序号  　出票日期  汇票号码　金    额  申请人账号　　　　　　　　　　"
        filecontext = filecontext + "收款人账号　　　　　　　　　　业务状态\n"
        filecontext = filecontext + "=================================================================================================================\n"
        f.write(filecontext+"\n")

        #=====循环组织文件数据====
        for i in range(0,len(records)):
            #=====通过汇票号码、汇票版本号取汇票类别====
            bilinf      = {}
            bilinf_dict = {'BILVER':records[i]['BILVER'],'BILNO':records[i]['BILNO'],'BILRS':records[i]['BILRS']}
            bilinf     = rccpsDBTrcc_bilinf.selectu(bilinf_dict)
            if bilinf == None:
                return AfaFlowControl.ExitThisFlow('S999','数据库操作失败')
            if len(bilinf) <= 0:
                return AfaFlowControl.ExitThisFlow('S999','通过汇票号码取汇票类别失败')
                 
            #=====写文件====
            filecontext=str(i+1).ljust(4) + bilinf['BILTYP'].ljust(10) + records[i]['BSPSQN'].ljust(13) \
                       + bilinf['BILDAT'].ljust(9)        + records[i]['BILNO'].ljust(11)         \
                       + str(bilinf['BILAMT']).ljust(11)  + bilinf['PYRACC'].ljust(30)            \
                       + bilinf['PYEACC'].ljust(34)       + bilinf['BILTYP']
            f.write(filecontext+"\n")

        #=====添加打印日期等====       
        filecontext = "-----------------------------------------------------------------------------------------------------------------\n"
        filecontext = filecontext +  "    打印日期:" + TradeContext.BJEDTE + "                           授权：　　　　　　　　　　　记账：  \n"
        f.write(filecontext)

        f.close()
        AfaLoggerFunc.tradeInfo(">>>生成文件结束")
    #====04 解付他行汇票====
    elif TradeContext.TRCCO == '04':
        AfaLoggerFunc.tradeInfo('>>>解付他行汇票清单打印操作')
        
        #====组织查询语句====
        sql = "BJEDTE >= '" + TradeContext.STRDAT + "'"
        sql = sql + " AND BJEDTE <= '" + TradeContext.ENDDAT + "'"
        sql = sql + " AND BESBNO =  '" + TradeContext.BESBNO + "'"
        sql = sql + " AND BRSFLG = '"  + PL_BRSFLG_SND + "'"
        sql = sql + " AND BILRS = '" + PL_BILRS_OUT + "'"

        #=====多笔查询====
        records = rccpsDBTrcc_bilbka.selectm(1,0,sql,"")
        if records == None:
            return AfaFlowControl.ExitThisFlow('A099','数据库操作失败' )
        if len(records) == 0:
            return AfaFlowControl.ExitThisFlow('A099','无满足条件记录' )

        #=====开始组织返回文件====
        filename="rccps_"+TradeContext.BETELR+"_"+AfaUtilTools.GetSysDate()+"_"+TradeContext.TransCode
        try:
            fpath=os.environ["AFAP_HOME"]+"/tmp/"
            f=open(fpath+filename,"w")
        except IOError:
            return AfaFlowControl.ExitThisFlow('S999','打开文件失败') 

        #=====写文件头====
        filecontext = "\n\n\n"
        filecontext = filecontext + "                                                  " + TradeContext.BESBNM + "解付他行汇票清单\n" 
        filecontext = filecontext + "起止日期：" + TradeContext.STRDAT + "~" + TradeContext.ENDDAT + "\n"
        filecontext = filecontext + "序号 汇票类别　报单序号  　出票日期  汇票号码　金    额  申请人账号　　　　　　　　　　"
        filecontext = filecontext + "收款人账号　　　　　　　　　　业务状态\n"
        filecontext = filecontext + "=================================================================================================================\n"
        f.write(filecontext+"\n")

        #=====循环组织文件数据====
        for i in range(0,len(records)):
            #=====通过汇票号码、汇票版本号取汇票类别====
            bilinf      = {}
            bilinf_dict = {'BILVER':records[i]['BILVER'],'BILNO':records[i]['BILNO'],'BILRS':records[i]['BILRS']}
            bilinf     = rccpsDBTrcc_bilinf.selectu(bilinf_dict)
            
            if bilinf == None:
                return AfaFlowControl.ExitThisFlow('S999','数据库操作失败')
            if len(bilinf) <= 0:
                return AfaFlowControl.ExitThisFlow('S999','通过汇票号码取汇票类别失败')
                 
            #=====写文件====
            filecontext=str(i+1).ljust(4) + bilinf['BILTYP'].ljust(10) + records[i]['BSPSQN'].ljust(13) \
                       + bilinf['BILDAT'].ljust(9)        + records[i]['BILNO'].ljust(11)         \
                       + str(bilinf['BILAMT']).ljust(11)  + bilinf['PYRACC'].ljust(30)            \
                       + bilinf['PYEACC'].ljust(34)       + bilinf['BILTYP']
            f.write(filecontext+"\n")

        #=====添加打印日期等====       
        filecontext = "-----------------------------------------------------------------------------------------------------------------\n"
        filecontext = filecontext +  "    打印日期:" + TradeContext.BJEDTE + "                           授权：　　　　　　　　　　　记账：  \n"
        f.write(filecontext)

        f.close()
        AfaLoggerFunc.tradeInfo(">>>生成文件结束")
    #=====05 退汇往帐====
    elif TradeContext.TRCCO == '05':
        AfaLoggerFunc.tradeInfo('>>>退汇往账清单打印操作')
        
        #=====组织查询语句====
        sql = "BJEDTE >= '" + TradeContext.STRDAT + "'"
        sql = sql + " AND BJEDTE <= '" + TradeContext.ENDDAT + "'"
        sql = sql + " AND BESBNO =  '" + TradeContext.BESBNO + "'"
        sql = sql + " AND BRSFLG = '"  + PL_BRSFLG_SND + "'"
        sql = sql + " AND TRCCO  = '2000004' "

        #=====多笔查询====
        ordersql = "ORDER BY TRCCO ASC"
        records = rccpsDBTrcc_trcbka.selectm(1,0,sql,ordersql)
        if records == None:
            return AfaFlowControl.ExitThisFlow('A099','数据库操作失败' )
        if len(records) == 0:
            return AfaFlowControl.ExitThisFlow('A099','无满足条件记录' )

        #=====开始组织返回文件====
        filename="rccps_"+TradeContext.BETELR+"_"+AfaUtilTools.GetSysDate()+"_"+TradeContext.TransCode
        try:
            fpath=os.environ["AFAP_HOME"]+"/tmp/"
            f=open(fpath+filename,"w")
        except IOError:
            return AfaFlowControl.ExitThisFlow('S999','打开文件失败') 

        #=====写文件头====
        filecontext = "\n\n\n"
        filecontext = filecontext + "                                                  " + TradeContext.BESBNM + "退汇往帐清单\n" 
        filecontext = filecontext + "起止日期：" + TradeContext.STRDAT + "~" + TradeContext.ENDDAT + "\n"
        filecontext = filecontext + "序号 业务种类　报单序号  　报单日期 发起行行号 接收行行号　金额      付款人账号　　　　　　　　　　"
        filecontext = filecontext + "收款人账号　　　　　　　　　　业务状态\n"
        filecontext = filecontext + "=================================================================================================================\n"
        f.write(filecontext+"\n")

        #=====循环组织文件数据====
        for i in range(0,len(records)):
            #=====通过报单序号和日期取状态====
            bcstat      = {}
            bcstat_dict = {'BJEDTE':records[i]['BJEDTE'],'BSPSQN':records[i]['BSPSQN']}
            bcstat     = rccpsDBTrcc_spbsta.selectu(bcstat_dict)
            if bcstat == None:
                return AfaFlowControl.ExitThisFlow('S999','数据库操作失败')
            if len(bcstat) <= 0:
                return AfaFlowControl.ExitThisFlow('S999','通过报单序号取业务状态失败')
                 
            #=====写文件====
            filecontext=str(i+1).ljust(4) +  records[i]['TRCCO'].ljust(10) + records[i]['BSPSQN'].ljust(13) \
                       + records[i]['BJEDTE'].ljust(9)    + records[i]['SNDBNKCO'].ljust(11)      \
                       + records[i]['RCVBNKCO'].ljust(11) + str(records[i]['OCCAMT']).ljust(11)   \
                       + records[i]['PYRACC'].ljust(30)   + records[i]['PYEACC'].ljust(34)        \
                       + bcstat['BCSTAT']
            f.write(filecontext+"\n")

        #=====添加打印日期等====       
        filecontext = "-----------------------------------------------------------------------------------------------------------------\n"
        filecontext = filecontext +  "    打印日期:" + TradeContext.BJEDTE + "                           授权：　　　　　　　　　　　记账：  \n"
        f.write(filecontext)

        f.close()
        AfaLoggerFunc.tradeInfo(">>>生成文件结束")
    #=====06 退汇来帐====
    elif TradeContext.TRCCO == '06':
        AfaLoggerFunc.tradeInfo('>>>退汇来账清单打印操作')
        
        #=====组织查询语句====
        sql = "BJEDTE >= '" + TradeContext.STRDAT + "'"
        sql = sql + " AND BJEDTE <= '" + TradeContext.ENDDAT + "'"
        sql = sql + " AND BESBNO =  '" + TradeContext.BESBNO + "'"
        sql = sql + " AND BRSFLG = '"  + PL_BRSFLG_RCV + "'"
        sql = sql + " AND TRCCO  = '2000004' "

        #=====多笔查询====
        ordersql = "ORDER BY TRCCO ASC"
        records = rccpsDBTrcc_trcbka.selectm(1,0,sql,ordersql)
        if records == None:
            return AfaFlowControl.ExitThisFlow('A099','数据库操作失败' )
        if len(records) == 0:
            return AfaFlowControl.ExitThisFlow('A099','无满足条件记录' )

        #=====开始组织返回文件====
        filename="rccps_"+TradeContext.BETELR+"_"+AfaUtilTools.GetSysDate()+"_"+TradeContext.TransCode
        try:
            fpath=os.environ["AFAP_HOME"]+"/tmp/"
            f=open(fpath+filename,"w")
        except IOError:
            return AfaFlowControl.ExitThisFlow('S999','打开文件失败') 

        #=====写文件头====
        filecontext = "\n\n\n"
        filecontext = filecontext + "                                                  " + TradeContext.BESBNM + "退汇来帐清单\n" 
        filecontext = filecontext + "起止日期：" + TradeContext.STRDAT + "~" + TradeContext.ENDDAT + "\n"
        filecontext = filecontext + "序号 业务种类　报单序号  　报单日期 发起行行号 接收行行号　金额      付款人账号　　　　　　　　　　"
        filecontext = filecontext + "收款人账号　　　　　　　　　　业务状态\n"
        filecontext = filecontext + "=================================================================================================================\n"
        f.write(filecontext+"\n")

        #=====循环组织文件数据====
        for i in range(0,len(records)):
            #=====通过报单序号和日期取状态====
            bcstat      = {}
            bcstat_dict = {'BJEDTE':records[i]['BJEDTE'],'BSPSQN':records[i]['BSPSQN']}
            bcstat     = rccpsDBTrcc_spbsta.selectu(bcstat_dict)
            if bcstat == None:
                return AfaFlowControl.ExitThisFlow('S999','数据库操作失败')
            if len(bcstat) <= 0:
                return AfaFlowControl.ExitThisFlow('S999','通过报单序号取业务状态失败')
                 
            #=====写文件====
            filecontext=str(i+1).ljust(4) +  records[i]['TRCCO'].ljust(10) + records[i]['BSPSQN'].ljust(13) \
                       + records[i]['BJEDTE'].ljust(9)    + records[i]['SNDBNKCO'].ljust(11)      \
                       + records[i]['RCVBNKCO'].ljust(11) + str(records[i]['OCCAMT']).ljust(11)   \
                       + records[i]['PYRACC'].ljust(30)   + records[i]['PYEACC'].ljust(34)        \
                       + bcstat['BCSTAT'] 
            f.write(filecontext+"\n")

        #=====添加打印日期等====       
        filecontext = "-----------------------------------------------------------------------------------------------------------------\n"
        filecontext = filecontext +  "    打印日期:" + TradeContext.BJEDTE + "                           授权：　　　　　　　　　　　记账：  \n"
        f.write(filecontext)

        f.close()
        AfaLoggerFunc.tradeInfo(">>>生成文件结束")
    #=====07 汇兑查询书====
    elif TradeContext.TRCCO == '07':
        AfaLoggerFunc.tradeInfo('>>>汇兑查询书清单打印操作')
        
        #=====组织查询语句====
        sql = "BJEDTE >= '" + TradeContext.STRDAT + "'"
        sql = sql + " AND BJEDTE <= '" + TradeContext.ENDDAT + "'"
        sql = sql + " AND BESBNO =  '" + TradeContext.BESBNO + "'"
        sql = sql + " AND TRCCO IN ('9900511','9900522') "

        #=====多笔查询====
        ordersql = "ORDER BY TRCCO ASC"
        records = rccpsDBTrcc_hdcbka.selectm(1,0,sql,ordersql)
        if records == None:
            return AfaFlowControl.ExitThisFlow('A099','数据库操作失败' )
        if len(records) == 0:
            return AfaFlowControl.ExitThisFlow('A099','无满足条件记录' )

        #=====开始组织返回文件====
        filename="rccps_"+TradeContext.BETELR+"_"+AfaUtilTools.GetSysDate()+"_"+TradeContext.TransCode
        try:
            fpath=os.environ["AFAP_HOME"]+"/tmp/"
            f=open(fpath+filename,"w")
        except IOError:
            return AfaFlowControl.ExitThisFlow('S999','打开文件失败') 

        #=====写文件头====
        filecontext = "\n\n\n"
        filecontext = filecontext + "                                                  " + TradeContext.BESBNM + "汇兑查询书清单\n" 
        filecontext = filecontext + "起止日期：" + TradeContext.STRDAT + "~" + TradeContext.ENDDAT + "\n"
        filecontext = filecontext + "序号  查询书号  　查询日期  往来标志  发起行行号  接收行行号　状态\n"
        filecontext = filecontext + "=================================================================================================================\n"
        f.write(filecontext+"\n")

        #=====循环组织文件数据====
        for i in range(0,len(records)):
            #=====写文件====
            filecontext=str(i+1).ljust(4) + records[i]['BSPSQN'].ljust(13) \
                       + records[i]['BJEDTE'].ljust(13)    + records[i]['BRSFLG'].ljust(8)      \
                       + records[i]['SNDBNKCO'].ljust(12) + records[i]['RCVBNKCO'].ljust(13)    \
                       + records[i]['ISDEAL'] 
            f.write(filecontext+"\n")

        #=====添加打印日期等====       
        filecontext = "-----------------------------------------------------------------------------------------------------------------\n"
        filecontext = filecontext +  "    打印日期:" + TradeContext.BJEDTE + "                           授权：　　　　　　　　　　　记账：  \n"
        f.write(filecontext)

        f.close()
        AfaLoggerFunc.tradeInfo(">>>生成文件结束")
    #=====08 汇兑查复书====
    elif TradeContext.TRCCO == '08':
        AfaLoggerFunc.tradeInfo('>>>汇兑查复书清单打印操作')
        
        #=====组织查询语句====
        sql = "BJEDTE >= '" + TradeContext.STRDAT + "'"
        sql = sql + " AND BJEDTE <= '" + TradeContext.ENDDAT + "'"
        sql = sql + " AND BESBNO =  '" + TradeContext.BESBNO + "'"
        sql = sql + " AND TRCCO IN ('9900512','9900523') "

        #=====多笔查询====
        ordersql = "ORDER BY TRCCO ASC"
        records = rccpsDBTrcc_hdcbka.selectm(1,0,sql,ordersql)
        if records == None:
            return AfaFlowControl.ExitThisFlow('A099','数据库操作失败' )
        if len(records) == 0:
            return AfaFlowControl.ExitThisFlow('A099','无满足条件记录' )

        #=====开始组织返回文件====
        filename="rccps_"+TradeContext.BETELR+"_"+AfaUtilTools.GetSysDate()+"_"+TradeContext.TransCode
        try:
            fpath=os.environ["AFAP_HOME"]+"/tmp/"
            f=open(fpath+filename,"w")
        except IOError:
            return AfaFlowControl.ExitThisFlow('S999','打开文件失败') 

        #=====写文件头====
        filecontext = "\n\n\n"
        filecontext = filecontext + "                                                  " + TradeContext.BESBNM + "汇兑查复书清单\n" 
        filecontext = filecontext + "起止日期：" + TradeContext.STRDAT + "~" + TradeContext.ENDDAT + "\n"
        filecontext = filecontext + "序号  查询书号  　查询日期  往来标志  发起行行号  接收行行号　状态\n"
        filecontext = filecontext + "=================================================================================================================\n"
        f.write(filecontext+"\n")

        #=====循环组织文件数据====
        for i in range(0,len(records)):
            #=====写文件====
            filecontext=str(i+1).ljust(4) + records[i]['BSPSQN'].ljust(13) \
                       + records[i]['BJEDTE'].ljust(9)    + records[i]['BRSFLG'].ljust(10)      \
                       + records[i]['SNDBNKCO'].ljust(11) + records[i]['RCVBNKCO'].ljust(11)    \
                       + records[i]['ISDEAL'] 
            f.write(filecontext+"\n")

        #=====添加打印日期等====       
        filecontext = "-----------------------------------------------------------------------------------------------------------------\n"
        filecontext = filecontext +  "    打印日期:" + TradeContext.BJEDTE + "                           授权：　　　　　　　　　　　记账：  \n"
        f.write(filecontext)

        f.close()
        AfaLoggerFunc.tradeInfo(">>>生成文件结束")
    #=====09 票据查询书====
    elif TradeContext.TRCCO == '09':
        AfaLoggerFunc.tradeInfo('>>>票据查询书清单打印操作')
        
        #=====组织查询语句====
        sql = "BJEDTE >= '" + TradeContext.STRDAT + "'"
        sql = sql + " AND BJEDTE <= '" + TradeContext.ENDDAT + "'"
        sql = sql + " AND BESBNO =  '" + TradeContext.BESBNO + "'"
        sql = sql + " AND TRCCO  = '9900520' "

        #=====多笔查询====
        ordersql = "ORDER BY TRCCO ASC"
        records = rccpsDBTrcc_pjcbka.selectm(1,0,sql,ordersql)
        if records == None:
            return AfaFlowControl.ExitThisFlow('A099','数据库操作失败' )
        if len(records) == 0:
            return AfaFlowControl.ExitThisFlow('A099','无满足条件记录' )

        #=====开始组织返回文件====
        filename="rccps_"+TradeContext.BETELR+"_"+AfaUtilTools.GetSysDate()+"_"+TradeContext.TransCode
        try:
            fpath=os.environ["AFAP_HOME"]+"/tmp/"
            f=open(fpath+filename,"w")
        except IOError:
            return AfaFlowControl.ExitThisFlow('S999','打开文件失败') 

        #=====写文件头====
        filecontext = "\n\n\n"
        filecontext = filecontext + "                                                  " + TradeContext.BESBNM + "票据查询书清单\n" 
        filecontext = filecontext + "起止日期：" + TradeContext.STRDAT + "~" + TradeContext.ENDDAT + "\n"
        filecontext = filecontext + "序号  查询书号  　查询日期  往来标志  发起行行号  接收行行号　状态\n"
        filecontext = filecontext + "=================================================================================================================\n"
        f.write(filecontext+"\n")

        #=====循环组织文件数据====
        for i in range(0,len(records)):
            #=====写文件====
            filecontext=str(i+1).ljust(4) + records[i]['BSPSQN'].ljust(13) \
                       + records[i]['BJEDTE'].ljust(9)    + records[i]['BRSFLG'].ljust(10)      \
                       + records[i]['SNDBNKCO'].ljust(11) + records[i]['RCVBNKCO'].ljust(11)    \
                       + records[i]['ISDEAL'] 
            f.write(filecontext+"\n")
        

        #=====添加打印日期等====       
        filecontext = "-----------------------------------------------------------------------------------------------------------------\n"
        filecontext = filecontext +  "    打印日期:" + TradeContext.BJEDTE + "                           授权：　　　　　　　　　　　记账：  \n"
        f.write(filecontext)

        f.close()
        AfaLoggerFunc.tradeInfo(">>>生成文件结束")
    #=====10 票据查复书====
    elif TradeContext.TRCCO == '10':
        AfaLoggerFunc.tradeInfo('>>>票据查复书清单打印操作')
        
        #=====组织查询语句====
        sql = "BJEDTE >= '" + TradeContext.STRDAT + "'"
        sql = sql + " AND BJEDTE <= '" + TradeContext.ENDDAT + "'"
        sql = sql + " AND BESBNO =  '" + TradeContext.BESBNO + "'"
        sql = sql + " AND TRCCO  = '9900521' "

        #=====多笔查询====
        ordersql = "ORDER BY TRCCO ASC"
        records = rccpsDBTrcc_pjcbka.selectm(1,0,sql,ordersql)
        if records == None:
            return AfaFlowControl.ExitThisFlow('A099','数据库操作失败' )
        if len(records) == 0:
            return AfaFlowControl.ExitThisFlow('A099','无满足条件记录' )

        #=====开始组织返回文件====
        filename="rccps_"+TradeContext.BETELR+"_"+AfaUtilTools.GetSysDate()+"_"+TradeContext.TransCode
        try:
            fpath=os.environ["AFAP_HOME"]+"/tmp/"
            f=open(fpath+filename,"w")
        except IOError:
            return AfaFlowControl.ExitThisFlow('S999','打开文件失败') 

        #=====写文件头====
        filecontext = "\n\n\n"
        filecontext = filecontext + "                                                  " + TradeContext.BESBNM + "票据查复书清单\n" 
        filecontext = filecontext + "起止日期：" + TradeContext.STRDAT + "~" + TradeContext.ENDDAT + "\n"
        filecontext = filecontext + "序号  查询书号  　查询日期  往来标志  发起行行号  接收行行号　状态\n"
        filecontext = filecontext + "=================================================================================================================\n"
        f.write(filecontext+"\n")

        #=====循环组织文件数据====
        for i in range(0,len(records)):
            #=====写文件====
            filecontext=str(i+1).ljust(4) + records[i]['BSPSQN'].ljust(13) \
                       + records[i]['BJEDTE'].ljust(9)    + records[i]['BRSFLG'].ljust(10)      \
                       + records[i]['SNDBNKCO'].ljust(11) + records[i]['RCVBNKCO'].ljust(11)    \
                       + records[i]['ISDEAL'] 
            f.write(filecontext+"\n")

        #=====添加打印日期等====       
        filecontext = "-----------------------------------------------------------------------------------------------------------------\n"
        filecontext = filecontext +  "    打印日期:" + TradeContext.BJEDTE + "                           授权：　　　　　　　　　　　记账：  \n"
        f.write(filecontext)

        f.close()
        AfaLoggerFunc.tradeInfo(">>>生成文件结束")
    #=====11 汇票查询书====
    elif TradeContext.TRCCO == '11':
        AfaLoggerFunc.tradeInfo('>>>汇票查询书清单打印操作')
        
        #=====组织查询语句====
        sql = "BJEDTE >= '" + TradeContext.STRDAT + "'"
        sql = sql + " AND BJEDTE <= '" + TradeContext.ENDDAT + "'"
        sql = sql + " AND BESBNO =  '" + TradeContext.BESBNO + "'"
        sql = sql + " AND TRCCO  = '9900526' "

        #=====多笔查询====
        ordersql = "ORDER BY TRCCO ASC"
        records = rccpsDBTrcc_hpcbka.selectm(1,0,sql,ordersql)
        if records == None:
            return AfaFlowControl.ExitThisFlow('A099','数据库操作失败' )
        if len(records) == 0:
            return AfaFlowControl.ExitThisFlow('A099','无满足条件记录' )

        #=====开始组织返回文件====
        filename="rccps_"+TradeContext.BETELR+"_"+AfaUtilTools.GetSysDate()+"_"+TradeContext.TransCode
        try:
            fpath=os.environ["AFAP_HOME"]+"/tmp/"
            f=open(fpath+filename,"w")
        except IOError:
            return AfaFlowControl.ExitThisFlow('S999','打开文件失败') 

        #=====写文件头====
        filecontext = "\n\n\n"
        filecontext = filecontext + "                                                  " + TradeContext.BESBNM + "汇票查询书清单\n" 
        filecontext = filecontext + "起止日期：" + TradeContext.STRDAT + "~" + TradeContext.ENDDAT + "\n"
        filecontext = filecontext + "序号  查询书号    出票日期   汇票号码  出票金额  往来标志  发起行行号  接收行行号　状态\n"
        filecontext = filecontext + "=================================================================================================================\n"
        f.write(filecontext+"\n")

        #=====循环组织文件数据====
        for i in range(0,len(records)):
            #=====写文件====
            filecontext=str(i+1).ljust(4) + records[i]['BSPSQN'].ljust(15) \
                       + records[i]['BILDAT'].ljust(9)    + records[i]['BILNO'].ljust(11)  \
                       + str(records[i]['BILAMT']).ljust(15) + records[i]['BRSFLG'].ljust(6)      \
                       + records[i]['SNDBNKCO'].ljust(11) + records[i]['RCVBNKCO'].ljust(13)    \
                       + records[i]['ISDEAL'] 
            f.write(filecontext+"\n")

        #=====添加打印日期等====       
        filecontext = "-----------------------------------------------------------------------------------------------------------------\n"
        filecontext = filecontext +  "    打印日期:" + TradeContext.BJEDTE + "                           授权：　　　　　　　　　　　记账：  \n"
        f.write(filecontext)

        f.close()
        AfaLoggerFunc.tradeInfo(">>>生成文件结束")
    #=====12 汇票查复书====
    elif TradeContext.TRCCO == '12':
        AfaLoggerFunc.tradeInfo('>>>汇票查复书清单打印操作')
        
        #=====组织查询语句====
        sql = "BJEDTE >= '" + TradeContext.STRDAT + "'"
        sql = sql + " AND BJEDTE <= '" + TradeContext.ENDDAT + "'"
        sql = sql + " AND BESBNO =  '" + TradeContext.BESBNO + "'"
        sql = sql + " AND TRCCO  = '9900527' "

        #=====多笔查询====
        ordersql = "ORDER BY TRCCO ASC"
        records = rccpsDBTrcc_hpcbka.selectm(1,0,sql,ordersql)
        if records == None:
            return AfaFlowControl.ExitThisFlow('A099','数据库操作失败' )
        if len(records) == 0:
            return AfaFlowControl.ExitThisFlow('A099','无满足条件记录' )

        #=====开始组织返回文件====
        filename="rccps_"+TradeContext.BETELR+"_"+AfaUtilTools.GetSysDate()+"_"+TradeContext.TransCode
        try:
            fpath=os.environ["AFAP_HOME"]+"/tmp/"
            f=open(fpath+filename,"w")
        except IOError:
            return AfaFlowControl.ExitThisFlow('S999','打开文件失败') 

        #=====写文件头====
        filecontext = "\n\n\n"
        filecontext = filecontext + "                                                  " + TradeContext.BESBNM + "汇票查复书清单\n" 
        filecontext = filecontext + "起止日期：" + TradeContext.STRDAT + "~" + TradeContext.ENDDAT + "\n"
        filecontext = filecontext + "序号  查询书号  　查询日期  往来标志  发起行行号  接收行行号　状态\n"
        filecontext = filecontext + "=================================================================================================================\n"
        f.write(filecontext+"\n")

        #=====循环组织文件数据====
        for i in range(0,len(records)):
            #=====写文件====
            filecontext=str(i+1).ljust(4) + records[i]['BSPSQN'].ljust(13) \
                       + records[i]['BJEDTE'].ljust(9)    + records[i]['BRSFLG'].ljust(10)      \
                       + records[i]['SNDBNKCO'].ljust(11) + records[i]['RCVBNKCO'].ljust(11)    \
                       + records[i]['ISDEAL'] 
            f.write(filecontext+"\n")

        #=====添加打印日期等====       
        filecontext = "-----------------------------------------------------------------------------------------------------------------\n"
        filecontext = filecontext +  "    打印日期:" + TradeContext.BJEDTE + "                           授权：　　　　　　　　　　　记账：  \n"
        f.write(filecontext)

        f.close()
        AfaLoggerFunc.tradeInfo(">>>生成文件结束")
    #=====13 自由格式书====
    elif TradeContext.TRCCO == '13':
        AfaLoggerFunc.tradeInfo('>>>自由格式书清单打印操作')
        
        #=====组织查询语句====
        sql = "BJEDTE >= '" + TradeContext.STRDAT + "'"
        sql = sql + " AND BJEDTE <= '" + TradeContext.ENDDAT + "'"
        sql = sql + " AND BESBNO =  '" + TradeContext.BESBNO + "'"
        sql = sql + " AND TRCCO IN ('9900513','9900524') "

        #=====多笔查询====
        ordersql = "ORDER BY TRCCO ASC"
        records = rccpsDBTrcc_hdcbka.selectm(1,0,sql,ordersql)
        if records == None:
            return AfaFlowControl.ExitThisFlow('A099','数据库操作失败' )
        if len(records) == 0:
            return AfaFlowControl.ExitThisFlow('A099','无满足条件记录' )

        #=====开始组织返回文件====
        filename="rccps_"+TradeContext.BETELR+"_"+AfaUtilTools.GetSysDate()+"_"+TradeContext.TransCode
        try:
            fpath=os.environ["AFAP_HOME"]+"/tmp/"
            f=open(fpath+filename,"w")
        except IOError:
            return AfaFlowControl.ExitThisFlow('S999','打开文件失败') 

        #=====写文件头====
        filecontext = "\n\n\n"
        filecontext = filecontext + "                                                  " + TradeContext.BESBNM + "自由格式书清单\n" 
        filecontext = filecontext + "起止日期：" + TradeContext.STRDAT + "~" + TradeContext.ENDDAT + "\n"
        filecontext = filecontext + "序号 业务种类　报 单 序 号　报单日期  发起行行号 接收行行号　往来标志　状态\n"
        filecontext = filecontext + "=================================================================================================================\n"
        f.write(filecontext+"\n")

        #=====循环组织文件数据====
        for i in range(0,len(records)):
            #=====写文件====
            filecontext=str(i+1).ljust(4) +  records[i]['TRCCO'].ljust(10) + records[i]['BSPSQN'].ljust(13) \
                       + records[i]['BJEDTE'].ljust(9)    + records[i]['SNDBNKCO'].ljust(11)      \
                       + records[i]['RCVBNKCO'].ljust(11) + records[i]['BRSFLG'].ljust(10)   \
                       + records[i]['ISDEAL']
            f.write(filecontext+"\n")

        #=====添加打印日期等====       
        filecontext = "-----------------------------------------------------------------------------------------------------------------\n"
        filecontext = filecontext +  "    打印日期:" + TradeContext.BJEDTE + "                           授权：　　　　　　　　　　　记账：  \n"
        f.write(filecontext)

        f.close()
        AfaLoggerFunc.tradeInfo(">>>生成文件结束")
    
    #=====15 通存通兑往账====
    elif(TradeContext.TRCCO == '15'):
        AfaLoggerFunc.tradeInfo('>>>通存通兑往账清单打印操作')
        
        #=====组织查询语句====
        sql = "BJEDTE >= '" + TradeContext.STRDAT + "'"
        sql = sql + " AND BJEDTE <= '" + TradeContext.ENDDAT + "'"
        sql = sql + " AND BESBNO =  '" + TradeContext.BESBNO + "'"
        sql = sql + " AND BRSFLG =  '" + PL_BRSFLG_SND       + "'"
        
        #=====多笔查询====
        ordersql = "ORDER BY TRCCO ASC"
        records = rccpsDBTrcc_wtrbka.selectm(1,0,sql,ordersql)
        if records == None:
            return AfaFlowControl.ExitThisFlow('A099','数据库操作失败' )
        if len(records) == 0:
            return AfaFlowControl.ExitThisFlow('A099','无满足条件记录' )
            
        #=====开始组织返回文件====
        filename="rccps_"+TradeContext.BETELR+"_"+AfaUtilTools.GetSysDate()+"_"+TradeContext.TransCode
        try:
            fpath=os.environ["AFAP_HOME"]+"/tmp/"
            f=open(fpath+filename,"w")
        except IOError:
            return AfaFlowControl.ExitThisFlow('S999','打开文件失败') 

        #=====写文件头====
        filecontext = "\n\n\n"
        filecontext = filecontext + "                                                  " + TradeContext.BESBNM + "通存通兑往账清单\n" 
        filecontext = filecontext + "起止日期：" + TradeContext.STRDAT + "~" + TradeContext.ENDDAT + "\n"
        filecontext = filecontext + "序号　报单日期  报单序号      接收行行号  交易代码　收款人账号           　   付款人账号              金额           手续费         状态\n"
        filecontext = filecontext + "================================================================================================================================================\n"
        f.write(filecontext+"\n")

        #=====循环组织文件数据====
        for i in range(0,len(records)):
            #=====查询此笔交易的当前状态====
            where_dict = {}
            where_dict = {'BJEDTE':records[i]['BJEDTE'],'BSPSQN':records[i]['BSPSQN']}
            spb_dict = rccpsDBTrcc_spbsta.selectu(where_dict)
            if(spb_dict == None):
                return AfaFlowControl.ExitThisFlow('S999','查询业务的当前状态失败')
            
            elif(len(spb_dict) == 0):
                return AfaFlowControl.ExitThisFlow('S999','查询业务的当前状态结果为空')
                
            else:
                AfaLoggerFunc.tradeInfo("查询业务的当前状态成功")
            
            #=====写文件====
            filecontext=str(i+1).ljust(6) +  records[i]['BJEDTE'].ljust(10) + records[i]['BSPSQN'].ljust(14) \
                       + records[i]['RCVBNKCO'].ljust(12)    + records[i]['TRCCO'].ljust(10)      \
                       + records[i]['PYEACC'].ljust(26) + records[i]['PYRACC'].ljust(25)   \
                       + str(records[i]['OCCAMT']).ljust(15) + str(records[i]['CUSCHRG']).ljust(15) + spb_dict['BCSTAT'].ljust(2)
            f.write(filecontext+"\n")

        #=====添加打印日期等====       
        filecontext = "-----------------------------------------------------------------------------------------------------------------\n"
        filecontext = filecontext +  "    打印日期:" + TradeContext.BJEDTE + "                           授权：　　　　　　　　　　　记账：  \n"
        f.write(filecontext)

        f.close()
        AfaLoggerFunc.tradeInfo(">>>生成文件结束")
        
    #=====14 通存通兑来账====
    elif(TradeContext.TRCCO == '14'):
        AfaLoggerFunc.tradeInfo('>>>通存通兑往账清单打印操作')
        
        #=====组织查询语句====
        sql = "BJEDTE >= '" + TradeContext.STRDAT + "'"
        sql = sql + " AND BJEDTE <= '" + TradeContext.ENDDAT + "'"
        sql = sql + " AND BESBNO =  '" + TradeContext.BESBNO + "'"
        sql = sql + " AND BRSFLG =  '" + PL_BRSFLG_RCV       + "'"
        
        #=====多笔查询====
        ordersql = "ORDER BY TRCCO ASC"
        records = rccpsDBTrcc_wtrbka.selectm(1,0,sql,ordersql)
        if records == None:
            return AfaFlowControl.ExitThisFlow('A099','数据库操作失败' )
        if len(records) == 0:
            return AfaFlowControl.ExitThisFlow('A099','无满足条件记录' )
            
        #=====开始组织返回文件====
        filename="rccps_"+TradeContext.BETELR+"_"+AfaUtilTools.GetSysDate()+"_"+TradeContext.TransCode
        try:
            fpath=os.environ["AFAP_HOME"]+"/tmp/"
            f=open(fpath+filename,"w")
        except IOError:
            return AfaFlowControl.ExitThisFlow('S999','打开文件失败') 

        #=====写文件头====
        filecontext = "\n\n\n"
        filecontext = filecontext + "                                                  " + TradeContext.BESBNM + "通存通兑来账清单\n" 
        filecontext = filecontext + "起止日期：" + TradeContext.STRDAT + "~" + TradeContext.ENDDAT + "\n"
        filecontext = filecontext + "序号　报单日期  报单序号      接收行行号  交易代码　收款人账号           　   付款人账号              金额           手续费         状态\n"
        filecontext = filecontext + "================================================================================================================================================\n"
        f.write(filecontext+"\n")

        #=====循环组织文件数据====
        for i in range(0,len(records)):
            #=====查询此笔交易的当前状态====
            where_dict = {}
            where_dict = {'BJEDTE':records[i]['BJEDTE'],'BSPSQN':records[i]['BSPSQN']}
            spb_dict = rccpsDBTrcc_spbsta.selectu(where_dict)
            if(spb_dict == None):
                return AfaFlowControl.ExitThisFlow('S999','查询业务的当前状态失败')
            
            elif(len(spb_dict) == 0):
                return AfaFlowControl.ExitThisFlow('S999','查询业务的当前状态结果为空')
                
            else:
                AfaLoggerFunc.tradeInfo("查询业务的当前状态成功")
            
            #=====写文件====
            filecontext=str(i+1).ljust(6) +  records[i]['BJEDTE'].ljust(10) + records[i]['BSPSQN'].ljust(14) \
                       + records[i]['RCVBNKCO'].ljust(12)    + records[i]['TRCCO'].ljust(10)      \
                       + records[i]['PYEACC'].ljust(26) + records[i]['PYRACC'].ljust(25)   \
                       + str(records[i]['OCCAMT']).ljust(15) + str(records[i]['CUSCHRG']).ljust(15) + spb_dict['BCSTAT'].ljust(2)
            f.write(filecontext+"\n")

        #=====添加打印日期等====       
        filecontext = "-----------------------------------------------------------------------------------------------------------------\n"
        filecontext = filecontext +  "    打印日期:" + TradeContext.BJEDTE + "                           授权：　　　　　　　　　　　记账：  \n"
        f.write(filecontext)

        f.close()
        AfaLoggerFunc.tradeInfo(">>>生成文件结束")
    
    else:
        return AfaFlowControl.ExitThisFlow('S999','业务类型错')

    TradeContext.errorCode = '0000'
    TradeContext.errorMsg  = '成功'
    TradeContext.PRTDAT    = TradeContext.BJEDTE        #打印日期
    TradeContext.PBDAFILE  = filename                   #文件名
    
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.本地类操作交易[TRC001_8535]退出***' )
    return True
