
#include "p10_board_ledhashtable.h"

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <dirent.h>
#include <fcntl.h>
#include <assert.h>
#include <sys/mman.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <sys/time.h>
#include <sys/resource.h>



//#include "128x32.h"


#define BCM2708_PERI_BASE        0x20000000
#define GPIO_BASE                (BCM2708_PERI_BASE + 0x200000) /* GPIO controller */
#define PAGE_SIZE (4*1024)
#define BLOCK_SIZE (4*1024)

int  mem_fd;
char *gpio_mem, *gpio_map;
char *spi0_mem, *spi0_map;

// I/O access
volatile unsigned *gpio;

// GPIO setup macros. Always use INP_GPIO(x) before using OUT_GPIO(x) or SET_GPIO_ALT(x,y)
#define INP_GPIO(g) *(gpio+((g)/10)) &= ~(7<<(((g)%10)*3))
#define OUT_GPIO(g) *(gpio+((g)/10)) |=  (1<<(((g)%10)*3))
#define SET_GPIO_ALT(g,a) *(gpio+(((g)/10))) |= (((a)<=3?(a)+4:(a)==4?3:2)<<(((g)%10)*3))
#define GPIO_SET *(gpio+7)  // sets   bits which are 1 ignores bits which are 0
#define GPIO_CLR *(gpio+10) // clears bits which are 1 ignores bits which are 0



// Set up a memory regions to access GPIO
void setup_io()
{
   /* open /dev/mem */
   if ((mem_fd = open("/dev/mem", O_RDWR|O_SYNC) ) < 0) 
   {
      printf("can't open /dev/mem \n");
      exit (-1);
   }

   /* mmap GPIO */

   // Allocate MAP block
   if ((gpio_mem = malloc(BLOCK_SIZE + (PAGE_SIZE-1))) == NULL) 
   {
      printf("allocation error \n");
      exit (-1);
   }

   // Make sure pointer is on 4K boundary
   if ((unsigned long)gpio_mem % PAGE_SIZE)
     gpio_mem += PAGE_SIZE - ((unsigned long)gpio_mem % PAGE_SIZE);

   // Now map it
   gpio_map = (unsigned char *)mmap(
      (caddr_t)gpio_mem,
      BLOCK_SIZE,
      PROT_READ|PROT_WRITE,
      MAP_SHARED|MAP_FIXED,
      mem_fd,
      GPIO_BASE
   );

   if ((long)gpio_map < 0) 
   {
      printf("mmap error %d\n", (int)gpio_map);
      exit (-1);
   }

   // Always use volatile pointer!
   gpio = (volatile unsigned *)gpio_map;
} 


set_as_output(int g)
{
    INP_GPIO(g); 
    OUT_GPIO(g);
}


output_high(int g)
{
       GPIO_SET = 1<<g;
}


output_low(int g)
{
       GPIO_CLR = 1<<g;
}



// Signal name to GPIO line mapping
#define CLK	7
#define SCLK	8
#define A	23
#define B	18
#define	OE	24
#define PIXEL	25


// 0 1 2 and 3 =   00 01 10 11 binary
select_row(int row)
{
	output_high(SCLK);				// Idle state for row clock line
	output_high(SCLK);				// Idle state for row clock line
	if (row==0)
	{	
		output_low(A);
		output_low(B);
	}
	if (row==1)
	{
		output_high(A);
		output_low(B);
	}
	if (row==2)
	{        
		output_low(A);
		output_high(B);
	}
	if (row==3)
	{
		output_high(A);
		output_high(B);
	}
	output_low(SCLK);				// Indicate board should take new address for active ROW
	output_low(SCLK);				// Indicate board should take new address for active ROW
	output_low(SCLK);				// Indicate board should take new address for active ROW
	output_high(SCLK);				// Idle state
	output_high(SCLK);				// Idle state
	output_high(SCLK);				// Idle state
}





// Toggles the clock to latch in a pixel, should be called 1024 times for an 8 panel display
latch_pixel()
{
	// Pixel clock - if this is not long enough we get noise on the display
	// unsure a few cycles low follwed by a few of high, try to avoid usleep as timer resolution is poor
	output_low(CLK);				// clock pixel in
	output_low(CLK);
	output_low(CLK);
	output_high(CLK);
	output_high(CLK);
	output_high(CLK);
	output_high(CLK);				// Idle state
	//printf("\n");
}



