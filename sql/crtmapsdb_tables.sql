--/***************************************************************************************************
--*     ����:       ����MAPSƽ̨������DB2
--*     ��������:   2008-01-11
--*     ����޸�����:
--/***************************************************************************************************/


connect to maps user maps using maps;


--/***************************************************************************************************
--*     ����:       �����ֵ�����                                                                    *
--*     ����:       ö����������                                                                    *
--*     ��ע:                                                                                       *
--*     ��������:   2006-11-29                                                                      *
--*     ����޸�����:                                                                               *
--*     Ӣ�ı���:   afa_maindict                                                                    *
--/***************************************************************************************************/

echo create table afa_maindict;
drop table afa_maindict;
create table afa_maindict(
    item                    varchar(5) not null,
    itemename               varchar(20) not null,
    itemcname               varchar(50) not null,
    constraint afa_maindict_key primary key (item)
)in maps_data index in maps_idx;

comment on column afa_maindict.item                     is '���';
comment on column afa_maindict.itemename                is 'Ӣ�ļ��';
comment on column afa_maindict.itemcname                is 'Ӣ������';



--/***************************************************************************************************
--*     ����:       �����ֵ��ӱ�                                                                    *
--*     ����:       ö����������                                                                    *
--*     ��ע:                                                                                       *
--*     ��������:   2006-11-29                                                                      *
--*     ����޸�����:                                                                               *
--*     Ӣ�ı���:   afa_subdict                                                                     *
--/***************************************************************************************************/

echo create table afa_subdict;
drop table afa_subdict;
create table afa_subdict(
    item                    varchar(5) not null,
    code                    varchar(10) not null,
    codename                varchar(50) not null,
    constraint afa_subdict_key primary key (item,code)
)in maps_data index in maps_idx;

comment on column afa_subdict.item                      is '���';
comment on column afa_subdict.code                      is '����';
comment on column afa_subdict.codename                  is '��������';



