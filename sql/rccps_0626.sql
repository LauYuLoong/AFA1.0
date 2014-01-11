-- This CLP file was created using DB2LOOK Version 9.1
-- Timestamp: ��Ԫ2008��06��26��  ������  11ʱ08��59��
-- Database Name: AFA            
-- Database Manager Version: DB2/AIX64 Version 9.1.0       
-- Database Codepage: 1383
-- Database Collating Sequence is: UNIQUE


CONNECT TO AFA;


---------------------------------
-- DDL Statements for Sequences
---------------------------------


CREATE SEQUENCE "AFA     "."ABDT_ONLINE_SEQ" AS INTEGER
	MINVALUE 1 MAXVALUE 99999999
	START WITH 1 INCREMENT BY 1
	CACHE 10 CYCLE NO ORDER;

CREATE SEQUENCE "AFA     "."BUSI_ONLINE_SEQ" AS INTEGER
	MINVALUE 1 MAXVALUE 99999999
	START WITH 1 INCREMENT BY 1
	CACHE 10 CYCLE NO ORDER;

ALTER SEQUENCE "AFA     "."BUSI_ONLINE_SEQ" RESTART WITH 7640;

CREATE SEQUENCE "AFA     "."RCC_SEQ" AS INTEGER
	MINVALUE 1 MAXVALUE 99999999
	START WITH 1 INCREMENT BY 1
	CACHE 10 CYCLE NO ORDER;

ALTER SEQUENCE "AFA     "."RCC_SEQ" RESTART WITH 1640;

CREATE SEQUENCE "AFA     "."RCCPS_SEQ" AS INTEGER
	MINVALUE 1 MAXVALUE 999999
	START WITH 1 INCREMENT BY 1
	CACHE 10 CYCLE NO ORDER;

ALTER SEQUENCE "AFA     "."RCCPS_SEQ" RESTART WITH 1770;

CREATE SEQUENCE "AFA     "."TYHD_SEQ" AS INTEGER
	MINVALUE 1 MAXVALUE 9999
	START WITH 1 INCREMENT BY 1
	CACHE 10 CYCLE NO ORDER;

ALTER SEQUENCE "AFA     "."TYHD_SEQ" RESTART WITH 70;

CREATE SEQUENCE "AFA     "."VOUH_ONLINE_SEQ" AS INTEGER
	MINVALUE 80000001 MAXVALUE 89999999
	START WITH 80000001 INCREMENT BY 1
	CACHE 20 CYCLE NO ORDER;

ALTER SEQUENCE "AFA     "."VOUH_ONLINE_SEQ" RESTART WITH 80000400;


------------------------------------------------
-- DDL Statements for table "AFA     "."AFA_MAINDICT"
------------------------------------------------
 

CREATE TABLE "AFA     "."AFA_MAINDICT"  (
		  "ITEM" VARCHAR(5) NOT NULL , 
		  "ITEMENAME" VARCHAR(20) NOT NULL , 
		  "ITEMCNAME" VARCHAR(50) NOT NULL )   
		 IN "AFA_DATA" INDEX IN "AFA_IDX" ; 

COMMENT ON COLUMN "AFA     "."AFA_MAINDICT"."ITEM" IS '���';

COMMENT ON COLUMN "AFA     "."AFA_MAINDICT"."ITEMCNAME" IS 'Ӣ������';

COMMENT ON COLUMN "AFA     "."AFA_MAINDICT"."ITEMENAME" IS 'Ӣ������';


-- DDL Statements for primary key on Table "AFA     "."AFA_MAINDICT"

ALTER TABLE "AFA     "."AFA_MAINDICT" 
	ADD CONSTRAINT "AFA_MAINDICT_KEY" PRIMARY KEY
		("ITEM");



------------------------------------------------
-- DDL Statements for table "AFA     "."AFA_SUBDICT"
------------------------------------------------
 

CREATE TABLE "AFA     "."AFA_SUBDICT"  (
		  "ITEM" VARCHAR(5) NOT NULL , 
		  "CODE" VARCHAR(10) NOT NULL , 
		  "CODENAME" VARCHAR(50) NOT NULL )   
		 IN "AFA_DATA" INDEX IN "AFA_IDX" ; 

COMMENT ON COLUMN "AFA     "."AFA_SUBDICT"."CODE" IS '����';

COMMENT ON COLUMN "AFA     "."AFA_SUBDICT"."CODENAME" IS '��������';

COMMENT ON COLUMN "AFA     "."AFA_SUBDICT"."ITEM" IS '���';


-- DDL Statements for primary key on Table "AFA     "."AFA_SUBDICT"

ALTER TABLE "AFA     "."AFA_SUBDICT" 
	ADD CONSTRAINT "AFA_SUBDICT_KEY" PRIMARY KEY
		("ITEM",
		 "CODE");



------------------------------------------------
-- DDL Statements for table "AFA     "."AFA_ACCTINFO"
------------------------------------------------
 

CREATE TABLE "AFA     "."AFA_ACCTINFO"  (
		  "SEQNO" SMALLINT NOT NULL , 
		  "ACCLEN" SMALLINT NOT NULL , 
		  "EIGENSTR1" VARCHAR(30) , 
		  "STARTBIT1" SMALLINT , 
		  "LEN1" SMALLINT , 
		  "EIGENSTR2" VARCHAR(30) , 
		  "STARTBIT2" SMALLINT , 
		  "LEN2" SMALLINT , 
		  "EIGENSTR3" VARCHAR(30) , 
		  "STARTBIT3" SMALLINT , 
		  "LEN3" SMALLINT , 
		  "EIGENSTR4" VARCHAR(30) , 
		  "STARTBIT4" SMALLINT , 
		  "LEN4" SMALLINT , 
		  "EIGENSTR5" VARCHAR(30) , 
		  "STARTBIT5" SMALLINT , 
		  "LEN5" SMALLINT , 
		  "ACCTYPE" VARCHAR(3) NOT NULL , 
		  "NOTE1" VARCHAR(30) , 
		  "NOTE2" VARCHAR(30) )   
		 IN "AFA_DATA" INDEX IN "AFA_IDX" ; 

COMMENT ON COLUMN "AFA     "."AFA_ACCTINFO"."ACCLEN" IS '��/�ʺų���';

COMMENT ON COLUMN "AFA     "."AFA_ACCTINFO"."ACCTYPE" IS '��/�ʺ�����';

COMMENT ON COLUMN "AFA     "."AFA_ACCTINFO"."EIGENSTR1" IS '������1';

COMMENT ON COLUMN "AFA     "."AFA_ACCTINFO"."EIGENSTR2" IS '������2';

COMMENT ON COLUMN "AFA     "."AFA_ACCTINFO"."EIGENSTR3" IS '������3';

COMMENT ON COLUMN "AFA     "."AFA_ACCTINFO"."EIGENSTR4" IS '������4';

COMMENT ON COLUMN "AFA     "."AFA_ACCTINFO"."EIGENSTR5" IS '������5';

COMMENT ON COLUMN "AFA     "."AFA_ACCTINFO"."LEN1" IS '������1����';

COMMENT ON COLUMN "AFA     "."AFA_ACCTINFO"."LEN2" IS '������2����';

COMMENT ON COLUMN "AFA     "."AFA_ACCTINFO"."LEN3" IS '������3����';

COMMENT ON COLUMN "AFA     "."AFA_ACCTINFO"."LEN4" IS '������4����';

COMMENT ON COLUMN "AFA     "."AFA_ACCTINFO"."LEN5" IS '������5����';

COMMENT ON COLUMN "AFA     "."AFA_ACCTINFO"."NOTE1" IS '��ע1';

COMMENT ON COLUMN "AFA     "."AFA_ACCTINFO"."NOTE2" IS '��ע2';

COMMENT ON COLUMN "AFA     "."AFA_ACCTINFO"."SEQNO" IS '���';

COMMENT ON COLUMN "AFA     "."AFA_ACCTINFO"."STARTBIT1" IS '������1��ʼλ';

COMMENT ON COLUMN "AFA     "."AFA_ACCTINFO"."STARTBIT2" IS '������2��ʼλ';

COMMENT ON COLUMN "AFA     "."AFA_ACCTINFO"."STARTBIT3" IS '������3��ʼλ';

COMMENT ON COLUMN "AFA     "."AFA_ACCTINFO"."STARTBIT4" IS '������4��ʼλ';

COMMENT ON COLUMN "AFA     "."AFA_ACCTINFO"."STARTBIT5" IS '������5��ʼλ';


-- DDL Statements for primary key on Table "AFA     "."AFA_ACCTINFO"

ALTER TABLE "AFA     "."AFA_ACCTINFO" 
	ADD CONSTRAINT "AFA_ACCTINFO_KEY" PRIMARY KEY
		("SEQNO");



------------------------------------------------
-- DDL Statements for table "AFA     "."AFA_KEYADM"
------------------------------------------------
 

CREATE TABLE "AFA     "."AFA_KEYADM"  (
		  "SYSID" VARCHAR(6) NOT NULL , 
		  "UNITNO" VARCHAR(8) NOT NULL , 
		  "SUBUNITNO" VARCHAR(8) NOT NULL , 
		  "LOGINID" VARCHAR(18) , 
		  "OLDPWD" VARCHAR(64) , 
		  "NEWPWD" VARCHAR(64) , 
		  "KEY1" VARCHAR(64) , 
		  "KEY2" VARCHAR(64) , 
		  "KEY3" VARCHAR(64) , 
		  "KEY4" VARCHAR(64) , 
		  "KEY5" VARCHAR(64) , 
		  "MODDATE" VARCHAR(8) , 
		  "SENDDATE" VARCHAR(8) , 
		  "NOTE1" VARCHAR(64) , 
		  "NOTE2" VARCHAR(64) )   
		 IN "AFA_DATA" INDEX IN "AFA_IDX" ; 

COMMENT ON COLUMN "AFA     "."AFA_KEYADM"."KEY1" IS '��Կ1';

COMMENT ON COLUMN "AFA     "."AFA_KEYADM"."KEY2" IS '��Կ2';

COMMENT ON COLUMN "AFA     "."AFA_KEYADM"."KEY3" IS '��Կ3';

COMMENT ON COLUMN "AFA     "."AFA_KEYADM"."KEY4" IS '��Կ4';

COMMENT ON COLUMN "AFA     "."AFA_KEYADM"."KEY5" IS '��Կ5';

COMMENT ON COLUMN "AFA     "."AFA_KEYADM"."LOGINID" IS '��¼��ʶ';

COMMENT ON COLUMN "AFA     "."AFA_KEYADM"."MODDATE" IS '�޸�����';

COMMENT ON COLUMN "AFA     "."AFA_KEYADM"."NEWPWD" IS '���û�����';

COMMENT ON COLUMN "AFA     "."AFA_KEYADM"."NOTE1" IS '��ע1';

COMMENT ON COLUMN "AFA     "."AFA_KEYADM"."NOTE2" IS '��ע2';

COMMENT ON COLUMN "AFA     "."AFA_KEYADM"."OLDPWD" IS 'ԭ�û�����';

COMMENT ON COLUMN "AFA     "."AFA_KEYADM"."SENDDATE" IS '��½����';

COMMENT ON COLUMN "AFA     "."AFA_KEYADM"."SUBUNITNO" IS '�̻���֧��λ����';

COMMENT ON COLUMN "AFA     "."AFA_KEYADM"."SYSID" IS 'ϵͳ��ʶ';

COMMENT ON COLUMN "AFA     "."AFA_KEYADM"."UNITNO" IS '�̻���λ����';


-- DDL Statements for primary key on Table "AFA     "."AFA_KEYADM"

ALTER TABLE "AFA     "."AFA_KEYADM" 
	ADD CONSTRAINT "AFA_KEYADM_KEY" PRIMARY KEY
		("SYSID",
		 "UNITNO",
		 "SUBUNITNO");



------------------------------------------------
-- DDL Statements for table "AFA     "."AFA_FEEADM"
------------------------------------------------
 

CREATE TABLE "AFA     "."AFA_FEEADM"  (
		  "SYSID" VARCHAR(6) NOT NULL , 
		  "UNITNO" VARCHAR(8) NOT NULL , 
		  "SUBUNITNO" VARCHAR(8) NOT NULL , 
		  "FEEFLAG" VARCHAR(1) NOT NULL , 
		  "AMOUNT" VARCHAR(17) NOT NULL , 
		  "NOTE1" VARCHAR(10) , 
		  "NOTE2" VARCHAR(20) )   
		 IN "AFA_DATA" INDEX IN "AFA_IDX" ; 

COMMENT ON COLUMN "AFA     "."AFA_FEEADM"."AMOUNT" IS '�շѽ��';

COMMENT ON COLUMN "AFA     "."AFA_FEEADM"."FEEFLAG" IS '�շ�ģʽ(1-��� 2-����)';

COMMENT ON COLUMN "AFA     "."AFA_FEEADM"."NOTE1" IS '��ע1';

COMMENT ON COLUMN "AFA     "."AFA_FEEADM"."NOTE2" IS '��ע2';

COMMENT ON COLUMN "AFA     "."AFA_FEEADM"."SUBUNITNO" IS '�̻��ӵ�λ����';

COMMENT ON COLUMN "AFA     "."AFA_FEEADM"."SYSID" IS 'ϵͳ��ʶ';

COMMENT ON COLUMN "AFA     "."AFA_FEEADM"."UNITNO" IS '�̻���λ����';


-- DDL Statements for primary key on Table "AFA     "."AFA_FEEADM"

ALTER TABLE "AFA     "."AFA_FEEADM" 
	ADD CONSTRAINT "AFA_FEEADM_KEY" PRIMARY KEY
		("SYSID",
		 "UNITNO",
		 "SUBUNITNO");



------------------------------------------------
-- DDL Statements for table "AFA     "."AFA_BILLDTL"
------------------------------------------------
 

CREATE TABLE "AFA     "."AFA_BILLDTL"  (
		  "SERIALNO" VARCHAR(8) NOT NULL , 
		  "SYSID" VARCHAR(6) NOT NULL , 
		  "UNITNO" VARCHAR(8) NOT NULL , 
		  "SUBUNITNO" VARCHAR(8) NOT NULL , 
		  "WORKDATE" VARCHAR(8) NOT NULL , 
		  "WORKTIME" VARCHAR(6) NOT NULL , 
		  "USERNO" VARCHAR(30) NOT NULL , 
		  "USERNAME" VARCHAR(60) , 
		  "BILLSTATUS" VARCHAR(1) NOT NULL , 
		  "PRTNUM" VARCHAR(2) NOT NULL , 
		  "ITEM1" VARCHAR(20) , 
		  "ITEM2" VARCHAR(20) , 
		  "ITEM3" VARCHAR(40) , 
		  "ITEM4" VARCHAR(40) , 
		  "ITEM5" VARCHAR(60) , 
		  "ITEM6" VARCHAR(60) , 
		  "BILLSERNO" VARCHAR(3) , 
		  "BILLDATA" VARCHAR(2048) )   
		 IN "AFA_DATA" INDEX IN "AFA_IDX" ; 

COMMENT ON COLUMN "AFA     "."AFA_BILLDTL"."BILLDATA" IS '��Ʊ����';

COMMENT ON COLUMN "AFA     "."AFA_BILLDTL"."BILLSERNO" IS '�ʵ�����';

COMMENT ON COLUMN "AFA     "."AFA_BILLDTL"."BILLSTATUS" IS '��Ʊ״̬(0.���� 1.����)';

COMMENT ON COLUMN "AFA     "."AFA_BILLDTL"."ITEM1" IS '������1';

COMMENT ON COLUMN "AFA     "."AFA_BILLDTL"."ITEM2" IS '������2';

COMMENT ON COLUMN "AFA     "."AFA_BILLDTL"."ITEM3" IS '������3';

COMMENT ON COLUMN "AFA     "."AFA_BILLDTL"."ITEM4" IS '������4';

COMMENT ON COLUMN "AFA     "."AFA_BILLDTL"."ITEM5" IS '������5';

COMMENT ON COLUMN "AFA     "."AFA_BILLDTL"."ITEM6" IS '������6';

COMMENT ON COLUMN "AFA     "."AFA_BILLDTL"."PRTNUM" IS '��ӡ����';

COMMENT ON COLUMN "AFA     "."AFA_BILLDTL"."SERIALNO" IS '��ˮ��';

COMMENT ON COLUMN "AFA     "."AFA_BILLDTL"."SUBUNITNO" IS '�̻���֧��λ����';

COMMENT ON COLUMN "AFA     "."AFA_BILLDTL"."SYSID" IS 'ϵͳ��ʶ';

COMMENT ON COLUMN "AFA     "."AFA_BILLDTL"."UNITNO" IS '�̻���λ����';

COMMENT ON COLUMN "AFA     "."AFA_BILLDTL"."USERNAME" IS '�û�����';

COMMENT ON COLUMN "AFA     "."AFA_BILLDTL"."USERNO" IS '�û���';

COMMENT ON COLUMN "AFA     "."AFA_BILLDTL"."WORKDATE" IS '��������';

COMMENT ON COLUMN "AFA     "."AFA_BILLDTL"."WORKTIME" IS '����ʱ��';


-- DDL Statements for indexes on Table "AFA     "."AFA_BILLDTL"

CREATE INDEX "AFA     "."AFA_BILLDTL_IDX1" ON "AFA     "."AFA_BILLDTL" 
		("SYSID" ASC,
		 "UNITNO" ASC,
		 "WORKDATE" ASC,
		 "USERNO" ASC)
		ALLOW REVERSE SCANS;


-- DDL Statements for indexes on Table "AFA     "."AFA_BILLDTL"

CREATE INDEX "AFA     "."AFA_BILLDTL_IDX2" ON "AFA     "."AFA_BILLDTL" 
		("WORKDATE" ASC,
		 "SERIALNO" ASC)
		ALLOW REVERSE SCANS;






------------------------------------------------
-- DDL Statements for table "AFA     "."AFA_HIS_SUBTRANSDTL"
------------------------------------------------
 

CREATE TABLE "AFA     "."AFA_HIS_SUBTRANSDTL"  (
		  "AGENTSERIALNO" VARCHAR(8) NOT NULL , 
		  "WORKDATE" VARCHAR(8) NOT NULL , 
		  "RECSEQNO" VARCHAR(2) NOT NULL , 
		  "DATA1" VARCHAR(1024) NOT NULL , 
		  "DATA2" VARCHAR(1024) )   
		 IN "AFA_DATA" INDEX IN "AFA_IDX" ; 

COMMENT ON COLUMN "AFA     "."AFA_HIS_SUBTRANSDTL"."AGENTSERIALNO" IS 'ҵ����ˮ��';

COMMENT ON COLUMN "AFA     "."AFA_HIS_SUBTRANSDTL"."DATA1" IS '������Ϣ1';

COMMENT ON COLUMN "AFA     "."AFA_HIS_SUBTRANSDTL"."DATA2" IS '������Ϣ2';

COMMENT ON COLUMN "AFA     "."AFA_HIS_SUBTRANSDTL"."RECSEQNO" IS '��¼���';

COMMENT ON COLUMN "AFA     "."AFA_HIS_SUBTRANSDTL"."WORKDATE" IS '��������';


-- DDL Statements for primary key on Table "AFA     "."AFA_HIS_SUBTRANSDTL"

ALTER TABLE "AFA     "."AFA_HIS_SUBTRANSDTL" 
	ADD CONSTRAINT "AFA_HSUBDTL_KEY" PRIMARY KEY
		("WORKDATE",
		 "AGENTSERIALNO");



------------------------------------------------
-- DDL Statements for table "AFA     "."AFA_SUBTRANSDTL"
------------------------------------------------
 

CREATE TABLE "AFA     "."AFA_SUBTRANSDTL"  (
		  "AGENTSERIALNO" VARCHAR(8) NOT NULL , 
		  "WORKDATE" VARCHAR(8) NOT NULL , 
		  "RECSEQNO" VARCHAR(2) NOT NULL , 
		  "DATA1" VARCHAR(1024) NOT NULL , 
		  "DATA2" VARCHAR(1024) )   
		 IN "AFA_DATA" INDEX IN "AFA_IDX" ; 

COMMENT ON COLUMN "AFA     "."AFA_SUBTRANSDTL"."AGENTSERIALNO" IS 'ҵ����ˮ��';

COMMENT ON COLUMN "AFA     "."AFA_SUBTRANSDTL"."DATA1" IS '������Ϣ1';

COMMENT ON COLUMN "AFA     "."AFA_SUBTRANSDTL"."DATA2" IS '������Ϣ2';

COMMENT ON COLUMN "AFA     "."AFA_SUBTRANSDTL"."RECSEQNO" IS '��¼���';

COMMENT ON COLUMN "AFA     "."AFA_SUBTRANSDTL"."WORKDATE" IS '��������';


-- DDL Statements for primary key on Table "AFA     "."AFA_SUBTRANSDTL"

ALTER TABLE "AFA     "."AFA_SUBTRANSDTL" 
	ADD CONSTRAINT "AFA_SUBDTL_KEY" PRIMARY KEY
		("WORKDATE",
		 "AGENTSERIALNO");



------------------------------------------------
-- DDL Statements for table "AFA     "."AFA_RESPCODE"
------------------------------------------------
 

CREATE TABLE "AFA     "."AFA_RESPCODE"  (
		  "SYSID" VARCHAR(6) NOT NULL , 
		  "UNITNO" VARCHAR(8) NOT NULL , 
		  "SUBUNITNO" VARCHAR(8) NOT NULL , 
		  "IRESPCODE" VARCHAR(20) NOT NULL , 
		  "ORESPCODE" VARCHAR(20) NOT NULL , 
		  "RESPMSG" VARCHAR(128) NOT NULL )   
		 IN "AFA_DATA" INDEX IN "AFA_IDX" ; 

COMMENT ON COLUMN "AFA     "."AFA_RESPCODE"."IRESPCODE" IS '�ڲ���Ӧ��';

COMMENT ON COLUMN "AFA     "."AFA_RESPCODE"."ORESPCODE" IS '�ⲿ��Ӧ��';

COMMENT ON COLUMN "AFA     "."AFA_RESPCODE"."RESPMSG" IS '��Ӧ��Ϣ';

COMMENT ON COLUMN "AFA     "."AFA_RESPCODE"."SUBUNITNO" IS '�̻���֧��λ����';

COMMENT ON COLUMN "AFA     "."AFA_RESPCODE"."SYSID" IS 'ϵͳ��ʶ';

COMMENT ON COLUMN "AFA     "."AFA_RESPCODE"."UNITNO" IS '�̻���λ����';


-- DDL Statements for primary key on Table "AFA     "."AFA_RESPCODE"

ALTER TABLE "AFA     "."AFA_RESPCODE" 
	ADD CONSTRAINT "AFA_RESPCODE_KEY" PRIMARY KEY
		("SYSID",
		 "UNITNO",
		 "SUBUNITNO",
		 "IRESPCODE",
		 "ORESPCODE");



------------------------------------------------
-- DDL Statements for table "AFA     "."AFA_SUMMARY"
------------------------------------------------
 

CREATE TABLE "AFA     "."AFA_SUMMARY"  (
		  "SYSID" VARCHAR(6) NOT NULL , 
		  "SUMNO" VARCHAR(3) NOT NULL , 
		  "SUMNAME" VARCHAR(60) , 
		  "NOTE1" VARCHAR(10) , 
		  "NOTE2" VARCHAR(20) )   
		 IN "AFA_DATA" INDEX IN "AFA_IDX" ; 

COMMENT ON COLUMN "AFA     "."AFA_SUMMARY"."NOTE1" IS '��ע1';

COMMENT ON COLUMN "AFA     "."AFA_SUMMARY"."NOTE2" IS '��ע2';

COMMENT ON COLUMN "AFA     "."AFA_SUMMARY"."SUMNAME" IS 'ժҪ����';

COMMENT ON COLUMN "AFA     "."AFA_SUMMARY"."SUMNO" IS 'ժҪ����';

COMMENT ON COLUMN "AFA     "."AFA_SUMMARY"."SYSID" IS 'ϵͳ��ʶ';


-- DDL Statements for primary key on Table "AFA     "."AFA_SUMMARY"

ALTER TABLE "AFA     "."AFA_SUMMARY" 
	ADD CONSTRAINT "AFA_SUMMARY_KEY" PRIMARY KEY
		("SYSID");



------------------------------------------------
-- DDL Statements for table "AFA     "."AFA_SYSTEM"
------------------------------------------------
 

