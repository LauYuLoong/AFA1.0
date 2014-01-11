# -*- coding: gbk -*-
################################################################################
#   �м�ҵ��ƽ̨.����������
#===============================================================================
#   �����ļ�:   AfaFunc.py
#   �޸�ʱ��:   2006-09-26
################################################################################
import exceptions,TradeContext,AfaDBFunc,TradeException,AfaUtilTools,ConfigParser,Party3Context,AfaLoggerFunc,AfaFlowControl,os,time,socket,UtilTools
from types import *

#=======================����ָ���������ļ�,section����ȡ��Ӧ����================
def GetConfigInfo( configFileName = '', sectionName='' ):

    AfaLoggerFunc.tradeInfo( '>>>��ȡ������Ϣ' )

    result=[]
    try:
        config = ConfigParser.ConfigParser( )
        config.readfp( open( configFileName ) )
        tmpResult = config.options( sectionName )

        for i in range( 0, len( tmpResult ) ):
            result.append( config.get( sectionName, tmpResult[i] ) )

    except Exception, e:
        AfaLoggerFunc.tradeFatal( str(e) )
        return 0
        
    return result


#=======================��ȡƽ̨��ˮ��DB2=======================================
def GetSerialno( seqName="BUSI_ONLINE_SEQ" ):

    AfaLoggerFunc.tradeInfo( '��ȡƽ̨��ˮ��' )

    sqlStr = "SELECT NEXTVAL FOR " + seqName + " FROM SYSIBM.SYSDUMMY1"
    records = AfaDBFunc.SelectSql( sqlStr )
    if records == None :
        TradeContext.errorCode = 'A0025'
        TradeContext.errorMsg = AfaDBFunc.sqlErrMsg
        return -1

    #��"0"(8λ)
    TradeContext.agentSerialno=str( records[0][0] ).rjust( 8, '0' )

    return str( records[0][0] )



