# About

Python script that takes logo image and places it on every image in the selected directory. 

# Info about add_logo.exe

This executable was made by pyinstaller:
```
pyinstaller --onefile add_logo.py
```

To run the executable 'add_logo.exe' you need:
1) To place an image that will serve as a logo in this directory (same directory as the executable) and that image should be named 'logo'.
2) To place directory with images in this directory (same directory as the executable) and that directory should be named 'images'.

# Example of usage with arguments
Open your terminal (Command Prompt/cmd) in the directory where this program is positioned. 

Available command line arguments can be listed by running the next line in your cmd:
```
add_logo.exe -h
```
or
```
add_logo.exe --help
```

## Example of command line arguments:
```
add_logo.exe --outPath out
```
will create new images in directory named 'out', or:
```
add_logo.exe --logoOffset 400 400
```
will offset logo from the bottom right corner by 400px to the left and up