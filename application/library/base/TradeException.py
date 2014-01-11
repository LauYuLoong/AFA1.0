# -*- coding: gbk -*-
##################################################################
#            自定义的异常类，用于交易异常时提前退出主执行流程
#＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
#                作    者：    陈 显 明 
#                修改时间：    20050602
##################################################################

import exceptions

class TradeException ( exceptions.Exception ): 

    #    构造函数声明，可以不带参数（缺省为None），用于创建该类的一个实例
    def __init__( self, arg = None ):
        self._args = arg  

    #    字符串输出函数，类似于Java的toString（）函数
    def __str__( self ):
        if( self._args != None ):
            return self._args            
        else:
            return "交易发生异常"
            
