# -*- coding: gbk -*-

####################################################################
#    ��    ��:    Tvouh024.py
#    ˵    ��:    ƾ֤����.��ӡ����
#    ��    ��:    �м�ҵ����ƽ̨��AFA��--- UNIX: AIX 5.3
#    ��    ��:    ���ǽ�
#    ��    ˾:    ������ͬ�Ƽ�
#    ������ַ:    ����
#    ����ʱ��:    2008��6��15��
#    ά����¼:
####################################################################

import TradeContext, AfaLoggerFunc, AfaUtilTools, AfaFunc, AfaFlowControl, AfaDBFunc
from types import *
import AfaLoggerFunc,VouhFunc,binascii,HostContext,VouhHostFunc,os


def tradeExit( code, msg ):
    TradeContext.errorCode, TradeContext.errorMsg=code, msg
    if code != '0000':
        return False
    return True

def main( ):
    
    AfaLoggerFunc.tradeInfo( '��ӡ����['+TradeContext.TemplateCode+']����' )
    
    #=============ǰ̨��������====================
    #TradeContext.sTellerNo          ��Ա�� 
    #TradeContext.sWorkDate          ��������
    #TrddeContext.sBesbNo            ������

    
    
    try:
        #=============��ȡ��������==========================
        HostContext.I1OTSB = TradeContext.sBesbNo         #������
        HostContext.I1SBNO = TradeContext.sBesbNo         #������
        HostContext.I1USID = TradeContext.sTellerNo       #��Ա��
        HostContext.I1WSNO = TradeContext.sWSNO           #�ն˺�
        if(not VouhHostFunc.CommHost('2001')):
            tradeExit(TradeContext.errorCode, TradeContext.errorMsg)
            raise AfaFlowControl.flowException( )
        if(TradeContext.errorCode == '0000'):
            SBNO = HostContext.O1SBCH
            AfaLoggerFunc.tradeInfo( SBNO )
        
        #=============��ȡ��Ա����==========================
        HostContext.I1TELR = TradeContext.sTellerNo       #��Ա��
        HostContext.I1SBNO = TradeContext.sBesbNo         #������
        HostContext.I1USID = TradeContext.sTellerNo       #��Ա��
        HostContext.I1WSNO = TradeContext.sWSNO           #�ն˺�
        if(not VouhHostFunc.CommHost('8809')):
            tradeExit(TradeContext.errorCode, TradeContext.errorMsg)
            raise AfaFlowControl.flowException( )
        if(TradeContext.errorCode == '0000'):
            TELLER = HostContext.O1TLRK
            AfaLoggerFunc.tradeInfo( TELLER )
        
        #=============��ʼ�����ر��ı���==================
        TradeContext.tradeResponse = []
        
        #=================��ȡ��������==============================
        #begin 20100920 �������޸� �������������ʱ��ѯ���Ϊ�ն��׳�����
        #TradeContext.sBesbName = VouhFunc.SelectBesbName(TradeContext.sBesbNo)
        if not VouhFunc.SelectBesbName(TradeContext.sBesbNo):
            raise AfaFlowControl.flowException( )
        else:
            TradeContext.sBesbName = VouhFunc.SelectBesbName(TradeContext.sBesbNo)
        #end

        #=====================��ȡ��������===============================
        #TradeContext.sBesbSty = VouhFunc.SelectBesbSty(TradeContext.sBesbNo)
        #AfaLoggerFunc.tradeInfo('================='+TradeContext.sBesbSty)

        #=============��ȡ��ǰϵͳʱ��====================
        TradeContext.sLstTrxDay = AfaUtilTools.GetSysDate( )
        TradeContext.sLstTrxTime = AfaUtilTools.GetSysTime( ) 
        
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
            AfaLoggerFunc.tradeInfo( '���׹�Աβ��ţ�' + TradeContext.sTellerTailNo ) 
        #end   
        
        vouh = []
        count1 = 0
        count2 = 0
        count3 = 0
        AfaLoggerFunc.tradeInfo(TradeContext.sTellerTailNo)
        sqlStr = "select VOUHTYPE,VOUHNAME from VOUH_PARAMETER where substr(BESBNO,1,6) = '" + (TradeContext.sBesbNo)[:6] + "' order by VOUHTYPE"
        AfaLoggerFunc.tradeInfo(sqlStr)
        records = AfaDBFunc.SelectSql( sqlStr )
        if( records == None ):
            tradeExit('A005067', '��ѯ[ƾ֤������]�����쳣!')
            raise AfaFlowControl.flowException( )
        elif( len( records ) == 0 ):
            tradeExit('A005068', 'ƾ֤������!' )
            raise AfaFlowControl.flowException( )
        else :
            for i in range(len(records)):
                num1 = 0
                num2 = 0
                num3 = 0
                if(SBNO == '33' and TELLER == "10"):
                    
                    #��ѯƾ֤������
                    sqlStr = "select SUM(CAST(VOUHNUM AS DECIMAL(25))) from VOUH_MODIFY \
                            where WORKDATE = '" + TradeContext.sWorkDate + "' \
                            and VOUHTYPE = '" + records[i][0] + "' \
                            and TELLERNO = '" + TradeContext.sTellerTailNo + "' \
                            and BESBNO = '" + TradeContext.sBesbNo + "' \
                            and TRANSTATUS = '0' \
                            and VOUHSTATUS = '0'"
                    res1 = AfaDBFunc.SelectSql( sqlStr )
                    AfaLoggerFunc.tradeInfo('sql1 = '+sqlStr)
                    if( res1 == None ):
                        tradeExit('A005067', '��ѯ[ƾ֤��]�����쳣!')
                        raise AfaFlowControl.flowException( )
                    elif( len( res1 ) == 0 ):
                        num1 = 0
                    else :
                        num1 = res1[0][0]
                        if(num1 == None):
                            num1 = 0
                        AfaLoggerFunc.tradeInfo(num1)  
                          
                    #��ѯƾ֤������
                    sqlStr = "select SUM(CAST(VOUHNUM AS DECIMAL(25))) from VOUH_MODIFY \
                            where WORKDATE = '" + TradeContext.sWorkDate + "' \
                            and TELLERNO = '" + TradeContext.sTellerTailNo + "' \
                            and VOUHTYPE = '" + records[i][0] + "' \
                            and BESBNO = '" + TradeContext.sBesbNo + "' \
                            and TRANSTATUS = '0' \
                            and VOUHSTATUS in ('1','2')"
                    res2 = AfaDBFunc.SelectSql( sqlStr )
                    AfaLoggerFunc.tradeInfo('sql2 = '+sqlStr)
                    if( res2 == None ):
                        tradeExit('A005067', '��ѯ[ƾ֤��]�����쳣!')
                        raise AfaFlowControl.flowException( )
                    elif( len( res2 ) == 0 ):
                        num2 = 0
                    else :
                        num2 = res2[0][0]
                        if(num2 == None):
                            num2 = 0
                        AfaLoggerFunc.tradeInfo(num2)  
                         
                    #��ѯƾ֤����
                    sqlStr = "select SUM(CAST(VOUHNUM AS DECIMAL(25))) from VOUH_REGISTER \
                            where VOUHTYPE = '" + records[i][0] + "' \
                            and TELLERNO = '" + TradeContext.sTellerTailNo + "' \
                            and BESBNO = '" + TradeContext.sBesbNo + "' \
                            and VOUHSTATUS = '0'"
                    res3 = AfaDBFunc.SelectSql( sqlStr )
                    AfaLoggerFunc.tradeInfo('sql3 = '+sqlStr)
                    if( res3 == None ):
                        tradeExit('A005067', '��ѯ[ƾ֤��]�����쳣!')
                        raise AfaFlowControl.flowException( )
                    elif( len( res3 ) == 0 ):
                        num3 = 0
                    else :
                        num3 = res3[0][0]
                        if(num3 == None):
                            num3 = 0
                        AfaLoggerFunc.tradeInfo(num3)  
                          
                elif(TELLER == "10"):
                    
                    #��ѯƾ֤������
                    sqlStr = "select SUM(CAST(VOUHNUM AS DECIMAL(25))) from VOUH_MODIFY \
                            where WORKDATE = '" + TradeContext.sWorkDate + "' \
                            and VOUHTYPE = '" + records[i][0] + "' \
                            and (TELLERNO = '" + TradeContext.sTellerTailNo + "' \
                            or RIVTELLER = '" + TradeContext.sTellerTailNo + "') \
                            and BESBNO = '" + TradeContext.sBesbNo + "' \
                            and TRANSTATUS = '0' \
                            and VOUHSTATUS = '2'"
                    res1 = AfaDBFunc.SelectSql( sqlStr )
                    AfaLoggerFunc.tradeInfo('sql1 = '+sqlStr)
                    if( res1 == None ):
                        tradeExit('A005067', '��ѯ[ƾ֤��]�����쳣!')
                        raise AfaFlowControl.flowException( )
                    elif( len( res1 ) == 0 ):
                        num1 = 0
                    else :
                        num1 = res1[0][0]
                        if(num1 == None):
                            num1 = 0
                            
                    #��ѯƾ֤������
                    sqlStr = "select SUM(CAST(VOUHNUM AS DECIMAL(25))) from VOUH_MODIFY \
                            where WORKDATE = '" + TradeContext.sWorkDate + "' \
                            and TELLERNO = '" + TradeContext.sTellerTailNo + "' \
                            and BESBNO = '" + TradeContext.sBesbNo + "' \
                            and VOUHTYPE = '" + records[i][0] + "' \
                            and TRANSTATUS = '0' \
                            and EXSTATUS = '2' \
                            and VOUHSTATUS in ('0','3')"
                    res2 = AfaDBFunc.SelectSql( sqlStr )
                    AfaLoggerFunc.tradeInfo('sql2 = '+sqlStr)
                    if( res2 == None ):
                        tradeExit('A005067', '��ѯ[ƾ֤��]�����쳣!')
                        raise AfaFlowControl.flowException( )
                    elif( len( res2 ) == 0 ):
                        num2 = 0
                    else :
                        num2 = res2[0][0]
                        if(num2 == None):
                            num2 = 0
                            
                    #��ѯƾ֤����
                    sqlStr = "select SUM(CAST(VOUHNUM AS DECIMAL(25))) from VOUH_REGISTER \
                            where VOUHTYPE = '" + records[i][0] + "' \
                            and TELLERNO = '" + TradeContext.sTellerTailNo + "' \
                            and BESBNO = '" + TradeContext.sBesbNo + "' \
                            and VOUHSTATUS = '2'"
                    res3 = AfaDBFunc.SelectSql( sqlStr )
                    AfaLoggerFunc.tradeInfo('sql3 = '+sqlStr)
                    if( res3 == None ):
                        tradeExit('A005067', '��ѯ[ƾ֤��]�����쳣!')
                        raise AfaFlowControl.flowException( )
                    elif( len( res3 ) == 0 ):
                        num3 = 0
                    else :
                        num3 = res3[0][0]
                        if(num3 == None):
                            num3 = 0
                            
                elif(TELLER == "20"):
                    
                    #��ѯƾ֤������
                    sqlStr = "select SUM(CAST(VOUHNUM AS DECIMAL(25))) from VOUH_MODIFY \
                            where WORKDATE = '" + TradeContext.sWorkDate + "' \
                            and VOUHTYPE = '" + records[i][0] + "' \
                            and substr(BESBNO,1,6) = '" + (TradeContext.sBesbNo)[:6] + "' \
                            and BESBNO = '" + TradeContext.sBesbNo + "' \
                            and TRANSTATUS = '0' \
                            and VOUHSTATUS = '2'"
                    res1 = AfaDBFunc.SelectSql( sqlStr )
                    AfaLoggerFunc.tradeInfo('sql1 = '+sqlStr)
                    if( res1 == None ):
                        tradeExit('A005067', '��ѯ[ƾ֤��]�����쳣!')
                        raise AfaFlowControl.flowException( )
                    elif( len( res1 ) == 0 ):
                        num1 = 0
                    else :
                        num1 = res1[0][0]
                        if(num1 == None):
                            num1 = 0
                            
                    #��ѯƾ֤������
                    sqlStr = "select SUM(CAST(VOUHNUM AS DECIMAL(25))) from VOUH_MODIFY \
                            where WORKDATE = '" + TradeContext.sWorkDate + "' \
                            and substr(BESBNO,1,6) = '" + (TradeContext.sBesbNo)[:6] + "' \
                            and BESBNO = '" + TradeContext.sBesbNo + "' \
                            and VOUHTYPE = '" + records[i][0] + "' \
                            and TRANSTATUS = '0' \
                            and EXSTATUS = '3' \
                            and VOUHSTATUS in ('2','4','5','6')"
                    res2 = AfaDBFunc.SelectSql( sqlStr )
                    AfaLoggerFunc.tradeInfo('sql2 = '+sqlStr)
                    if( res2 == None ):
                        tradeExit('A005067', '��ѯ[ƾ֤��]�����쳣!')
                        raise AfaFlowControl.flowException( )
                    elif( len( res2 ) == 0 ):
                        num2 = 0
                    else :
                        num2 = res2[0][0]
                        if(num2 == None):
                            num2 = 0
                            
                    #��ѯƾ֤����
                    sqlStr = "select SUM(CAST(VOUHNUM AS DECIMAL(25))) from VOUH_REGISTER \
                            where VOUHTYPE = '" + records[i][0] + "' \
                            and substr(BESBNO,1,6) = '" + (TradeContext.sBesbNo)[:6] + "' \
                            and BESBNO = '" + TradeContext.sBesbNo + "' \
                            and VOUHSTATUS in ('2','3')"
                    res3 = AfaDBFunc.SelectSql( sqlStr )
                    AfaLoggerFunc.tradeInfo('sql3 = '+sqlStr)
                    if( res3 == None ):
                        tradeExit('A005067', '��ѯ[ƾ֤��]�����쳣!')
                        raise AfaFlowControl.flowException( )
                    elif( len( res3 ) == 0 ):
                        num3 = 0
                    else :
                        num3 = res3[0][0]
                        if(num3 == None):
                            num3 = 0
                            
                else:
                    
                    #��ѯƾ֤������
                    sqlStr = "select SUM(CAST(VOUHNUM AS DECIMAL(25))) from VOUH_MODIFY \
                            where WORKDATE = '" + TradeContext.sWorkDate + "' \
                            and VOUHTYPE = '" + records[i][0] + "' \
                            and (TELLERNO = '" + TradeContext.sTellerTailNo + "' \
                            or RIVTELLER = '" + TradeContext.sTellerTailNo + "') \
                            and BESBNO = '" + TradeContext.sBesbNo + "' \
                            and TRANSTATUS = '0' \
                            and VOUHSTATUS = '3'"
                    res1 = AfaDBFunc.SelectSql( sqlStr )
                    AfaLoggerFunc.tradeInfo('sql1 = '+sqlStr)
                    if( res1 == None ):
                        tradeExit('A005067', '��ѯ[ƾ֤��]�����쳣!')
                        raise AfaFlowControl.flowException( )
                    elif( len( res1 ) == 0 ):
                        num1 = 0
                    else :
                        num1 = res1[0][0]
                        if(num1 == None):
                            num1 = 0
                            
                    #��ѯƾ֤������
                    sqlStr = "select SUM(CAST(VOUHNUM AS DECIMAL(25))) from VOUH_MODIFY \
                            where WORKDATE = '" + TradeContext.sWorkDate + "' \
                            and TELLERNO = '" + TradeContext.sTellerTailNo + "' \
                            and BESBNO = '" + TradeContext.sBesbNo + "' \
                            and VOUHTYPE = '" + records[i][0] + "' \
                            and TRANSTATUS = '0' \
                            and EXSTATUS = '3' \
                            and VOUHSTATUS in ('2','4','5','6')"
                    res2 = AfaDBFunc.SelectSql( sqlStr )
                    AfaLoggerFunc.tradeInfo('sql2 = '+sqlStr)
                    if( res2 == None ):
                        tradeExit('A005067', '��ѯ[ƾ֤��]�����쳣!')
                        raise AfaFlowControl.flowException( )
                    elif( len( res2 ) == 0 ):
                        num2 = 0
                    else :
                        num2 = res2[0][0]
                        if(num2 == None):
                            num2 = 0
                            
                    #��ѯƾ֤����
                    sqlStr = "select SUM(CAST(VOUHNUM AS DECIMAL(25))) from VOUH_REGISTER \
                            where VOUHTYPE = '" + records[i][0] + "' \
                            and TELLERNO = '" + TradeContext.sTellerTailNo + "' \
                            and BESBNO = '" + TradeContext.sBesbNo + "' \
                            and VOUHSTATUS = '3'"
                    res3 = AfaDBFunc.SelectSql( sqlStr )
                    AfaLoggerFunc.tradeInfo('sql3 = '+sqlStr)
                    if( res3 == None ):
                        tradeExit('A005067', '��ѯ[ƾ֤��]�����쳣!')
                        raise AfaFlowControl.flowException( )
                    elif( len( res3 ) == 0 ):
                        num3 = 0
                    else :
                        num3 = res3[0][0]
                        if(num3 == None):
                            num3 = 0
                    
                vouh.append([records[i][0],records[i][1],str(num1),str(num2),str(num3)])
                
                count1 = count1 + num1
                count2 = count2 + num2
                count3 = count3 + num3

        
        rBankFile= os.environ['AFAP_HOME'] + '/data/vouh/vouhtmp.txt'
      

        #����ҵ�񱨱��ļ�
        bFp = open(rBankFile, "w")
        AfaLoggerFunc.tradeInfo('-----' + TradeContext.sBesbNo)
        AfaLoggerFunc.tradeInfo('-----' + TradeContext.sBesbName)
        AfaLoggerFunc.tradeInfo('-----' + TradeContext.sTellerTailNo)
        AfaLoggerFunc.tradeInfo('-----' + TradeContext.sWorkDate)
        
        #д�����
        bFp.write('\n                          **************** ����ҵ��ƾ֤���� ****************                         \n\n')
        bFp.write('              ��������:' + TradeContext.sBesbNo + '        ��������: ' + TradeContext.sBesbName +  '\n')
        bFp.write('              ��Ա����:' + TradeContext.sTellerTailNo +  '            ����:' + TradeContext.sWorkDate +  '\n')
        bFp.write('    ------------------------------------------------------------------------------------------------------\n')
        bFp.write('    |   ���   | ƾ֤���� |          ƾ֤����            |   �շ�������  |   ����������  |      ���     |\n')
        bFp.write('    |----------|----------|------------------------------|---------------|---------------|---------------|\n')
            
        AfaLoggerFunc.tradeInfo('------------test5')
        for i in range( len( vouh ) ):

            wbuffer = '    |'
            wbuffer = wbuffer + str(i+1).ljust(10,' ') + '|'
            wbuffer = wbuffer +(vouh[i][0].strip()).ljust(10, ' ') + '|'
            wbuffer = wbuffer +(vouh[i][1].strip()).ljust(30, ' ') + '|'
            wbuffer = wbuffer +(vouh[i][2].strip()).rjust(15, ' ') + '|'
            wbuffer = wbuffer +(vouh[i][3].strip()).rjust(15, ' ') + '|'
            wbuffer = wbuffer +(vouh[i][4].strip()).rjust(15, ' ') + '|'

            #д�뱨���ļ�
            bFp.write(wbuffer + '\n')
            bFp.write('    |----------|----------|------------------------------|---------------|---------------|---------------|\n')
        
        bFp.write('    |   �ϼ�   |          |                              |' + str(count1).rjust(15,' ') + '|' + str(count2).rjust(15,' ') + '|' + str(count3).rjust(15,' ')+ '|\n')
        bFp.write('    ------------------------------------------------------------------------------------------------------\n')
        #�ر��ļ�
        bFp.close()
        
        TradeContext.tradeResponse.append( ['sBesbNo',TradeContext.sBesbNo] )
        TradeContext.tradeResponse.append( ['sTellerTailNo',TradeContext.sTellerTailNo] )
        TradeContext.tradeResponse.append( ['sTellerNo',TradeContext.sTellerNo] )             #ƾ֤�Ż�����201109 
        TradeContext.tradeResponse.append( ['sLstTrxDay',TradeContext.sLstTrxDay] )
        TradeContext.tradeResponse.append( ['sLstTrxTime',TradeContext.sLstTrxTime] )
        TradeContext.tradeResponse.append( ['sFileName','vouhtmp.txt'] )
        TradeContext.tradeResponse.append( ['errorCode','0000'] )
        TradeContext.tradeResponse.append( ['errorMsg','���׳ɹ�'] )
        AfaFunc.autoPackData()
        #=============�����˳�====================
        AfaLoggerFunc.tradeInfo( '��ӡ����['+TradeContext.TemplateCode+']�˳�' )
    except AfaFlowControl.flowException, e:
        AfaFlowControl.exitMainFlow( )
    except AfaFlowControl.accException:
        AfaFlowControl.exitMainFlow( )
    except Exception, e:
        AfaFlowControl.exitMainFlow(str(e))

  