CREATE TABLE "AFA     "."AFA_SYSTEM"  (
		  "SYSID" VARCHAR(6) NOT NULL , 
		  "SYSENAME" VARCHAR(10) , 
		  "SYSCNAME" VARCHAR(128) NOT NULL , 
		  "WORKDATE" VARCHAR(8) , 
		  "PREWORKDATE" VARCHAR(8) , 
		  "STATUS" VARCHAR(1) NOT NULL , 
		  "TYPE" VARCHAR(1) NOT NULL , 
		  "MAXAMOUNT" VARCHAR(17) NOT NULL , 
		  "TOTALAMOUNT" VARCHAR(17) NOT NULL , 
		  "CHANNELMODE" VARCHAR(1) NOT NULL , 
		  "ACTNOMODE" VARCHAR(1) NOT NULL , 
		  "NOTE1" VARCHAR(10) , 
		  "NOTE2" VARCHAR(20) , 
		  "NOTE3" VARCHAR(30) )   
		 IN "AFA_DATA" INDEX IN "AFA_IDX" ; 

COMMENT ON COLUMN "AFA     "."AFA_SYSTEM"."ACTNOMODE" IS '���ʹ���ģʽ(0-�����п��� 1-�����п��� 2-��֧�п���)';

COMMENT ON COLUMN "AFA     "."AFA_SYSTEM"."CHANNELMODE" IS '��������ģʽ(0-�����п��� 1-�����п��� 2-��֧�п���)';

COMMENT ON COLUMN "AFA     "."AFA_SYSTEM"."MAXAMOUNT" IS '���ʽ��׶��';

COMMENT ON COLUMN "AFA     "."AFA_SYSTEM"."NOTE1" IS '��ע1';

COMMENT ON COLUMN "AFA     "."AFA_SYSTEM"."NOTE2" IS '��ע2';

COMMENT ON COLUMN "AFA     "."AFA_SYSTEM"."NOTE3" IS '��ע3';

COMMENT ON COLUMN "AFA     "."AFA_SYSTEM"."PREWORKDATE" IS 'ҵ����һ������';

COMMENT ON COLUMN "AFA     "."AFA_SYSTEM"."STATUS" IS 'ϵͳ״̬(0-�ر� 1-���� 2-��ͣ 3-δ����)';

COMMENT ON COLUMN "AFA     "."AFA_SYSTEM"."SYSCNAME" IS 'ϵͳ��������';

COMMENT ON COLUMN "AFA     "."AFA_SYSTEM"."SYSENAME" IS 'ϵͳ���';

COMMENT ON COLUMN "AFA     "."AFA_SYSTEM"."SYSID" IS 'ϵͳ��ʶ';

COMMENT ON COLUMN "AFA     "."AFA_SYSTEM"."TOTALAMOUNT" IS '���ۼƽ��׶��';

COMMENT ON COLUMN "AFA     "."AFA_SYSTEM"."TYPE" IS 'ϵͳ����(0-���� 1-���� 2-֧��)';

COMMENT ON COLUMN "AFA     "."AFA_SYSTEM"."WORKDATE" IS 'ҵ������';


-- DDL Statements for primary key on Table "AFA     "."AFA_SYSTEM"

ALTER TABLE "AFA     "."AFA_SYSTEM" 
	ADD CONSTRAINT "AFA_SYSTEM_KEY" PRIMARY KEY
		("SYSID");



------------------------------------------------
-- DDL Statements for table "AFA     "."ABDT_UNITINFO"
------------------------------------------------
 

CREATE TABLE "AFA     "."ABDT_UNITINFO"  (
		  "APPNO" VARCHAR(6) NOT NULL , 
		  "BUSINO" VARCHAR(14) NOT NULL , 
		  "AGENTTYPE" VARCHAR(1) NOT NULL , 
		  "AGENTMODE" VARCHAR(1) NOT NULL , 
		  "VOUHTYPE" VARCHAR(2) , 
		  "VOUHNO" VARCHAR(25) , 
		  "ACCNO" VARCHAR(25) , 
		  "SUBACCNO" VARCHAR(10) , 
		  "SIGNUPMODE" VARCHAR(1) NOT NULL , 
		  "GETUSERNOMODE" VARCHAR(1) , 
		  "PROTNO" VARCHAR(30) , 
		  "APPNAME" VARCHAR(60) NOT NULL , 
		  "BUSINAME" VARCHAR(60) NOT NULL , 
		  "ADDRESS" VARCHAR(60) , 
		  "TEL" VARCHAR(20) , 
		  "USERNAME" VARCHAR(20) , 
		  "WORKDATE" VARCHAR(8) NOT NULL , 
		  "BATCHNO" VARCHAR(3) , 
		  "STARTDATE" VARCHAR(8) NOT NULL , 
		  "ENDDATE" VARCHAR(8) NOT NULL , 
		  "STARTTIME" VARCHAR(6) NOT NULL , 
		  "ENDTIME" VARCHAR(6) NOT NULL , 
		  "ZONENO" VARCHAR(10) NOT NULL , 
		  "BRNO" VARCHAR(10) NOT NULL , 
		  "TELLERNO" VARCHAR(10) , 
		  "REGDATE" VARCHAR(8) , 
		  "REGTIME" VARCHAR(6) , 
		  "STATUS" VARCHAR(1) NOT NULL , 
		  "CHKDATE" VARCHAR(8) , 
		  "CHKTIME" VARCHAR(6) , 
		  "CHKFLAG" VARCHAR(1) NOT NULL , 
		  "NOTE1" VARCHAR(10) , 
		  "NOTE2" VARCHAR(20) , 
		  "NOTE3" VARCHAR(30) , 
		  "NOTE4" VARCHAR(40) , 
		  "NOTE5" VARCHAR(50) )   
		 IN "AFA_DATA" INDEX IN "AFA_IDX" ; 

COMMENT ON COLUMN "AFA     "."ABDT_UNITINFO"."ACCNO" IS '�����˻�(�Թ��˻�)';

COMMENT ON COLUMN "AFA     "."ABDT_UNITINFO"."ADDRESS" IS '��ϵ��ַ';

COMMENT ON COLUMN "AFA     "."ABDT_UNITINFO"."AGENTMODE" IS 'ί�з�Χ';

COMMENT ON COLUMN "AFA     "."ABDT_UNITINFO"."AGENTTYPE" IS 'ί�з�ʽ';

COMMENT ON COLUMN "AFA     "."ABDT_UNITINFO"."APPNAME" IS 'ҵ������';

COMMENT ON COLUMN "AFA     "."ABDT_UNITINFO"."APPNO" IS 'ҵ����:AG + ˳���(4)';

COMMENT ON COLUMN "AFA     "."ABDT_UNITINFO"."BATCHNO" IS '���κ�';

COMMENT ON COLUMN "AFA     "."ABDT_UNITINFO"."BRNO" IS '��������';

COMMENT ON COLUMN "AFA     "."ABDT_UNITINFO"."BUSINAME" IS '��λ����';

COMMENT ON COLUMN "AFA     "."ABDT_UNITINFO"."BUSINO" IS '��λ���:��������(10) + ˳���(4)';

COMMENT ON COLUMN "AFA     "."ABDT_UNITINFO"."CHKDATE" IS '��������';

COMMENT ON COLUMN "AFA     "."ABDT_UNITINFO"."CHKFLAG" IS '���ʱ�־(0-δ���� 1-�Ѷ���)';

COMMENT ON COLUMN "AFA     "."ABDT_UNITINFO"."CHKTIME" IS '����ʱ��';

COMMENT ON COLUMN "AFA     "."ABDT_UNITINFO"."ENDDATE" IS 'ʧЧ����';

COMMENT ON COLUMN "AFA     "."ABDT_UNITINFO"."ENDTIME" IS '������ֹʱ��';

COMMENT ON COLUMN "AFA     "."ABDT_UNITINFO"."GETUSERNOMODE" IS '��λ�ͻ���Ż�ȡ��ʽ(0-����, 1-��ҵ)';

COMMENT ON COLUMN "AFA     "."ABDT_UNITINFO"."NOTE1" IS '��ע1';

COMMENT ON COLUMN "AFA     "."ABDT_UNITINFO"."NOTE2" IS '��ע2';

COMMENT ON COLUMN "AFA     "."ABDT_UNITINFO"."NOTE3" IS '��ע3';

COMMENT ON COLUMN "AFA     "."ABDT_UNITINFO"."NOTE4" IS '��ע4';

COMMENT ON COLUMN "AFA     "."ABDT_UNITINFO"."NOTE5" IS '��ע5';

COMMENT ON COLUMN "AFA     "."ABDT_UNITINFO"."PROTNO" IS 'Э���';

COMMENT ON COLUMN "AFA     "."ABDT_UNITINFO"."REGDATE" IS 'ע������';

COMMENT ON COLUMN "AFA     "."ABDT_UNITINFO"."REGTIME" IS 'ע��ʱ��';

COMMENT ON COLUMN "AFA     "."ABDT_UNITINFO"."SIGNUPMODE" IS 'ǩԼ��ʽ(0-˫��, 1-����)';

COMMENT ON COLUMN "AFA     "."ABDT_UNITINFO"."STARTDATE" IS '��Ч����';

COMMENT ON COLUMN "AFA     "."ABDT_UNITINFO"."STARTTIME" IS '����ʼʱ��';

COMMENT ON COLUMN "AFA     "."ABDT_UNITINFO"."STATUS" IS '״̬(0-δ����, 1-����, 2-�ر�, 3-ͣ��)';

COMMENT ON COLUMN "AFA     "."ABDT_UNITINFO"."SUBACCNO" IS '���˻�����';

COMMENT ON COLUMN "AFA     "."ABDT_UNITINFO"."TEL" IS '��ϵ�绰';

COMMENT ON COLUMN "AFA     "."ABDT_UNITINFO"."TELLERNO" IS '��Ա����';

COMMENT ON COLUMN "AFA     "."ABDT_UNITINFO"."USERNAME" IS '��ϵ��Ա';

COMMENT ON COLUMN "AFA     "."ABDT_UNITINFO"."VOUHNO" IS 'ƾ֤����';

COMMENT ON COLUMN "AFA     "."ABDT_UNITINFO"."VOUHTYPE" IS 'ƾ֤����';

COMMENT ON COLUMN "AFA     "."ABDT_UNITINFO"."WORKDATE" IS '��������';

COMMENT ON COLUMN "AFA     "."ABDT_UNITINFO"."ZONENO" IS '��������';


-- DDL Statements for primary key on Table "AFA     "."ABDT_UNITINFO"

ALTER TABLE "AFA     "."ABDT_UNITINFO" 
	ADD CONSTRAINT "ABDT_UNITINFO_KEY" PRIMARY KEY
		("APPNO",
		 "BUSINO",
		 "ZONENO",
		 "BRNO");



------------------------------------------------
-- DDL Statements for table "AFA     "."ABDT_CUSTINFO"
------------------------------------------------
 

CREATE TABLE "AFA     "."ABDT_CUSTINFO"  (
		  "APPNO" VARCHAR(6) NOT NULL , 
		  "BUSINO" VARCHAR(14) NOT NULL , 
		  "BUSIUSERNO" VARCHAR(20) NOT NULL , 
		  "BUSIUSERAPPNO" VARCHAR(20) NOT NULL , 
		  "BANKUSERNO" VARCHAR(12) , 
		  "VOUHTYPE" VARCHAR(2) , 
		  "VOUHNO" VARCHAR(23) , 
		  "ACCNO" VARCHAR(23) NOT NULL , 
		  "SUBACCNO" VARCHAR(10) , 
		  "CURRTYPE" VARCHAR(3) , 
		  "LIMITAMT" VARCHAR(17) , 
		  "PARTFLAG" VARCHAR(1) , 
		  "PROTOCOLNO" VARCHAR(20) NOT NULL , 
		  "CONTRACTDATE" VARCHAR(8) , 
		  "STARTDATE" VARCHAR(8) , 
		  "ENDDATE" VARCHAR(8) , 
		  "PASSCHKFLAG" VARCHAR(1) , 
		  "PASSWD" VARCHAR(16) , 
		  "IDCHKFLAG" VARCHAR(1) , 
		  "IDTYPE" VARCHAR(2) , 
		  "IDCODE" VARCHAR(20) , 
		  "NAMECHKFLAG" VARCHAR(1) , 
		  "USERNAME" VARCHAR(60) , 
		  "TEL" VARCHAR(20) , 
		  "ADDRESS" VARCHAR(60) , 
		  "ZIPCODE" VARCHAR(6) , 
		  "EMAIL" VARCHAR(50) , 
		  "STATUS" VARCHAR(1) NOT NULL , 
		  "ZONENO" VARCHAR(10) NOT NULL , 
		  "BRNO" VARCHAR(10) NOT NULL , 
		  "TELLERNO" VARCHAR(10) , 
		  "INDATE" VARCHAR(8) , 
		  "INTIME" VARCHAR(6) , 
		  "NOTE1" VARCHAR(10) , 
		  "NOTE2" VARCHAR(20) , 
		  "NOTE3" VARCHAR(30) , 
		  "NOTE4" VARCHAR(40) , 
		  "NOTE5" VARCHAR(50) )   
		 IN "AFA_DATA" INDEX IN "AFA_IDX" ; 

COMMENT ON COLUMN "AFA     "."ABDT_CUSTINFO"."ACCNO" IS '���ڴ���ʺ�(������һ��ͨ��һ��ͨģʽ�����뿨��������Ļ������ʺ�)';

COMMENT ON COLUMN "AFA     "."ABDT_CUSTINFO"."ADDRESS" IS '��ϵ��ַ';

COMMENT ON COLUMN "AFA     "."ABDT_CUSTINFO"."APPNO" IS 'ҵ����(AG + ˳���(4))';

COMMENT ON COLUMN "AFA     "."ABDT_CUSTINFO"."BANKUSERNO" IS '���пͻ����';

COMMENT ON COLUMN "AFA     "."ABDT_CUSTINFO"."BRNO" IS '�����(��������)';

COMMENT ON COLUMN "AFA     "."ABDT_CUSTINFO"."BUSINO" IS '��λ���(��������(10) + ˳���(4))';

COMMENT ON COLUMN "AFA     "."ABDT_CUSTINFO"."BUSIUSERAPPNO" IS '�̻��ͻ�Ӧ�ñ��';

COMMENT ON COLUMN "AFA     "."ABDT_CUSTINFO"."BUSIUSERNO" IS '��λ�ͻ����';

COMMENT ON COLUMN "AFA     "."ABDT_CUSTINFO"."CONTRACTDATE" IS 'ǩԼ����(��ͬ����)';

COMMENT ON COLUMN "AFA     "."ABDT_CUSTINFO"."CURRTYPE" IS '����(CNY-�����)';

COMMENT ON COLUMN "AFA     "."ABDT_CUSTINFO"."EMAIL" IS '��������';

COMMENT ON COLUMN "AFA     "."ABDT_CUSTINFO"."ENDDATE" IS 'ʧЧ����';

COMMENT ON COLUMN "AFA     "."ABDT_CUSTINFO"."IDCHKFLAG" IS '֤����֤��־(0-����֤ 1-���֤)';

COMMENT ON COLUMN "AFA     "."ABDT_CUSTINFO"."IDCODE" IS '֤������(18λ�ַ�)';

COMMENT ON COLUMN "AFA     "."ABDT_CUSTINFO"."IDTYPE" IS '֤������';

COMMENT ON COLUMN "AFA     "."ABDT_CUSTINFO"."INDATE" IS '¼������';

COMMENT ON COLUMN "AFA     "."ABDT_CUSTINFO"."INTIME" IS '¼��ʱ��';

COMMENT ON COLUMN "AFA     "."ABDT_CUSTINFO"."LIMITAMT" IS '�����޶�(Ҫ�������� =0-������ >0-�������)';

COMMENT ON COLUMN "AFA     "."ABDT_CUSTINFO"."NAMECHKFLAG" IS '������֤��־(0-����֤ 1-��֤)';

COMMENT ON COLUMN "AFA     "."ABDT_CUSTINFO"."NOTE1" IS '��ע1';

COMMENT ON COLUMN "AFA     "."ABDT_CUSTINFO"."NOTE2" IS '��ע2';

COMMENT ON COLUMN "AFA     "."ABDT_CUSTINFO"."NOTE3" IS '��ע3';

COMMENT ON COLUMN "AFA     "."ABDT_CUSTINFO"."NOTE4" IS '��ע4';

COMMENT ON COLUMN "AFA     "."ABDT_CUSTINFO"."NOTE5" IS '��ע5';

COMMENT ON COLUMN "AFA     "."ABDT_CUSTINFO"."PARTFLAG" IS '���ֿۿ��־(0-���ۿ� 1-���ֿۿ�)';

COMMENT ON COLUMN "AFA     "."ABDT_CUSTINFO"."PASSCHKFLAG" IS '������֤��־(0-����֤ 1-��ѯ���� 2-��������)';

COMMENT ON COLUMN "AFA     "."ABDT_CUSTINFO"."PASSWD" IS '����(����(�ɷ�����))';

COMMENT ON COLUMN "AFA     "."ABDT_CUSTINFO"."PROTOCOLNO" IS 'Э����(�Զ�����)';

COMMENT ON COLUMN "AFA     "."ABDT_CUSTINFO"."STARTDATE" IS '��Ч����';

COMMENT ON COLUMN "AFA     "."ABDT_CUSTINFO"."STATUS" IS '״̬(0-ע�� 1-����)';

COMMENT ON COLUMN "AFA     "."ABDT_CUSTINFO"."SUBACCNO" IS '���ʺ�';

COMMENT ON COLUMN "AFA     "."ABDT_CUSTINFO"."TEL" IS '��ϵ�绰';

COMMENT ON COLUMN "AFA     "."ABDT_CUSTINFO"."TELLERNO" IS '��Ա��';

COMMENT ON COLUMN "AFA     "."ABDT_CUSTINFO"."USERNAME" IS '�ͻ�����';

COMMENT ON COLUMN "AFA     "."ABDT_CUSTINFO"."VOUHNO" IS 'ƾ֤��(19��23λ����)';

COMMENT ON COLUMN "AFA     "."ABDT_CUSTINFO"."VOUHTYPE" IS 'ƾ֤����(01-��ǿ� 02-���ڴ���)';

COMMENT ON COLUMN "AFA     "."ABDT_CUSTINFO"."ZIPCODE" IS '�ʱ�';

COMMENT ON COLUMN "AFA     "."ABDT_CUSTINFO"."ZONENO" IS '������';


-- DDL Statements for indexes on Table "AFA     "."ABDT_CUSTINFO"

CREATE UNIQUE INDEX "AFA     "."ABDT_CUSTINFO_IDX1" ON "AFA     "."ABDT_CUSTINFO" 
		("APPNO" ASC,
		 "BUSINO" ASC,
		 "ACCNO" ASC)
		ALLOW REVERSE SCANS;


-- DDL Statements for indexes on Table "AFA     "."ABDT_CUSTINFO"

CREATE UNIQUE INDEX "AFA     "."ABDT_CUSTINFO_IDX2" ON "AFA     "."ABDT_CUSTINFO" 
		("APPNO" ASC,
		 "BUSINO" ASC,
		 "BUSIUSERNO" ASC)
		ALLOW REVERSE SCANS;


-- DDL Statements for indexes on Table "AFA     "."ABDT_CUSTINFO"

CREATE UNIQUE INDEX "AFA     "."ABDT_CUSTINFO_IDX3" ON "AFA     "."ABDT_CUSTINFO" 
		("APPNO" ASC,
		 "BUSINO" ASC,
		 "BANKUSERNO" ASC)
		ALLOW REVERSE SCANS;


-- DDL Statements for primary key on Table "AFA     "."ABDT_CUSTINFO"

ALTER TABLE "AFA     "."ABDT_CUSTINFO" 
	ADD PRIMARY KEY
		("PROTOCOLNO");



------------------------------------------------
-- DDL Statements for table "AFA     "."ABDT_BATCHINFO"
------------------------------------------------
 

CREATE TABLE "AFA     "."ABDT_BATCHINFO"  (
		  "BATCHNO" VARCHAR(16) NOT NULL , 
		  "APPNO" VARCHAR(6) NOT NULL , 
		  "BUSINO" VARCHAR(14) NOT NULL , 
		  "ZONENO" VARCHAR(10) NOT NULL , 
		  "BRNO" VARCHAR(10) NOT NULL , 
		  "USERNO" VARCHAR(10) NOT NULL , 
		  "ADMINNO" VARCHAR(10) , 
		  "TERMTYPE" VARCHAR(10) , 
		  "FILENAME" VARCHAR(60) NOT NULL , 
		  "INDATE" VARCHAR(8) NOT NULL , 
		  "INTIME" VARCHAR(6) , 
		  "BATCHDATE" VARCHAR(8) , 
		  "BATCHTIME" VARCHAR(6) , 
		  "TOTALNUM" VARCHAR(10) NOT NULL , 
		  "TOTALAMT" VARCHAR(17) NOT NULL , 
		  "SUCCNUM" VARCHAR(10) NOT NULL , 
		  "SUCCAMT" VARCHAR(17) NOT NULL , 
		  "FAILNUM" VARCHAR(10) NOT NULL , 
		  "FAILAMT" VARCHAR(17) NOT NULL , 
		  "STATUS" VARCHAR(2) NOT NULL , 
		  "BEGINDATE" VARCHAR(8) NOT NULL , 
		  "ENDDATE" VARCHAR(8) NOT NULL , 
		  "PROCMSG" VARCHAR(128) , 
		  "NOTE1" VARCHAR(10) , 
		  "NOTE2" VARCHAR(20) , 
		  "NOTE3" VARCHAR(30) , 
		  "NOTE4" VARCHAR(40) , 
		  "NOTE5" VARCHAR(50) )   
		 IN "AFA_DATA" INDEX IN "AFA_IDX" ; 

COMMENT ON COLUMN "AFA     "."ABDT_BATCHINFO"."ADMINNO" IS '����Ա';

COMMENT ON COLUMN "AFA     "."ABDT_BATCHINFO"."APPNO" IS 'ҵ����(AG + ˳���(4))';

COMMENT ON COLUMN "AFA     "."ABDT_BATCHINFO"."BATCHDATE" IS '�ύ����';

COMMENT ON COLUMN "AFA     "."ABDT_BATCHINFO"."BATCHNO" IS 'ί�к�(���κ�)(Ψһ(����+��ˮ��))';

COMMENT ON COLUMN "AFA     "."ABDT_BATCHINFO"."BATCHTIME" IS '�ύʱ��';

COMMENT ON COLUMN "AFA     "."ABDT_BATCHINFO"."BEGINDATE" IS '��Ч����';

COMMENT ON COLUMN "AFA     "."ABDT_BATCHINFO"."BRNO" IS '�����(��������)';

COMMENT ON COLUMN "AFA     "."ABDT_BATCHINFO"."BUSINO" IS '��λ���(��������(10) + ˳���(4))';

COMMENT ON COLUMN "AFA     "."ABDT_BATCHINFO"."ENDDATE" IS 'ʧЧ����';

COMMENT ON COLUMN "AFA     "."ABDT_BATCHINFO"."FAILAMT" IS 'ʧ�ܽ��';

COMMENT ON COLUMN "AFA     "."ABDT_BATCHINFO"."FAILNUM" IS 'ʧ�ܱ���';

COMMENT ON COLUMN "AFA     "."ABDT_BATCHINFO"."FILENAME" IS '�ϴ��ļ���(ҵ����+��λ���+����.TXT)';

COMMENT ON COLUMN "AFA     "."ABDT_BATCHINFO"."INDATE" IS '��������';

COMMENT ON COLUMN "AFA     "."ABDT_BATCHINFO"."INTIME" IS '����ʱ��';

COMMENT ON COLUMN "AFA     "."ABDT_BATCHINFO"."NOTE1" IS '��ע1';

COMMENT ON COLUMN "AFA     "."ABDT_BATCHINFO"."NOTE2" IS '��ע2';

COMMENT ON COLUMN "AFA     "."ABDT_BATCHINFO"."NOTE3" IS '��ע3';

COMMENT ON COLUMN "AFA     "."ABDT_BATCHINFO"."NOTE4" IS '��ע4';

COMMENT ON COLUMN "AFA     "."ABDT_BATCHINFO"."NOTE5" IS '��ע5';

COMMENT ON COLUMN "AFA     "."ABDT_BATCHINFO"."PROCMSG" IS '������Ϣ';

COMMENT ON COLUMN "AFA     "."ABDT_BATCHINFO"."STATUS" IS '״̬(00-�ϴ� 10-���� 11-������(����������) 20-���ύ 21-���ڴ����ύ�ļ� 22-���ύ(���ڴ���) 30-����� 31-���ڴ�������ļ� 32-����� 88-�������(�����ļ���ҵ�񱨱�) 40-����)';

COMMENT ON COLUMN "AFA     "."ABDT_BATCHINFO"."SUCCAMT" IS '�ɹ����';

COMMENT ON COLUMN "AFA     "."ABDT_BATCHINFO"."SUCCNUM" IS '�ɹ�����';

COMMENT ON COLUMN "AFA     "."ABDT_BATCHINFO"."TERMTYPE" IS '�ն�����';

COMMENT ON COLUMN "AFA     "."ABDT_BATCHINFO"."TOTALAMT" IS '�ܽ��';

COMMENT ON COLUMN "AFA     "."ABDT_BATCHINFO"."TOTALNUM" IS '�ܱ���';

