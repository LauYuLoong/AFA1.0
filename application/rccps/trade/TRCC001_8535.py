# -*- coding: gbk -*-
################################################################################
#   ũ����ϵͳ������.���������ģ��(1.���ز���).��������
#===============================================================================
#   �����ļ�:   TRCC001_8535.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  ������
#   �޸�ʱ��:   2008-07-11
#   ��    �ܣ�  ҵ���嵥��ѯ��ӡ
#               01-�������             02-�������
#               03-���л�Ʊ             04-�⸶����
#               05-�˻�����             06-�˻�����
#               07-��ѯ��               08-�鸴��
#               09-Ʊ�ݲ�ѯ��           10-Ʊ�ݲ鸴��
#               11-��Ʊ��ѯ��           12-��Ʊ�鸴��
#               13-���ɸ�ʽ��           14-ͨ��ͨ������
#               15-ͨ��ͨ������
###############################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc
import rccpsDBFunc,rccpsDBTrcc_trcbka,rccpsDBTrcc_subbra,rccpsDBTrcc_spbsta,rccpsDBTrcc_bilbka
import rccpsDBTrcc_hdcbka,rccpsDBTrcc_pjcbka,rccpsDBTrcc_bilinf,rccpsDBTrcc_hpcbka,rccpsDBTrcc_wtrbka
from types import *
from rccpsConst import *

