# -*- coding: gbk -*-
##################################################################
#   ũ����ϵͳ trcbka �ֵ䵽 trc_dict �ֵ�ӳ�亯��
#
#   ��    �ߣ�  �ر��
#   �����ļ�:   rccpsMap0000Dtrcbka2Dtrc_dict.py
#   �޸�ʱ��:   Mon Jun 23 17:33:44 2008
##################################################################
import AfaLoggerFunc,TradeContext
from types import *
def map(from_dict,to_dict):
        
    if from_dict.has_key('BJEDTE'):
        to_dict['BJEDTE'] = from_dict['BJEDTE']
        AfaLoggerFunc.tradeDebug('trc_dict[BJEDTE] = ' + str(to_dict['BJEDTE']))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['BJEDTE']������")

    if from_dict.has_key('BSPSQN'):
        to_dict['BSPSQN'] = from_dict['BSPSQN']
        AfaLoggerFunc.tradeDebug('trc_dict[BSPSQN] = ' + str(to_dict['BSPSQN']))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['BSPSQN']������")

    if from_dict.has_key('BRSFLG'):
        to_dict['BRSFLG'] = from_dict['BRSFLG']
        AfaLoggerFunc.tradeDebug('trc_dict[BRSFLG] = ' + str(to_dict['BRSFLG']))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['BRSFLG']������")

    if from_dict.has_key('BESBNO'):
        to_dict['BESBNO'] = from_dict['BESBNO']
        AfaLoggerFunc.tradeDebug('trc_dict[BESBNO] = ' + str(to_dict['BESBNO']))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['BESBNO']������")

    if from_dict.has_key('BEACSB'):
        to_dict['BEACSB'] = from_dict['BEACSB']
        AfaLoggerFunc.tradeDebug('trc_dict[BEACSB] = ' + str(to_dict['BEACSB']))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['BEACSB']������")

    if from_dict.has_key('BETELR'):
        to_dict['BETELR'] = from_dict['BETELR']
        AfaLoggerFunc.tradeDebug('trc_dict[BETELR] = ' + str(to_dict['BETELR']))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['BETELR']������")

    if from_dict.has_key('BEAUUS'):
        to_dict['BEAUUS'] = from_dict['BEAUUS']
        AfaLoggerFunc.tradeDebug('trc_dict[BEAUUS] = ' + str(to_dict['BEAUUS']))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['BEAUUS']������")

    if from_dict.has_key('TERMID'):
        to_dict['TERMID'] = from_dict['TERMID']
        AfaLoggerFunc.tradeDebug('trc_dict[TERMID] = ' + str(to_dict['TERMID']))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['TERMID']������")

    if from_dict.has_key('BBSSRC'):
        to_dict['BBSSRC'] = from_dict['BBSSRC']
        AfaLoggerFunc.tradeDebug('trc_dict[BBSSRC] = ' + str(to_dict['BBSSRC']))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['BBSSRC']������")

    if from_dict.has_key('DASQ'):
        to_dict['DASQ'] = from_dict['DASQ']
        AfaLoggerFunc.tradeDebug('trc_dict[DASQ] = ' + str(to_dict['DASQ']))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['DASQ']������")

    if from_dict.has_key('DCFLG'):
        to_dict['DCFLG'] = from_dict['DCFLG']
        AfaLoggerFunc.tradeDebug('trc_dict[DCFLG] = ' + str(to_dict['DCFLG']))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['DCFLG']������")

    if from_dict.has_key('OPRNO'):
        to_dict['OPRNO'] = from_dict['OPRNO']
        AfaLoggerFunc.tradeDebug('trc_dict[OPRNO] = ' + str(to_dict['OPRNO']))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['OPRNO']������")

    if from_dict.has_key('OPRATTNO'):
        to_dict['OPRATTNO'] = from_dict['OPRATTNO']
        AfaLoggerFunc.tradeDebug('trc_dict[OPRATTNO] = ' + str(to_dict['OPRATTNO']))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['OPRATTNO']������")

    if from_dict.has_key('NCCWKDAT'):
        to_dict['NCCWKDAT'] = from_dict['NCCWKDAT']
        AfaLoggerFunc.tradeDebug('trc_dict[NCCWKDAT] = ' + str(to_dict['NCCWKDAT']))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['NCCWKDAT']������")

    if from_dict.has_key('TRCCO'):
        to_dict['TRCCO'] = from_dict['TRCCO']
        AfaLoggerFunc.tradeDebug('trc_dict[TRCCO] = ' + str(to_dict['TRCCO']))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['TRCCO']������")

    if from_dict.has_key('TRCDAT'):
        to_dict['TRCDAT'] = from_dict['TRCDAT']
        AfaLoggerFunc.tradeDebug('trc_dict[TRCDAT] = ' + str(to_dict['TRCDAT']))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['TRCDAT']������")

    if from_dict.has_key('TRCNO'):
        to_dict['TRCNO'] = from_dict['TRCNO']
        AfaLoggerFunc.tradeDebug('trc_dict[TRCNO] = ' + str(to_dict['TRCNO']))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['TRCNO']������")

    if from_dict.has_key('SNDMBRCO'):
        to_dict['SNDMBRCO'] = from_dict['SNDMBRCO']
        AfaLoggerFunc.tradeDebug('trc_dict[SNDMBRCO] = ' + str(to_dict['SNDMBRCO']))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['SNDMBRCO']������")

    if from_dict.has_key('RCVMBRCO'):
        to_dict['RCVMBRCO'] = from_dict['RCVMBRCO']
        AfaLoggerFunc.tradeDebug('trc_dict[RCVMBRCO] = ' + str(to_dict['RCVMBRCO']))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['RCVMBRCO']������")

    if from_dict.has_key('SNDBNKCO'):
        to_dict['SNDBNKCO'] = from_dict['SNDBNKCO']
        AfaLoggerFunc.tradeDebug('trc_dict[SNDBNKCO] = ' + str(to_dict['SNDBNKCO']))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['SNDBNKCO']������")

    if from_dict.has_key('SNDBNKNM'):
        to_dict['SNDBNKNM'] = from_dict['SNDBNKNM']
        AfaLoggerFunc.tradeDebug('trc_dict[SNDBNKNM] = ' + str(to_dict['SNDBNKNM']))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['SNDBNKNM']������")

    if from_dict.has_key('RCVBNKCO'):
        to_dict['RCVBNKCO'] = from_dict['RCVBNKCO']
        AfaLoggerFunc.tradeDebug('trc_dict[RCVBNKCO] = ' + str(to_dict['RCVBNKCO']))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['RCVBNKCO']������")

    if from_dict.has_key('RCVBNKNM'):
        to_dict['RCVBNKNM'] = from_dict['RCVBNKNM']
        AfaLoggerFunc.tradeDebug('trc_dict[RCVBNKNM] = ' + str(to_dict['RCVBNKNM']))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['RCVBNKNM']������")

    if from_dict.has_key('CUR'):
        to_dict['CUR'] = from_dict['CUR']
        AfaLoggerFunc.tradeDebug('trc_dict[CUR] = ' + str(to_dict['CUR']))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['CUR']������")

    if from_dict.has_key('OCCAMT'):
        to_dict['OCCAMT'] = from_dict['OCCAMT']
        AfaLoggerFunc.tradeDebug('trc_dict[OCCAMT] = ' + str(to_dict['OCCAMT']))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['OCCAMT']������")

    if from_dict.has_key('CHRGTYP'):
        to_dict['CHRGTYP'] = from_dict['CHRGTYP']
        AfaLoggerFunc.tradeDebug('trc_dict[CHRGTYP] = ' + str(to_dict['CHRGTYP']))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['CHRGTYP']������")

    if from_dict.has_key('LOCCUSCHRG'):
        to_dict['LOCCUSCHRG'] = from_dict['LOCCUSCHRG']
        AfaLoggerFunc.tradeDebug('trc_dict[LOCCUSCHRG] = ' + str(to_dict['LOCCUSCHRG']))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['LOCCUSCHRG']������")

    if from_dict.has_key('CUSCHRG'):
        to_dict['CUSCHRG'] = from_dict['CUSCHRG']
        AfaLoggerFunc.tradeDebug('trc_dict[CUSCHRG] = ' + str(to_dict['CUSCHRG']))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['CUSCHRG']������")

    if from_dict.has_key('PYRACC'):
        to_dict['PYRACC'] = from_dict['PYRACC']
        AfaLoggerFunc.tradeDebug('trc_dict[PYRACC] = ' + str(to_dict['PYRACC']))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['PYRACC']������")

    if from_dict.has_key('PYRNAM'):
        to_dict['PYRNAM'] = from_dict['PYRNAM']
        AfaLoggerFunc.tradeDebug('trc_dict[PYRNAM] = ' + str(to_dict['PYRNAM']))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['PYRNAM']������")

    if from_dict.has_key('PYRADDR'):
        to_dict['PYRADDR'] = from_dict['PYRADDR']
        AfaLoggerFunc.tradeDebug('trc_dict[PYRADDR] = ' + str(to_dict['PYRADDR']))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['PYRADDR']������")

    if from_dict.has_key('PYEACC'):
        to_dict['PYEACC'] = from_dict['PYEACC']
        AfaLoggerFunc.tradeDebug('trc_dict[PYEACC] = ' + str(to_dict['PYEACC']))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['PYEACC']������")

    if from_dict.has_key('PYENAM'):
        to_dict['PYENAM'] = from_dict['PYENAM']
        AfaLoggerFunc.tradeDebug('trc_dict[PYENAM] = ' + str(to_dict['PYENAM']))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['PYENAM']������")

    if from_dict.has_key('PYEADDR'):
        to_dict['PYEADDR'] = from_dict['PYEADDR']
        AfaLoggerFunc.tradeDebug('trc_dict[PYEADDR] = ' + str(to_dict['PYEADDR']))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['PYEADDR']������")

    if from_dict.has_key('SEAL'):
        to_dict['SEAL'] = from_dict['SEAL']
        AfaLoggerFunc.tradeDebug('trc_dict[SEAL] = ' + str(to_dict['SEAL']))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['SEAL']������")

    if from_dict.has_key('USE'):
        to_dict['USE'] = from_dict['USE']
        AfaLoggerFunc.tradeDebug('trc_dict[USE] = ' + str(to_dict['USE']))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['USE']������")

    if from_dict.has_key('REMARK'):
        to_dict['REMARK'] = from_dict['REMARK']
        AfaLoggerFunc.tradeDebug('trc_dict[REMARK] = ' + str(to_dict['REMARK']))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['REMARK']������")

    if from_dict.has_key('BILTYP'):
        to_dict['BILTYP'] = from_dict['BILTYP']
        AfaLoggerFunc.tradeDebug('trc_dict[BILTYP] = ' + str(to_dict['BILTYP']))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['BILTYP']������")

    if from_dict.has_key('BILDAT'):
        to_dict['BILDAT'] = from_dict['BILDAT']
        AfaLoggerFunc.tradeDebug('trc_dict[BILDAT] = ' + str(to_dict['BILDAT']))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['BILDAT']������")

    if from_dict.has_key('BILNO'):
        to_dict['BILNO'] = from_dict['BILNO']
        AfaLoggerFunc.tradeDebug('trc_dict[BILNO] = ' + str(to_dict['BILNO']))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['BILNO']������")

    if from_dict.has_key('COMAMT'):
        to_dict['COMAMT'] = from_dict['COMAMT']
        AfaLoggerFunc.tradeDebug('trc_dict[COMAMT] = ' + str(to_dict['COMAMT']))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['COMAMT']������")

    if from_dict.has_key('OVPAYAMT'):
        to_dict['OVPAYAMT'] = from_dict['OVPAYAMT']
        AfaLoggerFunc.tradeDebug('trc_dict[OVPAYAMT] = ' + str(to_dict['OVPAYAMT']))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['OVPAYAMT']������")

    if from_dict.has_key('CPSAMT'):
        to_dict['CPSAMT'] = from_dict['CPSAMT']
        AfaLoggerFunc.tradeDebug('trc_dict[CPSAMT] = ' + str(to_dict['CPSAMT']))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['CPSAMT']������")

    if from_dict.has_key('RFUAMT'):
        to_dict['RFUAMT'] = from_dict['RFUAMT']
        AfaLoggerFunc.tradeDebug('trc_dict[RFUAMT] = ' + str(to_dict['RFUAMT']))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['RFUAMT']������")

    if from_dict.has_key('CERTTYPE'):
        to_dict['CERTTYPE'] = from_dict['CERTTYPE']
        AfaLoggerFunc.tradeDebug('trc_dict[CERTTYPE] = ' + str(to_dict['CERTTYPE']))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['CERTTYPE']������")

    if from_dict.has_key('CERTNO'):
        to_dict['CERTNO'] = from_dict['CERTNO']
        AfaLoggerFunc.tradeDebug('trc_dict[CERTNO] = ' + str(to_dict['CERTNO']))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['CERTNO']������")

    if from_dict.has_key('BOJEDT'):
        to_dict['BOJEDT'] = from_dict['BOJEDT']
        AfaLoggerFunc.tradeDebug('trc_dict[BOJEDT] = ' + str(to_dict['BOJEDT']))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['BOJEDT']������")

    if from_dict.has_key('BOSPSQ'):
        to_dict['BOSPSQ'] = from_dict['BOSPSQ']
        AfaLoggerFunc.tradeDebug('trc_dict[BOSPSQ] = ' + str(to_dict['BOSPSQ']))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['BOSPSQ']������")

    if from_dict.has_key('ORTRCDAT'):
        to_dict['ORTRCDAT'] = from_dict['ORTRCDAT']
        AfaLoggerFunc.tradeDebug('trc_dict[ORTRCDAT] = ' + str(to_dict['ORTRCDAT']))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['ORTRCDAT']������")

    if from_dict.has_key('ORTRCCO'):
        to_dict['ORTRCCO'] = from_dict['ORTRCCO']
        AfaLoggerFunc.tradeDebug('trc_dict[ORTRCCO] = ' + str(to_dict['ORTRCCO']))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['ORTRCCO']������")

    if from_dict.has_key('ORTRCNO'):
        to_dict['ORTRCNO'] = from_dict['ORTRCNO']
        AfaLoggerFunc.tradeDebug('trc_dict[ORTRCNO] = ' + str(to_dict['ORTRCNO']))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['ORTRCNO']������")

    if from_dict.has_key('ORSNDBNK'):
        to_dict['ORSNDBNK'] = from_dict['ORSNDBNK']
        AfaLoggerFunc.tradeDebug('trc_dict[ORSNDBNK] = ' + str(to_dict['ORSNDBNK']))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['ORSNDBNK']������")

    if from_dict.has_key('ORRCVBNK'):
        to_dict['ORRCVBNK'] = from_dict['ORRCVBNK']
        AfaLoggerFunc.tradeDebug('trc_dict[ORRCVBNK] = ' + str(to_dict['ORRCVBNK']))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['ORRCVBNK']������")

    if from_dict.has_key('STRINFO'):
        to_dict['STRINFO'] = from_dict['STRINFO']
        AfaLoggerFunc.tradeDebug('trc_dict[STRINFO] = ' + str(to_dict['STRINFO']))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['STRINFO']������")

    if from_dict.has_key('NOTE1'):
        to_dict['NOTE1'] = from_dict['NOTE1']
        AfaLoggerFunc.tradeDebug('trc_dict[NOTE1] = ' + str(to_dict['NOTE1']))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['NOTE1']������")

    if from_dict.has_key('NOTE2'):
        to_dict['NOTE2'] = from_dict['NOTE2']
        AfaLoggerFunc.tradeDebug('trc_dict[NOTE2] = ' + str(to_dict['NOTE2']))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['NOTE2']������")

    if from_dict.has_key('NOTE3'):
        to_dict['NOTE3'] = from_dict['NOTE3']
        AfaLoggerFunc.tradeDebug('trc_dict[NOTE3] = ' + str(to_dict['NOTE3']))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['NOTE3']������")

    if from_dict.has_key('NOTE4'):
        to_dict['NOTE4'] = from_dict['NOTE4']
        AfaLoggerFunc.tradeDebug('trc_dict[NOTE4] = ' + str(to_dict['NOTE4']))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['NOTE4']������")

    return True

