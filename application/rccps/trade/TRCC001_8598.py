# -*- coding: gbk -*-
################################################################################
#   农信银系统：往账.本地类操作(1.本地操作).错帐控制交易信息联动查询  柜面交易
#===============================================================================
#   模板文件:   TRCC001_8598.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  曾照泰
#   修改时间:   2011-05-23
################################################################################
import TradeContext,AfaLoggerFunc,AfaFlowControl,AfaUtilTools,AfaDBFunc,TradeFunc,os,AfaFunc,rccpsDBTrcc_acckj,rccpsHostFunc,rccpsGetFunc
from types import *
from rccpsConst import *
import rccpsDBFunc,rccpsState
import rccpsDBTrcc_wtrbka,rccpsDBTrcc_tddzmx

def SubModuleDoFst():    
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.本地类操作交易(1.本地操作).错帐控制交易信息联动查询[TRCC001_8596]进入***' )
    
    #=====必要性检查====
    #=====判断输入接口是否存在====
    TradeContext.BJEDTE=AfaUtilTools.GetHostDate( )
    TradeContext.TRCDAT=TradeContext.BJEDTE
    #获取流水号
    seqName="RCC_SEQ"
    sqlStr = "SELECT NEXTVAL FOR " + seqName + " FROM SYSIBM.SYSDUMMY1"
    records = AfaDBFunc.SelectSql( sqlStr )
    if records == None :
        raise AfaFlowControl.ExitThisFlow('A0025', AfaDBFun.sqlErrMsg )
    TradeContext.TRCNO=str( records[0][0] ).rjust( 8, '0' )
    
    if( not TradeContext.existVariable( "ORTRCDAT" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '原委托日期[ORTRCDAT]不存在')
        
    if( not TradeContext.existVariable( "ORSNDBNK" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '原发送行号[ORSNDBNK]不存在')
        
    if( not TradeContext.existVariable( "ORTRCNO" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '原交易流水号[ORTRCNO]不存在')
    
   
    #=====组织查询字典====                                                                                                                                                       
    AfaLoggerFunc.tradeInfo(">>>开始组织查询字典")                                                                                                                               
                                                                                                                                                                                 
    wheresql_dic={}                                                                                                                                                              
    wheresql_dic['TRCDAT']   =TradeContext.ORTRCDAT                                                                                                                                
    wheresql_dic['SNDBNKCO'] =TradeContext.ORSNDBNK                                                                                                                               
    wheresql_dic['TRCNO']    =TradeContext.ORTRCNO                                                                                                                                   
    wheresql_dic['TRCCO']    ='3000508'                 #交易码                                                                                                                  
    wheresql_dic['CONSTS']   ='0'                                                                                                                                                
                                                                                                                                                                                 
    #=====开始查询数据库====                                                                                                                                                     
    records=rccpsDBTrcc_acckj.selectu(wheresql_dic)          #查询错帐控制解控登记簿                                                                                             
    AfaLoggerFunc.tradeDebug('>>>记录['+str(records)+']')                                                                                                                        
    if(records==None):                                                                                                                                                           
        return AfaFlowControl.ExitThisFlow('A099','查询失败' )                                                                                                                   
    elif(len(records)==0):                                                                                                                                                       
        TradeContext.UNCONRST   ='1'                                                                                                                                             
        TradeContext.STRINFO  = '错帐解控失败，原错帐控制记录不存在'                                                                                                             
        return AfaFlowControl.ExitThisFlow('S999', "错帐解控失败，原错帐控制记录不存在")                                                                                         
    else:                                                                                                                                                                        
        if((records['ORTRCCO']=='3000103')or(records['ORTRCCO']=='3000105' )or(records['ORTRCCO']=='3000102')or(records['ORTRCCO']=='3000104')):                                 
            TradeContext.ACCNO     =   records['ORPYRACC']      #解控账号 
            TradeContext.ACCNONAME =   records['ORPYRNAM']      #户名                                                                                             
        else:                                                                                                                                                                    
            TradeContext.ACCNO     =   records['ORPYEACC']      #解控账号
            TradeContext.ACCNONAME =   records['ORPYENAM']      #户名                                                                                                   
        TradeContext.ERRCONBAL     =   records['ERRCONBAL']     #解控金额
        TradeContext.ORMFN         =   records['MSGFLGNO']      #参考报文标识号
        TradeContext.BETELR        =   records['BETELR']        #柜员号                                                                                        
        TradeContext.BESBNO        =   records['BESBNO']        #机构号
        #TradeContext.NCCWKDAT      =   records['NCCWKDAT'] 
        TradeContext.SNDMBRCO      =   records['SNDMBRCO']      #发送方成员行号
        TradeContext.RCVMBRCO      =   records['RCVMBRCO']      #接受成员行行号
        TradeContext.SNDBNKCO      =   records['SNDBNKCO']      
        TradeContext.SNDBNKNM      =   records['SNDBNKNM'] 
        TradeContext.RCVBNKCO      =   records['RCVBNKCO']
        TradeContext.RCVBNKNM      =   records['RCVBNKNM']
        TradeContext.AMOUNT        =   str(records['ERRCONBAL'])
       
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
            return AfaFlowControl.ExitThisFlow('S999', "错帐解控失败，原错帐已经解控")             
                                                                                                   
    #=====组织登记错帐控制解控登记簿的插入字典====                                                 
    AfaLoggerFunc.tradeInfo("组织登记错帐控制解控登记簿的插入字典")                                
    insert_dict = {}                                                                               
                                                                                                   
    insert_dict['TRCDAT']      = TradeContext.BJEDTE          #委托日期                             
    insert_dict['BSPSQN']      = '0'                          #保单序号                             
    insert_dict['MSGFLGNO']    = '1'                          #报文标识号                           
    insert_dict['ORMFN']       = TradeContext.ORMFN           #参考报文标识号                       
    insert_dict['TRCCO']       = '3000509'                    #交易码                               
    insert_dict['BRSFLG']      = '0'                          #往来标识                             
    insert_dict['BESBNO']      = TradeContext.BESBNO          #机构号                               
    insert_dict['BEACSB']      = ""                           #账务机构号                           
    insert_dict['BETELR']      = TradeContext.BETELR          #机构柜员号                           
    insert_dict['BEAUUS']      = ""                          #授权柜员号                           
    insert_dict['BEAUPS']      = ""                          #授权柜员密码                         
    insert_dict['TERMID']      = ""                          #终端号                               
    insert_dict['OPTYPE']       =''                          #业务类型                             
    insert_dict['NCCWKDAT']    = TradeContext.BJEDTE         #农信银中心日期                       
    insert_dict['TRCNO']       = TradeContext.TRCNO          #交易流水号                           
    insert_dict['SNDMBRCO']    = TradeContext.SNDMBRCO       #发送方成员行号                       
    insert_dict['RCVMBRCO']    = TradeContext.RCVMBRCO       #接受成员行行号                       
    insert_dict['SNDBNKCO']    = TradeContext.SNDBNKCO       #发送方行号
    insert_dict['SNDBNKNM']    = TradeContext.SNDBNKNM       #发送方行名
    insert_dict['RCVBNKCO']    = TradeContext.RCVBNKCO       #接受行号
    insert_dict['RCVBNKNM']    = TradeContext.RCVBNKNM       #接受行名                          
    insert_dict['ORTRCDAT']    = TradeContext.ORTRCDAT       #原委托日期                           
    insert_dict['ORTRCCO']     = '3000508'                   #原交易代码                           
    insert_dict['ORTRCNO']     = TradeContext.ORTRCNO        #交易流水号                           
    insert_dict['ORSNDSUBBNK'] = ''                          #原发起成员行号                       
    insert_dict['ORSNDBNK']    = TradeContext.ORSNDBNK       #原发起行号                           
    insert_dict['ORRCVSUBBNK'] = ''                          #原接受成员行行号                     
    insert_dict['ORRCVBNK']    = ''                          #原接受行名                           
    insert_dict['ORPYRACC']    = ''                          #原付款人账号                         
    insert_dict['ORPYRNAM']    = ''                          #原付款人名称                         
    insert_dict['ORPYEACC']    = ''                          #原收款人账号                         
    insert_dict['ORPYENAM']    = ''                          #原收款人名称                         
    insert_dict['CUR']         = '01'                        #币种                                 
    insert_dict['OCCAMT']      = '0'                         #原交易金额                           
    insert_dict['CHRG']        = '0'                         #手续费                               
    insert_dict['ERRCONBAL']   = TradeContext.ERRCONBAL      #错帐控制金额                         
    insert_dict['BALANCE'] = ""                                                                
    insert_dict['UNCONRST']= ""                                                            
    insert_dict['CONSTS']  = ""                                                            
    insert_dict['PRCCO']  =""                                                              
    insert_dict['STRINFO']     = ''           #附言                          
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
        TradeContext.BETELR        =   records['BETELR']        #柜员号
     
     
     #=====================与主机通讯进行错帐解控======================================== 
    #TradeContext.BESBNO='3401010079'
    #TradeContext.BETELR ='007907'
    #TradeContext.TERMID='1234567890'  
    TradeContext.kjflag='1'                                 #错帐控制标识位
    TradeContext.HostCode = '0061'
    rccpsHostFunc.CommHost('0061')   
    
    AfaLoggerFunc.tradeInfo("交易中处理(修改流水,主机后处理)")
    
    AfaLoggerFunc.tradeInfo("errorCode<<<<<<<<<<<"+TradeContext.errorCode)
    AfaLoggerFunc.tradeInfo("errorMsg<<<<<<<<<<"+TradeContext.errorMsg)
    
    #=====判断主机交易是否成功====
    if( TradeContext.errorCode != '0000' ):
        AfaLoggerFunc.tradeInfo("主机交易失败")
        
        TradeContext.PRCCO    = "NN1CA999"  #返回码
        TradeContext.STRINFO  = "主机失败 "+TradeContext.errorMsg[7:]+" "  #附言 
        TradeContext.UNCONRST='1'
        
        #=====更新错帐控制解控登记簿====
        AfaLoggerFunc.tradeInfo("组织更新字典")
        where_dict = {'ORTRCDAT':TradeContext.ORTRCDAT,'ORSNDBNK':TradeContext.ORSNDBNK,'ORTRCNO':TradeContext.ORTRCNO,'TRCCO':'3000509','TRCNO':TradeContext.TRCNO}   #原委托日期，原发送行号，原交易流水号
        update_dict = {'UNCONRST':TradeContext.UNCONRST,'STRINFO':TradeContext.STRINFO,'PRCCO':TradeContext.PRCCO}  #错误信息描述和返回码  

        AfaLoggerFunc.tradeInfo("开始更新错帐控制解控登记簿")
        
        res = rccpsDBTrcc_acckj.updateCmt(update_dict,where_dict)
        
        if( res == -1 ):
            return AfaFlowControl.ExitThisFlow('A009','更新错帐控制解控登记簿失败')
        AfaLoggerFunc.tradeInfo(res)   
    else:
        AfaLoggerFunc.tradeInfo("主机交易成功")
        #=====更新错帐控制解控登记簿====
        AfaLoggerFunc.tradeInfo("组织更新字典")
        TradeContext.PRCCO = "RCCI0000"              #返回码
        TradeContext.UNCONRST='0'
        TradeContext.STRINFO = "错帐解控成功"  #附言
        
        where_dict = {'ORTRCDAT':TradeContext.ORTRCDAT,'ORSNDBNK':TradeContext.ORSNDBNK,'ORTRCNO':TradeContext.ORTRCNO,'TRCCO':'3000509','TRCNO':TradeContext.TRCNO}   #原委托日期，原发送行号，原交易流水号
        update_dict = {'UNCONRST':TradeContext.UNCONRST,'STRINFO':TradeContext.STRINFO,'PRCCO':TradeContext.PRCCO}  #错误信息描述和返回码  

        AfaLoggerFunc.tradeInfo("开始更新错帐控制解控登记簿")
        res = rccpsDBTrcc_acckj.updateCmt(update_dict,where_dict)
        
        if( res == -1 ):
            return AfaFlowControl.ExitThisFlow('A009','更新错帐控制解控登记簿失败')
    
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.本地类操作(1.本地操作)错帐控制解控交易信息联动查询[TRCC001_8598]退出***')
    return True                                                              