# -*- coding: gbk -*-
##################################################################
#   ��������ƽ̨.������ͨѶ����
#=================================================================
#   �����ļ�:   AfaHostFunc.py
#   �޸�ʱ��:   2006-09-12
#
##################################################################
import  TradeContext,AfaFunc,UtilTools,HostComm,HostContext,HostDataHandler,AfaLoggerFunc,os
from types import *
import jiami
#====================��ʼ�������������ӿ�===========================
def InitGLHostReq( ):
    AfaLoggerFunc.tradeInfo("ִ��InitGLHostReq����")
    if (TradeContext.HostCode == '8813'):
        #ͬ��ת��/���
        AfaLoggerFunc.tradeInfo("ͬ��ת��/���")
        AfaLoggerFunc.tradeDebug("�ӿ�һ")
        #=====�ӿ�һ====
        HostContext.I1TRCD = TradeContext.I1TRCD
        HostContext.I1SBNO = TradeContext.I1SBNO
        HostContext.I1USID = TradeContext.I1USID
        HostContext.I1AUUS = TradeContext.I1AUUS
        HostContext.I1AUPS = TradeContext.I1AUPS
        HostContext.I1WSNO = TradeContext.I1WSNO
        HostContext.I1ACUR = TradeContext.I1ACUR
        
        #=====�ӿڶ�====
        AfaLoggerFunc.tradeDebug("�ӿڶ�")
        if(int(TradeContext.I1ACUR) != 0):
            HostContext.I2NBBH = []
            HostContext.I2CLDT = []
            HostContext.I2UNSQ = []
            HostContext.I2FEDT = []
            HostContext.I2RBSQ = []
            HostContext.I2DATE = []
            HostContext.I2TRDT = []
            HostContext.I2RGSQ = []
            HostContext.I2RVFG = []
            HostContext.I2SBNO = []
            HostContext.I2TELR = []
            HostContext.I2TRSQ = []
            HostContext.I2TINO = []
            HostContext.I2SBAC = []
            HostContext.I2ACNM = []
            HostContext.I2DASQ = []
            HostContext.I2CFFG = []
            HostContext.I2PSWD = []
            HostContext.I2PS16 = []
            HostContext.I2IDTY = []
            HostContext.I2IDNO = []
            HostContext.I2OPTY = []
            HostContext.I2CETY = []
            HostContext.I2CCSQ = []
            HostContext.I2PKFG = []
            HostContext.I2TRFG = []
            HostContext.I2RBAC = []
            HostContext.I2OTNM = []
            HostContext.I2CYNO = []
            HostContext.I2CTFG = []
            HostContext.I2CATR = []
            HostContext.I2WLBZ = []
            HostContext.I2TRAM = []
            HostContext.I2SMCD = []
            HostContext.I2CHEX = []
            HostContext.I2NMFG = []
            HostContext.I2FZNO = []
            HostContext.I2AMTT = []
            HostContext.I2AMST = []
            HostContext.I2APX1 = []
            HostContext.I2APX2 = []
            HostContext.I2REAC = []

        if(int(TradeContext.I1ACUR) == 1 ):
            HostContext.I2NBBH.append(TradeContext.I2NBBH)
            HostContext.I2CLDT.append(TradeContext.I2CLDT)
            HostContext.I2UNSQ.append(TradeContext.I2UNSQ)
            HostContext.I2FEDT.append(TradeContext.I2FEDT)
            HostContext.I2RBSQ.append(TradeContext.I2RBSQ)
            HostContext.I2DATE.append(TradeContext.I2P)
            HostContext.I2TRDT.append(TradeContext.I2TRDT)
            HostContext.I2RGSQ.append(TradeContext.I2RGSQ)
            HostContext.I2RVFG.append(TradeContext.I2RVFG)
            HostContext.I2SBNO.append(TradeContext.I2SBNO)
            HostContext.I2TELR.append(TradeContext.I2TELR)
            HostContext.I2TRSQ.append(TradeContext.I2TRSQ)
            HostContext.I2TINO.append(TradeContext.I2TINO)
            HostContext.I2SBAC.append(TradeContext.I2SBAC)
            HostContext.I2ACNM.append(TradeContext.I2ACNM)
            HostContext.I2DASQ.append(TradeContext.I2DASQ)
            HostContext.I2CFFG.append(TradeContext.I2CFFG)
            HostContext.I2PSWD.append(TradeContext.I2PSWD)
            HostContext.I2PS16.append(TradeContext.I2PS16)
            HostContext.I2IDTY.append(TradeContext.I2IDTY)
            HostContext.I2IDNO.append(TradeContext.I2IDNO)
            HostContext.I2OPTY.append(TradeContext.I2OPTY)
            HostContext.I2CETY.append(TradeContext.I2CETY)
            HostContext.I2CCSQ.append(TradeContext.I2CCSQ)
            HostContext.I2PKFG.append(TradeContext.I2PKFG)
            HostContext.I2TRFG.append(TradeContext.I2TRFG)
            HostContext.I2RBAC.append(TradeContext.I2RBAC)
            HostContext.I2OTNM.append(TradeContext.I2OTNM)
            HostContext.I2CYNO.append(TradeContext.I2CYNO)
            HostContext.I2CTFG.append(TradeContext.I2CTFG)
            HostContext.I2CATR.append(TradeContext.I2CATR)
            HostContext.I2WLBZ.append(TradeContext.I2WLBZ)
            HostContext.I2TRAM.append(TradeContext.I2TRAM)
            HostContext.I2SMCD.append(TradeContext.I2SMCD)
            HostContext.I2CHEX.append(TradeContext.I2CHEX)
            HostContext.I2NMFG.append(TradeContext.I2NMFG)
            HostContext.I2FZNO.append(TradeContext.I2FZNO)
            HostContext.I2AMTT.append(TradeContext.I2AMTT)
            HostContext.I2AMST.append(TradeContext.I2AMST)
            HostContext.I2APX1.append(TradeContext.I2APX1)
            HostContext.I2APX2.append(TradeContext.I2APX2)
            HostContext.I2REAC.append(TradeContext.I2REAC)
            
        else:
            for i in range(0,int(TradeContext.I1ACUR)):
                HostContext.I2NBBH.append(TradeContext.I2NBBH[i])
                HostContext.I2CLDT.append(TradeContext.I2CLDT[i])
                HostContext.I2UNSQ.append(TradeContext.I2UNSQ[i])
                HostContext.I2FEDT.append(TradeContext.I2FEDT[i])
                HostContext.I2RBSQ.append(TradeContext.I2RBSQ[i])
                HostContext.I2DATE.append(TradeContext.I2P[i])
                HostContext.I2TRDT.append(TradeContext.I2TRDT[i])
                HostContext.I2RGSQ.append(TradeContext.I2RGSQ[i])
                HostContext.I2RVFG.append(TradeContext.I2RVFG[i])
                HostContext.I2SBNO.append(TradeContext.I2SBNO[i])
                HostContext.I2TELR.append(TradeContext.I2TELR[i])
                HostContext.I2TRSQ.append(TradeContext.I2TRSQ[i])
                HostContext.I2TINO.append(TradeContext.I2TINO[i])
                HostContext.I2SBAC.append(TradeContext.I2SBAC[i])
                HostContext.I2ACNM.append(TradeContext.I2ACNM[i])
                HostContext.I2DASQ.append(TradeContext.I2DASQ[i])
                HostContext.I2CFFG.append(TradeContext.I2CFFG[i])
                HostContext.I2PSWD.append(TradeContext.I2PSWD[i])
                HostContext.I2PS16.append(TradeContext.I2PS16[i])
                HostContext.I2IDTY.append(TradeContext.I2IDTY[i])
                HostContext.I2IDNO.append(TradeContext.I2IDNO[i])
                HostContext.I2OPTY.append(TradeContext.I2OPTY[i])
                HostContext.I2CETY.append(TradeContext.I2CETY[i])
                HostContext.I2CCSQ.append(TradeContext.I2CCSQ[i])
                HostContext.I2PKFG.append(TradeContext.I2PKFG[i])
                HostContext.I2TRFG.append(TradeContext.I2TRFG[i])
                HostContext.I2RBAC.append(TradeContext.I2RBAC[i])
                HostContext.I2OTNM.append(TradeContext.I2OTNM[i])
                HostContext.I2CYNO.append(TradeContext.I2CYNO[i])
                HostContext.I2CTFG.append(TradeContext.I2CTFG[i])
                HostContext.I2CATR.append(TradeContext.I2CATR[i])
                HostContext.I2WLBZ.append(TradeContext.I2WLBZ[i])
                HostContext.I2TRAM.append(TradeContext.I2TRAM[i])
                HostContext.I2SMCD.append(TradeContext.I2SMCD[i])
                HostContext.I2CHEX.append(TradeContext.I2CHEX[i])
                HostContext.I2NMFG.append(TradeContext.I2NMFG[i])
                HostContext.I2FZNO.append(TradeContext.I2FZNO[i])
                HostContext.I2AMTT.append(TradeContext.I2AMTT[i])
                HostContext.I2AMST.append(TradeContext.I2AMST[i])
                HostContext.I2APX1.append(TradeContext.I2APX1[i])
                HostContext.I2APX2.append(TradeContext.I2APX2[i])
                HostContext.I2REAC.append(TradeContext.I2REAC[i])
        return True
        
    if (TradeContext.HostCode == '8860'):
        #��ѯ�ʻ���Ϣ
        AfaLoggerFunc.tradeInfo("��ѯ�ʻ���Ϣ")
        HostContext.I1TRCD = TradeContext.I1TRCD
        HostContext.I1SBNO = TradeContext.I1SBNO
        HostContext.I1USID = TradeContext.I1USID
        HostContext.I1AUUS = TradeContext.I1AUUS
        HostContext.I1AUPS = TradeContext.I1AUPS
        HostContext.I1WSNO = TradeContext.I1WSNO
        HostContext.I1ACCN = TradeContext.I1ACCN
        HostContext.I1CYNO = TradeContext.I1CYNO
        return True
    if (TradeContext.HostCode == '8800'):
        #����ƽ̨��ѯ
        AfaLoggerFunc.tradeInfo("����ƽ̨��ѯ")
        HostContext.I1TRCD = TradeContext.I1TRCD
        HostContext.I1SBNO = TradeContext.I1SBNO
        HostContext.I1USID = TradeContext.I1USID
        HostContext.I1AUUS = TradeContext.I1AUUS
        HostContext.I1AUPS = TradeContext.I1AUPS
        HostContext.I1WSNO = TradeContext.I1WSNO
        HostContext.I1STAR = TradeContext.I1STAR
        HostContext.I1RCNM = TradeContext.I1RCNM
        HostContext.I1CTNO = TradeContext.I1CTNO
        return True

    if (TradeContext.HostCode == '8861'):
        #У������
        AfaLoggerFunc.tradeInfo("У������")
        HostContext.I1TRCD = TradeContext.I1TRCD
        HostContext.I1SBNO = TradeContext.I1SBNO
        HostContext.I1USID = TradeContext.I1USID
        HostContext.I1AUUS = TradeContext.I1AUUS
        HostContext.I1AUPS = TradeContext.I1AUPS
        HostContext.I1WSNO = TradeContext.I1WSNO
        HostContext.I1ACCN = TradeContext.I1ACCN
        HostContext.I1CYNO = TradeContext.I1CYNO
        HostContext.I1CKFG = TradeContext.I1CKFG
        #ת����������Ϊ����
        in_data = TradeContext.I1PSWD
        AfaLoggerFunc.tradeInfo("��ʼת������,in_data=[" + in_data + "]")
        out_data = "      "
        ret = jiami.SecEncDecData(0,in_data,out_data)
        if ret != 0:
            AfaLoggerFunc.tradeInfo("����ת��ʧ��,ret=[" + str(ret) + "]")
            return False
        else:
            AfaLoggerFunc.tradeInfo("����ת���ɹ�,out_data=[" + out_data + "]")
            TradeContext.I1PSWD = out_data
        HostContext.I1PSWD = TradeContext.I1PSWD
        return True                                         
                                                            
                                                            
    if (TradeContext.HostCode == '8862'):                   
        #�����޸Ļ�����    
        AfaLoggerFunc.tradeInfo("�����޸Ļ�����")     
        HostContext.I1TRCD = TradeContext.I1TRCD
        HostContext.I1SBNO = TradeContext.I1SBNO
        HostContext.I1USID = TradeContext.I1USID
        HostContext.I1AUUS = TradeContext.I1AUUS
        HostContext.I1AUPS = TradeContext.I1AUPS
        HostContext.I1WSNO = TradeContext.I1WSNO
        HostContext.I1ACCN = TradeContext.I1ACCN
        HostContext.I1CYNO = TradeContext.I1CYNO
        HostContext.I1OPFG = TradeContext.I1OPFG
        HostContext.I1OPKD = TradeContext.I1OPKD
        #ת����������Ϊ����
        in_data = TradeContext.I1PSW1
        AfaLoggerFunc.tradeInfo("��ʼת������,in_data=[" + in_data + "]")
        out_data = "      "
        ret = jiami.SecEncDecData(0,in_data,out_data)
        if ret != 0:
            AfaLoggerFunc.tradeInfo("����ת��ʧ��,ret=[" + str(ret) + "]")
            return False
        else:
            AfaLoggerFunc.tradeInfo("����ת���ɹ�,out_data=[" + out_data + "]")
            HostContext.I1PSW1 = eval(repr(out_data))
        #HostContext.I1PSW1 = TradeContext.I1PSW1
        AfaLoggerFunc.tradeInfo("HostContext.I1PSW1=[" + HostContext.I1PSW1 + "]")
        #ת����������Ϊ����
        in_data = TradeContext.I1PSW2
        AfaLoggerFunc.tradeInfo("��ʼת������,in_data=[" + in_data + "]")
        out_data = "      "
        ret = jiami.SecEncDecData(0,in_data,out_data)
        if ret != 0:
            AfaLoggerFunc.tradeInfo("����ת��ʧ��,ret=[" + str(ret) + "]")
            return False
        else:
            AfaLoggerFunc.tradeInfo("����ת���ɹ�,out_data=[" + out_data + "]")
            HostContext.I1PSW2 = eval(repr(out_data))
        #HostContext.I1PSW2 = TradeContext.I1PSW2                                  
        AfaLoggerFunc.tradeInfo("HostContext.I1PSW1=[" + HostContext.I1PSW1 + "]")
        AfaLoggerFunc.tradeInfo("HostContext.I1PSW2=[" + HostContext.I1PSW2 + "]")
        return True                                         
                                                            
                                                            
    if (TradeContext.HostCode == '8863'):                   
        #��Ҫƾ֤��ʧ  
        AfaLoggerFunc.tradeInfo("��Ҫƾ֤��ʧ")       
        HostContext.I1TRCD = TradeContext.I1TRCD
        HostContext.I1SBNO = TradeContext.I1SBNO
        HostContext.I1USID = TradeContext.I1USID
        HostContext.I1AUUS = TradeContext.I1AUUS
        HostContext.I1AUPS = TradeContext.I1AUPS
        HostContext.I1WSNO = TradeContext.I1WSNO
        HostContext.I1ACCN = TradeContext.I1ACCN
        HostContext.I1CCNO = TradeContext.I1CCNO
        HostContext.I1CYNO = TradeContext.I1CYNO                                  
        return True                                         
                                                            
                                                            
    if (TradeContext.HostCode == '8864'):                   
        #��ѯ�˻���ϸ            
        AfaLoggerFunc.tradeInfo("��ѯ�˻���ϸ")    
        HostContext.I1TRCD = TradeContext.I1TRCD
        HostContext.I1SBNO = TradeContext.I1SBNO
        HostContext.I1USID = TradeContext.I1USID
        HostContext.I1AUUS = TradeContext.I1AUUS
        HostContext.I1AUPS = TradeContext.I1AUPS
        HostContext.I1WSNO = TradeContext.I1WSNO
        HostContext.I1ACCN = TradeContext.I1ACCN
        HostContext.I1CYNO = TradeContext.I1CYNO
        HostContext.I1STDT = TradeContext.I1STDT
        HostContext.I1EDDT = TradeContext.I1EDDT
        HostContext.I1STAR = TradeContext.I1STAR
        HostContext.I1RCNM = TradeContext.I1RCNM                         
        return True   
        
        
    if (TradeContext.HostCode == '8865'):                   
        #��ѯ�ͻ���Ϣ            
        AfaLoggerFunc.tradeInfo("��ѯ�ͻ���Ϣ")    
        HostContext.I1TRCD = TradeContext.I1TRCD
        HostContext.I1SBNO = TradeContext.I1SBNO
        HostContext.I1USID = TradeContext.I1USID
        HostContext.I1AUUS = TradeContext.I1AUUS
        HostContext.I1AUPS = TradeContext.I1AUPS
        HostContext.I1WSNO = TradeContext.I1WSNO
        HostContext.I1CUTY = TradeContext.I1CUTY
        HostContext.I1WDTP = TradeContext.I1WDTP
        HostContext.I1CTNO = TradeContext.I1CTNO
        HostContext.I1IDNO = TradeContext.I1IDNO
        HostContext.I1IDTY = TradeContext.I1IDTY
        return True           
        
        
    if(TradeContext.HostCode == '8866'):
        #֤���Ų�ѯ�˻���ϸ 
        AfaLoggerFunc.tradeInfo("֤���Ų�ѯ�˻���ϸ ")      
        HostContext.I1TRCD = TradeContext.I1TRCD
        HostContext.I1SBNO = TradeContext.I1SBNO
        HostContext.I1USID = TradeContext.I1USID
        HostContext.I1AUUS = TradeContext.I1AUUS
        HostContext.I1AUPS = TradeContext.I1AUPS
        HostContext.I1WSNO = TradeContext.I1WSNO
        HostContext.I1STAR = TradeContext.I1STAR
        HostContext.I1RCNM = TradeContext.I1RCNM
        HostContext.I1IDTY = TradeContext.I1IDTY
        HostContext.I1IDNO = TradeContext.I1IDNO
        #====����I1CETY�ֶ� �ź��޸���20100202=====
        HostContext.I1CETY = TradeContext.I1CETY 
        return True        

   
