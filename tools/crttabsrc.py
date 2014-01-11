# -*- coding: gbk -*-
###################################################################
#    作    者:   关彬捷
#==================================================================
#    说    明:   生成数据库操作函数
#    程序文件:   crttabsrc.py
#    建立日期:   2008-06-02
###################################################################

import os,sys,time
from types import *

#去所有空格
def trim( s ):
    temp=[]
    for i in range( len( s ) ):
        if s[i]!='\x20' and s[i]!='\x09':
            temp.append( s[i] )
    return ''.join( temp )

#获取.ini表配置文件内容tuple
def get_ini_tuple(ini_name):
    ini_path = os.environ['AFAP_HOME']
    ini_path = ini_path + "/ini/db/"
    ini_path = ini_path + ini_name + ".ini"

    if not os.path.exists(ini_path):
        raise SystemExit("配置文件:" + ini_path + "不存在")

    ini_file = open(ini_path,"r")
    ini_line = "\n"
    ini_list = []
    while ini_line:
        #print ini_line
        ini_line = ini_file.readline()
        ini_line = trim(ini_line)
        if ini_line[-1:] == '\n':
            ini_line = ini_line[0:-1]
        line_list = str(ini_line).split("|")
        if len(str(line_list[0])) > 1:
            ini_list.append(line_list[0])
    #print tuple(ini_list)

    ini_file.close()

    return tuple(ini_list)
    
#获取.ini表配置文件内容dict
def get_ini_dict(ini_name):
    ini_path = os.environ['AFAP_HOME']
    ini_path = ini_path + "/ini/db/"
    ini_path = ini_path + ini_name + ".ini"

    if not os.path.exists(ini_path):
        raise SystemExit("配置文件:" + ini_path + "不存在")

    ini_file = open(ini_path,"r")
    ini_line = "\n"
    ini_list = []
    ini_dict = {}
    while ini_line:
        #print ini_line
        ini_line = ini_file.readline()
        ini_line = trim(ini_line)
        if ini_line[-1:] == '\n':
            ini_line = ini_line[0:-1]
        line_list = str(ini_line).split("|")
        if len(str(line_list[0])) > 1:
            ini_dict[str(line_list[0])] = line_list[1]
    #print ini_dict
    ini_file.close()
    return ini_dict

#获取输出函数文件路径
def get_path(table_name):
    out_path = "/tmp/rccpsDBT" + sys.argv[1] + ".py"
    return out_path

#生成函数文件头
def input_title(table_name):
    txt = """\
# -*- coding: gbk -*-
##################################################################
#   农信银系统 %(tablename)s 数据库表操作函数
#
#   作    者：  关彬捷
#   程序文件:   rccpsDBT%(tablename)s.py
#   修改时间:   %(date)s
##################################################################
import AfaDBFunc,AfaLoggerFunc
from types import *

table_tuple = %(table_tuple)s
table_dict = %(table_dict)s
    """
    out_file = open(get_path(table_name),"w")
    print >> out_file,txt % {'tablename': table_name,'date': time.ctime(time.time()),'table_tuple': get_ini_tuple(table_name),'table_dict': get_ini_dict(table_name),}
    out_file.close()

#生成chk函数
def input_chk(table_name):
    txt = """\
def chk(where_dict):
    for item in where_dict.keys():
        if item not in table_tuple:
            AfaLoggerFunc.tradeError( '表[%(table_name)s]中无列[' + item + ']' )
            return False
    return True
    """
    out_file = open(get_path(table_name),"a")
    print >> out_file,txt % {'table_name': table_name,}
    out_file.close()

#生成count函数
def input_count(table_name):
    txt = """\
def count( wheresql ):

    sql = "SELECT count(*) FROM %(tablename)s WHERE " + wheresql
    AfaLoggerFunc.tradeInfo(sql)
    records = AfaDBFunc.SelectSql ( sql )
    if (records == None):
        return -1
    else:
        return int(records[0][0])
    """
    out_file = open(get_path(table_name),"a")
    print >> out_file,txt % {'tablename': table_name,}
    out_file.close()

#生成selectu函数
def input_selectu(table_name):
    txt = """\
def selectu( where_dict ):
    if not chk(where_dict):
        return None

    wheresql = ""
    for where_item in where_dict.keys():
        if table_dict[where_item] == 'S':
            wheresql = wheresql + where_item + " LIKE '" + where_dict[where_item] + "' and  "
        else:
            wheresql = wheresql + where_item + " = " + str(where_dict[where_item]) + " and "

    sql = "SELECT %(tableitem)s FROM %(tablename)s WHERE " + wheresql[0:-5]
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
    """
    out_file = open(get_path(table_name),"a")
    print >> out_file,txt % {'tableitem': ','.join(get_ini_tuple(table_name)),'tablename': table_name,}

