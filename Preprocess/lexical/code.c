#include <stdio.h>
#include <string.h>
void vul(int x)
{
	int n = ntohl(x);
	char chunk1[20] = malloc(20);
	memcpy(chunk1,"a",n);
    if(true)
    {
        char chunk2[20] = malloc(20);
        memcpy(chunk2,"b",n);
    }
    else if (1)
    {
        print("c");
        print("c");
    }
    else
    {
        print("d");
        print("d");
    }
}
int main()
{
	int x = 40;
	vul(x);
    for(int i =1;i<=x;i++)
    {
        printf("%c",chunk1[i]);
        printf("%c",chunk1[i]);
    }
    while(1)
    {
        printf("%c",chunk2[i]);
    } 
}