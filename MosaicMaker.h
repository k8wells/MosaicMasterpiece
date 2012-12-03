#ifndef IMAGEANALYZER_H 
#define IMAGEANALYZER_H

#include <stdio.h>
#include <jpeglib.h>
#include <jerror.h>
#include <stdlib.h>
#include <vector>
#include <string.h>
#include <math.h>
#include <map>
#include <ctype.h>
#include <string>

#define SUCCESS			0
#define FILE_NOT_FOUND	-1

using namespace std;

class MosaicMaker {
	int width, height, components;
	unsigned char **pixels, **newPixels;
	char *readFile, writeFile[11];

public:
	int ReadImage(string _filename);
	int BreakDown(int squareSize);
	
};

#endif
