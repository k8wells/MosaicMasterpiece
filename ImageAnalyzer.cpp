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

char* ImageAnalyzer::GetID(char _filename[])
{
	char idStr[10];
	int i = 0;
	while(true)
	{
		if (_filename[i + 9] == '_')
			break;
		if (isdigit(_filename[i + 9]))
			idStr[i] = _filename[i + 9];
		i++;
	}
	return idStr;
}

int ImageAnalyzer::ReadImage(char _filename[]) {
	struct jpeg_decompress_struct cinfo;
	struct jpeg_error_mgr jerr;
	readFile = _filename;	
	//pixels.clear();
	
	printf("OPENING IMAGE %s\n", readFile);
	FILE *image = fopen(readFile, "rb");
	
	if (!image)
	{
		printf("ERROR OPENING IMAGE %s\n", readFile);
		return FILE_NOT_FOUND;
	}
	
	// error handler
	cinfo.err = jpeg_std_error(&jerr);
	// decompression, read JPEG header
	jpeg_create_decompress(&cinfo);
	jpeg_stdio_src(&cinfo, image);
	// get image info
	jpeg_read_header(&cinfo, true);
	
	width = cinfo.image_width;
	height = cinfo.image_height;
	components = cinfo.num_components;
	
	printf("IMAGE INFO OBTAINED FOR %s\n", readFile);
	printf("W %i\tH %i\tC %i\n", width, height, components);
	
	// start reading image	
	JSAMPROW row_pointer[1];
	pixels = new unsigned char*[height];
	for (int i = 0; i < height; i++)
	{
		pixels[i] = new unsigned char[width * 3];
	}
	
	// decompress
	jpeg_start_decompress(&cinfo);
	// allocate memory
	row_pointer[0] = (JSAMPLE*)malloc(width * components);
	
	int y = 0, temp = 0;
	while(cinfo.output_scanline < height)
	{
		jpeg_read_scanlines(&cinfo, row_pointer, 1);
		for (int x = 0; x < width * components; x++)
		{
			pixels[y][x] = row_pointer[0][x];
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
	return 0;

}

ImageColor ImageAnalyzer::FindAvg() {
	/*if ((int readresult = ReadImage(_readName)) != 0)
		puts("ERROR READING IMAGE %i\n", readresult);*/
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

int ImageAnalyzer::CropAndResize(char ID[]) {
	// set up to write new image
	
	for (int y = 0; y < height; y++)
	{
		for (int x = 0; x < width * 3; x++)
		{
			printf("%03i ", pixels[y][x]);
		}
		printf("\n");
	}
	
	puts("STARTING CROP AND RESIZE");
	struct jpeg_compress_struct cinfo;
	struct jpeg_error_mgr jerr;
	FILE *out;
	sprintf(writeFile, "cr_%s.jpeg", ID);
	printf("%s\n", writeFile);
	JSAMPROW row_pointer[1];
	int row_stride;
	cinfo.err = jpeg_std_error(&jerr);
	jpeg_create_compress(&cinfo);
	if ((out = fopen(writeFile, "wb")) == NULL)
	{
		printf("ERROR OPENING FILE TO WRITE %s\n", writeFile);
		return -1;
	}
	jpeg_stdio_dest(&cinfo, out);
	cinfo.input_components = 3;
	cinfo.in_color_space = JCS_RGB;
	jpeg_set_quality(&cinfo, 10, TRUE);
	jpeg_set_defaults(&cinfo);
	int cropOff = 0;
	
	unsigned char **imgbuf;
	
	if (width == height)
	{
		puts("Image does not need to be cropped.");
		imgbuf = pixels;
	}

	// need to crop sides off
	else if (width > height)
	{
		cinfo.image_width = cinfo.image_height = height;
		row_stride = height;
		imgbuf = new unsigned char*[height];
		jpeg_start_compress(&cinfo, TRUE);
		
		cropOff = (width - height) / 2;
		printf("Cropping off %i pixels on each side\n", cropOff);
		
		for (int i = 0; i < height; i++)
		{
			imgbuf[i] = new unsigned char[height * 3];
		}
		
		int xx;
		for (int y = 0; y < height; y++)
		{
			xx = 0;
			for (int x = cropOff * 3; x < (cropOff + height) * 3; x++)
			{
				imgbuf[y][xx] = pixels[y][x];
				xx++;
			}
		}
	}
	
	// crop top and bottom
	else if (height > width)
	{
		cinfo.image_width = cinfo.image_height = width;
		row_stride = width;
		imgbuf = new unsigned char*[width];
		jpeg_start_compress(&cinfo, TRUE);
		
		cropOff = (height - width) / 2;
		printf("Cropping off %i pixels on each side\n", cropOff);
		
		for (int i = 0; i < width; i++)
		{
			imgbuf[i] = new unsigned char[width * 3];
		}
		
		int yy = 0;
		for (int y = cropOff; y < cropOff + width; y++)
		{
			for (int x = 0; x < width * 3; x++)
			{
				imgbuf[yy][x] = pixels[y][x];
			}
			yy++;
		}
	}
	
	while (cinfo.next_scanline < cinfo.image_height)
	{
		row_pointer[0] = imgbuf[cinfo.next_scanline];
		for (int i = 0; i < height * 3; i++)
		{
			printf("%03i ", imgbuf[cinfo.next_scanline][i]);
		}
		printf("\n");
		(void) jpeg_write_scanlines(&cinfo, row_pointer, 1);
	}
	jpeg_finish_compress(&cinfo);
	fclose(out);
	jpeg_destroy_compress(&cinfo);

	puts("IMAGE CROPPED");
	
}

void ImageAnalyzer::ProcessImg(char _readName[])
{
	ReadImage(_readName);
	//CropAndResize(0);
	char *id = GetID(_readName);
	CropAndResize(id);
	//ImageColor avgColor = FindAvg();
	//imageHash[readFile] = avgColor;
	
	//printf("IMAGE %s READ:\tAVG R %i\tAVG B %i\tAVG G %i\t\n", readFile, imageHash[readFile].R(), imageHash[readFile].B(), imageHash[readFile].G());
}

void ImageAnalyzer::ProcessChunk(coordinates _topLeft, coordinates _bottomRight) {
	
}


int main() {
	
	ImageAnalyzer I;
	//I.ProcessImg("images/sidecrop.jpeg");
	I.ProcessImg("pictures/8164531074_b2c4307ebc_z.jpg");
	//I.ProcessImg("pictures/8164039972_0f8d7eda6c_z.jpg");
}
