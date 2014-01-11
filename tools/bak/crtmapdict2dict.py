# -*- coding: gbk -*-
###################################################################
#    ��    ��:   �ر��
#==================================================================
#    ˵    ��:   ���������ļ������ֵ䵽�ֵ��ӳ�亯��
#    �����ļ�:   crtmaptable2table.py
#    ��������:   2008-06-02
###################################################################

import os,sys,time
from types import *

#��ȡ.ini���������ļ���Ϣ
def get_map_ini(ini_name):
    ini_path = os.environ['AFAP_HOME']
    ini_path = ini_path + "/ini/dictmap/"
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
def get_path(from_dict,to_dict):
    out_path = "/tmp/" + "rccpsMapD" + from_dict + "2D" + to_dict + ".py"
    return out_path
    
#���ɺ����ļ�ͷ
def input_title(from_dict,to_dict):
    txt = """\
# -*- coding: gbk -*-
##################################################################
#   ũ����ϵͳ %(from_dict)s �ֵ䵽 %(to_dict)s �ֵ�ӳ�亯��
#
#   ��    �ߣ�  �ر��
#   �����ļ�:   rccpsMapD%(from_dict)s2D%(to_dict)s.py
#   �޸�ʱ��:   %(date)s
##################################################################
import AfaDBFunc,AfaLoggerFunc
from types import *

def map(form_dict,to_dict):
    """
    out_file = open(get_path(from_dict,to_dict),"w")
    print >>out_file,txt % {'from_dict': from_dict,'to_dict': to_dict,'date': time.ctime(time.time()),}
    out_file.close()
    
#���ɺ����ļ�����
def input_map(from_dict,to_dict):
    txt = ""
    ini_name = from_dict + "2" + to_dict
    ini_list = get_map_ini(ini_name)
    for ini_line in ini_list:
        line_list = str(ini_line).split("|")
        txt = txt + "    if from_dict.has_key(\"" + line_list[0] + "\")"
        txt = txt + "        to_dict[\"" + line_list[1] + "\"] = from_dict[\"" + line_list[0] + "\"]\n"
        
    out_file = open(get_path(from_dict,to_dict),"a")
    print >> out_file,txt
    out_file.close()
    
if len(sys.argv) < 3:
    raise SystemExit("usage: crtmapdict2dict.sh from_dict to_dict")

input_title(sys.argv[1],sys.argv[2])
input_map(sys.argv[1],sys.argv[2])

#print "����" + get_path(sys.argv[1],sys.argv[2]) + "�ļ��ɹ�"
