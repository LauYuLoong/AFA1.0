---------------------------------------
--�������нŲ�
--����:������
--ʱ��:2008-08-02
--����:��ԭ�����ɻ������ݿ��������е���
--     ƽ̨���ݿ���
---------------------------------------

CONNECT TO AFA;

---------------------------------------
--ƽ̨��������
---------------------------------------

EXPORT TO BUSIINFO.del OF DEL SELECT * FROM DSDF_BUSIINFO;

EXPORT TO CUSTINFO.del OF DEL SELECT * FROM DSDF_CUSTINFO;

EXPORT TO BATCHINFO.del OF DEL SELECT * FROM DSDF_BATCHINFO;

EXPORT TO HISBUSIINFO.del OF DEL SELECT * FROM DSDF_HIS_BUSIINFO;

EXPORT TO HISCUSTINFO.del OF DEL SELECT * FROM DSDF_HIS_CUSTINFO;

EXPORT TO HISBATCHINFO.del OF DEL SELECT * FROM DSDF_HIS_BATCHINFO;

EXPORT TO CZDZB.del OF DEL SELECT * FROM DSDF_CZDZB;

EXPORT TO SUMMARY.del OF DEL SELECT * FROM DSDF_SUMMARY;

EXPORT TO MAINTRANSDTL.del OF DEL SELECT * FROM DSDF_MAINTRANSDTL WHERE APPNO='AG2008';

---------------------------------------
--��˰ҵ����������
---------------------------------------

EXPORT TO AA11.del OF DEL SELECT * FROM FS_AA11;

EXPORT TO BUSINOCONF.del OF DEL SELECT * FROM FS_BUSINOCONF;

EXPORT TO BUSINOINFO.del OF DEL SELECT * FROM FS_BUSINOINFO;

EXPORT TO DETAIL.del OF DEL SELECT * FROM FS_DETAIL;

EXPORT TO DPZGL.del OF DEL SELECT * FROM FS_DPZ_GL;

EXPORT TO FA13.del OF DEL SELECT * FROM FS_FA13;

EXPORT TO FA15.del OF DEL SELECT * FROM FS_FA15;

EXPORT TO FA16.del OF DEL SELECT * FROM FS_FA16;

EXPORT TO FA20.del OF DEL SELECT * FROM FS_FA20;

EXPORT TO FA21.del OF DEL SELECT * FROM FS_FA21;

EXPORT TO FA22.del OF DEL SELECT * FROM FS_FA22;

EXPORT TO FC06.del OF DEL SELECT * FROM FS_FC06;

EXPORT TO FC60.del OF DEL SELECT * FROM FS_FC60;

EXPORT TO FC70.del OF DEL SELECT * FROM FS_FC70;

EXPORT TO FC74.del OF DEL SELECT * FROM FS_FC74;

EXPORT TO FC74OUT.del OF DEL SELECT * FROM FS_FC74_OUT;

EXPORT TO FC75.del OF DEL SELECT * FROM FS_FC75;

EXPORT TO FC76.del OF DEL SELECT * FROM FS_FC76;

EXPORT TO FC76OUT.del OF DEL SELECT * FROM FS_FC76_OUT;

EXPORT TO FC84.del OF DEL SELECT * FROM FS_FC84;

EXPORT TO REMAIN.del OF DEL SELECT * FROM FS_REMAIN;

----------------------------------
--�����ύ
----------------------------------

COMMIT WORK;

CONNECT RESET;

TERMINATE;