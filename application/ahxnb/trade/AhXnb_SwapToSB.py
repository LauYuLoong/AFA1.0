# -*- coding: gbk -*-
###############################################################################
# 文件名称：AhXnb_SwapToSB.py
# 文件标识：
# 作    者：曾照泰
# 摘    要：转换批量代扣代发文件为社保需要的格式
#
###############################################################################
import TradeContext

TradeContext.sysType = 'ahxnb'     
                                   
import AfaDBFunc,os,AfaLoggerFunc
import AfaAdminFunc,sys,AfaFtpFunc
from types import *

#=========================处理函数==============================================
def file_Pro( ):
    try:
        #----1，查询未处理的批量文件
        sql = ""
        sql = sql + "select appno,busino,applydate,filetype ,filename,batchno,swapfilename"
        sql = sql + " from ahnx_file"
        sql = sql + " where status='3'"            #代发代扣上传文件转换成功
        sql = sql + " and filetype in ('0','1')"   #代发代扣
        
        AfaLoggerFunc.tradeInfo('>>>>>>>开始查询AHNX_FILE原交易：'+ str(sql))
        records = AfaDBFunc.SelectSql( sql ) 
                  
        if records==None:
            return ExitSubTrade("D0001" ,"查询AHNX_FILE失败")
        elif(len(records) == 0):
            return ExitSubTrade("D0001" ,"无此信息")
            
        else:
            AfaLoggerFunc.tradeInfo("AHNX_FILE表中的记录数：" +str(len(records)))
            for i in range(len(records)):
                TradeContext.mFileName    = records[i][4]
                TradeContext.swapFileName = records[i][6]
                TradeContext.batchno      = records[i][5]
                
                #----1.1，查询某一批次的处理状态(abdt_batchinfo)
                sql = ""
                sql = sql + "select status,procmsg"
                sql = sql + " from abdt_batchinfo"
                sql = sql + " where batchno='"+TradeContext.batchno +"'"   #批次号(ahxnb_file/abdt_batchinfo一致)
                
                AfaLoggerFunc.tradeInfo("查询ABDT_BATCHINFO表："+ str(sql))
                result = AfaDBFunc.SelectSql( sql )
                
                if result==None:
                    continue
                    #return ExitSubTrade("D0001" ,"查询表abdt_batchinfo失败")
                elif(len(result) == 0):
                    continue
                    #return ExitSubTrade("D0001" ,"无此信息")
                
                AfaLoggerFunc.tradeInfo("状态为:"+result[0][0])   
                #保存批量处理结果信息
                TradeContext.swapprocmsg = result[0][1]
                #保存批量处理结果状态，初始化为3（0-批量文件上传成功，待转换，1-处理成功，2-处理失败3，批量文件转换成功，待处理）
                TradeContext.swapstatus = "3"
                
                #----2，根据查询出来的批量处理状态，生成社保回盘文件 
                #----2.1，批量处理状态为88
                if(result[0][0] =='88'):
                
                    #20120916 新农保FTP下载批量回盘文件，到本地相应目录
                    #批量系统回盘文件目录：/home/maps/data/batch/down/
                    #新农保存放文件目录  ：/home/maps/afa/data/batch/down/
                    #begin
                    TradeContext.downFile = records[i][0]+records[i][1]+'0000'+ '_' + records[i][2]+'.RET'
                
                    if not AfaFtpFunc.getFile('AHXNB_GET',TradeContext.downFile,TradeContext.downFile) :
                        AfaLoggerFunc.tradeInfo('ftp下载批量回盘文件失败 : '+ TradeContext.downFile)
                        continue
                    #end
                
                    #状态置为成功
                    TradeContext.swapstatus = "1"
                    TradeContext.swapprocmsg = "批量处理已完成，可以下载回盘文件"
                    
                    #----2.1.1，生成代发回盘文件
                    if(records[i][3]=='0'):      #文件类型0：代发 1：代扣
                        AfaLoggerFunc.tradeInfo("进入生成代发回盘文件")
                        sFileName = os.environ['AFAP_HOME'] + '/data/batch/down/'+ records[i][0]+records[i][1]+'0000'+ '_' + records[i][2]+'.RET' 
                        
                        #胡友-20120210 修改
                        #dFileName = os.environ['AFAP_HOME'] + '/data/ahxnb/'+'yhdffk'+TradeContext.mFileName[6:] 
                        dFileName = os.environ['AFAP_HOME'] + '/data/ahxnb/'+'YHDFFK'+TradeContext.mFileName[6:-4]+'_F.TXT'       #代发失败回盘文件
                        dFileName_succ = os.environ['AFAP_HOME'] + '/data/ahxnb/'+'YHDFFK'+TradeContext.mFileName[6:-4]+'_S.TXT'  #代发成功回盘文件
                        #end
                        
                        AfaLoggerFunc.tradeInfo("转换前的文件为："+sFileName)
                        AfaLoggerFunc.tradeInfo("转换后(失败)的文件为："+dFileName)
                        AfaLoggerFunc.tradeInfo("转换后(成功)的文件为："+dFileName_succ)
                        
                        #胡友-20120210 修改，增加一个参数
                        if not batch_DF_FilePro(sFileName,dFileName,dFileName_succ):
                            #失败则continue跳出转化下一个文件
                            continue
                        #end
                        
                    #----2.1.2，生成代扣回盘文件
                    if(records[i][3]=='1'):      #文件类型0：代发 1：代扣
                        AfaLoggerFunc.tradeInfo("生成代扣回盘文件")
                        sFileName = os.environ['AFAP_HOME'] + '/data/batch/down/' + records[i][0]+records[i][1]+'0000' + '_'+records[i][2] + '.RET' 
                        
                        #胡友-20111130 begin
                        dFileName = os.environ['AFAP_HOME'] + '/data/ahxnb/' + 'YHDKFK' + TradeContext.mFileName[6:-4]+'_S.TXT'  #代扣成功回盘文件
                        dFileName_fail = os.environ['AFAP_HOME'] + '/data/ahxnb/'+'YHDKFK'+TradeContext.mFileName[6:-4]+'_F.TXT' #代扣失败回盘文件
                        #end
                        
                        AfaLoggerFunc.tradeInfo("转换前的文件为："+sFileName)
                        AfaLoggerFunc.tradeInfo("转换后(成功)的文件为："+dFileName)
                        AfaLoggerFunc.tradeInfo("转换后(失败)的文件为："+dFileName_fail)
                        
                        #胡友-20120210 修改，增加一个参数
                        if not batch_DK_FilePro(sFileName,dFileName,dFileName_fail):
                            #失败则continue跳出转化下一个文件
                            continue
                        #end
                
                #----2.2，批量处理状态为40
                elif(result[0][0] =='40'):
                    #设置处理状态为失败
                    TradeContext.swapstatus = "2"
                    TradeContext.swapprocmsg="批量代发代扣操作处理失败，文件转换成功，可以下载"
                    
                    #----2.2.1，生成代发回盘文件
                    if(records[i][3]=='0'):      #文件类型0：代发 1：代扣
                        AfaLoggerFunc.tradeInfo("生成代发回盘文件")
                        sFileName = os.environ['AFAP_HOME'] + '/data/ahxnb/'+ TradeContext.mFileName
                        
                        #胡友-20120210 修改回盘文件名
                        dFileName = os.environ['AFAP_HOME'] + '/data/ahxnb/'+'YHDFFK'+TradeContext.mFileName[6:-4]+'_F.TXT' 
                        dFileName_succ = os.environ['AFAP_HOME'] + '/data/ahxnb/'+'YHDFFK'+TradeContext.mFileName[6:-4]+'_S.TXT' 
                        #end
                        
                        AfaLoggerFunc.tradeInfo("转换前的文件为："+sFileName)
                        AfaLoggerFunc.tradeInfo("转换后(成功)的文件为："+dFileName_succ)
                        AfaLoggerFunc.tradeInfo("转换后(失败)的文件为："+dFileName)
                        
                        if not batch_DF_Fail_FilePro(sFileName,dFileName):
                            #失败则continue跳出转化下一个文件
                            continue
                            
                        #代发成功-空文件
                        wsfp=open(dFileName_succ,"w")
                        wsfp.write("")
                        wsfp.close( )
                    
                    #----2.2.1，生成代扣回盘文件
                    if(records[i][3]=='1'):      #文件类型0：代发 1：代扣
                        AfaLoggerFunc.tradeInfo("生成代扣回盘文件")
                        
                        #胡友-20120210 修改回盘文件名
                        sFileName = os.environ['AFAP_HOME'] + '/data/ahxnb/' + TradeContext.mFileName
                        dFileName = os.environ['AFAP_HOME'] + '/data/ahxnb/' + 'YHDKFK' + TradeContext.mFileName[6:-4]+'_S.TXT'       #代扣成功回盘文件
                        dFileName_fail = os.environ['AFAP_HOME'] + '/data/ahxnb/' + 'YHDKFK' + TradeContext.mFileName[6:-4]+'_F.TXT'  #代扣失败回盘文件
                        
                        if not batch_DK_Fail_FilePro(sFileName,dFileName_fail):
                            continue
                        #end
                        
                        AfaLoggerFunc.tradeInfo("转换前的文件为："+sFileName)
                        AfaLoggerFunc.tradeInfo("转换后(成功)的文件为："+dFileName)
                        AfaLoggerFunc.tradeInfo("转换后(失败)的文件为："+dFileName_fail)
                        
                        #代扣成功-空文件
                        wfp=open(dFileName,"w")
                        wfp.write("")
                        wfp.close( )
                        
                #----3，更新ahnx_file表
                sqlupdate = ""
                sqlupdate = sqlupdate + "update ahnx_file"
                sqlupdate = sqlupdate + " set status='"+ TradeContext.swapstatus +"'," #处理状态
                sqlupdate = sqlupdate + "procmsg='"+TradeContext.swapprocmsg+"'"       #处理信息
                sqlupdate = sqlupdate + " where batchno='"+TradeContext.batchno+"'"    #批次号
                
                AfaLoggerFunc.tradeInfo("更新AHNX_FILE语句："+str(sqlupdate))
                retcode = AfaDBFunc.UpdateSqlCmt( sqlupdate )
                
                if (retcode < 0):
                    #失败则continue跳出转化下一个文件
                    continue 
    except Exception, e:
        AfaLoggerFunc.tradeFatal( str(e) )
        return False

