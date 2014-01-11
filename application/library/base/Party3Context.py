# -*- coding: gbk -*-
##################################################################
#                  第三方通讯结果存放地
#＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
#                作    者：    陈 显 明 
#                修改时间：    20050623
##################################################################

#    判断交易中是否定义了某个指定名称的变量
def existVariable( varName ):
    vars = globals( )
    return vars.has_key( varName )

#    输出所有的变量名称
#def printNames( ):
#    vars = globals( )
#    for var in vars:
#        print var
        
def getNames( ):
    vars = globals( )
    return vars
