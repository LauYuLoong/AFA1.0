# -*- coding: gbk -*-
###################################################################
#    ��    ��:    Tvouh002.py
#    ˵    ��:    ƾ֤����-->ƾ֤���
#    ��    ��:    �м�ҵ����ƽ̨��AFA��--- UNIX: AIX 5.3
#    ��    ��:    ���ǽ�
#    ��    ˾:    ������ͬ�Ƽ�
#    ������ַ:    ����
#    ����ʱ��:    2008��6��11�� 
#    ά����¼:   
##################################################################
import TradeContext, AfaLoggerFunc, AfaUtilTools, AfaFunc, AfaFlowControl, AfaDBFunc
from types import *
import VouhFunc,VouhHostFunc,HostContext

#=============���ش�����,������Ϣ===================================
def tradeExit( code, msg ):
    TradeContext.errorCode, TradeContext.errorMsg=code, msg
    if code != '0000':
        return False
    return True

def main( ):
    AfaLoggerFunc.tradeInfo( 'ƾ֤���['+TradeContext.TemplateCode+']����' )

    #=============ǰ̨��������===================================
    #TradeContext.sBesbNo                                 ������
    #TradeContext.sCur                                    ���Ҵ���
    #TradeContext.sTellerNo                               ��Ա��
    #TradeContext.sVouhType                               ƾ֤����
    #TradeContext.sVouhName                               ƾ֤����
    #TradeContext.sStartNo                                ��ʼ����
    #TradeContext.sEndNo                                  ��ֹ����
    #TradeContext.sRivTeller                              �Է���Ա
    #TradeContext.sVouhStatus                             ƾ֤״̬
    #TradeContext.sVouhNum                                ƾ֤����
    #TradeContext.sLstTrxDay                              ���������
    #TradeContext.sLstTrxTime                             �����ʱ��
    #TradeContext.sDepository                             �����־
    #TradeContext.sVouhName                               ƾ֤����
    
    try:
        
        #================���========================
        TradeContext.sVouhType = VouhFunc.DelSpace(TradeContext.sVouhType.split("|")) 
        TradeContext.sVouhName = VouhFunc.DelSpace(TradeContext.sVouhName.split("|"))
        TradeContext.sStartNo  = VouhFunc.DelSpace(TradeContext.sStartNo.split("|"))
        TradeContext.sEndNo    = VouhFunc.DelSpace(TradeContext.sEndNo.split("|"))
        TradeContext.sVouhNum  = VouhFunc.DelSpace(TradeContext.sVouhNum.split("|"))
        TradeContext.sNum      = len(TradeContext.sVouhType)
        
        #==================�ݴ�==================================
        TradeContext.rVouhType = VouhFunc.AddSplit(TradeContext.sVouhType)
        TradeContext.rVouhName = VouhFunc.AddSplit(TradeContext.sVouhName)
        TradeContext.rStartNo  = VouhFunc.AddSplit(TradeContext.sStartNo)
        TradeContext.rEndNo    = VouhFunc.AddSplit(TradeContext.sEndNo)
        TradeContext.rVouhNum  = VouhFunc.AddSplit(TradeContext.sVouhNum)
        
        #=============��ʼ�����ر��ı���========================
        TradeContext.tradeResponse = []
        
        #=============������ˮ��========================
        TradeContext.sVouhSerial = VouhFunc.GetVouhSerial( )

        #=============��ȡ��ǰϵͳʱ��==========================
        TradeContext.sLstTrxDay  = AfaUtilTools.GetSysDate( )
        TradeContext.sLstTrxTime = AfaUtilTools.GetSysTime( )

        #=============��ƾ֤����״̬�������־====================
        TradeContext.sDepository  = '1' #�����־   1.���й���� 2.֧�й���� 3.�������� 4.��Աƾ֤��
        TradeContext.sExDepos     = ' ' #ԭ�����־
        TradeContext.sVouhStatus  = '0' #״̬       0.����δ�� 
        TradeContext.sExStatus    = ' ' #ԭ״̬
        TradeContext.sRivTeller   = '   '     #�Է���Ա
        TradeContext.sTransType    = 'ƾ֤���'
        
        #beginƾ֤�Ż�����201109  
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
            TradeContext.sTellerTailNo    = TradeContext.sTellerTailNobak[0]                 
            AfaLoggerFunc.tradeInfo( '��Աβ��ţ�' + TradeContext.sTellerTailNo ) 
        #end   
            
        #�ж��Ƿ�ع�
        n=0
        
        for i in range(TradeContext.sNum):

            #=============�������==========================
            sFlagBack   = '0'     #���ƾ֤��ֹ���������ƾ֤����ʼ�����Ƿ����������ϵ,'1':��;'0':��
            sFlagFront  = '0'     #���ƾ֤��ʼ���������ƾ֤����ֹ�����Ƿ����������ϵ,'1':��;'0':��

            n=n+1
        
            #============= �ж�������ʼ�����Ƿ�С�ڵ�����ֹ����============================
            if(int(TradeContext.sStartNo[i]) > int(TradeContext.sEndNo[i]) ):
                tradeExit('A005066', '�����ʼ���벻�ܴ�����ֹ����!')
                raise AfaFlowControl.flowException( )
            
            #ƾ֤�Ż�����201108
            #============= ��ѯ����ƾ֤���е�ƾ֤�Ŷ�============================
            #sqlStr = "select STARTNO,ENDNO,VOUHSTATUS from VOUH_REGISTER WHERE VOUHTYPE = '"\
            #+ TradeContext.sVouhType[i] + "' and BESBNO = '" + TradeContext.sBesbNo + "' and CUR = '" + TradeContext.sCur+"'"
            sqlStr = "select STARTNO,ENDNO ,VOUHSTATUS from VOUH_REGISTER where VOUHTYPE ='" + TradeContext.sVouhType[i] + "'" 
            sqlStr = sqlStr + " and VOUHSTATUS != '1' and BESBNO = '" + TradeContext.sBesbNo + "' and CUR = '" + TradeContext.sCur+"'"
            #end
             
            AfaLoggerFunc.tradeDebug(sqlStr)
            records = AfaDBFunc.SelectSql( sqlStr )
            AfaLoggerFunc.tradeInfo(records)
            
            if( records == None ):
                tradeExit('A005061', '��ѯ[ƾ֤�ǼǱ�]�����쳣!')
                raise AfaFlowControl.flowException( )
            elif( len( records ) == 0 ):    #������ݿ����޶�Ӧ��¼��ֱ�Ӳ���
                sqlStr = "insert into VOUH_REGISTER \
                (BESBNO,TELLERNO,DEPOSITORY,CUR,VOUHTYPE,STARTNO,ENDNO,RIVTELLER,VOUHSTATUS,\
                VOUHNUM,LSTTRXDAY,LSTTRXTIME) \
                values \
                ('"+TradeContext.sBesbNo+"','"+TradeContext.sTellerTailNo+"',\
                '"+TradeContext.sDepository+"','"+TradeContext.sCur+"','"+TradeContext.sVouhType[i]+"',\
                '"+TradeContext.sStartNo[i]+"','"+TradeContext.sEndNo[i]+"','"+TradeContext.sRivTeller+"',\
                '"+TradeContext.sVouhStatus+"','"+TradeContext.sVouhNum[i]+"',\
                '"+TradeContext.sLstTrxDay+"','"+TradeContext.sLstTrxTime+"')"
                AfaLoggerFunc.tradeDebug(sqlStr)
                records = AfaDBFunc.InsertSql( sqlStr )
                if records == -1 :
                    AfaLoggerFunc.tradeInfo( '���ݿ�ع�' )
                    AfaDBFunc.RollbackSql( )
                    tradeExit('A005062', 'ƾ֤���ʧ��,ƾ֤���ݿ����ʧ��!')
                    raise AfaFlowControl.flowException( )
                else:
                    tradeExit('0000', 'ƾ֤���ɹ�')       
            else :
                #�ж�����ƾ֤��ֹ������������ƾ֤�����Ƿ��н���,����records[x][0]
                #Ϊ��������ֹ����;records[x][1]Ϊ��������ʼ����,�ж�Ϊ�н��������Ϊ:
                #1.������ֹ������ڵ�����������ʼ����,����С�ڵ�����������ֹ����;
                #2.������ʼ������ڵ�����������ʼ����,����С�ڵ�����������ֹ����;
                #3.������ֹ������ڵ�����������ֹ����,����������ʼ����С�ڵ�����������ʼ����
                for x in range( len(records) ):
                    sTmpStartNo  = records[x][0]
                    sTmpEndNo    = records[x][1]
                    sTmpVouhStat = records[x][2]
                    if ((int(TradeContext.sEndNo[i])<=int(sTmpEndNo) and int(TradeContext.sEndNo[i])>=int(sTmpStartNo)) \
                    or (int(TradeContext.sStartNo[i])>=int(sTmpStartNo) and int(TradeContext.sStartNo[i])<=int(sTmpEndNo)) \
                    or ( int(TradeContext.sEndNo[i])>=int(sTmpEndNo) and int(TradeContext.sStartNo[i])<=int(sTmpStartNo))):
                        if( n > 1 ):
                            AfaLoggerFunc.tradeInfo( '���ݿ�ع�' )
                            AfaDBFunc.RollbackSql( )
                        tradeExit('A005063', 'ƾ֤���ʧ��,ƾ֤���д��ڱ�������ƾ֤!')
                        raise AfaFlowControl.flowException( )
                    elif ((int(TradeContext.sEndNo[i]) == (int(sTmpStartNo)-1)) and sTmpVouhStat == '0'):
                        sFlagBack = '1'          #�޽����Һ�����,�ú�������ʶ
                        sOperDelNo = records[x][0]
                        sOperEndNo = records[x][1]
                    elif ((int(TradeContext.sStartNo[i]) == (int(sTmpEndNo)+1)) and sTmpVouhStat == '0'):
                        sFlagFront = '1'         #�޽�����ǰ����,��ǰ������ʶ
                        sOperStartNo = records[x][0]
                #�����ƾ֤���������ͬ����ƾ֤���ں�������ϵ,������Ӧ�ļ�¼���й鲢
                if (  sFlagBack == '1' and sFlagFront == '0'):
                    sTmpVouhNum = str( int(sTmpEndNo) - int(TradeContext.sStartNo[i]) + 1 )
                    sqlStr = "update VOUH_REGISTER set \
                    STARTNO = '" + TradeContext.sStartNo[i] + "', \
                    VOUHNUM = '"+ sTmpVouhNum + "',\
                    TELLERNO = '" + TradeContext.sTellerTailNo + "',\
                    LSTTRXDAY = '"+ TradeContext.sLstTrxDay + "',\
                    LSTTRXTIME = '" + TradeContext.sLstTrxTime + "'\
                    where ENDNO = '" + sOperEndNo + "' AND VOUHSTATUS = '"+TradeContext.sVouhStatus+"' \
                    AND VOUHTYPE = '" + TradeContext.sVouhType[i]+ "' AND BESBNO = '" + TradeContext.sBesbNo+ "' \
                    AND CUR = '" + TradeContext.sCur+"'"
                    
                    AfaLoggerFunc.tradeDebug(sqlStr)
                    records = AfaDBFunc.UpdateSql( sqlStr )
                    if records == -1 :
                        AfaLoggerFunc.tradeInfo( '���ݿ�ع�' )
                        #�ع�
                        AfaDBFunc.RollbackSql( )
                        tradeExit('A005064', 'ƾ֤���ʧ��,ƾ֤���ݿ�����쳣!')
                        raise AfaFlowControl.flowException( )
                    elif records == 0 :
                        AfaLoggerFunc.tradeInfo( '���ݿ�ع�' )
                        #�ع�
                        AfaDBFunc.RollbackSql( )
                        tradeExit('A005062', 'ƾ֤���ʧ��,ƾ֤���ݿ����ʧ��!')
                        raise AfaFlowControl.flowException( )
                    else:
                        tradeExit('0000', 'ƾ֤���ɹ�')
            
                #�����ƾ֤���������ͬ����ƾ֤����ǰ������ϵ,������Ӧ�ļ�¼���й鲢
                elif (  sFlagFront == '1' and sFlagBack == '0' ):
                    sTmpVouhNum = str( int(TradeContext.sEndNo[i]) - int(sOperStartNo) + 1 )
                    sqlStr = "update VOUH_REGISTER set \
                    ENDNO = '" + TradeContext.sEndNo[i] + "', \
                    VOUHNUM = '" + sTmpVouhNum + "',\
                    TELLERNO = '" + TradeContext.sTellerTailNo+ "',\
                    LSTTRXDAY = '" + TradeContext.sLstTrxDay + "',\
                    LSTTRXTIME = '" + TradeContext.sLstTrxTime + "'\
                    where STARTNO = '" + sOperStartNo + "' AND VOUHSTATUS = '"+TradeContext.sVouhStatus+"' \
                    AND VOUHTYPE = '" + TradeContext.sVouhType[i]+ "' AND BESBNO = '" + TradeContext.sBesbNo + "' \
                    AND CUR ='"+ TradeContext.sCur+"'"
                    AfaLoggerFunc.tradeDebug(sqlStr)
                    records = AfaDBFunc.UpdateSql( sqlStr )
                    if records == -1 :
                        AfaLoggerFunc.tradeInfo( '���ݿ�ع�' )
                        #�ع�
                        AfaDBFunc.RollbackSql( )
                        tradeExit('A005064', 'ƾ֤���ʧ��,ƾ֤���ݿ�����쳣!')
                        raise AfaFlowControl.flowException( )
                    elif records == 0 :
                        AfaLoggerFunc.tradeInfo( '���ݿ�ع�' )
                        #�ع�
                        AfaDBFunc.RollbackSql( )
                        tradeExit('A005062', 'ƾ֤���ʧ��,ƾ֤���ݿ����ʧ��!')
                        raise AfaFlowControl.flowException( )
                    else:
                        tradeExit('0000', 'ƾ֤���ɹ�')
            
                #�����ƾ֤���������ͬ����ƾ֤����ǰ/��������ϵ,������Ӧ�ļ�¼���й鲢
                elif (  sFlagBack == '1' and sFlagFront == '1' ):
                    sTmpVouhNum = str( int(sOperEndNo) - int(sOperStartNo) + 1 )
                    sqlStr = "update VOUH_REGISTER set \
                    ENDNO = '" + sOperEndNo + "', VOUHNUM = '" + sTmpVouhNum + "',\
                    TELLERNO = '" + TradeContext.sTellerTailNo + "',\
                    LSTTRXDAY = '" + TradeContext.sLstTrxDay + "',\
                    LSTTRXTIME = '" + TradeContext.sLstTrxTime + "'\
                    where STARTNO = '" + sOperStartNo + "' AND VOUHSTATUS = '"+TradeContext.sVouhStatus+"' \
                    AND VOUHTYPE = '" + TradeContext.sVouhType[i]+ "' AND BESBNO = '" + TradeContext.sBesbNo + "' \
                    AND CUR = '"+ TradeContext.sCur+"'"
                    AfaLoggerFunc.tradeDebug(sqlStr)
                    records = AfaDBFunc.UpdateSql( sqlStr )
                    if records == -1 or records == 0 :
                        AfaLoggerFunc.tradeInfo( '���ݿ�ع�' )
                        #�ع�
                        AfaDBFunc.RollbackSql( )
                        tradeExit('A005062', 'ƾ֤���ʧ��,ƾ֤���ݿ����ʧ��!')
                        raise AfaFlowControl.flowException( )
                    else:      #�鲢�ɹ���,ɾ���鲢������һ��
                        sqlDel = "delete from VOUH_REGISTER \
                        where STARTNO = '" + sOperDelNo + "' AND VOUHSTATUS = '"+TradeContext.sVouhStatus+"' \
                        AND VOUHTYPE = '" + TradeContext.sVouhType[i]+ "' AND BESBNO ='"+ TradeContext.sBesbNo+"' \
                        AND CUR = '"+ TradeContext.sCur+"'"
                        AfaLoggerFunc.tradeDebug(sqlDel)
                        record = AfaDBFunc.DeleteSql( sqlDel )
                        if record == -1 or record == 0 :
                            AfaLoggerFunc.tradeInfo( '���ݿ�ع�' )
                            record = AfaDBFunc.RollbackSql( )
                            tradeExit('A005062', 'ƾ֤���ʧ��,ƾ֤���ݿ����ʧ��!')
                            raise AfaFlowControl.flowException( )
                        else:
                            tradeExit('0000', 'ƾ֤���ɹ�')
            
                #�����ƾ֤���������ͬ����ƾ֤�������κ�������ϵ,��ֱ�Ӳ���
                else:
                    sqlStr = "insert into VOUH_REGISTER \
                    (BESBNO,TELLERNO,DEPOSITORY,CUR,VOUHTYPE,STARTNO,ENDNO,RIVTELLER,VOUHSTATUS,\
                    VOUHNUM,LSTTRXDAY,LSTTRXTIME) \
                    values \
                    ('" + TradeContext.sBesbNo + "','" + TradeContext.sTellerTailNo + "',\
                    '"+TradeContext.sDepository+ "','" + TradeContext.sCur+"','"+ TradeContext.sVouhType[i]+"',\
                    '" + TradeContext.sStartNo[i] + "','" + TradeContext.sEndNo[i] + "','" + TradeContext.sRivTeller +"',\
                    '"+TradeContext.sVouhStatus+"','" + TradeContext.sVouhNum[i] + "',\
                    '" + TradeContext.sLstTrxDay + "','" + TradeContext.sLstTrxTime + "')"
                    AfaLoggerFunc.tradeDebug(sqlStr)
                    records = AfaDBFunc.InsertSql( sqlStr )
                    if records == -1 :
                        AfaLoggerFunc.tradeInfo( '���ݿ�ع�' )
                        AfaDBFunc.RollbackSql( )
                        tradeExit('A005062', 'ƾ֤���ʧ��,ƾ֤���ݿ����ʧ��!')
                        raise AfaFlowControl.flowException( )
                    else:
                        tradeExit('0000', 'ƾ֤���ɹ�')
    

        AfaLoggerFunc.tradeInfo( '------------����ƾ֤����ǼǱ�' )
        #����ƾ֤����ǼǱ�
        VouhFunc.VouhModify()
        
        #���ݿ��ύ
        AfaLoggerFunc.tradeInfo( '------------���ݿ��ύ' )
        AfaDBFunc.CommitSql( )
        
        #��������
        AfaLoggerFunc.tradeInfo( '------------��������' )
        TradeContext.sOperSty = '0'
        VouhHostFunc.VouhCommHost()
        TradeContext.sTranStatus = '0'
        AfaLoggerFunc.tradeInfo( '=======================12'+TradeContext.errorCode )
        #TradeContext.errorCode = '0000'
        if(TradeContext.errorCode <> '0000'):
            tmpErrorCode= TradeContext.errorCode
            tmpErrorMsg = TradeContext.errorMsg
        
            #����
            
            #=============��ƾ֤����״̬�������־====================
            TradeContext.sDepository  = '1' #�����־   1.���й���� 2.֧�й���� 3.�������� 4.��Աƾ֤��
            TradeContext.sExDepos     = '1' #ԭ�����־
            TradeContext.sVouhStatus  = '9' #״̬       0.����δ�� 9.������
            TradeContext.sExStatus    = '0' #ԭ״̬
            TradeContext.sRivTeller   = '   '     #�Է���Ա
            TradeContext.sTransType    = '����'
            TradeContext.sInTellerTailNo  = TradeContext.sTellerTailNo
            TradeContext.sInBesbNo    = TradeContext.sBesbNo

            #���׹�������    
            VouhFunc.VouhTrans()
            AfaDBFunc.CommitSql( )
            
            sqlDel = "delete from VOUH_REGISTER where VOUHSTATUS = '9'"
            AfaLoggerFunc.tradeDebug(sqlDel)
            record = AfaDBFunc.DeleteSqlCmt( sqlDel )
            if record == -1 or record == 0 :
                tradeExit('A005062', '����ʧ��,ƾ֤���ݿ����ʧ��!')
                raise AfaFlowControl.flowException( )
            else:
                AfaLoggerFunc.tradeInfo( '============================�Զ�������' )
                
            TradeContext.sTranStatus = '1'
            if(not TradeContext.existVariable( "HostSerno" )):
                TradeContext.HostSerno = ''    
            
            #������ˮ��
            VouhFunc.ModifyVouhModify()
            
            tradeExit(tmpErrorCode, tmpErrorMsg)
            raise AfaFlowControl.flowException( )
         
        #������ˮ��
        VouhFunc.ModifyVouhModify()        
        
        TradeContext.tradeResponse.append( ['sVouhSerial',TradeContext.sVouhSerial] )
        TradeContext.tradeResponse.append( ['sVouhType',TradeContext.rVouhType] )
        TradeContext.tradeResponse.append( ['sVouhName',TradeContext.rVouhName] )
        TradeContext.tradeResponse.append( ['sStartNo',TradeContext.rStartNo] )
        TradeContext.tradeResponse.append( ['sEndNo',TradeContext.rEndNo] )
        TradeContext.tradeResponse.append( ['sVouhNum',TradeContext.rVouhNum] )
        TradeContext.tradeResponse.append( ['sLstTrxDay',TradeContext.sLstTrxDay] )
        TradeContext.tradeResponse.append( ['sLstTrxTime',TradeContext.sLstTrxTime] )
        TradeContext.tradeResponse.append( ['sNum',str(TradeContext.sNum)] )
        TradeContext.tradeResponse.append( ['errorCode','0000'] )
        TradeContext.tradeResponse.append( ['errorMsg','��ѯ�ɹ�'] )
        
            
            #�Զ����
        AfaFunc.autoPackData()

        #=============�����˳�====================
        AfaLoggerFunc.tradeInfo( 'ƾ֤���['+TradeContext.TemplateCode+']�˳�' )
    except AfaFlowControl.flowException, e:
        AfaLoggerFunc.tradeInfo( '���ݿ�ع�' )
        AfaDBFunc.RollbackSql( )
        AfaFlowControl.exitMainFlow( )
    except AfaFlowControl.accException:
        AfaLoggerFunc.tradeInfo( '���ݿ�ع�' )
        AfaDBFunc.RollbackSql( )
        AfaFlowControl.exitMainFlow( )
    except Exception, e:
        AfaLoggerFunc.tradeInfo( '���ݿ�ع�' )
        AfaDBFunc.RollbackSql( )
        AfaFlowControl.exitMainFlow(str(e))

