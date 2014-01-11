--/***************************************************************************************************
--*     描述:       安徽MAPS平台公共表DB2
--*     创建日期:   2008-01-11
--*     最后修改日期:
--/***************************************************************************************************/


connect to maps user maps using maps;


--/***************************************************************************************************
--*     表名:       数据字典主表                                                                    *
--*     描述:       枚举类型数据                                                                    *
--*     备注:                                                                                       *
--*     创建日期:   2006-11-29                                                                      *
--*     最后修改日期:                                                                               *
--*     英文表名:   afa_maindict                                                                    *
--/***************************************************************************************************/

echo create table afa_maindict;
drop table afa_maindict;
create table afa_maindict(
    item                    varchar(5) not null,
    itemename               varchar(20) not null,
    itemcname               varchar(50) not null,
    constraint afa_maindict_key primary key (item)
)in maps_data index in maps_idx;

comment on column afa_maindict.item                     is '类别';
comment on column afa_maindict.itemename                is '英文简称';
comment on column afa_maindict.itemcname                is '英文名称';



--/***************************************************************************************************
--*     表名:       数据字典子表                                                                    *
--*     描述:       枚举类型数据                                                                    *
--*     备注:                                                                                       *
--*     创建日期:   2006-11-29                                                                      *
--*     最后修改日期:                                                                               *
--*     英文表名:   afa_subdict                                                                     *
--/***************************************************************************************************/

echo create table afa_subdict;
drop table afa_subdict;
create table afa_subdict(
    item                    varchar(5) not null,
    code                    varchar(10) not null,
    codename                varchar(50) not null,
    constraint afa_subdict_key primary key (item,code)
)in maps_data index in maps_idx;

comment on column afa_subdict.item                      is '类别';
comment on column afa_subdict.code                      is '代码';
comment on column afa_subdict.codename                  is '代码名称';



--/***************************************************************************************************
--*     表名:       机构信息表                                                                      *
--*     描述:       存储银行机构的有关信息                                                          *
--*     备注:                                                                                       *
--*     创建日期:   2006-11-29                                                                      *
--*     最后修改日期:                                                                               *
--*     英文表名:   afa_branch                                                                      *
--/***************************************************************************************************/

echo create table afa_branch;
drop table afa_branch;
create table afa_branch(
    branchno                varchar(10)   not null,  
    branchcode              varchar(20),
    type                    varchar(1)   not null,
    upbranchno              varchar(10)   not null,
    branchnames             varchar(20)  not null,
    branchname              varchar(128) not null,
    note1                   varchar(30),
    note2                   varchar(30),
    note3                   varchar(30),
    constraint afa_branch_key primary key (branchno)
)in maps_data index in maps_idx;

comment on column afa_branch.branchno                   is '网点号(分行号 支行号 网点号 00000-代表总行)';
comment on column afa_branch.branchcode                 is '机构代码(人民银行统一编码)';
comment on column afa_branch.type                       is '机构类型(0-总行 1-分行 2-支行 3-网点)';
comment on column afa_branch.upbranchno                 is '管辖机构号(分行号 支行号 00000-代表总行)';
comment on column afa_branch.branchnames                is '机构名称简称';
comment on column afa_branch.branchname                 is '机构名称全称';
comment on column afa_branch.note1                      is '备注1';
comment on column afa_branch.note2                      is '备注2';
comment on column afa_branch.note3                      is '备注3';










--/***************************************************************************************************
--*     表名:       帐户特征码信息表                                                                *
--*     描述:       存储卡/账号对应的属性，如卡/账号的长度、卡/账号的bin信息等                      *
--*     备注:                                                                                       *
--*     创建日期:   2006-11-29                                                                      *
--*     最后修改日期:                                                                               *
--*     英文表名:   afa_acctinfo                                                                    *
--/***************************************************************************************************/

echo create table afa_acctinfo;
drop table afa_acctinfo;
create table afa_acctinfo(
    seqno                   smallint not null,
    acclen                  smallint not null,
    eigenstr1               varchar(30),
    startbit1               smallint,
    len1                    smallint,
    eigenstr2               varchar(30),
    startbit2               smallint,
    len2                    smallint,
    eigenstr3               varchar(30),
    startbit3               smallint,
    len3                    smallint,
    eigenstr4               varchar(30),
    startbit4               smallint,
    len4                    smallint,
    eigenstr5               varchar(30),
    startbit5               smallint,
    len5                    smallint,
    acctype                 varchar(3) not null,
    note1                   varchar(30),
    note2                   varchar(30),
    constraint afa_acctinfo_key primary key (seqno)
)in maps_data index in maps_idx;

comment on column afa_acctinfo.seqno                    is '序号';
comment on column afa_acctinfo.acclen                   is '卡/帐号长度';
comment on column afa_acctinfo.eigenstr1                is '特征码1';
comment on column afa_acctinfo.startbit1                is '特征码1起始位';
comment on column afa_acctinfo.len1                     is '特征码1长度';
comment on column afa_acctinfo.eigenstr2                is '特征码2';
comment on column afa_acctinfo.startbit2                is '特征码2起始位';
comment on column afa_acctinfo.len2                     is '特征码2长度';
comment on column afa_acctinfo.eigenstr3                is '特征码3';
comment on column afa_acctinfo.startbit3                is '特征码3起始位';
comment on column afa_acctinfo.len3                     is '特征码3长度';
comment on column afa_acctinfo.eigenstr4                is '特征码4';
comment on column afa_acctinfo.startbit4                is '特征码4起始位';
comment on column afa_acctinfo.len4                     is '特征码4长度';
comment on column afa_acctinfo.eigenstr5                is '特征码5';
comment on column afa_acctinfo.startbit5                is '特征码5起始位';
comment on column afa_acctinfo.len5                     is '特征码5长度';
comment on column afa_acctinfo.acctype                  is '卡/帐号类型';
comment on column afa_acctinfo.note1                    is '备注1';
comment on column afa_acctinfo.note2                    is '备注2';



--/***************************************************************************************************
--*     表名:       密钥管理表                                                                      *
--*     描述:       存储每个应用对应的密钥信息                                                      *
--*     备注:                                                                                       *
--*     创建日期:   2006-11-29                                                                      *
--*     最后修改日期:                                                                               *
--*     英文表名:   afa_keyadm                                                                      *
--/***************************************************************************************************/

echo create table afa_keyadm;
drop table afa_keyadm;
create table afa_keyadm(
    sysid                   varchar(6) not null,
    unitno                  varchar(8) not null,
    subunitno               varchar(8) not null,
    loginid                 varchar(18),
    oldpwd                  varchar(64),
    newpwd                  varchar(64),
    key1                    varchar(64),
    key2                    varchar(64),
    key3                    varchar(64),
    key4                    varchar(64),
    key5                    varchar(64),
    moddate                 varchar(8),
    senddate                varchar(8),
    note1                   varchar(64),
    note2                   varchar(64),
    constraint afa_keyadm_key primary key (sysid,unitno,subunitno)
)in maps_data index in maps_idx;

comment on column afa_keyadm.sysid                      is '系统标识';
comment on column afa_keyadm.unitno                     is '商户单位代码';
comment on column afa_keyadm.subunitno                  is '商户分支单位代码';
comment on column afa_keyadm.loginid                    is '登录标识';
comment on column afa_keyadm.oldpwd                     is '原用户密码';
comment on column afa_keyadm.newpwd                     is '新用户密码';
comment on column afa_keyadm.key1                       is '密钥1';
comment on column afa_keyadm.key2                       is '密钥2';
comment on column afa_keyadm.key3                       is '密钥3';
comment on column afa_keyadm.key4                       is '密钥4';
comment on column afa_keyadm.key5                       is '密钥5';
comment on column afa_keyadm.moddate                    is '修改日期';
comment on column afa_keyadm.senddate                   is '登陆日期';
comment on column afa_keyadm.note1                      is '备注1';
comment on column afa_keyadm.note2                      is '备注2';



--/***************************************************************************************************
--*     表名:       主机响应码信息表                                                                *
--*     描述:       存储中间业务平台的交易流水                                                      *
--*     备注:                                                                                       *
--*     创建日期:   2006-11-29                                                                      *
--*     最后修改日期:                                                                               *
--*     英文表名:   afa_respcode                                                                    *
--/***************************************************************************************************/

echo create table afa_respcode;
drop table afa_respcode;
create table afa_respcode(
    sysid                   varchar(6)      not null,
    unitno                  varchar(8)      not null,
    irespcode               varchar(20)     not null,
    orespcode               varchar(20)     not null,
    respmsg                 varchar(128)    not null,
    constraint afa_respcode_key primary key (sysid,unitno,irespcode,orespcode)
)in maps_data index in maps_idx;

comment on column afa_respcode.sysid                    is '系统标识';
comment on column afa_respcode.unitno                   is '商户单位代码';
comment on column afa_respcode.subunitno                is '商户分支单位代码';
comment on column afa_respcode.irespcode                is '内部响应码';
comment on column afa_respcode.orespcode                is '外部响应码';
comment on column afa_respcode.respmsg                  is '响应信息';



--/***************************************************************************************************
--*     表名:       费用管理信息表                                                                  *
--*     描述:       存储中间业务平台的交易收费信息                                                  *
--*     备注:                                                                                       *
--*     创建日期:   2006-11-29                                                                      *
--*     最后修改日期:                                                                               *
--*     英文表名:   afa_feeadm                                                                      *
--/***************************************************************************************************/

echo create table afa_feeadm;
drop table afa_feeadm;
create table afa_feeadm(
    sysid                   varchar(6)      not null,
    unitno                  varchar(8)      not null,
    subunitno               varchar(8)      not null,
    feeflag                 varchar(1)      not null,
    amount                  varchar(17)      not null,
    note1                   varchar(10),
    note2                   varchar(20),
    constraint afa_feeadm_key primary key (sysid,unitno,subunitno)
)in maps_data index in maps_idx;

comment on column afa_feeadm.sysid                      is '系统标识';
comment on column afa_feeadm.unitno                     is '商户单位代码';
comment on column afa_feeadm.subunitno                  is '商户子单位代码';
comment on column afa_feeadm.feeflag                    is '收费模式(1-逐笔 2-汇总)';
comment on column afa_feeadm.amount                     is '收费金额';
comment on column afa_feeadm.note1                      is '备注1';
comment on column afa_feeadm.note2                      is '备注2';




--/***************************************************************************************************
--*     表名:       摘要管理信息表                                                                  *
--*     描述:       存储中间业务平台的主机摘要信息                                                  *
--*     备注:                                                                                       *
--*     创建日期:   2006-11-29                                                                      *
--*     最后修改日期:                                                                               *
--*     英文表名:   afa_summary                                                                      *
--/***************************************************************************************************/

