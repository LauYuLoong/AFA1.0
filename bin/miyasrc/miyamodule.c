#include <stdio.h>
#include <Python.h>
#include "./sunyard.c"

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

static PyObject *
miya_DraftEncrypt(PyObject * self, PyObject * args)
{
    int  iTransactType;
    char *sYwType;
    char *sDate;
    char *sSerialNo;
    char *sAmount;
    char *sSender;
    char *sReceiver;
    char *sOtherInfo;
    char *sCipherValue;

    char sConfFile[128];
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
	char YwType;
	int  ret,i,flag;
	char sLoopNum[5], sTimeOut[8];
	int  LoopNum=1,TimeOut=3;

    memset(IP,          0x00, sizeof(IP));
    memset(sz_ywtype,   0x00, sizeof(sz_ywtype));
    memset(Sender,      0x00, sizeof(Sender));
    memset(Receiver,    0x00, sizeof(Receiver));
    memset(SerialNo,    0x00, sizeof(SerialNo));
    memset(Date,        0x00, sizeof(Date));
    memset(CipherValue, 0x00, sizeof(CipherValue));
    memset(Amount,      0x00, sizeof(Amount));
    memset(OtherInfo,   0x00, sizeof(OtherInfo));
    memset(temp,        0x00, sizeof(temp));
    memset(sLoopNum,    0x00, sizeof(sLoopNum));
    memset(sTimeOut,    0x00, sizeof(sTimeOut));
    memset(sConfFile,   0x00, sizeof(sConfFile));


    /*配置文件名*/
    sprintf(sConfFile, "%s/conf/miya.conf", getenv("AFAP_HOME"));
    
    /*IP*/
	ret=GetKeyvalueFile(sConfFile, "IP", IP);
	if(ret!=0)
	{
		printf("GetKeyValueFile Error IP!\n");
		return Py_BuildValue("i", -1);
	}
	printf("IP=%s\n",IP); 


    /*LOOPNUM*/
	ret=GetKeyvalueFile(sConfFile, "LOOPNUM", sLoopNum);
	if(ret!=0)
	{
		printf("GetKeyValueFile Error LOOPNUM!\n");
		return Py_BuildValue("i", -1);
	}
    LoopNum = atoi(sLoopNum);
	printf("LoopNum=%d\n", LoopNum); 


    /*TIMEOUT*/
	ret=GetKeyvalueFile(sConfFile, "TIMEOUT", sTimeOut);
	if(ret!=0)
	{
		printf("GetKeyValueFile Error TIMEOUT!\n");
		return Py_BuildValue("i", -1);
	}
    TimeOut = atoi(sTimeOut);
	printf("TimeOut=%d\n", TimeOut);



    if ( !PyArg_ParseTuple(args, "i|s|s|s|s|s|s|s|s", &iTransactType, &sYwType, &sDate, &sSerialNo, &sAmount, &sSender, &sReceiver, &sOtherInfo, &sCipherValue) )
        return NULL;

    if ( strlen(sDate) < 1) {
        return Py_BuildValue("i", -2);
    }

    if ( strlen(sDate) < 8) {
        return Py_BuildValue("i", -3);
    }

    if ( strlen(sAmount) < 15) {
        return Py_BuildValue("i", -4);
    }

    if ( strlen(sSerialNo) < 8) {
        return Py_BuildValue("i", -5);
    }

    if ( strlen(sSender) < 12) {
        return Py_BuildValue("i", -6);
    }

    if ( strlen(sReceiver) < 12) {
        return Py_BuildValue("i", -7);
    }
    
    if ( strlen(sCipherValue) < 10) {
        return Py_BuildValue("i", -8);
    }


    /*处理类型--0：编押 1：核押*/
    TransactType = iTransactType;
    
    /*业务类型(1-现金汇票 2-转帐汇票 3-电子汇兑业务)*/
	YwType=sYwType[0];

    /*日期*/
    strcpy(Date, sDate);

    /*流水号*/
    strcpy(SerialNo, sSerialNo);

    /*金额*/
    strcpy(Amount, sAmount);

    /*发起行行号*/
    strcpy(Sender, sSender);

    /*接收行行号*/
    strcpy(Receiver, sReceiver);

    /*密押:编押时-出口值为计算出的密押, 核押时-入口值为需核验的密押*/
    strcpy(CipherValue, sCipherValue);
    
    /*其它信息(0x00,请注意不要填'0')*/
    memset(OtherInfo,0x00,60);
    strcpy(temp, sOtherInfo);
       
       
	/*赋值*/
	ret=SetParamAll(IP,IP,TimeOut);
	
	flag=0;
	while(flag<LoopNum)
	{
		flag++;

        /*
    	int DraftEncrypt(int TransactType,char YwType,char Date[8],char SerialNo[8],char Amount[15],char SendNode[12],char RecvNode[12],char OtherInfo[60],char CipherValue[10]);
    
    		参数说明：
    			TransactType：  处理类型--0：编押 1：核押
    			YwType：	    业务种类
                                '1' 现金汇票,
                                '2' 转帐汇票,
                                '3' 电子汇兑业务
    			Date：		    票据日期(汇票业务)或委托日期（电子汇兑业务）
                SerialNo：	    汇票号码(汇票业务)或交易流水号（电子汇兑业务）
    			Amount：	    金额 (单位为分,不含小数点) 不足15位前补'0'
    			SendNode：	    发起行行号 (例如："001000000000") 不足12位前补'0'
    			RecvNode：	    接收行行号，若无则全填'0'
    			OtherInfo：	    全填0x00(请注意不要填'0')
    			CipherValue：   密押
    						    编押时，出口值为计算出的密押
    						    核押时，入口值为需核验的密押
        */

        printf("TransactType= [%d]\n",    TransactType);
        printf("YwType      = [%c]\n",    YwType);
        printf("Date        = [%s]\n",    Date);
        printf("SerialNo    = [%s]\n",    SerialNo);
        printf("Amount      = [%s]\n",    Amount);
        printf("Sender      = [%s]\n",    Sender);
        printf("Receiver    = [%s]\n",    Receiver);
        printf("OtherInfo   = [%s]\n",    OtherInfo);
        printf("CipherValue = [%s]\n",    CipherValue);
    
		ret=DraftEncrypt(TransactType,YwType,Date,SerialNo,Amount,Sender,Receiver,OtherInfo,CipherValue);
		if(ret!=0)
		{
			printf("NO.%d Calculate Mac Error!(ret=%d)\n",flag,ret);
			memset(CipherValue, 0x00, sizeof(CipherValue));
			strcpy(CipherValue, "0000000000");
		}
		else
		{
			printf("NO.%d CipherValue=%s\n",flag,CipherValue);
		}
		/* TransactType 0-编押 1-核押 */
		if(TransactType == 0)
                {
		    strcpy(sCipherValue, CipherValue);
		    printf("编押密押=%s\n",sCipherValue);
                }
		else
                {
		    sCipherValue = (char *)CipherValue;
		    printf("核押密押=%s\n",sCipherValue);
                }
	}

    return Py_BuildValue("i", ret);
}


static PyMethodDef
miyaMethods[] =
{
    {"DraftEncrypt", miya_DraftEncrypt, METH_VARARGS, "Execute a miya command."},
    {NULL, NULL, 0, NULL}
};

void initmiya(void)
{
    Py_InitModule("miya", miyaMethods);
}
