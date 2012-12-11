class ImageColor {
	int red;
	int blue;
	int green;

public:
	ImageColor() {
		red = 0;
		green = 0;
		blue = 0;	
	}
	
	ImageColor(int _red, int _green, int _blue) {
		red = _red;
		green = _green;	
		blue = _blue;
	}
	
	void SetColors(int _red, int _green, int _blue){
		red = _red;
		green = _green;	
		blue = _blue;	
	}
	
	int R() { return red; }
	int G() { return green; }
	int B() { return blue; }
	
	void Print() {
		printf("R %03i\tG %03i\tB %03i\n", red, green, blue);
	}
};
