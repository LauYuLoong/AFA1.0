# -*- coding: gbk -*-
##################################################################
#   农信银.查询打印业务.汇兑业务查询复查自由格式登记薄查询
#=================================================================
#   程序文件:   TRCC001_8531.py
#   修改时间:   2008-06-06
#   作者：      潘广通
##################################################################
import os
import rccpsDBTrcc_hdcbka,rccpsDBTrcc_trcbka,rccpsDBTrcc_subbra,TradeContext,AfaLoggerFunc,AfaFlowControl,AfaUtilTools
from types import *

def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.本地类操作交易[TRC001_8531]进入***' )
    
    #=====判断输入接口值是否存在====
    if( not TradeContext.existVariable( "STRDAT" ) ):
        return AfaFlowControl.ExitThisFlow('A099','起始日期[STRDAT]不存在' )
    
    if( not TradeContext.existVariable( "ENDDAT" ) ):
        return AfaFlowControl.ExitThisFlow('A099','终止日期[ENDDAT]不存在' ) 
    
    if( not TradeContext.existVariable( "RECSTRNO" ) ):
        return AfaFlowControl.ExitThisFlow('A099','起始笔数[RECSTRNO]不存在' )

    #=====生成查询语句====
    wheresql=""
    wheresql = wheresql + "BESBNO='"        + TradeContext.BESBNO + "' " 
    wheresql=wheresql   + " AND BJEDTE>='"  + TradeContext.STRDAT + "'"
    wheresql=wheresql   + " AND BJEDTE<='"  + TradeContext.ENDDAT + "'"
    
    #=====判断交易代码是否为空====
    if(TradeContext.TRCCO != ""):
        wheresql = wheresql + " AND TRCCO='"  + TradeContext.TRCCO   + "'"
        
    #=====判断往来标识是否为空====
    if(TradeContext.BRSFLG != ""):
        wheresql = wheresql + " AND BRSFLG='" + TradeContext.BRSFLG  + "'"

    #=====判断查复标识是否为空或者9-全部====        
    if(TradeContext.ISDEAL != "9" and TradeContext.ISDEAL!=""):
        wheresql = wheresql + " AND ISDEAL='" + TradeContext.ISDEAL  + "'"
        
    AfaLoggerFunc.tradeDebug(">>>生成查询语句sql="+wheresql)

    #=====查询机构名====
    subbra_dict={'BESBNO':TradeContext.BESBNO}
    
    sub=rccpsDBTrcc_subbra.selectu(subbra_dict)
    if(sub==None):
        return AfaFlowControl.ExitThisFlow('A099','查询机构名失败' )        
    if(len(sub)==0):
        return AfaFlowControl.ExitThisFlow('A099','没有相应的机构名' )
    
    #=====判断打印类型====
    #=====0 不打印====
    if TradeContext.PRTTYPE=='0':
        AfaLoggerFunc.tradeInfo(">>>进入不打印处理")
        #=====判断报单序号是否为空====
        if(TradeContext.BSPSQN!=""):    
            wheresql = wheresql + " AND BSPSQN='" + TradeContext.BSPSQN  + "'"
        
        #=====得到总记录数====
        allcount=rccpsDBTrcc_hdcbka.count(wheresql)

        if(allcount==-1):
            return AfaFlowControl.ExitThisFlow('A099','超找总记录数失败' )
        
        #=====查询数据库====
        ordersql=" order by BJEDTE DESC,BSPSQN DESC"
        records=rccpsDBTrcc_hdcbka.selectm(TradeContext.RECSTRNO,10,wheresql,ordersql)
        
        if(records==None):
            return AfaFlowControl.ExitThisFlow('A099','查询失败' )        
        elif( len(records)<=0 ):
            return AfaFlowControl.ExitThisFlow('A099','未查找到数据' )        
        else:
            #=====生成文件====
            filename="rccps_"+TradeContext.BETELR+"_"+AfaUtilTools.GetHostDate()+"_"+TradeContext.TransCode
            fpath=os.environ["AFAP_HOME"]+"/tmp/"
            f=open(fpath+filename,"w")
            
            if(f==None):
                return AfaFlowControl.ExitThisFlow('A099','打开文件失败' )

            filecontext=""           
            #=====写文件操作====
            for i in range(0,len(records)):
                filecontext=records[i]['BJEDTE']  + "|" \
                           +records[i]['BSPSQN']  + "|" \
                           +records[i]['BRSFLG']  + "|" \
                           +records[i]['BESBNO']  + "|" \
                           +records[i]['BETELR']  + "|" \
                           +records[i]['BEAUUS']  + "|" \
                           +records[i]['NCCWKDAT']+ "|" \
                           +records[i]['TRCCO']   + "|" \
                           +records[i]['TRCDAT']  + "|" \
                           +records[i]['TRCNO']   + "|" \
                           +records[i]['SNDBNKCO']+ "|" \
                           +records[i]['SNDBNKNM']+ "|" \
                           +records[i]['RCVBNKCO']+ "|" \
                           +records[i]['RCVBNKNM']+ "|" \
                           +records[i]['BOJEDT']  + "|" \
                           +records[i]['BOSPSQ']  + "|" \
                           +records[i]['ORTRCCO'] + "|" \
                           +records[i]['CONT']    + "|" \
                           +records[i]['ISDEAL']  + "|" \
                           +records[i]['CUR']     + "|" \
                           +str(records[i]['OCCAMT'])+ "|" \
                           +records[i]['PYRACC']  + "|" \
                           +records[i]['PYEACC']  + "|" \
                           +records[i]['PRCCO']   + "|" \
                           +records[i]['STRINFO'] + "|" \
                           +records[i]['PYRNAM']  + "|" \
                           +records[i]['PYENAM']  + "|" 
                f.write(filecontext+"\n")
            AfaLoggerFunc.tradeInfo("生成文件结束")
            f.close()
            
            #=====输出接口赋值====
            TradeContext.RECCOUNT=str(len(records))     #查询笔数
            TradeContext.RECALLCOUNT=str(allcount)      #总笔数
            TradeContext.PBDAFILE=filename              #文件名
            TradeContext.errorCode="0000"
            TradeContext.errorMsg="查询成功"
    #=====1 打印====
    elif TradeContext.PRTTYPE=='1':
        #=====判断报单序号是否为空====
        if(TradeContext.BSPSQN!=""):    
            wheresql = wheresql + " AND BSPSQN='" + TradeContext.BSPSQN  + "'"
        else:
            return AfaFlowControl.ExitThisFlow('S999','报单序号[BSPSQN]不允许为空' )
            
        #=====查询数据库====
        records=rccpsDBTrcc_hdcbka.selectm(TradeContext.RECSTRNO,10,wheresql,"")
        
        if(records==None):
            return AfaFlowControl.ExitThisFlow('A099','查询失败' )        
        elif( len(records)<=0 ):
            return AfaFlowControl.ExitThisFlow('A099','未查找到数据' )        
        else:
            #=====查询书====
            if(TradeContext.TRCCO=='9900511'):                
                AfaLoggerFunc.tradeInfo(">>>业务类型为查询书")
                
                #=====查询原交易信息====
                where_dict={'BJEDTE':records[0]['BOJEDT'],'BSPSQN':records[0]['BOSPSQ']}
                
                ret=rccpsDBTrcc_trcbka.selectu(where_dict)
                if(ret==None):
                    return AfaFlowControl.ExitThisFlow('A099','查询原信息失败' )                    
                if(len(ret)==0):
                    return AfaFlowControl.ExitThisFlow('A099','未查找原信息' )
                    
                AfaLoggerFunc.tradeDebug(">>>开始生成查询书打印文本")
                
                #=====查询书打印格式====
                txt="""\
                
                                           %(BESBNM)s电子汇兑查询书
                               
                |-----------------------------------------------------------------------------|
                | 查询日期:     |      %(BJEDTE)s                                               |
                |-----------------------------------------------------------------------------|
                | 查询书号:     |      %(BSPSQN)s                                           |
                |-----------------------------------------------------------------------------|
                | 发起行行号:   |      %(SNDBNKCO)s                                             |
                |-----------------------------------------------------------------------------|
                | 接收行行号:   |      %(RCVBNKCO)s                                             |
                |-----------------------------------------------------------------------------|
                | 原交易金额:   |      %(OROCCAMT)-15.2f                                        |
                |-----------------------------------------------------------------------------|
                | 原发起行行号: |      %(ORSNDBNKCO)s                                             |
                |-----------------------------------------------------------------------------|
                | 原接收行行号: |      %(ORRCVBNKCO)s                                             |
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
                
                #=====写文件操作====
                file_name = 'rccps_' + records[0]['BJEDTE'] + '_' + TradeContext.BSPSQN + '_8531'    
                out_file = open(os.environ['AFAP_HOME'] + '/tmp/' + file_name,"wb")
                
                if out_file == None:
                    return AfaFlowControl.ExitThisFlow("S999", "生成文件异常")
                
                print >> out_file,txt % {'BESBNM':(sub['BESBNM']).ljust(10,' '),\
                                         'BJEDTE':(records[0]['BJEDTE']).ljust(8,' '),\
                                         'BSPSQN':(TradeContext.BSPSQN).ljust(12,' '),\
                                         'SNDBNKCO':(records[0]['SNDBNKCO']).ljust(10,' '),\
                                         'RCVBNKCO':(records[0]['RCVBNKCO']).ljust(10,' '),\
                                         'OROCCAMT':(records[0]['OCCAMT']),\
                                         'ORSNDBNKCO':(ret['SNDBNKCO']).ljust(10,' '),\
                                         'ORRCVBNKCO':(ret['RCVBNKCO']).ljust(10,' '),\
                                         'CONT1':(records[0]['CONT'][:68]).ljust(68,' '),\
                                         'CONT2':(records[0]['CONT'][68:138]).ljust(70,' '),\
                                         'CONT3':(records[0]['CONT'][138:208]).ljust(70,' '),\
                                         'CONT4':(records[0]['CONT'][208:]).ljust(70,' ')}
                
                out_file.close()
                
                TradeContext.PBDAFILE = file_name       #文件名
                
                AfaLoggerFunc.tradeDebug(">>>结束生成打印文本")            
            #=====查复书====
            elif(TradeContext.TRCCO=='9900512'):
                AfaLoggerFunc.tradeInfo(">>>业务类型为查复书")
                
                #=====查询原交易信息====
                where_dict={'BJEDTE':records[0]['BOJEDT'],'BSPSQN':records[0]['BOSPSQ']}
                    
                ret=rccpsDBTrcc_hdcbka.selectu(where_dict)
                if(ret==None):
                    return AfaFlowControl.ExitThisFlow('A099','查询原信息失败' )                    
                if(len(ret)==0):
                    return AfaFlowControl.ExitThisFlow('A099','未查找原信息' )

                #=====查复书打印格式====
                txt="""\
                
                                            %(BESBNM)s电子汇兑查复书
                                           
                    |-----------------------------------------------------------------------------|
                    | 查复日期:     |      %(BJEDTE)s                                               |
                    |-----------------------------------------------------------------------------|
                    | 查复书号:     |      %(BSPSQN)s                                           |
                    |-----------------------------------------------------------------------------|
                    | 接收行行号:   |      %(RCVBNKCO)s                                             |
                    |-----------------------------------------------------------------------------|
                    | 原查询日期:   |      %(BOJEDT)s                                               |
                    |-----------------------------------------------------------------------------|
                    | 原查询书号:   |      %(BOSPSQ)s                                           |
                    |-----------------------------------------------------------------------------|
                    | 原金额:       |      %(OROCCAMT)-15.2f                                        |
                    |-----------------------------------------------------------------------------|
                    | 原币种:       |      人民币                                                 |
                    |-----------------------------------------------------------------------------|
                    | 查复内容:     |                                                             |
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
                
                #====写文件操作====
                file_name = 'rccps_' + records[0]['BJEDTE'] + '_' + TradeContext.BSPSQN + '_8531'                
                out_file = open(os.environ['AFAP_HOME'] + '/tmp/' + file_name,"wb")
                
                if out_file == None:
                    return AfaFlowControl.ExitThisFlow("S999", "生成文件异常")
                
                print >> out_file,txt % {'BESBNM':(sub['BESBNM']).ljust(10,' '),\
                                         'BJEDTE':(records[0]['BJEDTE']).ljust(8,' '),\
                                         'BSPSQN':(TradeContext.BSPSQN).ljust(12,' '),\
                                         'RCVBNKCO':(records[0]['RCVBNKCO']).ljust(10,' '),\
                                         'BOJEDT':(records[0]['BOJEDT']).ljust(8,' '),\
                                         'BOSPSQ':(records[0]['BOSPSQ']).ljust(12,' '),\
                                         'OROCCAMT':(ret['OCCAMT']),\
                                         'CONT1':(records[0]['CONT'][:68]).ljust(68,' '),\
                                         'CONT2':(records[0]['CONT'][68:138]).ljust(70,' '),\
                                         'CONT3':(records[0]['CONT'][138:208]).ljust(70,' '),\
                                         'CONT4':(records[0]['CONT'][208:]).ljust(70,' ')}
                
                out_file.close()
                
                TradeContext.PBDAFILE = file_name   #文件名
                
                AfaLoggerFunc.tradeDebug("结束生成打印文本")
            #=====自由格式书====
            elif(TradeContext.TRCCO=='9900513'):            
                AfaLoggerFunc.tradeInfo(">>>业务类型为自由格式书")
                
                #=====自由格式书打印格式====
                txt="""\
                 
                                            %(BESBNM)s自由格式书
                                           
                    |-----------------------------------------------------------------------------|
                    | 日期:          |      %(BJEDTE)s                                              |
                    |-----------------------------------------------------------------------------|
                    | 自由格式书号:  |      %(BSPSQN)s                                          |
                    |-----------------------------------------------------------------------------|
                    | 发起行行号:    |      %(SNDBNKCO)s                                            |
                    |-----------------------------------------------------------------------------|
                    | 接收行行号:    |      %(RCVBNKCO)s                                            |
                    |-----------------------------------------------------------------------------|
                    | 内容:          |                                                            |
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
                
                #=====写文件操作====            
                file_name = 'rccps_' + records[0]['BJEDTE'] + '_' + TradeContext.BSPSQN + '_8531'    
                out_file = open(os.environ['AFAP_HOME'] + '/tmp/' + file_name,"wb")
                
                if out_file == None:
                    return AfaFlowControl.ExitThisFlow("S999", "生成文件异常")
                
                print >> out_file,txt % {'BESBNM':(sub['BESBNM']).ljust(10,' '),\
                                         'BJEDTE':(records[0]['BJEDTE']).ljust(8,' '),\
                                         'BSPSQN':(TradeContext.BSPSQN).ljust(12,' '),\
                                         'SNDBNKCO':(records[0]['SNDBNKCO']).ljust(10,' '),\
                                         'RCVBNKCO':(records[0]['RCVBNKCO']).ljust(10,' '),\
                                         'CONT1':(records[0]['CONT'][:68]).ljust(68,' '),\
                                         'CONT2':(records[0]['CONT'][68:138]).ljust(70,' '),\
                                         'CONT3':(records[0]['CONT'][138:208]).ljust(70,' '),\
                                         'CONT4':(records[0]['CONT'][208:]).ljust(70,' ')}
                
                out_file.close()
                
                TradeContext.PBDAFILE = file_name       #文件名
                
                AfaLoggerFunc.tradeDebug("结束生成打印文本")
            #=====特约汇兑查询书====
            elif(TradeContext.TRCCO=='9900522'):
                AfaLoggerFunc.tradeInfo(">>>业务类型为特约汇兑查询书")
                
                #=====查询原交易信息====
                where_dict={'BJEDTE':records[0]['BOJEDT'],'BSPSQN':records[0]['BOSPSQ']}
                    
                ret=rccpsDBTrcc_trcbka.selectu(where_dict)
                if(ret==None):
                    return AfaFlowControl.ExitThisFlow('A099','查询原信息失败' )                    
                if(len(ret)==0):
                    return AfaFlowControl.ExitThisFlow('A099','未查找原信息' )
  
                #=====特约电子汇兑查询书打印格式====
                txt="""\
                            
                                      %(BESBNM)s全国特约电子汇兑查询书
                                           
                    |-----------------------------------------------------------------------------|
                    | 查询日期:         |      %(BJEDTE)s                                           |
                    |-----------------------------------------------------------------------------|
                    | 特约汇兑查询书号: |      %(BSPSQN)s                                       |
                    |-----------------------------------------------------------------------------|
                    | 发起行行号:       |      %(SNDBNKCO)s                                         |
                    |-----------------------------------------------------------------------------|
                    | 接收行行号:       |      %(RCVBNKCO)s                                         |
                    |-----------------------------------------------------------------------------|  
                    | 原报单号:         |      %(BOSPSQ)s                                       |
                    |-----------------------------------------------------------------------------|  
                    | 原金额:           |      %(OROCCAMT)-15.2f                                    |
                    |-----------------------------------------------------------------------------|
                    | 原委托日期:       |      %(ORTRCDAT)s                                           |
                    |-----------------------------------------------------------------------------|
                    | 原发起行行号:     |      %(ORSNDBNKCO)s                                         |
                    |-----------------------------------------------------------------------------|
                    | 查询内容:         |                                                         |
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
                
                #====写文件操作====
                file_name = 'rccps_' + records[0]['BJEDTE'] + '_' + TradeContext.BSPSQN + '_8531'
                out_file = open(os.environ['AFAP_HOME'] + '/tmp/' + file_name,"wb")
                
                if out_file == None:
                    return AfaFlowControl.ExitThisFlow("S999", "生成打印文件异常")
                
                print >> out_file,txt % {'BESBNM':(sub['BESBNM']).ljust(10,' '),\
                                         'BJEDTE':(records[0]['BJEDTE']).ljust(8,' '),\
                                         'BSPSQN':(TradeContext.BSPSQN).ljust(12,' '),\
                                         'SNDBNKCO':(records[0]['SNDBNKCO']).ljust(10,' '),\
                                         'RCVBNKCO':(records[0]['RCVBNKCO']).ljust(10,' '),\
                                         'BOSPSQ':(records[0]['BOSPSQ']).ljust(10,' '),\
                                         'OROCCAMT':(ret['OCCAMT']),\
                                         'ORTRCDAT':(ret['TRCDAT']).ljust(8,' '),\
                                         'ORSNDBNKCO':(ret['SNDBNKCO']).ljust(10,' '),\
                                         'CONT1':(records[0]['CONT'][:68]).ljust(68,' '),\
                                         'CONT2':(records[0]['CONT'][68:138]).ljust(70,' '),\
                                         'CONT3':(records[0]['CONT'][138:208]).ljust(70,' '),\
                                         'CONT4':(records[0]['CONT'][208:]).ljust(70,' ')}
                
                out_file.close()
                
                TradeContext.PBDAFILE = file_name       #文件名
                
                AfaLoggerFunc.tradeDebug("结束生成打印文本")
            #=====特约汇兑查复书====
            elif(TradeContext.TRCCO=='9900523'):                
                AfaLoggerFunc.tradeInfo(">>>业务类型为特约汇兑查复书")
                
                #=====查询原交易信息====
                where_dict={'BJEDTE':records[0]['BOJEDT'],'BSPSQN':records[0]['BOSPSQ']}
                    
                ret=rccpsDBTrcc_hdcbka.selectu(where_dict)
                if(ret==None):
                    return AfaFlowControl.ExitThisFlow('A099','查询原信息失败' )                    
                if(len(ret)==0):
                    return AfaFlowControl.ExitThisFlow('A099','未查找原信息' )
                    
                #=====特约电子汇兑查复书打印格式====
                txt="""\
                
                                 
                                           %(BESBNM)s全国特约电子汇兑查复书
                                           
                    |-----------------------------------------------------------------------------|
                    | 查复日期:             |      %(BJEDTE)s                                       |
                    |-----------------------------------------------------------------------------|
                    | 特约汇兑查复书号:     |      %(BSPSQN)s                                   |
                    |-----------------------------------------------------------------------------|
                    | 发起行行号:           |      %(SNDBNKCO)s                                     |
                    |-----------------------------------------------------------------------------|
                    | 接收行行号:           |      %(RCVBNKCO)s                                     |
                    |-----------------------------------------------------------------------------|
                    | 原特约查询发起行行号: |      %(ORSNDBNKCO)s                                     |
                    |-----------------------------------------------------------------------------|
                    | 原特约查询日期:       |      %(BOJEDT)s                                       |
                    |-----------------------------------------------------------------------------|
                    | 原金额:               |      %(OROCCAMT)-15.2f                                |
                    |-----------------------------------------------------------------------------|
                    | 原委托日期:           |      %(ORTRCDAT)s                                       |
                    |-----------------------------------------------------------------------------|
                    | 原特约查询交易流水号: |      %(ORTRCNO)s                                   |
                    |-----------------------------------------------------------------------------|
                    | 查询内容:             |                                                     |
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
                
                #====写文件操作====
                file_name = 'rccps_' + records[0]['BJEDTE'] + '_' + TradeContext.BSPSQN + '_8531'               
                out_file = open(os.environ['AFAP_HOME'] + '/tmp/' + file_name,"wb")
                
                if out_file == None:
                    return AfaFlowControl.ExitThisFlow("S999", "生成打印文件异常")
                
                print >> out_file,txt % {'BESBNM':(sub['BESBNM']).ljust(10,' '),\
                                         'BJEDTE':(records[0]['BJEDTE']).ljust(8,' '),\
                                         'BSPSQN':(TradeContext.BSPSQN).ljust(12,' '),\
                                         'SNDBNKCO':(records[0]['SNDBNKCO']).ljust(10,' '),\
                                         'RCVBNKCO':(records[0]['RCVBNKCO']).ljust(10,' '),\
                                         'ORSNDBNKCO':(ret['SNDBNKCO']).ljust(10,' '),\
                                         'BOJEDT':(records[0]['BJEDTE']).ljust(8,' '),\
                                         'OROCCAMT':(ret['OCCAMT']),\
                                         'ORTRCDAT':(ret['TRCDAT']).ljust(8,' '),\
                                         'ORTRCNO':(ret['TRCNO']).ljust(12,' '),\
                                         'CONT1':(records[0]['CONT'][:68]).ljust(68,' '),\
                                         'CONT2':(records[0]['CONT'][68:138]).ljust(70,' '),\
                                         'CONT3':(records[0]['CONT'][138:208]).ljust(70,' '),\
                                         'CONT4':(records[0]['CONT'][208:]).ljust(70,' ')}
                
                out_file.close()
                
                TradeContext.PBDAFILE = file_name       #文件名
                
                AfaLoggerFunc.tradeDebug("结束生成打印文本")
            #=====特约汇兑自由格式书====
            elif(TradeContext.TRCCO=='9900524'):                
                AfaLoggerFunc.tradeInfo(">>>业务类型为特约汇兑自由格式书")
                
                #=====特约电子汇兑自由格式书打印格式====
                txt="""\
                
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
                
                #=====写文件操作====
                file_name = 'rccps_' + records[0]['BJEDTE'] + '_' + TradeContext.BSPSQN + '_8531'                
                out_file = open(os.environ['AFAP_HOME'] + '/tmp/' + file_name,"wb")
                
                if out_file == None:
                    return AfaFlowControl.ExitThisFlow("S999", "生成文件异常")
                
                print >> out_file,txt % {'BESBNM':(sub['BESBNM']).ljust(10,' '),\
                                         'BJEDTE':(records[0]['BJEDTE']).ljust(8,' '),\
                                         'BSPSQN':(TradeContext.BSPSQN).ljust(12,' '),\
                                         'SNDBNKCO':(records[0]['SNDBNKCO']).ljust(10,' '),\
                                         'RCVBNKCO':(records[0]['RCVBNKCO']).ljust(10,' '),\
                                         'CONT1':(records[0]['CONT'][:68]).ljust(68,' '),\
                                         'CONT2':(records[0]['CONT'][68:138]).ljust(70,' '),\
                                         'CONT3':(records[0]['CONT'][138:208]).ljust(70,' '),\
                                         'CONT4':(records[0]['CONT'][208:]).ljust(70,' ')}
                
                out_file.close()
                
                TradeContext.PBDAFILE = file_name       #文件名                
                AfaLoggerFunc.tradeInfo("结束生成打印文本")                    
            else:
                return AfaFlowControl.ExitThisFlow('A099','没有相关的业务类型' )    
        
        
        TradeContext.RECCOUNT="1"           #查询笔数
        TradeContext.RECALLCOUNT="1"        #总笔数
        TradeContext.errorCode="0000"
        TradeContext.errorMsg="查询成功"
              
    elif( len(TradeContext.PRTTYPE) == 0 ):
        return AfaFlowControl.ExitThisFlow('A099','打印标志为必输项' )  
    else:
        return AfaFlowControl.ExitThisFlow('A099','打印标志非法' )
    
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.本地类操作交易[TRC001_8531]退出***' )
    return True