#====================�������ķ���ֵ����TradeContext��==========
def HostToTrade():   
    if (TradeContext.HostCode == '8813'):
        #ͬ��ת��/���
        AfaLoggerFunc.tradeInfo("ͬ��ת��/���")
        AfaLoggerFunc.tradeDebug("�ӿ�һ")
        #=====�ӿ�һ====
#        TradeContext.O1MGID = HostContext.O1MGID
        TradeContext.O1ACUR = HostContext.O1ACUR
        TradeContext.O1TRDT = HostContext.O1TRDT
        TradeContext.O1TRTM = HostContext.O1TRTM
        TradeContext.O1TLSQ = HostContext.O1TLSQ
        
        AfaLoggerFunc.tradeDebug("�ӿڶ�")
        #=====�ӿڶ�=====
        if(int(HostContext.O1ACUR) != 0):
            TradeContext.O2NBBH = []
            TradeContext.O2FEDT = []
            TradeContext.O2RBSQ = []
            TradeContext.O2TRDT = []
            TradeContext.O2RGSQ = []
            TradeContext.O2TRSQ = []
            TradeContext.O2TINO = []
            TradeContext.O2SBAC = []
            TradeContext.O2ACNM = []
            TradeContext.O2ANTY = []
            TradeContext.O2ACBL = []
            TradeContext.O2OPNT = []
            TradeContext.O2DASQ = []
            TradeContext.O2RBAC = []
            TradeContext.O2OTNM = []
            TradeContext.O2CNTY = []
            TradeContext.O2OTSB = []
            TradeContext.O2AMFG = []
            TradeContext.O2REAC = []
            TradeContext.O2TRSB = []
            TradeContext.O2WLBZ = []
            TradeContext.O2TRAM = []
            TradeContext.O2CYNO = []
            TradeContext.O2CTFG = []
            TradeContext.O2CATR = []
            
        for i in range(0,int(HostContext.O1ACUR)):
            TradeContext.O2NBBH.append(HostContext.O2NBBH[i])
            TradeContext.O2FEDT.append(HostContext.O2FEDT[i])
            TradeContext.O2RBSQ.append(HostContext.O2RBSQ[i])
            TradeContext.O2TRDT.append(HostContext.O2TRDT[i])
            TradeContext.O2RGSQ.append(HostContext.O2RGSQ[i])
            TradeContext.O2TRSQ.append(HostContext.O2TRSQ[i])
            TradeContext.O2TINO.append(HostContext.O2TINO[i])
            TradeContext.O2SBAC.append(HostContext.O2SBAC[i])
            TradeContext.O2ACNM.append(HostContext.O2ACNM[i])
            TradeContext.O2ANTY.append(HostContext.O2ANTY[i])
            if(HostContext.O2ACBL[i].find(".") != -1):      #ȥ������е�С����
                temp = HostContext.O2ACBL[i].split(".")
                HostContext.O2ACBL[i] = temp[0]+temp[1]
            TradeContext.O2ACBL.append(HostContext.O2ACBL[i])
            TradeContext.O2OPNT.append(HostContext.O2OPNT[i])
            TradeContext.O2DASQ.append(HostContext.O2DASQ[i])
            TradeContext.O2RBAC.append(HostContext.O2RBAC[i])
            TradeContext.O2OTNM.append(HostContext.O2OTNM[i])
            TradeContext.O2CNTY.append(HostContext.O2CNTY[i])
            TradeContext.O2OTSB.append(HostContext.O2OTSB[i])
            TradeContext.O2AMFG.append(HostContext.O2AMFG[i])
            TradeContext.O2REAC.append(HostContext.O2REAC[i])
            TradeContext.O2TRSB.append(HostContext.O2TRSB[i])
            TradeContext.O2WLBZ.append(HostContext.O2WLBZ[i])
            if(HostContext.O2TRAM[i].find(".") != -1):      #ȥ������е�С����
                temp = HostContext.O2TRAM[i].split(".")
                HostContext.O2TRAM[i] = temp[0]+temp[1]
            TradeContext.O2TRAM.append(HostContext.O2TRAM[i])
            TradeContext.O2CYNO.append(HostContext.O2CYNO[i])
            TradeContext.O2CTFG.append(HostContext.O2CTFG[i])
            TradeContext.O2CATR.append(HostContext.O2CATR[i])
        return True
