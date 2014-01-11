#include <stdio.h>
#include <signal.h>
#include <string.h>
#include <time.h>
#include <sys/socket.h>
#include <netdb.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <fcntl.h>
#include "sunyard.h"

char ServerName1[100];	/*��Ѻ��������ַ1*/
char ServerName2[100];	/*��Ѻ��������ַ2*/
int  sock_check=-1;
int  m_TimeOut=10;
int  m_MyLoopNum=0;
int  m_MyLoopFlag=0;

/*****************************************************************************
DraftEncrypt:���Ѻ����
����˵����
			TransactType�� 	  ��������--0����Ѻ 1����Ѻ
			YwType��	  ҵ������(0x01,0x02,0x03)
					  (0x01=�ֽ��Ʊ,0x02=��תת�ʻ�Ʊ,0x03=����תת�ʻ�Ʊ)
			Date��		  ǩƱ����(���磺"19990101")
			SerialNo��	  ��Ʊ����("12345678")
			Amount��	  ��� (��λΪ��,����С����,����15λǰ��'0')
			SendNode��	  ǩ������ţ�(���磺"000000123456") ����12λǰ��'0'
			RecvNode��	  �Ҹ�����ţ�������ȫ��'0'
			OtherInfo��	  ������Ϣ����������60���ֽڵ�0x00
			CipherValue��	  ��Ѻ
						  ��Ѻʱ������ֵΪ���������Ѻ
						  ��Ѻʱ�����ֵΪ��������Ѻ

��������ֵ��
		0�� ��ʾ������������Ѻʱ��Ѻ��CipherValue�ֶη��أ���Ѻ��ʾ��Ѻ������ȷ .
		>0����Ѻϵͳ��������Ҫ�ػ���Ѻ�к��зǷ�ֵ��������Ѻ����ͨѶ����� .
		������룺
			9001	��������
			9002	���ʹ���
			9003	���մ���
			9004	��Ѻ����
			9005	��Ѻ����
			9006	�˶�ǩ������
			9007	�����б�ʶ����
			9008	�ձ��б�ʶ����
			9009	���ܿ������쳣
			9010	���ݱ��Ĵ���
			9011	����ͨ�ų�ʱ
			9012	�������ޱ�ѺȨ��

*/


int DraftEncrypt(int TransactType,char YwType,char* Date,char* SerialNo,char* Amount,char* SendNode,char* RecvNode,char* OtherInfo,char* CipherValue)
{
	int ret_code ;

	ret_code = CipherTransact(TransactType, YwType, Date, SerialNo, Amount, SendNode, RecvNode, OtherInfo, CipherValue);
	if((ret_code == ERR_CONNECT) || (ret_code == ERR_SEND) || 
        (ret_code == ERR_RECV) || (ret_code == ERR_TIMEOUT) || 
        (ret_code == ERR_EXCEPTION))
	{
		CloseConnect_MY();
		/*�����һ����Ѻ������ͨѶ�������Զ��õڶ�����Ѻ��������IP��ַ*/
		ret_code = CipherTransact(TransactType, YwType, Date, SerialNo, Amount, SendNode, RecvNode, OtherInfo, CipherValue);
		return ret_code;
	}
	else
	{
		return ret_code;
	}

	return ret_code;
}


void TcpOutTime(int signo)
{

}

void GetAscii(unsigned char *s,unsigned char *k,int len)
{
	char Temp[4];
	int i;
	for(i=0;i<=len;i+=2){
		sprintf(Temp,"%02X",k[i/2]);
		memcpy(s+i,Temp,2);
	}
	s[len]='\0';
}

