-- This CLP file was created using DB2LOOK Version 9.1
-- Timestamp: ��Ԫ2008��08��07��  ������  15ʱ59��18��
-- Database Name: AFA            
-- Database Manager Version: DB2/AIX64 Version 9.1.0       
-- Database Codepage: 1386
-- Database Collating Sequence is: UNIQUE


--CONNECT TO AFA USER AFA USING AFA;



---------------------------------
-- DDL Statements for Sequences
---------------------------------

CREATE SEQUENCE "AFA     "."RCC_SEQ" AS INTEGER
	MINVALUE 1 MAXVALUE 99999999
	START WITH 1 INCREMENT BY 1
	CACHE 10 CYCLE NO ORDER;

ALTER SEQUENCE "AFA     "."RCC_SEQ" RESTART WITH 183819;

CREATE SEQUENCE "AFA     "."RCCPS_SEQ" AS INTEGER
	MINVALUE 1 MAXVALUE 999999
	START WITH 1 INCREMENT BY 1
	CACHE 10 CYCLE NO ORDER;

ALTER SEQUENCE "AFA     "."RCCPS_SEQ" RESTART WITH 191679;

CREATE SEQUENCE "AFA     "."TYHD_SEQ" AS INTEGER
	MINVALUE 1 MAXVALUE 9999
	START WITH 1 INCREMENT BY 1
	CACHE 10 CYCLE NO ORDER;


------------------------------------------------
-- DDL Statements for table "AFA     "."RCC_HPCBKA"
------------------------------------------------
DROP TABLE "AFA     "."RCC_HPCBKA";

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
		  "STRINFO" VARCHAR(60) , 
		  "NOTE1" VARCHAR(10) , 
		  "NOTE2" VARCHAR(20) , 
		  "NOTE3" VARCHAR(60) , 
		  "NOTE4" VARCHAR(60) )   
		 IN "AFA_DATA" INDEX IN "AFA_IDX" ; 

COMMENT ON COLUMN "AFA     "."RCC_HPCBKA"."BEAUUS" IS '��Ȩ��Ա��';

COMMENT ON COLUMN "AFA     "."RCC_HPCBKA"."BESBNO" IS '������';

COMMENT ON COLUMN "AFA     "."RCC_HPCBKA"."BETELR" IS '��Ա��';

COMMENT ON COLUMN "AFA     "."RCC_HPCBKA"."BILAMT" IS '��Ʊ���';

COMMENT ON COLUMN "AFA     "."RCC_HPCBKA"."BILDAT" IS '��Ʊ����';

COMMENT ON COLUMN "AFA     "."RCC_HPCBKA"."BILNO" IS '��Ʊ����';

COMMENT ON COLUMN "AFA     "."RCC_HPCBKA"."BILVER" IS '��Ʊ�汾��';

COMMENT ON COLUMN "AFA     "."RCC_HPCBKA"."BJEDTE" IS '��������';

COMMENT ON COLUMN "AFA     "."RCC_HPCBKA"."BOJEDT" IS 'ԭ��������';

COMMENT ON COLUMN "AFA     "."RCC_HPCBKA"."BOSPSQ" IS 'ԭ�������';

COMMENT ON COLUMN "AFA     "."RCC_HPCBKA"."BRSFLG" IS '������ʶ(0-����;1-����)';

COMMENT ON COLUMN "AFA     "."RCC_HPCBKA"."BSPSQN" IS '�������';

COMMENT ON COLUMN "AFA     "."RCC_HPCBKA"."CONT" IS '����';

COMMENT ON COLUMN "AFA     "."RCC_HPCBKA"."CUR" IS '����';

COMMENT ON COLUMN "AFA     "."RCC_HPCBKA"."ISDEAL" IS '��ѯ�鸴��ʶ(0-δ�鸴;1-�Ѳ鸴)';

COMMENT ON COLUMN "AFA     "."RCC_HPCBKA"."NCCWKDAT" IS '��������';

COMMENT ON COLUMN "AFA     "."RCC_HPCBKA"."NOTE1" IS '�����ֶ�1';

COMMENT ON COLUMN "AFA     "."RCC_HPCBKA"."NOTE2" IS '�����ֶ�2';

COMMENT ON COLUMN "AFA     "."RCC_HPCBKA"."NOTE3" IS '�����ֶ�3';

COMMENT ON COLUMN "AFA     "."RCC_HPCBKA"."NOTE4" IS '�����ֶ�4';

COMMENT ON COLUMN "AFA     "."RCC_HPCBKA"."ORTRCCO" IS 'ԭ���״���';

COMMENT ON COLUMN "AFA     "."RCC_HPCBKA"."PAYWAY" IS '�Ҹ���ʽ';

COMMENT ON COLUMN "AFA     "."RCC_HPCBKA"."PRCCO" IS '���ķ��ش���';

COMMENT ON COLUMN "AFA     "."RCC_HPCBKA"."PYEACC" IS '�տ����˺�';

COMMENT ON COLUMN "AFA     "."RCC_HPCBKA"."PYENAM" IS '�տ��˻���';

COMMENT ON COLUMN "AFA     "."RCC_HPCBKA"."PYRACC" IS '��Ʊ���˺�';

COMMENT ON COLUMN "AFA     "."RCC_HPCBKA"."PYRNAM" IS '��Ʊ�˻���';

COMMENT ON COLUMN "AFA     "."RCC_HPCBKA"."RCVBNKCO" IS '�������к�';

COMMENT ON COLUMN "AFA     "."RCC_HPCBKA"."RCVBNKNM" IS '����������';

COMMENT ON COLUMN "AFA     "."RCC_HPCBKA"."RCVMBRCO" IS '���ճ�Ա�к�';

COMMENT ON COLUMN "AFA     "."RCC_HPCBKA"."SNDBNKCO" IS '�������к�';

COMMENT ON COLUMN "AFA     "."RCC_HPCBKA"."SNDBNKNM" IS '����������';

COMMENT ON COLUMN "AFA     "."RCC_HPCBKA"."SNDMBRCO" IS '���ͳ�Ա�к�';

COMMENT ON COLUMN "AFA     "."RCC_HPCBKA"."STRINFO" IS '���ķ��ش���˵��';

COMMENT ON COLUMN "AFA     "."RCC_HPCBKA"."TRCCO" IS '���״���';

COMMENT ON COLUMN "AFA     "."RCC_HPCBKA"."TRCDAT" IS '��������';

COMMENT ON COLUMN "AFA     "."RCC_HPCBKA"."TRCNO" IS '������ˮ��';


-- DDL Statements for primary key on Table "AFA     "."RCC_HPCBKA"

ALTER TABLE "AFA     "."RCC_HPCBKA" 
	ADD CONSTRAINT "RCC_HPCBKA_PK" PRIMARY KEY
		("BJEDTE",
		 "BSPSQN");



------------------------------------------------
-- DDL Statements for table "AFA     "."RCC_ATRCHK"
------------------------------------------------
DROP TABLE "AFA     "."RCC_ATRCHK";

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

COMMENT ON COLUMN "AFA     "."RCC_ATRCHK"."CUR" IS '����';

COMMENT ON COLUMN "AFA     "."RCC_ATRCHK"."NOTE1" IS '�����ֶ�1';

COMMENT ON COLUMN "AFA     "."RCC_ATRCHK"."NOTE2" IS '�����ֶ�2';

COMMENT ON COLUMN "AFA     "."RCC_ATRCHK"."NOTE3" IS '�����ֶ�3';

COMMENT ON COLUMN "AFA     "."RCC_ATRCHK"."NOTE4" IS '�����ֶ�4';

COMMENT ON COLUMN "AFA     "."RCC_ATRCHK"."RCTAMT" IS '���˴����ܽ��';

COMMENT ON COLUMN "AFA     "."RCC_ATRCHK"."RCTCNT" IS '���˴����ܱ���';

COMMENT ON COLUMN "AFA     "."RCC_ATRCHK"."RCVBNKCO" IS '�������к�';

COMMENT ON COLUMN "AFA     "."RCC_ATRCHK"."RDTAMT" IS '���˽���ܽ��';

COMMENT ON COLUMN "AFA     "."RCC_ATRCHK"."RDTCNT" IS '���˽���ܱ���';

COMMENT ON COLUMN "AFA     "."RCC_ATRCHK"."ROPRTPNO" IS 'ԭҵ������';

COMMENT ON COLUMN "AFA     "."RCC_ATRCHK"."SCTAMT" IS '���˴����ܽ��';

COMMENT ON COLUMN "AFA     "."RCC_ATRCHK"."SCTCNT" IS '���˴����ܱ���';

COMMENT ON COLUMN "AFA     "."RCC_ATRCHK"."SDTAMT" IS '���˽���ܽ��';

COMMENT ON COLUMN "AFA     "."RCC_ATRCHK"."SDTCNT" IS '���˽���ܱ���';

COMMENT ON COLUMN "AFA     "."RCC_ATRCHK"."SNDBNKCO" IS '�������к�';

COMMENT ON COLUMN "AFA     "."RCC_ATRCHK"."TRCCO" IS '���״���';

COMMENT ON COLUMN "AFA     "."RCC_ATRCHK"."TRCDAT" IS 'ί������';

COMMENT ON COLUMN "AFA     "."RCC_ATRCHK"."TRCNO" IS '������ˮ��';


-- DDL Statements for primary key on Table "AFA     "."RCC_ATRCHK"

ALTER TABLE "AFA     "."RCC_ATRCHK" 
	ADD CONSTRAINT "RCC_ATRCHK_PK" PRIMARY KEY
		("SNDBNKCO",
		 "TRCDAT",
		 "TRCNO");


------------------------------------------------
-- DDL Statements for table "AFA     "."RCC_CADBNK"
------------------------------------------------
DROP TABLE "AFA     "."RCC_ATRCHK";

CREATE TABLE "AFA     "."RCC_CADBNK"  (
		  "CARDBIN" VARCHAR(8) NOT NULL , 
		  "BANKBIN" VARCHAR(10) NOT NULL , 
		  "NOTE1" VARCHAR(10) , 
		  "NOTE2" VARCHAR(20) , 
		  "NOTE3" VARCHAR(60) , 
		  "NOTE4" VARCHAR(60) )   
		 IN "AFA_DATA" INDEX IN "AFA_IDX" ; 

COMMENT ON COLUMN "AFA     "."RCC_CADBNK"."BANKBIN" IS '�к�';

COMMENT ON COLUMN "AFA     "."RCC_CADBNK"."CARDBIN" IS '��BIN';

COMMENT ON COLUMN "AFA     "."RCC_CADBNK"."NOTE1" IS '�����ֶ�1';

COMMENT ON COLUMN "AFA     "."RCC_CADBNK"."NOTE2" IS '�����ֶ�2';

COMMENT ON COLUMN "AFA     "."RCC_CADBNK"."NOTE3" IS '�����ֶ�3';

COMMENT ON COLUMN "AFA     "."RCC_CADBNK"."NOTE4" IS '�����ֶ�4';


-- DDL Statements for primary key on Table "AFA     "."RCC_CADBNK"

ALTER TABLE "AFA     "."RCC_CADBNK" 
	ADD CONSTRAINT "RCC_CADBNK_PK" PRIMARY KEY
		("CARDBIN");


------------------------------------------------
-- DDL Statements for table "AFA     "."RCC_CSHALM"
------------------------------------------------
DROP TABLE "AFA     "."RCC_CSHALM";

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

COMMENT ON COLUMN "AFA     "."RCC_CSHALM"."BJEDTE" IS '��������';

COMMENT ON COLUMN "AFA     "."RCC_CSHALM"."BSPSQN" IS '�������';

COMMENT ON COLUMN "AFA     "."RCC_CSHALM"."CUR" IS '����';

COMMENT ON COLUMN "AFA     "."RCC_CSHALM"."NCCWKDAT" IS '��������';

COMMENT ON COLUMN "AFA     "."RCC_CSHALM"."NOTE1" IS '�����ֶ�1';

COMMENT ON COLUMN "AFA     "."RCC_CSHALM"."NOTE2" IS '�����ֶ�2';

COMMENT ON COLUMN "AFA     "."RCC_CSHALM"."NOTE3" IS '�����ֶ�3';

COMMENT ON COLUMN "AFA     "."RCC_CSHALM"."NOTE4" IS '�����ֶ�4';

COMMENT ON COLUMN "AFA     "."RCC_CSHALM"."POSALAMT" IS 'ͷ��Ԥ�����';

COMMENT ON COLUMN "AFA     "."RCC_CSHALM"."POSITION" IS 'ͷ�統ǰ���';

COMMENT ON COLUMN "AFA     "."RCC_CSHALM"."RCVBNKCO" IS '�������к�';

COMMENT ON COLUMN "AFA     "."RCC_CSHALM"."RCVBNKNM" IS '����������';

COMMENT ON COLUMN "AFA     "."RCC_CSHALM"."SNDBNKCO" IS '�������к�';

COMMENT ON COLUMN "AFA     "."RCC_CSHALM"."SNDBNKNM" IS '����������';

COMMENT ON COLUMN "AFA     "."RCC_CSHALM"."TRCCO" IS '���״���';

COMMENT ON COLUMN "AFA     "."RCC_CSHALM"."TRCDAT" IS '��������';

COMMENT ON COLUMN "AFA     "."RCC_CSHALM"."TRCNO" IS '������ˮ��';


-- DDL Statements for primary key on Table "AFA     "."RCC_CSHALM"

ALTER TABLE "AFA     "."RCC_CSHALM" 
	ADD CONSTRAINT "RCC_CSHALM_PK" PRIMARY KEY
		("BJEDTE",
		 "BSPSQN");


------------------------------------------------
-- DDL Statements for table "AFA     "."RCC_ERRINF"
------------------------------------------------
DROP TABLE "AFA     "."RCC_ERRINF";