#转换处理代发失败的数据格式
def batch_DF_FilePro(sFileName,dFileName,dFileName_succ):
    try:
        if ( os.path.exists(sFileName) and os.path.isfile(sFileName) ):
            AfaLoggerFunc.tradeInfo("批量处理数据文件存在")
            
            bfp = open(sFileName, "r")
            wfp = open(dFileName,"w")
            wsfp = open(dFileName_succ,"w")
            
            count = 0
            linebuf = bfp.readline()
            
            while ( len(linebuf) > 0 ):
                count = count + 1
                linebuf1=linebuf.split('|')
                
                if ( linebuf1[0] == "1" ):
                    #从第二行开始读取明细信息
                    linebuf = bfp.readline()
                    continue
                
                #----1，代发失败明细写入文件
                if((linebuf1[0] =='2') and (linebuf1[11]!='AAAAAAA')):
                    
                    wbuffer = ''
                    wbuffer = wbuffer + linebuf1[1] + '|'     #社保编号
                    #wbuffer = wbuffer + linebuf1[4] + '|'     #姓名
                    
                    sql = ""
                    sql = sql + "select identityno,sbbillno,Name"
                    sql = sql + " from ahxnb_swap"
                    sql = sql + " where sbno='" +linebuf1[1].lstrip().rstrip() + "'"  #社保编号
                    sql = sql + " and workdate= '" +  TradeContext.WorkDate + "'"     #申请日期
                                        
                    records = AfaDBFunc.SelectSql( sql ) 
                    
                    if records==None:
                        linebuf = bfp.readline()
                        continue
                        
                    if(len(records) == 0):
                        wbuffer = wbuffer + linebuf1[4].strip().split(';')[0].ljust(20,' ')  + '|'    #姓名
                        wbuffer = wbuffer + '查询ahxnb_swap无此记录'  + '|'    #身份证号
                        wbuffer = wbuffer + linebuf1[7]               + '|'    #代发金额
                        wbuffer = wbuffer + '查询ahxnb_swap无此记录'           #社保单据号
                        
                    elif(len(records) == 1):
                        wbuffer = wbuffer + linebuf1[4]    + '|'    #姓名
                        wbuffer = wbuffer + records[0][0]  + '|'    #身份证号
                        wbuffer = wbuffer + linebuf1[7]    + '|'    #代发金额
                        wbuffer = wbuffer + records[0][1].strip()   #社保单据号
                        
                    else:
                        Flag = '0'
                        for j in range(0,len(records)):
                            if( records[j][2].strip() == linebuf1[4].strip() ):
                                Flag = '1'
                                wbuffer = wbuffer + linebuf1[4].strip().split(';')[0].ljust(20,' ')  + '|'    #姓名
                                wbuffer = wbuffer + records[j][0]                      + '|'    #身份证号
                                wbuffer = wbuffer + linebuf1[7]                        + '|'    #代发金额
                                wbuffer = wbuffer + records[j][1].strip()                       #社保单据号
                        
                        if ( Flag == '0' ):
                            wbuffer = wbuffer + linebuf1[4].strip().split(';')[0].ljust(20,' ')+ '|'    #姓名
                            wbuffer = wbuffer + '同一客户多个批次，查询ahxnb_swap无此记录'         + '|'    #身份证号
                            wbuffer = wbuffer + linebuf1[7]                      + '|'    #代发金额
                            wbuffer = wbuffer + '同一客户多个批次，查询ahxnb_swap无此记录'                  #社保单据号
                            
                    wbuffer = wbuffer + '\n'
                    wfp.write(wbuffer)
                    
                #----2，代发成功明细写入文件
                elif((linebuf1[0] =='2') and (linebuf1[11]=='AAAAAAA')):
                    wbuffer = ''
                    wbuffer = wbuffer + linebuf1[1] + '|'     #社保编号
                    #wbuffer = wbuffer + linebuf1[4] + '|'    #姓名
                    
                    sql = ""
                    sql = sql + "select identityno,sbbillno,Name"
                    sql = sql + " from ahxnb_swap"
                    sql = sql + " where sbno='" +linebuf1[1].lstrip().rstrip() + "'"  #社保编号
                    sql = sql + " and workdate= '" +  TradeContext.WorkDate + "'"     #申请日期
                    
                    records = AfaDBFunc.SelectSql( sql ) 
                    
                    if records==None:
                        linebuf = bfp.readline()
                        continue
                        
                    if(len(records) == 0):
                        wbuffer = wbuffer + linebuf1[4].strip().split(';')[0].ljust(20,' ')  + '|'    #姓名
                        wbuffer = wbuffer + '查询ahxnb_swap无此记录'  + '|'    #身份证号
                        wbuffer = wbuffer + linebuf1[7]               + '|'    #代发金额
                        wbuffer = wbuffer + '查询ahxnb_swap无此记录'           #社保单据号
                        
                    elif(len(records) == 1):
                        wbuffer = wbuffer + linebuf1[4]    + '|'    #姓名
                        wbuffer = wbuffer + records[0][0]  + '|'    #身份证号
                        wbuffer = wbuffer + linebuf1[7]    + '|'    #代发金额
                        wbuffer = wbuffer + records[0][1].strip()     #社保单据号
                        
                    else:
                        Flag = '0'
                        for j in range(0,len(records)):
                            if( records[j][2].strip() == linebuf1[4].strip() ):
                                Flag = '1'
                                wbuffer = wbuffer + linebuf1[4].strip().split(';')[0].ljust(20,' ')  + '|'    #姓名
                                wbuffer = wbuffer + records[j][0]                      + '|'    #身份证号
                                wbuffer = wbuffer + linebuf1[7]                        + '|'    #代发金额
                                wbuffer = wbuffer + records[j][1].strip()                         #社保单据号
                        
                        if ( Flag == '0' ):
                            wbuffer = wbuffer + linebuf1[4].strip().split(';')[0].ljust(20,' ')+ '|'    #姓名
                            wbuffer = wbuffer + '同一客户多个批次，查询ahxnb_swap无此记录'         + '|'    #身份证号
                            wbuffer = wbuffer + linebuf1[7]                      + '|'    #代发金额
                            wbuffer = wbuffer + '同一客户多个批次，查询ahxnb_swap无此记录'
                    
                    wbuffer = wbuffer + '\n'
                    wsfp.write(wbuffer)
                            
                else:
                    wbuffer = ""
                    wbuffer = wbuffer + "批量回盘文件第" + str(count) + "行格式[字段]不正确，请检查"
                    wbuffer = wbuffer + "\n"
                    wfp.write(wbuffer)
                    
                linebuf = bfp.readline()
            
            #关闭文件
            bfp.close()
            wfp.close()
            wsfp.close()
            return True
        
        else:
            AfaLoggerFunc.tradeInfo("批量处理数据文件不存在或不是文件")
            return False 
                      
    except Exception, e:
        AfaLoggerFunc.tradeFatal( str(e) )
        bfp.close()
        wfp.close()
        wsfp.close()
        return False

