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
};

typedef pair<int, int> coordinates;

class ImageAnalyzer {
	int width, height, components;
	int redsum, bluesum, greensum;
	map<char*, ImageColor> imageHash;
	unsigned char **pixels;
	char *readFile, writeFile[18];

	
public:
	int Height() { return height; }
	int Width() { return width; }
	int Components() { return components; }
	char* GetID(char _filename[]);
	int ReadImage(char _filename[]);
	int CropAndResize(char ID[]);
	ImageColor FindAvg();
	void ProcessImg(char _filename[]);
	void ProcessChunk(coordinates _topLeft, coordinates _bottomRight);

};

#endif
