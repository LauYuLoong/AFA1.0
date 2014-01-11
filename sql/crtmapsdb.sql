Create db maps using codeset GBK TERRITORY CN catalog tablespace managed by system using ('/home/maps/db2maps/syscat') TEMPORARY TABLESPACE MANAGED BY system Using ('/home/maps/db2maps/systmp');
connect to maps user maps using maps;
CREATE BUFFERPOOL BUF_DATA_4K IMMEDIATE SIZE 51200 PAGESIZE 4K;
CREATE  REGULAR  TABLESPACE maps_data PAGESIZE 4K MANAGED BY DATABASE USING (FILE '/home/maps/db2maps/data4k/data4k' 262144 ) EXTENTSIZE 32 PREFETCHSIZE 32 BUFFERPOOL BUF_DATA_4K;
CREATE  REGULAR  TABLESPACE maps_idx  PAGESIZE 4K MANAGED BY DATABASE USING (FILE '/home/maps/db2maps/idx4k/idx4k' 262144 )  EXTENTSIZE 32 PREFETCHSIZE 32 BUFFERPOOL BUF_DATA_4K;