############################  ����ƽ̨��ѯ ###############################
    if (TradeContext.HostCode == '8800'):
        
        AfaLoggerFunc.tradeInfo("����ƽ̨��ѯ")
        #AfaLoggerFunc.tradeDebug("����ӿ�һ")
        
        TradeContext.O1MGID = HostContext.O1MGID
        TradeContext.O1ACUR = HostContext.O1ACUR
        TradeContext.O1TRDT = HostContext.O1TRDT
        TradeContext.O1TRTM = HostContext.O1TRTM
        TradeContext.O1TLSQ = HostContext.O1TLSQ
        TradeContext.O1CTNO = HostContext.O1CTNO
        TradeContext.O1CCTY = HostContext.O1CCTY
        TradeContext.O1CUNM = HostContext.O1CUNM
        TradeContext.O1SSEX = HostContext.O1SSEX
        TradeContext.O1OPNT = HostContext.O1OPNT
        TradeContext.O1ADDR = HostContext.O1ADDR
        TradeContext.O1IDTY = HostContext.O1IDTY
        TradeContext.O1IDNO = HostContext.O1IDNO
        TradeContext.O1PCSQ = HostContext.O1PCSQ
               
#        AfaLoggerFunc.tradeDebug("�ӿڶ�")
        #=====�ӿڶ�=====
        if(int(HostContext.O1PCSQ) != 0):
            TradeContext.O2ACNO = []
            TradeContext.O2AMCR = []
            TradeContext.O2KZBZ = []
            TradeContext.O2SBNO = []
            TradeContext.O2APID = []
            TradeContext.O2BAFG = []
            TradeContext.O2STCD = []
            TradeContext.O2OTH1 = []
            TradeContext.O2OTH2 = []
            for i in range(0,int(HostContext.O1PCSQ)):
                TradeContext.O2ACNO.append(HostContext.O2ACNO[i])
                TradeContext.O2AMCR.append(HostContext.O2AMCR[i])
                TradeContext.O2KZBZ.append(HostContext.O2KZBZ[i])
                TradeContext.O2SBNO.append(HostContext.O2SBNO[i])
                TradeContext.O2APID.append(HostContext.O2APID[i])
                TradeContext.O2BAFG.append(HostContext.O2BAFG[i])
                TradeContext.O2STCD.append(HostContext.O2STCD[i])
                TradeContext.O2OTH1.append(HostContext.O2OTH1[i])
                TradeContext.O2OTH2.append(HostContext.O2OTH2[i])

        return True
