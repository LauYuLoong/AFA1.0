# -*- coding: gbk -*-
###############################################################################
# Copyright (c) 2006,������ͬ�Ƽ���չ���޹�˾.Ӧ�ÿ���II��
# All rights reserved.
#
# �ļ����ƣ�T003001_038504.py
# �ļ���ʶ��
# ժ    Ҫ����˰����.���˲�ѯ
#   queryType ��ѯ��� 0.�ϼ��� 1.���˳ɹ���ϸ 2.���˲�����ϸ 
# ��ǰ�汾��1.0
# ��    �ߣ�
# ������ڣ�2006��12��05��
#
# ȡ���汾��
# ԭ �� �ߣ�
# ������ڣ�
###############################################################################
import TradeContext, AfaDBFunc,AfaLoggerFunc,ConfigParser,os,TipsFunc
import UtilTools
def SubModuleMainFst( ):
    try:
        #������״̬,��ȡ�����к�,�տ��к�
        if not TipsFunc.ChkBranchStatus():
            return TipsFunc.ExitThisFlow( 'A0027', '������״̬ʧ��' )
        if not TipsFunc.ChkLiquidStatus():
            return TipsFunc.ExitThisFlow( 'A0027', '������������Ϣʧ��' )
        
        sqlStr = "SELECT BATCHNO,WORKTIME,DEALSTATUS,ERRORMSG,PAYBKCODE,PAYEEBANKNO,CHKACCTTYPE,PRIORCHKACCTORD,TOTALNUM,TOTALAMT FROM TIPS_CHECKADM WHERE "
        sqlStr = sqlStr +" WORKDATE  = '" + TradeContext.checkDate.strip()   + "'"
        sqlStr = sqlStr +" AND BATCHNO = '"      + TradeContext.checkNo.strip()     + "'"
        sqlStr = sqlStr +" AND PAYBKCODE = '"    + TradeContext.payBkCode.strip()   + "'"
        sqlStr = sqlStr +" and PAYEEBANKNO  = '" + TradeContext.payeeBankNo.strip()      + "'"
        if TradeContext.brno != TradeContext.__mainBrno__: #ҵ��������
            sqlStr = sqlStr + " AND BRNO ='"  + TradeContext.brno  + "'"
        Records = AfaDBFunc.SelectSql( sqlStr )
        AfaLoggerFunc.tradeInfo(sqlStr)
        if( Records == None ):
            AfaLoggerFunc.tradeFatal('�������������쳣:'+AfaDBFunc.sqlErrMsg)
            return TipsFunc.ExitThisFlow( 'A0027', '���ݿ���������������쳣' )
        elif(len(Records)==0):
            return TipsFunc.ExitThisFlow( 'A0027', '�޴�����' )
        else:
            TradeContext.tradeResponse.append(['bNo'    ,str(Records[0][0])])           #�������κ�
            TradeContext.tradeResponse.append(['wTime'  ,str(Records[0][1])])           #����ʱ��
            TradeContext.tradeResponse.append(['dSta'   ,str(Records[0][2])])           #����״̬
            TradeContext.tradeResponse.append(['errM'   ,str(Records[0][3])])           #���δ�����
            TradeContext.tradeResponse.append(['PBk'    ,str(Records[0][4])])           #�����к�
            TradeContext.tradeResponse.append(['PBkN'   ,''])       #����������
            TradeContext.tradeResponse.append(['PeBk'   ,str(Records[0][5])])           #�տ��к�
            TradeContext.tradeResponse.append(['PeBkN'  ,''])           #�տ�������
            TradeContext.tradeResponse.append(['chkType',str(Records[0][6])])           #������������
            TradeContext.tradeResponse.append(['pBNo'   ,str(Records[0][7])])           #��һ��������
            TradeContext.payeeBankNo=Records[0][5]
            #�ϼ�        
            if not sumall():
                return False
                
    
        #д���ļ�
        mx_file_name = os.environ['AFAP_HOME'] + '/tmp/' + 'AH_' + TradeContext.teller + '.txt'
        TradeContext.tradeResponse.append(['fileName',  'AH_' + TradeContext.teller + '.txt'])
        
        if (os.path.exists(mx_file_name) and os.path.isfile(mx_file_name)):
            #�ļ�����,��ɾ��-�ٴ���
            os.system("rm " + mx_file_name)
        
        sfp = open(mx_file_name, "w")
        AfaLoggerFunc.tradeInfo('��ϸ�ļ�=['+mx_file_name+']')
        
        #��ϸ
        sqlStr = ''
        sqlStr = sqlStr + "WHERE NOTE1 ='" +TradeContext.checkDate +"'"
        sqlStr = sqlStr + " AND NOTE2 = '" +TradeContext.checkNo   +"'"
        sqlStr = sqlStr + " AND NOTE3 ='"  + TradeContext.payBkCode.strip()  + "'"   
        sqlStr = sqlStr + " AND NOTE4 ='"  + TradeContext.payeeBankNo.strip()  + "'"
        if TradeContext.brno != TradeContext.__mainBrno__: #ҵ��������
            sqlStr = sqlStr + " AND BRNO ='"  + TradeContext.brno  + "'"
        sqlStr=sqlStr+" AND (CHKFLAG!='9'  and  CORPCHKFLAG='9' or CHKFLAG!='0'  and  CORPCHKFLAG='0')"
        sqlStr=sqlStr+" ORDER BY SERIALNO"
        sqlStr_detail="SELECT WORKDATE,DRACCNO,TAXPAYCODE,cast(AMOUNT as decimal(17,2)),SERIALNO,CORPSERNO,CHKFLAG,CORPCHKFLAG FROM TIPS_MAINTRANSDTL  "
        sqlStr_detail=sqlStr_detail+sqlStr
        AfaLoggerFunc.tradeInfo(sqlStr_detail)
        Records = AfaDBFunc.SelectSql( sqlStr_detail )
        if( Records == None or Records <0):
            sfp.close()
            return TipsFunc.ExitThisFlow( 'A0027', '������쳣:'+AfaDBFunc.sqlErrMsg )
        elif( len( Records )==0 ):
            sfp.close()
            return TipsFunc.ExitThisFlow( 'A0027', 'û����������������' )
        else:
            for i in range(0,len(Records)):
                A0 = str(Records[i][0]).strip()         #WORKDATE
                A1 = str(Records[i][1]).strip()         #ACCNO        
                A2 = str(Records[i][2]).strip()         #USERNO       
                A3 = str(Records[i][3]).strip()         #AMOUNT       
                A4 = str(Records[i][4]).strip()         #SERIALNO
                A5 = str(Records[i][5]).strip()         #CORPSERIALNO
                if (Records[i][6]=='0' and Records[i][7]=='0'):
                    A6 = "���˳ɹ�"
                elif (Records[i][6]!='9' and Records[i][7]=='9'):
                    A6 = "���б����ж�"
                elif (Records[i][6]!='0' and Records[i][7]=='0'):
                    A6 = "���б����ж�"
                
                sfp.write(A0 +  '|'  +  A1 +  '|'  +  A2 +  '|'  +  A3 +  '|'  +  A4 +  '|'  +  A5 +  '|'  +  A6  +  '|' + '\n')
                
        sfp.close()                
        TradeContext.tradeResponse.append(['errorCode','0000'])
        TradeContext.tradeResponse.append(['errorMsg','���׳ɹ�'])

        AfaLoggerFunc.tradeInfo( '�˳����˲�ѯ[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' )
        return True
    except TipsFunc.flowException, e:
        # print e        
        TipsFunc.exitMainFlow( )
        
    except Exception, e:
        # print e
        TipsFunc.exitMainFlow(str(e))

