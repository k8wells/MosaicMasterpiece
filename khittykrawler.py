#November 2012
#Khitty Krawler
#Crawling Flickr
#The key and secret provided here are made under my name, Mary Thompson TAMU CSCE c/o 2012

import flickrapi
import elementtree
import urllib,urlparse
import os
import sys
import ujson

api_key = '203dfff102ee6fdc621efdf1bffcc666'
api_secret = '2ac117e2bdb82cb8'

flickr = flickrapi.FlickrAPI(api_key)
interesting_photos = flickr.interestingness_getList(per_page = "500", extras = "description, tags, machine_tags, url_z")
owners = []
user_photos = []

def getting_info():
    
    photo_info = []  
    for info in interesting_photos.iter():
	if info.get('title'):
	    owners.append(info.get('owner'))
    
    	    #The only photo info we're interested in
	    doc = dict(
	        title = info.get('title'),
	        desc = info.get('description'),
	        tags = info.get('tags'),
	        mtags = info.get('machine_tags'),
	        filename = info.get('id')+"_"+info.get('secret')+"_z.jpg"
	    )	
	    photo_info.append(doc)
    
    
    if owners:
    	#Getting photos from owners of interesting photos	
	
	#var = 200	#testing: pulling photos from 200 interesting photo owners
	for user in owners:
            user_photos = flickr.people_getPublicPhotos(per_page="500",user_id=user, extras = "description, tags, machine_tags, url_z")
	    #var -= 1
            #if var == 0:
		#break
	    
            
	    for info in user_photos.iter():
		if info.get('title'):
	    	    #The only photo info we're interested in
		    doc = dict(
			title = info.get('title'),
			desc = info.get('description'),
			tags = info.get('tags'),
			mtags = info.get('machine_tags'),
			filename = info.get('id')+"_"+info.get('secret')+"_z.jpg"
		    )	
		    photo_info.append(doc)   

    
    print "saving photo info"
    #print "Number of photos:",len(photo_info)
    photo_file = open("photo_info.json","w")
    for info in photo_info:
    	photo_file.write(ujson.dumps(info) + '\n')
    photo_file.write("Number of photos: "+str(len(photo_info)))
    #photo_file.write(user_photos)
    photo_file.close()

def download_images():

    photourl = []
    for photo in interesting_photos.iter():
        if photo.get('url_z') != None:
	    photourl.append(photo.get('url_z'))
    for photo in user_photos:
        if photo.get('url_z') != None:
	    photourl.append(photo.get('url_z'))

    for url in photourl:
	print 'downloading:', url
        image = urllib.URLopener()
        image.retrieve(url, os.path.basename(urlparse.urlparse(url).path)) 
        

def main():

    getting_info()
    #download_images()


if __name__=="__main__":
    main()