COMMENT ON COLUMN "AFA     "."ABDT_BATCHINFO"."USERNO" IS '����Ա';

COMMENT ON COLUMN "AFA     "."ABDT_BATCHINFO"."ZONENO" IS '������';


-- DDL Statements for indexes on Table "AFA     "."ABDT_BATCHINFO"

CREATE UNIQUE INDEX "AFA     "."ABDT_BATCHINFO_IDX1" ON "AFA     "."ABDT_BATCHINFO" 
		("APPNO" ASC,
		 "BUSINO" ASC,
		 "ZONENO" ASC,
		 "BRNO" ASC,
		 "INDATE" ASC,
		 "FILENAME" ASC)
		ALLOW REVERSE SCANS;


-- DDL Statements for primary key on Table "AFA     "."ABDT_BATCHINFO"

ALTER TABLE "AFA     "."ABDT_BATCHINFO" 
	ADD PRIMARY KEY
		("BATCHNO");



------------------------------------------------
-- DDL Statements for table "AFA     "."ABDT_LOGINFO"
------------------------------------------------
 

CREATE TABLE "AFA     "."ABDT_LOGINFO"  (
		  "ZONENO" VARCHAR(10) NOT NULL , 
		  "BRNO" VARCHAR(10) NOT NULL , 
		  "TELLERNO" VARCHAR(10) NOT NULL , 
		  "TERMID" VARCHAR(20) , 
		  "WORKDATE" VARCHAR(8) NOT NULL , 
		  "WORKTIME" VARCHAR(6) NOT NULL , 
		  "BATCHNO" VARCHAR(16) NOT NULL , 
		  "TASKTYPE" VARCHAR(2) NOT NULL , 
		  "TASKSTATUS" VARCHAR(2) NOT NULL , 
		  "TASKMSG" VARCHAR(128) , 
		  "NOTE1" VARCHAR(10) , 
		  "NOTE2" VARCHAR(20) )   
		 IN "AFA_DATA" INDEX IN "AFA_IDX" ; 

COMMENT ON COLUMN "AFA     "."ABDT_LOGINFO"."BATCHNO" IS 'ί�к�(���κ�)';

COMMENT ON COLUMN "AFA     "."ABDT_LOGINFO"."BRNO" IS '�����(��������)';

COMMENT ON COLUMN "AFA     "."ABDT_LOGINFO"."NOTE1" IS '��ע1';

COMMENT ON COLUMN "AFA     "."ABDT_LOGINFO"."NOTE2" IS '��ע2';

COMMENT ON COLUMN "AFA     "."ABDT_LOGINFO"."TASKMSG" IS '����������';

COMMENT ON COLUMN "AFA     "."ABDT_LOGINFO"."TASKSTATUS" IS '����״̬(0-�ɹ� 1-ʧ��2-�쳣)';

COMMENT ON COLUMN "AFA     "."ABDT_LOGINFO"."TASKTYPE" IS '��������(״̬(00-�ϴ� 10-���� 11-������(����������) 20-���ύ 21-���ڴ����ύ�ļ� 22-���ύ(���ڴ���) 30-����� 31-���ڴ�������ļ� 32-����� 88-�������(�����ļ���ҵ�񱨱�) 40-����))';

COMMENT ON COLUMN "AFA     "."ABDT_LOGINFO"."TELLERNO" IS '����Ա';

COMMENT ON COLUMN "AFA     "."ABDT_LOGINFO"."TERMID" IS '�ն˺�';

COMMENT ON COLUMN "AFA     "."ABDT_LOGINFO"."WORKDATE" IS '����';

COMMENT ON COLUMN "AFA     "."ABDT_LOGINFO"."WORKTIME" IS 'ʱ��';

COMMENT ON COLUMN "AFA     "."ABDT_LOGINFO"."ZONENO" IS '������';


-- DDL Statements for indexes on Table "AFA     "."ABDT_LOGINFO"

CREATE INDEX "AFA     "."ABDT_LOGINFO_IDX1" ON "AFA     "."ABDT_LOGINFO" 
		("WORKDATE" ASC,
		 "ZONENO" ASC,
		 "BRNO" ASC,
		 "TELLERNO" ASC)
		ALLOW REVERSE SCANS;






------------------------------------------------
-- DDL Statements for table "AFA     "."RCC_ATRCHK"
------------------------------------------------
 

CREATE TABLE "AFA     "."RCC_ATRCHK"  (
		  "SNDBNKCO" VARCHAR(10) NOT NULL , 
		  "TRCDAT" VARCHAR(8) NOT NULL , 
		  "TRCNO" VARCHAR(8) NOT NULL , 
		  "ROPRTPNO" VARCHAR(2) , 
		  "TRCCO" VARCHAR(7) , 
		  "RCVBNKCO" VARCHAR(10) , 
		  "CUR" VARCHAR(3) , 
		  "RDTCNT" DECIMAL(10,0) , 
		  "RDTAMT" DECIMAL(15,2) , 
		  "RCTCNT" DECIMAL(10,0) , 
		  "RCTAMT" DECIMAL(15,2) , 
		  "SDTCNT" DECIMAL(10,0) , 
		  "SDTAMT" DECIMAL(15,2) , 
		  "SCTCNT" DECIMAL(10,0) , 
		  "SCTAMT" DECIMAL(15,2) , 
		  "NOTE1" VARCHAR(10) , 
		  "NOTE2" VARCHAR(20) , 
		  "NOTE3" VARCHAR(60) , 
		  "NOTE4" VARCHAR(60) )   
		 IN "AFA_DATA" INDEX IN "AFA_IDX" ; 


-- DDL Statements for primary key on Table "AFA     "."RCC_ATRCHK"

ALTER TABLE "AFA     "."RCC_ATRCHK" 
	ADD CONSTRAINT "RCC_ATRCHK_PK" PRIMARY KEY
		("SNDBNKCO",
		 "TRCDAT",
		 "TRCNO");



------------------------------------------------
-- DDL Statements for table "AFA     "."RCC_CADBNK"
------------------------------------------------
 

CREATE TABLE "AFA     "."RCC_CADBNK"  (
		  "CARDBIN" VARCHAR(8) NOT NULL , 
		  "BANKBIN" VARCHAR(10) NOT NULL , 
		  "NOTE1" VARCHAR(10) , 
		  "NOTE2" VARCHAR(20) , 
		  "NOTE3" VARCHAR(60) , 
		  "NOTE4" VARCHAR(60) )   
		 IN "AFA_DATA" INDEX IN "AFA_IDX" ; 


-- DDL Statements for primary key on Table "AFA     "."RCC_CADBNK"

ALTER TABLE "AFA     "."RCC_CADBNK" 
	ADD CONSTRAINT "RCC_CADBNK_PK" PRIMARY KEY
		("CARDBIN");



------------------------------------------------
-- DDL Statements for table "AFA     "."RCC_CSHALM"
------------------------------------------------
 

CREATE TABLE "AFA     "."RCC_CSHALM"  (
		  "BJEDTE" VARCHAR(8) NOT NULL , 
		  "BSPSQN" VARCHAR(12) NOT NULL , 
		  "NCCWKDAT" VARCHAR(8) , 
		  "TRCCO" VARCHAR(7) , 
		  "TRCDAT" VARCHAR(8) , 
		  "TRCNO" VARCHAR(8) , 
		  "SNDBNKCO" VARCHAR(10) , 
		  "SNDBNKNM" VARCHAR(60) , 
		  "RCVBNKCO" VARCHAR(10) , 
		  "RCVBNKNM" VARCHAR(60) , 
		  "CUR" VARCHAR(3) , 
		  "POSITION" DECIMAL(15,2) , 
		  "POSALAMT" DECIMAL(15,2) , 
		  "NOTE1" VARCHAR(10) , 
		  "NOTE2" VARCHAR(20) , 
		  "NOTE3" VARCHAR(60) , 
		  "NOTE4" VARCHAR(60) )   
		 IN "AFA_DATA" INDEX IN "AFA_IDX" ; 


-- DDL Statements for primary key on Table "AFA     "."RCC_CSHALM"

ALTER TABLE "AFA     "."RCC_CSHALM" 
	ADD CONSTRAINT "RCC_CSHALM_PK" PRIMARY KEY
		("BJEDTE",
		 "BSPSQN");



------------------------------------------------
-- DDL Statements for table "AFA     "."RCC_ERRINF"
------------------------------------------------
 

CREATE TABLE "AFA     "."RCC_ERRINF"  (
		  "MBRTYP" VARCHAR(1) NOT NULL , 
		  "ERRKEY" VARCHAR(8) NOT NULL , 
		  "ERRSTR" VARCHAR(255) , 
		  "NOTE1" VARCHAR(10) , 
		  "NOTE2" VARCHAR(20) , 
		  "NOTE3" VARCHAR(60) , 
		  "NOTE4" VARCHAR(60) )   
		 IN "AFA_DATA" INDEX IN "AFA_IDX" ; 


-- DDL Statements for primary key on Table "AFA     "."RCC_ERRINF"

ALTER TABLE "AFA     "."RCC_ERRINF" 
	ADD CONSTRAINT "RCC_ERRINF_PK" PRIMARY KEY
		("MBRTYP",
		 "ERRKEY");



------------------------------------------------
-- DDL Statements for table "AFA     "."RCC_HDDZCZ"
------------------------------------------------
 

CREATE TABLE "AFA     "."RCC_HDDZCZ"  (
		  "SNDBNKCO" VARCHAR(10) NOT NULL , 
		  "TRCDAT" VARCHAR(8) NOT NULL , 
		  "TRCNO" VARCHAR(8) NOT NULL , 
		  "NCCWKDAT" VARCHAR(8) , 
		  "BJEDTE" VARCHAR(8) , 
		  "BSPSQN" VARCHAR(12) , 
		  "EACTYP" VARCHAR(1) , 
		  "EACINF" VARCHAR(60) , 
		  "ISDEAL" VARCHAR(1) , 
		  "NOTE1" VARCHAR(10) , 
		  "NOTE2" VARCHAR(20) , 
		  "NOTE3" VARCHAR(60) , 
		  "NOTE4" VARCHAR(60) )   
		 IN "AFA_DATA" INDEX IN "AFA_IDX" ; 


-- DDL Statements for primary key on Table "AFA     "."RCC_HDDZCZ"

ALTER TABLE "AFA     "."RCC_HDDZCZ" 
	ADD CONSTRAINT "RCC_HDDZCZ_PK" PRIMARY KEY
		("SNDBNKCO",
		 "TRCDAT",
		 "TRCNO");



------------------------------------------------
-- DDL Statements for table "AFA     "."RCC_HDDZHZ"
------------------------------------------------
 

CREATE TABLE "AFA     "."RCC_HDDZHZ"  (
		  "NCCWKDAT" VARCHAR(8) NOT NULL , 
		  "TRCCO" VARCHAR(7) NOT NULL , 
		  "BRSFLG" VARCHAR(1) NOT NULL , 
		  "TRCNAM" VARCHAR(60) , 
		  "TRCRSNM" VARCHAR(60) , 
		  "TCNT" SMALLINT NOT NULL , 
		  "CTAMT" DECIMAL(16,2) , 
		  "DTAMT" DECIMAL(16,2) , 
		  "OFSTAMT" DECIMAL(16,2) , 
		  "NOTE1" VARCHAR(10) , 
		  "NOTE2" VARCHAR(20) , 
		  "NOTE3" VARCHAR(60) , 
		  "NOTE4" VARCHAR(60) )   
		 IN "AFA_DATA" INDEX IN "AFA_IDX" ; 


-- DDL Statements for primary key on Table "AFA     "."RCC_HDDZHZ"

ALTER TABLE "AFA     "."RCC_HDDZHZ" 
	ADD CONSTRAINT "RCC_HDDZHZ_PK" PRIMARY KEY
		("NCCWKDAT",
		 "TRCCO",
		 "BRSFLG");



------------------------------------------------
-- DDL Statements for table "AFA     "."RCC_HDDZMX"
------------------------------------------------
 

CREATE TABLE "AFA     "."RCC_HDDZMX"  (
		  "SNDBNKCO" VARCHAR(10) NOT NULL , 
		  "TRCDAT" VARCHAR(8) NOT NULL , 
		  "TRCNO" VARCHAR(8) NOT NULL , 
		  "NCCWKDAT" VARCHAR(8) , 
		  "MSGTYPCO" VARCHAR(6) , 
		  "RCVMBRCO" VARCHAR(10) , 
		  "SNDMBRCO" VARCHAR(10) , 
		  "TRCCO" VARCHAR(7) , 
		  "SNDBRHCO" VARCHAR(6) , 
		  "SNDCLKNO" VARCHAR(8) , 
		  "SNDTRDAT" VARCHAR(8) , 
		  "SNDTRTIM" VARCHAR(6) , 
		  "MSGFLGNO" VARCHAR(26) , 
		  "ORMFN" VARCHAR(26) , 
		  "OPRTYPNO" VARCHAR(2) , 
		  "ROPRTPNO" VARCHAR(2) , 
		  "OPRSTNO" VARCHAR(3) , 
		  "SNDBNKNM" VARCHAR(60) , 
		  "RCVBNKCO" VARCHAR(10) , 
		  "RCVBNKNM" VARCHAR(60) , 
		  "CUR" VARCHAR(3) , 
		  "OCCAMT" DECIMAL(15,2) , 
		  "PYRACC" VARCHAR(32) , 
		  "PYRNAM" VARCHAR(60) , 
		  "PYRADDR" VARCHAR(60) , 
		  "PYEACC" VARCHAR(32) , 
		  "PYENAM" VARCHAR(60) , 
		  "PYEADDR" VARCHAR(60) , 
		  "OPRATTNO" VARCHAR(2) , 
		  "SEAL" VARCHAR(10) , 
		  "ORTRCCO" VARCHAR(7) , 
		  "ORSNDBNK" VARCHAR(10) , 
		  "ORRCVBNK" VARCHAR(10) , 
		  "ORTRCDAT" VARCHAR(8) , 
		  "ORTRCNO" VARCHAR(8) , 
		  "REMARK" VARCHAR(30) , 
		  "BILDAT" VARCHAR(8) , 
		  "BILNO" VARCHAR(8) , 
		  "BILTYP" VARCHAR(2) , 
		  "CPSAMT" DECIMAL(16,2) , 
		  "RFUAMT" DECIMAL(16,2) , 
		  "STRINFO" VARCHAR(60) , 
		  "USE" VARCHAR(20) , 
		  "BJEDTE" VARCHAR(8) , 
		  "BSPSQN" VARCHAR(12) , 
		  "BCSTAT" VARCHAR(2) , 
		  "BDWFLG" VARCHAR(1) , 
		  "EACTYP" VARCHAR(1) , 
		  "NOTE1" VARCHAR(10) , 
		  "NOTE2" VARCHAR(20) , 
		  "NOTE3" VARCHAR(60) , 
		  "NOTE4" VARCHAR(60) )   
		 IN "AFA_DATA" INDEX IN "AFA_IDX" ; 


-- DDL Statements for primary key on Table "AFA     "."RCC_HDDZMX"

ALTER TABLE "AFA     "."RCC_HDDZMX" 
	ADD CONSTRAINT "RCC_HDDZMX_PK" PRIMARY KEY
		("SNDBNKCO",
		 "TRCDAT",
		 "TRCNO");



------------------------------------------------
-- DDL Statements for table "AFA     "."RCC_HPDZCZ"
------------------------------------------------
 

CREATE TABLE "AFA     "."RCC_HPDZCZ"  (
		  "SNDBNKCO" VARCHAR(10) NOT NULL , 
		  "TRCDAT" VARCHAR(8) NOT NULL , 
		  "TRCNO" VARCHAR(8) NOT NULL , 
		  "NCCWKDAT" VARCHAR(8) , 
		  "BJEDTE" VARCHAR(8) , 
		  "BSPSQN" VARCHAR(12) , 
		  "EACTYP" VARCHAR(1) , 
		  "EACINF" VARCHAR(60) , 
		  "ISDEAL" VARCHAR(1) , 
		  "NOTE1" VARCHAR(10) , 
		  "NOTE2" VARCHAR(20) , 
		  "NOTE3" VARCHAR(60) , 
		  "NOTE4" VARCHAR(60) )   
		 IN "AFA_DATA" INDEX IN "AFA_IDX" ; 


-- DDL Statements for primary key on Table "AFA     "."RCC_HPDZCZ"

ALTER TABLE "AFA     "."RCC_HPDZCZ" 
	ADD CONSTRAINT "RCC_HPDZCZ_PK" PRIMARY KEY
		("SNDBNKCO",
		 "TRCDAT",
		 "TRCNO");



------------------------------------------------
-- DDL Statements for table "AFA     "."RCC_HPDZHZ"
------------------------------------------------
 

CREATE TABLE "AFA     "."RCC_HPDZHZ"  (
		  "NCCWKDAT" VARCHAR(8) NOT NULL , 
		  "TRCCO" VARCHAR(7) NOT NULL , 
		  "BRSFLG" VARCHAR(1) NOT NULL , 
		  "TRCNAM" VARCHAR(60) , 
		  "TRCRSNM" VARCHAR(60) , 
		  "TCNT" SMALLINT NOT NULL , 
		  "CTAMT" DECIMAL(16,2) , 
		  "DTAMT" DECIMAL(16,2) , 
		  "OFSTAMT" DECIMAL(16,2) , 
		  "CLAMT" DECIMAL(16,2) , 
		  "DLAMT" DECIMAL(16,2) , 
		  "OFSLAMT" DECIMAL(16,2) , 
		  "NOTE1" VARCHAR(10) , 
		  "NOTE2" VARCHAR(20) , 
		  "NOTE3" VARCHAR(60) , 
		  "NOTE4" VARCHAR(60) )   
		 IN "AFA_DATA" INDEX IN "AFA_IDX" ; 


-- DDL Statements for primary key on Table "AFA     "."RCC_HPDZHZ"

ALTER TABLE "AFA     "."RCC_HPDZHZ" 
	ADD CONSTRAINT "RCC_HPDZHZ_PK" PRIMARY KEY
		("NCCWKDAT",
		 "TRCCO",
		 "BRSFLG");



------------------------------------------------
-- DDL Statements for table "AFA     "."RCC_HPDZMX"
------------------------------------------------
 

CREATE TABLE "AFA     "."RCC_HPDZMX"  (
		  "SNDBNKCO" VARCHAR(10) NOT NULL , 
		  "TRCDAT" VARCHAR(8) NOT NULL , 
		  "TRCNO" VARCHAR(8) NOT NULL , 
		  "NCCWKDAT" VARCHAR(8) , 
		  "MSGTYPCO" VARCHAR(6) , 
		  "RCVMBRCO" VARCHAR(10) , 
		  "SNDMBRCO" VARCHAR(10) , 
		  "TRCCO" VARCHAR(7) , 
		  "SNDBRHCO" VARCHAR(6) , 
		  "SNDCLKNO" VARCHAR(8) , 
		  "SNDTRDAT" VARCHAR(8) , 
		  "SNDTRTIM" VARCHAR(6) , 
		  "MSGFLGNO" VARCHAR(26) , 
		  "ORMFN" VARCHAR(26) , 
		  "OPRTYPNO" VARCHAR(2) , 
		  "ROPRTPNO" VARCHAR(2) , 
		  "SNDBNKNM" VARCHAR(60) , 
		  "RCVBNKCO" VARCHAR(10) , 
		  "RCVBNKNM" VARCHAR(60) , 
		  "CUR" VARCHAR(3) , 
		  "OCCAMT" DECIMAL(15,2) , 
		  "PYRACC" VARCHAR(32) , 
		  "PYRNAM" VARCHAR(60) , 
		  "PYRADDR" VARCHAR(60) , 
		  "PYEACC" VARCHAR(32) , 
		  "PYENAM" VARCHAR(60) , 
		  "PYEADDR" VARCHAR(60) , 
		  "OPRATTNO" VARCHAR(2) , 
		  "SEAL" VARCHAR(10) , 
		  "BILDAT" VARCHAR(8) , 
		  "BILNO" VARCHAR(8) , 
		  "BILVER" VARCHAR(2) , 
		  "PAYWAY" VARCHAR(1) , 
		  "BILAMT" DECIMAL(15,2) , 
		  "RMNAMT" DECIMAL(15,2) , 
		  "USE" VARCHAR(20) , 
		  "REMARK" VARCHAR(30) , 
		  "BJEDTE" VARCHAR(8) , 
		  "BSPSQN" VARCHAR(12) , 
		  "BCSTAT" VARCHAR(2) , 
		  "BDWFLG" VARCHAR(1) , 
		  "EACTYP" VARCHAR(1) , 
		  "NOTE1" VARCHAR(10) , 
		  "NOTE2" VARCHAR(20) , 
		  "NOTE3" VARCHAR(60) , 
		  "NOTE4" VARCHAR(60) )   
		 IN "AFA_DATA" INDEX IN "AFA_IDX" ; 


-- DDL Statements for primary key on Table "AFA     "."RCC_HPDZMX"

ALTER TABLE "AFA     "."RCC_HPDZMX" 
	ADD CONSTRAINT "RCC_HPDZMX_PK" PRIMARY KEY
		("SNDBNKCO",
		 "TRCDAT",
		 "TRCNO");



------------------------------------------------
-- DDL Statements for table "AFA     "."RCC_INSBKA"
------------------------------------------------
 

CREATE TABLE "AFA     "."RCC_INSBKA"  (
		  "BJEDTE" VARCHAR(8) NOT NULL , 
		  "BSPSQN" VARCHAR(12) NOT NULL , 
		  "NCCWKDAT" VARCHAR(8) , 
		  "TRDT" VARCHAR(8) , 
		  "TLSQ" VARCHAR(10) , 
		  "SBAC" VARCHAR(32) , 
		  "RBAC" VARCHAR(32) , 
		  "DASQ" VARCHAR(8) , 
		  "MGID" VARCHAR(7) , 
		  "BDWFLG" VARCHAR(1) , 
		  "NOTE1" VARCHAR(10) , 
		  "NOTE2" VARCHAR(20) , 
		  "NOTE3" VARCHAR(60) , 
		  "NOTE4" VARCHAR(60) )   
		 IN "AFA_DATA" INDEX IN "AFA_IDX" ; 


-- DDL Statements for primary key on Table "AFA     "."RCC_INSBKA"

ALTER TABLE "AFA     "."RCC_INSBKA" 
	ADD CONSTRAINT "RCC_INSBKA_PK" PRIMARY KEY
		("BJEDTE",
		 "BSPSQN");



------------------------------------------------
-- DDL Statements for table "AFA     "."RCC_MBRIFA"
------------------------------------------------
 

CREATE TABLE "AFA     "."RCC_MBRIFA"  (
		  "OPRTYPNO" VARCHAR(2) NOT NULL , 
		  "ORWKDAT" VARCHAR(8) NOT NULL , 
		  "ORSYSST" VARCHAR(2) NOT NULL , 
		  "NWWKDAT" VARCHAR(8) NOT NULL , 
		  "NWSYSST" VARCHAR(2) NOT NULL , 
		  "HOLFLG" VARCHAR(1) NOT NULL , 
		  "STRINFO" VARCHAR(60) , 
		  "NOTE1" VARCHAR(10) , 
		  "NOTE2" VARCHAR(20) , 
		  "NOTE3" VARCHAR(60) , 
		  "NOTE4" VARCHAR(60) )   
		 IN "AFA_DATA" INDEX IN "AFA_IDX" ; 


-- DDL Statements for primary key on Table "AFA     "."RCC_MBRIFA"

ALTER TABLE "AFA     "."RCC_MBRIFA" 
	ADD CONSTRAINT "RCC_MBRIFA_PK" PRIMARY KEY
		("OPRTYPNO");



------------------------------------------------
-- DDL Statements for table "AFA     "."RCC_PAMTBL"
------------------------------------------------
 

CREATE TABLE "AFA     "."RCC_PAMTBL"  (
		  "BPATPE" VARCHAR(1) NOT NULL , 
		  "BPARAD" VARCHAR(18) NOT NULL , 
		  "BPACMT" VARCHAR(60) , 
		  "BPADAT" VARCHAR(255) , 
		  "BPAINF" VARCHAR(60) , 
		  "BEFTDT" VARCHAR(8) , 
		  "BINVDT" VARCHAR(8) , 
		  "NOTE1" VARCHAR(10) , 
		  "NOTE2" VARCHAR(20) , 
		  "NOTE3" VARCHAR(60) , 
		  "NOTE4" VARCHAR(60) )   
		 IN "AFA_DATA" INDEX IN "AFA_IDX" ; 


-- DDL Statements for primary key on Table "AFA     "."RCC_PAMTBL"

ALTER TABLE "AFA     "."RCC_PAMTBL" 
	ADD CONSTRAINT "RCC_PAMTBL_PK" PRIMARY KEY
		("BPATPE",
		 "BPARAD");