#生成selectm函数
def input_selectm(table_name):
    txt = """\
def selectm( start_no, sel_size, wheresql, ordersql):

    sql = "SELECT %(tableitem)s FROM (SELECT row_number() over(" + ordersql + ") as rowid,%(tableitem)s from %(tablename)s WHERE " + wheresql + " ) as tab1 where tab1.rowid >= " + str(start_no)
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
    """
    out_file = open(get_path(table_name),"a")
    print >> out_file,txt % {'tableitem': ','.join(get_ini_tuple(table_name)),'tablename': table_name,}

#生成insert函数
def input_insert(table_name):
    txt = """\
def insert( insert_dict ):
    if not chk(insert_dict):
        return -1 

    sql = "INSERT INTO %(tablename)s (" + ','.join(table_tuple) + ") VALUES ( "
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
    """
    out_file = open(get_path(table_name),"a")
    print >> out_file,txt % {'tablename': table_name,}

#生成update函数
def input_update(table_name):
    txt = """\
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


    sql = "UPDATE %(tablename)s SET " + updatesql[0:-1] + " WHERE " + wheresql[0:-5]
    AfaLoggerFunc.tradeInfo(sql)
    return AfaDBFunc.UpdateSql( sql )
    """
    out_file = open(get_path(table_name),"a")
    print >> out_file,txt % {'tablename': table_name,}

#生成delete函数
def input_delete(table_name):
    txt = """\
def delete( where_dict ):
    if not chk(where_dict):
        return -1

    wheresql = ""
    for where_item in where_dict.keys():
        if table_dict[where_item] == 'S':
            wheresql = wheresql + where_item + " LIKE '" + where_dict[where_item] + "' and  "
        else:
            wheresql = wheresql + where_item + " = " + str(where_dict[where_item]) + " and "

    sql = "DELETE FROM %(tablename)s WHERE " + wheresql[0:-5]
    AfaLoggerFunc.tradeInfo(sql)
    return AfaDBFunc.DeleteSql( sql )
    """
    out_file = open(get_path(table_name),"a")
    print >> out_file,txt % {'tablename': table_name,}
        
#生成insertCmt函数
def input_insertCmt(table_name):
    txt = """\
def insertCmt( insert_dict ):
    if not chk(insert_dict):
        return -1 

    sql = "INSERT INTO %(tablename)s (" + ','.join(table_tuple) + ") VALUES ( "
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
    """
    out_file = open(get_path(table_name),"a")
    print >> out_file,txt % {'tablename': table_name,}

#生成updateCmt函数
def input_updateCmt(table_name):
    txt = """\
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


    sql = "UPDATE %(tablename)s SET " + updatesql[0:-1] + " WHERE " + wheresql[0:-5]
    AfaLoggerFunc.tradeInfo(sql)
    return AfaDBFunc.UpdateSqlCmt( sql )
    """
    out_file = open(get_path(table_name),"a")
    print >> out_file,txt % {'tablename': table_name,}

#生成delete函数
def input_deleteCmt(table_name):
    txt = """\
def deleteCmt( where_dict ):
    if not chk(where_dict):
        return -1

    wheresql = ""
    for where_item in where_dict.keys():
        if table_dict[where_item] == 'S':
            wheresql = wheresql + where_item + " LIKE '" + where_dict[where_item] + "' and  "
        else:
            wheresql = wheresql + where_item + " = " + str(where_dict[where_item]) + " and "

    sql = "DELETE FROM %(tablename)s WHERE " + wheresql[0:-5]
    AfaLoggerFunc.tradeInfo(sql)
    return AfaDBFunc.DeleteSqlCmt( sql )
    """
    out_file = open(get_path(table_name),"a")
    print >> out_file,txt % {'tablename': table_name,}

#========================主函数=================================        
if __name__=='__main__':
    if len(sys.argv) < 2:
        raise SystemExit("usage: crttabsrc.sh tablename")

    input_title(sys.argv[1])
    input_chk(sys.argv[1])
    input_count(sys.argv[1])
    input_selectu(sys.argv[1])
    input_selectm(sys.argv[1])
    input_insert(sys.argv[1])
    input_update(sys.argv[1])
    input_delete(sys.argv[1])
    input_insertCmt(sys.argv[1])
    input_updateCmt(sys.argv[1])
    input_deleteCmt(sys.argv[1])

    #print "生成" + get_path(sys.argv[1]) + "文件成功"
