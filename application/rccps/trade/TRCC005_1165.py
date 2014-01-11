# -*- coding: gbk -*-
##################################################################
#   农信银.通存通兑错帐控制解控接收交易.错帐控制解控交易   #他行发起的错帐控制解控交易,我行做为开户行对账务进行控制解控处理
#=================================================================
#   程序文件:   TRCC005_1165.py
#   修改时间:   2011—05-17
#   作者：      曾照泰
##################################################################

import TradeContext,AfaLoggerFunc,AfaFlowControl,AfaAfeFunc,HostContext,AfaUtilTools,HostContext,rccpsDBTrcc_wtrbka,rccpsDBTrcc_tddzmx
import AfaFunc,rccpsDBFunc
import AfaDBFunc,rccpsState,rccpsGetFunc,rccpsHostFunc
import rccpsDBTrcc_acckj
from types import *
from rccpsConst import *

def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo("'***农信银系统：通存通兑错帐控制解控接收交易.错帐控制解控查询[1165] 进入")
    
    AfaLoggerFunc.tradeDebug("TradeContext.STRINFO=" + TradeContext.STRINFO)  #描述信息
    
    AfaLoggerFunc.tradeInfo("交易前处理(登记流水,主机前处理)")
    
    #=====判断是否存在重复交易====
    AfaLoggerFunc.tradeInfo("判断是否存在重复交易")
    acckj_dict = {'TRCDAT':TradeContext.TRCDAT,'TRCNO':TradeContext.TRCNO,'SNDBNKCO':TradeContext.SNDBNKCO}#委托日期，交易流水号，发送行号
    record_acckj = rccpsDBTrcc_acckj.selectu(acckj_dict)
    if( record_acckj == None ):
        return AfaFlowControl.ExitThisFlow('A009','判断重复交易时查询错帐控制解控登记簿失败')
        
    if( len(record_acckj) > 0 ):    #存在重复交易
        AfaLoggerFunc.tradeInfo("存在重复交易")
        
        #====组织应答报文====
        if (TradeContext.TRCCO=='3000508'):
            Rcvmbrco = TradeContext.ORSNDSUBBNK     #发送方成员行号  
        if (TradeContext.TRCCO=='3000509'):  
            Rcvmbrco = TradeContext.SNDMBRCO      
        Sndmbrco = TradeContext.RCVMBRCO        #接收方成员行号
        Ormfn    = TradeContext.ORRCVSUBBNK     #报文标识号
        #=====报文头====
        TradeContext.MSGTYPCO = 'SET010'                    #报文类代码
        TradeContext.RCVSTLBIN = Rcvmbrco                    #接受方成员行号
        TradeContext.SNDSTLBIN = Sndmbrco                    #发送方成员行号
        TradeContext.SNDBRHCO = TradeContext.BESBNO         #发起行网点号
        TradeContext.SNDCLKNO = TradeContext.BETELR         #发起行柜员号
        TradeContext.SNDTRDAT = TradeContext.TRCDAT         #发起行交易日期
        TradeContext.SNDTRTIM = TradeContext.BJETIM         #发起行交易时间
        TradeContext.MSGFLGNO = Rcvmbrco+TradeContext.TRCDAT + TradeContext.SerialNo  #报文标识号
        TradeContext.ORMFN    = Ormfn                                                 #参考报文标示号
        TradeContext.NCCWKDAT = TradeContext.NCCworkDate    #中心工作日期
        TradeContext.OPRTYPNO = '30'                        #业务类型
        TradeContext.ROPRTPNO = '30'                        #参考业务类型
        TradeContext.TRANTYP  = '0'                         #传输类型
        #=====业务要素集====
        TradeContext.OCCAMT   =  record_acckj['OCCAMT']     #交易金额
        TradeContext.CHRG     =  record_acckj['CHRG']       #手续费
        TradeContext.ERRCONBAL=  record_acckj['ERRCONBAL']  #错帐控制金额
        TradeContext.BALANCE  =  record_acckj['BALANCE']    #账号实际金额、
        TradeContext.UNCONRST =  record_acckj['UNCONRST']   #解控处理结果
        TradeContext.UNCONRST =  record_acckj['UNCONRST']   #控制状态
        TradeContext.PRCCO    = "RCCS1105"                  #返回码
        TradeContext.STRINFO  = "重复报文"                  #附言
        
        #=====直接向AFE发送通讯回执====
        AfaLoggerFunc.tradeInfo("直接向AFE发送通讯回执")
        AfaAfeFunc.CommAfe()
        
        AfaLoggerFunc.tradeInfo("重复报文，做丢弃处理")
        
        return AfaFlowControl.ExitThisFlow('A009','重复报文做丢弃处理')
