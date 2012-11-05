#include "ImageAnalyzer.h"

ImageColor::ImageColor() {
	red = 0;
	blue = 0;
	green = 0;
}

ImageColor::ImageColor(int _red, int _blue, int _green) {
	red = _red;
	blue = _blue;
	green = _green;
}

void ImageColor::SetColors(int _red, int _blue, int _green) {
	red = _red;
	blue = _blue;
	green = _green;
}


/////////////////////////////////////////////////////////////////////

int ImageAnalyzer::ReadImage(char _filename[]) {
	struct jpeg_decompress_struct cinfo;
	struct jpeg_error_mgr jerr;
	
	pixels.clear();
	
	printf("OPENING IMAGE %s\n", _filename);
	FILE *image = fopen(_filename, "rb");
	
	if (!image)
	{
		printf("ERROR OPENING IMAGE %s\n", _filename);
		return FILE_NOT_FOUND;
	}
	
	// error handler
	cinfo.err = jpeg_std_error(&jerr);
	
	puts("DECOMPRESSING IMAGE");
	// decompression, read JPEG header
	jpeg_create_decompress(&cinfo);
	jpeg_stdio_src(&cinfo, image);
	puts("GETTING IMAGE INFO");
	// get image info
	jpeg_read_header(&cinfo, true);
	
	puts("GETTING WIDTH");
	width = cinfo.image_width;
	puts("GETTING HEIGHT");
	height = cinfo.image_height;
	puts("GETTING COMPONENTS");
	components = cinfo.num_components;
	
	printf("IMAGE INFO OBTAINED FOR %s\n", _filename);
	printf("W %i\tH %i\tC %i\n", width, height, components);
	
	// start reading image	
	JSAMPROW row_pointer[1];
	for (int y = 0; y < height; y++)
	{
		vector<int> temp;
		pixels.push_back(temp);
	}
	
	// decompress
	jpeg_start_decompress(&cinfo);
	
	// allocate memory
	row_pointer[0] = (JSAMPLE*)malloc(width * components);
	printf("WIDTH %i * COMPONENTS %i = %i\n", width, components, width * components);
	
	int y = 0, temp = 0;
	while(cinfo.output_scanline < height)
	{
		jpeg_read_scanlines(&cinfo, row_pointer, 1);
		for (int x = 0; x < width * components; x++)
		{
			temp = row_pointer[0][x];
			pixels[y].push_back(temp);
		}
		y++;
	}
	
	for (int i = 0; i < width * components; i++)
	{
		row_pointer[0][i] = 0;
	}
	
	// finish decompression, fee memory
	jpeg_finish_decompress(&cinfo);
	jpeg_destroy_decompress(&cinfo);
	fclose(image);
	free(row_pointer[0]);

}

ImageColor ImageAnalyzer::FindAvg() {
	int R = 0, G = 0, B = 0;
	for (int y = 0; y < height; y++)
	{
		for (int x = 0; x < width; x++)
		{
			R += pixels[y][x * components];
			G += pixels[y][x * components + 1];
			B += pixels[y][x * components + 2];
			//printf("(%i, %i)\tR %i\tG %i\tB %i\n", x, y, R, G, B);
		}
	}
	R /= height * width;
	G /= height * width;
	B /= height * width;
	ImageColor color = ImageColor(R, G, B);
	return color;
}

void ImageAnalyzer::ProcessImg(char _filename[])
{
	ReadImage(_filename);
	ImageColor avgColor = FindAvg();
	imageHash[_filename] = avgColor;
	printf("IMAGE %s READ:\tAVG R %i\tAVG B %i\tAVG G %i\t\n", _filename, imageHash[_filename].R(), imageHash[_filename].B(), imageHash[_filename].G());
}

void ImageAnalyzer::ProcessChunk(coordinates _topLeft, coordinates _bottomRight) {
	
}


int main() {
	
	ImageAnalyzer I;
	I.ProcessImg("redchecker2.jpg");
}
