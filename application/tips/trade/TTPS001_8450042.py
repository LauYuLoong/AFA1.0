# -*- coding: gbk -*-
##################################################################
#   �м�ҵ��ƽ̨.�����ʽ�����
#   ���������������������ʽ����㵽�����У�11�ң�
#=================================================================
#   �����ļ�:   003001_0331112.py
#   �޸�ʱ��:   2007-8-18 13:43
##################################################################
import TradeContext, AfaLoggerFunc, UtilTools, AfaFlowControll, AfaDBFunc
#,AfaHostFunc,AfaFlowControl,TransDtlFunc
from types import *

def SubModuleMainFst( ):
    AfaLoggerFunc.tradeInfo('��˰����_�����ʽ����㿪ʼ[T003001_0331112]' )
    TradeContext.TransCode='0331112'
    try:
        #=============��ȡ��ǰϵͳʱ��====================
        TradeContext.workDate=UtilTools.GetSysDate( )
        TradeContext.workTime=UtilTools.GetSysTime( )
        
        #============ϵͳ��ʶ============
        sqlStr = "SELECT * FROM AFA_UNITADM WHERE APPNO = '" + TradeContext.appNo + "' AND "
        #============�̻�����============
        sqlStr = sqlStr+"UNITNO = '" + TradeContext.unitno + "' "
        AfaLoggerFunc.tradeInfo( sqlStr )
        records = AfaDBFunc.SelectSql( sqlStr )
        if( records == None ):
            return AfaFlowControll.ExitThisFlow( 'A0002', '�̻���Ϣ������쳣:'+AfaDBFunc.sqlErrMsg )
        elif( len( records )==0 ):
            AfaLoggerFunc.tradeError( sqlStr )
            return AfaFlowControll.ExitThisFlow( 'A0003', '�޴��̻���Ϣ' )
        else:
            records=UtilTools.ListFilterNone( records )
            ##=============�̻�����=============
            #TradeContext.unitName = records[0][2]
            ##=============�̻����=============
            #TradeContext.unitSName = records[0][3]
            #
            ##===============�ж��̻�״̬============================
            #if( records[0][4]=="0" ):
            #    return AfaFlowControll.ExitThisFlow( 'A0004', '���̻����ڹر�״̬,����������' )
            #elif( records[0][4]=="2" ):
            #    return AfaFlowControll.ExitThisFlow( 'A0005', '���̻�������ͣ״̬,����������' )
            #elif( records[0][4]=="3" ):
            #    return AfaFlowControll.ExitThisFlow( 'A0005', '���̻�����δ����״̬,����������' )
            ##=============���н�ɫ=============
            #TradeContext.__bankMode__ = records[0][5]
            #=============ҵ��ģʽ=============
            TradeContext.__busiMode__ = records[0][6]
            #=============�˻�ģʽ=============
            TradeContext.__accMode__ = records[0][7]
            AfaLoggerFunc.tradeInfo( 'ҵ��ģʽ:'+TradeContext.__busiMode__+'  �˻�ģʽ:'+ TradeContext.__accMode__)
            ##===============ҵ��ģʽ============================
            #if( TradeContext.__busiMode__!="2" ): 
            #======================�˻�ģʽ============================
            if( TradeContext.__accMode__ !="2" ):   #�޷�֧�̻���λ��������������
                return True
                ##===============�����̻����루�̻��ţ�============================
                #TradeContext.bankUnitno = records[0][8]
                ##===============������к�============================
                #if(len(records[0][9])>0):
                #    TradeContext.mainZoneno = records[0][9]
                ##===============���������============================
                #if(len(records[0][10])>0):
                #    TradeContext.mainBrno = records[0][10]
                ##===============���б���============================
                #TradeContext.bankno = records[0][16]
                ##=============��λ�˺�=============
                #TradeContext.__agentAccno__ = records[0][17]
                ##=============ժҪ���루�������ϵͳ��Ҫ��=============
                #TradeContext.__zhaiYaoCode__ = records[0][32]
                ##=============ժҪ���������ϵͳ��Ҫ��=============
                #TradeContext.__zhaiYao__ = records[0][33]
            if( TradeContext.__accMode__ == '2' ):
                #=============�����˺ţ��������ʺţ�=============
                TradeContext.agentAccno = records[0][17]
                #=========�̻���֧��λ=============
                #============ϵͳ��ʶ============
                sqlStr = "SELECT * FROM AFA_SUBUNITADM WHERE APPNO = '" + TradeContext.appNo + "' AND "
                #============�̻�����============
                sqlStr = sqlStr+"UNITNO = '" + TradeContext.unitno + "' "
                AfaLoggerFunc.tradeInfo( sqlStr )
                subRecords = AfaDBFunc.SelectSql( sqlStr )
                if(subRecords == None ):
                    # AfaLoggerFunc.tradeFatal( sqlStr )
                    return AfaFlowControll.ExitThisFlow( 'A0002', '�̻���֧��λ��Ϣ������쳣:'+AfaDBFunc.sqlErrMsg )
                elif( len( subRecords )==0 ):
                    return AfaFlowControll.ExitThisFlow( 'A0002', '�̻���֧��λ���޼�¼��������������' )
                else:
                    subRecords=UtilTools.ListFilterNone( subRecords )
                    for i in range( 0, len( subRecords ) ):
                        subUnitno = subRecords[i][2]
                        AfaLoggerFunc.tradeInfo( 'subunitno:'+subUnitno )
                        #=============ժҪ����=============
                        TradeContext.__zhaiYaoCode__ = subRecords[i][32]
                        #=============ժҪ=============
                        TradeContext.__zhaiYao__    = subRecords[i][33]
                        #=============���㣺����������������з������Ҫ����1391��Ŀ���====================
                        #ͳ����������˲�������Ϊת�˽��
                        if not DoSumAmountDiff(subUnitno):
                            return AfaFlowControll.ExitThisFlow( 'A0027', '���ܷ�����ʧ��' )
                        #TradeContext.amount='1'
                        TradeContext.amount     =str(long(float(TradeContext.amountDiff)))
                        if long(TradeContext.amount)>0 :
                            #����Ƿ��Ѿ�����
                            sqlStr_qs = "SELECT COUNT(*) FROM AFA_MAINTRANSDTL WHERE APPNO = '" + TradeContext.appNo + "'"
                            sqlStr_qs = sqlStr_qs + "AND  UNITNO = '" + TradeContext.unitno + "' "
                            sqlStr_qs = sqlStr_qs + "AND  SUBUNITNO = '" + subUnitno + "' "
                            sqlStr_qs = sqlStr_qs + "AND  USERNO = '-' "
                            sqlStr_qs = sqlStr_qs + "AND  NOTE2 = '" + TradeContext.ChkDate + "' "
                            sqlStr_qs = sqlStr_qs + "AND  NOTE3 = '" + TradeContext.ChkAcctOrd + "' "
                            sqlStr_qs = sqlStr_qs + "AND  NOTE4 = '" + TradeContext.PayBkCode.strip()   + "' "
                            sqlStr_qs = sqlStr_qs + "AND  NOTE5 = '" + TradeContext.PayeeBankNo.strip() + "' "
                            sqlStr_qs = sqlStr_qs + "AND  NOTE6 = '0'" 
                            AfaLoggerFunc.tradeInfo( sqlStr_qs )
                            Records_qs = AfaDBFunc.SelectSql( sqlStr_qs )
                            if(Records_qs == None ):
                                # AfaLoggerFunc.tradeFatal( sqlStr )
                                return AfaFlowControll.ExitThisFlow( 'A0002', '��ˮ������쳣:'+AfaDBFunc.sqlErrMsg )
                            elif (len(Records_qs)=0): 
                                TradeContext.__chkAccPwdCtl__='0'   
                                TradeContext.channelCode='009'
                                TradeContext.accType    ='001'
                                TradeContext.tellerno   ='999986'                   #
                                TradeContext.cashTelno  ='999986'                   #
                                TradeContext.termId     ='tips'
                                TradeContext.brno       =subUnitno                  #unitno��Ϊ���������
                                TradeContext.zoneno     =TradeContext.brno[0:3]
                                TradeContext.accno      =subRecords[i][18]          #����1391�˻���Ϊ�跽�˻�
                                TradeContext.__agentAccno__=subRecords[i][17]       #����2013�˻���Ϊ�����˻�
                                AfaLoggerFunc.tradeInfo( '�跽:'+TradeContext.accno+'����:' +TradeContext.__agentAccno__)
                                TradeContext.userno      ='-'
                                TradeContext.tradeType   ='T'                       #ת���ཻ��
                                TradeContext.userName    =subRecords[i][3]+'.������ˮ'
                                AfaFlowControl.GetBranchInfo(TradeContext.brno)
                                TradeContext.note1      =TradeContext.__mngZoneno__ #�ϼ��������
                                TradeContext.note2      =TradeContext.ChkDate            
                                TradeContext.note3      =TradeContext.ChkAcctOrd         
                                TradeContext.note4      =TradeContext.PayBkCode.strip()  
                                TradeContext.note5      =TradeContext.PayeeBankNo.strip()
                                TradeContext.note6      ='0' #�����ˮ
                                TradeContext.revTranF   ='0'
                                #TradeContext.tradeType  ='T' #ת���ཻ��
                                TradeContext.workTime   =UtilTools.GetSysTime( )
                                #=============��ȡƽ̨��ˮ��====================
                                if AfaFlowControl.GetSerialno( ) == -1 :
                                    AfaLoggerFunc.tradeInfo('>>>������:��ȡƽ̨��ˮ���쳣' )
                                    return AfaFlowControll.ExitThisFlow( 'A0027', '��ȡ��ˮ��ʧ��' )
                                #
                                TradeContext.subUnitno  =subUnitno       #��ˮ�з�֧�̻�����
                                #=============������ˮ��====================
                                if not TransDtlFunc.InsertDtl( ) :
                                    return AfaFlowControll.ExitThisFlow( 'A0027', '������ˮ��ʧ��' )
                                
                                #=============������ͨѶ====================
                                AfaHostFunc.AfaCommHost('705050') 
                                #if TradeContext.errorCode!='0000':
                                #    return False
                                #=============������������״̬====================
                                TransDtlFunc.UpdateDtl( 'TRADE' )
                            
                        #=============���㣺������2013��������2621====================
                        ##ͳ���������ܷ�������Ϊת�˽��
                        #if not DoSumAmount(subUnitno):
                        #    return AfaFlowControll.ExitThisFlow( 'A0027', '���ܷ�����ʧ��' )
                        #TradeContext.amount='1'
                        TradeContext.amount     =str(long(float(TradeContext.amountQS)))
                        if long(TradeContext.amount)>0 :
                            #����Ƿ��Ѿ�����
                            sqlStr_qs = "SELECT COUNT(*) FROM AFA_MAINTRANSDTL WHERE APPNO = '" + TradeContext.appNo + "'"
                            sqlStr_qs = sqlStr_qs + "AND  UNITNO = '" + TradeContext.unitno + "' "
                            sqlStr_qs = sqlStr_qs + "AND  SUBUNITNO = '" + subUnitno + "' "
                            sqlStr_qs = sqlStr_qs + "AND  USERNO = '-' "
                            sqlStr_qs = sqlStr_qs + "AND  NOTE2 = '" + TradeContext.ChkDate + "' "
                            sqlStr_qs = sqlStr_qs + "AND  NOTE3 = '" + TradeContext.ChkAcctOrd + "' "
                            sqlStr_qs = sqlStr_qs + "AND  NOTE4 = '" + TradeContext.PayBkCode.strip()   + "' "
                            sqlStr_qs = sqlStr_qs + "AND  NOTE5 = '" + TradeContext.PayeeBankNo.strip() + "' "
                            sqlStr_qs = sqlStr_qs + "AND  NOTE6 = '1'" 
                            AfaLoggerFunc.tradeInfo( sqlStr_qs )
                            Records_qs = AfaDBFunc.SelectSql( sqlStr_qs )
                            if(Records_qs == None ):
                                # AfaLoggerFunc.tradeFatal( sqlStr )
                                return AfaFlowControll.ExitThisFlow( 'A0002', '��ˮ������쳣:'+AfaDBFunc.sqlErrMsg )
                            elif (len(Records_qs)=0): 
                                TradeContext.__chkAccPwdCtl__='0'   
                                TradeContext.channelCode='009'
                                TradeContext.accType    ='001'
                                TradeContext.tellerno   ='999986'                   #
                                TradeContext.cashTelno  ='999986'                   #
                                TradeContext.termId     ='tips'
                                TradeContext.brno       =TradeContext.unitno        #unitno��Ϊ���������
                                TradeContext.zoneno     =TradeContext.brno[0:3]
                                TradeContext.accno      =subRecords[i][17]          #����2013�����˻���Ϊ�跽�˻�
                                TradeContext.__agentAccno__=TradeContext.agentAccno #������2621��Ϊ����
                                AfaLoggerFunc.tradeInfo( '�跽:'+TradeContext.accno+'����:' +TradeContext.__agentAccno__)
                                if TradeContext.accno==TradeContext.__agentAccno__: #��������
                                    continue
                                TradeContext.userno      ='-'
                                TradeContext.tradeType   ='T'                       #ת���ཻ��
                                TradeContext.userName    =subRecords[i][3]+'.������ˮ'
                                AfaFlowControl.GetBranchInfo(TradeContext.brno)
                                TradeContext.note1      =TradeContext.__mngZoneno__ #�ϼ��������
                                TradeContext.note2      =TradeContext.ChkDate            
                                TradeContext.note3      =TradeContext.ChkAcctOrd         
                                TradeContext.note4      =TradeContext.PayBkCode.strip()  
                                TradeContext.note5      =TradeContext.PayeeBankNo.strip()
                                TradeContext.note6      ='1' #������ˮ
                                TradeContext.revTranF   ='0'
                                TradeContext.workTime   =UtilTools.GetSysTime( )
                                #=============��ȡƽ̨��ˮ��====================
                                if AfaFlowControl.GetSerialno( ) == -1 :
                                    AfaLoggerFunc.tradeInfo('>>>������:��ȡƽ̨��ˮ���쳣' )
                                    return AfaFlowControll.ExitThisFlow( 'A0027', '��ȡ��ˮ��ʧ��' )
                                #
                                TradeContext.subUnitno  =TradeContext.unitno       #��ˮ�з�֧�̻�����=�̻�����
                                #=============������ˮ��====================
                                if not TransDtlFunc.InsertDtl( ) :
                                    return AfaFlowControll.ExitThisFlow( 'A0027', '������ˮ��ʧ��' )
                                
                                #=============������ͨѶ====================
                                AfaHostFunc.AfaCommHost('705050') 
                                #if TradeContext.errorCode!='0000':
                                #    return False
                                #=============������������״̬====================
                                TransDtlFunc.UpdateDtl( 'TRADE' )
                            
        #TradeContext.errorCode='0000'
        #TradeContext.errorMsg='���׳ɹ�'
        AfaLoggerFunc.tradeInfo('��˰����_�����ʽ��������[T003001_0331112]' )
        return True
    except Exception, e:
        AfaFlowControll.exitMainFlow(str(e))
