# -*- coding: gbk -*-
###################################################################
#    农信银系统.往账发送交易
#==================================================================
#    程序文件：  TRCC002_8506.py
#    修改时间：  2008-6-5
#    作    者：  刘雨龙
#==================================================================
#    修改时间：
#    修改者  ：
#==================================================================
#    功    能：  汇兑往账交易提交后，进行必要性检查、记录到数据库内
#		 ，向主机发起记账，记账后发送至mfe
###################################################################
import TradeContext,AfaLoggerFunc, rccpsDBFunc, AfaFlowControl ,AfaDBFunc
import TransBillFunc, AfaFunc, rccpsHostFunc,rccpsMap8506CTradeContext2Ddict
import rccpsDBTrcc_sstlog,rccpsState,rccpsDBTrcc_trcbka,rccpsDBTrcc_spbsta,rccpsEntries
import miya,os,time
from rccpsConst import *
from types import *

def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.主机类操作(1.本地操作).往账发送[TRCC002_8506]进入***' )
    
    #====begin 蔡永贵 20110215 增加====
    #新票据号是16位，需要取后8位，版本号为02，同时要兼容老票据号8位，版本号为01
    if len(TradeContext.BILNO) == 16:
        TradeContext.TMP_BILNO = TradeContext.BILNO[-8:]
    else:
        TradeContext.TMP_BILNO = TradeContext.BILNO
    #============end============
    
    AfaLoggerFunc.tradeInfo('>>>RCVSTLBIN: '+TradeContext.RCVSTLBIN)
    AfaLoggerFunc.tradeInfo('>>>SNDSTLBIN: '+TradeContext.SNDSTLBIN)
    #=====判断是否为同一成员行内====
    if TradeContext.RCVSTLBIN == TradeContext.SNDSTLBIN:
        return AfaFlowControl.ExitThisFlow('M999','同一成员行内禁止做此业务')
     
    ##===== 张恒  增加条件,如网银支付则不校验重复次数. 将手续费标志及金额字段赋值 20091109 ========##
    if (TradeContext.existVariable( "CHSHTP" ) and len(TradeContext.CHSHTP) != 0):          #手续费收取方式
        TradeContext.CHRGTYP      =      TradeContext.CHSHTP 
    else:
        TradeContext.CHRGTYP      =      '2'                                                #默认为不收
    if (TradeContext.existVariable( "CUSCHRG" ) and len(TradeContext.CUSCHRG) != 0):        #手续费金额
        TradeContext.LOCCUSCHRG   =      TradeContext.CUSCHRG  
    else :
        TradeContext.LOCCUSCHRG   =      '0.00'                                             #默认为0.00
    TradeContext.CUSCHRG          =      '0.00'                                             #异地手续费清0
    
    if str(TradeContext.OPRATTNO) != '12':                                                  #网银支付
    ##=====END=====================================================================================##
    
        #=====检查数据库是否有相同交易====
        sql = "BJEDTE = '" + TradeContext.BJEDTE + "'"                                      #日期
        sql = sql + " and BESBNO ='" + TradeContext.BESBNO + "'"                            #机构号
        if (TradeContext.existVariable( "PYRACC" ) and len(TradeContext.PYRACC) != 0):      #付款人账号
            sql = sql + " and PYRACC ='" + TradeContext.PYRACC + "'"
        if (TradeContext.existVariable( "RCVBNKCO" ) and len(TradeContext.RCVBNKCO) != 0):  #收款行行号
            sql = sql + " and RCVBNKCO = '" + TradeContext.RCVBNKCO + "'"
        if (TradeContext.existVariable( "PYEACC" ) and len(TradeContext.PYEACC) != 0):      #收款人账号
            sql = sql + " and PYEACC ='" + TradeContext.PYEACC + "'"
        if (TradeContext.existVariable( "OCCAMT" ) and len(TradeContext.OCCAMT) != 0):      #金额
            sql = sql + " and OCCAMT ="  + TradeContext.OCCAMT + ""
        if (TradeContext.existVariable( "OPRNO" ) and len(TradeContext.OPRNO) != 0):        #业务种类
            sql = sql + " and OPRNO  ='" + TradeContext.OPRNO  + "'"
        if (TradeContext.existVariable( "OPRATTNO" ) and len(TradeContext.OPRATTNO) != 0):  #业务属性
            sql = sql + " and OPRATTNO ='" + TradeContext.OPRATTNO + "'"
        if (TradeContext.existVariable( "BBSSRC" ) and len(TradeContext.BBSSRC) != 0):      #资金来源
            sql = sql + " and BBSSRC ='" + TradeContext.BBSSRC + "'"
        if (TradeContext.existVariable( "DASQ" ) and len(TradeContext.DASQ) != 0):          #销账序号
            sql = sql + " and DASQ   ='" + TradeContext.DASQ + "'"
        if (TradeContext.existVariable( "BILTYP" ) and len(TradeContext.BILTYP) != 0):      #票据种类
            sql = sql + " and BILTYP = '" + TradeContext.BILTYP  + "'"
        if (TradeContext.existVariable( "BILDAT" ) and len(TradeContext.BILDAT) != 0):      #票据日期
            sql = sql + " and BILDAT = '" + TradeContext.BILDAT  + "'"
        if (TradeContext.existVariable( "BILNO" ) and len(TradeContext.BILNO) != 0):        #票据号码
            sql = sql + " and BILNO  = '" + TradeContext.BILNO   + "'"
        if (TradeContext.existVariable( "NOTE1" ) and len(TradeContext.NOTE1) != 0):        #备注1
            sql = sql + " and NOTE1  = '" + TradeContext.NOTE1   + "'"

        #=====调用函数进行多笔查询====
        AfaLoggerFunc.tradeInfo( '>>>判断必要的字段是否重复，重复返回错误')
        record = rccpsDBTrcc_trcbka.selectm(1,10,sql,"")
        if record == None:
            return AfaFlowControl.ExitThisFlow('D000','数据库操作失败')
        if len(record) > 0:
            #====判断必要的字段是否重复，重复返回错误====
            for next in range(0, len(record)):
                spbsta = {'BJEDTE':TradeContext.BJEDTE,'BSPSQN':record[next]['BSPSQN']}
                rep = rccpsDBTrcc_spbsta.selectu(spbsta)
                if rep == None:
                    return AfaFlowControl.ExitThisFlow('D000', '数据库操作错误')
                elif len(rep) <= 0:
                    return AfaFlowControl.ExitThisFlow('D001', '数据库查询相同业务错误')
                else:
                    if rep['BDWFLG'] != PL_BDWFLG_FAIL:
                        return AfaFlowControl.ExitThisFlow('S000', '相同业务已录入，不允许重复提交')
    AfaLoggerFunc.tradeInfo( '>>>开始处理此笔业务' )
    #=====资金来源为1-个人结算户时，需要调用8811校验支付条件====
    if TradeContext.BBSSRC == '1':
        TradeContext.HostCode = '8811'
        TradeContext.ACCNO    = TradeContext.PYRACC     #付款人账户

        rccpsHostFunc.CommHost( '8811' )
       
        if TradeContext.errorCode != '0000':
            return AfaFlowControl.ExitThisFlow('S999','查询凭证信息出错')
        else:
            if TradeContext.PAYTYP != TradeContext.HPAYTYP:
                return AfaFlowControl.ExitThisFlow('S999','支付条件错误')

    #=====开始调用密押服务器====
    SEAL = '          '
    SNDBANKCO  = TradeContext.SNDBNKCO
    RCVBANKCO  = TradeContext.RCVBNKCO
    SNDBANKCO = SNDBANKCO.rjust(12,'0')
    RCVBANKCO = RCVBANKCO.rjust(12,'0')
    AMOUNT = TradeContext.OCCAMT.split('.')[0] + TradeContext.OCCAMT.split('.')[1]
    AMOUNT = AMOUNT.rjust(15,'0')
    
    AfaLoggerFunc.tradeDebug('AMOUNT=' + str(AMOUNT) )
    AfaLoggerFunc.tradeDebug('SNDBANKCO=' + str(SNDBANKCO) )
    AfaLoggerFunc.tradeDebug('RCVBANKCO=' + str(RCVBANKCO) )
    AfaLoggerFunc.tradeDebug('类型：' + str(PL_SEAL_ENC) )
    AfaLoggerFunc.tradeDebug('业务类型：' + str(PL_TYPE_DZHD) )
    AfaLoggerFunc.tradeDebug('日期' + TradeContext.TRCDAT )
    AfaLoggerFunc.tradeDebug('流水' + TradeContext.SerialNo )
    AfaLoggerFunc.tradeDebug('密押o[' + SEAL + ']')
    
    ret = miya.DraftEncrypt(PL_SEAL_ENC,PL_TYPE_DZHD,TradeContext.TRCDAT,TradeContext.SerialNo,AMOUNT,SNDBANKCO,RCVBANKCO,'',SEAL)
    AfaLoggerFunc.tradeDebug("ret[" + str(ret) + "]")
    AfaLoggerFunc.tradeDebug('密押[' + SEAL + ']')
    if ret != 0:
        return AfaFlowControl.ExitThisFlow('M9999','调用密押服务器失败')
    else:
        TradeContext.SEAL = SEAL
        AfaLoggerFunc.tradeDebug('密押new[' + TradeContext.SEAL + ']')   

    #=====开始向字典赋值====
    TradeContext.DCFLG = PL_DCFLG_CRE
    dict = {}
    if not rccpsMap8506CTradeContext2Ddict.map(dict):
        return AfaFlowControl.ExitThisFlow('M999', '字典赋值出错')

    #=====开始插入数据库====
    if not rccpsDBFunc.insTransTrc(dict):
        #=====RollBack操作====
        AfaDBFunc.RollbackSql()
        return AfaFlowControl.ExitThisFlow('D002', '插入数据库出错,RollBack成功')

    #=====commit操作====
    if not AfaDBFunc.CommitSql():
        #=====RollBack操作====
        AfaDBFunc.RollbackSql()
        return AfaFlowControl.ExitThisFlow('D011', '数据库Commit失败')
    else:
        AfaLoggerFunc.tradeDebug('COMMIT成功')

    #====送往主机字段增加收款人名称字段  ===
    if (TradeContext.existVariable( "PYRNAM" ) and len(TradeContext.PYRNAM) != 0):       #付款人名称
         TradeContext.ACNM     = TradeContext.PYRNAM
    else:
         TradeContext.ACNM     = ''
    if (TradeContext.existVariable( "PYENAM" ) and len(TradeContext.PYENAM) != 0):       #收款人名称
        TradeContext.OTNM      = TradeContext.PYENAM
    else:
        TradeContext.OTNM      = ''
        
    #汇兑往帐记帐字典赋值
    input_dict = {}
    input_dict['CHRGTYP']     = TradeContext.CHRGTYP                        #手续费收取方式
    input_dict['LOCCUSCHRG']  = TradeContext.LOCCUSCHRG                     #手续费金额
    input_dict['PYRACC']      = TradeContext.PYRACC                         #付款人账号
    input_dict['BBSSRC']      = TradeContext.BBSSRC                         #资金来源
    input_dict['OCCAMT']      = TradeContext.OCCAMT                         #交易金额
    input_dict['ACNM']        = TradeContext.ACNM                           #付款人名称
    input_dict['OTNM']        = TradeContext.OTNM                           #收款人名称
    input_dict['BESBNO']      = TradeContext.BESBNO
    #调用汇兑记账接口
    rccpsEntries.HDWZJZ(input_dict)

    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.主机类操作(1.本地操作).往账发送[TRCC002_8506]退出***' )
    return True
