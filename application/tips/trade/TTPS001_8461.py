# -*- coding: gbk -*-
##################################################################
#   ��˰����.���ɸ�ʽ���Ĳ�ѯ�ͷ���.���淢��
#=================================================================
#   �����ļ�:   TTPS001_8461.py
#   �޸�ʱ��:   2006-04-05
##################################################################
import TradeContext, AfaLoggerFunc, UtilTools, AfaDBFunc
import TipsFunc,AfaAfeFunc,os
from types import *

def SubModuleMainFst( ):
    AfaLoggerFunc.tradeInfo( '�������ɸ�ʽ���Ĳ�ѯ�ͷ���[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' )
    try:
        #=============��ȡ��ǰϵͳʱ��====================
        TradeContext.workDate=UtilTools.GetSysDate( )
        TradeContext.workTime=UtilTools.GetSysTime( )
        
        
        #============У�鹫���ڵ����Ч��==================
        # �����Լ��
        if( not TradeContext.existVariable( "operFlag" ) ):
            return TipsFunc.ExitThisFlow( 'A0001', '��ʶ[operFlag]ֵ������!' )
        
        ##=============��ȡƽ̨��ˮ��==================== 
        #if TipsFunc.GetSerialno( ) == -1 :
        #    raise TipsFunc.flowException( )
        #
        if TradeContext.operFlag=='0': #��ѯ
            if( not TradeContext.existVariable( "beginDate" ) ):
                return TipsFunc.ExitThisFlow( 'A0001', '��ʼ��[beginDate]ֵ������!' )
            if( not TradeContext.existVariable( "endDate" ) ):
                return TipsFunc.ExitThisFlow( 'A0001', '������[endDate]ֵ������!' )
            
            #=================================
            sql="SELECT * FROM TIPS_NOTE WHERE WORKDATE BETWEEN '"+ TradeContext.beginDate +"' AND '"+TradeContext.endDate+"'" 
            if( TradeContext.existVariable( "srcNodeCode" ) and len(TradeContext.srcNodeCode)>0):
                sql=sql+" AND SRCNODECODE ='"+TradeContext.srcNodeCode     +"'"
            if( TradeContext.existVariable( "desNodeCode" ) and len(TradeContext.desNodeCode)>0):
                sql=sql+" AND DESNODECODE ='"+TradeContext.desNodeCode     +"'"
            sql=sql+" ORDER BY WORKDATE,WORKTIME "
            AfaLoggerFunc.tradeInfo(sql)
            records = AfaDBFunc.SelectSql(sql)
            if( records == None ):
                AfaLoggerFunc.tradeFatal(sql)
                return TipsFunc.ExitThisFlow( 'A0002', '���ݿ�����쳣:'+AfaDBFunc.sqlErrMsg )
            elif( len( records )==0 ):
                return TipsFunc.ExitThisFlow( 'A0002', '�����������ļ�¼')
            else:
                records=UtilTools.ListFilterNone( records ,'')
                
                mx_file_name = os.environ['AFAP_HOME'] + '/tmp/' + 'AH_' + TradeContext.teller + '.txt'
                TradeContext.tradeResponse.append(['fileName',  'AH_' + TradeContext.teller + '.txt'])
            
                if (os.path.exists(mx_file_name) and os.path.isfile(mx_file_name)):
                    #�ļ�����,��ɾ��-�ٴ���
                    os.system("rm " + mx_file_name)
            
                sfp = open(mx_file_name, "w")
                AfaLoggerFunc.tradeInfo('��ϸ�ļ�=['+mx_file_name+']')
                i = 0
                while ( i  < len(records) ):
                    A0 = str(records[i][0]).strip()         #WORKDATE
                    A1 = str(records[i][1]).strip()         #WORKTIME
                    A2 = str(records[i][2]).strip()         #SrcNodeCode
                    A3 = str(records[i][3]).strip()         #DesNodeCode
                    A4 = str(records[i][4]).strip()         #SendOrgCode
                    A5 = str(records[i][5]).strip()         #RcvOrgCode 
                    A6 = str(records[i][6]).strip()         #Content    
            
                    sfp.write(A0 +  '|'  +  A1[0:2]+':' +A1[2:4]+':' + A1[4:6] +  '|'  +  A2 +  '|'  +  A3 +  '|'  +  A4 +  '|'  +  A5 +  '|'  +  A6 +  '|'  + '\n')
                    i=i+1
                sfp.close()

        elif TradeContext.operFlag=='1':
            #=============��ȡƽ̨��ˮ��====================
            if TipsFunc.GetSerialno( ) == -1 :
                WrtLog('>>>������:��ȡƽ̨��ˮ���쳣' )
                sys.exit()
            
            #=============�������ͨѶ====================
            AfaAfeFunc.CommAfe()
            if( TradeContext.errorCode != '0000' ):
                return False
            else:
                sql="insert into TIPS_NOTE"
                sql=sql+" values"
                sql=sql+"('"+TradeContext.workDate     +"'"
                sql=sql+",'"+TradeContext.workTime    +"'"
                sql=sql+",'"+TradeContext.srcNodeCode    +"'"
                sql=sql+",'"+TradeContext.desNodeCode    +"'"
                if( TradeContext.existVariable( "sendOrgCode" ) ):
                    sql=sql+",'"+TradeContext.sendOrgCode    +"'"
                else:
                    sql=sql+",''"
                if( TradeContext.existVariable( "rcvOrgCode" ) ):
                    sql=sql+",'"+TradeContext.rcvOrgCode    +"'"
                else:
                    sql=sql+",''"
                sql=sql+",'"+TradeContext.content +"'"
                sql=sql+")"
                AfaLoggerFunc.tradeInfo(sql)
                if( AfaDBFunc.InsertSqlCmt(sql) == -1 ):
                    AfaLoggerFunc.tradeFatal(sql)
                    return TipsFunc.ExitThisFlow( 'A0002', '���ݿ�����쳣:'+AfaDBFunc.sqlErrMsg )
        else :
            return TipsFunc.ExitThisFlow( 'A0002', '�������ʹ���')
            
        #=============�Զ����==================== 
        TradeContext.tradeResponse.append(['errorCode',  '0000'])
        TradeContext.tradeResponse.append(['errorMsg',  '���׳ɹ�'])
        #=============�����˳�====================
        AfaLoggerFunc.tradeInfo( '�˳����ɸ�ʽ���Ĳ�ѯ�ͷ���['+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' )
        return True
    except TipsFunc.flowException, e:
        return False
    except Exception, e:
        return TipsFunc.ExitThisFlow('A9999','ϵͳ�쳣'+str(e) )
def SubModuleMainSnd():
    return True   
