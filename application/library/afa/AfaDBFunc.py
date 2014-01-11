# -*- coding: gbk -*-
##################################################################
#   中间业务平台.数据库SQL类
#=================================================================
#   程序文件:   AfaDBFunc.py
#   修改时间:   2006-09-26
##################################################################
import Db2Connection,AfaLoggerFunc

sqlErrMsg=None

def executeQuery( sql ):
    global sqlErrMsg
    sqlErrMsg=''
    curs=None
    try:
        conn=Db2Connection.getConnection( )
        curs=conn.cursor( )
        curs.arraysize=10000
        curs.execute( sql )
        records=curs.fetchall( )
        curs.close( )
        return records
    except Exception, e:
        if( curs != None ):
            curs.close( )
        sqlErrMsg=str( e )
        AfaLoggerFunc.tradeError(sql)
        AfaLoggerFunc.tradeError( sqlErrMsg )
        return None

def executeQueryMany( sql , arraysize=0 ):
    global sqlErrMsg
    sqlErrMsg=''
    curs=None
    try:
        conn=Db2Connection.getConnection( )
        curs=conn.cursor( )
        curs.arraysize=arraysize
        curs.execute( sql )
        records=curs.fetchmany( )
        curs.close( )
        return records
    except Exception, e:
        if( curs != None ):
            curs.close( )
        sqlErrMsg=str( e )
        AfaLoggerFunc.tradeError(sql)
        AfaLoggerFunc.tradeError( sqlErrMsg )
        return None

def executeUpdate( sql ):
    global sqlErrMsg
    sqlErrMsg=''
    curs=None  
    try:
        conn=Db2Connection.getConnection( )
        curs=conn.cursor( )
        curs.execute( sql )
        rowcount=curs.rowcount
        curs.close( )
        return rowcount
    except Exception , e:
        if( curs != None ):
            curs.close( )
        sqlErrMsg=str( e )
        AfaLoggerFunc.tradeError(sql)
        AfaLoggerFunc.tradeError( sqlErrMsg )
        return -1

def executeUpdateCmt( sql ):
    global sqlErrMsg
    sqlErrMsg=''
    curs=None
    try:
        conn=Db2Connection.getConnection( )
        curs=conn.cursor( )
        curs.execute( sql )
        rowcount=curs.rowcount
        curs.execute( "COMMIT" )
        curs.close( )
        return rowcount
    except Exception , e:
        if( curs != None ):
            curs.close( )
        sqlErrMsg=str( e )
        AfaLoggerFunc.tradeError(sql)
        AfaLoggerFunc.tradeError( sqlErrMsg )
        return -1

def StartWorkSql( ):
    global sqlErrMsg
    sqlErrMsg=''
    curs=None
    try:
        conn=Db2Connection.getConnection( )
        curs=conn.cursor( )
        curs.execute( "START TRANSACTION" )
        curs.close( )
        return True
    except Exception , e:
        if( curs != None ):
            curs.close( )
        sqlErrMsg=str( e )
        AfaLoggerFunc.tradeError( sqlErrMsg )
        return False
        
def CommitSql( ):
    global sqlErrMsg
    sqlErrMsg=''
    curs=None
    try:
        conn=Db2Connection.getConnection( )
        curs=conn.cursor( )
        curs.execute( "COMMIT" )
        curs.close( )
        return True
    except Exception , e:
        if( curs != None ):
            curs.close( )
        sqlErrMsg=str( e )
        AfaLoggerFunc.tradeError( sqlErrMsg )
        return False

def RollbackSql( ):
    global sqlErrMsg
    sqlErrMsg=''
    curs=None
    try:
        conn=Db2Connection.getConnection( )
        curs=conn.cursor( )
        curs.execute( "ROLLBACK" )
        curs.close( )
        return True
    except Exception , e:
        if( curs != None ):
            curs.close( )
        sqlErrMsg=str( e )
        AfaLoggerFunc.tradeError( sqlErrMsg )
        return False

def InsertSqlCmt( sql ):
    return  executeUpdateCmt( sql )

def InsertSql( sql ):
    return  executeUpdate( sql )

def UpdateSql( sql ):
    return  executeUpdate( sql )

def UpdateSqlCmt( sql ):
    return  executeUpdateCmt( sql )

def DeleteSql( sql ):
    return  executeUpdate( sql )

def DeleteSqlCmt( sql ):
    return  executeUpdateCmt( sql )

def SelectSql( sql , arraysize=0 ):
    if not arraysize :
        return  executeQuery( sql )
    else:
        return  executeQueryMany( sql , arraysize )