###########################################################        
    if (TradeContext.HostCode == '8860'):
        #��ѯ�ʻ���Ϣ
        AfaLoggerFunc.tradeInfo("��ѯ�ʻ���Ϣ")
#        TradeContext.O1MGID = HostContext.O1MGID
        TradeContext.O1ACUR = HostContext.O1ACUR
        TradeContext.O1TRDT = HostContext.O1TRDT
        TradeContext.O1TRTM = HostContext.O1TRTM
        TradeContext.O1TLSQ = HostContext.O1TLSQ
        TradeContext.O1ACCN = HostContext.O1ACCN
        TradeContext.O1CUNO = HostContext.O1CUNO
        TradeContext.O1CUNM = HostContext.O1CUNM
        TradeContext.O1IDTY = HostContext.O1IDTY
        TradeContext.O1IDNO = HostContext.O1IDNO
        TradeContext.O1OPNT = HostContext.O1OPNT
        TradeContext.O1TOBN = HostContext.O1TOBN
        TradeContext.O1CCNO = HostContext.O1CCNO
        TradeContext.O1OPDT = HostContext.O1OPDT
        TradeContext.O1MADT = HostContext.O1MADT
        TradeContext.O1CLDT = HostContext.O1CLDT
        TradeContext.O1PERD = HostContext.O1PERD
        TradeContext.O1ACNM = HostContext.O1ACNM
        TradeContext.O1ACSY = HostContext.O1ACSY
        TradeContext.O1CYNO = HostContext.O1CYNO
        TradeContext.O1ACST = HostContext.O1ACST
        if(HostContext.O1ACBL.find(".") != -1):    #ȥ������е�С����
            HostContext.O1ACBL = HostContext.O1ACBL.split(".")
            TradeContext.O1ACBL = HostContext.O1ACBL[0]+HostContext.O1ACBL[1]
        else:
            TradeContext.O1ACBL = HostContext.O1ACBL
        if(HostContext.O1CUBL.find(".") != -1):    #ȥ������е�С����
            HostContext.O1CUBL = HostContext.O1CUBL.split(".")
            TradeContext.O1CUBL = HostContext.O1CUBL[0]+HostContext.O1CUBL[1]
        else:
            TradeContext.O1CUBL = HostContext.O1CUBL
        
        AfaLoggerFunc.tradeInfo("O1ACBL======"+str(TradeContext.O1ACBL))
        AfaLoggerFunc.tradeInfo("O1CUBL======"+str(TradeContext.O1CUBL))
        
        TradeContext.O1BLDE = HostContext.O1BLDE
        if(HostContext.O1EVAM.find(".") != -1):    #ȥ������е�С����
            HostContext.O1EVAM = HostContext.O1EVAM.split(".")
            TradeContext.O1EVAM = HostContext.O1EVAM[0]+HostContext.O1EVAM[1]
        else:
            TradeContext.O1EVAM = HostContext.O1EVAM
        TradeContext.O1SYAN = HostContext.O1SYA2    #�������ص��ֶ���O1SYAN��ΪO1SYN2     20090325
        TradeContext.O1ITCD = HostContext.O1ITCD
        TradeContext.O1ITEM = HostContext.O1ITEM
        return True


    if (TradeContext.HostCode == '8861'):
        #У������
        AfaLoggerFunc.tradeInfo("У������")
