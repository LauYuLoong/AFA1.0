# -*- coding: gbk -*-
##################################################################
#   ���մ���ƽ̨.���׷�Ʊ�������
#=================================================================
#   �����ļ�:   TransBillFunc.py
#   �޸�ʱ��:   2006-03-31
##################################################################
import TradeContext, TradeFunc, AfaLoggerFunc, sys, AfaDBFunc

################################################################################
# ������:    InsertBill
# ����:      billData       ��Ʊ����
#            billData       �������ͱ���Ϊlist
#            billData[0]    ��Ʊ����
#            billData[1]    ��Ʊ������item1������
#                           ���billData[0]==1,��ֻ��һ�ŷ�Ʊ��billData[1]����ΪString�ͱ���
#                           ���billData[0]>1,��һ�ʽ����ж��ŷ�Ʊ���ҷ�Ʊ��item1�б���������ݣ�
#                           ����˵��item1��ʾ���ڣ�ÿ�ŷ�Ʊ�����ڶ�����ͬ����ôbillData[1]ӦΪlist��
#                           ���ÿ�ŷ�Ʊ�����ڶ���ͬ��billData[1]����ΪString
#                           ���item1��δʹ�ã�billData[1]ӦΪ''
#                           ��billData[1]Ϊlistʱ
#                           billData[1][j]�д洢���ǵ�j�ŷ�Ʊ�Ķ�Ӧitem1����Ϣ
#                           billData[1][j]ӦΪString��
#           billData[2]     ��Ʊ������item2�����ݣ�˵����billData[1]����
#           billData[3]     ��Ʊ������item3�����ݣ�˵����billData[1]����
#           billData[4]     ��Ʊ������item4�����ݣ�˵����billData[1]����
#           billData[5]     ��Ʊ������item5�����ݣ�˵����billData[1]����
#           billData[6]     ��Ʊ������item6�����ݣ�˵����billData[1]����
#           billData[7]     ��Ʊ������billData�����ݣ�˵����billData[1]����
# ����ֵ��    True  ���뷢Ʊ��ɹ�    False ���뷢Ʊ��ʧ��
# ����˵����  ����Ʊ��Ϣ���뷢Ʊ����һ�β���һ�Ż��߶��ŷ�Ʊ��Ϣ
################################################################################
def InsertBill( billData ):

    AfaLoggerFunc.tradeInfo( '>>>���뷢Ʊ��Ϣ[begin]' )

    # count ��Ʊ�������-1
    if( int( TradeContext.__billSaveCtl__ ) == 0 ):
            return True

    if( billData is None or ( type( billData ) is not list and type( billData ) is not tuple ) or len( billData )<8 ):
           TradeContext.errorCode, TradeContext.errorMsg='A0040', '��Ʊ�����쳣'
           return False

    count=17
    BillDtl=[[]]*( count+1 )
    BillDtl[0] = TradeContext.agentSerialno             # SERIALNO      ����ҵ����ˮ��
    BillDtl[1] = TradeContext.sysId                     # APPNO         ҵ�����  
    BillDtl[2] = TradeContext.unitno                    # BUSINO        ��λ����
    
    if( TradeContext.existVariable( "subUnitno" ) ):
        BillDtl[3] = TradeContext.subUnitno             # SUBUNITNO     �ӵ�λ����
    else:
        BillDtl[3] = ''

    BillDtl[4] = TradeContext.workDate                  # WORKDATE      �������� yyyymmdd
    BillDtl[5] = TradeContext.workTime                  # WORKTIME      ����ʱ��  
    BillDtl[6] = TradeContext.userno                    # USERNO        �û��� 

    if( TradeContext.existVariable( "userName" ) ):
        BillDtl[7] = TradeContext.userName              # USERNAME      �û�����  
    else:
        BillDtl[7] = '' 

    BillDtl[8] = '0'                                    # BILLSTATUS    ��Ʊ״̬(0.���� 1.����)
    BillDtl[9] = '0'                                    # PRTNUM        ��ӡ����

    sql = "INSERT INTO AFA_BILLDTL(SERIALNO,SYSID,UNITNO,SUBUNITNO,WORKDATE,WORKTIME,USERNO,USERNAME,BILLSTATUS,PRTNUM,ITEM1,ITEM2,ITEM3,ITEM4,ITEM5,ITEM6,BILLSERNO,BILLDATA) VALUES("

    #��Ʊ����
    billCount=int( billData[0] )
    if ( billCount < 1 ):
        TradeContext.errorCode, TradeContext.errorMsg='A0038', '��Ʊ��������'
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

                TradeContext.errorCode, TradeContext.errorMsg='A0039', '���뷢Ʊ��ʧ��' + AfaDBFunc.sqlErrMsg
                return False

        AfaDBFunc.CommitSql( ) 

        AfaLoggerFunc.tradeInfo( '���뷢Ʊ��Ϣ[end]' )

        return True 

    except Exception, e:
        AfaLoggerFunc.tradeFatal( e )

        TradeContext.errorCode, TradeContext.errorMsg='A0040', '��Ʊ�����쳣'

        AfaDBFunc.RollbackSql( )

        return False  


################################################################################
# ������:    UpdateBill
# ����:      whereClause ����Ϊ��
# ����ֵ��    True  ���·�Ʊ��ɹ�    False ���·�Ʊ��ʧ��
# ����˵����  ���·�Ʊ��,����Ƿ�����,��TradeContext.preAgentSernoԭ������ˮ��Ӧ�ķ�Ʊ��Ϣ����Ϊ����״̬
#           ����ǲ���Ʊ��whereClauseָ���ķ�Ʊ��¼�Ĵ�ӡ������1
################################################################################
def UpdateBill( ):

    AfaLoggerFunc.tradeInfo( '>>>���·�Ʊ��Ϣ[begin]' )
        
    if( TradeContext.existVariable( "revTranF" ) and TradeContext.revTranF == '1' ):
        
        if( int( TradeContext.__billSaveCtl__ ) == 0 ):
            return True

        sql="UPDATE AFA_BILLDTL SET BILLSTATUS='1' WHERE WORKDATE='" + TradeContext.workDate + "' AND SERIALNO='" + TradeContext.preAgentSerno + "'"

    else:

        #�ж��޸ķ�Ʊ����
        if( not TradeContext.existVariable( "whereClause" ) ):
            TradeContext.errorCode, TradeContext.errorMsg='A0041', '��ڲ��������Ƿ�����ڲ�������Ϊ��'
            return False

            
        #����Ʊʱʹ��
        if( TradeContext.whereClause == '' ):
            TradeContext.errorCode, TradeContext.errorMsg='A0041', '��ڲ���������������ڲ�������Ϊ��'
            return False

        sql="UPDATE AFA_BILLDTL SET PRTNUM=char(int(PRTNUM)+1) WHERE " + whereClause

    AfaLoggerFunc.tradeInfo( sql )

    if( AfaDBFunc.UpdateSqlCmt( sql ) < 1 ):
        
        TradeContext.errorCode, TradeContext.errorMsg='A0042', '���·�Ʊ��Ϣ��ʧ��'+AfaDBFunc.sqlErrMsg
        
        return False

    AfaLoggerFunc.tradeInfo( '>>>���·�Ʊ��Ϣ[end]' )
    
    return True