------------------------------------------------
-- DDL Statements for table "AFA     "."RCC_QSQHQD"
------------------------------------------------
 

CREATE TABLE "AFA     "."RCC_QSQHQD"  (
		  "STRDAT" VARCHAR(8) NOT NULL , 
		  "ENDDAT" VARCHAR(8) NOT NULL , 
		  "BESBNO" VARCHAR(10) NOT NULL , 
		  "BESBNM" VARCHAR(60) , 
		  "TRCCHRGCNT" SMALLINT NOT NULL , 
		  "TRCCHRGAMT" DECIMAL(15,2) , 
		  "BILCHRGCNT" SMALLINT NOT NULL , 
		  "BILCHRGAMT" DECIMAL(15,2) , 
		  "UCSWCHRGCNT" SMALLINT NOT NULL , 
		  "UCSWCHRGAMT" DECIMAL(15,2) , 
		  "TCNT" SMALLINT NOT NULL , 
		  "TAMT" DECIMAL(15,2) , 
		  "ISDEAL" VARCHAR(1) , 
		  "FEDT" VARCHAR(8) , 
		  "RBSQ" VARCHAR(12) , 
		  "TRDT" VARCHAR(8) , 
		  "TLSQ" VARCHAR(10) , 
		  "MGID" VARCHAR(7) , 
		  "NOTE1" VARCHAR(20) , 
		  "NOTE2" VARCHAR(20) , 
		  "NOTE3" VARCHAR(60) , 
		  "NOTE4" VARCHAR(60) )   
		 IN "AFA_DATA" INDEX IN "AFA_IDX" ; 


-- DDL Statements for primary key on Table "AFA     "."RCC_QSQHQD"

ALTER TABLE "AFA     "."RCC_QSQHQD" 
	ADD CONSTRAINT "RCC_QSQHQD_PK" PRIMARY KEY
		("STRDAT",
		 "ENDDAT",
		 "BESBNO");



------------------------------------------------
-- DDL Statements for table "AFA     "."RCC_REKBAL"
------------------------------------------------
 

CREATE TABLE "AFA     "."RCC_REKBAL"  (
		  "BJEDTE" VARCHAR(8) NOT NULL , 
		  "BSPSQN" VARCHAR(12) NOT NULL , 
		  "BOJEDT" VARCHAR(8) , 
		  "BOSPSQ" VARCHAR(12) , 
		  "NCCWKDAT" VARCHAR(8) , 
		  "TRCDAT" VARCHAR(8) NOT NULL , 
		  "TRCNO" VARCHAR(8) NOT NULL , 
		  "SNDBNKCO" VARCHAR(10) NOT NULL , 
		  "TRCCO" VARCHAR(7) , 
		  "RCVBNKCO" VARCHAR(10) , 
		  "CUR" VARCHAR(3) , 
		  "LBDCFLG" VARCHAR(1) , 
		  "LSTDTBAL" DECIMAL(15,2) , 
		  "NTTDCFLG" VARCHAR(1) , 
		  "NTTBAL" DECIMAL(15,2) , 
		  "BALDCFLG" VARCHAR(1) , 
		  "TODAYBAL" DECIMAL(15,2) , 
		  "AVLBAL" DECIMAL(15,2) , 
		  "NTODAYBAL" DECIMAL(15,2) , 
		  "CHKRST" VARCHAR(1) , 
		  "NOTE1" VARCHAR(10) , 
		  "NOTE2" VARCHAR(20) , 
		  "NOTE3" VARCHAR(60) , 
		  "NOTE4" VARCHAR(60) )   
		 IN "AFA_DATA" INDEX IN "AFA_IDX" ; 


-- DDL Statements for indexes on Table "AFA     "."RCC_REKBAL"

CREATE UNIQUE INDEX "AFA     "."RCC_REKBAL_IDX1" ON "AFA     "."RCC_REKBAL" 
		("TRCDAT" ASC,
		 "TRCNO" ASC,
		 "SNDBNKCO" ASC)
		ALLOW REVERSE SCANS;


-- DDL Statements for primary key on Table "AFA     "."RCC_REKBAL"

ALTER TABLE "AFA     "."RCC_REKBAL" 
	ADD CONSTRAINT "RCC_REKBAL_PK" PRIMARY KEY
		("BJEDTE",
		 "BSPSQN");



------------------------------------------------
-- DDL Statements for table "AFA     "."RCC_SPBSTA"
------------------------------------------------
 

CREATE TABLE "AFA     "."RCC_SPBSTA"  (
		  "BJEDTE" VARCHAR(8) NOT NULL , 
		  "BSPSQN" VARCHAR(12) NOT NULL , 
		  "BCURSQ" SMALLINT NOT NULL , 
		  "BCSTAT" VARCHAR(2) , 
		  "BDWFLG" VARCHAR(1) , 
		  "NOTE1" VARCHAR(10) , 
		  "NOTE2" VARCHAR(20) , 
		  "NOTE3" VARCHAR(60) , 
		  "NOTE4" VARCHAR(60) )   
		 IN "AFA_DATA" INDEX IN "AFA_IDX" ; 


-- DDL Statements for primary key on Table "AFA     "."RCC_SPBSTA"

ALTER TABLE "AFA     "."RCC_SPBSTA" 
	ADD CONSTRAINT "RCC_SPBSTA_PK" PRIMARY KEY
		("BJEDTE",
		 "BSPSQN");



------------------------------------------------
-- DDL Statements for table "AFA     "."RCC_SUBBRA"
------------------------------------------------
 

CREATE TABLE "AFA     "."RCC_SUBBRA"  (
		  "BESBNO" VARCHAR(10) NOT NULL , 
		  "BESBNM" VARCHAR(60) , 
		  "BESBTP" VARCHAR(2) , 
		  "BTOPSB" VARCHAR(10) , 
		  "BEACSB" VARCHAR(10) , 
		  "BANKBIN" VARCHAR(10) , 
		  "SUBFLG" VARCHAR(1) , 
		  "STRINFO" VARCHAR(60) , 
		  "NOTE1" VARCHAR(10) , 
		  "NOTE2" VARCHAR(20) , 
		  "NOTE3" VARCHAR(60) , 
		  "NOTE4" VARCHAR(60) )   
		 IN "AFA_DATA" INDEX IN "AFA_IDX" ; 


-- DDL Statements for primary key on Table "AFA     "."RCC_SUBBRA"

ALTER TABLE "AFA     "."RCC_SUBBRA" 
	ADD CONSTRAINT "RCC_SUBBRA_PK" PRIMARY KEY
		("BESBNO");



------------------------------------------------
-- DDL Statements for table "AFA     "."RCC_TRCSTA"
------------------------------------------------
 

CREATE TABLE "AFA     "."RCC_TRCSTA"  (
		  "NCCWKDAT" VARCHAR(8) NOT NULL , 
		  "BESBNO" VARCHAR(10) NOT NULL , 
		  "TRCCO" VARCHAR(7) NOT NULL , 
		  "BRSFLG" VARCHAR(1) NOT NULL , 
		  "BTOPSB" VARCHAR(10) , 
		  "BEACSB" VARCHAR(10) , 
		  "TCNT" SMALLINT NOT NULL , 
		  "TAMT" DECIMAL(15,2) , 
		  "ISDEAL" VARCHAR(1) , 
		  "STRINFO" VARCHAR(60) , 
		  "NOTE1" VARCHAR(10) , 
		  "NOTE2" VARCHAR(20) , 
		  "NOTE3" VARCHAR(60) , 
		  "NOTE4" VARCHAR(60) )   
		 IN "AFA_DATA" INDEX IN "AFA_IDX" ; 


-- DDL Statements for primary key on Table "AFA     "."RCC_TRCSTA"

ALTER TABLE "AFA     "."RCC_TRCSTA" 
	ADD CONSTRAINT "RCC_TRCSTA_PK" PRIMARY KEY
		("NCCWKDAT",
		 "BESBNO",
		 "TRCCO",
		 "BRSFLG");



------------------------------------------------
-- DDL Statements for table "AFA     "."RCC_SSTLOG"
------------------------------------------------
 

CREATE TABLE "AFA     "."RCC_SSTLOG"  (
		  "BJEDTE" VARCHAR(8) NOT NULL , 
		  "BSPSQN" VARCHAR(12) NOT NULL , 
		  "BCURSQ" SMALLINT NOT NULL , 
		  "BESBNO" VARCHAR(10) , 
		  "BEACSB" VARCHAR(10) , 
		  "BETELR" VARCHAR(6) , 
		  "BEAUUS" VARCHAR(6) , 
		  "FEDT" VARCHAR(8) , 
		  "RBSQ" VARCHAR(12) , 
		  "TRDT" VARCHAR(8) , 
		  "TLSQ" VARCHAR(10) , 
		  "SBAC" VARCHAR(32) , 
		  "ACNM" VARCHAR(60) , 
		  "RBAC" VARCHAR(32) , 
		  "OTNM" VARCHAR(60) , 
		  "DASQ" VARCHAR(8) , 
		  "MGID" VARCHAR(7) , 
		  "PRCCO" VARCHAR(8) , 
		  "STRINFO" VARCHAR(60) , 
		  "BCSTAT" VARCHAR(2) , 
		  "BDWFLG" VARCHAR(1) , 
		  "PRTCNT" SMALLINT NOT NULL , 
		  "BJETIM" VARCHAR(20) , 
		  "NOTE1" VARCHAR(10) , 
		  "NOTE2" VARCHAR(20) , 
		  "NOTE3" VARCHAR(60) , 
		  "NOTE4" VARCHAR(60) )   
		 IN "AFA_DATA" INDEX IN "AFA_IDX" ; 


-- DDL Statements for primary key on Table "AFA     "."RCC_SSTLOG"

ALTER TABLE "AFA     "."RCC_SSTLOG" 
	ADD CONSTRAINT "RCC_SSTLOG_PK" PRIMARY KEY
		("BJEDTE",
		 "BSPSQN",
		 "BCURSQ");



------------------------------------------------
-- DDL Statements for table "AFA     "."ABDT_HIS_UNITINFO"
------------------------------------------------
 

CREATE TABLE "AFA     "."ABDT_HIS_UNITINFO"  (
		  "APPNO" VARCHAR(6) NOT NULL , 
		  "BUSINO" VARCHAR(14) NOT NULL , 
		  "AGENTTYPE" VARCHAR(1) NOT NULL , 
		  "AGENTMODE" VARCHAR(1) NOT NULL , 
		  "VOUHTYPE" VARCHAR(2) , 
		  "VOUHNO" VARCHAR(25) , 
		  "ACCNO" VARCHAR(25) , 
		  "SUBACCNO" VARCHAR(10) , 
		  "SIGNUPMODE" VARCHAR(1) NOT NULL , 
		  "GETUSERNOMODE" VARCHAR(1) , 
		  "PROTNO" VARCHAR(30) , 
		  "APPNAME" VARCHAR(60) NOT NULL , 
		  "BUSINAME" VARCHAR(60) NOT NULL , 
		  "ADDRESS" VARCHAR(60) , 
		  "TEL" VARCHAR(20) , 
		  "USERNAME" VARCHAR(20) , 
		  "WORKDATE" VARCHAR(8) NOT NULL , 
		  "BATCHNO" VARCHAR(3) , 
		  "STARTDATE" VARCHAR(8) NOT NULL , 
		  "ENDDATE" VARCHAR(8) NOT NULL , 
		  "STARTTIME" VARCHAR(6) NOT NULL , 
		  "ENDTIME" VARCHAR(6) NOT NULL , 
		  "ZONENO" VARCHAR(10) NOT NULL , 
		  "BRNO" VARCHAR(10) NOT NULL , 
		  "TELLERNO" VARCHAR(10) , 
		  "REGDATE" VARCHAR(8) , 
		  "REGTIME" VARCHAR(6) , 
		  "STATUS" VARCHAR(1) NOT NULL , 
		  "CHKDATE" VARCHAR(8) , 
		  "CHKTIME" VARCHAR(6) , 
		  "CHKFLAG" VARCHAR(1) NOT NULL , 
		  "NOTE1" VARCHAR(10) , 
		  "NOTE2" VARCHAR(20) , 
		  "NOTE3" VARCHAR(30) , 
		  "NOTE4" VARCHAR(40) , 
		  "NOTE5" VARCHAR(50) )   
		 IN "AFA_DATA" INDEX IN "AFA_IDX" ; 

COMMENT ON COLUMN "AFA     "."ABDT_HIS_UNITINFO"."ACCNO" IS '�����˻�(�Թ��˻�)';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_UNITINFO"."ADDRESS" IS '��ϵ��ַ';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_UNITINFO"."AGENTMODE" IS 'ί�з�Χ';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_UNITINFO"."AGENTTYPE" IS 'ί�з�ʽ';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_UNITINFO"."APPNAME" IS 'ҵ������';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_UNITINFO"."APPNO" IS 'ҵ����:AG + ˳���(4)';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_UNITINFO"."BATCHNO" IS '���κ�';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_UNITINFO"."BRNO" IS '��������';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_UNITINFO"."BUSINAME" IS '��λ����';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_UNITINFO"."BUSINO" IS '��λ���:��������(10) + ˳���(4)';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_UNITINFO"."CHKDATE" IS '��������';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_UNITINFO"."CHKFLAG" IS '���ʱ�־(0-δ���� 1-�Ѷ���)';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_UNITINFO"."CHKTIME" IS '����ʱ��';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_UNITINFO"."ENDDATE" IS 'ʧЧ����';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_UNITINFO"."ENDTIME" IS '������ֹʱ��';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_UNITINFO"."GETUSERNOMODE" IS '��λ�ͻ���Ż�ȡ��ʽ(0-����, 1-��ҵ)';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_UNITINFO"."NOTE1" IS '��ע1';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_UNITINFO"."NOTE2" IS '��ע2';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_UNITINFO"."NOTE3" IS '��ע3';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_UNITINFO"."NOTE4" IS '��ע4';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_UNITINFO"."NOTE5" IS '��ע5';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_UNITINFO"."PROTNO" IS 'Э���';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_UNITINFO"."REGDATE" IS 'ע������';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_UNITINFO"."REGTIME" IS 'ע��ʱ��';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_UNITINFO"."SIGNUPMODE" IS 'ǩԼ��ʽ(0-˫��, 1-����)';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_UNITINFO"."STARTDATE" IS '��Ч����';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_UNITINFO"."STARTTIME" IS '����ʼʱ��';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_UNITINFO"."STATUS" IS '״̬(0-δ����, 1-����, 2-�ر�, 3-ͣ��)';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_UNITINFO"."SUBACCNO" IS '���˻�����';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_UNITINFO"."TEL" IS '��ϵ�绰';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_UNITINFO"."TELLERNO" IS '��Ա����';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_UNITINFO"."USERNAME" IS '��ϵ��Ա';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_UNITINFO"."VOUHNO" IS 'ƾ֤����';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_UNITINFO"."VOUHTYPE" IS 'ƾ֤����';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_UNITINFO"."WORKDATE" IS '��������';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_UNITINFO"."ZONENO" IS '��������';


-- DDL Statements for indexes on Table "AFA     "."ABDT_HIS_UNITINFO"

CREATE INDEX "AFA     "."ABDT_HUNITINFO_IDX1" ON "AFA     "."ABDT_HIS_UNITINFO" 
		("APPNO" ASC,
		 "BUSINO" ASC,
		 "ZONENO" ASC,
		 "BRNO" ASC)
		ALLOW REVERSE SCANS;






------------------------------------------------
-- DDL Statements for table "AFA     "."ABDT_HIS_CUSTINFO"
------------------------------------------------
 

CREATE TABLE "AFA     "."ABDT_HIS_CUSTINFO"  (
		  "APPNO" VARCHAR(6) NOT NULL , 
		  "BUSINO" VARCHAR(14) NOT NULL , 
		  "BUSIUSERNO" VARCHAR(20) NOT NULL , 
		  "BUSIUSERAPPNO" VARCHAR(20) NOT NULL , 
		  "BANKUSERNO" VARCHAR(12) , 
		  "VOUHTYPE" VARCHAR(2) , 
		  "VOUHNO" VARCHAR(23) , 
		  "ACCNO" VARCHAR(23) NOT NULL , 
		  "SUBACCNO" VARCHAR(10) , 
		  "CURRTYPE" VARCHAR(3) , 
		  "LIMITAMT" VARCHAR(17) , 
		  "PARTFLAG" VARCHAR(1) , 
		  "PROTOCOLNO" VARCHAR(20) NOT NULL , 
		  "CONTRACTDATE" VARCHAR(8) , 
		  "STARTDATE" VARCHAR(8) , 
		  "ENDDATE" VARCHAR(8) , 
		  "PASSCHKFLAG" VARCHAR(1) , 
		  "PASSWD" VARCHAR(16) , 
		  "IDCHKFLAG" VARCHAR(1) , 
		  "IDTYPE" VARCHAR(2) , 
		  "IDCODE" VARCHAR(20) , 
		  "NAMECHKFLAG" VARCHAR(1) , 
		  "USERNAME" VARCHAR(60) , 
		  "TEL" VARCHAR(20) , 
		  "ADDRESS" VARCHAR(60) , 
		  "ZIPCODE" VARCHAR(6) , 
		  "EMAIL" VARCHAR(50) , 
		  "STATUS" VARCHAR(1) NOT NULL , 
		  "ZONENO" VARCHAR(10) NOT NULL , 
		  "BRNO" VARCHAR(10) NOT NULL , 
		  "TELLERNO" VARCHAR(10) , 
		  "INDATE" VARCHAR(8) , 
		  "INTIME" VARCHAR(6) , 
		  "NOTE1" VARCHAR(10) , 
		  "NOTE2" VARCHAR(20) , 
		  "NOTE3" VARCHAR(30) , 
		  "NOTE4" VARCHAR(40) , 
		  "NOTE5" VARCHAR(50) )   
		 IN "AFA_DATA" INDEX IN "AFA_IDX" ; 

COMMENT ON COLUMN "AFA     "."ABDT_HIS_CUSTINFO"."ACCNO" IS '���ڴ���ʺ�(������һ��ͨ��һ��ͨģʽ�����뿨��������Ļ������ʺ�)';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_CUSTINFO"."ADDRESS" IS '��ϵ��ַ';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_CUSTINFO"."APPNO" IS 'ҵ����(AG + ˳���(4))';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_CUSTINFO"."BANKUSERNO" IS '���пͻ����';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_CUSTINFO"."BRNO" IS '�����(��������)';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_CUSTINFO"."BUSINO" IS '��λ���(��������(10) + ˳���(4))';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_CUSTINFO"."BUSIUSERAPPNO" IS '�̻��ͻ�Ӧ�ñ��';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_CUSTINFO"."BUSIUSERNO" IS '��λ�ͻ����';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_CUSTINFO"."CONTRACTDATE" IS 'ǩԼ����(��ͬ����)';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_CUSTINFO"."CURRTYPE" IS '����(CNY-�����)';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_CUSTINFO"."EMAIL" IS '��������';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_CUSTINFO"."ENDDATE" IS 'ʧЧ����';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_CUSTINFO"."IDCHKFLAG" IS '֤����֤��־(0-����֤ 1-���֤)';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_CUSTINFO"."IDCODE" IS '֤������(18λ�ַ�)';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_CUSTINFO"."IDTYPE" IS '֤������';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_CUSTINFO"."INDATE" IS '¼������';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_CUSTINFO"."INTIME" IS '¼��ʱ��';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_CUSTINFO"."LIMITAMT" IS '�����޶�(Ҫ�������� =0-������ >0-�������)';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_CUSTINFO"."NAMECHKFLAG" IS '������֤��־(0-����֤ 1-��֤)';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_CUSTINFO"."NOTE1" IS '��ע1';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_CUSTINFO"."NOTE2" IS '��ע2';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_CUSTINFO"."NOTE3" IS '��ע3';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_CUSTINFO"."NOTE4" IS '��ע4';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_CUSTINFO"."NOTE5" IS '��ע5';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_CUSTINFO"."PARTFLAG" IS '���ֿۿ��־(0-���ۿ� 1-���ֿۿ�)';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_CUSTINFO"."PASSCHKFLAG" IS '������֤��־(0-����֤ 1-��ѯ���� 2-��������)';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_CUSTINFO"."PASSWD" IS '����(����(�ɷ�����))';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_CUSTINFO"."PROTOCOLNO" IS 'Э����(�Զ�����)';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_CUSTINFO"."STARTDATE" IS '��Ч����';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_CUSTINFO"."STATUS" IS '״̬(0-ע�� 1-����)';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_CUSTINFO"."SUBACCNO" IS '���ʺ�';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_CUSTINFO"."TEL" IS '��ϵ�绰';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_CUSTINFO"."TELLERNO" IS '��Ա��';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_CUSTINFO"."USERNAME" IS '�ͻ�����';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_CUSTINFO"."VOUHNO" IS 'ƾ֤��(19��23λ����)';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_CUSTINFO"."VOUHTYPE" IS 'ƾ֤����(01-��ǿ� 02-���ڴ���)';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_CUSTINFO"."ZIPCODE" IS '�ʱ�';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_CUSTINFO"."ZONENO" IS '������';


-- DDL Statements for indexes on Table "AFA     "."ABDT_HIS_CUSTINFO"

CREATE INDEX "AFA     "."ABDT_HCUSTINFO_IDX1" ON "AFA     "."ABDT_HIS_CUSTINFO" 
		("APPNO" ASC,
		 "BUSINO" ASC,
		 "ACCNO" ASC)
		ALLOW REVERSE SCANS;


-- DDL Statements for indexes on Table "AFA     "."ABDT_HIS_CUSTINFO"

CREATE INDEX "AFA     "."ABDT_HCUSTINFO_IDX2" ON "AFA     "."ABDT_HIS_CUSTINFO" 
		("APPNO" ASC,
		 "BUSINO" ASC,
		 "BUSIUSERNO" ASC)
		ALLOW REVERSE SCANS;


-- DDL Statements for indexes on Table "AFA     "."ABDT_HIS_CUSTINFO"

CREATE INDEX "AFA     "."ABDT_HCUSTINFO_IDX3" ON "AFA     "."ABDT_HIS_CUSTINFO" 
		("APPNO" ASC,
		 "BUSINO" ASC,
		 "BANKUSERNO" ASC)
		ALLOW REVERSE SCANS;


-- DDL Statements for primary key on Table "AFA     "."ABDT_HIS_CUSTINFO"

ALTER TABLE "AFA     "."ABDT_HIS_CUSTINFO" 
	ADD PRIMARY KEY
		("PROTOCOLNO");



------------------------------------------------
-- DDL Statements for table "AFA     "."ABDT_HIS_BATCHINFO"
------------------------------------------------
 

CREATE TABLE "AFA     "."ABDT_HIS_BATCHINFO"  (
		  "BATCHNO" VARCHAR(16) NOT NULL , 
		  "APPNO" VARCHAR(6) NOT NULL , 
		  "BUSINO" VARCHAR(14) NOT NULL , 
		  "ZONENO" VARCHAR(10) NOT NULL , 
		  "BRNO" VARCHAR(10) NOT NULL , 
		  "USERNO" VARCHAR(10) NOT NULL , 
		  "ADMINNO" VARCHAR(10) , 
		  "TERMTYPE" VARCHAR(10) , 
		  "FILENAME" VARCHAR(60) NOT NULL , 
		  "INDATE" VARCHAR(8) NOT NULL , 
		  "INTIME" VARCHAR(6) , 
		  "BATCHDATE" VARCHAR(8) , 
		  "BATCHTIME" VARCHAR(6) , 
		  "TOTALNUM" VARCHAR(10) NOT NULL , 
		  "TOTALAMT" VARCHAR(17) NOT NULL , 
		  "SUCCNUM" VARCHAR(10) NOT NULL , 
		  "SUCCAMT" VARCHAR(17) NOT NULL , 
		  "FAILNUM" VARCHAR(10) NOT NULL , 
		  "FAILAMT" VARCHAR(17) NOT NULL , 
		  "STATUS" VARCHAR(2) NOT NULL , 
		  "BEGINDATE" VARCHAR(8) NOT NULL , 
		  "ENDDATE" VARCHAR(8) NOT NULL , 
		  "PROCMSG" VARCHAR(128) , 
		  "NOTE1" VARCHAR(10) , 
		  "NOTE2" VARCHAR(20) , 
		  "NOTE3" VARCHAR(30) , 
		  "NOTE4" VARCHAR(40) , 
		  "NOTE5" VARCHAR(50) )   
		 IN "AFA_DATA" INDEX IN "AFA_IDX" ; 

