#include <stdlib.h>
#include <windows.h>
#include <stdio.h>
#include <conio.h>
#include <iostream>




int main(int argc, char *argv[])
{
   int n=0;
   DCB dcb={0};
   HANDLE hCom;
   BOOL fSuccess;
   char *comPortNumber[1];
   std::cout << "Name of COM port number: ";
   std::cin >> comPortNumber[1];
   std::cout << "here" << std::endl;
   char pcCommPort[256];
   snprintf(pcCommPort, sizeof(pcCommPort), "%s%s", "COM", comPortNumber);
   //~ char *pcCommPort = "COM2";
   char szBuff[40]={0};
   char otherBuff[40]={"300<CR>"};
   DWORD dwBytesRead=0;
   DWORD dwBytesWrite=0;
/***************************************CommTimeouts******************************************/
COMMTIMEOUTS timeouts={0};
timeouts.ReadIntervalTimeout=50;
timeouts.ReadTotalTimeoutConstant=50;
timeouts.ReadTotalTimeoutMultiplier=10;
timeouts.WriteTotalTimeoutConstant=50;
timeouts.WriteTotalTimeoutMultiplier=10;




/*******************************************Handle*******************************************/
   hCom = CreateFile( pcCommPort,
                    GENERIC_READ | GENERIC_WRITE,
                    FILE_SHARE_READ,    // must be opened with exclusive-access
                    NULL, // no security attributes
                    OPEN_EXISTING, // must use OPEN_EXISTING
                    FILE_ATTRIBUTE_NORMAL,    // not overlapped I/O
                    NULL  // hTemplate must be NULL for comm devices
                    );

/***************************************SET*UP*COM*PORT**************************************/
   if (hCom == INVALID_HANDLE_VALUE)
   {
       printf ("CreateFile failed with error %d.\n", GetLastError());
       return (1);
   }

   if(!SetCommTimeouts(hCom, &timeouts))
    {
        /*Well, then an error occurred*/
   }

   fSuccess = GetCommState(hCom, &dcb);

   if (!fSuccess)
   {
     /*More Error Handling*/
      printf ("GetCommState failed with error %d.\n", GetLastError());
      return (2);
   }


   dcb.BaudRate = 9600;     // set the baud rate
   dcb.ByteSize = 7;             // data size, xmit, and rcv
   dcb.Parity = EVENPARITY;        // no parity bit
   dcb.StopBits = ONESTOPBIT;    // one stop bit
   fSuccess = SetCommState(hCom, &dcb);

   if (!fSuccess)
   {
      printf ("SetCommState failed. Error: %d.\n", GetLastError());
      return (3);
   }

   printf ("Serial port %s successfully configured.\n", pcCommPort);
 //  return (0);

/*************************************Reading************************************************/

if(ReadFile(hCom, szBuff, 39, &dwBytesRead, NULL)){
   int j=0;
   for(j = 0; j < dwBytesRead; j++){
     printf("%c", szBuff[j]);
   }
   puts("\n"); // Print a new line after printing all the string.
}

if(WriteFile(hCom, otherBuff, 39, &dwBytesWrite, NULL)){
int i=0;
for(i=0;i<sizeof(otherBuff);i++){
    printf("%c", otherBuff[i]);
}
//printf("The size of dwBytesWrite is: %c", &otherBuff);
//printf("I wrote to the device\n");
//printf("I");
}
//printf("Heres szBuff %d\n", szBuff);

/********************************************************************************************/
CloseHandle(hCom);
return(0);

}