void GetHex(unsigned char *s,unsigned char *k,int len)
{
	char Temp[4];
	int i;
	for(i=0;i<=len;i+=2){
		s[i/2]=0;
		memcpy(Temp,k+i,2);
		if((Temp[0]>='0') && (Temp[0]<='9')) s[i/2]=(Temp[0]-'0')*16;
		if((Temp[0]>='a') && (Temp[0]<='f')) s[i/2]=(Temp[0]-'a'+10)*16;
		if((Temp[0]>='A') && (Temp[0]<='F')) s[i/2]=(Temp[0]-'A'+10)*16;
		if((Temp[1]>='0') && (Temp[1]<='9')) s[i/2]+=Temp[1]-'0';
		if((Temp[1]>='a') && (Temp[1]<='f')) s[i/2]+=Temp[1]-'a'+10;
		if((Temp[1]>='A') && (Temp[1]<='F')) s[i/2]+=Temp[1]-'A'+10;
	}
}

void GetCurrentDate(char* TimeMsg)
{
	long t;
	struct tm *pt;

	time(&t);
	pt=localtime(&t);

	sprintf(TimeMsg,"%d-%02d-%02d-%02d-%02d",(pt->tm_year+1900),(pt->tm_mon+1),pt->tm_mday,pt->tm_hour,pt->tm_min);
	TimeMsg[16]='\0';

}

int myrand()
{
	long t;

	time(&t);
	srand(t%rand());
	return(rand());
}

/* Connect myk */
int ConnectToHsm(int* sockid,char *Ip_Address)
{
	int ret;
	struct sockaddr_in client;
	struct hostent* hp;
	void (*func)(int);
	if(Ip_Address==NULL)
		strcpy(Ip_Address,"127.0.0.1");
	*sockid=socket(AF_INET,SOCK_STREAM,0);
	if(*sockid<0)
	{
		return(-2);
	}
	memset(&client, 0, sizeof(client));
	client.sin_family=AF_INET;
	client.sin_addr.s_addr=inet_addr(Ip_Address);
	client.sin_port=htons(8889);
	func=signal(SIGALRM,TcpOutTime);
	alarm(m_TimeOut);
	ret=-3;
	ret=connect(*sockid,(struct sockaddr *)&client,sizeof(client));
	alarm(0);
	signal(SIGALRM,func);
	if(ret<0)
	{
		close(*sockid);
		*sockid=-1;
		return(-4);
	}
	return(0);
}

/* Close socket */
int CloseConnect_MY()
{
	int ret;

	ret=shutdown(sock_check,2);
	ret=close(sock_check);
	sock_check=-1;
	if(m_MyLoopFlag==0)
		m_MyLoopFlag=1;
	else
		m_MyLoopFlag=0;
}

/* SetParam*/
int SetParam(char *My_IPAdress,int TimeOut)
{
	int ret;

	ret=strlen(My_IPAdress);
	if(ret>99)
		return -1;
	strcpy(ServerName1,My_IPAdress);
	strcpy(ServerName2,My_IPAdress);
	if(TimeOut<2)
		m_TimeOut=2;
	else if(TimeOut>120)
		m_TimeOut=120;
	else
		m_TimeOut=TimeOut;
	return 0;
}

int SetParamAll(char *My_IPAdress1,char *My_IPAdress2,int TimeOut)
{
	int ret;

	ret=strlen(My_IPAdress1);
	if(ret>99)
		return -1;
	strcpy(ServerName1,My_IPAdress1);

	ret=strlen(My_IPAdress2);
	if(ret>99)
		return -2;
	strcpy(ServerName2,My_IPAdress2);

	if(TimeOut<2)
		m_TimeOut=2;
	else if(TimeOut>120)
		m_TimeOut=120;
	else
		m_TimeOut=TimeOut;
	return 0;
}

