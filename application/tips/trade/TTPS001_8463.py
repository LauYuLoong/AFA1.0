# -*- coding: gbk -*-
###############################################################################
# Copyright (c) 2006,������ͬ�Ƽ���չ���޹�˾.Ӧ�ÿ���II��
# All rights reserved.
#
# �ļ����ƣ�T1004_8463.py
# �ļ���ʶ��
# ժ    Ҫ����˰����.TIPS���в����鿴
#
# ��ǰ�汾��1.0
# ��    �ߣ�
# ������ڣ�2007-11-5 16:02
###############################################################################
import TradeContext,  AfaFlowControl, AfaDBFunc,AfaLoggerFunc
import  os
#TipsFunc,LoggerHandler, UtilTools,UtilTools,
def SubModuleMainFst( ):
    AfaLoggerFunc.tradeInfo( '����TIPS���в����鿴['+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']'  )

    try:
        sqlstr = "select ParamTypeNo,ParamTypeDesc,DetailNo,DetailDesc,ParamValue from TIPS_RUNPARAM  WHERE"
        sqlstr = sqlstr + " ParamTypeNo='"        +  TradeContext.paramType      + "'"
        sqlstr = sqlstr + " order by DetailNo "
        AfaLoggerFunc.tradeInfo(sqlstr)
    
        records = AfaDBFunc.SelectSql( sqlstr )
        if ( records==None or len(records) == 0 ):
            return AfaFlowControl.ExitThisFlow('A0001', 'û�����������ļ�¼')
    
        mx_file_name = os.environ['AFAP_HOME'] + '/tmp/' + 'AH_' + TradeContext.teller + '.txt'
        TradeContext.tradeResponse.append(['fileName',  'AH_' + TradeContext.teller + '.txt'])
    
        if (os.path.exists(mx_file_name) and os.path.isfile(mx_file_name)):
            #�ļ�����,��ɾ��-�ٴ���
            os.system("rm " + mx_file_name)
    
        sfp = open(mx_file_name, "w")
        AfaLoggerFunc.tradeInfo('��ϸ�ļ�=['+mx_file_name+']')
    
        i = 0
        while ( i  < len(records) ):
            A0 = str(records[i][0]).strip()         #ParamTypeNo
            A1 = str(records[i][1]).strip()         #ParamTypeDesc
            A2 = str(records[i][2]).strip()         #DetailNo
            A3 = str(records[i][3]).strip()         #DetailDesc
            A4 = str(records[i][4]).strip()         #ParamValue
    
            sfp.write(A0 +  '|'  +  A1 +  '|'  +  A2 +  '|'  +  A3 +  '|'  +  A4 +  '|'  + '\n')
    
            i=i+1
    
        sfp.close()
    
        TradeContext.tradeResponse.append(['errorCode',  '0000'])
        TradeContext.tradeResponse.append(['errorMsg',   '���׳ɹ�'])
        AfaLoggerFunc.tradeInfo( '�˳�TIPS���в����鿴['+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']'  )
        return True
    except AfaFlowControl.flowException, e:
        return AfaFlowControl.ExitThisFlow('9999',str(e))
