import os, sys
from os.path import join as oj
import girder_client


### You need to change this depending on where you want to store the rawImage Data
imageFolderOnLocalMachine = "/home/dagutman/devel/KerasSimpsons_Tensorflow/rawImageData/"
imageFolderUID = '5b0ebfab92ca9a001733549d'

if not os.path.isdir(imageFolderOnLocalMachine):
	os.makedirs(imageFolderOnLocalMachine)

##import DSACBIRHelperFunctions as DSACBIR

class LinePrinter():
    """
    Print things to stdout on one line dynamically
    """
    def __init__(self,data):
        sys.stdout.write("\r\x1b[K"+data.__str__())
        sys.stdout.flush()


gc = girder_client.GirderClient(apiUrl='http://candygram.neurology.emory.edu:8080/api/v1')


### Get a list of all the image folders on the DSA Server
imageFoldersOnDSAServer = list([x['name'] for x in gc.listFolder(imageFolderUID)])


for char in imageFoldersOnDSAServer:
	print "Syncing data for %s" % char
	localFolderForChar = os.path.join(imageFolderOnLocalMachine,char)

	if not os.path.isdir(localFolderForChar):
		os.makedirs(localFolderForChar)


### Go through the image folders on the DSA Server and see how many images are in each folder and if all the
### local images are available/uploaded
## This determines which images are already uploaded to Girder, and in the next block I check if it's uploaded


GirderImageInfoDict = {}
imagesProcessed = imagesDownloaded = 0

for cf in gc.listFolder(imageFolderUID):  ## cf = characterFolder
    characterImages = list( gc.listItem(cf['_id']))
    print "There are a total of %d items for %s" % (len(characterImages), cf['name'])
    GirderImageInfoDict[cf['name']] = { 'girderFolderID': cf['_id'],'numItems': len(characterImages), 'imageItemData': characterImages,
                                      'imageItemNames' : [x['name'] for x in characterImages]
                                      }
  
    ## Check each image item for appropriate tags.. i.e. characterClass and largeItem
    if len(characterImages) > 0:
        localFolderForChar = os.path.join(imageFolderOnLocalMachine,char)

        for itm in characterImages:
            imagesProcessed +=1
            ### Check and see if the image has already been downloaded

            imageNameWPath = os.path.join(localFolderForChar, itm['name'])
            if not os.path.isfile( imageNameWPath):
            	### I first need to get the list of files uassociatd with the item, and download the first one
            	filesForItem = list(gc.listFile(itm['_id']))

            	gc.downloadFile(filesForItem[0]['_id'],imageNameWPath)
            	imagesDownloaded+=1
            LinePrinter("A total of %d images have been processed, and %d have been just Downloaded" % (imagesProcessed, imagesDownloaded))
    print ### Adds a linefeed between each character folder

    ### I am also going to iterate through each item in Girder, and make sure it has a largeImageTag
    ## And also has characterClass associated with each Item..
    #meta.charClass = charactername
    


    
#foldersOnLocalMachine = os.listdir(imageFolderOnLocalMachine)
## If I have a folder on my local machine but it's not on the DSA server I need to create it
#for f in foldersOnLocalMachine:
#    if f not in imageFoldersOnDSAServer:
#        print "Creating folder %s on the DSA Server " % f
#        gc.createFolder(imageFolderUID,f,reuseExisting=True)
