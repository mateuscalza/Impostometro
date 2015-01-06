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
    unsigned char buffer[4097];

    while (1) 
    {
        fp1 = fopen("arquivofinal.txt","r");

        for(i=0; i<4097; i++)
            fscanf(fp1,"%d,", &buffer[i]);

        fclose(fp1);
//        printf("%d",buffer[0]);
//        printf("%d",buffer[1]);
//        printf("%d",buffer[2]);
//        printf("%d\n",buffer[7]);

//        display_ascii_image(image_data);
        display_ascii_image(buffer);
     }

return 0;

}