COMMENT ON COLUMN "AFA     "."ABDT_HIS_BATCHINFO"."ADMINNO" IS '����Ա';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_BATCHINFO"."APPNO" IS 'ҵ����(AG + ˳���(4))';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_BATCHINFO"."BATCHDATE" IS '�ύ����';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_BATCHINFO"."BATCHNO" IS 'ί�к�(���κ�)(Ψһ(����+��ˮ��))';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_BATCHINFO"."BATCHTIME" IS '�ύʱ��';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_BATCHINFO"."BEGINDATE" IS '��Ч����';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_BATCHINFO"."BRNO" IS '�����(��������)';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_BATCHINFO"."BUSINO" IS '��λ���(��������(10) + ˳���(4))';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_BATCHINFO"."ENDDATE" IS 'ʧЧ����';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_BATCHINFO"."FAILAMT" IS 'ʧ�ܽ��';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_BATCHINFO"."FAILNUM" IS 'ʧ�ܱ���';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_BATCHINFO"."FILENAME" IS '�ϴ��ļ���(ҵ����+��λ���+����.TXT)';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_BATCHINFO"."INDATE" IS '��������';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_BATCHINFO"."INTIME" IS '����ʱ��';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_BATCHINFO"."NOTE1" IS '��ע1';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_BATCHINFO"."NOTE2" IS '��ע2';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_BATCHINFO"."NOTE3" IS '��ע3';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_BATCHINFO"."NOTE4" IS '��ע4';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_BATCHINFO"."NOTE5" IS '��ע5';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_BATCHINFO"."PROCMSG" IS '������Ϣ';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_BATCHINFO"."STATUS" IS '״̬(00-�ϴ� 10-���� 11-������(����������) 20-���ύ 21-���ڴ����ύ�ļ� 22-���ύ(���ڴ���) 30-����� 31-���ڴ�������ļ� 32-����� 88-�������(�����ļ���ҵ�񱨱�) 40-����)';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_BATCHINFO"."SUCCAMT" IS '�ɹ����';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_BATCHINFO"."SUCCNUM" IS '�ɹ�����';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_BATCHINFO"."TERMTYPE" IS '�ն�����';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_BATCHINFO"."TOTALAMT" IS '�ܽ��';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_BATCHINFO"."TOTALNUM" IS '�ܱ���';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_BATCHINFO"."USERNO" IS '����Ա';

COMMENT ON COLUMN "AFA     "."ABDT_HIS_BATCHINFO"."ZONENO" IS '������';


-- DDL Statements for indexes on Table "AFA     "."ABDT_HIS_BATCHINFO"

CREATE INDEX "AFA     "."ABDT_HBATCHINFO_IDX1" ON "AFA     "."ABDT_HIS_BATCHINFO" 
		("APPNO" ASC,
		 "BUSINO" ASC,
		 "ZONENO" ASC,
		 "BRNO" ASC,
		 "INDATE" ASC,
		 "FILENAME" ASC)
		ALLOW REVERSE SCANS;


-- DDL Statements for primary key on Table "AFA     "."ABDT_HIS_BATCHINFO"

ALTER TABLE "AFA     "."ABDT_HIS_BATCHINFO" 
	ADD PRIMARY KEY
		("BATCHNO");



------------------------------------------------
-- DDL Statements for table "AFA     "."AFA_CRONADM"
------------------------------------------------
 

CREATE TABLE "AFA     "."AFA_CRONADM"  (
		  "TASKID" VARCHAR(5) NOT NULL , 
		  "TASKNAME" VARCHAR(60) NOT NULL , 
		  "STATUS" VARCHAR(1) NOT NULL , 
		  "YEAR" VARCHAR(4) , 
		  "MONTH" VARCHAR(2) , 
		  "DAY" VARCHAR(2) , 
		  "HOUR" VARCHAR(2) , 
		  "MINUTE" VARCHAR(2) , 
		  "WDAY" VARCHAR(1) , 
		  "PROCNAME" VARCHAR(128) NOT NULL , 
		  "RUNTIME" VARCHAR(14) , 
		  "NOTE1" VARCHAR(30) , 
		  "NOTE2" VARCHAR(60) )   
		 IN "AFA_DATA" INDEX IN "AFA_IDX" ; 

COMMENT ON COLUMN "AFA     "."AFA_CRONADM"."DAY" IS '��';

COMMENT ON COLUMN "AFA     "."AFA_CRONADM"."HOUR" IS 'Сʱ';

COMMENT ON COLUMN "AFA     "."AFA_CRONADM"."MINUTE" IS '����';

COMMENT ON COLUMN "AFA     "."AFA_CRONADM"."MONTH" IS '��';

COMMENT ON COLUMN "AFA     "."AFA_CRONADM"."NOTE1" IS '��ע1';

COMMENT ON COLUMN "AFA     "."AFA_CRONADM"."NOTE2" IS '��ע2';

COMMENT ON COLUMN "AFA     "."AFA_CRONADM"."PROCNAME" IS '��������';

COMMENT ON COLUMN "AFA     "."AFA_CRONADM"."STATUS" IS '״̬(0-�ر� 1-����)';

COMMENT ON COLUMN "AFA     "."AFA_CRONADM"."TASKID" IS '����ID';

COMMENT ON COLUMN "AFA     "."AFA_CRONADM"."TASKNAME" IS '��������';

COMMENT ON COLUMN "AFA     "."AFA_CRONADM"."WDAY" IS '����';

COMMENT ON COLUMN "AFA     "."AFA_CRONADM"."YEAR" IS '��';


-- DDL Statements for primary key on Table "AFA     "."AFA_CRONADM"

ALTER TABLE "AFA     "."AFA_CRONADM" 
	ADD CONSTRAINT "AFA_CRONADM_KEY" PRIMARY KEY
		("TASKID");



------------------------------------------------
-- DDL Statements for table "AFA     "."VOUH_PARAMETER"
------------------------------------------------
 

CREATE TABLE "AFA     "."VOUH_PARAMETER"  (
		  "BESBNO" VARCHAR(10) NOT NULL , 
		  "VOUHTYPE" VARCHAR(3) NOT NULL , 
		  "VOUHNAME" VARCHAR(60) NOT NULL , 
		  "TELLERNO" VARCHAR(10) , 
		  "ACTIVEDATE" VARCHAR(8) )   
		 IN "AFA_DATA" ; 

COMMENT ON COLUMN "AFA     "."VOUH_PARAMETER"."ACTIVEDATE" IS '��Ч����';

COMMENT ON COLUMN "AFA     "."VOUH_PARAMETER"."BESBNO" IS '������';

COMMENT ON COLUMN "AFA     "."VOUH_PARAMETER"."TELLERNO" IS '��Ա��';

COMMENT ON COLUMN "AFA     "."VOUH_PARAMETER"."VOUHNAME" IS 'ƾ֤����';

COMMENT ON COLUMN "AFA     "."VOUH_PARAMETER"."VOUHTYPE" IS 'ƾ֤����';


-- DDL Statements for primary key on Table "AFA     "."VOUH_PARAMETER"

ALTER TABLE "AFA     "."VOUH_PARAMETER" 
	ADD CONSTRAINT "VOUH_PARAMETER_PK" PRIMARY KEY
		("BESBNO",
		 "VOUHTYPE");



------------------------------------------------
-- DDL Statements for table "AFA     "."VOUH_REGISTER"
------------------------------------------------
 

CREATE TABLE "AFA     "."VOUH_REGISTER"  (
		  "BESBNO" VARCHAR(10) NOT NULL , 
		  "BESBSTY" VARCHAR(2) , 
		  "TELLERNO" VARCHAR(10) , 
		  "DEPOSITORY" VARCHAR(1) NOT NULL , 
		  "CUR" VARCHAR(2) , 
		  "VOUHTYPE" VARCHAR(3) NOT NULL , 
		  "STARTNO" VARCHAR(10) NOT NULL , 
		  "ENDNO" VARCHAR(10) NOT NULL , 
		  "RIVTELLER" VARCHAR(10) , 
		  "VOUHSTATUS" VARCHAR(1) NOT NULL , 
		  "VOUHNUM" VARCHAR(10) NOT NULL , 
		  "LSTTRXDAY" VARCHAR(8) NOT NULL , 
		  "LSTTRXTIME" VARCHAR(8) NOT NULL , 
		  "NOTE1" VARCHAR(10) , 
		  "NOTE2" VARCHAR(10) , 
		  "NOTE3" VARCHAR(10) , 
		  "NOTE4" VARCHAR(10) , 
		  "NOTE5" VARCHAR(10) )   
		 IN "AFA_DATA" ; 

COMMENT ON COLUMN "AFA     "."VOUH_REGISTER"."BESBNO" IS '������';

COMMENT ON COLUMN "AFA     "."VOUH_REGISTER"."BESBSTY" IS '��������';

COMMENT ON COLUMN "AFA     "."VOUH_REGISTER"."CUR" IS '���Ҵ���';

COMMENT ON COLUMN "AFA     "."VOUH_REGISTER"."DEPOSITORY" IS '�����־';

COMMENT ON COLUMN "AFA     "."VOUH_REGISTER"."ENDNO" IS '��ֹ����';

COMMENT ON COLUMN "AFA     "."VOUH_REGISTER"."LSTTRXDAY" IS '���������';

COMMENT ON COLUMN "AFA     "."VOUH_REGISTER"."LSTTRXTIME" IS '�����ʱ��';

COMMENT ON COLUMN "AFA     "."VOUH_REGISTER"."RIVTELLER" IS '�Է���Ա';

COMMENT ON COLUMN "AFA     "."VOUH_REGISTER"."STARTNO" IS '��ʼ����';

COMMENT ON COLUMN "AFA     "."VOUH_REGISTER"."TELLERNO" IS '��Ա��';

COMMENT ON COLUMN "AFA     "."VOUH_REGISTER"."VOUHNUM" IS 'ƾ֤����';

COMMENT ON COLUMN "AFA     "."VOUH_REGISTER"."VOUHSTATUS" IS 'ƾ֤״̬';

COMMENT ON COLUMN "AFA     "."VOUH_REGISTER"."VOUHTYPE" IS 'ƾ֤����';






------------------------------------------------
-- DDL Statements for table "AFA     "."AFA_BRANCH"
------------------------------------------------
 

CREATE TABLE "AFA     "."AFA_BRANCH"  (
		  "BRANCHNO" VARCHAR(10) NOT NULL , 
		  "BRANCHCODE" VARCHAR(20) , 
		  "TYPE" VARCHAR(1) NOT NULL , 
		  "UPBRANCHNO" VARCHAR(10) NOT NULL , 
		  "BRANCHNAMES" VARCHAR(20) NOT NULL , 
		  "BRANCHNAME" VARCHAR(128) NOT NULL , 
		  "NOTE1" VARCHAR(30) , 
		  "NOTE2" VARCHAR(30) , 
		  "NOTE3" VARCHAR(30) )   
		 IN "AFA_DATA" INDEX IN "AFA_IDX" ; 

COMMENT ON COLUMN "AFA     "."AFA_BRANCH"."BRANCHCODE" IS '��������(��������ͳһ����)';

COMMENT ON COLUMN "AFA     "."AFA_BRANCH"."BRANCHNAME" IS '��������ȫ��';

COMMENT ON COLUMN "AFA     "."AFA_BRANCH"."BRANCHNAMES" IS '�������Ƽ��';

COMMENT ON COLUMN "AFA     "."AFA_BRANCH"."BRANCHNO" IS '�����(���к� ֧�к� ����� 00000-��������)';

COMMENT ON COLUMN "AFA     "."AFA_BRANCH"."NOTE1" IS '��ע1';

COMMENT ON COLUMN "AFA     "."AFA_BRANCH"."NOTE2" IS '��ע2';

COMMENT ON COLUMN "AFA     "."AFA_BRANCH"."NOTE3" IS '��ע3';

COMMENT ON COLUMN "AFA     "."AFA_BRANCH"."TYPE" IS '��������(0-���� 1-���� 2-֧�� 3-����)';

COMMENT ON COLUMN "AFA     "."AFA_BRANCH"."UPBRANCHNO" IS '��Ͻ������(���к� ֧�к� 00000-��������)';


-- DDL Statements for primary key on Table "AFA     "."AFA_BRANCH"

ALTER TABLE "AFA     "."AFA_BRANCH" 
	ADD CONSTRAINT "AFA_BRANCH_KEY" PRIMARY KEY
		("BRANCHNO");



------------------------------------------------
-- DDL Statements for table "AFA     "."AFA_UNITADM"
------------------------------------------------
 

CREATE TABLE "AFA     "."AFA_UNITADM"  (
		  "SYSID" VARCHAR(6) NOT NULL , 
		  "UNITNO" VARCHAR(8) NOT NULL , 
		  "UNITNAME" VARCHAR(128) NOT NULL , 
		  "UNITSNAME" VARCHAR(20) , 
		  "STATUS" VARCHAR(1) NOT NULL , 
		  "BUSIMODE" VARCHAR(1) NOT NULL , 
		  "ACCMODE" VARCHAR(1) NOT NULL , 
		  "BANKUNITNO" VARCHAR(10) NOT NULL , 
		  "ZONENO" VARCHAR(10) NOT NULL , 
		  "BRNO" VARCHAR(10) NOT NULL , 
		  "WORKDATE" VARCHAR(8) , 
		  "PREWORKDATE" VARCHAR(8) , 
		  "STARTTIME" VARCHAR(6) , 
		  "STOPTIME" VARCHAR(6) , 
		  "FEEFLAG" VARCHAR(1) NOT NULL , 
		  "BANKCODE" VARCHAR(20) , 
		  "ACCNO1" VARCHAR(32) , 
		  "ACCNO2" VARCHAR(32) , 
		  "ACCNO3" VARCHAR(32) , 
		  "ACCNO4" VARCHAR(32) , 
		  "ACCNO5" VARCHAR(32) , 
		  "ACCNO6" VARCHAR(32) , 
		  "NAME" VARCHAR(60) , 
		  "TELPHONE" VARCHAR(20) , 
		  "ADDRESS" VARCHAR(60) , 
		  "AGENTEIGEN" VARCHAR(16) NOT NULL , 
		  "LOGINSTATUS" VARCHAR(1) , 
		  "DAYENDSTATUS" VARCHAR(1) , 
		  "DAYENDTIME" VARCHAR(6) , 
		  "TRXCHKSTATUS" VARCHAR(1) , 
		  "TRXCHKTIME" VARCHAR(6) , 
		  "NOTE1" VARCHAR(20) , 
		  "NOTE2" VARCHAR(60) )   
		 IN "AFA_DATA" INDEX IN "AFA_IDX" ; 

COMMENT ON COLUMN "AFA     "."AFA_UNITADM"."ACCMODE" IS '�˻�ģʽ0-�޷��˻� 1-�з��˻�,�����̻����� 2-�з��˻�,���̻���֧��λ����)';

COMMENT ON COLUMN "AFA     "."AFA_UNITADM"."ACCNO1" IS '�ʺ�1';

COMMENT ON COLUMN "AFA     "."AFA_UNITADM"."ACCNO2" IS '�ʺ�2';

COMMENT ON COLUMN "AFA     "."AFA_UNITADM"."ACCNO3" IS '�ʺ�3';

COMMENT ON COLUMN "AFA     "."AFA_UNITADM"."ACCNO4" IS '�ʺ�4';

COMMENT ON COLUMN "AFA     "."AFA_UNITADM"."ACCNO5" IS '�ʺ�5';

COMMENT ON COLUMN "AFA     "."AFA_UNITADM"."ACCNO6" IS '�ʺ�6';

COMMENT ON COLUMN "AFA     "."AFA_UNITADM"."ADDRESS" IS '��ϵ��ַ';

COMMENT ON COLUMN "AFA     "."AFA_UNITADM"."AGENTEIGEN" IS 'ҵ��������(1-ǩ��У���־ 2-����У���־ 3-����У���־ 4-��Ӧ��ʹ�ñ�־ 5-�ӱ�ʹ�ñ�־ 6-��չģʽ 7-���׹���ʹ�ñ�־)';

COMMENT ON COLUMN "AFA     "."AFA_UNITADM"."BANKCODE" IS '���б���(�̻������з���ı���)';

COMMENT ON COLUMN "AFA     "."AFA_UNITADM"."BANKUNITNO" IS '�̻�����(���и��̻�����ı���)';

COMMENT ON COLUMN "AFA     "."AFA_UNITADM"."BRNO" IS '���������';

COMMENT ON COLUMN "AFA     "."AFA_UNITADM"."BUSIMODE" IS 'ҵ��ģʽ(0-�޷�֧���� 1-�з�֧����,ҵ����������̻����� 2-�з�֧����,ҵ��������̻���֧��λ����)';

COMMENT ON COLUMN "AFA     "."AFA_UNITADM"."DAYENDSTATUS" IS '����״̬(0-δ�� 1-����)';

COMMENT ON COLUMN "AFA     "."AFA_UNITADM"."DAYENDTIME" IS '����ʱ��';

COMMENT ON COLUMN "AFA     "."AFA_UNITADM"."FEEFLAG" IS '��ȡģʽ(0-���շ� 1-�շ�)';

COMMENT ON COLUMN "AFA     "."AFA_UNITADM"."LOGINSTATUS" IS 'ǩ��״̬(0-ǩ�� 1-ǩ��)';

COMMENT ON COLUMN "AFA     "."AFA_UNITADM"."NAME" IS '��ϵ��';

COMMENT ON COLUMN "AFA     "."AFA_UNITADM"."NOTE1" IS '��ע1';

COMMENT ON COLUMN "AFA     "."AFA_UNITADM"."NOTE2" IS '��ע2';

COMMENT ON COLUMN "AFA     "."AFA_UNITADM"."PREWORKDATE" IS 'ҵ����������';

COMMENT ON COLUMN "AFA     "."AFA_UNITADM"."STARTTIME" IS 'ҵ��ʼʱ��';

COMMENT ON COLUMN "AFA     "."AFA_UNITADM"."STATUS" IS '�̻�״̬(0-�ر� 1-���� 2-��ͣ 3-δ����)';

COMMENT ON COLUMN "AFA     "."AFA_UNITADM"."STOPTIME" IS 'ҵ�����ʱ��';

COMMENT ON COLUMN "AFA     "."AFA_UNITADM"."SYSID" IS 'ϵͳ��ʶ';

COMMENT ON COLUMN "AFA     "."AFA_UNITADM"."TELPHONE" IS '��ϵ�绰';

COMMENT ON COLUMN "AFA     "."AFA_UNITADM"."TRXCHKSTATUS" IS '����״̬(0-δ�� 1-�Ѷ������� 2-���������ʳɹ� 3-����������ʧ��)';

COMMENT ON COLUMN "AFA     "."AFA_UNITADM"."TRXCHKTIME" IS '����ʱ��';

COMMENT ON COLUMN "AFA     "."AFA_UNITADM"."UNITNAME" IS '�̻�����';

COMMENT ON COLUMN "AFA     "."AFA_UNITADM"."UNITNO" IS '�̻���λ����';

COMMENT ON COLUMN "AFA     "."AFA_UNITADM"."UNITSNAME" IS '�̻����';

COMMENT ON COLUMN "AFA     "."AFA_UNITADM"."WORKDATE" IS 'ҵ������';

COMMENT ON COLUMN "AFA     "."AFA_UNITADM"."ZONENO" IS '������к�';


-- DDL Statements for primary key on Table "AFA     "."AFA_UNITADM"

ALTER TABLE "AFA     "."AFA_UNITADM" 
	ADD CONSTRAINT "AFA_UNITADM_KEY" PRIMARY KEY
		("SYSID",
		 "UNITNO");



------------------------------------------------
-- DDL Statements for table "AFA     "."AFA_SUBUNITADM"
------------------------------------------------
 

CREATE TABLE "AFA     "."AFA_SUBUNITADM"  (
		  "SYSID" VARCHAR(6) NOT NULL , 
		  "UNITNO" VARCHAR(8) NOT NULL , 
		  "SUBUNITNO" VARCHAR(8) NOT NULL , 
		  "SUBUNITNAME" VARCHAR(128) NOT NULL , 
		  "SUBUNITSNAME" VARCHAR(20) , 
		  "STATUS" VARCHAR(1) NOT NULL , 
		  "WORKDATE" VARCHAR(8) , 
		  "PREWORKDATE" VARCHAR(8) , 
		  "STARTTIME" VARCHAR(6) , 
		  "STOPTIME" VARCHAR(6) , 
		  "FEEFLAG" VARCHAR(1) NOT NULL , 
		  "BANKCODE" VARCHAR(20) , 
		  "ZONENO" VARCHAR(10) NOT NULL , 
		  "BRNO" VARCHAR(10) NOT NULL , 
		  "BANKUNITNO" VARCHAR(10) NOT NULL , 
		  "ACCNO1" VARCHAR(30) , 
		  "ACCNO2" VARCHAR(30) , 
		  "ACCNO3" VARCHAR(30) , 
		  "ACCNO4" VARCHAR(30) , 
		  "ACCNO5" VARCHAR(30) , 
		  "ACCNO6" VARCHAR(30) , 
		  "NAME" VARCHAR(60) , 
		  "TELPHONE" VARCHAR(20) , 
		  "ADDRESS" VARCHAR(60) , 
		  "AGENTEIGEN" VARCHAR(16) , 
		  "LOGINSTATUS" VARCHAR(1) , 
		  "DAYENDSTATUS" VARCHAR(1) , 
		  "DAYENDTIME" VARCHAR(6) , 
		  "TRXCHKSTATUS" VARCHAR(1) , 
		  "TRXCHKTIME" VARCHAR(6) , 
		  "NOTE1" VARCHAR(20) , 
		  "NOTE2" VARCHAR(60) )   
		 IN "AFA_DATA" INDEX IN "AFA_IDX" ; 

COMMENT ON COLUMN "AFA     "."AFA_SUBUNITADM"."ACCNO1" IS '�ʺ�1';

COMMENT ON COLUMN "AFA     "."AFA_SUBUNITADM"."ACCNO2" IS '�ʺ�2';

COMMENT ON COLUMN "AFA     "."AFA_SUBUNITADM"."ACCNO3" IS '�ʺ�3';

COMMENT ON COLUMN "AFA     "."AFA_SUBUNITADM"."ACCNO4" IS '�ʺ�4';

COMMENT ON COLUMN "AFA     "."AFA_SUBUNITADM"."ACCNO5" IS '�ʺ�5';

COMMENT ON COLUMN "AFA     "."AFA_SUBUNITADM"."ACCNO6" IS '�ʺ�6';

COMMENT ON COLUMN "AFA     "."AFA_SUBUNITADM"."ADDRESS" IS '��ϵ��ַ';

COMMENT ON COLUMN "AFA     "."AFA_SUBUNITADM"."AGENTEIGEN" IS 'ҵ��������(1-ǩ��У���־ 2-����У���־ 3-����У���־ 4-��Ӧ��ʹ�ñ�־ 5-�ӱ�ʹ�ñ�־ 6-��չģʽ 7-���׹���ʹ�ñ�־)';

COMMENT ON COLUMN "AFA     "."AFA_SUBUNITADM"."BANKCODE" IS '���б���(�̻������з���ı���)';

COMMENT ON COLUMN "AFA     "."AFA_SUBUNITADM"."BANKUNITNO" IS '�̻�����(���и��̻�����ı���)';

COMMENT ON COLUMN "AFA     "."AFA_SUBUNITADM"."BRNO" IS '���������';

COMMENT ON COLUMN "AFA     "."AFA_SUBUNITADM"."DAYENDSTATUS" IS '����״̬(0-δ�� 1-����)';

COMMENT ON COLUMN "AFA     "."AFA_SUBUNITADM"."DAYENDTIME" IS '����ʱ��';

COMMENT ON COLUMN "AFA     "."AFA_SUBUNITADM"."FEEFLAG" IS '��ȡģʽ(0-���շ� 1-�շ�)';

COMMENT ON COLUMN "AFA     "."AFA_SUBUNITADM"."LOGINSTATUS" IS 'ǩ��״̬(0-ǩ�� 1-ǩ��)';

COMMENT ON COLUMN "AFA     "."AFA_SUBUNITADM"."NAME" IS '��ϵ��';

COMMENT ON COLUMN "AFA     "."AFA_SUBUNITADM"."NOTE1" IS '��ע1';

COMMENT ON COLUMN "AFA     "."AFA_SUBUNITADM"."NOTE2" IS '��ע2';

COMMENT ON COLUMN "AFA     "."AFA_SUBUNITADM"."PREWORKDATE" IS 'ҵ����������';

COMMENT ON COLUMN "AFA     "."AFA_SUBUNITADM"."STARTTIME" IS 'ҵ��ʼʱ��';

COMMENT ON COLUMN "AFA     "."AFA_SUBUNITADM"."STATUS" IS '�̻�״̬(0-�ر� 1-���� 2-��ͣ 3-δ����)';

COMMENT ON COLUMN "AFA     "."AFA_SUBUNITADM"."STOPTIME" IS 'ҵ�����ʱ��';

COMMENT ON COLUMN "AFA     "."AFA_SUBUNITADM"."SUBUNITNAME" IS '�̻�����';

COMMENT ON COLUMN "AFA     "."AFA_SUBUNITADM"."SUBUNITNO" IS '�̻���֧��λ����';