echo create table afa_summary;
drop table afa_summary;
create table afa_summary(
    sysid                   varchar(6)      not null,
    sumno                   varchar(3)      not null,
    sumname                 varchar(60),
    note1                   varchar(10),
    note2                   varchar(20),
    constraint afa_summary_key primary key (sysid)
)in maps_data index in maps_idx;

comment on column afa_summary.sysid            is '系统标识';
comment on column afa_summary.sumno            is '摘要代码';
comment on column afa_summary.sumname          is '摘要名称';
comment on column afa_summary.note1            is '备注1';
comment on column afa_summary.note2            is '备注2';


















--/***************************************************************************************************
--*     表名:       应用系统状态表                                                                  *
--*     描述:       存储每个应用系统的控制信息，主要有系统状态、类型、额度控制等                    *
--*     备注:                                                                                       *
--*     创建日期:   2006-11-29                                                                      *
--*     最后修改日期:                                                                               *
--*     英文表名:   afa_system                                                                      *
--/***************************************************************************************************/

echo create table afa_system;
drop table afa_system;
create table afa_system(
    sysid                   varchar(6)      not null,
    sysename                varchar(10),
    syscname                varchar(128)    not null,
    workdate                varchar(8),
    preworkdate             varchar(8),
    status                  varchar(1)      not null,
    type                    varchar(1)      not null,
    maxamount               varchar(17)     not null,
    totalamount             varchar(17)     not null,
    channelmode             varchar(1)      not null,
    actnomode               varchar(1)      not null,
    note1                   varchar(10),
    note2                   varchar(20),
    note3                   varchar(30),
    constraint afa_system_key primary key (sysid)
)in maps_data index in maps_idx;


comment on column afa_system.sysid                      is '系统标识';
comment on column afa_system.sysename                   is '系统简称';
comment on column afa_system.syscname                   is '系统中文名称';
comment on column afa_system.workdate                   is '业务日期';
comment on column afa_system.preworkdate                is '业务上一日日期';
comment on column afa_system.status                     is '系统状态(0-关闭 1-正常 2-暂停 3-未启用)';
comment on column afa_system.type                       is '系统类型(0-总行 1-分行 2-支行)';
comment on column afa_system.maxamount                  is '单笔交易额度';
comment on column afa_system.totalamount                is '日累计交易额度';
comment on column afa_system.channelmode                is '渠道管理模式(0-按总行控制 1-按分行控制 2-按支行控制)';
comment on column afa_system.actnomode                  is '介质管理模式(0-按总行控制 1-按分行控制 2-按支行控制)';
comment on column afa_system.note1                      is '备注1';
comment on column afa_system.note2                      is '备注2';
comment on column afa_system.note3                      is '备注3';



--/***************************************************************************************************
--*     表名:       商户单位信息表                                                                  *
--*     描述:       记录每个应用对应的有关商户的控制信息，主要有业务模式、账户模式、各类状态等      *
--*     备注:                                                                                       *
--*     创建日期:   2006-11-29                                                                      *
--*     最后修改日期:                                                                               *
--*     英文表名:   afa_unitadm                                                                     *
--/***************************************************************************************************/

echo create table afa_unitadm;
drop table afa_unitadm;
create table afa_unitadm(
    sysid                   varchar(6)      not null,
    unitno                  varchar(8)      not null,
    unitname                varchar(128)    not null,
    unitsname               varchar(20),
    status                  varchar(1)      not null,
    busimode                varchar(1)      not null,
    accmode                 varchar(1)      not null,
    bankunitno              varchar(10)      not null,
    zoneno                  varchar(10)     not null,
    brno                    varchar(10)     not null,
    workdate                varchar(8),
    preworkdate             varchar(8),
    starttime               varchar(6),
    stoptime                varchar(6),
    feeflag                 varchar(1)      not null,
    bankcode                varchar(20),
    accno1                  varchar(32),
    accno2                  varchar(32),
    accno3                  varchar(32),
    accno4                  varchar(32),
    accno5                  varchar(32),
    accno6                  varchar(32),
    name                    varchar(60),
    telphone                varchar(20),
    address                 varchar(60),
    agenteigen              varchar(16)     not null,
    loginstatus             varchar(1),
    dayendstatus            varchar(1),
    dayendtime              varchar(6),
    trxchkstatus            varchar(1),
    trxchktime              varchar(6),
    note1                   varchar(20),
    note2                   varchar(60),
    constraint afa_unitadm_key primary key (sysid,unitno)
)in maps_data index in maps_idx;

comment on column afa_unitadm.sysid                  is '系统标识';
comment on column afa_unitadm.unitno                 is '商户单位代码';
comment on column afa_unitadm.unitname               is '商户名称';
comment on column afa_unitadm.unitsname              is '商户简称';
comment on column afa_unitadm.status                 is '商户状态(0-关闭 1-启动 2-暂停 3-未启用)';
comment on column afa_unitadm.busimode               is '业务模式(0-无分支机构 1-有分支机构,业务参数按总商户控制 2-有分支机构,业务参数按商户分支单位控制)';
comment on column afa_unitadm.accmode                is '账户模式0-无分账户 1-有分账户,按总商户清算 2-有分账户,按商户分支单位清算)';
comment on column afa_unitadm.bankunitno             is '商户编码(银行给商户分配的编码)';
comment on column afa_unitadm.zoneno                 is '主办分行号';
comment on column afa_unitadm.brno                   is '主办网点号';
comment on column afa_unitadm.workdate               is '业务日期';
comment on column afa_unitadm.preworkdate            is '业务上日日期';
comment on column afa_unitadm.starttime              is '业务开始时间';
comment on column afa_unitadm.stoptime               is '业务结束时间';
comment on column afa_unitadm.feeflag                is '收取模式(0-不收费 1-收费)';
comment on column afa_unitadm.bankcode               is '银行编码(商户给银行分配的编码)';
comment on column afa_unitadm.accno1                 is '帐号1';
comment on column afa_unitadm.accno2                 is '帐号2';
comment on column afa_unitadm.accno3                 is '帐号3';
comment on column afa_unitadm.accno4                 is '帐号4';
comment on column afa_unitadm.accno5                 is '帐号5';
comment on column afa_unitadm.accno6                 is '帐号6';
comment on column afa_unitadm.name                   is '联系人';
comment on column afa_unitadm.telphone               is '联系电话';
comment on column afa_unitadm.address                is '联系地址';
comment on column afa_unitadm.agenteigen             is '业务特征码(1-签到校验标志 2-日终校验标志 3-对帐校验标志 4-响应码使用标志 5-子表使用标志 6-扩展模式 7-交易管理使用标志)';
comment on column afa_unitadm.loginstatus            is '签到状态(0-签退 1-签到)';
comment on column afa_unitadm.dayendstatus           is '日终状态(0-未做 1-已做)';
comment on column afa_unitadm.dayendtime             is '日终时间';
comment on column afa_unitadm.trxchkstatus           is '对帐状态(0-未做 1-已对主机帐 2-第三方对帐成功 3-第三方对帐失败)';
comment on column afa_unitadm.trxchktime             is '对帐时间';
comment on column afa_unitadm.note1                  is '备注1';
comment on column afa_unitadm.note2                  is '备注2';



--/***************************************************************************************************
--*     表名:       商户分支单位信息表                                                              *
--*     描述:       存储每个商户对应所有分支单位的控制信息，主要有业务模式、账户模式、各类状态等    *
--*     备注:                                                                                       *
--*     创建日期:   2006-11-29                                                                      *
--*     最后修改日期:                                                                               *
--*     英文表名:   afa_subunitadm                                                                  *
--/***************************************************************************************************/

echo create table afa_subunitadm;
drop table afa_subunitadm;
create table afa_subunitadm(
    sysid                   varchar(6)      not null,
    unitno                  varchar(8)      not null,
    subunitno               varchar(8)      not null,
    subunitname             varchar(128)    not null,
    subunitsname            varchar(20),
    status                  varchar(1)      not null,
    workdate                varchar(8),
    preworkdate             varchar(8),
    starttime               varchar(6),
    stoptime                varchar(6),
    feeflag                 varchar(1)      not null,
    bankcode                varchar(20),
    zoneno                  varchar(10)      not null,
    brno                    varchar(10)      not null,
    bankunitno              varchar(10)      not null,
    accno1                  varchar(32),
    accno2                  varchar(32),
    accno3                  varchar(32),
    accno4                  varchar(32),
    accno5                  varchar(32),
    accno6                  varchar(32),
    name                    varchar(60),
    telphone                varchar(20),
    address                 varchar(60),
    agenteigen              varchar(16),
    loginstatus             varchar(1),
    dayendstatus            varchar(1),
    dayendtime              varchar(6),
    trxchkstatus            varchar(1),
    trxchktime              varchar(6),
    note1                   varchar(20),
    note2                   varchar(60),
    constraint afa_subunitadm_key primary key (sysid,unitno,subunitno)
)in maps_data index in maps_idx;

comment on column afa_subunitadm.sysid                  is '系统标识';
comment on column afa_subunitadm.unitno                 is '商户单位代码';
comment on column afa_subunitadm.subunitno              is '商户分支单位代码';
comment on column afa_subunitadm.subunitname            is '商户名称';
comment on column afa_subunitadm.subunitsname           is '商户简称';
comment on column afa_subunitadm.status                 is '商户状态(0-关闭 1-启动 2-暂停 3-未启用)';
comment on column afa_subunitadm.workdate               is '业务日期';
comment on column afa_subunitadm.preworkdate            is '业务上日日期';
comment on column afa_subunitadm.starttime              is '业务开始时间';
comment on column afa_subunitadm.stoptime               is '业务结束时间';
comment on column afa_subunitadm.feeflag                is '收取模式(0-不收费 1-收费)';
comment on column afa_subunitadm.bankcode               is '银行编码(商户给银行分配的编码)';
comment on column afa_subunitadm.zoneno                 is '主办分行号';
comment on column afa_subunitadm.brno                   is '主办网点号';
comment on column afa_subunitadm.bankunitno             is '商户编码(银行给商户分配的编码)';
comment on column afa_subunitadm.accno1                 is '帐号1';
comment on column afa_subunitadm.accno2                 is '帐号2';
comment on column afa_subunitadm.accno3                 is '帐号3';
comment on column afa_subunitadm.accno4                 is '帐号4';
comment on column afa_subunitadm.accno5                 is '帐号5';
comment on column afa_subunitadm.accno6                 is '帐号6';
comment on column afa_subunitadm.name                   is '联系人';
comment on column afa_subunitadm.telphone               is '联系电话';
comment on column afa_subunitadm.address                is '联系地址';
comment on column afa_subunitadm.agenteigen             is '业务特征码(1-签到校验标志 2-日终校验标志 3-对帐校验标志 4-响应码使用标志 5-子表使用标志 6-扩展模式 7-交易管理使用标志)';
comment on column afa_subunitadm.loginstatus            is '签到状态(0-签退 1-签到)';
comment on column afa_subunitadm.dayendstatus           is '日终状态(0-未做 1-已做)';
comment on column afa_subunitadm.dayendtime             is '日终时间';
comment on column afa_subunitadm.trxchkstatus           is '对帐状态(0-未做 1-已对主机帐 2-第三方对帐成功 3-第三方对帐失败)';
comment on column afa_subunitadm.trxchktime             is '对帐时间';
comment on column afa_subunitadm.note1                  is '备注1';
comment on column afa_subunitadm.note2                  is '备注2';









