# -*- coding: gbk -*-
###############################################################################
# Copyright (c) 2011,������ͬ�Ƽ���չ���޹�˾.������ҵ��
# All rights reserved.
#
# �ļ����ƣ�TPS001_8484.py
# �ļ���ʶ��
# ժ    Ҫ����˰����.�����ϸ��ѯ
#
# ��ǰ�汾��1.0
# ��    �ߣ�
# ������ڣ�2011 �� 7 �� 26 ��
#
# ȡ���汾��
# ԭ �� �ߣ�������
# ������ڣ�
###############################################################################
import TradeContext
TradeContext.sysType = 'tips'
import AfaDBFunc,AfaLoggerFunc,os,TipsFunc,AfaFlowControl
#import UtilTools��TradeContext, ConfigParser
def SubModuleMainFst( ):
    try:
        
        AfaLoggerFunc.tradeInfo( '��������ϸ��ѯ['+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']'  )
        
        #��ϸд���ļ�
        #begin�������Ż�20120611
        #mx_file_name = os.environ['AFAP_HOME'] + '/data/batch/tips/' + 'AH_ERROR_' + TradeContext.teller + '_'+TradeContext.workDate+'.txt'
        mx_file_name = os.environ['AFAP_HOME'] + '/tmp/' + 'AH_ERROR_' + TradeContext.teller + '_'+TradeContext.workDate+'.txt'
        #end
        
        TradeContext.tradeResponse.append(['fileName',  'AH_ERROR_' + TradeContext.teller +'_'+TradeContext.workDate+'.txt'])
        
        if (os.path.exists(mx_file_name) and os.path.isfile(mx_file_name)):
            #�ļ�����,��ɾ��-�ٴ���
            os.system("rm " + mx_file_name)
        
        #====��ȡ������Ϣ=======   
        if not ChkLiquidStatus( ):
            return False
        
        
        #��ѯ����ʧ�ܵĽ�����ϸ
        sqlStr=''
        sqlStr=sqlStr + "SELECT BRNO,SERIALNO,DRACCNO,CRACCNO,TRADETYPE,TAXPAYNAME,AMOUNT,BANKSTATUS,CORPSTATUS,CHKFLAG,CORPCHKFLAG,REVTRANF,NOTE10 FROM TIPS_MAINTRANSDTL "
        sqlStr=sqlStr + " WHERE NOTE3 = '" + TradeContext.payBkCode.strip() + "' and WORKDATE = '" + TradeContext.date + "'"
        sqlStr=sqlStr + "and ((REVTRANF = '0' and BANKSTATUS = '0' and CORPSTATUS = '0' and ((CHKFLAG ='9' and CORPCHKFLAG ='9')or(CHKFLAG ='9' and CORPCHKFLAG ='0')or(CHKFLAG ='0' and CORPCHKFLAG ='9'))) "
        sqlStr=sqlStr + " or ( REVTRANF = '1' and BANKSTATUS != '0'))"
          
        AfaLoggerFunc.tradeInfo(sqlStr) 
           
        Records = AfaDBFunc.SelectSql( sqlStr )
           
        if( Records == None ):
            
            return TipsFunc.ExitThisFlow( 'A0027', '������쳣:'+AfaDBFunc.sqlErrMsg )
            
        elif( len( Records )==0 ):
            
            return TipsFunc.ExitThisFlow( 'A0027', 'û����������������' )
        else:
            sfp = open(mx_file_name, "w")
            AfaLoggerFunc.tradeInfo('��ϸ�ļ�=['+mx_file_name+']')
            for i in range(0,len(Records)):
                A0 = str(Records[i][0]).strip()           #������
                A1 = str(Records[i][1]).strip()           #ƽ̨��ˮ��     
                A2 = str(Records[i][2]).strip()           #�跽�˺�   
                A3 = str(Records[i][3]).strip()           #�����˺�
                A4 = str(Records[i][4]).strip()           #��������
                A5 = str(Records[i][5]).strip()           #��˰������
                A6 = str(Records[i][6]).strip()           #���׽��
                A7 = str(Records[i][7]).strip()           #����״̬
                A8 = str(Records[i][8]).strip()           #��ҵ״̬
                A9 = str(Records[i][9]).strip()           #�������˱�־
                A10 = str(Records[i][10]).strip()         #��ҵ���˱�־
                A11 = str(Records[i][11]).strip()         #�������ױ�־
                A12 = str(Records[i][12]).strip()         #��������      
       
                sfp.write(A0 + '|' + A1 + '|' + A2 + '|' + A3 + '|' + A4 + '|' + A5 + '|' + A6 + '|' + A7 + '|' + A8 + '|' + A9 + '|' + A10 + '|' + A11 + '|' + A12 + '\n')
                
            sfp.close()                
        
        TradeContext.tradeResponse.append(['errorCode','0000'])
        TradeContext.tradeResponse.append(['errorMsg','���׳ɹ�'])
       
        AfaLoggerFunc.tradeInfo( '�˳������ϸ��ѯ[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' )
    
        return True 
    
    except Exception, e:                  

        AfaFlowControl.exitMainFlow(str(e))      
                                              
#====��ȡ������Ϣ==========    
def ChkLiquidStatus():
    AfaLoggerFunc.tradeInfo( '>>>��ȡ������Ϣ' )
    
    sql ="SELECT PAYBKCODE,PAYEEBANKNO,TRECODE,TRENAME,PAYEEACCT,PAYBKNAME,STATUS FROM TIPS_LIQUIDATE_ADM WHERE "
    sql =sql + "BRNO = '" + TradeContext.brno + "'"
    
    AfaLoggerFunc.tradeInfo(sql)
    
    records = AfaDBFunc.SelectSql(sql)
    
    if( records == None ):
        AfaLoggerFunc.tradeFatal(sql)
        return TipsFunc.ExitThisFlow( 'A0002', '���ݿ�����쳣:'+AfaDBFunc.sqlErrMsg )
    elif( len( records )==0 ):
        return  TipsFunc.ExitThisFlow( 'A0027', '���������������У������Խ��ж��˲���ѯ' )
    else:
        if records[0][6]=='0':
            return TipsFunc.ExitThisFlow( 'A0027', 'ҵ����ֹͣ�����ɽ��в�ѯ' )
        if records[0][6]=='2':
            return TipsFunc.ExitThisFlow( 'A0027', 'ҵ������ͣ�����ɽ��в�ѯ' )
        AfaLoggerFunc.tradeInfo('�������������к�Ϊ'+ records[0][0])
        AfaLoggerFunc.tradeInfo('�����͵������к�Ϊ'+ TradeContext.payBkCode)
        if(records[0][0]!=TradeContext.payBkCode):
            return TipsFunc.ExitThisFlow( 'A0002', '�������кŲ���ȷ�����������˽���')
            
    AfaLoggerFunc.tradeInfo( '>>>��ȡ������Ϣ���' )
    return True    
