#include <stdio.h>
//#include "128x32.h"

void display_ascii_image(unsigned char *ptr)

{

        int offset;
        int x,y;
        int color;

        offset=0;

        for (x=0;x<32;x++)
        {
                for (y=0;y<128;y++)
                {
                        color=*(ptr+offset);
                        if (color==1)
                                printf("1");
                        else    printf(" ");
                        offset++;
                }

                printf("\n");
        }

        fflush(stdout);

        printf("\n");
}


int main()
{

    FILE *fp1;

    int i = 0;
    unsigned char buffer[24577];

        fp1 = fopen("arquivo.txt","r");

        for(i=0; i<24577; i++)
            fscanf(fp1,"%d,", &buffer[i]);

        fclose(fp1);
        display_ascii_image(buffer);

return 0;

}