/* CipherTransact */
int CipherTransact(int TransactType,char YwType,char* Date,char* SerialNo,char* Amount,char* SendNode,char* RecvNode,char* OtherInfo,char* CipherValue)
{
	unsigned char Send_Data[2000],Recv_Data[2000];
	char temp[100];
	unsigned char my_hex[16];
	int ret,Len_No,Len_Send,Len_Recv;
	int i;
	unsigned int my_value;
/*Package*/
	memset(Send_Data,0x00,180);
	memcpy(Send_Data,"SYD",3);
	Send_Data[3]=1;
	Send_Data[4]=m_MyLoopNum/256;
	Send_Data[5]=m_MyLoopNum%256;
	m_MyLoopNum=(m_MyLoopNum+1)%65536;
	Send_Data[6]=0;
	Send_Data[7]=124+32+5;

	if(TransactType==0)
		memcpy(Send_Data+8+32,"16000",5);
	else if(TransactType==1)
		memcpy(Send_Data+8+32,"16001",5);
	else
		memcpy(Send_Data+8+32,"16002",5);
	memcpy(Send_Data+8+32+5,&YwType,1);
	memcpy(Send_Data+8+32+6,Date,8);
	memcpy(Send_Data+8+32+14,SerialNo,8);
	memcpy(Send_Data+8+32+22,Amount,15);
	Len_No=strlen(SendNode);
	if(Len_No>12)
		Len_No=12;
	memcpy(Send_Data+8+32+37+(12-Len_No),SendNode,Len_No);
	Len_No=strlen(RecvNode);
	if(Len_No>12)
		Len_No=12;
	memcpy(Send_Data+8+32+49+(12-Len_No),RecvNode,Len_No);
	memcpy(Send_Data+8+32+61,OtherInfo,60);
	if((TransactType==1)||(TransactType==2))
	{
		memcpy(temp,CipherValue,10);
		temp[10]='\0';
#ifdef DEBUG
		printf("CipherValue:%s\n",temp);
#endif
		sscanf(temp,"%010u",&my_value);
		my_hex[0]=(my_value>>24)&0xff;
		my_hex[1]=(my_value>>16)&0xff;
		my_hex[2]=(my_value>>8)&0xff;
		my_hex[3]=(my_value)&0xff;
		GetAscii((unsigned char *)temp,(unsigned char *)my_hex,8);
		memcpy(Send_Data+8+32+121,temp,8);
#ifdef DEBUG
		printf("HEX:%02X %02X %02X %02X\n",my_hex[0],my_hex[1],my_hex[2],my_hex[3]);
		temp[8]='\0';
		printf("ASCII:%s\n",temp);
#endif
	}
	Len_Send=8+32+5+124;


	if(sock_check==-1)
	{
		if(m_MyLoopFlag==0)
		{
			ret=ConnectToHsm(&sock_check,ServerName1);
#ifdef DEBUG
			printf("ConnectToHsm1(ret=%d,IP=%s)\n",ret,ServerName1);
#endif
			if(ret!=0)
			{
				ret=ConnectToHsm(&sock_check,ServerName2);
#ifdef DEBUG
				printf("ConnectToHsm2(ret=%d,IP=%s)\n",ret,ServerName2);
#endif
			}
		}
		else
		{
			ret=ConnectToHsm(&sock_check,ServerName2);
#ifdef DEBUG
			printf("ConnectToHsm3(ret=%d,IP=%s)\n",ret,ServerName2);
#endif
			if(ret!=0)
			{
				ret=ConnectToHsm(&sock_check,ServerName1);
#ifdef DEBUG
				printf("ConnectToHsm4(ret=%d,IP=%s)\n",ret,ServerName1);
#endif
			}
		}
#ifdef DEBUG
		printf("ConnectToHsm5(ret=%d,flag=%d,sock=%d)\n",ret,m_MyLoopFlag,sock_check);
#endif
		if(ret!=0)
			return(ERR_CONNECT);
		if(sock_check==-1)
			return(ERR_CONNECT);
	}

/*Send To Hsm*/
#ifdef SOCKET_PACKET_180
	Len_Send=180;
#endif

#ifdef DEBUG
	printf("Send %d Bytes Data:\n",Len_Send);
	for(i=0;i<Len_Send;i++)
	{
		if((i % 25 ==0) && (i != 0)) printf("\n");
		printf("%02X ",*(Send_Data+i));
	}
	printf("\n");
#endif
	ret=-1;
	signal(SIGALRM,TcpOutTime);
	alarm(m_TimeOut);
	ret=send(sock_check,Send_Data,Len_Send,0);
#ifdef DEBUG
	printf("Send %d Bytes Data:\n",ret);
#endif
	if(ret!=Len_Send)
	{
		CloseConnect_MY();
		return(ERR_SEND);
	}
	alarm(0);
	if(ret<0)
	{
		CloseConnect_MY();
		return(ERR_TIMEOUT);
	}
/*Receiver From Hsm*/
	memset(Recv_Data,0x00,180);
	ret=-1;
	signal(SIGALRM,TcpOutTime);
	alarm(m_TimeOut);
#ifdef SOCKET_PACKET_180
	Len_Recv=180;
	ret=recv(sock_check,Recv_Data,Len_Recv,0);
#else
	ret=recv(sock_check,Recv_Data,5,0);
	if(ret!=5)
	{
		CloseConnect_MY();
		return(ERR_RECV);
	}
	Len_Recv=*(Recv_Data+3)*256 + *(Recv_Data+4);
	if(Len_Recv>180) Len_Recv=180;
	ret=recv(sock_check,Recv_Data+5,Len_Recv,0);
	Len_Recv=+5;
	printf("Received %d Bytes Data\n",ret);
#endif

	if(ret!=Len_Recv)
	{
		CloseConnect_MY();
		return(ERR_RECV);
	}
	alarm(0);
	if(ret<0)
	{
		CloseConnect_MY();
		return(ERR_TIMEOUT);
	}

#ifdef DEBUG
	printf("Received %d Bytes Data:\n",Len_Recv);
	for(i=0;i<Len_Recv;i++)
	{
		if((i % 25 ==0) && (i != 0)) printf("\n");
		printf("%02X ",*(Recv_Data+i));
	}
	printf("\n");
	printf("Retcode=%02X %02X %02X %02X\n",*(Recv_Data+5+37),*(Recv_Data+5+37+1),*(Recv_Data+5+37+2),*(Recv_Data+5+37+3));
#endif


	if(memcmp(Recv_Data+5+37,"\x30\x30\x30\x30",4)!=0)
	{
		if(memcmp(Recv_Data+5+37,"\x30\x33\x30\x32",4)==0)
			return (ERR_SENDER);
		else if(memcmp(Recv_Data+5+37,"\x30\x33\x30\x33",4)==0)
			return (ERR_RECEIVER);
		else if(memcmp(Recv_Data+5+37,"\x30\x33\x30\x39",4)==0)
			return (ERR_EXCEPTION);
		else if(memcmp(Recv_Data+5+37,"\x30\x33\x30\x34",4)==0)
			return (ERR_DATA);
		else if(memcmp(Recv_Data+5+37,"\x30\x33\x30\x31",4)==0)
			return(ERR_CHECK);
		else if(memcmp(Recv_Data+5+37,"\x30\x33\x30\x35",4)==0)
			return(ERR_PURVIEW);
		else
			return (ERR_DATA);
	}
	if((TransactType==0)||(TransactType==1))
	{
		memcpy(temp,Recv_Data+37+5+4,8);
		temp[8]='\0';
		GetHex((unsigned char *)my_hex,(unsigned char *)temp,8);
#ifdef DEBUG
		printf("ASCII:%s\n",temp);
		printf("HEX:%02X %02X %02X %02X\n",my_hex[0],my_hex[1],my_hex[2],my_hex[3]);
#endif
		my_value=0;
		my_value=my_value*256+my_hex[0];
		my_value=my_value*256+my_hex[1];
		my_value=my_value*256+my_hex[2];
		my_value=my_value*256+my_hex[3];
		sprintf(temp,"%010u",my_value);
		memcpy(CipherValue,temp,10);
#ifdef DEBUG
		printf("CipherValue:%s\n",temp);
#endif
	}
	return 0;
}
