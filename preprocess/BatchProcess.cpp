#include "ImageAnalyzer.h"
#include <fstream>
#include <sstream>
#include <dirent.h>
#include <stdio.h>
#include <iostream>


using namespace std;

int main() {
	ifstream filestream;
	ImageAnalyzer I;
	string filename;
	char *wholefile;
	DIR *dir;
	struct dirent *dirRef;
	size_t foundjpg, foundjpeg;
	FILE *json;
	json = fopen("colordata.json", "w");
	string line;
	puts("opening directory");
	if ((dir = opendir("./pictures")) == NULL)
	{
		puts("ERROR OPENING DIRECTORY");
		return -1;
	}
	puts("reading directory");
	while ((dirRef = readdir(dir)) != NULL)
	{
		filename = "pictures/" + string(dirRef->d_name);
		foundjpg = filename.find(".jpg");
		foundjpeg = filename.find(".jpeg");
		if (foundjpg != string::npos || foundjpeg != string::npos)
		{
			line = I.ProcessImg(filename);
			fprintf(json, "%s\n", line.c_str());
		}
		
	}
	fclose(json);
	closedir(dir);
	return 0;
	
}
