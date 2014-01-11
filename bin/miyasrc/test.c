/* test.c */
#include <stdio.h>
#include "sunyard.h"

/*
	功能:从ini文件中读取主题
	Key:传入的关键字
	KeyValue:传出的值
*/
int GetKeyvalueFile(char *filename,char* Key,char *KeyValue)
{
	FILE *SysSet;
	char SysPara[50][50][50];
	int lines,segm,offset;
	int flagname;
	int i,ch;
	SysSet=fopen(filename,"r");
	if(SysSet==NULL)
		return -1;
	lines=0;
	segm=0;
	offset=0;
     	for   ( ; ; )
     	{
           	ch = fgetc(SysSet);
           	if   ( ch == EOF )
		{
                     	SysPara[lines][segm][offset]   = '\0';
                	break;
		}
           	else
               	if ( ch == '=' )     /* 以 = 分隔 */
                {
                     SysPara[lines][segm++][offset]   = '\0';
                     offset = 0;
                }
                else
                     if  (  ch == '\r' || ch == '\n' )  /* 换行 */
                     {
                            SysPara[lines++][segm][offset]   = '\0';
			    offset=0;
                            segm = 0 ;
                     }
                     else
                            SysPara[lines][segm][offset++] = ch ;
	}
	fclose(SysSet);
	flagname=1;
	for(i=0;i<=lines;i++)
	{
		if(strcmp(SysPara[i][0],Key)==0)
		{
			strcpy(KeyValue,SysPara[i][1]);
			flagname=0;
		}
	}
	if(flagname)
	{
		KeyValue[0]=0;
		return -1;
	}
	return 0;
}


main(int argc,char **argv)
{
	char IP[100];
	char sz_ywtype[100];
	char Sender[30];
	char Receiver[30];
	char SerialNo[30];
	char Date[30];
	char CipherValue[30];
	char Amount[30];
	char OtherInfo[100];
	char temp[100];
	int  TransactType;
	char YwType=0x01;
	int  ret,i,flag;
	int  LoopNum=1,TimeOut=3;

	if(argc>=2)
		TransactType=atoi(argv[1]);                 /*处理类型--0：编押 1：核押*/
    else
        TransactType=0;                             /*默认：1-现金汇票 2-转帐汇票 3-电子汇兑业务*/

	if(argc>=3)
		strcpy(CipherValue,argv[2]);                /*密押:编押时-出口值为计算出的密押, 核押时-入口值为需核验的密押*/
	else
		strcpy(CipherValue,"0000000000");           
		
	if(argc>=4)
	{
		strcpy(CipherValue,argv[2]);                /*密押:编押时-出口值为计算出的密押, 核押时-入口值为需核验的密押*/
		strcpy(IP,argv[3]);                         /*IP地址*/
	}
	else
		strcpy(IP,"10.23.0.200");                   /*默认：10.23.0.200*/
		
		
	if(argc>=5)
		LoopNum=atoi(argv[4]);                      /*循环次数*/
	else
		LoopNum=1;                                  /*默认：1次*/
		
		
	if(argc>=6)
		TimeOut=atoi(argv[5]);                      /*超时*/
	else
		TimeOut=3;                                  /*默认：3次*/

/*
	strcpy(Date,        "19990101");
	strcpy(SerialNo,    "10000000");
	strcpy(Amount,      "000000000000100");
	strcpy(Sender,      "100000000001");
	strcpy(Receiver,    "100000000001");
*/

    /*读取测试配置文件*/
	ret=GetKeyvalueFile("./test.ini","YwType",sz_ywtype);
	if(ret!=0)
	{
		printf("GetKeyValueFile Error YwType!\n");
		return -1;
	}
	printf("YwType=%s\n",sz_ywtype); 
	
	YwType=sz_ywtype[0]-'0';
	printf("c=%02X\n",(unsigned char)YwType);


	ret=GetKeyvalueFile("./test.ini","Date",Date);
	if(ret!=0)
	{
		printf("GetKeyValueFile Error Date!\n");
		return -1;
	}
	printf("Date=%s\n",Date); 

	ret=GetKeyvalueFile("./test.ini","SerialNo",SerialNo);
	if(ret!=0)
	{
		printf("GetKeyValueFile Error SerialNo!\n");
		return -1;
	}
	printf("SerialNo=%s\n",SerialNo);

	ret=GetKeyvalueFile("./test.ini","Amount",Amount);
	if(ret!=0)
	{
		printf("GetKeyValueFile Error Amount!\n");
		return -1;
	}
	printf("Amount=%s\n",Amount); 

	ret=GetKeyvalueFile("./test.ini","Sender",Sender);
	if(ret!=0)
	{
		printf("GetKeyValueFile Error Sender!\n");
		return -1;
	}
	printf("Sender=%s\n",Sender); 

	ret=GetKeyvalueFile("./test.ini","Receiver",Receiver);
	if(ret!=0)
	{
		printf("GetKeyValueFile Error Receiver!\n");
		return -1;
	}
	printf("Receiver=%s\n",Receiver); 

	memset(OtherInfo,0x00,60);
    ret=GetKeyvalueFile("./test.ini","OtherInfo",temp);
	if(ret!=0)
	{
		printf("GetKeyValueFile OtherInfo NULL!\n");
		memset(OtherInfo,0x00,60);
	}

	if(YwType>=4)
	{
		OtherInfo[0]=((temp[0]&0x0F)<<4)+(temp[1]&0x0F);
		OtherInfo[1]=((temp[2]&0x0F)<<4)+(temp[3]&0x0F);
		OtherInfo[2]=((temp[4]&0x0F)<<4)+(temp[5]&0x0F);
		OtherInfo[3]=((temp[6]&0x0F)<<4)+(temp[7]&0x0F);
	}

	ret=SetParamAll(IP,IP,TimeOut);
	flag=0;
	while(flag<LoopNum)
	{
		flag++;

		ret=DraftEncrypt(TransactType,YwType,Date,SerialNo,Amount,Sender,Receiver,OtherInfo,CipherValue);
		if(ret!=0)
		{
			printf("NO.%d Calculate Mac Error!(ret=%d)\n",flag,ret);
		}
		else
			printf("NO.%d CipherValue=%s\n",flag,CipherValue);
	}
}