CREATE TABLE "AFA     "."RCC_ERRINF"  (
		  "MBRTYP" VARCHAR(1) NOT NULL , 
		  "ERRKEY" VARCHAR(8) NOT NULL , 
		  "ERRSTR" VARCHAR(255) , 
		  "NOTE1" VARCHAR(10) , 
		  "NOTE2" VARCHAR(20) , 
		  "NOTE3" VARCHAR(60) , 
		  "NOTE4" VARCHAR(60) )   
		 IN "AFA_DATA" INDEX IN "AFA_IDX" ; 

COMMENT ON COLUMN "AFA     "."RCC_ERRINF"."ERRKEY" IS '���ķ��ش���';

COMMENT ON COLUMN "AFA     "."RCC_ERRINF"."ERRSTR" IS '���ķ��ش���˵��';

COMMENT ON COLUMN "AFA     "."RCC_ERRINF"."MBRTYP" IS '��Ա������';

COMMENT ON COLUMN "AFA     "."RCC_ERRINF"."NOTE1" IS '�����ֶ�1';

COMMENT ON COLUMN "AFA     "."RCC_ERRINF"."NOTE2" IS '�����ֶ�2';

COMMENT ON COLUMN "AFA     "."RCC_ERRINF"."NOTE3" IS '�����ֶ�3';

COMMENT ON COLUMN "AFA     "."RCC_ERRINF"."NOTE4" IS '�����ֶ�4';


-- DDL Statements for primary key on Table "AFA     "."RCC_ERRINF"

ALTER TABLE "AFA     "."RCC_ERRINF" 
	ADD CONSTRAINT "RCC_ERRINF_PK" PRIMARY KEY
		("MBRTYP",
		 "ERRKEY");


------------------------------------------------
-- DDL Statements for table "AFA     "."RCC_HDDZCZ"
------------------------------------------------
DROP TABLE "AFA     "."RCC_HDDZCZ";

CREATE TABLE "AFA     "."RCC_HDDZCZ"  (
		  "SNDBNKCO" VARCHAR(10) NOT NULL , 
		  "TRCDAT" VARCHAR(8) NOT NULL , 
		  "TRCNO" VARCHAR(8) NOT NULL , 
		  "NCCWKDAT" VARCHAR(8) , 
		  "BJEDTE" VARCHAR(8) , 
		  "BSPSQN" VARCHAR(12) , 
		  "EACTYP" VARCHAR(2) , 
		  "EACINF" VARCHAR(60) , 
		  "ISDEAL" VARCHAR(1) , 
		  "NOTE1" VARCHAR(10) , 
		  "NOTE2" VARCHAR(20) , 
		  "NOTE3" VARCHAR(60) , 
		  "NOTE4" VARCHAR(60) )   
		 IN "AFA_DATA" INDEX IN "AFA_IDX" ; 

COMMENT ON COLUMN "AFA     "."RCC_HDDZCZ"."BJEDTE" IS '��������';

COMMENT ON COLUMN "AFA     "."RCC_HDDZCZ"."BSPSQN" IS '�������';

COMMENT ON COLUMN "AFA     "."RCC_HDDZCZ"."EACINF" IS '��������˵��';

COMMENT ON COLUMN "AFA     "."RCC_HDDZCZ"."EACTYP" IS '��������';

COMMENT ON COLUMN "AFA     "."RCC_HDDZCZ"."ISDEAL" IS '�����ʶ';

COMMENT ON COLUMN "AFA     "."RCC_HDDZCZ"."NCCWKDAT" IS '��������';

COMMENT ON COLUMN "AFA     "."RCC_HDDZCZ"."NOTE1" IS '�����ֶ�1';

COMMENT ON COLUMN "AFA     "."RCC_HDDZCZ"."NOTE2" IS '�����ֶ�2';

COMMENT ON COLUMN "AFA     "."RCC_HDDZCZ"."NOTE3" IS '�����ֶ�3';

COMMENT ON COLUMN "AFA     "."RCC_HDDZCZ"."NOTE4" IS '�����ֶ�4';

COMMENT ON COLUMN "AFA     "."RCC_HDDZCZ"."SNDBNKCO" IS '�������к�';

COMMENT ON COLUMN "AFA     "."RCC_HDDZCZ"."TRCDAT" IS 'ί������';

COMMENT ON COLUMN "AFA     "."RCC_HDDZCZ"."TRCNO" IS '������ˮ��';





------------------------------------------------
-- DDL Statements for table "AFA     "."RCC_HDDZHZ"
------------------------------------------------
DROP TABLE "AFA     "."RCC_HDDZHZ";

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

COMMENT ON COLUMN "AFA     "."RCC_HDDZHZ"."BRSFLG" IS '������ʶ(0-����;1-����)';

COMMENT ON COLUMN "AFA     "."RCC_HDDZHZ"."CTAMT" IS '�������ܽ��';

COMMENT ON COLUMN "AFA     "."RCC_HDDZHZ"."DTAMT" IS '�跽���ܽ��';

COMMENT ON COLUMN "AFA     "."RCC_HDDZHZ"."NCCWKDAT" IS '��������';

COMMENT ON COLUMN "AFA     "."RCC_HDDZHZ"."NOTE1" IS '�����ֶ�1';

COMMENT ON COLUMN "AFA     "."RCC_HDDZHZ"."NOTE2" IS '�����ֶ�2';

COMMENT ON COLUMN "AFA     "."RCC_HDDZHZ"."NOTE3" IS '�����ֶ�3';

COMMENT ON COLUMN "AFA     "."RCC_HDDZHZ"."NOTE4" IS '�����ֶ�4';

COMMENT ON COLUMN "AFA     "."RCC_HDDZHZ"."OFSTAMT" IS '������ܽ��';

COMMENT ON COLUMN "AFA     "."RCC_HDDZHZ"."TCNT" IS '���ܱ���';

COMMENT ON COLUMN "AFA     "."RCC_HDDZHZ"."TRCCO" IS '���״���';

COMMENT ON COLUMN "AFA     "."RCC_HDDZHZ"."TRCNAM" IS '��������';

COMMENT ON COLUMN "AFA     "."RCC_HDDZHZ"."TRCRSNM" IS '������ʶ����˵��';


-- DDL Statements for primary key on Table "AFA     "."RCC_HDDZHZ"

ALTER TABLE "AFA     "."RCC_HDDZHZ" 
	ADD CONSTRAINT "RCC_HDDZHZ_PK" PRIMARY KEY
		("NCCWKDAT",
		 "TRCCO",
		 "BRSFLG");


------------------------------------------------
-- DDL Statements for table "AFA     "."RCC_HPDZCZ"
------------------------------------------------
DROP TABLE "AFA     "."RCC_HPDZCZ";

CREATE TABLE "AFA     "."RCC_HPDZCZ"  (
		  "SNDBNKCO" VARCHAR(10) NOT NULL , 
		  "TRCDAT" VARCHAR(8) NOT NULL , 
		  "TRCNO" VARCHAR(8) NOT NULL , 
		  "NCCWKDAT" VARCHAR(8) , 
		  "BJEDTE" VARCHAR(8) , 
		  "BSPSQN" VARCHAR(12) , 
		  "EACTYP" VARCHAR(2) , 
		  "EACINF" VARCHAR(60) , 
		  "ISDEAL" VARCHAR(1) , 
		  "NOTE1" VARCHAR(10) , 
		  "NOTE2" VARCHAR(20) , 
		  "NOTE3" VARCHAR(60) , 
		  "NOTE4" VARCHAR(60) )   
		 IN "AFA_DATA" INDEX IN "AFA_IDX" ; 

COMMENT ON COLUMN "AFA     "."RCC_HPDZCZ"."BJEDTE" IS '��������';

COMMENT ON COLUMN "AFA     "."RCC_HPDZCZ"."BSPSQN" IS '�������';

COMMENT ON COLUMN "AFA     "."RCC_HPDZCZ"."EACINF" IS '��������˵��';

COMMENT ON COLUMN "AFA     "."RCC_HPDZCZ"."EACTYP" IS '��������';

COMMENT ON COLUMN "AFA     "."RCC_HPDZCZ"."ISDEAL" IS '�鸴��ʶ(0-δ�鸴;1-�Ѳ鸴)';

COMMENT ON COLUMN "AFA     "."RCC_HPDZCZ"."NCCWKDAT" IS '��������';

COMMENT ON COLUMN "AFA     "."RCC_HPDZCZ"."NOTE1" IS '�����ֶ�1';

COMMENT ON COLUMN "AFA     "."RCC_HPDZCZ"."NOTE2" IS '�����ֶ�2';

COMMENT ON COLUMN "AFA     "."RCC_HPDZCZ"."NOTE3" IS '�����ֶ�3';

COMMENT ON COLUMN "AFA     "."RCC_HPDZCZ"."NOTE4" IS '�����ֶ�4';

COMMENT ON COLUMN "AFA     "."RCC_HPDZCZ"."SNDBNKCO" IS '�������к�';

COMMENT ON COLUMN "AFA     "."RCC_HPDZCZ"."TRCDAT" IS 'ί������';

COMMENT ON COLUMN "AFA     "."RCC_HPDZCZ"."TRCNO" IS '������ˮ��';





------------------------------------------------
-- DDL Statements for table "AFA     "."RCC_HPDZHZ"
------------------------------------------------
DROP TABLE "AFA     "."RCC_HPDZHZ"

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

COMMENT ON COLUMN "AFA     "."RCC_HPDZHZ"."BRSFLG" IS '������ʶ(0-����;1-����)';

COMMENT ON COLUMN "AFA     "."RCC_HPDZHZ"."CLAMT" IS '����Ȧ����';

COMMENT ON COLUMN "AFA     "."RCC_HPDZHZ"."CTAMT" IS '�������ܽ��';

COMMENT ON COLUMN "AFA     "."RCC_HPDZHZ"."DLAMT" IS '�跽Ȧ����';

COMMENT ON COLUMN "AFA     "."RCC_HPDZHZ"."DTAMT" IS '�跽���ܽ��';

COMMENT ON COLUMN "AFA     "."RCC_HPDZHZ"."NCCWKDAT" IS '��������';

COMMENT ON COLUMN "AFA     "."RCC_HPDZHZ"."NOTE1" IS '�����ֶ�1';

COMMENT ON COLUMN "AFA     "."RCC_HPDZHZ"."NOTE2" IS '�����ֶ�2';

COMMENT ON COLUMN "AFA     "."RCC_HPDZHZ"."NOTE3" IS '�����ֶ�3';

COMMENT ON COLUMN "AFA     "."RCC_HPDZHZ"."NOTE4" IS '�����ֶ�4';

COMMENT ON COLUMN "AFA     "."RCC_HPDZHZ"."OFSLAMT" IS '����Ȧ����';

COMMENT ON COLUMN "AFA     "."RCC_HPDZHZ"."OFSTAMT" IS '������ܽ��';

COMMENT ON COLUMN "AFA     "."RCC_HPDZHZ"."TCNT" IS '���ܱ���';

COMMENT ON COLUMN "AFA     "."RCC_HPDZHZ"."TRCCO" IS '���״���';

COMMENT ON COLUMN "AFA     "."RCC_HPDZHZ"."TRCNAM" IS '��������';

COMMENT ON COLUMN "AFA     "."RCC_HPDZHZ"."TRCRSNM" IS '������ʶ˵��';


-- DDL Statements for primary key on Table "AFA     "."RCC_HPDZHZ"

ALTER TABLE "AFA     "."RCC_HPDZHZ" 
	ADD CONSTRAINT "RCC_HPDZHZ_PK" PRIMARY KEY
		("NCCWKDAT",
		 "TRCCO",
		 "BRSFLG");


------------------------------------------------
-- DDL Statements for table "AFA     "."RCC_HPDZMX"
------------------------------------------------
DROP TABLE "AFA     "."RCC_HPDZMX";

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

COMMENT ON COLUMN "AFA     "."RCC_HPDZMX"."BCSTAT" IS 'ҵ��״̬';

COMMENT ON COLUMN "AFA     "."RCC_HPDZMX"."BDWFLG" IS '״̬��ת�����ʶ';

COMMENT ON COLUMN "AFA     "."RCC_HPDZMX"."BILAMT" IS '��Ʊ���';

COMMENT ON COLUMN "AFA     "."RCC_HPDZMX"."BILDAT" IS '��Ʊ����';

COMMENT ON COLUMN "AFA     "."RCC_HPDZMX"."BILNO" IS '��Ʊ����';

COMMENT ON COLUMN "AFA     "."RCC_HPDZMX"."BILVER" IS '��Ʊ�汾��';

COMMENT ON COLUMN "AFA     "."RCC_HPDZMX"."BJEDTE" IS '��������';

COMMENT ON COLUMN "AFA     "."RCC_HPDZMX"."BSPSQN" IS '�������';

COMMENT ON COLUMN "AFA     "."RCC_HPDZMX"."CUR" IS '����';

COMMENT ON COLUMN "AFA     "."RCC_HPDZMX"."EACTYP" IS '��������';

COMMENT ON COLUMN "AFA     "."RCC_HPDZMX"."MSGFLGNO" IS '���ı�ʶ��';

COMMENT ON COLUMN "AFA     "."RCC_HPDZMX"."MSGTYPCO" IS '���������';

COMMENT ON COLUMN "AFA     "."RCC_HPDZMX"."NCCWKDAT" IS '��������';

COMMENT ON COLUMN "AFA     "."RCC_HPDZMX"."NOTE1" IS '�����ֶ�1';

COMMENT ON COLUMN "AFA     "."RCC_HPDZMX"."NOTE2" IS '�����ֶ�2';

COMMENT ON COLUMN "AFA     "."RCC_HPDZMX"."NOTE3" IS '�����ֶ�3';

COMMENT ON COLUMN "AFA     "."RCC_HPDZMX"."NOTE4" IS '�����ֶ�4';

COMMENT ON COLUMN "AFA     "."RCC_HPDZMX"."OCCAMT" IS 'ʵ�ʽ�����';

COMMENT ON COLUMN "AFA     "."RCC_HPDZMX"."OPRATTNO" IS 'ҵ������';

