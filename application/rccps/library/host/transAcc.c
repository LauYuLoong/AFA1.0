#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <python.h>

status PyObject *
int accno_crc(const char *acno, int len)
{
   int total=10;
   int i;
   for (i=0; i<len; ++i)
   {
       if (!isdigit(acno[i]))
           return -1;
       total=(total+acno[i]-'0')%10;
       total=(total==0)?10:total;
       total=(total+total)%11;
   }
   return (11-total)%10;
}


int main(int argc, char **argv)
{
   printf("%s : %d\n",argv[1],accno_crc(argv[1],atoi(argv[2])));
   return 0;
}