--/***************************************************************************************************
--*     表名:       交易信息管理表                                                                  *
--*     描述:       存储每个应用系统中每个商户的交易开通情况和交易特性信息                          *
--*     备注:                                                                                       *
--*     创建日期:   2006-11-29                                                                      *
--*     最后修改日期:                                                                               *
--*     英文表名:   afa_tradeadm                                                                    *
--/***************************************************************************************************/

echo create table afa_tradeadm;
drop table afa_tradeadm;
create table afa_tradeadm(
    sysid                   varchar(6)  not null,
    unitno                  varchar(8)  not null,
    subunitno               varchar(8)  not null,
    trxcode                 varchar(6)  not null,
    trxname                 varchar(60),
    starttime               varchar(6),
    stoptime                varchar(6),
    status                  varchar(1)  not null,
    channelcode             varchar(3)  not null,
    zoneno                  varchar(10) not null,
    brno                    varchar(10) not null,
    tellerno                varchar(10) not null,
    note1                   varchar(10),
    note2                   varchar(20),
    constraint afa_tradeadm_key primary key (sysid,unitno,subunitno,trxcode,channelcode,zoneno,brno,tellerno)
)in maps_data index in maps_idx;

comment on column afa_tradeadm.sysid                    is '系统标识';
comment on column afa_tradeadm.unitno                   is '商户单位代码';
comment on column afa_tradeadm.subunitno                is '商户分支单位代码';
comment on column afa_tradeadm.trxcode                  is '交易代码';
comment on column afa_tradeadm.trxname                  is '交易名称';
comment on column afa_tradeadm.starttime                is '业务开始时间';
comment on column afa_tradeadm.stoptime                 is '业务结束时间';
comment on column afa_tradeadm.status                   is '交易状态(0-未启用 1-开启 2-关闭 3-停用)';
comment on column afa_tradeadm.channelcode              is '渠道代码';
comment on column afa_tradeadm.zoneno                   is '分行号';
comment on column afa_tradeadm.brno                     is '网点号';
comment on column afa_tradeadm.tellerno                 is '柜员号';
comment on column afa_tradeadm.note1                    is '备注1';
comment on column afa_tradeadm.note2                    is '备注2';


--/***************************************************************************************************
--*     表名:       渠道信息管理表                                                                  *
--*     描述:       存储应用系统中商户所开通的各交易渠道的属性信息(开通状态等)                      *
--*     备注:                                                                                       *
--*     创建日期:   2006-11-29                                                                      *
--*     最后修改日期:                                                                               *
--*     英文表名:   afa_channeladm                                                                  *
--/***************************************************************************************************/

echo create table afa_channeladm;
drop table afa_channeladm;
create table afa_channeladm(
    sysid                   varchar(6)  not null,
    unitno                  varchar(8)  not null,
    subunitno               varchar(8)  not null,
    agentflag               varchar(2)  not null,
    zoneno                  varchar(10) not null,
    zhno                    varchar(10) not null,
    channelcode             varchar(3)  not null,
    agentbrno               varchar(10),
    agentteller             varchar(10),
    maxamount               varchar(17) not null,
    totalamount             varchar(17) not null,
    billsavectl             varchar(1)  not null,
    autorevtranctl          varchar(1)  not null,
    errchkctl               varchar(1)  not null,
    channelstatus           varchar(1)  not null,
    autochkacct             varchar(1)  not null,
    flag1                   varchar(1),
    flag2                   varchar(1),
    flag3                   varchar(1),
    flag4                   varchar(1),
    note1                   varchar(20),
    note2                   varchar(60),
    constraint afa_channeladm_key primary key (sysid,unitno,subunitno,agentflag,zoneno,zhno,channelcode)
)in maps_data index in maps_idx;

comment on column afa_channeladm.sysid                  is '系统标识';
comment on column afa_channeladm.unitno                 is '商户单位代码';
comment on column afa_channeladm.subunitno              is '商户分支单位代码';
comment on column afa_channeladm.agentflag              is '业务方式(01-代收 02-代付 03-批扣 04-批付)';
comment on column afa_channeladm.zoneno                 is '业务分行号';
comment on column afa_channeladm.zhno                   is '业务支行号';
comment on column afa_channeladm.channelcode            is '渠道代码';
comment on column afa_channeladm.agentbrno              is '外围系统网点号';
comment on column afa_channeladm.agentteller            is '外围系统出纳员号';
comment on column afa_channeladm.maxamount              is '单笔交易额度';
comment on column afa_channeladm.totalamount            is '日累计交易额度';
comment on column afa_channeladm.billsavectl            is '发票保存标志(0-不保存 1-保存)';
comment on column afa_channeladm.autorevtranctl         is '自动冲帐标志(0-不允许 1-允许)';
comment on column afa_channeladm.errchkctl              is '异常交易检测标志(0-不需要 1-需要)';
comment on column afa_channeladm.channelstatus          is '渠道状态(0-未启用 1-开启 2-关闭 3-停用)';
comment on column afa_channeladm.autochkacct            is '自动检查帐户类型(0-不判断 1-判断)';
comment on column afa_channeladm.flag1                  is '标志1(备用)';
comment on column afa_channeladm.flag2                  is '标志2(备用)';
comment on column afa_channeladm.flag3                  is '标志3(备用)';
comment on column afa_channeladm.flag4                  is '标志4(备用)';
comment on column afa_channeladm.note1                  is '备注1';
comment on column afa_channeladm.note2                  is '备注2';




--/***************************************************************************************************
--*     表名:       缴费介质管理表                                                                  *
--*     描述:       存储应用系统中商户所开通的各交易渠道所对应的缴费介质的属性信息(开通状态等)      *
--*     备注:                                                                                       *
--*     创建日期:   2006-11-29                                                                      *
--*     最后修改日期:                                                                               *
--*     英文表名:   afa_actnoadm                                                                    *
--/***************************************************************************************************/

echo table afa_actnoadm;
drop table afa_actnoadm;
create table afa_actnoadm(
    sysid                   varchar(6)  not null,
    unitno                  varchar(8)  not null,
    subunitno               varchar(8)  not null,
    agentflag               varchar(2)  not null,
    zoneno                  varchar(10) not null,
    zhno                    varchar(10) not null,
    channelcode             varchar(3)  not null,
    acttypecode             varchar(3)  not null,
    chkaccpwdctl            varchar(1)  not null,
    enpaccpwdctl            varchar(1)  not null,
    status                  varchar(1)  not null,
    constraint afa_actnoadm_key primary key (sysid,unitno,subunitno,agentflag,zoneno,zhno,channelcode,acttypecode)
)in maps_data index in maps_idx;

comment on column afa_actnoadm.sysid                    is '系统标识';
comment on column afa_actnoadm.unitno                   is '商户单位代码';
comment on column afa_actnoadm.subunitno                is '商户分支单位代码';
comment on column afa_actnoadm.agentflag                is '业务方式(01-代收 02-代付 03-批扣 04-批付)';
comment on column afa_actnoadm.zoneno                   is '分行号';
comment on column afa_actnoadm.zhno                     is '支行号';
comment on column afa_actnoadm.channelcode              is '渠道代码';
comment on column afa_actnoadm.acttypecode              is '缴费介质代码(000-现金 001-对私帐号 002-借记卡 003-贷记卡 004-对公帐号 005-公务卡)';
comment on column afa_actnoadm.chkaccpwdctl             is '校验帐户密码标志(0-不校验,1-校验)';
comment on column afa_actnoadm.enpaccpwdctl             is '帐户密码加密标志(0-不加密,1-加密)';
comment on column afa_actnoadm.status                   is '缴费介质状态(0-未启用 1-开启 2-关闭 3-停用)';





--/***************************************************************************************************
--*     表名:       定时调度管理表                                                                  *
--*     描述:       存储中间业务平台所有需要定时调度的程序和参数                                    *
--*     备注:                                                                                       *
--*     创建日期:   2006-11-29                                                                      *
--*     最后修改日期:                                                                               *
--*     英文表名:   afa_cronadm                                                                     *
--/***************************************************************************************************/

echo table afa_cronadm;
drop table afa_cronadm;
create table afa_cronadm(
    taskid          varchar(5)      not null,
    taskname        varchar(60)     not null,
    status          varchar(1)      not null,
    year            varchar(4),
    month           varchar(2),
    day             varchar(2),
    hour            varchar(2),
    minute          varchar(2),
    wday            varchar(1),
    procname        varchar(128)    not null,
    runtime         varchar(14),
    note1           varchar(30),
    note2           varchar(60),
    constraint afa_cronadm_key primary key (taskid)
)in maps_data index in maps_idx;

comment on column afa_cronadm.taskid           is '任务ID';
comment on column afa_cronadm.taskname         is '任务名称';
comment on column afa_cronadm.status           is '状态(0-关闭 1-启动)';
comment on column afa_cronadm.year             is '年';
comment on column afa_cronadm.month            is '月';
comment on column afa_cronadm.day              is '日';
comment on column afa_cronadm.hour             is '小时';
comment on column afa_cronadm.minute           is '分钟';
comment on column afa_cronadm.wday             is '星期';
comment on column afa_cronadm.procname         is '程序名称';
comment on column afa_cronadm.procname         is '程序名称';
comment on column afa_cronadm.note1            is '备注1';
comment on column afa_cronadm.note2            is '备注2';







--/***************************************************************************************************
--*     表名:       流水主表                                                                        *
--*     描述:       存储中间业务平台的交易流水                                                      *
--*     备注:                                                                                       *
--*     创建日期:   2006-11-29                                                                      *
--*     最后修改日期:                                                                               *
--*     英文表名:   afa_maintransdtl                                                                *
--/***************************************************************************************************/

