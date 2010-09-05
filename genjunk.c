/*
  genjunk.c - Generate a file with random bytes.
  Size can be specified in bytes (default), kilobytes (k),
  or megabytes (M) by appending k or M to end of number.

  Scott Livingston
  August 30, 2008
*/
  

#include <errno.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>


int main( int argc, char *argv[] )
{
	long fsize;
	size_t sl; //request size string length
	FILE *jfile;
	long i; //counter

	if (argc != 3) {
		printf( "Usage: genjunk filename size[k,M]\n" );
		return 1;
	}

	fsize = atoi( argv[2] );
	if (fsize < 0) {
		fprintf( stderr, "Error: invalid file size: %ld\n", fsize );
		return -1;
	}

	//determine input argument units
	sl = strlen( argv[2] );
	if (argv[2][sl-1] == 'k') { //kilobytes
		fsize = fsize*1024;
	} else if (argv[2][sl-1] == 'M') { //megabytes
		fsize = fsize*1048576;
	}

	//finally, generate the file.
	jfile = fopen( argv[1], "wb" );
	if (jfile == NULL) { //error
		fprintf( stderr, "fopen (called by genjunk): %s: ", argv[1] );
		perror( NULL );
		return -1;
	}
	
	for (i = 0; i < fsize; i++)
		fprintf( jfile, "%c", (unsigned char)rand() );

	fclose(jfile);

	return 0;
}
