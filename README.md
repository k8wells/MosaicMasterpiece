MosaicMasterpiece
=================
Minute Mosaic Masterpiece - make a photomosaic using Flickr images!

DEPENDENCIES
================
All instructions for installing on Linux systems; apologies to Windows users.
*Python 2.7*

*Pip:*
sudo apt-get install pip

*libjpeg:*
sudo apt-get install libjpeg8 libjpeg8-dev

*pygame:*
sudo apt-get install python-pygame

*ujson:*
sudo pip install ujson

*flickrapi:*
sudo pip install flickrapi

*elementtree:*
sudo pip install elementtree

*numpy:*
sudo pip install numpy

*stemming:*
sudo pip install stemming

HOW TO RUN
================
KHITTYKRAWLER.PY
----------------
For crawling Flickr to obtain pictures. Must replace APIKEY and APISECRET with your own key and secret.

*RUN:*
python khittykrawler.py

This will take a long time and lots of storage space.

IMAGE PROCESSING
----------------
Requires files BatchProcess.cpp, ImageAnalysis.cpp, ImageAnalysis.h

*COMPILE:* 
g++ -o batch BatchProcess.cpp ImageAnalysis.cpp -ljpeg -fpermissive

*RUN:*
./batch

Pictures to analyze should be in ./pictures; output will be placed in ./pictures/processed. You must create processed before running ./batch.

Output is colordata.json, cropped/resized images in ./pictures/processed.

SCORING.PY
----------------
Demonstrates the algorithm for determining the closest color to query color

You must have pygame installed to view this demo

*RUN:*
python scoring.py colordata.json

You will see a textbox looking graphic along with rows of circles of colors given in the data.

Using the numbers about QWERTY (keypad will not register), enter a RGB value in this format:
123,123,123
Include the commas and enter a correct RGB value or the program will crash. You can use the backspace to clear the box.
Then press Enter

You will see a circle of the color you entered appear to the right of the textbox and the closest color in the data will be have a white circle drawn around it.

You can continue to query different colors by deleting your previous RGB value, entering another, and hitting Enter again.

Press ESC to exit the application


CLUSTER3.PY
----------------
Analyzes the tags of all the pictures and arranges them into corresponding hierarchical clusters

You must have numpy installed
These file must also be included:
tfidf.py
cluster3.py
cluster_tests.py
datasample.json

*RUN:*
nosetests.py -s

This test file consists of 5 different tests.
The first two make sure that similar values are grouped into the same cluster.
the third test shows that the algorithm starts out with every picture being in its own cluster
the fourth test demonstrates that at the end of the algorithm there are only two main clusters.
the last test proves that every picture is included in a cluster