COMMENT ON COLUMN "AFA     "."RCC_HPDZMX"."OPRTYPNO" IS 'ҵ������';

COMMENT ON COLUMN "AFA     "."RCC_HPDZMX"."ORMFN" IS 'ԭ���ı�ʶ��';

COMMENT ON COLUMN "AFA     "."RCC_HPDZMX"."PAYWAY" IS '�Ҹ���ʽ';

COMMENT ON COLUMN "AFA     "."RCC_HPDZMX"."PYEACC" IS '�տ����˺�';

COMMENT ON COLUMN "AFA     "."RCC_HPDZMX"."PYEADDR" IS '�տ��˵�ַ';

COMMENT ON COLUMN "AFA     "."RCC_HPDZMX"."PYENAM" IS '�տ��˻���';

COMMENT ON COLUMN "AFA     "."RCC_HPDZMX"."PYRACC" IS '�������˺�';

COMMENT ON COLUMN "AFA     "."RCC_HPDZMX"."PYRADDR" IS '�����˵�ַ';

COMMENT ON COLUMN "AFA     "."RCC_HPDZMX"."PYRNAM" IS '�����˻���';

COMMENT ON COLUMN "AFA     "."RCC_HPDZMX"."RCVBNKCO" IS '�������к�';

COMMENT ON COLUMN "AFA     "."RCC_HPDZMX"."RCVBNKNM" IS '����������';

COMMENT ON COLUMN "AFA     "."RCC_HPDZMX"."RCVMBRCO" IS '���ճ�Ա�к�';

COMMENT ON COLUMN "AFA     "."RCC_HPDZMX"."REMARK" IS '��ע';

COMMENT ON COLUMN "AFA     "."RCC_HPDZMX"."RMNAMT" IS '������';

COMMENT ON COLUMN "AFA     "."RCC_HPDZMX"."ROPRTPNO" IS 'ԭҵ������';

COMMENT ON COLUMN "AFA     "."RCC_HPDZMX"."SEAL" IS '��Ѻ';

COMMENT ON COLUMN "AFA     "."RCC_HPDZMX"."SNDBNKCO" IS '�������к�';

COMMENT ON COLUMN "AFA     "."RCC_HPDZMX"."SNDBNKNM" IS '����������';

COMMENT ON COLUMN "AFA     "."RCC_HPDZMX"."SNDBRHCO" IS '�����������';

COMMENT ON COLUMN "AFA     "."RCC_HPDZMX"."SNDCLKNO" IS '�����й�Ա��';

COMMENT ON COLUMN "AFA     "."RCC_HPDZMX"."SNDMBRCO" IS '���ͳ�Ա�к�';

COMMENT ON COLUMN "AFA     "."RCC_HPDZMX"."SNDTRDAT" IS '�����н�������';

COMMENT ON COLUMN "AFA     "."RCC_HPDZMX"."SNDTRTIM" IS '�����н���ʱ��';

COMMENT ON COLUMN "AFA     "."RCC_HPDZMX"."TRCCO" IS '���״���';

COMMENT ON COLUMN "AFA     "."RCC_HPDZMX"."TRCDAT" IS 'ί������';

COMMENT ON COLUMN "AFA     "."RCC_HPDZMX"."TRCNO" IS '������ˮ��';

COMMENT ON COLUMN "AFA     "."RCC_HPDZMX"."USE" IS '��;';


-- DDL Statements for primary key on Table "AFA     "."RCC_HPDZMX"

ALTER TABLE "AFA     "."RCC_HPDZMX" 
	ADD CONSTRAINT "RCC_HPDZMX_PK" PRIMARY KEY
		("SNDBNKCO",
		 "TRCDAT",
		 "TRCNO");


------------------------------------------------
-- DDL Statements for table "AFA     "."RCC_INSBKA"
------------------------------------------------
DROP TABLE "AFA     "."RCC_INSBKA";

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

COMMENT ON COLUMN "AFA     "."RCC_INSBKA"."BDWFLG" IS '�����ʶ';

COMMENT ON COLUMN "AFA     "."RCC_INSBKA"."BJEDTE" IS '��������';

COMMENT ON COLUMN "AFA     "."RCC_INSBKA"."BSPSQN" IS '�������';

COMMENT ON COLUMN "AFA     "."RCC_INSBKA"."DASQ" IS '���������';

COMMENT ON COLUMN "AFA     "."RCC_INSBKA"."MGID" IS '����������';

COMMENT ON COLUMN "AFA     "."RCC_INSBKA"."NCCWKDAT" IS '��������';

COMMENT ON COLUMN "AFA     "."RCC_INSBKA"."NOTE1" IS '�����ֶ�1';

COMMENT ON COLUMN "AFA     "."RCC_INSBKA"."NOTE2" IS '�����ֶ�2';

COMMENT ON COLUMN "AFA     "."RCC_INSBKA"."NOTE3" IS '�����ֶ�3';

COMMENT ON COLUMN "AFA     "."RCC_INSBKA"."NOTE4" IS '�����ֶ�4';

COMMENT ON COLUMN "AFA     "."RCC_INSBKA"."RBAC" IS '�����˺�';

COMMENT ON COLUMN "AFA     "."RCC_INSBKA"."SBAC" IS '�跽�˺�';

COMMENT ON COLUMN "AFA     "."RCC_INSBKA"."TLSQ" IS '������ˮ��';

COMMENT ON COLUMN "AFA     "."RCC_INSBKA"."TRDT" IS '��������';


-- DDL Statements for primary key on Table "AFA     "."RCC_INSBKA"

ALTER TABLE "AFA     "."RCC_INSBKA" 
	ADD CONSTRAINT "RCC_INSBKA_PK" PRIMARY KEY
		("BJEDTE",
		 "BSPSQN");


------------------------------------------------
-- DDL Statements for table "AFA     "."RCC_MBRIFA"
------------------------------------------------
DROP TABLE "AFA     "."RCC_MBRIFA";

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

COMMENT ON COLUMN "AFA     "."RCC_MBRIFA"."HOLFLG" IS '����������';

COMMENT ON COLUMN "AFA     "."RCC_MBRIFA"."NOTE1" IS '�����ֶ�1(��������)';

COMMENT ON COLUMN "AFA     "."RCC_MBRIFA"."NOTE2" IS '�����ֶ�2';

COMMENT ON COLUMN "AFA     "."RCC_MBRIFA"."NOTE3" IS '�����ֶ�3';

COMMENT ON COLUMN "AFA     "."RCC_MBRIFA"."NOTE4" IS '�����ֶ�4';

COMMENT ON COLUMN "AFA     "."RCC_MBRIFA"."NWSYSST" IS '��ǰ���Ĺ���״̬';

COMMENT ON COLUMN "AFA     "."RCC_MBRIFA"."NWWKDAT" IS '��ǰ���Ĺ�������';

COMMENT ON COLUMN "AFA     "."RCC_MBRIFA"."OPRTYPNO" IS 'ҵ������';

COMMENT ON COLUMN "AFA     "."RCC_MBRIFA"."ORSYSST" IS 'ǰ���Ĺ���״̬';

COMMENT ON COLUMN "AFA     "."RCC_MBRIFA"."ORWKDAT" IS 'ǰ���Ĺ�������';

COMMENT ON COLUMN "AFA     "."RCC_MBRIFA"."STRINFO" IS '����';


-- DDL Statements for primary key on Table "AFA     "."RCC_MBRIFA"

ALTER TABLE "AFA     "."RCC_MBRIFA" 
	ADD CONSTRAINT "RCC_MBRIFA_PK" PRIMARY KEY
		("OPRTYPNO");


------------------------------------------------
-- DDL Statements for table "AFA     "."RCC_PAMTBL"
------------------------------------------------
DROP TABLE "AFA     "."RCC_PAMTBL";

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

COMMENT ON COLUMN "AFA     "."RCC_PAMTBL"."BEFTDT" IS '��Ч����';

COMMENT ON COLUMN "AFA     "."RCC_PAMTBL"."BINVDT" IS 'ʧЧ����';

COMMENT ON COLUMN "AFA     "."RCC_PAMTBL"."BPACMT" IS '����˵��';

COMMENT ON COLUMN "AFA     "."RCC_PAMTBL"."BPADAT" IS '��������';

COMMENT ON COLUMN "AFA     "."RCC_PAMTBL"."BPAINF" IS '������ע';

COMMENT ON COLUMN "AFA     "."RCC_PAMTBL"."BPARAD" IS '��������';

COMMENT ON COLUMN "AFA     "."RCC_PAMTBL"."BPATPE" IS '��������';

COMMENT ON COLUMN "AFA     "."RCC_PAMTBL"."NOTE1" IS '�����ֶ�1';

COMMENT ON COLUMN "AFA     "."RCC_PAMTBL"."NOTE2" IS '�����ֶ�2';

COMMENT ON COLUMN "AFA     "."RCC_PAMTBL"."NOTE3" IS '�����ֶ�3';

COMMENT ON COLUMN "AFA     "."RCC_PAMTBL"."NOTE4" IS '�����ֶ�4';


-- DDL Statements for primary key on Table "AFA     "."RCC_PAMTBL"

ALTER TABLE "AFA     "."RCC_PAMTBL" 
	ADD CONSTRAINT "RCC_PAMTBL_PK" PRIMARY KEY
		("BPATPE",
		 "BPARAD");


------------------------------------------------
-- DDL Statements for table "AFA     "."RCC_SPBSTA"
------------------------------------------------
DROP TABLE "AFA     "."RCC_SPBSTA";

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

COMMENT ON COLUMN "AFA     "."RCC_SPBSTA"."BCSTAT" IS 'ҵ��״̬';

COMMENT ON COLUMN "AFA     "."RCC_SPBSTA"."BCURSQ" IS '״̬���';

COMMENT ON COLUMN "AFA     "."RCC_SPBSTA"."BDWFLG" IS '��ת�����ʶ';

COMMENT ON COLUMN "AFA     "."RCC_SPBSTA"."BJEDTE" IS '��������';

COMMENT ON COLUMN "AFA     "."RCC_SPBSTA"."BSPSQN" IS '�������';

COMMENT ON COLUMN "AFA     "."RCC_SPBSTA"."NOTE1" IS '�����ֶ�1';

COMMENT ON COLUMN "AFA     "."RCC_SPBSTA"."NOTE2" IS '�����ֶ�2';

COMMENT ON COLUMN "AFA     "."RCC_SPBSTA"."NOTE3" IS '�����ֶ�3';

COMMENT ON COLUMN "AFA     "."RCC_SPBSTA"."NOTE4" IS '�����ֶ�4';


-- DDL Statements for primary key on Table "AFA     "."RCC_SPBSTA"

ALTER TABLE "AFA     "."RCC_SPBSTA" 
	ADD CONSTRAINT "RCC_SPBSTA_PK" PRIMARY KEY
		("BJEDTE",
		 "BSPSQN");


------------------------------------------------
-- DDL Statements for table "AFA     "."RCC_SUBBRA"
------------------------------------------------
DROP TABLE "AFA     "."RCC_SUBBRA";

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

COMMENT ON COLUMN "AFA     "."RCC_SUBBRA"."BANKBIN" IS 'ũ����ϵͳ�к�';

COMMENT ON COLUMN "AFA     "."RCC_SUBBRA"."BEACSB" IS '���������';

COMMENT ON COLUMN "AFA     "."RCC_SUBBRA"."BESBNM" IS '��������';

COMMENT ON COLUMN "AFA     "."RCC_SUBBRA"."BESBNO" IS '������';

COMMENT ON COLUMN "AFA     "."RCC_SUBBRA"."BESBTP" IS '��������';

COMMENT ON COLUMN "AFA     "."RCC_SUBBRA"."BTOPSB" IS '�ϼ�������';

COMMENT ON COLUMN "AFA     "."RCC_SUBBRA"."NOTE1" IS '�����ֶ�1';

COMMENT ON COLUMN "AFA     "."RCC_SUBBRA"."NOTE2" IS '�����ֶ�2';

COMMENT ON COLUMN "AFA     "."RCC_SUBBRA"."NOTE3" IS '�����ֶ�3';

COMMENT ON COLUMN "AFA     "."RCC_SUBBRA"."NOTE4" IS '�����ֶ�4';

COMMENT ON COLUMN "AFA     "."RCC_SUBBRA"."STRINFO" IS '����';

COMMENT ON COLUMN "AFA     "."RCC_SUBBRA"."SUBFLG" IS '�����ʶ(0-������;1-����)';


-- DDL Statements for primary key on Table "AFA     "."RCC_SUBBRA"

ALTER TABLE "AFA     "."RCC_SUBBRA" 
	ADD CONSTRAINT "RCC_SUBBRA_PK" PRIMARY KEY
		("BESBNO");


------------------------------------------------
-- DDL Statements for table "AFA     "."RCC_TRCSTA"
------------------------------------------------
DROP TABLE "AFA     "."RCC_TRCSTA";

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

COMMENT ON COLUMN "AFA     "."RCC_TRCSTA"."BEACSB" IS '���������';

COMMENT ON COLUMN "AFA     "."RCC_TRCSTA"."BESBNO" IS '������';

COMMENT ON COLUMN "AFA     "."RCC_TRCSTA"."BRSFLG" IS '������ʶ(0-����;1-����)';

COMMENT ON COLUMN "AFA     "."RCC_TRCSTA"."BTOPSB" IS '�ϼ�������';

COMMENT ON COLUMN "AFA     "."RCC_TRCSTA"."ISDEAL" IS '�����ʶ(0-δ����;1-�Ѵ���)';

COMMENT ON COLUMN "AFA     "."RCC_TRCSTA"."NCCWKDAT" IS '��������';

COMMENT ON COLUMN "AFA     "."RCC_TRCSTA"."NOTE1" IS '�����ֶ�1';

COMMENT ON COLUMN "AFA     "."RCC_TRCSTA"."NOTE2" IS '�����ֶ�2';

COMMENT ON COLUMN "AFA     "."RCC_TRCSTA"."NOTE3" IS '�����ֶ�3';

