#import "MosaicMaker.h"

// identical to ImageAnalyzer::ReadImage
int MosaicMaker::ReadImage(string _filename) {
	struct jpeg_decompress_struct cinfo;
	struct jpeg_error_mgr jerr;
	readFile = _filename.c_str();	
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
	return SUCCESS;
}

int MosaicMaker::BreakDown(int squareSize) {
	int newHeight = height/squareSize * 100;
	int newWidth = width/squareSize * 100;
	newPixels = new unsigned char*[newHeight];
	for (int y = 0; y < newHeight; y++)
	{
		newPixels[y] = new unsigned char[newWidth * 3];
	}
	int leftCrop = 0, topCrop = 0, rightCrop = 0, bottomCrop = 0;
	leftCrop = (width % squareSize) / 2;
	topCrop = (height % squareSize) / 2;
	rightCrop = (width % squareSize) - leftCrop;
	bottomCrop = (height % squareSize) - topCrop;
	
	puts("STARTING BREAKDOWN");
	struct jpeg_compress_struct cinfo;
	struct jpeg_error_mgr jerr;
	FILE *out;
	sprintf(writeFile, "missrev10.jpg");
	printf("CROPPING PICTURE %s\n", writeFile);
	JSAMPROW row_pointer[1];
	int row_stride;
	cinfo.err = jpeg_std_error(&jerr);
	jpeg_create_compress(&cinfo);
	puts("Opening file");
	if ((out = fopen(writeFile, "wb")) == NULL)
	{
		printf("ERROR OPENING FILE TO WRITE %s\n", writeFile);
		return -1;
	}
	jpeg_stdio_dest(&cinfo, out);
	cinfo.input_components = 3;
	cinfo.in_color_space = JCS_RGB;
	cinfo.image_width = newWidth;
	cinfo.image_height = newHeight;
	jpeg_set_quality(&cinfo, 10, TRUE);
	jpeg_set_defaults(&cinfo);
	jpeg_start_compress(&cinfo, TRUE);
	
	int r, g, b;
	int xBlock = 0, yBlock = 0;
	int x = 0, y = 0;
	/*printf("new y %i new x %i\n", newHeight, newWidth);
	printf("height = %i, topCrop = %i, bottomCrop = %i\n", height, topCrop, bottomCrop);
	printf("width = %i, leftCrop = %i, rightCrop = %i\n", width, leftCrop, rightCrop);*/
	
	for (int y = topCrop; y < height - bottomCrop; y += squareSize)
	{
		//printf("analyzing y %i\n", y);
		for (int x = leftCrop; x < (width - rightCrop) * 3; x += squareSize * 3)
		{
			//printf("analyzing x %i\n", x);
			// looping through squareSize
			r = 0, g = 0, b = 0;
			for (int sy = 0; sy < squareSize; sy++)
			{
				for (int sx = 0; sx < squareSize * 3; sx += 3)
				{
					//printf("y %i x %i sy %i sx %i\n", y, x, sy, sx);
					r += pixels[y + sy][x + sx];
					g += pixels[y+ sy][x + sx + 1];
					b += pixels[y + sy][x + sx + 2];
				}
			}
			r /= squareSize * squareSize;
			g /= squareSize * squareSize;
			b /= squareSize * squareSize;
			//printf("xBlock %i, yBlock %i\n", xBlock, yBlock);
			for (int yy = 0; yy < 100; yy++)
			{
				//printf("writing line %i\n", y);
				for (int xx = 0; xx < 300; xx += 3)
				{
					//printf("writing y %i, x %i\n", yBlock + yy, xBlock + xx);	
					newPixels[yBlock + yy][xBlock + xx] = r;
					newPixels[yBlock + yy][xBlock + xx + 1] = g;
					newPixels[yBlock + yy][xBlock + xx + 2] = b;
				}
			}
			xBlock += 300;
		}
		yBlock += 100;
		xBlock = 0;
	}
		
	while (cinfo.next_scanline < cinfo.image_height)
	{
		row_pointer[0] = newPixels[cinfo.next_scanline];
		(void) jpeg_write_scanlines(&cinfo, row_pointer, 1);
		//printf("scanline %i written\n", cinfo.next_scanline);	
	}
	jpeg_finish_compress(&cinfo);
	fclose(out);
	jpeg_destroy_compress(&cinfo);
	printf("NEW IMAGE SAVED: %s\n", writeFile);
}

int main() {
	MosaicMaker mm;
	mm.ReadImage("missrev.jpg");
	mm.BreakDown(10);
}
