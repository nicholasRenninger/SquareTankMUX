#include <stdlib.h>
#include <windows.h>
#include <stdio.h>
#include <conio.h>
#include <iostream>

#define READ_BUFFER_SIZE 100
#define WRITE_BUFFER_SIZE 100


int main(int argc, char *argv[])
{
   
   DCB dcb = {0};
   HANDLE hCom;
   BOOL fSuccess;
   char comPortNumber[1];
   std::cout << "Name of COM port number: ";
   scanf("%s", comPortNumber);
   char pcCommPort[256];
   snprintf(pcCommPort, sizeof(pcCommPort), "%s%s", "COM", comPortNumber);
   //~ char *pcCommPort = "COM2";
   char readBuff[READ_BUFFER_SIZE] = {0};
   char writeBuff[WRITE_BUFFER_SIZE] = {"@254PR1?;FF"};
   DWORD dwBytesRead=0;
   DWORD dwBytesWrite=0;  
   
/***************************************CommTimeouts******************************************/
COMMTIMEOUTS timeouts = {0};
timeouts.ReadIntervalTimeout = 50;
timeouts.ReadTotalTimeoutConstant = 50;
timeouts.ReadTotalTimeoutMultiplier = 10;
timeouts.WriteTotalTimeoutConstant = 50;
timeouts.WriteTotalTimeoutMultiplier = 10;




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
       printf ("CreateFile failed with error %Iu.\n", GetLastError()); // %Iu is for long unsigned int
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
      printf ("GetCommState failed with error %Iu.\n", GetLastError());
      return (2);
   }


   dcb.BaudRate = 9600;     // set the baud rate
   dcb.ByteSize = 8;             // data size, xmit, and rcv
   dcb.Parity = NOPARITY;        // no parity bit
   dcb.StopBits = ONESTOPBIT;    // one stop bit
   fSuccess = SetCommState(hCom, &dcb);

   if (!fSuccess)
   {
      printf ("SetCommState failed. Error: %Iu.\n", GetLastError());
      return (3);
   }

   printf ("Serial port %s successfully configured.\n", pcCommPort);
 //  return (0);

/*************************************Reading************************************************/

if(ReadFile(hCom, readBuff, READ_BUFFER_SIZE, &dwBytesRead, NULL)){
   
   for(unsigned int j = 0; j < sizeof(readBuff); j++){
     printf("%c", readBuff[j]);
   }
   puts("\nRead from the Device\n"); // Print a new line after printing all the string.
} else {

	printf("\nerror reading from device\n");
}


if(WriteFile(hCom, writeBuff, WRITE_BUFFER_SIZE, &dwBytesWrite, NULL)){

for(unsigned int i=0;i<sizeof(writeBuff);i++){
    printf("%c", writeBuff[i]);
}
printf("\nThe size of the Write Buffer is: %d\n", sizeof(writeBuff) - 1);
printf("Wrote to the device\n\n");
}

if(ReadFile(hCom, readBuff, READ_BUFFER_SIZE, &dwBytesRead, NULL)){
 
   for(unsigned int j = 0; j < sizeof(readBuff); j++){
     printf("%c", readBuff[j]);
   }
   puts("\nRead from the Device\n"); // Print a new line after printing all the string.
}


/********************************************************************************************/
CloseHandle(hCom);
return(0);

}

