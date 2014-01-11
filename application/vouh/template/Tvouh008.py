# -*- coding: gbk -*-
###################################################################
#    ��    ��:    Tvouh006.py
#    ˵    ��:    ������ɫ�հ���Ҫƾ֤����-->ƾ֤���Ĳ���ά��
#    ��    ��:    �м�ҵ����ƽ̨��AFA��--- UNIX: AIX 5.3
#    ��    ��:    ���ǿ
#    ��    ˾:    ������ͬ�Ƽ�
#    ������ַ:    �㶫��չ��������
#    ����ʱ��:    2007��2��28�� ������
#    ά����¼:
##################################################################
import TradeContext, AfaLoggerFunc, AfaUtilTools, AfaFunc, AfaFlowControl, AfaDBFunc
from types import *
import AfaLoggerFunc,VouhFunc,binascii

#=============���ش�����,������Ϣ===================================
def tradeExit( code, msg ):
    TradeContext.errorCode, TradeContext.errorMsg=code, msg
    if code != '0000':
        return False
    return True

def main():
    AfaLoggerFunc.tradeInfo( 'ƾ֤���Ĳ���ά��['+TradeContext.TemplateCode+']����' )
    #AfaLoggerFunc.afa_InitComp('Tvouh008','ƾ֤���Ĳ���ά��')

    try:
        #===========�����������Ƿ����===========
        # 1 ����,2 ��ѯ, 3 �޸�, 4 ɾ��
        if( not TradeContext.existVariable( "opeType" ) ):
            tradeExit( 'A005060', '��������[opeType]ֵ������!' )
            raise AfaFlowControl.flowException( )

        if TradeContext.opeType == '1': #����
            #==========����ƾ֤������Ϣ�Ƿ��Ѿ�����============
            sqlStr = "select VOUHTYPE from VOUH_PARAMETER \
                 where VOUHTYPE = '" + TradeContext.sVouhType+ "'\
                 and ZONENO = '" + TradeContext.sZoneNo+ "'"
            records = AfaDBFunc.SelectSql( sqlStr )
            if( records == None ):
                tradeExit( 'A005052', '��ѯ[ƾ֤����ά����]�����쳣!' )
                raise AfaFlowControl.flowException( )
            elif( len( records )!=0 ):
                tradeExit( 'A005053', 'ƾ֤�����Ѵ���!' )
                raise AfaFlowControl.flowException( )

            #=============��ʼ�����ر��ı���====================
            TradeContext.tradeResponse=[]
            sqlStr = "INSERT INTO VOUH_PARAMETER (ZONENO,VOUHTYPE,VOUHNAME,CTRLFLG,COUNTFLG,COUNTUNIT,PAYFLG,\
            MOVFLG,SALEFLG,PRICE,HEADLEN,VOUHLEN,ACTIVEDATE) VALUES ('"+TradeContext.sZoneNo+"','"+\
            TradeContext.sVouhType+"','"+TradeContext.sVouhName+"','2','0','0','0','0','0','0','"+\
            TradeContext.sHeadLen+"','"+TradeContext.sVouhLen+"','0')"

            records = AfaDBFunc.InsertSqlCmt( sqlStr )
            if records==-1 :
                tradeExit( 'A005054', '����[ƾ֤�����]������Ϣʧ��!' )
                raise AfaFlowControl.flowException( )
            tradeExit('0000', '�½��ɹ�')

        if TradeContext.opeType == '4':  #ɾ��
            sqlStr = "select * from VOUH_REGISTER \
                 where VOUHTYPE = '" + TradeContext.sVouhType+ "'\
                 and VOUHSTATUS != '8'"
            records = AfaDBFunc.SelectSql( sqlStr )
            AfaLoggerFunc.tradeDebug(sqlStr)
            if( records == None ):
                tradeExit( 'A005060', '��ѯ[ƾ֤�ǼǱ�]�����쳣!'  )
                raise AfaFlowControl.flowException( )
            elif( len( records ) > 0 ):
                tradeExit( 'A005061', '����ɾ��������Чƾ֤��ƾ֤����!' )
                raise AfaFlowControl.flowException( )
            sqlStr = "DELETE  FROM  VOUH_PARAMETER WHERE VOUHTYPE = '" + TradeContext.sVouhType+ "'\
                 and ZONENO = '" + TradeContext.sZoneNo+ "'"

            AfaLoggerFunc.tradeDebug(sqlStr)
            records = AfaDBFunc.DeleteSqlCmt( sqlStr )
            if records == -1:
                tradeExit( 'A005055', 'ɾ��[ƾ֤����ά����]�����쳣!' )
                raise AfaFlowControl.flowException( )
            if records == 0:
                tradeExit( 'A005056', '[ƾ֤����ά����]���޶�Ӧ��¼�ɱ�ɾ��!' )
                raise AfaFlowControl.flowException( )
            tradeExit('0000', 'ɾ���ɹ�')

        if TradeContext.opeType == '3':#�޸�
            #==============�޸�ƾ֤����ά����=====================

            sqlStr = "select * from VOUH_REGISTER \
                 where VOUHTYPE = '" + TradeContext.sVouhType+ "'\
                 and VOUHSTATUS != '8' and length(headstr) = " + TradeContext.sOldHeadLen
            records = AfaDBFunc.SelectSql( sqlStr )
            AfaLoggerFunc.tradeDebug(sqlStr)
            if( records == None ):
                tradeExit( 'A005060', '��ѯ[ƾ֤�ǼǱ�]�����쳣!'  )
                raise AfaFlowControl.flowException( )
            elif( len( records ) > 0 ):
                tradeExit( 'A005061', '�����޸Ĵ�����Чƾ֤��ƾ֤����!' )
                raise AfaFlowControl.flowException( )


            sqlStr = "UPDATE VOUH_PARAMETER set \
              VOUHNAME = '"+ TradeContext.sVouhName + "',VOUHLEN = '"+ TradeContext.sVouhLen+ "',\
              HEADLEN = '"+ TradeContext.sHeadLen+ "'"
            sqlStr = sqlStr +" WHERE VOUHTYPE = '" + TradeContext.oldVOUHTYPE + "'\
            and ZONENO = '" + TradeContext.sZoneNo+ "'"

            records = AfaDBFunc.UpdateSqlCmt( sqlStr )
            if records==-1 :
                tradeExit( 'A005057', '����[ƾ֤����ά����]��Ϣ�쳣!' )
                raise AfaFlowControl.flowException( )
            elif records==0 :
                tradeExit( 'A005058', '�޸�[ƾ֤����ά����]������Ϣʧ��!' )
                raise AfaFlowControl.flowException( )
            tradeExit('0000', '�޸ĳɹ�')

        if TradeContext.opeType == '2':#��ѯ
            #=============��ʼ�����ر��ı���====================
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
                tradeExit( 'A005052', '��ѯ[ƾ֤����ά����]�����쳣!'  )
                raise AfaFlowControl.flowException( )
            elif( len( records )==0 ):
                TradeContext.tradeResponse.append( ['retCount','0'] )
                tradeExit( 'A005059', '��ѯ[ƾ֤����ά����]������Ϣ������!' )
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
                TradeContext.tradeResponse.append( ['errorMsg', '��ѯ�ɹ�'] )
                tradeExit('0000', '��ѯ�ɹ�')

        #�Զ����
        AfaFunc.autoPackData()

        #=============�����˳�=========================================
       # AfaLoggerFunc.afa_SuccQuit(__name__,'ƾ֤���Ĳ���ά������')
    except AfaFlowControl.flowException, e:
        AfaFlowControl.exitMainFlow( )
    except AfaFlowControl.accException:
        AfaFlowControl.exitMainFlow( )
    except Exception, e:
        AfaFlowControl.exitMainFlow(str(e))