#        TradeContext.O1MGID = HostContext.O1MGID
        TradeContext.O1ACUR = HostContext.O1ACUR
        TradeContext.O1TRDT = HostContext.O1TRDT
        TradeContext.O1TRTM = HostContext.O1TRTM
        TradeContext.O1TLSQ = HostContext.O1TLSQ
        TradeContext.O1ACCN = HostContext.O1ACCN
        TradeContext.O1CFFG = HostContext.O1CFFG
        TradeContext.O1PWFG = HostContext.O1PWFG
        return True                                         
                                                            
                                                            
    if (TradeContext.HostCode == '8862'):                   
        #�����޸Ļ�����    
        AfaLoggerFunc.tradeInfo("�����޸Ļ�����")        
#        TradeContext.O1MGID = HostContext.O1MGID
        TradeContext.O1ACUR = HostContext.O1ACUR
        TradeContext.O1TRDT = HostContext.O1TRDT
        TradeContext.O1TRTM = HostContext.O1TRTM
        TradeContext.O1TLSQ = HostContext.O1TLSQ
        TradeContext.O1ACCN = HostContext.O1ACCN                               
        return True                                         
                                                            
                                                            
    if (TradeContext.HostCode == '8863'):                   
        #��Ҫƾ֤��ʧ         
        AfaLoggerFunc.tradeInfo("��Ҫƾ֤��ʧ ")     
