# -*- coding: gbk -*-
##################################################################
#             NATP协议中使用的字符串操作工具模块
#＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
#                作    者：    陈 显 明 
#                修改时间：    20051114
##################################################################

#    用指定的字符从左边填充字符串到指定的长度
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
        
#    用指定的字符从右边填充字符串到指定的长度
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

#    从字符串左边开始删除指定的字符
def lStripChar( srcString , stripChar ):
    index = 0
    while( srcString[index] == stripChar ):
        index = index + 1    
    return srcString[index:]
 
#    从字符串右边开始删除指定的字符 
def rStripChar( srcString , stripChar ):
    index = len( srcString )
    while( srcString[index - 1] == stripChar ):
        index = index - 1    
    return srcString[:index]

#    字符串填充/删除空格符
def lFillWithBlank( srcString, totalLength ):
    return lFillWithChar( srcString, totalLength, ' ' )
def rFillWithBlank( srcString, totalLength ):
    return rFillWithChar( srcString, totalLength, ' ' ) 
def lStripBlank( srcString ):
    return lStripChar( srcString , ' ' )       
def rStripBlank( srcString ):
    return rStripChar( srcString , ' ' )

#    字符串填充/删除"0"
def lFillWithZero( srcString, totalLength ):
    return lFillWithChar( srcString, totalLength, '0' )
def rFillWithZero( srcString, totalLength ):
    return rFillWithChar( srcString, totalLength, '0' )    
def lStripZero( srcString ):
    return lStripChar( srcString , '0' )   
def rStripZero( srcString ):
    return rStripChar( srcString , '0' )
    