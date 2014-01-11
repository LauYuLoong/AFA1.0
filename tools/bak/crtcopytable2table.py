# -*- coding: gbk -*-
###################################################################
#    作    者:   关彬捷
#==================================================================
#    说    明:   生成表字典到表字典的拷贝函数
#    程序文件:   crtcopytable2table.py
#    建立日期:   2008-06-02
###################################################################

import os,sys,time
from types import *

#获取.ini拷贝配置文件信息
def get_ini(ini_name):
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
    out_path = "/tmp/" + "rccpsCopyT" + from_table + "2T" + to_table + ".py"
    return out_path
    
#生成函数文件头
def input_title(from_table,to_table):
    txt = """\
# -*- coding: gbk -*-
##################################################################
#   农信银系统 %(from_table)s 表字典到 %(to_table)s 表字典拷贝函数
#
#   作    者：  关彬捷
#   程序文件:   rccpsCopyT%(from_table)s2T%(to_table)s.py
#   修改时间:   %(date)s
##################################################################
import AfaDBFunc,AfaLoggerFunc
from types import *

def copy(form_table,to_table):
    """
    out_file = open(get_path(from_table,to_table),"w")
    print >>out_file,txt % {'from_table': from_table,'to_table': to_table,'date': time.ctime(time.time()),}
    out_file.close()
    
#生成拷贝内容
def input_copy(from_table,to_table):
    from_list = get_ini(from_table)
    to_list = get_ini(to_table)
    
    txt = ""
    for to_item in to_list:
        if to_item in from_list:
            txt = txt + "    to_table['" + to_item + "'] = " + "from_table['" + to_item + "']\n"
    
    out_file = open(get_path(from_table,to_table),"a")
    print >> out_file,txt
    out_file.close()

if len(sys.argv) < 3:
    raise SystemExit("usage: crtcopytable2table.sh from_table to_table")

input_title(sys.argv[1],sys.argv[2])
input_copy(sys.argv[1],sys.argv[2])

#print "生成" + get_path(sys.argv[1],sys.argv[2]) + "文件成功"
