###############################################################################
# -*- coding: gbk -*-
# 文件标识：
# 摘    要：安徽非税
#
# 当前版本：1.0
# 作    者：
# 完成日期：2009年8月5日
###############################################################################

#表中的状态位 0 待查数据  1非非税
import TradeContext

TradeContext.sysType = 'cron'

import AfaDBFunc, AfaLoggerFunc, os, sys, HostContext, ConfigParser, HostComm, AfaUtilTools,AfaAdminFunc
from types import *



def GetLappConfig( CfgFileName = None ):
    try:
        config = ConfigParser.ConfigParser( )

        if( CfgFileName == None ):
            CfgFileName = os.environ['AFAP_HOME'] + '/conf/lapp.conf'

        config.readfp( open( CfgFileName ) )

        TradeContext.HOST_HOSTIP   = config.get('HOST_DZ', 'HOSTIP')
        TradeContext.HOST_USERNO   = config.get('HOST_DZ', 'USERNO')
        TradeContext.HOST_PASSWD   = config.get('HOST_DZ', 'PASSWD')

        TradeContext.HOST_LDIR     = os.environ['AFAP_HOME'] + "/data/ahfs/"        #本地路径
        TradeContext.HOST_RDIR     = 'FTAXLIB'            #config.get('HOST_DZ', 'RDIR')  #远程路径
        TradeContext.TRACE         = config.get('HOST_DZ', 'TRACE')

        return 0

    except Exception, e:
        print str(e)
        return -1

#下载帐号流水明细文件
def GetDetailFile(rfilename, lfilename):
    AfaLoggerFunc.tradeInfo( '--->开始下载文件' )
    try:
        #创建文件
        ftpShell = os.environ['AFAP_HOME'] + '/data/ahfs/shell/ahfs_ahfs.sh'
        ftpFp = open(ftpShell, "w")

        ftpFp.write('open ' + TradeContext.HOST_HOSTIP + '\n')
        ftpFp.write('user ' + TradeContext.HOST_USERNO + ' ' + TradeContext.HOST_PASSWD + '\n')

        #下载文件
        ftpFp.write('cd '  + TradeContext.HOST_RDIR + '\n')
        ftpFp.write('lcd ' + TradeContext.HOST_LDIR + '\n')
        ftpFp.write('quote type c 1381 ' + '\n')
        ftpFp.write('get ' + rfilename + ' ' + lfilename + '\n')

        ftpFp.close()

        ftpcmd = 'ftp -n < ' + ftpShell + ' 1>/dev/null 2>/dev/null '

        ret = os.system(ftpcmd)
        if ( ret != 0 ):
            return -1
        else:
            return 0

    except Exception, e:
        AfaLoggerFunc.tradeInfo(e)
        AfaLoggerFunc.tradeInfo('FTP处理异常')
        return -1


#20111102 陈浩添加
#begin
#------------------------------------------------------------------
#生成一个4位的序号
#------------------------------------------------------------------     
def CrtSequence( ):
    
    try:
        sqlStr = "SELECT NEXTVAL FOR FSYW_ONLINE_SEQ FROM SYSIBM.SYSDUMMY1"

        records = AfaDBFunc.SelectSql( sqlStr )
        if records == None :        
            TradeContext.errorCode,TradeContext.errorMsg    =   "9999","生成序列号异常"
            AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
            AfaLoggerFunc.tradeInfo( sqlStr )
            return False
        
        AfaLoggerFunc.tradeInfo( "序列号：" + str(records[0][0]) )
        
        #序列号
        TradeContext.sequenceNo = str(records[0][0]).rjust(4,'0')
        
        return 0

    except Exception, e:
        print str(e)
        return -1
        
#end        