echo create table afa_maintransdtl;
drop table afa_maintransdtl;
create table afa_maintransdtl(
    agentserialno           varchar(8)  not null,
    workdate                varchar(8)  not null,
    worktime                varchar(6)  not null,
    sysid                   varchar(6)  not null,
    unitno                  varchar(8)  not null,
    subunitno               varchar(8),
    agentflag               varchar(2)  not null,
    trxcode                 varchar(10) not null,
    zoneno                  varchar(10) not null,
    brno                    varchar(10) not null,
    tellerno                varchar(10) not null,
    cashtelno               varchar(10),
    authtellerno            varchar(10),
    channelcode             varchar(3)  not null,
    channelserno            varchar(40),
    termid                  varchar(20),
    customerid              varchar(16),
    userno                  varchar(30) not null,
    subuserno               varchar(30),
    username                varchar(100),
    acctype                 varchar(3)  not null,
    draccno                 varchar(30),
    craccno                 varchar(30),
    vouhtype                varchar(10),
    vouhno                  varchar(30),
    vouhdate                varchar(8),
    currType                varchar(3),
    currFlag                varchar(3),
    amount                  varchar(17) not null,
    subamount               varchar(17),
    revtranf                varchar(1)  not null,
    preagentserno           varchar(8),
    bankstatus              varchar(1),
    bankcode                varchar(10),
    bankserno               varchar(20),
    corpstatus              varchar(1),
    corpcode                varchar(10),
    corpserno               varchar(20),
    corptime                varchar(20),
    errormsg                varchar(128),
    chkflag                 varchar(1),
    corpchkflag             varchar(1),
    appendflag              varchar(1),
    note1                   varchar(20),
    note2                   varchar(20),
    note3                   varchar(40),
    note4                   varchar(40),
    note5                   varchar(60),
    note6                   varchar(60),
    note7                   varchar(80),
    note8                   varchar(80),
    note9                   varchar(100),
    note10                  varchar(100),
    constraint afa_maindtl_key primary key (workdate,agentserialno)
)in maps_data index in maps_idx;

create index afa_maindtl_idx2 on afa_maintransdtl(workdate,sysid,agentflag,revtranf,bankstatus,corpstatus) ;

create index afa_maindtl_idx3 on afa_maintransdtl(zoneno,sysid,agentflag);

comment on column afa_maintransdtl.agentserialno        is '业务流水号';
comment on column afa_maintransdtl.workdate             is '交易日期';
comment on column afa_maintransdtl.worktime             is '交易时间';
comment on column afa_maintransdtl.sysid                is '系统标识';
comment on column afa_maintransdtl.unitno               is '商户单位代码';
comment on column afa_maintransdtl.subunitno            is '商户分支单位代码';
comment on column afa_maintransdtl.agentflag            is '业务方式(01-代收 02-代付 03-批扣 04-批付)';
comment on column afa_maintransdtl.trxcode              is '交易码';
comment on column afa_maintransdtl.zoneno               is '分行号';
comment on column afa_maintransdtl.brno                 is '行所号';
comment on column afa_maintransdtl.tellerno             is '柜员号';
comment on column afa_maintransdtl.cashtelno            is '出纳员号';
comment on column afa_maintransdtl.authtellerno         is '授权柜员号';
comment on column afa_maintransdtl.channelcode          is '渠道代码';
comment on column afa_maintransdtl.channelserno         is '渠道流水号';
comment on column afa_maintransdtl.termid               is '终端号';
comment on column afa_maintransdtl.customerid           is '客户注册号';
comment on column afa_maintransdtl.userno               is '用户号';
comment on column afa_maintransdtl.subuserno            is '附加用户号';
comment on column afa_maintransdtl.username             is '用户名称';
comment on column afa_maintransdtl.acctype              is '帐户类型';
comment on column afa_maintransdtl.draccno              is '借方帐户号码';
comment on column afa_maintransdtl.craccno              is '贷方帐户号码';
comment on column afa_maintransdtl.vouhtype             is '凭证种类';
comment on column afa_maintransdtl.vouhno               is '凭证号';
comment on column afa_maintransdtl.vouhdate             is '凭证日期';
comment on column afa_maintransdtl.currType             is '币种';
comment on column afa_maintransdtl.currFlag             is '钞汇标志';
comment on column afa_maintransdtl.amount               is '交易金额';
comment on column afa_maintransdtl.subamount            is '附加金额';
comment on column afa_maintransdtl.revtranf             is '反交易标志(0-正交易 1-反交易 2-自动冲正)';
comment on column afa_maintransdtl.preagentserno        is '银行.原平台流水号(反交易有意义)';
comment on column afa_maintransdtl.bankstatus           is '银行.交易状态(0:正常 1:失败 2:异常 3.已冲正)';
comment on column afa_maintransdtl.bankcode             is '银行.交易返回码';
comment on column afa_maintransdtl.bankserno            is '银行.交易流水号';
comment on column afa_maintransdtl.corpstatus           is '企业.交易状态(0-正常 1-失败 2-异常 3-已冲正)';
comment on column afa_maintransdtl.corpcode             is '企业.交易返回码';
comment on column afa_maintransdtl.corpserno            is '企业.交易流水号';
comment on column afa_maintransdtl.corptime             is '企业.交易时间戳';
comment on column afa_maintransdtl.errormsg             is '交易错误信息';
comment on column afa_maintransdtl.chkflag              is '主机对帐标志(0-已对帐,交易成功 1-已对帐,交易失败, 9-未对帐)';
comment on column afa_maintransdtl.corpchkflag          is '企业对帐标志(0-已对帐,交易成功 1-已对帐,交易失败, 9-未对帐)';
comment on column afa_maintransdtl.appendflag           is '从表使用标志(0-无从表信息 1-有从表信息)';
comment on column afa_maintransdtl.note1                is '备注1';
comment on column afa_maintransdtl.note2                is '备注2';
comment on column afa_maintransdtl.note3                is '备注3';
comment on column afa_maintransdtl.note4                is '备注4';
comment on column afa_maintransdtl.note5                is '备注5';
comment on column afa_maintransdtl.note6                is '备注6';
comment on column afa_maintransdtl.note7                is '备注7';
comment on column afa_maintransdtl.note8                is '备注8';
comment on column afa_maintransdtl.note9                is '备注9';
comment on column afa_maintransdtl.note10               is '备注10';




--/***************************************************************************************************
--*     表名:       流水从表                                                                        *
--*     描述:       存储中间业务平台的交易流水的附加信息                                            *
--*     备注:                                                                                       *
--*     创建日期:   2006-11-29                                                                      *
--*     最后修改日期:                                                                               *
--*     英文表名:   afa_subtransdtl                                                                 *
--/***************************************************************************************************/

echo create table afa_subtransdtl;
drop table afa_subtransdtl;
create table afa_subtransdtl(
    agentserialno           varchar(8)      not null,
    workdate                varchar(8)      not null,
    recseqno                varchar(2)      not null,
    data1                   varchar(1024)   not null,
    data2                   varchar(1024),
    constraint afa_subdtl_key primary key (workdate,agentserialno)
)in maps_data index in maps_idx;

comment on column afa_subtransdtl.agentserialno        is '业务流水号';
comment on column afa_subtransdtl.workdate             is '交易日期';
comment on column afa_subtransdtl.recseqno             is '记录序号';
comment on column afa_subtransdtl.data1                is '附加信息1';
comment on column afa_subtransdtl.data2                is '附加信息2';


--/***************************************************************************************************
--*     表名:       历史流水主表                                                                    *
--*     描述:       中间业务平台的交易流水                                                          *
--*     备注:                                                                                       *
--*     创建日期:   2006-11-29                                                                      *
--*     最后修改日期:                                                                               *
--*     英文表名:   afa_maintransdtl                                                                *
--/***************************************************************************************************/

echo create table afa_his_maintransdtl;
drop table afa_his_maintransdtl;
create table afa_his_maintransdtl(
    agentserialno           varchar(8)  not null,
    workdate                varchar(8)  not null,
    worktime                varchar(6)  not null,
    sysid                   varchar(6)  not null,
    unitno                  varchar(8)  not null,
    subunitno               varchar(8),
    agentflag               varchar(2)  not null,
    trxcode                 varchar(10) not null,
    zoneno                  varchar(10)  not null,
    brno                    varchar(10)  not null,
    tellerno                varchar(10) not null,
    cashtelno               varchar(10),
    authtellerno            varchar(10),
    channelcode             varchar(3)  not null,
    channelserno            varchar(40),
    termid                  varchar(20),
    customerid              varchar(16),
    userno                  varchar(30) not null,
    subuserno               varchar(30),
    username                varchar(100),
    acctype                 varchar(3)  not null,
    draccno                 varchar(30),
    craccno                 varchar(30),
    vouhtype                varchar(10),
    vouhno                  varchar(30),
    vouhdate                varchar(8),
    currType                varchar(3),
    currFlag                varchar(3),
    amount                  varchar(17) not null,
    subamount               varchar(17),
    revtranf                varchar(1)  not null,
    preagentserno           varchar(8),
    bankstatus              varchar(1),
    bankcode                varchar(10),
    bankserno               varchar(20),
    corpstatus              varchar(1),
    corpcode                varchar(10),
    corpserno               varchar(20),
    corptime                varchar(20),
    errormsg                varchar(128),
    chkflag                 varchar(1),
    corpchkflag             varchar(1),
    appendflag              varchar(1),
    note1                   varchar(20),
    note2                   varchar(20),
    note3                   varchar(40),
    note4                   varchar(40),
    note5                   varchar(60),
    note6                   varchar(60),
    note7                   varchar(80),
    note8                   varchar(80),
    note9                   varchar(100),
    note10                  varchar(100),
    constraint afa_hmaindtl_key primary key (workdate,agentserialno)
)in maps_data index in maps_idx;

create index afa_hmaindtl_idx2 on afa_his_maintransdtl(workdate,sysid,agentflag,revtranf,bankstatus,corpstatus);

create index afa_hmaindtl_idx3 on afa_his_maintransdtl(zoneno,sysid,agentflag);

