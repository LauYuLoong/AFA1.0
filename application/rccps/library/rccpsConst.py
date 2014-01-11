#  --*--coding: gbk --*--
##################################################################
#   农信银系统.常量模块
#=================================================================
#   程序文件:   rccpsConst.py
#   作    者:   关彬捷
#   修改时间:   2008-06-10
##################################################################

PL_BJEDTE         = '20080409'

PL_RCV_CENTER     = '1000000000' #农信银清算中心
PL_RCV_CENNAM     = '农信银清算中心'

PL_BESBNO_BCLRSB  = '3400008889' #省清算中心机构号
PL_BETELR_AUTO    = '999996'     #自动柜员

PL_BCSTAT_INIT    = '00'    #初始
PL_BCSTAT_SND     = '10'    #发送
PL_BCSTAT_ACC     = '20'    #记账
PL_BCSTAT_HCAC    = '21'    #抹账
PL_BCSTAT_MFERCV  = '30'    #MFE收妥
PL_BCSTAT_CONFPAY = '31'    #确认付款
PL_BCSTAT_MFERFE  = '40'    #拒绝
PL_BCSTAT_MFEQUE  = '41'    #排队
PL_BCSTAT_MFESTL  = '42'    #清算
PL_BCSTAT_CAC     = '50'    #撤销
PL_BCSTAT_BNKRCV  = '60'    #行内收妥
PL_BCSTAT_CONFACC = '61'    #确认入账
PL_BCSTAT_AUTO    = '70'    #自动入账
PL_BCSTAT_HANG    = '71'    #自动挂账
PL_BCSTAT_AUTOPAY = '72'    #自动扣款
PL_BCSTAT_QTR     = '80'    #退汇
PL_BCSTAT_CANC    = '81'    #冲销

#=====刘雨龙 20081129 新增自动冲正状态====
PL_BCSTAT_CANCEL  = '82'    #冲正
#=====关彬捷 20081225 新增手工结转状态====
PL_BCSTAT_TRAS    = '43'    #手工结转

#PL_BCSTAT_EMERG  = '90'    #紧急止付
PL_BCSTAT_LONG    = '91'    #长款
PL_BCSTAT_SHORT   = '92'    #短款
PL_BCSTAT_DEL     = '93'    #删除

PL_BDWFLG_SUCC    = '1'     #成功
PL_BDWFLG_FAIL    = '2'     #失败
PL_BDWFLG_WAIT    = '9'     #处理中

PL_ISDEAL_UNDO    = '0'     #未处理或未处理
PL_ISDEAL_ISDO    = '1'     #已处理或已查复

PL_BRSFLG_SND     = '0'     #往账
PL_BRSFLG_RCV     = '1'     #来账

PL_MBRTRCST_RCV   = '20'    #正常接收
PL_MBRTRCST_ACSUC = '21'    #记账成功
PL_MBRTRCST_ACFAL = '22'    #记账失败
PL_MBRTRCST_CNF   = '23'    #已确认
PL_MBRTRCST_CURE  = '24'    #已冲正
PL_MBRTRCST_RUSH  = '25'    #已冲销
PL_MBRTRCST_REPR  = '26'    #已补正
PL_MBRTRCST_UNRCV = '27'    #未收到

PL_TRCCO_HD       = '20'    #汇兑
PL_TRCCO_HP       = '21'    #汇票
PL_TRCCO_TCTD     = '30'    #通存通兑
PL_TRCCO_QT       = '99'    #其它

PL_SEAL_ENC       = 0       #加密押
PL_SEAL_DEC       = 1       #核密押

PL_TYPE_XJHP      = '1'     #现金汇票
PL_TYPE_ZZHP      = '2'     #转账汇票
PL_TYPE_DZHD      = '3'     #现金汇兑

PL_SUBFLG_SUB     = '0'     #被代理
PL_SUBFLG_AGE     = '1'     #代理

PL_DCFLG_DEB      = '1'     #借
PL_DCFLG_CRE      = '2'     #贷

PL_BILRS_INN      = '0'     #本行签发的汇票
PL_BILRS_OUT      = '1'     #他行签发的汇票

PL_HPSTAT_SIGN    = '01'    #签发
PL_HPSTAT_PAYC    = '02'    #解付
PL_HPSTAT_CANC    = '03'    #撤销
PL_HPSTAT_HANG    = '04'    #挂失
PL_HPSTAT_RETN    = '05'    #退票
PL_HPSTAT_DEHG    = '06'    #解挂
PL_HPSTAT_CLER    = '07'    #结清

PL_BILTYP_CASH    = '0'     #现金汇票
PL_BILTYP_TRAN    = '1'     #转账汇票

PL_PAYWAY_CASH    = '0'     #现金
PL_PAYWAY_TRAN    = '1'     #非现金

