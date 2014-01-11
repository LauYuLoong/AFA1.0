#  -*- coding: gbk -*-
##################################################################
#   �м�ҵ��ƽ̨.����ͨ���ݿ������
#=================================================================
#   �����ļ�:   AfaybtDb.py
#   �޸�ʱ��:   2010-07-28
#   ��    ��:   Agree
##################################################################
import TradeContext,AfaLoggerFunc,AfaDBFunc,AfaUtilTools,AfaFlowControl,TransBillFunc,AfaFunc
from types import *


################################################################################
# �� �� ��: AdbInsertQueDtl
# ����˵��: ����ͨ ������Ϣ�Ǽ���ˮ
# �޸ļ�¼��
# ����ֵ��    True  ������ˮ��ɹ�    False ������ˮ��ʧ��
# ����˵����  ����ˮ��Ϣ������ˮ��
################################################################################
def AdbInsertQueDtl( ):
    AfaLoggerFunc.tradeInfo( '>>>>>>>��ʼ��������ͨ��Ϣ��: [ybt_info ]<<<<<<<')
    
    #��ˮ�������-1
    count=42
    TransDtl=[[]]*( count+1 )
   
    #�м�ҵ����Ϣ
    TransDtl[0] = TradeContext.agentSerialno                              # AGENTSERIALNO ����ҵ����ˮ��
    TransDtl[1] = TradeContext.sysId                                      # SYSID         ϵͳ��ʶ
    TransDtl[2] = TradeContext.workDate                                   # WORKDATE      ��������
    TransDtl[3] = TradeContext.workTime                                   # WORKTIME      ����ʱ��
    TransDtl[4] = TradeContext.brno                                       # BRNO          ���׻���
    TransDtl[5] = TradeContext.tellerno                                   # TELLERNO      ��Ա��
    
    #Ͷ����Ϣ
    TransDtl[6] = TradeContext.unitno                                     # unitno        ���չ�˾����
    TransDtl[7] = TradeContext.tb_date                                    # tb_date       Ͷ������
    TransDtl[8] = TradeContext.applno                                     # applno        Ͷ������
    TransDtl[9] =TradeContext.I1CETY                                      #pz_type        ƾ֤����
    TransDtl[10] = TradeContext.userno                                    # bd_print_no   ����ӡˢ�ţ�ƾ֤�ţ� 
    TransDtl[11] =TradeContext.amount                                     #amount       Ӧ�ɱ���
    
    #��ʼ��TransDtl[12]��TransDtl[14]
    TransDtl[12] = ''
    TransDtl[14] = ''
    
    #AfaLoggerFunc.tradeInfo('------------test1-----------------')
    
    #������Ϣ������|�����գ�                             
    if( TradeContext.existVariable( "productid" ) ):                      #productid      ��������
        TransDtl[12] = TransDtl[12] + TradeContext.productid.strip()
    TransDtl[12] = TransDtl[12] + "|"
    
    if ( TradeContext.existVariable( "productid1" ) ):                    #productid1    ��������
        TransDtl[12] = TransDtl[12] + TradeContext.productid1.strip()
   
    #�����ڼ�����  
    if( TradeContext.existVariable( "pre_tormtype" ) ):                   #tormtype     �����ڼ�����   
        TransDtl[13] = TradeContext.pre_tormtype  
    
    #�����ڼ�
    if( TradeContext.existVariable( "coverage_year" ) ):                  #�����ڼ� ����ݻ���ʼ���ڣ�            
        TransDtl[14] = TransDtl[14] + TradeContext.coverage_year.strip()
    TransDtl[14] = TransDtl[14] + "|"
    
    if ( TradeContext.existVariable( "TermDate" ) ):                      #��ֹ���� 
        TransDtl[14] = TransDtl[14] + TradeContext.TermDate.strip()    
                              
    if( TradeContext.existVariable( "paydatelimit" ) ):                   #�ɷ�����
        TransDtl[15] = TradeContext.paydatelimit
          
    if( TradeContext.existVariable( "pre_paymethod" ) ):                  #�ɷѷ�ʽ
        TransDtl[16] = TradeContext.pre_paymethod
    
    #Ͷ������Ϣ
    if( TradeContext.existVariable( "tbr_name" ) ):                       #Ͷ��������
        TransDtl[17] = TradeContext.tbr_name
    
    if( TradeContext.existVariable( "pre_tbr_sex" ) ):                    #Ͷ�����Ա�
        TransDtl[18] = TradeContext.pre_tbr_sex
    
    if( TradeContext.existVariable( "tbr_birth" ) ):                      #Ͷ��������
        TransDtl[19] = TradeContext.tbr_birth
    
    if( TradeContext.existVariable( "pre_tbr_idtype" ) ):                     #Ͷ����֤������
        TransDtl[20] = TradeContext.pre_tbr_idtype
    
    if( TradeContext.existVariable( "tbr_idno" ) ):                       #Ͷ����֤������
        TransDtl[21] = TradeContext.tbr_idno
    
    if( TradeContext.existVariable( "tbr_addr" ) ):                       #Ͷ���˵�ַ
        TransDtl[22] = TradeContext.tbr_addr
   
    if( TradeContext.existVariable( "tbr_postcode" ) ):                   #Ͷ�����ʱ�
        TransDtl[23] = TradeContext.tbr_postcode
    
    if( TradeContext.existVariable( "tbr_tel" ) ):                        #Ͷ���˵绰
        TransDtl[24] = TradeContext.tbr_tel
    else:
        TransDtl[24] = ''
        
    if( TradeContext.existVariable( "tbr_mobile" ) ):                     #Ͷ�����ƶ��绰
        TransDtl[25] = TradeContext.tbr_mobile
    else:
        TransDtl[25] = ''
        
    if( TradeContext.existVariable( "tbr_email" ) ):                      #Ͷ��������
        TransDtl[26] = TradeContext.tbr_email
    else:
        TransDtl[26] = ''
        
    if( TradeContext.existVariable( "pre_tbr_bbr_rela" ) ):                   #Ͷ�����뱻���˹�ϵ
        TransDtl[27] = TradeContext.pre_tbr_bbr_rela  
    
    #��������Ϣ
    if( TradeContext.existVariable( "bbr_name" ) ):                       #����������
        TransDtl[28] = TradeContext.bbr_name
    
    if( TradeContext.existVariable( "bbr_sex" ) ):                        #�������Ա�
        TransDtl[29] = TradeContext.bbr_sex
   
    if( TradeContext.existVariable( "bbr_birth" ) ):                      #����������
        TransDtl[30] = TradeContext.bbr_birth
    
    if( TradeContext.existVariable( "pre_bbr_idtype" ) ):                     #������֤������
        TransDtl[31] = TradeContext.pre_bbr_idtype
    
    if( TradeContext.existVariable( "bbr_idno" ) ):                       #������֤����
        TransDtl[32] = TradeContext.bbr_idno
        
    if( TradeContext.existVariable( "bbr_addr" ) ):                       #�����˵�ַ
        TransDtl[33] = TradeContext.bbr_addr
    else:
        TransDtl[33]= ''
        
    if( TradeContext.existVariable( "bbr_postcode" ) ):                   #�������ʱ�
        TransDtl[34] = TradeContext.bbr_postcode
    else:
        TransDtl[34] =''
        
    if( TradeContext.existVariable( "bbr_tel" ) ):                        #�����˵绰
        TransDtl[35] = TradeContext.bbr_tel
    else:
        TransDtl[35]=''
        
    if( TradeContext.existVariable( "bbr_mobile" ) ):                     #�������ƶ��绰
        TransDtl[36] = TradeContext.bbr_mobile
    else:
        TransDtl[36]=''
        
    if( TradeContext.existVariable( "bbr_email" ) ):                      #����������
        TransDtl[37] = TradeContext.bbr_email
    else:
        TransDtl[37]=''

    #��ʼ����Ϣ
    TransDtl[38] = ''
    TransDtl[39] = ''
    TransDtl[40] = ''
    TransDtl[41] = ''
    TransDtl[42] = ''
    
    #��������Ϣ
    #������1��Ϣ������|֤������|֤������|�Ա�|����|�뱻���˹�ϵ|����˳��|����ݶ�(����)|����ݶ��ĸ����
    if( TradeContext.existVariable( "syr_1" ) and len(TradeContext.syr_1)!=0 ): 
        TransDtl[38] = TransDtl[38] + TradeContext.syr_1
    else:
        TransDtl[38]='' 
    
    if ( TradeContext.existVariable( "syr_2" ) and len(TradeContext.syr_2)!=0):                        
        TransDtl[39] = TransDtl[39] + TradeContext.syr_2
    else:
        TransDtl[39]=''
            
    if( TradeContext.existVariable( "syr_3" )and len(TradeContext.syr_3)!=0 ):                   
        TransDtl[40] = TransDtl[40] + TradeContext.syr_3
    else:
         TransDtl[40]=''
    
    if ( TradeContext.existVariable( "syr_4" ) and len(TradeContext.syr_4)!=0 ):                   
        TransDtl[41] = TransDtl[41] + TradeContext.syr_4
    else:
        TransDtl[41]=''  
    
    if ( TradeContext.existVariable( "syr_5" )and len(TradeContext.syr_5)!=0  ):                 
        TransDtl[42] = TransDtl[42] + TradeContext.syr_5
    else:
        TransDtl[42]=''    
  
    sql = "INSERT INTO YBT_INFO ("
    sql = sql + "AGENTSERIALNO,SYSID,WORKDATE,WORKTIME,BRNO,TELLERNO,CPICNO,SUBMISDATE,SUBMINO,PROCODE,PRINTNO,AMOUNT,XZINFO,"
    sql = sql + "TORMTYPE,EFFTORM,PAYOUTDUR,PAYOUTTYPE,TBR_NAME,TBR_SEX,TBR_BIRTH,TBR_IDTYPE,TBR_IDNO,TBR_ADDR,TBR_POSTCODE,"
    sql = sql + "TBR_TEL,TBR_MOBILE,TBR_EMAIL,TBR_BBR_RELA,BBR_NAME,BBR_SEX,BBR_BIRTH,BBR_IDTYPE,BBR_IDNO,BBR_ADDR,BBR_POSTCODE,"
    sql = sql + "BBR_TEL,BBR_MOBILE,BBR_EMAIL,SYR_INFO1,SYR_INFO2,SYR_INFO3,SYR_INFO4,SYR_INFO5) VALUES("

    i=0
    for i in range( 0, count ):
        if( type( TransDtl[i] ) is int ):
            sql=sql+str( TransDtl[i] )+","
        else:
            sql=sql+"'"+ TransDtl[i]+"',"
    
    sql=sql+"'"+TransDtl[count]+"')"
    
    AfaLoggerFunc.tradeInfo( '>>>>>>>�±�Ͷ�����׵Ǽ���ˮ<<<<<<< ' + str(sql))
    
    #���벢�ύ����
    result=AfaDBFunc.InsertSqlCmt( sql )
        
    if( result < 1 ):
        TradeContext.errorCode, TradeContext.errorMsg='A0044', '������ˮ��ʧ��'+AfaDBFunc.sqlErrMsg
        return False
    
    else:
        return True




