import argparse
import os
from PIL import Image 

"""
Python program for placing a logo on every image in 'images' directory.
@author: Luka Šulc
"""
def parseInput():
    parser = argparse.ArgumentParser(description='Takes logo image and places it on every image in the selected directory.')
    parser.add_argument('--logoName', default='logo', type=str,
                        help='name of the logo file')
    parser.add_argument('--logoDim', nargs='+', default=[15, 15], type=int,
                        help='two numbers which represent percentages of the size of the original image, \
                            ex. original_image_width*first_number/100 = logo_width, \
                                original_image_height*second_number/100 = logo_height, must be separated by space')
    parser.add_argument('--logoOffset', nargs='+', default=[40, 40], type=int,
                        help='logo offset, must be separated by space')
    # parser.add_argument('--logoCustom', nargs='+',
    #                     help='logo custom coordinates, must be separated by space')
    parser.add_argument('--imagesPath', default='./images', type=str,
                        help='path to the directory/folder which contains \
                            images on which the logo will be applied')
    parser.add_argument('--imagesDim', nargs='+', default=[2592, 1728], type=int,
                        help='dimensions of output images, default width=2592|height=1728')
    parser.add_argument('--outPath', default='./images_logo', type=str,
                        help='name of the logo file')
    parser.add_argument('--verbose', default=True, action=argparse.BooleanOptionalAction,
                        help='prints out additional information, can affect performance')
                        
    return parser, parser.parse_args()

def checkBeforeExecution(args: argparse.Namespace):

    logoPath = None
    prefixed = []
    for filename in os.listdir(os.getcwd()):
        if not filename.split('.')[0] == (args.logoName):
            continue
        logoPath = os.path.join(os.getcwd(),filename)
        if os.path.isfile(logoPath):
            prefixed.append(filename)

    if len(prefixed) == 0:
        raise Exception("Current directory doesn't contain a file that starts with default name 'logo'. Change logo filename to 'logo' or run program with --logoName flag.")
    elif len(prefixed) > 1:
        raise Exception("Current directory contains multiple files that starts with default name 'logo'. Change logo filename to 'logo', delete access files named 'logo' or run program with --logoName flag.")

    imagesPath = os.path.join(os.getcwd(), args.imagesPath.split('./')[1]) if args.imagesPath.startswith('./') else args.imagesPath
    if not os.path.isdir(imagesPath):
        raise Exception("Current directory doesn't contain a directory that starts with default name 'images'. Place directory that contains images to the current directory and name it 'images' or run program with --imagesPath flag.")
    
    outPathPath = os.path.join(os.getcwd(), args.outPath.split('./')[1]) if args.outPath.startswith('./') else args.outPath
    if os.path.isdir(outPathPath) and len(os.listdir(outPathPath)) != 0:
        if input(f"Directory '{outPathPath}' is not empty. You could potentially override some or all files. Are you sure you want to do that? (y/n)") != 'y':
            raise Exception("Current directory is not empty. User decided not to override!")
 
    return logoPath, imagesPath

def getImage(path, dimension=None):
    img = Image.open(path)
    if dimension:
        img = img.resize(dimension)
    return img

def applylogo(logoPath, imagesPath, args: argparse.Namespace):
    outPath = args.outPath
    if outPath.startswith('./'):
        outPath = os.path.join(os.getcwd(), outPath.split('./')[1])
    if not os.path.isdir(outPath):
        os.mkdir(outPath)
    
    list_of_images = os.listdir(imagesPath)
    for i, filename in enumerate(list_of_images):
        i += 1
        if args.verbose:
            print(f"Processing image {i} out of {len(list_of_images)}...")
        image = getImage(os.path.join(imagesPath, filename), args.imagesDim)
        logo = getImage(logoPath, (int(image.width*args.logoDim[0]/100), int(image.height*args.logoDim[1]/100)))
        image.paste(logo, (image.width - logo.width - args.logoOffset[0], image.height - logo.height - args.logoOffset[1]), logo)
        image.save(os.path.join(outPath, filename))
    print('Processed all images!')

def main():
    _, args = parseInput()
    paths = checkBeforeExecution(args)
    applylogo(*paths, args)

if __name__ == "__main__":
    task_state = 'UNDEFINED'
    try:
        main()
        task_state = 'SUCCEDED'
    except Exception as m:
        print(m)
        task_state = 'FAILED'
    input(f'TASK {task_state}... press any key to exit')
    