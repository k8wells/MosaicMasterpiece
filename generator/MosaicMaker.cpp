#import "MosaicMaker.h"

Block::Block() {
	color = ImageColor();
	x = y = 0;
}

Block::Block(ImageColor _color, int _x, int _y) {
	color = _color;
	x = _x;
	y = _y;
}

void Block::Set(ImageColor _color, int _x, int _y) {
	color = _color;
	x = _x;
	y = _y;	
}

/////////////////////////////////////////////////////////////////////

// ------------ Pipe functions ------------ //
int MosaicMaker::OpenPipe() {
    puts("Opening pipes...");
	int ret = 0;
	writeFifo = "cppToPy";
	readFifo = "pyToCpp";
	if(mkfifo(writeFifo, 0666) != 0)
	{
		//if (errno != EEXIST)
			perror("ERROR CREATING WRITE PIPE");
	/*	else if (errno != SUCCESS)
			puts("Write pipe is already open.");*/
		//return ret;
	}
	//puts("Write pipe created.");
	fdw = open(writeFifo, O_WRONLY);
	if (fdw == -1)
	{
		perror("ERROR OPENING WRITE PIPE");
		//return -1;
	}
	//puts("Write pipe opened.");
	if(mkfifo(readFifo, 0666) != 0)
	{
		//if (errno != EEXIST)
			perror("ERROR CREATING READ PIPE");
		/*else if (errno != SUCCESS)
			puts("Read pipe is already open.");*/
		//return ret;
	}
	//puts("Read pipe created.");
	fdr = open(readFifo, O_RDONLY);
	if (fdr == -1)
	{
		perror("ERROR OPENING READ PIPE");
		//return -1;
	}
	puts("Pipes opened.");
	return 0;
}

int MosaicMaker::WriteTags(string tags) {
	int bytes = 0;
	printf("%s, %i\n", tags.c_str(), tags.size());
	if ((bytes = write(fdw, tags.c_str(), tags.size())) < 0)
	{
		perror("ERROR WRITING TAGS");
		return -1;
	}
	return 0;
}

int MosaicMaker::WriteColor(ImageColor c) {
	int bytes = 0;
	char colorBuf[11];
	sprintf(colorBuf, "%03i,%03i,%03i", c.R(), c.G(), c.B());
	printf("Sending %s\n", colorBuf);
	if ((bytes = write(fdw, colorBuf, 11 * sizeof(char))) < 0)
	{
		perror("ERROR WRITING COLOR");
		return -1;
	}
	return 0;
}

string MosaicMaker::ReadID() {
	int bytes = 0;
	char buf[16];
	memset(buf, 0, 16*sizeof(char));
	
	//printf("reading fdr = %i\n", fdr);
	if ((bytes = read(5, buf, 16)) < 0)
	{
		perror("ERROR READING ID");
		return "0";
	}
	//printf("Received ID %s\n", buf);
	string id = buf;
	return id;
}

int MosaicMaker::ClosePipe() {
	ImageColor stopColor  = ImageColor(-1, -1, -1);
	WriteColor(stopColor);
	close(fdr);
	close(fdw);
	unlink(readFifo);
	unlink(writeFifo);
	puts("Pipe closed.");
}

// ------------ Image functions ------------ //

int blocksWritten = 0, blocksAnalyzed = 0;

