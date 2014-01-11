# -*- coding: gbk -*-
##################################################################
#   ��˰����.����Э��У��.���淢��
#=================================================================
#   �����ļ�:   TTPS001_8451.py
#   �޸�ʱ��:   2006-04-05
##################################################################
import TradeContext, AfaLoggerFunc, UtilTools, TradeFunc,AfaDBFunc
import TipsFunc,AfaAfeFunc,TipsHostFunc,HostContext
from types import *

def SubModuleMainFst( ):
    AfaLoggerFunc.tradeInfo( '��������Э����֤/����[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' )

    try:
        #=============��ȡ��ǰϵͳʱ��====================
        #TradeContext.workDate=UtilTools.GetSysDate( )
        TradeContext.workTime=UtilTools.GetSysTime( )
        
        ##====��ȡ��������=======
        #if not TipsFunc.GetUnitWorkdate( ):
        #    return False
        
        #============У�鹫���ڵ����Ч��==================
        # �����Լ��
        if( not TradeContext.existVariable( "VCSign" ) ):
            return TipsFunc.ExitThisFlow( 'A0001', '��ʶ[VCSign]ֵ������!' )
        if( not TradeContext.existVariable( "zoneno" ) ):
            return TipsFunc.ExitThisFlow( 'A0001', '���к�[zoneno]ֵ������!' )
        if( not TradeContext.existVariable( "channelCode" ) ):
            return TipsFunc.ExitThisFlow( 'A0001', '��������[channelCode]ֵ������!' )
        if( not TradeContext.existVariable( "brno" ) ):
            return TipsFunc.ExitThisFlow( 'A0001', '������[brno]ֵ������!' )
        if( not TradeContext.existVariable( "teller" ) ):
            return TipsFunc.ExitThisFlow( 'A0001', '��Ա��[teller]ֵ������!' )
        if( not TradeContext.existVariable( "accno" ) ):
            return TipsFunc.ExitThisFlow( 'A0001', '�ʺ�[accno]ֵ������!' )
        if( not TradeContext.existVariable( "taxPayCode" ) ):
            return TipsFunc.ExitThisFlow( 'A0001', '��˰�˱���[taxPayCode]ֵ������!' )
        if( not TradeContext.existVariable( "taxPayName" ) ):
            return TipsFunc.ExitThisFlow( 'A0001', '��˰������[taxPayName]ֵ������!' )
        if( not TradeContext.existVariable( "passWDFlag" ) ):
            return TipsFunc.ExitThisFlow( 'A0001', '������֤��־[passWDFlag]ֵ������!' )
        if( not TradeContext.existVariable( "payBkCode" ) ):
            return TipsFunc.ExitThisFlow( 'A0001', '�������к�[payBkCode]ֵ������!' )
            
        TradeContext.note1 = TradeContext.payBkCode
        
        if(TradeContext.passWDFlag == '0'):
            #��֤����
            TradeContext.sBrNo = TradeContext.brno          #���׻���
            TradeContext.sTeller = TradeContext.teller      #���׹�Ա
            TradeContext.sTermId = TradeContext.termId      #�ն˺� 
            HostContext.I1ACNO = TradeContext.accno         #�����ʻ�
            HostContext.I1CYNO = '01'
            accnoLen = len(TradeContext.accno)
            if(accnoLen == 23):
                HostContext.I1CFFG = 'A'
            elif(accnoLen == 19):
                HostContext.I1CFFG = '0'
                HostContext.I1CETY = (TradeContext.accno)[6:8]
                HostContext.I1CCSQ = (TradeContext.accno)[8:19]
            else:
                return TipsFunc.ExitThisFlow( 'A0001', '�ʺŴ���' )
            HostContext.I1PSWD = TradeContext.passWD    
            
            if(not TipsHostFunc.CommHost('8810')):    
                return TipsFunc.ExitThisFlow( TradeContext.errorCode, TradeContext.errorMsg )
            if(TradeContext.errorCode == '0000'):
                if(HostContext.O1CFFG == '1'):
                    return TipsFunc.ExitThisFlow( 'A0001', '�������!' )
        
        #=============�ж�Ӧ��״̬====================
        if not TipsFunc.ChkAppStatus( ) :
            raise TipsFunc.flowException( )
        #=============�жϻ����Ƿ�ͨ��Ӧ��===============
        #if not TipsFunc.ChkBranchStatus( ) :
        #    raise TipsFunc.flowException( )
        #=============��ȡƽ̨��ˮ��==================== 
        if TipsFunc.GetSerialno( ) == -1 :
            raise TipsFunc.flowException( )
        
        #ǩԼ
        if TradeContext.VCSign=='0':
            #=============�ж�״̬====================
            sql="SELECT STATUS FROM TIPS_CUSTINFO WHERE "
            sql=sql+" TAXORGCODE ='"+TradeContext.taxOrgCode     +"'"
            sql=sql+" AND TAXPAYCODE='"+TradeContext.taxPayCode+"'"
            sql=sql+" AND PROTOCOLNO='"+TradeContext.protocolNo+"'"
            sql=sql+" AND PAYACCT='"+TradeContext.accno+"'"
            records = AfaDBFunc.SelectSql(sql)
            AfaLoggerFunc.tradeFatal(sql)
            if( records == None or  records <0):
                #AfaLoggerFunc.tradeFatal(sql)
                return TipsFunc.ExitThisFlow( 'A0002', '���ݿ�����쳣:'+AfaDBFunc.sqlErrMsg )
            elif( len( records )==0 ):
                AfaLoggerFunc.tradeInfo( "�ÿͻ���δǩԼ������������" )
            else:
                AfaLoggerFunc.tradeFatal(sql)
                AfaLoggerFunc.tradeInfo(records[0][0])
                UtilTools.ListFilterNone( records )
                AfaLoggerFunc.tradeInfo( "==================1" )
                #0-ע�� 1-������˫��������֤�� 2-��ʱ״̬�����з���������֤��3-��ʱ״̬�����з������ѳ�����
                if (records[0][0]=="1" or records[0][0]=="2" ): #���иÿͻ���¼��״̬Ϊ"������"��������ǩԼ
                    return TipsFunc.ExitThisFlow( 'A0002', '�ͻ���Ż��ʺ��Ѿ�ǩԼ�������ظ�ǩԼ')
            AfaLoggerFunc.tradeInfo( "==================2" )
            TradeContext.status = '2'
            #TradeContext.revTranF       ='0' #������
            #TradeContext.tradeType      ='S' #ǩԼ�ཻ��
            #TradeContext.amount         ='0' #
            #TradeContext.__agentAccno__ =''  #�跽�ʺ��ÿ�
            ##��¼ǩԼ��ˮ
            #if not TipsFunc.InsertDtl( ) :
            #    return False
            #=============�������ͨѶ====================
            #AfaAfeFunc.CommAfe()
            TradeContext.__status__='0'
            TradeContext.errorCode='0000'
            TradeContext.errorMsg='���׳ɹ�'
            
            ##=============������ˮ��====================
            #if( not TipsFunc.UpdateDtl( 'TRADE' ) ):
            #    return False
            AfaLoggerFunc.tradeInfo( "==================3" )
            if TradeContext.errorCode!='0000':
                return TipsFunc.ExitThisFlow(TradeContext.errorCode, TradeContext.errorMsg)
            if ( len( records )!=0 ):
                sql="update TIPS_CUSTINFO set "
                sql=sql+" PAYACCT         ='"+TradeContext.accno      +"'"
                sql=sql+",STATUS     ='"+'2'                     +"'"
                sql=sql+",TAXPAYNAME      ='"+TradeContext.taxPayName  +"'"
                sql=sql+",HANDORGNAME      ='"+TradeContext.handOrgName  +"'"
                sql=sql+",STARTDATE     ='"+TradeContext.workDate   +"'"
                sql=sql+",ZONENO     ='"+TradeContext.zoneno     +"'"
                sql=sql+",BRNO       ='"+TradeContext.brno       +"'"
                sql=sql+",TELLERNO   ='"+TradeContext.teller   +"'"
                if( TradeContext.existVariable( "NOTE1" ) ):
                    sql=sql+",NOTE1         ='"+TradeContext.note1   +"'"
                if( TradeContext.existVariable( "NOTE2" ) ):
                    sql=sql+",NOTE2         ='"+TradeContext.note2   +"'"
                if( TradeContext.existVariable( "NOTE3" ) ):
                    sql=sql+",NOTE3         ='"+TradeContext.note3   +"'"
                if( TradeContext.existVariable( "NOTE4" ) ):
                    sql=sql+",NOTE4         ='"+TradeContext.note4   +"'"
                if( TradeContext.existVariable( "NOTE5" ) ):
                    sql=sql+",NOTE5         ='"+TradeContext.note5   +"'"
                sql=sql+" WHERE TAXORGCODE ='"+TradeContext.taxOrgCode     +"'"
                sql=sql+" AND TAXPAYCODE ='"+TradeContext.taxPayCode     +"'"
                AfaLoggerFunc.tradeInfo(sql)
                if( AfaDBFunc.UpdateSql(sql) == -1 ):
                    AfaLoggerFunc.tradeFatal(sql)
                    return TipsFunc.ExitThisFlow( 'A0002', '���ݿ�����쳣:'+AfaDBFunc.sqlErrMsg )
            else:
                sql="insert into TIPS_CUSTINFO(TAXPAYCODE,TAXORGCODE,PROTOCOLNO,PAYACCT,IDTYPE,IDCODE,TAXPAYNAME,STATUS,"
                sql=sql+"HANDORGNAME,STARTDATE,ENDDATE,ZONENO,BRNO,TELLERNO,WORKDATE,PAYOPBKCODE,"
                sql=sql+"NOTE1,NOTE2,NOTE3,NOTE4,NOTE5)"
                sql=sql+" values"
                sql=sql+"('"+TradeContext.taxPayCode    +"'"
                sql=sql+",'"+TradeContext.taxOrgCode    +"'"
                sql=sql+",'"+TradeContext.protocolNo+"'"
                sql=sql+",'"+TradeContext.accno     +"'"
                sql=sql+",'',''"
                sql=sql+",'"+TradeContext.taxPayName +"'"
                sql=sql+",'2'" #��ʱ״̬������������֤���Ϊ1
                if( TradeContext.existVariable( "handOrgName" ) ):
                    sql=sql+",'"+TradeContext.handOrgName    +"'"
                else:
                    sql=sql+",''"
                #if( TradeContext.existVariable( "custAdd" ) ):
                #    sql=sql+",'"+TradeContext.custAdd    +"'"
                #else:
                #    sql=sql+",''"
                #if( TradeContext.existVariable( "zipCode" ) ):
                #    sql=sql+",'"+TradeContext.zipCode    +"'"
                #else:
                #    sql=sql+",''"
                #if( TradeContext.existVariable( "email" ) ):
                #    sql=sql+",'"+TradeContext.email    +"'"
                #else:
                #    sql=sql+",''"
                sql=sql+",'"+TradeContext.workDate    +"'"
                sql=sql+",''"
                sql=sql+",'"+TradeContext.zoneno      +"'"
                sql=sql+",'"+TradeContext.brno    +"'"
                sql=sql+",'"+TradeContext.teller    +"'"
                sql=sql+",'"+TradeContext.workDate    +"'"
                sql=sql+",'"+TradeContext.payOpBkCode    +"'"
                if( TradeContext.existVariable( "note1" ) ):
                    sql=sql+",'"+TradeContext.note1    +"'"
                else:
                    sql=sql+",''"
                if( TradeContext.existVariable( "note2" ) ):
                    sql=sql+",'"+TradeContext.note2    +"'"
                else:
                    sql=sql+",''"          
                if( TradeContext.existVariable( "note3" ) ):
                    sql=sql+",'"+TradeContext.note3    +"'"
                else:
                    sql=sql+",''"
                if( TradeContext.existVariable( "note4" ) ):
                    sql=sql+",'"+TradeContext.note4    +"'"
                else:
                    sql=sql+",''"
                if( TradeContext.existVariable( "note5" ) ):
                    sql=sql+",'"+TradeContext.note5    +"'"
                else:
                    sql=sql+",''"
                sql=sql+")"
                AfaLoggerFunc.tradeInfo(sql)
                records=AfaDBFunc.InsertSqlCmt(sql)
                if( records == 0 ):
                    return TipsFunc.ExitThisFlow( 'A0002', '���ݿ�����쳣:'+AfaDBFunc.sqlErrMsg )
                
                if( records == -1 ):
                    return TipsFunc.ExitThisFlow( 'A0002', '���ݿ�����쳣:'+AfaDBFunc.sqlErrMsg )
                AfaLoggerFunc.tradeInfo('***************')
        elif TradeContext.VCSign=='1':
            #=============�ж�״̬====================
            sql="SELECT STATUS"
            sql=sql+" FROM TIPS_CUSTINFO WHERE TAXPAYCODE ='"+TradeContext.taxPayCode +"'"
            sql=sql+" and PAYACCT     ='"+TradeContext.accno  +"'"
            sql=sql+" and PROTOCOLNO  ='"+TradeContext.protocolNo  +"'"
            sql=sql+" and TAXORGCODE  ='"+TradeContext.taxOrgCode  +"'"
            AfaLoggerFunc.tradeInfo(sql)
            records = AfaDBFunc.SelectSql(sql)
            if( records == None or  records <0):
                AfaLoggerFunc.tradeFatal(sql)
                return TipsFunc.ExitThisFlow( 'A0002', '���ݿ�����쳣:'+AfaDBFunc.sqlErrMsg )
            elif( len( records )==0 ):
                return TipsFunc.ExitThisFlow( 'A0027', '�ÿͻ�����Э����δ��֤���޷�����' )
            elif( len( records )>1 ):
                return TipsFunc.ExitThisFlow( 'A0027', '���ڶ�����֤��¼' )
            else:
                AfaLoggerFunc.tradeFatal(sql)
                AfaLoggerFunc.tradeInfo(records[0][0])
                UtilTools.ListFilterNone( records )
                if (records[0][0]=='0' or records[0][0]=='3'):
                    return TipsFunc.ExitThisFlow( 'A0027', '����Э��״̬Ϊ�ѳ����������ظ�����' )
            TradeContext.status = '3'
            #TradeContext.revTranF       ='0' #������
            #TradeContext.tradeType      ='U' #��Լ�ཻ��
            #TradeContext.amount         ='0' #
            #TradeContext.__agentAccno__ =''  #�跽�ʺ��ÿ�
            ##��¼ǩԼ��ˮ
            #if not TipsFunc.InsertDtl( ) :
            #    return False
            #=============�������ͨѶͨѶ====================
            #AfaAfeFunc.CommAfe()
            #TradeContext.__status__='0'
            #TradeContext.errorCode='0000'
            #TradeContext.errorMsg='���׳ɹ�'
            ##=============������ˮ��====================
            #if( not TipsFunc.UpdateDtl( 'TRADE' ) ):
            #    return False
            #if TradeContext.errorCode!='0000':
            #    return TipsFunc.ExitThisFlow(TradeContext.errorCode, TradeContext.errorMsg)
            #if TradeContext.errorCode=='0000':
            sql="update TIPS_CUSTINFO set "
            sql=sql+" STATUS     ='"+'3'                     +"'"
            sql=sql+",ENDDATE      ='"+TradeContext.workDate   +"'"
            sql=sql+",ZONENO     ='"+TradeContext.zoneno     +"'"
            sql=sql+",BRNO       ='"+TradeContext.brno       +"'"
            sql=sql+",TELLERNO   ='"+TradeContext.teller   +"'"
            sql=sql+" WHERE TAXPAYCODE ='"  +TradeContext.taxPayCode   +"'"
            sql=sql+" AND PAYACCT ='"       +TradeContext.accno        +"'"
            sql=sql+" AND PROTOCOLNO  ='"   +TradeContext.protocolNo   +"'"
            sql=sql+" AND TAXORGCODE  ='"   +TradeContext.taxOrgCode   +"'"
            AfaLoggerFunc.tradeInfo(sql)
            if( AfaDBFunc.UpdateSql(sql) == -1 ):
                AfaLoggerFunc.tradeFatal(sql)
                return TipsFunc.ExitThisFlow( 'A0002', '���ݿ�����쳣:'+AfaDBFunc.sqlErrMsg )
        #=============�Զ����==================== 
        TradeContext.errorCode='0000'
        TradeContext.errorMsg='���׳ɹ�'
        #=============�����˳�====================
        AfaLoggerFunc.tradeInfo( '�˳�����Э����֤/����['+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' )
        return True
    except TipsFunc.flowException, e:
        return False
    except Exception, e:
        return TipsFunc.ExitThisFlow('A9999','ϵͳ�쳣'+str(e) )
def SubModuleMainSnd():
    return True   