COMMENT ON COLUMN "AFA     "."RCC_TRCSTA"."NOTE4" IS '�����ֶ�4';

COMMENT ON COLUMN "AFA     "."RCC_TRCSTA"."STRINFO" IS '����';

COMMENT ON COLUMN "AFA     "."RCC_TRCSTA"."TAMT" IS '���ܽ��';

COMMENT ON COLUMN "AFA     "."RCC_TRCSTA"."TCNT" IS '���ܱ���';

COMMENT ON COLUMN "AFA     "."RCC_TRCSTA"."TRCCO" IS '���״���';


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
DROP TABLE "AFA     "."RCC_SSTLOG";

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
		  "DASQ" VARCHAR(9) , 
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

COMMENT ON COLUMN "AFA     "."RCC_SSTLOG"."ACNM" IS '�跽����';

COMMENT ON COLUMN "AFA     "."RCC_SSTLOG"."BCSTAT" IS 'ҵ��״̬';

COMMENT ON COLUMN "AFA     "."RCC_SSTLOG"."BCURSQ" IS '������ʶ(0-����;1-����)';

COMMENT ON COLUMN "AFA     "."RCC_SSTLOG"."BDWFLG" IS '��ת�����ʶ';

COMMENT ON COLUMN "AFA     "."RCC_SSTLOG"."BEACSB" IS '���������';

COMMENT ON COLUMN "AFA     "."RCC_SSTLOG"."BEAUUS" IS '��Ȩ��Ա��';

COMMENT ON COLUMN "AFA     "."RCC_SSTLOG"."BESBNO" IS '������';

COMMENT ON COLUMN "AFA     "."RCC_SSTLOG"."BETELR" IS '��Ա��';

COMMENT ON COLUMN "AFA     "."RCC_SSTLOG"."BJEDTE" IS '��������';

COMMENT ON COLUMN "AFA     "."RCC_SSTLOG"."BJETIM" IS '����ʱ��';

COMMENT ON COLUMN "AFA     "."RCC_SSTLOG"."BSPSQN" IS '�������';

COMMENT ON COLUMN "AFA     "."RCC_SSTLOG"."DASQ" IS '�������';

COMMENT ON COLUMN "AFA     "."RCC_SSTLOG"."FEDT" IS 'ǰ������';

COMMENT ON COLUMN "AFA     "."RCC_SSTLOG"."MGID" IS '����������';

COMMENT ON COLUMN "AFA     "."RCC_SSTLOG"."NOTE1" IS '�����ֶ�1';

COMMENT ON COLUMN "AFA     "."RCC_SSTLOG"."NOTE2" IS '�����ֶ�2';

COMMENT ON COLUMN "AFA     "."RCC_SSTLOG"."NOTE3" IS '�����ֶ�3';

COMMENT ON COLUMN "AFA     "."RCC_SSTLOG"."NOTE4" IS '�����ֶ�4';

COMMENT ON COLUMN "AFA     "."RCC_SSTLOG"."OTNM" IS '��������';

COMMENT ON COLUMN "AFA     "."RCC_SSTLOG"."PRCCO" IS '���ķ�����';

COMMENT ON COLUMN "AFA     "."RCC_SSTLOG"."PRTCNT" IS '��ӡ����';

COMMENT ON COLUMN "AFA     "."RCC_SSTLOG"."RBAC" IS '�����˺�';

COMMENT ON COLUMN "AFA     "."RCC_SSTLOG"."RBSQ" IS 'ǰ����ˮ��';

COMMENT ON COLUMN "AFA     "."RCC_SSTLOG"."SBAC" IS '�跽�˺�';

COMMENT ON COLUMN "AFA     "."RCC_SSTLOG"."STRINFO" IS '������˵��';

COMMENT ON COLUMN "AFA     "."RCC_SSTLOG"."TLSQ" IS '������ˮ��';

COMMENT ON COLUMN "AFA     "."RCC_SSTLOG"."TRDT" IS '��������';


-- DDL Statements for primary key on Table "AFA     "."RCC_SSTLOG"

ALTER TABLE "AFA     "."RCC_SSTLOG" 
	ADD CONSTRAINT "RCC_SSTLOG_PK" PRIMARY KEY
		("BJEDTE",
		 "BSPSQN",
		 "BCURSQ");


------------------------------------------------
-- DDL Statements for table "AFA     "."RCC_PBDATA"
------------------------------------------------
DROP TABLE "AFA     "."RCC_PBDATA";

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

COMMENT ON COLUMN "AFA     "."RCC_PBDATA"."EFCTDAT" IS '��Ч����';

COMMENT ON COLUMN "AFA     "."RCC_PBDATA"."NCCWKDAT" IS '��������';

COMMENT ON COLUMN "AFA     "."RCC_PBDATA"."NOTE1" IS '�����ֶ�1';

COMMENT ON COLUMN "AFA     "."RCC_PBDATA"."NOTE2" IS '�����ֶ�2';

COMMENT ON COLUMN "AFA     "."RCC_PBDATA"."NOTE3" IS '�����ֶ�3';

COMMENT ON COLUMN "AFA     "."RCC_PBDATA"."NOTE4" IS '�����ֶ�4';

COMMENT ON COLUMN "AFA     "."RCC_PBDATA"."PBDAFILE" IS '���������ļ���';

COMMENT ON COLUMN "AFA     "."RCC_PBDATA"."PBDATYP" IS '������������';

COMMENT ON COLUMN "AFA     "."RCC_PBDATA"."RCVBNKCO" IS '�������к�';

COMMENT ON COLUMN "AFA     "."RCC_PBDATA"."SNDBNKCO" IS '�������к�';

COMMENT ON COLUMN "AFA     "."RCC_PBDATA"."TRCCO" IS '���״���';

COMMENT ON COLUMN "AFA     "."RCC_PBDATA"."TRCDAT" IS 'ί������';

COMMENT ON COLUMN "AFA     "."RCC_PBDATA"."TRCNO" IS '������ˮ��';


-- DDL Statements for primary key on Table "AFA     "."RCC_PBDATA"

ALTER TABLE "AFA     "."RCC_PBDATA" 
	ADD CONSTRAINT "RCC_PBDATE_PK" PRIMARY KEY
		("TRCDAT",
		 "TRCNO",
		 "SNDBNKCO");


------------------------------------------------
-- DDL Statements for table "AFA     "."RCC_PAYBNK"
------------------------------------------------
DROP TABLE "AFA     "."RCC_PAYBNK";

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

COMMENT ON COLUMN "AFA     "."RCC_PAYBNK"."ALTTYPE" IS '������²���';

COMMENT ON COLUMN "AFA     "."RCC_PAYBNK"."BANKADDR" IS '��ַ';

COMMENT ON COLUMN "AFA     "."RCC_PAYBNK"."BANKATTR" IS '����';

COMMENT ON COLUMN "AFA     "."RCC_PAYBNK"."BANKBIN" IS '�к�';

COMMENT ON COLUMN "AFA     "."RCC_PAYBNK"."BANKNAM" IS '������ȫ��';

COMMENT ON COLUMN "AFA     "."RCC_PAYBNK"."BANKPC" IS '�ʱ�';

COMMENT ON COLUMN "AFA     "."RCC_PAYBNK"."BANKSTATUS" IS '״̬';

COMMENT ON COLUMN "AFA     "."RCC_PAYBNK"."BANKTEL" IS '�绰';

COMMENT ON COLUMN "AFA     "."RCC_PAYBNK"."EFCTDAT" IS '��Ч����';

COMMENT ON COLUMN "AFA     "."RCC_PAYBNK"."INVDAT" IS 'ʧЧ����';

COMMENT ON COLUMN "AFA     "."RCC_PAYBNK"."NEWOFLG" IS '�¾�ϵͳ��ʶ';

COMMENT ON COLUMN "AFA     "."RCC_PAYBNK"."NOTE1" IS '�����ֶ�1';

COMMENT ON COLUMN "AFA     "."RCC_PAYBNK"."NOTE2" IS '�����ֶ�2';

COMMENT ON COLUMN "AFA     "."RCC_PAYBNK"."NOTE3" IS '�����ֶ�3';

COMMENT ON COLUMN "AFA     "."RCC_PAYBNK"."NOTE4" IS '�����ֶ�4';

COMMENT ON COLUMN "AFA     "."RCC_PAYBNK"."PRIVILEGE" IS 'ҵ��Ȩ��';

COMMENT ON COLUMN "AFA     "."RCC_PAYBNK"."STLBANKBIN" IS '��Ա�к�';

COMMENT ON COLUMN "AFA     "."RCC_PAYBNK"."STRINFO" IS '����';


-- DDL Statements for primary key on Table "AFA     "."RCC_PAYBNK"

ALTER TABLE "AFA     "."RCC_PAYBNK" 
	ADD CONSTRAINT "RCC_PAYBNK_PK" PRIMARY KEY
		("BANKBIN");


------------------------------------------------
-- DDL Statements for table "AFA     "."RCC_BILINF"
------------------------------------------------
DROP TABLE "AFA     "."RCC_BILINF";

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

COMMENT ON COLUMN "AFA     "."RCC_BILINF"."BILAMT" IS '��Ʊ���';

COMMENT ON COLUMN "AFA     "."RCC_BILINF"."BILDAT" IS '��Ʊ����';

COMMENT ON COLUMN "AFA     "."RCC_BILINF"."BILNO" IS '��Ʊ����';

COMMENT ON COLUMN "AFA     "."RCC_BILINF"."BILRS" IS '��Ʊ�������б�ʶ(0-����ǩ���Ļ�Ʊ;1-����ǩ���Ļ�Ʊ)';

COMMENT ON COLUMN "AFA     "."RCC_BILINF"."BILTYP" IS '��Ʊ����(0-�ֽ��Ʊ;1-ת�˻�Ʊ)';

COMMENT ON COLUMN "AFA     "."RCC_BILINF"."BILVER" IS '��Ʊ�汾��';

COMMENT ON COLUMN "AFA     "."RCC_BILINF"."CUR" IS '����';

COMMENT ON COLUMN "AFA     "."RCC_BILINF"."HPCUSQ" IS '��Ʊ״̬���';

COMMENT ON COLUMN "AFA     "."RCC_BILINF"."HPSTAT" IS '��Ʊ״̬';

COMMENT ON COLUMN "AFA     "."RCC_BILINF"."NOTE1" IS '�����ֶ�1';

COMMENT ON COLUMN "AFA     "."RCC_BILINF"."NOTE2" IS '�����ֶ�2';

COMMENT ON COLUMN "AFA     "."RCC_BILINF"."NOTE3" IS '�����ֶ�3';

COMMENT ON COLUMN "AFA     "."RCC_BILINF"."NOTE4" IS '�����ֶ�4';

COMMENT ON COLUMN "AFA     "."RCC_BILINF"."OCCAMT" IS 'ʵ�ʽ�����';

COMMENT ON COLUMN "AFA     "."RCC_BILINF"."PAYBNKCO" IS '���������к�';

COMMENT ON COLUMN "AFA     "."RCC_BILINF"."PAYBNKNM" IS '������������';

COMMENT ON COLUMN "AFA     "."RCC_BILINF"."PAYWAY" IS '�Ҹ���ʽ(0-�ֽ�;1-���ֽ�)';

COMMENT ON COLUMN "AFA     "."RCC_BILINF"."PYEACC" IS '�տ����˺�';

COMMENT ON COLUMN "AFA     "."RCC_BILINF"."PYEADDR" IS '�տ��˵�ַ';

COMMENT ON COLUMN "AFA     "."RCC_BILINF"."PYENAM" IS '�տ��˻���';

COMMENT ON COLUMN "AFA     "."RCC_BILINF"."PYHACC" IS '��Ʊ���˺�';

COMMENT ON COLUMN "AFA     "."RCC_BILINF"."PYHADDR" IS '��Ʊ�˵�ַ';

COMMENT ON COLUMN "AFA     "."RCC_BILINF"."PYHNAM" IS '��Ʊ�˻���';

COMMENT ON COLUMN "AFA     "."RCC_BILINF"."PYIACC" IS '��Ʊ�����˺�';

COMMENT ON COLUMN "AFA     "."RCC_BILINF"."PYINAM" IS '��Ʊ���˻���';

COMMENT ON COLUMN "AFA     "."RCC_BILINF"."PYITYP" IS '��Ʊ��������';

COMMENT ON COLUMN "AFA     "."RCC_BILINF"."PYRACC" IS '��Ʊ���˺�';

COMMENT ON COLUMN "AFA     "."RCC_BILINF"."PYRADDR" IS '��Ʊ�˵�ַ';

COMMENT ON COLUMN "AFA     "."RCC_BILINF"."PYRNAM" IS '��Ʊ�˻���';

COMMENT ON COLUMN "AFA     "."RCC_BILINF"."REMARK" IS '��ע';

COMMENT ON COLUMN "AFA     "."RCC_BILINF"."REMBNKCO" IS '��Ʊ���к�';

COMMENT ON COLUMN "AFA     "."RCC_BILINF"."REMBNKNM" IS '��Ʊ������';

COMMENT ON COLUMN "AFA     "."RCC_BILINF"."RMNAMT" IS '������';

COMMENT ON COLUMN "AFA     "."RCC_BILINF"."SEAL" IS '��Ʊ��Ѻ';

COMMENT ON COLUMN "AFA     "."RCC_BILINF"."USE" IS '��;';


-- DDL Statements for primary key on Table "AFA     "."RCC_BILINF"

ALTER TABLE "AFA     "."RCC_BILINF" 
	ADD CONSTRAINT "RCC_BILINF_PK" PRIMARY KEY
		("BILVER",
		 "BILNO",
		 "BILRS");





------------------------------------------------
-- DDL Statements for table "AFA     "."RCC_MRQTBL"
------------------------------------------------
DROP TABLE "AFA     "."RCC_MRQTBL";

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

COMMENT ON COLUMN "AFA     "."RCC_MRQTBL"."BJEDTE" IS '��������';

COMMENT ON COLUMN "AFA     "."RCC_MRQTBL"."BSPSQN" IS '�������';