#���ܳɹ������� 
def DoSumAmount(psSubUnitno):
    sSqlStr="SELECT SUM(AMOUNT) FROM AFA_MAINTRANSDTL WHERE  APPNO='"+TradeContext.appNo+"'"
    sSqlStr=sSqlStr+" AND UNITNO='"+TradeContext.unitno+"'"
    sSqlStr=sSqlStr+" AND SUBUNITNO='"+psSubUnitno+"'"
    sSqlStr=sSqlStr+" AND NOTE9='"+TradeContext.ChkDate+"'"
    sSqlStr=sSqlStr+" AND NOTE10='"+TradeContext.ChkAcctOrd+"'"
    sSqlStr=sSqlStr+" AND CHKFLAG='0' AND CORPCHKFLAG='0'"
    AfaLoggerFunc.tradeInfo( sSqlStr )
    SumRecords = AfaDBFunc.SelectSql( sSqlStr )
    if(SumRecords == None ):
        # AfaLoggerFunc.tradeFatal( sqlStr )
        return AfaFlowControll.ExitThisFlow( 'A0002', '��ˮ�������쳣:'+AfaDBFunc.sqlErrMsg )
    else:
        SumRecords=UtilTools.ListFilterNone( SumRecords ,'0')
        TradeContext.amount=SumRecords[0][0]
        AfaLoggerFunc.tradeInfo( '�������緢����'+str(TradeContext.amount) )
    return True

