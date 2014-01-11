# -*- coding: gbk -*-
##################################################################
#   农信银.查询打印业务.票据查询查复登记簿查询
#=================================================================
#   程序文件:   TRCC001_8532.py
#   修改时间:   2008-06-08
#   作者：      潘广通
##################################################################
import os
import rccpsDBTrcc_pjcbka,rccpsDBTrcc_subbra,TradeContext,AfaLoggerFunc,AfaFlowControl,AfaUtilTools,rccpsDBFunc
from types import *

def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.本地类操作交易[TRC001_8532]进入***' )
    
    #=====判断输入接口值是否存在====
    if( not TradeContext.existVariable( "STRDAT" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '起始日期[STRDAT]不存在')
        
    if( not TradeContext.existVariable( "ENDDAT" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '结束日期[ENDDAT]不存在')
    
    if( not TradeContext.existVariable( "RECSTRNO" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '起始笔数[RECSTRNO]不存在')
    
    if(len(TradeContext.PRTTYPE)==0):
        return AfaFlowControl.ExitThisFlow("S999", "打印标志[PRTTYPE]不允许为空")  
    
    #=====组织sql语句====
    wheresql=""
    wheresql = wheresql + "BESBNO='" + TradeContext.BESBNO + "' "
    wheresql=wheresql+" and BJEDTE>='"+TradeContext.STRDAT+"'"
    wheresql=wheresql+" AND BJEDTE<='"+TradeContext.ENDDAT+"'"
    
    #=====判断查复标识是否为空或为9-全部====
    if(TradeContext.ISDEAL != "" and TradeContext.ISDEAL != "9"):
        wheresql=wheresql+" AND ISDEAL='"+TradeContext.ISDEAL+"'"
    
    #=====判断往来标识是否为空====
    if(TradeContext.BRSFLG!=""):
        wheresql=wheresql+" AND BRSFLG='"+TradeContext.BRSFLG+"'"
    
    #=====判断交易代码是否为空====
    if(TradeContext.TRCCO !="" ):
        wheresql=wheresql+" AND TRCCO='"+TradeContext.TRCCO+"'" #业务类型（交易代码）
    
    start_no=TradeContext.RECSTRNO      #起始笔数
    sel_size=10
    
    #=====查询机构名====
    subbra_dict={'BESBNO':TradeContext.BESBNO}
    
    sub=rccpsDBTrcc_subbra.selectu(subbra_dict)
    if(sub==None):
        return AfaFlowControl.ExitThisFlow('A099','查询机构名失败' )
    if(len(sub)==0):
        return AfaFlowControl.ExitThisFlow('A099','机构名称无满足条件记录' )
    
    #=====判断打印类型 0  不打印====
    if(TradeContext.PRTTYPE=='0'):
        AfaLoggerFunc.tradeInfo(">>>进入不打印处理")
        
        #=====判断查询查复书号是否为空====
        if(TradeContext.BSPSQN!="" ):
            wheresql=wheresql+" AND BSPSQN='"+TradeContext.BSPSQN+"'"  
            
        #=====查询总记录数====
        allcount=rccpsDBTrcc_pjcbka.count(wheresql)
        if(allcount==-1):
            return AfaFlowControl.ExitThisFlow('A099','查找总记录数失败' )
            
        #=====查询数据库====
        ordersql=" order by BJEDTE DESC,BSPSQN DESC"
        records=rccpsDBTrcc_pjcbka.selectm(start_no,sel_size,wheresql,ordersql)
        
        if records==None:
            return AfaFlowControl.ExitThisFlow('A099','查询失败' )
        if len(records)<=0:
            return AfaFlowControl.ExitThisFlow('A099','没有查找到数据' )        
        else:
            #=====生成文件====
            filename="rccps_"+TradeContext.BETELR+"_"+AfaUtilTools.GetHostDate()+"_"+TradeContext.TransCode   
            fpath=os.environ["AFAP_HOME"]+"/tmp/"
                
            try:
                f=open(fpath+filename,"w") 
            except :
                AfaLoggerFunc.tradeInfo(">>>打开文件失败")
                return AfaFlowControl.ExitThisFlow('A099','打开文件失败' )
            filecontext=""
            
            #=====写文件操作====
            for i in range(0,len(records)):
                #=====生成文件内容====
                AfaLoggerFunc.tradeDebug( "生成文件内容 ")
                filecontext=records[i]['BJEDTE']     + "|" \
                           +records[i]['BSPSQN']     + "|" \
                           +records[i]['BRSFLG']     + "|" \
                           +records[i]['BESBNO']     + "|" \
                           +records[i]['BETELR']     + "|" \
                           +records[i]['BEAUUS']     + "|" \
                           +records[i]['NCCWKDAT']   + "|" \
                           +records[i]['TRCCO']      + "|" \
                           +records[i]['TRCDAT']     + "|" \
                           +records[i]['TRCNO']      + "|" \
                           +records[i]['SNDBNKCO']   + "|" \
                           +records[i]['SNDBNKNM']   + "|" \
                           +records[i]['RCVBNKCO']   + "|" \
                           +records[i]['RCVBNKNM']   + "|" \
                           +records[i]['BOJEDT']     + "|" \
                           +records[i]['BOSPSQ']     + "|" \
                           +records[i]['ORTRCCO']    + "|" \
                           +records[i]['CONT']       + "|" \
                           +records[i]['ISDEAL']     + "|" \
                           +records[i]['BILDAT']     + "|" \
                           +records[i]['BILNO']      + "|" \
                           +records[i]['BILPNAM']    + "|" \
                           +records[i]['BILENDDT']   + "|" \
                           +str(records[i]['BILAMT'])+ "|" \
                           +records[i]['PYENAM']     + "|" \
                           +records[i]['HONBNKNM']   + "|" \
                           +records[i]['PRCCO']      + "|" \
                           +records[i]['STRINFO']    + "|"
                f.write(filecontext+"\n")
            f.close()
            
            #=====输出接口赋值====
            TradeContext.PBDAFILE=filename              #文件名
            TradeContext.RECCOUNT=str(len(records))     #查询笔数
            TradeContext.RECALLCOUNT=str(allcount)      #总笔数
            
    #=====打印处理 1 打印====        
    elif(TradeContext.PRTTYPE=='1'):
        AfaLoggerFunc.tradeInfo(">>>进入打印处理")
        
        #=====判断查询查复书号是否为空====
        if(TradeContext.BSPSQN!="" ):
            wheresql=wheresql+" AND BSPSQN='"+TradeContext.BSPSQN+"'"           
        else:
            return AfaFlowControl.ExitThisFlow('A099','查询查复书号[BSPSQN]不允许为空' )
            
        #=====查询数据库====
        records = rccpsDBTrcc_pjcbka.selectm(TradeContext.RECSTRNO,10,wheresql,"")
        
        if(records==None):
            return AfaFlowControl.ExitThisFlow('A099','查询失败' )        
        elif( len(records)<=0 ):
            return AfaFlowControl.ExitThisFlow('A099','未查找到数据' )            
        else:
            #=====票据查询书====
            if(TradeContext.TRCCO=='9900520'):                
                AfaLoggerFunc.tradeInfo(">>>业务类型为票据查询书")
                
                #=====票据查询书打印格式====
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
                
                #====写文件操作====
                file_name = 'rccps_' + records[0]['BJEDTE'] + '_' + TradeContext.BSPSQN + '_8532'
                out_file = open(os.environ['AFAP_HOME'] + '/tmp/' + file_name,"wb")
                
                if out_file == None:
                    return AfaFlowControl.ExitThisFlow("S999", "生成打印文件异常")
                
                print >> out_file,txt % {'BESBNM':(sub['BESBNM']).ljust(10,' '),\
                                         'BJEDTE':(records[0]['BJEDTE']).ljust(8,' '),\
                                         'BSPSQN':(TradeContext.BSPSQN).ljust(12,' '),\
                                         'SNDBNKCO':(records[0]['SNDBNKCO']).ljust(10,' '),\
                                         'RCVBNKCO':(records[0]['RCVBNKCO']).ljust(10,' '),\
                                         'BILDAT':(records[0]['BILDAT']).ljust(8,' '),\
                                         'BILENDDT':(records[0]['BILENDDT']).ljust(8,' '),\
                                         'BILNO':(records[0]['BILNO']).ljust(16,' '),\
                                         'BILPNAM':(records[0]['BILPNAM']).ljust(60,' '),\
                                         'HONBNKNM':(records[0]['HONBNKNM']).ljust(60,' '),\
                                         'CONT1':(records[0]['CONT'][:68]).ljust(68,' '),\
                                         'CONT2':(records[0]['CONT'][68:138]).ljust(70,' '),\
                                         'CONT3':(records[0]['CONT'][138:208]).ljust(70,' '),\
                                         'CONT4':(records[0]['CONT'][208:]).ljust(70,' ')}
                
                out_file.close()
                
                TradeContext.PBDAFILE = file_name       #文件名
                
                AfaLoggerFunc.tradeDebug("结束生成打印文本")
            #=====票据查复书====
            elif(TradeContext.TRCCO=='9900521'):               
                AfaLoggerFunc.tradeInfo(">>>业务类型为票据查复书")
                
                #=====查询原交易信息====
                where_dict={'BJEDTE':records[0]['BOJEDT'],'BSPSQN':records[0]['BOSPSQ']}
                
                ret=rccpsDBTrcc_pjcbka.selectu(where_dict)
                if(ret==None):
                    return AfaFlowControl.ExitThisFlow('A099','查询原信息失败' )                    
                if(len(ret)==0):
                    return AfaFlowControl.ExitThisFlow('A099','未查找原信息' )
                
                #=====票据查复书打印格式====
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
           |        %(CONT1)s           |                                            
           |                                                                                       |
           |        %(CONT2)s         |                                              
           |                                                                                       |
           |        %(CONT3)s         |                                              
           |                                                                                       |
           |        %(CONT4)s         |                                              
           |                                                                                       |
           |---------------------------------------------------------------------------------------|
           打印日期: %(BJEDTE)s      授权:                       记账:
                """
                
                #====写文件操作====
                file_name = 'rccps_' + records[0]['BJEDTE'] + '_' + TradeContext.BSPSQN + '_8532'
                out_file = open(os.environ['AFAP_HOME'] + '/tmp/' + file_name,"wb")
                
                if out_file == None:
                    return AfaFlowControl.ExitThisFlow("S999", "生成打印文件异常")
                
                print >> out_file,txt % {'BESBNM':(sub['BESBNM']).ljust(10,' '),\
                                         'BJEDTE':(records[0]['BJEDTE']).ljust(8,' '),\
                                         'BSPSQN':(TradeContext.BSPSQN).ljust(12,' '),\
                                         'SNDBNKCO':(records[0]['SNDBNKCO']).ljust(10,' '),\
                                         'RCVBNKCO':(records[0]['RCVBNKCO']).ljust(10,' '),\
                                         'BILDAT':(records[0]['BILDAT']).ljust(8,' '),\
                                         'BILENDDT':(records[0]['BILENDDT']).ljust(8,' '),\
                                         'BILNO':(records[0]['BILNO']).ljust(16,' '),\
                                         'BILPNAM':(records[0]['BILPNAM']).ljust(60,' '),\
                                         'PYENAM':(records[0]['PYENAM']).ljust(60,' '),\
                                         'HONBNKNM':(records[0]['HONBNKNM']).ljust(60,' '),\
                                         'BOJEDT':(records[0]['BOJEDT']).ljust(8,' '),\
                                         'ORSNDBNKCO':(ret['SNDBNKCO']).ljust(10,' '),\
                                         'BOSPSQ':(records[0]['BOSPSQ']).ljust(12,' '),\
                                         'CONT1':(records[0]['CONT'][:68]).ljust(68,' '),\
                                         'CONT2':(records[0]['CONT'][68:138]).ljust(70,' '),\
                                         'CONT3':(records[0]['CONT'][138:208]).ljust(70,' '),\
                                         'CONT4':(records[0]['CONT'][208:]).ljust(70,' ')}
                
                out_file.close()
                
                TradeContext.PBDAFILE = file_name       #文件名
                
                AfaLoggerFunc.tradeDebug("结束生成打印文本")                            
            else:
                return AfaFlowControl.ExitThisFlow("S999", "业务类型非法")   
    
        TradeContext.RECCOUNT='1'           #查询笔数
        TradeContext.RECALLCOUNT='1'        #总笔数
        TradeContext.errorCode="0000"
        TradeContext.errorMsg="查询成功"
      
    else:
        return AfaFlowControl.ExitThisFlow("S999", "打印标志非法")  

    TradeContext.errorCode="0000"
    TradeContext.errorMsg="查询成功"
                
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.本地类操作交易[TRC001_8532]退出***' )
    return True