##############非重复交易#################################################################
    AfaLoggerFunc.tradeInfo("非重复交易") 
    #=====组织登记错帐控制解控登记簿的插入字典====
    AfaLoggerFunc.tradeInfo("组织登记错帐控制解控登记簿的插入字典")
    insert_dict = {}
     
    insert_dict['TRCDAT']      = TradeContext.TRCDAT         #委托日期 
    insert_dict['BSPSQN']      = TradeContext.BSPSQN         #保单序号
    insert_dict['MSGFLGNO']    = TradeContext.MSGFLGNO       #报文标识号
    insert_dict['ORMFN']       = TradeContext.ORMFN          #参考报文标识号
    insert_dict['TRCCO']       = TradeContext.TRCCO          #交易码
    insert_dict['BRSFLG']      = TradeContext.BRSFLG         #往来标识  
    insert_dict['BESBNO']      = TradeContext.BESBNO         #机构号 
    insert_dict['BEACSB']      = ""                          #账务机构号
    insert_dict['BETELR']      = TradeContext.BETELR         #机构柜员号
    insert_dict['BEAUUS']      = ""                          #授权柜员号
    insert_dict['BEAUPS']      = ""                          #授权柜员密码
    insert_dict['TERMID']      = ""                          #终端号
    insert_dict['OPTYPE']       = TradeContext.OPTYPE        #业务类型
    insert_dict['NCCWKDAT']    = TradeContext.NCCWKDAT       #农信银中心日期
    insert_dict['TRCNO']       = TradeContext.TRCNO          #交易流水号
    insert_dict['SNDMBRCO']    = TradeContext.SNDMBRCO       #发送方成员行号
    insert_dict['RCVMBRCO']    = TradeContext.RCVMBRCO       #接受成员行行号
    insert_dict['SNDBNKCO']    = TradeContext.SNDBNKCO       #发送方行号
    insert_dict['SNDBNKNM']    = TradeContext.SNDBNKNM       #发送方行名
    insert_dict['RCVBNKCO']    = TradeContext.RCVBNKCO       #接受行号
    insert_dict['RCVBNKNM']    = TradeContext.RCVBNKNM       #接受行名
    insert_dict['ORTRCDAT']    = TradeContext.ORTRCDAT       #原委托日期
    insert_dict['ORTRCCO']     = TradeContext.ORTRCCO        #原交易代码
    insert_dict['ORTRCNO']     = TradeContext.ORTRCNO        #交易流水号
    insert_dict['ORSNDSUBBNK'] = TradeContext.ORSNDSUBBNK    #原发起成员行号
    insert_dict['ORSNDBNK']    = TradeContext.ORSNDBNK       #原发起行号
    insert_dict['ORRCVSUBBNK'] = TradeContext.ORRCVSUBBNK    #原接受成员行行号
    insert_dict['ORRCVBNK']    = TradeContext.ORRCVBNK       #原接受行名
    insert_dict['ORPYRACC']    = TradeContext.ORPYRACC       #原付款人账号
    insert_dict['ORPYRNAM']    = TradeContext.ORPYRNAM       #原付款人名称
    insert_dict['ORPYEACC']    = TradeContext.ORPYEACC       #原收款人账号
    insert_dict['ORPYENAM']    = TradeContext.ORPYENAM       #原收款人名称
    insert_dict['CUR']         = '01'                        #币种
    insert_dict['OCCAMT']      = TradeContext.OCCAMT         #原交易金额
    insert_dict['CHRG']        = TradeContext.CHRG           #手续费
    insert_dict['ERRCONBAL']   = TradeContext.ERRCONBAL      #错帐控制金额
    if( TradeContext.existVariable( "BALANCE" ) ):
        insert_dict['BALANCE']     = TradeContext.BALANCE        #账号实际金额
    else:
        insert_dict['BALANCE'] = ""   
    if( TradeContext.existVariable( "UNCONRST" ) ):
        insert_dict['UNCONRST']    = TradeContext.UNCONRST       #解控处理结果
    else:
        insert_dict['UNCONRST']= ""   
    if( TradeContext.existVariable( "CONSTS" ) ):
        insert_dict['CONSTS']      = TradeContext.CONSTS         #控制状态
    else:
        insert_dict['CONSTS']  = ""    
    
    if( TradeContext.existVariable( "PRCCO" ) ):
        insert_dict['PRCCO']       = TradeContext.PRCCO          #中心返回码
    else:
        insert_dict['PRCCO']  =""   
    insert_dict['STRINFO']     = TradeContext.STRINFO           #附言
    insert_dict['NOTE1']       = TradeContext.BJETIM            #时间
    insert_dict['NOTE2']       = ""
    insert_dict['NOTE3']       = ""
    insert_dict['NOTE4']       = ""
    insert_dict['NOTE5']       = ""
    
    #=====登记错帐控制解控登记簿====
    AfaLoggerFunc.tradeInfo("开始登记错帐控制解控登记簿")
    AfaLoggerFunc.tradeInfo(insert_dict)
    res = rccpsDBTrcc_acckj.insertCmt(insert_dict)
    if( res == -1 ):
        return AfaFlowControl.ExitThisFlow('A009','登记错帐控制解控登记簿失败')
   
    #来账错帐控制处理    
    if(TradeContext.TRCCO=='3000508'):     #如果是来账错帐控制控处理， 先查询原需要控制的错帐是否存在，交易业务要素是否正确
        #=====组织查询字典====                            
        AfaLoggerFunc.tradeInfo(">>>开始组织查询字典，判断原需要错帐控制的记录是否存在")    
       
        wheresql_dic={}
        wheresql_dic['TRCDAT'] =TradeContext.ORTRCDAT   #原交易日期
        wheresql_dic['SNDBNKCO']=TradeContext.ORSNDBNK  #原发送行号
        wheresql_dic['TRCNO']=TradeContext.ORTRCNO      #原交易流水号
        
        #=====开始查询数据库====
        records=rccpsDBTrcc_wtrbka.selectu(wheresql_dic)          #查询错帐控制解控登记簿 
        AfaLoggerFunc.tradeDebug('>>>记录['+str(records)+']')
        if(records==None):                                        
            return AfaFlowControl.ExitThisFlow('A099','查询失败' )
        elif(len(records)==0):
            records=rccpsDBTrcc_tddzmx.selectu(wheresql_dic)      #查询错帐控制解控对账明细信息登记簿
            AfaLoggerFunc.tradeDebug('>>>记录['+str(records)+']')
            if(records==None):
                return AfaFlowControl.ExitThisFlow('A099','查询失败' )
            elif(len(records)==0): 
                TradeContext.CONSTS  ='1' 
                TradeContext.STRINFO ='错帐控制失败，无错帐原始记录,请检查输入数据的要素'  
                hzAfe()                                                                   
                return AfaFlowControl.ExitThisFlow('S999', "错帐控制失败，无错帐原始记录,请检查输入数据的要素")  
            else:
                
                ORTRCCO           = records['TRCCO']         #原交易代码         
                ORSNDSUBBNK       = records['SNDMBRCO']      #原发起成员行号     
                ORRCVSUBBNK       = records['RCVMBRCO']      #原接收成员行号      
                ORRCVBNK          = records['RCVBNKCO']      #原接受行号    
                ORPYRACC          = records['PYRACC']        #原付款人账号  
                ORPYEACC          = records['PYEACC']        #原收款人账号  
                OCCAMT            = str(records['OCCAMT'])   #原交易金额
                OCCAMT            = str((long)(((float)(OCCAMT)) * 100 + 0.1))   #去掉金额小数点，用于比较原交易金额是否相等
                CHRG              = str(records['CUSCHRG'])    #原手续费
                CHRG              = str((long)(((float)(CHRG)) * 100 + 0.1))     #去掉金额小数点，用于比较原手续费是否相等 
                PYRNAM            = records['PYRNAM'].strip()           #付款人名称
                PYENAM            = records['PYENAM'].strip()           #收款人名称
                 
            
                if (ORTRCCO!=TradeContext.ORTRCCO): 
                    TradeContext.CONSTS  ='1'
                    TradeContext.STRINFO ='错帐控制失败，原交易码不符'   
                    hzAfe()                                                                 
                    return AfaFlowControl.ExitThisFlow('S999', "错帐控制失败，原交易码不符")
                         
                if (ORSNDSUBBNK!=TradeContext.ORSNDSUBBNK):     
                    TradeContext.CONSTS  ='1'    
                    TradeContext.STRINFO = '错帐控制失败，原发起成员行号不符'  
                    hzAfe()                                                                   
                    return AfaFlowControl.ExitThisFlow('S999', "错帐控制失败，原发起成员行号不符")  
                                                                                 
                if (ORRCVSUBBNK!=TradeContext.ORRCVSUBBNK):                       
                    TradeContext.CONSTS  ='1'    
                    TradeContext.STRINFO  = '错帐控制失败，原接受成员行号不符'  
                    hzAfe()                                                                        
                    return AfaFlowControl.ExitThisFlow('S999', "错帐控制失败，原接受成员行号不符") 
                    
                if (ORRCVBNK!=TradeContext.ORRCVBNK):                         
                    TradeContext.CONSTS  ='1'
                    TradeContext.STRINFO  = '错帐控制失败，原接受行号不符'  
                    hzAfe()                                                                        
                    return AfaFlowControl.ExitThisFlow('S999', "错帐控制失败，原接受行号不符") 
                    
                if (ORPYRACC!=TradeContext.ORPYRACC):           
                    TradeContext.CONSTS  ='1' 
                    TradeContext.STRINFO  = '错帐控制失败，原付款人账号不符'   
                    hzAfe()                                                                      
                    return AfaFlowControl.ExitThisFlow('S999', "错帐控制失败，原付款人账号不符") 
                
                if (PYRNAM!=TradeContext.ORPYRNAM.strip()):                            
                    TradeContext.CONSTS  ='1'                                    
                    TradeContext.STRINFO  = '错帐控制失败，原付款人名称不符'                   
                    hzAfe()
                    return AfaFlowControl.ExitThisFlow('S999', "错帐控制失败，原付款人名称不符")
                                                                          
                if (ORPYEACC!=TradeContext.ORPYEACC):             
                    TradeContext.CONSTS  ='1'                     
                    TradeContext.STRINFO  = '错帐控制失败，原收款款人账号不符' 
                    hzAfe()                                                                     
                    return AfaFlowControl.ExitThisFlow('S999', "错帐控制失败，原收款款人账号不符")   
                
                if (PYENAM!=TradeContext.ORPYENAM.strip()):                            
                    TradeContext.CONSTS  ='1'                                    
                    TradeContext.STRINFO  = '错帐控制失败，原收款人名称不符'                   
                    hzAfe()
                    return AfaFlowControl.ExitThisFlow('S999', "错帐控制失败，原收款人名称不符")
               
                if (OCCAMT!=TradeContext.OCCAMT):              
                    TradeContext.CONSTS  ='1'                      
                    TradeContext.STRINFO  = '错帐控制失败，原交易金额不符'  
                    hzAfe()                                                                          
                    return AfaFlowControl.ExitThisFlow('S999', "错帐控制失败，原交易金额不符")
                       
                if (CHRG!=TradeContext.CHRG):              
                    TradeContext.CONSTS  ='1'                  
                    TradeContext.STRINFO  = '错帐控制失败，原交易手续费不符' 
                    hzAfe()                                                                     
                    return AfaFlowControl.ExitThisFlow('S999', "错帐控制失败，原交易手续费不符")  
        else:
            
            ORTRCCO           = records['TRCCO']           #原交易代码         
            ORSNDSUBBNK       = records['SNDMBRCO']        #原发起成员行号     
            ORRCVSUBBNK       = records['RCVMBRCO']        #原接收成员行号      
            ORRCVBNK          = records['RCVBNKCO']        #原接受行号    
            ORPYRACC          = records['PYRACC'].strip()  #原付款人账号  
            ORPYEACC          = records['PYEACC'].strip()  #原收款人账号  
            OCCAMT            = str(records['OCCAMT'])     #原交易金额
            OCCAMT            = str((long)(((float)(OCCAMT)) * 100 + 0.1))   #去掉金额小数点，用于比较原交易金额是否相等
            CHRG              = str(records['CUSCHRG'])    #原手续费
            CHRG              = str((long)(((float)(CHRG)) * 100 + 0.1))     #去掉金额小数点，用于比较原手续费是否相等
            PYRNAM            = records['PYRNAM'].strip()           #付款人名称
            PYENAM            = records['PYENAM'].strip()           #收款人名称
            
            AfaLoggerFunc.tradeInfo(CHRG)
            AfaLoggerFunc.tradeInfo(type(CHRG))
            AfaLoggerFunc.tradeInfo(type(TradeContext.CHRG))
            AfaLoggerFunc.tradeInfo("TradeContext.CHRG:" + TradeContext.CHRG) 
            
            if (ORTRCCO!=TradeContext.ORTRCCO):                              
                TradeContext.CONSTS  ='1'                                    
                TradeContext.STRINFO ='错帐控制失败，原交易码不符'  
                hzAfe()
                return AfaFlowControl.ExitThisFlow('S999', "错帐控制失败，原交易码不符")                       
                                                                        
            if (ORSNDSUBBNK!=TradeContext.ORSNDSUBBNK):                      
                TradeContext.CONSTS  ='1'                                    
                TradeContext.STRINFO = '错帐控制失败，原发起成员行号不符'
                hzAfe()                
                return AfaFlowControl.ExitThisFlow('S999', "错帐控制失败，原发起成员行号不符") 
                                                                            
            if (ORRCVSUBBNK!=TradeContext.ORRCVSUBBNK):                      
                TradeContext.CONSTS  ='1'                                    
                TradeContext.STRINFO  = '错帐控制失败，原接受成员行号不符'                 
                hzAfe()
                return AfaFlowControl.ExitThisFlow('S999', "错帐控制失败，原接受成员行号不符") 
                                                                             
            if (ORRCVBNK!=TradeContext.ORRCVBNK):                            
                TradeContext.CONSTS  ='1'                                    
                TradeContext.STRINFO  = '错帐控制失败，原接受行号不符'    
                hzAfe()
                return AfaFlowControl.ExitThisFlow('S999', "错帐控制失败，原接受行号不符")               
                                                                             
            if (ORPYRACC!=TradeContext.ORPYRACC.strip()):                            
                TradeContext.CONSTS  ='1'                                    
                TradeContext.STRINFO  = '错帐控制失败，原付款人账号不符'                   
                AfaLoggerFunc.tradeInfo(ORPYRACC)
                AfaLoggerFunc.tradeInfo(TradeContext.ORPYRACC)
                hzAfe()
                return AfaFlowControl.ExitThisFlow('S999', "错帐控制失败，原付款人账号不符")
            
            if (PYRNAM!=TradeContext.ORPYRNAM.strip()):                            
                TradeContext.CONSTS  ='1'                                    
                TradeContext.STRINFO  = '错帐控制失败，原付款人名称不符'                   
                hzAfe()
                return AfaFlowControl.ExitThisFlow('S999', "错帐控制失败，原付款人名称不符")
                                                                             
            if (ORPYEACC!=TradeContext.ORPYEACC.strip()):                            
                TradeContext.CONSTS  ='1'                                    
                TradeContext.STRINFO  = '错帐控制失败，原收款款人账号不符'                 
                hzAfe()
                return AfaFlowControl.ExitThisFlow('S999', "错帐控制失败，原收款款人账号不符")
            
            if (PYENAM!=TradeContext.ORPYENAM.strip()):                            
                TradeContext.CONSTS  ='1'                                    
                TradeContext.STRINFO  = '错帐控制失败，原收款人名称不符'                   
                hzAfe()
                return AfaFlowControl.ExitThisFlow('S999', "错帐控制失败，原收款人名称不符")
            
            if (OCCAMT!=TradeContext.OCCAMT): 
                                              
                TradeContext.CONSTS  ='1'                                    
                TradeContext.STRINFO  = '错帐控制失败，原交易金额不符'
                hzAfe()
                return AfaFlowControl.ExitThisFlow('S999', "错帐控制失败，原交易金额不符")
                                                                             
            if (CHRG!=TradeContext.CHRG):                                    
                TradeContext.CONSTS  ='1'                                    
                TradeContext.STRINFO  = '错帐控制失败，原交易手续费不符' 
                hzAfe()
                return AfaFlowControl.ExitThisFlow('S999', "错帐控制失败，原交易手续费不符")  
                  
        #=====组织查询字典====                            
        AfaLoggerFunc.tradeInfo(">>>开始组织查询字典，判断是否是重复控制")    
       
        wheresql_dic={}
        wheresql_dic['ORTRCDAT'] =TradeContext.ORTRCDAT     #原交易日期
        wheresql_dic['ORSNDBNK'] =TradeContext.ORSNDBNK     #原发送行号
        wheresql_dic['ORTRCNO']  =TradeContext.ORTRCNO      #原交易流水号
        if (TradeContext.TRCCO=='3000508'):
            wheresql_dic['TRCCO']    ='3000508'
            wheresql_dic['CONSTS']   ='0'                       #错帐控制成功标识             
        if (TradeContext.TRCCO=='3000509'):
            wheresql_dic['TRCCO']    ='3000509'
            wheresql_dic['UNCONRST'] ='0' 
            
        #=====开始查询数据库====
        records=rccpsDBTrcc_acckj.selectu(wheresql_dic)          #查询错帐控制解控登记簿 
        AfaLoggerFunc.tradeDebug('>>>记录['+str(records)+']')
        if(records==None):                                        
            return AfaFlowControl.ExitThisFlow('A099','查询失败' )
        if(len(records)>0):
            TradeContext.STRINFO  = '该错帐已经控制或已经解控，不能重复控制' 
            hzAfe()
            return AfaFlowControl.ExitThisFlow('S999', "该错帐已经控制或解控，不能重复控制")
        
        #=====================与主机通讯查询余额======================================== 
        TradeContext.HostCode = '8810'
        if(len(TradeContext.ORPYEACC.strip())!=0):
            TradeContext.ACCNO    = TradeContext.ORPYEACC
        else:
            TradeContext.ACCNO    = TradeContext.ORPYRACC
        
        #tiger新增
        if((TradeContext.ORTRCCO=='3000103')or(TradeContext.ORTRCCO=='3000105' )):
            AfaLoggerFunc.tradeInfo('tiger1111')
            TradeContext.ACCNO    = TradeContext.ORPYRACC
        
        AfaLoggerFunc.tradeInfo("test3" + TradeContext.ACCNO)
        
        rccpsHostFunc.CommHost('8810')
        
        #=====判断主机交易是否成功====   
        if( TradeContext.errorCode != '0000' ):  
            AfaLoggerFunc.tradeInfo("主机交易失败")                                        
            TradeContext.CONSTS  ='1'                                                                               
            TradeContext.STRINFO  = "主机查询余额失败 "+TradeContext.errorMsg[7:]+" "  #附言
            hzAfe()                                                                      
            return AfaFlowControl.ExitThisFlow('S999', "主机查询余额失败") 
        else:
            TradeContext.ACCBAL = HostContext.O1ACBL           #帐户余额
            TradeContext.AVLBAL = HostContext.O1CUBL           #可用余额
            TradeContext.BALANCE  = TradeContext.AVLBAL        #实际可用金额     
            AfaLoggerFunc.tradeInfo(HostContext.O1CUBL)
            
            if((float(TradeContext.AVLBAL)) < (float(TradeContext.ERRCONBAL))):    #账号可用金额不足错帐控制金额 
                TradeContext.CONSTS  ='1'                 
                TradeContext.STRINFO  = '账号可用金额不足错帐控制金额' 
                TradeContext.BALANCE  = TradeContext.AVLBAL    #实际可用金额 
                hzAfe()                                                         
                return AfaFlowControl.ExitThisFlow('S999', "账号可用金额不足错帐控制金额")  
        
        #调用0061主机错帐控制交易
        TradeContext.HostCode = '0061'
        TradeContext.kjflag='0'                                 #错帐控制标识位
        
    #来账错帐解控处理                                                                                            
    if(TradeContext.TRCCO=='3000509'):     #如果是来账错帐解控 先查询原需要解控的错帐是否存在，是否已经解控
        #=====组织查询字典====                                                                                       
        AfaLoggerFunc.tradeInfo(">>>开始组织查询字典,看原错帐控制记录是否存在")                                                               
                                                                                                                     
        wheresql_dic={}                                                                                              
        wheresql_dic['MSGFLGNO'] =TradeContext.ORMFN        #错帐控制的报文标识号                                                 
        wheresql_dic['TRCCO']    ='3000508'                 #交易码  
        wheresql_dic['TRCDAT'] =TradeContext.ORTRCDAT       #原交易日期
        wheresql_dic['SNDBNKCO'] =TradeContext.ORSNDBNK      #原发送行号
        wheresql_dic['TRCNO']  =TradeContext.ORTRCNO        #原交易流水号
        wheresql_dic['CONSTS']   ='0'                                                                   
                                                                                                                     
        #=====开始查询数据库====                                                                                     
        records=rccpsDBTrcc_acckj.selectu(wheresql_dic)          #查询错帐控制解控登记簿                             
        AfaLoggerFunc.tradeDebug('>>>记录['+str(records)+']')                                                        
        if(records==None):                                                                                           
            return AfaFlowControl.ExitThisFlow('A099','查询失败' )                                                   
        elif(len(records)==0):                                                                                       
            TradeContext.UNCONRST   ='1'                  
            TradeContext.STRINFO  = '错帐解控失败，原错帐控制记录不存在' 
            hzAfe()                                                                   
            return AfaFlowControl.ExitThisFlow('S999', "错帐解控失败，原错帐控制记录不存在")
        else:
            AfaLoggerFunc.tradeInfo("kkkkk"+records['ORTRCCO'] )
            if((records['ORTRCCO']=='3000103')or(records['ORTRCCO']=='3000105' )or(records['ORTRCCO']=='3000102')or(records['ORTRCCO']=='3000104')):
                AfaLoggerFunc.tradeInfo("yyyyyyyyyyyyyyyy")
                TradeContext.ACCNO     =   records['ORPYRACC']      #解控账号
            else: 
                AfaLoggerFunc.tradeInfo("XXXXXXXXXXXXXXXX")   
                TradeContext.ACCNO     =   records['ORPYEACC']      #解控账号
            AfaLoggerFunc.tradeInfo("fffffffff"+TradeContext.ACCNO )  
            TradeContext.ERRCONBAL    =   records['ERRCONBAL']     #解控金额 
            
        AfaLoggerFunc.tradeInfo(">>>开始组织查询字典，看是否是重复解控")  
        wheresql_dic={}                                                                                              
        wheresql_dic['TRCCO']      ='3000509'                 #交易码                                                 
        wheresql_dic['ORTRCDAT']   =TradeContext.ORTRCDAT     #原交易日期
        wheresql_dic['ORSNDBNK']   =TradeContext.ORSNDBNK     #原发送行号
        wheresql_dic['ORTRCNO']    =TradeContext.ORTRCNO      #原交易流水号
        wheresql_dic['UNCONRST']   ='0'  
        
        #=====开始查询数据库====                                                                                     
        records=rccpsDBTrcc_acckj.selectu(wheresql_dic)          #查询错帐控制解控登记簿                             
        AfaLoggerFunc.tradeDebug('>>>记录['+str(records)+']')                                                        
        if(records==None):                                                                                           
            return AfaFlowControl.ExitThisFlow('A099','查询失败' )  
        if(len(records)>0):
            if (records['UNCONRST'] == '0'):           #解控状态
                TradeContext.UNCONSTS  ='0'                                   
                TradeContext.STRINFO  = '错帐解控失败，原错帐已经解控'
                hzAfe()                                                                            
                return AfaFlowControl.ExitThisFlow('S999', "错帐解控失败，原错帐已经解控")
        
        #TradeContext.ACCNO    = TradeContext.ORPYEACC              
        #调用0061主机错帐解控交易
        TradeContext.HostCode = '0061'
        TradeContext.kjflag='1'                                 #错帐控制标识位

    AfaLoggerFunc.tradeInfo("交易前处理(登记流水,主机前处理)  结束")
        
    return True    
 