################################################################################
# �� �� ���� AdbSelectQueDtl
# ����˵��: �ɷѽ��׵��������سɹ����ѯ�Ƿ����ԭͶ�����ŵļ�¼
# �޸ļ�¼: 
# ��    ע: 
# ��    ��: 
###############################################################################     
def AdbSelectQueDtl( ):
   
    AfaLoggerFunc.tradeInfo( '>>>>>>>��ʼ��ѯԭ����<<<<<<<') 
      
    sql = "select * from YBT_INFO "
    sql = sql + " where WORKDATE = '" + TradeContext.workDate.strip() + "'"         #��������
    sql = sql + " and   SUBMINO  = '" + TradeContext.applno.strip()   + "'"         #Ͷ������
    sql = sql + " and   cpicno   = '" + TradeContext.unitno           + "'"         #���չ�˾��λ����
    sql = sql + " and   tellerno = '" + TradeContext.tellerno         + "'"         #���׹�Ա��
    
    AfaLoggerFunc.tradeInfo( '>>>>>>>��ʼ��ѯԭ���ף�'+ str(sql)) 
    
    records = AfaDBFunc.SelectSql( sql ) 
   
    AfaLoggerFunc.tradeInfo('��ѯ����¼����Ϊ��'+str(len(records)))
    
    #û�м�¼���������
    if(len(records)==0):
        if not AdbInsertQueDtl( ):
            raise AfaFlowControl.flowException() 
        else:
            return True       
   
    #�м�¼�����ԭ��¼       
    else:
        if not AdbUpdateQueDtl( ):
            raise AfaFlowControl.flowException()
        else:
            return True    





