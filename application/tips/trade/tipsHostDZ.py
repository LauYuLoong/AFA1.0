# -*- coding: gbk -*-
################################################################################
#   ��˰����ϵͳ��ϵͳ������.TIPS����Ľ��ж���
#===============================================================================
#   �����ļ�:   tipsHostDZ.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  �ر��
#   �޸�ʱ��:   2009-11-09
#   �� �� �ߣ�  ������
#   �޸����ڣ�  2011-5-16
#   �޸����ݣ�  ����������ʱ��������ѯ����ˮ�����������״̬���жϵ������Ƿ���
#               ���ˣ���������Ѷ��ˣ������������ֱ���޸�״̬Ϊ���˳ɹ���
#               ��δ���ˣ������Ѽ��ˣ�����Ҫ�������
################################################################################
import TradeContext
TradeContext.sysType = 'tips'
TradeContext.TransCode = 'tipsHostDZ'
import AfaUtilTools,AfaDBFunc,os,sys,AfaFtpFunc
import TipsHostFunc,TipsFunc
from types import *
from tipsConst import *

if __name__ == '__main__':
    
    try:
        TipsFunc.WrtLog("***��˰����ϵͳ: ϵͳ������.TIPS����Ľ��ж���[tipsHostDZ]����***")
        
        if(len(sys.argv)==2):
            TradeContext.chkDate=sys.argv[1]
        else:
            #=============��ȡ��ǰϵͳʱ��====================
            #TradeContext.workDate='20110713'
            TradeContext.workDate=AfaUtilTools.GetSysDate( )
            TradeContext.chkDate =TradeContext.workDate
        
        #==========��������ǰ����==============================================
        TradeContext.sBrNo    = TIPS_SBNO_QS                    #���׻�����
        TradeContext.sTeller  = TIPS_TELLERNO_AUTO              #���׹�Ա��
        TradeContext.sTermId  = '123456'                        #�ն˺�  
        TradeContext.sOpeFlag = '2'                            #������־0-	�����ռ��������˻����ļ� 1-�����ռ�����ļ� 2-�������ж��˱���
        TradeContext.entrustDate = TradeContext.chkDate        #�������� 
            
        
        #�����������������ļ�===========================================================================
        TipsFunc.WrtLog('>>>8833�����������������ļ�')
        if not TipsHostFunc.CommHost('8833'):
            TipsFunc.exitMainFlow()
        TipsFunc.WrtLog("errorMsg = [" + TradeContext.errorMsg + "]")
        if TradeContext.errorCode != '0000':
            TipsFunc.exitMainFlow()
        
        #�������������ļ�===========================================================================
        TipsFunc.WrtLog('>>>�������������ļ�')
        #if(not TipsFunc.getHost('TPRZA','BANKMDS')):
        if (not AfaFtpFunc.getFile("TIPS_DZ","TPRZA","TPRZA")):
            TradeContext.errorCode, TradeContext.errorMsg = "S999","�������������ļ��쳣"
            TipsFunc.exitMainFlow()
        
        sFileName = '/home/maps/afa/data/batch/tips/TPRZA'
        dFileName = '/home/maps/afa/data/batch/tips/TIPS_DZ_' + TradeContext.chkDate+ '.txt'
        fFileFld = 'tprza.fld'
           
        #ת��=======================================================================================
        TipsFunc.WrtLog('>>>ת��')
        if not TipsFunc.FormatFile("0",sFileName,dFileName,fFileFld):
            TradeContext.errorCode, TradeContext.errorMsg= "S999","ת�������ļ������쳣"
            TipsFunc.exitMainFlow()
            
        #ƥ�������ϸ
        TipsFunc.WrtLog('>>>ƥ�������ϸ')
        
        t_sum=0   #�ܱ���
        t_amt=0.00 #�ܽ��
        s_sum=0   #��������ܱ���
        s_amt=0.00 #��������ܽ��
        u_sum=0    #���˲����ܱ���
        u_amt=0.00 #���˲����ܽ��
        
        file_name = 'TIPS_DZ_' + TradeContext.chkDate+'.txt'
        file_path = os.environ['AFAP_HOME'] + "/data/batch/tips/"
        rb = open(file_path + file_name , 'r')
        #��ȡһ��
        lineBuf = rb.readline()
        iLine=0
        while ( len(lineBuf) > 87 ):
            iLine=iLine+1
            sItemBuf = lineBuf.split('<fld>')         
            
            if ( len(sItemBuf) < 7 ):
                rb.close() 
                TipsFunc.ExitThisFlow( '9000', '�����ļ���ʽ����(' + file_name + ')')    
                TradeContext.errorCode, TradeContext.errorMsg= "S999",'�����ļ���ʽ����(' + file_name + ')'
                TipsFunc.exitMainFlow()
            
            
            workdate =   sItemBuf[0].strip()    #��������
            serialno =   sItemBuf[1].strip()    #��ˮ��
            daccno   =   sItemBuf[2].strip()    #�跽�ʺ�
            caccno   =   sItemBuf[3].strip()    #�����ʺ�	
            amount   =   sItemBuf[4].strip()    #������
            wlbz     =   sItemBuf[5].strip()    #������־
            status   =   sItemBuf[6].strip()    #��¼״̬
            
            if status != "0":
                lineBuf = rb.readline()
                continue
            
            t_sum=t_sum+1
            t_amt=t_amt+float(amount)
                
            #ƥ���м�ҵ����ϸ
            #===== modify by liu.yl at 2011/5/16 ====
            #===== ������ѯ�ֶ�corpchkflg ====
            #sql_s = "select taxpaycode,amount,serialno,zoneno,brno,tellerno,bankstatus from tips_maintransdtl where workdate='"+workdate+"' and serialno='"+serialno+"'"
            sql_s = "select taxpaycode,amount,serialno,zoneno,brno,tellerno,bankstatus,corpchkflag from tips_maintransdtl "
            sql_s = sql_s + "where workdate='"+workdate+"' and serialno='"+serialno+"'"            
            #===== end of modify ====
            
            sql_s = sql_s + " and revtranf='0'"
            records_s=AfaDBFunc.SelectSql(sql_s)
            if records_s==None:
                TipsFunc.WrtLog(sql_s)
                TradeContext.errorCode, TradeContext.errorMsg= "S999",'���ݿ��쳣'
                TipsFunc.exitMainFlow()
            elif(len(records_s)==0):
               TipsFunc.WrtLog('�м�ҵ��ƽ̨�޴˽�����ˮ'+serialno+',�޷��Զ�����')
               u_sum=u_sum+1
               u_amt=u_amt+float(records_s[0][1])
               
               lineBuf = rb.readline()
               continue
            else:
                if records_s[0][6] != "0":
                    TipsFunc.WrtLog("�˽�����ˮ"+serialno+",�м�ҵ��ƽ̨δ����,�����Ѽ���,�жϵ�����״̬�Ƿ����")
                    
                    #===== add by liu.yl at 2011/5/17 ====
                    #===== �����ж������Ƿ������� ====
                    #===== �����в������,�����Ѽ��˳ɹ�(������˱�ʾ�ɹ�),ֱ���޸ļ�¼״̬Ϊ�ɹ� ====
                    #===== �����в��������,�޸ļ�¼״̬Ϊ�ɹ�,������� ====
                    if records_s[0][7] == "0":
                        TipsFunc.WrtLog("�˽�����ˮ"+serialno+",������������ˣ�����ԭ��������״̬Ϊ���˳ɹ�")
                        #���½�������״̬Ϊ���˳ɹ�
                        sql_u="update tips_maintransdtl set bankstatus = '0',chkflag='0',errormsg = '����ʱǿ�������ɹ�' "
                        sql_u=sql_u + "where workdate = '" + workdate + "' and serialno = '" + serialno + "'"
                    
                        rec = AfaDBFunc.UpdateSqlCmt(sql_u)
                        if rec < 0:
                            TipsFunc.WrtLog(sql_u)
                            TradeContext.errorCode, TradeContext.errorMsg = "S999",'���ݿ��쳣'
                            TipsFunc.exitMainFlow()

                        s_sum=s_sum+1
                        s_amt=s_amt+float(records_s[0][1])

                        lineBuf = rb.readline()
                        continue
                    else:
                        TipsFunc.WrtLog("�˽�����ˮ"+serialno+",������δ������ˣ�����ԭ��������״̬Ϊ���˳ɹ�,Ȼ���Զ�����")
                    #===== end of add ====
                    
                    #���½�������״̬Ϊ���˳ɹ�
                    sql_u = "update tips_maintransdtl set bankstatus = '0',errormsg = '����ʱǿ�������ɹ�������'"
                    sql_u = sql_u + "where workdate = '" + workdate + "' and serialno = '" + serialno + "'"
                    
                    rec = AfaDBFunc.UpdateSqlCmt(sql_u)
                    if rec < 0:
                        TipsFunc.WrtLog(sql_u)
                        TradeContext.errorCode, TradeContext.errorMsg = "S999",'���ݿ��쳣'
                        TipsFunc.exitMainFlow()
                    
                    #�Զ����˳�ʼ��
                    TradeContext.taxPayCode     =records_s[0][0]   #�û���
                    TradeContext.amount         =records_s[0][1]   #���
                    TradeContext.preAgentSerno  =records_s[0][2]   #ԭ������ˮ��
                    TradeContext.zoneno         =records_s[0][3]    
                    TradeContext.brno           =records_s[0][4]    
                    TradeContext.teller         =records_s[0][5] 
                    
                    TradeContext.channelCode = '007'
                    TradeContext.workDate = TradeContext.chkDate
                    TradeContext.workTime = AfaUtilTools.GetSysTime( )
                    TradeContext.appNo      ='AG2010'
                    TradeContext.busiNo     ='00000000000001'
                    
                    TradeContext.TransCode = 'tipsHostDZ'
                    
                    #============У�鹫���ڵ����Ч��==================
                    if ( not TipsFunc.Cancel_ChkVariableExist( ) ):
                        TipsFunc.exitMainFlow()
                    
                    #=============�жϷ����������Ƿ�ƥ��ԭ����====================
                    if( not TipsFunc.ChkRevInfo( TradeContext.preAgentSerno ) ):
                        TipsFunc.exitMainFlow()
                    
                    #=============��ȡƽ̨��ˮ��====================
                    if( not TipsFunc.GetSerialno( ) ):
                        TipsFunc.exitMainFlow()
                    
                    #=============������ˮ��====================
                    if( not TipsFunc.InsertDtl( ) ):
                        TipsFunc.exitMainFlow()
                    
                    #=============������ͨѶ====================
                    TipsFunc.CommHost( )
                    
                    errorCode=TradeContext.errorCode
                    if TradeContext.errorCode=='SXR0010' :  #ԭ���������ѳ��������ɳɹ�����
                        TradeContext.__status__='0'
                        TradeContext.errorCode, TradeContext.errorMsg = '0000', '�����ɹ�'
                    
                    #=============���½�����ˮ====================
                    if( not TipsFunc.UpdateDtl( 'TRADE' ) ):
                        if errorCode == '0000':
                            TradeContext.errorMsg='ȡ�����׳ɹ� '+TradeContext.errorMsg
                        TipsFunc.exitMainFlow()
                    
                    #===== add by liu.yl at 2011/5/16 ====
                    #===== ���½�������״̬Ϊ�����ɹ� ====
                    if TradeContext.errorCode == '0000':
                        sql_u = "update tips_maintransdtl set bankstatus = '3',chkflag='9',errormsg = '����ʱ�ɹ�����'"
                        sql_u = sql_u + "where workdate = '" + workdate + "' and serialno = '" + serialno + "'"
                    
                        rec = AfaDBFunc.UpdateSqlCmt(sql_u)
                        if rec < 0:
                            TipsFunc.WrtLog(sql_u)
                            TradeContext.errorCode, TradeContext.errorMsg = "S999",'���ݿ��쳣'
                            TipsFunc.exitMainFlow()
                    #===== end of add ====
                        
                    u_sum=u_sum+1
                    u_amt=u_amt+float(records_s[0][1])
                else:
                    TipsFunc.WrtLog("�˽�����ˮ"+serialno+",���˳ɹ�")

                    s_sum=s_sum+1
                    s_amt=s_amt+float(records_s[0][1])
                    
                    #������������״̬
                    sql_u = "update tips_maintransdtl set chkflag = '0' where workdate = '" + workdate + "' and serialno = '" + serialno + "'"
                    rec = AfaDBFunc.UpdateSqlCmt(sql_u)
                    if rec < 0:
                        TipsFunc.WrtLog(sql_u)
                        TradeContext.errorCode, TradeContext.errorMsg = "S999",'���ݿ��쳣'
                        TipsFunc.exitMainFlow()

            #��ȡ��һ��
            lineBuf = rb.readline()
        
        TipsFunc.WrtLog('>>>���˽���')
        TipsFunc.WrtLog('>>>    ��������:' + TradeContext.chkDate)
        TipsFunc.WrtLog('>>>      �ܱ���:' + str(t_sum) + '          �ܽ��:' + str(t_amt))   
        TipsFunc.WrtLog('>>>�����������:' + str(s_sum) + '    ����������:' + str(s_amt))  
        TipsFunc.WrtLog('>>>���˲�������:' + str(u_sum) + '    ���˲������:' + str(u_amt))  
        
        TipsFunc.WrtLog("***��˰����ϵͳ: ϵͳ������.TIPS����Ľ��ж���[tipsHostDZ]����***")
    
    except Exception, e:
        #�����쳣

        if( not TradeContext.existVariable( "errorCode" ) or str(e) ):
            TradeContext.errorCode = 'A9999'
            TradeContext.errorMsg = 'ϵͳ����['+ str(e) +']'

        if TradeContext.errorCode != '0000' :
            TipsFunc.WrtLog( 'errorCode=['+TradeContext.errorCode+']' )
            TipsFunc.WrtLog( 'errorMsg=['+TradeContext.errorMsg+']' )
            TipsFunc.WrtLog('tipsHostDZ�����ж�')

        sys.exit(-1)
