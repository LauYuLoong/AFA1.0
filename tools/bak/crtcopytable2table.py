# -*- coding: gbk -*-
###################################################################
#    ��    ��:   �ر��
#==================================================================
#    ˵    ��:   ���ɱ��ֵ䵽���ֵ�Ŀ�������
#    �����ļ�:   crtcopytable2table.py
#    ��������:   2008-06-02
###################################################################

import os,sys,time
from types import *

#��ȡ.ini���������ļ���Ϣ
def get_ini(ini_name):
    ini_path = os.environ['AFAP_HOME']
    ini_path = ini_path + "/ini/db/"
    ini_path = ini_path + ini_name + ".ini"

    if not os.path.exists(ini_path):
        raise SystemExit("�����ļ�:" + ini_path + "������")

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
    
#��ȡ��������ļ�·��
def get_path(from_table,to_table):
    out_path = "/tmp/" + "rccpsCopyT" + from_table + "2T" + to_table + ".py"
    return out_path
    
#���ɺ����ļ�ͷ
def input_title(from_table,to_table):
    txt = """\
# -*- coding: gbk -*-
##################################################################
#   ũ����ϵͳ %(from_table)s ���ֵ䵽 %(to_table)s ���ֵ俽������
#
#   ��    �ߣ�  �ر��
#   �����ļ�:   rccpsCopyT%(from_table)s2T%(to_table)s.py
#   �޸�ʱ��:   %(date)s
##################################################################
import AfaDBFunc,AfaLoggerFunc
from types import *

def copy(form_table,to_table):
    """
    out_file = open(get_path(from_table,to_table),"w")
    print >>out_file,txt % {'from_table': from_table,'to_table': to_table,'date': time.ctime(time.time()),}
    out_file.close()
    
#���ɿ�������
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

#print "����" + get_path(sys.argv[1],sys.argv[2]) + "�ļ��ɹ�"
