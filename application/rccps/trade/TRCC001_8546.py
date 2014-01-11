# -*- coding: gbk -*-
##################################################################
#   ũ����.��ѯҵ��.��һ��ܺ˶Բ�ѯ
#=================================================================
#   �����ļ�:   TRCC001_8546.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  ������
#   �޸�ʱ��:   2008-06-12
##################################################################
import TradeContext,AfaLoggerFunc,AfaFlowControl,AfaUtilTools,rccpsDBTrcc_hddzhz,os
import rccpsDBTrcc_trcbka,AfaDBFunc

from types import *
from rccpsConst import *

def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(1.���ز���)����[TRC001_8546]����***' )
    
    #=====�жϽӿ��Ƿ����====
    if not TradeContext.existVariable("NCCWKDAT"):
        return AfaFlowControl.ExitThisFlow('M999','���Ĺ�������[NCCWKDAT]������')

    #=====���кŲ�ѯ====
    sql = "NCCWKDAT = '" + TradeContext.NCCWKDAT + "'"
    
    #=====��ѯ���ݿ⣬�õ���ѯ�����====
    record=rccpsDBTrcc_hddzhz.selectm(TradeContext.RECSTRNO,10,sql,"")  
    if record == None:
        return AfaFlowControl.ExitThisFlow('D000','���ݿ����ʧ��')
    elif len(record) <= 0:
        return AfaFlowControl.ExitThisFlow('D000','û�����������ļ�¼')
    else:
        #=====���ļ�����====
        filename = 'rccps_' + TradeContext.BETELR + '_' + AfaUtilTools.GetSysDate() + '_' + TradeContext.TransCode 
        try:
            fpath=os.environ["AFAP_HOME"]+"/tmp/"
            f=open(fpath+filename,"w")
        except IOError:
            return AfaFlowControl.ExitThisFlow('A999','���ļ�ʧ��')

        #=====��֯�����ļ�====
        for i in range( 0, len(record) ):
            #=====�ж�ҵ�����ͺ�������ʾ=====
            if( record[i]['TRCCO'] == '0000000' and record[i]['BRSFLG'] == '0' ):
                #=====�ϼ� ���ʻ���====
                AfaLoggerFunc.tradeInfo('�ϼ� ���ʻ���')
                                
                #=====�������ܽ��====
                AfaLoggerFunc.tradeInfo('�ϼ� ���ʻ���__��������')

                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat='" + PL_BCSTAT_MFESTL + "'"
                trcbka_sql = "select sum(OCCAMT) from rcc_trcbka where BRSFLG='0' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                trcbka_sql = trcbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeInfo('trcbka_sqlΪ��' + trcbka_sql)
                trcbka_list = AfaDBFunc.SelectSql(trcbka_sql)
                if( trcbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','��Ʊ��Ϣ�Ǽǲ�����ʧ��')
                elif( len(trcbka_list) <= 0 ):
                    TradeContext.INRCTAMT = 0.00
                else:
                    if( trcbka_list[0][0] == None ):
                        TradeContext.INRCTAMT = 0.00
                    else:
                        TradeContext.INRCTAMT = trcbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCTAMTΪ��'+  str(TradeContext.INRCTAMT))
                
                #=====�跽���ܽ��====
                AfaLoggerFunc.tradeInfo('�ϼ� ���ʻ���__�跽����')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat='" + PL_BCSTAT_MFESTL + "'"
                trcbka_sql = "select sum(OCCAMT) from rcc_trcbka where BRSFLG='0' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                trcbka_sql = trcbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeInfo('trcbka_sqlΪ��' + trcbka_sql)
                trcbka_list = AfaDBFunc.SelectSql(trcbka_sql)
                if( trcbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','��Ʊ��Ϣ�Ǽǲ�����ʧ��')
                elif( len(trcbka_list) <= 0 ):
                    TradeContext.INRDTAMT = 0.00
                else:
                    if( trcbka_list[0][0] == None ):
                        TradeContext.INRDTAMT = 0.00
                    else:
                        TradeContext.INRDTAMT = trcbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRDTAMTΪ��'+  str(TradeContext.INRDTAMT))
                
                #=====������ܽ��====
                AfaLoggerFunc.tradeInfo('�ϼ� ���ʻ���__�������')
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT - TradeContext.INRDTAMT
                AfaLoggerFunc.tradeInfo('INROFSTAMTΪ��'+ str(TradeContext.INROFSTAMT))
                
            
###########################################################################################################################
            
            elif( record[i]['TRCCO'] == '0000000' and record[i]['BRSFLG'] == '1' ):
                #=====�ϼ� ���ʻ���====
                AfaLoggerFunc.tradeInfo('�ϼ� ���ʻ���')
                #=====�������ܽ��====
                AfaLoggerFunc.tradeInfo('�ϼ� ���ʻ���__��������')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in('70','71','80')"
                trcbka_sql = "select sum(OCCAMT) from rcc_trcbka where BRSFLG='1' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                trcbka_sql = trcbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeInfo('trcbka_sqlΪ��' + trcbka_sql)
                trcbka_list = AfaDBFunc.SelectSql(trcbka_sql)
                if( trcbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','��Ʊ��Ϣ�Ǽǲ�����ʧ��')
                elif( len(trcbka_list) <= 0 ):
                    TradeContext.INRCTAMT = 0.00
                else:
                    if( trcbka_list[0][0] == None ):
                        TradeContext.INRCTAMT = 0.00
                    else:
                        TradeContext.INRCTAMT = trcbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCTAMTΪ��'+  str(TradeContext.INRCTAMT))
                
                #=====�跽���ܽ��====
                AfaLoggerFunc.tradeInfo('�ϼ� ���ʻ���__�跽����')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in('70','71','80')"
                trcbka_sql = "select sum(OCCAMT) from rcc_trcbka where BRSFLG='1' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                trcbka_sql = trcbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeInfo('trcbka_sqlΪ��' + trcbka_sql)
                trcbka_list = AfaDBFunc.SelectSql(trcbka_sql)
                if( trcbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','��Ʊ��Ϣ�Ǽǲ�����ʧ��')
                elif( len(trcbka_list) <= 0 ):
                    TradeContext.INRDTAMT = 0.00
                else:
                    if( trcbka_list[0][0] == None ):
                        TradeContext.INRDTAMT = 0.00
                    else:
                        TradeContext.INRDTAMT = trcbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRDTAMTΪ��'+  str(TradeContext.INRDTAMT))
                
                #=====������ܽ��====
                AfaLoggerFunc.tradeInfo('�ϼ� ���ʻ���__�������')   
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT - TradeContext.INRDTAMT
                AfaLoggerFunc.tradeInfo('INROFSTAMTΪ��'+ str(TradeContext.INROFSTAMT))
            
############################################################################################################################# 
            
            elif( record[i]['TRCCO'] == '0000000' and record[i]['BRSFLG'] == '9' ):
                #=====�ϼ� �������====
                AfaLoggerFunc.tradeInfo('�ϼ� �������')
                #=====�������ܽ��====
                AfaLoggerFunc.tradeInfo('�ϼ� �������__��������')
                
#                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in('70','71','42','80')"
#                trcbka_sql = "select sum(OCCAMT) from rcc_trcbka where DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
#                trcbka_sql = trcbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
#                AfaLoggerFunc.tradeInfo('trcbka_sqlΪ��' + trcbka_sql)
#                trcbka_list = AfaDBFunc.SelectSql(trcbka_sql)
#                if( trcbka_list == None ):
#                    f.close()
#                    return AfaFlowControl.ExitThisFlow('D000','��Ʊ��Ϣ�Ǽǲ�����ʧ��')
#                elif( len(trcbka_list) <= 0 ):
#                    TradeContext.INRCTAMT = 0.00
#                else:
#                    if( trcbka_list[0][0] == None ):
#                        TradeContext.INRCTAMT = 0.00
#                    else:
#                        TradeContext.INRCTAMT = trcbka_list[0][0]
                        
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat='42'"
                trcbka_sql = "select sum(OCCAMT) from rcc_trcbka where BRSFLG='0' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                trcbka_sql = trcbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeInfo('trcbka_sqlΪ��' + trcbka_sql)
                trcbka_list = AfaDBFunc.SelectSql(trcbka_sql)
                if( trcbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','��Ʊ��Ϣ�Ǽǲ�����ʧ��')
                elif( len(trcbka_list) <= 0 ):
                    TradeContext.INRCTAMT1 = 0.00
                else:
                    if( trcbka_list[0][0] == None ):
                        TradeContext.INRCTAMT1 = 0.00
                    else:
                        TradeContext.INRCTAMT1 = trcbka_list[0][0]
                        
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in('70','71','80')"
                trcbka_sql = "select sum(OCCAMT) from rcc_trcbka where BRSFLG='1' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                trcbka_sql = trcbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeInfo('trcbka_sqlΪ��' + trcbka_sql)
                trcbka_list = AfaDBFunc.SelectSql(trcbka_sql)
                if( trcbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','��Ʊ��Ϣ�Ǽǲ�����ʧ��')
                elif( len(trcbka_list) <= 0 ):
                    TradeContext.INRCTAMT2 = 0.00
                else:
                    if( trcbka_list[0][0] == None ):
                        TradeContext.INRCTAMT2 = 0.00
                    else:
                        TradeContext.INRCTAMT2 = trcbka_list[0][0]
                        
                TradeContext.INRCTAMT = TradeContext.INRCTAMT1 + TradeContext.INRCTAMT2
                                        
                AfaLoggerFunc.tradeInfo('INRCTAMTΪ��'+  str(TradeContext.INRCTAMT))
                
                #=====�跽���ܽ��====
                AfaLoggerFunc.tradeInfo('�ϼ� �������__�跽����')
                
#                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in('70','71','42','80')"
#                trcbka_sql = "select sum(OCCAMT) from rcc_trcbka where DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
#                trcbka_sql = trcbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
#                AfaLoggerFunc.tradeInfo('trcbka_sqlΪ��' + trcbka_sql)
#                trcbka_list = AfaDBFunc.SelectSql(trcbka_sql)
#                if( trcbka_list == None ):
#                    f.close()
#                    return AfaFlowControl.ExitThisFlow('D000','��Ʊ��Ϣ�Ǽǲ�����ʧ��')
#                elif( len(trcbka_list) <= 0 ):
#                    TradeContext.INRDTAMT = 0.00
#                else:
#                    if( trcbka_list[0][0] == None ):
#                        TradeContext.INRDTAMT = 0.00
#                    else:
#                        TradeContext.INRDTAMT = trcbka_list[0][0]

                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat='42'"
                trcbka_sql = "select sum(OCCAMT) from rcc_trcbka where BRSFLG='0' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                trcbka_sql = trcbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeInfo('trcbka_sqlΪ��' + trcbka_sql)
                trcbka_list = AfaDBFunc.SelectSql(trcbka_sql)
                if( trcbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','��Ʊ��Ϣ�Ǽǲ�����ʧ��')
                elif( len(trcbka_list) <= 0 ):
                    TradeContext.INRDTAMT1 = 0.00
                else:
                    if( trcbka_list[0][0] == None ):
                        TradeContext.INRDTAMT1 = 0.00
                    else:
                        TradeContext.INRDTAMT1 = trcbka_list[0][0]
                        
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in('70','71','80')"
                trcbka_sql = "select sum(OCCAMT) from rcc_trcbka where BRSFLG='1' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                trcbka_sql = trcbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeInfo('trcbka_sqlΪ��' + trcbka_sql)
                trcbka_list = AfaDBFunc.SelectSql(trcbka_sql)
                if( trcbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','��Ʊ��Ϣ�Ǽǲ�����ʧ��')
                elif( len(trcbka_list) <= 0 ):
                    TradeContext.INRDTAMT2 = 0.00
                else:
                    if( trcbka_list[0][0] == None ):
                        TradeContext.INRDTAMT2 = 0.00
                    else:
                        TradeContext.INRDTAMT2 = trcbka_list[0][0]
                        
                TradeContext.INRDTAMT = TradeContext.INRDTAMT1 + TradeContext.INRDTAMT2
                                        
                AfaLoggerFunc.tradeInfo('INRDTAMTΪ��'+  str(TradeContext.INRDTAMT))
                
                #=====������ܽ��====
                AfaLoggerFunc.tradeInfo('�ϼ� �������__�������')
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT - TradeContext.INRDTAMT
                AfaLoggerFunc.tradeInfo('INROFSTAMTΪ��'+ str(TradeContext.INROFSTAMT))   
            
##############################################################################################################################            
            
            elif( record[i]['TRCCO'] == '2000001' and record[i]['BRSFLG'] == '0' ):
                #=====��� ����====
                AfaLoggerFunc.tradeInfo('��� ����')
                #=====�������ܽ��====
                AfaLoggerFunc.tradeInfo('��� ����__��������')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat='" + PL_BCSTAT_MFESTL + "'"
                trcbka_sql = "select sum(OCCAMT) from rcc_trcbka where TRCCO='2000001' and BRSFLG='0' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                trcbka_sql = trcbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeInfo('trcbka_sqlΪ��' + trcbka_sql)
                trcbka_list = AfaDBFunc.SelectSql(trcbka_sql)
                if( trcbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','��Ʊ��Ϣ�Ǽǲ�����ʧ��')
                elif( len(trcbka_list) <= 0 ):
                    TradeContext.INRCTAMT = 0.00
                else:
                    if( trcbka_list[0][0] == None ):
                        TradeContext.INRCTAMT = 0.00
                    else:
                        TradeContext.INRCTAMT = trcbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCTAMTΪ��'+  str(TradeContext.INRCTAMT))
                
                #=====�跽���ܽ��====
                AfaLoggerFunc.tradeInfo('��� ����__�跽����')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat='" + PL_BCSTAT_MFESTL + "'"
                trcbka_sql = "select sum(OCCAMT) from rcc_trcbka where TRCCO='2000001' and BRSFLG='0' and  DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                trcbka_sql = trcbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeInfo('trcbka_sqlΪ��' + trcbka_sql)
                trcbka_list = AfaDBFunc.SelectSql(trcbka_sql)
                if( trcbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','��Ʊ��Ϣ�Ǽǲ�����ʧ��')
                elif( len(trcbka_list) <= 0 ):
                    TradeContext.INRDTAMT = 0.00
                else:
                    if( trcbka_list[0][0] == None ):
                        TradeContext.INRDTAMT = 0.00
                    else:
                        TradeContext.INRDTAMT = trcbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRDTAMTΪ��'+  str(TradeContext.INRDTAMT))
                
                #=====������ܽ��====
                AfaLoggerFunc.tradeInfo('��� ����__�������')   
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT - TradeContext.INRDTAMT
                AfaLoggerFunc.tradeInfo('INROFSTAMTΪ��'+ str(TradeContext.INROFSTAMT))   
            
##############################################################################################################################            
            
            elif( record[i]['TRCCO'] == '2000001' and record[i]['BRSFLG'] == '1' ):
                #=====��� ����====
                AfaLoggerFunc.tradeInfo('��� ����')
                #=====�������ܽ��====
                AfaLoggerFunc.tradeInfo('��� ����__��������')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in('70','71','80')"
                trcbka_sql = "select sum(OCCAMT) from rcc_trcbka where TRCCO='2000001' and BRSFLG='1' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                trcbka_sql = trcbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeInfo('trcbka_sqlΪ��' + trcbka_sql)
                trcbka_list = AfaDBFunc.SelectSql(trcbka_sql)
                if( trcbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','��Ʊ��Ϣ�Ǽǲ�����ʧ��')
                elif( len(trcbka_list) <= 0 ):
                    TradeContext.INRCTAMT = 0.00
                else:
                    if( trcbka_list[0][0] == None ):
                        TradeContext.INRCTAMT = 0.00
                    else:
                        TradeContext.INRCTAMT = trcbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCTAMTΪ��'+  str(TradeContext.INRCTAMT))
                
                #=====�跽���ܽ��====
                AfaLoggerFunc.tradeInfo('��� ����__�跽����')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in('70','71','80')"
                trcbka_sql = "select sum(OCCAMT) from rcc_trcbka where TRCCO='2000001' and BRSFLG='1' and  DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                trcbka_sql = trcbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeInfo('trcbka_sqlΪ��' + trcbka_sql)
                trcbka_list = AfaDBFunc.SelectSql(trcbka_sql)
                if( trcbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','��Ʊ��Ϣ�Ǽǲ�����ʧ��')
                elif( len(trcbka_list) <= 0 ):
                    TradeContext.INRDTAMT = 0.00
                else:
                    if( trcbka_list[0][0] == None ):
                        TradeContext.INRDTAMT = 0.00
                    else:
                        TradeContext.INRDTAMT = trcbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRDTAMTΪ��'+  str(TradeContext.INRDTAMT))
                
                #=====������ܽ��====
                AfaLoggerFunc.tradeInfo('��� ����__�������') 
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT - TradeContext.INRDTAMT
                AfaLoggerFunc.tradeInfo('INROFSTAMTΪ��'+ str(TradeContext.INROFSTAMT))     
            
##############################################################################################################################            

            elif( record[i]['TRCCO'] == '2000002' and record[i]['BRSFLG'] == '0' ):
                #=====ί���տ�� ����====
                AfaLoggerFunc.tradeInfo('ί���տ�� ����')
                #=====�������ܽ��====
                AfaLoggerFunc.tradeInfo('ί���տ�� ����__��������')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat='" + PL_BCSTAT_MFESTL + "'"
                trcbka_sql = "select sum(OCCAMT) from rcc_trcbka where TRCCO='2000002' and BRSFLG='0' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                trcbka_sql = trcbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeInfo('trcbka_sqlΪ��' + trcbka_sql)
                trcbka_list = AfaDBFunc.SelectSql(trcbka_sql)
                if( trcbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','��Ʊ��Ϣ�Ǽǲ�����ʧ��')
                elif( len(trcbka_list) <= 0 ):
                    TradeContext.INRCTAMT = 0.00
                else:
                    if( trcbka_list[0][0] == None ):
                        TradeContext.INRCTAMT = 0.00
                    else:
                        TradeContext.INRCTAMT = trcbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCTAMTΪ��'+  str(TradeContext.INRCTAMT))
                
                #=====�跽���ܽ��====
                AfaLoggerFunc.tradeInfo('ί���տ�� ����__�跽����')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat='" + PL_BCSTAT_MFESTL + "'"
                trcbka_sql = "select sum(OCCAMT) from rcc_trcbka where TRCCO='2000002' and BRSFLG='0' and  DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                trcbka_sql = trcbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeInfo('trcbka_sqlΪ��' + trcbka_sql)
                trcbka_list = AfaDBFunc.SelectSql(trcbka_sql)
                if( trcbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','��Ʊ��Ϣ�Ǽǲ�����ʧ��')
                elif( len(trcbka_list) <= 0 ):
                    TradeContext.INRDTAMT = 0.00
                else:
                    if( trcbka_list[0][0] == None ):
                        TradeContext.INRDTAMT = 0.00
                    else:
                        TradeContext.INRDTAMT = trcbka_list[0][0]
                        
                #=====������ܽ��====
                AfaLoggerFunc.tradeInfo('ί���տ�� ����__�������')
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT - TradeContext.INRDTAMT
                AfaLoggerFunc.tradeInfo('INROFSTAMTΪ��'+ str(TradeContext.INROFSTAMT))   
            
##############################################################################################################################            

            elif( record[i]['TRCCO'] == '2000002' and record[i]['BRSFLG'] == '1' ):
                #=====ί���տ�� ����====
                AfaLoggerFunc.tradeInfo('ί���տ�� ����')
                #=====�������ܽ��====
                AfaLoggerFunc.tradeInfo('ί���տ�� ����__��������')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in('70','71','80')"
                trcbka_sql = "select sum(OCCAMT) from rcc_trcbka where TRCCO='2000002' and BRSFLG='1' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                trcbka_sql = trcbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeInfo('trcbka_sqlΪ��' + trcbka_sql)
                trcbka_list = AfaDBFunc.SelectSql(trcbka_sql)
                if( trcbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','��Ʊ��Ϣ�Ǽǲ�����ʧ��')
                elif( len(trcbka_list) <= 0 ):
                    TradeContext.INRCTAMT = 0.00
                else:
                    if( trcbka_list[0][0] == None ):
                        TradeContext.INRCTAMT = 0.00
                    else:
                        TradeContext.INRCTAMT = trcbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCTAMTΪ��'+  str(TradeContext.INRCTAMT))
                
                #=====�跽���ܽ��====
                AfaLoggerFunc.tradeInfo('ί���տ�� ����__�跽����')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in('70','71','80')"
                trcbka_sql = "select sum(OCCAMT) from rcc_trcbka where TRCCO='2000002' and BRSFLG='1' and  DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                trcbka_sql = trcbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeInfo('trcbka_sqlΪ��' + trcbka_sql)
                trcbka_list = AfaDBFunc.SelectSql(trcbka_sql)
                if( trcbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','��Ʊ��Ϣ�Ǽǲ�����ʧ��')
                elif( len(trcbka_list) <= 0 ):
                    TradeContext.INRDTAMT = 0.00
                else:
                    if( trcbka_list[0][0] == None ):
                        TradeContext.INRDTAMT = 0.00
                    else:
                        TradeContext.INRDTAMT = trcbka_list[0][0]
                        
                #=====������ܽ��====
                AfaLoggerFunc.tradeInfo('ί���տ�� ����__�������') 
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT - TradeContext.INRDTAMT
                AfaLoggerFunc.tradeInfo('INROFSTAMTΪ��'+ str(TradeContext.INROFSTAMT))   
            
##############################################################################################################################            

            elif( record[i]['TRCCO'] == '2000003' and record[i]['BRSFLG'] == '0' ):
                #=====���ճи����� ����====
                AfaLoggerFunc.tradeInfo('���ճи����� ����')
                #=====�������ܽ��====
                AfaLoggerFunc.tradeInfo('���ճи����� ����__��������')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat='" + PL_BCSTAT_MFESTL + "'"
                trcbka_sql = "select sum(OCCAMT) from rcc_trcbka where TRCCO='2000003' and BRSFLG='0' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                trcbka_sql = trcbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeInfo('trcbka_sqlΪ��' + trcbka_sql)
                trcbka_list = AfaDBFunc.SelectSql(trcbka_sql)
                if( trcbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','��Ʊ��Ϣ�Ǽǲ�����ʧ��')
                elif( len(trcbka_list) <= 0 ):
                    TradeContext.INRCTAMT = 0.00
                else:
                    if( trcbka_list[0][0] == None ):
                        TradeContext.INRCTAMT = 0.00
                    else:
                        TradeContext.INRCTAMT = trcbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCTAMTΪ��'+  str(TradeContext.INRCTAMT))
                
                #=====�跽���ܽ��====
                AfaLoggerFunc.tradeInfo('���ճи����� ����__�跽����')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat='" + PL_BCSTAT_MFESTL + "'"
                trcbka_sql = "select sum(OCCAMT) from rcc_trcbka where TRCCO='2000003' and BRSFLG='0' and  DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                trcbka_sql = trcbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeInfo('trcbka_sqlΪ��' + trcbka_sql)
                trcbka_list = AfaDBFunc.SelectSql(trcbka_sql)
                if( trcbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','��Ʊ��Ϣ�Ǽǲ�����ʧ��')
                elif( len(trcbka_list) <= 0 ):
                    TradeContext.INRDTAMT = 0.00
                else:
                    if( trcbka_list[0][0] == None ):
                        TradeContext.INRDTAMT = 0.00
                    else:
                        TradeContext.INRDTAMT = trcbka_list[0][0]
                        
                #=====������ܽ��====
                AfaLoggerFunc.tradeInfo('���ճи����� ����__�������') 
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT - TradeContext.INRDTAMT
                AfaLoggerFunc.tradeInfo('INROFSTAMTΪ��'+ str(TradeContext.INROFSTAMT))   
            
##############################################################################################################################            

            elif( record[i]['TRCCO'] == '2000003' and record[i]['BRSFLG'] == '1' ):
                #=====���ճи����� ����====
                AfaLoggerFunc.tradeInfo('���ճи����� ����')
                #=====�������ܽ��====
                AfaLoggerFunc.tradeInfo('���ճи����� ����__��������')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in('70','71','80')"
                trcbka_sql = "select sum(OCCAMT) from rcc_trcbka where TRCCO='2000003' and BRSFLG='1' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                trcbka_sql = trcbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeInfo('trcbka_sqlΪ��' + trcbka_sql)
                trcbka_list = AfaDBFunc.SelectSql(trcbka_sql)
                if( trcbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','��Ʊ��Ϣ�Ǽǲ�����ʧ��')
                elif( len(trcbka_list) <= 0 ):
                    TradeContext.INRCTAMT = 0.00
                else:
                    if( trcbka_list[0][0] == None ):
                        TradeContext.INRCTAMT = 0.00
                    else:
                        TradeContext.INRCTAMT = trcbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCTAMTΪ��'+  str(TradeContext.INRCTAMT))
                
                #=====�跽���ܽ��====
                AfaLoggerFunc.tradeInfo('���ճи����� ����__�跽����')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in('70','71','80')"
                trcbka_sql = "select sum(OCCAMT) from rcc_trcbka where TRCCO='2000003' and BRSFLG='1' and  DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                trcbka_sql = trcbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeInfo('trcbka_sqlΪ��' + trcbka_sql)
                trcbka_list = AfaDBFunc.SelectSql(trcbka_sql)
                if( trcbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','��Ʊ��Ϣ�Ǽǲ�����ʧ��')
                elif( len(trcbka_list) <= 0 ):
                    TradeContext.INRDTAMT = 0.00
                else:
                    if( trcbka_list[0][0] == None ):
                        TradeContext.INRDTAMT = 0.00
                    else:
                        TradeContext.INRDTAMT = trcbka_list[0][0]
                        
                #=====������ܽ��====
                AfaLoggerFunc.tradeInfo('���ճи����� ����__�������')
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT - TradeContext.INRDTAMT
                AfaLoggerFunc.tradeInfo('INROFSTAMTΪ��'+ str(TradeContext.INROFSTAMT))   
            
##############################################################################################################################            
            
            elif( record[i]['TRCCO'] == '2000004' and record[i]['BRSFLG'] == '0' ):
                #=====�����˻�ҵ�� ����====
                AfaLoggerFunc.tradeInfo('�����˻�ҵ�� ����')
                #=====�������ܽ��====
                AfaLoggerFunc.tradeInfo('�����˻�ҵ�� ����__��������')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat='" + PL_BCSTAT_MFESTL + "'"
                trcbka_sql = "select sum(OCCAMT) from rcc_trcbka where TRCCO='2000004' and BRSFLG='0' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                trcbka_sql = trcbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeInfo('trcbka_sqlΪ��' + trcbka_sql)
                trcbka_list = AfaDBFunc.SelectSql(trcbka_sql)
                if( trcbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','��Ʊ��Ϣ�Ǽǲ�����ʧ��')
                elif( len(trcbka_list) <= 0 ):
                    TradeContext.INRCTAMT = 0.00
                else:
                    if( trcbka_list[0][0] == None ):
                        TradeContext.INRCTAMT = 0.00
                    else:
                        TradeContext.INRCTAMT = trcbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCTAMTΪ��'+  str(TradeContext.INRCTAMT))
                
                #=====�跽���ܽ��====
                AfaLoggerFunc.tradeInfo('�����˻�ҵ�� ����__�跽����')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat='" + PL_BCSTAT_MFESTL + "'"
                trcbka_sql = "select sum(OCCAMT) from rcc_trcbka where TRCCO='2000004' and BRSFLG='0' and  DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                trcbka_sql = trcbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeInfo('trcbka_sqlΪ��' + trcbka_sql)
                trcbka_list = AfaDBFunc.SelectSql(trcbka_sql)
                if( trcbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','��Ʊ��Ϣ�Ǽǲ�����ʧ��')
                elif( len(trcbka_list) <= 0 ):
                    TradeContext.INRDTAMT = 0.00
                else:
                    if( trcbka_list[0][0] == None ):
                        TradeContext.INRDTAMT = 0.00
                    else:
                        TradeContext.INRDTAMT = trcbka_list[0][0]
                        
                #=====������ܽ��====
                AfaLoggerFunc.tradeInfo('�����˻�ҵ�� ����__�������') 
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT - TradeContext.INRDTAMT
                AfaLoggerFunc.tradeInfo('INROFSTAMTΪ��'+ str(TradeContext.INROFSTAMT)) 
            
###############################################################################################################################            
            
            elif( record[i]['TRCCO'] == '2000004' and record[i]['BRSFLG'] == '1' ):
                #=====�����˻�ҵ�� ����====
                AfaLoggerFunc.tradeInfo('�����˻�ҵ�� ����')
                #=====�������ܽ��====
                AfaLoggerFunc.tradeInfo('�����˻�ҵ�� ����__��������')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in('70','71','80')"
                trcbka_sql = "select sum(OCCAMT) from rcc_trcbka where TRCCO='2000004' and BRSFLG='1' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                trcbka_sql = trcbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeInfo('trcbka_sqlΪ��' + trcbka_sql)
                trcbka_list = AfaDBFunc.SelectSql(trcbka_sql)
                if( trcbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','��Ʊ��Ϣ�Ǽǲ�����ʧ��')
                elif( len(trcbka_list) <= 0 ):
                    TradeContext.INRCTAMT = 0.00
                else:
                    if( trcbka_list[0][0] == None ):
                        TradeContext.INRCTAMT = 0.00
                    else:
                        TradeContext.INRCTAMT = trcbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCTAMTΪ��'+  str(TradeContext.INRCTAMT))
                
                #=====�跽���ܽ��====
                AfaLoggerFunc.tradeInfo('�����˻�ҵ�� ����__�跽����')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in('70','71','80')"
                trcbka_sql = "select sum(OCCAMT) from rcc_trcbka where TRCCO='2000004' and BRSFLG='1' and  DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                trcbka_sql = trcbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeInfo('trcbka_sqlΪ��' + trcbka_sql)
                trcbka_list = AfaDBFunc.SelectSql(trcbka_sql)
                if( trcbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','��Ʊ��Ϣ�Ǽǲ�����ʧ��')
                elif( len(trcbka_list) <= 0 ):
                    TradeContext.INRDTAMT = 0.00
                else:
                    if( trcbka_list[0][0] == None ):
                        TradeContext.INRDTAMT = 0.00
                    else:
                        TradeContext.INRDTAMT = trcbka_list[0][0]
                        
                #=====������ܽ��====
                AfaLoggerFunc.tradeInfo('�����˻�ҵ�� ����__�������') 
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT - TradeContext.INRDTAMT
                AfaLoggerFunc.tradeInfo('INROFSTAMTΪ��'+ str(TradeContext.INROFSTAMT)) 
            
###############################################################################################################################            

            elif( record[i]['TRCCO'] == '2000009' and record[i]['BRSFLG'] == '0' ):
                #=====�¾�ϵͳ�Խ� ����====
                AfaLoggerFunc.tradeInfo('�¾�ϵͳ�Խ� ����')
                #=====�������ܽ��====
                AfaLoggerFunc.tradeInfo('�¾�ϵͳ�Խ� ����__��������')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat='" + PL_BCSTAT_MFESTL + "'"
                trcbka_sql = "select sum(OCCAMT) from rcc_trcbka where TRCCO='2000009' and BRSFLG='0' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                trcbka_sql = trcbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeInfo('trcbka_sqlΪ��' + trcbka_sql)
                trcbka_list = AfaDBFunc.SelectSql(trcbka_sql)
                if( trcbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','��Ʊ��Ϣ�Ǽǲ�����ʧ��')
                elif( len(trcbka_list) <= 0 ):
                    TradeContext.INRCTAMT = 0.00
                else:
                    if( trcbka_list[0][0] == None ):
                        TradeContext.INRCTAMT = 0.00
                    else:
                        TradeContext.INRCTAMT = trcbka_list[0][0]
                        
                #=====�跽���ܽ��====
                AfaLoggerFunc.tradeInfo('�¾�ϵͳ�Խ� ����__�跽����')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat='" + PL_BCSTAT_MFESTL + "'"
                trcbka_sql = "select sum(OCCAMT) from rcc_trcbka where TRCCO='2000009' and BRSFLG='0' and  DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                trcbka_sql = trcbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeInfo('trcbka_sqlΪ��' + trcbka_sql)
                trcbka_list = AfaDBFunc.SelectSql(trcbka_sql)
                if( trcbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','��Ʊ��Ϣ�Ǽǲ�����ʧ��')
                elif( len(trcbka_list) <= 0 ):
                    TradeContext.INRDTAMT = 0.00
                else:
                    if( trcbka_list[0][0] == None ):
                        TradeContext.INRDTAMT = 0.00
                    else:
                        TradeContext.INRDTAMT = trcbka_list[0][0]
                        
                #=====������ܽ��====
                AfaLoggerFunc.tradeInfo('�¾�ϵͳ�Խ� ����__�������')
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT - TradeContext.INRDTAMT
                AfaLoggerFunc.tradeInfo('INROFSTAMTΪ��'+ str(TradeContext.INROFSTAMT)) 
            
###############################################################################################################################            
            
            elif( record[i]['TRCCO'] == '2000009' and record[i]['BRSFLG'] == '1' ):
                #=====�¾�ϵͳ�Խ� ����====
                AfaLoggerFunc.tradeInfo('�¾�ϵͳ�Խ� ����')
                #=====�������ܽ��====
                AfaLoggerFunc.tradeInfo('�¾�ϵͳ�Խ� ����__��������')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in('70','71','80')"
                trcbka_sql = "select sum(OCCAMT) from rcc_trcbka where TRCCO='2000009' and BRSFLG='1' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                trcbka_sql = trcbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeInfo('trcbka_sqlΪ��' + trcbka_sql)
                trcbka_list = AfaDBFunc.SelectSql(trcbka_sql)
                if( trcbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','��Ʊ��Ϣ�Ǽǲ�����ʧ��')
                elif( len(trcbka_list) <= 0 ):
                    TradeContext.INRCTAMT = 0.00
                else:
                    if( trcbka_list[0][0] == None ):
                        TradeContext.INRCTAMT = 0.00
                    else:
                        TradeContext.INRCTAMT = trcbka_list[0][0]
                        
                #=====�跽���ܽ��====
                AfaLoggerFunc.tradeInfo('�¾�ϵͳ�Խ� ����__�跽����')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in('70','71','80')"
                trcbka_sql = "select sum(OCCAMT) from rcc_trcbka where TRCCO='2000009' and BRSFLG='1' and  DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                trcbka_sql = trcbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeInfo('trcbka_sqlΪ��' + trcbka_sql)
                trcbka_list = AfaDBFunc.SelectSql(trcbka_sql)
                if( trcbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','��Ʊ��Ϣ�Ǽǲ�����ʧ��')
                elif( len(trcbka_list) <= 0 ):
                    TradeContext.INRDTAMT = 0.00
                else:
                    if( trcbka_list[0][0] == None ):
                        TradeContext.INRDTAMT = 0.00
                    else:
                        TradeContext.INRDTAMT = trcbka_list[0][0]
                        
                #=====������ܽ��====
                AfaLoggerFunc.tradeInfo('�¾�ϵͳ�Խ� ����__�������') 
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT - TradeContext.INRDTAMT
                AfaLoggerFunc.tradeInfo('INROFSTAMTΪ��'+ str(TradeContext.INROFSTAMT)) 
            
###############################################################################################################################            

            
            #====��Ҫ�ӻ��ҵ��Ǽǲ�ͳ�����ڻ��ҵ������ܱ���====
            trcbka_sql = "select count(*) from rcc_trcbka where "
            trcbka_sql = trcbka_sql + "NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
 
            #=====�ж�BRSFLG====
            if str(record[i]['BRSFLG']) != '9':
                trcbka_sql = trcbka_sql + " and BRSFLG='" + record[i]['BRSFLG'] + "'"
            
            #=====�ж�TRCCO====
            if str(record[i]['TRCCO']) != '0000000':
                trcbka_sql = trcbka_sql + " and TRCCO ='" + record[i]['TRCCO'] + "'"

            #=====���������˸�ֵ��ͬ�Ľ���״̬====
            if record[i]['BRSFLG'] == PL_BRSFLG_SND:
                #=====�����ѯ��Ҫ���⴦��===
                trcbka_sql = trcbka_sql + " and bspsqn in (select bspsqn from rcc_spbsta where bcstat ='" + PL_BCSTAT_MFESTL + "'"
                trcbka_sql = trcbka_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "')"
            elif record[i]['BRSFLG'] == PL_BRSFLG_RCV:
                trcbka_sql = trcbka_sql + " and bspsqn in (select bspsqn from rcc_spbsta where bcstat in ('70','71','80')"
                trcbka_sql = trcbka_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "')"
            else:
                trcbka_sql = trcbka_sql + " and bspsqn in (select bspsqn from rcc_spbsta where bcstat in ('70','71','42','80')"
                trcbka_sql = trcbka_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "')"
            AfaLoggerFunc.tradeDebug( 'sql==' + trcbka_sql ) 
            
            #=====��ѯ���ݿ�====
            count = AfaDBFunc.SelectSql(trcbka_sql)
            if(count==None):
                f.close()
                return AfaFlowControl.ExitThisFlow('D000','���ݿ����ʧ��')
            if len(count) == 0:
                f.close()
                return AfaFlowControl.ExitThisFlow('D000','�����������ļ�¼')
            else:
                TradeContext.INRTCNT = str(count[0][0])

            #=====��ʼ��֯�ļ�����====
            filecont = ''
            filecont = filecont + record[i]['NCCWKDAT']     + "|" + record[i]['TRCCO']            + "|"
            filecont = filecont + record[i]['BRSFLG']       + "|" + record[i]['TRCNAM']           + "|"
            filecont = filecont + record[i]['TRCRSNM']      + "|" + str(record[i]['TCNT'])        + "|"
            filecont = filecont + TradeContext.INRTCNT      + "|"                                 
            filecont = filecont + str(record[i]['CTAMT'])   + "|" + str(TradeContext.INRCTAMT)    + "|"
            filecont = filecont + str(record[i]['DTAMT'])   + "|" + str(TradeContext.INRDTAMT)    + "|"
            filecont = filecont + str(record[i]['OFSTAMT']) + "|" + str(TradeContext.INROFSTAMT)  + "|\n"
            f.write(filecont)

        #=====�ر��ļ�====
        f.close()

    #=====��ѯ�ܼ�¼��====
    allcount=rccpsDBTrcc_hddzhz.count(sql)     #�õ��ܼ�¼����
    if(allcount==None):
        return AfaFlowControl.ExitThisFlow('D000','���ݿ����ʧ��')
    else:
        TradeContext.RECALLCOUNT = str(allcount)

    TradeContext.PBDAFILE = filename            #�ļ���
    TradeContext.RECCOUNT = str(len(record))    #��ѯ����
    TradeContext.errorMsg="��ѯ�ɹ�"
    TradeContext.errorCode="0000"
    
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(1.���ز���)����[TRC001_8546]�˳�***' )
    return True
