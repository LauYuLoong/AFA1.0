# -*- coding: gbk -*-
##################################################################
#   农信银系统.函数检查类
#=================================================================
#   程序文件:   rccpsChkTrcbka.py
#   修改时间:   2008-06-07
##################################################################
import TradeContext,AfaLoggerFunc
from types import *
import exceptions,os,time

################################################################################
# 函数名:    ChkTrcbka()
# 参数:      无 
# 返回值：    True  设置状态成功    False 设置状态失败
# 函数说明：  检查表中的字段是否存在 
# 编写时间：   2008-6-5
# 作者：       刘雨龙
################################################################################
def ChkTrcbka():
    #=====开始字段检查====
    AfaLoggerFunc.tradeInfo( '>>>开始Trcbka表字段检查' )
    #=====判断交易日期是否存在====
    if  TradeContext.existVariable( "BEJDTE" ):
        trcbka["BJEDTE"] = TradeContext.BJEDTE
    else:
        TradeContext.errorCode = 'O201'
        TradeContext.errorMsg  = '交易日期不存在'
        return False
    #=====判断报单序号是否存在====
    if  TradeContext.existVariable( "BSPSQN" ):
        trcbka["BSPSQN"] = TradeContext.BSPSQN
    else:
        TradeContext.errorCode = 'M006'
        TradeContext.errorMsg  = '报单序号不存在'
        return False
    #====判断往来账标识是否存在====
    if  TradeContext.existVariable( "BRSFLG" ):
        trcbka["BRSFLG"] = TradeContext.BRSFLG
    else:
        TradeContext.errorCode = 'M999'
        TradeContext.errorMsg = '往来账标识不存在'
        return False
    #=====判断机构号是否存在====
    if TradeContext.existVariable( "BESBNO" ):
        trcbka["BESBNO"] = TradeContext.BESBNO
    else:
        TradeContext.errorCode = 'M999'
        TradeContext.errorMsg  = '机构号不存在'
        return False
    #====判断账务机构号是否存在====
    if TradeContext.existVariable( "BEACSB" ):
        trcbka["BEACSB"] = TradeContext.BEACSB
    else:
        trcbka["BEACSB"] = ''
    #=====判断柜员号是否存在====
    if TradeContext.existVariable( "BETELR" ):
        trcbka["BETELR"] = TradeContext.BEACSB
    else:
        TradeContext.errorCode = 'M999'
        TradeContext.errorMsg  = '柜员号不存在'
        return False
    #=====判断授权柜员号====
    if TradeContext.existVariable( "BEAUUS" ):
        trcbka["BEAUUS"] = TradeContext.BEAUUS
    else:
        trcbka["BEAUUS"] = ''
    #====判断借贷标志是否存在====
    if TradeContext.existVariable( "DCFLG" ):
        trcbka["DCFLG"] = TradeContext.DCFLG
    else:
        trcbka["DCFLG"] = ''
    #=====判断业务序号是否存在====
    if TradeContext.existVariable( "OPRNO" ):
        trcbka["OPRNO"] = TradeContext.OPRNO
    else:
        trcbka["DCFLG"] = ''
    #=====判断业务属性是否存在====
    if TradeContext.existVariable( "OPRATTNO" ):
        trcbka["OPRATTNO"] = TradeContext.OPRATTNO
    else:
        trcbka["OPRATTNO"] = ''
    #=====判断中心日期是否存在====
    if TradeContext.existVariable( "NCCWKDAT" ):
        trcbka["NCCWKDAT"]= TradeContext.NCCWKDAT
    else:
        TradeContext.errorCode = 'M999'
        TradeContext.errorMsg  = '中心日期不存在'
        return False
    #=====判断交易代码是否存在====
    if TradeContext.existVariable( "TRCCO" ):
        trcbka["TRCCO"] = TradeContext.TRCCO
    else:
        TradeContext.errorCode = 'M999'
        TradeContext.errorMsg  = '交易代码不存在'
        return False
    #=====判断委托日期是否存在====
    if TradeContext.existVariable( 'TRCDAT' ):
        trcbka['TRCDAT'] = TradeContext.TRCDAT
    else:
        trcbka['TRCDAT'] = ''
    #=====判断交易流水号是否存在====
    if TradeContext.existVariable( 'TRCNO' ):
        trcbka['TRCNO'] = TradeContext.TRCNO
    else:
        TradeContext.errorCode = 'M999'
        TradeContext.errorMsg  = '交易流水号不存在'
        return False
    #=====判断发送行号是否存在====
    if TradeContext.existVariable( 'SNDBNKCO' ):
        trcbka['SNDBNKCO'] = TradeContext.SNDBNKCO
    else:
        trcbka['SNDBNKCO'] = ''
    #=====判断发送行名是否存在====
    if TradeContext.existVariable( 'SNDBNKNM' ):
        trcbka['SNDBNKCO'] = TradeContext.SNDBNKNM
    else:
        trcbka['SNDBNKCO'] = ''
    #=====判断接收行号是否存在====
    if TradeContext.existVariable( 'RCVBNKCO' ):
        trcbka['RCVBNKCO'] = TradeContext.RCVBNKCO
    else:
        trcbka['RCVBNKCO'] = ''
    #====判断接收行名是否存在====
    if TradeContext.existVariable( 'RCVBNKNM' ):
        trcbka['RCVBNKNM'] = TradeContext.RCVBNKNM
    else:
        trcbka['RCVBNKNM'] = ''
    #=====判断接收行名是否存在====
    if TradeContext.existVariable( 'CUR' ):
        trcbka['CUR'] = TradeContext.CUR
    else:
        TradeContext.errorCode = 'M999'
        TradeContext.errorMsg  = '币种不存在'
        return False
    #=====判断交易金额是否存在====
    if TradeContext.existVariable( 'OCCAMT' ):
        trcbka['OCCAMT'] = TradeContext.OCCAMT
    else:
        TradeContext.errorCode = 'M999'
        TradeContext.errorMsg  = '交易金额不存在'
        return False
    #=====判断手续费收取方式是否存在====
    if TradeContext.existVariable( 'CHRGTYP' ):
        trcbka['CHRGTYP'] = TradeContext.CHRGTYP
    else:
        trcbka['CHRGTYP'] = ''
    #=====判断本地客户手续费是否存在====
    if TradeContext.existVariable( 'LOCCUSCHRG' ):
        trcbka['LOCCUSCHRG'] = TradeContext.LOCCUSCHRG
    else:
        trcbka['LOCCUSCHRG'] = ''
    #=====判断异地客户手续费是否存在====
    if TradeContext.existVariable( 'CUSCHRG' ):
        trcbka['CUSCHRG'] = TradeContext.CUSCHRG
    else:
        trcbka['CUSCHRG'] = ''
    #=====判断付款人账号是否存在====
    if TradeContext.existVariable( 'PYRACC' ):
        trcbka['PYRACC'] = TradeContext.PYRACC
    else:
        trcbka['PYRACC'] = ''
    #=====判断付款人户名是否存在====
    if TradeContext.existVariable( 'PYRNAM' ):
        trcbka['PYRNAM'] = TradeContext.PYRNAM
    else:
        trcbka['PYRNAM'] = ''
    #=====判断付款人地址是否存在====
    if TradeContext.existVariable( 'PYRADDR' ):
        trcbka['PYRADDR'] = TradeContext.PYRADDR
    else:
        trcbka['PYRADDR'] = ''
    #=====判断收款人账号是否存在====
    if TradeContext.existVariable( 'PYEACC' ):
        trcbka['PYEACC'] = TradeContext.PYEACC
    else:
        trcbka['PYEACC'] = ''
    #=====判断收款人户名是否存在====
    if TradeContext.existVariable( 'PYENAM' ):
        trcbka['PYENAM'] = TradeContext.PYENAM
    else:
        trcbka['PYENAM'] = ''   
    #=====判断付款人地址是否存在====
    if TradeContext.existVariable( 'PYEADDR' ):
        trcbka['PYEADDR'] = TradeContext.PYEADDR
    else:
        trcbka['PYEADDR'] = ''
    #=====判断密押是否存在====
    if TradeContext.existVariable( 'SEAL' ):
        trcbka['SEAL'] = TradeContext.SEAL
    else:
        trcbka['SEAL'] = ''
    #=====判断用途是否存在====
    if TradeContext.existVariable( 'USE' ):
        trcbka['USE'] = TradeContext.USE
    else:
        trcbka['USE'] = ''
    #=====判断备注是否存在====
    if TradeContext.existVariable( 'REMARK' ):
        trcbka['REMARK'] = TradeContext.REMARK
    else:
        trcbka['REMARK'] = ''
    #=====判断票据种类是否存在====
    if TradeContext.existVariable( 'BILTYP' ):
        trcbka['BILTYP'] = TradeContext.BILTYP
    else:
        trcbka['BILTYP'] = ''
    #=====判断票据日期是否存在====
    if TradeContext.existVariable( 'BILDAT' ):
        trcbka['BILDAT'] = TradeContext.BILDAT
    else:
        trcbka['BILDAT'] = ''
    #=====判断票据号码是否存在====
    if TradeContext.existVariable( 'BILNO' ):
        trcbka['BILNO'] = TradeContext.BILNO
    else:
        trcbka['BILNO'] = ''
    #=====判断原托收金额是否存在====
    if TradeContext.existVariable( 'COMAMT' ):
        trcbka['COMAMT'] = TradeContext.COMAMT
    else:
        trcbka['COMAMT'] = ''
    #=====判断多付金额是否存在====
    if TradeContext.existVariable( 'OVPAYAMT' ):
        trcbka['OVPAYAMT'] = TradeContext.OVPAYAMT
    else:
        trcbka['OVPAYAMT'] = ''
    #=====判断赔偿金金额是否存在====
    if TradeContext.existVariable( 'CPSAMT' ):
        trcbka['CPSAMT'] = TradeContext.CPSAMT
    else:
        trcbka['CPSAMT'] = ''
    #=====判断拒付金额是否存在====
    if TradeContext.existVariable( 'RFUAMT' ):
        trcbka['RFUAMT'] = TradeContext.RFUAMT
    else:
        trcbka['RFUAMT'] = ''
    #=====判断凭证种类是否存在====
    if TradeContext.existVariable( 'CERTTYPE' ):
        trcbka['CERTTYPE'] = TradeContext.CERTTYPE
    else:
        trcbka['CERTTYPE'] = ''
    #=====判断凭证号码是否存在====
    if TradeContext.existVariable( 'CERTNO' ):
        trcbka['CERTNO'] = TradeContext.CERTNO
    else:
        trcbka['CERTNO'] = ''
    #=====判断原交易日期是否存在====
    if TradeContext.existVariable( 'BOJEDT' ):
        trcbka['BOJEDT'] = TradeContext.BOJEDT
    else:
        trcbka['BOJEDT'] = ''
    #=====判断原报单序号是否存在====
    if TradeContext.existVariable( 'BOSPSQ' ):
        trcbka['BOSPSQ'] = TradeContext.BOSPSQ
    else:
        trcbka['BOSPSQ'] = ''
    #=====判断原委托日期是否存在====
    if TradeContext.existVariable( 'ORTRCDAT' ):
        trcbka['ORTRCDAT'] = TradeContext.ORTRCDAT
    else:
        trcbka['ORTRCDAT'] = ''
    #=====判断原交易代码是否存在====
    if TradeContext.existVariable( 'ORTRCCO' ):
        trcbka['ORTRCCO'] = TradeContext.ORTRCCO
    else:
        trcbka['ORTRCCO'] = ''
    #=====判断原交易流水号是否存在====
    if TradeContext.existVariable( 'ORTRCNO' ):
        trcbka['ORTRCNO'] = TradeContext.ORTRCNO
    else:
        trcbka['ORTRCNO'] = ''
    #=====判断原发送行号是否存在====
    if TradeContext.existVariable( 'ORSNDBNK' ):
        trcbka['ORSNDBNK'] = TradeContext.ORSNDBNK
    else:
        trcbka['ORSNDBNK'] = ''
    #=====判断原接收行号是否存在====
    if TradeContext.existVariable( 'ORRCVBNK' ):
        trcbka['ORRCVBNK'] = TradeContext.ORRCVBNK
    else:
        trcbka['ORRCVBNK'] = ''
    #=====判断附言是否存在====
    if TradeContext.existVariable( 'STRINFO' ):
        trcbka['STRINFO'] = TradeContext.STRINFO
    else:
        trcbka['STRINFO'] = ''
    #=====判断备注1是否存在====
    if TradeContext.existVariable( 'NOTE1' ):
        trcbka['NOTE1'] = TradeContext.NOTE1
    else:
        trcbka['NOTE1'] = ''
    #=====判断备注2是否存在====
    if TradeContext.existVariable( 'NOTE2' ):
        trcbka['NOTE2'] = TradeContext.NOTE2
    else:
        trcbka['NOTE2'] = ''
    #=====判断备注3是否存在====
    if TradeContext.existVariable( 'NOTE3' ):
        trcbka['NOTE3'] = TradeContext.NOTE3
    else:
        trcbka['NOTE3'] = ''
    #=====判断备注4是否存在====
    if TradeContext.existVariable( 'NOTE4' ):
        trcbka['NOTE4'] = TradeContext.NOTE4
    else:
        trcbka['NOTE4'] = ''
    return trcbka