#        TradeContext.O1MGID = HostContext.O1MGID
        TradeContext.O1ACUR = HostContext.O1ACUR
        TradeContext.O1TRDT = HostContext.O1TRDT
        TradeContext.O1TRTM = HostContext.O1TRTM
        TradeContext.O1TLSQ = HostContext.O1TLSQ
        TradeContext.O1ACCN = HostContext.O1ACCN
        TradeContext.O1CCNO = HostContext.O1CCNO                             
        return True                                         
                                                            
                                                            
    if (TradeContext.HostCode == '8864'):                   
        #��ѯ�˻���ϸ  
        AfaLoggerFunc.tradeInfo("��ѯ�˻���ϸ") 
        AfaLoggerFunc.tradeDebug("�ӿ�һ")
        #=====�ӿ�һ====
#        TradeContext.O1MGID = HostContext.O1MGID
        TradeContext.O1ACUR = HostContext.O1ACUR
        TradeContext.O1TRDT = HostContext.O1TRDT
        TradeContext.O1TRTM = HostContext.O1TRTM
        TradeContext.O1TLSQ = HostContext.O1TLSQ
        TradeContext.O1ACCN = HostContext.O1ACCN
        TradeContext.O1CCNO = HostContext.O1CCNO
        AfaLoggerFunc.tradeDebug("�ӿڶ�")
        #=====�ӿڶ�====
        if(int(HostContext.O1ACUR) != 0):
            TradeContext.O2ACCN = []
            TradeContext.O2ORDT = []
            TradeContext.O2ERTM = []
            TradeContext.O2ORTC = []
            TradeContext.O2AMCD = []
            TradeContext.O2TRAM = []
            TradeContext.O2ACBL = []
            TradeContext.O2TRSN = []
            TradeContext.O2ORUS = []
            TradeContext.O2ORAU = []
            TradeContext.O2ORTS = []
            TradeContext.O2CATR = []
            TradeContext.O2SMCD = []
            TradeContext.O2CHEX = []
            TradeContext.O2RVSB = []
            TradeContext.O2CCNO = []
            
        
        for i in range(0,int(HostContext.O1ACUR)):
            TradeContext.O2ACCN.append(HostContext.O2ACCN[i])
            TradeContext.O2ORDT.append(HostContext.O2ORDT[i])
            TradeContext.O2ERTM.append(HostContext.O2ERTM[i])
            TradeContext.O2ORTC.append(HostContext.O2ORTC[i])
            TradeContext.O2AMCD.append(HostContext.O2AMCD[i])
            if(HostContext.O2TRAM[i].find(".") != -1):    #ȥ������е�С����
               temp = HostContext.O2TRAM[i].split(".")
               HostContext.O2TRAM[i] = temp[0].lstrip("-")+temp[1] 
            TradeContext.O2TRAM.append(HostContext.O2TRAM[i])
            if(HostContext.O2ACBL[i].find(".") != -1):     #ȥ������е�С����
               temp = HostContext.O2ACBL[i].split(".")
               HostContext.O2ACBL[i] = temp[0]+temp[1] 
            TradeContext.O2ACBL.append(HostContext.O2ACBL[i])
            TradeContext.O2TRSN.append(HostContext.O2TRSN[i])
            TradeContext.O2ORUS.append(HostContext.O2ORUS[i])
            TradeContext.O2ORAU.append(HostContext.O2ORAU[i])
            TradeContext.O2ORTS.append(HostContext.O2ORTS[i])
            TradeContext.O2CATR.append(HostContext.O2CATR[i])
            TradeContext.O2SMCD.append(HostContext.O2SMCD[i])
            TradeContext.O2CHEX.append(HostContext.O2CHEX[i])
            TradeContext.O2RVSB.append(HostContext.O2RVSB[i])
            TradeContext.O2CCNO.append(HostContext.O2CCNO[i])                                    
        return True           
        
    if (TradeContext.HostCode == '8865'):
        #��ѯ�ͻ���Ϣ
        AfaLoggerFunc.tradeInfo("��ѯ�ͻ���Ϣ")
        TradeContext.O1MGID = HostContext.O1MGID
        TradeContext.O1ACUR = HostContext.O1ACUR
        TradeContext.O1TRDT = HostContext.O1TRDT
        TradeContext.O1TRTM = HostContext.O1TRTM
        TradeContext.O1TLSQ = HostContext.O1TLSQ
        TradeContext.O1CTNO = HostContext.O1CTNO
        TradeContext.O1CUNM = HostContext.O1CUNM
        TradeContext.O1ALNM = HostContext.O1ALNM
        TradeContext.O1ENEM = HostContext.O1ENEM
        TradeContext.O1SEKD = HostContext.O1SEKD
        TradeContext.O1SHFG = HostContext.O1SHFG
        TradeContext.O1OPUS = HostContext.O1OPUS
        TradeContext.O1OPNT = HostContext.O1OPNT
        TradeContext.O1OPDT = HostContext.O1OPDT
        TradeContext.O1SSEX = HostContext.O1SSEX
        TradeContext.O1BDAY = HostContext.O1BDAY
        TradeContext.O1IDTY = HostContext.O1IDTY
        TradeContext.O1IDNO = HostContext.O1IDNO
        TradeContext.O1IDUN = HostContext.O1IDUN
        TradeContext.O1ADDR = HostContext.O1ADDR
        TradeContext.O1ENAD = HostContext.O1ENAD
        TradeContext.O1WKUT = HostContext.O1WKUT
        TradeContext.O1POCD = HostContext.O1POCD
        TradeContext.O1TLNO = HostContext.O1TLNO
        TradeContext.O1FXNO = HostContext.O1FXNO
        TradeContext.O1PREF = HostContext.O1PREF
        TradeContext.O1POSI = HostContext.O1POSI
        return True     
        
    if(TradeContext.HostCode == '8866'):  
        #֤���Ų�ѯ�˻���ϸ 
        AfaLoggerFunc.tradeInfo("֤���Ų�ѯ�˻���ϸ") 
        AfaLoggerFunc.tradeInfo("�ӿ�һ")    
        #�ӿ�һ 
        TradeContext.O1MGID = HostContext.O1MGID     
        TradeContext.O1ACUR = HostContext.O1ACUR 
        TradeContext.O1TRDT = HostContext.O1TRDT 
        TradeContext.O1TRTM = HostContext.O1TRTM                          
        #�ӿڶ�
        if(int(HostContext.O1ACUR) != 0):
            AfaLoggerFunc.tradeInfo("�ӿڶ�")
            TradeContext.O2ACCN = []
            TradeContext.O2ACC1 = []
            TradeContext.O2SVAC = []
            TradeContext.O2ACNO = []
            TradeContext.O2CETY = []
            TradeContext.O2CCSQ = []
            TradeContext.O2WDDS = []
            TradeContext.O2BKDS = []
            TradeContext.O2SEDT = []
            
        for i in range(0,int(HostContext.O1ACUR)):
            TradeContext.O2ACCN.append(HostContext.O2ACCN[i])
            TradeContext.O2ACC1.append(HostContext.O2ACC1[i])
            TradeContext.O2SVAC.append(HostContext.O2SVAC[i])
            TradeContext.O2ACNO.append(HostContext.O2ACNO[i])
            TradeContext.O2CETY.append(HostContext.O2CETY[i])
            TradeContext.O2CCSQ.append(HostContext.O2CCSQ[i])
            TradeContext.O2WDDS.append(HostContext.O2WDDS[i])
            TradeContext.O2BKDS.append(HostContext.O2BKDS[i])
            TradeContext.O2SEDT.append(HostContext.O2SEDT[i])
        return True

   

