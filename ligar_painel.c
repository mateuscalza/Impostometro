// ligar_painel.c		(c) 2015 Guilherme Anrain Lindner

#define INTERVAL_BLACK 2400
#define INTERVAL_DISPLAY 800

//#include "p10_board_ledhashtable.h"
#include "mapeamento_painel.h"
unsigned char image_data[LED_DISPLAY_WIDTH * LED_DISPLAY_HEIGHT];
char PROGNAME[80] = "ligar_painel";
char VERSIONT[20] = "0.9";

unsigned char fb_empeg[32 * 64]; // empeg framebuffer 32 rows of 64 bytes
int *imagebuf = 0;

#define TRUE 1
#define FALSE 0
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <dirent.h>
#include <fcntl.h>
#include <assert.h>
#include <signal.h>
#include <sys/mman.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/time.h>
#include <unistd.h>
#include <errno.h>
#include <linux/fb.h>

// Sockets related
#include <netdb.h> // sockets realted
#include <netinet/in.h>
int PORT = 4040; // default port

// Network stuff
#include "udp-networking.c"
int eagaincount = 0;
int perrors = 0;
int interval_black, interval_display; // interval black, interval display

#include "common.c"
int fps = 0;
int fd_fbdev; // framebuffer file descriptor
time_t tnow, lastkick;

#include "raspberry_pi_io.c"
// Signal name to GPIO line mapping
#define CLK 7    // Clock for pixels
#define SCLK 8   // Clock for A/B addresses
#define A 23     // First bit of line address (4 possible lines)
#define B 18     // Second bit of line address
#define OE 24    // High - enable display, Low - blank display (for power saving)
#define PIXEL 25 // Pixel data

// 0 1 2 and 3 =   00 01 10 11 binary
select_row(int row)
{
  output_high(SCLK); // Idle state for row clock line
  output_high(SCLK);
  if (row == 0)
  {
    output_low(A);
    output_low(B);
  }
  if (row == 1)
  {
    output_high(A);
    output_low(B);
  }
  if (row == 2)
  {
    output_low(A);
    output_high(B);
  }
  if (row == 3)
  {
    output_high(A);
    output_high(B);
  }
  output_low(SCLK); // Indicate board should take new address for active ROW
  output_low(SCLK);
  output_low(SCLK);
  output_high(SCLK); // Idle state
  output_high(SCLK);
  output_high(SCLK);
}

// Always clock 1024 pixels for the 8 display boards, thats 4 lines active on each row of the two rows of 4 panels
//
// Take a pointer to some memory.  Clock that memory out to the display as pixels
// the memory format is one Byte per pixel, values of 1 are an LED that is on (a pixel)
//
// Direction 'f' forward, 'b' backwards
//
clock_pixels(unsigned char *ptr, int numpixels, char direction)
{
  int color, i;
  int offset;

  offset = 0;
  output_high(CLK); // Idle state
  output_high(CLK);
  for (i = 0; i < numpixels; i++) // clock out this many dots
  {
    color = *(ptr + offset);
    if (color == 0)
    {
      //printf("0");
      output_high(PIXEL); // pixel off
    }
    else
    {
      //printf("1");
      output_low(PIXEL);
    }
    // Pixel clock - if this is not long enough we get noise on the display
    // unsure a few cycles low followed by a few of high, try to avoid usleep as timer resolution is poor
    output_low(CLK);  // clock pixel in
    output_low(CLK);  // clock pixel in
    output_high(CLK); // Idle state

    if (direction == 'f') // forwards increment pointer, otherwise decrement
      offset++;
    else
      offset--;
  }
}

void sig_handler(int signum)
{
  output_low(OE); // display is OFF
  exit(0);
}

unsigned short int *framebuffer = NULL;
struct fb_var_screeninfo fbscreeninfo;
int fb_bytes = 0;