################################################################################
# �� �� ���� AdbUpdateQueDtl
# ����˵��: ����ԭͶ����¼(YBT_INFO��)ȷ��һ��Ͷ�����Ŷ�Ӧһ����¼
# �޸ļ�¼: 

# ��    ע: 
# ��    ��: 
###############################################################################          
def AdbUpdateQueDtl( ):
    
    AfaLoggerFunc.tradeInfo( '>>>>>>>��ʼ����ԭͶ����¼ȷ��һ��Ͷ�����Ŷ�Ӧһ����¼<<<<<<<')
    
    sqlupdate = ""
    sqlupdate = sqlupdate + " update YBT_INFO SET "
    
    #ϵͳ��Ϣ
    sqlupdate = sqlupdate + "AGENTSERIALNO = '" + TradeContext.agentSerialno.strip() + "',"                        # AGENTSERIALNO ����ҵ����ˮ��
    sqlupdate = sqlupdate + "SYSID         = '" + TradeContext.sysId.strip()         + "',"                        # SYSID         ϵͳ��ʶ
    sqlupdate = sqlupdate + "WORKDATE      = '" + TradeContext.workDate.strip()      + "',"                        # WORKDATE      ��������
    sqlupdate = sqlupdate + "WORKTIME      = '" + TradeContext.workTime.strip()      + "',"                        # WORKTIME      ����ʱ��
    sqlupdate = sqlupdate + "BRNO          = '" + TradeContext.brno.strip()          + "',"                        # BRNO          ���׻���
    sqlupdate = sqlupdate + "TELLERNO      = '" + TradeContext.tellerno.strip()      + "',"                        # TELLERNO      ��Ա��
    
    #Ͷ����Ϣ
    sqlupdate = sqlupdate + "CPICNO        = '" + TradeContext.unitno.strip()         +"',"                        # unitno        ���չ�˾����
    sqlupdate = sqlupdate + "SUBMISDATE    = '" + TradeContext.tb_date.strip()        +"',"                        # tb_date       Ͷ������
    sqlupdate = sqlupdate + "SUBMINO       = '" + TradeContext.applno.strip()         +"',"                        # applno        Ͷ������
    sqlupdate = sqlupdate + "PROCODE       = '" + TradeContext.I1CETY.strip()         +"',"                        #pz_type        ƾ֤����
    sqlupdate = sqlupdate + "PRINTNO       = '" + TradeContext.userno.strip()         +"',"                        # bd_print_no   ����ӡˢ�ţ�ƾ֤�ţ�
    sqlupdate = sqlupdate + "AMOUNT        = '" + TradeContext.amount.strip()         +"',"                        #amount         Ӧ�ɱ���
    
    #������Ϣ������|�����գ�file1��Ϊ�м��������������Ϣ
    TradeContext.file1 = ""
    
    if TradeContext.existVariable( "productid" ):                                                                  #productid      ��������
        TradeContext.file1 = TradeContext.file1 + TradeContext.productid.strip() 
    TradeContext.file1     = TradeContext.file1 + "|"    
       
    if TradeContext.existVariable( "productid1" ):                                                                 #productid1     ��������
        TradeContext.file1 = TradeContext.file1 +TradeContext.productid1.strip()
    
    if ( len(str(TradeContext.file1.strip())) > 0): 
        sqlupdate = sqlupdate + "XZINFO = '"+TradeContext.file1+"', " 
   
    #�����ڼ�����     
    if( TradeContext.existVariable( "pre_tormtype" ) ):
        sqlupdate = sqlupdate + "TORMTYPE = '" + TradeContext.pre_tormtype.strip() + "',"              
    
    #�����ڼ� file2��Ϊ�м����������Ϣ   
    TradeContext.file2=""
    
    if TradeContext.existVariable( "coverage_year" ):                                             #�����ڼ� ����ݻ���ʼ���ڣ�                      
        TradeContext.file2 = TradeContext.file2 + TradeContext.coverage_year.strip() 
    TradeContext.file2 = TradeContext.file2 + "|"    
       
    if TradeContext.existVariable( "TermDate" ):                                                  #��ֹ����                    
        TradeContext.file2 = TradeContext.file2 +TradeContext.TermDate.strip()  
    
    if ( len(str(TradeContext.file2.strip())) > 0): 
        sqlupdate = sqlupdate + "EFFTORM = '"+TradeContext.file2+"', " 
    
    
        
    if( TradeContext.existVariable( "paydatelimit" ) ):                                            #�ɷ�����
        sqlupdate = sqlupdate + "PAYOUTDUR = '" + TradeContext.paydatelimit.strip() + "',"   
              
    if( TradeContext.existVariable( "pre_paymethod" ) ):                                           #�ɷѷ�ʽ 
        sqlupdate = sqlupdate + "PAYOUTTYPE = '" + TradeContext.pre_paymethod.strip() + "',"   
      
    #Ͷ������Ϣ        
    if( TradeContext.existVariable( "tbr_name" ) ):                                                #Ͷ��������
        sqlupdate = sqlupdate + "TBR_NAME = '" + TradeContext.tbr_name.strip() + "',"    
    
    if( TradeContext.existVariable( "pre_tbr_sex" ) ):                                                 #Ͷ�����Ա�
        sqlupdate = sqlupdate + "TBR_SEX = '" + TradeContext.pre_tbr_sex.strip() + "',"    
    
    if( TradeContext.existVariable( "tbr_birth" ) ):                                               #Ͷ��������
        sqlupdate = sqlupdate + "TBR_BIRTH= '" + TradeContext.tbr_birth.strip() + "',"    
   
    if( TradeContext.existVariable( "pre_tbr_idtype" ) ):                                              #Ͷ����֤������
        sqlupdate = sqlupdate + " TBR_IDTYPE='" + TradeContext.pre_tbr_idtype.strip() + "',"
    
    if( TradeContext.existVariable( "tbr_idno" ) ):                                                #Ͷ����֤������
        sqlupdate = sqlupdate + " TBR_IDNO='" + TradeContext.tbr_idno.strip() + "',"
   
    if( TradeContext.existVariable( "tbr_addr" ) ):                                                #Ͷ���˵�ַ
        sqlupdate = sqlupdate + " TBR_ADDR='" + TradeContext.tbr_addr.strip() + "',"
    
    if( TradeContext.existVariable( "tbr_postcode" ) ):                                            #Ͷ�����ʱ�
        sqlupdate = sqlupdate + " TBR_POSTCODE='" + TradeContext.tbr_postcode.strip() + "',"
        
    if( TradeContext.existVariable( "tbr_tel" ) ):                                                 #Ͷ���˵绰
        sqlupdate = sqlupdate + " TBR_TEL= '" + TradeContext.tbr_tel.strip() + "',"
    else:
        sqlupdate = sqlupdate + " TBR_TEL= '',"  
          
    if( TradeContext.existVariable( "tbr_mobile" ) ):                                             #Ͷ�����ƶ��绰
        sqlupdate = sqlupdate + " TBR_MOBILE= '" + TradeContext.tbr_mobile.strip() + "',"
    else:
        sqlupdate = sqlupdate + " TBR_MOBILE= '',"    
        
    if( TradeContext.existVariable( "tbr_email" ) ):                                              #Ͷ��������
         sqlupdate = sqlupdate + " TBR_EMAIL= '" + TradeContext.tbr_email.strip() + "',"
    else:
         sqlupdate = sqlupdate + "TBR_EMAIL = ''," 
         
    if( TradeContext.existVariable( "pre_tbr_bbr_rela" ) ):                                       #Ͷ�����뱻���˹�ϵ
        sqlupdate = sqlupdate + " TBR_BBR_RELA= '" + TradeContext.pre_tbr_bbr_rela.strip() + "',"     
     
    #��������Ϣ
    if( TradeContext.existVariable( "bbr_name" ) ):                                               #����������
        sqlupdate = sqlupdate + " BBR_NAME= '" + TradeContext.bbr_name.strip() + "',"
    
    if( TradeContext.existVariable( "bbr_sex" ) ):                                                #�������Ա�
        sqlupdate = sqlupdate + " BBR_SEX= '" + TradeContext.bbr_sex.strip() + "',"
    
    if( TradeContext.existVariable( "bbr_birth" ) ):                                              #����������
        sqlupdate = sqlupdate + " BBR_BIRTH= '" + TradeContext.bbr_birth.strip() + "',"
    
    if( TradeContext.existVariable( "pre_bbr_idtype" ) ):                                         #������֤������
        sqlupdate = sqlupdate + " BBR_IDTYPE= '" + TradeContext.pre_bbr_idtype.strip() + "',"
    
    if( TradeContext.existVariable( "bbr_idno" ) ):                                               #������֤����
        sqlupdate = sqlupdate + " BBR_IDNO= '" + TradeContext.bbr_idno.strip() + "',"
        
    if( TradeContext.existVariable( "bbr_addr" ) ):                                               #�����˵�ַ
        sqlupdate = sqlupdate + " BBR_ADDR= '" + TradeContext.bbr_addr.strip() + "',"
    else:
        sqlupdate = sqlupdate + " BBR_ADDR= '',"
        
    if( TradeContext.existVariable( "bbr_postcode" ) ):                                           #�������ʱ�
        sqlupdate = sqlupdate + " BBR_POSTCODE= '" + TradeContext.bbr_postcode.strip() + "',"
    else:
        sqlupdate = sqlupdate + " BBR_POSTCODE= '',"
        
    if( TradeContext.existVariable( "bbr_tel" ) ):                                                #�����˵绰
        sqlupdate = sqlupdate + " BBR_TEL= '" + TradeContext.bbr_tel.strip() + "',"
    else:
        sqlupdate = sqlupdate + " BBR_TEL= '',"
        
    if( TradeContext.existVariable( "bbr_mobile" ) ):                                             #�������ƶ��绰
        sqlupdate = sqlupdate + " BBR_MOBILE= '" + TradeContext.bbr_mobile.strip() + "',"
    else:
        sqlupdate = sqlupdate + " BBR_MOBILE= '',"
        
    if( TradeContext.existVariable( "bbr_email" ) ):                                              #����������
        sqlupdate = sqlupdate + " BBR_EMAIL= '" + TradeContext.bbr_email.strip() + "',"
    else:
        sqlupdate = sqlupdate + " BBR_EMAIL= '',"
        
    #��������Ϣ
    #������1��Ϣ������|֤������|֤������|�Ա�|����|�뱻���˹�ϵ|����˳��|����ݶ�(����)|����ݶ��ĸ����   
    if( TradeContext.existVariable( "syr_1" ) and len(TradeContext.syr_1)!=0 ):                   #������1��Ϣ    
        sqlupdate = sqlupdate + " SYR_INFO1= '" + TradeContext.syr_1.strip() + "',"   
    else:
        sqlupdate = sqlupdate + " SYR_INFO1= ''," 
         
    if( TradeContext.existVariable( "syr_2" ) and len(TradeContext.syr_2)!=0 ):                   #������2��Ϣ    
        sqlupdate = sqlupdate + " SYR_INFO2= '" + TradeContext.syr_2.strip() + "',"                 
    else:
        sqlupdate = sqlupdate + " SYR_INFO2= '',"
        
    if( TradeContext.existVariable( "syr_3" ) and len(TradeContext.syr_3)!=0 ):                   #������3��Ϣ    
        sqlupdate = sqlupdate + " SYR_INFO3= '" + TradeContext.syr_3.strip() + "',"  
    else:
        sqlupdate = sqlupdate + " SYR_INFO3= '',"
        
    if( TradeContext.existVariable( "syr_4" ) and len(TradeContext.syr_4)!=0 ):                   #������4��Ϣ    
        sqlupdate = sqlupdate + " SYR_INFO4= '" + TradeContext.syr_4.strip() + "',"    
    else:
        sqlupdate = sqlupdate + " SYR_INFO4= '',"
        
    if( TradeContext.existVariable( "syr_5" ) and len(TradeContext.syr_5)!=0 ):                   #������5��Ϣ    
        sqlupdate = sqlupdate + " SYR_INFO5= '" + TradeContext.syr_5.strip() + "'"  
    else:
        sqlupdate = sqlupdate + " SYR_INFO5= ''"
        
    sqlupdate = sqlupdate + " where WORKDATE = '"+TradeContext.workDate+"' and SUBMINO = '"+TradeContext.applno+"'"
    
    AfaLoggerFunc.tradeInfo( 'sqlupdate = ' + str(sqlupdate))                                     #���SQL���
    
    #���²��ύ����
    record=AfaDBFunc.UpdateSqlCmt( sqlupdate )
    
    if( record > 0 ):
        AfaLoggerFunc.tradeInfo( '>>>>>>>����ԭͶ����¼�ɹ�<<<<<<<')
        return True
        
    if( record == 0 ):
        AfaLoggerFunc.tradeInfo( '>>>>>>>��Ͷ����¼<<<<<<<')
        TradeContext.errorCode,TradeContext.errorMsg='A0100','��Ͷ����¼'
        return False
        
    else :
        AfaLoggerFunc.tradeInfo( '>>>>>>>����ԭͶ����¼ʧ��<<<<<<<')
        TradeContext.errorCode, TradeContext.errorMsg='A0100', '����ԭͶ����¼ʧ��' + AfaDBFunc.sqlErrMsg
        return False
      
