# -*- coding: gbk -*-

#�жϽ������Ƿ�����ĳ��ָ�����Ƶı���
def existVariable( varName ):
    vars = globals( )
    return vars.has_key( varName )


def getNames( ):
    vars = globals( )
    #return vars.keys( )
    return vars
