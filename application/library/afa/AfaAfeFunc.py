# -*- coding: gbk -*-
##################################################################
#   �м�ҵ��ƽ̨.��AFEͨѶ����
#=================================================================
#   �����ļ�:   AfaAfeFunc.py
#   �޸�ʱ��:   2006-03-31
##################################################################
import TradeContext, AfaFunc, Party3Context, AfapComm,AfaLoggerFunc
import os

#=======================��ȡAFE����,����Ӧ�ô������ֲ�ͬ�Ķ˿�==================
def GetAfeConfigure( ):
    
    afeConf=os.environ['AFAP_HOME'] + '/conf/afe.conf'
    
    result=AfaFunc.GetConfigInfo( afeConf, TradeContext.sysId )
    
    return result



#=======================��AFEͨѶ===============================================
def CommAfeAutoPack( names='' ):
    
    AfaLoggerFunc.tradeInfo( '>>>����CommAfeAutoPack(��ͨѶǰ��ͨѶ�Ĵ������)')
    
    #�ж��Ƿ�ʹ���˱����ֶ�
    if( TradeContext.existVariable( 'reserve' ) ):
        AfapComm.setHead( TradeContext.TransCode, TradeContext.TemplateCode, TradeContext.reserve )
    else:
        AfapComm.setHead( TradeContext.TransCode, TradeContext.TemplateCode, '0000' )


    #�Ƿ�ͨ���ļ����õķ�ʽ��ȡ�ֶ�
    if( names == '' ):
        names = TradeContext.getNames( )


    #�����Զ����
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

    #��ȡAFE�����ļ�
    afeConf=GetAfeConfigure( )
        
    AfaLoggerFunc.tradeInfo(">>>AFE�����ļ�"+"   ".join(afeConf))
    if( not afeConf ):
        TradeContext.errorCode = 'A0001'
        TradeContext.errorMsg  = 'AFE�����ļ������ڻ���������Ϣ������'
        TradeContext.__status__= '1'
        TradeContext.tradeResponse = [[ 'errorCode', TradeContext.errorCode ], [ 'errorMsg', TradeContext.errorMsg]]
        AfaLoggerFunc.tradeInfo('�����ļ���'+TradeContext.errorCode+TradeContext.errorMsg)
        return False



    #��AFEͨѶ,��������
    result = AfapComm.sendRequest( afeConf[0], int( afeConf[1] ), int( afeConf[2] ) )
        
    ret=result[0]
    if( ret != 0 ):        
        TradeContext.errorCode = str( ret )
        if( ret == -3 ):
            #��������ʧ��,�����쳣�������
            TradeContext.__status__='2'
            TradeContext.errorMsg = '������Ӧ����ʧ��'
            
        else:
            TradeContext.__status__='1'
            if( ret == -1 ):
                TradeContext.errorMsg = '���ӷ�����ʧ��'

            elif( ret == -2 ):
                TradeContext.errorMsg = '���ӷ�����ʧ��'
                
            elif( ret == -4 ):
                TradeContext.errorMsg = '����Party3Context������ʧ��'
                
            else:
                TradeContext.errorMsg = '��AFEͨѶ����,δ֪��������'

        TradeContext.tradeResponse = [[ 'errorCode', TradeContext.errorCode ], [ 'errorMsg', TradeContext.errorMsg]]
            
        return False
    
    #����������Ϣ
    return AfeParseRet( )


#=======================��ͨѶǰ�ý������ݽ���===============================================
def CommAfe( ):

    AfaLoggerFunc.tradeInfo('>>>��ͨѶǰ�ý������ݽ���')

    TradeContext.errorCode = 'C999'
    TradeContext.errorMsg  = 'ϵͳ�쳣(�������ͨѶ)'

    return CommAfeAutoPack( )


#����ͨѶǰ�÷�����Ϣ   
def AfeParseRet( ):
    
    #========================����ת��======================
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


    # Ҫ��AFE���ش������errorCode,�������������̻��Ǵ�������
    if( not Party3Context.existVariable( 'errorCode' ) ):
        TradeContext.errorCode='A0001'
        TradeContext.errorMsg ='������������[errorCode]������'
        TradeContext.__status__='1'
        TradeContext.tradeResponse = [[ 'errorCode', TradeContext.errorCode ], [ 'errorMsg', TradeContext.errorMsg]]
        return False


    #�ж��Ƿ�ʹ�÷�����ת��
    if TradeContext.sysId != 'RCC01' and TradeContext.__respFlag__=='1' :
        # AFE���ش������

        #Ĭ��Ϊ�쳣״̬
        TradeContext.__status__='2'
        
        #������ת��
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
    
        # AFE���ش������
        if( Party3Context.errorCode != '0000' ):
            
            if Party3Context.errorCode != '9999':
                TradeContext.__status__='1'
            else:
                TradeContext.__status__='2'

            TradeContext.errorCode=Party3Context.errorCode

            if( Party3Context.existVariable( 'errorMsg' ) ):
                TradeContext.errorMsg =Party3Context.errorMsg          
            else:
                TradeContext.errorMsg ='�������ͨѶʧ�ܣ�����δ֪'

            return False
            
        # �ɹ�����
        TradeContext.__status__='0'
        TradeContext.errorCode ='0000'
        TradeContext.errorMsg  ='�������ͨѶ�ɹ�'
        return True