--/***************************************************************************************************
--*     ����:       ������Ϣ��                                                                      *
--*     ����:       �洢���л������й���Ϣ                                                          *
--*     ��ע:                                                                                       *
--*     ��������:   2006-11-29                                                                      *
--*     ����޸�����:                                                                               *
--*     Ӣ�ı���:   afa_branch                                                                      *
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

comment on column afa_branch.branchno                   is '�����(���к� ֧�к� ����� 00000-��������)';
comment on column afa_branch.branchcode                 is '��������(��������ͳһ����)';
comment on column afa_branch.type                       is '��������(0-���� 1-���� 2-֧�� 3-����)';
comment on column afa_branch.upbranchno                 is '��Ͻ������(���к� ֧�к� 00000-��������)';
comment on column afa_branch.branchnames                is '�������Ƽ��';
comment on column afa_branch.branchname                 is '��������ȫ��';
comment on column afa_branch.note1                      is '��ע1';
comment on column afa_branch.note2                      is '��ע2';
comment on column afa_branch.note3                      is '��ע3';










--/***************************************************************************************************
--*     ����:       �ʻ���������Ϣ��                                                                *
--*     ����:       �洢��/�˺Ŷ�Ӧ�����ԣ��翨/�˺ŵĳ��ȡ���/�˺ŵ�bin��Ϣ��                      *
--*     ��ע:                                                                                       *
--*     ��������:   2006-11-29                                                                      *
--*     ����޸�����:                                                                               *
--*     Ӣ�ı���:   afa_acctinfo                                                                    *
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

comment on column afa_acctinfo.seqno                    is '���';
comment on column afa_acctinfo.acclen                   is '��/�ʺų���';
comment on column afa_acctinfo.eigenstr1                is '������1';
comment on column afa_acctinfo.startbit1                is '������1��ʼλ';
comment on column afa_acctinfo.len1                     is '������1����';
comment on column afa_acctinfo.eigenstr2                is '������2';
comment on column afa_acctinfo.startbit2                is '������2��ʼλ';
comment on column afa_acctinfo.len2                     is '������2����';
comment on column afa_acctinfo.eigenstr3                is '������3';
comment on column afa_acctinfo.startbit3                is '������3��ʼλ';
comment on column afa_acctinfo.len3                     is '������3����';
comment on column afa_acctinfo.eigenstr4                is '������4';
comment on column afa_acctinfo.startbit4                is '������4��ʼλ';
comment on column afa_acctinfo.len4                     is '������4����';
comment on column afa_acctinfo.eigenstr5                is '������5';
comment on column afa_acctinfo.startbit5                is '������5��ʼλ';
comment on column afa_acctinfo.len5                     is '������5����';
comment on column afa_acctinfo.acctype                  is '��/�ʺ�����';
comment on column afa_acctinfo.note1                    is '��ע1';
comment on column afa_acctinfo.note2                    is '��ע2';



--/***************************************************************************************************
--*     ����:       ��Կ�����                                                                      *
--*     ����:       �洢ÿ��Ӧ�ö�Ӧ����Կ��Ϣ                                                      *
--*     ��ע:                                                                                       *
--*     ��������:   2006-11-29                                                                      *
--*     ����޸�����:                                                                               *
--*     Ӣ�ı���:   afa_keyadm                                                                      *
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

comment on column afa_keyadm.sysid                      is 'ϵͳ��ʶ';
comment on column afa_keyadm.unitno                     is '�̻���λ����';
comment on column afa_keyadm.subunitno                  is '�̻���֧��λ����';
comment on column afa_keyadm.loginid                    is '��¼��ʶ';
comment on column afa_keyadm.oldpwd                     is 'ԭ�û�����';
comment on column afa_keyadm.newpwd                     is '���û�����';
comment on column afa_keyadm.key1                       is '��Կ1';
comment on column afa_keyadm.key2                       is '��Կ2';
comment on column afa_keyadm.key3                       is '��Կ3';
comment on column afa_keyadm.key4                       is '��Կ4';
comment on column afa_keyadm.key5                       is '��Կ5';
comment on column afa_keyadm.moddate                    is '�޸�����';
comment on column afa_keyadm.senddate                   is '��½����';
comment on column afa_keyadm.note1                      is '��ע1';
comment on column afa_keyadm.note2                      is '��ע2';



--/***************************************************************************************************
--*     ����:       ������Ӧ����Ϣ��                                                                *
--*     ����:       �洢�м�ҵ��ƽ̨�Ľ�����ˮ                                                      *
--*     ��ע:                                                                                       *
--*     ��������:   2006-11-29                                                                      *
--*     ����޸�����:                                                                               *
--*     Ӣ�ı���:   afa_respcode                                                                    *
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

comment on column afa_respcode.sysid                    is 'ϵͳ��ʶ';
comment on column afa_respcode.unitno                   is '�̻���λ����';
comment on column afa_respcode.subunitno                is '�̻���֧��λ����';
comment on column afa_respcode.irespcode                is '�ڲ���Ӧ��';
comment on column afa_respcode.orespcode                is '�ⲿ��Ӧ��';
comment on column afa_respcode.respmsg                  is '��Ӧ��Ϣ';



--/***************************************************************************************************
--*     ����:       ���ù�����Ϣ��                                                                  *
--*     ����:       �洢�м�ҵ��ƽ̨�Ľ����շ���Ϣ                                                  *
--*     ��ע:                                                                                       *
--*     ��������:   2006-11-29                                                                      *
--*     ����޸�����:                                                                               *
--*     Ӣ�ı���:   afa_feeadm                                                                      *
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

comment on column afa_feeadm.sysid                      is 'ϵͳ��ʶ';
comment on column afa_feeadm.unitno                     is '�̻���λ����';
comment on column afa_feeadm.subunitno                  is '�̻��ӵ�λ����';
comment on column afa_feeadm.feeflag                    is '�շ�ģʽ(1-��� 2-����)';
comment on column afa_feeadm.amount                     is '�շѽ��';
comment on column afa_feeadm.note1                      is '��ע1';
comment on column afa_feeadm.note2                      is '��ע2';




--/***************************************************************************************************
--*     ����:       ժҪ������Ϣ��                                                                  *
--*     ����:       �洢�м�ҵ��ƽ̨������ժҪ��Ϣ                                                  *
--*     ��ע:                                                                                       *
--*     ��������:   2006-11-29                                                                      *
--*     ����޸�����:                                                                               *
--*     Ӣ�ı���:   afa_summary                                                                      *
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

comment on column afa_summary.sysid            is 'ϵͳ��ʶ';
comment on column afa_summary.sumno            is 'ժҪ����';
comment on column afa_summary.sumname          is 'ժҪ����';
comment on column afa_summary.note1            is '��ע1';
comment on column afa_summary.note2            is '��ע2';


















--/***************************************************************************************************
--*     ����:       Ӧ��ϵͳ״̬��                                                                  *
--*     ����:       �洢ÿ��Ӧ��ϵͳ�Ŀ�����Ϣ����Ҫ��ϵͳ״̬�����͡���ȿ��Ƶ�                    *
--*     ��ע:                                                                                       *
--*     ��������:   2006-11-29                                                                      *
--*     ����޸�����:                                                                               *
--*     Ӣ�ı���:   afa_system                                                                      *
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


comment on column afa_system.sysid                      is 'ϵͳ��ʶ';
comment on column afa_system.sysename                   is 'ϵͳ���';
comment on column afa_system.syscname                   is 'ϵͳ��������';
comment on column afa_system.workdate                   is 'ҵ������';
comment on column afa_system.preworkdate                is 'ҵ����һ������';
comment on column afa_system.status                     is 'ϵͳ״̬(0-�ر� 1-���� 2-��ͣ 3-δ����)';
comment on column afa_system.type                       is 'ϵͳ����(0-���� 1-���� 2-֧��)';
comment on column afa_system.maxamount                  is '���ʽ��׶��';
comment on column afa_system.totalamount                is '���ۼƽ��׶��';
comment on column afa_system.channelmode                is '��������ģʽ(0-�����п��� 1-�����п��� 2-��֧�п���)';
comment on column afa_system.actnomode                  is '���ʹ���ģʽ(0-�����п��� 1-�����п��� 2-��֧�п���)';
comment on column afa_system.note1                      is '��ע1';
comment on column afa_system.note2                      is '��ע2';
comment on column afa_system.note3                      is '��ע3';



--/***************************************************************************************************
--*     ����:       �̻���λ��Ϣ��                                                                  *
--*     ����:       ��¼ÿ��Ӧ�ö�Ӧ���й��̻��Ŀ�����Ϣ����Ҫ��ҵ��ģʽ���˻�ģʽ������״̬��      *
--*     ��ע:                                                                                       *
--*     ��������:   2006-11-29                                                                      *
--*     ����޸�����:                                                                               *
--*     Ӣ�ı���:   afa_unitadm                                                                     *
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

comment on column afa_unitadm.sysid                  is 'ϵͳ��ʶ';
comment on column afa_unitadm.unitno                 is '�̻���λ����';
comment on column afa_unitadm.unitname               is '�̻�����';
comment on column afa_unitadm.unitsname              is '�̻����';
comment on column afa_unitadm.status                 is '�̻�״̬(0-�ر� 1-���� 2-��ͣ 3-δ����)';
comment on column afa_unitadm.busimode               is 'ҵ��ģʽ(0-�޷�֧���� 1-�з�֧����,ҵ����������̻����� 2-�з�֧����,ҵ��������̻���֧��λ����)';
comment on column afa_unitadm.accmode                is '�˻�ģʽ0-�޷��˻� 1-�з��˻�,�����̻����� 2-�з��˻�,���̻���֧��λ����)';
comment on column afa_unitadm.bankunitno             is '�̻�����(���и��̻�����ı���)';
comment on column afa_unitadm.zoneno                 is '������к�';
comment on column afa_unitadm.brno                   is '���������';
comment on column afa_unitadm.workdate               is 'ҵ������';
comment on column afa_unitadm.preworkdate            is 'ҵ����������';
comment on column afa_unitadm.starttime              is 'ҵ��ʼʱ��';
comment on column afa_unitadm.stoptime               is 'ҵ�����ʱ��';
comment on column afa_unitadm.feeflag                is '��ȡģʽ(0-���շ� 1-�շ�)';
comment on column afa_unitadm.bankcode               is '���б���(�̻������з���ı���)';
comment on column afa_unitadm.accno1                 is '�ʺ�1';
comment on column afa_unitadm.accno2                 is '�ʺ�2';
comment on column afa_unitadm.accno3                 is '�ʺ�3';
comment on column afa_unitadm.accno4                 is '�ʺ�4';
comment on column afa_unitadm.accno5                 is '�ʺ�5';
comment on column afa_unitadm.accno6                 is '�ʺ�6';
comment on column afa_unitadm.name                   is '��ϵ��';
comment on column afa_unitadm.telphone               is '��ϵ�绰';
comment on column afa_unitadm.address                is '��ϵ��ַ';
comment on column afa_unitadm.agenteigen             is 'ҵ��������(1-ǩ��У���־ 2-����У���־ 3-����У���־ 4-��Ӧ��ʹ�ñ�־ 5-�ӱ�ʹ�ñ�־ 6-��չģʽ 7-���׹���ʹ�ñ�־)';
comment on column afa_unitadm.loginstatus            is 'ǩ��״̬(0-ǩ�� 1-ǩ��)';
comment on column afa_unitadm.dayendstatus           is '����״̬(0-δ�� 1-����)';
comment on column afa_unitadm.dayendtime             is '����ʱ��';
comment on column afa_unitadm.trxchkstatus           is '����״̬(0-δ�� 1-�Ѷ������� 2-���������ʳɹ� 3-����������ʧ��)';
comment on column afa_unitadm.trxchktime             is '����ʱ��';
comment on column afa_unitadm.note1                  is '��ע1';
comment on column afa_unitadm.note2                  is '��ע2';



--/***************************************************************************************************
--*     ����:       �̻���֧��λ��Ϣ��                                                              *
--*     ����:       �洢ÿ���̻���Ӧ���з�֧��λ�Ŀ�����Ϣ����Ҫ��ҵ��ģʽ���˻�ģʽ������״̬��    *
--*     ��ע:                                                                                       *
--*     ��������:   2006-11-29                                                                      *
--*     ����޸�����:                                                                               *
--*     Ӣ�ı���:   afa_subunitadm                                                                  *
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

comment on column afa_subunitadm.sysid                  is 'ϵͳ��ʶ';
comment on column afa_subunitadm.unitno                 is '�̻���λ����';
comment on column afa_subunitadm.subunitno              is '�̻���֧��λ����';
comment on column afa_subunitadm.subunitname            is '�̻�����';
comment on column afa_subunitadm.subunitsname           is '�̻����';
comment on column afa_subunitadm.status                 is '�̻�״̬(0-�ر� 1-���� 2-��ͣ 3-δ����)';
comment on column afa_subunitadm.workdate               is 'ҵ������';
comment on column afa_subunitadm.preworkdate            is 'ҵ����������';
comment on column afa_subunitadm.starttime              is 'ҵ��ʼʱ��';
comment on column afa_subunitadm.stoptime               is 'ҵ�����ʱ��';
comment on column afa_subunitadm.feeflag                is '��ȡģʽ(0-���շ� 1-�շ�)';
comment on column afa_subunitadm.bankcode               is '���б���(�̻������з���ı���)';
comment on column afa_subunitadm.zoneno                 is '������к�';
comment on column afa_subunitadm.brno                   is '���������';
comment on column afa_subunitadm.bankunitno             is '�̻�����(���и��̻�����ı���)';
comment on column afa_subunitadm.accno1                 is '�ʺ�1';
comment on column afa_subunitadm.accno2                 is '�ʺ�2';
comment on column afa_subunitadm.accno3                 is '�ʺ�3';
comment on column afa_subunitadm.accno4                 is '�ʺ�4';
comment on column afa_subunitadm.accno5                 is '�ʺ�5';
comment on column afa_subunitadm.accno6                 is '�ʺ�6';
comment on column afa_subunitadm.name                   is '��ϵ��';
comment on column afa_subunitadm.telphone               is '��ϵ�绰';
comment on column afa_subunitadm.address                is '��ϵ��ַ';
comment on column afa_subunitadm.agenteigen             is 'ҵ��������(1-ǩ��У���־ 2-����У���־ 3-����У���־ 4-��Ӧ��ʹ�ñ�־ 5-�ӱ�ʹ�ñ�־ 6-��չģʽ 7-���׹���ʹ�ñ�־)';
comment on column afa_subunitadm.loginstatus            is 'ǩ��״̬(0-ǩ�� 1-ǩ��)';
comment on column afa_subunitadm.dayendstatus           is '����״̬(0-δ�� 1-����)';
comment on column afa_subunitadm.dayendtime             is '����ʱ��';
comment on column afa_subunitadm.trxchkstatus           is '����״̬(0-δ�� 1-�Ѷ������� 2-���������ʳɹ� 3-����������ʧ��)';
comment on column afa_subunitadm.trxchktime             is '����ʱ��';
comment on column afa_subunitadm.note1                  is '��ע1';
comment on column afa_subunitadm.note2                  is '��ע2';









--/***************************************************************************************************
--*     ����:       ������Ϣ�����                                                                  *
--*     ����:       �洢ÿ��Ӧ��ϵͳ��ÿ���̻��Ľ��׿�ͨ����ͽ���������Ϣ                          *
--*     ��ע:                                                                                       *
--*     ��������:   2006-11-29                                                                      *
--*     ����޸�����:                                                                               *
--*     Ӣ�ı���:   afa_tradeadm                                                                    *
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

comment on column afa_tradeadm.sysid                    is 'ϵͳ��ʶ';
comment on column afa_tradeadm.unitno                   is '�̻���λ����';
comment on column afa_tradeadm.subunitno                is '�̻���֧��λ����';
comment on column afa_tradeadm.trxcode                  is '���״���';
comment on column afa_tradeadm.trxname                  is '��������';
comment on column afa_tradeadm.starttime                is 'ҵ��ʼʱ��';
comment on column afa_tradeadm.stoptime                 is 'ҵ�����ʱ��';
comment on column afa_tradeadm.status                   is '����״̬(0-δ���� 1-���� 2-�ر� 3-ͣ��)';
comment on column afa_tradeadm.channelcode              is '��������';
comment on column afa_tradeadm.zoneno                   is '���к�';
comment on column afa_tradeadm.brno                     is '�����';
comment on column afa_tradeadm.tellerno                 is '��Ա��';
comment on column afa_tradeadm.note1                    is '��ע1';
comment on column afa_tradeadm.note2                    is '��ע2';


--/***************************************************************************************************
--*     ����:       ������Ϣ�����                                                                  *
--*     ����:       �洢Ӧ��ϵͳ���̻�����ͨ�ĸ�����������������Ϣ(��ͨ״̬��)                      *
--*     ��ע:                                                                                       *
--*     ��������:   2006-11-29                                                                      *
--*     ����޸�����:                                                                               *
--*     Ӣ�ı���:   afa_channeladm                                                                  *
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

comment on column afa_channeladm.sysid                  is 'ϵͳ��ʶ';
comment on column afa_channeladm.unitno                 is '�̻���λ����';
comment on column afa_channeladm.subunitno              is '�̻���֧��λ����';
comment on column afa_channeladm.agentflag              is 'ҵ��ʽ(01-���� 02-���� 03-���� 04-����)';
comment on column afa_channeladm.zoneno                 is 'ҵ����к�';
comment on column afa_channeladm.zhno                   is 'ҵ��֧�к�';
comment on column afa_channeladm.channelcode            is '��������';
comment on column afa_channeladm.agentbrno              is '��Χϵͳ�����';
comment on column afa_channeladm.agentteller            is '��Χϵͳ����Ա��';
comment on column afa_channeladm.maxamount              is '���ʽ��׶��';
comment on column afa_channeladm.totalamount            is '���ۼƽ��׶��';
comment on column afa_channeladm.billsavectl            is '��Ʊ�����־(0-������ 1-����)';
comment on column afa_channeladm.autorevtranctl         is '�Զ����ʱ�־(0-������ 1-����)';
comment on column afa_channeladm.errchkctl              is '�쳣���׼���־(0-����Ҫ 1-��Ҫ)';
comment on column afa_channeladm.channelstatus          is '����״̬(0-δ���� 1-���� 2-�ر� 3-ͣ��)';
comment on column afa_channeladm.autochkacct            is '�Զ�����ʻ�����(0-���ж� 1-�ж�)';
comment on column afa_channeladm.flag1                  is '��־1(����)';
comment on column afa_channeladm.flag2                  is '��־2(����)';
comment on column afa_channeladm.flag3                  is '��־3(����)';
comment on column afa_channeladm.flag4                  is '��־4(����)';
comment on column afa_channeladm.note1                  is '��ע1';
comment on column afa_channeladm.note2                  is '��ע2';




--/***************************************************************************************************
--*     ����:       �ɷѽ��ʹ����                                                                  *
--*     ����:       �洢Ӧ��ϵͳ���̻�����ͨ�ĸ�������������Ӧ�Ľɷѽ��ʵ�������Ϣ(��ͨ״̬��)      *
--*     ��ע:                                                                                       *
--*     ��������:   2006-11-29                                                                      *
--*     ����޸�����:                                                                               *
--*     Ӣ�ı���:   afa_actnoadm                                                                    *
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

comment on column afa_actnoadm.sysid                    is 'ϵͳ��ʶ';
comment on column afa_actnoadm.unitno                   is '�̻���λ����';
comment on column afa_actnoadm.subunitno                is '�̻���֧��λ����';
comment on column afa_actnoadm.agentflag                is 'ҵ��ʽ(01-���� 02-���� 03-���� 04-����)';
comment on column afa_actnoadm.zoneno                   is '���к�';
comment on column afa_actnoadm.zhno                     is '֧�к�';
comment on column afa_actnoadm.channelcode              is '��������';
comment on column afa_actnoadm.acttypecode              is '�ɷѽ��ʴ���(000-�ֽ� 001-��˽�ʺ� 002-��ǿ� 003-���ǿ� 004-�Թ��ʺ� 005-����)';
comment on column afa_actnoadm.chkaccpwdctl             is 'У���ʻ������־(0-��У��,1-У��)';
comment on column afa_actnoadm.enpaccpwdctl             is '�ʻ�������ܱ�־(0-������,1-����)';
comment on column afa_actnoadm.status                   is '�ɷѽ���״̬(0-δ���� 1-���� 2-�ر� 3-ͣ��)';





--/***************************************************************************************************
--*     ����:       ��ʱ���ȹ����                                                                  *
--*     ����:       �洢�м�ҵ��ƽ̨������Ҫ��ʱ���ȵĳ���Ͳ���                                    *
--*     ��ע:                                                                                       *
--*     ��������:   2006-11-29                                                                      *
--*     ����޸�����:                                                                               *
--*     Ӣ�ı���:   afa_cronadm                                                                     *
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

comment on column afa_cronadm.taskid           is '����ID';
comment on column afa_cronadm.taskname         is '��������';
comment on column afa_cronadm.status           is '״̬(0-�ر� 1-����)';
comment on column afa_cronadm.year             is '��';
comment on column afa_cronadm.month            is '��';
comment on column afa_cronadm.day              is '��';
comment on column afa_cronadm.hour             is 'Сʱ';
comment on column afa_cronadm.minute           is '����';
comment on column afa_cronadm.wday             is '����';
comment on column afa_cronadm.procname         is '��������';
comment on column afa_cronadm.procname         is '��������';
comment on column afa_cronadm.note1            is '��ע1';
comment on column afa_cronadm.note2            is '��ע2';







--/***************************************************************************************************
--*     ����:       ��ˮ����                                                                        *
--*     ����:       �洢�м�ҵ��ƽ̨�Ľ�����ˮ                                                      *
--*     ��ע:                                                                                       *
--*     ��������:   2006-11-29                                                                      *
--*     ����޸�����:                                                                               *
--*     Ӣ�ı���:   afa_maintransdtl                                                                *
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

comment on column afa_maintransdtl.agentserialno        is 'ҵ����ˮ��';
comment on column afa_maintransdtl.workdate             is '��������';
comment on column afa_maintransdtl.worktime             is '����ʱ��';
comment on column afa_maintransdtl.sysid                is 'ϵͳ��ʶ';
comment on column afa_maintransdtl.unitno               is '�̻���λ����';
comment on column afa_maintransdtl.subunitno            is '�̻���֧��λ����';
comment on column afa_maintransdtl.agentflag            is 'ҵ��ʽ(01-���� 02-���� 03-���� 04-����)';
comment on column afa_maintransdtl.trxcode              is '������';
comment on column afa_maintransdtl.zoneno               is '���к�';
comment on column afa_maintransdtl.brno                 is '������';
comment on column afa_maintransdtl.tellerno             is '��Ա��';
comment on column afa_maintransdtl.cashtelno            is '����Ա��';
comment on column afa_maintransdtl.authtellerno         is '��Ȩ��Ա��';
comment on column afa_maintransdtl.channelcode          is '��������';
comment on column afa_maintransdtl.channelserno         is '������ˮ��';
comment on column afa_maintransdtl.termid               is '�ն˺�';
comment on column afa_maintransdtl.customerid           is '�ͻ�ע���';
comment on column afa_maintransdtl.userno               is '�û���';
comment on column afa_maintransdtl.subuserno            is '�����û���';
comment on column afa_maintransdtl.username             is '�û�����';
comment on column afa_maintransdtl.acctype              is '�ʻ�����';
comment on column afa_maintransdtl.draccno              is '�跽�ʻ�����';
comment on column afa_maintransdtl.craccno              is '�����ʻ�����';
comment on column afa_maintransdtl.vouhtype             is 'ƾ֤����';
comment on column afa_maintransdtl.vouhno               is 'ƾ֤��';
comment on column afa_maintransdtl.vouhdate             is 'ƾ֤����';
comment on column afa_maintransdtl.currType             is '����';
comment on column afa_maintransdtl.currFlag             is '�����־';
comment on column afa_maintransdtl.amount               is '���׽��';
comment on column afa_maintransdtl.subamount            is '���ӽ��';
comment on column afa_maintransdtl.revtranf             is '�����ױ�־(0-������ 1-������ 2-�Զ�����)';
comment on column afa_maintransdtl.preagentserno        is '����.ԭƽ̨��ˮ��(������������)';
comment on column afa_maintransdtl.bankstatus           is '����.����״̬(0:���� 1:ʧ�� 2:�쳣 3.�ѳ���)';
comment on column afa_maintransdtl.bankcode             is '����.���׷�����';
comment on column afa_maintransdtl.bankserno            is '����.������ˮ��';
comment on column afa_maintransdtl.corpstatus           is '��ҵ.����״̬(0-���� 1-ʧ�� 2-�쳣 3-�ѳ���)';
comment on column afa_maintransdtl.corpcode             is '��ҵ.���׷�����';
comment on column afa_maintransdtl.corpserno            is '��ҵ.������ˮ��';
comment on column afa_maintransdtl.corptime             is '��ҵ.����ʱ���';
comment on column afa_maintransdtl.errormsg             is '���״�����Ϣ';
comment on column afa_maintransdtl.chkflag              is '�������ʱ�־(0-�Ѷ���,���׳ɹ� 1-�Ѷ���,����ʧ��, 9-δ����)';
comment on column afa_maintransdtl.corpchkflag          is '��ҵ���ʱ�־(0-�Ѷ���,���׳ɹ� 1-�Ѷ���,����ʧ��, 9-δ����)';
comment on column afa_maintransdtl.appendflag           is '�ӱ�ʹ�ñ�־(0-�޴ӱ���Ϣ 1-�дӱ���Ϣ)';
comment on column afa_maintransdtl.note1                is '��ע1';
comment on column afa_maintransdtl.note2                is '��ע2';
comment on column afa_maintransdtl.note3                is '��ע3';
comment on column afa_maintransdtl.note4                is '��ע4';
comment on column afa_maintransdtl.note5                is '��ע5';
comment on column afa_maintransdtl.note6                is '��ע6';
comment on column afa_maintransdtl.note7                is '��ע7';
comment on column afa_maintransdtl.note8                is '��ע8';
comment on column afa_maintransdtl.note9                is '��ע9';
comment on column afa_maintransdtl.note10               is '��ע10';




--/***************************************************************************************************
--*     ����:       ��ˮ�ӱ�                                                                        *
--*     ����:       �洢�м�ҵ��ƽ̨�Ľ�����ˮ�ĸ�����Ϣ                                            *
--*     ��ע:                                                                                       *
--*     ��������:   2006-11-29                                                                      *
--*     ����޸�����:                                                                               *
--*     Ӣ�ı���:   afa_subtransdtl                                                                 *
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

comment on column afa_subtransdtl.agentserialno        is 'ҵ����ˮ��';
comment on column afa_subtransdtl.workdate             is '��������';
comment on column afa_subtransdtl.recseqno             is '��¼���';
comment on column afa_subtransdtl.data1                is '������Ϣ1';
comment on column afa_subtransdtl.data2                is '������Ϣ2';


--/***************************************************************************************************
--*     ����:       ��ʷ��ˮ����                                                                    *
--*     ����:       �м�ҵ��ƽ̨�Ľ�����ˮ                                                          *
--*     ��ע:                                                                                       *
--*     ��������:   2006-11-29                                                                      *
--*     ����޸�����:                                                                               *
--*     Ӣ�ı���:   afa_maintransdtl                                                                *
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

comment on column afa_his_maintransdtl.agentserialno        is 'ҵ����ˮ��';
comment on column afa_his_maintransdtl.workdate             is '��������';
comment on column afa_his_maintransdtl.worktime             is '����ʱ��';
comment on column afa_his_maintransdtl.sysid                is 'ϵͳ��ʶ';
comment on column afa_his_maintransdtl.unitno               is '�̻���λ����';
comment on column afa_his_maintransdtl.subunitno            is '�̻���֧��λ����';
comment on column afa_his_maintransdtl.agentflag            is 'ҵ��ʽ(01-���� 02-���� 03-���� 04-����)';
comment on column afa_his_maintransdtl.trxcode              is '������';
comment on column afa_his_maintransdtl.zoneno               is '���к�';
comment on column afa_his_maintransdtl.brno                 is '������';
comment on column afa_his_maintransdtl.tellerno             is '��Ա��';
comment on column afa_his_maintransdtl.cashtelno            is '����Ա��';
comment on column afa_his_maintransdtl.authtellerno         is '��Ȩ��Ա��';
comment on column afa_his_maintransdtl.channelcode          is '��������';
comment on column afa_his_maintransdtl.channelserno         is '������ˮ��';
comment on column afa_his_maintransdtl.termid               is '�ն˺�';
comment on column afa_his_maintransdtl.customerid           is '�ͻ�ע���';
comment on column afa_his_maintransdtl.userno               is '�û���';
comment on column afa_his_maintransdtl.subuserno            is '�����û���';
comment on column afa_his_maintransdtl.username             is '�û�����';
comment on column afa_his_maintransdtl.acctype              is '�ʻ�����';
comment on column afa_his_maintransdtl.draccno              is '�跽�ʻ�����';
comment on column afa_his_maintransdtl.craccno              is '�����ʻ�����';
comment on column afa_his_maintransdtl.vouhtype             is 'ƾ֤����';
comment on column afa_his_maintransdtl.vouhno               is 'ƾ֤��';
comment on column afa_his_maintransdtl.vouhdate             is 'ƾ֤����';
comment on column afa_his_maintransdtl.currType             is '����';
comment on column afa_his_maintransdtl.currFlag             is '�����־';
comment on column afa_his_maintransdtl.amount               is '���׽��';
comment on column afa_his_maintransdtl.subamount            is '���ӽ��';
comment on column afa_his_maintransdtl.revtranf             is '�����ױ�־(0-������ 1-������ 2-�Զ�����)';
comment on column afa_his_maintransdtl.preagentserno        is '����.ԭƽ̨��ˮ��(������������)';
comment on column afa_his_maintransdtl.bankstatus           is '����.����״̬(0:���� 1:ʧ�� 2:�쳣 3.�ѳ���)';
comment on column afa_his_maintransdtl.bankcode             is '����.���׷�����';
comment on column afa_his_maintransdtl.bankserno            is '����.������ˮ��';
comment on column afa_his_maintransdtl.corpstatus           is '��ҵ.����״̬(0-���� 1-ʧ�� 2-�쳣 3-�ѳ���)';
comment on column afa_his_maintransdtl.corpcode             is '��ҵ.���׷�����';
comment on column afa_his_maintransdtl.corpserno            is '��ҵ.������ˮ��';
comment on column afa_his_maintransdtl.corptime             is '��ҵ.����ʱ���';
comment on column afa_his_maintransdtl.errormsg             is '���״�����Ϣ';
comment on column afa_his_maintransdtl.chkflag              is '�������ʱ�־(0-�Ѷ���,���׳ɹ� 1-�Ѷ���,����ʧ��, 9-δ����)';
comment on column afa_his_maintransdtl.corpchkflag          is '��ҵ���ʱ�־(0-�Ѷ���,���׳ɹ� 1-�Ѷ���,����ʧ��, 9-δ����)';
comment on column afa_his_maintransdtl.appendflag           is '�ӱ�ʹ�ñ�־(0-�޴ӱ���Ϣ 1-�дӱ���Ϣ)';
comment on column afa_his_maintransdtl.note1                is '��ע1';
comment on column afa_his_maintransdtl.note2                is '��ע2';
comment on column afa_his_maintransdtl.note3                is '��ע3';
comment on column afa_his_maintransdtl.note4                is '��ע4';
comment on column afa_his_maintransdtl.note5                is '��ע5';
comment on column afa_his_maintransdtl.note6                is '��ע6';
comment on column afa_his_maintransdtl.note7                is '��ע7';
comment on column afa_his_maintransdtl.note8                is '��ע8';
comment on column afa_his_maintransdtl.note9                is '��ע9';
comment on column afa_his_maintransdtl.note10               is '��ע10';



--/***************************************************************************************************
--*     ����:       ��ʷ��ˮ�ӱ�                                                                    *
--*     ����:       �洢�м�ҵ��ƽ̨����ʷ������ˮ�ĸ�����Ϣ                                        *
--*     ��ע:                                                                                       *
--*     ��������:   2006-11-29                                                                      *
--*     ����޸�����:                                                                               *
--*     Ӣ�ı���:   afa_his_subtransdtl                                                             *
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

comment on column afa_his_subtransdtl.agentserialno        is 'ҵ����ˮ��';
comment on column afa_his_subtransdtl.workdate             is '��������';
comment on column afa_his_subtransdtl.recseqno             is '��¼���';
comment on column afa_his_subtransdtl.data1                is '������Ϣ1';
comment on column afa_his_subtransdtl.data2                is '������Ϣ2';


--/***************************************************************************************************
--*     ����:       ��Ʊ��Ϣ��                                                                      *
--*     ����:       �洢Ӧ��ϵͳ�ķ�Ʊ��Ϣ                                                          *
--*     ��ע:                                                                                       *
--*     ��������:   2006-11-29                                                                      *
--*     ����޸�����:                                                                               *
--*     Ӣ�ı���:   afa_billdtl                                                                     *
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

comment on column afa_billdtl.serialno                  is '��ˮ��';
comment on column afa_billdtl.sysid                     is 'ϵͳ��ʶ';
comment on column afa_billdtl.unitno                    is '�̻���λ����';
comment on column afa_billdtl.subunitno                 is '�̻���֧��λ����';
comment on column afa_billdtl.workdate                  is '��������';
comment on column afa_billdtl.worktime                  is '����ʱ��';
comment on column afa_billdtl.userno                    is '�û���';
comment on column afa_billdtl.username                  is '�û�����';
comment on column afa_billdtl.billstatus                is '��Ʊ״̬(0.���� 1.����)';
comment on column afa_billdtl.prtnum                    is '��ӡ����';
comment on column afa_billdtl.item1                     is '������1';
comment on column afa_billdtl.item2                     is '������2';
comment on column afa_billdtl.item3                     is '������3';
comment on column afa_billdtl.item4                     is '������4';
comment on column afa_billdtl.item5                     is '������5';
comment on column afa_billdtl.item6                     is '������6';
comment on column afa_billdtl.billserno                 is '�ʵ�����';
comment on column afa_billdtl.billdata                  is '��Ʊ����';




--/***************************************************************************************************
--*     ������:     ������������                                                                    *
--*     ����:       ��������Ҫ���ڷ�������������ˮ��                                                *
--*     ��ע:                                                                                       *
--*     ��������:   2006-11-29                                                                      *
--*     ����޸�����:                                                                               *
--*     Ӣ��������: busi_online_seq                                                                 *
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
--*     ������:     ������������                                                                    *
--*     ����:       ��������Ҫ���ڷ�������������ˮ��                                                *
--*     ��ע:                                                                                       *
--*     ��������:   2006-11-29                                                                      *
--*     ����޸�����:                                                                               *
--*     Ӣ��������: busi_online_seq                                                                 *
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
--*     ����:       ��λЭ���                                                                      *
--*     ����:       �洢����ϵͳί�е�λ��Ϣ                                                        *
--*     ��ע:                                                                                       *
--*     ��������:   2006-11-29                                                                      *
--*     ����޸�����:                                                                               *
--*     Ӣ�ı���:   abdt_unitinfo                                                                   *
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

comment on column abdt_unitinfo.appno			is 'ҵ����:AG + ˳���(4)';
comment on column abdt_unitinfo.busino          is '��λ���:��������(10) + ˳���(4)';
comment on column abdt_unitinfo.agenttype       is 'ί�з�ʽ';
comment on column abdt_unitinfo.agentmode       is 'ί�з�Χ';
comment on column abdt_unitinfo.vouhtype        is 'ƾ֤����';
comment on column abdt_unitinfo.vouhno          is 'ƾ֤����';
comment on column abdt_unitinfo.accno           is '�����˻�(�Թ��˻�)';
comment on column abdt_unitinfo.subaccno        is '���˻�����';
comment on column abdt_unitinfo.signupmode      is 'ǩԼ��ʽ(0-˫��, 1-����)';
comment on column abdt_unitinfo.getusernomode   is '��λ�ͻ���Ż�ȡ��ʽ(0-����, 1-��ҵ)';
comment on column abdt_unitinfo.protno          is 'Э���';
comment on column abdt_unitinfo.appname         is 'ҵ������';
comment on column abdt_unitinfo.businame        is '��λ����';
comment on column abdt_unitinfo.address         is '��ϵ��ַ';
comment on column abdt_unitinfo.tel             is '��ϵ�绰';
comment on column abdt_unitinfo.username        is '��ϵ��Ա';
comment on column abdt_unitinfo.workdate        is '��������';
comment on column abdt_unitinfo.batchno         is '���κ�';
comment on column abdt_unitinfo.startdate       is '��Ч����';
comment on column abdt_unitinfo.enddate         is 'ʧЧ����';
comment on column abdt_unitinfo.starttime       is '����ʼʱ��';
comment on column abdt_unitinfo.endtime         is '������ֹʱ��';
comment on column abdt_unitinfo.zoneno          is '��������';
comment on column abdt_unitinfo.brno            is '��������';
comment on column abdt_unitinfo.tellerno        is '��Ա����';
comment on column abdt_unitinfo.regdate         is 'ע������';
comment on column abdt_unitinfo.regtime         is 'ע��ʱ��';
comment on column abdt_unitinfo.status          is '״̬(0-δ����, 1-����, 2-�ر�, 3-ͣ��)';
comment on column abdt_unitinfo.chkdate         is '��������';
comment on column abdt_unitinfo.chktime         is '����ʱ��';
comment on column abdt_unitinfo.chkflag         is '���ʱ�־(0-δ���� 1-�Ѷ���)';
comment on column abdt_unitinfo.note1           is '��ע1';
comment on column abdt_unitinfo.note2           is '��ע2';
comment on column abdt_unitinfo.note3           is '��ע3';
comment on column abdt_unitinfo.note4           is '��ע4';
comment on column abdt_unitinfo.note5           is '��ע5';






--/***************************************************************************************************
--*     ����:       ��λЭ����ʷ��                                                                  *
--*     ����:       �洢����ϵͳί�е�λ��ʷ��Ϣ                                                    *
--*     ��ע:                                                                                       *
--*     ��������:   2006-11-29                                                                      *
--*     ����޸�����:                                                                               *
--*     Ӣ�ı���:   abdt_his_unitinfo                                                               *
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

comment on column abdt_his_unitinfo.appno			is 'ҵ����:AG + ˳���(4)';
comment on column abdt_his_unitinfo.busino          is '��λ���:��������(10) + ˳���(4)';
comment on column abdt_his_unitinfo.agenttype       is 'ί�з�ʽ';
comment on column abdt_his_unitinfo.agentmode       is 'ί�з�Χ';
comment on column abdt_his_unitinfo.vouhtype        is 'ƾ֤����';
comment on column abdt_his_unitinfo.vouhno          is 'ƾ֤����';
comment on column abdt_his_unitinfo.accno           is '�����˻�(�Թ��˻�)';
comment on column abdt_his_unitinfo.subaccno        is '���˻�����';
comment on column abdt_his_unitinfo.signupmode      is 'ǩԼ��ʽ(0-˫��, 1-����)';
comment on column abdt_his_unitinfo.getusernomode   is '��λ�ͻ���Ż�ȡ��ʽ(0-����, 1-��ҵ)';
comment on column abdt_his_unitinfo.protno          is 'Э���';
comment on column abdt_his_unitinfo.appname         is 'ҵ������';
comment on column abdt_his_unitinfo.businame        is '��λ����';
comment on column abdt_his_unitinfo.address         is '��ϵ��ַ';
comment on column abdt_his_unitinfo.tel             is '��ϵ�绰';
comment on column abdt_his_unitinfo.username        is '��ϵ��Ա';
comment on column abdt_his_unitinfo.workdate        is '��������';
comment on column abdt_his_unitinfo.batchno         is '���κ�';
comment on column abdt_his_unitinfo.startdate       is '��Ч����';
comment on column abdt_his_unitinfo.enddate         is 'ʧЧ����';
comment on column abdt_his_unitinfo.starttime       is '����ʼʱ��';
comment on column abdt_his_unitinfo.endtime         is '������ֹʱ��';
comment on column abdt_his_unitinfo.zoneno          is '��������';
comment on column abdt_his_unitinfo.brno            is '��������';
comment on column abdt_his_unitinfo.tellerno        is '��Ա����';
comment on column abdt_his_unitinfo.regdate         is 'ע������';
comment on column abdt_his_unitinfo.regtime         is 'ע��ʱ��';
comment on column abdt_his_unitinfo.status          is '״̬(0-δ����, 1-����, 2-�ر�, 3-ͣ��)';
comment on column abdt_his_unitinfo.chkdate         is '��������';
comment on column abdt_his_unitinfo.chktime         is '����ʱ��';
comment on column abdt_his_unitinfo.chkflag         is '���ʱ�־(0-δ���� 1-�Ѷ���)';
comment on column abdt_his_unitinfo.note1           is '��ע1';
comment on column abdt_his_unitinfo.note2           is '��ע2';
comment on column abdt_his_unitinfo.note3           is '��ע3';
comment on column abdt_his_unitinfo.note4           is '��ע4';
comment on column abdt_his_unitinfo.note5           is '��ע5';



--/***************************************************************************************************
--*     ����:       ����Э���                                                                      *
--*     ����:       �洢����ϵͳί�и�����Ϣ                                                        *
--*     ��ע:                                                                                       *
--*     ��������:   2006-11-29                                                                      *
--*     ����޸�����:                                                                               *
--*     Ӣ�ı���:   abdt_custinfo                                                                   *
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

comment on column abdt_custinfo.appno	           is 'ҵ����(AG + ˳���(4))';
comment on column abdt_custinfo.busino	           is '��λ���(��������(10) + ˳���(4))';
comment on column abdt_custinfo.busiuserno	       is '��λ�ͻ����';
comment on column abdt_custinfo.busiuserappno	   is '�̻��ͻ�Ӧ�ñ��';
comment on column abdt_custinfo.bankuserno	       is '���пͻ����';
comment on column abdt_custinfo.vouhtype	       is 'ƾ֤����(01-��ǿ� 02-���ڴ���)';
comment on column abdt_custinfo.vouhno	           is 'ƾ֤��(19��23λ����)';
comment on column abdt_custinfo.accno	           is '���ڴ���ʺ�(������һ��ͨ��һ��ͨģʽ�����뿨��������Ļ������ʺ�)';
comment on column abdt_custinfo.subaccno	       is '���ʺ�';
comment on column abdt_custinfo.currtype	       is '����(CNY-�����)';
comment on column abdt_custinfo.limitamt	       is '�����޶�(Ҫ�������� =0-������ >0-�������)';
comment on column abdt_custinfo.partflag	       is '���ֿۿ��־(0-���ۿ� 1-���ֿۿ�)';
comment on column abdt_custinfo.protocolno	       is 'Э����(�Զ�����)';
comment on column abdt_custinfo.contractdate	   is 'ǩԼ����(��ͬ����)';
comment on column abdt_custinfo.startdate	       is '��Ч����';
comment on column abdt_custinfo.enddate	           is 'ʧЧ����';
comment on column abdt_custinfo.passchkflag	       is '������֤��־(0-����֤ 1-��ѯ���� 2-��������)';
comment on column abdt_custinfo.passwd	           is '����(����(�ɷ�����))';
comment on column abdt_custinfo.idchkflag	       is '֤����֤��־(0-����֤ 1-���֤)';
comment on column abdt_custinfo.idtype	           is '֤������';
comment on column abdt_custinfo.idcode	           is '֤������(18λ�ַ�)';
comment on column abdt_custinfo.namechkflag	       is '������֤��־(0-����֤ 1-��֤)';
comment on column abdt_custinfo.username	       is '�ͻ�����';
comment on column abdt_custinfo.tel	               is '��ϵ�绰';
comment on column abdt_custinfo.address	           is '��ϵ��ַ';
comment on column abdt_custinfo.zipcode	           is '�ʱ�';
comment on column abdt_custinfo.email	           is '��������';
comment on column abdt_custinfo.status	           is '״̬(0-ע�� 1-����)';
comment on column abdt_custinfo.zoneno	           is '������';
comment on column abdt_custinfo.brno	           is '�����(��������)';
comment on column abdt_custinfo.tellerno	       is '��Ա��';
comment on column abdt_custinfo.indate	           is '¼������';
comment on column abdt_custinfo.intime	           is '¼��ʱ��';
comment on column abdt_custinfo.note1	           is '��ע1';
comment on column abdt_custinfo.note2	           is '��ע2';
comment on column abdt_custinfo.note3	           is '��ע3';
comment on column abdt_custinfo.note4              is '��ע4';
comment on column abdt_custinfo.note5              is '��ע5';


--/***************************************************************************************************
--*     ����:       ����Э����ʷ��                                                                  *
--*     ����:       �洢����ϵͳί�и�����ʷ��Ϣ                                                    *
--*     ��ע:                                                                                       *
--*     ��������:   2006-11-29                                                                      *
--*     ����޸�����:                                                                               *
--*     Ӣ�ı���:   abdt_his_custinfo                                                               *
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

comment on column abdt_his_custinfo.appno	           is 'ҵ����(AG + ˳���(4))';
comment on column abdt_his_custinfo.busino	           is '��λ���(��������(10) + ˳���(4))';
comment on column abdt_his_custinfo.busiuserno	       is '��λ�ͻ����';
comment on column abdt_his_custinfo.busiuserappno	   is '�̻��ͻ�Ӧ�ñ��';
comment on column abdt_his_custinfo.bankuserno	       is '���пͻ����';
comment on column abdt_his_custinfo.vouhtype	       is 'ƾ֤����(01-��ǿ� 02-���ڴ���)';
comment on column abdt_his_custinfo.vouhno	           is 'ƾ֤��(19��23λ����)';
comment on column abdt_his_custinfo.accno	           is '���ڴ���ʺ�(������һ��ͨ��һ��ͨģʽ�����뿨��������Ļ������ʺ�)';
comment on column abdt_his_custinfo.subaccno	       is '���ʺ�';
comment on column abdt_his_custinfo.currtype	       is '����(CNY-�����)';
comment on column abdt_his_custinfo.limitamt	       is '�����޶�(Ҫ�������� =0-������ >0-�������)';
comment on column abdt_his_custinfo.partflag	       is '���ֿۿ��־(0-���ۿ� 1-���ֿۿ�)';
comment on column abdt_his_custinfo.protocolno	       is 'Э����(�Զ�����)';
comment on column abdt_his_custinfo.contractdate	   is 'ǩԼ����(��ͬ����)';
comment on column abdt_his_custinfo.startdate	       is '��Ч����';
comment on column abdt_his_custinfo.enddate	           is 'ʧЧ����';
comment on column abdt_his_custinfo.passchkflag	       is '������֤��־(0-����֤ 1-��ѯ���� 2-��������)';
comment on column abdt_his_custinfo.passwd	           is '����(����(�ɷ�����))';
comment on column abdt_his_custinfo.idchkflag	       is '֤����֤��־(0-����֤ 1-���֤)';
comment on column abdt_his_custinfo.idtype	           is '֤������';
comment on column abdt_his_custinfo.idcode	           is '֤������(18λ�ַ�)';
comment on column abdt_his_custinfo.namechkflag	       is '������֤��־(0-����֤ 1-��֤)';
comment on column abdt_his_custinfo.username	       is '�ͻ�����';
comment on column abdt_his_custinfo.tel	               is '��ϵ�绰';
comment on column abdt_his_custinfo.address	           is '��ϵ��ַ';
comment on column abdt_his_custinfo.zipcode	           is '�ʱ�';
comment on column abdt_his_custinfo.email	           is '��������';
comment on column abdt_his_custinfo.status	           is '״̬(0-ע�� 1-����)';
comment on column abdt_his_custinfo.zoneno	           is '������';
comment on column abdt_his_custinfo.brno	           is '�����(��������)';
comment on column abdt_his_custinfo.tellerno	       is '��Ա��';
comment on column abdt_his_custinfo.indate	           is '¼������';
comment on column abdt_his_custinfo.intime	           is '¼��ʱ��';
comment on column abdt_his_custinfo.note1	           is '��ע1';
comment on column abdt_his_custinfo.note2	           is '��ע2';
comment on column abdt_his_custinfo.note3	           is '��ע3';
comment on column abdt_his_custinfo.note4              is '��ע4';
comment on column abdt_his_custinfo.note5              is '��ע5';


--/***************************************************************************************************
--*     ����:       ������Ϣ��                                                                      *
--*     ����:       �洢����ϵͳ����������Ϣ                                                        *
--*     ��ע:                                                                                       *
--*     ��������:   2006-11-29                                                                      *
--*     ����޸�����:                                                                               *
--*     Ӣ�ı���:   abdt_batchinfo                                                                  *
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


comment on column abdt_batchinfo.batchno	                is 'ί�к�(���κ�)(Ψһ(����+��ˮ��))';
comment on column abdt_batchinfo.appno	                    is 'ҵ����(AG + ˳���(4))';
comment on column abdt_batchinfo.busino	                    is '��λ���(��������(10) + ˳���(4))';
comment on column abdt_batchinfo.zoneno	                    is '������';
comment on column abdt_batchinfo.brno	                    is '�����(��������)';
comment on column abdt_batchinfo.userno	                    is '����Ա';
comment on column abdt_batchinfo.adminno	                is '����Ա';
comment on column abdt_batchinfo.termtype	                is '�ն�����';
comment on column abdt_batchinfo.filename	                is '�ϴ��ļ���(ҵ����+��λ���+����.TXT)';
comment on column abdt_batchinfo.indate	                    is '��������';
comment on column abdt_batchinfo.intime	                    is '����ʱ��';
comment on column abdt_batchinfo.batchdate	                is '�ύ����';
comment on column abdt_batchinfo.batchtime	                is '�ύʱ��';
comment on column abdt_batchinfo.totalnum	                is '�ܱ���';
comment on column abdt_batchinfo.totalamt	                is '�ܽ��';
comment on column abdt_batchinfo.succnum	                is '�ɹ�����';
comment on column abdt_batchinfo.succamt	                is '�ɹ����';
comment on column abdt_batchinfo.failnum	                is 'ʧ�ܱ���';
comment on column abdt_batchinfo.failamt	                is 'ʧ�ܽ��';
comment on column abdt_batchinfo.status	                    is '״̬(00-�ϴ� 10-���� 11-������(����������) 20-���ύ 21-���ڴ����ύ�ļ� 22-���ύ(���ڴ���) 30-����� 31-���ڴ�������ļ� 32-����� 88-�������(�����ļ���ҵ�񱨱�) 40-����)';
comment on column abdt_batchinfo.begindate	                is '��Ч����';
comment on column abdt_batchinfo.enddate	                is 'ʧЧ����';
comment on column abdt_batchinfo.procmsg	                is '������Ϣ';
comment on column abdt_batchinfo.note1	                    is '��ע1';
comment on column abdt_batchinfo.note2	                    is '��ע2';
comment on column abdt_batchinfo.note3	                    is '��ע3';
comment on column abdt_batchinfo.note4	                    is '��ע4';
comment on column abdt_batchinfo.note5	                    is '��ע5';





--/***************************************************************************************************
--*     ����:       ������Ϣ��ʷ��                                                                  *
--*     ����:       �洢����ϵͳ������ʷ������Ϣ                                                    *
--*     ��ע:                                                                                       *
--*     ��������:   2006-11-29                                                                      *
--*     ����޸�����:                                                                               *
--*     Ӣ�ı���:   abdt_his_batchinfo                                                              *
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


comment on column abdt_his_batchinfo.batchno	                is 'ί�к�(���κ�)(Ψһ(����+��ˮ��))';
comment on column abdt_his_batchinfo.appno	                    is 'ҵ����(AG + ˳���(4))';
comment on column abdt_his_batchinfo.busino	                    is '��λ���(��������(10) + ˳���(4))';
comment on column abdt_his_batchinfo.zoneno	                    is '������';
comment on column abdt_his_batchinfo.brno	                    is '�����(��������)';
comment on column abdt_his_batchinfo.userno	                    is '����Ա';
comment on column abdt_his_batchinfo.adminno	                is '����Ա';
comment on column abdt_his_batchinfo.termtype	                is '�ն�����';
comment on column abdt_his_batchinfo.filename	                is '�ϴ��ļ���(ҵ����+��λ���+����.TXT)';
comment on column abdt_his_batchinfo.indate	                    is '��������';
comment on column abdt_his_batchinfo.intime	                    is '����ʱ��';
comment on column abdt_his_batchinfo.batchdate	                is '�ύ����';
comment on column abdt_his_batchinfo.batchtime	                is '�ύʱ��';
comment on column abdt_his_batchinfo.totalnum	                is '�ܱ���';
comment on column abdt_his_batchinfo.totalamt	                is '�ܽ��';
comment on column abdt_his_batchinfo.succnum	                is '�ɹ�����';
comment on column abdt_his_batchinfo.succamt	                is '�ɹ����';
comment on column abdt_his_batchinfo.failnum	                is 'ʧ�ܱ���';
comment on column abdt_his_batchinfo.failamt	                is 'ʧ�ܽ��';
comment on column abdt_his_batchinfo.status	                    is '״̬(00-�ϴ� 10-���� 11-������(����������) 20-���ύ 21-���ڴ����ύ�ļ� 22-���ύ(���ڴ���) 30-����� 31-���ڴ�������ļ� 32-����� 88-�������(�����ļ���ҵ�񱨱�) 40-����)';
comment on column abdt_his_batchinfo.begindate	                is '��Ч����';
comment on column abdt_his_batchinfo.enddate	                is 'ʧЧ����';
comment on column abdt_his_batchinfo.procmsg	                is '������Ϣ';
comment on column abdt_his_batchinfo.note1	                    is '��ע1';
comment on column abdt_his_batchinfo.note2	                    is '��ע2';
comment on column abdt_his_batchinfo.note3	                    is '��ע3';
comment on column abdt_his_batchinfo.note4	                    is '��ע4';
comment on column abdt_his_batchinfo.note5	                    is '��ע5';













--/***************************************************************************************************
--*     ����:       ������־��                                                                      *
--*     ����:       �洢����ϵͳ���в�����־                                                        *
--*     ��ע:                                                                                       *
--*     ��������:   2006-11-29                                                                      *
--*     ����޸�����:                                                                               *
--*     Ӣ�ı���:   abdt_loginfo                                                                    *
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


comment on column abdt_loginfo.zoneno	                is '������';
comment on column abdt_loginfo.brno	                    is '�����(��������)';
comment on column abdt_loginfo.tellerno	                is '����Ա';
comment on column abdt_loginfo.termid	                is '�ն˺�';
comment on column abdt_loginfo.workdate	                is '����';
comment on column abdt_loginfo.worktime	                is 'ʱ��';
comment on column abdt_loginfo.batchno	                is 'ί�к�(���κ�)';
comment on column abdt_loginfo.tasktype	                is '��������(״̬(00-�ϴ� 10-���� 11-������(����������) 20-���ύ 21-���ڴ����ύ�ļ� 22-���ύ(���ڴ���) 30-����� 31-���ڴ�������ļ� 32-����� 88-�������(�����ļ���ҵ�񱨱�) 40-����))';
comment on column abdt_loginfo.taskstatus	            is '����״̬(0-�ɹ�  1-ʧ��2-�쳣)';
comment on column abdt_loginfo.taskmsg	                is '����������';
comment on column abdt_loginfo.note1	                is '��ע1';
comment on column abdt_loginfo.note2	                is '��ע2';




--/***************************************************************************************************
--*     ����:       ����ҵ����Ϣ��                                                                  *
--*     ����:       �洢����ҵ���������Ϣ                                                          *
--*     ��ע:                                                                                       *
--*     ��������:   2006-11-29                                                                      *
--*     ����޸�����:                                                                               *
--*     Ӣ�ı���:   abdt_loginfo                                                                    *
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

comment on column afa_zhywinfo.id                  is 'ҵ����';
comment on column afa_zhywinfo.flag                is '��/����';
comment on column afa_zhywinfo.brno                is '���б��';
comment on column afa_zhywinfo.fwqip               is '�������û���';
comment on column afa_zhywinfo.fwqport	           is '����������';
comment on column afa_zhywinfo.dburl               is '������URL';
comment on column afa_zhywinfo.ftpid               is 'ftp�û���';
comment on column afa_zhywinfo.ftppw               is 'ftp����';
comment on column afa_zhywinfo.note1               is '��ע1';
comment on column afa_zhywinfo.note2               is '��ע2';



--/***************************************************************************************************
--*     ����:       �û���Ϣ��                                                                      *
--*     ����:       ����������������û���Ϣ                                                        *
--*     ��ע:                                                                                       *
--*     ��������:   2006-11-29                                                                      *
--*     ����޸�����:                                                                               *
--*     Ӣ�ı���:   abdt_loginfo                                                                    *
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

comment on column abdt_userinfo.zoneno			is '������';
comment on column abdt_userinfo.brno			is '�����(��������)';
comment on column abdt_userinfo.userno			is '����Ա';
comment on column abdt_userinfo.username		is '�û�����';
comment on column abdt_userinfo.address		    is '��ϵ��ַ';
comment on column abdt_userinfo.tel			    is '��ϵ�绰';
comment on column abdt_userinfo.regdate			is 'ע������';
comment on column abdt_userinfo.regtime			is 'ע��ʱ��';
comment on column abdt_userinfo.password		is '����';
comment on column abdt_userinfo.dutyno			is '��λ����';
comment on column abdt_userinfo.status			is '״̬';
comment on column abdt_userinfo.note1			is '��ע1';
comment on column abdt_userinfo.note2			is '��ע2';
comment on column abdt_userinfo.note3			is '��ע3';
comment on column abdt_userinfo.note4		    is '��ע4';
comment on column abdt_userinfo.note5			is '��ע5';





--/***************************************************************************************************
--*     ����:       �������ձ�                                                                      *
--*     ����:       �������ձ�(���������)                                                          *
--*     ��ע:                                                                                       *
--*     ��������:   2006-11-29                                                                      *
--*     ����޸�����:                                                                               *
--*     Ӣ�ı���:   abdt_czdzb                                                                      *
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

comment on column abdt_czdzb.appno			is 'ҵ����';
comment on column abdt_czdzb.czzjdm			is '�ʽ����';
comment on column abdt_czdzb.zjdmmc			is '��λ����';
comment on column abdt_czdzb.note1		    is '��ע1';
comment on column abdt_czdzb.note2		    is '��ע2';

commit;
