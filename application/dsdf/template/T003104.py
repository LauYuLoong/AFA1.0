# -*- coding: gbk -*-
################################################################################
#   ���մ���.����Ʊģ��
#===============================================================================
#   ģ���ļ�:   003104.py
#   �޸�ʱ��:   2006-04-05
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaFunc,AfaTransDtlFunc,AfaFlowControl,AfaDBFunc,os,AfaAfeFunc,Party3Context
from types import *

def main( ):

    AfaLoggerFunc.tradeInfo('******���մ���.����Ʊģ��[' + TradeContext.TemplateCode + ']����******')

    try:

        #=====================��ʼ�����ر��ı���================================
        TradeContext.tradeResponse=[]

        #=====================��ȡ��ǰϵͳʱ��==================================
        TradeContext.workDate=AfaUtilTools.GetSysDate( )
        TradeContext.workTime=AfaUtilTools.GetSysTime( )

        #=====================�ж�Ӧ��ϵͳ״̬==================================
        if not AfaFunc.ChkSysStatus( ) :
            raise AfaFlowControl.flowException( )
                
        #=====================У�鹫���ڵ����Ч��==============================
        if( not TradeContext.existVariable( "sysId") ):
            raise AfaFlowControl.flowException( 'A0001', 'ϵͳ��ʶ[sysId]ֵ������,���ܽ��в���Ʊ' )

        if( not TradeContext.existVariable( "userno") ):
            raise AfaFlowControl.flowException( 'A0001', '�û���[userno]ֵ������,���ܽ��в���Ʊ' )

        #=====================�ж�Ӧ��ϵͳ״̬==================================
        if not AfaFunc.ChkSysStatus( ) :
            raise AfaFlowControl.flowException( )

        #=====================�ж��̻�״̬======================================
        if not AfaFunc.ChkUnitStatus( ) :
            raise AfaFlowControl.flowException( )

        #=====================�ж�����״̬======================================
        if not AfaFunc.ChkChannelStatus( ) :
            raise AfaFlowControl.flowException( )

        #������־(0-��ѯ��Ʊ��Ϣ 1-�޸Ĵ�ӡ���� 2-�ӵ�������ȡ��Ʊ��Ϣ,���д�ӡ)
        if( not TradeContext.existVariable( "procFlag") ):
            raise AfaFlowControl.flowException( 'A0001', '������־[tradeFlag"]ֵ������,���ܽ��в���Ʊ' )

        if(TradeContext.procFlag=="0"):

            #��ѯ��Ʊ��Ϣ
            sql="SELECT BILLDATA,ITEM1,ITEM2,ITEM3,ITEM4,ITEM5,ITEM6,BILLSERNO,SERIALNO,PRTNUM,WORKDATE,BILLSTATUS FROM AFA_BILLDTL WHERE "
            sql=sql + " SYSID='"      + TradeContext.sysId  + "'"
            sql=sql + " AND UNITNO='" + TradeContext.unitno + "'"

            if( TradeContext.existVariable( "subUnitno") ):
                sql=sql + " AND SUBUNITNO='" + TradeContext.subUnitno + "'"

            if( TradeContext.existVariable( "userno") ):
                sql=sql + " AND USERNO='" + TradeContext.userno + "'"

            if( TradeContext.existVariable( "payMonth") ):
                sql=sql + " AND WORKDATE LIKE '" + TradeContext.payMonth + "%'"

            if( TradeContext.existVariable( "item1") ):
                sql=sql + " AND ITEM1='"  + TradeContext.item1  + "'"

            if( TradeContext.existVariable( "item2") ):
                sql=sql + " AND ITEM2='"  + TradeContext.item1  + "'"

            if( TradeContext.existVariable( "item3") ):
                sql=sql + " AND ITEM3='"  + TradeContext.item1  + "'"

            if( TradeContext.existVariable( "item4") ):
                sql=sql + " AND ITEM4='"  + TradeContext.item1  + "'"

            if( TradeContext.existVariable( "item5") ):
                sql=sql + " AND ITEM5='"  + TradeContext.item1  + "'"

            if( TradeContext.existVariable( "item6") ):
                sql=sql + " AND ITEM6='"  + TradeContext.item1  + "'"

            sql=sql + " ORDER BY WORKDATE DESC,WORKTIME DESC "

            AfaLoggerFunc.tradeInfo( sql )

            records = AfaDBFunc.SelectSql(sql)

            if( records == None ):
                raise AfaFlowControl.flowException( 'A0002', '���ݿ�����쳣:' + AfaDBFunc.sqlErrMsg )

            if(len(records)==0):
                raise AfaFlowControl.flowException( 'A0002', '�޷��������ļ�¼' )

            if(int(records[0][9])==3):
                raise AfaFlowControl.flowException( 'A0002', '���3���ش�' )

            if(int(records[0][11])==1):
               raise AfaFlowControl.flowException( 'A0002', 'Ʊ�������ϣ��������ӡ' )

            TradeContext.billNum = str(len(records))        #��Ʊ����

            if ( TradeContext.TransType=='0' ):
                #������ʼ��
                TradeContext.billData = []                  #��Ʊ��Ϣ
                TradeContext.item1    = []                  #������1
                TradeContext.item2    = []                  #������2
                TradeContext.item3    = []                  #������3
                TradeContext.item4    = []                  #������4
                TradeContext.item5    = []                  #������5
                TradeContext.item6    = []                  #������6
                TradeContext.billserno= []                  #��Ʊ���
                TradeContext.serialno = []                  #�м�ҵ����ˮ��
                TradeContext.prtnum   = []                  #��ӡ����
                TradeContext.paydate  = []                  #֧������

                #���
                for i in range( 0, len(records) ):
                    TradeContext.billData.append(records[i][0])
                    TradeContext.item1.append(records[i][1])
                    TradeContext.item2.append(records[i][2])
                    TradeContext.item3.append(records[i][3])
                    TradeContext.item4.append(records[i][4])
                    TradeContext.item5.append(records[i][5])
                    TradeContext.item6.append(records[i][6])
                    TradeContext.billserno.append(records[i][7])
                    TradeContext.serialno.append(records[i][8])
                    TradeContext.prtnum.append(records[i][9])
                    TradeContext.paydate.append(records[i][10])
            else:
                MxFileName = os.environ['AFAP_HOME'] + '/tmp/MX' + TradeContext.zoneno + TradeContext.brno + TradeContext.tellerno + '.TXT'
                AfaLoggerFunc.tradeInfo('>>>��ϸ�ļ�:['+MxFileName+']')

                if (os.path.exists(MxFileName) and os.path.isfile(MxFileName)):
                    #�ļ�����,��ɾ��-�ٴ���
                    os.system("rm " + MxFileName)

                #������ϸ�ļ�
                sfp = open(MxFileName, "w")

                for i in range( 0, len(records) ):
                    wBuffer = ""
                    wBuffer = wBuffer + records[i][0]
                    wBuffer = wBuffer + records[i][1]
                    wBuffer = wBuffer + records[i][2]
                    wBuffer = wBuffer + records[i][3]
                    wBuffer = wBuffer + records[i][4]
                    wBuffer = wBuffer + records[i][5]
                    wBuffer = wBuffer + records[i][6]
                    wBuffer = wBuffer + records[i][7]
                    wBuffer = wBuffer + records[i][8]
                    wBuffer = wBuffer + records[i][9]
                    wBuffer = wBuffer + records[i][10]

                    sfp.write(wBuffer + '\n')

                sfp.close()

        elif(TradeContext.procFlag=="1"):

            #�ӵ�������ȡ��Ʊ��Ϣ,���д�ӡ

            #=====================��ȡƽ̨��ˮ��====================================
            if( not AfaFunc.GetSerialno( ) ):
                raise AfaFlowControl.flowException( )

            #=====================����ӿ�(ǰ����)==================================
            subModuleExistFlag=0
            subModuleName = 'T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode
            try:
                subModuleHandle=__import__( subModuleName )

            except Exception, e:
                AfaLoggerFunc.tradeInfo( e)

            else:
                AfaLoggerFunc.tradeInfo( 'ִ��['+subModuleName+']ģ��' )
                subModuleExistFlag=1
                if not subModuleHandle.SubModuleDoFst( ) :
                    raise AfaFlowControl.flowException( )

            #��ͨѶǰ�ý���
            AfaAfeFunc.CommAfe()

            if TradeContext.errorCode!='0000' :
                raise AfaFlowControl.flowException( )

            #��Ʊ����
            TradeContext.billNum = Party3Context.billNum

            if ( TradeContext.TransType=='0' ):
                #������ʼ��
                TradeContext.billData = []                  #��Ʊ��Ϣ
                TradeContext.item1    = []                  #������1
                TradeContext.item2    = []                  #������2
                TradeContext.item3    = []                  #������3
                TradeContext.item4    = []                  #������4
                TradeContext.item5    = []                  #������5
                TradeContext.item6    = []                  #������6
                TradeContext.billserno= []                  #��Ʊ���
                TradeContext.serialno = []                  #�м�ҵ����ˮ��
                TradeContext.prtnum   = []                  #��ӡ����
                TradeContext.paydate  = []                  #֧������

                if ( int(Party3Context.billNum) == 1 ):
                    #���(һ�ŷ�Ʊ)
                        TradeContext.billData   = Party3Context.billData
                        TradeContext.item1      = Party3Context.item1
                        TradeContext.item2      = Party3Context.item2
                        TradeContext.item3      = Party3Context.item3
                        TradeContext.item4      = Party3Context.item4
                        TradeContext.item5      = Party3Context.item5
                        TradeContext.item6      = Party3Context.item6
                        TradeContext.billserno  = Party3Context.billserno
                        TradeContext.serialno   = Party3Context.serialno
                        TradeContext.prtnum     = Party3Context.prtnum
                        TradeContext.paydate    = Party3Context.paydate
                else:
                    #���(���ŷ�Ʊ)
                    for i in range( 0, int(Party3Context.billNum) ):
                        TradeContext.billData.append(Party3Context.billData[i])
                        TradeContext.item1.append(Party3Context.item1[i])
                        TradeContext.item2.append(Party3Context.item2[i])
                        TradeContext.item3.append(Party3Context.item3[i])
                        TradeContext.item4.append(Party3Context.item4[i])
                        TradeContext.item5.append(Party3Context.item5[i])
                        TradeContext.item6.append(Party3Context.item6[i])
                        TradeContext.billserno.append(Party3Context.billserno[i])
                        TradeContext.serialno.append(Party3Context.serialno[i])
                        TradeContext.prtnum.append(Party3Context.prtnum[i])
                        TradeContext.paydate.append(Party3Context.paydate[i])
            else:
                MxFileName = os.environ['AFAP_HOME'] + '/tmp/MX' + TradeContext.zoneno + TradeContext.brno + TradeContext.tellerno + '.TXT'
                AfaLoggerFunc.tradeInfo('>>>��ϸ�ļ�:['+MxFileName+']')

                if (os.path.exists(MxFileName) and os.path.isfile(MxFileName)):
                    #�ļ�����,��ɾ��-�ٴ���
                    os.system("rm " + MxFileName)

                #������ϸ�ļ�
                sfp = open(MxFileName, "w")

                if ( int(Party3Context.billNum) == 1 ):
                    #���(һ�ŷ�Ʊ)
                        wBuffer = ""
                        wBuffer = wBuffer + Party3Context.billData
                        wBuffer = wBuffer + Party3Context.item1
                        wBuffer = wBuffer + Party3Context.item2
                        wBuffer = wBuffer + Party3Context.item3
                        wBuffer = wBuffer + Party3Context.item4
                        wBuffer = wBuffer + Party3Context.item5
                        wBuffer = wBuffer + Party3Context.item6
                        wBuffer = wBuffer + Party3Context.billserno
                        wBuffer = wBuffer + Party3Context.serialno
                        wBuffer = wBuffer + Party3Context.prtnum
                        wBuffer = wBuffer + Party3Context.paydate
                        sfp.write(wBuffer + '\n')
                        sfp.close()
                else:
                    #���(���ŷ�Ʊ)
                    for i in range( 0, int(Party3Context.billNum) ):
                        wBuffer = ""
                        wBuffer = wBuffer + Party3Context.billData[i]
                        wBuffer = wBuffer + Party3Context.item1[i]
                        wBuffer = wBuffer + Party3Context.item2[i]
                        wBuffer = wBuffer + Party3Context.item3[i]
                        wBuffer = wBuffer + Party3Context.item4[i]
                        wBuffer = wBuffer + Party3Context.item5[i]
                        wBuffer = wBuffer + Party3Context.item6[i]
                        wBuffer = wBuffer + Party3Context.billserno[i]
                        wBuffer = wBuffer + Party3Context.serialno[i]
                        wBuffer = wBuffer + Party3Context.prtnum[i]
                        wBuffer = wBuffer + Party3Context.paydate[i]
                        sfp.write(wBuffer + '\n')
                    sfp.close()

            #=====================����ӿ�(����)==================================
            if ( subModuleExistFlag==1 ) :
                if not subModuleHandle.SubModuleDoSnd():
                    raise AfaFlowControl.flowException( )

        #=====================�Զ����==========================================
        TradeContext.errorCode = '0000'
        TradeContext.errorMsg  = '���׳ɹ�'
        AfaFunc.autoPackData()

        #=====================�����˳�==========================================
        AfaLoggerFunc.tradeInfo('******���մ���.����Ʊģ��[' + TradeContext.TemplateCode + ']�˳�******' )

    except AfaFlowControl.flowException, e:
        AfaFlowControl.exitMainFlow( str(e) )

    except Exception, e:
        AfaFlowControl.exitMainFlow( str(e) )
