// Optionally listen for 2 seconds, if we hear UDP data then just continue as normal.  If no UDP data then try and start framebuffer UDP code
// on empeg player
// empeg player must have hiijack kernel, also must have an entry "ktelnetd_port=23" in file /empeg/var/config.ini on the player to enable telnet
// empeg need executable /broadcastfb_proc in its root filesystem
//
void kick_empeg(char *ipaddress, int olist)
{
        int packets_received;
        unsigned char dummy[2048];
        char line[2048];
        char originating_ip[32];
        char cmdline[2048];
        int i;
	int eagaincount;
	int perrors;

	if (olist==TRUE)
	{
        	packets_received=0;
        	for (i=0;i<200;i++)
        	{
                	if (udp_receive(dummy,sizeof(dummy),originating_ip,FALSE,FALSE,&eagaincount,&perrors)==TRUE)
                        	packets_received++;
                	usleep(1000);
        	}
        	if (packets_received != 0)
                	return;    				                      		// Got some data, no action needed
	}

        printf("Kicked empeg player at %s\n",ipaddress); fflush(stdout);
        sprintf(cmdline,"sh -c \"(sleep 1;echo '/broadcastfb_proc &' ;sleep 1) |telnet %s \" & ",ipaddress);
        system(cmdline);
}




// Font rendering code
// Note: mplayer seems to be used 32 bits per pixel even against 24 bit displays ? Stepping is 4 bytes not 3
#include "font_6x11.h"
#define CHAR_HEIGHT  11
#define CHAR_WIDTH   6
#define CHAR_START   4
#include <time.h>
void add_text(char *TEXT,char *byteperpixel_led_buffer, int width, int height, int offset_down,int offset_across, int color)
{
    time_t      t;
    struct tm  *tm;
    char        line[1024];
    char        *ptr;
    int         i,x,y,f,len;


    // from the top

    strcpy(line,TEXT);
    len=strlen(line);

    ptr = byteperpixel_led_buffer;

    int blanklines=(offset_down * width);
    //Origin must be absolute bottom left so the text is written over when image is scaled and relabeled
    for (y = 0; y < CHAR_HEIGHT; y++)
    {
        ptr = byteperpixel_led_buffer + blanklines + (width * y) + offset_across;
        for (x = 0; x < len; x++)
        {
            f = fontdata[line[x] * CHAR_HEIGHT + y];
            for (i = CHAR_WIDTH; i >= 0; i--)
            {
                if (f & (CHAR_START << i))
            		ptr[0] = color;  	              				// Pixel on
                ptr++;
            }
            ptr--;									// Adjust char spacing
        }
    }
}





// Convert a framebuffer of empeg format (32 lines of 2 bytes per pixel)  into led panel data (32 lines of 1 byte per pixel)
convert_empegfb_to_leds(unsigned char *empegpixels, unsigned char *ledpixels)
{
        int a,b;
        unsigned char empegdualpixel;

        b=0;
        for (a=0;a<2048;a++)
        {
                empegdualpixel=*(empegpixels+a);       					// got 2 pixels
                ledpixels[b]= (empegdualpixel & 0x3);					// 00000011 in binary, mask off just the leas sig 2 bits

		// Translate two bits to pixel into 1 byte per pixel.
                switch (ledpixels[b])							// Are the two bits ....
                {
                        case 0:   { ledpixels[b]=0; break; }				// 00  = off
                        case 1:   { ledpixels[b]=0; break; }				// 01  = off
                        case 2:   { ledpixels[b]=0; break; }				// 10  = off
                        case 3:   { ledpixels[b]=1; break; }				// 11  = on
                }
                b++;

                ledpixels[b]= (empegdualpixel & 0x30) >>4;                              // mask value with 00110000 and shift right 4 to give 000000XX
                switch (ledpixels[b])
                {
                        case 0:   { ledpixels[b]=0; break; }
                        case 1:   { ledpixels[b]=0; break; }
                        case 2:   { ledpixels[b]=0; break; }
                        case 3:   { ledpixels[b]=1; break; }
                }
                b++;
        }
}




// Convert a framebuffer of empeg format (32 lines of 2 bytes per pixel)  into led panel data (32 lines of 1 byte per pixel)
convert_empegfb_to_leds_threshhold(int t, unsigned char *empegpixels, unsigned char *ledpixels)
{
        int a,b;
        unsigned char empegdualpixel;

        b=0;
        for (a=0;a<2048;a++)
        {
                empegdualpixel=*(empegpixels+a);       					// got 2 pixels
                ledpixels[b]= (empegdualpixel & 0x3);					// 00000011 in binary, mask off just the least sig 2 bits

		// Translate two bits to pixel into 1 byte per pixel.
                if (ledpixels[b] < t)							// values below t are off
                        ledpixels[b]=0;
		else	ledpixels[b]=1;
                b++;

                ledpixels[b]= (empegdualpixel & 0x30) >>4;                              // mask value with 00110000 and shift right 4 to give 000000XX
                if (ledpixels[b] < t)
                        ledpixels[b]=0;
		else	ledpixels[b]=1;
                b++;
        }
}