#主机摘要代码
PL_RCCSMCD_HPQF   = '610'   #汇票签发
PL_RCCSMCD_HPJF   = '611'   #汇票解付
PL_RCCSMCD_HPCX   = '612'   #汇票撤销
PL_RCCSMCD_HPTK   = '613'   #汇票退款
PL_RCCSMCD_WCX    = '614'   #往撤销
PL_RCCSMCD_JJZF   = '615'   #紧急止付
PL_RCCSMCD_WCH    = '616'   #往冲回
PL_RCCSMCD_LTH    = '617'   #来退汇
PL_RCCSMCD_HDWZ   = '618'   #汇兑往账
PL_RCCSMCD_HDLZ   = '619'   #汇兑来账
PL_RCCSMCD_HPLZ   = '620'   #汇票来账
#通存通兑相关
PL_RCCSMCD_SXF    = '015'   #手续费
PL_RCCSMCD_XJTCWZ = '630'   #现金通存往账
PL_RCCSMCD_XJTDWZ = '631'   #现金通兑往账
PL_RCCSMCD_XJTCLZ = '621'   #现金通存来账
PL_RCCSMCD_XJTDLZ = '622'   #现金通兑来账
PL_RCCSMCD_BZYWZ  = '623'   #行内账户转异地往账
PL_RCCSMCD_YZBWZ  = '624'   #异地账户转行内往账
PL_RCCSMCD_BZYLZ  = '626'   #行内账户转异地来账
PL_RCCSMCD_YZBLZ  = '627'   #异地账户转行内来账
PL_RCCSMCD_CX     = '625'   #冲销
PL_RCCSMCD_CZ     = 'ADJ'   #冲正
PL_RCCSMCD_DZMZ   = '628'   #对账后抹账
PL_RCCSMCD_DZBJ   = '629'   #对账后补记账


#=====刘雨龙  20080626 账号前添加币种代码：01====
PL_ACC_NXYDQSWZ   = '01065100000005'   #农信银待清算往账
PL_ACC_NXYDQSLZ   = '01065600000005'   #农信银待清算来账
PL_ACC_NXYDJLS    = '01060300000003'   #农信银待解临时款项
PL_ACC_NXYDXZ     = '01053700000007'   #农信银待销账
PL_ACC_HCHK       = '01053800000001'   #汇出汇款
#=====刘雨龙  20080911 新增2621科目====
PL_ACC_DYKJQ      = '01061200000001'   #多余款
#=====关彬捷  20081023 增加5111手续费科目
PL_ACC_TCTDSXF    = '01082000000006'   #通存通兑手续费
#=====张恒    20091109 新增0651手续费科目
PL_ACC_HDSXF      = '01082000000002'   #汇兑手续费
#=====关彬捷  20081217  新增1391其他应收款科目=====
PL_ACC_QTYSK      = '01032100000013'   #其他应收款
#=====关彬捷  20081217  新增2621其他应付款科目=====
PL_ACC_QTYFK      = '01061200000001'   #其他应付款
#=====关彬捷  20081225  新增4601农信银往账科目和4602农信银来账科目=====
PL_ACC_NXYWZ      = '01075100000005'   #农信银往账
PL_ACC_NXYLZ      = '01075600000005'   #农信银来账

#=====关彬捷  20080804 增加OPRNO代码
PL_HDOPRNO_HD     = '00'       #汇兑
PL_HDOPRNO_WT     = '01'       #委托收款(划回)
PL_HDOPRNO_TS     = '02'       #托收承付(划回)
PL_HDOPRNO_TY     = '04'       #特约汇兑
PL_HDOPRNO_TH     = '09'       #退汇
PL_HPOPRNO_QF     = '00'       #签发
PL_HPOPRNO_JF     = '01'       #解付
PL_HPOPRNO_CX     = '03'       #撤销
PL_HPOPRNO_GS     = '04'       #挂失
PL_HPOPRNO_JG     = '05'       #解挂
PL_HPOPRNO_TP     = '06'       #退票
PL_HPOPRNO_CF     = '07'       #超期付款
PL_TDOPRNO_TC     = '20'       #现金通存
PL_TDOPRNO_BZY    = '21'       #本地账户转异地
PL_TDOPRNO_TD     = '22'       #现金通兑
PL_TDOPRNO_YZB    = '23'       #异地账户转本地
PL_TDOPRNO_CZ     = '24'       #冲正
PL_TDOPRNO_CX     = '25'       #冲销
PL_TDOPRNO_BZ     = '26'       #补正

#=====关彬捷  20081030 增加系统参数类型
PL_BPATPE_STR     = '0'        #字符
PL_BPATPE_NUM     = '1'        #数字
PL_BPATPE_MON     = '2'        #金额

#=====刘雨龙  20081124 增加手续费收取方式====
PL_CHRG_CASH      = '0'        # 现金
PL_CHRG_TYPE      = '1'        #转账
PL_CHRG_NONE      = '2'        #不收费
