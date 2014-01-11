# -*- coding: gbk -*-
##################################################################
#   中间业务平台.
#=================================================================
#   程序文件:   4201_8430.py
#   程序说明:   [8430--6000112]新保保费试算
#   修改时间:   2009-04-07
##################################################################
import TradeContext, AfaLoggerFunc, AfaUtilTools, AfaFunc, Party3Context,AfaAfeFunc,AfaFlowControl,AfaAhAdb
import AfaHostFunc
from types import *

def SubModuleDoFst( ):

    #begin  20091120  蔡永贵  增加
    #校验保险公司代码和凭证种类是否合法
    if not AfaAhAdb.ADBCheckCert( ):
        return False
    #end

    AfaLoggerFunc.tradeInfo( '初始化交易变量' )
    #交易代码
    TradeContext.tradeCode = TradeContext.TransCode
    #用户编号/保险单号
    TradeContext.UserNo = TradeContext.CpicNo
    #地址
    if( TradeContext.existVariable( "Line" ) and len(TradeContext.Line.strip()) > 0):
        TradeContext.Address = TradeContext.Line
    #电话
    if( TradeContext.existVariable( "DialNum" ) and len(TradeContext.DialNum.strip()) > 0):
        TradeContext.TelePhone = TradeContext.DialNum
    #邮编
    if( TradeContext.existVariable( "Zip" ) and len(TradeContext.Zip.strip()) > 0):
        TradeContext.ZipCode = TradeContext.Zip
    #身份证号码
    TradeContext.IdCode = TradeContext.GovtID

    #受益人是否为法定标志
    #if( TradeContext.existVariable( "BenficType" ) ):
    #    if ( TradeContext.BenficType == "1"):
    #        TradeContext.BenficStr = "Y"
    #    else:
    #        TradeContext.BenficStr = "N"

    #AfaLoggerFunc.tradeDebug("BenficStr=[" + TradeContext.BenficStr + "]")

    #关彬捷 20091124 根据单位编码获取保险公司信息
    AfaAhAdb.ADBGetInfoByUnitno()
    
    #险种
    if( TradeContext.existVariable( "ProCode" ) ):
        if ( TradeContext.ProCode == '1'):
            #TradeContext.ProCodeStr = "EL5612"     #安贷宝B
            TradeContext.BenficStr = "N"           #第一受益人类型
            TradeContext.BenficName2 = "法定"      #第二受益人-法定
        elif ( TradeContext.ProCode == '2'):
            #TradeContext.ProCodeStr = "211610"     #华夏借款人意外伤害保险
            TradeContext.BenficStr = "Y"           #第一受益人类型
        else:
            TradeContext.BenficStr = ""

    AfaLoggerFunc.tradeDebug("BenficStr=[" + TradeContext.BenficStr + "]")
            

    return True
def SubModuleDoSnd():
    AfaLoggerFunc.tradeInfo('进入查询交易[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']与第三方通讯后处理' )
    try:
        Party3Context.unitno      = TradeContext.unitno
        Party3Context.ProCode = TradeContext.ProCode
        names = Party3Context.getNames( )
        for name in names:
            value = getattr( Party3Context, name )
            setattr( TradeContext, name, value )
            #AfaLoggerFunc.tradeInfo("字段名称  ["+str(name)+"] =  "+str(value))
        if( TradeContext.errorCode == '0000' ):
        #    if( TradeContext.existVariable( "ProCodeStr" ) ):
        #        if (TradeContext.ProCodeStr == "EL5601"):            
        #            TradeContext.ProCode = "0"                      #安贷宝A
        #        elif (TradeContext.ProCodeStr == "EL5602"):
        #            TradeContext.ProCode = "1"                      #安贷宝B
        #        elif (TradeContext.ProCodeStr == "211610"):
        #            TradeContext.ProCode = "2"                      #华夏借款人意外伤害保险
            if not AfaAhAdb.AdbInsertQueDtl( ):
                raise AfaFlowControl.accException()
        AfaLoggerFunc.tradeInfo('退出查询交易与第三方通讯后处理' )
        return True
        
    except AfaFlowControl.flowException, e:
        AfaFlowControl.exitMainFlow( str(e) )
        
    except AfaFlowControl.accException:
        AfaFlowControl.exitMainFlow( )
        
    except Exception, e:
        AfaFlowControl.exitMainFlow(str(e))
