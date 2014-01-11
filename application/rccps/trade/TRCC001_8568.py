# -*- coding: gbk -*-
##################################################################
#   ũ����.��ѯҵ��.ͨ��ͨ�һ��ܺ˶Բ�ѯ
#=================================================================
#   �����ļ�:   TRCC001_8568.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  ����
#   �޸�ʱ��:   2008-12-22
##################################################################
import TradeContext,AfaLoggerFunc,AfaFlowControl,AfaUtilTools,AfaDBFunc
import rccpsDBTrcc_wtrbka,rccpsDBTrcc_tddzhz
from types import *
from rccpsConst import *

def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(1.���ز���)ͨ��ͨ�һ��ܺ˶Բ�ѯ[TRC001_8568]����***' )
    #=====�жϽӿ��Ƿ����====
    if not TradeContext.existVariable("NCCWKDAT"):
        return AfaFlowControl.ExitThisFlow('M999','���Ĺ�������[NCCWKDAT]������')

    #=====���кŲ�ѯ====
    sql = "NCCWKDAT = '" + TradeContext.NCCWKDAT + "'"
    
    #=====��ѯ���ݿ⣬�õ���ѯ�����====
    record=rccpsDBTrcc_tddzhz.selectm(TradeContext.RECSTRNO,10,sql,"")  
    if record == None:
        return AfaFlowControl.ExitThisFlow('D000','���ݿ����ʧ��')
    elif len(record) <= 0:
        return AfaFlowControl.ExitThisFlow('D000','û�����������ļ�¼')
    else:
        filename = 'rccps_' + TradeContext.BETELR + '_' + AfaUtilTools.GetSysDate() + '_' + TradeContext.TransCode 
        try:
            f=open("/home/maps/afa/tmp/"+filename,"w")
        except IOError:
            AfaLoggerFunc.tradeInfo('���ļ�ʧ��')
            return AfaFlowControl.ExitThisFlow('A999','���ļ�ʧ��')

        AfaLoggerFunc.tradeDebug( '�ļ�����' + filename )
        #=====��֯�����ļ�====
        AfaLoggerFunc.tradeDebug( 'start=' + str(record) )
        
        for i in range( 0, len(record) ):