#=====================���Ի�����(���ز���)======================================
def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.�������������[TRC001_8535]����***' )
    
    #=====�ж�ҵ�������Ƿ����====
    if not (TradeContext.existVariable( "TRCCO" ) and len(TradeContext.TRCCO) != 0):
        return AfaFlowControl.ExitThisFlow('S999','ҵ������[TRCCO]�����ڻ�Ϊ��')

    #=====ȡ����ʱ��====
    TradeContext.BJEDTE = AfaUtilTools.GetSysDate( )

    #=====ͨ�������Ų�ѯ��������====
    ret    = {}
    subbra = {'BESBNO':TradeContext.BESBNO}
    
    ret = rccpsDBTrcc_subbra.selectu(subbra)
    if ret == None:
        return AfaFlowControl.ExitThisFlow('S999','���ݿ����ʧ��')
    if len(ret) <= 0:
        if TradeContext.TRCCO not in ('14','15'):
            return AfaFlowControl.ExitThisFlow('S999','���ݿ����޻�����['+TradeContext.BESBNO+']')
        else:
            TradeContext.BESBNM = TradeContext.BESBNO
    else:
        TradeContext.BESBNM  = ret['BESBNM'] 

    #=====�ж�ҵ������  01  �������====
    if TradeContext.TRCCO == '01':
        AfaLoggerFunc.tradeInfo('>>>��������嵥��ӡ����')
        
        #=====��֯��ѯ���====
        sql = "BJEDTE >= '" + TradeContext.STRDAT + "'"
        sql = sql + " AND BJEDTE <= '" + TradeContext.ENDDAT + "'"
        sql = sql + " AND BESBNO =  '" + TradeContext.BESBNO + "'"
        sql = sql + " AND BRSFLG = '"  + PL_BRSFLG_SND + "'"
        sql = sql + " AND TRCCO IN ('2000001','2000002','2000003','2000009') "

        #=====��ʲ�ѯ====
        ordersql = "ORDER BY TRCCO ASC"
        records = rccpsDBTrcc_trcbka.selectm(1,0,sql,ordersql)
        
        if records == None:
            return AfaFlowControl.ExitThisFlow('A099','���ݿ����ʧ��' )
        if len(records) == 0:
            return AfaFlowControl.ExitThisFlow('A099','������������¼' )

        #=====��ʼ��֯�����ļ�====
        filename="rccps_"+TradeContext.BETELR+"_"+AfaUtilTools.GetSysDate()+"_"+TradeContext.TransCode
        try:
            fpath=os.environ["AFAP_HOME"]+"/tmp/"
            f=open(fpath+filename,"w")
        except IOError:
            return AfaFlowControl.ExitThisFlow('S999','���ļ�ʧ��') 

        #=====д�ļ�ͷ====
        filecontext = "\n\n\n"
        filecontext = filecontext + "                                                  " + TradeContext.BESBNM + "���ӻ�������嵥\n" 
        filecontext = filecontext + "��ֹ���ڣ�" + TradeContext.STRDAT + "~" + TradeContext.ENDDAT + "\n"
        filecontext = filecontext + "��� ҵ�����ࡡ�������  ���������� �������к� �������кš����      �������˺š�������������������"
        filecontext = filecontext + "�տ����˺š�������������������ҵ��״̬\n"
        filecontext = filecontext + "=================================================================================================================\n"
        f.write(filecontext+"\n")

        #=====ѭ����֯�ļ�����====
        for i in range(0,len(records)):
            #=====ͨ��������ź�����ȡ״̬====
            bcstat      = {}
            bcstat_dict = {'BJEDTE':records[i]['BJEDTE'],'BSPSQN':records[i]['BSPSQN']}
            bcstat     = rccpsDBTrcc_spbsta.selectu(bcstat_dict)
            if bcstat == None:
                return AfaFlowControl.ExitThisFlow('S999','���ݿ����ʧ��')
            if len(bcstat) <= 0:
                return AfaFlowControl.ExitThisFlow('S999','ͨ���������ȡҵ��״̬ʧ��')
                 
            #=====д�ļ�====
            filecontext=str(i+1).ljust(4) +  records[i]['TRCCO'].ljust(10) + records[i]['BSPSQN'].ljust(13) \
                       + records[i]['BJEDTE'].ljust(9)    + records[i]['SNDBNKCO'].ljust(11)      \
                       + records[i]['RCVBNKCO'].ljust(11) + str(records[i]['OCCAMT']).ljust(11)   \
                       + records[i]['PYRACC'].ljust(30)   + records[i]['PYEACC'].ljust(34)        \
                       + bcstat['BCSTAT']
            f.write(filecontext+"\n")

        #=====��Ӵ�ӡ���ڵ�====       
        filecontext = "-----------------------------------------------------------------------------------------------------------------\n"
        filecontext = filecontext +  "    ��ӡ����:" + TradeContext.BJEDTE + "                           ��Ȩ���������������������������ˣ�  \n"
        f.write(filecontext)

        f.close()
        AfaLoggerFunc.tradeInfo(">>>�����ļ�����")
    #=====02 �������====
    elif TradeContext.TRCCO == '02':
        AfaLoggerFunc.tradeInfo('>>>��������嵥��ӡ����')
        
        #=====��֯��ѯ���====
        sql = "BJEDTE >= '" + TradeContext.STRDAT + "'"
        sql = sql + " AND BJEDTE <= '" + TradeContext.ENDDAT + "'"
        sql = sql + " AND BESBNO =  '" + TradeContext.BESBNO + "'"
        sql = sql + " AND BRSFLG = '"  + PL_BRSFLG_RCV + "'"
        sql = sql + " AND TRCCO IN ('2000001','2000002','2000003','2000009')"

        #=====��ʲ�ѯ====
        ordersql = "ORDER BY TRCCO ASC"
        records = rccpsDBTrcc_trcbka.selectm(1,0,sql,ordersql)
        if records == None:
            return AfaFlowControl.ExitThisFlow('A099','���ݿ����ʧ��' )
        if len(records) == 0:
            return AfaFlowControl.ExitThisFlow('A099','������������¼' )

        #=====��ʼ��֯�����ļ�====
        filename="rccps_"+TradeContext.BETELR+"_"+AfaUtilTools.GetSysDate()+"_"+TradeContext.TransCode
        try:
            fpath=os.environ["AFAP_HOME"]+"/tmp/"
            f=open(fpath+filename,"w")
        except IOError:
            return AfaFlowControl.ExitThisFlow('S999','���ļ�ʧ��') 

        #=====д�ļ�ͷ====
        filecontext = "\n\n\n"
        filecontext = filecontext + "                                                  " + TradeContext.BESBNM + "���ӻ�������嵥\n" 
        filecontext = filecontext + "��ֹ���ڣ�" + TradeContext.STRDAT + "~" + TradeContext.ENDDAT + "\n"
        filecontext = filecontext + "��� ��Ʊ��𡡱������  ����Ʊ���� ��Ʊ����  ���      �������˺š�������������������"
        filecontext = filecontext + "�տ����˺š�������������������ҵ��״̬\n"
        filecontext = filecontext + "=================================================================================================================\n"
        f.write(filecontext+"\n")

        #=====ѭ����֯�ļ�����====
        for i in range(0,len(records)):
            #=====ͨ��������ź�����ȡ״̬====
            bcstat      = {}
            bcstat_dict = {'BJEDTE':records[i]['BJEDTE'],'BSPSQN':records[i]['BSPSQN']}
            bcstat     = rccpsDBTrcc_spbsta.selectu(bcstat_dict)
            if bcstat == None:
                return AfaFlowControl.ExitThisFlow('S999','���ݿ����ʧ��')
            if len(bcstat) <= 0:
                return AfaFlowControl.ExitThisFlow('S999','ͨ���������ȡҵ��״̬ʧ��')
                 
            #=====д�ļ�====
            filecontext=str(i+1).ljust(4) +  records[i]['TRCCO'].ljust(10) + records[i]['BSPSQN'].ljust(13) \
                       + records[i]['BJEDTE'].ljust(9)    + records[i]['SNDBNKCO'].ljust(11)      \
                       + records[i]['RCVBNKCO'].ljust(11) + str(records[i]['OCCAMT']).ljust(11)   \
                       + records[i]['PYRACC'].ljust(30)   + records[i]['PYEACC'].ljust(34)        \
                       + bcstat['BCSTAT']
            f.write(filecontext+"\n")

        #=====��Ӵ�ӡ���ڵ�====       
        filecontext = "-----------------------------------------------------------------------------------------------------------------\n"
        filecontext = filecontext +  "    ��ӡ����:" + TradeContext.BJEDTE + "                           ��Ȩ���������������������������ˣ�  \n"
        f.write(filecontext)

        f.close()
        AfaLoggerFunc.tradeInfo(">>>�����ļ�����")
    #====03 ���л�Ʊǩ��====
    elif TradeContext.TRCCO == '03':
        AfaLoggerFunc.tradeInfo('>>>���л�Ʊǩ���嵥��ӡ����')
        
        #====��֯��ѯ���====
        sql = "BJEDTE >= '" + TradeContext.STRDAT + "'"
        sql = sql + " AND BJEDTE <= '" + TradeContext.ENDDAT + "'"
        sql = sql + " AND BESBNO =  '" + TradeContext.BESBNO + "'"
        sql = sql + " AND BRSFLG = '"  + PL_BRSFLG_SND + "'"
        sql = sql + " AND BILRS = '" + PL_BILRS_INN + "' AND HPSTAT = '" + PL_HPSTAT_SIGN + "'"

        #=====��ʲ�ѯ====
        records = rccpsDBTrcc_bilbka.selectm(1,0,sql,"")
        if records == None:
            return AfaFlowControl.ExitThisFlow('A099','���ݿ����ʧ��' )
        if len(records) == 0:
            return AfaFlowControl.ExitThisFlow('A099','������������¼' )

        #=====��ʼ��֯�����ļ�====
        filename="rccps_"+TradeContext.BETELR+"_"+AfaUtilTools.GetSysDate()+"_"+TradeContext.TransCode
        try:
            fpath=os.environ["AFAP_HOME"]+"/tmp/"
            f=open(fpath+filename,"w")
        except IOError:
            return AfaFlowControl.ExitThisFlow('S999','���ļ�ʧ��') 

        #=====д�ļ�ͷ====
        filecontext = "\n\n\n"
        filecontext = filecontext + "                                                  " + TradeContext.BESBNM + "���л�Ʊǩ���嵥\n" 
        filecontext = filecontext + "��ֹ���ڣ�" + TradeContext.STRDAT + "~" + TradeContext.ENDDAT + "\n"
        filecontext = filecontext + "��� ��Ʊ��𡡱������  ����Ʊ����  ��Ʊ���롡��    ��  �������˺š�������������������"
        filecontext = filecontext + "�տ����˺š�������������������ҵ��״̬\n"
        filecontext = filecontext + "=================================================================================================================\n"
        f.write(filecontext+"\n")

        #=====ѭ����֯�ļ�����====
        for i in range(0,len(records)):
            #=====ͨ����Ʊ���롢��Ʊ�汾��ȡ��Ʊ���====
            bilinf      = {}
            bilinf_dict = {'BILVER':records[i]['BILVER'],'BILNO':records[i]['BILNO'],'BILRS':records[i]['BILRS']}
            bilinf     = rccpsDBTrcc_bilinf.selectu(bilinf_dict)
            if bilinf == None:
                return AfaFlowControl.ExitThisFlow('S999','���ݿ����ʧ��')
            if len(bilinf) <= 0:
                return AfaFlowControl.ExitThisFlow('S999','ͨ����Ʊ����ȡ��Ʊ���ʧ��')
                 
            #=====д�ļ�====
            filecontext=str(i+1).ljust(4) + bilinf['BILTYP'].ljust(10) + records[i]['BSPSQN'].ljust(13) \
                       + bilinf['BILDAT'].ljust(9)        + records[i]['BILNO'].ljust(11)         \
                       + str(bilinf['BILAMT']).ljust(11)  + bilinf['PYRACC'].ljust(30)            \
                       + bilinf['PYEACC'].ljust(34)       + bilinf['BILTYP']
            f.write(filecontext+"\n")

        #=====��Ӵ�ӡ���ڵ�====       
        filecontext = "-----------------------------------------------------------------------------------------------------------------\n"
        filecontext = filecontext +  "    ��ӡ����:" + TradeContext.BJEDTE + "                           ��Ȩ���������������������������ˣ�  \n"
        f.write(filecontext)

        f.close()
        AfaLoggerFunc.tradeInfo(">>>�����ļ�����")
    #====04 �⸶���л�Ʊ====
    elif TradeContext.TRCCO == '04':
        AfaLoggerFunc.tradeInfo('>>>�⸶���л�Ʊ�嵥��ӡ����')
        
        #====��֯��ѯ���====
        sql = "BJEDTE >= '" + TradeContext.STRDAT + "'"
        sql = sql + " AND BJEDTE <= '" + TradeContext.ENDDAT + "'"
        sql = sql + " AND BESBNO =  '" + TradeContext.BESBNO + "'"
        sql = sql + " AND BRSFLG = '"  + PL_BRSFLG_SND + "'"
        sql = sql + " AND BILRS = '" + PL_BILRS_OUT + "'"

        #=====��ʲ�ѯ====
        records = rccpsDBTrcc_bilbka.selectm(1,0,sql,"")
        if records == None:
            return AfaFlowControl.ExitThisFlow('A099','���ݿ����ʧ��' )
        if len(records) == 0:
            return AfaFlowControl.ExitThisFlow('A099','������������¼' )

        #=====��ʼ��֯�����ļ�====
        filename="rccps_"+TradeContext.BETELR+"_"+AfaUtilTools.GetSysDate()+"_"+TradeContext.TransCode
        try:
            fpath=os.environ["AFAP_HOME"]+"/tmp/"
            f=open(fpath+filename,"w")
        except IOError:
            return AfaFlowControl.ExitThisFlow('S999','���ļ�ʧ��') 

        #=====д�ļ�ͷ====
        filecontext = "\n\n\n"
        filecontext = filecontext + "                                                  " + TradeContext.BESBNM + "�⸶���л�Ʊ�嵥\n" 
        filecontext = filecontext + "��ֹ���ڣ�" + TradeContext.STRDAT + "~" + TradeContext.ENDDAT + "\n"
        filecontext = filecontext + "��� ��Ʊ��𡡱������  ����Ʊ����  ��Ʊ���롡��    ��  �������˺š�������������������"
        filecontext = filecontext + "�տ����˺š�������������������ҵ��״̬\n"
        filecontext = filecontext + "=================================================================================================================\n"
        f.write(filecontext+"\n")

        #=====ѭ����֯�ļ�����====
        for i in range(0,len(records)):
            #=====ͨ����Ʊ���롢��Ʊ�汾��ȡ��Ʊ���====
            bilinf      = {}
            bilinf_dict = {'BILVER':records[i]['BILVER'],'BILNO':records[i]['BILNO'],'BILRS':records[i]['BILRS']}
            bilinf     = rccpsDBTrcc_bilinf.selectu(bilinf_dict)
            
            if bilinf == None:
                return AfaFlowControl.ExitThisFlow('S999','���ݿ����ʧ��')
            if len(bilinf) <= 0:
                return AfaFlowControl.ExitThisFlow('S999','ͨ����Ʊ����ȡ��Ʊ���ʧ��')
                 
            #=====д�ļ�====
            filecontext=str(i+1).ljust(4) + bilinf['BILTYP'].ljust(10) + records[i]['BSPSQN'].ljust(13) \
                       + bilinf['BILDAT'].ljust(9)        + records[i]['BILNO'].ljust(11)         \
                       + str(bilinf['BILAMT']).ljust(11)  + bilinf['PYRACC'].ljust(30)            \
                       + bilinf['PYEACC'].ljust(34)       + bilinf['BILTYP']
            f.write(filecontext+"\n")

        #=====��Ӵ�ӡ���ڵ�====       
        filecontext = "-----------------------------------------------------------------------------------------------------------------\n"
        filecontext = filecontext +  "    ��ӡ����:" + TradeContext.BJEDTE + "                           ��Ȩ���������������������������ˣ�  \n"
        f.write(filecontext)

        f.close()
        AfaLoggerFunc.tradeInfo(">>>�����ļ�����")
    #=====05 �˻�����====
    elif TradeContext.TRCCO == '05':
        AfaLoggerFunc.tradeInfo('>>>�˻������嵥��ӡ����')
        
        #=====��֯��ѯ���====
        sql = "BJEDTE >= '" + TradeContext.STRDAT + "'"
        sql = sql + " AND BJEDTE <= '" + TradeContext.ENDDAT + "'"
        sql = sql + " AND BESBNO =  '" + TradeContext.BESBNO + "'"
        sql = sql + " AND BRSFLG = '"  + PL_BRSFLG_SND + "'"
        sql = sql + " AND TRCCO  = '2000004' "

        #=====��ʲ�ѯ====
        ordersql = "ORDER BY TRCCO ASC"
        records = rccpsDBTrcc_trcbka.selectm(1,0,sql,ordersql)
        if records == None:
            return AfaFlowControl.ExitThisFlow('A099','���ݿ����ʧ��' )
        if len(records) == 0:
            return AfaFlowControl.ExitThisFlow('A099','������������¼' )

        #=====��ʼ��֯�����ļ�====
        filename="rccps_"+TradeContext.BETELR+"_"+AfaUtilTools.GetSysDate()+"_"+TradeContext.TransCode
        try:
            fpath=os.environ["AFAP_HOME"]+"/tmp/"
            f=open(fpath+filename,"w")
        except IOError:
            return AfaFlowControl.ExitThisFlow('S999','���ļ�ʧ��') 

        #=====д�ļ�ͷ====
        filecontext = "\n\n\n"
        filecontext = filecontext + "                                                  " + TradeContext.BESBNM + "�˻������嵥\n" 
        filecontext = filecontext + "��ֹ���ڣ�" + TradeContext.STRDAT + "~" + TradeContext.ENDDAT + "\n"
        filecontext = filecontext + "��� ҵ�����ࡡ�������  ���������� �������к� �������кš����      �������˺š�������������������"
        filecontext = filecontext + "�տ����˺š�������������������ҵ��״̬\n"
        filecontext = filecontext + "=================================================================================================================\n"
        f.write(filecontext+"\n")

        #=====ѭ����֯�ļ�����====
        for i in range(0,len(records)):
            #=====ͨ��������ź�����ȡ״̬====
            bcstat      = {}
            bcstat_dict = {'BJEDTE':records[i]['BJEDTE'],'BSPSQN':records[i]['BSPSQN']}
            bcstat     = rccpsDBTrcc_spbsta.selectu(bcstat_dict)
            if bcstat == None:
                return AfaFlowControl.ExitThisFlow('S999','���ݿ����ʧ��')
            if len(bcstat) <= 0:
                return AfaFlowControl.ExitThisFlow('S999','ͨ���������ȡҵ��״̬ʧ��')
                 
            #=====д�ļ�====
            filecontext=str(i+1).ljust(4) +  records[i]['TRCCO'].ljust(10) + records[i]['BSPSQN'].ljust(13) \
                       + records[i]['BJEDTE'].ljust(9)    + records[i]['SNDBNKCO'].ljust(11)      \
                       + records[i]['RCVBNKCO'].ljust(11) + str(records[i]['OCCAMT']).ljust(11)   \
                       + records[i]['PYRACC'].ljust(30)   + records[i]['PYEACC'].ljust(34)        \
                       + bcstat['BCSTAT']
            f.write(filecontext+"\n")

        #=====��Ӵ�ӡ���ڵ�====       
        filecontext = "-----------------------------------------------------------------------------------------------------------------\n"
        filecontext = filecontext +  "    ��ӡ����:" + TradeContext.BJEDTE + "                           ��Ȩ���������������������������ˣ�  \n"
        f.write(filecontext)

        f.close()
        AfaLoggerFunc.tradeInfo(">>>�����ļ�����")
    #=====06 �˻�����====
    elif TradeContext.TRCCO == '06':
        AfaLoggerFunc.tradeInfo('>>>�˻������嵥��ӡ����')
        
        #=====��֯��ѯ���====
        sql = "BJEDTE >= '" + TradeContext.STRDAT + "'"
        sql = sql + " AND BJEDTE <= '" + TradeContext.ENDDAT + "'"
        sql = sql + " AND BESBNO =  '" + TradeContext.BESBNO + "'"
        sql = sql + " AND BRSFLG = '"  + PL_BRSFLG_RCV + "'"
        sql = sql + " AND TRCCO  = '2000004' "

        #=====��ʲ�ѯ====
        ordersql = "ORDER BY TRCCO ASC"
        records = rccpsDBTrcc_trcbka.selectm(1,0,sql,ordersql)
        if records == None:
            return AfaFlowControl.ExitThisFlow('A099','���ݿ����ʧ��' )
        if len(records) == 0:
            return AfaFlowControl.ExitThisFlow('A099','������������¼' )

        #=====��ʼ��֯�����ļ�====
        filename="rccps_"+TradeContext.BETELR+"_"+AfaUtilTools.GetSysDate()+"_"+TradeContext.TransCode
        try:
            fpath=os.environ["AFAP_HOME"]+"/tmp/"
            f=open(fpath+filename,"w")
        except IOError:
            return AfaFlowControl.ExitThisFlow('S999','���ļ�ʧ��') 

        #=====д�ļ�ͷ====
        filecontext = "\n\n\n"
        filecontext = filecontext + "                                                  " + TradeContext.BESBNM + "�˻������嵥\n" 
        filecontext = filecontext + "��ֹ���ڣ�" + TradeContext.STRDAT + "~" + TradeContext.ENDDAT + "\n"
        filecontext = filecontext + "��� ҵ�����ࡡ�������  ���������� �������к� �������кš����      �������˺š�������������������"
        filecontext = filecontext + "�տ����˺š�������������������ҵ��״̬\n"
        filecontext = filecontext + "=================================================================================================================\n"
        f.write(filecontext+"\n")

        #=====ѭ����֯�ļ�����====
        for i in range(0,len(records)):
            #=====ͨ��������ź�����ȡ״̬====
            bcstat      = {}
            bcstat_dict = {'BJEDTE':records[i]['BJEDTE'],'BSPSQN':records[i]['BSPSQN']}
            bcstat     = rccpsDBTrcc_spbsta.selectu(bcstat_dict)
            if bcstat == None:
                return AfaFlowControl.ExitThisFlow('S999','���ݿ����ʧ��')
            if len(bcstat) <= 0:
                return AfaFlowControl.ExitThisFlow('S999','ͨ���������ȡҵ��״̬ʧ��')
                 
            #=====д�ļ�====
            filecontext=str(i+1).ljust(4) +  records[i]['TRCCO'].ljust(10) + records[i]['BSPSQN'].ljust(13) \
                       + records[i]['BJEDTE'].ljust(9)    + records[i]['SNDBNKCO'].ljust(11)      \
                       + records[i]['RCVBNKCO'].ljust(11) + str(records[i]['OCCAMT']).ljust(11)   \
                       + records[i]['PYRACC'].ljust(30)   + records[i]['PYEACC'].ljust(34)        \
                       + bcstat['BCSTAT'] 
            f.write(filecontext+"\n")

        #=====��Ӵ�ӡ���ڵ�====       
        filecontext = "-----------------------------------------------------------------------------------------------------------------\n"
        filecontext = filecontext +  "    ��ӡ����:" + TradeContext.BJEDTE + "                           ��Ȩ���������������������������ˣ�  \n"
        f.write(filecontext)

        f.close()
        AfaLoggerFunc.tradeInfo(">>>�����ļ�����")
    #=====07 ��Ҳ�ѯ��====
    elif TradeContext.TRCCO == '07':
        AfaLoggerFunc.tradeInfo('>>>��Ҳ�ѯ���嵥��ӡ����')
        
        #=====��֯��ѯ���====
        sql = "BJEDTE >= '" + TradeContext.STRDAT + "'"
        sql = sql + " AND BJEDTE <= '" + TradeContext.ENDDAT + "'"
        sql = sql + " AND BESBNO =  '" + TradeContext.BESBNO + "'"
        sql = sql + " AND TRCCO IN ('9900511','9900522') "

        #=====��ʲ�ѯ====
        ordersql = "ORDER BY TRCCO ASC"
        records = rccpsDBTrcc_hdcbka.selectm(1,0,sql,ordersql)
        if records == None:
            return AfaFlowControl.ExitThisFlow('A099','���ݿ����ʧ��' )
        if len(records) == 0:
            return AfaFlowControl.ExitThisFlow('A099','������������¼' )

        #=====��ʼ��֯�����ļ�====
        filename="rccps_"+TradeContext.BETELR+"_"+AfaUtilTools.GetSysDate()+"_"+TradeContext.TransCode
        try:
            fpath=os.environ["AFAP_HOME"]+"/tmp/"
            f=open(fpath+filename,"w")
        except IOError:
            return AfaFlowControl.ExitThisFlow('S999','���ļ�ʧ��') 

        #=====д�ļ�ͷ====
        filecontext = "\n\n\n"
        filecontext = filecontext + "                                                  " + TradeContext.BESBNM + "��Ҳ�ѯ���嵥\n" 
        filecontext = filecontext + "��ֹ���ڣ�" + TradeContext.STRDAT + "~" + TradeContext.ENDDAT + "\n"
        filecontext = filecontext + "���  ��ѯ���  ����ѯ����  ������־  �������к�  �������кš�״̬\n"
        filecontext = filecontext + "=================================================================================================================\n"
        f.write(filecontext+"\n")

        #=====ѭ����֯�ļ�����====
        for i in range(0,len(records)):
            #=====д�ļ�====
            filecontext=str(i+1).ljust(4) + records[i]['BSPSQN'].ljust(13) \
                       + records[i]['BJEDTE'].ljust(13)    + records[i]['BRSFLG'].ljust(8)      \
                       + records[i]['SNDBNKCO'].ljust(12) + records[i]['RCVBNKCO'].ljust(13)    \
                       + records[i]['ISDEAL'] 
            f.write(filecontext+"\n")

        #=====��Ӵ�ӡ���ڵ�====       
        filecontext = "-----------------------------------------------------------------------------------------------------------------\n"
        filecontext = filecontext +  "    ��ӡ����:" + TradeContext.BJEDTE + "                           ��Ȩ���������������������������ˣ�  \n"
        f.write(filecontext)

        f.close()
        AfaLoggerFunc.tradeInfo(">>>�����ļ�����")
    #=====08 ��Ҳ鸴��====
    elif TradeContext.TRCCO == '08':
        AfaLoggerFunc.tradeInfo('>>>��Ҳ鸴���嵥��ӡ����')
        
        #=====��֯��ѯ���====
        sql = "BJEDTE >= '" + TradeContext.STRDAT + "'"
        sql = sql + " AND BJEDTE <= '" + TradeContext.ENDDAT + "'"
        sql = sql + " AND BESBNO =  '" + TradeContext.BESBNO + "'"
        sql = sql + " AND TRCCO IN ('9900512','9900523') "

        #=====��ʲ�ѯ====
        ordersql = "ORDER BY TRCCO ASC"
        records = rccpsDBTrcc_hdcbka.selectm(1,0,sql,ordersql)
        if records == None:
            return AfaFlowControl.ExitThisFlow('A099','���ݿ����ʧ��' )
        if len(records) == 0:
            return AfaFlowControl.ExitThisFlow('A099','������������¼' )

        #=====��ʼ��֯�����ļ�====
        filename="rccps_"+TradeContext.BETELR+"_"+AfaUtilTools.GetSysDate()+"_"+TradeContext.TransCode
        try:
            fpath=os.environ["AFAP_HOME"]+"/tmp/"
            f=open(fpath+filename,"w")
        except IOError:
            return AfaFlowControl.ExitThisFlow('S999','���ļ�ʧ��') 

        #=====д�ļ�ͷ====
        filecontext = "\n\n\n"
        filecontext = filecontext + "                                                  " + TradeContext.BESBNM + "��Ҳ鸴���嵥\n" 
        filecontext = filecontext + "��ֹ���ڣ�" + TradeContext.STRDAT + "~" + TradeContext.ENDDAT + "\n"
        filecontext = filecontext + "���  ��ѯ���  ����ѯ����  ������־  �������к�  �������кš�״̬\n"
        filecontext = filecontext + "=================================================================================================================\n"
        f.write(filecontext+"\n")

        #=====ѭ����֯�ļ�����====
        for i in range(0,len(records)):
            #=====д�ļ�====
            filecontext=str(i+1).ljust(4) + records[i]['BSPSQN'].ljust(13) \
                       + records[i]['BJEDTE'].ljust(9)    + records[i]['BRSFLG'].ljust(10)      \
                       + records[i]['SNDBNKCO'].ljust(11) + records[i]['RCVBNKCO'].ljust(11)    \
                       + records[i]['ISDEAL'] 
            f.write(filecontext+"\n")

        #=====��Ӵ�ӡ���ڵ�====       
        filecontext = "-----------------------------------------------------------------------------------------------------------------\n"
        filecontext = filecontext +  "    ��ӡ����:" + TradeContext.BJEDTE + "                           ��Ȩ���������������������������ˣ�  \n"
        f.write(filecontext)

        f.close()
        AfaLoggerFunc.tradeInfo(">>>�����ļ�����")
    #=====09 Ʊ�ݲ�ѯ��====
    elif TradeContext.TRCCO == '09':
        AfaLoggerFunc.tradeInfo('>>>Ʊ�ݲ�ѯ���嵥��ӡ����')
        
        #=====��֯��ѯ���====
        sql = "BJEDTE >= '" + TradeContext.STRDAT + "'"
        sql = sql + " AND BJEDTE <= '" + TradeContext.ENDDAT + "'"
        sql = sql + " AND BESBNO =  '" + TradeContext.BESBNO + "'"
        sql = sql + " AND TRCCO  = '9900520' "

        #=====��ʲ�ѯ====
        ordersql = "ORDER BY TRCCO ASC"
        records = rccpsDBTrcc_pjcbka.selectm(1,0,sql,ordersql)
        if records == None:
            return AfaFlowControl.ExitThisFlow('A099','���ݿ����ʧ��' )
        if len(records) == 0:
            return AfaFlowControl.ExitThisFlow('A099','������������¼' )

        #=====��ʼ��֯�����ļ�====
        filename="rccps_"+TradeContext.BETELR+"_"+AfaUtilTools.GetSysDate()+"_"+TradeContext.TransCode
        try:
            fpath=os.environ["AFAP_HOME"]+"/tmp/"
            f=open(fpath+filename,"w")
        except IOError:
            return AfaFlowControl.ExitThisFlow('S999','���ļ�ʧ��') 

        #=====д�ļ�ͷ====
        filecontext = "\n\n\n"
        filecontext = filecontext + "                                                  " + TradeContext.BESBNM + "Ʊ�ݲ�ѯ���嵥\n" 
        filecontext = filecontext + "��ֹ���ڣ�" + TradeContext.STRDAT + "~" + TradeContext.ENDDAT + "\n"
        filecontext = filecontext + "���  ��ѯ���  ����ѯ����  ������־  �������к�  �������кš�״̬\n"
        filecontext = filecontext + "=================================================================================================================\n"
        f.write(filecontext+"\n")

        #=====ѭ����֯�ļ�����====
        for i in range(0,len(records)):
            #=====д�ļ�====
            filecontext=str(i+1).ljust(4) + records[i]['BSPSQN'].ljust(13) \
                       + records[i]['BJEDTE'].ljust(9)    + records[i]['BRSFLG'].ljust(10)      \
                       + records[i]['SNDBNKCO'].ljust(11) + records[i]['RCVBNKCO'].ljust(11)    \
                       + records[i]['ISDEAL'] 
            f.write(filecontext+"\n")
        

        #=====��Ӵ�ӡ���ڵ�====       
        filecontext = "-----------------------------------------------------------------------------------------------------------------\n"
        filecontext = filecontext +  "    ��ӡ����:" + TradeContext.BJEDTE + "                           ��Ȩ���������������������������ˣ�  \n"
        f.write(filecontext)

        f.close()
        AfaLoggerFunc.tradeInfo(">>>�����ļ�����")
    #=====10 Ʊ�ݲ鸴��====
    elif TradeContext.TRCCO == '10':
        AfaLoggerFunc.tradeInfo('>>>Ʊ�ݲ鸴���嵥��ӡ����')
        
        #=====��֯��ѯ���====
        sql = "BJEDTE >= '" + TradeContext.STRDAT + "'"
        sql = sql + " AND BJEDTE <= '" + TradeContext.ENDDAT + "'"
        sql = sql + " AND BESBNO =  '" + TradeContext.BESBNO + "'"
        sql = sql + " AND TRCCO  = '9900521' "

        #=====��ʲ�ѯ====
        ordersql = "ORDER BY TRCCO ASC"
        records = rccpsDBTrcc_pjcbka.selectm(1,0,sql,ordersql)
        if records == None:
            return AfaFlowControl.ExitThisFlow('A099','���ݿ����ʧ��' )
        if len(records) == 0:
            return AfaFlowControl.ExitThisFlow('A099','������������¼' )

        #=====��ʼ��֯�����ļ�====
        filename="rccps_"+TradeContext.BETELR+"_"+AfaUtilTools.GetSysDate()+"_"+TradeContext.TransCode
        try:
            fpath=os.environ["AFAP_HOME"]+"/tmp/"
            f=open(fpath+filename,"w")
        except IOError:
            return AfaFlowControl.ExitThisFlow('S999','���ļ�ʧ��') 

        #=====д�ļ�ͷ====
        filecontext = "\n\n\n"
        filecontext = filecontext + "                                                  " + TradeContext.BESBNM + "Ʊ�ݲ鸴���嵥\n" 
        filecontext = filecontext + "��ֹ���ڣ�" + TradeContext.STRDAT + "~" + TradeContext.ENDDAT + "\n"
        filecontext = filecontext + "���  ��ѯ���  ����ѯ����  ������־  �������к�  �������кš�״̬\n"
        filecontext = filecontext + "=================================================================================================================\n"
        f.write(filecontext+"\n")

        #=====ѭ����֯�ļ�����====
        for i in range(0,len(records)):
            #=====д�ļ�====
            filecontext=str(i+1).ljust(4) + records[i]['BSPSQN'].ljust(13) \
                       + records[i]['BJEDTE'].ljust(9)    + records[i]['BRSFLG'].ljust(10)      \
                       + records[i]['SNDBNKCO'].ljust(11) + records[i]['RCVBNKCO'].ljust(11)    \
                       + records[i]['ISDEAL'] 
            f.write(filecontext+"\n")

        #=====��Ӵ�ӡ���ڵ�====       
        filecontext = "-----------------------------------------------------------------------------------------------------------------\n"
        filecontext = filecontext +  "    ��ӡ����:" + TradeContext.BJEDTE + "                           ��Ȩ���������������������������ˣ�  \n"
        f.write(filecontext)

        f.close()
        AfaLoggerFunc.tradeInfo(">>>�����ļ�����")
    #=====11 ��Ʊ��ѯ��====
    elif TradeContext.TRCCO == '11':
        AfaLoggerFunc.tradeInfo('>>>��Ʊ��ѯ���嵥��ӡ����')
        
        #=====��֯��ѯ���====
        sql = "BJEDTE >= '" + TradeContext.STRDAT + "'"
        sql = sql + " AND BJEDTE <= '" + TradeContext.ENDDAT + "'"
        sql = sql + " AND BESBNO =  '" + TradeContext.BESBNO + "'"
        sql = sql + " AND TRCCO  = '9900526' "

        #=====��ʲ�ѯ====
        ordersql = "ORDER BY TRCCO ASC"
        records = rccpsDBTrcc_hpcbka.selectm(1,0,sql,ordersql)
        if records == None:
            return AfaFlowControl.ExitThisFlow('A099','���ݿ����ʧ��' )
        if len(records) == 0:
            return AfaFlowControl.ExitThisFlow('A099','������������¼' )

        #=====��ʼ��֯�����ļ�====
        filename="rccps_"+TradeContext.BETELR+"_"+AfaUtilTools.GetSysDate()+"_"+TradeContext.TransCode
        try:
            fpath=os.environ["AFAP_HOME"]+"/tmp/"
            f=open(fpath+filename,"w")
        except IOError:
            return AfaFlowControl.ExitThisFlow('S999','���ļ�ʧ��') 

        #=====д�ļ�ͷ====
        filecontext = "\n\n\n"
        filecontext = filecontext + "                                                  " + TradeContext.BESBNM + "��Ʊ��ѯ���嵥\n" 
        filecontext = filecontext + "��ֹ���ڣ�" + TradeContext.STRDAT + "~" + TradeContext.ENDDAT + "\n"
        filecontext = filecontext + "���  ��ѯ���    ��Ʊ����   ��Ʊ����  ��Ʊ���  ������־  �������к�  �������кš�״̬\n"
        filecontext = filecontext + "=================================================================================================================\n"
        f.write(filecontext+"\n")

        #=====ѭ����֯�ļ�����====
        for i in range(0,len(records)):
            #=====д�ļ�====
            filecontext=str(i+1).ljust(4) + records[i]['BSPSQN'].ljust(15) \
                       + records[i]['BILDAT'].ljust(9)    + records[i]['BILNO'].ljust(11)  \
                       + str(records[i]['BILAMT']).ljust(15) + records[i]['BRSFLG'].ljust(6)      \
                       + records[i]['SNDBNKCO'].ljust(11) + records[i]['RCVBNKCO'].ljust(13)    \
                       + records[i]['ISDEAL'] 
            f.write(filecontext+"\n")

        #=====��Ӵ�ӡ���ڵ�====       
        filecontext = "-----------------------------------------------------------------------------------------------------------------\n"
        filecontext = filecontext +  "    ��ӡ����:" + TradeContext.BJEDTE + "                           ��Ȩ���������������������������ˣ�  \n"
        f.write(filecontext)

        f.close()
        AfaLoggerFunc.tradeInfo(">>>�����ļ�����")
    #=====12 ��Ʊ�鸴��====
    elif TradeContext.TRCCO == '12':
        AfaLoggerFunc.tradeInfo('>>>��Ʊ�鸴���嵥��ӡ����')
        
        #=====��֯��ѯ���====
        sql = "BJEDTE >= '" + TradeContext.STRDAT + "'"
        sql = sql + " AND BJEDTE <= '" + TradeContext.ENDDAT + "'"
        sql = sql + " AND BESBNO =  '" + TradeContext.BESBNO + "'"
        sql = sql + " AND TRCCO  = '9900527' "

        #=====��ʲ�ѯ====
        ordersql = "ORDER BY TRCCO ASC"
        records = rccpsDBTrcc_hpcbka.selectm(1,0,sql,ordersql)
        if records == None:
            return AfaFlowControl.ExitThisFlow('A099','���ݿ����ʧ��' )
        if len(records) == 0:
            return AfaFlowControl.ExitThisFlow('A099','������������¼' )

        #=====��ʼ��֯�����ļ�====
        filename="rccps_"+TradeContext.BETELR+"_"+AfaUtilTools.GetSysDate()+"_"+TradeContext.TransCode
        try:
            fpath=os.environ["AFAP_HOME"]+"/tmp/"
            f=open(fpath+filename,"w")
        except IOError:
            return AfaFlowControl.ExitThisFlow('S999','���ļ�ʧ��') 

        #=====д�ļ�ͷ====
        filecontext = "\n\n\n"
        filecontext = filecontext + "                                                  " + TradeContext.BESBNM + "��Ʊ�鸴���嵥\n" 
        filecontext = filecontext + "��ֹ���ڣ�" + TradeContext.STRDAT + "~" + TradeContext.ENDDAT + "\n"
        filecontext = filecontext + "���  ��ѯ���  ����ѯ����  ������־  �������к�  �������кš�״̬\n"
        filecontext = filecontext + "=================================================================================================================\n"
        f.write(filecontext+"\n")

        #=====ѭ����֯�ļ�����====
        for i in range(0,len(records)):
            #=====д�ļ�====
            filecontext=str(i+1).ljust(4) + records[i]['BSPSQN'].ljust(13) \
                       + records[i]['BJEDTE'].ljust(9)    + records[i]['BRSFLG'].ljust(10)      \
                       + records[i]['SNDBNKCO'].ljust(11) + records[i]['RCVBNKCO'].ljust(11)    \
                       + records[i]['ISDEAL'] 
            f.write(filecontext+"\n")

        #=====��Ӵ�ӡ���ڵ�====       
        filecontext = "-----------------------------------------------------------------------------------------------------------------\n"
        filecontext = filecontext +  "    ��ӡ����:" + TradeContext.BJEDTE + "                           ��Ȩ���������������������������ˣ�  \n"
        f.write(filecontext)

        f.close()
        AfaLoggerFunc.tradeInfo(">>>�����ļ�����")
    #=====13 ���ɸ�ʽ��====
    elif TradeContext.TRCCO == '13':
        AfaLoggerFunc.tradeInfo('>>>���ɸ�ʽ���嵥��ӡ����')
        
        #=====��֯��ѯ���====
        sql = "BJEDTE >= '" + TradeContext.STRDAT + "'"
        sql = sql + " AND BJEDTE <= '" + TradeContext.ENDDAT + "'"
        sql = sql + " AND BESBNO =  '" + TradeContext.BESBNO + "'"
        sql = sql + " AND TRCCO IN ('9900513','9900524') "

        #=====��ʲ�ѯ====
        ordersql = "ORDER BY TRCCO ASC"
        records = rccpsDBTrcc_hdcbka.selectm(1,0,sql,ordersql)
        if records == None:
            return AfaFlowControl.ExitThisFlow('A099','���ݿ����ʧ��' )
        if len(records) == 0:
            return AfaFlowControl.ExitThisFlow('A099','������������¼' )

        #=====��ʼ��֯�����ļ�====
        filename="rccps_"+TradeContext.BETELR+"_"+AfaUtilTools.GetSysDate()+"_"+TradeContext.TransCode
        try:
            fpath=os.environ["AFAP_HOME"]+"/tmp/"
            f=open(fpath+filename,"w")
        except IOError:
            return AfaFlowControl.ExitThisFlow('S999','���ļ�ʧ��') 

        #=====д�ļ�ͷ====
        filecontext = "\n\n\n"
        filecontext = filecontext + "                                                  " + TradeContext.BESBNM + "���ɸ�ʽ���嵥\n" 
        filecontext = filecontext + "��ֹ���ڣ�" + TradeContext.STRDAT + "~" + TradeContext.ENDDAT + "\n"
        filecontext = filecontext + "��� ҵ�����ࡡ�� �� �� �š���������  �������к� �������кš�������־��״̬\n"
        filecontext = filecontext + "=================================================================================================================\n"
        f.write(filecontext+"\n")

        #=====ѭ����֯�ļ�����====
        for i in range(0,len(records)):
            #=====д�ļ�====
            filecontext=str(i+1).ljust(4) +  records[i]['TRCCO'].ljust(10) + records[i]['BSPSQN'].ljust(13) \
                       + records[i]['BJEDTE'].ljust(9)    + records[i]['SNDBNKCO'].ljust(11)      \
                       + records[i]['RCVBNKCO'].ljust(11) + records[i]['BRSFLG'].ljust(10)   \
                       + records[i]['ISDEAL']
            f.write(filecontext+"\n")

        #=====��Ӵ�ӡ���ڵ�====       
        filecontext = "-----------------------------------------------------------------------------------------------------------------\n"
        filecontext = filecontext +  "    ��ӡ����:" + TradeContext.BJEDTE + "                           ��Ȩ���������������������������ˣ�  \n"
        f.write(filecontext)

        f.close()
        AfaLoggerFunc.tradeInfo(">>>�����ļ�����")
    
    #=====15 ͨ��ͨ������====
    elif(TradeContext.TRCCO == '15'):
        AfaLoggerFunc.tradeInfo('>>>ͨ��ͨ�������嵥��ӡ����')
        
        #=====��֯��ѯ���====
        sql = "BJEDTE >= '" + TradeContext.STRDAT + "'"
        sql = sql + " AND BJEDTE <= '" + TradeContext.ENDDAT + "'"
        sql = sql + " AND BESBNO =  '" + TradeContext.BESBNO + "'"
        sql = sql + " AND BRSFLG =  '" + PL_BRSFLG_SND       + "'"
        
        #=====��ʲ�ѯ====
        ordersql = "ORDER BY TRCCO ASC"
        records = rccpsDBTrcc_wtrbka.selectm(1,0,sql,ordersql)
        if records == None:
            return AfaFlowControl.ExitThisFlow('A099','���ݿ����ʧ��' )
        if len(records) == 0:
            return AfaFlowControl.ExitThisFlow('A099','������������¼' )
            
        #=====��ʼ��֯�����ļ�====
        filename="rccps_"+TradeContext.BETELR+"_"+AfaUtilTools.GetSysDate()+"_"+TradeContext.TransCode
        try:
            fpath=os.environ["AFAP_HOME"]+"/tmp/"
            f=open(fpath+filename,"w")
        except IOError:
            return AfaFlowControl.ExitThisFlow('S999','���ļ�ʧ��') 

        #=====д�ļ�ͷ====
        filecontext = "\n\n\n"
        filecontext = filecontext + "                                                  " + TradeContext.BESBNM + "ͨ��ͨ�������嵥\n" 
        filecontext = filecontext + "��ֹ���ڣ�" + TradeContext.STRDAT + "~" + TradeContext.ENDDAT + "\n"
        filecontext = filecontext + "��š���������  �������      �������к�  ���״��롡�տ����˺�           ��   �������˺�              ���           ������         ״̬\n"
        filecontext = filecontext + "================================================================================================================================================\n"
        f.write(filecontext+"\n")

        #=====ѭ����֯�ļ�����====
        for i in range(0,len(records)):
            #=====��ѯ�˱ʽ��׵ĵ�ǰ״̬====
            where_dict = {}
            where_dict = {'BJEDTE':records[i]['BJEDTE'],'BSPSQN':records[i]['BSPSQN']}
            spb_dict = rccpsDBTrcc_spbsta.selectu(where_dict)
            if(spb_dict == None):
                return AfaFlowControl.ExitThisFlow('S999','��ѯҵ��ĵ�ǰ״̬ʧ��')
            
            elif(len(spb_dict) == 0):
                return AfaFlowControl.ExitThisFlow('S999','��ѯҵ��ĵ�ǰ״̬���Ϊ��')
                
            else:
                AfaLoggerFunc.tradeInfo("��ѯҵ��ĵ�ǰ״̬�ɹ�")
            
            #=====д�ļ�====
            filecontext=str(i+1).ljust(6) +  records[i]['BJEDTE'].ljust(10) + records[i]['BSPSQN'].ljust(14) \
                       + records[i]['RCVBNKCO'].ljust(12)    + records[i]['TRCCO'].ljust(10)      \
                       + records[i]['PYEACC'].ljust(26) + records[i]['PYRACC'].ljust(25)   \
                       + str(records[i]['OCCAMT']).ljust(15) + str(records[i]['CUSCHRG']).ljust(15) + spb_dict['BCSTAT'].ljust(2)
            f.write(filecontext+"\n")

        #=====��Ӵ�ӡ���ڵ�====       
        filecontext = "-----------------------------------------------------------------------------------------------------------------\n"
        filecontext = filecontext +  "    ��ӡ����:" + TradeContext.BJEDTE + "                           ��Ȩ���������������������������ˣ�  \n"
        f.write(filecontext)

        f.close()
        AfaLoggerFunc.tradeInfo(">>>�����ļ�����")
        
    #=====14 ͨ��ͨ������====
    elif(TradeContext.TRCCO == '14'):
        AfaLoggerFunc.tradeInfo('>>>ͨ��ͨ�������嵥��ӡ����')
        
        #=====��֯��ѯ���====
        sql = "BJEDTE >= '" + TradeContext.STRDAT + "'"
        sql = sql + " AND BJEDTE <= '" + TradeContext.ENDDAT + "'"
        sql = sql + " AND BESBNO =  '" + TradeContext.BESBNO + "'"
        sql = sql + " AND BRSFLG =  '" + PL_BRSFLG_RCV       + "'"
        
        #=====��ʲ�ѯ====
        ordersql = "ORDER BY TRCCO ASC"
        records = rccpsDBTrcc_wtrbka.selectm(1,0,sql,ordersql)
        if records == None:
            return AfaFlowControl.ExitThisFlow('A099','���ݿ����ʧ��' )
        if len(records) == 0:
            return AfaFlowControl.ExitThisFlow('A099','������������¼' )
            
        #=====��ʼ��֯�����ļ�====
        filename="rccps_"+TradeContext.BETELR+"_"+AfaUtilTools.GetSysDate()+"_"+TradeContext.TransCode
        try:
            fpath=os.environ["AFAP_HOME"]+"/tmp/"
            f=open(fpath+filename,"w")
        except IOError:
            return AfaFlowControl.ExitThisFlow('S999','���ļ�ʧ��') 

        #=====д�ļ�ͷ====
        filecontext = "\n\n\n"
        filecontext = filecontext + "                                                  " + TradeContext.BESBNM + "ͨ��ͨ�������嵥\n" 
        filecontext = filecontext + "��ֹ���ڣ�" + TradeContext.STRDAT + "~" + TradeContext.ENDDAT + "\n"
        filecontext = filecontext + "��š���������  �������      �������к�  ���״��롡�տ����˺�           ��   �������˺�              ���           ������         ״̬\n"
        filecontext = filecontext + "================================================================================================================================================\n"
        f.write(filecontext+"\n")

        #=====ѭ����֯�ļ�����====
        for i in range(0,len(records)):
            #=====��ѯ�˱ʽ��׵ĵ�ǰ״̬====
            where_dict = {}
            where_dict = {'BJEDTE':records[i]['BJEDTE'],'BSPSQN':records[i]['BSPSQN']}
            spb_dict = rccpsDBTrcc_spbsta.selectu(where_dict)
            if(spb_dict == None):
                return AfaFlowControl.ExitThisFlow('S999','��ѯҵ��ĵ�ǰ״̬ʧ��')
            
            elif(len(spb_dict) == 0):
                return AfaFlowControl.ExitThisFlow('S999','��ѯҵ��ĵ�ǰ״̬���Ϊ��')
                
            else:
                AfaLoggerFunc.tradeInfo("��ѯҵ��ĵ�ǰ״̬�ɹ�")
            
            #=====д�ļ�====
            filecontext=str(i+1).ljust(6) +  records[i]['BJEDTE'].ljust(10) + records[i]['BSPSQN'].ljust(14) \
                       + records[i]['RCVBNKCO'].ljust(12)    + records[i]['TRCCO'].ljust(10)      \
                       + records[i]['PYEACC'].ljust(26) + records[i]['PYRACC'].ljust(25)   \
                       + str(records[i]['OCCAMT']).ljust(15) + str(records[i]['CUSCHRG']).ljust(15) + spb_dict['BCSTAT'].ljust(2)
            f.write(filecontext+"\n")

        #=====��Ӵ�ӡ���ڵ�====       
        filecontext = "-----------------------------------------------------------------------------------------------------------------\n"
        filecontext = filecontext +  "    ��ӡ����:" + TradeContext.BJEDTE + "                           ��Ȩ���������������������������ˣ�  \n"
        f.write(filecontext)

        f.close()
        AfaLoggerFunc.tradeInfo(">>>�����ļ�����")
    
    else:
        return AfaFlowControl.ExitThisFlow('S999','ҵ�����ʹ�')

    TradeContext.errorCode = '0000'
    TradeContext.errorMsg  = '�ɹ�'
    TradeContext.PRTDAT    = TradeContext.BJEDTE        #��ӡ����
    TradeContext.PBDAFILE  = filename                   #�ļ���
    
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.�������������[TRC001_8535]�˳�***' )
    return True