COMMENT ON COLUMN "AFA     "."RCC_MRQTBL"."NOTE1" IS '�����ֶ�1';

COMMENT ON COLUMN "AFA     "."RCC_MRQTBL"."NOTE2" IS '�����ֶ�2';

COMMENT ON COLUMN "AFA     "."RCC_MRQTBL"."NOTE3" IS '�����ֶ�3';

COMMENT ON COLUMN "AFA     "."RCC_MRQTBL"."NOTE4" IS '�����ֶ�4';

COMMENT ON COLUMN "AFA     "."RCC_MRQTBL"."NPCACNT" IS '����֧��ϵͳ�˺�';

COMMENT ON COLUMN "AFA     "."RCC_MRQTBL"."NPCBKID" IS '����֧��ϵͳ�к�';

COMMENT ON COLUMN "AFA     "."RCC_MRQTBL"."NPCBKNM" IS '����֧��ϵͳ����';

COMMENT ON COLUMN "AFA     "."RCC_MRQTBL"."OCCAMT" IS '�������';

COMMENT ON COLUMN "AFA     "."RCC_MRQTBL"."PRCCO" IS '���ķ�����';

COMMENT ON COLUMN "AFA     "."RCC_MRQTBL"."RCVBNKCO" IS '�������к�';

COMMENT ON COLUMN "AFA     "."RCC_MRQTBL"."RCVBNKNM" IS '����������';

COMMENT ON COLUMN "AFA     "."RCC_MRQTBL"."RCVMBRCO" IS '���ճ�Ա�к�';

COMMENT ON COLUMN "AFA     "."RCC_MRQTBL"."REMARK" IS '��ע';

COMMENT ON COLUMN "AFA     "."RCC_MRQTBL"."SNDBNKCO" IS '�������к�';

COMMENT ON COLUMN "AFA     "."RCC_MRQTBL"."SNDBNKNM" IS '����������';

COMMENT ON COLUMN "AFA     "."RCC_MRQTBL"."SNDMBRCO" IS '���ͳ�Ա�к�';

COMMENT ON COLUMN "AFA     "."RCC_MRQTBL"."STRINFO" IS '���ķ�����˵��';

COMMENT ON COLUMN "AFA     "."RCC_MRQTBL"."TRCCO" IS '���״���';

COMMENT ON COLUMN "AFA     "."RCC_MRQTBL"."TRCDAT" IS 'ί������';

COMMENT ON COLUMN "AFA     "."RCC_MRQTBL"."TRCNO" IS '������ˮ��';


-- DDL Statements for primary key on Table "AFA     "."RCC_MRQTBL"

ALTER TABLE "AFA     "."RCC_MRQTBL" 
	ADD CONSTRAINT "RCC_MRQTBL_PK" PRIMARY KEY
		("BJEDTE",
		 "BSPSQN");


------------------------------------------------
-- DDL Statements for table "AFA     "."RCC_TRCCAN"
------------------------------------------------
DROP TABLE "AFA     "."RCC_TRCCAN";

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

COMMENT ON COLUMN "AFA     "."RCC_TRCCAN"."BEAUUS" IS '��Ȩ��Ա��';

COMMENT ON COLUMN "AFA     "."RCC_TRCCAN"."BESBNO" IS '������';

COMMENT ON COLUMN "AFA     "."RCC_TRCCAN"."BETELR" IS '��Ա��';

COMMENT ON COLUMN "AFA     "."RCC_TRCCAN"."BJEDTE" IS '��������';

COMMENT ON COLUMN "AFA     "."RCC_TRCCAN"."BOJEDT" IS 'ԭ��������';

COMMENT ON COLUMN "AFA     "."RCC_TRCCAN"."BOSPSQ" IS 'ԭ�������';

COMMENT ON COLUMN "AFA     "."RCC_TRCCAN"."BRSFLG" IS '������ʶ(0-����;1-����)';

COMMENT ON COLUMN "AFA     "."RCC_TRCCAN"."BSPSQN" IS '�������';

COMMENT ON COLUMN "AFA     "."RCC_TRCCAN"."CLRESPN" IS '����Ӧ��(0-����;1-���ܳ���)';

COMMENT ON COLUMN "AFA     "."RCC_TRCCAN"."CONT" IS '����';

COMMENT ON COLUMN "AFA     "."RCC_TRCCAN"."CUR" IS '����';

COMMENT ON COLUMN "AFA     "."RCC_TRCCAN"."NCCWKDAT" IS '��������';

COMMENT ON COLUMN "AFA     "."RCC_TRCCAN"."NOTE1" IS '�����ֶ�1';

COMMENT ON COLUMN "AFA     "."RCC_TRCCAN"."NOTE2" IS '�����ֶ�2';

COMMENT ON COLUMN "AFA     "."RCC_TRCCAN"."NOTE3" IS '�����ֶ�3';

COMMENT ON COLUMN "AFA     "."RCC_TRCCAN"."NOTE4" IS '�����ֶ�4';

COMMENT ON COLUMN "AFA     "."RCC_TRCCAN"."OCCAMT" IS '���׽��';

COMMENT ON COLUMN "AFA     "."RCC_TRCCAN"."ORTRCCO" IS 'ԭ���״���';

COMMENT ON COLUMN "AFA     "."RCC_TRCCAN"."PRCCO" IS '���ķ�����';

COMMENT ON COLUMN "AFA     "."RCC_TRCCAN"."RCVBNKCO" IS '�������к�';

COMMENT ON COLUMN "AFA     "."RCC_TRCCAN"."RCVBNKNM" IS '����������';

COMMENT ON COLUMN "AFA     "."RCC_TRCCAN"."RCVMBRCO" IS '���ճ�Ա�к�';

COMMENT ON COLUMN "AFA     "."RCC_TRCCAN"."SNDBNKCO" IS '�������к�';

COMMENT ON COLUMN "AFA     "."RCC_TRCCAN"."SNDBNKNM" IS '����������';

COMMENT ON COLUMN "AFA     "."RCC_TRCCAN"."SNDMBRCO" IS '���ͳ�Ա�к�';

COMMENT ON COLUMN "AFA     "."RCC_TRCCAN"."STRINFO" IS '���ķ�����˵��';

COMMENT ON COLUMN "AFA     "."RCC_TRCCAN"."TRCCO" IS '���״���';

COMMENT ON COLUMN "AFA     "."RCC_TRCCAN"."TRCDAT" IS 'ί������';

COMMENT ON COLUMN "AFA     "."RCC_TRCCAN"."TRCNO" IS '������ˮ��';


-- DDL Statements for primary key on Table "AFA     "."RCC_TRCCAN"

ALTER TABLE "AFA     "."RCC_TRCCAN" 
	ADD CONSTRAINT "RCC_TRCCAN_PK" PRIMARY KEY
		("BJEDTE",
		 "BSPSQN");


------------------------------------------------
-- DDL Statements for table "AFA     "."RCC_EXISTP"
------------------------------------------------
DROP TABLE "AFA     "."RCC_EXISTP";

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

COMMENT ON COLUMN "AFA     "."RCC_EXISTP"."BEAUUS" IS '��Ȩ��Ա��';

COMMENT ON COLUMN "AFA     "."RCC_EXISTP"."BESBNO" IS '������';

COMMENT ON COLUMN "AFA     "."RCC_EXISTP"."BETELR" IS '��Ա��';

COMMENT ON COLUMN "AFA     "."RCC_EXISTP"."BJEDTE" IS '��������';

COMMENT ON COLUMN "AFA     "."RCC_EXISTP"."BOJEDT" IS 'ԭ��������';

COMMENT ON COLUMN "AFA     "."RCC_EXISTP"."BOSPSQ" IS 'ԭ�������';

COMMENT ON COLUMN "AFA     "."RCC_EXISTP"."BRSFLG" IS '������ʶ(0-����;1-����)';

COMMENT ON COLUMN "AFA     "."RCC_EXISTP"."BSPSQN" IS '�������';

COMMENT ON COLUMN "AFA     "."RCC_EXISTP"."CONT" IS '����';

COMMENT ON COLUMN "AFA     "."RCC_EXISTP"."CUR" IS '����';

COMMENT ON COLUMN "AFA     "."RCC_EXISTP"."NCCWKDAT" IS '��������';

COMMENT ON COLUMN "AFA     "."RCC_EXISTP"."NOTE1" IS '�����ֶ�1';

COMMENT ON COLUMN "AFA     "."RCC_EXISTP"."NOTE2" IS '�����ֶ�2';

COMMENT ON COLUMN "AFA     "."RCC_EXISTP"."NOTE3" IS '�����ֶ�3';

COMMENT ON COLUMN "AFA     "."RCC_EXISTP"."NOTE4" IS '�����ֶ�4';

COMMENT ON COLUMN "AFA     "."RCC_EXISTP"."OCCAMT" IS '���׽��';

COMMENT ON COLUMN "AFA     "."RCC_EXISTP"."ORTRCCO" IS 'ԭ���״���';

COMMENT ON COLUMN "AFA     "."RCC_EXISTP"."PRCCO" IS '���ķ�����';

COMMENT ON COLUMN "AFA     "."RCC_EXISTP"."RCVBNKCO" IS '�������к�';

COMMENT ON COLUMN "AFA     "."RCC_EXISTP"."RCVBNKNM" IS '����������';

COMMENT ON COLUMN "AFA     "."RCC_EXISTP"."RCVMBRCO" IS '���ճ�Ա�к�';

COMMENT ON COLUMN "AFA     "."RCC_EXISTP"."SNDBNKCO" IS '�������к�';

COMMENT ON COLUMN "AFA     "."RCC_EXISTP"."SNDBNKNM" IS '����������';

COMMENT ON COLUMN "AFA     "."RCC_EXISTP"."SNDMBRCO" IS '���ͳ�Ա�к�';

COMMENT ON COLUMN "AFA     "."RCC_EXISTP"."STRINFO" IS '���ķ�����˵��';

COMMENT ON COLUMN "AFA     "."RCC_EXISTP"."TRCCO" IS '���״���';

COMMENT ON COLUMN "AFA     "."RCC_EXISTP"."TRCDAT" IS 'ί������';

COMMENT ON COLUMN "AFA     "."RCC_EXISTP"."TRCNO" IS '������ˮ��';


-- DDL Statements for primary key on Table "AFA     "."RCC_EXISTP"

ALTER TABLE "AFA     "."RCC_EXISTP" 
	ADD CONSTRAINT "RCC_EXISTP_PK" PRIMARY KEY
		("BJEDTE",
		 "BSPSQN");


------------------------------------------------
-- DDL Statements for table "AFA     "."RCC_HDDZMX"
------------------------------------------------
DROP TABLE "AFA     "."RCC_HDDZMX";

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

COMMENT ON COLUMN "AFA     "."RCC_HDDZMX"."BCSTAT" IS '����״̬';

COMMENT ON COLUMN "AFA     "."RCC_HDDZMX"."BDWFLG" IS '��ת�����ʶ';

COMMENT ON COLUMN "AFA     "."RCC_HDDZMX"."BILDAT" IS 'Ʊ������';

COMMENT ON COLUMN "AFA     "."RCC_HDDZMX"."BILNO" IS 'Ʊ�ݺ���';

COMMENT ON COLUMN "AFA     "."RCC_HDDZMX"."BILTYP" IS 'Ʊ������';

COMMENT ON COLUMN "AFA     "."RCC_HDDZMX"."BJEDTE" IS '��������';

COMMENT ON COLUMN "AFA     "."RCC_HDDZMX"."BSPSQN" IS '�������';

COMMENT ON COLUMN "AFA     "."RCC_HDDZMX"."CPSAMT" IS '�⳥����';

COMMENT ON COLUMN "AFA     "."RCC_HDDZMX"."CUR" IS '����';

COMMENT ON COLUMN "AFA     "."RCC_HDDZMX"."EACTYP" IS '��������';

COMMENT ON COLUMN "AFA     "."RCC_HDDZMX"."MSGFLGNO" IS '���ı�ʶ��';

COMMENT ON COLUMN "AFA     "."RCC_HDDZMX"."MSGTYPCO" IS '���ı�ʶ��';

COMMENT ON COLUMN "AFA     "."RCC_HDDZMX"."NCCWKDAT" IS '��������';

COMMENT ON COLUMN "AFA     "."RCC_HDDZMX"."NOTE1" IS '�����ֶ�1';

COMMENT ON COLUMN "AFA     "."RCC_HDDZMX"."NOTE2" IS '�����ֶ�2';

COMMENT ON COLUMN "AFA     "."RCC_HDDZMX"."NOTE3" IS '�����ֶ�3';

COMMENT ON COLUMN "AFA     "."RCC_HDDZMX"."NOTE4" IS '�����ֶ�4';

COMMENT ON COLUMN "AFA     "."RCC_HDDZMX"."OCCAMT" IS '���׽��';

COMMENT ON COLUMN "AFA     "."RCC_HDDZMX"."OPRATTNO" IS 'ҵ������';

COMMENT ON COLUMN "AFA     "."RCC_HDDZMX"."OPRSTNO" IS 'ҵ��״̬';

COMMENT ON COLUMN "AFA     "."RCC_HDDZMX"."OPRTYPNO" IS 'ҵ������';

COMMENT ON COLUMN "AFA     "."RCC_HDDZMX"."ORMFN" IS 'ԭ���ı�ʶ��';

COMMENT ON COLUMN "AFA     "."RCC_HDDZMX"."ORRCVBNK" IS 'ԭ�����к�';

COMMENT ON COLUMN "AFA     "."RCC_HDDZMX"."ORSNDBNK" IS 'ԭ�����к�';

COMMENT ON COLUMN "AFA     "."RCC_HDDZMX"."ORTRCCO" IS 'ԭ���״���';

COMMENT ON COLUMN "AFA     "."RCC_HDDZMX"."ORTRCDAT" IS 'ԭ���״���';

COMMENT ON COLUMN "AFA     "."RCC_HDDZMX"."ORTRCNO" IS 'ԭ������ˮ��';

