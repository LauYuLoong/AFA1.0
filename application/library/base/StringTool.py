# -*- coding: gbk -*-
##################################################################
#             NATPЭ����ʹ�õ��ַ�����������ģ��
#������������������������������������������������������������������������������
#                ��    �ߣ�    �� �� �� 
#                �޸�ʱ�䣺    20051114
##################################################################

#    ��ָ�����ַ����������ַ�����ָ���ĳ���
def lFillWithChar( srcString, totalLength, fillChar ):
    srcLen = len( srcString )    
    if( srcLen > totalLength ):
        print "Error: string too long,can't fill(", srcLen, ">", totalLength, ")!"
        return None       
    if( srcLen == totalLength ):
        return srcString
            
    if( srcLen < totalLength ):
        result = srcString
        while( srcLen < totalLength ):
            result = fillChar + result
            srcLen = srcLen + 1
        return result
        
#    ��ָ�����ַ����ұ�����ַ�����ָ���ĳ���
def rFillWithChar( srcString, totalLength, fillChar ):
    srcLen = len( srcString )    
    if( srcLen > totalLength ):
        print "Error: string too long,can't fill(", srcLen, ">", totalLength, ")!"
        return None       
    if( srcLen == totalLength ):
        return srcString
            
    if( srcLen < totalLength ):
        result = srcString
        while( srcLen < totalLength ):
            result = result + fillChar
            srcLen = srcLen + 1
        return result

#    ���ַ�����߿�ʼɾ��ָ�����ַ�
def lStripChar( srcString , stripChar ):
    index = 0
    while( srcString[index] == stripChar ):
        index = index + 1    
    return srcString[index:]
 
#    ���ַ����ұ߿�ʼɾ��ָ�����ַ� 
def rStripChar( srcString , stripChar ):
    index = len( srcString )
    while( srcString[index - 1] == stripChar ):
        index = index - 1    
    return srcString[:index]

#    �ַ������/ɾ���ո��
def lFillWithBlank( srcString, totalLength ):
    return lFillWithChar( srcString, totalLength, ' ' )
def rFillWithBlank( srcString, totalLength ):
    return rFillWithChar( srcString, totalLength, ' ' ) 
def lStripBlank( srcString ):
    return lStripChar( srcString , ' ' )       
def rStripBlank( srcString ):
    return rStripChar( srcString , ' ' )

#    �ַ������/ɾ��"0"
def lFillWithZero( srcString, totalLength ):
    return lFillWithChar( srcString, totalLength, '0' )
def rFillWithZero( srcString, totalLength ):
    return rFillWithChar( srcString, totalLength, '0' )    
def lStripZero( srcString ):
    return lStripChar( srcString , '0' )   
def rStripZero( srcString ):
    return rStripChar( srcString , '0' )
    