# -*- coding: gbk -*-
###################################################################
#    ��    ��:   �ر��
#==================================================================
#    ˵    ��:   ���������ļ����ɱ��ֵ䵽���ֵ��ӳ�亯��
#    �����ļ�:   crtmaptable2table.py
#    ��������:   2008-06-02
###################################################################

import os,sys,time
from types import *

#��ȡ.ini���������ļ���Ϣ
def get_map_ini(ini_name):
    ini_path = os.environ['AFAP_HOME']
    ini_path = ini_path + "/ini/tablemap/"
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
    
#��ȡ.ini�����������ļ���Ϣ
def get_table_ini(ini_name):
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
    out_path = "/tmp/" + "rccpsMapT" + from_table + "2T" + to_table + ".py"
    return out_path
    
#���ɺ����ļ�ͷ
def input_title(from_table,to_table):
    txt = """\
# -*- coding: gbk -*-
##################################################################
#   ũ����ϵͳ %(from_table)s ���ֵ䵽 %(to_table)s ���ֵ�ӳ�亯��
#
#   ��    �ߣ�  �ر��
#   �����ļ�:   rccpsMapT%(from_table)s2T%(to_table)s.py
#   �޸�ʱ��:   %(date)s
##################################################################
import AfaDBFunc,AfaLoggerFunc
from types import *

def map(form_table,to_table):
    """
    out_file = open(get_path(from_table,to_table),"w")
    print >>out_file,txt % {'from_table': from_table,'to_table': to_table,'date': time.ctime(time.time()),}
    out_file.close()
    
#���ɺ����ļ�����
def input_map(from_table,to_table):
    txt = ""
    ini_name = from_table + "2" + to_table
    ini_list = get_map_ini(ini_name)
    for ini_line in ini_list:
        line_list = str(ini_line).split("|")
        if not line_list[0] in get_table_ini(from_table):
            raise SystemExit("��[" + from_table + "]�в�������[" + line_list[0] + "]")
        if not line_list[1] in get_table_ini(to_table):
            raise SystemExit("��[" + to_table + "]�в�������[" + line_list[1] + "]")
        txt = txt + "    to_table['" + line_list[1] + "'] = from_table['" + line_list[0] + "']\n"
        
    out_file = open(get_path(from_table,to_table),"a")
    print >> out_file,txt
    out_file.close()
    
if len(sys.argv) < 3:
    raise SystemExit("usage: crtmaptable2table.sh from_table to_table")

input_title(sys.argv[1],sys.argv[2])
input_map(sys.argv[1],sys.argv[2])

#print "����" + get_path(sys.argv[1],sys.argv[2]) + "�ļ��ɹ�"
