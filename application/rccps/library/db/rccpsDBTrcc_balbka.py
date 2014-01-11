# -*- coding: gbk -*-
##################################################################
#   ũ����ϵͳ rcc_balbka ���ݿ���������
#
#   ��    �ߣ�  �ر��
#   �����ļ�:   rccpsDBTrcc_balbka.py
#   �޸�ʱ��:   Tue Dec 16 19:39:19 2008
##################################################################
import AfaDBFunc,AfaLoggerFunc
from types import *

table_tuple = ('BJEDTE', 'BSPSQN', 'BRSFLG', 'BESBNO', 'BEACSB', 'BETELR', 'BEAUUS', 'BEAUPS', 'TERMID', 'OPRNO', 'OPRATTNO', 'NCCWKDAT', 'TRCCO', 'TRCDAT', 'TRCNO', 'MSGFLGNO', 'SNDMBRCO', 'RCVMBRCO', 'SNDBNKCO', 'SNDBNKNM', 'RCVBNKCO', 'RCVBNKNM', 'CUR', 'CHRGTYP', 'LOCCUSCHRG', 'CUSCHRG', 'PYRACC', 'PYEACC', 'STRINFO', 'CERTTYPE', 'CERTNO', 'BNKBKNO', 'AVLBAL', 'ACCBAL', 'PRCCO', 'PRCINFO', 'NOTE1', 'NOTE2', 'NOTE3', 'NOTE4')
table_dict = {'BEAUUS': 'S', 'TRCDAT': 'S', 'MSGFLGNO': 'S', 'TRCCO': 'S', 'STRINFO': 'S', 'SNDMBRCO': 'S', 'RCVMBRCO': 'S', 'CUR': 'S', 'BJEDTE': 'S', 'BNKBKNO': 'S', 'BSPSQN': 'S', 'RCVBNKCO': 'S', 'OPRATTNO': 'S', 'CERTTYPE': 'S', 'TERMID': 'S', 'SNDBNKNM': 'S', 'BEACSB': 'S', 'RCVBNKNM': 'S', 'NCCWKDAT': 'S', 'BRSFLG': 'S', 'CERTNO': 'S', 'PYEACC': 'S', 'CHRGTYP': 'S', 'PRCCO': 'S', 'PYRACC': 'S', 'AVLBAL': 'F', 'PRCINFO': 'S', 'CUSCHRG': 'F', 'LOCCUSCHRG': 'F', 'NOTE1': 'S', 'OPRNO': 'S', 'NOTE3': 'S', 'NOTE2': 'S', 'NOTE4': 'S', 'BEAUPS': 'S', 'SNDBNKCO': 'S', 'TRCNO': 'S', 'BESBNO': 'S', 'BETELR': 'S', 'ACCBAL': 'F'}
    
def chk(where_dict):
    for item in where_dict.keys():
        if item not in table_tuple:
            AfaLoggerFunc.tradeError( '��[rcc_balbka]������[' + item + ']' )
            return False
    return True
    
def count( wheresql ):

    sql = "SELECT count(*) FROM rcc_balbka WHERE " + wheresql
    AfaLoggerFunc.tradeInfo(sql)
    records = AfaDBFunc.SelectSql ( sql )
    if (records == None):
        return -1
    else:
        return int(records[0][0])
    
