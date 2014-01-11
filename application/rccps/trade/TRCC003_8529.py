# -*- coding: gbk -*-
##################################################################
#   农信银.查询打印业务.支付业务状态查询
#=================================================================
#   程序文件:   TRCC003_8529.py
#   修改时间:   2008-06-05
#   修改者  ：  刘雨龙
#   修改时间：  2008-07-02
##################################################################
#   修改时间：  2008-08-07
#   修改内容：  增加汇票部分的业务
#   修改者  ：  潘广通
##################################################################
#   修改时间：  2008-10-24
#   修改内容：  增加通存通兑部分
#   修改者  ：  潘广通
##################################################################
import rccpsDBTrcc_ztcbka,TradeContext,AfaLoggerFunc,AfaFlowControl,AfaUtilTools,AfaDBFunc,rccpsDBFunc
import rccpsDBTrcc_trcbka,rccpsDBTrcc_wtrbka,rccpsMap8529Dtrcbka_dict2Dztcbka_dict,rccpsMap8529Dbilbka2Dztcbka
from types import *
from rccpsConst import *

def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( "进入查询 ")
    #=====判断接口是否存在====
    if( not TradeContext.existVariable( "BOJEDT" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '无报单日期,处理失败')
    if( not TradeContext.existVariable( "BOSPSQ" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '无交易序号,处理失败')
    if( not TradeContext.existVariable( "CONT" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '无查询内容,处理失败')
    
    #=====判断业务类型=====
    AfaLoggerFunc.tradeInfo("开始判断业务类型")
    
    if( TradeContext.OPRTYPNO == '20' ):    #汇兑
        AfaLoggerFunc.tradeInfo("进入汇兑处理")
            
        #=====查询数据库====
        trcbka_dict = {}
        res=rccpsDBFunc.getTransTrc(TradeContext.BOJEDT,TradeContext.BOSPSQ,trcbka_dict)
        if(res==False):
            return AfaFlowControl.ExitThisFlow('S999','数据库中无记录') 
        
        #=====刘雨龙 2008-07-21 新增往来账标志判断====
        if trcbka_dict['BRSFLG']  ==  PL_BRSFLG_RCV:
            return AfaFlowControl.ExitThisFlow('S999','非往帐业务不允许此操作')
        
        ztcbka_dict={}
        #=====设置插入字典====
        if not rccpsMap8529Dtrcbka_dict2Dztcbka_dict.map(trcbka_dict,ztcbka_dict):
            return AfaFlowControl.ExitThisFlow('M999','字典赋值错误')
 
        ztcbka_dict['CONT']=TradeContext.CONT   #手工添加的字段
        #=====刘雨龙 20080702 修改交易日期和报单序号====
        ztcbka_dict['BJEDTE']   =  TradeContext.BJEDTE
        ztcbka_dict['BSPSQN']   =  TradeContext.BSPSQN
        ztcbka_dict['ORTRCCO']  =  ztcbka_dict['TRCCO']
        ztcbka_dict['NCCWKDAT'] =  TradeContext.NCCworkDate
        ztcbka_dict['TRCCO']    =  "9900506"             #9900506 止付业务状态查询
        ztcbka_dict['TRCNO']    =  TradeContext.SerialNo
        ztcbka_dict['SNDMBRCO'] =  TradeContext.SNDSTLBIN
        ztcbka_dict['RCVMBRCO'] =  TradeContext.RCVSTLBIN
        ztcbka_dict['ISDEAL']   =  PL_ISDEAL_UNDO
        ztcbka_dict['BOJEDT']   =  TradeContext.BOJEDT
        ztcbka_dict['BOSPSQ']   =  TradeContext.BOSPSQ
    
        AfaLoggerFunc.tradeInfo("ztcbka_dict:"+str(ztcbka_dict))
        
        #=====插入数据库====
        AfaLoggerFunc.tradeInfo("开始插入数据库")
        #=====刘雨龙 20080702 修改insert_dict为ztcbka_dict====
        rowcount=rccpsDBTrcc_ztcbka.insertCmt(ztcbka_dict)
        if(rowcount==-1):
            return AfaFlowControl.ExitThisFlow('A099','插入数据库失败' )
    
        #=====刘雨龙 20080702 新增发送农信银中心字段====
        TradeContext.ORTRCCO  = ztcbka_dict['ORTRCCO']
        TradeContext.ORTRCDAT = ztcbka_dict['TRCDAT']
        TradeContext.ORTRCNO  = ztcbka_dict['TRCNO']
        TradeContext.ORSNDBNK = ztcbka_dict['SNDBNKCO']
        TradeContext.ORRCVBNK = ztcbka_dict['RCVBNKCO']
        TradeContext.OROCCAMT = str(ztcbka_dict['OCCAMT'])
        #TradeContext.OPRTYPNO = TradeContext.OPRTYPNO[0:2]
        TradeContext.OPRTYPNO = '99'
        TradeContext.ROPRTPNO = TradeContext.ORTRCCO[0:2]
        
        
    elif( TradeContext.OPRTYPNO == '21' ):    #汇票
        AfaLoggerFunc.tradeInfo("进入汇票处理")
        
        #=====查询数据库====
        bilbka_dict = {}
        res = rccpsDBFunc.getTransBil(TradeContext.BOJEDT,TradeContext.BOSPSQ,bilbka_dict)
        if( res == False ):
            return AfaFlowControl.ExitThisFlow('S999','数据库中无记录')
            
        #=====判断往来标志====
        if( bilbka_dict['BRSFLG'] == PL_BRSFLG_RCV ):
            return AfaFlowControl.ExitThisFlow('S999','非往帐业务不允许此操作')
        
        #=====查询汇票信息登记簿====
        bilinf_dict = {}
        ret = rccpsDBFunc.getInfoBil(bilbka_dict['BILVER'],bilbka_dict['BILNO'],bilbka_dict['BILRS'],bilinf_dict)
        if( ret == False ):
            return AfaFlowControl.ExitThisFlow('S999','汇票信息登记簿中无记录')
        
        #=====给插入字典赋值====
#        ztcbka_dict={}
#        if not rccpsMap8529Dbilbka2Dztcbka.map(bilbka_dict,ztcbka_dict):
#            return AfaFlowControl.ExitThisFlow('M999','字典赋值错误')
        AfaLoggerFunc.tradeInfo("开始给插入字典赋值")
        ztcbka_dict = {}
        
        ztcbka_dict['BJEDTE']   = TradeContext.BJEDTE
        ztcbka_dict['BSPSQN']   = TradeContext.BSPSQN
        ztcbka_dict['BRSFLG']   = PL_BRSFLG_SND
        ztcbka_dict['BESBNO']   = TradeContext.BESBNO
        ztcbka_dict['BEACSB']   = ""
        ztcbka_dict['BETELR']   = TradeContext.BETELR
        ztcbka_dict['BEAUUS']   = ""
        ztcbka_dict['NCCWKDAT'] = TradeContext.NCCworkDate
        ztcbka_dict['TRCCO']    = '9900506'
        ztcbka_dict['TRCDAT']   = TradeContext.TRCDAT
        ztcbka_dict['TRCNO']    = TradeContext.SerialNo
        ztcbka_dict['SNDMBRCO'] = bilbka_dict['SNDMBRCO']
        ztcbka_dict['RCVMBRCO'] = bilbka_dict['RCVMBRCO']
        ztcbka_dict['SNDBNKCO'] = TradeContext.SNDBNKCO
        ztcbka_dict['SNDBNKNM'] = TradeContext.SNDBNKNM
        ztcbka_dict['RCVBNKCO'] = bilbka_dict['RCVBNKCO']
        ztcbka_dict['RCVBNKNM'] = bilbka_dict['RCVBNKNM']
        ztcbka_dict['BOJEDT']   = bilbka_dict['BJEDTE']
        ztcbka_dict['BOSPSQ']   = bilbka_dict['BSPSQN']
        ztcbka_dict['ORTRCCO']  = bilbka_dict['TRCCO']
        ztcbka_dict['CUR']      = bilinf_dict['CUR']
        #=====判断业务状态====
        if( bilbka_dict['HPSTAT'] == PL_HPSTAT_PAYC ):  #解付
            ztcbka_dict['OCCAMT'] = bilinf_dict['OCCAMT']
        else:
            ztcbka_dict['OCCAMT'] = bilinf_dict['BILAMT']
        ztcbka_dict['CONT']     = TradeContext.CONT
        ztcbka_dict['NCCTRCST'] = ""
        ztcbka_dict['MBRTRCST'] = ""
        ztcbka_dict['ISDEAL']   = PL_ISDEAL_UNDO
        ztcbka_dict['PRCCO']    = ""
        ztcbka_dict['STRINFO']  = ""
        ztcbka_dict['NOTE1']    = bilbka_dict['NOTE1']
        ztcbka_dict['NOTE2']    = bilbka_dict['NOTE2']
        ztcbka_dict['NOTE3']    = bilbka_dict['NOTE3']
        ztcbka_dict['NOTE4']    = bilbka_dict['NOTE4']
        
        AfaLoggerFunc.tradeInfo("OCCAMT="+str(bilinf_dict['OCCAMT']))
        
        #=====登记业务状态查询查复登记簿====
        AfaLoggerFunc.tradeInfo("开始插入业务状态查询查复登记簿")
        rowcount=rccpsDBTrcc_ztcbka.insertCmt(ztcbka_dict)
        if(rowcount==-1):
            return AfaFlowControl.ExitThisFlow('A099','插入数据库失败' )
            
        #=====给业务状态查询报文赋值====
        AfaLoggerFunc.tradeInfo("开始给业务状态查询报文赋值")
        #=====报文头====
        TradeContext.NCCWKDAT = TradeContext.NCCworkDate
        TradeContext.RCVMBRCO = bilbka_dict['RCVMBRCO']
        TradeContext.RCVSTLBIN = bilbka_dict['RCVMBRCO']
        TradeContext.SNDSTLBIN = TradeContext.SNDSTLBIN
        TradeContext.SNDMBRCO = TradeContext.SNDSTLBIN
        TradeContext.SNDBRHCO = TradeContext.BESBNO
        TradeContext.SNDCLKNO = TradeContext.BETELR
#        TradeContext.SNDTRDAT = TradeContext.BJEDTE
#        TradeContext.SNDTRTIM = TradeContext.BJETIM
        TradeContext.ORMFN    = TradeContext.RCVSTLBIN+TradeContext.BJEDTE+TradeContext.SerialNo
        TradeContext.OPRTYPNO = '99'
        TradeContext.ROPRTPNO = '21'
        TradeContext.TRANTYP  = '0'
        #=====业务要素集====
        TradeContext.TRCCO    = '9900506'
#        TradeContext.SNDBNKCO = 
#        TradeContext.SNDBNKNM = 
        TradeContext.RCVBNKCO = bilbka_dict['RCVBNKCO']
        TradeContext.RCVBNKNM = bilbka_dict['RCVBNKNM']
        TradeContext.TRCDAT   = TradeContext.BJEDTE
        TradeContext.TRCNO    = TradeContext.SerialNo
        TradeContext.ORTRCCO  = bilbka_dict['TRCCO']
        TradeContext.ORTRCDAT = bilbka_dict['TRCDAT']
        TradeContext.ORTRCNO  = bilbka_dict['TRCNO']
        TradeContext.ORSNDBNK = bilbka_dict['SNDBNKCO']
        TradeContext.ORRCVBNK = bilbka_dict['RCVBNKCO']
        TradeContext.ORCUR    = bilinf_dict['CUR']        #11
        TradeContext.OROCCAMT = str(bilinf_dict['OCCAMT'])
        
        AfaLoggerFunc.tradeInfo("支付业务状态查询，汇票处理结束")
        
    #=====通存通兑=====
    elif( TradeContext.OPRTYPNO == '30' ):
        AfaLoggerFunc.tradeInfo("开始通存通兑处理")
        
        #=====判断要查询的交易是否为当日交易====
        if( TradeContext.BOJEDT != TradeContext.BJEDTE ):
            return AfaFlowControl.ExitThisFlow('A009','原交易不是当日交易')
        
        #=====查询通存通兑业务登记簿====
        AfaLoggerFunc.tradeInfo("查询通存通兑业务登记簿")
        where_dict = {'BJEDTE':TradeContext.BOJEDT,'BSPSQN':TradeContext.BOSPSQ}
        wtrbka_dict = rccpsDBTrcc_wtrbka.selectu(where_dict)
        if( wtrbka_dict == None ):
            return AfaFlowControl.ExitThisFlow('A009','查询通存通兑业务登记簿失败')
            
        if( len(wtrbka_dict) == 0 ):
            return AfaFlowControl.ExitThisFlow('A009','查询通存通兑业务登记簿结果为空') 
            
        #=====判断要查询的交易是否是本机构发起的====
        AfaLoggerFunc.tradeInfo("判断要查询的交易是否是本机构发起的")
        if( wtrbka_dict['BESBNO'] != TradeContext.BESBNO ):
            return AfaFlowControl.ExitThisFlow('A009','要查询的交易不是本机构发起的') 
            
        #=====登记业务状态查询查复登记簿====
        AfaLoggerFunc.tradeInfo("登记业务状态查询查复登记簿")
        
        #=====给插入字典赋值====
        AfaLoggerFunc.tradeInfo("给插入字典赋值")
        ztcbka_dict = {}
        ztcbka_dict['BJEDTE']   = TradeContext.BJEDTE
        ztcbka_dict['BSPSQN']   = TradeContext.BSPSQN
        ztcbka_dict['BRSFLG']   = PL_BRSFLG_SND
        ztcbka_dict['BESBNO']   = TradeContext.BESBNO
        ztcbka_dict['BEACSB']   = ""
        ztcbka_dict['BETELR']   = TradeContext.BETELR
        ztcbka_dict['BEAUUS']   = ""
        ztcbka_dict['NCCWKDAT'] = TradeContext.NCCworkDate
        ztcbka_dict['TRCCO']    = '9900506'
        ztcbka_dict['TRCDAT']   = TradeContext.TRCDAT
        ztcbka_dict['TRCNO']    = TradeContext.SerialNo
        ztcbka_dict['SNDMBRCO'] = wtrbka_dict['SNDMBRCO']
        ztcbka_dict['RCVMBRCO'] = wtrbka_dict['RCVMBRCO']
        ztcbka_dict['SNDBNKCO'] = TradeContext.SNDBNKCO
        ztcbka_dict['SNDBNKNM'] = TradeContext.SNDBNKNM
        ztcbka_dict['RCVBNKCO'] = wtrbka_dict['RCVBNKCO']
        ztcbka_dict['RCVBNKNM'] = wtrbka_dict['RCVBNKNM']
        ztcbka_dict['BOJEDT']   = wtrbka_dict['BJEDTE']
        ztcbka_dict['BOSPSQ']   = wtrbka_dict['BSPSQN']
        ztcbka_dict['ORTRCCO']  = wtrbka_dict['TRCCO']
        ztcbka_dict['CUR']      = wtrbka_dict['CUR']
        ztcbka_dict['OCCAMT']   = wtrbka_dict['OCCAMT']
        ztcbka_dict['CONT']     = TradeContext.CONT
        ztcbka_dict['NCCTRCST'] = ""
        ztcbka_dict['MBRTRCST'] = ""
        ztcbka_dict['ISDEAL']   = PL_ISDEAL_UNDO
        ztcbka_dict['PRCCO']    = ""
        ztcbka_dict['STRINFO']  = ""
        ztcbka_dict['NOTE1']    = wtrbka_dict['NOTE1']
        ztcbka_dict['NOTE2']    = wtrbka_dict['NOTE2']
        ztcbka_dict['NOTE3']    = wtrbka_dict['NOTE3']
        ztcbka_dict['NOTE4']    = wtrbka_dict['NOTE4']
        
        AfaLoggerFunc.tradeInfo("开始插入业务状态查询查复登记簿")
        rowcount=rccpsDBTrcc_ztcbka.insertCmt(ztcbka_dict)
        if(rowcount==-1):
            return AfaFlowControl.ExitThisFlow('A099','插入数据库失败' )
        
        #=====开始给也务状态查询报文赋值====
        #=====报文头====
        TradeContext.MSGTYPCO  = "SET008"
        TradeContext.NCCWKDAT  = TradeContext.NCCworkDate
        TradeContext.RCVMBRCO  = wtrbka_dict['RCVMBRCO']
        TradeContext.RCVSTLBIN = wtrbka_dict['RCVMBRCO']
        TradeContext.SNDSTLBIN = TradeContext.SNDSTLBIN
        TradeContext.SNDMBRCO  = TradeContext.SNDSTLBIN
        TradeContext.SNDBRHCO  = TradeContext.BESBNO
        TradeContext.SNDCLKNO  = TradeContext.BETELR
#        TradeContext.SNDTRDAT  = TradeContext.BJEDTE
#        TradeContext.SNDTRTIM  = TradeContext.BJETIM
        TradeContext.ORMFN     = wtrbka_dict['MSGFLGNO']
        TradeContext.OPRTYPNO  = '99'
        TradeContext.ROPRTPNO  = '30'
        TradeContext.TRANTYP   = '0'
        #=====业务要素集====
        TradeContext.TRCCO    = '9900506'
#        TradeContext.SNDBNKCO = 
#        TradeContext.SNDBNKNM = 
        TradeContext.RCVBNKCO = wtrbka_dict['RCVBNKCO']
        TradeContext.RCVBNKNM = wtrbka_dict['RCVBNKNM']
#        TradeContext.TRCDAT   = TradeContext.BJEDTE
        TradeContext.TRCNO    = TradeContext.SerialNo
        TradeContext.ORTRCCO  = wtrbka_dict['TRCCO']
        TradeContext.ORTRCDAT = wtrbka_dict['TRCDAT']
        TradeContext.ORTRCNO  = wtrbka_dict['TRCNO']
        TradeContext.ORSNDBNK = wtrbka_dict['SNDBNKCO']
        TradeContext.ORRCVBNK = wtrbka_dict['RCVBNKCO']
        TradeContext.ORCUR    = wtrbka_dict['CUR']        #11
        TradeContext.OROCCAMT = str(wtrbka_dict['OCCAMT'])
#        TradeContext.CONT     = 
    else:
        return AfaFlowControl.ExitThisFlow('S999','业务类型错误')
        
        
    return True

def SubModuleDoSnd():
    #=====判断errorCode====
    AfaLoggerFunc.tradeInfo("进入接口2")
    if TradeContext.errorCode != "0000":
        AfaLoggerFunc.tradeInfo("AFE发送失败")    
        return AfaFlowControl.ExitThisFlow(TradeContext.errorCode,TradeContext.errorMsg)
    
    AfaLoggerFunc.tradeInfo("AFE发送成功")    
    TradeContext.errorCode = '0000'
    TradeContext.errorMsg  = '交易成功'

    return True 