COMMENT ON COLUMN "AFA     "."RCC_HDDZMX"."PYEACC" IS '�տ����˺�';

COMMENT ON COLUMN "AFA     "."RCC_HDDZMX"."PYEADDR" IS '�տ��˵�ַ';

COMMENT ON COLUMN "AFA     "."RCC_HDDZMX"."PYENAM" IS '�տ��˻���';

COMMENT ON COLUMN "AFA     "."RCC_HDDZMX"."PYRACC" IS '�������˺�';

COMMENT ON COLUMN "AFA     "."RCC_HDDZMX"."PYRADDR" IS '�����˵�ַ';

COMMENT ON COLUMN "AFA     "."RCC_HDDZMX"."PYRNAM" IS '�����˻���';

COMMENT ON COLUMN "AFA     "."RCC_HDDZMX"."RCVBNKCO" IS '�������к�';

COMMENT ON COLUMN "AFA     "."RCC_HDDZMX"."RCVBNKNM" IS '����������';

COMMENT ON COLUMN "AFA     "."RCC_HDDZMX"."RCVMBRCO" IS '���ճ�Ա�к�';

COMMENT ON COLUMN "AFA     "."RCC_HDDZMX"."REMARK" IS '��ע';

COMMENT ON COLUMN "AFA     "."RCC_HDDZMX"."RFUAMT" IS '�ܸ�����';

COMMENT ON COLUMN "AFA     "."RCC_HDDZMX"."ROPRTPNO" IS 'ԭҵ������';

COMMENT ON COLUMN "AFA     "."RCC_HDDZMX"."SEAL" IS '��Ѻ';

COMMENT ON COLUMN "AFA     "."RCC_HDDZMX"."SNDBNKCO" IS '�������к�';

COMMENT ON COLUMN "AFA     "."RCC_HDDZMX"."SNDBNKNM" IS '����������';

COMMENT ON COLUMN "AFA     "."RCC_HDDZMX"."SNDBRHCO" IS '���ͻ�����';

COMMENT ON COLUMN "AFA     "."RCC_HDDZMX"."SNDCLKNO" IS '���͹�Ա��';

COMMENT ON COLUMN "AFA     "."RCC_HDDZMX"."SNDMBRCO" IS '���ͳ�Ա�к�';

COMMENT ON COLUMN "AFA     "."RCC_HDDZMX"."SNDTRDAT" IS '���ͽ�������';

COMMENT ON COLUMN "AFA     "."RCC_HDDZMX"."SNDTRTIM" IS '���ͽ���ʱ��';

COMMENT ON COLUMN "AFA     "."RCC_HDDZMX"."STRINFO" IS '����';

COMMENT ON COLUMN "AFA     "."RCC_HDDZMX"."TRCCO" IS '���״���';

COMMENT ON COLUMN "AFA     "."RCC_HDDZMX"."TRCDAT" IS 'ί������';

COMMENT ON COLUMN "AFA     "."RCC_HDDZMX"."TRCNO" IS '������ˮ��';

COMMENT ON COLUMN "AFA     "."RCC_HDDZMX"."USE" IS '��;';


-- DDL Statements for primary key on Table "AFA     "."RCC_HDDZMX"

ALTER TABLE "AFA     "."RCC_HDDZMX" 
	ADD CONSTRAINT "RCC_HDDZMX_PK" PRIMARY KEY
		("SNDBNKCO",
		 "TRCDAT",
		 "TRCNO");








------------------------------------------------
-- DDL Statements for table "AFA     "."RCC_PJCBKA"
------------------------------------------------
DROP TABLE "AFA     "."RCC_PJCBKA";

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
		  "CONT" VARCHAR(255) , 
		  "ISDEAL" VARCHAR(1) , 
		  "PRCCO" VARCHAR(8) , 
		  "STRINFO" VARCHAR(60) , 
		  "NOTE1" VARCHAR(10) , 
		  "NOTE2" VARCHAR(20) , 
		  "NOTE3" VARCHAR(60) , 
		  "NOTE4" VARCHAR(60) )   
		 IN "AFA_DATA" ; 

COMMENT ON COLUMN "AFA     "."RCC_PJCBKA"."BEAUUS" IS '��Ȩ��Ա��';

COMMENT ON COLUMN "AFA     "."RCC_PJCBKA"."BESBNO" IS '������';

COMMENT ON COLUMN "AFA     "."RCC_PJCBKA"."BETELR" IS '��Ա��';

COMMENT ON COLUMN "AFA     "."RCC_PJCBKA"."BILAMT" IS '��Ʊ���';

COMMENT ON COLUMN "AFA     "."RCC_PJCBKA"."BILDAT" IS 'Ʊ������';

COMMENT ON COLUMN "AFA     "."RCC_PJCBKA"."BILENDDT" IS 'Ʊ�ݵ�����';

COMMENT ON COLUMN "AFA     "."RCC_PJCBKA"."BILNO" IS 'Ʊ�ݺ���';

COMMENT ON COLUMN "AFA     "."RCC_PJCBKA"."BILPNAM" IS '��Ʊ������';

COMMENT ON COLUMN "AFA     "."RCC_PJCBKA"."BJEDTE" IS '��������';

COMMENT ON COLUMN "AFA     "."RCC_PJCBKA"."BOJEDT" IS 'ԭ��������';

COMMENT ON COLUMN "AFA     "."RCC_PJCBKA"."BOSPSQ" IS 'ԭ�������';

COMMENT ON COLUMN "AFA     "."RCC_PJCBKA"."BRSFLG" IS '������ʶ(0-����;1-����)';

COMMENT ON COLUMN "AFA     "."RCC_PJCBKA"."BSPSQN" IS '�������';

COMMENT ON COLUMN "AFA     "."RCC_PJCBKA"."CONT" IS '����';

COMMENT ON COLUMN "AFA     "."RCC_PJCBKA"."HONBNKNM" IS '�ж�������';

COMMENT ON COLUMN "AFA     "."RCC_PJCBKA"."ISDEAL" IS '�鸴��ʶ(0-δ�鸴;1-�Ѳ鸴)';

COMMENT ON COLUMN "AFA     "."RCC_PJCBKA"."NCCWKDAT" IS '��������';

COMMENT ON COLUMN "AFA     "."RCC_PJCBKA"."NOTE1" IS '�����ֶ�1';

COMMENT ON COLUMN "AFA     "."RCC_PJCBKA"."NOTE2" IS '�����ֶ�2';

COMMENT ON COLUMN "AFA     "."RCC_PJCBKA"."NOTE3" IS '�����ֶ�3';

COMMENT ON COLUMN "AFA     "."RCC_PJCBKA"."NOTE4" IS '�����ֶ�4';

COMMENT ON COLUMN "AFA     "."RCC_PJCBKA"."ORTRCCO" IS 'ԭ���״���';

COMMENT ON COLUMN "AFA     "."RCC_PJCBKA"."PRCCO" IS '���ķ�����';

COMMENT ON COLUMN "AFA     "."RCC_PJCBKA"."PYENAM" IS '�տ�������';

COMMENT ON COLUMN "AFA     "."RCC_PJCBKA"."RCVBNKCO" IS '�������к�';

COMMENT ON COLUMN "AFA     "."RCC_PJCBKA"."RCVBNKNM" IS '����������';

COMMENT ON COLUMN "AFA     "."RCC_PJCBKA"."RCVMBRCO" IS '���ճ�Ա�к�';

COMMENT ON COLUMN "AFA     "."RCC_PJCBKA"."SNDBNKCO" IS '�������к�';

COMMENT ON COLUMN "AFA     "."RCC_PJCBKA"."SNDBNKNM" IS '����������';

COMMENT ON COLUMN "AFA     "."RCC_PJCBKA"."SNDMBRCO" IS '���ͳ�Ա�к�';

COMMENT ON COLUMN "AFA     "."RCC_PJCBKA"."STRINFO" IS '���ķ�����˵��';

COMMENT ON COLUMN "AFA     "."RCC_PJCBKA"."TRCCO" IS '���״���';

COMMENT ON COLUMN "AFA     "."RCC_PJCBKA"."TRCDAT" IS 'ί������';

COMMENT ON COLUMN "AFA     "."RCC_PJCBKA"."TRCNO" IS '������ˮ��';





------------------------------------------------
-- DDL Statements for table "AFA     "."RCC_REKBAL"
------------------------------------------------
DROP TABLE "AFA     "."RCC_REKBAL";

CREATE TABLE "AFA     "."RCC_REKBAL"  (
		  "BJEDTE" VARCHAR(8) NOT NULL , 
		  "BSPSQN" VARCHAR(12) NOT NULL , 
		  "BRSFLG" VARCHAR(1) , 
		  "TRCCO" VARCHAR(7) , 
		  "NCCWKDAT" VARCHAR(8) , 
		  "TRCDAT" VARCHAR(8) , 
		  "TRCNO" VARCHAR(8) , 
		  "SNDMBRCO" VARCHAR(10) , 
		  "RCVMBRCO" VARCHAR(10) , 
		  "SNDBNKCO" VARCHAR(10) , 
		  "SNDBNKNM" VARCHAR(60) , 
		  "RCVBNKCO" VARCHAR(10) , 
		  "RCVBNKNM" VARCHAR(60) , 
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
		  "BOJEDT" VARCHAR(8) , 
		  "BOSPSQ" VARCHAR(12) , 
		  "PRCCO" VARCHAR(8) , 
		  "STRINFO" VARCHAR(60) , 
		  "NOTE1" VARCHAR(10) , 
		  "NOTE2" VARCHAR(20) , 
		  "NOTE3" VARCHAR(60) , 
		  "NOTE4" VARCHAR(60) )   
		 IN "AFA_DATA" INDEX IN "AFA_IDX" ; 

COMMENT ON COLUMN "AFA     "."RCC_REKBAL"."AVLBAL" IS '�������';

COMMENT ON COLUMN "AFA     "."RCC_REKBAL"."BALDCFLG" IS '�������跽������ʶ';

COMMENT ON COLUMN "AFA     "."RCC_REKBAL"."BJEDTE" IS '��������';

COMMENT ON COLUMN "AFA     "."RCC_REKBAL"."BOJEDT" IS 'ԭ��������';

COMMENT ON COLUMN "AFA     "."RCC_REKBAL"."BOSPSQ" IS 'ԭ�������';

COMMENT ON COLUMN "AFA     "."RCC_REKBAL"."BRSFLG" IS '������ʶ(0-����;1-����)';

COMMENT ON COLUMN "AFA     "."RCC_REKBAL"."BSPSQN" IS '�������';

COMMENT ON COLUMN "AFA     "."RCC_REKBAL"."CHKRST" IS '���˽��';

COMMENT ON COLUMN "AFA     "."RCC_REKBAL"."CUR" IS '����';

COMMENT ON COLUMN "AFA     "."RCC_REKBAL"."LBDCFLG" IS '�������跽������ʶ';

COMMENT ON COLUMN "AFA     "."RCC_REKBAL"."LSTDTBAL" IS '�������';

COMMENT ON COLUMN "AFA     "."RCC_REKBAL"."NCCWKDAT" IS '��������';

COMMENT ON COLUMN "AFA     "."RCC_REKBAL"."NOTE1" IS '�����ֶ�1';

COMMENT ON COLUMN "AFA     "."RCC_REKBAL"."NOTE2" IS '�����ֶ�2';

COMMENT ON COLUMN "AFA     "."RCC_REKBAL"."NOTE3" IS '�����ֶ�3';

COMMENT ON COLUMN "AFA     "."RCC_REKBAL"."NOTE4" IS '�����ֶ�4';

COMMENT ON COLUMN "AFA     "."RCC_REKBAL"."NTODAYBAL" IS '���ڽ������';

COMMENT ON COLUMN "AFA     "."RCC_REKBAL"."NTTBAL" IS '���������';

COMMENT ON COLUMN "AFA     "."RCC_REKBAL"."NTTDCFLG" IS '���������跽������ʶ';

COMMENT ON COLUMN "AFA     "."RCC_REKBAL"."PRCCO" IS '���ķ�����';

COMMENT ON COLUMN "AFA     "."RCC_REKBAL"."RCVBNKCO" IS '�������к�';

COMMENT ON COLUMN "AFA     "."RCC_REKBAL"."RCVBNKNM" IS '����������';

COMMENT ON COLUMN "AFA     "."RCC_REKBAL"."RCVMBRCO" IS '���ճ�Ա�к�';

COMMENT ON COLUMN "AFA     "."RCC_REKBAL"."SNDBNKCO" IS '�������к�';

COMMENT ON COLUMN "AFA     "."RCC_REKBAL"."SNDBNKNM" IS '����������';

COMMENT ON COLUMN "AFA     "."RCC_REKBAL"."SNDMBRCO" IS '���ͳ�Ա�к�';

COMMENT ON COLUMN "AFA     "."RCC_REKBAL"."STRINFO" IS '���ķ�����˵��';

COMMENT ON COLUMN "AFA     "."RCC_REKBAL"."TODAYBAL" IS '�������';

COMMENT ON COLUMN "AFA     "."RCC_REKBAL"."TRCCO" IS '���״���';

COMMENT ON COLUMN "AFA     "."RCC_REKBAL"."TRCDAT" IS 'ί������';

COMMENT ON COLUMN "AFA     "."RCC_REKBAL"."TRCNO" IS '������ˮ��';


-- DDL Statements for indexes on Table "AFA     "."RCC_REKBAL"

CREATE UNIQUE INDEX "AFA     "."RCC_REKBAL_IDX1" ON "AFA     "."RCC_REKBAL" 
		("TRCDAT" ASC,
		 "TRCNO" ASC,
		 "SNDBNKCO" ASC)
		PCTFREE 10 ALLOW REVERSE SCANS;


-- DDL Statements for primary key on Table "AFA     "."RCC_REKBAL"

ALTER TABLE "AFA     "."RCC_REKBAL" 
	ADD CONSTRAINT "RCC_REKBAL_PK" PRIMARY KEY
		("BJEDTE",
		 "BSPSQN");