def selectu( where_dict ):
    if not chk(where_dict):
        return None

    wheresql = ""
    for where_item in where_dict.keys():
        if table_dict[where_item] == 'S':
            wheresql = wheresql + where_item + " LIKE '" + where_dict[where_item] + "' and  "
        else:
            wheresql = wheresql + where_item + " = " + str(where_dict[where_item]) + " and "

    sql = "SELECT BJEDTE,BSPSQN,BRSFLG,BESBNO,BEACSB,BETELR,BEAUUS,BEAUPS,TERMID,OPRNO,OPRATTNO,NCCWKDAT,TRCCO,TRCDAT,TRCNO,MSGFLGNO,SNDMBRCO,RCVMBRCO,SNDBNKCO,SNDBNKNM,RCVBNKCO,RCVBNKNM,CUR,CHRGTYP,LOCCUSCHRG,CUSCHRG,PYRACC,PYEACC,STRINFO,CERTTYPE,CERTNO,BNKBKNO,AVLBAL,ACCBAL,PRCCO,PRCINFO,NOTE1,NOTE2,NOTE3,NOTE4 FROM rcc_balbka WHERE " + wheresql[0:-5]
    AfaLoggerFunc.tradeInfo(sql)
    records = AfaDBFunc.SelectSql( sql )
    if (records == None):
        return None
    elif (len(records) > 1):
        AfaLoggerFunc.tradeError("��ѯ�����Ψһ,�����ѯ����[" + wheresql[0:-5] + "]")
        return None
    elif (len(records) == 0):
        AfaLoggerFunc.tradeError("��ѯ���Ϊ��,��ѯ����[" + wheresql[0:-5] + "]")
        tmp_dict = {}
        return tmp_dict
    else:
        tmp_dict = {}
        for i in xrange(0,len(table_tuple)):
            if len(str(records[0][i])) == 0:
                tmp_dict[table_tuple[i]] = ""
            else:
                tmp_dict[table_tuple[i]] = records[0][i]
        #AfaLoggerFunc.tradeInfo("return return_dict:" + str(tmp_dict))
        return tmp_dict
    
def selectm( start_no, sel_size, wheresql, ordersql):

    sql = "SELECT BJEDTE,BSPSQN,BRSFLG,BESBNO,BEACSB,BETELR,BEAUUS,BEAUPS,TERMID,OPRNO,OPRATTNO,NCCWKDAT,TRCCO,TRCDAT,TRCNO,MSGFLGNO,SNDMBRCO,RCVMBRCO,SNDBNKCO,SNDBNKNM,RCVBNKCO,RCVBNKNM,CUR,CHRGTYP,LOCCUSCHRG,CUSCHRG,PYRACC,PYEACC,STRINFO,CERTTYPE,CERTNO,BNKBKNO,AVLBAL,ACCBAL,PRCCO,PRCINFO,NOTE1,NOTE2,NOTE3,NOTE4 FROM (SELECT row_number() over(" + ordersql + ") as rowid,BJEDTE,BSPSQN,BRSFLG,BESBNO,BEACSB,BETELR,BEAUUS,BEAUPS,TERMID,OPRNO,OPRATTNO,NCCWKDAT,TRCCO,TRCDAT,TRCNO,MSGFLGNO,SNDMBRCO,RCVMBRCO,SNDBNKCO,SNDBNKNM,RCVBNKCO,RCVBNKNM,CUR,CHRGTYP,LOCCUSCHRG,CUSCHRG,PYRACC,PYEACC,STRINFO,CERTTYPE,CERTNO,BNKBKNO,AVLBAL,ACCBAL,PRCCO,PRCINFO,NOTE1,NOTE2,NOTE3,NOTE4 from rcc_balbka WHERE " + wheresql + " ) as tab1 where tab1.rowid >= " + str(start_no)
    AfaLoggerFunc.tradeInfo(sql)
    records = AfaDBFunc.SelectSql( sql, sel_size )
    if (records == None):
        return None
    elif (len(records) == 0):
        AfaLoggerFunc.tradeWarn("��ѯ���Ϊ��,��ѯ����[" + wheresql + "]")
        tmp_list = []
        return tmp_list
    else:
        tmp_list = []
        for i in xrange(0,len(records)):
            tmp_dict = {}
            for j in xrange(0,len(table_tuple)):
                if len(str(records[i][j])) == 0:
                    tmp_dict[str(table_tuple[j])] = ""
                else:
                    tmp_dict[str(table_tuple[j])] = records[i][j]
            tmp_list.append(tmp_dict)
        #AfaLoggerFunc.tradeInfo("return list:" + str(tmp_list))
        return tmp_list
    
def insert( insert_dict ):
    if not chk(insert_dict):
        return -1 

    sql = "INSERT INTO rcc_balbka (" + ','.join(table_tuple) + ") VALUES ( "
    for table_item in table_tuple:
        if table_dict[table_item] == 'S':
            if insert_dict.has_key(table_item):
                sql = sql + "'" + insert_dict[table_item] + "',"
            else:
                sql = sql + "'',"
        else:
            if insert_dict.has_key(table_item) and str(insert_dict[table_item]) != '':
                sql = sql + str(insert_dict[table_item]) + ","
            else:
                sql = sql + "0,"
    sql = sql[0:-1] + ")"

    AfaLoggerFunc.tradeInfo(sql)
    return AfaDBFunc.InsertSql( sql )
    
