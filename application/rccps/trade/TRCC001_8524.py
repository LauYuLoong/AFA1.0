# -*- coding: gbk -*-
##################################################################
#   ũ����.��ѯ��ӡҵ��.���ҵ��������ϸ��ѯ
#=================================================================
#   �����ļ�:   TRCC001_8524.py
#   �޸�ʱ��:   2008-06-06
##################################################################
import rccpsDBTrcc_trcbka,TradeContext,AfaLoggerFunc,AfaFlowControl,AfaUtilTools,rccpsDBFunc,rccpsDBTrcc_spbsta,rccpsState
from types import *
from rccpsConst import *
import os

def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ: ����.�������������[RCC001_8524]����***' )
    
    #=====�ж�����ӿ�ֵ�Ƿ����====
    if( not TradeContext.existVariable( "STRDAT" ) ):
        return AfaFlowControl.ExitThisFlow('A099','��ʼ����[STRDAT]������' )
    if( not TradeContext.existVariable( "ENDDAT" ) ):
        return AfaFlowControl.ExitThisFlow('A099','��ֹ����[ENDDAT]������' )
    if( not TradeContext.existVariable( "BRSFLG" ) ):
        return AfaFlowControl.ExitThisFlow('A099','������־[BRSFLG]������' )
        
    #=====��֯��ѯsql���====
    AfaLoggerFunc.tradeInfo( "��֯��ѯ���")


    if(TradeContext.BESBNO == "3400008889" and TradeContext.RCVBNKCO != ""):    
        sql= "BJEDTE >='"+TradeContext.STRDAT+"' and BJEDTE <='"
        sql= sql + TradeContext.ENDDAT + "'"
    else:
        sql= "BESBNO='" + TradeContext.BESBNO + "' " 
        sql= sql + "and BJEDTE >='"+TradeContext.STRDAT+"' and BJEDTE <='"
        sql= sql + TradeContext.ENDDAT + "'"
    
    if(TradeContext.BRSFLG != ""):
        sql= sql + " and BRSFLG='"+TradeContext.BRSFLG+"'"
        
    AfaLoggerFunc.tradeDebug( "1.sql=" + sql )
    #=====�ж�������ѯ�����Ƿ����====
    if(TradeContext.OPRNO != ""):               #ҵ������
        sql = sql + " and OPRNO='" + TradeContext.OPRNO + "'"
    if(TradeContext.OPRATTNO != ""):            #ҵ������
        sql = sql + " and OPRATTNO='" + TradeContext.OPRATTNO + "'"
    if(TradeContext.BSPSQN != ""):              #�������
        sql = sql + " and BSPSQN='" + TradeContext.BSPSQN + "'"
    if(float(TradeContext.OCCAMT) != 0.0):      #���׽��
        sql = sql + " and OCCAMT=" + TradeContext.OCCAMT
    if(TradeContext.RCVBNKCO != ""):            #�����к�
        sql = sql + " and RCVBNKCO='" + TradeContext.RCVBNKCO + "'"
    if(TradeContext.BCSTAT != ""):              #����״̬
        if(TradeContext.BDWFLG!= ""):           #��ת��־
            sql = sql + " and exists (select * from RCC_SPBSTA where "
            sql = sql + " BJEDTE = RCC_TRCBKA.BJEDTE"
            sql = sql + " and BSPSQN = RCC_TRCBKA.BSPSQN"
            sql = sql + " and BCSTAT = '" + TradeContext.BCSTAT + "'"
            sql = sql + " and BDWFLG='" + TradeContext.BDWFLG + "')"
        else:
            sql = sql + " and exists (select * from RCC_SPBSTA tab2 where "
            sql = sql + " BJEDTE = RCC_TRCBKA.BJEDTE"
            sql = sql + " and BSPSQN = RCC_TRCBKA.BSPSQN"
            sql = sql + " and BCSTAT = '" + TradeContext.BCSTAT + "')"
            
    AfaLoggerFunc.tradeDebug( "sql=" + sql )
    
    #=====��ʼ��ѯ�ܱ���====
    TradeContext.RECALLCOUNT=str(rccpsDBTrcc_trcbka.count(sql))     #�ܼ�¼����
    
    AfaLoggerFunc.tradeDebug( '>>>�ܱ���=' + TradeContext.RECALLCOUNT )
    
    #=====��ѯ���ݿ�====    
    ordersql=" order by BJEDTE DESC,BSPSQN DESC"   #��֯��������������
    AfaLoggerFunc.tradeInfo("��ѯ����Ϊ��"+sql)
    
    records=rccpsDBTrcc_trcbka.selectm(TradeContext.RECSTRNO,10,sql,ordersql)
    
    if(records==None):
        return AfaFlowControl.ExitThisFlow('A099','��ѯʧ��' )       
    elif(len(records)==0):
        return AfaFlowControl.ExitThisFlow('A099','û�в��ҵ���¼' )    
    else:        		
        try:
            #=====���ļ�====	
            AfaLoggerFunc.tradeInfo(">>>�����ļ�")
            filename="rccps_"+TradeContext.BETELR+"_"+AfaUtilTools.GetHostDate()+"_"+TradeContext.TransCode
            fpath=os.environ["AFAP_HOME"]+"/tmp/"

            f=open(fpath+filename,"w")
	        
            #=====PL_HDOPRNO_TH 09 �˻�====
            if(TradeContext.OPRNO==PL_HDOPRNO_TH):	
                AfaLoggerFunc.tradeInfo(">>>�����˻㴦��")	
	            #=====�õ��ļ����ݣ������ļ�====
                for i in range(0,len(records)):
                    #=====�õ�ҵ��״̬BCSTAT====
                    state_dict={}
                    ret=rccpsState.getTransStateCur(records[i]['BJEDTE'],records[i]['BSPSQN'],state_dict)
                    if(ret==False):
                        return AfaFlowControl.ExitThisFlow( 'S999', '��ǰ״̬�Ǽǲ����޴˽���״̬' )
                    #=====д�ļ�����====
                    filecontext = records[i]['BJEDTE']        + "|" \
                                + records[i]['BSPSQN']        + "|" \
                                + records[i]['BRSFLG']        + "|" \
                                + records[i]['BESBNO']        + "|" \
                                + records[i]['BEACSB']        + "|" \
                                + records[i]['BETELR']        + "|" \
                                + records[i]['BEAUUS']        + "|" \
                                + records[i]['TRCCO']         + "|" \
                                + records[i]['OPRNO']         + "|" \
                                + records[i]['OPRATTNO']      + "|" \
                                + records[i]['TRCDAT']        + "|" \
                                + records[i]['TRCNO']         + "|" \
                                + records[i]['SNDBNKCO']      + "|" \
                                + records[i]['SNDBNKNM']      + "|" \
                                + records[i]['RCVBNKCO']      + "|" \
                                + records[i]['RCVBNKNM']      + "|" \
                                + records[i]['CUR']           + "|" \
                                + str(records[i]['OCCAMT'])   + "|" \
                                + records[i]['PYRACC']        + "|" \
                                + records[i]['PYRNAM']        + "|" \
                                + records[i]['PYRADDR']       + "|" \
                                + records[i]['PYEACC']        + "|" \
                                + records[i]['PYENAM']        + "|" \
                                + records[i]['PYEADDR']       + "|" \
                                + records[i]['USE']           + "|" \
                                + records[i]['REMARK']        + "|" \
                                + records[i]['BILTYP']        + "|" \
                                + records[i]['BILDAT']        + "|" \
                                + records[i]['BILNO']         + "|" \
                                + str(records[i]['COMAMT'])   + "|" \
                                + str(records[i]['OVPAYAMT']) + "|" \
                                + str(records[i]['CPSAMT'])   + "|" \
                                + str(records[i]['RFUAMT'])   + "|" \
                                + records[i]['CERTTYPE']      + "|" \
                                + records[i]['CERTNO']        + "|" \
                                + records[i]['ORTRCCO']       + "|" \
                                + records[i]['ORTRCDAT']      + "|" \
                                + records[i]['ORTRCNO']       + "|" \
                                + records[i]['ORSNDBNK']      + "|" \
                                + records[i]['ORRCVBNK']      + "|" \
                                + records[i]['PYRACC']        + "|" \
                                + records[i]['PYRNAM']        + "|" \
                                + records[i]['PYEACC']        + "|" \
                                + records[i]['PYENAM']        + "|" \
                                + records[i]['STRINFO']       + "|" \
                                + state_dict['BCSTAT']        + "|" \
                                + state_dict['BDWFLG']        + "|"	\
                                + records[i]['BOJEDT']        + "|" \
                                + records[i]['BOSPSQ']        + "|" \
                                + records[i]['CHRGTYP']       + "|" \
                                + str(records[i]['LOCCUSCHRG'])    + "|" 
                    f.write(filecontext+"\n")                    
            #=====���˻�====
            else:
                AfaLoggerFunc.tradeInfo(">>>������˻㴦��")
                for i in range(len(records)):
                    #=====�õ�ҵ��״̬BCSTAT====
                    state_dict={}
                    ret=rccpsState.getTransStateCur(records[i]['BJEDTE'],records[i]['BSPSQN'],state_dict)
                    if(state_dict==False):
                        return AfaFlowControl.ExitThisFlow( 'S999', '��ǰ״̬�Ǽǲ����޴˽���״̬' )
                    #=====д�ļ�����====
                    filecontext = records[i]['BJEDTE']   +    "|" \
                                + records[i]['BSPSQN']   +    "|" \
                                + records[i]['BRSFLG']   +    "|" \
                                + records[i]['BESBNO']   +    "|" \
                                + records[i]['BEACSB']   +    "|" \
                                + records[i]['BETELR']   +    "|" \
                                + records[i]['BEAUUS']   +    "|" \
                                + records[i]['TRCCO']    +    "|" \
                                + records[i]['OPRNO']    +    "|" \
                                + records[i]['OPRATTNO'] +    "|" \
                                + records[i]['TRCDAT']   +    "|" \
                                + records[i]['TRCNO']    +    "|" \
                                + records[i]['SNDBNKCO'] +    "|" \
                                + records[i]['SNDBNKNM'] +    "|" \
                                + records[i]['RCVBNKCO'] +    "|" \
                                + records[i]['RCVBNKNM'] +    "|" \
                                + records[i]['CUR']      +    "|" \
                                + str(records[i]['OCCAMT'])+  "|" \
                                + records[i]['PYRACC']   +    "|" \
                                + records[i]['PYRNAM']   +    "|" \
                                + records[i]['PYRADDR']  +    "|" \
                                + records[i]['PYEACC']   +    "|" \
                                + records[i]['PYENAM']   +    "|" \
                                + records[i]['PYEADDR']  +    "|" \
                                + records[i]['USE']      +    "|" \
                                + records[i]['REMARK']   +    "|" \
                                + records[i]['BILTYP']   +    "|" \
                                + records[i]['BILDAT']   +    "|" \
                                + records[i]['BILNO']    +    "|" \
                                + str(records[i]['COMAMT'])+  "|" \
                                + str(records[i]['OVPAYAMT'])+"|" \
                                + str(records[i]['CPSAMT'])+  "|" \
                                + str(records[i]['RFUAMT'])+  "|" \
                                + records[i]['CERTTYPE']   +  "|" \
                                + records[i]['CERTNO']     +  "|" \
                                + records[i]['ORTRCCO']    +  "|" \
                                + records[i]['ORTRCDAT']   +  "|" \
                                + records[i]['ORTRCNO']    +  "|" \
                                + records[i]['ORSNDBNK']   +  "|" \
                                + records[i]['ORRCVBNK']   +  "|" \
                                + "" + "|" + "" + "|" + "" +  "|" + "" + "|" \
                                + records[i]['STRINFO']    +  "|" \
                                + state_dict['BCSTAT']     +  "|" \
                                + state_dict['BDWFLG']     +  "|" \
                                + records[i]['BOJEDT']     +  "|" \
                                + records[i]['BOSPSQ']     +  "|" \
                                + records[i]['CHRGTYP']    +  "|" \
                                + str(records[i]['LOCCUSCHRG']) +  "|" 
                    f.write(filecontext+"\n")
                    
                f.close()
                AfaLoggerFunc.tradeInfo(">>>�����ļ�����")
	    
        except Exception, e:
            #=====�ر��ļ�====
            f.close()
            return AfaFlowControl.ExitThisFlow('A099','д�뷵���ļ�ʧ��' )    
	    
        #=====����ӿڸ�ֵ====
        TradeContext.RECCOUNT=str(len(records))     #��ѯ����
        TradeContext.errorCode="0000"               #������
        TradeContext.errorMsg="�ɹ�"                #������Ϣ
        TradeContext.PBDAFILE=filename              #�ļ���
        
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ: ����.�������������[RCC001_8524]�˳�***' )
    return True
