# -*- coding: gbk -*-
##################################################################
#   代收代付平台.交易发票表操作类
#=================================================================
#   程序文件:   TransBillFunc.py
#   修改时间:   2006-03-31
##################################################################
import TradeContext, TradeFunc, AfaLoggerFunc, sys, AfaDBFunc

################################################################################
# 函数名:    InsertBill
# 参数:      billData       发票数据
#            billData       数据类型必须为list
#            billData[0]    发票张数
#            billData[1]    发票表中列item1的数据
#                           如果billData[0]==1,即只有一张发票，billData[1]可以为String型变量
#                           如果billData[0]>1,即一笔交易有多张发票，且发票表item1中必须插入数据，
#                           例如说，item1表示帐期，每张发票的帐期都不相同，那么billData[1]应为list，
#                           如果每张发票的帐期都相同，billData[1]可以为String
#                           如果item1列未使用，billData[1]应为''
#                           当billData[1]为list时
#                           billData[1][j]中存储的是第j张发票的对应item1的信息
#                           billData[1][j]应为String型
#           billData[2]     发票表中列item2的数据，说明与billData[1]类似
#           billData[3]     发票表中列item3的数据，说明与billData[1]类似
#           billData[4]     发票表中列item4的数据，说明与billData[1]类似
#           billData[5]     发票表中列item5的数据，说明与billData[1]类似
#           billData[6]     发票表中列item6的数据，说明与billData[1]类似
#           billData[7]     发票表中列billData的数据，说明与billData[1]类似
# 返回值：    True  插入发票表成功    False 插入发票表失败
# 函数说明：  将发票信息插入发票表，可一次插入一张或者多张发票信息
################################################################################
def InsertBill( billData ):

    AfaLoggerFunc.tradeInfo( '>>>插入发票信息[begin]' )

    # count 发票表的列数-1
    if( int( TradeContext.__billSaveCtl__ ) == 0 ):
            return True

    if( billData is None or ( type( billData ) is not list and type( billData ) is not tuple ) or len( billData )<8 ):
           TradeContext.errorCode, TradeContext.errorMsg='A0040', '发票数据异常'
           return False

    count=17
    BillDtl=[[]]*( count+1 )
    BillDtl[0] = TradeContext.agentSerialno             # SERIALNO      代理业务流水号
    BillDtl[1] = TradeContext.sysId                     # APPNO         业务编码  
    BillDtl[2] = TradeContext.unitno                    # BUSINO        单位编码
    
    if( TradeContext.existVariable( "subUnitno" ) ):
        BillDtl[3] = TradeContext.subUnitno             # SUBUNITNO     子单位代码
    else:
        BillDtl[3] = ''

    BillDtl[4] = TradeContext.workDate                  # WORKDATE      交易日期 yyyymmdd
    BillDtl[5] = TradeContext.workTime                  # WORKTIME      交易时间  
    BillDtl[6] = TradeContext.userno                    # USERNO        用户号 

    if( TradeContext.existVariable( "userName" ) ):
        BillDtl[7] = TradeContext.userName              # USERNAME      用户名称  
    else:
        BillDtl[7] = '' 

    BillDtl[8] = '0'                                    # BILLSTATUS    发票状态(0.正常 1.作废)
    BillDtl[9] = '0'                                    # PRTNUM        打印次数

    sql = "INSERT INTO AFA_BILLDTL(SERIALNO,SYSID,UNITNO,SUBUNITNO,WORKDATE,WORKTIME,USERNO,USERNAME,BILLSTATUS,PRTNUM,ITEM1,ITEM2,ITEM3,ITEM4,ITEM5,ITEM6,BILLSERNO,BILLDATA) VALUES("

    #发票数量
    billCount=int( billData[0] )
    if ( billCount < 1 ):
        TradeContext.errorCode, TradeContext.errorMsg='A0038', '发票张数错误'
        return False

    try:
        for i in range( 0, billCount ):
            for j in range( 1, 8 ):
                if( type( billData[j] ) is str ):
                    BillDtl[9+j] = billData[j]

                elif( type( billData[j] ) is list or type( billData[j] ) is tuple ):
                    BillDtl[9+j] = billData[j][i]
                    
                else:
                    BillDtl[9+j]=''

            BillDtl[count]=str( i + 1 )

            sql1 = sql

            for k in range( 0, count ):
                sql1=sql1+ "'"+ BillDtl[k]+"',"  
                
            sql1=sql1+"'"+BillDtl[count]+"')"

            AfaLoggerFunc.tradeInfo( sql1 )

            if( AfaDBFunc.InsertSql( sql1 ) < 1 ):
                
                AfaDBFunc.RollbackSql( )

                TradeContext.errorCode, TradeContext.errorMsg='A0039', '插入发票表失败' + AfaDBFunc.sqlErrMsg
                return False

        AfaDBFunc.CommitSql( ) 

        AfaLoggerFunc.tradeInfo( '插入发票信息[end]' )

        return True 

    except Exception, e:
        AfaLoggerFunc.tradeFatal( e )

        TradeContext.errorCode, TradeContext.errorMsg='A0040', '发票数据异常'

        AfaDBFunc.RollbackSql( )

        return False  


################################################################################
# 函数名:    UpdateBill
# 参数:      whereClause 可以为空
# 返回值：    True  更新发票表成功    False 更新发票表失败
# 函数说明：  更新发票表,如果是反交易,将TradeContext.preAgentSerno原交易流水对应的发票信息更新为作废状态
#           如果是补打发票将whereClause指定的发票记录的打印次数加1
################################################################################
def UpdateBill( ):

    AfaLoggerFunc.tradeInfo( '>>>更新发票信息[begin]' )
        
    if( TradeContext.existVariable( "revTranF" ) and TradeContext.revTranF == '1' ):
        
        if( int( TradeContext.__billSaveCtl__ ) == 0 ):
            return True

        sql="UPDATE AFA_BILLDTL SET BILLSTATUS='1' WHERE WORKDATE='" + TradeContext.workDate + "' AND SERIALNO='" + TradeContext.preAgentSerno + "'"

    else:

        #判断修改发票条件
        if( not TradeContext.existVariable( "whereClause" ) ):
            TradeContext.errorCode, TradeContext.errorMsg='A0041', '入口参数条件非法，入口参数不能为空'
            return False

            
        #补打发票时使用
        if( TradeContext.whereClause == '' ):
            TradeContext.errorCode, TradeContext.errorMsg='A0041', '入口参数条件不符，入口参数不能为空'
            return False

        sql="UPDATE AFA_BILLDTL SET PRTNUM=char(int(PRTNUM)+1) WHERE " + whereClause

    AfaLoggerFunc.tradeInfo( sql )

    if( AfaDBFunc.UpdateSqlCmt( sql ) < 1 ):
        
        TradeContext.errorCode, TradeContext.errorMsg='A0042', '更新发票信息表失败'+AfaDBFunc.sqlErrMsg
        
        return False

    AfaLoggerFunc.tradeInfo( '>>>更新发票信息[end]' )
    
    return True
