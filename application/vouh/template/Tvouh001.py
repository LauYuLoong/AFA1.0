# -*- coding: gbk -*-
###################################################################
#    ��    ��:    Tvouh001.py
#    ˵    ��:    ƾ֤����-->ƾ֤���Ĳ���ά��
#    ��    ��:    �м�ҵ����ƽ̨��AFA��--- UNIX: AIX 5.3
#    ��    ��:    ���ǽ�
#    ��    ˾:    ������ͬ�Ƽ�
#    ������ַ:    ����
#    ����ʱ��:    2008��6��12��
#    ά����¼:
##################################################################
import TradeContext, AfaLoggerFunc, AfaUtilTools, AfaFunc, AfaFlowControl, AfaDBFunc
from types import *
import VouhFunc,HostContext,VouhHostFunc

#=============���ش�����,������Ϣ===================================
def tradeExit( code, msg ):
    TradeContext.errorCode, TradeContext.errorMsg=code, msg
    if code != '0000':
        return False
    return True

def main():
    AfaLoggerFunc.tradeInfo( 'ƾ֤���Ĳ���ά��['+TradeContext.TemplateCode+']����' )
    
    #=============ǰ̨��������===================================
    #TradeContext.sBesbNo                                 ������
    #TradeContext.sTellerNo                               ��Ա��
    #TradeContext.opeType                                 ��������
    #TradeContext.sVouhType                               ƾ֤����
    #TradeContext.sVouhName                               ƾ֤����
    #TradeContext.sNum                                    �ظ�����
    

    #=============��ȡ��ǰϵͳʱ��==========================
    TradeContext.sLstTrxDay  = AfaUtilTools.GetSysDate( )
    TradeContext.sLstTrxTime = AfaUtilTools.GetSysTime( )
        
    try:        
        #=============��ȡ��������==========================
        HostContext.I1OTSB = TradeContext.sBesbNo         #������
        HostContext.I1SBNO = TradeContext.sBesbNo         #������
        HostContext.I1USID = TradeContext.sTellerNo       #��Ա��
        HostContext.I1WSNO = TradeContext.sWSNO           #�ն˺�
        
        if(not VouhHostFunc.CommHost('2001')):
            VouhFunc.tradeExit( TradeContext.errorCode, TradeContext.errorMsg )
            raise AfaFlowControl.flowException( )
        if(TradeContext.errorCode == '0000'):
            SBNO = HostContext.O1SBCH
            AfaLoggerFunc.tradeInfo( SBNO )
            
        #beginƾ֤�Ż�����LLJ  201109     
        #=============��ȡ��Աβ���===============================
        HostContext.I1SBNO = TradeContext.sBesbNo         #������
        HostContext.I1USID = TradeContext.sTellerNo       #��Ա��
        HostContext.I1WSNO = TradeContext.sWSNO           #�ն˺�
        HostContext.I1EDDT = TradeContext.sLstTrxDay      #��ֹ����
        HostContext.I1TELR = TradeContext.sTellerNo       #��Ա����
        
        if(not VouhHostFunc.CommHost('0104')):
            VouhFunc.tradeExit( TradeContext.errorCode, TradeContext.errorMsg )
            raise AfaFlowControl.flowException( )
        if(TradeContext.errorCode == '0000'):
            TradeContext.sTellerTailNobak = HostContext.O2CABO
            TradeContext.sTellerTailNo    = TradeContext.sTellerTailNobak[0]                 #��Աβ���TradeContext.sTellerTailNo
            AfaLoggerFunc.tradeInfo( '��Աβ��ţ�' + TradeContext.sTellerTailNo )   
        #end 
        
        #=============��ʼ�����ر��ı���========================
        TradeContext.tradeResponse = []
        
        #================���========================
        if(TradeContext.existVariable("sVouhType")):
            TradeContext.sVouhType = VouhFunc.DelSpace(TradeContext.sVouhType.split("|"))
            TradeContext.sNum = len(TradeContext.sVouhType)
        if(TradeContext.existVariable("sVouhName")):
            TradeContext.sVouhName  = VouhFunc.DelSpace(TradeContext.sVouhName.split("|"))
        AfaLoggerFunc.tradeInfo( '=================='+str(TradeContext.sNum) )
        
        #===========�����������Ƿ����===========
        # 1 ����,2 ɾ��, 3 �޸�, 4 ��ѯ
        if( not TradeContext.existVariable( "opeType" ) ):
            tradeExit( 'A005060', '��������[opeType]ֵ������!' )
            raise AfaFlowControl.flowException( )

        if TradeContext.opeType == '1': #����
        
            if(SBNO <> '33' and SBNO <> '02' ):
                tradeExit( 'A0001', '�û�����Ա���ܽ��д˲���!' )
                raise AfaFlowControl.flowException( )
        
            n=0
        
            for i in range(TradeContext.sNum):
                n=n+1
                #==========����ƾ֤������Ϣ�Ƿ��Ѿ�����============
                sqlStr = "select VOUHTYPE from VOUH_PARAMETER \
                     where VOUHTYPE = '" + TradeContext.sVouhType[i] + "'\
                     and BESBNO = '" + TradeContext.sBesbNo + "'"
                AfaLoggerFunc.tradeInfo( 'sql = ' + sqlStr )
                records = AfaDBFunc.SelectSql( sqlStr )
                if( records == None ):
                    if(n>1):
                        AfaLoggerFunc.tradeInfo( '���ݿ�ع�' )
                        AfaDBFunc.RollbackSql( )
                    tradeExit( 'A005052', '��ѯ[ƾ֤����ά����]�����쳣!' )
                    raise AfaFlowControl.flowException( )
                elif( len( records )!=0 ):
                    if(n>1):
                        AfaLoggerFunc.tradeInfo( '���ݿ�ع�' )
                        AfaDBFunc.RollbackSql( )
                    tradeExit( 'A005053', 'ƾ֤�����Ѵ���!' )
                    raise AfaFlowControl.flowException( )
                    
                #==========����ƾ֤������Ϣ�Ƿ��Ѿ�����============
                sqlStr = "select VOUHNAME from VOUH_PARAMETER \
                     where trim(VOUHNAME) = trim('" + TradeContext.sVouhName[i] + "')\
                     and BESBNO = '" + TradeContext.sBesbNo + "'"
                AfaLoggerFunc.tradeInfo( 'sql = ' + sqlStr )
                records = AfaDBFunc.SelectSql( sqlStr )
                if( records == None ):
                    if(n>1):
                        AfaLoggerFunc.tradeInfo( '���ݿ�ع�' )
                        AfaDBFunc.RollbackSql( )
                    tradeExit( 'A005052', '��ѯ[ƾ֤����ά����]�����쳣!' )
                    raise AfaFlowControl.flowException( )
                elif( len( records )!=0 ):
                    if(n>1):
                        AfaLoggerFunc.tradeInfo( '���ݿ�ع�' )
                        AfaDBFunc.RollbackSql( )
                    tradeExit( 'A005053', 'ƾ֤�����Ѵ���!' )
                    raise AfaFlowControl.flowException( )
                
                #=============��ʼ�����ر��ı���====================
                TradeContext.tradeResponse=[]
                sqlStr = "INSERT INTO VOUH_PARAMETER (BESBNO,VOUHTYPE,VOUHNAME,TELLERNO,ACTIVEDATE,STATUS) VALUES ('"+TradeContext.sBesbNo+"','"+\
                TradeContext.sVouhType[i]+"','"+TradeContext.sVouhName[i]+"','"+TradeContext.sTellerTailNo+"','"+TradeContext.sLstTrxDay+"','1')"
                
                AfaLoggerFunc.tradeInfo( sqlStr )
                records = AfaDBFunc.InsertSql( sqlStr )
                
                if records < 0 :
                    AfaLoggerFunc.tradeInfo( '���ݿ�ع�' )
                    AfaDBFunc.RollbackSql( )
                    tradeExit( 'A005054', '����[ƾ֤�����]������Ϣʧ��!' )
                    raise AfaFlowControl.flowException( )
            #���ݿ��ύ
            AfaLoggerFunc.tradeInfo( '------------���ݿ��ύ' )
            AfaDBFunc.CommitSql( )
            
            TradeContext.tradeResponse.append( ['sNum',str(TradeContext.sNum)] )
            TradeContext.tradeResponse.append( ['sLstTrxDay',TradeContext.sLstTrxDay] )
            TradeContext.tradeResponse.append( ['sLstTrxTime',TradeContext.sLstTrxTime] )
            TradeContext.tradeResponse.append( ['errorCode','0000'] )
            TradeContext.tradeResponse.append( ['errorMsg','���׳ɹ�'] )

        if TradeContext.opeType == '3':  #ɾ��
            
            if(SBNO <> '33' and SBNO <> '02' ):
                tradeExit( 'A0001', '�û�����Ա���ܽ��д˲���!' )
                raise AfaFlowControl.flowException( )
                
            n = 0
            for i in range(TradeContext.sNum):
                n=n+1
                sqlStr = "select * from VOUH_REGISTER \
                     where VOUHTYPE = '" + TradeContext.sVouhType[i]+ "' \
                     and VOUHSTATUS <> '6' \
                     and BESBNO = '"+TradeContext.sBesbNo+"'"
                records = AfaDBFunc.SelectSql( sqlStr )
                AfaLoggerFunc.tradeDebug(sqlStr)
                if( records == None ):
                    if(n>1):
                        AfaLoggerFunc.tradeInfo( '���ݿ�ع�' )
                        AfaDBFunc.RollbackSql( )
                    tradeExit( 'A005060', '��ѯ[ƾ֤�ǼǱ�]�����쳣!'  )
                    raise AfaFlowControl.flowException( )
                elif( len( records ) > 0 ):
                    if(n>1):
                        AfaLoggerFunc.tradeInfo( '���ݿ�ع�' )
                        AfaDBFunc.RollbackSql( )
                    tradeExit( 'A005061', '����ɾ��������Чƾ֤��ƾ֤����!' )
                    raise AfaFlowControl.flowException( )
                sqlStr = "DELETE  FROM  VOUH_PARAMETER WHERE VOUHTYPE = '" + TradeContext.sVouhType[i]+ "'\
                     and BESBNO = '" + TradeContext.sBesbNo+ "'"
                
                AfaLoggerFunc.tradeDebug(sqlStr)
                records = AfaDBFunc.DeleteSql( sqlStr )
                if records == -1:
                    AfaLoggerFunc.tradeInfo( '���ݿ�ع�' )
                    AfaDBFunc.RollbackSql( )
                    tradeExit( 'A005055', 'ɾ��[ƾ֤����ά����]�����쳣!' )
                    raise AfaFlowControl.flowException( )
                if records == 0:
                    AfaLoggerFunc.tradeInfo( '���ݿ�ع�' )
                    AfaDBFunc.RollbackSql( )
                    tradeExit( 'A005056', '[ƾ֤����ά����]���޶�Ӧ��¼�ɱ�ɾ��!' )
                    raise AfaFlowControl.flowException( )
                
            #���ݿ��ύ
            AfaLoggerFunc.tradeInfo( '------------���ݿ��ύ' )
            AfaDBFunc.CommitSql( )
            
            TradeContext.tradeResponse.append( ['sNum',str(TradeContext.sNum)] )
            TradeContext.tradeResponse.append( ['sLstTrxDay',TradeContext.sLstTrxDay] )
            TradeContext.tradeResponse.append( ['sLstTrxTime',TradeContext.sLstTrxTime] )
            TradeContext.tradeResponse.append( ['errorCode','0000'] )
            TradeContext.tradeResponse.append( ['errorMsg','���׳ɹ�'] )

        if TradeContext.opeType == '2':#�޸�
        
            if(SBNO <> '33' and SBNO <> '02' ):
                tradeExit( 'A0001', '�û�����Ա���ܽ��д˲���!' )
                raise AfaFlowControl.flowException( )
                
            n=0     
            #==============�޸�ƾ֤����ά����=====================
            for i in range(TradeContext.sNum):
                n=n+1

                #==========����ƾ֤������Ϣ�Ƿ��Ѿ�����============
                sqlStr = "select VOUHNAME from VOUH_PARAMETER \
                     where trim(VOUHNAME) = trim('" + TradeContext.sVouhName[i] + "')\
                     and BESBNO = '" + TradeContext.sBesbNo + "'"
                AfaLoggerFunc.tradeInfo( 'sql = ' + sqlStr )
                records = AfaDBFunc.SelectSql( sqlStr )
                if( records == None ):
                    if(n>1):
                        AfaLoggerFunc.tradeInfo( '���ݿ�ع�' )
                        AfaDBFunc.RollbackSql( )
                    tradeExit( 'A005052', '��ѯ[ƾ֤����ά����]�����쳣!' )
                    raise AfaFlowControl.flowException( )
                elif( len( records )!=0 ):
                    if(n>1):
                        AfaLoggerFunc.tradeInfo( '���ݿ�ع�' )
                        AfaDBFunc.RollbackSql( )
                    tradeExit( 'A005053', 'ƾ֤�����Ѵ���!' )
                    raise AfaFlowControl.flowException( )
                
                sqlStr = "UPDATE VOUH_PARAMETER set \
                  VOUHNAME = '"+ TradeContext.sVouhName[i] + "'"
                sqlStr = sqlStr +" WHERE VOUHTYPE = '" + TradeContext.sVouhType[i] + "'\
                and BESBNO = '" + TradeContext.sBesbNo+ "'"
                
                records = AfaDBFunc.UpdateSql( sqlStr )
                if records==-1 :
                    AfaLoggerFunc.tradeInfo( '���ݿ�ع�' )
                    AfaDBFunc.RollbackSql( )
                    tradeExit( 'A005057', '����[ƾ֤����ά����]��Ϣ�쳣!' )
                    raise AfaFlowControl.flowException( )
                elif records==0 :
                    AfaLoggerFunc.tradeInfo( '���ݿ�ع�' )
                    AfaDBFunc.RollbackSql( )
                    tradeExit( 'A005058', '�޸�[ƾ֤����ά����]������Ϣʧ��!' )
                    raise AfaFlowControl.flowException( )
            #���ݿ��ύ
            AfaLoggerFunc.tradeInfo( '------------���ݿ��ύ' )
            AfaDBFunc.CommitSql( )
            
            TradeContext.tradeResponse.append( ['sNum',str(TradeContext.sNum)] )
            TradeContext.tradeResponse.append( ['sLstTrxDay',TradeContext.sLstTrxDay] )
            TradeContext.tradeResponse.append( ['sLstTrxTime',TradeContext.sLstTrxTime] )
            TradeContext.tradeResponse.append( ['errorCode','0000'] )
            TradeContext.tradeResponse.append( ['errorMsg','���׳ɹ�'] )

        if TradeContext.opeType == '4':#��ѯ
              
            TradeContext.tradeResponse=[]
            sqlStr = "SELECT VOUHTYPE,VOUHNAME,BESBNO FROM VOUH_PARAMETER WHERE (SUBSTR(BESBNO,1,6) = '"+ (TradeContext.sBesbNo)[:6] +"' \
                    or BESBNO ='3400008887')"
            if (len(TradeContext.sVouhType)!=0 and len(TradeContext.sVouhType[0])!=0):
                sqlStr = sqlStr + " AND VOUHTYPE = '" + TradeContext.sVouhType[0] + "' AND STATUS = '1'"
            
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

                sTotal=len( records )
                sVouhType = ''
                sVouhName = ''
                sBESBNO = ''
                for i in range( 0, len( records ) ):
                    if( i <> 0):
                        strSplit = '|'
                    else:
                        strSplit = ''
                    sVouhType = sVouhType + strSplit + records[i][0]
                    sVouhName = sVouhName + strSplit + records[i][1]
                    sBESBNO = sBESBNO + strSplit + records[i][2]
                
                TradeContext.tradeResponse.append( ['sVouhType',sVouhType] )
                TradeContext.tradeResponse.append( ['sVouhName',sVouhName] )
                TradeContext.tradeResponse.append( ['sBESBNO',sBESBNO] )
                TradeContext.tradeResponse.append( ['sLstTrxDay',TradeContext.sLstTrxDay] )
                TradeContext.tradeResponse.append( ['sLstTrxTime',TradeContext.sLstTrxTime] )
                TradeContext.tradeResponse.append( ['sTotal',str(sTotal)] )
                TradeContext.tradeResponse.append( ['errorCode','0000'] )
                TradeContext.tradeResponse.append( ['errorMsg','��ѯ�ɹ�'] )

                tradeExit('0000', '��ѯ�ɹ�')

        #�Զ����
        AfaFunc.autoPackData()

        #=============�����˳�=========================================
        AfaLoggerFunc.tradeInfo( 'ƾ֤���Ĳ���ά��['+TradeContext.TemplateCode+']�˳�' )
    except AfaFlowControl.flowException, e:
        AfaFlowControl.exitMainFlow( )
    except AfaFlowControl.accException:
        AfaFlowControl.exitMainFlow( )
    except Exception, e:
        AfaFlowControl.exitMainFlow(str(e))
