
// Bit crappy, but we only need one UDP receive buffer so just make it all global for lazy code
int udpsockfd;										// UDP socket file descriptor
struct sockaddr_in recvaddr;								// An IP address record structure

udp_setup_socket(int listen)
{
	// Open socket
        udpsockfd = socket(PF_INET, SOCK_DGRAM, 0);
	if (udpsockfd<0)
        {
                perror("error, could not create socket");
                exit(1);
        }
        printf("%s: Socket created\n",PROGNAME);
	fflush(stdout);

	// Setuop socket, specify listening interfaces etc
        recvaddr.sin_family = AF_INET;
        recvaddr.sin_port = htons(PORT);
        recvaddr.sin_addr.s_addr = INADDR_ANY;
        memset(recvaddr.sin_zero,'\0',sizeof (recvaddr.sin_zero));

	// Put socket in non blcoking mode
	int flags = fcntl(udpsockfd, F_GETFL);						// Get the sockets flags
	flags |= O_NONBLOCK;								// Set NONBLOCK flag
	if (fcntl(udpsockfd, F_SETFL, flags) == -1)					// Write flags back
	{
                perror("error,fcnctl failed - could not set socket to nonblocking");
		exit(1);
	}

	// Bind to socket, start socket listening
	if (listen==TRUE)
	{
		int bret;
        	bret = bind(udpsockfd, (struct sockaddr*) &recvaddr, sizeof (recvaddr));
		if (bret < 0)
        	{
			printf("(%d) for port (%d)\n",bret,PORT);
                	perror("bind failed, only one process can bind at a time");
                	exit(1);
        	}
        	fprintf(stderr,"%s: Listening for UDP data on port %d \n",PROGNAME,PORT);
		fflush(stderr);
	}
}



// Get a UDP packet if one exists
int udp_receive (unsigned char *ubuffer,int packetsize,char *originating_ip, int verbose, int hexdump, int *eagaincount, int *perrors)
{
	//struct sockaddr_in recvaddr;							// An IP address record structure
	int c,i;
	unsigned int offs;
        int numbytes;
        int addr_len;

        addr_len = sizeof(recvaddr);
	//numbytes = recvfrom (udpsockfd, ubuffer, packetsize, 0, (struct sockaddr *) &recvaddr, &addr_len);
	numbytes = recvfrom (udpsockfd, (char*)ubuffer, packetsize, 0, (struct sockaddr *) &recvaddr, &addr_len);

	if (numbytes>0)
	{
		// Packet too small, this is an error
		if (numbytes!=packetsize)
		{
			*perrors=*perrors+1;
			printf("size wrong got %d bytes expecing %d bytes\n",numbytes,packetsize);
			fflush(stdout);
			// tell caller it was not a packet so it doesnt try and process it
			return(FALSE);
		}

		sprintf(originating_ip,"%s",(char*)inet_ntoa(recvaddr.sin_addr));
		if (verbose==TRUE)							// If chatty is true show receipt of packets
		{
			printf("%s: received %d bytes from %s via UDP port %d  ",PROGNAME,numbytes,originating_ip,PORT);  
			fflush(stdout);
		}
 
		if (hexdump==TRUE)							// If dump is true show packets as hexdump
		{
			if (verbose==TRUE)
				printf(" Dumping contents\n");
			c=0; offs=0;
			printf("%04X: ",offs);
			for (i=0;i<numbytes;i++)
			{
				//printf("%c",udpbuffer[i]);				// ASCII
				printf("%02X ",ubuffer[i]);				// HEX
				c++;
				if (c==16)
				{
					offs=offs+16;
					c=0;
					printf("\n%04X: ",offs);
					fflush(stdout);
				}
			}
			printf("\n");
		}
		return(TRUE);
	}

	// If recvfrom returns a negative value an error occured
	if (numbytes<0)
	{
		if (errno!=EAGAIN)							// we ignore this one !
		{
			//sprintf(lasterror,"%s",strerror(errno));
			fflush(stdout);
		}
		else
		{
			// count number of EAGAIN (nothing to read) non blocked reads here. If we dont get any in one second then we have 
			// a problem :-( 
			// windows does not generate eagain
			*eagaincount=*eagaincount+1;
		}
	}
	return(FALSE);									// No data, probably got EAGAIN
}


