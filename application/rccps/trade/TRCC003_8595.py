# -*- coding: gbk -*-
##################################################################
#   农信银.通存通兑往账交易.错帐控制和解控请求  柜面交易
#=================================================================
#   程序文件:   TRCC003_8595.py
#   修改时间:   2011-05-11
#   作者：      曾照泰
##################################################################
import TradeContext,AfaFlowControl,AfaLoggerFunc,AfaAdminFunc,rccpsDBTrcc_acckj
import rccpsDBTrcc_balbka,rccpsDBTrcc_paybnk,rccpsDBTrcc_subbra
import rccpsMap8595CTradeContext2Dacckj
from types import *
from rccpsConst import *

def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo("'***农信银系统：通存通兑往账交易.错帐控制/解控[8595] 进入")
    
    AfaLoggerFunc.tradeInfo("交易前处理(本地操作,中心前处理)")
    
    #=====校验错帐控制交易变量是否存在====                                              
    if not TradeContext.existVariable("OPTYPE"):          #操作类型  错帐控制/错帐解控  
        return AfaFlowControl.ExitThisFlow('A099','操作类型类型不能为空')               
    
    #=====判断帐户类型====
    if( TradeContext.OPTYPE == '0' ): #错帐控制
        AfaLoggerFunc.tradeInfo("进入错帐控制操作处理")
        TradeContext.TRCCO = '3000508'            #交易码
        
        if not TradeContext.existVariable("TRCDAT"):          #委托日期
            return AfaFlowControl.ExitThisFlow('A099','委托日期不能为空')  
        
        if not TradeContext.existVariable("SNDBNKCO"):          #发起行号
            return AfaFlowControl.ExitThisFlow('A099','发起行号不能为空')    
        
        if not TradeContext.existVariable("SNDBNKNM"):          #发起行名
            return AfaFlowControl.ExitThisFlow('A099','发起行名不能为空')    
        
        if not TradeContext.existVariable("RCVBNKCO"):          #接受行号
            return AfaFlowControl.ExitThisFlow('A099','接受行号不能为空')    
        
        if not TradeContext.existVariable("RCVBNKNM"):          #接受行名
            return AfaFlowControl.ExitThisFlow('A099','接受行名不能为空')   
        
        if not TradeContext.existVariable("ORTRCDAT"):          #原委托日期
            return AfaFlowControl.ExitThisFlow('A099','原委托日期不能为空')  
            
        if not TradeContext.existVariable("ORTRCCO"):          #原交易代码
            return AfaFlowControl.ExitThisFlow('A099','原交易代码不能为空')  
                 
        if not TradeContext.existVariable("ORTRCNO"):           #原交易流水号
            return AfaFlowControl.ExitThisFlow('A099','原交易流水号不能为空') 
            
        if not TradeContext.existVariable("ORSNDSUBBNK"):         #原发起成员行号
            return AfaFlowControl.ExitThisFlow('A099','原发起成员行号不能为空')  
            
        if not TradeContext.existVariable("ORSNDBNK"):         #原发送行号
            return AfaFlowControl.ExitThisFlow('A099','原发起成员行号不能为空')  
            
        if not TradeContext.existVariable("ORRCVSUBBNK"):          #原接受成员行号
            return AfaFlowControl.ExitThisFlow('A099','原接受成员行号不能为空')  
        
        if not TradeContext.existVariable("ORRCVBNK"):          #原接受行号
            return AfaFlowControl.ExitThisFlow('A099','原接受行号不能为空')  
        
        if not TradeContext.existVariable("CUR"):              #货币符号
            return AfaFlowControl.ExitThisFlow('A099','原货币符号不能为空')  
        
        if not TradeContext.existVariable("OCCAMT"):        #原交易金额
            return AfaFlowControl.ExitThisFlow('A099','原交易金额不能为空') 
             
        if not TradeContext.existVariable("CHRG"):          #原手续费
            return AfaFlowControl.ExitThisFlow('A099','原手续费不能为空') 
                     
        if not TradeContext.existVariable("ERRCONBAL"):          #控制或解控金额
            return AfaFlowControl.ExitThisFlow('A099','控制或解控金额不能为空') 
        
        OCCAMT    = float(TradeContext.OCCAMT)    #交易金额
        ERRCONBAL = float(TradeContext.ERRCONBAL) #错帐控制金额
        CHRG      = float(TradeContext.CHRG)      #手续费 
        
        #if  ERRCONBAL>(OCCAMT+CHRG):
        #     return AfaFlowControl.ExitThisFlow('A099','错帐控制金额不能超过原交易金额')
        
        #错帐控制时需要校验发起行号和接受行号必须与原发起行号和原接受行号一致
        AfaLoggerFunc.tradeInfo(TradeContext.SNDBNKCO )
        AfaLoggerFunc.tradeInfo(TradeContext.ORSNDBNK )
        
        if (TradeContext.SNDBNKCO != TradeContext.ORSNDBNK):
            return AfaFlowControl.ExitThisFlow('A099','发起行号和原发起行号不符')
        
        AfaLoggerFunc.tradeInfo(TradeContext.RCVBNKCO )
        AfaLoggerFunc.tradeInfo(TradeContext.ORRCVBNK )
        
        if (TradeContext.RCVBNKCO != TradeContext.ORRCVBNK):
            return AfaFlowControl.ExitThisFlow('A099','接受行号和原接受行号不符')    
        
        #判断委托日期和原交易日期的差值是否大于15个工作日
        sTrxDate   = AfaAdminFunc.getTimeFromNow(-15)   #取出当前日期的前15天的日期
        #if (TradeContext.ORTRCDAT < sTrxDate ):
        #    return AfaFlowControl.ExitThisFlow('A099','错帐控制日期最迟不得超过原交易日后15日')   
        #end
       
        #=====组织查询字典====                            
        AfaLoggerFunc.tradeInfo(">>>开始组织查询字典")    
        
        wheresql_dic={}
        wheresql_dic['ORTRCDAT'] =TradeContext.ORTRCDAT   #原交易日期
        wheresql_dic['SNDBNKCO'] =TradeContext.ORSNDBNK   #原发送行号
        wheresql_dic['ORTRCNO']  =TradeContext.ORTRCNO    #原交易流水号
        wheresql_dic['TRCCO']    ="3000508"               #错帐控制交易码
        wheresql_dic['CONSTS']    ="0"                    #控制成功
        
        #=====开始查询数据库====
        records=rccpsDBTrcc_acckj.selectu(wheresql_dic)          #查询错帐控制解控登记簿 
        AfaLoggerFunc.tradeDebug('>>>记录['+str(records)+']')
        if(records==None):                                        
            return AfaFlowControl.ExitThisFlow('A099','查询失败' )
        elif(len(records)>0):
            return AfaFlowControl.ExitThisFlow('A099','该笔错帐已经控制成功，不能重复控制')
            
    elif( TradeContext.OPTYPE == '1' ): #错帐解控
        AfaLoggerFunc.tradeInfo("进入错帐解控操作处理")
        TradeContext.TRCCO = '3000509'            #交易码  
        #=====校验错帐控制交易变量是否存在====  
        if not TradeContext.existVariable("TRCDAT"):          #委托日期      
            return AfaFlowControl.ExitThisFlow('A099','委托日期不能为空')    
        
        if not TradeContext.existVariable("SNDBNKCO"):          #发起行号     
            return AfaFlowControl.ExitThisFlow('A099','发起行号不能为空')     
                                                                               
        if not TradeContext.existVariable("SNDBNKNM"):          #发起行名     
            return AfaFlowControl.ExitThisFlow('A099','发起行名不能为空')     
        
        if not TradeContext.existVariable("RCVBNKCO"):          #接受行号   
            return AfaFlowControl.ExitThisFlow('A099','接受行号不能为空')   
                                                                            
        if not TradeContext.existVariable("RCVBNKNM"):          #接受行名   
            return AfaFlowControl.ExitThisFlow('A099','接受行名不能为空')   
    
        if not TradeContext.existVariable("ORTRCDAT"):          #原委托日期        
            return AfaFlowControl.ExitThisFlow('A099','原委托日期不能为空')        
                                                                                   
        if not TradeContext.existVariable("ORTRCNO"):           #原交易流水号     
            return AfaFlowControl.ExitThisFlow('A099','原交易流水号不能为空')     
                                                          
        #=====组织查询字典====                            
        AfaLoggerFunc.tradeInfo(">>>开始组织查询字典")    
        
        wheresql_dic={}
        wheresql_dic['TRCDAT'] =TradeContext.ORTRCDAT   #原交易日期
        wheresql_dic['SNDBNKCO'] =TradeContext.ORSNDBNK   #原发送行号
        wheresql_dic['TRCNO']  =TradeContext.ORTRCNO     #原交易流水号
        wheresql_dic['TRCCO']    ="3000508"               #错帐控制交易码
        wheresql_dic['CONSTS']    ="0"                    #控制成功
        
        #=====开始查询数据库====
        records=rccpsDBTrcc_acckj.selectu(wheresql_dic)          #查询错帐控制解控登记簿 
        AfaLoggerFunc.tradeDebug('>>>记录['+str(records)+']')
        if(records==None):                                        
            return AfaFlowControl.ExitThisFlow('A099','查询失败' )
        
        elif(len(records)==0):
            return AfaFlowControl.ExitThisFlow('A099','没有查找到原错帐控制交易数据，请检查输入数据是否有误,或者原交易控制失败，不能解控。')
        
        else:
            TradeContext.ORMFNBAK = records['MSGFLGNO']                 #错帐控制的报文标识号 在解控时需要放在参考报文标识号中
            if  ((records['ORTRCCO']=='3000103')or(records['ORTRCCO']=='3000105')or (records['ORTRCCO']=='3000102')or(records['ORTRCCO']=='3000104')):
                TradeContext.ACCNO    = records['ORPYRACC']
                TradeContext.ACCNONAME= records['ORPYRNAM'] 
            else:
                TradeContext.ACCNO    = records['ORPYEACC']             #错帐解控账号 
                TradeContext.ACCNONAME= records['ORPYENAM']             #错帐解控账户名 
            
            TradeContext.AMOUNT       = str(records['ERRCONBAL'])             #错帐解控金额
            
    else:
        return AfaFlowControl.ExitThisFlow("S999", "非法的操作类型")
       
    #=====组织错帐控制/解控请求报文====
    AfaLoggerFunc.tradeInfo("开始组错帐控制/解控请求报文")
    
    #=====报文头====
    TradeContext.MSGTYPCO = 'SET009'                    #实时信息报文   无业务要素  SET000网络ECHO报文
    #是否需要把接受成员行号和发送成员行号赋值
    TradeContext.SNDMBRCO = TradeContext.SNDSTLBIN      #发送成员行号
    TradeContext.RCVMBRCO = TradeContext.RCVSTLBIN      #接收成员行号
    #TradeContext.SNDSTLBIN= PL_BESBNO_BCLRSB           #发送方成员行号
    #TradeContext.RCVSTLBIN= PL_RCV_CENTER          #接受方成员行号
    TradeContext.SNDBRHCO = TradeContext.BESBNO    #发送机构号
    TradeContext.SNDCLKNO = TradeContext.BETELR    #发送柜员号 
    TradeContext.SNDTRDAT = TradeContext.TRCDAT    #发送请求的日期
    TradeContext.SNDTRTIM = TradeContext.BJETIM    #发送请求的时间
    TradeContext.MSGFLGNO = TradeContext.SNDSTLBIN + TradeContext.TRCDAT + TradeContext.SerialNo  #发送行号，发送日期，交易流水号 共同组成报文标识号
    TradeContext.ORMFN     = TradeContext.ORSNDBNK + TradeContext.ORTRCDAT + TradeContext.ORTRCNO  #参考报文标识号 原发送行号，原发送日期，原交易流水号          
    #当为错帐解控时 报文参考标识号为错帐控制的报文标识号
    if(TradeContext.TRCCO == '3000509' ):
        TradeContext.ORMFN = TradeContext.ORMFNBAK
    TradeContext.NCCWKDAT = TradeContext.NCCworkDate  #农信银中心日期
    TradeContext.OPRTYPNO = "30"                   #业务类型
    TradeContext.ROPRTPNO = "30"                   #参考业务类型
    TradeContext.TRANTYP  = "0"                    #传输类型
    #=====业务要素集==== 
    TradeContext.TRCNO    =  TradeContext.SerialNo #交易流水号    
    TradeContext.CUR      = "CNY"                  #货币符号
    TradeContext.PRCCO    = ""                     #返回码   
    
    #=====登记错帐控制解控登记簿====
    AfaLoggerFunc.tradeInfo('给登记字典赋值')
    insert_dict = {}
    rccpsMap8595CTradeContext2Dacckj.map(insert_dict)
    insert_dict['CUR']      = '01'                #币种 
    insert_dict['MSGFLGNO'] = TradeContext.MSGFLGNO #报文标识号
    insert_dict['BRSFLG']   = PL_BRSFLG_SND #往账标识
    insert_dict['NOTE1']     = TradeContext.BJETIM
    
    AfaLoggerFunc.tradeInfo('开始登记错帐控制和解控登记簿')
    res = rccpsDBTrcc_acckj.insertCmt(insert_dict)
    if( res == -1 ):
        return AfaFlowControl.ExitThisFlow('A009','登记错帐控制解控登记簿失败')
        
    AfaLoggerFunc.tradeInfo("交易前处理(本地操作,中心前处理) 结束")
    
    return True    
        