comment on column afa_his_maintransdtl.agentserialno        is '业务流水号';
comment on column afa_his_maintransdtl.workdate             is '交易日期';
comment on column afa_his_maintransdtl.worktime             is '交易时间';
comment on column afa_his_maintransdtl.sysid                is '系统标识';
comment on column afa_his_maintransdtl.unitno               is '商户单位代码';
comment on column afa_his_maintransdtl.subunitno            is '商户分支单位代码';
comment on column afa_his_maintransdtl.agentflag            is '业务方式(01-代收 02-代付 03-批扣 04-批付)';
comment on column afa_his_maintransdtl.trxcode              is '交易码';
comment on column afa_his_maintransdtl.zoneno               is '分行号';
comment on column afa_his_maintransdtl.brno                 is '行所号';
comment on column afa_his_maintransdtl.tellerno             is '柜员号';
comment on column afa_his_maintransdtl.cashtelno            is '出纳员号';
comment on column afa_his_maintransdtl.authtellerno         is '授权柜员号';
comment on column afa_his_maintransdtl.channelcode          is '渠道代码';
comment on column afa_his_maintransdtl.channelserno         is '渠道流水号';
comment on column afa_his_maintransdtl.termid               is '终端号';
comment on column afa_his_maintransdtl.customerid           is '客户注册号';
comment on column afa_his_maintransdtl.userno               is '用户号';
comment on column afa_his_maintransdtl.subuserno            is '附加用户号';
comment on column afa_his_maintransdtl.username             is '用户名称';
comment on column afa_his_maintransdtl.acctype              is '帐户类型';
comment on column afa_his_maintransdtl.draccno              is '借方帐户号码';
comment on column afa_his_maintransdtl.craccno              is '贷方帐户号码';
comment on column afa_his_maintransdtl.vouhtype             is '凭证种类';
comment on column afa_his_maintransdtl.vouhno               is '凭证号';
comment on column afa_his_maintransdtl.vouhdate             is '凭证日期';
comment on column afa_his_maintransdtl.currType             is '币种';
comment on column afa_his_maintransdtl.currFlag             is '钞汇标志';
comment on column afa_his_maintransdtl.amount               is '交易金额';
comment on column afa_his_maintransdtl.subamount            is '附加金额';
comment on column afa_his_maintransdtl.revtranf             is '反交易标志(0-正交易 1-反交易 2-自动冲正)';
comment on column afa_his_maintransdtl.preagentserno        is '银行.原平台流水号(反交易有意义)';
comment on column afa_his_maintransdtl.bankstatus           is '银行.交易状态(0:正常 1:失败 2:异常 3.已冲正)';
comment on column afa_his_maintransdtl.bankcode             is '银行.交易返回码';
comment on column afa_his_maintransdtl.bankserno            is '银行.交易流水号';
comment on column afa_his_maintransdtl.corpstatus           is '企业.交易状态(0-正常 1-失败 2-异常 3-已冲正)';
comment on column afa_his_maintransdtl.corpcode             is '企业.交易返回码';
comment on column afa_his_maintransdtl.corpserno            is '企业.交易流水号';
comment on column afa_his_maintransdtl.corptime             is '企业.交易时间戳';
comment on column afa_his_maintransdtl.errormsg             is '交易错误信息';
comment on column afa_his_maintransdtl.chkflag              is '主机对帐标志(0-已对帐,交易成功 1-已对帐,交易失败, 9-未对帐)';
comment on column afa_his_maintransdtl.corpchkflag          is '企业对帐标志(0-已对帐,交易成功 1-已对帐,交易失败, 9-未对帐)';
comment on column afa_his_maintransdtl.appendflag           is '从表使用标志(0-无从表信息 1-有从表信息)';
comment on column afa_his_maintransdtl.note1                is '备注1';
comment on column afa_his_maintransdtl.note2                is '备注2';
comment on column afa_his_maintransdtl.note3                is '备注3';
comment on column afa_his_maintransdtl.note4                is '备注4';
comment on column afa_his_maintransdtl.note5                is '备注5';
comment on column afa_his_maintransdtl.note6                is '备注6';
comment on column afa_his_maintransdtl.note7                is '备注7';
comment on column afa_his_maintransdtl.note8                is '备注8';
comment on column afa_his_maintransdtl.note9                is '备注9';
comment on column afa_his_maintransdtl.note10               is '备注10';



--/***************************************************************************************************
--*     表名:       历史流水从表                                                                    *
--*     描述:       存储中间业务平台的历史交易流水的附加信息                                        *
--*     备注:                                                                                       *
--*     创建日期:   2006-11-29                                                                      *
--*     最后修改日期:                                                                               *
--*     英文表名:   afa_his_subtransdtl                                                             *
--/***************************************************************************************************/

echo create table afa_his_subtransdtl;
drop table afa_his_subtransdtl;
create table afa_his_subtransdtl(
    agentserialno           varchar(8)      not null,
    workdate                varchar(8)      not null,
    recseqno                varchar(2)      not null,
    data1                   varchar(1024)   not null,
    data2                   varchar(1024),
    constraint afa_hsubdtl_key primary key (workdate,agentserialno)
)in maps_data index in maps_idx;

comment on column afa_his_subtransdtl.agentserialno        is '业务流水号';
comment on column afa_his_subtransdtl.workdate             is '交易日期';
comment on column afa_his_subtransdtl.recseqno             is '记录序号';
comment on column afa_his_subtransdtl.data1                is '附加信息1';
comment on column afa_his_subtransdtl.data2                is '附加信息2';


--/***************************************************************************************************
--*     表名:       发票信息表                                                                      *
--*     描述:       存储应用系统的发票信息                                                          *
--*     备注:                                                                                       *
--*     创建日期:   2006-11-29                                                                      *
--*     最后修改日期:                                                                               *
--*     英文表名:   afa_billdtl                                                                     *
--/***************************************************************************************************/

echo create table afa_billdtl;
drop table afa_billdtl;
create table afa_billdtl (
    serialno                varchar(8) not null,
    sysid                   varchar(6) not null,
    unitno                  varchar(8) not null,
    subunitno               varchar(8) not null,
    workdate                varchar(8) not null,
    worktime                varchar(6) not null,
    userno                  varchar(40) not null,
    username                varchar(60),
    billstatus              varchar(1) not null,
    prtnum                  varchar(2) not null,
    item1                   varchar(20),
    item2                   varchar(20),
    item3                   varchar(40),
    item4                   varchar(40),
    item5                   varchar(60),
    item6                   varchar(60),
    billserno               varchar(3),
    billdata                varchar(2048)
)in maps_data index in maps_idx;

echo create index afa_billdtl_idx1;
create index afa_billdtl_idx1 on afa_billdtl(sysid,unitno,workdate,userno) ;
echo create index afa_billdtl_idx2;
create index afa_billdtl_idx2 on afa_billdtl(workdate,serialno);

comment on column afa_billdtl.serialno                  is '流水号';
comment on column afa_billdtl.sysid                     is '系统标识';
comment on column afa_billdtl.unitno                    is '商户单位代码';
comment on column afa_billdtl.subunitno                 is '商户分支单位代码';
comment on column afa_billdtl.workdate                  is '工作日期';
comment on column afa_billdtl.worktime                  is '工作时间';
comment on column afa_billdtl.userno                    is '用户号';
comment on column afa_billdtl.username                  is '用户名称';
comment on column afa_billdtl.billstatus                is '发票状态(0.正常 1.作废)';
comment on column afa_billdtl.prtnum                    is '打印次数';
comment on column afa_billdtl.item1                     is '数据项1';
comment on column afa_billdtl.item2                     is '数据项2';
comment on column afa_billdtl.item3                     is '数据项3';
comment on column afa_billdtl.item4                     is '数据项4';
comment on column afa_billdtl.item5                     is '数据项5';
comment on column afa_billdtl.item6                     is '数据项6';
comment on column afa_billdtl.billserno                 is '帐单数量';
comment on column afa_billdtl.billdata                  is '发票数据';




--/***************************************************************************************************
--*     序列名:     联机交易序列                                                                    *
--*     描述:       该序列主要用于分配联机交易流水号                                                *
--*     备注:                                                                                       *
--*     创建日期:   2006-11-29                                                                      *
--*     最后修改日期:                                                                               *
--*     英文序列名: busi_online_seq                                                                 *
--****************************************************************************************************/

echo create sequence busi_online_seq;
drop sequence busi_online_seq;
create sequence busi_online_seq
    minvalue 50000000
    maxvalue 99999999
    start with 1
    increment by 1
    cache 10
    cycle;
commit;



--/***************************************************************************************************
--*     序列名:     批量交易序列                                                                    *
--*     描述:       该序列主要用于分配联机交易流水号                                                *
--*     备注:                                                                                       *
--*     创建日期:   2006-11-29                                                                      *
--*     最后修改日期:                                                                               *
--*     英文序列名: busi_online_seq                                                                 *
--****************************************************************************************************/
echo create sequence abdt_online_seq;
drop sequence abdt_online_seq;
create sequence abdt_online_seq
    minvalue 10000000
    maxvalue 99999999
    start with 10000000
    increment by 1
    cache 10
    cycle;
commit;



--/***************************************************************************************************
--*     表名:       单位协议表                                                                      *
--*     描述:       存储批量系统委托单位信息                                                        *
--*     备注:                                                                                       *
--*     创建日期:   2006-11-29                                                                      *
--*     最后修改日期:                                                                               *
--*     英文表名:   abdt_unitinfo                                                                   *
--/***************************************************************************************************/
echo create table abdt_unitinfo;
drop table abdt_unitinfo;
create table abdt_unitinfo(
	appno               varchar(6) 			not null,
	busino              varchar(14)  		not null,
	agenttype           varchar(1) 			not null,
	agentmode           varchar(1) 			not null,
	vouhtype            varchar(2),
	vouhno              varchar(30),
	accno               varchar(30),
	subaccno            varchar(10),
	signupmode          varchar(1) 			not null,
	getusernomode       varchar(1),
	protno              varchar(30),
	appname             varchar(60)			not null,
	businame            varchar(60)			not null,
	address             varchar(60),
	tel                 varchar(20),
	username            varchar(20),
	workdate            varchar(8)			not null,
	batchno             varchar(3),
	startdate           varchar(8) 			not null,
	enddate             varchar(8) 			not null,
	starttime           varchar(6) 			not null,
	endtime             varchar(6) 			not null,
	zoneno              varchar(10) 		not null,
	brno                varchar(10) 		not null,
	tellerno            varchar(10),
	regdate             varchar(8),
	regtime             varchar(6),
	status              varchar(1) 			not null,
    chkdate             varchar(8),
    chktime             varchar(6),
    chkflag             varchar(1) 			not null,
	note1               varchar(10),
	note2               varchar(20),
	note3               varchar(30),
	note4               varchar(40),
	note5               varchar(50),
	constraint abdt_unitinfo_key primary key(appno, busino, zoneno, brno)
)in maps_data index in maps_idx;

