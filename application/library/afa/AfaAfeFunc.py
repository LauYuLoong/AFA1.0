# -*- coding: gbk -*-
##################################################################
#   中间业务平台.与AFE通讯函数
#=================================================================
#   程序文件:   AfaAfeFunc.py
#   修改时间:   2006-03-31
##################################################################
import TradeContext, AfaFunc, Party3Context, AfapComm,AfaLoggerFunc
import os

#=======================读取AFE配置,根据应用代码区分不同的端口==================
def GetAfeConfigure( ):
    
    afeConf=os.environ['AFAP_HOME'] + '/conf/afe.conf'
    
    result=AfaFunc.GetConfigInfo( afeConf, TradeContext.sysId )
    
    return result



#=======================与AFE通讯===============================================
def CommAfeAutoPack( names='' ):
    
    AfaLoggerFunc.tradeInfo( '>>>进入CommAfeAutoPack(与通讯前置通讯的打包方法)')
    
    #判断是否使用了保留字段
    if( TradeContext.existVariable( 'reserve' ) ):
        AfapComm.setHead( TradeContext.TransCode, TradeContext.TemplateCode, TradeContext.reserve )
    else:
        AfapComm.setHead( TradeContext.TransCode, TradeContext.TemplateCode, '0000' )


    #是否通过文件配置的方式读取字段
    if( names == '' ):
        names = TradeContext.getNames( )


    #数据自动打包
    for name in names:
        value = getattr( TradeContext, name )
        if ( not name.startswith( '__' ) ) :
            if( type( value ) is str ) :
                AfapComm.addField( name, value )

            elif( type( value ) is list ) :
                for elem in value:
                    if type(elem) is not str :
                        AfaLoggerFunc.tradeInfo('CommAfeAutoPack  [value is not sting]'+'['+name+']')
                        continue
                    AfapComm.addField( name, elem)

    #读取AFE配置文件
    afeConf=GetAfeConfigure( )
        
    AfaLoggerFunc.tradeInfo(">>>AFE配置文件"+"   ".join(afeConf))
    if( not afeConf ):
        TradeContext.errorCode = 'A0001'
        TradeContext.errorMsg  = 'AFE配置文件不存在或者配置信息不存在'
        TradeContext.__status__= '1'
        TradeContext.tradeResponse = [[ 'errorCode', TradeContext.errorCode ], [ 'errorMsg', TradeContext.errorMsg]]
        AfaLoggerFunc.tradeInfo('配置文件错'+TradeContext.errorCode+TradeContext.errorMsg)
        return False



    #与AFE通讯,交换数据
    result = AfapComm.sendRequest( afeConf[0], int( afeConf[1] ), int( afeConf[2] ) )
        
    ret=result[0]
    if( ret != 0 ):        
        TradeContext.errorCode = str( ret )
        if( ret == -3 ):
            #接收数据失败,判作异常情况处理
            TradeContext.__status__='2'
            TradeContext.errorMsg = '接收响应数据失败'
            
        else:
            TradeContext.__status__='1'
            if( ret == -1 ):
                TradeContext.errorMsg = '连接服务器失败'

            elif( ret == -2 ):
                TradeContext.errorMsg = '连接服务器失败'
                
            elif( ret == -4 ):
                TradeContext.errorMsg = '设置Party3Context中数据失败'
                
            else:
                TradeContext.errorMsg = '与AFE通讯错误,未知错误类型'

        TradeContext.tradeResponse = [[ 'errorCode', TradeContext.errorCode ], [ 'errorMsg', TradeContext.errorMsg]]
            
        return False
    
    #分析返回信息
    return AfeParseRet( )


#=======================与通讯前置进行数据交换===============================================
def CommAfe( ):

    AfaLoggerFunc.tradeInfo('>>>与通讯前置进行数据交换')

    TradeContext.errorCode = 'C999'
    TradeContext.errorMsg  = '系统异常(与第三方通讯)'

    return CommAfeAutoPack( )


