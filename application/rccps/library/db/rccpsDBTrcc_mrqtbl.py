# -*- coding: gbk -*-
##################################################################
#   农信银系统 rcc_mrqtbl 数据库表操作函数
#
#   作    者：  关彬捷
#   程序文件:   rccpsDBTrcc_mrqtbl.py
#   修改时间:   Tue Dec 16 19:39:22 2008
##################################################################
import AfaDBFunc,AfaLoggerFunc
from types import *

table_tuple = ('BJEDTE', 'BSPSQN', 'TRCCO', 'SNDBNKCO', 'SNDBNKNM', 'RCVBNKCO', 'RCVBNKNM', 'SNDMBRCO', 'RCVMBRCO', 'TRCDAT', 'TRCNO', 'NPCBKID', 'NPCBKNM', 'NPCACNT', 'OCCAMT', 'REMARK', 'PRCCO', 'STRINFO', 'NOTE1', 'NOTE2', 'NOTE4', 'NOTE3')
table_dict = {'TRCDAT': 'S', 'NPCBKID': 'S', 'PRCCO': 'S', 'SNDMBRCO': 'S', 'RCVMBRCO': 'S', 'OCCAMT': 'F', 'BJEDTE': 'S', 'REMARK': 'S', 'NPCACNT': 'S', 'BSPSQN': 'S', 'RCVBNKCO': 'S', 'SNDBNKNM': 'S', 'TRCCO': 'S', 'RCVBNKNM': 'S', 'NPCBKNM': 'S', 'STRINFO': 'S', 'NOTE1': 'S', 'NOTE3': 'S', 'NOTE2': 'S', 'NOTE4': 'S', 'SNDBNKCO': 'S', 'TRCNO': 'S'}
    
def chk(where_dict):
    for item in where_dict.keys():
        if item not in table_tuple:
            AfaLoggerFunc.tradeError( '表[rcc_mrqtbl]中无列[' + item + ']' )
            return False
    return True
    
def count( wheresql ):

    sql = "SELECT count(*) FROM rcc_mrqtbl WHERE " + wheresql
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

    sql = "SELECT BJEDTE,BSPSQN,TRCCO,SNDBNKCO,SNDBNKNM,RCVBNKCO,RCVBNKNM,SNDMBRCO,RCVMBRCO,TRCDAT,TRCNO,NPCBKID,NPCBKNM,NPCACNT,OCCAMT,REMARK,PRCCO,STRINFO,NOTE1,NOTE2,NOTE4,NOTE3 FROM rcc_mrqtbl WHERE " + wheresql[0:-5]
    AfaLoggerFunc.tradeInfo(sql)
    records = AfaDBFunc.SelectSql( sql )
    if (records == None):
        return None
    elif (len(records) > 1):
        AfaLoggerFunc.tradeError("查询结果非唯一,请检查查询条件[" + wheresql[0:-5] + "]")
        return None
    elif (len(records) == 0):
        AfaLoggerFunc.tradeError("查询结果为空,查询条件[" + wheresql[0:-5] + "]")
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

    sql = "SELECT BJEDTE,BSPSQN,TRCCO,SNDBNKCO,SNDBNKNM,RCVBNKCO,RCVBNKNM,SNDMBRCO,RCVMBRCO,TRCDAT,TRCNO,NPCBKID,NPCBKNM,NPCACNT,OCCAMT,REMARK,PRCCO,STRINFO,NOTE1,NOTE2,NOTE4,NOTE3 FROM (SELECT row_number() over(" + ordersql + ") as rowid,BJEDTE,BSPSQN,TRCCO,SNDBNKCO,SNDBNKNM,RCVBNKCO,RCVBNKNM,SNDMBRCO,RCVMBRCO,TRCDAT,TRCNO,NPCBKID,NPCBKNM,NPCACNT,OCCAMT,REMARK,PRCCO,STRINFO,NOTE1,NOTE2,NOTE4,NOTE3 from rcc_mrqtbl WHERE " + wheresql + " ) as tab1 where tab1.rowid >= " + str(start_no)
    AfaLoggerFunc.tradeInfo(sql)
    records = AfaDBFunc.SelectSql( sql, sel_size )
    if (records == None):
        return None
    elif (len(records) == 0):
        AfaLoggerFunc.tradeWarn("查询结果为空,查询条件[" + wheresql + "]")
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

    sql = "INSERT INTO rcc_mrqtbl (" + ','.join(table_tuple) + ") VALUES ( "
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


    sql = "UPDATE rcc_mrqtbl SET " + updatesql[0:-1] + " WHERE " + wheresql[0:-5]
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

    sql = "DELETE FROM rcc_mrqtbl WHERE " + wheresql[0:-5]
    AfaLoggerFunc.tradeInfo(sql)
    return AfaDBFunc.DeleteSql( sql )
    
def insertCmt( insert_dict ):
    if not chk(insert_dict):
        return -1 

    sql = "INSERT INTO rcc_mrqtbl (" + ','.join(table_tuple) + ") VALUES ( "
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


    sql = "UPDATE rcc_mrqtbl SET " + updatesql[0:-1] + " WHERE " + wheresql[0:-5]
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

    sql = "DELETE FROM rcc_mrqtbl WHERE " + wheresql[0:-5]
    AfaLoggerFunc.tradeInfo(sql)
    return AfaDBFunc.DeleteSqlCmt( sql )
    