#��ѯ���˳ɹ�����������ͽ��
def sumall():       
    #�ɹ��ܼ�
    AfaLoggerFunc.tradeInfo('��ѯ���˳ɹ�����������ͽ��')
    sumsql="SELECT count(*),sum(cast(amount as decimal(17,2))) "
    sumsql = sumsql + "FROM TIPS_MAINTRANSDTL  "
    sumsql = sumsql + "WHERE NOTE1 ='"+TradeContext.checkDate+"'"
    sumsql = sumsql + " AND NOTE2 = '"+TradeContext.checkNo+"'"
    sumsql = sumsql + " AND CHKFLAG='0' and CORPCHKFLAG='0'"
    sumsql = sumsql + " AND NOTE3='"  + TradeContext.payBkCode.strip()  + "'"   
    sumsql = sumsql + " AND NOTE4='"  + TradeContext.payeeBankNo.strip()  + "'"
    sumSucc=AfaDBFunc.SelectSql( sumsql)
    AfaLoggerFunc.tradeInfo(sumsql)
    AfaLoggerFunc.tradeInfo("�ɹ��ܼ�"+repr(sumSucc))
    if( sumSucc == None or sumSucc < 0 ):
        # None ��ѯʧ��
        return TipsFunc.ExitThisFlow( 'A0025', '���ݿ�������� ͳ�Ƴɹ���������!'+AfaDBFunc.sqlErrMsg  )
    #�����ܼ�
    sumsql="SELECT count(*),sum(cast(amount as decimal(17,2))) "
    sumsql = sumsql + "FROM TIPS_MAINTRANSDTL  "
    sumsql = sumsql + "WHERE NOTE1 ='"+TradeContext.checkDate+"'"
    sumsql = sumsql + " AND  NOTE2 = '"+TradeContext.checkNo+"'"
    sumsql = sumsql + " AND (CHKFLAG!='9'  and  CORPCHKFLAG='9' or CHKFLAG!='0'  and  CORPCHKFLAG='0')"
    sumsql = sumsql + " AND  NOTE3='"  + TradeContext.payBkCode.strip()  + "'"   
    sumsql = sumsql + " AND NOTE4='"  + TradeContext.payeeBankNo.strip()  + "'"
    AfaLoggerFunc.tradeInfo(sumsql)
    sumFail=AfaDBFunc.SelectSql( sumsql)
    AfaLoggerFunc.tradeInfo("�����ܼ�"+repr(sumFail))
    if( sumFail == None or sumFail < 0):
        # None ��ѯʧ��
        return TipsFunc.ExitThisFlow( 'A0025', '���ݿ�������� ͳ�Ʋ����������!' +AfaDBFunc.sqlErrMsg  )
    sumSucc=UtilTools.ListFilterNone(sumSucc,0)
    sumFail=UtilTools.ListFilterNone(sumFail,0)
    TradeContext.tradeResponse.append( ['sSum', str(sumSucc[0][0])] )  
    TradeContext.tradeResponse.append( ['sAmt', str(sumSucc[0][1])] )
    TradeContext.tradeResponse.append( ['fSum', str(sumFail[0][0])] )  
    TradeContext.tradeResponse.append( ['fAmt', str(sumFail[0][1])] )  
    return True
    