#分析通讯前置返回信息   
def AfeParseRet( ):
    
    #========================数据转储======================
    if( Party3Context.existVariable( "afe_appendFlag" ) ):
        TradeContext.afe_appendFlag  = Party3Context.afe_appendFlag

    if( Party3Context.existVariable( "afe_appendData1" ) ):
        TradeContext.afe_appendData1  = Party3Context.afe_appendData1

    if( Party3Context.existVariable( "afe_appendData2" ) ):
        TradeContext.afe_appendData2  = Party3Context.afe_appendData2

    if( Party3Context.existVariable( "afe_billData" ) ):
        TradeContext.billData   = Party3Context.afe_billData

    if( Party3Context.existVariable( "afe_corpSerno" ) ):
        TradeContext.corpSerno  = Party3Context.afe_corpSerno

    if( Party3Context.existVariable( "afe_corpTime" ) ):
        TradeContext.corpTime   = Party3Context.afe_corpTime

    if( Party3Context.existVariable( "afe_unitno" ) ):
        TradeContext.unitno     = Party3Context.afe_unitno

    if( Party3Context.existVariable( "afe_note1" ) ):
        TradeContext.note1      = Party3Context.afe_note1

    if( Party3Context.existVariable( "afe_note2" ) ):
        TradeContext.note2      = Party3Context.afe_note2

    if( Party3Context.existVariable( "afe_note3" ) ):
        TradeContext.note3      = Party3Context.afe_note3

    if( Party3Context.existVariable( "afe_note4" ) ):
        TradeContext.note4      = Party3Context.afe_note4

    if( Party3Context.existVariable( "afe_note5" ) ):
        TradeContext.note5      = Party3Context.afe_note5

    if( Party3Context.existVariable( "afe_note6" ) ):
        TradeContext.note6      = Party3Context.afe_note6

    if( Party3Context.existVariable( "afe_note7" ) ):
        TradeContext.note7      = Party3Context.afe_note7

    if( Party3Context.existVariable( "afe_note8" ) ):
        TradeContext.note8      = Party3Context.afe_note8

    if( Party3Context.existVariable( "afe_note9" ) ):
        TradeContext.note9      = Party3Context.afe_note9

    if( Party3Context.existVariable( "afe_note10" ) ):
        TradeContext.note10     = Party3Context.afe_note10


    # 要求AFE返回错误代表errorCode,无论是正常流程还是错误流程
    if( not Party3Context.existVariable( 'errorCode' ) ):
        TradeContext.errorCode='A0001'
        TradeContext.errorMsg ='第三方返回码[errorCode]不存在'
        TradeContext.__status__='1'
        TradeContext.tradeResponse = [[ 'errorCode', TradeContext.errorCode ], [ 'errorMsg', TradeContext.errorMsg]]
        return False


    #判断是否使用返回码转换
    if TradeContext.sysId != 'RCC01' and TradeContext.__respFlag__=='1' :
        # AFE返回错误情况

        #默认为异常状态
        TradeContext.__status__='2'
        
        #返回码转换
        result = AfaFunc.GetRespMsg(Party3Context.errorCode)
        if not result :
            return False

        if TradeContext.errorCode == '0000':
            TradeContext.__status__='0'
            return True

        else:
            if TradeContext.errorCode != '9999':
                TradeContext.__status__='1'
            else:
                TradeContext.__status__='2'

            return False
    else:
    
        # AFE返回错误情况
        if( Party3Context.errorCode != '0000' ):
            
            if Party3Context.errorCode != '9999':
                TradeContext.__status__='1'
            else:
                TradeContext.__status__='2'

            TradeContext.errorCode=Party3Context.errorCode

            if( Party3Context.existVariable( 'errorMsg' ) ):
                TradeContext.errorMsg =Party3Context.errorMsg          
            else:
                TradeContext.errorMsg ='与第三方通讯失败，错误未知'

            return False
            
        # 成功返回
        TradeContext.__status__='0'
        TradeContext.errorCode ='0000'
        TradeContext.errorMsg  ='与第三方通讯成功'
        return True
