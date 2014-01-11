# -*- coding: gbk -*-
################################################################################
#   代收代付.补打发票模板
#===============================================================================
#   模板文件:   003104.py
#   修改时间:   2006-04-05
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaFunc,AfaTransDtlFunc,AfaFlowControl,AfaDBFunc,os,AfaAfeFunc,Party3Context
from types import *

def main( ):

    AfaLoggerFunc.tradeInfo('******代收代付.补打发票模板[' + TradeContext.TemplateCode + ']进入******')

    try:

        #=====================初始化返回报文变量================================
        TradeContext.tradeResponse=[]

        #=====================获取当前系统时间==================================
        TradeContext.workDate=AfaUtilTools.GetSysDate( )
        TradeContext.workTime=AfaUtilTools.GetSysTime( )

        #=====================判断应用系统状态==================================
        if not AfaFunc.ChkSysStatus( ) :
            raise AfaFlowControl.flowException( )
                
        #=====================校验公共节点的有效性==============================
        if( not TradeContext.existVariable( "sysId") ):
            raise AfaFlowControl.flowException( 'A0001', '系统标识[sysId]值不存在,不能进行补打发票' )

        if( not TradeContext.existVariable( "userno") ):
            raise AfaFlowControl.flowException( 'A0001', '用户号[userno]值不存在,不能进行补打发票' )

        #=====================判断应用系统状态==================================
        if not AfaFunc.ChkSysStatus( ) :
            raise AfaFlowControl.flowException( )

        #=====================判断商户状态======================================
        if not AfaFunc.ChkUnitStatus( ) :
            raise AfaFlowControl.flowException( )

        #=====================判断渠道状态======================================
        if not AfaFunc.ChkChannelStatus( ) :
            raise AfaFlowControl.flowException( )

        #操作标志(0-查询发票信息 1-修改打印次数 2-从第三方获取发票信息,进行打印)
        if( not TradeContext.existVariable( "procFlag") ):
            raise AfaFlowControl.flowException( 'A0001', '操作标志[tradeFlag"]值不存在,不能进行补打发票' )

        if(TradeContext.procFlag=="0"):

            #查询发票信息
            sql="SELECT BILLDATA,ITEM1,ITEM2,ITEM3,ITEM4,ITEM5,ITEM6,BILLSERNO,SERIALNO,PRTNUM,WORKDATE,BILLSTATUS FROM AFA_BILLDTL WHERE "
            sql=sql + " SYSID='"      + TradeContext.sysId  + "'"
            sql=sql + " AND UNITNO='" + TradeContext.unitno + "'"

            if( TradeContext.existVariable( "subUnitno") ):
                sql=sql + " AND SUBUNITNO='" + TradeContext.subUnitno + "'"

            if( TradeContext.existVariable( "userno") ):
                sql=sql + " AND USERNO='" + TradeContext.userno + "'"

            if( TradeContext.existVariable( "payMonth") ):
                sql=sql + " AND WORKDATE LIKE '" + TradeContext.payMonth + "%'"

            if( TradeContext.existVariable( "item1") ):
                sql=sql + " AND ITEM1='"  + TradeContext.item1  + "'"

            if( TradeContext.existVariable( "item2") ):
                sql=sql + " AND ITEM2='"  + TradeContext.item1  + "'"

            if( TradeContext.existVariable( "item3") ):
                sql=sql + " AND ITEM3='"  + TradeContext.item1  + "'"

            if( TradeContext.existVariable( "item4") ):
                sql=sql + " AND ITEM4='"  + TradeContext.item1  + "'"

            if( TradeContext.existVariable( "item5") ):
                sql=sql + " AND ITEM5='"  + TradeContext.item1  + "'"

            if( TradeContext.existVariable( "item6") ):
                sql=sql + " AND ITEM6='"  + TradeContext.item1  + "'"

            sql=sql + " ORDER BY WORKDATE DESC,WORKTIME DESC "

            AfaLoggerFunc.tradeInfo( sql )

            records = AfaDBFunc.SelectSql(sql)

            if( records == None ):
                raise AfaFlowControl.flowException( 'A0002', '数据库操作异常:' + AfaDBFunc.sqlErrMsg )

            if(len(records)==0):
                raise AfaFlowControl.flowException( 'A0002', '无符合条件的记录' )

            if(int(records[0][9])==3):
                raise AfaFlowControl.flowException( 'A0002', '最多3次重打' )

            if(int(records[0][11])==1):
               raise AfaFlowControl.flowException( 'A0002', '票据已作废，不允许打印' )

            TradeContext.billNum = str(len(records))        #发票数量

            if ( TradeContext.TransType=='0' ):
                #变量初始化
                TradeContext.billData = []                  #发票信息
                TradeContext.item1    = []                  #附加项1
                TradeContext.item2    = []                  #附加项2
                TradeContext.item3    = []                  #附加项3
                TradeContext.item4    = []                  #附加项4
                TradeContext.item5    = []                  #附加项5
                TradeContext.item6    = []                  #附加项6
                TradeContext.billserno= []                  #发票序号
                TradeContext.serialno = []                  #中间业务流水号
                TradeContext.prtnum   = []                  #打印次数
                TradeContext.paydate  = []                  #支付日期

                #打包
                for i in range( 0, len(records) ):
                    TradeContext.billData.append(records[i][0])
                    TradeContext.item1.append(records[i][1])
                    TradeContext.item2.append(records[i][2])
                    TradeContext.item3.append(records[i][3])
                    TradeContext.item4.append(records[i][4])
                    TradeContext.item5.append(records[i][5])
                    TradeContext.item6.append(records[i][6])
                    TradeContext.billserno.append(records[i][7])
                    TradeContext.serialno.append(records[i][8])
                    TradeContext.prtnum.append(records[i][9])
                    TradeContext.paydate.append(records[i][10])
            else:
                MxFileName = os.environ['AFAP_HOME'] + '/tmp/MX' + TradeContext.zoneno + TradeContext.brno + TradeContext.tellerno + '.TXT'
                AfaLoggerFunc.tradeInfo('>>>明细文件:['+MxFileName+']')

                if (os.path.exists(MxFileName) and os.path.isfile(MxFileName)):
                    #文件存在,先删除-再创建
                    os.system("rm " + MxFileName)

                #创建明细文件
                sfp = open(MxFileName, "w")

                for i in range( 0, len(records) ):
                    wBuffer = ""
                    wBuffer = wBuffer + records[i][0]
                    wBuffer = wBuffer + records[i][1]
                    wBuffer = wBuffer + records[i][2]
                    wBuffer = wBuffer + records[i][3]
                    wBuffer = wBuffer + records[i][4]
                    wBuffer = wBuffer + records[i][5]
                    wBuffer = wBuffer + records[i][6]
                    wBuffer = wBuffer + records[i][7]
                    wBuffer = wBuffer + records[i][8]
                    wBuffer = wBuffer + records[i][9]
                    wBuffer = wBuffer + records[i][10]

                    sfp.write(wBuffer + '\n')

                sfp.close()

        elif(TradeContext.procFlag=="1"):

            #从第三方获取发票信息,进行打印

            #=====================获取平台流水号====================================
            if( not AfaFunc.GetSerialno( ) ):
                raise AfaFlowControl.flowException( )

            #=====================外调接口(前处理)==================================
            subModuleExistFlag=0
            subModuleName = 'T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode
            try:
                subModuleHandle=__import__( subModuleName )

            except Exception, e:
                AfaLoggerFunc.tradeInfo( e)

            else:
                AfaLoggerFunc.tradeInfo( '执行['+subModuleName+']模块' )
                subModuleExistFlag=1
                if not subModuleHandle.SubModuleDoFst( ) :
                    raise AfaFlowControl.flowException( )

            #与通讯前置交换
            AfaAfeFunc.CommAfe()

            if TradeContext.errorCode!='0000' :
                raise AfaFlowControl.flowException( )

            #发票数量
            TradeContext.billNum = Party3Context.billNum

            if ( TradeContext.TransType=='0' ):
                #变量初始化
                TradeContext.billData = []                  #发票信息
                TradeContext.item1    = []                  #附加项1
                TradeContext.item2    = []                  #附加项2
                TradeContext.item3    = []                  #附加项3
                TradeContext.item4    = []                  #附加项4
                TradeContext.item5    = []                  #附加项5
                TradeContext.item6    = []                  #附加项6
                TradeContext.billserno= []                  #发票序号
                TradeContext.serialno = []                  #中间业务流水号
                TradeContext.prtnum   = []                  #打印次数
                TradeContext.paydate  = []                  #支付日期

                if ( int(Party3Context.billNum) == 1 ):
                    #打包(一张发票)
                        TradeContext.billData   = Party3Context.billData
                        TradeContext.item1      = Party3Context.item1
                        TradeContext.item2      = Party3Context.item2
                        TradeContext.item3      = Party3Context.item3
                        TradeContext.item4      = Party3Context.item4
                        TradeContext.item5      = Party3Context.item5
                        TradeContext.item6      = Party3Context.item6
                        TradeContext.billserno  = Party3Context.billserno
                        TradeContext.serialno   = Party3Context.serialno
                        TradeContext.prtnum     = Party3Context.prtnum
                        TradeContext.paydate    = Party3Context.paydate
                else:
                    #打包(多张发票)
                    for i in range( 0, int(Party3Context.billNum) ):
                        TradeContext.billData.append(Party3Context.billData[i])
                        TradeContext.item1.append(Party3Context.item1[i])
                        TradeContext.item2.append(Party3Context.item2[i])
                        TradeContext.item3.append(Party3Context.item3[i])
                        TradeContext.item4.append(Party3Context.item4[i])
                        TradeContext.item5.append(Party3Context.item5[i])
                        TradeContext.item6.append(Party3Context.item6[i])
                        TradeContext.billserno.append(Party3Context.billserno[i])
                        TradeContext.serialno.append(Party3Context.serialno[i])
                        TradeContext.prtnum.append(Party3Context.prtnum[i])
                        TradeContext.paydate.append(Party3Context.paydate[i])
            else:
                MxFileName = os.environ['AFAP_HOME'] + '/tmp/MX' + TradeContext.zoneno + TradeContext.brno + TradeContext.tellerno + '.TXT'
                AfaLoggerFunc.tradeInfo('>>>明细文件:['+MxFileName+']')

                if (os.path.exists(MxFileName) and os.path.isfile(MxFileName)):
                    #文件存在,先删除-再创建
                    os.system("rm " + MxFileName)

                #创建明细文件
                sfp = open(MxFileName, "w")

                if ( int(Party3Context.billNum) == 1 ):
                    #打包(一张发票)
                        wBuffer = ""
                        wBuffer = wBuffer + Party3Context.billData
                        wBuffer = wBuffer + Party3Context.item1
                        wBuffer = wBuffer + Party3Context.item2
                        wBuffer = wBuffer + Party3Context.item3
                        wBuffer = wBuffer + Party3Context.item4
                        wBuffer = wBuffer + Party3Context.item5
                        wBuffer = wBuffer + Party3Context.item6
                        wBuffer = wBuffer + Party3Context.billserno
                        wBuffer = wBuffer + Party3Context.serialno
                        wBuffer = wBuffer + Party3Context.prtnum
                        wBuffer = wBuffer + Party3Context.paydate
                        sfp.write(wBuffer + '\n')
                        sfp.close()
                else:
                    #打包(多张发票)
                    for i in range( 0, int(Party3Context.billNum) ):
                        wBuffer = ""
                        wBuffer = wBuffer + Party3Context.billData[i]
                        wBuffer = wBuffer + Party3Context.item1[i]
                        wBuffer = wBuffer + Party3Context.item2[i]
                        wBuffer = wBuffer + Party3Context.item3[i]
                        wBuffer = wBuffer + Party3Context.item4[i]
                        wBuffer = wBuffer + Party3Context.item5[i]
                        wBuffer = wBuffer + Party3Context.item6[i]
                        wBuffer = wBuffer + Party3Context.billserno[i]
                        wBuffer = wBuffer + Party3Context.serialno[i]
                        wBuffer = wBuffer + Party3Context.prtnum[i]
                        wBuffer = wBuffer + Party3Context.paydate[i]
                        sfp.write(wBuffer + '\n')
                    sfp.close()

            #=====================外调接口(后处理)==================================
            if ( subModuleExistFlag==1 ) :
                if not subModuleHandle.SubModuleDoSnd():
                    raise AfaFlowControl.flowException( )

        #=====================自动打包==========================================
        TradeContext.errorCode = '0000'
        TradeContext.errorMsg  = '交易成功'
        AfaFunc.autoPackData()

        #=====================程序退出==========================================
        AfaLoggerFunc.tradeInfo('******代收代付.补打发票模板[' + TradeContext.TemplateCode + ']退出******' )

    except AfaFlowControl.flowException, e:
        AfaFlowControl.exitMainFlow( str(e) )

    except Exception, e:
        AfaFlowControl.exitMainFlow( str(e) )