def update( update_dict,where_dict ):
    if not chk(update_dict):
        return -1
    if not chk(where_dict):
        return -1

    updatesql = ""
    for update_item in update_dict.keys():
        if table_dict[update_item] == 'S':
            updatesql = updatesql + update_item + " = '" + update_dict[update_item] + "',"
        else:
            updatesql = updatesql + update_item + " = " + str(update_dict[update_item]) + ","

    wheresql = ""
    for where_item in where_dict.keys():
        if table_dict[where_item] == 'S':
            wheresql = wheresql + where_item + " LIKE '" + where_dict[where_item] + "' and  "
        else:
            wheresql = wheresql + where_item + " = " + str(where_dict[where_item]) + " and "


    sql = "UPDATE rcc_balbka SET " + updatesql[0:-1] + " WHERE " + wheresql[0:-5]
    AfaLoggerFunc.tradeInfo(sql)
    return AfaDBFunc.UpdateSql( sql )
    
def delete( where_dict ):
    if not chk(where_dict):
        return -1

    wheresql = ""
    for where_item in where_dict.keys():
        if table_dict[where_item] == 'S':
            wheresql = wheresql + where_item + " LIKE '" + where_dict[where_item] + "' and  "
        else:
            wheresql = wheresql + where_item + " = " + str(where_dict[where_item]) + " and "

    sql = "DELETE FROM rcc_balbka WHERE " + wheresql[0:-5]
    AfaLoggerFunc.tradeInfo(sql)
    return AfaDBFunc.DeleteSql( sql )
    
def insertCmt( insert_dict ):
    if not chk(insert_dict):
        return -1 

    sql = "INSERT INTO rcc_balbka (" + ','.join(table_tuple) + ") VALUES ( "
    for table_item in table_tuple:
        if table_dict[table_item] == 'S':
            if insert_dict.has_key(table_item):
                sql = sql + "'" + insert_dict[table_item] + "',"
            else:
                sql = sql + "'',"
        else:
            if insert_dict.has_key(table_item) and str(insert_dict[table_item]) != '':
                sql = sql + str(insert_dict[table_item]) + ","
            else:
                sql = sql + "0,"
    sql = sql[0:-1] + ")"

    AfaLoggerFunc.tradeInfo(sql)
    return AfaDBFunc.InsertSqlCmt( sql )
    
def updateCmt( update_dict,where_dict ):
    if not chk(update_dict):
        return -1
    if not chk(where_dict):
        return -1

    updatesql = ""
    for update_item in update_dict.keys():
        if table_dict[update_item] == 'S':
            updatesql = updatesql + update_item + " = '" + update_dict[update_item] + "',"
        else:
            updatesql = updatesql + update_item + " = " + str(update_dict[update_item]) + ","

    wheresql = ""
    for where_item in where_dict.keys():
        if table_dict[where_item] == 'S':
            wheresql = wheresql + where_item + " LIKE '" + where_dict[where_item] + "' and  "
        else:
            wheresql = wheresql + where_item + " = " + str(where_dict[where_item]) + " and "


    sql = "UPDATE rcc_balbka SET " + updatesql[0:-1] + " WHERE " + wheresql[0:-5]
    AfaLoggerFunc.tradeInfo(sql)
    return AfaDBFunc.UpdateSqlCmt( sql )
    
def deleteCmt( where_dict ):
    if not chk(where_dict):
        return -1

    wheresql = ""
    for where_item in where_dict.keys():
        if table_dict[where_item] == 'S':
            wheresql = wheresql + where_item + " LIKE '" + where_dict[where_item] + "' and  "
        else:
            wheresql = wheresql + where_item + " = " + str(where_dict[where_item]) + " and "

    sql = "DELETE FROM rcc_balbka WHERE " + wheresql[0:-5]
    AfaLoggerFunc.tradeInfo(sql)
    return AfaDBFunc.DeleteSqlCmt( sql )
    
