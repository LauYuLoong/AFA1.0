insert into rcc_wtrbka_his (select * from rcc_wtrbka where bjedte >= '20090201' and bjedte < '20090301');
commit;
--export to '/home/maps/afa/data/rccps/db2export/rcc_wtrbka_20090101_20090201.del' of del select * from rcc_wtrbka where bjedte >= '20090101' and bjedte < '20090201';
--delete from rcc_wtrbka where bjedte >= '20090101' and bjedte < '20090201';

--insert into rcc_spbsta_his (select * from rcc_spbsta where bjedte >= '20090101' and bjedte < '20090201');
--commit;
--export to '/home/maps/afa/data/rccps/db2export/rcc_spbsta_20090101_20090201.del' of del select * from rcc_spbsta where bjedte >= '20090101' and bjedte < '20090201';
--delete from rcc_spbsta where bjedte >= '20090101' and bjedte < '20090201';

--insert into rcc_sstlog_his (select * from rcc_sstlog where bjedte >= '20090101' and bjedte < '20090201');
--commit;
--export to '/home/maps/afa/data/rccps/db2export/rcc_sstlog_20090101_20090201.del' of del select * from rcc_sstlog where bjedte >= '20090101' and bjedte < '20090201';
--delete from rcc_sstlog where bjedte >= '20090101' and bjedte < '20090201';