comment on column abdt_unitinfo.appno			is '业务编号:AG + 顺序号(4)';
comment on column abdt_unitinfo.busino          is '单位编号:机构代码(10) + 顺序号(4)';
comment on column abdt_unitinfo.agenttype       is '委托方式';
comment on column abdt_unitinfo.agentmode       is '委托范围';
comment on column abdt_unitinfo.vouhtype        is '凭证类型';
comment on column abdt_unitinfo.vouhno          is '凭证号码';
comment on column abdt_unitinfo.accno           is '银行账户(对公账户)';
comment on column abdt_unitinfo.subaccno        is '子账户代码';
comment on column abdt_unitinfo.signupmode      is '签约方式(0-双方, 1-三方)';
comment on column abdt_unitinfo.getusernomode   is '单位客户编号获取方式(0-本地, 1-企业)';
comment on column abdt_unitinfo.protno          is '协议号';
comment on column abdt_unitinfo.appname         is '业务名称';
comment on column abdt_unitinfo.businame        is '单位名称';
comment on column abdt_unitinfo.address         is '联系地址';
comment on column abdt_unitinfo.tel             is '联系电话';
comment on column abdt_unitinfo.username        is '联系人员';
comment on column abdt_unitinfo.workdate        is '工作日期';
comment on column abdt_unitinfo.batchno         is '批次号';
comment on column abdt_unitinfo.startdate       is '生效日期';
comment on column abdt_unitinfo.enddate         is '失效日期';
comment on column abdt_unitinfo.starttime       is '服务开始时间';
comment on column abdt_unitinfo.endtime         is '服务终止时间';
comment on column abdt_unitinfo.zoneno          is '地区代码';
comment on column abdt_unitinfo.brno            is '机构代码';
comment on column abdt_unitinfo.tellerno        is '柜员代码';
comment on column abdt_unitinfo.regdate         is '注册日期';
comment on column abdt_unitinfo.regtime         is '注册时间';
comment on column abdt_unitinfo.status          is '状态(0-未启用, 1-开启, 2-关闭, 3-停用)';
comment on column abdt_unitinfo.chkdate         is '对账日期';
comment on column abdt_unitinfo.chktime         is '对账时间';
comment on column abdt_unitinfo.chkflag         is '对帐标志(0-未对账 1-已对账)';
comment on column abdt_unitinfo.note1           is '备注1';
comment on column abdt_unitinfo.note2           is '备注2';
comment on column abdt_unitinfo.note3           is '备注3';
comment on column abdt_unitinfo.note4           is '备注4';
comment on column abdt_unitinfo.note5           is '备注5';






--/***************************************************************************************************
--*     表名:       单位协议历史表                                                                  *
--*     描述:       存储批量系统委托单位历史信息                                                    *
--*     备注:                                                                                       *
--*     创建日期:   2006-11-29                                                                      *
--*     最后修改日期:                                                                               *
--*     英文表名:   abdt_his_unitinfo                                                               *
--/***************************************************************************************************/
echo create table abdt_his_unitinfo;
drop table abdt_his_unitinfo;
create table abdt_his_unitinfo(
	appno               varchar(6) 			not null,
	busino              varchar(14)  		not null,
	agenttype           varchar(1) 			not null,
	agentmode           varchar(1) 			not null,
	vouhtype            varchar(2),
	vouhno              varchar(30),
	accno               varchar(30),
	subaccno            varchar(10),
	signupmode          varchar(1) 			not null,
	getusernomode       varchar(1),
	protno              varchar(30),
	appname             varchar(60)			not null,
	businame            varchar(60)			not null,
	address             varchar(60),
	tel                 varchar(20),
	username            varchar(20),
	workdate            varchar(8)			not null,
	batchno             varchar(3),
	startdate           varchar(8) 			not null,
	enddate             varchar(8) 			not null,
	starttime           varchar(6) 			not null,
	endtime             varchar(6) 			not null,
	zoneno              varchar(10) 		not null,
	brno                varchar(10) 		not null,
	tellerno            varchar(10),
	regdate             varchar(8),
	regtime             varchar(6),
	status              varchar(1) 			not null,
    chkdate             varchar(8),
    chktime             varchar(6),
    chkflag             varchar(1) 			not null,
	note1               varchar(10),
	note2               varchar(20),
	note3               varchar(30),
	note4               varchar(40),
	note5               varchar(50)
)in maps_data index in maps_idx;

echo create index abdt_hunitinfo_idx1;
create index abdt_hunitinfo_idx1 on abdt_his_unitinfo(appno, busino, zoneno, brno);

comment on column abdt_his_unitinfo.appno			is '业务编号:AG + 顺序号(4)';
comment on column abdt_his_unitinfo.busino          is '单位编号:机构代码(10) + 顺序号(4)';
comment on column abdt_his_unitinfo.agenttype       is '委托方式';
comment on column abdt_his_unitinfo.agentmode       is '委托范围';
comment on column abdt_his_unitinfo.vouhtype        is '凭证类型';
comment on column abdt_his_unitinfo.vouhno          is '凭证号码';
comment on column abdt_his_unitinfo.accno           is '银行账户(对公账户)';
comment on column abdt_his_unitinfo.subaccno        is '子账户代码';
comment on column abdt_his_unitinfo.signupmode      is '签约方式(0-双方, 1-三方)';
comment on column abdt_his_unitinfo.getusernomode   is '单位客户编号获取方式(0-本地, 1-企业)';
comment on column abdt_his_unitinfo.protno          is '协议号';
comment on column abdt_his_unitinfo.appname         is '业务名称';
comment on column abdt_his_unitinfo.businame        is '单位名称';
comment on column abdt_his_unitinfo.address         is '联系地址';
comment on column abdt_his_unitinfo.tel             is '联系电话';
comment on column abdt_his_unitinfo.username        is '联系人员';
comment on column abdt_his_unitinfo.workdate        is '工作日期';
comment on column abdt_his_unitinfo.batchno         is '批次号';
comment on column abdt_his_unitinfo.startdate       is '生效日期';
comment on column abdt_his_unitinfo.enddate         is '失效日期';
comment on column abdt_his_unitinfo.starttime       is '服务开始时间';
comment on column abdt_his_unitinfo.endtime         is '服务终止时间';
comment on column abdt_his_unitinfo.zoneno          is '地区代码';
comment on column abdt_his_unitinfo.brno            is '机构代码';
comment on column abdt_his_unitinfo.tellerno        is '柜员代码';
comment on column abdt_his_unitinfo.regdate         is '注册日期';
comment on column abdt_his_unitinfo.regtime         is '注册时间';
comment on column abdt_his_unitinfo.status          is '状态(0-未启用, 1-开启, 2-关闭, 3-停用)';
comment on column abdt_his_unitinfo.chkdate         is '对账日期';
comment on column abdt_his_unitinfo.chktime         is '对账时间';
comment on column abdt_his_unitinfo.chkflag         is '对帐标志(0-未对账 1-已对账)';
comment on column abdt_his_unitinfo.note1           is '备注1';
comment on column abdt_his_unitinfo.note2           is '备注2';
comment on column abdt_his_unitinfo.note3           is '备注3';
comment on column abdt_his_unitinfo.note4           is '备注4';
comment on column abdt_his_unitinfo.note5           is '备注5';



--/***************************************************************************************************
--*     表名:       个人协议表                                                                      *
--*     描述:       存储批量系统委托个人信息                                                        *
--*     备注:                                                                                       *
--*     创建日期:   2006-11-29                                                                      *
--*     最后修改日期:                                                                               *
--*     英文表名:   abdt_custinfo                                                                   *
--/***************************************************************************************************/
echo create table abdt_custinfo;
drop table abdt_custinfo;
create table abdt_custinfo(
	appno				varchar(6)			not null,
	busino              varchar(14) 		not null,
	busiuserno          varchar(20)			not null,
	busiuserappno       varchar(20)			not null,
	bankuserno          varchar(12),
	vouhtype            varchar(2),
	vouhno              varchar(30),
	accno               varchar(30)			not null,
	subaccno            varchar(10),
	currtype            varchar(3),
	limitamt            varchar(17),
	partflag            varchar(1),
	protocolno          varchar(30)			not null   primary key,
	contractdate        varchar(8),
	startdate           varchar(8),
	enddate             varchar(8),
	passchkflag         varchar(1),
	passwd              varchar(16),
	idchkflag           varchar(1),
	idtype              varchar(2),
	idcode              varchar(20),
	namechkflag         varchar(1),
	username            varchar(60),
	tel                 varchar(20),
	address             varchar(60),
	zipcode             varchar(6),
	email               varchar(50),
	status              varchar(1) 			not null,
	zoneno              varchar(10)			not null,
	brno                varchar(10)			not null,
	tellerno            varchar(10),
	indate				varchar(8),
	intime				varchar(6),
	note1               varchar(10),
	note2               varchar(20),
	note3               varchar(30),
	note4               varchar(40),
	note5               varchar(50)
)in maps_data index in maps_idx;

echo create table abdt_custinfo_idx1;
create unique index abdt_custinfo_idx1 on abdt_custinfo(appno,busino,accno);

echo create table abdt_custinfo_idx2;
create unique index abdt_custinfo_idx2 on abdt_custinfo(appno,busino,busiuserno);

echo create table abdt_custinfo_idx3;
create unique index abdt_custinfo_idx3 on abdt_custinfo(appno,busino,bankuserno);

comment on column abdt_custinfo.appno	           is '业务编号(AG + 顺序号(4))';
comment on column abdt_custinfo.busino	           is '单位编号(机构代码(10) + 顺序号(4))';
comment on column abdt_custinfo.busiuserno	       is '单位客户编号';
comment on column abdt_custinfo.busiuserappno	   is '商户客户应用编号';
comment on column abdt_custinfo.bankuserno	       is '银行客户编号';
comment on column abdt_custinfo.vouhtype	       is '凭证类型(01-借记卡 02-活期存折)';
comment on column abdt_custinfo.vouhno	           is '凭证号(19或23位数字)';
comment on column abdt_custinfo.accno	           is '活期存款帐号(若采用一卡通或一本通模式，输入卡或折下面的活期子帐号)';
comment on column abdt_custinfo.subaccno	       is '子帐号';
comment on column abdt_custinfo.currtype	       is '币种(CNY-人民币)';
comment on column abdt_custinfo.limitamt	       is '交易限额(要求是整数 =0-不限制 >0-金额上限)';
comment on column abdt_custinfo.partflag	       is '部分扣款标志(0-足额扣款 1-部分扣款)';
comment on column abdt_custinfo.protocolno	       is '协议编号(自动生成)';
comment on column abdt_custinfo.contractdate	   is '签约日期(合同日期)';
comment on column abdt_custinfo.startdate	       is '生效日期';
comment on column abdt_custinfo.enddate	           is '失效日期';
comment on column abdt_custinfo.passchkflag	       is '密码验证标志(0-不验证 1-查询密码 2-交易密码)';
comment on column abdt_custinfo.passwd	           is '密码(备用(缴费密码))';
comment on column abdt_custinfo.idchkflag	       is '证件验证标志(0-不验证 1-身份证)';
comment on column abdt_custinfo.idtype	           is '证件类型';
comment on column abdt_custinfo.idcode	           is '证件号码(18位字符)';
comment on column abdt_custinfo.namechkflag	       is '姓名验证标志(0-不验证 1-验证)';
comment on column abdt_custinfo.username	       is '客户姓名';
comment on column abdt_custinfo.tel	               is '联系电话';
comment on column abdt_custinfo.address	           is '联系地址';
comment on column abdt_custinfo.zipcode	           is '邮编';
comment on column abdt_custinfo.email	           is '电子邮箱';
comment on column abdt_custinfo.status	           is '状态(0-注销 1-正常)';
comment on column abdt_custinfo.zoneno	           is '地区号';
comment on column abdt_custinfo.brno	           is '网点号(机构代码)';
comment on column abdt_custinfo.tellerno	       is '柜员号';
comment on column abdt_custinfo.indate	           is '录入日期';
comment on column abdt_custinfo.intime	           is '录入时间';
comment on column abdt_custinfo.note1	           is '备注1';
comment on column abdt_custinfo.note2	           is '备注2';
comment on column abdt_custinfo.note3	           is '备注3';
comment on column abdt_custinfo.note4              is '备注4';
comment on column abdt_custinfo.note5              is '备注5';


