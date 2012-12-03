#ifndef IMAGEANALYZER_H 
#define IMAGEANALYZER_HFIFO permissions

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
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include "../ImageColor.h"

#define SUCCESS			0
#define FILE_NOT_FOUND	-1

using namespace std;

class Block {
	ImageColor color;
	int x, y;
	
public:
	Block();
	Block(ImageColor _color, int _x, int _y);
	int R() { return color.R(); }
	int G() { return color.G(); }
	int B() { return color.B(); }
	int Y() { return y; }
	int X() { return x; }
	void Set(ImageColor _color, int _x, int _y);
	void Print();
};

class MosaicMaker {
	int width, height, components;
	unsigned char **pixels, **mainPic, **newPixels;
	char *readFile, writeFile[11];
	int fd;
	char *fifo;

public:
	int OpenPipe();
	int WriteTags(string tags);
	int WriteColor(ImageColor c);
	string ReadID();
	int ClosePipe();
	int ReadImage(string _filename);
	int BreakDown(int squareSize);
	void WriteBlock(string filename, Block block);
};

#endif