###########################################主函数###########################################
if __name__=='__main__':

    if ( len(sys.argv) != 2 ):
        TradeContext.serDate = AfaAdminFunc.getTimeFromNow(int(-1))
    else:
        sOffSet                =   sys.argv[1]
        TradeContext.serDate   = AfaAdminFunc.getTimeFromNow(int(sOffSet))

    TradeContext.workDate  =   AfaUtilTools.GetSysDate( )
    TradeContext.workTime =   AfaUtilTools.GetSysTime( )
    #TradeContext.serDate  =   AfaAdminFunc.getTimeFromNow(int(-1))
    #TradeContext.serDate  =   '20090910'
    #TradeContext.serDate  =   '20110601'
    AfaLoggerFunc.tradeInfo( TradeContext.serDate )
    TradeContext.opType   =   '0'
    #TradeContext.appNo    =   'AG2008'
    TradeContext.teller   =   '999986'

    #begin 20100609 蔡永贵修改
    #sqlstr_bus  =  "select busino from fs_businoconf"
    sqlstr_bus = "select busino,bankno from fs_businoconf"
    #end

    records_bus = AfaDBFunc.SelectSql( sqlstr_bus )
    if records_bus == None or len(records_bus)==0 :
        TradeContext.errorCode,TradeContext.errorMsg    =   "0001","查找单位信息表异常"
        AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
        AfaLoggerFunc.tradeInfo( sqlstr_bus )
        sys.exit(1)
    for i in range( len(records_bus) ):
        TradeContext.busiNo  = records_bus[i][0].strip()

        #begin 20100609 蔡永贵增加
        TradeContext.bankbm  = records_bus[i][1].strip()
        if ( TradeContext.bankbm == '012' ):
            TradeContext.appNo = "AG2008"
            
        else:
            TradeContext.appNo = "AG2012"
        #end

        TradeContext.brno    = TradeContext.busiNo[0:10]
        AfaLoggerFunc.tradeInfo( TradeContext.brno )

        #begin 20100609 蔡永贵修改
        #sqlstr_acc   =   "select accno from abdt_unitinfo  where appno='AG2008' and busino='" +  TradeContext.busiNo + "'"
        sqlstr_acc   =   "select accno from abdt_unitinfo  where busino='" +  TradeContext.busiNo + "'"
        sqlstr_acc   =   sqlstr_acc + " and appno = '" + TradeContext.appNo + "'"
        #end

        records_acc = AfaDBFunc.SelectSql( sqlstr_acc )
        if records_bus == None or len(records_bus)==0 :
            TradeContext.errorCode,TradeContext.errorMsg    =   "0001","查找单位信息表异常"
            AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
            AfaLoggerFunc.tradeInfo( sqlstr_bus )
            continue
            #sys.exit(1)

        else:
            TradeContext.accno   =   records_acc[0][0]

        #通讯区打包
        HostContext.I1TRCD = '8847'                        #交易码
        HostContext.I1SBNO = TradeContext.brno             #交易机构号
        HostContext.I1USID = '999986'                      #交易柜员号
        HostContext.I1AUUS = ""                            #授权柜员
        HostContext.I1AUPS = ""                            #授权柜员密码
        HostContext.I1WSNO = '10.12.2.199'                 #终端号
        
        
        #20111102 陈浩修改 文件名加序列号 确保唯一性
        #begin    
        #获取一个4位的序列号，用于拼上送核心的开户文件名 确保唯一性
        
        if CrtSequence() < 0 :
            TradeContext.errorCode  =   "0001"
            TradeContext.errorMsg   =   "生成文件序列号失败"
            continue

        #HostContext.I1FINA = 'AG12345678'                             #文件名称
        HostContext.I1FINA = 'AG1234'+ TradeContext.sequenceNo         #文件名称(10位)  
        #end
        
        HostContext.I1STDT = TradeContext.serDate          #开始日期
        HostContext.I1EDDT = TradeContext.serDate          #终止日期
        HostContext.I1ACCN = TradeContext.accno            #对公活期帐号
        AfaLoggerFunc.tradeInfo('返回结果:交易帐号     = ' + HostContext.I1ACCN)

        HostTradeCode = "8847".ljust(10,' ')
        HostComm.callHostTrade( os.environ['AFAP_HOME'] + '/conf/hostconf/AH8847.map', HostTradeCode, "0002" )
        if( HostContext.host_Error ):
            AfaLoggerFunc.tradeInfo('>>>主机交易失败=[' + str(HostContext.host_ErrorType) + ']:' +  HostContext.host_ErrorMsg)
            TradeContext.errorCode  =   "0001"
            TradeContext.errorMsg   =   HostContext.host_ErrorMsg
            continue
            #sys.exit(1)
        else:
            if ( HostContext.O1MGID == "AAAAAAA" ):
                AfaLoggerFunc.tradeInfo('>>>查询处理结果=[' + HostContext.O1MGID + ']交易成功')
                AfaLoggerFunc.tradeInfo('返回结果:文件名称     = ' + HostContext.O1FINA)        #文件名称
                AfaLoggerFunc.tradeInfo('返回结果:交易日期     = ' + HostContext.O1TRDT)        #交易日期
                AfaLoggerFunc.tradeInfo('返回结果:交易时间     = ' + HostContext.O1TRTM)        #交易时间

            else:
                TradeContext.errorCode  =   "0001"
                TradeContext.errorMsg   =   HostContext.O1INFO
                AfaLoggerFunc.tradeInfo('主机返回结果:' + TradeContext.errorMsg)
                continue
                #sys.exit(1)

        AfaLoggerFunc.tradeInfo( "********************中台帐号流水明细查询开始***************" )
        if GetLappConfig() < 0 :
            TradeContext.errorCode  =   "0001"
            TradeContext.errorMsg   =   "读取配置文件错误"
            continue
            #sys.exit(1)

        AfaLoggerFunc.tradeInfo(TradeContext.HOST_HOSTIP)
        AfaLoggerFunc.tradeInfo(TradeContext.HOST_USERNO)
        AfaLoggerFunc.tradeInfo(TradeContext.HOST_PASSWD)
        AfaLoggerFunc.tradeInfo(TradeContext.TRACE      )
        AfaLoggerFunc.tradeInfo(TradeContext.HOST_LDIR  )
        AfaLoggerFunc.tradeInfo(TradeContext.HOST_RDIR  )

        #fileName    =   os.environ['AFAP_HOME'] + "/data/ahfs/" + TradeContext.FileName
        #=====张恒修改文件名加银行编码======
        lFileName    =   'DOWN_8477_' + TradeContext.bankbm+TradeContext.busiNo + '.txt'
        AfaLoggerFunc.tradeInfo( '下载文件名称【' + lFileName + "】" )
        if GetDetailFile( HostContext.O1FINA,lFileName ) != 0 :
            TradeContext.errorCode  =   "0001"
            TradeContext.errorMsg   =   "ftp流水明细文件失败"
            continue
            #sys.exit(1)

        AfaLoggerFunc.tradeInfo( "********************中台帐号流水明细查询结束***************" )
        TradeContext.errorCode      =   "0000"
        TradeContext.errorMsg       =   "中台帐号流水明细查询成功"
        TradeContext.downFileName   =   lFileName

        TradeContext.FileName   =   TradeContext.downFileName


        #-----------------------根据单位编码配置获取财政信息----------------------------
        #begin 20100609 蔡永贵修改
        #sqlstr      =   "select aaa010,bankno from fs_businoinfo where busino='" + TradeContext.busiNo + "'"
        sqlstr      =   "select aaa010,bankno from fs_businoinfo where busino='" + TradeContext.busiNo + "'"
        sqlstr      =   sqlstr + " and bankno = '" + TradeContext.bankbm + "'"
        #end


        records = AfaDBFunc.SelectSql( sqlstr )
        if records == None or len(records)==0 :
            TradeContext.errorCode,TradeContext.errorMsg    =   "0001","查找单位信息表异常"
            AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
            AfaLoggerFunc.tradeInfo( sqlstr )
            continue
            #sys.exit(1)

        elif len(records) > 1:
            TradeContext.errorCode,TradeContext.errorMsg    =   "0001","单位信息表异常:一个单位编号对应了多个财政信息"
            AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
            AfaLoggerFunc.tradeInfo( sqlstr )
            continue
            #sys.exit(1)

        TradeContext.AAA010     =   records[0][0].strip()
        TradeContext.AFA101     =   records[0][1].strip()

        try:
            #查询未清分过的
            if TradeContext.opType  ==   '0':

                if( not TradeContext.existVariable( "FileName" ) ):
                    TradeContext.errorCode,TradeContext.errorMsg    =   '0001','文件名称为空'
                    continue
                    #sys.exit(1)

                fileName = os.environ['AFAP_HOME'] + "/data/ahfs/" + TradeContext.FileName

                AfaLoggerFunc.tradeInfo( '文件名称：' + fileName )
                if ( os.path.exists(fileName) and os.path.isfile(fileName) ):
                    AfaLoggerFunc.tradeInfo( '进入查询未清分' )
                    fp      =   open(fileName,"r")
                    sLine   =   fp.readline()
                    while ( sLine ):
                        AfaLoggerFunc.tradeInfo( "********************中台清分查询开始***************" )


                        LineItem    =   sLine.split("<fld>")

                        dateTmp     =   TradeContext.serDate[0:4] + '-' + TradeContext.serDate[4:6] + '-' + TradeContext.serDate[6:8]
                        sqlstr      =   ""
                        #begin 20100609 蔡永贵修改
                        #sqlstr      =   "select * from fs_fc74 where afc401='" + LineItem[0].strip() + "' and afc015='" + dateTmp + "' and busino='" + TradeContext.busiNo + "'"
                        sqlstr      =   sqlstr + "select * from fs_fc74 where afc401='" + LineItem[0].strip() + "' and afc015='" + dateTmp + "' and busino='" + TradeContext.busiNo + "'"
                        sqlstr      =   sqlstr + " and afa101 = '" + TradeContext.AFA101 + "'"
                        #end

                        AfaLoggerFunc.tradeInfo( sqlstr )
                        records = AfaDBFunc.SelectSql( sqlstr )
                        if( records == None  ):
                            TradeContext.errorCode  =   "0001"
                            TradeContext.errorMsg   =   "查找流水明细表异常"
                            AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
                            continue
                            #sys.exit(1)

                        #如果没有查到流水号码，则插入一条记录
                        if ( len( records)==0 ):

                            #begin 20100609 蔡永贵修改
                            sql2 = ""
                            #sql2 = "select accno from fs_businoinfo where busino='" + TradeContext.busiNo + "'"
                            sql2 = sql2 + "select accno from fs_businoinfo where busino='" + TradeContext.busiNo + "'"
                            sql2 = sql2 + " and bankno = '" + TradeContext.bankbm + "'"
                            #end

                            red = AfaDBFunc.SelectSql( sql2 )
                            if red == None or len(red)==0 :
                                TradeContext.errorCode,TradeContext.errorMsg    =   "0001","查找单位信息表异常"
                                AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
                                AfaLoggerFunc.tradeInfo( sql2 )
                                #=====没有则赋空====
                                TradeContext.accno1 = ''

                            #=====赋值====
                            TradeContext.accno1 = red[0][0]

                            AfaLoggerFunc.tradeInfo( '插入流水号码%s' %LineItem[0] )
                            sqlstr      =   ""          #流水号               缴款人名称         缴款人账号  收费金额        银行收款时间
                            sqlstr      =   "insert into fs_fc74 (AFC401,AAA010,AFA101,AFC004,AFC006,AFC007,AFC008,AFC011,AFC015,PAYTIME,AFC016,TELLER,BUSINO,FZPH,AFA091,AFC001,NOFEE,FLAG,DATE,TIME) values ( "

                            dateTmp     =   LineItem[5].strip()
                            dateTmp     =   dateTmp[0:4] + '-' + dateTmp[4:6] + '-' + dateTmp[6:8]

                            sqlstr      =   sqlstr  + "'" +  LineItem[0].strip()         + "',"         #流水号
                            sqlstr      =   sqlstr  + "'" +  TradeContext.AAA010         + "',"         #财政区划内码
                            sqlstr      =   sqlstr  + "'" +  TradeContext.AFA101         + "',"         #银行外码

                            #sqlstr      =   sqlstr  + "'" +  ''                         + "',"         #收款人帐号
                            sqlstr      =   sqlstr  + "'" +  TradeContext.accno1           + "',"         #收款人帐号

                            sqlstr      =   sqlstr  + "'" +  LineItem[1].strip()         + "',"         #交款人名
                            sqlstr      =   sqlstr  + "'" +  ''                          + "',"         #缴款人开户行
                            sqlstr      =   sqlstr  + "'" +  LineItem[2].strip()         + "',"         #缴款人帐号
                            sqlstr      =   sqlstr  + "'" +  LineItem[3].strip()         + "',"         #收费金额
                            sqlstr      =   sqlstr  + "'" +  dateTmp                     + "',"         #收款日期
                            sqlstr      =   sqlstr  + "'" +  LineItem[4].strip()         + "',"         #收款时间
                            sqlstr      =   sqlstr  + "'" +  TradeContext.brno           + "',"         #银行网点

                            sqlstr      =   sqlstr  + "'" +  TradeContext.teller         + "',"         #柜员号
                            sqlstr      =   sqlstr  + "'" +  TradeContext.busiNo         + "',"         #单位编号
                            sqlstr      =   sqlstr  + "'" +  ''                          + "',"         #支票号
                            sqlstr      =   sqlstr  + "'" +  ''                          + "',"         #大厅外码
                            sqlstr      =   sqlstr  + "'" +  ''                          + "',"         #缴款书编号
                            sqlstr      =   sqlstr  + "'" +  ''                          + "',"         #缴款书金额
                            sqlstr      =   sqlstr  + "'" +  '*'                         + "',"         #标志位,初始化为未处理状态
                            sqlstr      =   sqlstr  + "'" +  '00000000'                  + "',"         #日期
                            sqlstr      =   sqlstr  + "'" +  TradeContext.workTime       + "')"         #时间


                            if( AfaDBFunc.InsertSql( sqlstr ) < 1 ):
                                AfaDBFunc.RollbackSql( )
                                AfaLoggerFunc.tradeInfo( "插入数据库失败" )
                                AfaLoggerFunc.tradeInfo(sqlstr)
                                AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
                                TradeContext.errorCode  =   "0001"
                                TradeContext.errorMsg   =   "插入流水表失败"
                                continue
                                #sys.exit(1)

                            AfaDBFunc.CommitSql( )

                        sLine   =   fp.readline()

                    #从数据库中查询出来数据，写到文件中去
                    sqlstr  =   ""

                    dateTmp     =   TradeContext.serDate[0:4] + '-' + TradeContext.serDate[4:6] + '-' + TradeContext.serDate[6:8]

                    #begin 20100609 蔡永贵修改
                    #当前状态、流水号、收费金额、缴款人账号、缴款人名称、收款日期、银行收款时间
                    sqlstr  = ""
                    #sqlstr  =   "select flag,afc401,afc011,afc008,afc006,afc015,paytime from fs_fc74 where afc015='" + dateTmp + "' and busino='" + TradeContext.busiNo + "' and afc016='" + TradeContext.brno + "' and flag='*'  and date='00000000' "
                    sqlstr  =   sqlstr + "select flag,afc401,afc011,afc008,afc006,afc015,paytime from fs_fc74 where afc015='" + dateTmp + "' and busino='" + TradeContext.busiNo + "' and afc016='" + TradeContext.brno + "' and flag='*'  and date='00000000' "
                    sqlstr  =   sqlstr + " and afa101 = '" + TradeContext.AFA101 + "'"
                    #end

                    AfaLoggerFunc.tradeInfo( sqlstr )
                    records = AfaDBFunc.SelectSql( sqlstr )
                    if( records == None  ):
                        TradeContext.errorCode  =   "0001"
                        TradeContext.errorMsg   =   "查找流水信息失败"
                        AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
                        AfaLoggerFunc.tradeInfo( sqlstr + AfaDBFunc.sqlErrMsg )
                        continue
                        #sys.exit(1)

                    else:
                        #将数据写到文件中去
                        lDir        =   os.environ['AFAP_HOME'] + "/data/ahfs/"             #本地目录
                        #====张恒修改加上银行编码
                        fName       =   "DOWN_8474_" + TradeContext.bankbm+TradeContext.busiNo + ".txt"         #文件名称

                        try:
                            hp      =   open(lDir+fName,"w")

                            hp.write( str(len(records)) + "\n" )
                            i       =   0
                            while( i < len(records) ):
                                lineList    =   list(records[i])

                                if lineList[0]   ==  '*':
                                    lineList[0]  =   '1'

                                #转化日期格式将0000-00-00转化为00000000
                                lineList[5]  =   lineList[5].replace('-','')

                                hp.write( "|".join( lineList ) )
                                if i != len(records) -1 :
                                    hp.write( "\n" )

                                i = i + 1
                            else:
                                hp.close()
                                TradeContext.downFileName   =   fName

                        except Exception, e:
                            AfaLoggerFunc.tradeInfo( str(e) )
                            TradeContext.errorCode  =   "0001"
                            TradeContext.errorMsg   =   "写文件异常"
                            continue
                            #sys.exit(1)

                else:
                    AfaLoggerFunc.tradeInfo( "文件" + fileName + "不存在" )
                    TradeContext.errorCode  =   "0002"
                    TradeContext.errorMsg   =   "没有找到上传文件"
                    continue
                    #sys.exit(1)

            AfaLoggerFunc.tradeInfo( "********************中台清分查询结束***************" )
            TradeContext.errorCode  =   "0000"
            TradeContext.errorMsg   =   "清分查询成功"
            continue
            #sys.exit(0)

        except Exception, e:
            AfaLoggerFunc.tradeInfo( str(e) )
            TradeContext.errorCode  =   "0003"
            TradeContext.errorMsg   =   "清分查询异常"
            sys.exit(1)

        except Exception, e:
            AfaLoggerFunc.tradeInfo( str(e) )
            TradeContext.errorCode  =   "0003"
            TradeContext.errorMsg   =   "清分查询异常"
            sys.exit(1)


