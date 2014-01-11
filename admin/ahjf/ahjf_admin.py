# -*- coding: gbk -*-
###############################################################################
# 文件名称：ahjf_admin.py
# 摘    要：安徽交罚项目对账
# 当前版本：1.0
# 作    者：
# 完成日期：2011年01月21日
###############################################################################
import TradeContext

TradeContext.sysType = 'ahjf'

import ConfigParser, sys, AfaDBFunc, os,HostContext,AfaUtilTools,AfaAdminFunc
from types import *



##########################################对帐处理##########################################
def SendToCorp(sysId,unitNo,trxDate):

    try:
        #银行交易流水，银行交易日期,银行交易时间，银行网点编码,银行网点操作员，财政区划，业务类型，交易渠道，交款日期,处罚决定书编号，
        #交款书号,付款人名字，付款人账号，付款人银行，罚款金额，滞纳金，总金额
        sqlStr = "SELECT agentserialno,workDate,workTime,brno,tellerno,note1,agentflag,channelcode,note7,userno,note3,username,"
        sqlStr = sqlStr + "draccno,note6,note4,note5,amount from afa_maintransdtl where "
        sqlStr = sqlStr + " SYSID = '"        + sysId    + "'"
        sqlStr = sqlStr + " AND UNITNO = '"   + unitNo   + "'"
        sqlStr = sqlStr + " AND WORKDATE='"   + trxDate  + "'"
        sqlStr = sqlStr + " and revtranf = '0' and bankstatus = '0' and ChkFlag = '0'"

        AfaAdminFunc.WrtLog(sqlStr)

        records = AfaDBFunc.SelectSql( sqlStr )
        if (records==None):
            AfaAdminFunc.WrtLog('>>>处理结果:生成对帐处理失败,数据库异常')
            return False

        if (len(records)==0):
            AfaAdminFunc.WrtLog('>>>处理结果:没有任何流水信息,不需要与企业进行对帐,请科技人员确定')
            return False


        #创建交换文件
        localFileName = 'DOC_012' + '_' + trxDate + '_' + TradeContext.workTime  + '.txt'

        AfaAdminFunc.WrtLog(localFileName)

        dzfp= open(TradeContext.CORP_LDIR + '/' + localFileName,  "w")
        
        totalnum = 0
        totalamt = 0
        
        chuFaLeiBie = ''
        for i in range(0, len(records)):
            tmpStr = ""
            #银行交易流水
            tmpStr = tmpStr + records[i][0].strip() +  chr(05)
            #银行交易日期
            tmpStr = tmpStr + records[i][1].strip() +  chr(05)
            #银行交易时间
            tmpStr = tmpStr + records[i][2].strip() +  chr(05)
            #银行网点编码
            tmpStr = tmpStr + records[i][3].strip() +  chr(05)
            #银行网点操作员
            tmpStr = tmpStr + records[i][4].strip() +  chr(05)
            #财政区划
            tmpStr = tmpStr + records[i][5].strip() +  chr(05)
            #业务类型
            #tmpStr = tmpStr + records[i][6].strip() +  chr(05)
            tmpStr = tmpStr + '00' +  chr(05)
            #交易渠道
            #tmpStr = tmpStr + records[i][7].strip() +  chr(05)
            tmpStr = tmpStr + '00' +  chr(05) 
            #交款日期
            tmpStr = tmpStr + records[i][8].strip() +  chr(05)
            #处罚决定书编号
            tmpStr = tmpStr + records[i][9].strip() +  chr(05)
            #交款书号
            #tmpStr = tmpStr + records[i][10].strip() +  chr(05)
            tmpStr = tmpStr + '' +  chr(05)
            #付款人名字
            tmpStr = tmpStr + records[i][11].strip() +  chr(05)
            #付款人账号
            tmpStr = tmpStr + records[i][12].strip() +  chr(05)
            #付款人银行
            tmpStr = tmpStr + records[i][13].strip() +  chr(05)
            #罚款金额
            tmpStr = tmpStr + records[i][14].strip() +  chr(05)
            #滞纳金
            tmpStr = tmpStr + records[i][15].strip() +  chr(05)
            #总金额
            tmpStr = tmpStr + records[i][16].strip() +  chr(05)
            tmpStr = tmpStr +"\n"
            dzfp.write(tmpStr)

            totalnum = totalnum + 1
            totalamt = totalamt + (float)(records[i][16].strip())

        dzfp.close()

        sqlStr = "update afa_maintransdtl set corpchkflag = '0' where "
        sqlStr = sqlStr + " SYSID       ='"     +  sysId   +"'"
        sqlStr = sqlStr + " AND WORKDATE='"     + trxDate  + "'"
        sqlStr = sqlStr + " and revtranf = '0' and bankstatus = '0' and ChkFlag = '0'"
        
        AfaAdminFunc.WrtLog(sqlStr)
        
        if not AfaDBFunc.UpdateSqlCmt(sqlStr):
            AfaAdminFunc.WrtLog('>>>处理结果:更新企业对账标识失败')
            return False

        AfaAdminFunc.WrtLog('>>>处理结果:对帐处理成功[总笔数='+str(totalnum) + ',总金额=' + str(totalamt) + ']')
        
       
        #文件字节长度
        TradeContext.DZFILESIZE = str(os.path.getsize(TradeContext.CORP_LDIR + '/' + localFileName))
        #对帐文件名
        rfileName = 'DOC_012' + '_' + trxDate + '_' + TradeContext.workTime + '_' + TradeContext.DZFILESIZE + '.txt'

        #总笔数
        TradeContext.DZNUM = str(totalnum)

        #总金额
        TradeContext.DZAMT = str(totalamt)
        
        if not AfaAdminFunc.PutDzFile(sysId, localFileName, rfileName):
            return False

        return True

    except Exception, e:
        AfaAdminFunc.WrtLog(str(e))
        AfaAdminFunc.WrtLog('对帐处理异常')
        return False
        
