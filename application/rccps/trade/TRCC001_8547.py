# -*- coding: gbk -*-
##################################################################
#   ũ����.��ѯҵ��.��Ʊ���ܺ˶Բ�ѯ
#=================================================================
#   �����ļ�:   TRCC001_8547.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  ������
#   �޸�ʱ��:   2008-06-12
##################################################################
#   �޸���  ��  �˹�ͨ
#   �޸�ʱ�䣺  2008-09-18
#   �޸����ݣ�  ���ڽ���ͳ��
##################################################################
import TradeContext,AfaLoggerFunc,AfaFlowControl,AfaUtilTools,rccpsDBTrcc_hpdzhz
import rccpsDBTrcc_bilbka,AfaDBFunc
from types import *
from rccpsConst import *

def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '>>>��ʼ��Ʊ���ܺ˶Բ�ѯ' )
    #=====�жϽӿ��Ƿ����====
    if not TradeContext.existVariable("NCCWKDAT"):
        TradeContext.errorCode = 'N999'
        TradeContext.errorMsg = '��������Ϊ��'
        return False

    #=====���кŲ�ѯ====
    sql = "NCCWKDAT = '" + TradeContext.NCCWKDAT + "'"
    #=====��ѯ���ݿ⣬�õ���ѯ�����====
    record=rccpsDBTrcc_hpdzhz.selectm(TradeContext.RECSTRNO,10,sql,"")  
    if record == None:
        return AfaFlowControl.ExitThisFlow('D000','���ݿ����ʧ��')
    elif len(record) <= 0:
        return AfaFlowControl.ExitThisFlow('D000','û�����������ļ�¼')
    else:
        filename = 'rccps_' + TradeContext.BETELR + '_' + AfaUtilTools.GetSysDate() + '_' + TradeContext.TransCode 
        try:
            f=open("/home/maps/afa/tmp/"+filename,"w")
        except IOError:
            AfaLoggerFunc.tradeDebug('���ļ�ʧ��')
            return AfaFlowControl.ExitThisFlow('A999','���ļ�ʧ��')

        AfaLoggerFunc.tradeDebug( '�ļ�����' + filename )
        #=====��֯�����ļ�====
        AfaLoggerFunc.tradeDebug( 'start=' + str(record) )
        
        for i in range( 0, len(record) ):
                        
            #=====ͨ�����״����������ʾ���ж�ҵ������====
            #=====�ϼ� ���˻���====
            if( record[i]['TRCCO'] == '0000000' and record[i]['BRSFLG'] == '0' ):
                AfaLoggerFunc.tradeInfo('��ʼ�ϼ� ���˻���')
                #=====�������ܽ��====   
                AfaLoggerFunc.tradeInfo('�ϼ� ���˻���__�������ܽ��')
                bilbka_sql1 = "select BILVER from rcc_bilbka where BRSFLG='0' and DCFLG='2' and TRCCO='2100100' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql1 = bilbka_sql1 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT='" + PL_BCSTAT_MFESTL + "' and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql2 = "select BILNO from rcc_bilbka where BRSFLG='0' and DCFLG='2' and TRCCO='2100100' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql2 = bilbka_sql2 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT='" + PL_BCSTAT_MFESTL + "' and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql3 = "select BILRS from rcc_bilbka where BRSFLG='0' and DCFLG='2' and TRCCO='2100100' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql3 = bilbka_sql3 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT='" + PL_BCSTAT_MFESTL + "' and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilinf_sql = "select sum(OCCAMT) from rcc_bilinf where BILVER in(" + bilbka_sql1 + ")"
                bilinf_sql = bilinf_sql + " and BILNO in(" + bilbka_sql2 + ")"
                bilinf_sql = bilinf_sql + " and BILRS in(" + bilbka_sql3 + ")"
                bilinf_sql = bilinf_sql + " with ur "
                AfaLoggerFunc.tradeDebug('bilinf_sqlΪ��'+ bilinf_sql)
                bilinf_list = AfaDBFunc.SelectSql(bilinf_sql)
                if( bilinf_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','��Ʊ��Ϣ�Ǽǲ�����ʧ��')
                elif( len(bilinf_list) <= 0 ):
                    TradeContext.INRCTAMT = 0.00
                else:
                    if( bilinf_list[0][0] == None ):
                        TradeContext.INRCTAMT =0.00
                    else:
                        TradeContext.INRCTAMT = bilinf_list[0][0]
#                TradeContext.INRCTAMT = 0.00
                
                #=====�跽���ܽ��====    
                AfaLoggerFunc.tradeInfo('�ϼ� ���˻���__�跽���ܽ��')
                bilbka_sql1 = "select BILVER from rcc_bilbka where BRSFLG='0' and DCFLG='1' and TRCCO='2100100' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql1 = bilbka_sql1 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT='" + PL_BCSTAT_MFESTL + "' and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql2 = "select BILNO from rcc_bilbka where BRSFLG='0' and DCFLG='1' and TRCCO='2100100' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql2 = bilbka_sql2 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT='" + PL_BCSTAT_MFESTL + "' and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql3 = "select BILRS from rcc_bilbka where BRSFLG='0' and DCFLG='1' and TRCCO='2100100' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql3 = bilbka_sql3 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT='" + PL_BCSTAT_MFESTL + "' and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilinf_sql = "select sum(OCCAMT) from rcc_bilinf where BILVER in(" + bilbka_sql1 + ")"
                bilinf_sql = bilinf_sql + " and BILNO in(" + bilbka_sql2 + ")"
                bilinf_sql = bilinf_sql + " and BILRS in(" + bilbka_sql3 + ")"
                bilinf_sql = bilinf_sql + " with ur "
                AfaLoggerFunc.tradeDebug('bilinf_sqlΪ��'+ bilinf_sql)
                bilinf_list = AfaDBFunc.SelectSql(bilinf_sql)
                if( bilinf_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','��Ʊ��Ϣ�Ǽǲ�����ʧ��')
                elif( len(bilinf_list) <= 0 ):
                    TradeContext.INRDTAMT = 0.00
                else:
                    if( bilinf_list[0][0] == None ):
                        TradeContext.INRDTAMT = 0.00
                    else:
                        TradeContext.INRDTAMT = bilinf_list[0][0]
                        
                
                        
                #=====������ܽ��====
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT - TradeContext.INRDTAMT
                
                #=====����Ȧ����====
                AfaLoggerFunc.tradeInfo('�ϼ� ���˻���__����Ȧ����')
                bilbka_sql1 = "select BILVER from rcc_bilbka where BRSFLG='0' and DCFLG='1' and TRCCO in('2100001','2100103','2100101') and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilkba_sql1 = bilbka_sql1 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT='" + PL_BCSTAT_MFESTL + "' and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql2 = "select BILNO from rcc_bilbka where BRSFLG='0' and DCFLG='1' and TRCCO in('2100001','2100103','2100101')  and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql2 = bilbka_sql2 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT='" + PL_BCSTAT_MFESTL + "' and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql3 = "select BILRS from rcc_bilbka where BRSFLG='0' and DCFLG='1' and TRCCO in('2100001','2100103','2100101')  and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql3 = bilbka_sql3 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT='" + PL_BCSTAT_MFESTL + "' and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilinf_sql = "select sum(BILAMT) from rcc_bilinf where BILVER in(" + bilbka_sql1 + ")"
                bilinf_sql = bilinf_sql + " and BILNO in(" + bilbka_sql2 + ")"
                bilinf_sql = bilinf_sql + " and BILRS in(" + bilbka_sql3 + ")"
                bilinf_sql = bilinf_sql + " with ur "
                AfaLoggerFunc.tradeDebug('bilinf_sqlΪ��'+ bilinf_sql)
                bilinf_list = AfaDBFunc.SelectSql(bilinf_sql)
                AfaLoggerFunc.tradeDebug('bilinf_list[0][0]:'+str(bilinf_list[0][0]))
                if( bilinf_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','��Ʊ��Ϣ�Ǽǲ�����ʧ��')
                elif( len(bilinf_list) <= 0 ):
                    TradeContext.INRCLAMT = 0.00
                else:
                    if( bilinf_list[0][0] == None ):
                        TradeContext.INRCLAMT = 0.00
                    else:
                        TradeContext.INRCLAMT = bilinf_list[0][0]
                #=====�跽Ȧ����====
                AfaLoggerFunc.tradeInfo('�ϼ� ���˻���__�跽Ȧ����')
                bilbka_sql1 = "select BILVER from rcc_bilbka where BRSFLG='0' and DCFLG='2' and TRCCO in('2100001','2100103','2100101') and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilkba_sql1 = bilbka_sql1 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT='" + PL_BCSTAT_MFESTL + "' and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql2 = "select BILNO from rcc_bilbka where BRSFLG='0' and DCFLG='2' and TRCCO in('2100001','2100103','2100101') and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql2 = bilbka_sql2 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT='" + PL_BCSTAT_MFESTL + "' and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql3 = "select BILRS from rcc_bilbka where BRSFLG='0' and DCFLG='2' and TRCCO in('2100001','2100103','2100101') and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql3 = bilbka_sql3 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT='" + PL_BCSTAT_MFESTL + "' and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilinf_sql = "select sum(BILAMT) from rcc_bilinf where BILVER in(" + bilbka_sql1 + ")"
                bilinf_sql = bilinf_sql + " and BILNO in(" + bilbka_sql2 + ")"
                bilinf_sql = bilinf_sql + " and BILRS in(" + bilbka_sql3 + ")"
                bilinf_sql = bilinf_sql + " with ur "
                AfaLoggerFunc.tradeDebug('bilinf_sqlΪ��'+ bilinf_sql)
                bilinf_list = AfaDBFunc.SelectSql(bilinf_sql)
                AfaLoggerFunc.tradeDebug('bilinf_list[0][0]:'+str(bilinf_list[0][0]))
                if( bilinf_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','��Ʊ��Ϣ�Ǽǲ�����ʧ��')
                elif( len(bilinf_list) <= 0 ):
                    TradeContext.INRDLAMT = 0.00
                else:
                    if( bilinf_list[0][0] == None ):
                        TradeContext.INRDLAMT = 0.00
                    else:
                        TradeContext.INRDLAMT = bilinf_list[0][0]
                
                #=====����Ȧ����====
                TradeContext.INROFSLAMT = TradeContext.INRCLAMT - TradeContext.INRDLAMT
                
#======================================================================================================                
            #=====�ϼ� ���Ż���====    
            elif( record[i]['TRCCO'] == '0000000' and record[i]['BRSFLG'] == '1' ):
                AfaLoggerFunc.tradeInfo('��ʼ�ϼ� ���˻���')
                
                #=====�������ܽ��====
                AfaLoggerFunc.tradeInfo('��ʼ�ϼ� ���˻���__�������ܽ��')
                bilbka_sql1 = "select BILVER from rcc_bilbka where BRSFLG='1' and DCFLG='2' and TRCCO in('2100100') and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql1 = bilbka_sql1 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT in('70','71') and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql2 = "select BILNO from rcc_bilbka where BRSFLG='1' and DCFLG='2' and TRCCO in('2100100') and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql2 = bilbka_sql2 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT in('70','71') and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql3 = "select BILRS from rcc_bilbka where BRSFLG='1' and DCFLG='2' and TRCCO in('2100100') and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql3 = bilbka_sql3 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT in('70','71') and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilinf_sql = "select sum(OCCAMT) from rcc_bilinf where BILVER in(" + bilbka_sql1 + ")"
                bilinf_sql = bilinf_sql + " and BILNO in(" + bilbka_sql2 + ")"
                bilinf_sql = bilinf_sql + " and BILRS in(" + bilbka_sql3 + ")"
                bilinf_sql = bilinf_sql + " with ur "
                AfaLoggerFunc.tradeDebug('bilinf_sqlΪ��'+ bilinf_sql)
                bilinf_list = AfaDBFunc.SelectSql(bilinf_sql)
                if( bilinf_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','��Ʊ��Ϣ�Ǽǲ�����ʧ��')
                elif( len(bilinf_list) == 0 ):
                    TradeContext.INRCTAMT = 0.00
                else:
                    if( bilinf_list[0][0] == None ):
                        TradeContext.INRCTAMT = 0.00
                    else:
                        TradeContext.INRCTAMT = bilinf_list[0][0]
                
                #=====�跽���ܽ��====
                AfaLoggerFunc.tradeInfo('��ʼ�ϼ� ���˻���__�跽���ܽ��')
                bilbka_sql1 = "select BILVER from rcc_bilbka where BRSFLG='1' and DCFLG='1' and TRCCO in('2100100','2100101','2100103') and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql1 = bilbka_sql1 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT in('70','71') and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql2 = "select BILNO from rcc_bilbka where BRSFLG='1' and DCFLG='1' and TRCCO in('2100100','2100101','2100103') and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql2 = bilbka_sql2 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT in('70','71') and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql3 = "select BILRS from rcc_bilbka where BRSFLG='1' and DCFLG='1' and TRCCO in('2100100','2100101','2100103') and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql3 = bilbka_sql3 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT in('70','71') and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilinf_sql = "select sum(OCCAMT) from rcc_bilinf where BILVER in(" + bilbka_sql1 + ")"
                bilinf_sql = bilinf_sql + " and BILNO in(" + bilbka_sql2 + ")"
                bilinf_sql = bilinf_sql + " and BILRS in(" + bilbka_sql3 + ")"
                bilinf_sql = bilinf_sql + " with ur "
                AfaLoggerFunc.tradeDebug('bilinf_sqlΪ��'+ bilinf_sql)
                bilinf_list = AfaDBFunc.SelectSql(bilinf_sql)
                if( bilinf_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','��Ʊ��Ϣ�Ǽǲ�����ʧ��')
                elif( len(bilinf_list) == 0 ):
                    TradeContext.INRDTAMT = 0.00
                else:
                    if( bilinf_list[0][0] == None ):
                        TradeContext.INRDTAMT = 0.00
                    else:
                        TradeContext.INRDTAMT = bilinf_list[0][0]
                
                #=====������ܽ��====
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT - TradeContext.INRDTAMT
                
                #=====����Ȧ����====
                AfaLoggerFunc.tradeInfo('��ʼ�ϼ� ���˻���__����Ȧ����')
                bilbka_sql1 = "select BILVER from rcc_bilbka where BRSFLG='1' and DCFLG='1' and TRCCO='2100100' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql1 = bilbka_sql1 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT in('70','71') and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql2 = "select BILNO from rcc_bilbka where BRSFLG='1' and DCFLG='1' and TRCCO='2100100' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql2 = bilbka_sql2 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT in('70','71') and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql3 = "select BILRS from rcc_bilbka where BRSFLG='1' and DCFLG='1' and TRCCO='2100100' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql3 = bilbka_sql3 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT in('70','71') and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilinf_sql = "select sum(BILAMT) from rcc_bilinf where BILVER in(" + bilbka_sql1 + ")"
                bilinf_sql = bilinf_sql + " and BILNO in(" + bilbka_sql2 + ")"
                bilinf_sql = bilinf_sql + " and BILRS in(" + bilbka_sql3 + ")"
                bilinf_sql = bilinf_sql + " with ur "
                AfaLoggerFunc.tradeDebug('bilinf_sqlΪ��'+ bilinf_sql)
                bilinf_list = AfaDBFunc.SelectSql(bilinf_sql)
                if( bilinf_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','��Ʊ��Ϣ�Ǽǲ�����ʧ��')
                elif( len(bilinf_list) == 0 ):
                    TradeContext.INRCLAMT = 0.00
                else:
                    if( bilinf_list[0][0] == None ):
                        TradeContext.INRCLAMT = 0.00
                    else:
                        TradeContext.INRCLAMT = bilinf_list[0][0]

#                TradeContext.INRCLAMT = 0.00
                        
                #=====�跽Ȧ����====
                AfaLoggerFunc.tradeInfo('��ʼ�ϼ� ���˻���__�跽Ȧ����')
                bilbka_sql1 = "select BILVER from rcc_bilbka where BRSFLG='1' and DCFLG='2' and TRCCO='2100100' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql1 = bilbka_sql1 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT in('70','71') and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql2 = "select BILNO from rcc_bilbka where BRSFLG='1' and DCFLG='2' and TRCCO='2100100' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql2 = bilbka_sql2 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT in('70','71') and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql3 = "select BILRS from rcc_bilbka where BRSFLG='1' and DCFLG='2' and TRCCO='2100100' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql3 = bilbka_sql3 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT in('70','71') and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilinf_sql = "select sum(BILAMT) from rcc_bilinf where BILVER in(" + bilbka_sql1 + ")"
                bilinf_sql = bilinf_sql + " and BILNO in(" + bilbka_sql2 + ")"
                bilinf_sql = bilinf_sql + " and BILRS in(" + bilbka_sql3 + ")"
                bilinf_sql = bilinf_sql + " with ur "
                AfaLoggerFunc.tradeDebug('bilinf_sqlΪ��'+ bilinf_sql)
                bilinf_list = AfaDBFunc.SelectSql(bilinf_sql)
                if( bilinf_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','��Ʊ��Ϣ�Ǽǲ�����ʧ��')
                elif( len(bilinf_list) == 0 ):
                    TradeContext.INRDLAMT = 0.00
                else:
                    if( bilinf_list[0][0] == None ):
                        TradeContext.INRDLAMT = 0.00
                    else:
                        TradeContext.INRDLAMT = bilinf_list[0][0]
                
                #=====����Ȧ����====
                TradeContext.INROFSLAMT = TradeContext.INRCLAMT - TradeContext.INRDLAMT
            
#=============================================================================================================================            
            #=====�ϼ� �������====
            elif( record[i]['TRCCO'] == '0000000' and record[i]['BRSFLG'] == '9' ):
                AfaLoggerFunc.tradeInfo('��ʼ�ϼ� �������')
                #=====�������ܽ��====
                AfaLoggerFunc.tradeInfo('��ʼ�ϼ� �������__�������ܽ��')
                bilbka_sql1 = "select BILVER from rcc_bilbka where DCFLG='2' and TRCCO='2100100' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql1 = bilbka_sql1 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT in('70','71','42') and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql2 = "select BILNO from rcc_bilbka where DCFLG='2' and TRCCO='2100100' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql2 = bilbka_sql2 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT in('70','71','42') and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql3 = "select BILRS from rcc_bilbka where DCFLG='2' and TRCCO='2100100' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql3 = bilbka_sql3 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT in('70','71','42') and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilinf_sql = "select sum(OCCAMT) from rcc_bilinf where BILVER in(" + bilbka_sql1 + ")"
                bilinf_sql = bilinf_sql + " and BILNO in(" + bilbka_sql2 + ")"
                bilinf_sql = bilinf_sql + " and BILRS in(" + bilbka_sql3 + ")"
                bilinf_sql = bilinf_sql + " with ur "
                AfaLoggerFunc.tradeDebug('bilinf_sqlΪ��'+ bilinf_sql)
                bilinf_list = AfaDBFunc.SelectSql(bilinf_sql)
                if( bilinf_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','��Ʊ��Ϣ�Ǽǲ�����ʧ��')
                elif( len(bilinf_list) <= 0 ):
                    TradeContext.INRCTAMT = 0.00
                else:
                    if( bilinf_list[0][0] == None ):
                        TradeContext.INRCTAMT = 0.00
                    else:
                        TradeContext.INRCTAMT = bilinf_list[0][0]
                
                AfaLoggerFunc.tradeDebug('INRCTAMTΪ��'+ str(TradeContext.INRCTAMT))
                
                #=====�跽���ܽ��====
                AfaLoggerFunc.tradeInfo('��ʼ�ϼ� �������__�跽���ܽ��')
                bilbka_sql1 = "select BILVER from rcc_bilbka where DCFLG='1' and TRCCO='2100100' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql1 = bilbka_sql1 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT in('70','71','42') and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql2 = "select BILNO from rcc_bilbka where DCFLG='1' and TRCCO='2100100' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql2 = bilbka_sql2 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT in('70','71','42') and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql3 = "select BILRS from rcc_bilbka where DCFLG='1' and TRCCO='2100100' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql3 = bilbka_sql3 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT in('70','71','42') and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilinf_sql = "select sum(OCCAMT) from rcc_bilinf where BILVER in(" + bilbka_sql1 + ")"
                bilinf_sql = bilinf_sql + " and BILNO in(" + bilbka_sql2 + ")"
                bilinf_sql = bilinf_sql + " and BILRS in(" + bilbka_sql3 + ")"
                bilinf_sql = bilinf_sql + " with ur "
                AfaLoggerFunc.tradeDebug('bilinf_sqlΪ��'+ bilinf_sql)
                bilinf_list = AfaDBFunc.SelectSql(bilinf_sql)
                if( bilinf_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','��Ʊ��Ϣ�Ǽǲ�����ʧ��')
                elif( len(bilinf_list) <= 0 ):
                    TradeContext.INRDTAMT = 0.00
                else:
                    if( bilinf_list[0][0] == None ):
                        TradeContext.INRDTAMT = 0.00
                    #=====������ 20081014====
                    else:
                        TradeContext.INRDTAMT = bilinf_list[0][0]
                        
                AfaLoggerFunc.tradeDebug('INRDTAMTΪ��'+ str(TradeContext.INRDTAMT))
                        
                #=====������ܽ��====
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT - TradeContext.INRDTAMT
                
                #=====����Ȧ����====
                AfaLoggerFunc.tradeInfo('��ʼ�ϼ� �������__����Ȧ����')
                bilbka_sql1 = "select BILVER||BILNO||BILRS from rcc_bilbka where DCFLG='1' and TRCCO in('2100100','2100101','2100103') and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql1 = bilbka_sql1 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT in('70','71','42') and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql2 = "select BILNO from rcc_bilbka where DCFLG='1' and TRCCO in('2100100','2100101','2100103') and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql2 = bilbka_sql2 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT in('70','71','42') and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql3 = "select BILRS from rcc_bilbka where DCFLG='1' and TRCCO in('2100100','2100101','2100103') and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql3 = bilbka_sql3 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT in('70','71','42') and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilinf_sql = "select sum(BILAMT) from rcc_bilinf where BILVER||BILNO||BILRS in(" + bilbka_sql1 + ")"
                #bilinf_sql = bilinf_sql + " and BILNO in(" + bilbka_sql2 + ")"
                #bilinf_sql = bilinf_sql + " and BILRS in(" + bilbka_sql3 + ")"
                bilinf_sql = bilinf_sql + " with ur "
                AfaLoggerFunc.tradeDebug('bilinf_sqlΪ��'+ bilinf_sql)
                bilinf_list = AfaDBFunc.SelectSql(bilinf_sql)
                if( bilinf_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','��Ʊ��Ϣ�Ǽǲ�����ʧ��')
                elif( len(bilinf_list) == 0 ):
                    TradeContext.INRCLAMT = 0.00
                else:
                    if( bilinf_list[0][0] == None ):
                        TradeContext.INRCLAMT = 0.00
                    else:
                        TradeContext.INRCLAMT = bilinf_list[0][0]
                        
                AfaLoggerFunc.tradeDebug('INRCTAMTΪ��'+ str(TradeContext.INRCLAMT))
                        
                #=====�跽Ȧ����====
                AfaLoggerFunc.tradeInfo('��ʼ�ϼ� �������__�跽Ȧ����')
                bilbka_sql1 = "select BILVER from rcc_bilbka where DCFLG='2' and TRCCO='2100001' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql1 = bilbka_sql1 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT in('70','71','42') and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql2 = "select BILNO from rcc_bilbka where DCFLG='2' and TRCCO='2100001' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql2 = bilbka_sql2 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT in('70','71','42') and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql3 = "select BILRS from rcc_bilbka where DCFLG='2' and TRCCO='2100001' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql3 = bilbka_sql3 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT in('70','71','42') and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilinf_sql = "select sum(BILAMT) from rcc_bilinf where BILVER in(" + bilbka_sql1 + ")"
                bilinf_sql = bilinf_sql + " and BILNO in(" + bilbka_sql2 + ")"
                bilinf_sql = bilinf_sql + " and BILRS in(" + bilbka_sql3 + ")"
                bilinf_sql = bilinf_sql + " with ur "
                AfaLoggerFunc.tradeDebug('bilinf_sqlΪ��'+ bilinf_sql)
                bilinf_list = AfaDBFunc.SelectSql(bilinf_sql)
                if( bilinf_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','��Ʊ��Ϣ�Ǽǲ�����ʧ��')
                elif( len(bilinf_list) == 0 ):
                    TradeContext.INRDLAMT = 0.00
                else:
                    if( bilinf_list[0][0] ==None ):
                        TradeContext.INRDLAMT = 0.00
                    else:
                        TradeContext.INRDLAMT = bilinf_list[0][0]
                        
                AfaLoggerFunc.tradeDebug('INRCTAMTΪ��'+ str(TradeContext.INRDLAMT))
                
                #=====����Ȧ����====
                TradeContext.INROFSLAMT = TradeContext.INRCLAMT - TradeContext.INRDLAMT
            
#====================================================================================================            
            #=====��Ʊǩ�� ����====
            elif( record[i]['TRCCO'] == '2100001' and record[i]['BRSFLG'] == '0' ):
                AfaLoggerFunc.tradeInfo('��ʼ��Ʊǩ�� ����')
                #=====�������ܽ��====
                TradeContext.INRCTAMT = 0
                
                #=====�跽���ܽ��====
                TradeContext.INRDTAMT = 0
                        
                #=====������ܽ��====
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT - TradeContext.INRDTAMT
                
                #=====����Ȧ����====
                AfaLoggerFunc.tradeInfo('��ʼ��Ʊǩ�� ����__����Ȧ����')
                bilbka_sql1 = "select BILVER from rcc_bilbka where BRSFLG='0' and DCFLG='1' and TRCCO='2100001' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql1 = bilbka_sql1 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT='" + PL_BCSTAT_MFESTL + "' and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql2 = "select BILNO from rcc_bilbka where BRSFLG='0' and DCFLG='1' and TRCCO='2100001' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql2 = bilbka_sql2 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT='" + PL_BCSTAT_MFESTL + "' and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql3 = "select BILRS from rcc_bilbka where BRSFLG='0' and DCFLG='1' and TRCCO='2100001' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql3 = bilbka_sql3 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT='" + PL_BCSTAT_MFESTL + "' and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilinf_sql = "select sum(BILAMT) from rcc_bilinf where BILVER in(" + bilbka_sql1 + ")"
                bilinf_sql = bilinf_sql + " and BILNO in(" + bilbka_sql2 + ")"
                bilinf_sql = bilinf_sql + " and BILRS in(" + bilbka_sql3 + ")"
                bilinf_sql = bilinf_sql + " with ur "
                AfaLoggerFunc.tradeDebug('bilinf_sqlΪ��'+ bilinf_sql)
                bilinf_list = AfaDBFunc.SelectSql(bilinf_sql)
                if( bilinf_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','��Ʊ��Ϣ�Ǽǲ�����ʧ��')
                elif( len(bilinf_list) == 0 ):
                    TradeContext.INRCLAMT = 0.00
                else:
                    if( bilinf_list[0][0] == None ):
                        TradeContext.INRCLAMT = 0.00
                    else:
                        TradeContext.INRCLAMT = bilinf_list[0][0]
              
                #=====�跽Ȧ����====
                AfaLoggerFunc.tradeInfo('��ʼ��Ʊǩ�� ����__�跽Ȧ����')
                bilbka_sql1 = "select BILVER from rcc_bilbka where BRSFLG='0' and DCFLG='2' and TRCCO='2100001' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql1 = bilbka_sql1 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT='" + PL_BCSTAT_MFESTL + "' and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql2 = "select BILNO from rcc_bilbka where BRSFLG='0' and DCFLG='2' and TRCCO='2100001' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql2 = bilbka_sql2 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT='" + PL_BCSTAT_MFESTL + "' and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql3 = "select BILRS from rcc_bilbka where BRSFLG='0' and DCFLG='2' and TRCCO='2100001' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql3 = bilbka_sql3 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT='" + PL_BCSTAT_MFESTL + "' and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilinf_sql = "select sum(BILAMT) from rcc_bilinf where BILVER in(" + bilbka_sql1 + ")"
                bilinf_sql = bilinf_sql + " and BILNO in(" + bilbka_sql2 + ")"
                bilinf_sql = bilinf_sql + " and BILRS in(" + bilbka_sql3 + ")"
                bilinf_sql = bilinf_sql + " with ur "
                AfaLoggerFunc.tradeDebug('bilinf_sqlΪ��'+ bilinf_sql)
                bilinf_list = AfaDBFunc.SelectSql(bilinf_sql)
                if( bilinf_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','��Ʊ��Ϣ�Ǽǲ�����ʧ��')
                elif( len(bilinf_list) == 0 ):
                    TradeContext.INRDLAMT = 0.00
                else:
                    if( bilinf_list[0][0] == None ):
                        TradeContext.INRDLAMT = 0.00
                    else:
                        TradeContext.INRDLAMT = bilinf_list[0][0]
#                TradeContext.INRDLAMT = 0.00
                
                #=====����Ȧ����====
                TradeContext.INROFSLAMT = TradeContext.INRCLAMT - TradeContext.INRDLAMT
            
#===================================================================================================            
            #=====��Ʊ�⸶ ����====
            elif( record[i]['TRCCO'] == '2100100' and record[i]['BRSFLG'] == '0' ):
                AfaLoggerFunc.tradeInfo('��Ʊ�⸶ ���˻���')
                #=====�������ܽ��====
                AfaLoggerFunc.tradeInfo('��Ʊ�⸶ ���˻���__�������ܽ��')
                bilbka_sql1 = "select BILVER from rcc_bilbka where BRSFLG='0' and DCFLG='2' and TRCCO='2100100' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql1 = bilbka_sql1 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT='" + PL_BCSTAT_MFESTL + "' and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql2 = "select BILNO from rcc_bilbka where BRSFLG='0' and DCFLG='2' and TRCCO='2100100' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql2 = bilbka_sql2 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT='" + PL_BCSTAT_MFESTL + "' and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql3 = "select BILRS from rcc_bilbka where BRSFLG='0' and DCFLG='2' and TRCCO='2100100' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql3 = bilbka_sql3 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT='" + PL_BCSTAT_MFESTL + "' and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilinf_sql = "select sum(OCCAMT) from rcc_bilinf where BILVER in(" + bilbka_sql1 + ")"
                bilinf_sql = bilinf_sql + " and BILNO in(" + bilbka_sql2 + ")"
                bilinf_sql = bilinf_sql + " and BILRS in(" + bilbka_sql3 + ")"
                bilinf_sql = bilinf_sql + " with ur "
                AfaLoggerFunc.tradeDebug('bilinf_sqlΪ��'+ bilinf_sql)
                bilinf_list = AfaDBFunc.SelectSql(bilinf_sql)
                if( bilinf_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','��Ʊ��Ϣ�Ǽǲ�����ʧ��')
                elif( len(bilinf_list) <= 0 ):
                    TradeContext.INRCTAMT = 0.00
                else:
                    if( bilinf_list[0][0] == None ):
                        TradeContext.INRCTAMT = 0.00
                    else:
                        TradeContext.INRCTAMT = bilinf_list[0][0]

#                TradeContext.INRCTAMT = 0.00
                        
                AfaLoggerFunc.tradeDebug('INRCTAMTΪ��'+ str(TradeContext.INRCTAMT))
                
                #=====�跽���ܽ��====
                AfaLoggerFunc.tradeInfo('��Ʊ�⸶ ����__�跽���ܽ��')
                bilbka_sql1 = "select BILVER from rcc_bilbka where BRSFLG='0' and DCFLG='1' and TRCCO='2100100' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql1 = bilbka_sql1 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT='" + PL_BCSTAT_MFESTL + "' and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql2 = "select BILNO from rcc_bilbka where BRSFLG='0' and DCFLG='1' and TRCCO='2100100' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql2 = bilbka_sql2 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT='" + PL_BCSTAT_MFESTL + "' and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql3 = "select BILRS from rcc_bilbka where BRSFLG='0' and DCFLG='1' and TRCCO='2100100' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql3 = bilbka_sql3 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT='" + PL_BCSTAT_MFESTL + "' and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilinf_sql = "select sum(OCCAMT) from rcc_bilinf where BILVER in(" + bilbka_sql1 + ")"
                bilinf_sql = bilinf_sql + " and BILNO in(" + bilbka_sql2 + ")"
                bilinf_sql = bilinf_sql + " and BILRS in(" + bilbka_sql3 + ")"
                bilinf_sql = bilinf_sql + " with ur "
                AfaLoggerFunc.tradeDebug('bilinf_sqlΪ��'+ bilinf_sql)
                bilinf_list = AfaDBFunc.SelectSql(bilinf_sql)
                if( bilinf_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','��Ʊ��Ϣ�Ǽǲ�����ʧ��')
                elif( len(bilinf_list) <= 0 ):
                    TradeContext.INRDTAMT = 0.00
                else:
                    if( bilinf_list[0][0] == None ):
                        TradeContext.INRDTAMT = 0.00
                    else:
                        TradeContext.INRDTAMT = bilinf_list[0][0]
                        
                #=====������ܽ��====
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT - TradeContext.INRDTAMT
                
                #=====����Ȧ����====
                TradeContext.INRCLAMT = 0.00
                
                #=====�跽Ȧ����====
                TradeContext.INRDLAMT = 0.00
                
                #=====����Ȧ����====
                TradeContext.INROFSLAMT = TradeContext.INRCLAMT - TradeContext.INRDLAMT
                
#===========================================================================================================           
            #=====��Ʊ�⸶ ����====
            elif( record[i]['TRCCO'] == '2100100' and record[i]['BRSFLG'] == '1' ):
                AfaLoggerFunc.tradeInfo('��ʼ��Ʊ�⸶ ����')
                #=====�������ܽ��====
                AfaLoggerFunc.tradeInfo('��Ʊ�⸶ ����__�������ܽ��')
                bilbka_sql1 = "select BILVER from rcc_bilbka where BRSFLG='1' and DCFLG='2' and TRCCO='2100100' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql1 = bilbka_sql1 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT in('70','71') and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql2 = "select BILNO from rcc_bilbka where BRSFLG='1' and DCFLG='2' and TRCCO='2100100' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql2 = bilbka_sql2 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT in('70','71') and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql3 = "select BILRS from rcc_bilbka where BRSFLG='1' and DCFLG='2' and TRCCO='2100100' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql3 = bilbka_sql3 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT in('70','71') and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilinf_sql = "select sum(OCCAMT) from rcc_bilinf where BILVER in(" + bilbka_sql1 + ")"
                bilinf_sql = bilinf_sql + " and BILNO in(" + bilbka_sql2 + ")"
                bilinf_sql = bilinf_sql + " and BILRS in(" + bilbka_sql3 + ")"
                bilinf_sql = bilinf_sql + " with ur "
                AfaLoggerFunc.tradeDebug('bilinf_sqlΪ��'+ bilinf_sql)
                bilinf_list = AfaDBFunc.SelectSql(bilinf_sql)
                if( bilinf_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','��Ʊ��Ϣ�Ǽǲ�����ʧ��')
                elif( len(bilinf_list) <= 0 ):
                    TradeContext.INRCTAMT = 0.00
                else:
                    if( bilinf_list[0][0] == None ):
                        TradeContext.INRCTAMT = 0.00
                    else:
                        TradeContext.INRCTAMT = bilinf_list[0][0]
                
                AfaLoggerFunc.tradeDebug('INRCTAMTΪ��'+  str(TradeContext.INRCTAMT))
                
                #=====�跽���ܽ��====
                AfaLoggerFunc.tradeInfo('��Ʊ�⸶ ����__�跽���ܽ��')
                bilbka_sql1 = "select BILVER from rcc_bilbka where BRSFLG='1' and DCFLG='1' and TRCCO='2100100' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql1 = bilbka_sql1 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT in('70','71') and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql2 = "select BILNO from rcc_bilbka where BRSFLG='1' and DCFLG='1' and TRCCO='2100100' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql2 = bilbka_sql2 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT in('70','71') and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql3 = "select BILRS from rcc_bilbka where BRSFLG='1' and DCFLG='1' and TRCCO='2100100' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql3 = bilbka_sql3 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT in('70','71') and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilinf_sql = "select sum(OCCAMT) from rcc_bilinf where BILVER in(" + bilbka_sql1 + ")"
                bilinf_sql = bilinf_sql + " and BILNO in(" + bilbka_sql2 + ")"
                bilinf_sql = bilinf_sql + " and BILRS in(" + bilbka_sql3 + ")"
                bilinf_sql = bilinf_sql + " with ur "
                AfaLoggerFunc.tradeDebug('bilinf_sqlΪ��'+ bilinf_sql)
                bilinf_list = AfaDBFunc.SelectSql(bilinf_sql)
                if( bilinf_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','��Ʊ��Ϣ�Ǽǲ�����ʧ��')
                elif( len(bilinf_list) <= 0 ):
                    TradeContext.INRDTAMT = 0.00
                else:
                    if( bilinf_list[0][0] == None ):
                        TradeContext.INRDTAMT = 0.00
                    else:
                        TradeContext.INRDTAMT = bilinf_list[0][0]

                #=====������ܽ��====
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT - TradeContext.INRDTAMT
                
                #=====����Ȧ����====
                AfaLoggerFunc.tradeInfo('��Ʊ�⸶ ����__����Ȧ����')
                bilbka_sql1 = "select BILVER from rcc_bilbka where BRSFLG='1' and DCFLG='1' and TRCCO='2100100' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql1 = bilbka_sql1 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT in('70','71') and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql2 = "select BILNO from rcc_bilbka where BRSFLG='1' and DCFLG='1' and TRCCO='2100100' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql2 = bilbka_sql2 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT in('70','71') and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql3 = "select BILRS from rcc_bilbka where BRSFLG='1' and DCFLG='1' and TRCCO='2100100' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql3 = bilbka_sql3 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT in('70','71') and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilinf_sql = "select sum(BILAMT) from rcc_bilinf where BILVER in(" + bilbka_sql1 + ")"
                bilinf_sql = bilinf_sql + " and BILNO in(" + bilbka_sql2 + ")"
                bilinf_sql = bilinf_sql + " and BILRS in(" + bilbka_sql3 + ")"
                bilinf_sql = bilinf_sql + " with ur "
                AfaLoggerFunc.tradeDebug('bilinf_sqlΪ��'+ bilinf_sql)
                bilinf_list = AfaDBFunc.SelectSql(bilinf_sql)
                if( bilinf_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','��Ʊ��Ϣ�Ǽǲ�����ʧ��')
                elif( len(bilinf_list) <= 0 ):
                    TradeContext.INRCLAMT = 0.00
                else:
                    if( bilinf_list[0][0] == None ):
                        TradeContext.INRCLAMT = 0.00
                    else:
                        TradeContext.INRCLAMT = bilinf_list[0][0]

#                TradeContext.INRCLAMT = 0.00
                        
                AfaLoggerFunc.tradeDebug('INRCLAMTΪ��' + str(TradeContext.INRCLAMT))
                
                #=====�跽Ȧ����====
                AfaLoggerFunc.tradeInfo('��Ʊ�⸶ ����__�跽Ȧ����')
                bilbka_sql1 = "select BILVER from rcc_bilbka where BRSFLG='1' and DCFLG='2' and TRCCO='2100100' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql1 = bilbka_sql1 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT in('70','71') and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql2 = "select BILNO from rcc_bilbka where BRSFLG='1' and DCFLG='2' and TRCCO='2100100' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql2 = bilbka_sql2 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT in('70','71') and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql3 = "select BILRS from rcc_bilbka where BRSFLG='1' and DCFLG='2' and TRCCO='2100100' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql3 = bilbka_sql3 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT in('70','71') and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilinf_sql = "select sum(BILAMT) from rcc_bilinf where BILVER in(" + bilbka_sql1 + ")"
                bilinf_sql = bilinf_sql + " and BILNO in(" + bilbka_sql2 + ")"
                bilinf_sql = bilinf_sql + " and BILRS in(" + bilbka_sql3 + ")"
                bilinf_sql = bilinf_sql + " with ur "
                AfaLoggerFunc.tradeDebug('bilinf_sqlΪ��'+ bilinf_sql)
                bilinf_list = AfaDBFunc.SelectSql(bilinf_sql)
                if( bilinf_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','��Ʊ��Ϣ�Ǽǲ�����ʧ��')
                elif( len(bilinf_list) <= 0 ):
                    TradeContext.INRDLAMT = 0.00
                else:
                    if( bilinf_list[0][0] == None ):
                        TradeContext.INRDLAMT = 0.00
                    else:
                        TradeContext.INRDLAMT = bilinf_list[0][0]
                TradeContext.INRDLAMT = 0.00
                
                #=====����Ȧ����====
                TradeContext.INROFSLAMT = TradeContext.INRCLAMT - TradeContext.INRDLAMT

#==================================================================================================================                
            #=====��Ʊ���� ����====
            elif( record[i]['TRCCO'] == '2100101' and record[i]['BRSFLG'] == '0' ):
                AfaLoggerFunc.tradeInfo('��ʼ��Ʊ���� ����')
                #=====�������ܽ��====
                AfaLoggerFunc.tradeInfo('��Ʊ���� ����__�������ܽ��')
#                bilbka_sql1 = "select BILVER from rcc_bilbka where BRSFLG='0' and DCFLG='2' and TRCCO='2100101' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
#                bilbka_sql1 = bilbka_sql1 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT='" + PL_BCSTAT_MFESTL + "' and BDWFLG='" + PL_BDWFLG_SUCC + "')"
#                bilbka_sql2 = "select BILNO from rcc_bilbka where BRSFLG='0' and DCFLG='2' and TRCCO='2100101' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
#                bilbka_sql2 = bilbka_sql2 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT='" + PL_BCSTAT_MFESTL + "' and BDWFLG='" + PL_BDWFLG_SUCC + "')"
#                bilbka_sql3 = "select BILRS from rcc_bilbka where BRSFLG='0' and DCFLG='2' and TRCCO='2100101' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
#                bilbka_sql3 = bilbka_sql3 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT='" + PL_BCSTAT_MFESTL + "' and BDWFLG='" + PL_BDWFLG_SUCC + "')"
#                bilinf_sql = "select sum(BILAMT) from rcc_bilinf where BILVER in(" + bilbka_sql1 + ")"
#                bilinf_sql = bilinf_sql + " and BILNO in(" + bilbka_sql2 + ")"
#                bilinf_sql = bilinf_sql + " and BILRS in(" + bilbka_sql3 + ")"
                bilinf_sql = bilinf_sql + " with ur "
#                AfaLoggerFunc.tradeInfo('bilinf_sqlΪ��'+ bilinf_sql)
#                bilinf_list = AfaDBFunc.SelectSql(bilinf_sql)
#                if( bilinf_list == None ):
#                    f.close()
#                    return AfaFlowControl.ExitThisFlow('D000','��Ʊ��Ϣ�Ǽǲ�����ʧ��')
#                elif( len(bilinf_list) <= 0 ):
#                    TradeContext.INRCTAMT = 0.00
#                else:
#                    if( bilinf_list[0][0] == None ):
#                        TradeContext.INRCTAMT = 0.00
#                    else:
#                        TradeContext.INRCTAMT = bilinf_list[0][0]

                TradeContext.INRCTAMT = 0.00
                
                AfaLoggerFunc.tradeDebug('INRCTAMTΪ��'+ str(TradeContext.INRCTAMT))
                
                #=====�跽���ܽ��====
                TradeContext.INRDTAMT = 0.00
                        
                #=====������ܽ��====
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT - TradeContext.INRDTAMT
                
                #=====����Ȧ����====
                AfaLoggerFunc.tradeInfo('��Ʊ���� ����__�跽Ȧ����')
                bilbka_sql1 = "select BILVER from rcc_bilbka where BRSFLG='0' and DCFLG='1' and TRCCO='2100101' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql1 = bilbka_sql1 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT='" + PL_BCSTAT_MFESTL + "' and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql2 = "select BILNO from rcc_bilbka where BRSFLG='0' and DCFLG='1' and TRCCO='2100101' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql2 = bilbka_sql2 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT='" + PL_BCSTAT_MFESTL + "' and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql3 = "select BILRS from rcc_bilbka where BRSFLG='0' and DCFLG='1' and TRCCO='2100101' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql3 = bilbka_sql3 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT='" + PL_BCSTAT_MFESTL + "' and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilinf_sql = "select sum(BILAMT) from rcc_bilinf where BILVER in(" + bilbka_sql1 + ")"
                bilinf_sql = bilinf_sql + " and BILNO in(" + bilbka_sql2 + ")"
                bilinf_sql = bilinf_sql + " and BILRS in(" + bilbka_sql3 + ")"
                bilinf_sql = bilinf_sql + " with ur "
                AfaLoggerFunc.tradeDebug('bilinf_sqlΪ��'+ bilinf_sql)
                bilinf_list = AfaDBFunc.SelectSql(bilinf_sql)
                if( bilinf_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','��Ʊ��Ϣ�Ǽǲ�����ʧ��')
                elif( len(bilinf_list) <= 0 ):
                    TradeContext.INRCLAMT = 0.00
                else:
                    if( bilinf_list[0][0] == None ):
                        TradeContext.INRCLAMT = 0.00
                    else:
                        TradeContext.INRCLAMT = bilinf_list[0][0]
#                TradeContext.INRCLAMT = 0.00
                
                #=====�跽Ȧ����====
                AfaLoggerFunc.tradeInfo('��Ʊ���� ����__�跽Ȧ����')
                bilbka_sql1 = "select BILVER from rcc_bilbka where BRSFLG='0' and DCFLG='2' and TRCCO='2100101' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql1 = bilbka_sql1 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT='" + PL_BCSTAT_MFESTL + "' and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql2 = "select BILNO from rcc_bilbka where BRSFLG='0' and DCFLG='2' and TRCCO='2100101' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql2 = bilbka_sql2 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT='" + PL_BCSTAT_MFESTL + "' and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql3 = "select BILRS from rcc_bilbka where BRSFLG='0' and DCFLG='2' and TRCCO='2100101' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql3 = bilbka_sql3 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT='" + PL_BCSTAT_MFESTL + "' and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilinf_sql = "select sum(BILAMT) from rcc_bilinf where BILVER in(" + bilbka_sql1 + ")"
                bilinf_sql = bilinf_sql + " and BILNO in(" + bilbka_sql2 + ")"
                bilinf_sql = bilinf_sql + " and BILRS in(" + bilbka_sql3 + ")"
                bilinf_sql = bilinf_sql + " with ur "
                AfaLoggerFunc.tradeDebug('bilinf_sqlΪ��'+ bilinf_sql)
                bilinf_list = AfaDBFunc.SelectSql(bilinf_sql)
                if( bilinf_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','��Ʊ��Ϣ�Ǽǲ�����ʧ��')
                elif( len(bilinf_list) <= 0 ):
                    TradeContext.INRDLAMT = 0.00
                else:
                    if( bilinf_list[0][0] == None ):
                        TradeContext.INRDLAMT = 0.00
                    else:
                        TradeContext.INRDLAMT = bilinf_list[0][0]
                
                #=====����Ȧ����====
                TradeContext.INROFSLAMT = TradeContext.INRCLAMT - TradeContext.INRDLAMT

#==========================================================================================================
            #=====��Ʊ��Ʊ ����====
            elif( record[i]['TRCCO'] == '2100103' and record[i]['BRSFLG'] == '0' ):
                AfaLoggerFunc.tradeInfo('��ʼ��Ʊ��Ʊ ����')
                #=====�������ܽ��====
                AfaLoggerFunc.tradeInfo('��Ʊ��Ʊ ���˻���__�������ܽ��')
#                bilbka_sql1 = "select BILVER from rcc_bilbka where BRSFLG='0' and DCFLG='2' and TRCCO='2100103' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
#                bilbka_sql1 = bilbka_sql1 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT='" + PL_BCSTAT_MFESTL + "' and BDWFLG='" + PL_BDWFLG_SUCC + "')"
#                bilbka_sql2 = "select BILNO from rcc_bilbka where BRSFLG='0' and DCFLG='2' and TRCCO='2100103' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
#                bilbka_sql2 = bilbka_sql2 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT='" + PL_BCSTAT_MFESTL + "' and BDWFLG='" + PL_BDWFLG_SUCC + "')"
#                bilbka_sql3 = "select BILRS from rcc_bilbka where BRSFLG='0' and DCFLG='2' and TRCCO='2100103' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
#                bilbka_sql3 = bilbka_sql3 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT='" + PL_BCSTAT_MFESTL + "' and BDWFLG='" + PL_BDWFLG_SUCC + "')"
#                bilinf_sql = "select sum(OCCAMT) from rcc_bilinf where BILVER in(" + bilbka_sql1 + ")"
#                bilinf_sql = bilinf_sql + " and BILNO in(" + bilbka_sql2 + ")"
#                bilinf_sql = bilinf_sql + " and BILRS in(" + bilbka_sql3 + ")"
                bilinf_sql = bilinf_sql + " with ur "
#                AfaLoggerFunc.tradeInfo('bilinf_sqlΪ��'+ bilinf_sql)
#                bilinf_list = AfaDBFunc.SelectSql(bilinf_sql)
#                if( bilinf_list == None ):
#                    f.close()
#                    return AfaFlowControl.ExitThisFlow('D000','��Ʊ��Ϣ�Ǽǲ�����ʧ��')
#                elif( len(bilinf_list) <= 0 ):
#                    TradeContext.INRCTAMT = 0.00
#                else:
#                    if( bilinf_list[0][0] == None ):
#                        TradeContext.INRCTAMT = 0.00
#                    else:
#                        TradeContext.INRCTAMT = bilinf_list[0][0]
#                        
#                AfaLoggerFunc.tradeInfo('INRCTAMTΪ��'+ str(TradeContext.INRCTAMT))
                TradeContext.INRCTAMT = 0.00
                
                #=====�跽���ܽ��====
                TradeContext.INRDTAMT = 0.00
                        
                #=====������ܽ��====
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT - TradeContext.INRDTAMT
                
                #=====����Ȧ����====
                AfaLoggerFunc.tradeInfo('��Ʊ��Ʊ ���˻���__����Ȧ����')
                bilbka_sql1 = "select BILVER from rcc_bilbka where BRSFLG='0' and DCFLG='1' and TRCCO='2100103' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql1 = bilbka_sql1 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT='" + PL_BCSTAT_MFESTL + "' and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql2 = "select BILNO from rcc_bilbka where BRSFLG='0' and DCFLG='1' and TRCCO='2100103' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql2 = bilbka_sql2 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT='" + PL_BCSTAT_MFESTL + "' and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql3 = "select BILRS from rcc_bilbka where BRSFLG='0' and DCFLG='1' and TRCCO='2100103' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql3 = bilbka_sql3 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT='" + PL_BCSTAT_MFESTL + "' and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilinf_sql = "select sum(BILAMT) from rcc_bilinf where BILVER in(" + bilbka_sql1 + ")"
                bilinf_sql = bilinf_sql + " and BILNO in(" + bilbka_sql2 + ")"
                bilinf_sql = bilinf_sql + " and BILRS in(" + bilbka_sql3 + ")"
                bilinf_sql = bilinf_sql + " with ur "
                AfaLoggerFunc.tradeDebug('bilinf_sqlΪ��'+ bilinf_sql)
                bilinf_list = AfaDBFunc.SelectSql(bilinf_sql)
                if( bilinf_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','��Ʊ��Ϣ�Ǽǲ�����ʧ��')
                elif( len(bilinf_list) <= 0 ):
                    TradeContext.INRCTAMT = 0.00
                else:
                    if( bilinf_list[0][0] == None ):
                        TradeContext.INRCLAMT = 0.00
                    else:
                        TradeContext.INRCLAMT = bilinf_list[0][0]

#                TradeContext.INRCLAMT = 0.00
                        
                AfaLoggerFunc.tradeDebug('INRCLAMTΪ��'+ str(TradeContext.INRCLAMT))

                
                #=====�跽Ȧ����====
                AfaLoggerFunc.tradeInfo('��Ʊ��Ʊ ����__�跽Ȧ����')
                bilbka_sql1 = "select BILVER from rcc_bilbka where BRSFLG='0' and DCFLG='2' and TRCCO='2100103' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql1 = bilbka_sql1 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT='" + PL_BCSTAT_MFESTL + "' and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql2 = "select BILNO from rcc_bilbka where BRSFLG='0' and DCFLG='2' and TRCCO='2100103' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql2 = bilbka_sql2 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT='" + PL_BCSTAT_MFESTL + "' and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql3 = "select BILRS from rcc_bilbka where BRSFLG='0' and DCFLG='2' and TRCCO='2100103' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql3 = bilbka_sql3 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT='" + PL_BCSTAT_MFESTL + "' and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilinf_sql = "select sum(BILAMT) from rcc_bilinf where BILVER in(" + bilbka_sql1 + ")"
                bilinf_sql = bilinf_sql + " and BILNO in(" + bilbka_sql2 + ")"
                bilinf_sql = bilinf_sql + " and BILRS in(" + bilbka_sql3 + ")"
                bilinf_sql = bilinf_sql + " with ur "
                AfaLoggerFunc.tradeDebug('bilinf_sqlΪ��'+ bilinf_sql)
                bilinf_list = AfaDBFunc.SelectSql(bilinf_sql)
                if( bilinf_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','��Ʊ��Ϣ�Ǽǲ�����ʧ��')
                elif( len(bilinf_list) <= 0 ):
                    TradeContext.INRDLAMT = 0.00
                else:
                    if( bilinf_list[0][0] == None ):
                        TradeContext.INRDLAMT = 0.00
                    else:
                        TradeContext.INRDLAMT = bilinf_list[0][0]
                
                #=====����Ȧ����====
                TradeContext.INROFSLAMT = TradeContext.INRCLAMT - TradeContext.INRDLAMT
            
#==========================================================================================================================================                
            AfaLoggerFunc.tradeInfo('���ڻ��������Ϊ��'+str(TradeContext.INROFSTAMT))
           
            #=====���������ܱ���====
            AfaLoggerFunc.tradeInfo('��ʼ���������ܱ���')
            #=====��֯��ѯbilbka�Ĳ�ѯ���====
            bilbka_sql = ""
            bilbka_sql = "select count(*) from rcc_bilbka where "           
            bilbka_sql = bilbka_sql + "NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
            
            if record[i]['TRCCO'] == '0000000':
                bilbka_sql = bilbka_sql + " and TRCCO in ('2100001','2100100','2100101','2100103')"
            else:
                bilbka_sql = bilbka_sql + " and TRCCO='" + record[i]['TRCCO'] + "'"
                
            if record[i]['BRSFLG'] == '9':
                bilbka_sql = bilbka_sql + " and BRSFLG in ('1','0')"
            else:
                bilbka_sql = bilbka_sql + " and BRSFLG='" + record[i]['BRSFLG'] + "'"
                
            if( record[i]['BRSFLG'] == PL_BRSFLG_SND ):
                bilbka_sql = bilbka_sql + " and bspsqn in (select bspsqn from rcc_spbsta where bcstat='" + PL_BCSTAT_MFESTL + "'"
                bilbka_sql = bilbka_sql + " and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                
            elif( record[i]['BRSFLG'] == PL_BRSFLG_RCV ):
                bilbka_sql = bilbka_sql + " and bspsqn in (select bspsqn from rcc_spbsta where bcstat in('70','71')"
                bilbka_sql = bilbka_sql + " and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                
            else:
                bilbka_sql = bilbka_sql + " and bspsqn in (select bspsqn from rcc_spbsta where bcstat in('70','71','42')"
                bilbka_sql = bilbka_sql + " and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                
            bilinf_sql = bilinf_sql + " with ur "
            AfaLoggerFunc.tradeDebug( 'SQLl==' + bilbka_sql )
            #count = rccpsDBTrcc_bilbka.count(bilbka_sql)
            AfaLoggerFunc.tradeDebug("<<<��ѯ�ܱ���")
            count = AfaDBFunc.SelectSql(bilbka_sql)
            if count == None:
                f.close()
                return AfaFlowControl.ExitThisFlow('D000','��ѯ�ܱ���ʧ��')
            else:
                TradeContext.INRTCNT = str(count[0][0])                  
            AfaLoggerFunc.tradeDebug( '�����ܱ���=' + TradeContext.INRTCNT )
            
            #=====��ʼ��֯�ļ�����====
            filecont = ''
            filecont = filecont + record[i]['NCCWKDAT']         + "|" + record[i]['TRCCO']           + "|"
            filecont = filecont + record[i]['BRSFLG']           + "|" + record[i]['TRCNAM']          + "|"
            filecont = filecont + record[i]['TRCRSNM']          + "|" + str(record[i]['TCNT'])       + "|"
            filecont = filecont + TradeContext.INRTCNT          + "|"
            filecont = filecont + str(record[i]['CTAMT'])       + "|" + str(record[i]['CLAMT'])      + "|"
            filecont = filecont + str(TradeContext.INRCTAMT)    + "|" + str(TradeContext.INRCLAMT)   + "|"
            filecont = filecont + str(record[i]['DTAMT'])       + "|" + str(record[i]['DLAMT'])      + "|"
            filecont = filecont + str(TradeContext.INRDTAMT)    + "|" + str(TradeContext.INRDLAMT)   + "|"
            filecont = filecont + str(record[i]['OFSTAMT'])     + "|" + str(record[i]['OFSLAMT'])    + "|"
            filecont = filecont + str(TradeContext.INROFSTAMT)  + "|" + str(TradeContext.INROFSLAMT) + "|\n"
            AfaLoggerFunc.tradeDebug( '�ļ�����=' + filecont )

            #=====д���ļ�====
            f.write(filecont)
            
        #=====�ر��ļ�====
        f.close()

    #=====��ѯ�ܼ�¼��====
    allcount=rccpsDBTrcc_hpdzhz.count(sql)     #�õ��ܼ�¼����
    if(allcount==None):
        return AfaFlowControl.ExitThisFlow('D000','���ݿ����ʧ��')
    else:
        TradeContext.RECALLCOUNT = str(allcount)

    TradeContext.PBDAFILE = filename 
    TradeContext.RECCOUNT = str(len(record))
    TradeContext.errorMsg="��ѯ�ɹ�"
    TradeContext.errorCode="0000"
    
    return True
