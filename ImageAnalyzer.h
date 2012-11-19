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

typedef pair<int, int> coordinates;

class ImageAnalyzer {
	int width, height, components;
	int redsum, bluesum, greensum;

	unsigned char **pixels;
	char *readFile, writeFile[18];

	
public:
	map<string, ImageColor> imageHash;
	int Height() { return height; }
	int Width() { return width; }
	int Components() { return components; }
	string GetID(string _filename);
	int ReadImage(string _filename);
	int CropAndResize(string ID);
	ImageColor FindAvg();
	string ProcessImg(string _filename);
	void ProcessChunk(coordinates _topLeft, coordinates _bottomRight);

};

#endif
