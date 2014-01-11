# -*- coding: gbk -*-
##################################################################
#   ��˰����.����Э���ѯ.���淢��
#=================================================================
#   �����ļ�:   003001_91141.py
#   �޸�ʱ��:   2006-04-05
##################################################################
import TradeContext, AfaLoggerFunc, UtilTools, TipsFunc,AfaDBFunc
from types import *

def SubModuleMainFst( ):

    AfaLoggerFunc.tradeInfo( '����ͻ�ǩԼ��ѯ[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' )
    try:
        #=============��ȡ��ǰϵͳʱ��====================
        TradeContext.workDate=UtilTools.GetSysDate( )
        TradeContext.workTime=UtilTools.GetSysTime( )

          #============У�鹫���ڵ����Ч��==================
        # �����Լ��
        if( not TradeContext.existVariable( "channelCode" ) ):
            return TipsFunc.ExitThisFlow( 'A0001', '��������[channelCode]ֵ������!' )
        if( not TradeContext.existVariable( "zoneno" ) ):
            return TipsFunc.ExitThisFlow( 'A0001', '���к�[zoneno]ֵ������!' )
        if( not TradeContext.existVariable( "brno" ) ):
            return TipsFunc.ExitThisFlow( 'A0001', '������[brno]ֵ������!' )
        if( not TradeContext.existVariable( "opType" ) ):
            return TipsFunc.ExitThisFlow( 'A0001', '��������[opType]ֵ������!' )
        if( not TradeContext.existVariable( "taxOrgCode" ) ):
            return TipsFunc.ExitThisFlow( 'A0001', '���ջ��ش���[taxOrgCode]ֵ������!' )
        if( not TradeContext.existVariable( "taxPayCode" ) ):
            return TipsFunc.ExitThisFlow( 'A0001', '��˰�˱���[taxPayCode]ֵ������!' )
        if( not TradeContext.existVariable( "accno" ) ):
            return TipsFunc.ExitThisFlow( 'A0001', '�����˻�[accno]ֵ������!' )
        if( not TradeContext.existVariable( "protocolNo" ) ):
            return TipsFunc.ExitThisFlow( 'A0001', 'Э�����[protocolNo]ֵ������!' )

        if TradeContext.opType=='0':
            AfaLoggerFunc.tradeInfo('>>>��ѯ')
            #=============�ж�״̬====================
            sql="SELECT STATUS,TAXPAYCODE,PROTOCOLNO,PAYACCT,IDTYPE,IDCODE,TAXPAYNAME,"
            sql=sql+"TAXORGCODE,HANDORGNAME,STARTDATE,ENDDATE,ZONENO,BRNO,TELLERNO,WORKDATE,"
            sql=sql+"NOTE1,NOTE2,NOTE3,NOTE4,NOTE5"
            sql=sql+" FROM TIPS_CUSTINFO WHERE 1=1 "
            sql=sql+" and TAXORGCODE     ='"+TradeContext.taxOrgCode  +"'"
            
            if( len(TradeContext.taxPayCode) != 0 ):
            	AfaLoggerFunc.tradeInfo('>>>' + TradeContext.taxPayCode)
            	sql=sql+" AND TAXPAYCODE ='"+TradeContext.taxPayCode +"'"
            if( len(TradeContext.accno) != 0 ):
            	sql=sql+" and PAYACCT     ='"+TradeContext.accno  +"'"
            if( len(TradeContext.protocolNo) != 0 ):
            	sql=sql+" and PROTOCOLNO     ='"+TradeContext.protocolNo  +"'"
            
            AfaLoggerFunc.tradeInfo(sql)
            records = AfaDBFunc.SelectSql(sql)
            if( records == None ):
                AfaLoggerFunc.tradeFatal(sql)
                return TipsFunc.ExitThisFlow( 'A0002', '���ݿ�����쳣:'+AfaDBFunc.sqlErrMsg )
            elif( len( records )==0 ):
                return TipsFunc.ExitThisFlow( 'A0027', '�ÿͻ���δǩԼ' )
            elif( len( records )>1 ):
                return TipsFunc.ExitThisFlow( 'A0027', '���ڶ���ǩԼ��¼' )
            else:
                AfaLoggerFunc.tradeFatal(sql)
                AfaLoggerFunc.tradeInfo(records[0][0])
                UtilTools.ListFilterNone( records )
                if (records[0][0]=='1'):
                    TradeContext.status='Э������֤��������ʹ��'
                elif (records[0][0]=='2'):
                    TradeContext.status='���ж���ǩԼ���ȴ����ջ�����֤Э��'
                elif (records[0][0]=='3'):
                    TradeContext.status='���ж��ѽ�Լ���ȴ����ջ��س���Э��'
                else:
                    TradeContext.status='Э���ѳ���'
                TradeContext.taxPayCode =records[0][1]
                TradeContext.protocolNo =records[0][2]
                TradeContext.accno      =records[0][3]
                TradeContext.idType     =records[0][4]
                TradeContext.idCode     =records[0][5]
                TradeContext.taxPayName =records[0][6]
                TradeContext.taxOrgCode =records[0][7]
                TradeContext.handOrgName =records[0][8]
                TradeContext.workDate = records[0][14]
                TradeContext.note2      =records[0][16]
                
                TipsFunc.GetTaxOrg(TradeContext.taxOrgCode)
        elif TradeContext.opType=='1':
            AfaLoggerFunc.tradeInfo('>>>ɾ��')
            #=============�ж�״̬====================
            sql="SELECT STATUS,TAXPAYCODE,PROTOCOLNO,PAYACCT,IDTYPE,IDCODE,TAXPAYNAME,"
            sql=sql+"TAXORGCODE,HANDORGNAME,STARTDATE,ENDDATE,ZONENO,BRNO,TELLERNO,WORKDATE,"
            sql=sql+"NOTE1,NOTE2,NOTE3,NOTE4,NOTE5"
            sql=sql+" FROM TIPS_CUSTINFO WHERE TAXORGCODE  ='"+TradeContext.taxOrgCode +"'"
            
            if( len(TradeContext.taxPayCode) != 0 ):
            	AfaLoggerFunc.tradeInfo('>>>' + TradeContext.taxPayCode)
            	sql=sql+" AND TAXPAYCODE ='"+TradeContext.taxPayCode +"'"
            if( len(TradeContext.accno) != 0 ):
            	sql=sql+" and PAYACCT     ='"+TradeContext.accno  +"'"
            if( len(TradeContext.protocolNo) != 0 ):
            	sql=sql+" and PROTOCOLNO     ='"+TradeContext.protocolNo  +"'"

            AfaLoggerFunc.tradeInfo(sql)
            records = AfaDBFunc.SelectSql(sql)
            if( records == None or  records <0):
                AfaLoggerFunc.tradeFatal(sql)
                return TipsFunc.ExitThisFlow( 'A0002', '���ݿ�����쳣:'+AfaDBFunc.sqlErrMsg )
            elif( len( records )==0 ):
                #return TipsFunc.ExitThisFlow( 'A0027', '�ÿͻ�����Э����δǩԼ���޷�����' )
                return TipsFunc.ExitThisFlow( 'A0027', '�ÿͻ�����Э����δǩԼ���޷�ɾ��' )
            elif( len( records )>1 ):
                return TipsFunc.ExitThisFlow( 'A0027', '���ڶ�����֤��¼' )
            else:
                AfaLoggerFunc.tradeFatal(sql)
                AfaLoggerFunc.tradeInfo(records[0][0])
                UtilTools.ListFilterNone( records )
                #if (records[0][0]=='0' or records[0][0]=='3'):
                #    return TipsFunc.ExitThisFlow( 'A0027', '����Э��״̬Ϊ�ѳ����������ظ�����' )
                if (records[0][0]=='1'):
                    #return TipsFunc.ExitThisFlow( 'A0027', '����Э��״̬Ϊ����֤�����ܳ���' )
                    return TipsFunc.ExitThisFlow( 'A0027', '����Э��״̬Ϊ����֤������ɾ����������Լ����' )
            TradeContext.taxPayCode =records[0][1]
            TradeContext.protocolNo =records[0][2]
            TradeContext.accno      =records[0][3]
            TradeContext.idType     =records[0][4]
            TradeContext.idCode     =records[0][5]
            TradeContext.taxPayName =records[0][6]
            TradeContext.taxOrgCode =records[0][7]
            TradeContext.handOrgName =records[0][8]
            TradeContext.workDate = records[0][14]
            TradeContext.note2      =records[0][16]
            TipsFunc.GetTaxOrg(TradeContext.taxOrgCode)
            TradeContext.status = 'ɾ���ɹ�'

            #sql="update TIPS_CUSTINFO set "
            #sql=sql+" STATUS     ='"+'3'                     +"'"
            #sql=sql+",ENDDATE      ='"+TradeContext.workDate   +"'"
            #sql=sql+",ZONENO     ='"+TradeContext.zoneno     +"'"
            #sql=sql+",BRNO       ='"+TradeContext.brno       +"'"
            #sql=sql+",TELLERNO   ='"+TradeContext.teller   +"'"
            #sql=sql+" WHERE TAXPAYCODE ='"  +TradeContext.taxPayCode   +"'"
            #sql=sql+" AND PAYACCT ='"       +TradeContext.accno        +"'"
            #sql=sql+" AND PROTOCOLNO  ='"   +TradeContext.protocolNo   +"'"
            #sql=sql+" AND TAXORGCODE  ='"   +TradeContext.taxOrgCode   +"'"
            #AfaLoggerFunc.tradeInfo(sql)
            #if( AfaDBFunc.UpdateSqlCmt(sql) == -1 ):
            #    AfaLoggerFunc.tradeFatal(sql)
            #    return TipsFunc.ExitThisFlow( 'A0002', '���ݿ�����쳣:'+AfaDBFunc.sqlErrMsg )
            sql="delete "
            sql="DELETE FROM TIPS_CUSTINFO WHERE TAXORGCODE  ='"+TradeContext.taxOrgCode +"'"
            
            if( len(TradeContext.taxPayCode) != 0 ):
            	AfaLoggerFunc.tradeInfo('>>>' + TradeContext.taxPayCode)
            	sql=sql+" AND TAXPAYCODE ='"+TradeContext.taxPayCode +"'"
            if( len(TradeContext.accno) != 0 ):
            	sql=sql+" and PAYACCT     ='"+TradeContext.accno  +"'"
            if( len(TradeContext.protocolNo) != 0 ):
            	sql=sql+" and PROTOCOLNO     ='"+TradeContext.protocolNo  +"'"

            AfaLoggerFunc.tradeInfo(sql)
            rec=AfaDBFunc.DeleteSqlCmt(sql)
            if rec<0:
                return TipsFunc.ExitThisFlow( 'A0002', '���ݿ�����쳣:'+AfaDBFunc.sqlErrMsg )
            
        else:
            return TipsFunc.ExitThisFlow('0001', 'δ����ò�������')
            
        #=============�Զ����==================== 
        TradeContext.errorCode='0000'
        TradeContext.errorMsg='���׳ɹ�'
        #=============�����˳�====================
        AfaLoggerFunc.tradeInfo( '�˳��ͻ���Ϣά��ģ��['+TradeContext.TemplateCode+']\n' )
        return True
    except TipsFunc.flowException, e:
        TipsFunc.exitMainFlow( )
    except TipsFunc.accException:
        TipsFunc.exitMainFlow( )
    except Exception, e:
        TipsFunc.exitMainFlow(str(e))  
def SubModuleMainSnd():
    return True   