------------------------------------------------
-- DDL Statements for table "AFA     "."RCC_HDCBKA"
------------------------------------------------
DROP TABLE "AFA     "."RCC_HDCBKA";

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
		  "PYRNAM" VARCHAR(60) , 
		  "PYEACC" VARCHAR(32) , 
		  "PYENAM" VARCHAR(60) , 
		  "ISDEAL" VARCHAR(1) , 
		  "PRCCO" VARCHAR(8) , 
		  "STRINFO" VARCHAR(60) , 
		  "NOTE1" VARCHAR(10) , 
		  "NOTE2" VARCHAR(20) , 
		  "NOTE3" VARCHAR(60) , 
		  "NOTE4" VARCHAR(60) )   
		 IN "AFA_DATA" INDEX IN "AFA_IDX" ; 

COMMENT ON COLUMN "AFA     "."RCC_HDCBKA"."BEAUUS" IS '��Ȩ��Ա��';

COMMENT ON COLUMN "AFA     "."RCC_HDCBKA"."BESBNO" IS '������';

COMMENT ON COLUMN "AFA     "."RCC_HDCBKA"."BETELR" IS '��Ա��';

COMMENT ON COLUMN "AFA     "."RCC_HDCBKA"."BJEDTE" IS '��������';

COMMENT ON COLUMN "AFA     "."RCC_HDCBKA"."BOJEDT" IS 'ԭ��������';

COMMENT ON COLUMN "AFA     "."RCC_HDCBKA"."BOSPSQ" IS 'ԭ�������';

COMMENT ON COLUMN "AFA     "."RCC_HDCBKA"."BRSFLG" IS '������ʶ(0-����;1-����)';

COMMENT ON COLUMN "AFA     "."RCC_HDCBKA"."BSPSQN" IS '�������';

COMMENT ON COLUMN "AFA     "."RCC_HDCBKA"."CONT" IS '����';

COMMENT ON COLUMN "AFA     "."RCC_HDCBKA"."CUR" IS '����';

COMMENT ON COLUMN "AFA     "."RCC_HDCBKA"."ISDEAL" IS '��ѯ�鸴��ʶ(0-δ�鸴;1-�Ѳ鸴)';

COMMENT ON COLUMN "AFA     "."RCC_HDCBKA"."NCCWKDAT" IS '��������';

COMMENT ON COLUMN "AFA     "."RCC_HDCBKA"."NOTE1" IS '�����ֶ�1';

COMMENT ON COLUMN "AFA     "."RCC_HDCBKA"."NOTE2" IS '�����ֶ�2';

COMMENT ON COLUMN "AFA     "."RCC_HDCBKA"."NOTE3" IS '�����ֶ�3';

COMMENT ON COLUMN "AFA     "."RCC_HDCBKA"."NOTE4" IS '�����ֶ�4';

COMMENT ON COLUMN "AFA     "."RCC_HDCBKA"."OCCAMT" IS '���׽��';

COMMENT ON COLUMN "AFA     "."RCC_HDCBKA"."ORTRCCO" IS 'ԭ���״���';

COMMENT ON COLUMN "AFA     "."RCC_HDCBKA"."PRCCO" IS '���ķ�����';

COMMENT ON COLUMN "AFA     "."RCC_HDCBKA"."PYEACC" IS '�տ����˺�';

COMMENT ON COLUMN "AFA     "."RCC_HDCBKA"."PYENAM" IS '�տ��˻���';

COMMENT ON COLUMN "AFA     "."RCC_HDCBKA"."PYRACC" IS '�������˺�';

COMMENT ON COLUMN "AFA     "."RCC_HDCBKA"."PYRNAM" IS '�����˻���';

COMMENT ON COLUMN "AFA     "."RCC_HDCBKA"."RCVBNKCO" IS '�������к�';

COMMENT ON COLUMN "AFA     "."RCC_HDCBKA"."RCVBNKNM" IS '����������';

COMMENT ON COLUMN "AFA     "."RCC_HDCBKA"."RCVMBRCO" IS '���ճ�Ա�к�';

COMMENT ON COLUMN "AFA     "."RCC_HDCBKA"."SNDBNKCO" IS '�������к�';

COMMENT ON COLUMN "AFA     "."RCC_HDCBKA"."SNDBNKNM" IS '����������';

COMMENT ON COLUMN "AFA     "."RCC_HDCBKA"."SNDMBRCO" IS '���ͳ�Ա�к�';

COMMENT ON COLUMN "AFA     "."RCC_HDCBKA"."STRINFO" IS '���ķ�����˵��';

COMMENT ON COLUMN "AFA     "."RCC_HDCBKA"."TRCCO" IS '���״���';

COMMENT ON COLUMN "AFA     "."RCC_HDCBKA"."TRCDAT" IS 'ί������';

COMMENT ON COLUMN "AFA     "."RCC_HDCBKA"."TRCNO" IS '������ˮ��';


-- DDL Statements for primary key on Table "AFA     "."RCC_HDCBKA"

ALTER TABLE "AFA     "."RCC_HDCBKA" 
	ADD CONSTRAINT "RCC_HDCBKA_PK" PRIMARY KEY
		("BJEDTE",
		 "BSPSQN");


------------------------------------------------
-- DDL Statements for table "AFA     "."RCC_TRCBKA"
------------------------------------------------
DROP TABLE "AFA     "."RCC_TRCBKA";

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
		  "TRCDAT" VARCHAR(8) NOT NULL , 
		  "TRCNO" VARCHAR(8) NOT NULL , 
		  "SNDMBRCO" VARCHAR(10) , 
		  "RCVMBRCO" VARCHAR(10) , 
		  "SNDBNKCO" VARCHAR(10) NOT NULL , 
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

COMMENT ON COLUMN "AFA     "."RCC_TRCBKA"."BBSSRC" IS '�ʽ���Դ';

COMMENT ON COLUMN "AFA     "."RCC_TRCBKA"."BEACSB" IS '���������';

COMMENT ON COLUMN "AFA     "."RCC_TRCBKA"."BEAUUS" IS '��Ȩ��Ա��';

COMMENT ON COLUMN "AFA     "."RCC_TRCBKA"."BESBNO" IS '������';

COMMENT ON COLUMN "AFA     "."RCC_TRCBKA"."BETELR" IS '��Ա��';

COMMENT ON COLUMN "AFA     "."RCC_TRCBKA"."BILDAT" IS 'Ʊ������';

COMMENT ON COLUMN "AFA     "."RCC_TRCBKA"."BILNO" IS 'Ʊ�ݺ���';

COMMENT ON COLUMN "AFA     "."RCC_TRCBKA"."BILTYP" IS 'Ʊ������';

COMMENT ON COLUMN "AFA     "."RCC_TRCBKA"."BJEDTE" IS '��������';

COMMENT ON COLUMN "AFA     "."RCC_TRCBKA"."BOJEDT" IS 'ԭ��������';

COMMENT ON COLUMN "AFA     "."RCC_TRCBKA"."BOSPSQ" IS 'ԭ�������';

COMMENT ON COLUMN "AFA     "."RCC_TRCBKA"."BRSFLG" IS '������ʶ(0-����;1-����)';

COMMENT ON COLUMN "AFA     "."RCC_TRCBKA"."BSPSQN" IS '�������';

COMMENT ON COLUMN "AFA     "."RCC_TRCBKA"."CERTNO" IS '֤������';

COMMENT ON COLUMN "AFA     "."RCC_TRCBKA"."CERTTYPE" IS '֤������';

COMMENT ON COLUMN "AFA     "."RCC_TRCBKA"."CHRGTYP" IS '��������ȡ��ʽ';

COMMENT ON COLUMN "AFA     "."RCC_TRCBKA"."COMAMT" IS 'ԭ���ս��';

COMMENT ON COLUMN "AFA     "."RCC_TRCBKA"."CPSAMT" IS '�⳥����';

COMMENT ON COLUMN "AFA     "."RCC_TRCBKA"."CUR" IS '����';

COMMENT ON COLUMN "AFA     "."RCC_TRCBKA"."CUSCHRG" IS '��ؿͻ�������';

COMMENT ON COLUMN "AFA     "."RCC_TRCBKA"."DASQ" IS '�������';

COMMENT ON COLUMN "AFA     "."RCC_TRCBKA"."DCFLG" IS '�����ʶ(1-��;2-��)';

COMMENT ON COLUMN "AFA     "."RCC_TRCBKA"."LOCCUSCHRG" IS '���ؿͻ�������';

COMMENT ON COLUMN "AFA     "."RCC_TRCBKA"."NCCWKDAT" IS '��������';

COMMENT ON COLUMN "AFA     "."RCC_TRCBKA"."NOTE1" IS '�����ֶ�1';

COMMENT ON COLUMN "AFA     "."RCC_TRCBKA"."NOTE2" IS '�����ֶ�2';

COMMENT ON COLUMN "AFA     "."RCC_TRCBKA"."NOTE3" IS '�����ֶ�3';

COMMENT ON COLUMN "AFA     "."RCC_TRCBKA"."NOTE4" IS '�����ֶ�4';

COMMENT ON COLUMN "AFA     "."RCC_TRCBKA"."OCCAMT" IS '���׽��';

COMMENT ON COLUMN "AFA     "."RCC_TRCBKA"."OPRATTNO" IS 'ҵ������';

COMMENT ON COLUMN "AFA     "."RCC_TRCBKA"."OPRNO" IS 'ҵ������';

COMMENT ON COLUMN "AFA     "."RCC_TRCBKA"."ORRCVBNK" IS 'ԭ�����к�';

COMMENT ON COLUMN "AFA     "."RCC_TRCBKA"."ORSNDBNK" IS 'ԭ�����к�';

COMMENT ON COLUMN "AFA     "."RCC_TRCBKA"."ORTRCCO" IS 'ԭ���״���';

COMMENT ON COLUMN "AFA     "."RCC_TRCBKA"."ORTRCDAT" IS 'ԭί������';

COMMENT ON COLUMN "AFA     "."RCC_TRCBKA"."ORTRCNO" IS 'ԭ������ˮ��';

COMMENT ON COLUMN "AFA     "."RCC_TRCBKA"."OVPAYAMT" IS '�ึ���';

COMMENT ON COLUMN "AFA     "."RCC_TRCBKA"."PYEACC" IS '�տ����˺�';

COMMENT ON COLUMN "AFA     "."RCC_TRCBKA"."PYEADDR" IS '�տ��˵�ַ';

COMMENT ON COLUMN "AFA     "."RCC_TRCBKA"."PYENAM" IS '�տ��˻���';

COMMENT ON COLUMN "AFA     "."RCC_TRCBKA"."PYRACC" IS '�������˺�';

COMMENT ON COLUMN "AFA     "."RCC_TRCBKA"."PYRADDR" IS '�����˵�ַ';

COMMENT ON COLUMN "AFA     "."RCC_TRCBKA"."PYRNAM" IS '�����˻���';

COMMENT ON COLUMN "AFA     "."RCC_TRCBKA"."RCVBNKCO" IS '�������к�';

COMMENT ON COLUMN "AFA     "."RCC_TRCBKA"."RCVBNKNM" IS '����������';

COMMENT ON COLUMN "AFA     "."RCC_TRCBKA"."RCVMBRCO" IS '���ճ�Ա�к�';

COMMENT ON COLUMN "AFA     "."RCC_TRCBKA"."REMARK" IS '��ע';

COMMENT ON COLUMN "AFA     "."RCC_TRCBKA"."RFUAMT" IS '�ܸ����';

COMMENT ON COLUMN "AFA     "."RCC_TRCBKA"."SEAL" IS '��Ѻ';

COMMENT ON COLUMN "AFA     "."RCC_TRCBKA"."SNDBNKCO" IS '�������к�';

COMMENT ON COLUMN "AFA     "."RCC_TRCBKA"."SNDBNKNM" IS '����������';

COMMENT ON COLUMN "AFA     "."RCC_TRCBKA"."SNDMBRCO" IS '���ͳ�Ա�к�';

COMMENT ON COLUMN "AFA     "."RCC_TRCBKA"."STRINFO" IS '����';

COMMENT ON COLUMN "AFA     "."RCC_TRCBKA"."TERMID" IS '�ն˺�';

COMMENT ON COLUMN "AFA     "."RCC_TRCBKA"."TRCCO" IS '���״���';

COMMENT ON COLUMN "AFA     "."RCC_TRCBKA"."TRCDAT" IS 'ί������';

COMMENT ON COLUMN "AFA     "."RCC_TRCBKA"."TRCNO" IS '������ˮ��';

COMMENT ON COLUMN "AFA     "."RCC_TRCBKA"."USE" IS '��;';


-- DDL Statements for primary key on Table "AFA     "."RCC_TRCBKA"

ALTER TABLE "AFA     "."RCC_TRCBKA" 
	ADD CONSTRAINT "RCC_TRCBKA_PK" PRIMARY KEY
		("BJEDTE",
		 "BSPSQN");


-- DDL Statements for unique constraints on Table "AFA     "."RCC_TRCBKA"


ALTER TABLE "AFA     "."RCC_TRCBKA" 
	ADD UNIQUE
		("TRCDAT",
		 "TRCNO",
		 "SNDBNKCO");

------------------------------------------------
-- DDL Statements for table "AFA     "."RCC_BILBKA"
------------------------------------------------
DROP TABLE "AFA     "."RCC_BILBKA";

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
		  "OPRNO" VARCHAR(2) , 
		  "OPRATTNO" VARCHAR(2) , 
		  "NCCWKDAT" VARCHAR(8) , 
		  "TRCCO" VARCHAR(7) , 
		  "TRCDAT" VARCHAR(8) NOT NULL , 
		  "TRCNO" VARCHAR(8) NOT NULL , 
		  "SNDMBRCO" VARCHAR(10) , 
		  "RCVMBRCO" VARCHAR(10) , 
		  "SNDBNKCO" VARCHAR(10) NOT NULL , 
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
		  "CERTTYPE" VARCHAR(2) , 
		  "CERTNO" VARCHAR(20) , 
		  "NOTE1" VARCHAR(10) , 
		  "NOTE2" VARCHAR(20) , 
		  "NOTE3" VARCHAR(60) , 
		  "NOTE4" VARCHAR(60) )   
		 IN "AFA_DATA" INDEX IN "AFA_IDX" ; 