###########################################主函数###########################################
if __name__=='__main__':

    AfaAdminFunc.WrtLog( '**********安徽交罚对账操作开始**********' )
    
    TradeContext.workTime=AfaUtilTools.GetSysTime( )
    
    if ( len(sys.argv) in (3,4)):
    
        sSysId1     = sys.argv[1]          #业务代码
        sUnitno1    = sys.argv[2]          #公司代码
        if ( len(sys.argv) == 3 ):
            #sTrxDate = '20110704'
            sTrxDate = AfaUtilTools.GetSysDate( ) 
        else:
            sTrxDate = sys.argv[3]          #对账日期
        
        if ( sSysId1 == 'AG2017' ):
            AfaAdminFunc.WrtLog('>>>安徽交罚对帐开始') 
        
        else:
            AfaAdminFunc.WrtLog('>>>无此业务类型，请检查参数') 
            sys.exit(-1)
            
        AfaAdminFunc.WrtLog('系统编码 = ' + sSysId1)
        AfaAdminFunc.WrtLog('单位编码 = ' + sUnitno1)
        AfaAdminFunc.WrtLog('对账日期 = ' + sTrxDate)
            
        #读取配置文件
        if ( not AfaAdminFunc.GetAdminConfig(sSysId1 + "_AHJF") ) :
            AfaAdminFunc.WrtLog('>>>读取配置文件失败') 
            sys.exit(-1)
        
        #与主机对账
        AfaAdminFunc.WrtLog('>>>与主机对帐开始')
        if not AfaAdminFunc.MatchData(sSysId1,sUnitno1,sTrxDate):
            AfaAdminFunc.WrtLog('>>>与主机对账失败，程序中止') 
            sys.exit(-1)
        AfaAdminFunc.WrtLog('>>>与主机对帐结束')
        
        #与企业对账
        AfaAdminFunc.WrtLog('>>>与企业对帐对账开始')
        if not SendToCorp(sSysId1,sUnitno1,sTrxDate):
            AfaAdminFunc.WrtLog('>>>与企业对账失败，程序中止')
            sys.exit(-1)
        AfaAdminFunc.WrtLog('>>>与企业对帐对账结束')
        
        
    else:
        print( '用法1: jtfk_Proc sysid1 unitno1 date')
        sys.exit(-1)

    AfaAdminFunc.WrtLog( '**********安徽交罚对账操作结束**********' )

    sys.exit(0)
