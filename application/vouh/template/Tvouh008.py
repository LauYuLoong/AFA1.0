# -*- coding: gbk -*-
###################################################################
#    文    件:    Tvouh006.py
#    说    明:    分行特色空白重要凭证管理-->凭证中心参数维护
#    环    境:    中间业务新平台（AFA）--- UNIX: AIX 5.3
#    作    者:    孙国强
#    公    司:    北京赞同科技
#    创建地址:    广东发展银行总行
#    创建时间:    2007年2月28日 星期三
#    维护纪录:
##################################################################
import TradeContext, AfaLoggerFunc, AfaUtilTools, AfaFunc, AfaFlowControl, AfaDBFunc
from types import *
import AfaLoggerFunc,VouhFunc,binascii

#=============返回错误码,错误信息===================================
def tradeExit( code, msg ):
    TradeContext.errorCode, TradeContext.errorMsg=code, msg
    if code != '0000':
        return False
    return True

def main():
    AfaLoggerFunc.tradeInfo( '凭证中心参数维护['+TradeContext.TemplateCode+']进入' )
    #AfaLoggerFunc.afa_InitComp('Tvouh008','凭证中心参数维护')

    try:
        #===========检查操作类型是否存在===========
        # 1 新增,2 查询, 3 修改, 4 删除
        if( not TradeContext.existVariable( "opeType" ) ):
            tradeExit( 'A005060', '操作类型[opeType]值不存在!' )
            raise AfaFlowControl.flowException( )

        if TradeContext.opeType == '1': #新增
            #==========检查该凭证种类信息是否已经存在============
            sqlStr = "select VOUHTYPE from VOUH_PARAMETER \
                 where VOUHTYPE = '" + TradeContext.sVouhType+ "'\
                 and ZONENO = '" + TradeContext.sZoneNo+ "'"
            records = AfaDBFunc.SelectSql( sqlStr )
            if( records == None ):
                tradeExit( 'A005052', '查询[凭证参数维护表]操作异常!' )
                raise AfaFlowControl.flowException( )
            elif( len( records )!=0 ):
                tradeExit( 'A005053', '凭证种类已存在!' )
                raise AfaFlowControl.flowException( )

            #=============初始化返回报文变量====================
            TradeContext.tradeResponse=[]
            sqlStr = "INSERT INTO VOUH_PARAMETER (ZONENO,VOUHTYPE,VOUHNAME,CTRLFLG,COUNTFLG,COUNTUNIT,PAYFLG,\
            MOVFLG,SALEFLG,PRICE,HEADLEN,VOUHLEN,ACTIVEDATE) VALUES ('"+TradeContext.sZoneNo+"','"+\
            TradeContext.sVouhType+"','"+TradeContext.sVouhName+"','2','0','0','0','0','0','0','"+\
            TradeContext.sHeadLen+"','"+TradeContext.sVouhLen+"','0')"

            records = AfaDBFunc.InsertSqlCmt( sqlStr )
            if records==-1 :
                tradeExit( 'A005054', '新增[凭证号码表]基本信息失败!' )
                raise AfaFlowControl.flowException( )
            tradeExit('0000', '新建成功')

        if TradeContext.opeType == '4':  #删除
            sqlStr = "select * from VOUH_REGISTER \
                 where VOUHTYPE = '" + TradeContext.sVouhType+ "'\
                 and VOUHSTATUS != '8'"
            records = AfaDBFunc.SelectSql( sqlStr )
            AfaLoggerFunc.tradeDebug(sqlStr)
            if( records == None ):
                tradeExit( 'A005060', '查询[凭证登记表]操作异常!'  )
                raise AfaFlowControl.flowException( )
            elif( len( records ) > 0 ):
                tradeExit( 'A005061', '不能删除存在有效凭证的凭证参数!' )
                raise AfaFlowControl.flowException( )
            sqlStr = "DELETE  FROM  VOUH_PARAMETER WHERE VOUHTYPE = '" + TradeContext.sVouhType+ "'\
                 and ZONENO = '" + TradeContext.sZoneNo+ "'"

            AfaLoggerFunc.tradeDebug(sqlStr)
            records = AfaDBFunc.DeleteSqlCmt( sqlStr )
            if records == -1:
                tradeExit( 'A005055', '删除[凭证参数维护表]操作异常!' )
                raise AfaFlowControl.flowException( )
            if records == 0:
                tradeExit( 'A005056', '[凭证参数维护表]内无对应记录可被删除!' )
                raise AfaFlowControl.flowException( )
            tradeExit('0000', '删除成功')

        if TradeContext.opeType == '3':#修改
            #==============修改凭证参数维护表=====================

            sqlStr = "select * from VOUH_REGISTER \
                 where VOUHTYPE = '" + TradeContext.sVouhType+ "'\
                 and VOUHSTATUS != '8' and length(headstr) = " + TradeContext.sOldHeadLen
            records = AfaDBFunc.SelectSql( sqlStr )
            AfaLoggerFunc.tradeDebug(sqlStr)
            if( records == None ):
                tradeExit( 'A005060', '查询[凭证登记表]操作异常!'  )
                raise AfaFlowControl.flowException( )
            elif( len( records ) > 0 ):
                tradeExit( 'A005061', '不能修改存在有效凭证的凭证参数!' )
                raise AfaFlowControl.flowException( )


            sqlStr = "UPDATE VOUH_PARAMETER set \
              VOUHNAME = '"+ TradeContext.sVouhName + "',VOUHLEN = '"+ TradeContext.sVouhLen+ "',\
              HEADLEN = '"+ TradeContext.sHeadLen+ "'"
            sqlStr = sqlStr +" WHERE VOUHTYPE = '" + TradeContext.oldVOUHTYPE + "'\
            and ZONENO = '" + TradeContext.sZoneNo+ "'"

            records = AfaDBFunc.UpdateSqlCmt( sqlStr )
            if records==-1 :
                tradeExit( 'A005057', '更新[凭证参数维护表]信息异常!' )
                raise AfaFlowControl.flowException( )
            elif records==0 :
                tradeExit( 'A005058', '修改[凭证参数维护表]基本信息失败!' )
                raise AfaFlowControl.flowException( )
            tradeExit('0000', '修改成功')

        if TradeContext.opeType == '2':#查询
            #=============初始化返回报文变量====================
            TradeContext.tradeResponse=[]
            sqlStr = "SELECT VOUHTYPE,VOUHNAME,VOUHLEN,HEADLEN,ZONENO FROM VOUH_PARAMETER WHERE ZONENO = '"+ TradeContext.sZoneNo +"'"
            if (len(TradeContext.sVouhType)!=0):
                sqlStr = sqlStr + " AND VOUHTYPE = '" + TradeContext.sVouhType + "'"
            if (len(TradeContext.sVouhName)!=0):
                sqlStr = sqlStr + " AND VOUHNAME = '" + TradeContext.sVouhName + "'"
            if (len(TradeContext.sVouhType)==0 and len(TradeContext.sVouhName)==0 ):
                sqlStr = sqlStr
                
            #sqlStr="SELECT VOUHTYPE,VOUHNAME,VOUHLEN,HEADLEN,ZONENO FROM VOUH_PARAMETER WHERE ZONENO ='000000' AND VOUHTYPE = '0000002343' AND VOUHNAME = 'adfsadf'"
            AfaLoggerFunc.tradeInfo( 'sqlStr = ' + sqlStr )
            records = AfaDBFunc.SelectSql( sqlStr )
            if( records == None ):
                TradeContext.tradeResponse.append( ['retCount','0'] )
                tradeExit( 'A005052', '查询[凭证参数维护表]操作异常!'  )
                raise AfaFlowControl.flowException( )
            elif( len( records )==0 ):
                TradeContext.tradeResponse.append( ['retCount','0'] )
                tradeExit( 'A005059', '查询[凭证参数维护表]基本信息不存在!' )
                raise AfaFlowControl.flowException( )
            else:
                records=AfaUtilTools.ListFilterNone( records )
                baseInfoNames=['sVouhType','sVouhName','sVouhLen','sHeadLen','sZoneNo']
                total=len( records )
                for i in range( 0, len( records ) ):
                    j=0
                    for name in baseInfoNames:
                       TradeContext.tradeResponse.append( [name, records[i][j]] )
                       j=j+1
                TradeContext.tradeResponse.append( ['retCount', str( total )] )
                TradeContext.tradeResponse.append( ['errorCode', '0000'] )
                TradeContext.tradeResponse.append( ['errorMsg', '查询成功'] )
                tradeExit('0000', '查询成功')

        #自动打包
        AfaFunc.autoPackData()

        #=============程序退出=========================================
       # AfaLoggerFunc.afa_SuccQuit(__name__,'凭证中心参数维护交易')
    except AfaFlowControl.flowException, e:
        AfaFlowControl.exitMainFlow( )
    except AfaFlowControl.accException:
        AfaFlowControl.exitMainFlow( )
    except Exception, e:
        AfaFlowControl.exitMainFlow(str(e))