COMMENT ON COLUMN "AFA     "."AFA_SUBUNITADM"."SUBUNITSNAME" IS '�̻����';

COMMENT ON COLUMN "AFA     "."AFA_SUBUNITADM"."SYSID" IS 'ϵͳ��ʶ';

COMMENT ON COLUMN "AFA     "."AFA_SUBUNITADM"."TELPHONE" IS '��ϵ�绰';

COMMENT ON COLUMN "AFA     "."AFA_SUBUNITADM"."TRXCHKSTATUS" IS '����״̬(0-δ�� 1-�Ѷ������� 2-���������ʳɹ� 3-����������ʧ��)';

COMMENT ON COLUMN "AFA     "."AFA_SUBUNITADM"."TRXCHKTIME" IS '����ʱ��';

COMMENT ON COLUMN "AFA     "."AFA_SUBUNITADM"."UNITNO" IS '�̻���λ����';

COMMENT ON COLUMN "AFA     "."AFA_SUBUNITADM"."WORKDATE" IS 'ҵ������';

COMMENT ON COLUMN "AFA     "."AFA_SUBUNITADM"."ZONENO" IS '������к�';


-- DDL Statements for primary key on Table "AFA     "."AFA_SUBUNITADM"

ALTER TABLE "AFA     "."AFA_SUBUNITADM" 
	ADD CONSTRAINT "AFA_SUBUNITADM_KEY" PRIMARY KEY
		("SYSID",
		 "UNITNO",
		 "SUBUNITNO");



------------------------------------------------
-- DDL Statements for table "AFA     "."AFA_TRADEADM"
------------------------------------------------
 

CREATE TABLE "AFA     "."AFA_TRADEADM"  (
		  "SYSID" VARCHAR(6) NOT NULL , 
		  "UNITNO" VARCHAR(8) NOT NULL , 
		  "SUBUNITNO" VARCHAR(8) NOT NULL , 
		  "TRXCODE" VARCHAR(6) NOT NULL , 
		  "TRXNAME" VARCHAR(60) , 
		  "STARTTIME" VARCHAR(6) , 
		  "STOPTIME" VARCHAR(6) , 
		  "STATUS" VARCHAR(1) NOT NULL , 
		  "CHANNELCODE" VARCHAR(3) NOT NULL , 
		  "ZONENO" VARCHAR(10) NOT NULL , 
		  "BRNO" VARCHAR(10) NOT NULL , 
		  "TELLERNO" VARCHAR(10) NOT NULL , 
		  "NOTE1" VARCHAR(10) , 
		  "NOTE2" VARCHAR(20) )   
		 IN "AFA_DATA" INDEX IN "AFA_IDX" ; 

COMMENT ON COLUMN "AFA     "."AFA_TRADEADM"."BRNO" IS '�����';

COMMENT ON COLUMN "AFA     "."AFA_TRADEADM"."CHANNELCODE" IS '��������';

COMMENT ON COLUMN "AFA     "."AFA_TRADEADM"."NOTE1" IS '��ע1';

COMMENT ON COLUMN "AFA     "."AFA_TRADEADM"."NOTE2" IS '��ע2';

COMMENT ON COLUMN "AFA     "."AFA_TRADEADM"."STARTTIME" IS 'ҵ��ʼʱ��';

COMMENT ON COLUMN "AFA     "."AFA_TRADEADM"."STATUS" IS '����״̬(0-δ���� 1-���� 2-�ر� 3-ͣ��)';

COMMENT ON COLUMN "AFA     "."AFA_TRADEADM"."STOPTIME" IS 'ҵ�����ʱ��';

COMMENT ON COLUMN "AFA     "."AFA_TRADEADM"."SUBUNITNO" IS '�̻���֧��λ����';

COMMENT ON COLUMN "AFA     "."AFA_TRADEADM"."SYSID" IS 'ϵͳ��ʶ';

COMMENT ON COLUMN "AFA     "."AFA_TRADEADM"."TELLERNO" IS '��Ա��';

COMMENT ON COLUMN "AFA     "."AFA_TRADEADM"."TRXCODE" IS '���״���';

COMMENT ON COLUMN "AFA     "."AFA_TRADEADM"."TRXNAME" IS '��������';

COMMENT ON COLUMN "AFA     "."AFA_TRADEADM"."UNITNO" IS '�̻���λ����';

COMMENT ON COLUMN "AFA     "."AFA_TRADEADM"."ZONENO" IS '���к�';


-- DDL Statements for primary key on Table "AFA     "."AFA_TRADEADM"

ALTER TABLE "AFA     "."AFA_TRADEADM" 
	ADD CONSTRAINT "AFA_TRADEADM_KEY" PRIMARY KEY
		("SYSID",
		 "UNITNO",
		 "TRXCODE",
		 "CHANNELCODE",
		 "ZONENO",
		 "BRNO",
		 "TELLERNO");



------------------------------------------------
-- DDL Statements for table "AFA     "."AFA_CHANNELADM"
------------------------------------------------
 

CREATE TABLE "AFA     "."AFA_CHANNELADM"  (
		  "SYSID" VARCHAR(6) NOT NULL , 
		  "UNITNO" VARCHAR(8) NOT NULL , 
		  "SUBUNITNO" VARCHAR(8) NOT NULL , 
		  "AGENTFLAG" VARCHAR(2) NOT NULL , 
		  "ZONENO" VARCHAR(10) NOT NULL , 
		  "ZHNO" VARCHAR(10) NOT NULL , 
		  "CHANNELCODE" VARCHAR(3) NOT NULL , 
		  "AGENTBRNO" VARCHAR(6) , 
		  "AGENTTELLER" VARCHAR(10) , 
		  "MAXAMOUNT" VARCHAR(17) NOT NULL , 
		  "TOTALAMOUNT" VARCHAR(17) NOT NULL , 
		  "BILLSAVECTL" VARCHAR(1) NOT NULL , 
		  "AUTOREVTRANCTL" VARCHAR(1) NOT NULL , 
		  "ERRCHKCTL" VARCHAR(1) NOT NULL , 
		  "CHANNELSTATUS" VARCHAR(1) NOT NULL , 
		  "AUTOCHKACCT" VARCHAR(1) NOT NULL , 
		  "FLAG1" VARCHAR(1) , 
		  "FLAG2" VARCHAR(1) , 
		  "FLAG3" VARCHAR(1) , 
		  "FLAG4" VARCHAR(1) , 
		  "NOTE1" VARCHAR(20) , 
		  "NOTE2" VARCHAR(60) )   
		 IN "AFA_DATA" INDEX IN "AFA_IDX" ; 

COMMENT ON COLUMN "AFA     "."AFA_CHANNELADM"."AGENTBRNO" IS '��Χϵͳ�����';

COMMENT ON COLUMN "AFA     "."AFA_CHANNELADM"."AGENTFLAG" IS 'ҵ��ʽ(01-���� 02-���� 03-���� 04-����)';

COMMENT ON COLUMN "AFA     "."AFA_CHANNELADM"."AGENTTELLER" IS '��Χϵͳ����Ա��';

COMMENT ON COLUMN "AFA     "."AFA_CHANNELADM"."AUTOCHKACCT" IS '�Զ�����ʻ�����(0-���ж� 1-�ж�)';

COMMENT ON COLUMN "AFA     "."AFA_CHANNELADM"."AUTOREVTRANCTL" IS '�Զ����ʱ�־(0-������ 1-����)';

COMMENT ON COLUMN "AFA     "."AFA_CHANNELADM"."BILLSAVECTL" IS '��Ʊ�����־(0-������ 1-����)';

COMMENT ON COLUMN "AFA     "."AFA_CHANNELADM"."CHANNELCODE" IS '��������';

COMMENT ON COLUMN "AFA     "."AFA_CHANNELADM"."CHANNELSTATUS" IS '����״̬(0-δ���� 1-���� 2-�ر� 3-ͣ��)';

COMMENT ON COLUMN "AFA     "."AFA_CHANNELADM"."ERRCHKCTL" IS '�쳣���׼���־(0-����Ҫ 1-��Ҫ)';

COMMENT ON COLUMN "AFA     "."AFA_CHANNELADM"."FLAG1" IS '��־1(����)';

COMMENT ON COLUMN "AFA     "."AFA_CHANNELADM"."FLAG2" IS '��־2(����)';

COMMENT ON COLUMN "AFA     "."AFA_CHANNELADM"."FLAG3" IS '��־3(����)';

COMMENT ON COLUMN "AFA     "."AFA_CHANNELADM"."FLAG4" IS '��־4(����)';

COMMENT ON COLUMN "AFA     "."AFA_CHANNELADM"."MAXAMOUNT" IS '���ʽ��׶��';

COMMENT ON COLUMN "AFA     "."AFA_CHANNELADM"."NOTE1" IS '��ע1';

COMMENT ON COLUMN "AFA     "."AFA_CHANNELADM"."NOTE2" IS '��ע2';

COMMENT ON COLUMN "AFA     "."AFA_CHANNELADM"."SUBUNITNO" IS '�̻���֧��λ����';

COMMENT ON COLUMN "AFA     "."AFA_CHANNELADM"."SYSID" IS 'ϵͳ��ʶ';

COMMENT ON COLUMN "AFA     "."AFA_CHANNELADM"."TOTALAMOUNT" IS '���ۼƽ��׶��';

COMMENT ON COLUMN "AFA     "."AFA_CHANNELADM"."UNITNO" IS '�̻���λ����';

COMMENT ON COLUMN "AFA     "."AFA_CHANNELADM"."ZHNO" IS 'ҵ��֧�к�';

COMMENT ON COLUMN "AFA     "."AFA_CHANNELADM"."ZONENO" IS 'ҵ����к�';


-- DDL Statements for primary key on Table "AFA     "."AFA_CHANNELADM"

ALTER TABLE "AFA     "."AFA_CHANNELADM" 
	ADD CONSTRAINT "AFA_CHANNELADM_KEY" PRIMARY KEY
		("SYSID",
		 "UNITNO",
		 "SUBUNITNO",
		 "AGENTFLAG",
		 "ZONENO",
		 "ZHNO",
		 "CHANNELCODE");



------------------------------------------------
-- DDL Statements for table "AFA     "."AFA_ACTNOADM"
------------------------------------------------
 

CREATE TABLE "AFA     "."AFA_ACTNOADM"  (
		  "SYSID" VARCHAR(6) NOT NULL , 
		  "UNITNO" VARCHAR(8) NOT NULL , 
		  "SUBUNITNO" VARCHAR(8) NOT NULL , 
		  "AGENTFLAG" VARCHAR(2) NOT NULL , 
		  "ZONENO" VARCHAR(10) NOT NULL , 
		  "ZHNO" VARCHAR(10) NOT NULL , 
		  "CHANNELCODE" VARCHAR(3) NOT NULL , 
		  "ACTTYPECODE" VARCHAR(3) NOT NULL , 
		  "CHKACCPWDCTL" VARCHAR(1) NOT NULL , 
		  "ENPACCPWDCTL" VARCHAR(1) NOT NULL , 
		  "STATUS" VARCHAR(1) NOT NULL )   
		 IN "AFA_DATA" INDEX IN "AFA_IDX" ; 

COMMENT ON COLUMN "AFA     "."AFA_ACTNOADM"."ACTTYPECODE" IS '�ɷѽ��ʴ���(000-�ֽ� 001-��˽�ʺ� 002-��ǿ� 003-���ǿ� 004-�Թ��ʺ� 005-����)';

COMMENT ON COLUMN "AFA     "."AFA_ACTNOADM"."AGENTFLAG" IS 'ҵ��ʽ(01-���� 02-���� 03-���� 04-����)';

COMMENT ON COLUMN "AFA     "."AFA_ACTNOADM"."CHANNELCODE" IS '��������';

COMMENT ON COLUMN "AFA     "."AFA_ACTNOADM"."CHKACCPWDCTL" IS 'У���ʻ������־(0-��У��,1-У��)';

COMMENT ON COLUMN "AFA     "."AFA_ACTNOADM"."ENPACCPWDCTL" IS '�ʻ�������ܱ�־(0-������,1-����)';

COMMENT ON COLUMN "AFA     "."AFA_ACTNOADM"."STATUS" IS '�ɷѽ���״̬(0-δ���� 1-���� 2-�ر� 3-ͣ��)';

COMMENT ON COLUMN "AFA     "."AFA_ACTNOADM"."SUBUNITNO" IS '�̻���֧��λ����';

COMMENT ON COLUMN "AFA     "."AFA_ACTNOADM"."SYSID" IS 'ϵͳ��ʶ';

COMMENT ON COLUMN "AFA     "."AFA_ACTNOADM"."UNITNO" IS '�̻���λ����';

COMMENT ON COLUMN "AFA     "."AFA_ACTNOADM"."ZHNO" IS '֧�к�';

COMMENT ON COLUMN "AFA     "."AFA_ACTNOADM"."ZONENO" IS '���к�';


-- DDL Statements for primary key on Table "AFA     "."AFA_ACTNOADM"

ALTER TABLE "AFA     "."AFA_ACTNOADM" 
	ADD CONSTRAINT "AFA_ACTNOADM_KEY" PRIMARY KEY
		("SYSID",
		 "UNITNO",
		 "SUBUNITNO",
		 "AGENTFLAG",
		 "ZONENO",
		 "ZHNO",
		 "CHANNELCODE",
		 "ACTTYPECODE");



------------------------------------------------
-- DDL Statements for table "AFA     "."AFA_MAINTRANSDTL"
------------------------------------------------
 

CREATE TABLE "AFA     "."AFA_MAINTRANSDTL"  (
		  "AGENTSERIALNO" VARCHAR(8) NOT NULL , 
		  "WORKDATE" VARCHAR(8) NOT NULL , 
		  "WORKTIME" VARCHAR(6) NOT NULL , 
		  "SYSID" VARCHAR(6) NOT NULL , 
		  "UNITNO" VARCHAR(8) NOT NULL , 
		  "SUBUNITNO" VARCHAR(8) , 
		  "AGENTFLAG" VARCHAR(2) NOT NULL , 
		  "TRXCODE" VARCHAR(10) NOT NULL , 
		  "ZONENO" VARCHAR(10) NOT NULL , 
		  "BRNO" VARCHAR(10) NOT NULL , 
		  "TELLERNO" VARCHAR(10) NOT NULL , 
		  "CASHTELNO" VARCHAR(10) , 
		  "AUTHTELLERNO" VARCHAR(10) , 
		  "CHANNELCODE" VARCHAR(3) NOT NULL , 
		  "CHANNELSERNO" VARCHAR(40) , 
		  "TERMID" VARCHAR(20) , 
		  "CUSTOMERID" VARCHAR(16) , 
		  "USERNO" VARCHAR(30) NOT NULL , 
		  "SUBUSERNO" VARCHAR(30) , 
		  "USERNAME" VARCHAR(100) , 
		  "ACCTYPE" VARCHAR(3) NOT NULL , 
		  "DRACCNO" VARCHAR(30) , 
		  "CRACCNO" VARCHAR(30) , 
		  "VOUHTYPE" VARCHAR(10) , 
		  "VOUHNO" VARCHAR(30) , 
		  "VOUHDATE" VARCHAR(8) , 
		  "CURRTYPE" VARCHAR(3) , 
		  "CURRFLAG" VARCHAR(3) , 
		  "AMOUNT" VARCHAR(17) NOT NULL , 
		  "SUBAMOUNT" VARCHAR(17) , 
		  "REVTRANF" VARCHAR(1) NOT NULL , 
		  "PREAGENTSERNO" VARCHAR(8) , 
		  "BANKSTATUS" VARCHAR(1) , 
		  "BANKCODE" VARCHAR(10) , 
		  "BANKSERNO" VARCHAR(20) , 
		  "CORPSTATUS" VARCHAR(1) , 
		  "CORPCODE" VARCHAR(10) , 
		  "CORPSERNO" VARCHAR(20) , 
		  "CORPTIME" VARCHAR(20) , 
		  "ERRORMSG" VARCHAR(128) , 
		  "CHKFLAG" VARCHAR(1) , 
		  "CORPCHKFLAG" VARCHAR(1) , 
		  "APPENDFLAG" VARCHAR(1) , 
		  "NOTE1" VARCHAR(20) , 
		  "NOTE2" VARCHAR(20) , 
		  "NOTE3" VARCHAR(40) , 
		  "NOTE4" VARCHAR(40) , 
		  "NOTE5" VARCHAR(60) , 
		  "NOTE6" VARCHAR(60) , 
		  "NOTE7" VARCHAR(80) , 
		  "NOTE8" VARCHAR(80) , 
		  "NOTE9" VARCHAR(100) , 
		  "NOTE10" VARCHAR(100) )   
		 IN "AFA_DATA" INDEX IN "AFA_IDX" ; 

COMMENT ON COLUMN "AFA     "."AFA_MAINTRANSDTL"."ACCTYPE" IS '�ʻ�����';

COMMENT ON COLUMN "AFA     "."AFA_MAINTRANSDTL"."AGENTFLAG" IS 'ҵ��ʽ(01-���� 02-���� 03-���� 04-����)';

COMMENT ON COLUMN "AFA     "."AFA_MAINTRANSDTL"."AGENTSERIALNO" IS 'ҵ����ˮ��';

COMMENT ON COLUMN "AFA     "."AFA_MAINTRANSDTL"."AMOUNT" IS '���׽��';

COMMENT ON COLUMN "AFA     "."AFA_MAINTRANSDTL"."APPENDFLAG" IS '�ӱ�ʹ�ñ�־(0-�޴ӱ���Ϣ 1-�дӱ���Ϣ)';

COMMENT ON COLUMN "AFA     "."AFA_MAINTRANSDTL"."AUTHTELLERNO" IS '��Ȩ��Ա��';

COMMENT ON COLUMN "AFA     "."AFA_MAINTRANSDTL"."BANKCODE" IS '����.���׷�����';

COMMENT ON COLUMN "AFA     "."AFA_MAINTRANSDTL"."BANKSERNO" IS '����.������ˮ��';

COMMENT ON COLUMN "AFA     "."AFA_MAINTRANSDTL"."BANKSTATUS" IS '����.����״̬(0:���� 1:ʧ�� 2:�쳣 3.�ѳ���)';

COMMENT ON COLUMN "AFA     "."AFA_MAINTRANSDTL"."BRNO" IS '������';

COMMENT ON COLUMN "AFA     "."AFA_MAINTRANSDTL"."CASHTELNO" IS '����Ա��';

COMMENT ON COLUMN "AFA     "."AFA_MAINTRANSDTL"."CHANNELCODE" IS '��������';

COMMENT ON COLUMN "AFA     "."AFA_MAINTRANSDTL"."CHANNELSERNO" IS '������ˮ��';

COMMENT ON COLUMN "AFA     "."AFA_MAINTRANSDTL"."CHKFLAG" IS '�������ʱ�־(0-�Ѷ���,���׳ɹ� 1-�Ѷ���,����ʧ��, 9-δ����)';

COMMENT ON COLUMN "AFA     "."AFA_MAINTRANSDTL"."CORPCHKFLAG" IS '��ҵ���ʱ�־(0-�Ѷ���,���׳ɹ� 1-�Ѷ���,����ʧ��, 9-δ����)';

COMMENT ON COLUMN "AFA     "."AFA_MAINTRANSDTL"."CORPCODE" IS '��ҵ.���׷�����';

COMMENT ON COLUMN "AFA     "."AFA_MAINTRANSDTL"."CORPSERNO" IS '��ҵ.������ˮ��';

COMMENT ON COLUMN "AFA     "."AFA_MAINTRANSDTL"."CORPSTATUS" IS '��ҵ.����״̬(0-���� 1-ʧ�� 2-�쳣 3-�ѳ���)';

COMMENT ON COLUMN "AFA     "."AFA_MAINTRANSDTL"."CORPTIME" IS '��ҵ.����ʱ���';

COMMENT ON COLUMN "AFA     "."AFA_MAINTRANSDTL"."CRACCNO" IS '�����ʻ�����';

COMMENT ON COLUMN "AFA     "."AFA_MAINTRANSDTL"."CURRFLAG" IS '�����־';

COMMENT ON COLUMN "AFA     "."AFA_MAINTRANSDTL"."CURRTYPE" IS '����';

COMMENT ON COLUMN "AFA     "."AFA_MAINTRANSDTL"."CUSTOMERID" IS '�ͻ�ע���';

COMMENT ON COLUMN "AFA     "."AFA_MAINTRANSDTL"."DRACCNO" IS '�跽�ʻ�����';

COMMENT ON COLUMN "AFA     "."AFA_MAINTRANSDTL"."ERRORMSG" IS '���״�����Ϣ';

COMMENT ON COLUMN "AFA     "."AFA_MAINTRANSDTL"."NOTE1" IS '��ע1';

COMMENT ON COLUMN "AFA     "."AFA_MAINTRANSDTL"."NOTE10" IS '��ע10';

COMMENT ON COLUMN "AFA     "."AFA_MAINTRANSDTL"."NOTE2" IS '��ע2';

COMMENT ON COLUMN "AFA     "."AFA_MAINTRANSDTL"."NOTE3" IS '��ע3';

COMMENT ON COLUMN "AFA     "."AFA_MAINTRANSDTL"."NOTE4" IS '��ע4';

COMMENT ON COLUMN "AFA     "."AFA_MAINTRANSDTL"."NOTE5" IS '��ע5';

COMMENT ON COLUMN "AFA     "."AFA_MAINTRANSDTL"."NOTE6" IS '��ע6';

COMMENT ON COLUMN "AFA     "."AFA_MAINTRANSDTL"."NOTE7" IS '��ע7';

COMMENT ON COLUMN "AFA     "."AFA_MAINTRANSDTL"."NOTE8" IS '��ע8';

COMMENT ON COLUMN "AFA     "."AFA_MAINTRANSDTL"."NOTE9" IS '��ע9';

COMMENT ON COLUMN "AFA     "."AFA_MAINTRANSDTL"."PREAGENTSERNO" IS '����.ԭƽ̨��ˮ��(������������)';

COMMENT ON COLUMN "AFA     "."AFA_MAINTRANSDTL"."REVTRANF" IS '�����ױ�־(0-������ 1-������ 2-�Զ�����)';

COMMENT ON COLUMN "AFA     "."AFA_MAINTRANSDTL"."SUBAMOUNT" IS '���ӽ��';

COMMENT ON COLUMN "AFA     "."AFA_MAINTRANSDTL"."SUBUNITNO" IS '�̻���֧��λ����';

COMMENT ON COLUMN "AFA     "."AFA_MAINTRANSDTL"."SUBUSERNO" IS '�����û���';

COMMENT ON COLUMN "AFA     "."AFA_MAINTRANSDTL"."SYSID" IS 'ϵͳ��ʶ';

COMMENT ON COLUMN "AFA     "."AFA_MAINTRANSDTL"."TELLERNO" IS '��Ա��';

COMMENT ON COLUMN "AFA     "."AFA_MAINTRANSDTL"."TERMID" IS '�ն˺�';

COMMENT ON COLUMN "AFA     "."AFA_MAINTRANSDTL"."TRXCODE" IS '������';

COMMENT ON COLUMN "AFA     "."AFA_MAINTRANSDTL"."UNITNO" IS '�̻���λ����';

COMMENT ON COLUMN "AFA     "."AFA_MAINTRANSDTL"."USERNAME" IS '�û�����';

COMMENT ON COLUMN "AFA     "."AFA_MAINTRANSDTL"."USERNO" IS '�û���';

COMMENT ON COLUMN "AFA     "."AFA_MAINTRANSDTL"."VOUHDATE" IS 'ƾ֤����';

COMMENT ON COLUMN "AFA     "."AFA_MAINTRANSDTL"."VOUHNO" IS 'ƾ֤��';

COMMENT ON COLUMN "AFA     "."AFA_MAINTRANSDTL"."VOUHTYPE" IS 'ƾ֤����';

COMMENT ON COLUMN "AFA     "."AFA_MAINTRANSDTL"."WORKDATE" IS '��������';

COMMENT ON COLUMN "AFA     "."AFA_MAINTRANSDTL"."WORKTIME" IS '����ʱ��';

COMMENT ON COLUMN "AFA     "."AFA_MAINTRANSDTL"."ZONENO" IS '���к�';


-- DDL Statements for indexes on Table "AFA     "."AFA_MAINTRANSDTL"

CREATE INDEX "AFA     "."AFA_MAINDTL_IDX2" ON "AFA     "."AFA_MAINTRANSDTL" 
		("WORKDATE" ASC,
		 "SYSID" ASC,
		 "AGENTFLAG" ASC,
		 "REVTRANF" ASC,
		 "BANKSTATUS" ASC,
		 "CORPSTATUS" ASC)
		ALLOW REVERSE SCANS;


-- DDL Statements for indexes on Table "AFA     "."AFA_MAINTRANSDTL"

CREATE INDEX "AFA     "."AFA_MAINDTL_IDX3" ON "AFA     "."AFA_MAINTRANSDTL" 
		("ZONENO" ASC,
		 "SYSID" ASC,
		 "AGENTFLAG" ASC)
		ALLOW REVERSE SCANS;