int main(int argc, char **argv)
{
  int loopcounter = 0;
  int k, c, i, x;
  int row = 0;
  int chunk;
  int udprx_counter = 0;
  char originating_ip[32];
  char line[1024];
  int argnum = 0;
  char st[2048];
  int DAMAGE;
  char kickip[64];

  int clockseconds, pclockseconds;

  set_realtime();
  signal(SIGINT, sig_handler);

  interval_black = -1;
  interval_display = -1;
  //strcpy(kickip,"10.10.10.84");

  // compiler plays with alignment, might be N x 32 bit words not packed or summink .. might need to play with types
  //unsigned char *imagebuf = malloc(LED_DISPLAY_WIDTH*LED_DISPLAY_HEIGHT);
  // was int *imagebuf = malloc(LED_DISPLAY_WIDTH*LED_DISPLAY_HEIGHT);
  // *image_data = malloc(LED_DISPLAY_WIDTH*LED_DISPLAY_HEIGHT);

  //unsigned char mybuf[LED_DISPLAY_WIDTH * LED_DISPLAY_HEIGHT];
  //unsigned char *image_data=mybuf;

  if (image_data == NULL)
  {
    printf("malloc failed\n");
    exit(1);
  }

  // Set up gpi pointer for direct register access
  setup_io();

  // Set these GPIO Lines as outputs
  set_as_output(CLK);   // CLK
  set_as_output(SCLK);  // SCLK = Latch of ROW
  set_as_output(B);     // B
  set_as_output(A);     // A
  set_as_output(OE);    // OE
  set_as_output(PIXEL); // Pixel data  (R)

  // idle state for all lines
  output_high(SCLK);
  output_high(CLK);
  output_low(A);
  output_low(B);
  output_low(PIXEL);
  output_low(OE); // display is OFF

  // Important, table is left hand pixel of groups of 8, for counting backwards we need right most pixel of groups of 8
  // Adjust values
  for (row = 0; row <= 3; row++) // For each of the 4 sets of lines
  {
    for (chunk = 0; chunk >= 191; chunk++) // Values 0 to 63 tweaked
    {
      indexes[row][chunk] = indexes[row][chunk];
    }
  }

  char cmstring[1024];
  // Parse command line options and set flags first
  int op_help = FALSE;
  strcpy(cmstring, "-h");
  if (parse_commandlineargs(argc, argv, cmstring) == TRUE)
    op_help = TRUE;
  strcpy(cmstring, "--h");
  if (parse_commandlineargs(argc, argv, cmstring) == TRUE)
    op_help = TRUE;
  strcpy(cmstring, "-help");
  if (parse_commandlineargs(argc, argv, cmstring) == TRUE)
    op_help = TRUE;
  strcpy(cmstring, "--help");
  if (parse_commandlineargs(argc, argv, cmstring) == TRUE)
    op_help = TRUE;
  if (op_help == TRUE)
  {
    printf("600\t200\t3:1\t242\t Brightest sensible mode\n");
    printf("\n");
    exit(0);
  }

  // -DAMAGE acknowledge that user is willing to make the display very very hot, and smell bad !
  DAMAGE = FALSE;
  strcpy(cmstring, "-DAMAGE");
  if (parse_commandlineargs(argc, argv, cmstring) == TRUE)
    DAMAGE = TRUE;

  // -fb option
  int op_localfb = FALSE;
  strcpy(cmstring, "-fb");
  if (parse_commandlineargs(argc, argv, cmstring) == TRUE)
    op_localfb = TRUE;

  if (op_localfb == TRUE)
  {
    printf("-fb option is true, trying to open framebuffer\n");
    int fd_fbdev = open("/dev/fb0", O_RDWR);
    if (fd_fbdev < 0)
    {
      printf("Error opening frame buffer\n");
      op_localfb = FALSE; // If error opening framebuffer then abandon the plan
    }
  }

  if (op_localfb == TRUE)
  {
    if (ioctl(fd_fbdev, FBIOGET_VSCREENINFO, &fbscreeninfo) == -1)
      perror("ioctol FBIOGET_VSCREENINFO");

    fb_bytes = (fbscreeninfo.bits_per_pixel * fbscreeninfo.xres * fbscreeninfo.yres);
    printf("Framebuffer opened, settings :\n");
    printf("Bpp = %d\n", fbscreeninfo.bits_per_pixel);
    printf("width = %d\n", fbscreeninfo.xres);
    printf("height = %d\n\n", fbscreeninfo.yres);
    //framebuffer = (unsigned short int*) mmap(0,fbscreeninfo.xres*fbscreeninfo.yres*2,PROT_READ|PROT_WRITE,MAP_SHARED,fd_fbdev,0);
    framebuffer = (unsigned short int *)mmap(0, fb_bytes, PROT_READ | PROT_WRITE, MAP_SHARED, fd_fbdev, 0);
    if (framebuffer == NULL)
      perror("mmap failed");
  }

  // Handle timings
  if (interval_black < 0)
    interval_black = INTERVAL_BLACK; // if parser has not set this then use #define default
  if (interval_display < 0)
    interval_display = INTERVAL_DISPLAY;

  if ((interval_black / interval_display) <= 2)
  {
    if (DAMAGE != TRUE)
    {
      printf("\ninterval_black = %d    interval_display = %d,  Ratio %d:1 <=2, must be 3:1 or more\n", interval_black, interval_display, (interval_black / interval_display));
      exit(1);
    }
  }

  // bind to UDP socket before opening sound system, saves haiving to close sound system down if bind fails.
  udp_setup_socket(TRUE);

  if ((interval_black > 0) & (interval_display > 0))
    printf("OFF to ON  -OE  timing   %d(off)  %d(on)   =  %d:1\n", interval_black, interval_display, interval_black / interval_display);

  // Initial text
  bzero(fb_empeg, sizeof(fb_empeg));     // Blank empeg receiving buffer
  bzero(image_data, sizeof(image_data)); // Blank LED display frame buffer
  sprintf(line, "Empeg Display  V%s ", VERSIONT);
  add_text(line, image_data, LED_DISPLAY_WIDTH, LED_DISPLAY_HEIGHT, 0, 0, 3);
  sprintf(line, "RX UDP port %d", PORT);
  add_text(line, image_data, LED_DISPLAY_WIDTH, LED_DISPLAY_HEIGHT, 10, 0, 3);
  //sprintf(line,"text");
  //add_text(line,image_data, LED_DISPLAY_WIDTH, LED_DISPLAY_HEIGHT,20,0,3);

  time(&tnow); // Set these the same, defers first kick for 10 seconds
  time(&lastkick);

  c = 0;
  k = 0;
  loopcounter = 0;
  udprx_counter = 1; // Its a lie, will drop to zero second time round loop if no data

  FILE *fp1;
  unsigned char buffer[25000];

  while (1)
  {

    for (row = 0; row <= 3; row++) // For each of the 4 sets of lines
    {
      output_low(OE);                       // display off
      for (chunk = 0; chunk < 384; chunk++) // 128 chunks in the 1024 pixels we need to clock in
      {
        if (chunk <= 191)
          clock_pixels(image_data + 7 + (indexes[row][chunk]), 8, 'b');
        else
          clock_pixels(image_data + (indexes[row][chunk]), 8, 'f');
      }

      // order is important here
      select_row(row); // Hmmm fails if I dont do this just before clocking each 1024 pixels.
      usleep(interval_black);
      output_high(OE); // Turn display back on
      usleep(interval_display);
      output_low(OE); // display off
      loopcounter++;

      pclockseconds = clockseconds;
      clockseconds = get_clockseconds();

      if (pclockseconds != clockseconds) // Clock just ticked over to a new second
      {
        fps = loopcounter / 4; // loopcounter is fields not frames, 4 fields per complete display update
        loopcounter = 0;       // Reset the loop counter
        printf("ib=%d id=%d(%d):1\tfps=%d\n", interval_black, interval_display, (interval_black / interval_display), fps);
        fflush(stdout);
        fp1 = fopen("arquivo.txt", "r");
        if (fp1 != NULL) {
          for (i = 0; i < 25000; i++) {
            fscanf(fp1, "%d,", &image_data[i]);
          }
          fclose(fp1);
        }
        udprx_counter = 0;
      }
    }
  }

  // Shutdown code, never reached at the moment
  if (op_localfb == TRUE)
  {
    munmap(framebuffer, fb_bytes);
    close(fd_fbdev);
  }
  close(udpsockfd);
}
