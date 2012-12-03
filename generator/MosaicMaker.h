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

class ImageColor {
	int red;
	int blue;
	int green;

public:
	ImageColor();
	ImageColor(int _red, int _blue, int _green);
	void SetColors(int _red, int _blue, int _green);
	int R() { return red; }
	int B() { return blue; }
	int G() { return green; }
	void Print();
};

class Block {
	ImageColor color;
	int x, y;
	
public:
	Block();
	Block(ImageColor _color, int _x, int _y);
	void SetBlock(ImageColor _color, int _x, int _y);
	void Print();
}

class MosaicMaker {
	int width, height, components;
	unsigned char **pixels, **mainPicture, **newPixels;
	char *readFile, writeFile[11];

public:
	int ReadImage(string _filename);
	int BreakDown(int squareSize);
	void WriteBlock(char _filename, Block block);
};

#endif