// identical to ImageAnalyzer::ReadImage
unsigned char** MosaicMaker::ReadImage(string _filename) {
   // printf("read %s fdr = %i\n", _filename.c_str(), fdr);
	struct jpeg_decompress_struct cinfo;
	struct jpeg_error_mgr jerr;
	readFile = _filename.c_str();	
	//pixels.clear();
	
	//printf("Opening image %s\n", readFile);
	FILE *image = fopen(readFile, "rb");
	
	if (!image)
	{
		printf("ERROR OPENING IMAGE %s\n", readFile);
		return NULL;
		//return FILE_NOT_FOUND;
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
	
	/*printf("Image info obtained for %s\n", readFile);
	printf("W %i\tH %i\tC %i\n", width, height, components);*/
	
	// start reading image	
	JSAMPROW row_pointer[1];
	unsigned char **array = new unsigned char*[height];
	for (int i = 0; i < height; i++)
	{
		array[i] = new unsigned char[width * 3];
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
			array[y][x] = row_pointer[0][x];
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
	return array;
	//return SUCCESS;
}

int MosaicMaker::BreakDown(string filename, int resLevel) {
	mainPic = ReadImage(filename);
	char resStr[4];
	filename.erase(filename.length() - 4, filename.length() - 1); 
	int mainWidth = width;
	int mainHeight = height;
	int squareSize = 0;
	if (resLevel == 1)
	{
		squareSize = mainWidth / 16;
		sprintf(resStr, "low");
	}
	else if (resLevel == 2)
	{
		squareSize = mainWidth / 32;
		sprintf(resStr, "med");
	}
	else if (resLevel == 3)
	{
		squareSize = mainWidth / 64;
		sprintf(resStr, "high");
	}
	else
	{
		squareSize = mainWidth / 32;
		sprintf(resStr, "high");
	}
	
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

	puts("Starting breakdown.");
	struct jpeg_compress_struct cinfo;
	struct jpeg_error_mgr jerr;
	FILE *out;
	sprintf(writeFile, "%s_%s.jpg", filename.c_str(), resStr);
	printf("CROPPING PICTURE %s\n", writeFile);
	JSAMPROW row_pointer[1];
	int row_stride;
	cinfo.err = jpeg_std_error(&jerr);
	jpeg_create_compress(&cinfo);
	//puts("Opening file");
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
	
	Block block;
	ImageColor c;
	int r, g, b;
	int xBlock = 0, yBlock = 0;
	int x = 0, y = 0;
	/*printf("new height %i new width %i\n", newHeight, newWidth);
	printf("height = %i, topCrop = %i, bottomCrop = %i\n", height, topCrop, bottomCrop);
	printf("width = %i, leftCrop = %i, rightCrop = %i\n", width, leftCrop, rightCrop);
	printf("what it should be (%i, %i)\n", (newWidth - rightCrop) * 3, newHeight - bottomCrop);*/
	for (y = topCrop; y < mainHeight - bottomCrop; y += squareSize)
	{
		for (x = leftCrop; x < (mainWidth - rightCrop) * 3; x += squareSize * 3)
		{
			//printf("analyzing x %i\n", x);
			// looping through squareSize
			r = 0, g = 0, b = 0;
			for (int sy = 0; sy < squareSize; sy++)
			{
				for (int sx = 0; sx < squareSize * 3; sx += 3)
				{
					//printf("y %i x %i sy %i sx %i\n", y, x, sy, sx);
					r += mainPic[y + sy][x + sx];
					g += mainPic[y+ sy][x + sx + 1];
					b += mainPic[y + sy][x + sx + 2];
				}
			}
			blocksAnalyzed++;
			r /= squareSize * squareSize;
			g /= squareSize * squareSize;
			b /= squareSize * squareSize;
			c.SetColors(r, g, b);
			//printf("xBlock %i, yBlock %i\n", xBlock, yBlock);
			//printf("block fdr = %i\n", fdr);
			block.Set(c, xBlock, yBlock);
			WriteColor(c);
			string id = ReadID();
			WriteBlock(id, block);
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
	printf("New image saved: %s\n", writeFile);
	printf("blocks analyzed: %i, blocks written: %i\n", blocksAnalyzed, blocksWritten);
	delete [] mainPic;
	delete [] newPixels;
}

void MosaicMaker::WriteBlock(string id, Block block) {
	blocksWritten++;
	string filename = "/home/kate/MosaicMasterpiece/pictures/processed/" + id + ".jpg";
	// if it's a valid ID and file exists
	if (id.compare("0") != 0 && ReadImage(filename) != NULL)
	{
		unsigned char **tinypic = ReadImage(filename);
		//printf("Writing to %i, %i\n", block.X(), block.Y());
		printf("Writing image %s\n", filename.c_str());
		for (int yy = 0; yy < 100; yy++)
		{
			//printf("writing line %i\n", y);
			for (int xx = 0; xx < 300; xx += 3)
			{
				//printf("writing y %i, x %i\n", yBlock + yy, xBlock + xx);	

				newPixels[block.Y() + yy][block.X() + xx] = tinypic[yy][xx];
				newPixels[block.Y() + yy][block.X() + xx + 1] = tinypic[yy][xx + 1];
				newPixels[block.Y() + yy][block.X() + xx + 2] = tinypic[yy][xx + 2];
			}
		}
		delete [] tinypic;
	}
	else
	{
	    puts("No image matching that ID found.");
	    //printf("Writing to %i, %i\n", block.X(), block.Y());
		for (int yy = 0; yy < 100; yy++)
		{
			//printf("writing line %i\n", y);
			for (int xx = 0; xx < 300; xx += 3)
			{
				//printf("writing y %i, x %i\n", yBlock + yy, xBlock + xx);	
				newPixels[block.Y() + yy][block.X() + xx] = block.R();
				newPixels[block.Y() + yy][block.X() + xx + 1] = block.G();
				newPixels[block.Y() + yy][block.X() + xx + 2] = block.B();
			}
		}
	}
}

int main(int argc, char *argv[]) {
	Glib::RefPtr<Gtk::Application> app =
    	Gtk::Application::create(argc, argv,
    	"org.gtkmm.examples");
	GUIWindow window;
	return app->run(window);
}