#转换成银行反馈社保代扣成功时数据格式
def batch_DK_FilePro(sFileName,dFileName,dFileName_fail):
    try:
        if ( os.path.exists(sFileName) and os.path.isfile(sFileName) ):
            AfaLoggerFunc.tradeInfo("批量处理数据文件存在")
            
            bfp = open(sFileName, "r")
            wfp = open(dFileName,"w")
            ffp = open(dFileName_fail,"w")
            
            count = 0
            linebuf = bfp.readline()
            
            while ( len(linebuf) > 0 ):
                count = count + 1
                linebuf1=linebuf.split('|')
                
                if ( linebuf1[0] == "1" ):
                    #从第二行开始读取明细信息
                    linebuf = bfp.readline()
                    continue
                
                #----1，代扣成功明细写入文件
                if((linebuf1[0] =='2') and (linebuf1[11]=='AAAAAAA')):
                    wbuffer = ''
                    wbuffer = wbuffer + linebuf1[1] + '|'     #社保编号
                    #wbuffer = wbuffer + linebuf1[4] + '|'     #姓名 
                    
                    sql = "select identityno,sbbillno,Name"
                    sql = sql + " from ahxnb_swap"
                    sql = sql + " where sbno='" +linebuf1[1].lstrip().rstrip() + "'"
                    sql = sql + " and workdate= '" +  TradeContext.WorkDate + "'"
                    AfaLoggerFunc.tradeInfo(sql)
                    records = AfaDBFunc.SelectSql( sql ) 
                    AfaLoggerFunc.tradeInfo(records)
                    if records==None:
                        linebuf = bfp.readline()
                        continue
                        
                    if(len(records) == 0):
                        wbuffer = wbuffer + linebuf1[4].strip().split(';')[0].ljust(20,' ')            + '|'  #姓名 
                        wbuffer = wbuffer + "swap表无此记录"       + '|'  #身份证号
                        wbuffer = wbuffer + linebuf1[7]            + '|'  #金额
                        wbuffer = wbuffer + "swap表无此记录"       + '|'  #批次号
                        
                    elif(len(records) == 1):
                        wbuffer = wbuffer + linebuf1[4]    + '|'    #姓名
                        wbuffer = wbuffer + records[0][0]  + '|'    #身份证号
                        wbuffer = wbuffer + linebuf1[7]    + '|'    #代发金额
                        wbuffer = wbuffer + records[0][1].strip()       #社保单据号
                        
                    else:
                        Flag = '0'
                        for j in range(0,len(records)):
                            if( records[j][2].strip() == linebuf1[4].strip() ):
                                AfaLoggerFunc.tradeInfo(str(j) + records[j][2].strip())
                                AfaLoggerFunc.tradeInfo(linebuf1[4].strip())
                                Flag = '1'
                                wbuffer = wbuffer + linebuf1[4].strip().split(';')[0].ljust(20,' ')  + '|'    #姓名
                                wbuffer = wbuffer + records[j][0]                      + '|'    #身份证号
                                wbuffer = wbuffer + linebuf1[7]                        + '|'    #代发金额
                                wbuffer = wbuffer + records[j][1].strip()                         #社保单据号
                        
                        if ( Flag == '0' ):
                            wbuffer = wbuffer + linebuf1[4].strip().split(';')[0].ljust(20,' ')+ '|'    #姓名
                            wbuffer = wbuffer + '同一客户多个批次，查询ahxnb_swap无此记录'         + '|'    #身份证号
                            wbuffer = wbuffer + linebuf1[7]                      + '|'    #代发金额
                            wbuffer = wbuffer + '同一客户多个批次，查询ahxnb_swap无此记录'
                    
                    wbuffer = wbuffer + '\n'
                    wfp.write(wbuffer)
                
                #----2，代扣失败明细写入文件
                elif( (linebuf1[0] =='2') and (linebuf1[11]!='AAAAAAA') ):
                    wbuffer = ''
                    wbuffer = wbuffer + linebuf1[1]    + '|'     #社保编号
                    #wbuffer = wbuffer + linebuf1[4]    + '|'     #姓名
                    
                    sql = ""
                    sql = sql + "select identityno,sbbillno,Name"
                    sql = sql + " from ahxnb_swap"
                    sql = sql + " where sbno='" + linebuf1[1].strip() + "'"      #社保编号
                    sql = sql + " and workdate= '" + TradeContext.WorkDate + "'" #申请日期
                    
                    records = AfaDBFunc.SelectSql( sql ) 
                    
                    if records==None:
                        linebuf = bfp.readline()
                        continue
                        
                    if(len(records) == 0):
                        wbuffer = wbuffer + linebuf1[4].strip().split(';')[0].ljust(20,' ')            + '|'  #姓名 
                        wbuffer = wbuffer + "swap表无此记录"       + '|'  #身份证号
                        wbuffer = wbuffer + linebuf1[7]            + '|'  #金额
                        wbuffer = wbuffer + "swap表无此记录"       + '|'  #社保单据号
                        wbuffer = wbuffer + "该客户在AHXNB_SWAP表中无记录" + ''   #返回说明
                        
                    elif(len(records) == 1):
                        wbuffer = wbuffer + linebuf1[4]    + '|'    #姓名
                        wbuffer = wbuffer + records[0][0]  + '|'    #身份证号
                        wbuffer = wbuffer + linebuf1[7]    + '|'    #代发金额
                        wbuffer = wbuffer + records[0][1].strip()  + '|'    #社保单据号
                        wbuffer = wbuffer + linebuf1[10].strip()    #返回说明
                        
                    else:
                        Flag = '0'
                        for j in range(0,len(records)):
                            if( records[j][2].strip() == linebuf1[4].strip() ):
                                Flag = '1'
                                wbuffer = wbuffer + linebuf1[4].strip().split(';')[0].ljust(20,' ')  + '|'    #姓名
                                wbuffer = wbuffer + records[j][0]                      + '|'    #身份证号
                                wbuffer = wbuffer + linebuf1[7]                        + '|'    #代发金额
                                wbuffer = wbuffer + records[j][1].strip()              + '|'    #社保单据号
                                wbuffer = wbuffer + linebuf1[10].strip()                        #返回说明
                        
                        if ( Flag == '0' ):
                            wbuffer = wbuffer + linebuf1[4].strip().split(';')[0].ljust(20,' ')+ '|'    #姓名
                            wbuffer = wbuffer + '同一客户多个批次，查询ahxnb_swap无此记录'         + '|'    #身份证号
                            wbuffer = wbuffer + linebuf1[7]                      + '|'    #代发金额
                            wbuffer = wbuffer + '同一客户多个批次，查询ahxnb_swap无此记录' + '|'
                            wbuffer = wbuffer + linebuf1[10].strip()                      #返回说明
                    
                    wbuffer = wbuffer + '\n'
                    ffp.write(wbuffer)
                
                else:
                    wbuffer = ""
                    wbuffer = wbuffer + "批量回盘文件第"+str(count)+"行格式有误，请检查"
                    wbuffer = wbuffer + "\n"
                    ffp.write(wbuffer)
                    
                linebuf = bfp.readline()
                
            #关闭文件
            bfp.close()
            wfp.close()
            ffp.close()
            return True
            
        else:
            AfaLoggerFunc.tradeInfo("批量处理数据文件不存在或不是文件")
            return False 
                         
    except Exception, e:
        AfaLoggerFunc.tradeFatal( str(e) )
        bfp.close()
        wfp.close()
        ffp.close()
        return False