def SubModuleDoSnd():
    AfaLoggerFunc.tradeInfo("交易中处理(修改流水,主机后处理,中心前处理)")
    
    AfaLoggerFunc.tradeInfo("errorCode<<<<<<<<<<<"+TradeContext.errorCode)
    AfaLoggerFunc.tradeInfo("errorMsg<<<<<<<<<<"+TradeContext.errorMsg)
    
    #=====判断主机交易是否成功====
    if( TradeContext.errorCode != '0000' ):
        AfaLoggerFunc.tradeInfo("主机交易失败")
        
        TradeContext.PRCCO    = "NN1CA999"  #返回码
        TradeContext.STRINFO  = "主机失败 "+TradeContext.errorMsg[7:]+" "  #附言 
        
        #=====更新错帐控制解控登记簿====
        AfaLoggerFunc.tradeInfo("组织更新字典")
        where_dict = {'TRCDAT':TradeContext.TRCDAT,'BSPSQN':TradeContext.BSPSQN}   #日期和平台流水号
        if (TradeContext.TRCCO=='3000508'):
            TradeContext.CONSTS='1'
            update_dict = {'CONSTS':TradeContext.CONSTS,'STRINFO':TradeContext.STRINFO,'PRCCO':TradeContext.PRCCO}  #错误信息描述和返回码  
        if (TradeContext.TRCCO=='3000509'):
            TradeContext.UNCONRST='1'   
            update_dict = {'UNCONRST':TradeContext.UNCONRST,'STRINFO':TradeContext.STRINFO,'PRCCO':TradeContext.PRCCO}  #错误信息描述和返回码  
        AfaLoggerFunc.tradeInfo("开始更新错帐控制解控登记簿")
        
        res = rccpsDBTrcc_acckj.updateCmt(update_dict,where_dict)
        
        if( res == -1 ):
            return AfaFlowControl.ExitThisFlow('A009','更新错帐控制解控登记簿失败')
    else:
        AfaLoggerFunc.tradeInfo("主机交易成功")
        #=====更新错帐控制解控登记簿====
        AfaLoggerFunc.tradeInfo("组织更新字典")
        TradeContext.PRCCO = "RCCI0000"              #返回码
        
        if(TradeContext.TRCCO=='3000508'):
            TradeContext.CONSTS='0'
            TradeContext.STRINFO = "错帐控制成功"  #附言
            update_dict = {'BALANCE':TradeContext.BALANCE,'CONSTS':TradeContext.CONSTS,'STRINFO':TradeContext.STRINFO,'PRCCO':TradeContext.PRCCO} 
        
        if(TradeContext.TRCCO=='3000509'):
            TradeContext.UNCONRST='0'
            TradeContext.STRINFO = "错帐解控成功"  #附言
            update_dict = {'UNCONRST':TradeContext.UNCONRST,'STRINFO':TradeContext.STRINFO,'PRCCO':TradeContext.PRCCO}
        
        where_dict = {'TRCDAT':TradeContext.TRCDAT,'BSPSQN':TradeContext.BSPSQN}    #日期和中台流水号
                          
        AfaLoggerFunc.tradeInfo("开始更新错帐控制解控登记簿")
        res = rccpsDBTrcc_acckj.updateCmt(update_dict,where_dict)
        
        if( res == -1 ):
            return AfaFlowControl.ExitThisFlow('A009','更新错帐控制解控登记簿失败')
            
    #=====开始错帐控制解控应答报文赋值====
    AfaLoggerFunc.tradeInfo("开始给卡错帐控制解控应答报文赋值")
    
    Rcvmbrco = TradeContext.SNDMBRCO    #发送行行号
    Sndmbrco = TradeContext.RCVMBRCO    #接受行行号
    Ormfn    = TradeContext.MSGFLGNO    #参考报文标识号
    #=====报文头====
    TradeContext.MSGTYPCO = 'SET010'  #报文类代码
    TradeContext.RCVSTLBIN = Rcvmbrco #接受方成员行号
    TradeContext.SNDSTLBIN = Sndmbrco #发送方成员行号
    TradeContext.SNDBRHCO = TradeContext.BESBNO         #发起行网点号
    TradeContext.SNDCLKNO = TradeContext.BETELR         #发起行柜员号
    TradeContext.SNDTRDAT = TradeContext.TRCDAT         #发起行交易日期
    TradeContext.SNDTRTIM = TradeContext.BJETIM         #发起行交易时间
    TradeContext.MSGFLGNO = Rcvmbrco+TradeContext.TRCDAT + TradeContext.SerialNo        #报文标示号
    TradeContext.ORMFN    = Ormfn                             #参考报文标示号
    TradeContext.NCCWKDAT = TradeContext.NCCworkDate          #中心工作日期
    TradeContext.OPRTYPNO = '30'     #业务类型
    TradeContext.ROPRTPNO = '30'     #参考业务类型
    TradeContext.TRANTYP  = '0'      #传输类型
    #=====业务要素集====

        
    AfaLoggerFunc.tradeInfo("交易中处理(修改流水,主机后处理,中心前处理)  结束")
    
    return True    
    
