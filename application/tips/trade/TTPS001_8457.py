# -*- coding: gbk -*-
###############################################################################
# Copyright (c) 2006,������ͬ�Ƽ���չ���޹�˾.������ҵ��
# All rights reserved.
#
# �ļ����ƣ�TTPS001_8457.py
# �ļ���ʶ��
# ժ    Ҫ����˰����.���˲�ѯ
# ��ǰ�汾��1.0
# ��    �ߣ�
# ������ڣ�2008��12��05��
#
# ȡ���汾��
# ԭ �� �ߣ�
# ������ڣ�
###############################################################################
import TradeContext, AfaDBFunc,AfaLoggerFunc,os,TipsFunc
import UtilTools
def SubModuleMainFst( ):
    AfaLoggerFunc.tradeInfo( '������˲�ѯ[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' )
    #������״̬,��ȡ�����к�,�տ��к�
    if not TipsFunc.ChkBranchStatus():
        return TipsFunc.ExitThisFlow( 'A0027', '������״̬ʧ��' )

    #�ϼ�        
    if not sumall():
        return False

    #��ϸд���ļ�
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
    ###################################################################################
    #guanbj 20091105 maps��tips�Ķ��˳ɹ��󼴿ɲ�ѯ���˽��
    #sqlStr=sqlStr+" AND CHKFLAG='0' and CORPCHKFLAG='0'"
    sqlStr=sqlStr+" AND CORPCHKFLAG='0'"
    ###################################################################################
    sqlStr=sqlStr+" ORDER BY SERIALNO"
    sqlStr_detail="SELECT WORKDATE,DRACCNO,TAXPAYNAME,SERIALNO,TAXPAYCODE,cast(AMOUNT as decimal(17,2)) FROM TIPS_MAINTRANSDTL  "
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
            A0 = str(Records[i][0]).strip()         #��������
            A1 = str(Records[i][1]).strip()         #�ʺ�     
            A2 = str(Records[i][2]).strip()         #����   
            A3 = str(Records[i][3]).strip()         #������ˮ
            A4 = str(Records[i][4]).strip()         #��˰�˱���
            A5 = str(Records[i][5]).strip()         #���       

            sfp.write(A0 +  '|'  +  A1 +  '|'  +  A2 +  '|'  +  A3 +  '|'  +  A4 +  '|'  +  A5 +  '|' + '\n')
            
    sfp.close()                
    TradeContext.tradeResponse.append(['errorCode','0000'])
    TradeContext.tradeResponse.append(['errorMsg','���׳ɹ�'])

    AfaLoggerFunc.tradeInfo( '�˳����˲�ѯ[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' )
    return True

#��ѯ���˳ɹ�����������ͽ��
def sumall():       
    #�ɹ��ܼ�
    AfaLoggerFunc.tradeInfo('��ѯ���˳ɹ������ͽ��')
    sumsql="SELECT count(*),sum(cast(amount as decimal(17,2))) "
    sumsql = sumsql + "FROM TIPS_MAINTRANSDTL  "
    sumsql = sumsql + "WHERE NOTE1 ='"+TradeContext.checkDate+"'"
    sumsql = sumsql + " AND NOTE2 = '"+TradeContext.checkNo+"'"
    ###################################################################################
    #guanbj 20091105 �޸Ĳ�ѯ���˽��ֻ��ѯmaps��tips�Ķ��˳ɹ�����Ϣ
    #sumsql = sumsql + " AND CHKFLAG='0' and CORPCHKFLAG='0'"
    sumsql=sumsql +" AND CORPCHKFLAG='0'"
    ###################################################################################
    sumsql = sumsql + " AND NOTE3='"  + TradeContext.payBkCode.strip()  + "'"   
    sumsql = sumsql + " AND NOTE4='"  + TradeContext.payeeBankNo.strip()  + "'"
    sumSucc=AfaDBFunc.SelectSql( sumsql)
    AfaLoggerFunc.tradeInfo(sumsql)
    AfaLoggerFunc.tradeInfo("�ɹ��ܼ�"+repr(sumSucc))
    if( sumSucc == None ):
        # None ��ѯʧ��
        return TipsFunc.ExitThisFlow( 'A0025', '���ݿ�������� ͳ�Ƴɹ���������!'+AfaDBFunc.sqlErrMsg  )
    if sumSucc[0][0] == 0:
        return TipsFunc.ExitThisFlow( 'A0027', 'û����������������' )

    sumSucc=UtilTools.ListFilterNone(sumSucc,0)
    TradeContext.tradeResponse.append( ['sSum', str(sumSucc[0][0])] )  
    TradeContext.tradeResponse.append( ['sAmt', str(sumSucc[0][1])] )

    return True
    