#=======================�ж�Ӧ��ϵͳ״̬========================================
def ChkSysStatus( ):


    AfaLoggerFunc.tradeInfo( '>>>�ж�Ӧ��ϵͳ״̬' )


    #=======================����ֵ����Ч��У��==========================
    if( not TradeContext.existVariable( "sysId" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', 'Ӧ��ϵͳ��ʶ[sysId]ֵ������!' )
    else:
        TradeContext.sysId=AfaUtilTools.Lfill( TradeContext.sysId, 6, '0' )
        
        
    #=======================���㼶����========================================
    #if(not GetBranchInfo(TradeContext.brno)):
    #    return False
    #else:
    #    if( int(TradeContext.__branchType__) != 3):
    #        return AfaFlowControl.ExitThisFlow( '0001', '��Ӫҵ���㣬���������˽���' )
    

    #=======================ϵͳ��ʶ============================================
    sqlStr = "SELECT * FROM AFA_SYSTEM WHERE SYSID = '" + TradeContext.sysId + "'"

    AfaLoggerFunc.tradeInfo( sqlStr )

    records = AfaDBFunc.SelectSql( sqlStr )
    if( records == None ):
        return AfaFlowControl.ExitThisFlow( 'A0002', 'Ӧ��ϵͳ״̬������쳣:'+AfaDBFunc.sqlErrMsg )

    elif( len( records )!=0 ):
        AfaUtilTools.ListFilterNone( records )

        #=======================�ж�ϵͳ״̬====================================
        if( records[0][5]=="0" ):
            return AfaFlowControl.ExitThisFlow( 'A0004', '��Ӧ��ϵͳ���ڹر�״̬,����������' )
                
        elif( records[0][5]=="2" ):
            return AfaFlowControl.ExitThisFlow( 'A0005', '��Ӧ��ϵͳ������ͣ״̬,����������' )
                
        elif( records[0][5]=="3" ):
            return AfaFlowControl.ExitThisFlow( 'A0005', '��Ӧ��ϵͳ����δ����״̬,����������' )

        #=======================����ȫ�ֱ���====================================

        #ϵͳӢ�ļ��
        TradeContext.sysEName = records[0][1]
        
        #ϵͳ��������
        TradeContext.sysCName = records[0][2]

        #ϵͳ����(0-����Ӧ�� 1-����Ӧ�� 2-֧��Ӧ��)
        TradeContext.__type__ = records[0][6]


        #���ʽ��׶��(�����Ϊ0ʱ��ʾ�����ƶ��)
        if(len(records[0][7])==0):
            TradeContext.__sysMaxAmount__ = '0'
        else:
            TradeContext.__sysMaxAmount__ = records[0][7]

        AfaLoggerFunc.tradeInfo( '::::::ϵͳ���ʶ��  =' + TradeContext.__sysMaxAmount__ )

        #���ۼƽ��׶��(�����Ϊ0ʱ��ʾ�����ƶ��)
        if(len(records[0][8])==0):
            TradeContext.__sysTotalamount__ = '0'
        else:
            TradeContext.__sysTotalamount__ = records[0][8]

        AfaLoggerFunc.tradeInfo( '::::::ϵͳ�ۼƶ��  =' + TradeContext.__sysTotalamount__ )

        #��齻�׶��(1-ϵͳ 2-����)
        if(not ChkAmtStatus('1')):
            return False
                
        #��������ģʽ(0-�����п��� 1-�����п��� 2-��֧�п���)
        TradeContext.__channelMode__ = records[0][9]
        AfaLoggerFunc.tradeInfo( '::::::��������ģʽ  =' + TradeContext.__channelMode__ )

        #�ɷѽ��ʹ���ģʽ(0-�����п��� 1-�����п��� 2-��֧�п���)
        TradeContext.__actnoMode__ = records[0][10]
        AfaLoggerFunc.tradeInfo( '::::::���ʹ���ģʽ  =' + TradeContext.__actnoMode__ )


        #��ȡժҪ����(�������ϵͳ��Ҫ)(Ĭ��=258)
        if( not GetSummaryInfo( ) ):
            return False
            
        return True
        
    else:
     
        return AfaFlowControl.ExitThisFlow( 'A0003', '��ϵͳ������Ϣ' )


#=======================�ж��̻�״̬============================================
def ChkUnitStatus( ):

    AfaLoggerFunc.tradeInfo( '>>>�жϵ�λ״̬' )
        
    #=======================����ֵ����Ч��У��==================================
    if( not TradeContext.existVariable( "unitno" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '��λ����[unitno]ֵ������!' )
            

    #=======================��λ��Ϣ============================================
    sqlStr = "SELECT * FROM AFA_UNITADM WHERE SYSID = '" + TradeContext.sysId + "' AND UNITNO = '" + TradeContext.unitno + "' "

    AfaLoggerFunc.tradeInfo( sqlStr )

    records = AfaDBFunc.SelectSql( sqlStr )
    if( records == None ):
        return AfaFlowControl.ExitThisFlow( 'A0002', '��λ��Ϣ������쳣:'+AfaDBFunc.sqlErrMsg )

    elif( len( records ) != 0 ):
        AfaUtilTools.ListFilterNone( records )

        #=======================����ȫ�ֱ���====================================

        #��λ����
        TradeContext.unitName = records[0][2]

        #��λ���
        TradeContext.unitSName = records[0][3]

        #=======================�жϵ�λ״̬====================================
        if( records[0][4]=="0" ):
            return AfaFlowControl.ExitThisFlow( 'A0004', '�õ�λ���ڹر�״̬,����������' )

        elif( records[0][4]=="2" ):
            return AfaFlowControl.ExitThisFlow( 'A0005', '�õ�λ������ͣ״̬,����������' )

        elif( records[0][4]=="3" ):
            return AfaFlowControl.ExitThisFlow( 'A0005', '�õ�λ����δ����״̬,����������' )


        #ҵ��ģʽ(0-�޷�֧���� 1-�з�֧����,ҵ��������̻���λ���� 2-�з�֧����,ҵ��������̻���֧��λ����
        TradeContext.__busiMode__ = records[0][5]
        AfaLoggerFunc.tradeInfo( '::::::ҵ��ģʽ  =' + TradeContext.__busiMode__ )

        
        #�˻�ģʽ(0-�޷��˻� 1-�з��˻�,�����̻����� 2-�з��˻�,���̻���֧��λ����)
        TradeContext.__accMode__ = records[0][6]
        AfaLoggerFunc.tradeInfo( '::::::�˻�ģʽ  =' + TradeContext.__accMode__ )

        
        #=======================ҵ��ģʽ========================================
        if( TradeContext.__busiMode__ != "2" ):
            
            #�жϷ���ʱ��
            if( len(records[0][12]) == 0 ):
                records[0][12]='000000'
                
            if( len(records[0][13]) == 0 ):
                records[0][13]='000000'

            if( long( TradeContext.workTime )<long( records[0][12] ) or long( TradeContext.workTime )>long( records[0][13] ) ):
                return AfaFlowControl.ExitThisFlow( 'A0007', "������ҵ�񿪷�ʱ��,����ÿ��["+records[0][12]+"->"+records[0][13]+"]����ҵ��" )


            #��ȡģʽ(0-���շ� 1-ģʽһ(����շ�) 2-ģʽ��(�����շ�))
            TradeContext.__feeFlag__ = records[0][14]
            AfaLoggerFunc.tradeInfo( '::::::������ȡģʽ  =' + TradeContext.__feeFlag__ )

            
            #���������(1-ǩ��У���־ 2-����У���־ 3-����У���־ 4-��Ӧ��ʹ�ñ�־ 5-�ӱ�ʹ�ñ�־ 6-��չģʽ 7-��Կʹ�ñ�־)
            TradeContext.__agentEigen__ = records[0][25]

            AfaLoggerFunc.tradeInfo( '::::::ǩ��У���־  =' + TradeContext.__agentEigen__[0] )
            AfaLoggerFunc.tradeInfo( '::::::����У���־  =' + TradeContext.__agentEigen__[1] )
            AfaLoggerFunc.tradeInfo( '::::::����У���־  =' + TradeContext.__agentEigen__[2] )
            AfaLoggerFunc.tradeInfo( '::::::��Ӧ��ʹ�ñ�־=' + TradeContext.__agentEigen__[3] )
            AfaLoggerFunc.tradeInfo( '::::::�ӱ�ʹ�ñ�־  =' + TradeContext.__agentEigen__[4] )
            AfaLoggerFunc.tradeInfo( '::::::��չģʽ      =' + TradeContext.__agentEigen__[5] )
            AfaLoggerFunc.tradeInfo( '::::::��Կʹ�ñ�־  =' + TradeContext.__agentEigen__[6] )
            
            #�ж��Ƿ���ǩ��ǩ�˽���
            if( not TradeContext.existVariable( "__signFlag__" ) ):
                
                #���ǩ����־
                if( TradeContext.__agentEigen__[0]=='1' and records[0][26]=="0" ):
                    return AfaFlowControl.ExitThisFlow( 'A0008', '�õ�λ��û��ǩ��,�������˽���' )

            else:
                if TradeContext.__signFlag__ == '1' :
                    
                    #ǩ��
                    return SignIn( )
                        
                else:
                
                    #ǩ��
                    return SignOut( )


            #������ձ�־(0-δ�� 1-����)
            if( TradeContext.__agentEigen__[1]=='1' and records[0][27]=="1" ):
                return AfaFlowControl.ExitThisFlow( 'A0009', '�õ�λ�������ղ���,�������˽���' )
                    
            #�����ʱ�־(0��δ�� 1-�Ѷ������� 2-���������ʳɹ� 3-����������ʧ��)
            if( TradeContext.__agentEigen__[2]=='1' and long(records[0][29])>=1 ):
                return AfaFlowControl.ExitThisFlow( 'A0010', '�õ�λ�������ʲ���,�������˽���' )


            #��Ӧ��ת����־
            TradeContext.__respFlag__ = TradeContext.__agentEigen__[3]


            #��Կʹ�ñ�־
            TradeContext.__keyFlag__ = TradeContext.__agentEigen__[6]


            #��Կʹ�ñ�־
            if ( TradeContext.__keyFlag__=='1' ):
                if( not GetKeyInfo( ) ):
                    return False

            #�շ�ʹ�ñ�־
            if ( TradeContext.__feeFlag__=='1' ):
                if( not GetFeeInfo( ) ):
                    return False
                    
        #=======================�˻�ģʽ========================================
        if( TradeContext.__accMode__ != "2" ):
            
            #�����̻�����(�̻���)
            TradeContext.bankUnitno = records[0][7]
            
            #������к�
            if(len(records[0][8])>0):
                TradeContext.mainZoneno = records[0][8]
                
            #���������
            if(len(records[0][9])>0):
                TradeContext.mainBrno = records[0][9]


            #���б���(�̻������з���ı���)
            TradeContext.bankno       = records[0][15]
            
            #��λ�˺�(accno1)
            TradeContext.__agentAccno__  = records[0][16]
            TradeContext.__agentAccno1__ = records[0][17]
            TradeContext.__agentAccno2__ = records[0][18]
            TradeContext.__agentAccno3__ = records[0][19]
            TradeContext.__agentAccno4__ = records[0][20]
            TradeContext.__agentAccno5__ = records[0][21]

        #=======================��֧����/���˻�=================================
        if(TradeContext.__busiMode__ == '2' or TradeContext.__accMode__ == '2' ):
            #�ж��̻���֧��λ��Ϣ״̬
            if( not ChkSubUnitStatus( ) ):
                return False

        else:
            if( not TradeContext.existVariable( "subUnitno" ) ):
                TradeContext.subUnitno='00000000'

        return True
        
    else:

        return AfaFlowControl.ExitThisFlow( 'A0003', '�޵�λ��Ϣ' )



#=======================�жϷ�֧��λ��Ϣ״̬====================================
def ChkSubUnitStatus( ):

    AfaLoggerFunc.tradeInfo( '>>>�ж��ӵ�λ��Ϣ״̬' )

    #=======================����ֵ����Ч��У��==================================
    if( not TradeContext.existVariable( "subUnitno" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '��֧��λ����[subUnitno]ֵ������!' )

    #=======================�ӵ�λ��Ϣ==========================================
    sqlStr = "SELECT * FROM AFA_SUBUNITADM WHERE SYSID = '" + TradeContext.sysId + "' AND UNITNO = '" + TradeContext.unitno + "' AND SUBUNITNO = '" + TradeContext.subUnitno + "' "

    AfaLoggerFunc.tradeInfo( sqlStr )

    subRecords = AfaDBFunc.SelectSql( sqlStr )
        
    if(subRecords == None ):
        return AfaFlowControl.ExitThisFlow( 'A0002', '�ӵ�λ��Ϣ������쳣:'+AfaDBFunc.sqlErrMsg )

    elif( len( subRecords )!=0 ):

        AfaUtilTools.ListFilterNone( subRecords )

        #��λ����
        TradeContext.subUnitName = subRecords[0][3]
        
        #��λ���
        TradeContext.subUnitSName = subRecords[0][4]

        #=======================ҵ��ģʽ========================================
        if(TradeContext.__busiMode__ == '2' ):
            
            #�жϷ�֧��λ״̬
            if( subRecords[0][5]=="0" ):
                return AfaFlowControl.ExitThisFlow( 'A0004', '���ӵ�λ���ڹر�״̬,����������' )
                    
            elif( subRecords[0][5]=="2" ):
                return AfaFlowControl.ExitThisFlow( 'A0005', '���ӵ�λ������ͣ״̬,����������' )
                    
            elif( subRecords[0][5]=="3" ):
                return AfaFlowControl.ExitThisFlow( 'A0005', '���ӵ�λ����δ����״̬,����������' )
                    
            #�жϷ���ʱ��
            if( len(subRecords[0][8])==0 ):
                subRecords[0][8]='000000'
                
            if( len(subRecords[0][9])==0 ):
                subRecords[0][9]='000000'

            if( long( TradeContext.workTime )<long( subRecords[0][8] ) or long( TradeContext.workTime )>long( subRecords[0][9] ) ):
                return AfaFlowControl.ExitThisFlow( 'A0007', "������ҵ�񿪷�ʱ��,����ÿ��["+subRecords[0][8]+"->"+subRecords[0][9]+"]����ҵ��" )


            #��ȡģʽ(0-���շ� 1-ģʽһ(����շ�) 2-ģʽ��(�����շ�))
            TradeContext.__feeFlag__ = subRecords[0][10]
            
            
            #���������(1-ǩ��У���־ 2-����У���־ 3-����У���־ 4-��Ӧ��ʹ�ñ�־ 5-�ӱ�ʹ�ñ�־ 6-��չģʽ 7-��Կʹ�ñ�־)
            TradeContext.__agentEigen__ = subRecords[0][24]

            AfaLoggerFunc.tradeInfo( '::::::ǩ��У���־  =' + TradeContext.__agentEigen__[0] )
            AfaLoggerFunc.tradeInfo( '::::::����У���־  =' + TradeContext.__agentEigen__[1] )
            AfaLoggerFunc.tradeInfo( '::::::����У���־  =' + TradeContext.__agentEigen__[2] )
            AfaLoggerFunc.tradeInfo( '::::::��Ӧ��ʹ�ñ�־=' + TradeContext.__agentEigen__[3] )
            AfaLoggerFunc.tradeInfo( '::::::�ӱ�ʹ�ñ�־  =' + TradeContext.__agentEigen__[4] )
            AfaLoggerFunc.tradeInfo( '::::::��չģʽ      =' + TradeContext.__agentEigen__[5] )
            AfaLoggerFunc.tradeInfo( '::::::��Կʹ�ñ�־  =' + TradeContext.__agentEigen__[6] )
            
            #�ж��Ƿ���ǩ��ǩ�˽���
            if( not TradeContext.existVariable( "__signFlag__" ) ):
                
                #���ǩ����־
                if( TradeContext.__agentEigen__[0]=='1' and subRecords[0][25]=="0" ):
                    return AfaFlowControl.ExitThisFlow( 'A0008', '���ӵ�λ��û��ǩ��,�������˽���' )
                        
            else:
                if TradeContext.__signFlag__ == '1' :
                    
                    #ǩ��
                    return SignIn( )
                        
                else:
                
                    #ǩ��
                    return SignOut( )
                        
                        
            #������ձ�־
            if( TradeContext.__agentEigen__[1]=='1' and subRecords[0][26]=="1" ):
                return AfaFlowControl.ExitThisFlow( 'A0009', '���ӵ�λ�������ղ���,�������˽���' )
                    
            #�����ʱ�־
            if( TradeContext.__agentEigen__[2]=='1' and subRecords[0][28]=="1" ):
                return AfaFlowControl.ExitThisFlow( 'A0010', '���ӵ�λ�������ʲ���,�������˽���' )
                    
            #��Ӧ��ת����־
            TradeContext.__respFlag__ = TradeContext.__agentEigen__[3]

            #��Կʹ�ñ�־
            TradeContext.__keyFlag__ = TradeContext.__agentEigen__[6]


            #��ȡ��Կʹ�ñ�־
            if ( TradeContext.__keyFlag__=='1' ):
                if( not GetKeyInfo( ) ):
                    return False


            #��ȡ�շ�ʹ�ñ�־
            if ( TradeContext.__feeFlag__=='1' ):
                if( not GetFeeInfo( ) ):
                    return False
                    
        #=======================�˻�ģʽ========================================
        if(TradeContext.__accMode__ == '2' ):
            
            #������к�
            if(len(subRecords[0][12])>0):
                TradeContext.mainZoneno = subRecords[0][12]
                
            #���������
            if(len(subRecords[0][13])>0):
                TradeContext.mainBrno = subRecords[0][13]
                
            #�̻�����(���и��̻�����ı���)
            TradeContext.bankUnitno = subRecords[0][14]

            #���б���(�̻������з���ı���)
            TradeContext.bankno = subRecords[0][11]

            #��λ�˺�
            TradeContext.__agentAccno__  = subRecords[0][15]
            TradeContext.__agentAccno1__ = subRecords[0][16]
            TradeContext.__agentAccno2__ = subRecords[0][17]
            TradeContext.__agentAccno3__ = subRecords[0][18]
            TradeContext.__agentAccno4__ = subRecords[0][19]
            TradeContext.__agentAccno5__ = subRecords[0][20]

        return True

    else:
        return AfaFlowControl.ExitThisFlow( 'A0002', '���ӵ�λ��Ϣ' )


#=======================Ӧ��ǩ��================================================
def SignIn( ):
    
    ret=SignMode( '1' )
        
    if( ret < 1 ):
        return AfaFlowControl.ExitThisFlow( 'A0052', 'ǩ��ʧ��' )
            
    return True


#=======================Ӧ��ǩ��================================================
def SignOut( ):

    ret=SignMode( '0' )
        
    if( ret < 1 ):
        return AfaFlowControl.ExitThisFlow( 'A0052', 'ǩ��ʧ��' )
            
    return True


#=======================Ӧ��ǩ��/��=============================================
def SignMode( flag ):
    
    if(TradeContext.__busiMode__ != '2'):
        sql="UPDATE AFA_UNITADM SET LOGINSTATUS='"    + flag + "' WHERE SYSID='" + TradeContext.sysId + "' AND UNITNO='" + TradeContext.unitno + "'"
        
    else:
        sql="UPDATE AFA_SUBUNITADM SET LOGINSTATUS='" + flag + "' WHERE SYSID='" + TradeContext.sysId + "' AND UNITNO='" + TradeContext.unitno + "' AND SUBUNITNO='" + TradeContext.subUnitno+"'"

    return AfaDBFunc.UpdateSqlCmt( sql )


#=======================�жϽ���״̬============================================
def ChkTradeStatus( ):

    AfaLoggerFunc.tradeInfo( '>>>�жϽ���״̬' )
        
    #=======================����ֵ����Ч��У��==================================
    if( not TradeContext.existVariable( "TransCode" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '���״���[TransCode]ֵ������!' )

    #ϵͳ��ʶ
    sqlStr = "SELECT * FROM AFA_TRADEADM WHERE SYSID='" + TradeContext.sysId

    #��λ����=
    sqlStr = sqlStr + "' AND UNITNO='" + TradeContext.unitno

    #ҵ��ģʽ
    if(TradeContext.__busiMode__ == '2' ):
        #�ӵ�λ����
        sqlStr = sqlStr + "' AND SUBUNITNO='" + TradeContext.subUnitno

    #���״���
    sqlStr = sqlStr + "' AND TRXCODE='" + TradeContext.TransCode + "'"

    #��������
    sqlStr = sqlStr + "' AND CHANNELCODE='" + TradeContext.channelCode + "' OR CHANNELCODE='" + "00000" + "'"

    #������
    sqlStr = sqlStr + "' AND ZONENO='"   + TradeContext.zoneno    + "' OR ZONENO='"   + "00000" + "'"

    #�����
    sqlStr = sqlStr + "' AND BRNO='"     + TradeContext.brno      + "' OR BRNO='"     + "00000" + "'"

    #��Ա��
    sqlStr = sqlStr + "' AND TELLERNO='" + TradeContext.tellerno  + "' OR TELLERNO='" + "00000" + "'"

    AfaLoggerFunc.tradeInfo( sqlStr )

    records = AfaDBFunc.SelectSql( sqlStr )
        
    if( records == None ):
        return AfaFlowControl.ExitThisFlow( 'A0002', '������Ϣ���������쳣:'+AfaDBFunc.sqlErrMsg )

    elif( len( records )!=0 ):
        AfaUtilTools.ListFilterNone( records )
        
        #�жϽ���״̬
        if( records[0][7]=="0" ):
            return AfaFlowControl.ExitThisFlow( 'A0004', '�ý��״���δ����״̬,�������˽���' )
                
        elif( records[0][7]=="2" ):
            return AfaFlowControl.ExitThisFlow( 'A0005', '�ý��״��ڹر�״̬,�������˽���' )

        elif( records[0][7]=="3" ):
            return AfaFlowControl.ExitThisFlow( 'A0006', '�ý��״���ͣ��״̬,�������˽���' )

        #�жϷ���ʱ��
        if( long( TradeContext.workTime )<long( records[0][5] ) or long( TradeContext.workTime )>long( records[0][6] ) ):
            return AfaFlowControl.ExitThisFlow( 'A0007', "�����ý��׿���ʱ��,����ÿ��["+records[0][5]+"->"+records[0][6]+"]����ҵ��" )

        return True

    else:
        return AfaFlowControl.ExitThisFlow( 'A0007', '�޴�Ȩ��,�������˽���' )


################################################################################
# ������:    ChkChannelStatus
# ����:      ��
# ����ֵ��    True  У��ɹ�    False У��ʧ��
# ����˵����  ��ѯ������Ϣ���ȡ������������Ϣ��һ��Ϊ��ѯ�ɷѻ���ȡ������ʹ��    
################################################################################
def ChkChannelStatus( ):

    AfaLoggerFunc.tradeInfo( '>>>�ж�����״̬' )
        
    #=======================����ֵ����Ч��У��==================================
    if( not TradeContext.existVariable( "channelCode" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '��������[channelCode]ֵ������!' )
            
    #ϵͳ��ʶ
    sqlStr = "SELECT * FROM AFA_CHANNELADM WHERE SYSID='" + TradeContext.sysId
    
    #��λ����
    sqlStr = sqlStr + "' AND UNITNO='" + TradeContext.unitno
    
    #ҵ��ģʽ
    if(TradeContext.__busiMode__ == '2' ):
        
        #�ӵ�λ����
        sqlStr = sqlStr + "' AND SUBUNITNO='" + TradeContext.subUnitno
        
    #ҵ��ʽ
    sqlStr = sqlStr + "' AND AGENTFLAG='" + TradeContext.agentFlag

    #ҵ�������
    if(TradeContext.__channelMode__ == '0' ):
        sqlStr = sqlStr + "' AND ZONENO='" + '00000'
    else:
        sqlStr = sqlStr + "' AND ZONENO='" + TradeContext.zoneno

        if(TradeContext.__channelMode__ == '2' ):

            #ҵ��֧�к�
            sqlStr = sqlStr + "' AND ZHNO='" + TradeContext.zhno

    #��������
    sqlStr = sqlStr + "' AND CHANNELCODE='" + TradeContext.channelCode + "'"

    AfaLoggerFunc.tradeInfo( sqlStr )

    records = AfaDBFunc.SelectSql( sqlStr )
    if( records == None ):
        return AfaFlowControl.ExitThisFlow( 'A0002', '������Ϣ������쳣:'+AfaDBFunc.sqlErrMsg )

    elif( len( records )!=0 ):
        AfaUtilTools.ListFilterNone( records )

        #=======================�ж�ҵ��״̬====================================
        if( records[0][14]=="0" ):
            return AfaFlowControl.ExitThisFlow( 'A0004', '��ҵ����������δ����״̬,�������˽���' )

        elif( records[0][14]=="2" ):
            return AfaFlowControl.ExitThisFlow( 'A0005', '��ҵ���������ڹر�״̬,�������˽���' )
                
        elif( records[0][14]=="3" ):
            return AfaFlowControl.ExitThisFlow( 'A0006', '��ҵ����������ͣ��״̬,�������˽���' )


        #=======================��Χϵͳ�����/����Ա��=========================
        if( TradeContext.channelCode != '005' ):
            if(len(records[0][7])==0):
                return AfaFlowControl.ExitThisFlow( 'A0006', '��Χϵͳ������Ϊ��,�������˽���' )
            else:
                TradeContext.__agentBrno__=records[0][7]

            if(len(records[0][8])==0):
                return AfaFlowControl.ExitThisFlow( 'A0006', '��Χϵͳ����Ա��Ϊ��,�������˽���' )
            else:
                TradeContext.__agentTeller__=records[0][8]

                
        #�������ʽ��׶��
        if(len(records[0][9])==0):
            TradeContext.__chanlMaxAmount__ = '0'
        else:
            TradeContext.__chanlMaxAmount__=records[0][9]
            
        AfaLoggerFunc.tradeInfo( '::::::�������ʶ��  =' + TradeContext.__chanlMaxAmount__ )

        #�������ۼƽ��׶��
        if(len(records[0][10])==0):
            TradeContext.__chanlTotalAmount__ = '0'
        else:
            TradeContext.__chanlTotalAmount__=records[0][10]
            
        AfaLoggerFunc.tradeInfo( '::::::�����ۼƶ��  =' + TradeContext.__chanlTotalAmount__ )

        #����������׶��
        if(not ChkAmtStatus('2')):
            return False

                
        #��Ʊ�����־
        TradeContext.__billSaveCtl__=records[0][11]
        AfaLoggerFunc.tradeInfo( '::::::��Ʊ�����־  =' + TradeContext.__billSaveCtl__ )

        #�Զ����ʱ�־
        TradeContext.__autoRevTranCtl__=records[0][12]
        AfaLoggerFunc.tradeInfo( '::::::�Զ����ʱ�־  =' + TradeContext.__autoRevTranCtl__ )

        #�쳣���׼���־
        TradeContext.__errChkCtl__=records[0][13]
        AfaLoggerFunc.tradeInfo( '::::::�쳣����־  =' + TradeContext.__errChkCtl__ )

        #�Զ�����ʻ�����
        TradeContext.__autoChkAcct__=records[0][15]
        AfaLoggerFunc.tradeInfo( '::::::�쳣����־  =' + TradeContext.__autoChkAcct__ )


        if( TradeContext.channelCode != "005" ):
            
            #��Χ����Ľ���,���û�����������Ա��,�ӱ��л�ȡ
            
            #�����
            if( not TradeContext.existVariable( "brno" ) or len( TradeContext.brno ) == 0 ):
                TradeContext.brno=TradeContext.__agentBrno__
                
            #��Ա��
            if( not TradeContext.existVariable( "tellerno" ) or len( TradeContext.tellerno ) == 0 ):
                TradeContext.tellerno  = TradeContext.__agentTeller__
                TradeContext.cashTelno = TradeContext.__agentTeller__


        #�쳣���׼��
        if( TradeContext.__errChkCtl__ == '1' and ( not ( TradeContext.existVariable( 'revTranF' ) and TradeContext.revTranF == '1' ) ) ):

            iRetCode = ChkAbnormal( )
            if( iRetCode == -1 ):
                TradeContext.errorCode, TradeContext.errorMsg='A0035', '����쳣����ʧ��'+AfaDBFunc.sqlErrMsg
                return False

            if( iRetCode == 1 ):
                TradeContext.errorCode, TradeContext.errorMsg='A0036', '����ҵ������쳣����,��ʹ���쳣���׽��д���'
                return False


        #�����Ҫ�Զ�����ʻ�����,������Ӧ����,ֻ�������������ж�
        if( TradeContext.existVariable('revTranF') and TradeContext.revTranF=='0' and TradeContext.existVariable('accno') and TradeContext.__autoChkAcct__=='1' ):
            if ( GetAccType( TradeContext.accno ) == 0 ):
                TradeContext.errorCode, TradeContext.errorMsg='A0037', 'û�ж�Ӧ���ʻ�������Ϣ'
                return False

        return True
        
    else:
        return AfaFlowControl.ExitThisFlow( 'A0003', '������������Ϣ' )


################################################################################
# ������:    ChkAbnormal
# ����:      ��
# ����ֵ��    0  ���쳣����    1  ���쳣����    -1  ��ѯ��ˮ�����쳣ʧ��
# ����˵����  ����Ա��ѯ��ˮ���е������쳣���� 
################################################################################
def ChkAbnormal( ):

    AfaLoggerFunc.tradeInfo( '>>>��ѯ��ˮ���е��쳣����' )

    #ҵ��ʽ(01-���� 02-���� 03-���� 04-����)
    if (TradeContext.agentFlag=='01' or TradeContext.agentFlag=='03'):
        sqlStr = "SELECT COUNT(*) FROM AFA_MAINTRANSDTL WHERE WORKDATE='"
        sqlStr = sqlStr + TradeContext.workDate + "' AND SYSID='" + TradeContext.sysId
        sqlStr = sqlStr + "' AND ZONENO='"+TradeContext.zoneno+"' AND BRNO='"+TradeContext.brno
        sqlStr = sqlStr + "' AND TELLERNO='"+TradeContext.tellerno+"' AND REVTRANF='0' AND (BANKSTATUS='2' OR (BANKSTATUS='0' AND CORPSTATUS IN ('1', '2','3')))"
       
    else:
        sqlStr = "SELECT COUNT(*) FROM AFA_MAINTRANSDTL WHERE WORKDATE='"
        sqlStr = TradeContext.workDate + "' AND SYSID='" + TradeContext.sysId
        sqlStr = sqlStr + "' AND ZONENO='"+TradeContext.zoneno+"' AND BRNO='"+TradeContext.brno
        sqlStr = sqlStr + "' AND TELLERNO='"+TradeContext.tellerno+"' AND REVTRANF='0' AND (CORPSTATUS='2' OR (CORPSTATUS='0' AND BANKSTATUS IN ('1', '2','3')))"


    #��λ����
    sqlStr = sqlStr + " AND UNITNO='" + TradeContext.unitno

    #ҵ��ģʽ
    if(TradeContext.__busiMode__ == '2' ):
        #�ӵ�λ����
        sqlStr = sqlStr + "' AND SUBUNITNO='" + TradeContext.subUnitno
        
    #��������
    sqlStr = sqlStr + "' AND CHANNELCODE='" + TradeContext.channelCode + "'"

    AfaLoggerFunc.tradeInfo( sqlStr )

    result=AfaDBFunc.SelectSql( sqlStr )
    if( result == None ):
        #��ѯ��ˮ�����쳣ʧ��
        return -1
        
    if( result[0][0]!=0 ):
        #���쳣����
        return 1
        
    else:
        #���쳣����
        return 0


################################################################################
# ������:    GetAccType
# ����:      ���˺�
# ����ֵ��    0  ʧ��    1  �ɹ�
# ����˵����  �Զ��ж��˻�����
################################################################################
def GetAccType( card ):

    AfaLoggerFunc.tradeInfo( '>>>��ȡ�˻�����' )
        
    cardlen=len( card )
    i=2
    #�ȽϺ���
    def signCompare( x, card ):
        if not x[i] or card[( x[i+1]-1 ):( x[i+1]-1+x[i+2] )]==x[i]:
            return 1
        else:
            return 0
    sqlstr = "SELECT SEQNO,ACCLEN,EIGENSTR1,STARTBIT1,LEN1,EIGENSTR2,STARTBIT2,LEN2,EIGENSTR3,STARTBIT3,LEN3,"
    sqlstr = sqlstr + "EIGENSTR4,STARTBIT4,LEN4,EIGENSTR5,STARTBIT5,LEN5,"
    sqlstr = sqlstr + "ACCTYPE FROM AFA_ACCTINFO WHERE ACCLEN="+str(cardlen)+" ORDER BY SEQNO"

    AfaLoggerFunc.tradeInfo( sqlstr )
    
    a = AfaDBFunc.SelectSql( sqlstr )
    if a:
        for i in range( i, len( a[0] )-1, 3 ):                                  #ע��i����һ�κ�Ż�ʧ��
            for x in a:
                a=[x for x in a if signCompare( x, card )]                      #��a��ѭ��ɸȡ����������Ԫ�أ������·���a��    
        if len( a )<1: 
            TradeContext.errorCode, TradeContext.errorMsg='A0020', '�޷��жϸ��˺�����,���������˺�'
            return 0                                                            #���Ϊ[] �򷵻�0
        elif len( a )==1:                                                       #���ֻ��һ�����ϼ�¼ �򷵻ظ�����¼��acctype
            TradeContext.accType=a[0][17]
            return 1
        else:                                                                    #�����������������
            for i in range( i, 2, -3 ):
                    for x in a:
                        if x[i]:
                            a=[x]
            TradeContext.accType=a[0][17]
            return 1
    else:
        TradeContext.errorCode, TradeContext.errorMsg='A0025', '�޶�Ӧ�˺�����,���������˺�:['+AfaDBFunc.sqlErrMsg+']'
        return 0


################################################################################
# ������:    ChkActStatus
# ����:      ��
# ����ֵ��    0  ʧ��    1  �ɹ�
# ����˵����  У��ɷѽ��ʵĺϷ���
################################################################################
def ChkActStatus( ):

    AfaLoggerFunc.tradeInfo( '>>>У��ɷѽ��ʵĺϷ���' )

    #=======================����ֵ����Ч��У��==================================
    if( not TradeContext.existVariable( "accType" ) or len(TradeContext.accType)==0 ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '�ɷѽ��ʴ���[accType]ֵ������!' )
            
    #ϵͳ��ʶ
    sqlStr = "SELECT * FROM AFA_ACTNOADM WHERE SYSID='" + TradeContext.sysId
    
    #��λ����
    sqlStr = sqlStr + "' AND UNITNO='" + TradeContext.unitno
    
    #ҵ��ģʽ
    if(TradeContext.__busiMode__ == '2' ):
        
        #�ӵ�λ����
        sqlStr = sqlStr + "' AND SUBUNITNO='" + TradeContext.subUnitno
        
    #ҵ��ʽ
    sqlStr = sqlStr + "' AND AGENTFLAG='" + TradeContext.agentFlag
    

    #=======================�ɷѽ��ʹ���ģʽ====================================
   
    #������
    if(TradeContext.__actnoMode__ == '0' ):
        sqlStr = sqlStr + "' AND ZONENO='" + "00000"
    else:
        sqlStr = sqlStr + "' AND ZONENO='" + TradeContext.zoneno

        #ҵ��֧�к�
        if(TradeContext.__actnoMode__ == '2' ):
            sqlStr = sqlStr + "' AND ZHNO='" + TradeContext.zhno

    #��������
    sqlStr = sqlStr + "' AND CHANNELCODE='" + TradeContext.channelCode
    
    
    #�ɷѽ��ʴ���
    sqlStr = sqlStr + "' AND ACTTYPECODE='" + TradeContext.accType + "'"


    AfaLoggerFunc.tradeInfo( sqlStr )


    records = AfaDBFunc.SelectSql( sqlStr )
    if( records == None ):
        return AfaFlowControl.ExitThisFlow( 'A0002', '�ɷѽ�����Ϣ������쳣:'+AfaDBFunc.sqlErrMsg )
            
    elif( len( records )!=0 ):
        AfaUtilTools.ListFilterNone( records )
            
        #�ж�ҵ��״̬
        if( records[0][10]=="0" ):
            return AfaFlowControl.ExitThisFlow( 'A0004', '�ýɷѽ���û�п�ͨ,�������˽���' )
                
        TradeContext.__chkAccPwdCtl__= records[0][8]
        TradeContext.__enpAccPwdCtl__= records[0][9]
        
        return True

    else:
        return AfaFlowControl.ExitThisFlow( 'A0003', 'û�п�ͨ��Ӧ�Ľɷѽ���' )




################################################################################
# ������:    ChkAmtStatus
# ����:      chkType:1.��Ӧ��ϵͳͳ�Ƽ��;2.��Ӧ��ϵͳ������ͳ�Ƽ��
# ����ֵ��    False  ʧ��    True  �ɹ�
# ����˵����  ���Ӧ��ϵͳ���շ������
################################################################################
def ChkAmtStatus(chkType=''):

    if(not TradeContext.existVariable( "revTranF" ) or TradeContext.revTranF!='0'):
        return True

    AfaLoggerFunc.tradeInfo( '>>>���У��' )

    #���ϵͳ���ʽ��׶��
    if (chkType=='1'):
        if (long(TradeContext.__sysMaxAmount__)>0 and long(float(TradeContext.amount)*100)>long(TradeContext.__sysMaxAmount__)) :
            return AfaFlowControl.ExitThisFlow( 'A0004', '���׽��ܴ���ϵͳ����ĵ�������׽��[' + TradeContext.__sysMaxAmount__ + ']' )
                
    #���ϵͳ�������ʽ��׶��
    elif (chkType=='2'):
        if(long(TradeContext.__chanlMaxAmount__)>0 and long(float(TradeContext.amount)*100)>long(TradeContext.__chanlMaxAmount__) ):
            return AfaFlowControl.ExitThisFlow( 'A0004', '���׽��ܴ���ϵͳ��������ĵ�������׽��[' + TradeContext.__chanlMaxAmount__ + ']' )


    #=======================���ϵͳ���ۼƽ��׶��==============================
    if (chkType=='1' and long(TradeContext.__sysTotalamount__)>0):
        sqlStr = "SELECT SUM(CAST(AMOUNT AS DECIMAL(17,2))) FROM AFA_MAINTRANSDTL WHERE SYSID = '" + TradeContext.sysId + "' AND REVTRANF = '0' "

        AfaLoggerFunc.tradeInfo( sqlStr )

        records = AfaDBFunc.SelectSql( sqlStr )
            
        if( records == None ):
            return AfaFlowControl.ExitThisFlow( 'A0002', '��ˮ�������쳣:'+AfaDBFunc.sqlErrMsg )
                
        records=AfaUtilTools.ListFilterNone( records )
            
        if( type(records[0][0]) is StringType ):
            records[0][0]=0

        if(long(TradeContext.__sysTotalamount__)<long(records[0][0])+long(float(TradeContext.amount)*100)):
            return AfaFlowControl.ExitThisFlow( 'A0004', '���׽��ܴ���ϵͳ������ս��׶��[' + TradeContext.__sysTotalamount__ + ']' )


    #=======================����������ۼƽ��׶��==============================
    elif (chkType=='2' and long(TradeContext.__chanlTotalAmount__)>0):
        
        sqlStr = "SELECT SUM(CAST(AMOUNT AS DECIMAL(17,2))) FROM AFA_MAINTRANSDTL WHERE SYSID = '" + TradeContext.sysId + "' AND REVTRANF = '0"
        
        
        #��λ����
        sqlStr = sqlStr + "' AND UNITNO = '" + TradeContext.unitno
        
        
        #ҵ��ģʽ
        if(TradeContext.__busiMode__ == '2' ):
            #�ӵ�λ����
            sqlStr = sqlStr + "' AND SUBUNITNO = '" + TradeContext.subUnitno
        
            
        #ҵ��ʽ
        sqlStr = sqlStr + "' AND AGENTFLAG = '" + TradeContext.agentFlag
        
        
        #ҵ�������
        if(TradeContext.__channelMode__ == '0' ):
            sqlStr = sqlStr + "' AND ZONENO = '" + '00000'
        else:
            sqlStr = sqlStr + "' AND ZONENO = '" + TradeContext.zoneno
            
            if(TradeContext.__channelMode__ == '2' ):
                #ҵ��֧�к�
                sqlStr = sqlStr + "' AND ZHNO = '" + TradeContext.zhno

        #��������
        sqlStr = sqlStr + "' AND CHANNELCODE = '" + TradeContext.channelCode + "'"
        
        
        AfaLoggerFunc.tradeInfo( sqlStr )


        records = AfaDBFunc.SelectSql( sqlStr )
            
            
        if( records == None ):
            return AfaFlowControl.ExitThisFlow( 'A0002', '��ˮ�������쳣:'+AfaDBFunc.sqlErrMsg )
              
                
        records=AfaUtilTools.ListFilterNone( records )
        if( type(records[0][0]) is StringType ):
            records[0][0]=0


        if(long(TradeContext.__chanlTotalAmount__)<long(records[0][0])+long(float(TradeContext.amount)*100)):
            return AfaFlowControl.ExitThisFlow( 'A0004', '���׽��ܴ���ϵͳ����������ս��׶��[' + TradeContext.__chanlTotalAmount__ + ']' )


    return True

################################################################################
# ������:    RespCodeMsg
# ����:      outcode:�ⲿ��Ӧ��
# ����ֵ��    0  ʧ��    1  �ɹ�
# ����˵����  �����ⲿ��Ӧ���ȡ�ⲿ��Ӧ��Ϣ
################################################################################
def RespCodeMsg( outcode ):

    AfaLoggerFunc.tradeInfo( '>>>ת��������Ӧ��' )

    sqlStr="SELECT * FROM AFA_RESPCODE WHERE SYSID='HOST' AND ORESPCODE='" + outcode + "'"
    
    AfaLoggerFunc.tradeInfo( sqlStr )

    records=AfaDBFunc.SelectSql( sqlStr )
    if( records == None ):
        return AfaFlowControl.ExitThisFlow( 'A0002', '��Ӧ����Ϣ������쳣:'+AfaDBFunc.sqlErrMsg )
            
    elif( len( records ) != 0 ):
        AfaUtilTools.ListFilterNone( records )
        TradeContext.__irespCode__=records[0][3]
        AfaLoggerFunc.tradeInfo( '����������:['+outcode+']['+TradeContext.__irespCode__+']' )
        return records[0][5]

    else:
        return AfaFlowControl.ExitThisFlow( 'A0003', '��Ӧ����Ϣ��û����Ӧ��¼' )

    return True

################################################################################
# ������:    GetRespMsg
# ����:      outcode:�ⲿ��Ӧ��
# ����ֵ��    0  ʧ��    1  �ɹ�
# ����˵����  �����ⲿ��Ӧ���ȡ�ⲿ��Ӧ��Ϣ
################################################################################
def GetRespMsg( outcode ):

    AfaLoggerFunc.tradeInfo( '>>>ת���ⲿ��Ӧ��' )
        
    AfaLoggerFunc.tradeInfo( '>>>���=' + outcode)

    sqlStr="SELECT IRESPCODE,RESPMSG FROM AFA_RESPCODE WHERE SYSID='" + TradeContext.sysId + "' AND UNITNO = '" + TradeContext.unitno + "' AND ORESPCODE='" + outcode + "'"

    AfaLoggerFunc.tradeInfo( sqlStr )

    records=AfaDBFunc.SelectSql( sqlStr )
        
    if( records == None ):
        return AfaFlowControl.ExitThisFlow( 'A0002', '��Ӧ����Ϣ������쳣:'+AfaDBFunc.sqlErrMsg )
            
    elif( len( records )!=0 ):
        AfaUtilTools.ListFilterNone( records )

        TradeContext.errorCode = records[0][0]
        TradeContext.errorMsg  = records[0][1]
        AfaLoggerFunc.tradeInfo( '������:['+outcode+']['+TradeContext.errorCode+']['+TradeContext.errorMsg+']' )

    else:

        TradeContext.errorCode=outcode
        TradeContext.errorMsg ='δ֪����'

        AfaLoggerFunc.tradeInfo( 'δ�ҵ���Ӧ����Ϣ��������:['+TradeContext.errorCode+'][δ֪����]' )

    return True

################################################################################
# ������:    GetTradeName
# ����:      fileName:�ļ���
# ����ֵ��    0  ʧ��    temp  ��������
# ����˵����  ��ȡ�ļ��еı�����
################################################################################
def GetTradeName( fileName ):

    temp=[]
    try:
        testFile=open( fileName, 'r' )
        for y in testFile.readlines( ):
            temp.append( y.replace( '\n', '' ) )
        testFile.close( )
        return temp
    except Exception, e:
        AfaLoggerFunc.tradeError(str(e))
        return 0



################################################################################
# ������:    autoPackData
# ����:      ��
# ����ֵ��    True �ɹ�
# ����˵����  �Զ����
################################################################################
def autoPackData( ):

    AfaLoggerFunc.tradeInfo( '>>>�Զ����' )

    #�׳��������
    SendUpdData()

    if( not TradeContext.existVariable( "tradeResponse" ) or not TradeContext.tradeResponse ):
        
        TradeContext.tradeResponse=[]
        
        #ƽ̨�ڲ�����
        names = TradeContext.getNames( )
        for name in names:
            if ( not name.startswith( '__' ) and name != 'tradeResponse' ) :
                value = getattr( TradeContext, name )
                if( type( value ) is StringType ) :
                    TradeContext.tradeResponse.append( [name, value] )
                elif( type( value ) is ListType ) :
                    for elem in value:
                        if type(elem) is not str :
                            AfaLoggerFunc.tradeInfo( 'autoPackData  [value is not sting]')
                            continue
                        TradeContext.tradeResponse.append( [name, elem] )
                           
        #���������ر���
        names = Party3Context.getNames( )
        for name in names:
            if ( name.startswith( 'dn_' ) ) :
                value = getattr( Party3Context, name )
                if( type( value ) is StringType ) :
                    TradeContext.tradeResponse.append( [name, value] )
                elif( type( value ) is ListType ) :
                    for elem in value:
                        TradeContext.tradeResponse.append( [name, elem] )
        
    else:
        return False
        
    return True



#=======================��ѯ�����ֵ����Ч��У��==========================
def Query_ChkVariableExist( ):

    AfaLoggerFunc.tradeInfo( '>>>��ѯ�����ֵ����Ч��У��' )
        
    if( not TradeContext.existVariable( "sysId" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', 'ϵͳ��ʶ[sysId]ֵ������!' )

    if( not TradeContext.existVariable( "agentFlag" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', 'ҵ��ʽ[agentFlag]ֵ������!' )


    if( not TradeContext.existVariable( "channelCode" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '��������[channelCode]ֵ������!' )

    if( TradeContext.channelCode == '005' ):
        if( not TradeContext.existVariable( "zoneno" ) ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '���к�[zoneno]ֵ������!' )

        if( not TradeContext.existVariable( "brno" ) ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '������[brno]ֵ������!' )

        if( not TradeContext.existVariable( "tellerno" ) ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '������[tellerno]ֵ������!' )

    return True

#=======================�ɷ������ֵ����Ч��У��==========================
def Pay_ChkVariableExist( ):

    AfaLoggerFunc.tradeInfo( '>>>�ɷ������ֵ����Ч��У��' )
        
    if( not TradeContext.existVariable( "sysId" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', 'ϵͳ��ʶ[sysId]ֵ������!' )


    if( not TradeContext.existVariable( "agentFlag" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', 'ҵ��ʽ[agentFlag]ֵ������!' )


    if( not TradeContext.existVariable( "channelCode" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '��������[channelCode]ֵ������!' )


    if( TradeContext.channelCode == '005' ):
        if( not TradeContext.existVariable( "zoneno" ) ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '���кź�[zoneno]ֵ������!' )
                
        if( not TradeContext.existVariable( "brno" ) ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '������[brno]ֵ������!' )
                
        if( not TradeContext.existVariable( "tellerno" ) ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '��Ա��[tellerno]ֵ������!' )
                
        if( not TradeContext.existVariable( "cashTelno" ) ):
            TradeContext.cashTelno = TradeContext.tellerno

    if( not TradeContext.existVariable( "operno" ) ):
        TradeContext.operno='00000'
        
        
    if( not TradeContext.existVariable( "zhno" ) or len( TradeContext.zhno ) == 0 ):
        TradeContext.zhno='00000'


    if( not TradeContext.existVariable( "amount" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '���[amount]ֵ������!' )


    if( not TradeContext.existVariable( "userno" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '�û���[userno]ֵ������!' )


    if( not TradeContext.existVariable( "accno" ) ):
        TradeContext.accType='000'


    TradeContext.revTranF='0'

    return True



#=======================ȡ�����ױ���ֵ����Ч��У��==========================
def Cancel_ChkVariableExist( ):

    AfaLoggerFunc.tradeInfo( '>>>ȡ�����ױ���ֵ����Ч��У��' )
        
    if( not TradeContext.existVariable( "sysId" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', 'ϵͳ��ʶ[sysId]ֵ������!' )


    if( not TradeContext.existVariable( "agentFlag" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '����ҵ��ʽ[agentFlag]ֵ������!' )


    if( not TradeContext.existVariable( "channelCode" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '��������[channelCode]ֵ������!' )

    if( TradeContext.channelCode == '005' ):
        if( not TradeContext.existVariable( "zoneno" ) ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '���к�[zoneno]ֵ������!' )
                
        if( not TradeContext.existVariable( "brno" ) ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '������[brno]ֵ������!' )

        if( not TradeContext.existVariable( "tellerno" ) ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '��Ա��[tellerno]ֵ������!' )
                
        if( not TradeContext.existVariable( "cashTelno" ) ):
            TradeContext.cashTelno = TradeContext.tellerno


    if( not TradeContext.existVariable( "operno" ) ):
        TradeContext.operno='00000'

        
    if( not TradeContext.existVariable( "zhno" ) or len( TradeContext.zhno ) == 0 ):
        TradeContext.zhno='00000'


    if( not TradeContext.existVariable( "amount" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '���[amount]ֵ������!' )

            
    if( not TradeContext.existVariable( "preAgentSerno" ) and not TradeContext.existVariable( "preChannelSerno" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', 'ԭ������ˮ��[preAgentSerno��preChannelSerno]ֵ������!' )


    if( not TradeContext.existVariable( "userno" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '�û���[userno]ֵ������!' )


    if( not TradeContext.existVariable( "accno" ) ):
        TradeContext.accno=''
        TradeContext.accType='000'
        
        
    TradeContext.revTranF='1'
    
    
    return True

#===============У�鷴��������������,������ˮ�űȶ��û���/�ʺ�/���׽��=========
def ChkRevInfo( ):

    AfaLoggerFunc.tradeInfo( '>>>У�鷴��������������' )
        
    sqlstr = "SELECT REVTRANF,USERNO,CRACCNO,DRACCNO,AMOUNT,AGENTFLAG,ACCTYPE,TELLERNO,CASHTELNO,"
    sqlstr = sqlstr + "SUBUSERNO,SUBAMOUNT,USERNAME,VOUHTYPE,TERMID,"
    sqlstr = sqlstr + "VOUHNO,VOUHDATE,BANKSERNO,CORPSERNO,CORPTIME,NOTE1,NOTE2,NOTE3,NOTE4,NOTE5,NOTE6,"
    sqlstr = sqlstr + "NOTE7,NOTE8,NOTE9,NOTE10,AGENTSERIALNO,CURRTYPE,CURRFLAG FROM AFA_MAINTRANSDTL WHERE "
    
    iSernoFlag = 0
    if ( TradeContext.existVariable( "preAgentSerno" ) and len(TradeContext.preAgentSerno)>0 ) :
        sqlstr = sqlstr + " AGENTSERIALNO='"+TradeContext.preAgentSerno+"' AND "
        iSernoFlag = 1

    if ( TradeContext.existVariable( "preChannelSerno" ) and len(TradeContext.preChannelSerno)>0 ) :
        sqlstr = sqlstr + " CHANNELSERNO='"+TradeContext.preChannelSerno+"' AND "
        iSernoFlag = 2


    sqlstr = sqlstr + " WORKDATE='"+TradeContext.workDate+ "' AND BANKSTATUS='0' AND CORPSTATUS='0' "
    
    if ( iSernoFlag == 0 ):
        return AfaFlowControl.ExitThisFlow( 'A0025', 'ԭ�м�ҵ����ˮ�ź���ҵ��ˮ�Ų���ͬʱΪ��' )
            
    
    AfaLoggerFunc.tradeInfo( sqlstr )


    tmp = AfaDBFunc.SelectSql( sqlstr )
    if tmp == None :
        return AfaFlowControl.ExitThisFlow( 'A0025', AfaDBFunc.sqlErrMsg )
            
            
    elif len( tmp ) == 0 :
        return AfaFlowControl.ExitThisFlow( 'A0045', 'δ����ԭ����' )


    tmp=AfaUtilTools.ListFilterNone( tmp )

    temp=tmp[0]
    if temp[0]!='0':                    #У�鷴���ױ�־
        return AfaFlowControl.ExitThisFlow( 'A0020', '��ƥ����Ϣ�����ױ�־����' )
            
            
    if temp[7]!=TradeContext.tellerno:  #У���Ա��
        return AfaFlowControl.ExitThisFlow( 'A0020', '��Ա�Ų�ƥ��' )
            
            
    if temp[8]!=TradeContext.cashTelno: #У�����Ա��
        return AfaFlowControl.ExitThisFlow( 'A0020', '����Ա�Ų�ƥ��' )
            
            
    if temp[1]!=TradeContext.userno:    #У���û���
        return AfaFlowControl.ExitThisFlow( 'A0020', '�û��Ų�ƥ��' )       


    if temp[4]!=TradeContext.amount:    #У����
        return AfaFlowControl.ExitThisFlow( 'A0020', '��ƥ��' )
            
            
    TradeContext.__crAccno__  = temp[2]         #�����˺�
    TradeContext.__drAccno__  = temp[3]         #�跽�˺�
    TradeContext.accType      = temp[6]         #�˻�����
    TradeContext.subUserno    = temp[9]         #�����û���
    TradeContext.subAmount    = temp[10]        #���ӽ��
    TradeContext.userName     = temp[11]        #�û�����
    TradeContext.vouhType     = temp[12]        #ƾ֤����
    TradeContext.termId       = temp[13]        #�ն˺�
    TradeContext.vouhno       = temp[14]        #ƾ֤��
    TradeContext.vouhDate     = temp[15]        #ƾ֤����
    TradeContext.bankSerno    = temp[16]        #������ˮ
    TradeContext.corpSerno    = temp[17]        #��ҵ��ˮ
    TradeContext.corpTime     = temp[18]        #��ҵʱ���
    TradeContext.note1        = temp[19]        #��ע1
    TradeContext.note2        = temp[20]        #��ע2
    TradeContext.note3        = temp[21]        #��ע3
    TradeContext.note4        = temp[22]        #��ע4
    TradeContext.note5        = temp[23]        #��ע5
    TradeContext.note6        = temp[24]        #��ע6
    TradeContext.note7        = temp[25]        #��ע7
    TradeContext.note8        = temp[26]        #��ע8
    TradeContext.note9        = temp[27]        #��ע9
    TradeContext.note10       = temp[28]        #��ע10

    if ( iSernoFlag == 2 ):
        TradeContext.preAgentSerno= temp[29]    #ԭ�м�ҵ����ˮ��

    TradeContext.currType     = temp[30]        #����
    TradeContext.currFlag     = temp[31]        #�����־

    return True



################################################################################
# ������:    GetBranchInfo
# ����:      branchno
# ����ֵ��    False  ʧ��;    �ɹ�����list
# ����˵����  ��ȡ������Ϣ
################################################################################
def GetBranchInfo(branchno=''):

    AfaLoggerFunc.tradeInfo( '>>>��ѯ��ȡ������Ϣ' )

    sqlStr="SELECT UPBRANCHNO,BRANCHCODE,TYPE,BRANCHNAMES,BRANCHNAME FROM AFA_BRANCH WHERE BRANCHNO='" + branchno + "'"

    AfaLoggerFunc.tradeInfo( sqlStr )

    records=AfaDBFunc.SelectSql( sqlStr )
        
    if( records == None ):
        return AfaFlowControl.ExitThisFlow( 'A0002', '��ѯ������ʧ��:'+AfaDBFunc.sqlErrMsg )
            
    elif ( len( records )==0):
        return AfaFlowControl.ExitThisFlow( 'A0002', '�޷��ҵ���Ӧ�Ļ�����' )
            
    elif ( len( records )>1):
        return AfaFlowControl.ExitThisFlow( 'A0002', '�鵽����������' )
            
    else:
        AfaUtilTools.ListFilterNone( records )
        TradeContext.__mngZoneno__   = records[0][0]
        TradeContext.__branchCode__  = records[0][1]
        TradeContext.__branchType__  = records[0][2]
        TradeContext.__branchNames__ = records[0][3]
        TradeContext.__branchName__  = records[0][4]
        
        AfaLoggerFunc.tradeInfo('��Ͻ������:['+TradeContext.__mngZoneno__+']')

    return True


################################################################################
# ������:    GetSummaryInfo
# ����:      ��
# ����ֵ��    False  ʧ��;    �ɹ����� True
# ����˵����  ��ȡ����ժҪ��Ϣ
################################################################################
def GetSummaryInfo( ):

    AfaLoggerFunc.tradeInfo( '>>>��ѯժҪ������Ϣ' )

    sqlStr="SELECT SUMNO,SUMNAME FROM AFA_SUMMARY WHERE SYSID='" + TradeContext.sysId + "'"

    AfaLoggerFunc.tradeInfo( sqlStr )

    records=AfaDBFunc.SelectSql( sqlStr )

    if( records == None ):
        return AfaFlowControl.ExitThisFlow( 'A0002', '��ѯժҪ������Ϣʧ��:' + AfaDBFunc.sqlErrMsg )
            
    elif ( len( records )==0 ):
        TradeContext.__summaryCode__='258'
        TradeContext.__summaryName__='Ĭ��'

    elif ( len( records )>1):
        return AfaFlowControl.ExitThisFlow( 'A0002', '�鵽����ժҪ������Ϣ' )

    else:
        AfaUtilTools.ListFilterNone( records )
        TradeContext.__summaryCode__=records[0][0]
        TradeContext.__summaryName__=records[0][1]

    AfaLoggerFunc.tradeInfo('>>>ժҪ����:['+TradeContext.__summaryCode__+']')
    AfaLoggerFunc.tradeInfo('>>>ժҪ����:['+TradeContext.__summaryName__+']')

    return True



################################################################################
# ������:    GetKeyInfo
# ����:      ��
# ����ֵ��    False  ʧ��;    �ɹ����� True
# ����˵����  ��ȡ��Կ��Ϣ
################################################################################
def GetKeyInfo( ):

    AfaLoggerFunc.tradeInfo('>>>��ȡKEY��Ϣ')

    sqlStr = "SELECT KEY1,KEY2 FROM AFA_KEYADM WHERE SYSID='" + TradeContext.sysId + "' AND UNITNO='" + TradeContext.unitno +"'"


    if ( TradeContext.__busiMode__ == '2' ):
         sqlStr =  sqlStr + " AND SUBUNITNO='" + TradeContext.subUnitno +"'"
         
         
    AfaLoggerFunc.tradeInfo( sqlStr )


    records=AfaDBFunc.SelectSql( sqlStr )
    
    
    if( records == None ):
        return AfaFlowControl.ExitThisFlow( 'A0002', '��ѯ��Կ��Ϣʧ��:' + AfaDBFunc.sqlErrMsg )
            
    elif ( len( records )==0 ):
        return AfaFlowControl.ExitThisFlow( 'A0002', 'û�з�����Կ��Ϣ' )

    elif ( len( records )>1):
        return AfaFlowControl.ExitThisFlow( 'A0002', '�鵽������Կ��Ϣ' )

    else:
        AfaUtilTools.ListFilterNone( records )
        TradeContext.initKey = records[0][0]
        TradeContext.commKey = records[0][1]

    AfaLoggerFunc.tradeInfo('>>>initKey:[' + TradeContext.initKey + ']')

    AfaLoggerFunc.tradeInfo('>>>commKey:[' + TradeContext.commKey + ']')

    return True
    
    

################################################################################
# ������:    GetFeeInfo
# ����:      ��
# ����ֵ��    False  ʧ��;    �ɹ����� True
# ����˵����  ��ȡ������Ϣ
################################################################################
def GetFeeInfo( ):


    AfaLoggerFunc.tradeInfo('>>>��ȡ������Ϣ')


    sqlStr = "SELECT FEEFLAG,AMOUNT FROM AFA_FEEADM WHERE SYSID='" + TradeContext.sysId + "' AND UNITNO='" + TradeContext.unitno +"'"


    if ( TradeContext.__busiMode__ == '2' ):
         sqlStr =  sqlStr + " AND SUBUNITNO='" + TradeContext.subUnitno +"'"


    AfaLoggerFunc.tradeInfo( sqlStr )


    records=AfaDBFunc.SelectSql( sqlStr )


    if( records == None ):
        return AfaFlowControl.ExitThisFlow( 'A0002', '��ѯ������Ϣʧ��:' + AfaDBFunc.sqlErrMsg )


    elif ( len( records )==0 ):
        return AfaFlowControl.ExitThisFlow( 'A0002', '�޷�����Ϣ' )


    elif ( len( records )>1):
        return AfaFlowControl.ExitThisFlow( 'A0002', '�鵽����������Ϣ' )


    else:
        AfaUtilTools.ListFilterNone( records )
            
        if ( records[0][0] == '1' ):
            TradeContext.__feeAmount__ = records[0][1]

            AfaLoggerFunc.tradeInfo('>>>����շ�:[' + TradeContext.__feeAmount__ + ']')
                
        else:
            AfaLoggerFunc.tradeInfo('>>>�����շ�:��ģʽĿǰ��֧��]')

        return True
    
    
    
################################################################################
# ������:    ChkMainbrno
# ����:      psSysid,psUnitid,psSubUnitid,psBrno ҵ����룬�̻����룬��֧�̻����룬���������
# ����ֵ��    False  ʧ��;    �ɹ�����list
# ����˵����  �ж�psBrno�Ƿ�Ϊҵ��psSysid,psUnitid,psSubUnitid����������
################################################################################
def ChkMainbrno(psSysid,psUnitid,psSubUnitid,psBrno):

    AfaLoggerFunc.tradeInfo( '>>>����Ƿ�Ϊ������' )


    #ϵͳ��ʶ
    sqlStr = "SELECT BRNO,BUSIMODE,ACCMODE FROM AFA_UNITADM WHERE SYSID = '" + psSysid + "' AND "
    
    
    #��λ����
    sqlStr = sqlStr + "UNITNO = '" + psUnitid + "'"    
    

    AfaLoggerFunc.tradeInfo( sqlStr )


    records=AfaDBFunc.SelectSql( sqlStr )
    if( records == None ):
        return AfaFlowControl.ExitThisFlow( 'A0002', '��ѯ���к�ʧ��:'+AfaDBFunc.sqlErrMsg )
            
            
    elif ( len( records )==0):
        return AfaFlowControl.ExitThisFlow( 'A0002', '�޷��ҵ���Ӧ�ķ��кŻ��Ͻ���к�' )
            
            
    elif ( len( records )>1):
        return AfaFlowControl.ExitThisFlow( 'A0002', '�鵽�������кŻ��Ͻ���кż�¼' )
            
            
    else:
        if(records[0][1]=='2' or records[0][2]=='2'):
            
            #ϵͳ��ʶ
            sqlStr = "SELECT BRNO FROM AFA_SUBUNITADM WHERE SYSID = '" + psSysid + "' AND "

            #��λ����
            sqlStr = sqlStr + "UNITNO = '" + psUnitid + "' AND SUBUNITNO = '" + psSubUnitid + "'"

            AfaLoggerFunc.tradeInfo( sqlStr )

            subrecords=AfaDBFunc.SelectSql( sqlStr )
            if( subrecords == None ):
                return AfaFlowControl.ExitThisFlow( 'A0002', '��ѯ���к�ʧ��:' + AfaDBFunc.sqlErrMsg )
                    
                    
            elif ( len( subrecords )==0):
                return AfaFlowControl.ExitThisFlow( 'A0002', '�޷��ҵ���Ӧ�ķ��кŻ��Ͻ���к�' )
                    
                    
            elif ( len( subrecords )>1):
                return AfaFlowControl.ExitThisFlow( 'A0002', '�鵽�������кŻ��Ͻ���кż�¼' )
                    
                    
            else:
                AfaUtilTools.ListFilterNone( subrecords )
                if(psBrno==subrecords[0][0]):
                    return True
                    
        else:
            AfaUtilTools.ListFilterNone( records )
                
            if(psBrno==records[0][0]):
                return True
            
    return False    


################################################################################
# ������:    SendUpdData
# ����ֵ��   False-ʧ��; True-�ɹ�
# ����˵����  
################################################################################
def SendUpdData( ):

    try:

        AfaLoggerFunc.tradeInfo( '>>>�׳��������' )

        #ƴװ�㲥��Ϣ
        sndBuf = "oid=1.3.6.1.4.1.26350.1.6.6.6.6" + "|"


        #���״���
        if( TradeContext.existVariable( "TemplateCode" ) and TradeContext.existVariable( "TransCode" ) ):
            #���ױ�ʶ
            sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.1.1=" + TradeContext.TemplateCode + '-' + TradeContext.TransCode + "|"
        else:
            return False


        #ϵͳ����
        if ( TradeContext.existVariable( "sysId" ) ):
            sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.1="  + TradeContext.sysId + "|"

            if (TradeContext.sysId=="RCC01"):
                TradeContext.sysCName = "ũ����"

            elif (TradeContext.sysId=="AG2008"):
                TradeContext.sysCName = "��˰����"

        elif ( TradeContext.existVariable( "sysType" ) ):
            sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.1="  + TradeContext.sysType + "|"

            if (TradeContext.sysType=="abdt"):
                TradeContext.sysCName = "��������"

            elif (TradeContext.sysType=="vouh"):
                TradeContext.sysCName = "ƾ֤����"

        else:
            sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.1="  + "AG0000" + "|"      
            TradeContext.sysCName = "����ϵͳ"


        #ϵͳ����
        if( TradeContext.existVariable( "sysCName" ) ):
            sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.2="  + TradeContext.sysCName + "|"      
        else:
            sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.2="  + "" + "|"     



        #���״���
        sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.3=" + TradeContext.TemplateCode + '-' + TradeContext.TransCode + "|"


        #��������
        if( TradeContext.existVariable( "TransName" ) ):
            sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.4="  + TradeContext.TransName + "|"      
        else:
            sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.4="  + "" + "|"


            
        #��ˮ��
        if( TradeContext.existVariable( "agentSerialno" ) ):
            sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.5="  + TradeContext.agentSerialno + "|"     
             
        elif( TradeContext.existVariable( "BSPSQN" ) ):
            sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.5="  + TradeContext.BSPSQN + "|"     

        elif( TradeContext.existVariable( "SerialNo" ) ):
            sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.5="  + TradeContext.SerialNo + "|"     

        else:
            sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.5="  + "00000000" + "|"



        #��������
        if( TradeContext.existVariable( "workDate" ) ):
            sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.6="  + TradeContext.workDate + "|"      
        else:
            sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.6="  + UtilTools.GetSysDate( ) + "|"



        #����ʱ��
        if( TradeContext.existVariable( "workTime" ) ):
            sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.7="  + TradeContext.workTime + "|"      
        else:
            sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.7="  + UtilTools.GetSysTime( ) + "|"
            


        #������
        if( TradeContext.existVariable( "brno" ) ):
            sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.8="  + TradeContext.brno + "|"     
            
        elif ( TradeContext.existVariable( "BESBNO" ) ):
            sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.8="  + TradeContext.BESBNO + "|"     

        elif ( TradeContext.existVariable( "I1SBNO" ) ):
            sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.8="  + TradeContext.I1SBNO + "|"     

        else:
            sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.8="  + "0000000000" + "|"
            


        #��Ա��
        if( TradeContext.existVariable( "tellerno" ) ):
            sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.9="  + TradeContext.tellerno + "|"      
            
        elif ( TradeContext.existVariable( "BETELR" ) ):
            sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.9="  + TradeContext.BETELR + "|"    

        elif ( TradeContext.existVariable( "I1USID" ) ):
            sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.9="  + TradeContext.I1USID + "|"    

        else:
            sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.9="  + "" + "|"


        #��������
        if( TradeContext.existVariable( "channelCode" ) ):
            if TradeContext.channelCode=="001":
                sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.10="  + "�����ն�"  + "|"   
                
            elif TradeContext.channelCode=="002":
                sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.10="  + "ATM"       + "|"   
                
            elif TradeContext.channelCode=="003":
                sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.10="  + "�绰����"  + "|"   
                
            elif TradeContext.channelCode=="004":
                sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.10="  + "��������"  + "|"   
                
            elif TradeContext.channelCode=="005":
                sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.10="  + "����"      + "|"   
                
            elif TradeContext.channelCode=="006":
                sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.10="  + "�˹���ϯ"  + "|"   
                
            elif TradeContext.channelCode=="007":
                sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.10="  + "�ֻ�����"  + "|"   
                
            elif TradeContext.channelCode=="008":
                sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.10="  + "��ҵ"      + "|"   
                
            elif TradeContext.channelCode=="009":
                sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.10="  + "����ƽ̨"  + "|"   
                
            elif TradeContext.channelCode=="010":
                sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.10="  + "POS"       + "|"   
                
            else:
                sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.10="  + ""          + "|"   
                
        else:
            sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.10="      + ""          + "|"


        #�ɷѽ���
        if( TradeContext.existVariable( "accType" ) ):
            if TradeContext.accType=="000":
                sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.11="  + "�ֽ�"      + "|"      
                
            elif TradeContext.accType=="001":
                sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.11="  + "�����˺�"  + "|"   
                
            elif TradeContext.accType=="002":
                sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.11="  + "��ǿ�"    + "|"   

            elif TradeContext.accType=="003":
                sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.11="  + "���ǿ�"    + "|"   

            elif TradeContext.accType=="004":
                sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.11="  + "��λ�˺�"  + "|"   

            elif TradeContext.accType=="005":
                sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.11="  + "����"    + "|"   

            else:
                sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.11="  + ""          + "|"  

        else:
            sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.11="      + ""          + "|"



        #�˺�
        if( TradeContext.existVariable( "accno" ) ):
            sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.12="  + TradeContext.accno + "|"      
        else:
            sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.12="  + ""                 + "|"      



        #�ɷѽ��
        if( TradeContext.existVariable( "amount" ) ):
            sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.13="  + TradeContext.amount + "|"      
        else:
            sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.13="  + "" + "|"
            

        #���ش���
        if( TradeContext.existVariable( "errorCode" ) ):
            sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.14="  + TradeContext.errorCode + "|"

        elif( TradeContext.existVariable( "tradeResponse" ) ):
            tmpErrorCode = ""
            for varlist in TradeContext.tradeResponse:
                if varlist[0] == 'errorCode':
                    tmpErrorCode = varlist[1]
                    break
            sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.14="  + tmpErrorCode + "|"
        else:
            sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.14="  + "" + "|"


        #������Ϣ
        if( TradeContext.existVariable( "errorMsg" ) ):
            sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.15="  + TradeContext.errorMsg + "|"      


        elif( TradeContext.existVariable( "tradeResponse" ) ):
            tmpErrorMsg = ""
            for varlist in TradeContext.tradeResponse:
                if varlist[0] == 'errorMsg':
                    tmpErrorMsg = varlist[1]
                    break
            sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.15="  + tmpErrorMsg + "|"
        else:
            sndBuf = sndBuf + "1.3.6.1.4.1.26350.1.6.6.6.6.2.15="  + "" + "|"

        host     = "10.0.130.30"
        lhost    = "10.0.130.30"
        textport = "20089"

        #�����׽���
        sockfd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            port = int(textport)
    
        except ValueError:
            port = socket.getservbyname(textport, 'udp')

        #�IP
        sockfd.bind((lhost, 0))
            
        #��������
        sockfd.connect((host, port))
    
        #������Ϣ
        sockfd.sendall(sndBuf)
    
        #�ر�����(0-�Ͽ�����ͨ�� 1-�Ͽ�����ͨ�� 3-ͬʱ�Ͽ�����ͨ���ͽ���ͨ��)
        sockfd.close()
    
        return True
        
    except Exception, e:
        AfaLoggerFunc.tradeError(str(e))
        return False