-- DDL Statements for primary key on Table "AFA     "."AFA_MAINTRANSDTL"

ALTER TABLE "AFA     "."AFA_MAINTRANSDTL" 
	ADD CONSTRAINT "AFA_MAINDTL_KEY" PRIMARY KEY
		("WORKDATE",
		 "AGENTSERIALNO");



------------------------------------------------
-- DDL Statements for table "AFA     "."AFA_HIS_MAINTRANSDTL"
------------------------------------------------
 

CREATE TABLE "AFA     "."AFA_HIS_MAINTRANSDTL"  (
		  "AGENTSERIALNO" VARCHAR(8) NOT NULL , 
		  "WORKDATE" VARCHAR(8) NOT NULL , 
		  "WORKTIME" VARCHAR(6) NOT NULL , 
		  "SYSID" VARCHAR(6) NOT NULL , 
		  "UNITNO" VARCHAR(8) NOT NULL , 
		  "SUBUNITNO" VARCHAR(8) , 
		  "AGENTFLAG" VARCHAR(2) NOT NULL , 
		  "TRXCODE" VARCHAR(10) NOT NULL , 
		  "ZONENO" VARCHAR(10) NOT NULL , 
		  "BRNO" VARCHAR(10) NOT NULL , 
		  "TELLERNO" VARCHAR(10) NOT NULL , 
		  "CASHTELNO" VARCHAR(10) , 
		  "AUTHTELLERNO" VARCHAR(10) , 
		  "CHANNELCODE" VARCHAR(3) NOT NULL , 
		  "CHANNELSERNO" VARCHAR(40) , 
		  "TERMID" VARCHAR(20) , 
		  "CUSTOMERID" VARCHAR(13) , 
		  "USERNO" VARCHAR(30) NOT NULL , 
		  "SUBUSERNO" VARCHAR(30) , 
		  "USERNAME" VARCHAR(100) , 
		  "ACCTYPE" VARCHAR(3) NOT NULL , 
		  "DRACCNO" VARCHAR(30) , 
		  "CRACCNO" VARCHAR(30) , 
		  "VOUHTYPE" VARCHAR(10) , 
		  "VOUHNO" VARCHAR(30) , 
		  "VOUHDATE" VARCHAR(8) , 
		  "CURRTYPE" VARCHAR(3) , 
		  "CURRFLAG" VARCHAR(3) , 
		  "AMOUNT" VARCHAR(17) NOT NULL , 
		  "SUBAMOUNT" VARCHAR(17) , 
		  "REVTRANF" VARCHAR(1) NOT NULL , 
		  "PREAGENTSERNO" VARCHAR(8) , 
		  "BANKSTATUS" VARCHAR(1) , 
		  "BANKCODE" VARCHAR(10) , 
		  "BANKSERNO" VARCHAR(20) , 
		  "CORPSTATUS" VARCHAR(1) , 
		  "CORPCODE" VARCHAR(10) , 
		  "CORPSERNO" VARCHAR(20) , 
		  "CORPTIME" VARCHAR(20) , 
		  "ERRORMSG" VARCHAR(200) , 
		  "CHKFLAG" VARCHAR(1) , 
		  "CORPCHKFLAG" VARCHAR(1) , 
		  "APPENDFLAG" VARCHAR(1) , 
		  "NOTE1" VARCHAR(20) , 
		  "NOTE2" VARCHAR(20) , 
		  "NOTE3" VARCHAR(40) , 
		  "NOTE4" VARCHAR(40) , 
		  "NOTE5" VARCHAR(60) , 
		  "NOTE6" VARCHAR(60) , 
		  "NOTE7" VARCHAR(80) , 
		  "NOTE8" VARCHAR(80) , 
		  "NOTE9" VARCHAR(100) , 
		  "NOTE10" VARCHAR(100) )   
		 IN "AFA_DATA" INDEX IN "AFA_IDX" ; 

COMMENT ON COLUMN "AFA     "."AFA_HIS_MAINTRANSDTL"."ACCTYPE" IS '�ʻ�����';

COMMENT ON COLUMN "AFA     "."AFA_HIS_MAINTRANSDTL"."AGENTFLAG" IS 'ҵ��ʽ(01-���� 02-���� 03-���� 04-����)';

COMMENT ON COLUMN "AFA     "."AFA_HIS_MAINTRANSDTL"."AGENTSERIALNO" IS 'ҵ����ˮ��';

COMMENT ON COLUMN "AFA     "."AFA_HIS_MAINTRANSDTL"."AMOUNT" IS '���׽��';

COMMENT ON COLUMN "AFA     "."AFA_HIS_MAINTRANSDTL"."APPENDFLAG" IS '�ӱ�ʹ�ñ�־(0-�޴ӱ���Ϣ 1-�дӱ���Ϣ)';

COMMENT ON COLUMN "AFA     "."AFA_HIS_MAINTRANSDTL"."AUTHTELLERNO" IS '��Ȩ��Ա��';

COMMENT ON COLUMN "AFA     "."AFA_HIS_MAINTRANSDTL"."BANKCODE" IS '����.���׷�����';

COMMENT ON COLUMN "AFA     "."AFA_HIS_MAINTRANSDTL"."BANKSERNO" IS '����.������ˮ��';

COMMENT ON COLUMN "AFA     "."AFA_HIS_MAINTRANSDTL"."BANKSTATUS" IS '����.����״̬(0:���� 1:ʧ�� 2:�쳣 3.�ѳ���)';

COMMENT ON COLUMN "AFA     "."AFA_HIS_MAINTRANSDTL"."BRNO" IS '������';

COMMENT ON COLUMN "AFA     "."AFA_HIS_MAINTRANSDTL"."CASHTELNO" IS '����Ա��';

COMMENT ON COLUMN "AFA     "."AFA_HIS_MAINTRANSDTL"."CHANNELCODE" IS '��������';

COMMENT ON COLUMN "AFA     "."AFA_HIS_MAINTRANSDTL"."CHANNELSERNO" IS '������ˮ��';

COMMENT ON COLUMN "AFA     "."AFA_HIS_MAINTRANSDTL"."CHKFLAG" IS '�������ʱ�־(0-�Ѷ���,���׳ɹ� 1-�Ѷ���,����ʧ��, 9-δ����)';

COMMENT ON COLUMN "AFA     "."AFA_HIS_MAINTRANSDTL"."CORPCHKFLAG" IS '��ҵ���ʱ�־(0-�Ѷ���,���׳ɹ� 1-�Ѷ���,����ʧ��, 9-δ����)';

COMMENT ON COLUMN "AFA     "."AFA_HIS_MAINTRANSDTL"."CORPCODE" IS '��ҵ.���׷�����';

COMMENT ON COLUMN "AFA     "."AFA_HIS_MAINTRANSDTL"."CORPSERNO" IS '��ҵ.������ˮ��';

COMMENT ON COLUMN "AFA     "."AFA_HIS_MAINTRANSDTL"."CORPSTATUS" IS '��ҵ.����״̬(0-���� 1-ʧ�� 2-�쳣 3-�ѳ���)';

COMMENT ON COLUMN "AFA     "."AFA_HIS_MAINTRANSDTL"."CORPTIME" IS '��ҵ.����ʱ���';

COMMENT ON COLUMN "AFA     "."AFA_HIS_MAINTRANSDTL"."CRACCNO" IS '�����ʻ�����';

COMMENT ON COLUMN "AFA     "."AFA_HIS_MAINTRANSDTL"."CURRFLAG" IS '�����־';

COMMENT ON COLUMN "AFA     "."AFA_HIS_MAINTRANSDTL"."CURRTYPE" IS '����';

COMMENT ON COLUMN "AFA     "."AFA_HIS_MAINTRANSDTL"."CUSTOMERID" IS '�ͻ�ע���';

COMMENT ON COLUMN "AFA     "."AFA_HIS_MAINTRANSDTL"."DRACCNO" IS '�跽�ʻ�����';

COMMENT ON COLUMN "AFA     "."AFA_HIS_MAINTRANSDTL"."ERRORMSG" IS '���״�����Ϣ';

COMMENT ON COLUMN "AFA     "."AFA_HIS_MAINTRANSDTL"."NOTE1" IS '��ע1';

COMMENT ON COLUMN "AFA     "."AFA_HIS_MAINTRANSDTL"."NOTE10" IS '��ע10';

COMMENT ON COLUMN "AFA     "."AFA_HIS_MAINTRANSDTL"."NOTE2" IS '��ע2';

COMMENT ON COLUMN "AFA     "."AFA_HIS_MAINTRANSDTL"."NOTE3" IS '��ע3';

COMMENT ON COLUMN "AFA     "."AFA_HIS_MAINTRANSDTL"."NOTE4" IS '��ע4';

COMMENT ON COLUMN "AFA     "."AFA_HIS_MAINTRANSDTL"."NOTE5" IS '��ע5';

COMMENT ON COLUMN "AFA     "."AFA_HIS_MAINTRANSDTL"."NOTE6" IS '��ע6';

COMMENT ON COLUMN "AFA     "."AFA_HIS_MAINTRANSDTL"."NOTE7" IS '��ע7';

COMMENT ON COLUMN "AFA     "."AFA_HIS_MAINTRANSDTL"."NOTE8" IS '��ע8';

COMMENT ON COLUMN "AFA     "."AFA_HIS_MAINTRANSDTL"."NOTE9" IS '��ע9';

COMMENT ON COLUMN "AFA     "."AFA_HIS_MAINTRANSDTL"."PREAGENTSERNO" IS '����.ԭƽ̨��ˮ��(������������)';

COMMENT ON COLUMN "AFA     "."AFA_HIS_MAINTRANSDTL"."REVTRANF" IS '�����ױ�־(0-������ 1-������ 2-�Զ�����)';

COMMENT ON COLUMN "AFA     "."AFA_HIS_MAINTRANSDTL"."SUBAMOUNT" IS '���ӽ��';

COMMENT ON COLUMN "AFA     "."AFA_HIS_MAINTRANSDTL"."SUBUNITNO" IS '�̻���֧��λ����';

COMMENT ON COLUMN "AFA     "."AFA_HIS_MAINTRANSDTL"."SUBUSERNO" IS '�����û���';

COMMENT ON COLUMN "AFA     "."AFA_HIS_MAINTRANSDTL"."SYSID" IS 'ϵͳ��ʶ';

COMMENT ON COLUMN "AFA     "."AFA_HIS_MAINTRANSDTL"."TELLERNO" IS '��Ա��';

COMMENT ON COLUMN "AFA     "."AFA_HIS_MAINTRANSDTL"."TERMID" IS '�ն˺�';

COMMENT ON COLUMN "AFA     "."AFA_HIS_MAINTRANSDTL"."TRXCODE" IS '������';

COMMENT ON COLUMN "AFA     "."AFA_HIS_MAINTRANSDTL"."UNITNO" IS '�̻���λ����';

COMMENT ON COLUMN "AFA     "."AFA_HIS_MAINTRANSDTL"."USERNAME" IS '�û�����';

COMMENT ON COLUMN "AFA     "."AFA_HIS_MAINTRANSDTL"."USERNO" IS '�û���';

COMMENT ON COLUMN "AFA     "."AFA_HIS_MAINTRANSDTL"."VOUHDATE" IS 'ƾ֤����';

COMMENT ON COLUMN "AFA     "."AFA_HIS_MAINTRANSDTL"."VOUHNO" IS 'ƾ֤��';

COMMENT ON COLUMN "AFA     "."AFA_HIS_MAINTRANSDTL"."VOUHTYPE" IS 'ƾ֤����';

COMMENT ON COLUMN "AFA     "."AFA_HIS_MAINTRANSDTL"."WORKDATE" IS '��������';

COMMENT ON COLUMN "AFA     "."AFA_HIS_MAINTRANSDTL"."WORKTIME" IS '����ʱ��';

COMMENT ON COLUMN "AFA     "."AFA_HIS_MAINTRANSDTL"."ZONENO" IS '���к�';


-- DDL Statements for indexes on Table "AFA     "."AFA_HIS_MAINTRANSDTL"

CREATE INDEX "AFA     "."AFA_HMAINDTL_IDX2" ON "AFA     "."AFA_HIS_MAINTRANSDTL" 
		("WORKDATE" ASC,
		 "SYSID" ASC,
		 "AGENTFLAG" ASC,
		 "REVTRANF" ASC,
		 "BANKSTATUS" ASC,
		 "CORPSTATUS" ASC)
		ALLOW REVERSE SCANS;


-- DDL Statements for indexes on Table "AFA     "."AFA_HIS_MAINTRANSDTL"

CREATE INDEX "AFA     "."AFA_HMAINDTL_IDX3" ON "AFA     "."AFA_HIS_MAINTRANSDTL" 
		("ZONENO" ASC,
		 "SYSID" ASC,
		 "AGENTFLAG" ASC)
		ALLOW REVERSE SCANS;


-- DDL Statements for primary key on Table "AFA     "."AFA_HIS_MAINTRANSDTL"

ALTER TABLE "AFA     "."AFA_HIS_MAINTRANSDTL" 
	ADD CONSTRAINT "AFA_HMAINDTL_KEY" PRIMARY KEY
		("WORKDATE",
		 "AGENTSERIALNO");



------------------------------------------------
-- DDL Statements for table "AFA     "."RCC_HDCBKA"
------------------------------------------------
 

CREATE TABLE "AFA     "."RCC_HDCBKA"  (
		  "BJEDTE" VARCHAR(8) NOT NULL , 
		  "BSPSQN" VARCHAR(12) NOT NULL , 
		  "BRSFLG" VARCHAR(1) NOT NULL , 
		  "BESBNO" VARCHAR(10) , 
		  "BETELR" VARCHAR(6) , 
		  "BEAUUS" VARCHAR(6) , 
		  "NCCWKDAT" VARCHAR(8) , 
		  "TRCCO" VARCHAR(7) , 
		  "TRCDAT" VARCHAR(8) , 
		  "TRCNO" VARCHAR(8) , 
		  "SNDMBRCO" VARCHAR(10) , 
		  "RCVMBRCO" VARCHAR(10) , 
		  "SNDBNKCO" VARCHAR(10) , 
		  "SNDBNKNM" VARCHAR(60) , 
		  "RCVBNKCO" VARCHAR(10) , 
		  "RCVBNKNM" VARCHAR(60) , 
		  "BOJEDT" VARCHAR(8) , 
		  "BOSPSQ" VARCHAR(12) , 
		  "ORTRCCO" VARCHAR(7) , 
		  "CUR" VARCHAR(3) , 
		  "OCCAMT" DECIMAL(15,2) , 
		  "CONT" VARCHAR(255) , 
		  "PYRACC" VARCHAR(32) , 
		  "PYEACC" VARCHAR(32) , 
		  "ISDEAL" VARCHAR(1) , 
		  "PRCCO" VARCHAR(8) , 
		  "NOTE1" VARCHAR(10) , 
		  "NOTE2" VARCHAR(20) , 
		  "NOTE3" VARCHAR(60) , 
		  "NOTE4" VARCHAR(60) )   
		 IN "AFA_DATA" INDEX IN "AFA_IDX" ; 


-- DDL Statements for primary key on Table "AFA     "."RCC_HDCBKA"

ALTER TABLE "AFA     "."RCC_HDCBKA" 
	ADD CONSTRAINT "RCC_HDCBKA_PK" PRIMARY KEY
		("BJEDTE",
		 "BSPSQN");



------------------------------------------------
-- DDL Statements for table "AFA     "."RCC_HPCBKA"
------------------------------------------------
 

CREATE TABLE "AFA     "."RCC_HPCBKA"  (
		  "BJEDTE" VARCHAR(8) NOT NULL , 
		  "BSPSQN" VARCHAR(12) NOT NULL , 
		  "BRSFLG" VARCHAR(1) NOT NULL , 
		  "BESBNO" VARCHAR(10) , 
		  "BETELR" VARCHAR(6) , 
		  "BEAUUS" VARCHAR(6) , 
		  "NCCWKDAT" VARCHAR(8) , 
		  "TRCCO" VARCHAR(7) , 
		  "TRCDAT" VARCHAR(8) , 
		  "TRCNO" VARCHAR(8) , 
		  "SNDMBRCO" VARCHAR(10) , 
		  "RCVMBRCO" VARCHAR(10) , 
		  "SNDBNKCO" VARCHAR(10) , 
		  "SNDBNKNM" VARCHAR(60) , 
		  "RCVBNKCO" VARCHAR(10) , 
		  "RCVBNKNM" VARCHAR(60) , 
		  "BOJEDT" VARCHAR(8) , 
		  "BOSPSQ" VARCHAR(12) , 
		  "ORTRCCO" VARCHAR(7) , 
		  "BILVER" VARCHAR(2) , 
		  "BILNO" VARCHAR(8) , 
		  "BILDAT" VARCHAR(8) , 
		  "PAYWAY" VARCHAR(1) , 
		  "CUR" VARCHAR(3) , 
		  "BILAMT" DECIMAL(15,2) , 
		  "PYRACC" VARCHAR(32) , 
		  "PYRNAM" VARCHAR(60) , 
		  "PYEACC" VARCHAR(32) , 
		  "PYENAM" VARCHAR(60) , 
		  "CONT" VARCHAR(255) , 
		  "ISDEAL" VARCHAR(1) , 
		  "PRCCO" VARCHAR(8) , 
		  "NOTE1" VARCHAR(10) , 
		  "NOTE2" VARCHAR(20) , 
		  "NOTE3" VARCHAR(60) , 
		  "NOTE4" VARCHAR(60) )   
		 IN "AFA_DATA" INDEX IN "AFA_IDX" ; 


-- DDL Statements for primary key on Table "AFA     "."RCC_HPCBKA"

ALTER TABLE "AFA     "."RCC_HPCBKA" 
	ADD CONSTRAINT "RCC_HPCBKA_PK" PRIMARY KEY
		("BJEDTE",
		 "BSPSQN");



------------------------------------------------
-- DDL Statements for table "AFA     "."RCC_PJCBKA"
------------------------------------------------
 

CREATE TABLE "AFA     "."RCC_PJCBKA"  (
		  "BJEDTE" VARCHAR(8) NOT NULL , 
		  "BSPSQN" VARCHAR(12) NOT NULL , 
		  "BRSFLG" VARCHAR(1) NOT NULL , 
		  "BESBNO" VARCHAR(10) , 
		  "BETELR" VARCHAR(6) , 
		  "BEAUUS" VARCHAR(6) , 
		  "NCCWKDAT" VARCHAR(8) , 
		  "TRCCO" VARCHAR(7) , 
		  "TRCDAT" VARCHAR(8) , 
		  "TRCNO" VARCHAR(8) , 
		  "SNDMBRCO" VARCHAR(10) , 
		  "RCVMBRCO" VARCHAR(10) , 
		  "SNDBNKCO" VARCHAR(10) , 
		  "SNDBNKNM" VARCHAR(60) , 
		  "RCVBNKCO" VARCHAR(10) , 
		  "RCVBNKNM" VARCHAR(60) , 
		  "BOJEDT" VARCHAR(8) , 
		  "BOSPSQ" VARCHAR(12) , 
		  "ORTRCCO" VARCHAR(7) , 
		  "BILDAT" VARCHAR(8) , 
		  "BILNO" VARCHAR(8) , 
		  "BILPNAM" VARCHAR(60) , 
		  "BILENDDT" VARCHAR(8) , 
		  "BILAMT" DECIMAL(15,2) , 
		  "PYENAM" VARCHAR(60) , 
		  "HONBNKNM" VARCHAR(60) , 
		  "CONT" VARCHAR(60) , 
		  "ISDEAL" VARCHAR(1) , 
		  "PRCCO" VARCHAR(8) , 
		  "NOTE1" VARCHAR(10) , 
		  "NOTE2" VARCHAR(20) , 
		  "NOTE3" VARCHAR(60) , 
		  "NOTE4" VARCHAR(60) )   
		 IN "AFA_DATA" INDEX IN "AFA_IDX" ; 


-- DDL Statements for indexes on Table "AFA     "."RCC_PJCBKA"

CREATE UNIQUE INDEX "AFA     "."RCC_PJCBKA_IDX1" ON "AFA     "."RCC_PJCBKA" 
		("BJEDTE" ASC,
		 "BSPSQN" ASC)
		PCTFREE 10 ALLOW REVERSE SCANS;


-- DDL Statements for primary key on Table "AFA     "."RCC_PJCBKA"

ALTER TABLE "AFA     "."RCC_PJCBKA" 
	ADD CONSTRAINT "RCC_PJCBKA_PK" PRIMARY KEY
		("BJEDTE",
		 "BSPSQN",
		 "BRSFLG");



------------------------------------------------
-- DDL Statements for table "AFA     "."RCC_ZTCBKA"
------------------------------------------------
 

CREATE TABLE "AFA     "."RCC_ZTCBKA"  (
		  "BJEDTE" VARCHAR(8) NOT NULL , 
		  "BSPSQN" VARCHAR(12) NOT NULL , 
		  "BRSFLG" VARCHAR(1) NOT NULL , 
		  "BESBNO" VARCHAR(10) , 
		  "BEACSB" VARCHAR(10) , 
		  "BETELR" VARCHAR(6) , 
		  "BEAUUS" VARCHAR(6) , 
		  "NCCWKDAT" VARCHAR(8) , 
		  "TRCCO" VARCHAR(7) , 
		  "TRCDAT" VARCHAR(8) , 
		  "TRCNO" VARCHAR(8) , 
		  "SNDMBRCO" VARCHAR(10) , 
		  "RCVMBRCO" VARCHAR(10) , 
		  "SNDBNKCO" VARCHAR(10) , 
		  "SNDBNKNM" VARCHAR(60) , 
		  "RCVBNKCO" VARCHAR(10) , 
		  "RCVBNKNM" VARCHAR(60) , 
		  "BOJEDT" VARCHAR(8) , 
		  "BOSPSQ" VARCHAR(12) , 
		  "ORTRCCO" VARCHAR(7) , 
		  "CUR" VARCHAR(3) , 
		  "OCCAMT" DECIMAL(15,2) , 
		  "CONT" VARCHAR(255) , 
		  "NCCTRCST" VARCHAR(2) , 
		  "MBRTRCST" VARCHAR(2) , 
		  "ISDEAL" VARCHAR(1) , 
		  "PRCCO" VARCHAR(8) , 
		  "NOTE1" VARCHAR(10) , 
		  "NOTE2" VARCHAR(20) , 
		  "NOTE3" VARCHAR(60) , 
		  "NOTE4" VARCHAR(60) )   
		 IN "AFA_DATA" INDEX IN "AFA_IDX" ; 


-- DDL Statements for primary key on Table "AFA     "."RCC_ZTCBKA"

ALTER TABLE "AFA     "."RCC_ZTCBKA" 
	ADD CONSTRAINT "RCC_ZTCBKA_PK" PRIMARY KEY
		("BJEDTE",
		 "BSPSQN",
		 "BRSFLG");



------------------------------------------------
-- DDL Statements for table "AFA     "."VOUH_FRONT_CRSBA"
------------------------------------------------
 

CREATE TABLE "AFA     "."VOUH_FRONT_CRSBA"  (
		  "SBSBTP" CHAR(1) , 
		  "SBSBCH" CHAR(2) , 
		  "SBCCCD" CHAR(4) , 
		  "SBBKCD" CHAR(3) , 
		  "SBSSNO" CHAR(6) , 
		  "SBSBNO" CHAR(10) , 
		  "SBSBSE" CHAR(4) , 
		  "SBSBLV" CHAR(1) , 
		  "SBSBNM" CHAR(40) , 
		  "SBEXNO" CHAR(9) , 
		  "SBADDR" CHAR(42) , 
		  "SBTLNO" CHAR(15) , 
		  "SBCUCN" CHAR(20) , 
		  "SBSEDT" DECIMAL(8,0) , 
		  "SBDDEV" CHAR(12) , 
		  "SBPRTQ" CHAR(14) , 
		  "SBTPSB" CHAR(10) , 
		  "SBTPAC" CHAR(10) , 
		  "SBCUTN" DECIMAL(4,0) , 
		  "SBTOTN" DECIMAL(4,0) , 
		  "SBBRNO" CHAR(5) , 
		  "SBCLSQ" CHAR(2) , 
		  "SBTSFG" CHAR(1) , 
		  "SBNTFG" CHAR(1) , 
		  "SBACFG" CHAR(1) , 
		  "SBEXDT" DECIMAL(8,0) , 
		  "SBSTCD" CHAR(1) )   
		 IN "AFA_DATA" ; 

COMMENT ON COLUMN "AFA     "."VOUH_FRONT_CRSBA"."SBACFG" IS '�Ƿ������ʻ���־';

COMMENT ON COLUMN "AFA     "."VOUH_FRONT_CRSBA"."SBADDR" IS '��ַ';

