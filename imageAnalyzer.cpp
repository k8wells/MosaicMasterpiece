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
	
	FILE *image = fopen(_filename, "rb");
	
	if (!image)
	{
		printf("ERROR OPENING IMAGE %s\n", _filename);
		return FILE_NOT_FOUND;
	}
	
	// error handler
	cinfo.err = jpeg_std_err(&jerr);
	// decompression, read JPEG header
	jpeg_create_decompress(&cinfo);
	jpeg_stdio_src(&cinfo, image);
	// get image inf
	jpeg_read_header(&cinfo, true);
	
	width = cinfo.image_width;
	height = cinfo.image_height;
	components = cinfo.num_components;
	
	printf("IMAGE INFO OBTAINED FOR %s\n", _filename);
	printf("W %i\tH %i\tC %i\n", width, height, components);
	
	// start reading image	
	JSAMPROW row_pointer[1];
	// decompress
	jpeg_start_decompress(&cinfo);
	
	// allocate memory
	
	// finish decompression, fee memory
	jpeg_finish_decompress(&cinfo);
	jpeg_destroy_decompress(&cinfo);
	fclose(img);
	free(row_pointer[0]);
	imageHash[_filename] = ImageColor();
	printf("IMAGE %s READ:\tAVG R %i\tAVG B %i\tAVG G %i\t\n", _filename, imageHash[_filename].R(), imageHash[_filename].B(), imageHash[_filename].G());
}