################################################################################
# �� �� ��: ADBUpdateTransdtl
# ����˵��:�ɷѽ��׵��������سɹ�����¼�¼
# �޸ļ�¼: 
# ��    ע: 
# ��    ��: 
###############################################################################
def ADBUpdateTransdtl( ):
    AfaLoggerFunc.tradeInfo( '>>>>>>>��ʼ����ԭ�ɷѽ���<<<<<<<')
    
    #��ʼ����Ϣ
    sqlupdate = ""
    TradeContext.note1  = ""
    TradeContext.note2  = ""
    TradeContext.note3  = ""
    TradeContext.note4  = ""
    TradeContext.note5  = ""
    TradeContext.note6  = ""
    TradeContext.note7  = ""
    TradeContext.note8  = ""
    TradeContext.note9  = ""
    TradeContext.note10 = ""
    
    sqlupdate = sqlupdate + "update afa_maintransdtl set "

    #corpSerno:���µ�������ˮ��
    if TradeContext.existVariable( "corpSerno" ):
        sqlupdate = sqlupdate + " corpSerno = '" + TradeContext.corpSerno.strip() + "' "
    else:
        sqlupdate = sqlupdate + " corpSerno = '' "

    #note1:�˺Ŵ���|���ڱ���|���ս��|����
    #if( TradeContext.existVariable( "acc_code" ) ):
        #TradeContext.note1 = TradeContext.note1 + TradeContext.acc_code.strip()
    #TradeContext.note1 = TradeContext.note1 + "|"

    if( TradeContext.existVariable( "premium" ) ):
        TradeContext.note1 = TradeContext.note1 + TradeContext.premium.strip()
    TradeContext.note1 = TradeContext.note1 + "|"
    
    if( TradeContext.existVariable( "prem" ) ):
        TradeContext.note1 = TradeContext.note1 + TradeContext.prem.strip()
    TradeContext.note1 = TradeContext.note1 + "|"
    
    if( TradeContext.existVariable( "premium1" ) ):
        TradeContext.note1 = TradeContext.note1 + TradeContext.premium1.strip()
    
    #note2:������������|������������|�����ڼ䣨�ɷ����ޣ�
    #if ( TradeContext.existVariable( "payenddate" ) ):
        #TradeContext.note2 = TradeContext.note2 + TradeContext.payenddate.strip()
    #TradeContext.note2 = TradeContext.note2 + "|"

    #if ( TradeContext.existVariable( "charge_period" ) ):
    #    TradeContext.note2 = TradeContext.note2 + TradeContext.charge_period.strip()
    #TradeContext.note2 = TradeContext.note2 + "|"

    if ( TradeContext.existVariable( "paydatelimit" ) ):
        TradeContext.note2 = TradeContext.note2 + TradeContext.paydatelimit.strip()
    
   
    #note3:Ͷ������|��������|������Ч����
    if( TradeContext.existVariable( "tb_date" ) ):
        TradeContext.note3 = TradeContext.note3 + TradeContext.tb_date.strip()
    TradeContext.note3 = TradeContext.note3 + "|"

    if( TradeContext.existVariable( "paydate" ) ):
        TradeContext.note3 = TradeContext.note3 + TradeContext.paydate.strip()
    #TradeContext.note3 = TradeContext.note3 + "|"

    #if ( TradeContext.existVariable( "validate" ) ):
        #TradeContext.note3 = TradeContext.note3 + TradeContext.validate.strip()
   
    #note4:Ͷ��������|Ͷ����֤������|��Ͷ���˹�ϵ
    if( TradeContext.existVariable( "tbr_name" ) ):
        TradeContext.note4 = TradeContext.note4 + TradeContext.tbr_name.strip()
    TradeContext.note4 = TradeContext.note4 + "|"

    if ( TradeContext.existVariable( "tbr_idno" ) ):
       TradeContext.note4 = TradeContext.note4 + TradeContext.tbr_idno.strip()
    TradeContext.note4 = TradeContext.note4 + "|"
    if ( TradeContext.existVariable( "tbr_bbr_rela" ) ):
       TradeContext.note4 = TradeContext.note4 + TradeContext.tbr_bbr_rela.strip()
    
    
    #note5:����������|������֤������|�뱻�����˹�ϵ
    if( TradeContext.existVariable( "bbr_name" ) ):
        TradeContext.note5 = TradeContext.note5 + TradeContext.bbr_name.strip()
    TradeContext.note5 = TradeContext.note5 + "|"

    if ( TradeContext.existVariable( "bbr_idno" ) ):
        TradeContext.note5 = TradeContext.note5 + TradeContext.bbr_idno.strip()
    TradeContext.note5 = TradeContext.note5 + "|"
    
    if ( TradeContext.existVariable( "syr_bbr_rela" ) ):
        TradeContext.note5 = TradeContext.note5 + TradeContext.syr_bbr_rela.strip()
    
    
    #note6:����Ӫ��ԱԱ����|���ѷ�ʽ
    if( TradeContext.existVariable( "salerno" ) ):
        TradeContext.note6 = TradeContext.note6 + TradeContext.salerno.strip()
    TradeContext.note6 = TradeContext.note6 + "|"
   
    if( TradeContext.existVariable( "paymethod1" ) ):
        TradeContext.note6 = TradeContext.note6 + TradeContext.paymethod1.strip()   
    
    
    #note7:���ѷ�ʽ|�ɷ��ڴ�|�����ڼ�
    if( TradeContext.existVariable( "paymethod" ) ):
        TradeContext.note7 = TradeContext.note7 + TradeContext.paymethod.strip()
    TradeContext.note7 = TradeContext.note7 + "|"

    if ( TradeContext.existVariable( "rev_frequ" ) ):
        TradeContext.note7 = TradeContext.note7 + TradeContext.rev_frequ.strip()
    TradeContext.note7 = TradeContext.note7 + "|"
    
    if ( TradeContext.existVariable( "payyear" ) ):
        TradeContext.note7 = TradeContext.note7 + TradeContext.payyear.strip()
    
    #note8:�������ִ���|��������|��������|�����ڼ�����|�����ڼ�
    if ( TradeContext.existVariable( "productid" ) ):
        TradeContext.note8 = TradeContext.note8 + TradeContext.productid.strip()
    TradeContext.note8 = TradeContext.note8 + "|"

    if ( TradeContext.existVariable( "productname" ) ):
        TradeContext.note8 = TradeContext.note8 + TradeContext.productname.strip()
    TradeContext.note8 = TradeContext.note8 + "|"
    
    if ( TradeContext.existVariable( "productid1" ) ):
        TradeContext.note8 = TradeContext.note8 + TradeContext.productid1.strip()
    TradeContext.note8 = TradeContext.note8 + "|"
   
    if ( TradeContext.existVariable( "coverage_period" ) ):
        TradeContext.note8 = TradeContext.note8 + TradeContext.coverage_period.strip()
    TradeContext.note8 = TradeContext.note8 + "|"
    
    if ( TradeContext.existVariable( "coverage_year" ) ):
        TradeContext.note8 = TradeContext.note8 + TradeContext.coverage_year.strip 
    
    #note9:Ͷ������|Ͷ������|���յ���|�����ձ�־
    if( TradeContext.existVariable( "amt_unit" ) ):
        TradeContext.note9 = TradeContext.note9 + TradeContext.amt_unit.strip()
    TradeContext.note9 = TradeContext.note9 + "|"

    if ( TradeContext.existVariable( "applno" ) ):
        TradeContext.note9 = TradeContext.note9 + TradeContext.applno.strip()
    TradeContext.note9 = TradeContext.note9 + "|"
    
    if( TradeContext.existVariable( "policy" ) ):
        TradeContext.note9 = TradeContext.note9 + TradeContext.policy.strip()
    TradeContext.note9 = TradeContext.note9 + "|"

    if ( TradeContext.existVariable( "mainsubflg" ) ):
        TradeContext.note9 = TradeContext.note9 + TradeContext.mainsubflg.strip()
    
    #note10:��������Ϣ
    #if( TradeContext.existVariable( "syr_1" ) ):
    #   TradeContext.note10 = TradeContext.note10 + TradeContext.syr_1.strip()
    #TradeContext.note10 = TradeContext.note10 + "|"

    #if ( TradeContext.existVariable( "syr_2" ) ):
    #    TradeContext.note10 = TradeContext.note10 + TradeContext.syr_2.strip()
    #TradeContext.note10 = TradeContext.note10 + "|"
    
    #if( TradeContext.existVariable( "syr_3" ) ):
    #    TradeContext.note10 = TradeContext.note10 + TradeContext.syr_3.strip()
    #TradeContext.note10 = TradeContext.note10 + "|"

    #if ( TradeContext.existVariable( "syr_4" ) ):
    #   TradeContext.note10 = TradeContext.note10 + TradeContext.syr_4.strip()
    #TradeContext.note10 = TradeContext.note10 + "|"
    
    #if( TradeContext.existVariable( "syr_5" ) ):
    #    TradeContext.note10 = TradeContext.note10 + TradeContext.syr_5.strip()
    
    if ( len(str(TradeContext.note1.strip())) > 0):
        sqlupdate = sqlupdate + ",note1 = '"+TradeContext.note1+"' "
    if ( len(str(TradeContext.note2.strip())) > 0):
        sqlupdate = sqlupdate + ",note2 = '"+TradeContext.note2+"' "
    if ( len(str(TradeContext.note3.strip())) > 0):
        sqlupdate = sqlupdate + ",note3 = '"+TradeContext.note3+"' "
    if ( len(str(TradeContext.note4.strip())) > 0):
        sqlupdate = sqlupdate + ",note4 = '"+TradeContext.note4+"' "
    if ( len(str(TradeContext.note5.strip())) > 0):
        sqlupdate = sqlupdate + ",note5 = '"+TradeContext.note5+"' "
    if ( len(str(TradeContext.note6.strip())) > 0):
        sqlupdate = sqlupdate + ",note6 = '"+TradeContext.note6+"' "
    if ( len(str(TradeContext.note7.strip())) > 0):
        sqlupdate = sqlupdate + ",note7 = '"+TradeContext.note7+"' "
    if ( len(str(TradeContext.note8.strip())) > 0):
        sqlupdate = sqlupdate + ",note8 = '"+TradeContext.note8+"' "
    if ( len(str(TradeContext.note9.strip())) > 0):
        sqlupdate = sqlupdate + ",note9 = '"+TradeContext.note9+"' "
    #if ( len(str(TradeContext.note10.strip())) > 0):
    #    sqlupdate = sqlupdate + ",note10 = '"+TradeContext.note10+"' "
    
    sqlupdate = sqlupdate + " where sysid = '"+TradeContext.sysId+"' and agentserialno = '"+TradeContext.agentSerialno+"'"
    
    AfaLoggerFunc.tradeInfo( 'sqlupdate = ' + str(sqlupdate))
    
    record=AfaDBFunc.UpdateSqlCmt( sqlupdate )
    
    if( record > 0 ):
        AfaLoggerFunc.tradeInfo( '>>>>>>>����ԭ�ɷѽ��׳ɹ�<<<<<<<')
        return True
    
    if( record == 0 ):
        AfaLoggerFunc.tradeInfo( '>>>>>>>����ԭ�ɷѽ���ʧ��<<<<<<<')
        TradeContext.errorCode,TradeContext.errorMsg='A0100','δ����ԭʼ����'
        return False
    else :
        AfaLoggerFunc.tradeInfo( '>>>>>>>����ԭ�ɷѽ���ʧ��<<<<<<<')
        TradeContext.errorCode, TradeContext.errorMsg='A0100', '����ԭ����״̬ʧ��' + AfaDBFunc.sqlErrMsg
        return False

        
        