########################################################################################################################
            #=====�ж�ҵ�����ͺ�������ʾ====
            if( record[i]['TRCCO'] == '0000000' and record[i]['BRSFLG'] == '1'):
                
                ##=====�ϼ� ��������====
                AfaLoggerFunc.tradeInfo('��ʼ==�ϼ� ��������==')
                
                #=====�������ܽ��====
                AfaLoggerFunc.tradeInfo('�ϼ� ��������__�������ܽ��')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('70','72','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where BRSFLG='1' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in (" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sqlΪ�� ' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','ͨ��ͨ�ҵǼǲ�����ʧ��')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCTAMT = 0.00
                    else:
                        TradeContext.INRCTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCTAMTΪ��'+  str(TradeContext.INRCTAMT))
                
                #=====�跽���ܽ��====
                AfaLoggerFunc.tradeInfo('�ϼ� ��������__�跽���ܽ��')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('70','72','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where BRSFLG='1' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sqlΪ��' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','ͨ��ͨ�ҵǼǲ�����ʧ��')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRDTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRDTAMT = 0.00
                    else:
                        TradeContext.INRDTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRDTAMTΪ��'+  str(TradeContext.INRDTAMT))    
                
                #=====��������������====
                AfaLoggerFunc.tradeInfo('�ϼ� ��������__��������������')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('70','72','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(CUSCHRG) from rcc_wtrbka where BRSFLG='1' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and TRCCO in ('3000102','3000103','3000104','3000105') and CHRGTYP='1'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sqlΪ��' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','ͨ��ͨ�ҵǼǲ�����ʧ��')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCHRCTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCHRCTAMT = 0.00
                    else:
                        TradeContext.INRCHRCTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCHRCTAMTΪ��'+  str(TradeContext.INRCHRCTAMT))
                
                #=====�跽����������====
                AfaLoggerFunc.tradeInfo('�ϼ� ��������__�跽����������')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('70','72','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(CUSCHRG) from rcc_wtrbka where BRSFLG='1' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and TRCCO in ('3000102','3000103','3000104','3000105') and CHRGTYP='1'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sqlΪ��' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','ͨ��ͨ�ҵǼǲ�����ʧ��')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCHRDTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCHRDTAMT = 0.00
                    else:
                        TradeContext.INRCHRDTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCHRDTAMTΪ��'+  str(TradeContext.INRCHRDTAMT))   
                
                #=====������ܽ��====
                AfaLoggerFunc.tradeInfo('�ϼ� ��������__�������')
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT + TradeContext.INRCHRCTAMT - TradeContext.INRDTAMT - TradeContext.INRCHRDTAMT
                AfaLoggerFunc.tradeInfo('INROFSTAMTΪ��'+ str(TradeContext.INROFSTAMT))
                
########################################################################################################################
            elif( record[i]['TRCCO'] == '0000000' and record[i]['BRSFLG'] == '3' ): 
                
                ##=====�ϼ� ���˻���====
                AfaLoggerFunc.tradeInfo('��ʼ==�ϼ� ���˻���==')
                
                #=====�������ܽ��====
                AfaLoggerFunc.tradeInfo('�ϼ� ���˻���__�������ܽ��')
                TradeContext.INRCTAMT = 0.00
                
                #=====�跽���ܽ��====
                TradeContext.INRDTAMT = 0.00
                
                #=====��������������====
                TradeContext.INRCHRCTAMT = 0.00
                
                #=====�跽����������====
                TradeContext.INRCHRDTAMT = 0.00
                
                #=====������ܽ��====
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT + TradeContext.INRCHRCTAMT - TradeContext.INRDTAMT - TradeContext.INRCHRDTAMT
                AfaLoggerFunc.tradeInfo('INROFSTAMTΪ��'+ str(TradeContext.INROFSTAMT))
                
########################################################################################################################
            elif( record[i]['TRCCO'] == '0000000' and record[i]['BRSFLG'] == '0' ): 
                
                ##=====�ϼ� �������====
                AfaLoggerFunc.tradeInfo('��ʼ==�ϼ� �������==')
                
                #=====�������ܽ��====   
                AfaLoggerFunc.tradeInfo('�ϼ� �������__�������ܽ��')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('42','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where BRSFLG='0' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sqlΪ��' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','ͨ��ͨ�ҵǼǲ�����ʧ��')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCTAMT = 0.00
                    else:
                        TradeContext.INRCTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCTAMTΪ��'+  str(TradeContext.INRCTAMT))
                
                #=====�跽���ܽ��====
                AfaLoggerFunc.tradeInfo('�ϼ� �������__�跽���ܽ��')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('42','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where BRSFLG='0' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sqlΪ��' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','ͨ��ͨ�ҵǼǲ�����ʧ��')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRDTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRDTAMT = 0.00
                    else:
                        TradeContext.INRDTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRDTAMTΪ��'+  str(TradeContext.INRDTAMT))    
                
                #=====��������������====
                AfaLoggerFunc.tradeInfo('�ϼ� �������__��������������')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('42','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(CUSCHRG) from rcc_wtrbka where BRSFLG='0' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and TRCCO in ('3000102','3000103','3000104','3000105') and CHRGTYP='1'" 
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sqlΪ��' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','ͨ��ͨ�ҵǼǲ�����ʧ��')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCHRCTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCHRCTAMT = 0.00
                    else:
                        TradeContext.INRCHRCTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCHRCTAMTΪ��'+  str(TradeContext.INRCHRCTAMT))
                
                #=====�跽����������====
                AfaLoggerFunc.tradeInfo('�ϼ� �������__�跽����������')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('42','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(CUSCHRG) from rcc_wtrbka where BRSFLG='0' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and TRCCO in ('3000102','3000103','3000104','3000105') and CHRGTYP='1'" 
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sqlΪ��' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','ͨ��ͨ�ҵǼǲ�����ʧ��')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCHRDTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCHRDTAMT = 0.00
                    else:
                        TradeContext.INRCHRDTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCHRDTAMTΪ��'+  str(TradeContext.INRCHRDTAMT))
                
                #=====������ܽ��====
                AfaLoggerFunc.tradeInfo('�ϼ� �������__�������')
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT + TradeContext.INRCHRCTAMT - TradeContext.INRDTAMT - TradeContext.INRCHRDTAMT
                AfaLoggerFunc.tradeInfo('INROFSTAMTΪ��'+ str(TradeContext.INROFSTAMT)) 
                
########################################################################################################################
            elif( record[i]['TRCCO'] == '0000000' and record[i]['BRSFLG'] == '2' ):

                ##=====�ϼ� �������====
                AfaLoggerFunc.tradeInfo('��ʼ==�ϼ� �������==')
                
                #=====�������ܽ��====   
                AfaLoggerFunc.tradeInfo('�ϼ� �������__�������ܽ��')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('70','72','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where BRSFLG='1' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sqlΪ��' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','ͨ��ͨ�ҵǼǲ�����ʧ��')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCTAMT1 = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCTAMT1 = 0.00
                    else:
                        TradeContext.INRCTAMT1 = wtrbka_list[0][0]
                        
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('42','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where BRSFLG='0' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sqlΪ��' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','ͨ��ͨ�ҵǼǲ�����ʧ��')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCTAMT2 = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCTAMT2 = 0.00
                    else:
                        TradeContext.INRCTAMT2 = wtrbka_list[0][0]
               
                TradeContext.INRCTAMT = TradeContext.INRCTAMT1 + TradeContext.INRCTAMT2                        
                AfaLoggerFunc.tradeInfo('INRCTAMTΪ��'+  str(TradeContext.INRCTAMT))
                
                #=====�跽���ܽ��====
                AfaLoggerFunc.tradeInfo('�ϼ� �������__�跽���ܽ��')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('70','72','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where BRSFLG='1' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sqlΪ��' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','ͨ��ͨ�ҵǼǲ�����ʧ��')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRDTAMT1 = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRDTAMT1 = 0.00
                    else:
                        TradeContext.INRDTAMT1 = wtrbka_list[0][0]
                        
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('42','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where BRSFLG='0' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sqlΪ��' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','ͨ��ͨ�ҵǼǲ�����ʧ��')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRDTAMT2 = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRDTAMT2 = 0.00
                    else:
                        TradeContext.INRDTAMT2 = wtrbka_list[0][0]
                                        
                TradeContext.INRDTAMT = TradeContext.INRDTAMT1 + TradeContext.INRDTAMT2                        
                AfaLoggerFunc.tradeInfo('INRDTAMTΪ��'+  str(TradeContext.INRDTAMT))    
                
                #=====��������������====
                AfaLoggerFunc.tradeInfo('�ϼ� �������__��������������')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('70','72','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(CUSCHRG) from rcc_wtrbka where BRSFLG='1' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and TRCCO in ('3000102','3000103','3000104','3000105') and CHRGTYP='1'" 
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sqlΪ��' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','ͨ��ͨ�ҵǼǲ�����ʧ��')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCHRCTAMT1 = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCHRCTAMT1 = 0.00
                    else:
                        TradeContext.INRCHRCTAMT1 = wtrbka_list[0][0]
                        
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('42','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(CUSCHRG) from rcc_wtrbka where BRSFLG='0' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and TRCCO in ('3000102','3000103','3000104','3000105') and CHRGTYP='1'" 
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sqlΪ��' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','ͨ��ͨ�ҵǼǲ�����ʧ��')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCHRCTAMT2 = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCHRCTAMT2 = 0.00
                    else:
                        TradeContext.INRCHRCTAMT2 = wtrbka_list[0][0]
                                        
                TradeContext.INRCHRCTAMT = TradeContext.INRCHRCTAMT1 + TradeContext.INRCHRCTAMT2                        
                AfaLoggerFunc.tradeInfo('INRCHRCTAMTΪ��'+  str(TradeContext.INRCHRCTAMT))
                
                #=====�跽����������====
                AfaLoggerFunc.tradeInfo('�ϼ� �������__�跽����������')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('70','72','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(CUSCHRG) from rcc_wtrbka where BRSFLG='1' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and TRCCO in ('3000102','3000103','3000104','3000105') and CHRGTYP='1'" 
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sqlΪ��' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','ͨ��ͨ�ҵǼǲ�����ʧ��')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCHRDTAMT1 = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCHRDTAMT1 = 0.00
                    else:
                        TradeContext.INRCHRDTAMT1 = wtrbka_list[0][0]
                        
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('42','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(CUSCHRG) from rcc_wtrbka where BRSFLG='0' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and TRCCO in ('3000102','3000103','3000104','3000105') and CHRGTYP='1'" 
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sqlΪ��' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','ͨ��ͨ�ҵǼǲ�����ʧ��')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCHRDTAMT2 = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCHRDTAMT2 = 0.00
                    else:
                        TradeContext.INRCHRDTAMT2 = wtrbka_list[0][0]
                                        
                TradeContext.INRCHRDTAMT = TradeContext.INRCHRDTAMT1 + TradeContext.INRCHRDTAMT2                        
                AfaLoggerFunc.tradeInfo('INRCHRDTAMTΪ��'+  str(TradeContext.INRCHRDTAMT))
                
                #=====������ܽ��====
                AfaLoggerFunc.tradeInfo('�ϼ� �������__�������')
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT + TradeContext.INRCHRCTAMT - TradeContext.INRDTAMT - TradeContext.INRCHRDTAMT
                AfaLoggerFunc.tradeInfo('INROFSTAMTΪ��'+ str(TradeContext.INROFSTAMT))
                
########################################################################################################################
            elif( record[i]['TRCCO'] == '3000001' and record[i]['BRSFLG'] == '1' ):
                ##=====ATM��ת�� ��������====
                AfaLoggerFunc.tradeInfo('��ʼ==ATM��ת�� ��������==')
                
                #=====�������ܽ��====
                TradeContext.INRCTAMT = 0.00
                
                #=====�跽���ܽ��====
                TradeContext.INRDTAMT = 0.00
                
                #=====��������������====
                TradeContext.INRCHRCTAMT = 0.00
                
                #=====�跽����������====
                TradeContext.INRCHRDTAMT = 0.00
                
                #=====������ܽ��====
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT + TradeContext.INRCHRCTAMT - TradeContext.INRDTAMT - TradeContext.INRCHRDTAMT
                
########################################################################################################################
            elif( record[i]['TRCCO'] == '3000001' and record[i]['BRSFLG'] == '0' ):
                ##=====ATM��ת�� �������====
                AfaLoggerFunc.tradeInfo('��ʼ==ATM��ת�� �������==')
                
                #=====�������ܽ��====
                TradeContext.INRCTAMT = 0.00
                
                #=====�跽���ܽ��====
                TradeContext.INRDTAMT = 0.00
                
                #=====��������������====
                TradeContext.INRCHRCTAMT = 0.00
                
                #=====�跽����������====
                TradeContext.INRCHRDTAMT = 0.00
                
                #=====������ܽ��====
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT + TradeContext.INRCHRCTAMT - TradeContext.INRDTAMT - TradeContext.INRCHRDTAMT
                
########################################################################################################################
            elif( record[i]['TRCCO'] == '3000002' and record[i]['BRSFLG'] == '1' ):

                ##=====��̨������ ��������====
                AfaLoggerFunc.tradeInfo('��ʼ==��̨������ ��������==')
                
                #=====�������ܽ��====   
                AfaLoggerFunc.tradeInfo('��̨������ ��������__�������ܽ��')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('70','72','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where TRCCO='3000002' and BRSFLG='1' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sqlΪ��' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','ͨ��ͨ�ҵǼǲ�����ʧ��')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCTAMT = 0.00
                    else:
                        TradeContext.INRCTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCTAMTΪ��'+  str(TradeContext.INRCTAMT))
                
                #=====�跽���ܽ��====
                AfaLoggerFunc.tradeInfo('��̨������ ��������__�跽���ܽ��')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('70','72','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where TRCCO='3000002' and BRSFLG='1' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sqlΪ��' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','ͨ��ͨ�ҵǼǲ�����ʧ��')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRDTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRDTAMT = 0.00
                    else:
                        TradeContext.INRDTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRDTAMTΪ��'+  str(TradeContext.INRDTAMT))    
                
                #=====��������������====
                TradeContext.INRCHRCTAMT = 0.00
                AfaLoggerFunc.tradeInfo('INRCHRCTAMTΪ��'+  str(TradeContext.INRCHRCTAMT))
                
                #=====�跽����������====
                TradeContext.INRCHRDTAMT = 0.00
                AfaLoggerFunc.tradeInfo('INRCHRDTAMTΪ��'+  str(TradeContext.INRCHRDTAMT))
                
                #=====������ܽ��====
                AfaLoggerFunc.tradeInfo('��̨������ ��������__�������')
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT + TradeContext.INRCHRCTAMT - TradeContext.INRDTAMT - TradeContext.INRCHRDTAMT
                AfaLoggerFunc.tradeInfo('INROFSTAMTΪ��'+ str(TradeContext.INROFSTAMT)) 

#########################################################################################################################
            elif( record[i]['TRCCO'] == '3000002' and record[i]['BRSFLG'] == '0' ): 
                
                ##=====��̨������ �������====
                AfaLoggerFunc.tradeInfo('��ʼ==��̨������ �������==')
                
                 #=====�������ܽ��====   
                AfaLoggerFunc.tradeInfo('��̨������ �������__�������ܽ��')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('42','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where TRCCO='3000002' and BRSFLG='0' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sqlΪ��' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','ͨ��ͨ�ҵǼǲ�����ʧ��')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCTAMT = 0.00
                    else:
                        TradeContext.INRCTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCTAMTΪ��'+  str(TradeContext.INRCTAMT))
                
                #=====�跽���ܽ��====
                AfaLoggerFunc.tradeInfo('��̨������ �������__�跽���ܽ��')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('42','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where TRCCO='3000002' and BRSFLG='0' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sqlΪ��' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','ͨ��ͨ�ҵǼǲ�����ʧ��')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRDTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRDTAMT = 0.00
                    else:
                        TradeContext.INRDTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRDTAMTΪ��'+  str(TradeContext.INRDTAMT))    
                
                #=====��������������====
                TradeContext.INRCHRCTAMT = 0.00
                AfaLoggerFunc.tradeInfo('INRCHRCTAMTΪ��'+  str(TradeContext.INRCHRCTAMT))
                
                #=====�跽����������====
                TradeContext.INRCHRDTAMT = 0.00
                AfaLoggerFunc.tradeInfo('INRCHRDTAMTΪ��'+  str(TradeContext.INRCHRDTAMT))
                
                #=====������ܽ��====
                AfaLoggerFunc.tradeInfo('��̨������ �������__�������')
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT + TradeContext.INRCHRCTAMT - TradeContext.INRDTAMT - TradeContext.INRCHRDTAMT
                AfaLoggerFunc.tradeInfo('INROFSTAMTΪ��'+ str(TradeContext.INROFSTAMT))   
                
#########################################################################################################################
            elif( record[i]['TRCCO'] == '3000003' and record[i]['BRSFLG'] == '1' ):

                ##=====��̨����ת�� ��������====
                AfaLoggerFunc.tradeInfo('��ʼ==��̨����ת�� ��������==')
                
                #=====�������ܽ��====   
                AfaLoggerFunc.tradeInfo('��̨����ת�� ��������__�������ܽ��')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('70','72','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where TRCCO='3000003' and BRSFLG='1' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sqlΪ��' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','ͨ��ͨ�ҵǼǲ�����ʧ��')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCTAMT = 0.00
                    else:
                        TradeContext.INRCTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCTAMTΪ��'+  str(TradeContext.INRCTAMT))
                
                #=====�跽���ܽ��====
                AfaLoggerFunc.tradeInfo('��̨����ת�� ��������__�跽���ܽ��')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('70','72','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where TRCCO='3000003' and BRSFLG='1' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sqlΪ��' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','ͨ��ͨ�ҵǼǲ�����ʧ��')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRDTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRDTAMT = 0.00
                    else:
                        TradeContext.INRDTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRDTAMTΪ��'+  str(TradeContext.INRDTAMT))    
                
                #=====��������������====
                TradeContext.INRCHRCTAMT = 0.00
                AfaLoggerFunc.tradeInfo('INRCHRCTAMTΪ��'+  str(TradeContext.INRCHRCTAMT))
                
                #=====�跽����������====
                TradeContext.INRCHRDTAMT = 0.00
                AfaLoggerFunc.tradeInfo('INRCHRDTAMTΪ��'+  str(TradeContext.INRCHRDTAMT))
                
                #=====������ܽ��====
                AfaLoggerFunc.tradeInfo('��̨����ת�� ��������__�������')
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT + TradeContext.INRCHRCTAMT - TradeContext.INRDTAMT - TradeContext.INRCHRDTAMT
                AfaLoggerFunc.tradeInfo('INROFSTAMTΪ��'+ str(TradeContext.INROFSTAMT)) 
                
########################################################################################################################
            elif( record[i]['TRCCO'] == '3000003' and record[i]['BRSFLG'] == '0' ): 
                
                ##=====��̨����ת�� �������====
                AfaLoggerFunc.tradeInfo('��ʼ==��̨����ת�� �������==')
                
                 #=====�������ܽ��====   
                AfaLoggerFunc.tradeInfo('��̨����ת�� �������__�������ܽ��')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('42','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where TRCCO='3000003' and BRSFLG='0' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sqlΪ��' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','ͨ��ͨ�ҵǼǲ�����ʧ��')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCTAMT = 0.00
                    else:
                        TradeContext.INRCTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCTAMTΪ��'+  str(TradeContext.INRCTAMT))
                
                #=====�跽���ܽ��====
                AfaLoggerFunc.tradeInfo('��̨����ת�� �������__�跽���ܽ��')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('42','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where TRCCO='3000003' and BRSFLG='0' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sqlΪ��' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','ͨ��ͨ�ҵǼǲ�����ʧ��')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRDTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRDTAMT = 0.00
                    else:
                        TradeContext.INRDTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRDTAMTΪ��'+  str(TradeContext.INRDTAMT))    
                
                #=====��������������====
                TradeContext.INRCHRCTAMT = 0.00
                AfaLoggerFunc.tradeInfo('INRCHRCTAMTΪ��'+  str(TradeContext.INRCHRCTAMT))
                
                #=====�跽����������====
                TradeContext.INRCHRDTAMT = 0.00
                AfaLoggerFunc.tradeInfo('INRCHRDTAMTΪ��'+  str(TradeContext.INRCHRDTAMT))
                
                #=====������ܽ��====
                AfaLoggerFunc.tradeInfo('��̨����ת�� �������__�������')
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT + TradeContext.INRCHRCTAMT - TradeContext.INRDTAMT - TradeContext.INRCHRDTAMT
                AfaLoggerFunc.tradeInfo('INROFSTAMTΪ��'+ str(TradeContext.INROFSTAMT)) 
                
########################################################################################################################
            elif( record[i]['TRCCO'] == '3000004' and record[i]['BRSFLG'] == '1' ):

                ##=====��̨�۴��� ��������====
                AfaLoggerFunc.tradeInfo('��ʼ==��̨�۴��� ��������==')
                
                #=====�������ܽ��====   
                AfaLoggerFunc.tradeInfo('��̨�۴��� ��������__�������ܽ��')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('70','72','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where TRCCO='3000004' and BRSFLG='1' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sqlΪ��' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','ͨ��ͨ�ҵǼǲ�����ʧ��')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCTAMT = 0.00
                    else:
                        TradeContext.INRCTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCTAMTΪ��'+  str(TradeContext.INRCTAMT))
                
                #=====�跽���ܽ��====
                AfaLoggerFunc.tradeInfo('��̨�۴��� ��������__�跽���ܽ��')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('70','72','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where TRCCO='3000004' and BRSFLG='1' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sqlΪ��' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','ͨ��ͨ�ҵǼǲ�����ʧ��')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRDTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRDTAMT = 0.00
                    else:
                        TradeContext.INRDTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRDTAMTΪ��'+  str(TradeContext.INRDTAMT))    
                
                #=====��������������====
                TradeContext.INRCHRCTAMT = 0.00
                AfaLoggerFunc.tradeInfo('INRCHRCTAMTΪ��'+  str(TradeContext.INRCHRCTAMT))
                
                #=====�跽����������====
                TradeContext.INRCHRDTAMT = 0.00
                AfaLoggerFunc.tradeInfo('INRCHRDTAMTΪ��'+  str(TradeContext.INRCHRDTAMT))
                
                #=====������ܽ��====
                AfaLoggerFunc.tradeInfo('��̨�۴��� ��������__�������')
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT + TradeContext.INRCHRCTAMT - TradeContext.INRDTAMT - TradeContext.INRCHRDTAMT
                AfaLoggerFunc.tradeInfo('INROFSTAMTΪ��'+ str(TradeContext.INROFSTAMT))
                
########################################################################################################################
            elif( record[i]['TRCCO'] == '3000004' and record[i]['BRSFLG'] == '0' ): 
                
                ##=====��̨�۴��� �������====
                AfaLoggerFunc.tradeInfo('��ʼ==��̨�۴��� �������==')
                
                 #=====�������ܽ��====   
                AfaLoggerFunc.tradeInfo('��̨�۴��� �������__�������ܽ��')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('42','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where TRCCO='3000004' and BRSFLG='0' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sqlΪ��' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','ͨ��ͨ�ҵǼǲ�����ʧ��')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCTAMT = 0.00
                    else:
                        TradeContext.INRCTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCTAMTΪ��'+  str(TradeContext.INRCTAMT))
                
                #=====�跽���ܽ��====
                AfaLoggerFunc.tradeInfo('��̨�۴��� �������__�跽���ܽ��')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('42','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where TRCCO='3000004' and BRSFLG='0' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sqlΪ��' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','ͨ��ͨ�ҵǼǲ�����ʧ��')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRDTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRDTAMT = 0.00
                    else:
                        TradeContext.INRDTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRDTAMTΪ��'+  str(TradeContext.INRDTAMT))    
                
                #=====��������������====
                TradeContext.INRCHRCTAMT = 0.00
                AfaLoggerFunc.tradeInfo('INRCHRCTAMTΪ��'+  str(TradeContext.INRCHRCTAMT))
                
                #=====�跽����������====
                TradeContext.INRCHRDTAMT = 0.00
                AfaLoggerFunc.tradeInfo('INRCHRDTAMTΪ��'+  str(TradeContext.INRCHRDTAMT))
                
                #=====������ܽ��====
                AfaLoggerFunc.tradeInfo('��̨�۴��� �������__�������')
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT + TradeContext.INRCHRCTAMT - TradeContext.INRDTAMT - TradeContext.INRCHRDTAMT
                AfaLoggerFunc.tradeInfo('INROFSTAMTΪ��'+ str(TradeContext.INROFSTAMT))  
                           
########################################################################################################################
            elif( record[i]['TRCCO'] == '3000005' and record[i]['BRSFLG'] == '1' ):

                ##=====��̨�۱�ת�� ��������====
                AfaLoggerFunc.tradeInfo('��ʼ==��̨�۱�ת�� ��������==')
                
                #=====�������ܽ��====   
                AfaLoggerFunc.tradeInfo('��̨�۱�ת�� ��������__�������ܽ��')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('70','72','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where TRCCO='3000005' and BRSFLG='1' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sqlΪ��' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','ͨ��ͨ�ҵǼǲ�����ʧ��')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCTAMT = 0.00
                    else:
                        TradeContext.INRCTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCTAMTΪ��'+  str(TradeContext.INRCTAMT))
                
                #=====�跽���ܽ��====
                AfaLoggerFunc.tradeInfo('��̨�۱�ת�� ��������__�跽���ܽ��')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('70','72','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where TRCCO='3000005' and BRSFLG='1' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sqlΪ��' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','ͨ��ͨ�ҵǼǲ�����ʧ��')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRDTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRDTAMT = 0.00
                    else:
                        TradeContext.INRDTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRDTAMTΪ��'+  str(TradeContext.INRDTAMT))    
                
                #=====��������������====
                TradeContext.INRCHRCTAMT = 0.00
                AfaLoggerFunc.tradeInfo('INRCHRCTAMTΪ��'+  str(TradeContext.INRCHRCTAMT))
                
                #=====�跽����������====
                TradeContext.INRCHRDTAMT = 0.00
                AfaLoggerFunc.tradeInfo('INRCHRDTAMTΪ��'+  str(TradeContext.INRCHRDTAMT))
                
                #=====������ܽ��====
                AfaLoggerFunc.tradeInfo('��̨�۱�ת�� ��������__�������')
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT + TradeContext.INRCHRCTAMT - TradeContext.INRDTAMT - TradeContext.INRCHRDTAMT
                AfaLoggerFunc.tradeInfo('INROFSTAMTΪ��'+ str(TradeContext.INROFSTAMT)) 
                
########################################################################################################################
            elif( record[i]['TRCCO'] == '3000005' and record[i]['BRSFLG'] == '0' ): 
                
                ##=====��̨�۱�ת�� �������====
                AfaLoggerFunc.tradeInfo('��ʼ==��̨�۱�ת�� �������==')
                
                 #=====�������ܽ��====   
                AfaLoggerFunc.tradeInfo('��̨�۱�ת�� �������__�������ܽ��')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('42','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where TRCCO='3000005' and BRSFLG='0' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sqlΪ��' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','ͨ��ͨ�ҵǼǲ�����ʧ��')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCTAMT = 0.00
                    else:
                        TradeContext.INRCTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCTAMTΪ��'+  str(TradeContext.INRCTAMT))
                
                #=====�跽���ܽ��====
                AfaLoggerFunc.tradeInfo('��̨�۱�ת�� �������__�跽���ܽ��')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('42','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where TRCCO='3000005' and BRSFLG='0' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sqlΪ��' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','ͨ��ͨ�ҵǼǲ�����ʧ��')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRDTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRDTAMT = 0.00
                    else:
                        TradeContext.INRDTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRDTAMTΪ��'+  str(TradeContext.INRDTAMT))    
                
                #=====��������������====
                TradeContext.INRCHRCTAMT = 0.00
                AfaLoggerFunc.tradeInfo('INRCHRCTAMTΪ��'+  str(TradeContext.INRCHRCTAMT))
                
                #=====�跽����������====
                TradeContext.INRCHRDTAMT = 0.00
                AfaLoggerFunc.tradeInfo('INRCHRDTAMTΪ��'+  str(TradeContext.INRCHRDTAMT))
                
                #=====������ܽ��====
                AfaLoggerFunc.tradeInfo('��̨�۱�ת�� �������__�������')
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT + TradeContext.INRCHRCTAMT - TradeContext.INRDTAMT - TradeContext.INRCHRDTAMT
                AfaLoggerFunc.tradeInfo('INROFSTAMTΪ��'+ str(TradeContext.INROFSTAMT)) 
                    
########################################################################################################################
            elif( record[i]['TRCCO'] == '3000100' and record[i]['BRSFLG'] == '1' ):
                
                ##=====ATMȡ�� ��������====
                AfaLoggerFunc.tradeInfo('��ʼ==ATMȡ�� ��������==')
                
                #=====�������ܽ��====
                TradeContext.INRCTAMT = 0.00
                AfaLoggerFunc.tradeInfo('INRCTAMTΪ��'+  str(TradeContext.INRCTAMT))
                
                #=====�跽���ܽ��====
                TradeContext.INRDTAMT = 0.00
                AfaLoggerFunc.tradeInfo('INRDTAMTΪ��'+  str(TradeContext.INRDTAMT))
                
                #=====��������������====
                TradeContext.INRCHRCTAMT = 0.00
                AfaLoggerFunc.tradeInfo('INRCHRCTAMTΪ��'+  str(TradeContext.INRCHRCTAMT))
                
                #=====�跽����������====
                TradeContext.INRCHRDTAMT = 0.00
                AfaLoggerFunc.tradeInfo('INRCHRDTAMTΪ��'+  str(TradeContext.INRCHRDTAMT))
                
                #=====������ܽ��====
                AfaLoggerFunc.tradeInfo('ATMȡ�� ��������__�������')
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT + TradeContext.INRCHRCTAMT - TradeContext.INRDTAMT - TradeContext.INRCHRDTAMT
                AfaLoggerFunc.tradeInfo('INROFSTAMTΪ��'+ str(TradeContext.INROFSTAMT))
                
########################################################################################################################
            elif( record[i]['TRCCO'] == '3000100' and record[i]['BRSFLG'] == '0' ):
                
                ##=====ATMȡ�� �������====
                AfaLoggerFunc.tradeInfo('��ʼ==ATMȡ�� �������==')
                
                #=====�������ܽ��====
                TradeContext.INRCTAMT = 0.00
                AfaLoggerFunc.tradeInfo('INRCTAMTΪ��'+  str(TradeContext.INRCTAMT))
                
                #=====�跽���ܽ��====
                TradeContext.INRDTAMT = 0.00
                AfaLoggerFunc.tradeInfo('INRDTAMTΪ��'+  str(TradeContext.INRDTAMT))
                
                #=====��������������====
                TradeContext.INRCHRCTAMT = 0.00
                AfaLoggerFunc.tradeInfo('INRCHRCTAMTΪ��'+  str(TradeContext.INRCHRCTAMT))
                
                #=====�跽����������====
                TradeContext.INRCHRDTAMT = 0.00
                AfaLoggerFunc.tradeInfo('INRCHRDTAMTΪ��'+  str(TradeContext.INRCHRDTAMT))
                
                #=====������ܽ��====
                AfaLoggerFunc.tradeInfo('ATMȡ�� �������__�������')
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT + TradeContext.INRCHRCTAMT - TradeContext.INRDTAMT - TradeContext.INRCHRDTAMT
                AfaLoggerFunc.tradeInfo('INROFSTAMTΪ��'+ str(TradeContext.INROFSTAMT))
                
########################################################################################################################
            elif( record[i]['TRCCO'] == '3000101' and record[i]['BRSFLG'] == '1' ):
                
                ##=====ATM��ת�� ��������====
                AfaLoggerFunc.tradeInfo('��ʼ==ATM��ת�� ��������==')
                
                #=====�������ܽ��====
                TradeContext.INRCTAMT = 0.00
                AfaLoggerFunc.tradeInfo('INRCTAMTΪ��'+  str(TradeContext.INRCTAMT))
                
                #=====�跽���ܽ��====
                TradeContext.INRDTAMT = 0.00
                AfaLoggerFunc.tradeInfo('INRDTAMTΪ��'+  str(TradeContext.INRDTAMT))
                
                #=====��������������====
                TradeContext.INRCHRCTAMT = 0.00
                AfaLoggerFunc.tradeInfo('INRCHRCTAMTΪ��'+  str(TradeContext.INRCHRCTAMT))
                
                #=====�跽����������====
                TradeContext.INRCHRDTAMT = 0.00
                AfaLoggerFunc.tradeInfo('INRCHRDTAMTΪ��'+  str(TradeContext.INRCHRDTAMT))
                
                #=====������ܽ��====
                AfaLoggerFunc.tradeInfo('ATM��ת�� ��������__�������')
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT + TradeContext.INRCHRCTAMT - TradeContext.INRDTAMT - TradeContext.INRCHRDTAMT
                AfaLoggerFunc.tradeInfo('INROFSTAMTΪ��'+ str(TradeContext.INROFSTAMT))
                
########################################################################################################################
            elif( record[i]['TRCCO'] == '3000101' and record[i]['BRSFLG'] == '0' ):
                
                ##=====ATM��ת�� �������====
                AfaLoggerFunc.tradeInfo('��ʼ==ATM��ת�� �������==')
                
                #=====�������ܽ��====
                TradeContext.INRCTAMT = 0.00
                AfaLoggerFunc.tradeInfo('INRCTAMTΪ��'+  str(TradeContext.INRCTAMT))
                
                #=====�跽���ܽ��====
                TradeContext.INRDTAMT = 0.00
                AfaLoggerFunc.tradeInfo('INRDTAMTΪ��'+  str(TradeContext.INRDTAMT))
                
                #=====��������������====
                TradeContext.INRCHRCTAMT = 0.00
                AfaLoggerFunc.tradeInfo('INRCHRCTAMTΪ��'+  str(TradeContext.INRCHRCTAMT))
                
                #=====�跽����������====
                TradeContext.INRCHRDTAMT = 0.00
                AfaLoggerFunc.tradeInfo('INRCHRDTAMTΪ��'+  str(TradeContext.INRCHRDTAMT))
                
                #=====������ܽ��====
                AfaLoggerFunc.tradeInfo('ATM��ת�� �������__�������')
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT + TradeContext.INRCHRCTAMT - TradeContext.INRDTAMT - TradeContext.INRCHRDTAMT
                AfaLoggerFunc.tradeInfo('INROFSTAMTΪ��'+ str(TradeContext.INROFSTAMT))
                
########################################################################################################################                
            elif( record[i]['TRCCO'] == '3000102' and record[i]['BRSFLG'] == '1' ):

                ##=====��̨��ȡ�� ��������====
                AfaLoggerFunc.tradeInfo('��ʼ==��̨��ȡ�� ��������==')
                
                #=====�������ܽ��====   
                AfaLoggerFunc.tradeInfo('��̨��ȡ�� ��������__�������ܽ��')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('70','72','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where TRCCO='3000102' and BRSFLG='1' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sqlΪ��' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','ͨ��ͨ�ҵǼǲ�����ʧ��')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCTAMT = 0.00
                    else:
                        TradeContext.INRCTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCTAMTΪ��'+  str(TradeContext.INRCTAMT))
                
                #=====�跽���ܽ��====
                AfaLoggerFunc.tradeInfo('��̨��ȡ�� ��������__�跽���ܽ��')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('70','72','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where TRCCO='3000102' and BRSFLG='1' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sqlΪ��' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','ͨ��ͨ�ҵǼǲ�����ʧ��')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRDTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRDTAMT = 0.00
                    else:
                        TradeContext.INRDTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRDTAMTΪ��'+  str(TradeContext.INRDTAMT))    
                
                #=====��������������====
                AfaLoggerFunc.tradeInfo('��̨��ȡ�� ��������__��������������')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('70','72','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(CUSCHRG) from rcc_wtrbka where TRCCO='3000102' and CHRGTYP='1' and BRSFLG='1' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sqlΪ��' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','ͨ��ͨ�ҵǼǲ�����ʧ��')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCHRCTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCHRCTAMT = 0.00
                    else:
                        TradeContext.INRCHRCTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCHRCTAMTΪ��'+  str(TradeContext.INRCHRCTAMT))
                
                #=====�跽����������====
                AfaLoggerFunc.tradeInfo('��̨��ȡ�� ��������__�跽����������')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('70','72','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(CUSCHRG) from rcc_wtrbka where TRCCO='3000102' and CHRGTYP='1' and BRSFLG='1' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sqlΪ��' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','ͨ��ͨ�ҵǼǲ�����ʧ��')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCHRDTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCHRDTAMT = 0.00
                    else:
                        TradeContext.INRCHRDTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCHRDTAMTΪ��'+  str(TradeContext.INRCHRDTAMT))
                
                #=====������ܽ��====
                AfaLoggerFunc.tradeInfo('��̨��ȡ�� ��������__�������')
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT + TradeContext.INRCHRCTAMT - TradeContext.INRDTAMT - TradeContext.INRCHRDTAMT
                AfaLoggerFunc.tradeInfo('INROFSTAMTΪ��'+ str(TradeContext.INROFSTAMT))
                
########################################################################################################################
            elif( record[i]['TRCCO'] == '3000102' and record[i]['BRSFLG'] == '0' ): 
                
                ##=====��̨��ȡ�� �������====
                AfaLoggerFunc.tradeInfo('��ʼ==��̨��ȡ�� �������==')
                
                 #=====�������ܽ��====   
                AfaLoggerFunc.tradeInfo('��̨��ȡ�� �������__�������ܽ��')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('42','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where TRCCO='3000102' and BRSFLG='0' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sqlΪ��' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','ͨ��ͨ�ҵǼǲ�����ʧ��')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCTAMT = 0.00
                    else:
                        TradeContext.INRCTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCTAMTΪ��'+  str(TradeContext.INRCTAMT))
                
                #=====�跽���ܽ��====
                AfaLoggerFunc.tradeInfo('��̨��ȡ�� �������__�跽���ܽ��')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('42','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where TRCCO='3000102' and BRSFLG='0' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sqlΪ��' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','ͨ��ͨ�ҵǼǲ�����ʧ��')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRDTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRDTAMT = 0.00
                    else:
                        TradeContext.INRDTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRDTAMTΪ��'+  str(TradeContext.INRDTAMT))    
                
                #=====��������������====
                AfaLoggerFunc.tradeInfo('��̨��ȡ�� �������__��������������')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('42','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(CUSCHRG) from rcc_wtrbka where TRCCO='3000102' and CHRGTYP='1' and BRSFLG='0' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sqlΪ��' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','ͨ��ͨ�ҵǼǲ�����ʧ��')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCHRCTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCHRCTAMT = 0.00
                    else:
                        TradeContext.INRCHRCTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCHRCTAMTΪ��'+  str(TradeContext.INRCHRCTAMT))
                
                #=====�跽����������====
                AfaLoggerFunc.tradeInfo('��̨��ȡ�� �������__�跽����������')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('42','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(CUSCHRG) from rcc_wtrbka where TRCCO='3000102' and CHRGTYP='1' and BRSFLG='0' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sqlΪ��' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','ͨ��ͨ�ҵǼǲ�����ʧ��')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCHRDTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCHRDTAMT = 0.00
                    else:
                        TradeContext.INRCHRDTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCHRDTAMTΪ��'+  str(TradeContext.INRCHRDTAMT))
                
                #=====������ܽ��====
                AfaLoggerFunc.tradeInfo('��̨��ȡ�� �������__�������')
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT + TradeContext.INRCHRCTAMT - TradeContext.INRDTAMT - TradeContext.INRCHRDTAMT
                AfaLoggerFunc.tradeInfo('INROFSTAMTΪ��'+ str(TradeContext.INROFSTAMT))
                     
########################################################################################################################                          
            elif( record[i]['TRCCO'] == '3000103' and record[i]['BRSFLG'] == '1' ):

                ##=====��̨����ת�� ��������====
                AfaLoggerFunc.tradeInfo('��ʼ==��̨����ת�� ��������==')
                
                #=====�������ܽ��====   
                AfaLoggerFunc.tradeInfo('��̨����ת�� ��������__�������ܽ��')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('70','72','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where TRCCO='3000103' and BRSFLG='1' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sqlΪ��' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','ͨ��ͨ�ҵǼǲ�����ʧ��')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCTAMT = 0.00
                    else:
                        TradeContext.INRCTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCTAMTΪ��'+  str(TradeContext.INRCTAMT))
                
                #=====�跽���ܽ��====
                AfaLoggerFunc.tradeInfo('��̨����ת�� ��������__�跽���ܽ��')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('70','72','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where TRCCO='3000103' and BRSFLG='1' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sqlΪ��' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','ͨ��ͨ�ҵǼǲ�����ʧ��')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRDTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRDTAMT = 0.00
                    else:
                        TradeContext.INRDTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRDTAMTΪ��'+  str(TradeContext.INRDTAMT))    
                
                #=====��������������====
                AfaLoggerFunc.tradeInfo('��̨����ת�� ��������__��������������')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('70','72','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(CUSCHRG) from rcc_wtrbka where TRCCO='3000103' and CHRGTYP='1' and BRSFLG='1' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sqlΪ��' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','ͨ��ͨ�ҵǼǲ�����ʧ��')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCHRCTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCHRCTAMT = 0.00
                    else:
                        TradeContext.INRCHRCTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCHRCTAMTΪ��'+  str(TradeContext.INRCHRCTAMT))
                
                #=====�跽����������====
                AfaLoggerFunc.tradeInfo('��̨����ת�� ��������__�跽����������')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('70','72','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(CUSCHRG) from rcc_wtrbka where TRCCO='3000103' and CHRGTYP='1' and BRSFLG='1' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sqlΪ��' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','ͨ��ͨ�ҵǼǲ�����ʧ��')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCHRDTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCHRDTAMT = 0.00
                    else:
                        TradeContext.INRCHRDTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCHRDTAMTΪ��'+  str(TradeContext.INRCHRDTAMT))
                
                #=====������ܽ��====
                AfaLoggerFunc.tradeInfo('��̨����ת�� ��������__�������')
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT + TradeContext.INRCHRCTAMT - TradeContext.INRDTAMT - TradeContext.INRCHRDTAMT
                AfaLoggerFunc.tradeInfo('INROFSTAMTΪ��'+ str(TradeContext.INROFSTAMT))  
                
########################################################################################################################
            elif( record[i]['TRCCO'] == '3000103' and record[i]['BRSFLG'] == '0' ): 
                
                ##=====��̨����ת�� �������====
                AfaLoggerFunc.tradeInfo('��ʼ==��̨����ת�� �������==')
                
                 #=====�������ܽ��====   
                AfaLoggerFunc.tradeInfo('��̨����ת�� �������__�������ܽ��')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('42','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where TRCCO='3000103' and BRSFLG='0' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sqlΪ��' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','ͨ��ͨ�ҵǼǲ�����ʧ��')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCTAMT = 0.00
                    else:
                        TradeContext.INRCTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCTAMTΪ��'+  str(TradeContext.INRCTAMT))
                
                #=====�跽���ܽ��====
                AfaLoggerFunc.tradeInfo('��̨����ת�� �������__�跽���ܽ��')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('42','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where TRCCO='3000103' and BRSFLG='0' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sqlΪ��' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','ͨ��ͨ�ҵǼǲ�����ʧ��')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRDTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRDTAMT = 0.00
                    else:
                        TradeContext.INRDTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRDTAMTΪ��'+  str(TradeContext.INRDTAMT))    
                
                #=====��������������====
                AfaLoggerFunc.tradeInfo('��̨����ת�� �������__��������������')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('42','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(CUSCHRG) from rcc_wtrbka where TRCCO='3000103' and CHRGTYP='1' and BRSFLG='0' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sqlΪ��' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','ͨ��ͨ�ҵǼǲ�����ʧ��')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCHRCTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCHRCTAMT = 0.00
                    else:
                        TradeContext.INRCHRCTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCHRCTAMTΪ��'+  str(TradeContext.INRCHRCTAMT))
                
                #=====�跽����������====
                AfaLoggerFunc.tradeInfo('��̨����ת�� �������__�跽����������')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('42','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(CUSCHRG) from rcc_wtrbka where TRCCO='3000103' and CHRGTYP='1' and BRSFLG='0' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sqlΪ��' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','ͨ��ͨ�ҵǼǲ�����ʧ��')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCHRDTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCHRDTAMT = 0.00
                    else:
                        TradeContext.INRCHRDTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCHRDTAMTΪ��'+  str(TradeContext.INRCHRDTAMT))  
                
                #=====������ܽ��====
                AfaLoggerFunc.tradeInfo('��̨����ת�� �������__�������')
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT + TradeContext.INRCHRCTAMT - TradeContext.INRDTAMT - TradeContext.INRCHRDTAMT
                AfaLoggerFunc.tradeInfo('INROFSTAMTΪ��'+ str(TradeContext.INROFSTAMT))
                        
########################################################################################################################
            elif( record[i]['TRCCO'] == '3000104' and record[i]['BRSFLG'] == '1' ):

                ##=====��̨��ȡ�� ��������====
                AfaLoggerFunc.tradeInfo('��ʼ==��̨��ȡ�� ��������==')
                
                #=====�������ܽ��====   
                AfaLoggerFunc.tradeInfo('��̨��ȡ�� ��������__�������ܽ��')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('70','72','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where TRCCO='3000104' and BRSFLG='1' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sqlΪ��' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','ͨ��ͨ�ҵǼǲ�����ʧ��')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCTAMT = 0.00
                    else:
                        TradeContext.INRCTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCTAMTΪ��'+  str(TradeContext.INRCTAMT))
                
                #=====�跽���ܽ��====
                AfaLoggerFunc.tradeInfo('��̨��ȡ�� ��������__�跽���ܽ��')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('70','72','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where TRCCO='3000104' and BRSFLG='1' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sqlΪ��' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','ͨ��ͨ�ҵǼǲ�����ʧ��')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRDTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRDTAMT = 0.00
                    else:
                        TradeContext.INRDTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRDTAMTΪ��'+  str(TradeContext.INRDTAMT))    
                
                #=====��������������====
                AfaLoggerFunc.tradeInfo('��̨��ȡ�� ��������__��������������')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('70','72','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(CUSCHRG) from rcc_wtrbka where TRCCO='3000104' and CHRGTYP='1' and BRSFLG='1' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sqlΪ��' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','ͨ��ͨ�ҵǼǲ�����ʧ��')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCHRCTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCHRCTAMT = 0.00
                    else:
                        TradeContext.INRCHRCTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCHRCTAMTΪ��'+  str(TradeContext.INRCHRCTAMT))
                
                #=====�跽����������====
                AfaLoggerFunc.tradeInfo('��̨��ȡ�� ��������__�跽����������')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('70','72','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(CUSCHRG) from rcc_wtrbka where TRCCO='3000104' and CHRGTYP='1' and BRSFLG='1' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sqlΪ��' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','ͨ��ͨ�ҵǼǲ�����ʧ��')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCHRDTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCHRDTAMT = 0.00
                    else:
                        TradeContext.INRCHRDTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCHRDTAMTΪ��'+  str(TradeContext.INRCHRDTAMT))
                
                #=====������ܽ��====
                AfaLoggerFunc.tradeInfo('��̨��ȡ�� ��������__�������')
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT + TradeContext.INRCHRCTAMT - TradeContext.INRDTAMT - TradeContext.INRCHRDTAMT
                AfaLoggerFunc.tradeInfo('INROFSTAMTΪ��'+ str(TradeContext.INROFSTAMT)) 
                
########################################################################################################################
            elif( record[i]['TRCCO'] == '3000104' and record[i]['BRSFLG'] == '0' ): 
                
                ##=====��̨��ȡ�� �������====
                AfaLoggerFunc.tradeInfo('��ʼ==��̨��ȡ�� �������==')
                
                 #=====�������ܽ��====   
                AfaLoggerFunc.tradeInfo('��̨��ȡ�� �������__�������ܽ��')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('42','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where TRCCO='3000104' and BRSFLG='0' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sqlΪ��' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','ͨ��ͨ�ҵǼǲ�����ʧ��')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCTAMT = 0.00
                    else:
                        TradeContext.INRCTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCTAMTΪ��'+  str(TradeContext.INRCTAMT))
                
                #=====�跽���ܽ��====
                AfaLoggerFunc.tradeInfo('��̨��ȡ�� �������__�跽���ܽ��')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('42','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where TRCCO='3000104' and BRSFLG='0' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sqlΪ��' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','ͨ��ͨ�ҵǼǲ�����ʧ��')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRDTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRDTAMT = 0.00
                    else:
                        TradeContext.INRDTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRDTAMTΪ��'+  str(TradeContext.INRDTAMT))    
                
                #=====��������������====
                AfaLoggerFunc.tradeInfo('��̨��ȡ�� �������__��������������')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('42','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(CUSCHRG) from rcc_wtrbka where TRCCO='3000104' and CHRGTYP='1' and BRSFLG='0' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sqlΪ��' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','ͨ��ͨ�ҵǼǲ�����ʧ��')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCHRCTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCHRCTAMT = 0.00
                    else:
                        TradeContext.INRCHRCTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCHRCTAMTΪ��'+  str(TradeContext.INRCHRCTAMT))
                
                #=====�跽����������====
                AfaLoggerFunc.tradeInfo('��̨��ȡ�� �������__�跽����������')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('42','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(CUSCHRG) from rcc_wtrbka where TRCCO='3000104' and CHRGTYP='1' and BRSFLG='0' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sqlΪ��' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','ͨ��ͨ�ҵǼǲ�����ʧ��')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCHRDTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCHRDTAMT = 0.00
                    else:
                        TradeContext.INRCHRDTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCHRDTAMTΪ��'+  str(TradeContext.INRCHRDTAMT)) 
                
                #=====������ܽ��====
                AfaLoggerFunc.tradeInfo('��̨��ȡ�� �������__�������')
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT + TradeContext.INRCHRCTAMT - TradeContext.INRDTAMT - TradeContext.INRCHRDTAMT
                AfaLoggerFunc.tradeInfo('INROFSTAMTΪ��'+ str(TradeContext.INROFSTAMT))
                                
########################################################################################################################
            elif( record[i]['TRCCO'] == '3000105' and record[i]['BRSFLG'] == '1' ):

                ##=====��̨����ת�� ��������====
                AfaLoggerFunc.tradeInfo('��ʼ==��̨����ת�� ��������==')
                
                #=====�������ܽ��====   
                AfaLoggerFunc.tradeInfo('��̨����ת�� ��������__�������ܽ��')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('70','72','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where TRCCO='3000105' and BRSFLG='1' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sqlΪ��' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','ͨ��ͨ�ҵǼǲ�����ʧ��')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCTAMT = 0.00
                    else:
                        TradeContext.INRCTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCTAMTΪ��'+  str(TradeContext.INRCTAMT))
                
                #=====�跽���ܽ��====
                AfaLoggerFunc.tradeInfo('��̨����ת�� ��������__�跽���ܽ��')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('70','72','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where TRCCO='3000105' and BRSFLG='1' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sqlΪ��' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','ͨ��ͨ�ҵǼǲ�����ʧ��')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRDTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRDTAMT = 0.00
                    else:
                        TradeContext.INRDTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRDTAMTΪ��'+  str(TradeContext.INRDTAMT))    
                
                #=====��������������====
                AfaLoggerFunc.tradeInfo('��̨����ת�� ��������__��������������')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('70','72','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(CUSCHRG) from rcc_wtrbka where TRCCO='3000105' and CHRGTYP='1' and BRSFLG='1' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sqlΪ��' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','ͨ��ͨ�ҵǼǲ�����ʧ��')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCHRCTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCHRCTAMT = 0.00
                    else:
                        TradeContext.INRCHRCTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCHRCTAMTΪ��'+  str(TradeContext.INRCHRCTAMT))
                
                #=====�跽����������====
                AfaLoggerFunc.tradeInfo('��̨����ת�� ��������__�跽����������')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('70','72','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(CUSCHRG) from rcc_wtrbka where TRCCO='3000105' and CHRGTYP='1' and BRSFLG='1' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sqlΪ��' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','ͨ��ͨ�ҵǼǲ�����ʧ��')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCHRDTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCHRDTAMT = 0.00
                    else:
                        TradeContext.INRCHRDTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCHRDTAMTΪ��'+  str(TradeContext.INRCHRDTAMT))
                
                #=====������ܽ��====
                AfaLoggerFunc.tradeInfo('��̨����ת�� ��������__�������')
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT + TradeContext.INRCHRCTAMT - TradeContext.INRDTAMT - TradeContext.INRCHRDTAMT
                AfaLoggerFunc.tradeInfo('INROFSTAMTΪ��'+ str(TradeContext.INROFSTAMT)) 
                
########################################################################################################################
            elif( record[i]['TRCCO'] == '3000105' and record[i]['BRSFLG'] == '0' ): 
                
                ##=====��̨����ת�� �������====
                AfaLoggerFunc.tradeInfo('��ʼ==��̨����ת�� �������==')
                
                 #=====�������ܽ��====   
                AfaLoggerFunc.tradeInfo('��̨����ת�� �������__�������ܽ��')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('42','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where TRCCO='3000105' and BRSFLG='0' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sqlΪ��' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','ͨ��ͨ�ҵǼǲ�����ʧ��')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCTAMT = 0.00
                    else:
                        TradeContext.INRCTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCTAMTΪ��'+  str(TradeContext.INRCTAMT))
                
                #=====�跽���ܽ��====
                AfaLoggerFunc.tradeInfo('��̨����ת�� �������__�跽���ܽ��')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('42','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where TRCCO='3000105' and BRSFLG='0' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sqlΪ��' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','ͨ��ͨ�ҵǼǲ�����ʧ��')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRDTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRDTAMT = 0.00
                    else:
                        TradeContext.INRDTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRDTAMTΪ��'+  str(TradeContext.INRDTAMT))    
                
                #=====��������������====
                AfaLoggerFunc.tradeInfo('��̨����ת�� �������__��������������')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('42','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(CUSCHRG) from rcc_wtrbka where TRCCO='3000105' and CHRGTYP='1' and BRSFLG='0' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sqlΪ��' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','ͨ��ͨ�ҵǼǲ�����ʧ��')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCHRCTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCHRCTAMT = 0.00
                    else:
                        TradeContext.INRCHRCTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCHRCTAMTΪ��'+  str(TradeContext.INRCHRCTAMT))
                
                #=====�跽����������====
                AfaLoggerFunc.tradeInfo('��̨����ת�� �������__�跽����������')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('42','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(CUSCHRG) from rcc_wtrbka where TRCCO='3000105' and CHRGTYP='1' and BRSFLG='0' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sqlΪ��' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','ͨ��ͨ�ҵǼǲ�����ʧ��')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCHRDTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCHRDTAMT = 0.00
                    else:
                        TradeContext.INRCHRDTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCHRDTAMTΪ��'+  str(TradeContext.INRCHRDTAMT)) 
                
                #=====������ܽ��====
                AfaLoggerFunc.tradeInfo('��̨����ת�� �������__�������')
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT + TradeContext.INRCHRCTAMT - TradeContext.INRDTAMT - TradeContext.INRCHRDTAMT
                AfaLoggerFunc.tradeInfo('INROFSTAMTΪ��'+ str(TradeContext.INROFSTAMT))
                   
########################################################################################################################
            elif( record[i]['TRCCO'] == '3000503' and record[i]['BRSFLG'] == '1' ):

                ##=====��̨���ȷ�� ��������====
                AfaLoggerFunc.tradeInfo('��ʼ==��̨���ȷ�� ��������==')
                
                #=====�������ܽ��====   
                AfaLoggerFunc.tradeInfo('��̨���ȷ�� ��������__�������ܽ��')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('70','72','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where TRCCO='3000503' and BRSFLG='1' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sqlΪ��' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','ͨ��ͨ�ҵǼǲ�����ʧ��')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCTAMT = 0.00
                    else:
                        TradeContext.INRCTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCTAMTΪ��'+  str(TradeContext.INRCTAMT))
                
                #=====�跽���ܽ��====
                AfaLoggerFunc.tradeInfo('��̨���ȷ�� ��������__�跽���ܽ��')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('70','72','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where TRCCO='3000503' and BRSFLG='1' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sqlΪ��' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','ͨ��ͨ�ҵǼǲ�����ʧ��')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRDTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRDTAMT = 0.00
                    else:
                        TradeContext.INRDTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRDTAMTΪ��'+  str(TradeContext.INRDTAMT))    
                
                #=====��������������====
                AfaLoggerFunc.tradeInfo('��̨���ȷ�� ��������__��������������')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('70','72','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(CUSCHRG) from rcc_wtrbka where TRCCO='3000503' and BRSFLG='1' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sqlΪ��' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','ͨ��ͨ�ҵǼǲ�����ʧ��')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCHRCTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCHRCTAMT = 0.00
                    else:
                        TradeContext.INRCHRCTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCHRCTAMTΪ��'+  str(TradeContext.INRCHRCTAMT))
                
                #=====�跽����������====
                AfaLoggerFunc.tradeInfo('��̨���ȷ�� ��������__�跽����������')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('70','72','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(CUSCHRG) from rcc_wtrbka where TRCCO='3000503' and BRSFLG='1' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sqlΪ��' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','ͨ��ͨ�ҵǼǲ�����ʧ��')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCHRDTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCHRDTAMT = 0.00
                    else:
                        TradeContext.INRCHRDTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCHRDTAMTΪ��'+  str(TradeContext.INRCHRDTAMT))
                
                #=====������ܽ��====
                AfaLoggerFunc.tradeInfo('��̨���ȷ�� ��������__�������')
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT + TradeContext.INRCHRCTAMT - TradeContext.INRDTAMT - TradeContext.INRCHRDTAMT
                AfaLoggerFunc.tradeInfo('INROFSTAMTΪ��'+ str(TradeContext.INROFSTAMT)) 
                
########################################################################################################################
            elif( record[i]['TRCCO'] == '3000503' and record[i]['BRSFLG'] == '0' ): 
                
                ##=====��̨���ȷ�� �������====
                AfaLoggerFunc.tradeInfo('��ʼ==��̨���ȷ�� �������==')
                
                 #=====�������ܽ��====   
                AfaLoggerFunc.tradeInfo('��̨���ȷ�� �������__�������ܽ��')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('42','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where TRCCO='3000503' and BRSFLG='0' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sqlΪ��' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','ͨ��ͨ�ҵǼǲ�����ʧ��')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCTAMT = 0.00
                    else:
                        TradeContext.INRCTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCTAMTΪ��'+  str(TradeContext.INRCTAMT))
                
                #=====�跽���ܽ��====
                AfaLoggerFunc.tradeInfo('��̨���ȷ�� �������__�跽���ܽ��')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('42','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where TRCCO='3000503' and BRSFLG='0' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sqlΪ��' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','ͨ��ͨ�ҵǼǲ�����ʧ��')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRDTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRDTAMT = 0.00
                    else:
                        TradeContext.INRDTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRDTAMTΪ��'+  str(TradeContext.INRDTAMT))    
                
                #=====��������������====
                AfaLoggerFunc.tradeInfo('��̨���ȷ�� �������__��������������')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('42','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(CUSCHRG) from rcc_wtrbka where TRCCO='3000503' and BRSFLG='0' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sqlΪ��' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','ͨ��ͨ�ҵǼǲ�����ʧ��')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCHRCTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCHRCTAMT = 0.00
                    else:
                        TradeContext.INRCHRCTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCHRCTAMTΪ��'+  str(TradeContext.INRCHRCTAMT))
                
                #=====�跽����������====
                AfaLoggerFunc.tradeInfo('��̨���ȷ�� �������__�跽����������')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('42','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(CUSCHRG) from rcc_wtrbka where TRCCO='3000503' and BRSFLG='0' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sqlΪ��' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','ͨ��ͨ�ҵǼǲ�����ʧ��')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCHRDTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCHRDTAMT = 0.00
                    else:
                        TradeContext.INRCHRDTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCHRDTAMTΪ��'+  str(TradeContext.INRCHRDTAMT)) 
                
                #=====������ܽ��====
                AfaLoggerFunc.tradeInfo('��̨���ȷ�� �������__�������')
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT + TradeContext.INRCHRCTAMT - TradeContext.INRDTAMT - TradeContext.INRCHRDTAMT
                AfaLoggerFunc.tradeInfo('INROFSTAMTΪ��'+ str(TradeContext.INROFSTAMT)) 
                   
########################################################################################################################
            elif( record[i]['TRCCO'] == '3000504' and record[i]['BRSFLG'] == '1' ):

                ##=====��̨���� ��������====
                AfaLoggerFunc.tradeInfo('��ʼ==��̨���� ��������==')
                
                #=====�������ܽ��====   
                AfaLoggerFunc.tradeInfo('��̨���� ��������__�������ܽ��')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where TRCCO='3000504' and BRSFLG='1' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sqlΪ��' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','ͨ��ͨ�ҵǼǲ�����ʧ��')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCTAMT = 0.00
                    else:
                        TradeContext.INRCTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCTAMTΪ��'+  str(TradeContext.INRCTAMT))
                
                #=====�跽���ܽ��====
                AfaLoggerFunc.tradeInfo('��̨���� ��������__�跽���ܽ��')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where TRCCO='3000504' and BRSFLG='1' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sqlΪ��' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','ͨ��ͨ�ҵǼǲ�����ʧ��')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRDTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRDTAMT = 0.00
                    else:
                        TradeContext.INRDTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRDTAMTΪ��'+  str(TradeContext.INRDTAMT))    
                
                #=====��������������====
                AfaLoggerFunc.tradeInfo('��̨���� ��������__��������������')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(CUSCHRG) from rcc_wtrbka where TRCCO='3000504' and BRSFLG='1' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sqlΪ��' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','ͨ��ͨ�ҵǼǲ�����ʧ��')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCHRCTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCHRCTAMT = 0.00
                    else:
                        TradeContext.INRCHRCTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCHRCTAMTΪ��'+  str(TradeContext.INRCHRCTAMT))
                
                #=====�跽����������====
                AfaLoggerFunc.tradeInfo('��̨���� ��������__�跽����������')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(CUSCHRG) from rcc_wtrbka where TRCCO='3000504' and BRSFLG='1' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sqlΪ��' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','ͨ��ͨ�ҵǼǲ�����ʧ��')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCHRDTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCHRDTAMT = 0.00
                    else:
                        TradeContext.INRCHRDTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCHRDTAMTΪ��'+  str(TradeContext.INRCHRDTAMT))
                
                #=====������ܽ��====
                AfaLoggerFunc.tradeInfo('��̨���� ��������__�������')
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT + TradeContext.INRCHRCTAMT - TradeContext.INRDTAMT - TradeContext.INRCHRDTAMT
                AfaLoggerFunc.tradeInfo('INROFSTAMTΪ��'+ str(TradeContext.INROFSTAMT))
                
########################################################################################################################
            elif( record[i]['TRCCO'] == '3000504' and record[i]['BRSFLG'] == '0' ): 
                
                ##=====��̨���� �������====
                AfaLoggerFunc.tradeInfo('��ʼ==��̨���� �������==')
                
                 #=====�������ܽ��====   
                AfaLoggerFunc.tradeInfo('��̨���� �������__�������ܽ��')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where TRCCO='3000504' and BRSFLG='0' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sqlΪ��' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','ͨ��ͨ�ҵǼǲ�����ʧ��')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCTAMT = 0.00
                    else:
                        TradeContext.INRCTAMT = wtrbka_list[0][0]
                        
                AfaLoggerFunc.tradeInfo('INRCTAMTΪ��'+  str(TradeContext.INRCTAMT))
                
                #=====�跽���ܽ��====
                AfaLoggerFunc.tradeInfo('��̨���� �������__�跽���ܽ��')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where TRCCO='3000504' and BRSFLG='0' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sqlΪ��' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','ͨ��ͨ�ҵǼǲ�����ʧ��')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRDTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRDTAMT = 0.00
                    else:
                        TradeContext.INRDTAMT = wtrbka_list[0][0]
                
                AfaLoggerFunc.tradeInfo('INRDTAMTΪ��'+  str(TradeContext.INRDTAMT))    
                
                #=====��������������====
                AfaLoggerFunc.tradeInfo('��̨���� �������__��������������')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(CUSCHRG) from rcc_wtrbka where TRCCO='3000504' and BRSFLG='0' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sqlΪ��' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','ͨ��ͨ�ҵǼǲ�����ʧ��')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCHRCTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCHRCTAMT = 0.00
                    else:
                        TradeContext.INRCHRCTAMT = wtrbka_list[0][0]
                
                AfaLoggerFunc.tradeInfo('INRCHRCTAMTΪ��'+  str(TradeContext.INRCHRCTAMT))
                
                #=====�跽����������====
                AfaLoggerFunc.tradeInfo('��̨���� �������__�跽����������')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(CUSCHRG) from rcc_wtrbka where TRCCO='3000504' and BRSFLG='0' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sqlΪ��' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','ͨ��ͨ�ҵǼǲ�����ʧ��')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCHRDTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCHRDTAMT = 0.00
                    else:
                        TradeContext.INRCHRDTAMT = wtrbka_list[0][0]
                
                AfaLoggerFunc.tradeInfo('INRCHRDTAMTΪ��'+  str(TradeContext.INRCHRDTAMT)) 
                
                #=====������ܽ��====
                AfaLoggerFunc.tradeInfo('��̨���� �������__�������')
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT + TradeContext.INRCHRCTAMT - TradeContext.INRDTAMT - TradeContext.INRCHRDTAMT
                AfaLoggerFunc.tradeInfo('INROFSTAMTΪ��'+ str(TradeContext.INROFSTAMT))
                
########################################################################################################################
            elif( record[i]['TRCCO'] == '3000505' and record[i]['BRSFLG'] == '1' ):
                
                ##=====��̨�������� ��������====
                AfaLoggerFunc.tradeInfo('��ʼ==��̨�������� ��������==')
                
                #=====�������ܽ��====
                TradeContext.INRCTAMT = 0.00
                AfaLoggerFunc.tradeInfo('INRCTAMTΪ��'+  str(TradeContext.INRCTAMT))
                
                #=====�跽���ܽ��====
                TradeContext.INRDTAMT = 0.00
                AfaLoggerFunc.tradeInfo('INRDTAMTΪ��'+  str(TradeContext.INRDTAMT))
                
                #=====��������������====
                TradeContext.INRCHRCTAMT = 0.00
                AfaLoggerFunc.tradeInfo('INRCHRCTAMTΪ��'+  str(TradeContext.INRCHRCTAMT))
                
                #=====�跽����������====
                TradeContext.INRCHRDTAMT = 0.00
                AfaLoggerFunc.tradeInfo('INRCHRDTAMTΪ��'+  str(TradeContext.INRCHRDTAMT))
                
                #=====������ܽ��====
                AfaLoggerFunc.tradeInfo('��̨�������� ��������__�������')
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT + TradeContext.INRCHRCTAMT - TradeContext.INRDTAMT - TradeContext.INRCHRDTAMT
                AfaLoggerFunc.tradeInfo('INROFSTAMTΪ��'+ str(TradeContext.INROFSTAMT))
                
########################################################################################################################
            elif( record[i]['TRCCO'] == '3000505' and record[i]['BRSFLG'] == '0' ):
                
                ##=====��̨�������� �������====
                AfaLoggerFunc.tradeInfo('��ʼ==��̨�������� �������==')
                
                #=====�������ܽ��====
                TradeContext.INRCTAMT = 0.00
                AfaLoggerFunc.tradeInfo('INRCTAMTΪ��'+  str(TradeContext.INRCTAMT))
                
                #=====�跽���ܽ��====
                TradeContext.INRDTAMT = 0.00
                AfaLoggerFunc.tradeInfo('INRDTAMTΪ��'+  str(TradeContext.INRDTAMT))
                
                #=====��������������====
                TradeContext.INRCHRCTAMT = 0.00
                AfaLoggerFunc.tradeInfo('INRCHRCTAMTΪ��'+  str(TradeContext.INRCHRCTAMT))
                
                #=====�跽����������====
                TradeContext.INRCHRDTAMT = 0.00
                AfaLoggerFunc.tradeInfo('INRCHRDTAMTΪ��'+  str(TradeContext.INRCHRDTAMT))
                
                #=====������ܽ��====
                AfaLoggerFunc.tradeInfo('��̨�������� �������__�������')
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT + TradeContext.INRCHRCTAMT - TradeContext.INRDTAMT - TradeContext.INRCHRDTAMT
                AfaLoggerFunc.tradeInfo('INROFSTAMTΪ��'+ str(TradeContext.INROFSTAMT))
                   
########################################################################################################################
########################################################################################################################
            
            #====��ͨ��ͨ��ҵ��Ǽǲ�ͳ������ͨ��ͨ��ҵ���ܱ���====
            wtrbka_sql = "select count(*) from rcc_wtrbka where NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
            
            #=====�ж�BRSFLG====
            if str(record[i]['BRSFLG']) != '2':
                wtrbka_sql = wtrbka_sql + " and BRSFLG='" + record[i]['BRSFLG'] + "'"
            
            #=====�ж�TRCCO====
            if str(record[i]['TRCCO']) != '0000000':
                wtrbka_sql = wtrbka_sql + " and TRCCO ='" + record[i]['TRCCO'] + "'"

            #=====���������˸�ֵ��ͬ�Ľ���״̬====
            if record[i]['BRSFLG'] == PL_BRSFLG_SND:
                wtrbka_sql = wtrbka_sql + " and bspsqn in (select bspsqn from rcc_spbsta where bcstat in ('42','81')"
                wtrbka_sql = wtrbka_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "')"
            elif record[i]['BRSFLG'] == PL_BRSFLG_RCV:
                wtrbka_sql = wtrbka_sql + " and bspsqn in (select bspsqn from rcc_spbsta where bcstat in ('70','72','81')"
                wtrbka_sql = wtrbka_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "')"
            else:
                wtrbka_sql = wtrbka_sql + " and bspsqn in (select bspsqn from rcc_spbsta where bcstat in ('70','72','42','81')"
                wtrbka_sql = wtrbka_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "')"
            AfaLoggerFunc.tradeDebug( 'sql==' + wtrbka_sql ) 
            
            #=====��ѯ���ݿ�====
            count = AfaDBFunc.SelectSql(wtrbka_sql)
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
            filecont = filecont + record[i]['NCCWKDAT']       + "|" 
            filecont = filecont + record[i]['TRCCO']          + "|"
            filecont = filecont + record[i]['BRSFLG']         + "|" 
            filecont = filecont + record[i]['TRCNAM']         + "|"
            filecont = filecont + record[i]['TRCRSNM']        + "|" 
            filecont = filecont + str(record[i]['TCNT'])      + "|" + str(TradeContext.INRTCNT)       + "|"                               
            filecont = filecont + str(record[i]['CTAMT'])     + "|" + str(TradeContext.INRCTAMT)      + "|"
            filecont = filecont + str(record[i]['DTAMT'])     + "|" + str(TradeContext.INRDTAMT)      + "|"
            filecont = filecont + str(record[i]['CHRCTAMT'])  + "|" + str(TradeContext.INRCHRCTAMT)   + "|"
            filecont = filecont + str(record[i]['CHRDTAMT'])  + "|" + str(TradeContext.INRCHRDTAMT)   + "|"
            filecont = filecont + str(record[i]['OFSTAMT'])   + "|" + str(TradeContext.INROFSTAMT)    + "|\n"
            f.write(filecont)

        #=====�ر��ļ�====
        f.close()

    #=====��ѯ�ܼ�¼��====
    allcount=rccpsDBTrcc_tddzhz.count(sql)     #�õ��ܼ�¼����
    if(allcount==None):
        return AfaFlowControl.ExitThisFlow('D000','���ݿ����ʧ��')
    else:
        TradeContext.RECALLCOUNT = str(allcount)

    TradeContext.PBDAFILE = filename            #�ļ���
    TradeContext.RECCOUNT = str(len(record))    #��ѯ����
    TradeContext.errorMsg="��ѯ�ɹ�"
    TradeContext.errorCode="0000"
    
    AfaLoggerFunc.tradeInfo(  '***ũ����ϵͳ������.���������(1.���ز���)ͨ��ͨ�һ��ܺ˶Բ�ѯ[TRC001_8568] �˳�***'  )
    return True
