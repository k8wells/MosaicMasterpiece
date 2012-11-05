#ifndef IMAGEANALYZER_H 
#define IMAGEANALYZER_H

#include <vector>
#include <stdio>
#include <jpeglib.h>
#include <string.h>
#include <math.h>

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
	void setColors(int _red, int _blue, int _green);
	int R() { return red; }
	int B() { return blue; }
	int G() { return green; }
}

class ColorMatrix {
	
}

class ImageAnalyzer {
	int width, height, components;
	vector<vector<ImageColor> > pixels;
	int redsum, bluesum, greensum;
	map<String, ImageColor> imageHash;
	
public:
	int Height() { return height; }
	int Width() { return width; }
	int Components() { return components; }
	int ReadImage(char _filename[]);
	//ImageColor GetAvgColor(char _imgname[]);

}

#endif