################################################################################
# �� �� ��: ADBCheckCert
# ����˵��: ���ƾ֤�����뱣�չ�˾�Ƿ��Ӧ
# 
# ��    ע:
# ��    ��:
###############################################################################
def ADBCheckCert( ):
    AfaLoggerFunc.tradeInfo('>>>>��ȡ���չ�˾[' + TradeContext.unitno + ']ƾ֤�ţ���У��<<<<')
    sql = ""
    sql = sql + " select certtype from afa_adbpam where "
    sql = sql + " unitno='" + TradeContext.unitno + "'"                       #��λ���ƣ����ݱ��չ�˾�����
                                                                              #��ѯƾ֤���ࣩ
    sql = sql + " and certtype='" + TradeContext.I1CETY + "'"
    
    AfaLoggerFunc.tradeInfo( sql )
    
    record = AfaDBFunc.SelectSql( sql )
    
    if ( record==None ):
        AfaLoggerFunc.tradeInfo( '>>>>��ѯƾ֤�����쳣<<<<' )
        TradeContext.errorCode,TradeContext.errorMsg = 'A0100', '��ѯƾ֤�����쳣'
        return False
        
    if ( len(record) <= 0):
        AfaLoggerFunc.tradeInfo( '>>>>���չ�˾�����ƾ֤����Ƿ�<<<<' )
        TradeContext.errorCode,TradeContext.errorMsg = 'A0100', '���չ�˾�����ƾ֤����Ƿ�'
        return False
    
    return True


