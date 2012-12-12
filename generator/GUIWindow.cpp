#include "MosaicMaker.h"

GUIWindow::GUIWindow() : bigbox(Gtk::ORIENTATION_VERTICAL, 15),
	filebox(Gtk::ORIENTATION_HORIZONTAL, 5),
	sizebox(Gtk::ORIENTATION_VERTICAL, 5)
{
	resLevel = 3;
	set_border_width(10);
	bigbox.set_homogeneous(false);
	filebox.set_homogeneous(false);
	set_size_request(400, 600);
	set_title("Mosaic Masterpiece");
	add(bigbox);
	filename.set_max_length(300);
	filename.set_text("Pick an image...");
	tags.set_text("Tags...");
	tags.set_max_length(300);
	browse.set_label("Browse...");
	close.set_label("Close");
	run.set_label("RUN!");
	
	low.set_label("Low");
	med.set_label("Medium");
	high.set_label("High");
	
	sizegroup = low.get_group();
	med.set_group(sizegroup);
	high.set_group(sizegroup);
	high.set_active(true);
	
	run.signal_clicked().connect(sigc::mem_fun(*this, &GUIWindow::OnRun));
	close.signal_clicked().connect(sigc::mem_fun(*this, &GUIWindow::OnClose));
	low.signal_clicked().connect(sigc::mem_fun(*this, &GUIWindow::LowRes));
	med.signal_clicked().connect(sigc::mem_fun(*this, &GUIWindow::MedRes));
	high.signal_clicked().connect(sigc::mem_fun(*this, &GUIWindow::HighRes));
	
	status.set_label("Waiting for a picture...");
	
	//filebox.pack_start(filename);
	//filebox.pack_start(run);
	
	sizebox.pack_start(low);
	sizebox.pack_start(med);
	sizebox.pack_start(high);
	
	bigbox.pack_start(status);
	bigbox.pack_start(filename);
	bigbox.pack_start(browse);
	bigbox.pack_start(sizebox);
	bigbox.pack_start(tags);
	bigbox.pack_start(run);
	bigbox.pack_start(close);
	show_all_children();
	
	mm.OpenPipe();
}

void GUIWindow::OnRun() {
	string file = (string) filename.get_text();
	string tagStr = (string) tags.get_text();
	status.set_label(file);
	if (tagStr.compare("Tags..."))
		mm.WriteTags("");
	else	
		mm.WriteTags(tagStr);
	mm.BreakDown(file, resLevel);
}

void GUIWindow::OnClose() {
	mm.ClosePipe();
	hide();
}

void GUIWindow::LowRes() {
	resLevel = 1;
}

void GUIWindow::MedRes() {
	resLevel = 2;
}

void GUIWindow::HighRes() {
	resLevel = 3;
}