def SubModuleDoSnd():
    AfaLoggerFunc.tradeInfo('交易后处理')
    
    AfaLoggerFunc.tradeInfo('errorCode:' + TradeContext.errorCode)
    AfaLoggerFunc.tradeInfo('errorMsg:' + TradeContext.errorMsg)
    
    #=====判断AFE是否发送成功====
    if TradeContext.errorCode != '0000':
        #=====更改中心返回码，和附言====
        AfaLoggerFunc.tradeInfo("开始更新错帐控制解控登记簿")
        update_dict = {'PRCCO':'RCCS1105','STRINFO':'AFE发送失败'}                 #返回码，返回码对应的信息描述
        where_dict = {'TRCDAT':TradeContext.TRCDAT,'BSPSQN':TradeContext.BSPSQN}   #系统日期，平台流水号(报文编号)
        res = rccpsDBTrcc_acckj.updateCmt(update_dict,where_dict)
        if( res == -1 ):
            return AfaFlowControl.ExitThisFlow('A009','更新错帐控制解控登记簿失败')
           
        return AfaFlowControl.ExitThisFlow(TradeContext.errorCode,'向中心发送错帐控制解控请求报文失败')
    
    else:
        AfaLoggerFunc.tradeInfo('发送成功')
        
        update_dict = {'PRCCO':'RCCS1000','STRINFO':'AFE发送成功'}   #返回码，返回码对应的信息描述               
        where_dict = {'TRCDAT':TradeContext.TRCDAT,'BSPSQN':TradeContext.BSPSQN} #系统日期，平台流水号(报文编号) 
        res = rccpsDBTrcc_acckj.updateCmt(update_dict,where_dict)                                                
        if( res == -1 ):                                                                                         
            return AfaFlowControl.ExitThisFlow('A009','更新错帐控制解控登记簿失败')                              
                                                                                                                 
        AfaLoggerFunc.tradeInfo('交易后处理 结束')
    
        AfaLoggerFunc.tradeInfo("'***农信银系统：通存通兑往账交易.错帐控制解控[8595] 退出")
    
        return True
    