#转换处理整个文件都是代发失败的数据格式
def batch_DF_Fail_FilePro(sFileName,dFileName):
    try:
        if ( os.path.exists(sFileName) and os.path.isfile(sFileName) ):  
            AfaLoggerFunc.tradeInfo("批量处理数据文件存在")
           
            wfp = open(dFileName,"w")
            bfp = open(sFileName, "r")
            
            linebuf = bfp.readline()
            
            while ( len(linebuf) > 0 ):
                linebuf1=linebuf.split('|')

                wbuffer = ''
                wbuffer = wbuffer + linebuf1[0]   + '|'       #社保编号
                wbuffer = wbuffer + linebuf1[1]   + '|'       #姓名
                wbuffer = wbuffer + linebuf1[2]   + '|'       #身份证号
                wbuffer = wbuffer + linebuf1[3]   + '|'       #代发金额
                wbuffer = wbuffer + linebuf1[4]               #社保单据号
                
                wbuffer = wbuffer + '\n'
                wfp.write(wbuffer)
                
                linebuf = bfp.readline() 
                
            #关闭文件
            wfp.close()
            bfp.close()
            return True
        
        else:
            AfaLoggerFunc.tradeInfo("批量处理数据文件不存在或不是文件")
            return False 
                      
    except Exception, e:
        AfaLoggerFunc.tradeFatal( str(e) )
        wfp.close()
        bfp.close()
        return False
        
