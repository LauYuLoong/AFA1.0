# -*- coding: gbk -*-
###############################################################################
# Copyright (c) 2006,������ͬ�Ƽ���չ���޹�˾.������ҵ��
# All rights reserved.
#
# �ļ����ƣ�TPS001_8455.py
# �ļ���ʶ��
# ժ    Ҫ����˰����.��ѯ������ϸ
#
# ��ǰ�汾��1.0
# ��    �ߣ�
# ������ڣ�2006��12��05��
#
# ȡ���汾��
# ԭ �� �ߣ�
# ������ڣ�
###############################################################################
import TradeContext, AfaDBFunc,AfaLoggerFunc
import  TipsFunc,os
#LoggerHandler, UtilTools,  UtilTools,
def SubModuleMainFst( ):
    AfaLoggerFunc.tradeInfo( '�����ѯ������ϸ['+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']'  )

    try:
        sqlstr = "SELECT SERIALNO,WORKDATE,TAXPAYCODE,TAXPAYNAME,DRACCNO,AMOUNT,BANKSTATUS,BANKSERNO,CORPSTATUS,CORPSERNO,ERRORMSG FROM TIPS_MAINTRANSDTL WHERE 1=1 "
        #��������
        if not QueryBrno(TradeContext.brno):
            sqlstr = sqlstr + " AND BRNO='"     +  TradeContext.brno   + "'"
        else:
            sqlstr = sqlstr + " AND NOTE3='"     +  TradeContext.PayBkCode   + "'"    
            
        if( TradeContext.existVariable('serNo') and len(TradeContext.serNo) > 0 ):
             sqlstr = sqlstr + " AND SERIALNO='"     +  TradeContext.serNo   + "'"
        else:
            sqlstr = sqlstr + " AND REVTRANF='" +  "0"                     + "'"
        
            sqlstr = sqlstr + " AND WORKDATE BETWEEN '" + TradeContext.beginDate + "' AND '"+ TradeContext.endDate+"'"
        
            if ( TradeContext.existVariable('transStatus') and len(TradeContext.transStatus) > 0 ):
                if ( TradeContext.transStatus=='1' ):              #�ɹ�
                    AfaLoggerFunc.tradeInfo('>>>��ѯ�ɹ���ˮ')
                    sqlstr = sqlstr + " AND BANKSTATUS='0'"
                    sqlstr = sqlstr + " AND CORPSTATUS='0'"
        
                elif ( TradeContext.transStatus=='2' ):            #ʧ��
                    AfaLoggerFunc.tradeInfo('>>>��ѯʧ����ˮ')
                    sqlstr = sqlstr + " AND BANKSTATUS='1'"
        
                elif ( TradeContext.transStatus=='3' ):            #�쳣
                    AfaLoggerFunc.tradeInfo('>>>��ѯ�쳣��ˮ')
                    sqlstr = sqlstr + " AND ( BANKSTATUS='2'"
                    sqlstr = sqlstr + " OR (BANKSTATUS='0' AND CORPSTATUS='1')"
                    sqlstr = sqlstr + " OR (BANKSTATUS='0' AND CORPSTATUS='2') )"
        
                else:
                    AfaLoggerFunc.tradeInfo('>>>��ѯȫ����ˮ')
                    
            if ( TradeContext.existVariable('transChannel') and len(TradeContext.transChannel) > 0 ):
                if ( TradeContext.transChannel=='1' ):              #����ɷ�
                    AfaLoggerFunc.tradeInfo('>>>����ɷ�')
                    sqlstr = sqlstr + " AND TRADETYPE='1'"
        
                elif ( TradeContext.transChannel=='7' ):            #������ʵʱ�ɷ�
                    AfaLoggerFunc.tradeInfo('>>>������ʵʱ�ɷ�')
                    sqlstr = sqlstr + " AND TRADETYPE='7'"
        
                elif ( TradeContext.transChannel=='8' ):            #�����������ɷ�
                    AfaLoggerFunc.tradeInfo('>>>�����������ɷ�')
                    sqlstr = sqlstr + " AND TRADETYPE='8'"
        
                else:
                    AfaLoggerFunc.tradeInfo('>>>ȫ��')
        
            if ( TradeContext.existVariable('userno') and len(TradeContext.userno) > 0 ):
                sqlstr = sqlstr + " AND TAXPAYCODE='" + TradeContext.userno + "'"
        
        AfaLoggerFunc.tradeInfo(sqlstr)
    
        records = AfaDBFunc.SelectSql( sqlstr )
        if ( records==None or len(records) == 0 ):
            return TipsFunc.ExitThisFlow('A0001', '�޽�����ϸ')
    
        else:
            AfaLoggerFunc.tradeInfo('�ܹ���[' + str(len(records)) + ']����ˮ')
    
        mx_file_name = os.environ['AFAP_HOME'] + '/tmp/' + 'AH_' + TradeContext.teller + '.txt'
        TradeContext.tradeResponse.append(['fileName',  'AH_' + TradeContext.teller + '.txt'])
    
        if (os.path.exists(mx_file_name) and os.path.isfile(mx_file_name)):
            #�ļ�����,��ɾ��-�ٴ���
            os.system("rm " + mx_file_name)
    
        sfp = open(mx_file_name, "w")
        AfaLoggerFunc.tradeInfo('��ϸ�ļ�=['+mx_file_name+']')
    
        i = 0
        while ( i  < len(records) ):
            A0 = str(records[i][0]).strip()         #SERIALNO
            A1 = str(records[i][1]).strip()         #WORKDATE
            A2 = str(records[i][2]).strip()         #USERNO
            A3 = str(records[i][3]).strip()         #USERNAME
            A4 = str(records[i][4]).strip()         #ACCNO
            A5 = str(records[i][5]).strip()         #AMOUNT
            A6 = str(records[i][6]).strip()         #BANKSTATUS
            A7 = str(records[i][7]).strip()         #SERIALNO
            A8 = str(records[i][8]).strip()         #CORPSTATUS
            A9 = str(records[i][9]).strip()         #CORPSERNO
            A10 = str(records[i][10]).strip()         #ERRORMSG
            
            sfp.write(A0 +  '|'  +  A1 +  '|'  +  A2 +  '|'  +  A3 +  '|'  +  A4 +  '|'  +  A5 +  '|'  +  A6  +  '|'  +  A7 +  '|' +  A8 +  '|'+  A9 +  '|' +  A10 +  '|' + '\n')
    
            i=i+1
    
        sfp.close()
    
        TradeContext.tradeResponse.append(['errorCode',  '0000'])
        TradeContext.tradeResponse.append(['errorMsg',   '���׳ɹ�'])
        return True
    except TipsFunc.flowException, e:
        return TipsFunc.ExitThisFlow('9999',str(e))

def QueryBrno(brno):
    AfaLoggerFunc.tradeInfo('��ѯ������Ӧ�ĸ����к�')
    sql="select brno,paybkcode from TIPS_BRANCH_ADM where brno='"+brno+"'"
    AfaLoggerFunc.tradeInfo(sql)
    records=AfaDBFunc.SelectSql(sql)
    if records==None:
        return False
    elif(len(records)==0):
        return False
    else:
        TradeContext.PayBkCode=records[0][1]
        return True
        
    
    