################################################################################
# �� �� ��: ADBUpdateTransdtlRev
# ����˵��: �����ɷѽ��׵��������سɹ�����·��ؽ����Ϣ
# �޸ļ�¼: 
# ��    ע: ֻ���ڳ���ʧ�ܵ�����²ż�¼ʧ����Ϣ
# ��    ��: 
###############################################################################
def ADBUpdateTransdtlRev( ):
    sqlupdate = ""
   
    AfaLoggerFunc.tradeInfo( '>>>>>>>��ʼ����ԭ�������׽����Ϣ<<<<<<<')
   
    sqlupdate = sqlupdate + "update afa_maintransdtl set "
    sqlupdate = sqlupdate + " corpcode = '"+TradeContext.errorCode.strip()+"' "
    sqlupdate = sqlupdate + ", errorMsg = '"+TradeContext.errorMsg.strip()+"' "
    sqlupdate = sqlupdate + " where sysid = '"+TradeContext.sysId+"' and agentserialno = '"+TradeContext.agentSerialno+"'"
   
    AfaLoggerFunc.tradeInfo( 'sqlupdate = ' + str(sqlupdate))
   
    record=AfaDBFunc.UpdateSqlCmt( sqlupdate )
   
    if( record > 0 ):
        AfaLoggerFunc.tradeInfo( '>>>>>>>����ԭ�������׽����Ϣ�ɹ�<<<<<<<')
        return True
    if( record == 0 ):
        AfaLoggerFunc.tradeInfo( '>>>>>>>����ԭ�������׽����Ϣʧ��<<<<<<<')
        TradeContext.errorCode,TradeContext.errorMsg='A0100','δ����ԭʼ����'
        return False
    else :
        AfaLoggerFunc.tradeInfo( '>>>>>>>����ԭ�������׽����Ϣʧ��<<<<<<<')
        TradeContext.errorCode, TradeContext.errorMsg='A0100', '����ԭ����״̬ʧ��' + AfaDBFunc.sqlErrMsg
        return False
