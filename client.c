#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <netdb.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <arpa/inet.h>
 
int main(void)
{
  int sockfd = 0,n = 0;
  char recvBuff[1024];
  struct sockaddr_in serv_addr;

  struct hostent *hen; //from the example file
  char buffer[1024]; //from the example file
 
  memset(recvBuff, '0' ,sizeof(recvBuff));
  if((sockfd = socket(AF_INET, SOCK_STREAM, 0))< 0)
    {
      printf("\n Error : Could not create socket \n");
      return 1;
    }

  hen = gethostbyname("sam.cs164"); //takes in my ip address (of client)
    
  serv_addr.sin_family = AF_INET;
  serv_addr.sin_port = htons(5000);

  

  bcopy((char *)hen->h_addr, (char *)&serv_addr.sin_addr.s_addr, hen->h_length); //this is for accepting client ip
  
  if(connect(sockfd, (struct sockaddr *)&serv_addr, sizeof(serv_addr))<0)
    {
      printf("\n Error : Connect Failed \n");
      return 1;
    }
 
  while(1) {
      fgets(buffer, 1024, stdin); //this will take in the user input
      n = write(sockfd, buffer, strlen(buffer)); //this will send the input to the server
  
  while((n = read(sockfd, recvBuff, sizeof(recvBuff)-1)) > 0)
    {
      recvBuff[n] = 0;
      if(fputs(recvBuff, stdout) == EOF)
    {
      printf("\n Error : Fputs error");
    }
      printf("\n");
    }
 
  if( n < 0)
    {
      printf("\n Read Error \n");
    }
 
  }
  return 0;
}