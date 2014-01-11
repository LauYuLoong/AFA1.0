# -*- coding: gbk -*-
###################################################################
#    作    者:   关彬捷
#==================================================================
#    说    明:   根据配置文件生成表字典到表字典的映射函数
#    程序文件:   crtmaptable2table.py
#    建立日期:   2008-06-02
###################################################################

import os,sys,time
from types import *

#获取.ini拷贝配置文件信息
def get_map_ini(ini_name):
    ini_path = os.environ['AFAP_HOME']
    ini_path = ini_path + "/ini/tablemap/"
    ini_path = ini_path + ini_name + ".ini"

    if not os.path.exists(ini_path):
        raise SystemExit("配置文件:" + ini_path + "不存在")

    ini_file = open(ini_path,"r")
    ini_line = "\n"
    ini_list = []
    while ini_line:
        ini_line = ini_file.readline()
        if len(ini_line) > 1:
             if (ini_line[-1:] == '\n'):
                 ini_list.append(ini_line[0:-1])
             else:
                 ini_list.append(ini_line)
    return ini_list
    
#获取.ini表属性配置文件信息
def get_table_ini(ini_name):
    ini_path = os.environ['AFAP_HOME']
    ini_path = ini_path + "/ini/db/"
    ini_path = ini_path + ini_name + ".ini"

    if not os.path.exists(ini_path):
        raise SystemExit("配置文件:" + ini_path + "不存在")

    ini_file = open(ini_path,"r")
    ini_line = "\n"
    ini_list = []
    while ini_line:
        ini_line = ini_file.readline()
        if len(ini_line) > 1:
             if (ini_line[-1:] == '\n'):
                 ini_list.append(ini_line[0:-1])
             else:
                 ini_list.append(ini_line)
    return ini_list
    
#获取输出函数文件路径
def get_path(from_table,to_table):
    out_path = "/tmp/" + "rccpsMapT" + from_table + "2T" + to_table + ".py"
    return out_path
    
#生成函数文件头
def input_title(from_table,to_table):
    txt = """\
# -*- coding: gbk -*-
##################################################################
#   农信银系统 %(from_table)s 表字典到 %(to_table)s 表字典映射函数
#
#   作    者：  关彬捷
#   程序文件:   rccpsMapT%(from_table)s2T%(to_table)s.py
#   修改时间:   %(date)s
##################################################################
import AfaDBFunc,AfaLoggerFunc
from types import *

def map(form_table,to_table):
    """
    out_file = open(get_path(from_table,to_table),"w")
    print >>out_file,txt % {'from_table': from_table,'to_table': to_table,'date': time.ctime(time.time()),}
    out_file.close()
    
#生成函数文件内容
def input_map(from_table,to_table):
    txt = ""
    ini_name = from_table + "2" + to_table
    ini_list = get_map_ini(ini_name)
    for ini_line in ini_list:
        line_list = str(ini_line).split("|")
        if not line_list[0] in get_table_ini(from_table):
            raise SystemExit("表[" + from_table + "]中不存在列[" + line_list[0] + "]")
        if not line_list[1] in get_table_ini(to_table):
            raise SystemExit("表[" + to_table + "]中不存在列[" + line_list[1] + "]")
        txt = txt + "    to_table['" + line_list[1] + "'] = from_table['" + line_list[0] + "']\n"
        
    out_file = open(get_path(from_table,to_table),"a")
    print >> out_file,txt
    out_file.close()
    
if len(sys.argv) < 3:
    raise SystemExit("usage: crtmaptable2table.sh from_table to_table")

input_title(sys.argv[1],sys.argv[2])
input_map(sys.argv[1],sys.argv[2])

#print "生成" + get_path(sys.argv[1],sys.argv[2]) + "文件成功"