#���ܲ��췢���� 
def DoSumAmountDiff(psSubUnitno):
    sSqlStr="SELECT SUM(AMOUNT) FROM AFA_MAINTRANSDTL WHERE  APPNO='"+TradeContext.appNo+"'"
    sSqlStr=sSqlStr+" AND UNITNO='"+TradeContext.unitno+"'"
    sSqlStr=sSqlStr+" AND SUBUNITNO='"+psSubUnitno+"'"
    sSqlStr=sSqlStr+" AND NOTE9='"+TradeContext.ChkDate+"'"
    sSqlStr=sSqlStr+" AND NOTE10='"+TradeContext.ChkAcctOrd+"'"
    sSqlStr=sSqlStr+" AND CHKFLAG='0'"
    AfaLoggerFunc.tradeInfo( sSqlStr )
    SumRecords = AfaDBFunc.SelectSql( sSqlStr )
    if(SumRecords == None ):
        # AfaLoggerFunc.tradeFatal( sqlStr )
        return AfaFlowControll.ExitThisFlow( 'A0002', '��ˮ�������쳣:'+AfaDBFunc.sqlErrMsg )
    else:
        SumRecords=UtilTools.ListFilterNone( SumRecords ,'0')
        TradeContext.amount=str(SumRecords[0][0])
        AfaLoggerFunc.tradeInfo( '�������緢����'+str(TradeContext.amount) )    

    sSqlStr="SELECT SUM(AMOUNT)*100 FROM CHECK_TRANSDTL WHERE  APPNO='"+TradeContext.appNo+"'"
    sSqlStr=sSqlStr+" AND UNITNO='"+TradeContext.unitno+"'"
    sSqlStr=sSqlStr+" AND SUBUNITNO='"+psSubUnitno+"'"
    sSqlStr=sSqlStr +" and workDate  = '" + TradeContext.ChkDate            + "'"
    sSqlStr=sSqlStr +" and Batchno   = '" + TradeContext.ChkAcctOrd         + "'"
    sSqlStr=sSqlStr +" AND NOTE3     ='"  + TradeContext.PayBkCode.strip()  + "'"   
    sSqlStr=sSqlStr +" AND NOTE2     ='"  + TradeContext.PayeeBankNo.strip()  + "'"
    #sSqlStr=sSqlStr+" AND CHKFLAG!='0' AND CORPCHKFLAG='0'"
    AfaLoggerFunc.tradeInfo( sSqlStr )
    SumRecords = AfaDBFunc.SelectSql( sSqlStr )
    if(SumRecords == None ):
        # AfaLoggerFunc.tradeFatal( sqlStr )
        return AfaFlowControll.ExitThisFlow( 'A0002', '��ˮ�������쳣:'+AfaDBFunc.sqlErrMsg )
    else:
        SumRecords=UtilTools.ListFilterNone( SumRecords ,'0')
        TradeContext.amountQS=str(SumRecords[0][0])
        AfaLoggerFunc.tradeInfo( '�������������'+str(TradeContext.amount) )
    TradeContext.amountDiff=str(long(float(TradeContext.amountQS)) - long(float(TradeContext.amount)))
    
    return True
    