COMMENT ON COLUMN "AFA     "."VOUH_FRONT_CRSBA"."SBBKCD" IS '���д���';

COMMENT ON COLUMN "AFA     "."VOUH_FRONT_CRSBA"."SBBRNO" IS '�����к�';

COMMENT ON COLUMN "AFA     "."VOUH_FRONT_CRSBA"."SBCCCD" IS '�������Ĵ���';

COMMENT ON COLUMN "AFA     "."VOUH_FRONT_CRSBA"."SBCLSQ" IS '���ϼ������ʺ����';

COMMENT ON COLUMN "AFA     "."VOUH_FRONT_CRSBA"."SBCUCN" IS '��ϵ��';

COMMENT ON COLUMN "AFA     "."VOUH_FRONT_CRSBA"."SBCUTN" IS '��ǰ����';

COMMENT ON COLUMN "AFA     "."VOUH_FRONT_CRSBA"."SBDDEV" IS '�ͱ��豸��';

COMMENT ON COLUMN "AFA     "."VOUH_FRONT_CRSBA"."SBEXDT" IS '��������';

COMMENT ON COLUMN "AFA     "."VOUH_FRONT_CRSBA"."SBEXNO" IS '������';

COMMENT ON COLUMN "AFA     "."VOUH_FRONT_CRSBA"."SBNTFG" IS '�Ƿ�������־';

COMMENT ON COLUMN "AFA     "."VOUH_FRONT_CRSBA"."SBPRTQ" IS '��ӡ������';

COMMENT ON COLUMN "AFA     "."VOUH_FRONT_CRSBA"."SBSBCH" IS '��������';

COMMENT ON COLUMN "AFA     "."VOUH_FRONT_CRSBA"."SBSBLV" IS '��������';

COMMENT ON COLUMN "AFA     "."VOUH_FRONT_CRSBA"."SBSBNM" IS '����';

COMMENT ON COLUMN "AFA     "."VOUH_FRONT_CRSBA"."SBSBNO" IS '��������';

COMMENT ON COLUMN "AFA     "."VOUH_FRONT_CRSBA"."SBSBSE" IS '�������';

COMMENT ON COLUMN "AFA     "."VOUH_FRONT_CRSBA"."SBSBTP" IS '��������(0.����/1.����)';

COMMENT ON COLUMN "AFA     "."VOUH_FRONT_CRSBA"."SBSEDT" IS '����ʱ��';

COMMENT ON COLUMN "AFA     "."VOUH_FRONT_CRSBA"."SBSSNO" IS '�����־';

COMMENT ON COLUMN "AFA     "."VOUH_FRONT_CRSBA"."SBSTCD" IS '��¼״̬';

COMMENT ON COLUMN "AFA     "."VOUH_FRONT_CRSBA"."SBTLNO" IS '�绰����';

COMMENT ON COLUMN "AFA     "."VOUH_FRONT_CRSBA"."SBTOTN" IS '���ճ���';

COMMENT ON COLUMN "AFA     "."VOUH_FRONT_CRSBA"."SBTPAC" IS '�����ϼ�';

COMMENT ON COLUMN "AFA     "."VOUH_FRONT_CRSBA"."SBTPSB" IS '�����ϼ�';

COMMENT ON COLUMN "AFA     "."VOUH_FRONT_CRSBA"."SBTSFG" IS '�ս���';






------------------------------------------------
-- DDL Statements for table "AFA     "."RCC_PBDATA"
------------------------------------------------
 

CREATE TABLE "AFA     "."RCC_PBDATA"  (
		  "TRCDAT" VARCHAR(8) NOT NULL , 
		  "TRCNO" VARCHAR(8) NOT NULL , 
		  "SNDBNKCO" VARCHAR(10) NOT NULL , 
		  "NCCWKDAT" VARCHAR(8) , 
		  "TRCCO" VARCHAR(7) , 
		  "RCVBNKCO" VARCHAR(10) , 
		  "EFCTDAT" VARCHAR(8) , 
		  "PBDATYP" VARCHAR(3) , 
		  "PBDAFILE" VARCHAR(255) , 
		  "NOTE1" VARCHAR(10) , 
		  "NOTE2" VARCHAR(20) , 
		  "NOTE3" VARCHAR(60) , 
		  "NOTE4" VARCHAR(60) )   
		 IN "AFA_DATA" INDEX IN "AFA_IDX" ; 


-- DDL Statements for primary key on Table "AFA     "."RCC_PBDATA"

ALTER TABLE "AFA     "."RCC_PBDATA" 
	ADD CONSTRAINT "RCC_PBDATE_PK" PRIMARY KEY
		("TRCDAT",
		 "TRCNO",
		 "SNDBNKCO");



------------------------------------------------
-- DDL Statements for table "AFA     "."RCC_BILBKA"
------------------------------------------------
 

CREATE TABLE "AFA     "."RCC_BILBKA"  (
		  "BJEDTE" VARCHAR(8) NOT NULL , 
		  "BSPSQN" VARCHAR(12) NOT NULL , 
		  "BRSFLG" VARCHAR(1) NOT NULL , 
		  "BESBNO" VARCHAR(10) , 
		  "BEACSB" VARCHAR(10) , 
		  "BETELR" VARCHAR(6) , 
		  "BEAUUS" VARCHAR(6) , 
		  "TERMID" VARCHAR(20) NOT NULL , 
		  "BBSSRC" VARCHAR(1) NOT NULL , 
		  "DASQ" VARCHAR(10) , 
		  "DCFLG" VARCHAR(1) , 
		  "OPRATTNO" VARCHAR(2) , 
		  "NCCWKDAT" VARCHAR(8) , 
		  "TRCCO" VARCHAR(7) , 
		  "TRCDAT" VARCHAR(8) , 
		  "TRCNO" VARCHAR(8) , 
		  "SNDMBRCO" VARCHAR(10) , 
		  "RCVMBRCO" VARCHAR(10) , 
		  "SNDBNKCO" VARCHAR(10) , 
		  "SNDBNKNM" VARCHAR(60) , 
		  "RCVBNKCO" VARCHAR(10) , 
		  "RCVBNKNM" VARCHAR(60) , 
		  "BILVER" VARCHAR(2) , 
		  "BILNO" VARCHAR(8) , 
		  "CHRGTYP" VARCHAR(1) , 
		  "LOCCUSCHRG" DECIMAL(15,2) , 
		  "BILRS" VARCHAR(1) , 
		  "HPCUSQ" SMALLINT NOT NULL , 
		  "HPSTAT" VARCHAR(2) , 
		  "NOTE1" VARCHAR(10) , 
		  "NOTE2" VARCHAR(20) , 
		  "NOTE3" VARCHAR(60) , 
		  "NOTE4" VARCHAR(60) )   
		 IN "AFA_DATA" INDEX IN "AFA_IDX" ; 


-- DDL Statements for primary key on Table "AFA     "."RCC_BILBKA"

ALTER TABLE "AFA     "."RCC_BILBKA" 
	ADD CONSTRAINT "RCC_BILBKA_PK" PRIMARY KEY
		("BJEDTE",
		 "BSPSQN");



------------------------------------------------
-- DDL Statements for table "AFA     "."RCC_TRCBKA"
------------------------------------------------
 

CREATE TABLE "AFA     "."RCC_TRCBKA"  (
		  "BJEDTE" VARCHAR(8) NOT NULL , 
		  "BSPSQN" VARCHAR(12) NOT NULL , 
		  "BRSFLG" VARCHAR(1) NOT NULL , 
		  "BESBNO" VARCHAR(10) NOT NULL , 
		  "BEACSB" VARCHAR(10) , 
		  "BETELR" VARCHAR(6) NOT NULL , 
		  "BEAUUS" VARCHAR(6) , 
		  "TERMID" VARCHAR(20) , 
		  "BBSSRC" VARCHAR(1) NOT NULL , 
		  "DASQ" VARCHAR(10) , 
		  "DCFLG" VARCHAR(1) , 
		  "OPRNO" VARCHAR(2) , 
		  "OPRATTNO" VARCHAR(2) , 
		  "NCCWKDAT" VARCHAR(8) NOT NULL , 
		  "TRCCO" VARCHAR(7) NOT NULL , 
		  "TRCDAT" VARCHAR(8) , 
		  "TRCNO" VARCHAR(8) NOT NULL , 
		  "SNDMBRCO" VARCHAR(10) , 
		  "RCVMBRCO" VARCHAR(10) , 
		  "SNDBNKCO" VARCHAR(10) , 
		  "SNDBNKNM" VARCHAR(60) , 
		  "RCVBNKCO" VARCHAR(10) , 
		  "RCVBNKNM" VARCHAR(60) , 
		  "CUR" VARCHAR(3) NOT NULL , 
		  "OCCAMT" DECIMAL(15,2) NOT NULL , 
		  "CHRGTYP" VARCHAR(1) , 
		  "LOCCUSCHRG" DECIMAL(15,2) , 
		  "CUSCHRG" DECIMAL(15,2) , 
		  "PYRACC" VARCHAR(32) , 
		  "PYRNAM" VARCHAR(60) , 
		  "PYRADDR" VARCHAR(60) , 
		  "PYEACC" VARCHAR(32) , 
		  "PYENAM" VARCHAR(60) , 
		  "PYEADDR" VARCHAR(60) , 
		  "SEAL" VARCHAR(10) , 
		  "USE" VARCHAR(20) , 
		  "REMARK" VARCHAR(60) , 
		  "BILTYP" VARCHAR(2) , 
		  "BILDAT" VARCHAR(8) , 
		  "BILNO" VARCHAR(8) , 
		  "COMAMT" DECIMAL(15,2) , 
		  "OVPAYAMT" DECIMAL(15,2) , 
		  "CPSAMT" DECIMAL(15,2) , 
		  "RFUAMT" DECIMAL(15,2) , 
		  "CERTTYPE" VARCHAR(2) , 
		  "CERTNO" VARCHAR(20) , 
		  "BOJEDT" VARCHAR(8) , 
		  "BOSPSQ" VARCHAR(12) , 
		  "ORTRCDAT" VARCHAR(10) , 
		  "ORTRCCO" VARCHAR(7) , 
		  "ORTRCNO" VARCHAR(8) , 
		  "ORSNDBNK" VARCHAR(10) , 
		  "ORRCVBNK" VARCHAR(10) , 
		  "STRINFO" VARCHAR(60) , 
		  "NOTE1" VARCHAR(10) , 
		  "NOTE2" VARCHAR(20) , 
		  "NOTE3" VARCHAR(60) , 
		  "NOTE4" VARCHAR(60) )   
		 IN "AFA_DATA" INDEX IN "AFA_IDX" ; 


-- DDL Statements for primary key on Table "AFA     "."RCC_TRCBKA"

ALTER TABLE "AFA     "."RCC_TRCBKA" 
	ADD CONSTRAINT "RCC_TRCBKA_PK" PRIMARY KEY
		("BJEDTE",
		 "BSPSQN");



------------------------------------------------
-- DDL Statements for table "AFA     "."RCC_PAYBNK"
------------------------------------------------
 

CREATE TABLE "AFA     "."RCC_PAYBNK"  (
		  "BANKBIN" VARCHAR(10) NOT NULL , 
		  "BANKSTATUS" VARCHAR(1) , 
		  "BANKATTR" VARCHAR(2) , 
		  "STLBANKBIN" VARCHAR(10) , 
		  "BANKNAM" VARCHAR(60) , 
		  "BANKADDR" VARCHAR(60) , 
		  "BANKPC" VARCHAR(6) , 
		  "BANKTEL" VARCHAR(30) , 
		  "EFCTDAT" VARCHAR(8) , 
		  "INVDAT" VARCHAR(8) , 
		  "ALTTYPE" VARCHAR(1) , 
		  "PRIVILEGE" VARCHAR(20) , 
		  "NEWOFLG" VARCHAR(1) , 
		  "STRINFO" VARCHAR(60) , 
		  "NOTE1" VARCHAR(10) , 
		  "NOTE2" VARCHAR(20) , 
		  "NOTE3" VARCHAR(60) , 
		  "NOTE4" VARCHAR(60) )   
		 IN "AFA_DATA" INDEX IN "AFA_IDX" ; 


-- DDL Statements for primary key on Table "AFA     "."RCC_PAYBNK"

ALTER TABLE "AFA     "."RCC_PAYBNK" 
	ADD CONSTRAINT "RCC_PAYBNK_PK" PRIMARY KEY
		("BANKBIN");



------------------------------------------------
-- DDL Statements for table "AFA     "."RCC_BILINF"
------------------------------------------------
 

CREATE TABLE "AFA     "."RCC_BILINF"  (
		  "BILVER" VARCHAR(2) NOT NULL , 
		  "BILNO" VARCHAR(8) NOT NULL , 
		  "BILRS" VARCHAR(1) NOT NULL , 
		  "BILTYP" VARCHAR(2) , 
		  "BILDAT" VARCHAR(8) , 
		  "PAYWAY" VARCHAR(1) , 
		  "REMBNKCO" VARCHAR(10) , 
		  "REMBNKNM" VARCHAR(60) , 
		  "PAYBNKCO" VARCHAR(10) , 
		  "PAYBNKNM" VARCHAR(60) , 
		  "PYRACC" VARCHAR(32) , 
		  "PYRNAM" VARCHAR(60) , 
		  "PYRADDR" VARCHAR(60) , 
		  "PYEACC" VARCHAR(32) , 
		  "PYENAM" VARCHAR(60) , 
		  "PYEADDR" VARCHAR(60) , 
		  "PYHACC" VARCHAR(32) , 
		  "PYHNAM" VARCHAR(60) , 
		  "PYHADDR" VARCHAR(60) , 
		  "PYITYP" VARCHAR(1) , 
		  "PYIACC" VARCHAR(32) , 
		  "PYINAM" VARCHAR(60) , 
		  "BILAMT" DECIMAL(15,2) , 
		  "OCCAMT" DECIMAL(15,2) , 
		  "RMNAMT" DECIMAL(15,2) , 
		  "CUR" VARCHAR(3) , 
		  "SEAL" VARCHAR(10) , 
		  "USE" VARCHAR(20) , 
		  "REMARK" VARCHAR(30) , 
		  "HPCUSQ" SMALLINT NOT NULL , 
		  "HPSTAT" VARCHAR(2) , 
		  "NOTE1" VARCHAR(10) , 
		  "NOTE2" VARCHAR(20) , 
		  "NOTE3" VARCHAR(60) , 
		  "NOTE4" VARCHAR(60) )   
		 IN "AFA_DATA" ; 

COMMENT ON COLUMN "AFA     "."RCC_BILINF"."PAYBNKCO" IS '���������к�';

COMMENT ON COLUMN "AFA     "."RCC_BILINF"."PAYBNKNM" IS '������������';

COMMENT ON COLUMN "AFA     "."RCC_BILINF"."REMBNKCO" IS '��Ʊ���к�';

COMMENT ON COLUMN "AFA     "."RCC_BILINF"."REMBNKNM" IS '��Ʊ������';


-- DDL Statements for primary key on Table "AFA     "."RCC_BILINF"

ALTER TABLE "AFA     "."RCC_BILINF" 
	ADD CONSTRAINT "RCC_BILINF_PK" PRIMARY KEY
		("BILVER",
		 "BILNO",
		 "BILRS");



------------------------------------------------
-- DDL Statements for table "AFA     "."VOUH_MODIFY"
------------------------------------------------
 

CREATE TABLE "AFA     "."VOUH_MODIFY"  (
		  "VOUHSERIAL" VARCHAR(8) NOT NULL , 
		  "WORKDATE" VARCHAR(8) , 
		  "VOUHNUM" VARCHAR(10) , 
		  "WORKTIME" VARCHAR(6) , 
		  "BESBNO" VARCHAR(10) NOT NULL , 
		  "TELLERNO" VARCHAR(10) , 
		  "CUR" VARCHAR(2) , 
		  "VOUHTYPE" VARCHAR(10) NOT NULL , 
		  "STARTNO" VARCHAR(20) , 
		  "ENDNO" VARCHAR(20) , 
		  "RIVTELLER" VARCHAR(10) , 
		  "DEPOSITORY" VARCHAR(1) , 
		  "EXDEPOS" VARCHAR(1) , 
		  "VOUHSTATUS" VARCHAR(1) , 
		  "EXSTATUS" VARCHAR(1) , 
		  "TRANSTYPE" VARCHAR(20) )   
		 IN "AFA_DATA" ; 

COMMENT ON COLUMN "AFA     "."VOUH_MODIFY"."BESBNO" IS '������';

COMMENT ON COLUMN "AFA     "."VOUH_MODIFY"."CUR" IS '���Ҵ���';

COMMENT ON COLUMN "AFA     "."VOUH_MODIFY"."DEPOSITORY" IS '�����־';

COMMENT ON COLUMN "AFA     "."VOUH_MODIFY"."ENDNO" IS '��ֹ����';

COMMENT ON COLUMN "AFA     "."VOUH_MODIFY"."EXDEPOS" IS 'ԭ�����־';

COMMENT ON COLUMN "AFA     "."VOUH_MODIFY"."EXSTATUS" IS 'ԭ״̬';

COMMENT ON COLUMN "AFA     "."VOUH_MODIFY"."RIVTELLER" IS '�Է���Ա';

COMMENT ON COLUMN "AFA     "."VOUH_MODIFY"."STARTNO" IS '��ʼ����';

COMMENT ON COLUMN "AFA     "."VOUH_MODIFY"."TELLERNO" IS '��Ա��';

COMMENT ON COLUMN "AFA     "."VOUH_MODIFY"."TRANSTYPE" IS '�������';

COMMENT ON COLUMN "AFA     "."VOUH_MODIFY"."VOUHNUM" IS 'ƾ֤����';

COMMENT ON COLUMN "AFA     "."VOUH_MODIFY"."VOUHSERIAL" IS 'ƾ֤��ˮ��';

COMMENT ON COLUMN "AFA     "."VOUH_MODIFY"."VOUHSTATUS" IS '״̬';

COMMENT ON COLUMN "AFA     "."VOUH_MODIFY"."VOUHTYPE" IS 'ƾ֤����';

COMMENT ON COLUMN "AFA     "."VOUH_MODIFY"."WORKDATE" IS '��������';

COMMENT ON COLUMN "AFA     "."VOUH_MODIFY"."WORKTIME" IS '����ʱ��';






------------------------------------------------
-- DDL Statements for table "AFA     "."AFA_TEST1"
------------------------------------------------
 

CREATE TABLE "AFA     "."AFA_TEST1"  (
		  "NOTE1" CHAR(30) , 
		  "NOTE2" CHAR(30) )   
		 IN "AFA_DATA" ; 






------------------------------------------------
-- DDL Statements for table "AFA     "."AFA_TEST2"
------------------------------------------------
 

CREATE TABLE "AFA     "."AFA_TEST2"  (
		  "NOTE1" CHAR(30) , 
		  "NOTE2" CHAR(30) )   
		 IN "AFA_DATA" ; 






------------------------------------------------
-- DDL Statements for table "AFA     "."RCC_MRQTBL"
------------------------------------------------
 

CREATE TABLE "AFA     "."RCC_MRQTBL"  (
		  "BJEDTE" VARCHAR(8) NOT NULL , 
		  "BSPSQN" VARCHAR(12) NOT NULL , 
		  "TRCCO" VARCHAR(8) , 
		  "SNDBNKCO" VARCHAR(10) , 
		  "SNDBNKNM" VARCHAR(60) , 
		  "RCVBNKCO" VARCHAR(10) , 
		  "RCVBNKNM" VARCHAR(60) , 
		  "SNDMBRCO" VARCHAR(10) , 
		  "RCVMBRCO" VARCHAR(10) , 
		  "TRCDAT" VARCHAR(8) , 
		  "TRCNO" VARCHAR(8) , 
		  "NPCBKID" VARCHAR(12) , 
		  "NPCBKNM" VARCHAR(60) , 
		  "NPCACNT" VARCHAR(32) , 
		  "OCCAMT" DECIMAL(15,2) , 
		  "REMARK" VARCHAR(60) , 
		  "PRCCO" VARCHAR(8) , 
		  "STRINFO" VARCHAR(60) , 
		  "NOTE1" VARCHAR(10) , 
		  "NOTE2" VARCHAR(20) , 
		  "NOTE3" VARCHAR(60) , 
		  "NOTE4" VARCHAR(60) )   
		 IN "AFA_DATA" INDEX IN "AFA_IDX" ; 


-- DDL Statements for primary key on Table "AFA     "."RCC_MRQTBL"

ALTER TABLE "AFA     "."RCC_MRQTBL" 
	ADD CONSTRAINT "RCC_MRQTBL_PK" PRIMARY KEY
		("BJEDTE",
		 "BSPSQN");



------------------------------------------------
-- DDL Statements for table "AFA     "."RCC_TRCCAN"
------------------------------------------------
 

CREATE TABLE "AFA     "."RCC_TRCCAN"  (
		  "BJEDTE" VARCHAR(8) NOT NULL , 
		  "BSPSQN" VARCHAR(12) NOT NULL , 
		  "BRSFLG" VARCHAR(1) , 
		  "BESBNO" VARCHAR(10) , 
		  "BETELR" VARCHAR(6) , 
		  "BEAUUS" VARCHAR(6) , 
		  "NCCWKDAT" VARCHAR(8) , 
		  "TRCCO" VARCHAR(7) , 
		  "TRCDAT" VARCHAR(8) , 
		  "TRCNO" VARCHAR(8) , 
		  "SNDMBRCO" VARCHAR(10) , 
		  "RCVMBRCO" VARCHAR(10) , 
		  "SNDBNKCO" VARCHAR(10) , 
		  "SNDBNKNM" VARCHAR(60) , 
		  "RCVBNKCO" VARCHAR(10) , 
		  "RCVBNKNM" VARCHAR(60) , 
		  "BOJEDT" VARCHAR(8) , 
		  "BOSPSQ" VARCHAR(12) , 
		  "ORTRCCO" VARCHAR(7) , 
		  "CUR" VARCHAR(3) , 
		  "OCCAMT" DECIMAL(15,2) , 
		  "CONT" VARCHAR(255) , 
		  "CLRESPN" VARCHAR(1) , 
		  "PRCCO" VARCHAR(8) , 
		  "STRINFO" VARCHAR(60) , 
		  "NOTE1" VARCHAR(10) , 
		  "NOTE2" VARCHAR(20) , 
		  "NOTE3" VARCHAR(60) , 
		  "NOTE4" VARCHAR(60) )   
		 IN "AFA_DATA" INDEX IN "AFA_IDX" ; 


-- DDL Statements for primary key on Table "AFA     "."RCC_TRCCAN"

ALTER TABLE "AFA     "."RCC_TRCCAN" 
	ADD CONSTRAINT "RCC_TRCCAN_PK" PRIMARY KEY
		("BJEDTE",
		 "BSPSQN");



------------------------------------------------
-- DDL Statements for table "AFA     "."RCC_EXISTP"
------------------------------------------------
 

CREATE TABLE "AFA     "."RCC_EXISTP"  (
		  "BJEDTE" VARCHAR(8) NOT NULL , 
		  "BSPSQN" VARCHAR(12) NOT NULL , 
		  "BRSFLG" VARCHAR(1) , 
		  "BESBNO" VARCHAR(10) , 
		  "BETELR" VARCHAR(6) , 
		  "BEAUUS" VARCHAR(6) , 
		  "NCCWKDAT" VARCHAR(8) , 
		  "TRCCO" VARCHAR(7) , 
		  "TRCDAT" VARCHAR(8) , 
		  "TRCNO" VARCHAR(8) , 
		  "SNDMBRCO" VARCHAR(10) , 
		  "RCVMBRCO" VARCHAR(10) , 
		  "SNDBNKCO" VARCHAR(10) , 
		  "SNDBNKNM" VARCHAR(60) , 
		  "RCVBNKCO" VARCHAR(10) , 
		  "RCVBNKNM" VARCHAR(60) , 
		  "BOJEDT" VARCHAR(8) , 
		  "BOSPSQ" VARCHAR(12) , 
		  "ORTRCCO" VARCHAR(7) , 
		  "CUR" VARCHAR(3) , 
		  "OCCAMT" DECIMAL(15,2) , 
		  "CONT" VARCHAR(255) , 
		  "PRCCO" VARCHAR(8) , 
		  "STRINFO" VARCHAR(60) , 
		  "NOTE1" VARCHAR(10) , 
		  "NOTE2" VARCHAR(20) , 
		  "NOTE3" VARCHAR(60) , 
		  "NOTE4" VARCHAR(60) )   
		 IN "AFA_DATA" INDEX IN "AFA_IDX" ; 


-- DDL Statements for primary key on Table "AFA     "."RCC_EXISTP"

ALTER TABLE "AFA     "."RCC_EXISTP" 
	ADD CONSTRAINT "RCC_EXISTP_PK" PRIMARY KEY
		("BJEDTE",
		 "BSPSQN");









COMMIT WORK;

CONNECT RESET;

TERMINATE;