update_leds()
{
	// Now we have 1024 pixels clocked in update the display
   	output_low(OE);	
   	output_low(OE);	
   	output_low(OE);	
   	output_low(OE);	
   	output_high(OE);
   	output_high(OE);
   	output_high(OE);
   	output_high(OE);
}


 
// Always clock 1024 pixels for the 8 display boards, thats 4 lines active on each row of the two rows of 4 panels
//
// Take a pointer to some memory.  Clock that memory out to the display as pixels
// the memory format is one Byte per pixel, values of 1 are an LED that is on (a pixel)
// 
// Direction 'f' forward, 'b' backwards
//
//clock_pixels(short int *ptr,int numpixels,char direction)
clock_pixels(unsigned char *ptr,int numpixels,char direction)
{
  	int color,i;
	int offset;


	offset=0;
	output_high(CLK);						// Idle state
	output_high(CLK);
  	for (i=0;i<numpixels;i++)					// clock out this many dots
	{
		color=*(ptr+offset);
		if (color==0)
		{
			//printf("0");
			output_high(PIXEL);				// pixel off
		}
		else	
		{
			//printf("1");
			output_low(PIXEL);
		}
		// Pixel clock - if this is not long enough we get noise on the display
		// unsure a few cycles low follwed by a few of high, try to avoid usleep as timer resolution is poor
		output_low(CLK);					// clock pixel in
		output_low(CLK);
		output_low(CLK);
		output_low(CLK);
		output_low(CLK);
		output_low(CLK);
		output_high(CLK);
		output_high(CLK);
		output_high(CLK);					// Idle state
		output_high(CLK);					// Idle state
		output_high(CLK);					// Idle state
		output_high(CLK);					// Idle state

		if (direction=='f')					// forwards increment pointer, otherwise decrement
			offset++;
		else
			offset--;
   	}
	//printf("\n");
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
			//color=*ptr+offset;
			color=*(ptr+offset);
			if (color==1)
				printf("1");
			else	printf(" ");
			offset++;
		}
		printf("\n");
	}
	fflush(stdout);
	printf("\n");
}




int main(int argc, char **argv)
{ 
  int i,x;
  int row=0;

  // compiler plays with alignment, might be N x 32 bit words not packed or summink .. might need to play with types
  //unsigned char *imagebuf = malloc(LEDS_WIDTH*LEDS_HEIGHT);
  // was int *imagebuf = malloc(LEDS_WIDTH*LEDS_HEIGHT);
  //*imagebuf = malloc(LEDS_WIDTH*LEDS_HEIGHT);

  //unsigned char mybuf[4096];
  //unsigned char *imagebuf=mybuf;

  //if (imagebuf==NULL)
  //{
	//printf("malloc failed\n");
	//exit(1);
  //}

  setpriority(PRIO_PROCESS,0,-10);                                                        // Give this process a CPU boost

  // Set up gpi pointer for direct register access
  setup_io();

  // Set these GPIO Lines as outputs
  set_as_output(CLK);									// CLK
  set_as_output(SCLK);									// SCLK = Latch of ROW
  set_as_output(B);									// B
  set_as_output(A);									// A
  set_as_output(OE);									// OE
  set_as_output(PIXEL);									// Pixel data  (R)


  // idle state for all lines
  output_high(SCLK);
  output_high(CLK);
  output_low(A);
  output_low(B);
  output_low(PIXEL);
  output_high(OE);


//  printf("image size = %d, should be 4096 with luck\n",sizeof(buffer));
  fflush(stdout);

  printf("first index line 1 = %d\n",indexes[0][0]);
  printf("first index line 2 = %d\n",indexes[1][0]);
  printf("first index line 3 = %d\n",indexes[2][0]);
  printf("first index line 4 = %d\n",indexes[3][0]);


 int chunk;
 //display_ascii_image(buffer);



 // Adjust values, these values need to be 8 more to the right
 for (row=0;row<=3;row++)								// For each of the 4 sets of lines
 {
       	for (chunk=0;chunk<=63;chunk++)			 				// Values 0 to 63 tweaked
	{
		indexes[row][chunk]=indexes[row][chunk]+8;
	}
 } 



  while (1)
  {

    FILE *fp1;

    int i = 0;
    unsigned char buffer[4097];

    //while (1) 
    //{
        fp1 = fopen("arquivofinal.txt","r");

        for(i=0; i<4097; i++)
            fscanf(fp1,"%d,", &buffer[i]);

        fclose(fp1);



       	//*********************************************************************************************************************
	for (row=0;row<=3;row++)							// For each of the 4 sets of lines
	{
		// One set of 4 panels is upside down relative to the other, so half the line data needs to clock in forwards half backwards
       		for (chunk=0;chunk<128;chunk++)						// 128 chunks in the 1024 pixels we need to clock in 
		{
			 // imagebuf is pointer + offset extracted from array
			 //printf("row=%d  chunk=%d   indexes[row][chunk]=%d\n",row,chunk,indexes[row][chunk]); fflush(stdout);

			 if (chunk<=63)
  				clock_pixels(buffer-1+(indexes[row][chunk]),8,'b');	
  			 else	clock_pixels(buffer+(indexes[row][chunk]),8,'f');

			//if ((indexes[row][chunk]>=728)&(indexes[row][chunk]<=735))
				//printf("row=%d  chunk=%d   indexes[row][chunk]=%d\n",row,chunk,indexes[row][chunk]); fflush(stdout);
		}

		// this way round is best i think
		update_leds();								// Now we have 1024 pixels clocked in update the display
       		select_row(row);							// Hmmm fails if I dont do this just before clocking each 1024 pixels ... 

		usleep(3000);
	}
   }
}