COMMENT ON COLUMN "AFA     "."RCC_BILBKA"."BBSSRC" IS '�ʽ���Դ';

COMMENT ON COLUMN "AFA     "."RCC_BILBKA"."BEACSB" IS '���������';

COMMENT ON COLUMN "AFA     "."RCC_BILBKA"."BEAUUS" IS '��Ȩ��Ա��';

COMMENT ON COLUMN "AFA     "."RCC_BILBKA"."BESBNO" IS '������';

COMMENT ON COLUMN "AFA     "."RCC_BILBKA"."BETELR" IS '��Ա��';

COMMENT ON COLUMN "AFA     "."RCC_BILBKA"."BILNO" IS '��Ʊ����';

COMMENT ON COLUMN "AFA     "."RCC_BILBKA"."BILRS" IS '��Ʊ�������б�ʶ(0-����ǩ���Ļ�Ʊ;1-����ǩ���Ļ�Ʊ)';

COMMENT ON COLUMN "AFA     "."RCC_BILBKA"."BILVER" IS '��Ʊ�汾��';

COMMENT ON COLUMN "AFA     "."RCC_BILBKA"."BJEDTE" IS '��������';

COMMENT ON COLUMN "AFA     "."RCC_BILBKA"."BRSFLG" IS '������ʶ(0-����;1-����)';

COMMENT ON COLUMN "AFA     "."RCC_BILBKA"."BSPSQN" IS '�������';

COMMENT ON COLUMN "AFA     "."RCC_BILBKA"."CERTNO" IS '֤������';

COMMENT ON COLUMN "AFA     "."RCC_BILBKA"."CERTTYPE" IS '֤������';

COMMENT ON COLUMN "AFA     "."RCC_BILBKA"."CHRGTYP" IS '��������ȡ��ʽ';

COMMENT ON COLUMN "AFA     "."RCC_BILBKA"."DASQ" IS '�������';

COMMENT ON COLUMN "AFA     "."RCC_BILBKA"."DCFLG" IS '�����ʶ(1-��;2-��)';

COMMENT ON COLUMN "AFA     "."RCC_BILBKA"."HPCUSQ" IS '��Ʊ״̬���';

COMMENT ON COLUMN "AFA     "."RCC_BILBKA"."HPSTAT" IS '��Ʊ״̬';

COMMENT ON COLUMN "AFA     "."RCC_BILBKA"."LOCCUSCHRG" IS '������';

COMMENT ON COLUMN "AFA     "."RCC_BILBKA"."NCCWKDAT" IS '��������';

COMMENT ON COLUMN "AFA     "."RCC_BILBKA"."NOTE1" IS '�����ֶ�1';

COMMENT ON COLUMN "AFA     "."RCC_BILBKA"."NOTE2" IS '�����ֶ�2';

COMMENT ON COLUMN "AFA     "."RCC_BILBKA"."NOTE3" IS '�����ֶ�3';

COMMENT ON COLUMN "AFA     "."RCC_BILBKA"."NOTE4" IS '�����ֶ�4';

COMMENT ON COLUMN "AFA     "."RCC_BILBKA"."OPRATTNO" IS 'ҵ������';

COMMENT ON COLUMN "AFA     "."RCC_BILBKA"."OPRNO" IS 'ҵ������';

COMMENT ON COLUMN "AFA     "."RCC_BILBKA"."RCVBNKCO" IS '�������к�';

COMMENT ON COLUMN "AFA     "."RCC_BILBKA"."RCVBNKNM" IS '����������';

COMMENT ON COLUMN "AFA     "."RCC_BILBKA"."RCVMBRCO" IS '���ճ�Ա�к�';

COMMENT ON COLUMN "AFA     "."RCC_BILBKA"."SNDBNKCO" IS '�������к�';

COMMENT ON COLUMN "AFA     "."RCC_BILBKA"."SNDBNKNM" IS '����������';

COMMENT ON COLUMN "AFA     "."RCC_BILBKA"."SNDMBRCO" IS '���ͳ�Ա�к�';

COMMENT ON COLUMN "AFA     "."RCC_BILBKA"."TERMID" IS '�ն˺�';

COMMENT ON COLUMN "AFA     "."RCC_BILBKA"."TRCCO" IS '���״���';

COMMENT ON COLUMN "AFA     "."RCC_BILBKA"."TRCDAT" IS '��������';

COMMENT ON COLUMN "AFA     "."RCC_BILBKA"."TRCNO" IS '������ˮ��';


-- DDL Statements for primary key on Table "AFA     "."RCC_BILBKA"

ALTER TABLE "AFA     "."RCC_BILBKA" 
	ADD CONSTRAINT "RCC_BILBKA_PK" PRIMARY KEY
		("BJEDTE",
		 "BSPSQN");


-- DDL Statements for unique constraints on Table "AFA     "."RCC_BILBKA"


ALTER TABLE "AFA     "."RCC_BILBKA" 
	ADD UNIQUE
		("TRCDAT",
		 "TRCNO",
		 "SNDBNKCO");

------------------------------------------------
-- DDL Statements for table "AFA     "."RCC_ZTCBKA"
------------------------------------------------
DROP TABLE "AFA     "."RCC_ZTCBKA";

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
		  "STRINFO" VARCHAR(60) , 
		  "NOTE1" VARCHAR(10) , 
		  "NOTE2" VARCHAR(20) , 
		  "NOTE3" VARCHAR(60) , 
		  "NOTE4" VARCHAR(60) )   
		 IN "AFA_DATA" INDEX IN "AFA_IDX" ; 

COMMENT ON COLUMN "AFA     "."RCC_ZTCBKA"."BEACSB" IS '���������';

COMMENT ON COLUMN "AFA     "."RCC_ZTCBKA"."BEAUUS" IS '��Ȩ��Ա��';

COMMENT ON COLUMN "AFA     "."RCC_ZTCBKA"."BESBNO" IS '������';

COMMENT ON COLUMN "AFA     "."RCC_ZTCBKA"."BETELR" IS '��Ա��';

COMMENT ON COLUMN "AFA     "."RCC_ZTCBKA"."BJEDTE" IS '��������';

COMMENT ON COLUMN "AFA     "."RCC_ZTCBKA"."BOJEDT" IS 'ԭ��������';

COMMENT ON COLUMN "AFA     "."RCC_ZTCBKA"."BOSPSQ" IS 'ԭ�������';

COMMENT ON COLUMN "AFA     "."RCC_ZTCBKA"."BRSFLG" IS '������ʶ(0-����;1-����)';

COMMENT ON COLUMN "AFA     "."RCC_ZTCBKA"."BSPSQN" IS '�������';

COMMENT ON COLUMN "AFA     "."RCC_ZTCBKA"."CONT" IS '����';

COMMENT ON COLUMN "AFA     "."RCC_ZTCBKA"."CUR" IS '����';

COMMENT ON COLUMN "AFA     "."RCC_ZTCBKA"."ISDEAL" IS '�鸴��ʶ(0-δ�鸴;1-�Ѳ鸴)';

COMMENT ON COLUMN "AFA     "."RCC_ZTCBKA"."MBRTRCST" IS '��Ա�н���״̬';

COMMENT ON COLUMN "AFA     "."RCC_ZTCBKA"."NCCTRCST" IS '���Ľ���״̬';

COMMENT ON COLUMN "AFA     "."RCC_ZTCBKA"."NCCWKDAT" IS '��������';

COMMENT ON COLUMN "AFA     "."RCC_ZTCBKA"."NOTE1" IS '�����ֶ�1';

COMMENT ON COLUMN "AFA     "."RCC_ZTCBKA"."NOTE2" IS '�����ֶ�2';

COMMENT ON COLUMN "AFA     "."RCC_ZTCBKA"."NOTE3" IS '�����ֶ�3';

COMMENT ON COLUMN "AFA     "."RCC_ZTCBKA"."NOTE4" IS '�����ֶ�4';

COMMENT ON COLUMN "AFA     "."RCC_ZTCBKA"."OCCAMT" IS '���׽��';

COMMENT ON COLUMN "AFA     "."RCC_ZTCBKA"."ORTRCCO" IS 'ԭ���״���';

COMMENT ON COLUMN "AFA     "."RCC_ZTCBKA"."PRCCO" IS '���ķ�����';

COMMENT ON COLUMN "AFA     "."RCC_ZTCBKA"."RCVBNKCO" IS '�������к�';

COMMENT ON COLUMN "AFA     "."RCC_ZTCBKA"."RCVBNKNM" IS '����������';

COMMENT ON COLUMN "AFA     "."RCC_ZTCBKA"."RCVMBRCO" IS '���ճ�Ա�к�';

COMMENT ON COLUMN "AFA     "."RCC_ZTCBKA"."SNDBNKCO" IS '�������к�';

COMMENT ON COLUMN "AFA     "."RCC_ZTCBKA"."SNDBNKNM" IS '����������';

COMMENT ON COLUMN "AFA     "."RCC_ZTCBKA"."SNDMBRCO" IS '���ͳ�Ա�к�';

COMMENT ON COLUMN "AFA     "."RCC_ZTCBKA"."STRINFO" IS '���ķ�����˵��';

COMMENT ON COLUMN "AFA     "."RCC_ZTCBKA"."TRCCO" IS '���״���';

COMMENT ON COLUMN "AFA     "."RCC_ZTCBKA"."TRCDAT" IS 'ί������';

COMMENT ON COLUMN "AFA     "."RCC_ZTCBKA"."TRCNO" IS '������ˮ��';


-- DDL Statements for primary key on Table "AFA     "."RCC_ZTCBKA"

ALTER TABLE "AFA     "."RCC_ZTCBKA" 
	ADD CONSTRAINT "RCC_ZTCBKA_PK" PRIMARY KEY
		("BJEDTE",
		 "BSPSQN",
		 "BRSFLG");


------------------------------------------------
-- DDL Statements for table "AFA     "."RCC_QSQHQD"
------------------------------------------------
DROP TABLE "AFA     "."RCC_QSQHQD";

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
		  "STRINFO" VARCHAR(60) , 
		  "NOTE1" VARCHAR(20) , 
		  "NOTE2" VARCHAR(20) , 
		  "NOTE3" VARCHAR(60) , 
		  "NOTE4" VARCHAR(60) )   
		 IN "AFA_DATA" INDEX IN "AFA_IDX" ; 

COMMENT ON COLUMN "AFA     "."RCC_QSQHQD"."BESBNM" IS '��������';

COMMENT ON COLUMN "AFA     "."RCC_QSQHQD"."BESBNO" IS '������';

COMMENT ON COLUMN "AFA     "."RCC_QSQHQD"."BILCHRGAMT" IS 'ȫ����Ʊ�������ܽ��';

COMMENT ON COLUMN "AFA     "."RCC_QSQHQD"."BILCHRGCNT" IS 'ȫ����Ʊ�������ܱ���';

COMMENT ON COLUMN "AFA     "."RCC_QSQHQD"."ENDDAT" IS '��������';

COMMENT ON COLUMN "AFA     "."RCC_QSQHQD"."FEDT" IS 'ǰ������';

COMMENT ON COLUMN "AFA     "."RCC_QSQHQD"."ISDEAL" IS '�����ʶ(0-δ����;1-�Ѵ���)';

COMMENT ON COLUMN "AFA     "."RCC_QSQHQD"."MGID" IS '����������';

COMMENT ON COLUMN "AFA     "."RCC_QSQHQD"."NOTE1" IS '�����ֶ�1';

COMMENT ON COLUMN "AFA     "."RCC_QSQHQD"."NOTE2" IS '�����ֶ�2';

COMMENT ON COLUMN "AFA     "."RCC_QSQHQD"."NOTE3" IS '�����ֶ�3';

COMMENT ON COLUMN "AFA     "."RCC_QSQHQD"."NOTE4" IS '�����ֶ�4';

COMMENT ON COLUMN "AFA     "."RCC_QSQHQD"."RBSQ" IS 'ǰ����ˮ��';

COMMENT ON COLUMN "AFA     "."RCC_QSQHQD"."STRDAT" IS '��ʼ����';

COMMENT ON COLUMN "AFA     "."RCC_QSQHQD"."STRINFO" IS '������˵��';

COMMENT ON COLUMN "AFA     "."RCC_QSQHQD"."TAMT" IS '���ܽ��';

COMMENT ON COLUMN "AFA     "."RCC_QSQHQD"."TCNT" IS '���ܱ���';

COMMENT ON COLUMN "AFA     "."RCC_QSQHQD"."TLSQ" IS '������ˮ��';

COMMENT ON COLUMN "AFA     "."RCC_QSQHQD"."TRCCHRGAMT" IS 'ʵʱ����������ܽ��';

COMMENT ON COLUMN "AFA     "."RCC_QSQHQD"."TRCCHRGCNT" IS 'ʵʱ����������ܱ���';

COMMENT ON COLUMN "AFA     "."RCC_QSQHQD"."TRDT" IS '��������';

COMMENT ON COLUMN "AFA     "."RCC_QSQHQD"."UCSWCHRGAMT" IS 'ͨ��ͨ���������ܽ��';

COMMENT ON COLUMN "AFA     "."RCC_QSQHQD"."UCSWCHRGCNT" IS 'ͨ��ͨ���������ܱ���';


-- DDL Statements for primary key on Table "AFA     "."RCC_QSQHQD"

ALTER TABLE "AFA     "."RCC_QSQHQD" 
	ADD CONSTRAINT "RCC_QSQHQD_PK" PRIMARY KEY
		("STRDAT",
		 "ENDDAT",
		 "BESBNO");








COMMIT WORK;

CONNECT RESET;

TERMINATE;

