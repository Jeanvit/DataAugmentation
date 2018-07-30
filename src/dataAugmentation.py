'''
Author: Jean Vitor de Paulo
site : www.jeanvitor.com

Script to randomly apply Geometric Transformations/Noise on an image, generating an output slightly different (or not). 
This is usually used in Machine Learning for data augmentation.
All the output images will be placed inside the 'Output images' folder by default

'''


import cv2
import numpy as np
import random
import sys
import getopt
import os

def sp_noise(image,prob):
	output = np.zeros(image.shape,np.uint8)
	thres = 1 - prob 
	for i in range(image.shape[0]):
		for j in range(image.shape[1]):
			rdn = random.random()
			if rdn < prob:
				output[i][j] = 0
			elif rdn > thres:
				output[i][j] = 255
			else:
				output[i][j] = image[i][j]
	return output

# credits of that cool bar to https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
def progress(count, total, suffix=''):
    bar_len = 25
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s %s\r' % (bar, percents, '%', suffix))
    sys.stdout.flush() 


def main(argv):
	outputSize = 0
	randomizerLevel = 20
	local = ''
	outputFolder = "Output images\\"
	borderMode =  cv2.BORDER_REPLICATE
	noiseLevel = 0.0
	try:
		opts, args = getopt.getopt(argv,"hi:o:n:r:m:w:",["ilocal=","osize=","rlevel=","output=","bmode=","nlevel"])
	except getopt.GetoptError as error:
		print (error)
		print ('image.py -i <imageName> -n <quantity> -r <randomizerLevel> -o <OutputFolder> -m <BorderMode> -w <noiseLevel>')
		sys.exit()
	for opt, arg in opts:
		if opt == '-h':
			print ("This is a script to process an image n times, randomly generating a")
			print ("processed output, based on the original image. ")
			print ("All the output images will be placed inside the 'Output images' folder by default\n")
			print ('usage: image.py -i <imageName> -n <quantity> -r <randomizerLevel> -o <OutputFolder> -m <BorderMode> -w <noiseLevel>\n')
			print ("-i : Image name")
			print ("-n : The number of output images")
			print ("-o : The output folder")
			print ("-r : The randomizer level specifies how agressively the image will be changed. Default = 20")
			print ("-m : Border mode: default=0 (cv2.BORDER_REPLICATE) use 1 to choose cv2.BORDER_CONSTANT")
			print ("-w : Noise level between 0 and 1, default=0\n")
			sys.exit()
		elif opt in ("-i", "--ilocal"):
			local = str(arg)
			img = cv2.imread(local, cv2.IMREAD_UNCHANGED)
			if img is None:
				print ("Invalid image")
				sys.exit()
		elif opt in ("-n", "--xsize"):
			outputSize = int(arg)
			if (outputSize <= 0) :
				print ("Please specify an output bigger than 0")
				sys.exit()
		elif opt in ("-r", "--rlevel"):
			randomizerLevel = int(arg)
			if (randomizerLevel == 0 or randomizerLevel == 1):
				print ("Please specify a higher randomizer level (-h for help)")
				sys.exit()
		elif opt in ("-o", "--output"):
			outputFolder = str(arg)
		elif opt in ("-m", "--bmode"):
			if (int(arg)==1):
				borderMode = cv2.BORDER_CONSTANT
		elif opt in ("-w", "--nlevel"):
			noiseLevel = float(arg)

	rows, cols, layers = img.shape
	print("\n\nGenerating ",outputSize ,"randomized images from file ", local, "in ", outputFolder, "Randomize level: ", randomizerLevel, "\n")
	if not os.path.exists(outputFolder):
		os.makedirs(outputFolder)
	for i in range(0,outputSize):
		dst = img
		randomNumber = random.randint(2,randomizerLevel)
		randomSign = 1
		if (random.randint(1,2) == 2):
			randomSign = randomSign * -1
		
		if (noiseLevel != 0.0 ):
			dst = sp_noise(dst,random.uniform(0, noiseLevel))
	
		#Rotation
		M = cv2.getRotationMatrix2D((cols/2,rows/2),randomizerLevel * randomNumber ,1)
		dst = cv2.warpAffine(dst,M,(cols,rows),borderMode=borderMode)
		
		#Translation
		M = np.float32([[random.uniform(0.6, 1),0,cols%randomNumber* randomSign] ,[0,random.uniform(0.6, 1) ,rows%randomNumber * randomSign]])
		dst = cv2.warpAffine(dst,M,(cols,rows),borderMode=borderMode)
		
		#mean = 25.0   # some constant
		#std = 1.0    # some constant (standard deviation)
		#noisy_img = dst + np.random.normal(mean, std, img.shape)
		#dst = np.clip(noisy_img, 0, 255)  # we might get out of bounds due to noise
		try:
			cv2.imwrite(''.join([outputFolder,str(i) , ".png"]),dst)
			progress(i+1,outputSize)
		except e as imwriteError:
			print ("Error while writing images: ", imwriteError)
		cv2.waitKey()
		cv2.destroyAllWindows()

if __name__ == "__main__":
	main(sys.argv[1:])
	print("\n Done!\n")