--/***************************************************************************************************
--*     表名:       个人协议历史表                                                                  *
--*     描述:       存储批量系统委托个人历史信息                                                    *
--*     备注:                                                                                       *
--*     创建日期:   2006-11-29                                                                      *
--*     最后修改日期:                                                                               *
--*     英文表名:   abdt_his_custinfo                                                               *
--/***************************************************************************************************/
echo create table abdt_his_custinfo;
drop table abdt_his_custinfo;
create table abdt_his_custinfo(
	appno				varchar(6)			not null,
	busino              varchar(14) 		not null,
	busiuserno          varchar(20)			not null,
	busiuserappno       varchar(20)			not null,
	bankuserno          varchar(12),
	vouhtype            varchar(2),
	vouhno              varchar(30),
	accno               varchar(30)			not null,
	subaccno            varchar(10),
	currtype            varchar(3),
	limitamt            varchar(17),
	partflag            varchar(1),
	protocolno          varchar(30)			not null   primary key,
	contractdate        varchar(8),
	startdate           varchar(8),
	enddate             varchar(8),
	passchkflag         varchar(1),
	passwd              varchar(16),
	idchkflag           varchar(1),
	idtype              varchar(2),
	idcode              varchar(20),
	namechkflag         varchar(1),
	username            varchar(60),
	tel                 varchar(20),
	address             varchar(60),
	zipcode             varchar(6),
	email               varchar(50),
	status              varchar(1) 			not null,
	zoneno              varchar(10)			not null,
	brno                varchar(10)			not null,
	tellerno            varchar(10),
	indate				varchar(8),
	intime				varchar(6),
	note1               varchar(10),
	note2               varchar(20),
	note3               varchar(30),
	note4               varchar(40),
	note5               varchar(50)
)in maps_data index in maps_idx;

echo create table abdt_hcustinfo_idx1;
create unique index abdt_hcustinfo_idx1 on abdt_his_custinfo(appno,busino,accno);

echo create table abdt_hcustinfo_idx2;
create unique index abdt_hcustinfo_idx2 on abdt_his_custinfo(appno,busino,busiuserno);

echo create table abdt_hcustinfo_idx3;
create unique index abdt_hcustinfo_idx3 on abdt_his_custinfo(appno,busino,bankuserno);

comment on column abdt_his_custinfo.appno	           is '业务编号(AG + 顺序号(4))';
comment on column abdt_his_custinfo.busino	           is '单位编号(机构代码(10) + 顺序号(4))';
comment on column abdt_his_custinfo.busiuserno	       is '单位客户编号';
comment on column abdt_his_custinfo.busiuserappno	   is '商户客户应用编号';
comment on column abdt_his_custinfo.bankuserno	       is '银行客户编号';
comment on column abdt_his_custinfo.vouhtype	       is '凭证类型(01-借记卡 02-活期存折)';
comment on column abdt_his_custinfo.vouhno	           is '凭证号(19或23位数字)';
comment on column abdt_his_custinfo.accno	           is '活期存款帐号(若采用一卡通或一本通模式，输入卡或折下面的活期子帐号)';
comment on column abdt_his_custinfo.subaccno	       is '子帐号';
comment on column abdt_his_custinfo.currtype	       is '币种(CNY-人民币)';
comment on column abdt_his_custinfo.limitamt	       is '交易限额(要求是整数 =0-不限制 >0-金额上限)';
comment on column abdt_his_custinfo.partflag	       is '部分扣款标志(0-足额扣款 1-部分扣款)';
comment on column abdt_his_custinfo.protocolno	       is '协议编号(自动生成)';
comment on column abdt_his_custinfo.contractdate	   is '签约日期(合同日期)';
comment on column abdt_his_custinfo.startdate	       is '生效日期';
comment on column abdt_his_custinfo.enddate	           is '失效日期';
comment on column abdt_his_custinfo.passchkflag	       is '密码验证标志(0-不验证 1-查询密码 2-交易密码)';
comment on column abdt_his_custinfo.passwd	           is '密码(备用(缴费密码))';
comment on column abdt_his_custinfo.idchkflag	       is '证件验证标志(0-不验证 1-身份证)';
comment on column abdt_his_custinfo.idtype	           is '证件类型';
comment on column abdt_his_custinfo.idcode	           is '证件号码(18位字符)';
comment on column abdt_his_custinfo.namechkflag	       is '姓名验证标志(0-不验证 1-验证)';
comment on column abdt_his_custinfo.username	       is '客户姓名';
comment on column abdt_his_custinfo.tel	               is '联系电话';
comment on column abdt_his_custinfo.address	           is '联系地址';
comment on column abdt_his_custinfo.zipcode	           is '邮编';
comment on column abdt_his_custinfo.email	           is '电子邮箱';
comment on column abdt_his_custinfo.status	           is '状态(0-注销 1-正常)';
comment on column abdt_his_custinfo.zoneno	           is '地区号';
comment on column abdt_his_custinfo.brno	           is '网点号(机构代码)';
comment on column abdt_his_custinfo.tellerno	       is '柜员号';
comment on column abdt_his_custinfo.indate	           is '录入日期';
comment on column abdt_his_custinfo.intime	           is '录入时间';
comment on column abdt_his_custinfo.note1	           is '备注1';
comment on column abdt_his_custinfo.note2	           is '备注2';
comment on column abdt_his_custinfo.note3	           is '备注3';
comment on column abdt_his_custinfo.note4              is '备注4';
comment on column abdt_his_custinfo.note5              is '备注5';


--/***************************************************************************************************
--*     表名:       批量信息表                                                                      *
--*     描述:       存储批量系统所有批次信息                                                        *
--*     备注:                                                                                       *
--*     创建日期:   2006-11-29                                                                      *
--*     最后修改日期:                                                                               *
--*     英文表名:   abdt_batchinfo                                                                  *
--/***************************************************************************************************/
echo create table abdt_batchinfo;
drop table abdt_batchinfo;
create table abdt_batchinfo(
	batchno			varchar(16)		not null primary key,
	appno           varchar(6) 		not null,
	busino          varchar(14) 	not null,
	zoneno          varchar(10)		not null,
	brno            varchar(10) 	not null,
	userno          varchar(10)   	not null,
	adminno         varchar(10),
	termtype        varchar(10),
	filename        varchar(60) 	not null,
	indate          varchar(8)   	not null,
	intime          varchar(6),
	batchdate       varchar(8),
	batchtime       varchar(6),
	totalnum        varchar(10)		not null,
	totalamt        varchar(17) 	not null,
	succnum         varchar(10) 	not null,
	succamt         varchar(17) 	not null,
	failnum         varchar(10)		not null,
	failamt         varchar(17)		not null,
	status          varchar(2)		not null,
	begindate       varchar(8)		not null,
	enddate         varchar(8)		not null,
	procmsg         varchar(128),
	note1           varchar(10),
	note2           varchar(20),
	note3           varchar(30),
	note4           varchar(40),
	note5           varchar(50)
)in maps_data index in maps_idx;


echo create table abdt_batchinfo_idx1;
create unique index abdt_batchinfo_idx1 on abdt_batchinfo(appno,busino,zoneno,brno,indate,filename);


comment on column abdt_batchinfo.batchno	                is '委托号(批次号)(唯一(日期+流水号))';
comment on column abdt_batchinfo.appno	                    is '业务编号(AG + 顺序号(4))';
comment on column abdt_batchinfo.busino	                    is '单位编号(机构代码(10) + 顺序号(4))';
comment on column abdt_batchinfo.zoneno	                    is '地区号';
comment on column abdt_batchinfo.brno	                    is '网点号(机构代码)';
comment on column abdt_batchinfo.userno	                    is '操作员';
comment on column abdt_batchinfo.adminno	                is '管理员';
comment on column abdt_batchinfo.termtype	                is '终端类型';
comment on column abdt_batchinfo.filename	                is '上传文件名(业务编号+单位编号+日期.TXT)';
comment on column abdt_batchinfo.indate	                    is '申请日期';
comment on column abdt_batchinfo.intime	                    is '申请时间';
comment on column abdt_batchinfo.batchdate	                is '提交日期';
comment on column abdt_batchinfo.batchtime	                is '提交时间';
comment on column abdt_batchinfo.totalnum	                is '总笔数';
comment on column abdt_batchinfo.totalamt	                is '总金额';
comment on column abdt_batchinfo.succnum	                is '成功笔数';
comment on column abdt_batchinfo.succamt	                is '成功金额';
comment on column abdt_batchinfo.failnum	                is '失败笔数';
comment on column abdt_batchinfo.failamt	                is '失败金额';
comment on column abdt_batchinfo.status	                    is '状态(00-上传 10-申请 11-待审批(法人行审批) 20-待提交 21-正在处理提交文件 22-已提交(正在处理…) 30-待提回 31-正在处理提回文件 32-已提回 88-处理完成(回盘文件、业务报表) 40-撤销)';
comment on column abdt_batchinfo.begindate	                is '生效日期';
comment on column abdt_batchinfo.enddate	                is '失效日期';
comment on column abdt_batchinfo.procmsg	                is '处理信息';
comment on column abdt_batchinfo.note1	                    is '备注1';
comment on column abdt_batchinfo.note2	                    is '备注2';
comment on column abdt_batchinfo.note3	                    is '备注3';
comment on column abdt_batchinfo.note4	                    is '备注4';
comment on column abdt_batchinfo.note5	                    is '备注5';