#====================���������ݽ���=============================
def CommHost( result = None ):

    AfaLoggerFunc.tradeInfo('>>>����ͨѶ����[CommHost]')
        
    TradeContext.errorCode = 'H999'
    TradeContext.errorMsg  = 'ϵͳ�쳣(������ͨѶ)'

    if (result == '8813'):
        AfaLoggerFunc.tradeInfo('>>>���ʼ���')
        mapfile=os.environ['AFAP_HOME'] + '/conf/hostconf/AH8813.map'
        TradeContext.HostCode = '8813'
        InitGLHostReq()

    elif (result == '8860'):
        AfaLoggerFunc.tradeInfo('>>>��ѯ�ʻ���Ϣ')
        mapfile=os.environ['AFAP_HOME'] + '/conf/hostconf/AH8860.map'
        TradeContext.HostCode = '8860'
        InitGLHostReq()
    elif (result == '8800'):
        AfaLoggerFunc.tradeInfo('>>>����ƽ̨��ѯ')
        mapfile=os.environ['AFAP_HOME'] + '/conf/hostconf/AH8800.map'
        TradeContext.HostCode = '8800'
        InitGLHostReq()           
    elif (result == '8861'):
        AfaLoggerFunc.tradeInfo('>>>У������')
        mapfile=os.environ['AFAP_HOME'] + '/conf/hostconf/AH8861.map'
        TradeContext.HostCode = '8861'
        InitGLHostReq()

    elif (result == '8862'):
        AfaLoggerFunc.tradeInfo('>>>�����޸Ļ�����')
        mapfile=os.environ['AFAP_HOME'] + '/conf/hostconf/AH8862.map'
        TradeContext.HostCode = '8862'
        InitGLHostReq()

    elif (result == '8863'):
        AfaLoggerFunc.tradeInfo('>>>��Ҫƾ֤��ʧ')
        mapfile=os.environ['AFAP_HOME'] + '/conf/hostconf/AH8863.map'
        TradeContext.HostCode = '8863'
        InitGLHostReq()

    elif (result == '8864'):
        AfaLoggerFunc.tradeInfo('>>>��ѯ�˻���ϸ')
        mapfile=os.environ['AFAP_HOME'] + '/conf/hostconf/AH8864.map'
        TradeContext.HostCode = '8864'
        InitGLHostReq()
        
    elif(result == '8865'):
        AfaLoggerFunc.tradeInfo('>>>��ѯ�ͻ���Ϣ')
        mapfile=os.environ['AFAP_HOME'] + '/conf/hostconf/AH8865.map'
        TradeContext.HostCode = '8865'
        InitGLHostReq()
        
    elif(result == '8866'):
        AfaLoggerFunc.tradeInfo('>>>֤���Ų�ѯ�˻���ϸ')
        mapfile=os.environ['AFAP_HOME'] + '/conf/hostconf/AH8866.map'
        TradeContext.HostCode = '8866'
        InitGLHostReq()

    else:
        TradeContext.errorCode = 'A9999'
        TradeContext.errorMsg  = '�����������'
        return False

    #�˴����״���Ҫ��10λ,�Ҳ��ո�
    HostComm.callHostTrade( mapfile, UtilTools.Rfill(TradeContext.HostCode,10,' ') ,'0002' )

    if HostContext.host_Error:
        AfaLoggerFunc.tradeFatal( 'host_Error:'+str( HostContext.host_ErrorType )+':'+HostContext.host_ErrorMsg )

        if HostContext.host_ErrorType != 5 :
            TradeContext.__status__='1'
            TradeContext.errorCode='A0101'
            TradeContext.errorMsg=HostContext.host_ErrorMsg
        else :
            TradeContext.__status__='2'
            TradeContext.errorCode='A0102'
            TradeContext.errorMsg=HostContext.host_ErrorMsg
        return False

    #================�����������ذ�====================
    return HostParseRet(result )


#================�����������ذ�====================
def HostParseRet( hostType ):

    if (HostContext.host_Error == True):    #����ͨѶ����
        TradeContext.__status__='2'
        TradeContext.errorCode, TradeContext.errorMsg = 'A9998', '����ͨѶ����'
        TradeContext.bankCode  = HostContext.host_ErrorType                       #ͨѶ�������
        return False

    if( HostContext.O1MGID == 'AAAAAAA' ): #�ɹ�
        TradeContext.__status__='0'
        TradeContext.errorCode, TradeContext.errorMsg = '0000', '�����ɹ�'
        #=====�����8866���������ɹ�������������O1TLSQ�ֶ�====
        if HostContext.existVariable('O1TLSQ'):
            TradeContext.bankSerno = HostContext.O1TLSQ                               #��Ա��ˮ��

        TradeContext.bankCode  = HostContext.O1MGID                               #�������ش���
        HostToTrade()
        return True

    else:                                  #ʧ��
        TradeContext.__status__='1'
        TradeContext.errorCode, TradeContext.errorMsg = HostContext.O1MGID, HostContext.O1INFO
        return False