//*********************************************************************************************************************************
// This function would normally only be used by something generating pixel data for the sign
// Convert a one byte per pixel image into a 2 bytes per pixel image (empeg frame buffer format)
// Source = one byte per pixel  -  destination = two pixels per byte
void convert_leds_to_empegfb(unsigned char *ledpixels, unsigned char *empegpixels)
{
        int a;
        int epixelidx;
        int twopixelbyte;                                                               // Two pixels in one byte  00110011

        epixelidx=0;
        for (a=0;a<(128*32);a=a+2)                                                      // For every other pixel in ledpixels buffer (one byte per pixel)
        {
                twopixelbyte=ledpixels[a];                                              // force to 000000NN
                twopixelbyte=twopixelbyte+(ledpixels[a+1]<<4); 				// add      00NN0000   to give  00NN00NN byte
                empegpixels[epixelidx]=twopixelbyte;                                    // Copy value to destination buffer
                epixelidx++;
        }
}




// Display the contents of a one byte per pixel image as ASCII art
// hard coded 128x32 at the moment
display_ascii_image(unsigned char *ptr)
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
                        if (color!=0)
                                printf("1");
                        else    printf(" ");
                        offset++;
                }
                printf("\n");
        }
        fflush(stdout);
        printf("\n");
}





#include <time.h>
int get_clockseconds()
{
        time_t  t;
        struct tm   *tm;

        time(&t);
        tm=localtime(&t);
        return(tm->tm_sec);
}



// This makes a huge difference on 3.x kernel and works reasonably well on 2.6 kernel
#include <sched.h>
void set_realtime(void)
{
  	struct sched_param sparam;
  	sparam.sched_priority = sched_get_priority_max(SCHED_RR);
  	sched_setscheduler(0, SCHED_FIFO, &sparam);
}




// Returns true if a file exists
int file_exists(char *fname)
{
        FILE *fp;

        if ((fp=fopen(fname,"r+"))==NULL)
                return(FALSE);

        fclose(fp);
        return(TRUE);
}


// ***************************************************************************************************************************
// Parse command line arguments
int parse_commandlineargs(int argc,char **argv,char *findthis)
{
        int i,x,n;
        char st[512],tm[512];

        if (argc==1)
                return(FALSE);                                                          // If no command line args then dont bother

        for (i=1;i<argc;i++)                                                            // For every command line argument
        {
                if (strcmp(findthis,argv[i])==0)                                        // If this is the string we are looking for
                {
                        //printf("found %s\n",findthis);
                        n=0;
                        tm[0]='\0';
                        if (argc-1>i)                                                   // If the next argument exists then thats the bit we need to
                        {                                                               // return to the caller.
                                strcpy(tm,argv[i+1]);
                                //printf("args=%s\n",tm);
                        }

                        if (strlen(tm)>0)                                               // If have another agument after our string
                                strcpy(findthis,tm);                                    // Then copy it over the callers "findthis" string
                        else    findthis[0]='\0';                                       // or ensure its blank

                        return(TRUE);
                }
        }
        return(FALSE);
}


// ***************************************************************************************************************************
// Which command line argument does this string occur in
// Returns -1 if not found or the argument number if the string is found
int parse_findargument(int argc,char **argv,char *findthis)
{
        int i,x,n;
        char st[512],tm[512];

        if (argc==0)
                return(-1);   								// If no command line args then dont bother

        for (i=0;i<argc;i++)                                                            // For every command line argument
        {
                if (strcmp(findthis,argv[i])==0)                                        // If this is the string we are looking for
                {
                        //printf("found %s\n",findthis);
                        n=0;
                        tm[0]='\0';
                        if (argc-1>i)                                                   // If the next argument exists then thats the bit we need to
                        {                                                               // return to the caller.
                                strcpy(tm,argv[i+1]);
                                //printf("args=%s\n",tm);
                        }

                        if (strlen(tm)>0)                                               // If have another agument after our string
                                strcpy(findthis,tm);                                    // Then copy it over the callers "findthis" string
                        else    findthis[0]='\0';                                       // or ensure its blank

                        return(i);
                }
        }
        return(-1);
}