def SubModuleDoSnd():
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.主机类操作(2.主机记账).往账发送[TRCC002_8506]进入***' )
    AfaLoggerFunc.tradeInfo( '>>>开始更新主机返回结果信息' )
    
    #=====从主机返回信息取借贷方账号和主机返回信息====
    sstlog = {}
    sstlog["BJEDTE"] = TradeContext.BJEDTE      #交易日期
    sstlog["BSPSQN"] = TradeContext.BSPSQN      #报单序号
    sstlog["SBAC"] = TradeContext.SBAC          #借方账号
    sstlog["ACNM"] = TradeContext.PYRNAM        #借方户名
    sstlog["RBAC"] = TradeContext.RBAC          #贷方账号
    sstlog["OTNM"] = '0651科目'                 #贷方户名

    #=====判断主机返回结果====
    if TradeContext.errorCode != '0000':
        sstlog['BCSTAT'] = PL_BCSTAT_ACC
        sstlog['BDWFLG'] = PL_BDWFLG_FAIL
        sstlog["MGID"] = TradeContext.errorCode     #主机返回码
        sstlog["STRINFO"] = TradeContext.errorMsg   #主机返回信息
    elif TradeContext.errorCode == '0000':
        sstlog['BCSTAT'] = PL_BCSTAT_ACC
        sstlog['BDWFLG'] = PL_BDWFLG_SUCC
        sstlog["TRDT"] = TradeContext.TRDT    #主机日期
        sstlog["TLSQ"] = TradeContext.TLSQ    #主机流水号
        sstlog["MGID"] = TradeContext.MGID    #主机返回信息
        sstlog["DASQ"] = TradeContext.DASQ    #销账序号
    #测试用
    AfaLoggerFunc.tradeInfo( 'TradeContext.__status__ ='+TradeContext.__status__)
    
    if TradeContext.__status__=='2':            #异常情况
        #====需要触发主机抹账交易===
        #汇兑往帐抹帐字典赋值
        input_dict = {}
        input_dict['BJEDTE']     = TradeContext.BJEDTE
        input_dict['BSPSQN']     = TradeContext.BSPSQN
        input_dict['PYRACC']     = TradeContext.PYRACC                         #付款人账号
        input_dict['OCCAMT']     = str(TradeContext.OCCAMT)
        input_dict['BBSSRC']     = TradeContext.BBSSRC
        input_dict['BESBNO']     = TradeContext.BESBNO

        #调用汇兑往帐抹帐
        rccpsEntries.HDWZMZ(input_dict) 

        #=====调用主机函数进行抹账
        rccpsHostFunc.CommHost( TradeContext.HostCode )
 
        #=====判断主机返回值====
        if TradeContext.errorCode == '0000':
            sstlog['BCSTAT'] = PL_BCSTAT_ACC
            sstlog['BDWFLG'] = PL_BDWFLG_FAIL
            TradeContext.errorCode = 'D011'         #赋值返回错误
            TradeContext.errorMsg  = '记账失败，系统自动冲正成功'
        else:
            sstlog['BCSTAT'] = PL_BCSTAT_ACC
            sstlog['BDWFLG'] = PL_BDWFLG_WAIT
            TradeContext.errorCode = 'D011'         #赋值返回错误
            TradeContext.errorMsg  = '记账失败，系统自动冲正失败'

    #=====修改sstlog表中数据====
    AfaLoggerFunc.tradeInfo( '字典：' + str(sstlog) )

    if not rccpsState.setTransState(sstlog):
        return AfaFlowControl.ExitThisFlow(TradeContext.errorCode, TradeContext.errorMsg)
    else:
        #=====commit操作====
        AfaDBFunc.CommitSql()
        AfaLoggerFunc.tradeInfo('>>>commit成功')

    #=====判断主机返回，不成功返回错误到前台====
    if TradeContext.errorCode != '0000':
        return AfaFlowControl.ExitThisFlow(TradeContext.errorCode, TradeContext.errorMsg)

    #=====赋值农信银中心需要字段====
    TradeContext.TRANTYP   = '0'   #传输类型
    TradeContext.OPRTYPNO  = '20'  #业务属性
    #TradeContext.BJEDTE    = TradeContext.NCCworkDate
    #TradeContext.TRCDAT    = TradeContext.NCCworkDate

    #=====设置sstlog表中状态为：抹账-处理中====
    TradeContext.BCSTAT  = PL_BCSTAT_SND
    TradeContext.BDWFLG  = PL_BDWFLG_WAIT

    if not rccpsState.newTransState(TradeContext.BJEDTE,TradeContext.BSPSQN,TradeContext.BCSTAT,TradeContext.BDWFLG):
        #=====RollBack操作====
        if not AfaDBFunc.RollbackSql():
            return AfaFlowControl.ExitThisFlow('M999', '发送农信银中心失败,设置状态失败,系统自动回滚')
    else:
        #=====commit操作====
        if not AfaDBFunc.CommitSql():
            AfaDBFunc.RollbackSql()
            return AfaFlowControl.ExitThisFlow('M999', '发送农信银中心失败,设置状态失败,系统自动回滚')

    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.主机类操作(2.主机记账).往账发送[TRCC002_8506]退出***' )
    return True
