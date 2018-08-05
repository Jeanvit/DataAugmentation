# About

Script to randomly apply Geometric Transformations/Noise on an image, generating an output slightly different (or not). 
This is usually used in Machine Learning for data augmentation.

# Requeriments

- Python
- OpenCV
- numpy


# Usage


`dataAugmentation.py -i <imageName> -n <quantity> -r <randomizerLevel> -o <OutputFolder> -m <BorderMode> -w <noiseLevel> `

### Parameters

- `-i` : Image name

- `-n` : The number of output images

- `-o` : The output folder

- `-r` : The randomizer level specifies how aggressively the image will be changed. Default = 20

- `-m` : Border mode: default=0 (cv2.BORDER_REPLICATE) use 1 to choose cv2.BORDER_CONSTANT

- `-w` : Noise level between 0 and 1, default=0

- `-h` : help