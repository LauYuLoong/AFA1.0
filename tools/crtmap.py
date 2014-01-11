# -*- coding: gbk -*-
###################################################################
#    作    者:   关彬捷
#==================================================================
#    说    明:   根据配置文件生成
#                字典到字典
#                或Context到字典
#                或字典到Context
#                的映射函数
#    程序文件:   crtmaptable2table.py
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


#获取.ini拷贝配置文件信息
def get_map_ini(ini_name):
    ini_path = os.environ['AFAP_HOME']
    ini_path = ini_path + "/ini/map/"
    ini_path = ini_path + ini_name + ".ini"

    if not os.path.exists(ini_path):
        raise SystemExit("配置文件:" + ini_path + "不存在")

    ini_file = open(ini_path,"r")
    ini_line = "\n"
    ini_list = []
    #print ini_list
    while ini_line:
        tmp_list = []
        ini_line = ini_file.readline()
        ini_line = trim(ini_line)
        if (ini_line[-1:] == '\n'):
            ini_line = ini_line[0:-1]
        if len(ini_line) > 0:
            for tmp_item in ini_line.split('|'):
                tmp_list.append(tmp_item)
            ini_list.append(tmp_list)
    #print ini_list

    ini_file.close()

    return ini_list
    
    
#获取输出函数文件路径
def get_path(from_type,from_dict,to_type,to_dict,tran_code):
    out_path = "/tmp/" + "rccpsMap" + tran_code + from_type + from_dict + "2" + to_type + to_dict + ".py"
    #print out_path
    return out_path
    
#生成函数文件头
def input_title(from_type,from_dict,to_type,to_dict,tran_code):
    txt = """\
# -*- coding: gbk -*-
##################################################################
#   农信银系统 %(from_dict)s 字典到 %(to_dict)s 字典映射函数
#
#   作    者：  关彬捷
#   程序文件:   rccpsMap%(tran_code)s%(from_type)s%(from_dict)s2%(to_type)s%(to_dict)s.py
#   修改时间:   %(date)s
##################################################################
import AfaLoggerFunc,TradeContext
from types import *
"""
    if from_type == 'D' and to_type == 'D':
        txt = txt + """\
def map(from_dict,to_dict):
        """
    elif from_type == 'D' and to_type == 'C':
        txt = txt + """\
def map(from_dict):
        """
    elif from_type == 'C' and to_type == 'D':
        txt = txt + """\
def map(to_dict):
        """
    out_file = open(get_path(from_type,from_dict,to_type,to_dict,tran_code),"w")
    print >>out_file,txt % {'from_type':from_type,'from_dict': from_dict,'to_type':to_type,'to_dict': to_dict,'date': time.ctime(time.time()),'tran_code': tran_code,}
    out_file.close()
    
#生成函数文件内容
def input_map(from_type,from_dict,to_type,to_dict,tran_code):
    txt = ""
    ini_name = tran_code + from_dict + "2" + to_dict
    ini_list = get_map_ini(ini_name)
    #print from_type
    for line_list in ini_list:
        #print line_list
        #print line_list[2]
        if from_type == 'C':
            txt = txt + "    if " + from_dict + ".existVariable('" + line_list[0] + "'):\n"
        elif from_type == 'D':
            txt = txt + "    if from_dict.has_key('" + line_list[0] + "'):\n"
                
        if to_type == 'C' and from_type == 'D':
            txt = txt + "        " + to_dict + "." + line_list[1] + " = from_dict['" + line_list[0] + "']\n"
            txt = txt + "        AfaLoggerFunc.tradeDebug('" + to_dict + "." + line_list[1] + " = ' + str(" + to_dict + "." + line_list[1] + "))\n"
        if to_type == 'D' and from_type == 'C':
            txt = txt + "        to_dict['" + line_list[1] + "'] = " + from_dict + "." + line_list[0] + "\n"
            txt = txt + "        AfaLoggerFunc.tradeDebug('" + to_dict + "[" + line_list[1] + "] = ' + str(to_dict['" + line_list[1] + "']))\n"
        if to_type == 'D' and from_type == 'D':
            txt = txt + "        to_dict['" + trim(line_list[1]) + "'] = from_dict['" + trim(line_list[0]) + "']\n"
            txt = txt + "        AfaLoggerFunc.tradeDebug('" + to_dict + "[" + line_list[1] + "] = ' + str(to_dict['" + line_list[1] + "']))\n"
            
        if line_list[3] != "":
            txt = txt + "    else:\n"
            txt = txt + "        AfaLoggerFunc.tradeWarn(\"" + line_list[3] + "\")\n"
        else:
            txt = txt + "    else:\n"
            if from_type == 'C':
                txt = txt + "        AfaLoggerFunc.tradeDebug(\"" + from_dict + "." + line_list[0] + "不存在\")\n"
            else:
                txt = txt + "        AfaLoggerFunc.tradeDebug(\"" + from_dict + "['" + line_list[0] + "']不存在\")\n"
            
        if line_list[2] == 'Y':
            txt = txt + "        return False\n"
        
        txt = txt + "\n"
    
    txt = txt + "    return True\n"
        
    out_file = open(get_path(from_type,from_dict,to_type,to_dict,tran_code),"a")
    print >> out_file,txt
    out_file.close()

#========================主函数=======================================
if __name__=='__main__':    
    if len(sys.argv) < 6:
        raise SystemExit("usage: crtmap.sh from_type from_struct to_type to_struct tran_code")

    if sys.argv[1] == "dict":
        from_type = 'D'
    elif sys.argv[1] == "context":
        from_type = 'C'
    else:
        raise SystemExit("无法识别的from结构类型[" + sys.argv[1] + "]")

    if sys.argv[3] == "dict":
        to_type = 'D'
    elif sys.argv[3] == "context":
        to_type = 'C'
    else:
        raise SystemExit("无法识别的to结构类型[" + sys.argv[3] + "]")

    input_title(from_type,sys.argv[2],to_type,sys.argv[4],sys.argv[5])
    input_map(from_type,sys.argv[2],to_type,sys.argv[4],sys.argv[5])

    #print "生成" + get_path(from_type,sys.argv[2],from_type,sys.argv[4],sys.argv[5]) + "文件成功"
