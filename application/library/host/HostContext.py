# -*- coding: gbk -*-

#判断交易中是否定义了某个指定名称的变量
def existVariable( varName ):
    vars = globals( )
    return vars.has_key( varName )


def getNames( ):
    vars = globals( )
    #return vars.keys( )
    return vars