--/***************************************************************************************************
--*     表名:       批量信息历史表                                                                  *
--*     描述:       存储批量系统所有历史批次信息                                                    *
--*     备注:                                                                                       *
--*     创建日期:   2006-11-29                                                                      *
--*     最后修改日期:                                                                               *
--*     英文表名:   abdt_his_batchinfo                                                              *
--/***************************************************************************************************/
echo create table abdt_his_batchinfo;
drop table abdt_his_batchinfo;
create table abdt_his_batchinfo(
	batchno			varchar(16)		not null primary key,
	appno           varchar(6) 		not null,
	busino          varchar(14) 	not null,
	zoneno          varchar(10)		not null,
	brno            varchar(10) 	not null,
	userno          varchar(10)   	not null,
	adminno         varchar(10),
	termtype        varchar(10),
	filename        varchar(60) 	not null,
	indate          varchar(8)   	not null,
	intime          varchar(6),
	batchdate       varchar(8),
	batchtime       varchar(6),
	totalnum        varchar(10)		not null,
	totalamt        varchar(17) 	not null,
	succnum         varchar(10) 	not null,
	succamt         varchar(17) 	not null,
	failnum         varchar(10)		not null,
	failamt         varchar(17)		not null,
	status          varchar(2)		not null,
	begindate       varchar(8)		not null,
	enddate         varchar(8)		not null,
	procmsg         varchar(128),
	note1           varchar(10),
	note2           varchar(20),
	note3           varchar(30),
	note4           varchar(40),
	note5           varchar(50)
)in maps_data index in maps_idx;


echo create table abdt_hbatchinfo_idx1;
create unique index abdt_hbatchinfo_idx1 on abdt_his_batchinfo(appno,busino,zoneno,brno,indate,filename);


comment on column abdt_his_batchinfo.batchno	                is '委托号(批次号)(唯一(日期+流水号))';
comment on column abdt_his_batchinfo.appno	                    is '业务编号(AG + 顺序号(4))';
comment on column abdt_his_batchinfo.busino	                    is '单位编号(机构代码(10) + 顺序号(4))';
comment on column abdt_his_batchinfo.zoneno	                    is '地区号';
comment on column abdt_his_batchinfo.brno	                    is '网点号(机构代码)';
comment on column abdt_his_batchinfo.userno	                    is '操作员';
comment on column abdt_his_batchinfo.adminno	                is '管理员';
comment on column abdt_his_batchinfo.termtype	                is '终端类型';
comment on column abdt_his_batchinfo.filename	                is '上传文件名(业务编号+单位编号+日期.TXT)';
comment on column abdt_his_batchinfo.indate	                    is '申请日期';
comment on column abdt_his_batchinfo.intime	                    is '申请时间';
comment on column abdt_his_batchinfo.batchdate	                is '提交日期';
comment on column abdt_his_batchinfo.batchtime	                is '提交时间';
comment on column abdt_his_batchinfo.totalnum	                is '总笔数';
comment on column abdt_his_batchinfo.totalamt	                is '总金额';
comment on column abdt_his_batchinfo.succnum	                is '成功笔数';
comment on column abdt_his_batchinfo.succamt	                is '成功金额';
comment on column abdt_his_batchinfo.failnum	                is '失败笔数';
comment on column abdt_his_batchinfo.failamt	                is '失败金额';
comment on column abdt_his_batchinfo.status	                    is '状态(00-上传 10-申请 11-待审批(法人行审批) 20-待提交 21-正在处理提交文件 22-已提交(正在处理…) 30-待提回 31-正在处理提回文件 32-已提回 88-处理完成(回盘文件、业务报表) 40-撤销)';
comment on column abdt_his_batchinfo.begindate	                is '生效日期';
comment on column abdt_his_batchinfo.enddate	                is '失效日期';
comment on column abdt_his_batchinfo.procmsg	                is '处理信息';
comment on column abdt_his_batchinfo.note1	                    is '备注1';
comment on column abdt_his_batchinfo.note2	                    is '备注2';
comment on column abdt_his_batchinfo.note3	                    is '备注3';
comment on column abdt_his_batchinfo.note4	                    is '备注4';
comment on column abdt_his_batchinfo.note5	                    is '备注5';













--/***************************************************************************************************
--*     表名:       批量日志表                                                                      *
--*     描述:       存储批量系统所有操作日志                                                        *
--*     备注:                                                                                       *
--*     创建日期:   2006-11-29                                                                      *
--*     最后修改日期:                                                                               *
--*     英文表名:   abdt_loginfo                                                                    *
--/***************************************************************************************************/
echo create table abdt_loginfo;
drop table abdt_loginfo;
create table abdt_loginfo(
	zoneno          varchar(10)		not null,
	brno            varchar(10) 	not null,
	tellerno        varchar(10)   	not null,
	termid          varchar(20),
	workdate        varchar(8) 	    not null,
	worktime        varchar(8)		not null,
	batchno         varchar(16)		not null,
	tasktype        varchar(2)		not null,
	taskstatus      varchar(2)		not null,
	taskmsg         varchar(128),
	note1           varchar(10),
	note2           varchar(20)
)in maps_data index in maps_idx;


echo create table abdt_loginfo_idx1;
create index abdt_loginfo_idx1 on abdt_loginfo(workdate,zoneno,brno,tellerno);


comment on column abdt_loginfo.zoneno	                is '地区号';
comment on column abdt_loginfo.brno	                    is '网点号(机构代码)';
comment on column abdt_loginfo.tellerno	                is '操作员';
comment on column abdt_loginfo.termid	                is '终端号';
comment on column abdt_loginfo.workdate	                is '日期';
comment on column abdt_loginfo.worktime	                is '时间';
comment on column abdt_loginfo.batchno	                is '委托号(批次号)';
comment on column abdt_loginfo.tasktype	                is '动作类型(状态(00-上传 10-申请 11-待审批(法人行审批) 20-待提交 21-正在处理提交文件 22-已提交(正在处理…) 30-待提回 31-正在处理提回文件 32-已提回 88-处理完成(回盘文件、业务报表) 40-撤销))';
comment on column abdt_loginfo.taskstatus	            is '动作状态(0-成功  1-失败2-异常)';
comment on column abdt_loginfo.taskmsg	                is '动作处理结果';
comment on column abdt_loginfo.note1	                is '备注1';
comment on column abdt_loginfo.note2	                is '备注2';




--/***************************************************************************************************
--*     表名:       总行业务信息表                                                                  *
--*     描述:       存储总行业务服务器信息                                                          *
--*     备注:                                                                                       *
--*     创建日期:   2006-11-29                                                                      *
--*     最后修改日期:                                                                               *
--*     英文表名:   abdt_loginfo                                                                    *
--/***************************************************************************************************/
drop table afa_zhywinfo;
CREATE TABLE afa_zhywinfo(  	
id	               		        varchar(6) not null,	
flag					varchar(1) not null,	
brno	              		        varchar(6) not null,   	
fwqip	            		        varchar(20),	
fwqport					varchar(10),	
dburl					varchar(40) not null,	
ftpid					varchar(20),
ftppw					varchar(20),
note1					varchar(30),
note2					varchar(30),    
constraint afa_zhywinfo_key primary key (id));

comment on column afa_zhywinfo.id                  is '业务编号';
comment on column afa_zhywinfo.flag                is '主/分行';
comment on column afa_zhywinfo.brno                is '分行编号';
comment on column afa_zhywinfo.fwqip               is '服务器用户号';
comment on column afa_zhywinfo.fwqport	           is '服务器密码';
comment on column afa_zhywinfo.dburl               is '服务器URL';
comment on column afa_zhywinfo.ftpid               is 'ftp用户号';
comment on column afa_zhywinfo.ftppw               is 'ftp密码';
comment on column afa_zhywinfo.note1               is '备注1';
comment on column afa_zhywinfo.note2               is '备注2';



--/***************************************************************************************************
--*     表名:       用户信息表                                                                      *
--*     描述:       存放批量管理所有用户信息                                                        *
--*     备注:                                                                                       *
--*     创建日期:   2006-11-29                                                                      *
--*     最后修改日期:                                                                               *
--*     英文表名:   abdt_loginfo                                                                    *
--/***************************************************************************************************/
drop table abdt_userinfo;
create table abdt_userinfo(
	zoneno		varchar(10) 	not null,
	brno		varchar(10) 	not null,
	userno		varchar(10) 	not null,
	username	varchar(20),
	address		varchar(128),
	tel		    varchar(20),
	regdate		varchar(8),
	regtime		varchar(6),
	password	varchar(16) 	not null,
	dutyno		varchar(2) 		not null,
	status		varchar(1) 		not null,
	note1		varchar(10),
	note2		varchar(20),
	note3		varchar(30),
	note4		varchar(40),
	note5		varchar(50),
	constraint userinfo_key primary key(zoneno, brno, userno)
)in maps_data index in maps_idx;

comment on column abdt_userinfo.zoneno			is '地区号';
comment on column abdt_userinfo.brno			is '网点号(机构代码)';
comment on column abdt_userinfo.userno			is '操作员';
comment on column abdt_userinfo.username		is '用户名称';
comment on column abdt_userinfo.address		    is '联系地址';
comment on column abdt_userinfo.tel			    is '联系电话';
comment on column abdt_userinfo.regdate			is '注册日期';
comment on column abdt_userinfo.regtime			is '注册时间';
comment on column abdt_userinfo.password		is '密码';
comment on column abdt_userinfo.dutyno			is '岗位编码';
comment on column abdt_userinfo.status			is '状态';
comment on column abdt_userinfo.note1			is '备注1';
comment on column abdt_userinfo.note2			is '备注2';
comment on column abdt_userinfo.note3			is '备注3';
comment on column abdt_userinfo.note4		    is '备注4';
comment on column abdt_userinfo.note5			is '备注5';





--/***************************************************************************************************
--*     表名:       财政对照表                                                                      *
--*     描述:       财政对照表(财政特殊表)                                                          *
--*     备注:                                                                                       *
--*     创建日期:   2006-11-29                                                                      *
--*     最后修改日期:                                                                               *
--*     英文表名:   abdt_czdzb                                                                      *
--/***************************************************************************************************/
drop table abdt_czdzb;
create table abdt_czdzb(
	appno		varchar(10) 	not null,
	czzjdm		varchar(10) 	not null,
	zjdmmc		varchar(60) 	not null,
	note1		varchar(10),
	note2		varchar(20),
	constraint abdt_czdzb_key primary key(appno, czzjdm)
)in maps_data index in maps_idx;

comment on column abdt_czdzb.appno			is '业务编号';
comment on column abdt_czdzb.czzjdm			is '资金代码';
comment on column abdt_czdzb.zjdmmc			is '单位名称';
comment on column abdt_czdzb.note1		    is '备注1';
comment on column abdt_czdzb.note2		    is '备注2';

commit;
