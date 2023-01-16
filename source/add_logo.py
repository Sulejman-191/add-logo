import argparse
import os
from PIL import Image 

"""
Python program for placing a logo on every image in 'images' directory.
@author: Luka Šulc
"""
def parseInput():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--logoName', default='logo',
                        help='name of the logo file')
    parser.add_argument('--logoDim', nargs='+', default=[70, 50],
                        help='dimension of the logo file, must be separated by space')
    parser.add_argument('--logoOffset', nargs='+', default=[40, 40],
                        help='logo offset  , must be separated by space')
    # parser.add_argument('--logoCustom', nargs='+',
    #                     help='logo custom coordinates, must be separated by space')
    parser.add_argument('--imagesPath', default='./images',
                        help='path to the directory/folder which contains \
                            images on which the logo will be applied')
    parser.add_argument('--outDir', default='./images_logo',
                        help='name of the logo file')
    parser.add_argument('--verbose', default=False,
                        help='prints out additional information, can affect performance')
    return parser, parser.parse_args()

def checkBeforeExecution(args: argparse.Namespace):
    prefixed = [filename for filename in os.listdir('.') if (filename.startswith(args.logoName) and os.path.isfile(filename))]
    if len(prefixed) == 0:
        raise Exception("Current directory doesn't contain a file that starts with default name 'logo'. Change logo filename to 'logo' or run program with --logoName flag.")
    elif len(prefixed) > 1:
        raise Exception("Current directory contains multiple files that starts with default name 'logo'. Change logo filename to 'logo', delete access files named 'logo' or run program with --logoName flag.")
    
    imagesPath = os.path.join(os.getcwd(), args.imagesPath.split('./')[1]) if args.imagesPath.startswith('./') else args.imagesPath
    if not os.path.isdir(imagesPath):
        raise Exception("Current directory doesn't contain a directory that starts with default name 'images'. Place directory that contains images to the current directory and name it 'images' or run program with --imagesPath flag.")
    
    outDirPath = os.path.join(os.getcwd(), args.outDir.split('./')[1]) if args.outDir.startswith('./') else args.outDir
    if os.path.isdir(outDirPath) and len(os.listdir(outDirPath)) != 0:
        if input(f"Directory '{outDirPath}' is not empty. You could potentially override some or all files. Are you sure you want to do that?") != 'y':
            raise Exception("Current directory is not empty. User decided not to override!")
 
    logoPath = os.path.join(os.getcwd(), prefixed[0])
    return logoPath, imagesPath

def applylogo(logoPath, imagesPath, args: argparse.Namespace):
    logo = Image.open(logoPath)
    logo = logo.resize(args.logoDim)
    logoWidth = logo.width
    logoHeight = logo.height
    outPath = args.outDir
    if args.outDir.startswith('./'):
        outPath = os.path.join(os.getcwd(), args.outDir.split('./')[1])
    if not os.path.isdir(outPath):
        os.mkdir(outPath)

    list_of_images = os.listdir(imagesPath)
    for i, filename in enumerate(list_of_images):
        i += 1
        if args.verbose:
            print(f"Processing image {i} out of {len(list_of_images)}...")
        image = Image.open(os.path.join(imagesPath, filename))
        imageWidth = image.width
        imageHeight = image.height
        image.paste(logo, (imageWidth - logoWidth - args.logoOffset[0], imageHeight - logoHeight - args.logoOffset[1]), logo)
        image.save(os.path.join(outPath, filename))
    print('Processed all images!')

def main():
    parser, args = parseInput()
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
    