def SubModuleDoTrd():
    AfaLoggerFunc.tradeInfo("交易后处理")
    
    AfaLoggerFunc.tradeInfo("errorCode<<<<<<<<<<<"+TradeContext.errorCode)
    AfaLoggerFunc.tradeInfo("errorMsg<<<<<<<<<<"+TradeContext.errorMsg)
    
    #=====判断afe返回结果====
    if TradeContext.errorCode == '0000':
        AfaLoggerFunc.tradeInfo('>>>发送成功')
    else:
        AfaLoggerFunc.tradeInfo('>>>发送失败')

    AfaLoggerFunc.tradeInfo("交易后处理 结束")
    
    AfaLoggerFunc.tradeInfo("'***农信银系统：通存通兑错帐控制解控接收交易.错帐控制解控查询[1165] 退出")

    return True  


#当交易要素不符时向农信银中心直接返回错误信息，交易终止
def hzAfe():
    #=====开始错帐控制解控应答报文赋值====
    AfaLoggerFunc.tradeInfo("开始给卡错帐控制解控应答报文赋值")
    
    Rcvmbrco = TradeContext.SNDMBRCO    #发送行行号
    Sndmbrco = TradeContext.RCVMBRCO    #接受行行号
    Ormfn    = TradeContext.MSGFLGNO    #参考报文提示号
    #=====报文头====
    TradeContext.MSGTYPCO = 'SET010'  #报文类代码
    TradeContext.RCVSTLBIN = Rcvmbrco #接受方成员行号
    TradeContext.SNDSTLBIN = Sndmbrco #发送方成员行号
    TradeContext.SNDBRHCO = TradeContext.BESBNO         #发起行网点号
    TradeContext.SNDCLKNO = TradeContext.BETELR         #发起行柜员号
    TradeContext.SNDTRDAT = TradeContext.TRCDAT         #发起行交易日期
    TradeContext.SNDTRTIM = TradeContext.BJETIM         #发起行交易时间
    TradeContext.MSGFLGNO = Rcvmbrco+TradeContext.TRCDAT + TradeContext.SerialNo        #报文标示号
    TradeContext.ORMFN    = Ormfn                             #参考报文标示号
    TradeContext.NCCWKDAT = TradeContext.NCCworkDate          #中心工作日期
    TradeContext.OPRTYPNO = '30'     #业务类型
    TradeContext.ROPRTPNO = '30'     #参考业务类型
    TradeContext.TRANTYP  = '0'      #传输类型        
    TradeContext.PRCCO    = "NN1CA999"  #返回码                                                                   
    
    #=====更新错帐控制解控登记簿====
    AfaLoggerFunc.tradeInfo("组织更新字典")
    where_dict = {'TRCDAT':TradeContext.TRCDAT,'BSPSQN':TradeContext.BSPSQN}   #日期和平台流水号
    if (TradeContext.TRCCO=='3000508'):
        TradeContext.CONSTS='1'
        update_dict = {'CONSTS':TradeContext.CONSTS,'STRINFO':TradeContext.STRINFO,'PRCCO':TradeContext.PRCCO}  #错误信息描述和返回码  
    if (TradeContext.TRCCO=='3000509'):
        TradeContext.UNCONRST='1'   
        update_dict = {'UNCONRST':TradeContext.UNCONRST,'STRINFO':TradeContext.STRINFO,'PRCCO':TradeContext.PRCCO}  #错误信息描述和返回码  
    AfaLoggerFunc.tradeInfo("开始更新错帐控制解控登记簿")
    
    res = rccpsDBTrcc_acckj.updateCmt(update_dict,where_dict)
    
    if( res == -1 ):
        return AfaFlowControl.ExitThisFlow('A009','更新错帐控制解控登记簿失败')
    #=====直接向AFE发送通讯回执====
    AfaLoggerFunc.tradeInfo("直接向AFE发送通讯回执")
    AfaAfeFunc.CommAfe()