def SubModuleDoTrd():
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.主机类操作(3.中心记账).往账发送[TRCC002_8506]进入***' )
    AfaLoggerFunc.tradeInfo( '>>>判断发送农信银中心返回结果' )

    #=====设置记账函数接口====
    sstlog_dict = {}
    sstlog_dict["BJEDTE"] = TradeContext.BJEDTE   #交易日期
    sstlog_dict["BSPSQN"] = TradeContext.BSPSQN     #报单序号

    #=====判断第三方返回值,返回成功时====
    if TradeContext.errorCode == '0000':
        sstlog_dict['BCSTAT'] = PL_BCSTAT_SND
        sstlog_dict['BDWFLG'] = PL_BDWFLG_SUCC

        #=====设置状态为发送成功====
        if not rccpsState.setTransState(sstlog_dict):
            #=====RollBack操作====
            AfaDBFunc.RollbackSql()
            return AfaFlowControl.ExitThisFlow(TradeContext.errorCode, TradeContext.errorMsg)
        else:
            #=====commit操作====
            AfaDBFunc.CommitSql()
            TradeContext.errorCode = '0000'
            TradeContext.errorMsg  = '发送农信银中心成功'
    #=====判断第三方返回值,返回失败时====
    else:
        sstlog_dict['BCSTAT'] = PL_BCSTAT_SND
        sstlog_dict['BDWFLG'] = PL_BDWFLG_FAIL
        #=====设置状态为发送失败====
        if not rccpsState.setTransState(sstlog_dict):
            #=====RollBack操作====
            AfaDBFunc.RollbackSql()
            return AfaFlowControl.ExitThisFlow(TradeContext.errorCode, TradeContext.errorMsg)
        else:
            #=====commit操作====
            AfaDBFunc.CommitSql()
            AfaLoggerFunc.tradeDebug( '>>>commit send succ' )

        #=====调用主机函数进行抹账====
        AfaLoggerFunc.tradeInfo('>>>开始抹账处理')

        #=====设置sstlog表中状态为：抹账-处理中====
        TradeContext.BOSPSQ  = TradeContext.BSPSQN
        TradeContext.BOJEDT  = TradeContext.BJEDTE
        TradeContext.BCSTAT  = PL_BCSTAT_HCAC
        TradeContext.BDWFLG  = PL_BDWFLG_WAIT

        if not rccpsState.newTransState(TradeContext.BJEDTE,TradeContext.BSPSQN,TradeContext.BCSTAT,TradeContext.BDWFLG):
            #=====RollBack操作====
            if not AfaDBFunc.RollbackSql():
                return AfaFlowControl.ExitThisFlow('M999', '发送农信银中心失败,设置状态失败,系统自动回滚')
        else:
            #=====commit操作====
            if not AfaDBFunc.CommitSql():
                AfaDBFunc.RollbackSql()
                return AfaFlowControl.ExitThisFlow('M999', '发送农信银中心失败,设置状态失败,系统自动回滚')

        #=====字典赋值==== 
        sstlog_new = {}
        sstlog_new["BJEDTE"] = TradeContext.BJEDTE                                   #交易日期
        sstlog_new["BSPSQN"] = TradeContext.BSPSQN                                   #报单序号
        
        #汇兑往帐抹帐字典赋值
        input_dict = {}
        input_dict['BJEDTE']     = TradeContext.BJEDTE
        input_dict['BSPSQN']     = TradeContext.BSPSQN
        input_dict['PYRACC']     = TradeContext.PYRACC                         #付款人账号
        input_dict['OCCAMT']     = str(TradeContext.OCCAMT)
        input_dict['BBSSRC']     = TradeContext.BBSSRC
        input_dict['BESBNO']     = TradeContext.BESBNO

        #调用汇兑往帐抹帐
        rccpsEntries.HDWZMZ(input_dict) 

        #=====设置记账函数接口====
        rccpsHostFunc.CommHost( TradeContext.HostCode )
            
        if TradeContext.errorCode == '0000':
            sstlog_new['DASQ']   = TradeContext.DASQ
            sstlog_new['PRTCNT'] = 1                     #打印次数
            sstlog_new['BCSTAT'] = PL_BCSTAT_HCAC
            sstlog_new['BDWFLG'] = PL_BDWFLG_SUCC
            sstlog_new['SBAC']   = TradeContext.SBAC
            sstlog_new['RBAC']   = TradeContext.RBAC      
            sstlog_new["MGID"]   = TradeContext.errorCode       #主机返回码
            sstlog_new["STRINFO"]= TradeContext.errorMsg        #主机返回信息
            sstlog_new["TRDT"]   = TradeContext.TRDT            #主机日期
            sstlog_new["TLSQ"]   = TradeContext.TLSQ            #主机流水号
            
            TradeContext.errorCode = 'D011'             #赋值返回错误
            TradeContext.errorMsg  = '发送农信银中心失败，系统自动冲正成功'
        else:
            sstlog_new['BCSTAT'] = PL_BCSTAT_HCAC
            sstlog_new['BDWFLG'] = PL_BDWFLG_FAIL
            TradeContext.errorCode = 'D011'             #赋值返回错误
            TradeContext.errorMsg  = '发送农信银中心失败，系统自动冲正失败'

        #=====修改sstlog表中记录状态为：抹账-成功/失败====
        if not rccpsState.setTransState(sstlog_new):
            return AfaFlowControl.ExitThisFlow(TradeContext.errorCode, TradeContext.errorMsg)
        else:
            #=====commit操作====
            AfaDBFunc.CommitSql()
    
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.主机类操作(3.中心记账).往账发送[TRCC002_8506]退出***' )
    return True