#转换处理整个文件都是代扣失败的数据格式
def batch_DK_Fail_FilePro(sFileName,dFileName_fail):
    try:
        if ( os.path.exists(sFileName) and os.path.isfile(sFileName) ):  
            AfaLoggerFunc.tradeInfo("批量处理数据文件存在")
           
            wfp = open(dFileName_fail,"w")
            bfp = open(sFileName, "r")
            
            linebuf = bfp.readline()
            
            while ( len(linebuf) > 0 ):                                        
                linebuf1=linebuf.split('|')

                wbuffer = ''
                wbuffer = wbuffer + linebuf1[0]   + '|'       #社保编号
                wbuffer = wbuffer + linebuf1[1]   + '|'       #姓名    
                wbuffer = wbuffer + linebuf1[2]   + '|'       #身份证号
                wbuffer = wbuffer + linebuf1[3]   + '|'       #代发金额
                wbuffer = wbuffer + linebuf1[4]   + '|'       #社保单据号
                wbuffer = wbuffer + "批量系统处理失败(40状态)"   + ''        #返回说明
                
                wbuffer = wbuffer + '\n'
                wfp.write(wbuffer)
                
                linebuf = bfp.readline() 
                    
            #关闭文件
            wfp.close()
            bfp.close()
            return True 
        
        else:
            AfaLoggerFunc.tradeInfo("批量处理数据文件不存在或不是文件")
            return False 
                      
    except Exception, e:
        AfaLoggerFunc.tradeFatal( str(e) )
        wfp.close()
        bfp.close()
        return False

#------------------------------------------------------------------
def ExitSubTrade( errorCode, errorMsg ):

    if( len( errorCode )!=0 ):
        TradeContext.errorCode = errorCode
        TradeContext.errorMsg  =errorMsg
        AfaLoggerFunc.tradeInfo( errorMsg )

    if( errorCode.isdigit( )==True and long( errorCode )==0 ):
        return True

    else:
        return False
        
        
        
#######################################主函数###########################################
if __name__=='__main__':

    AfaLoggerFunc.tradeInfo('********************批量转换格式开始********************')
    #默认取前一天的日期，即转换前一天的数据
    if ( len(sys.argv) != 2 ):
        TradeContext.WorkDate = AfaAdminFunc.getTimeFromNow(-1)
        
    #转换具体日期的数据
    else:
        TradeContext.WorkDate =sys.argv[1]
   
    #转换处理
    file_Pro( )
    
    AfaLoggerFunc.tradeInfo('********************批量转换格式结束********************')
