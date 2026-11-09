# Spooky Paint Program
A spooky-scary Halloween-themed computer application that can be used for creating digital images

## Download links
* ### Windows
    x86_64 binary --> [Download here](https://github.com/DevMa7e1/SpookyPaintProgram/releases/download/v1.0.0/SpookyPaintProgram-Windows.zip)

* ### Linux
    x86_64 binary --> [Download here](https://github.com/DevMa7e1/SpookyPaintProgram/releases/download/v1.0.0/SpookyPaintProgram-Linux.zip)

## How to run the executable
### Linux
After unzipping, you will need to open a terminal, go to the location of the binary, and run the command `chmod +x SpookyPaintProgram`. Afterwards, you can run the ELF binary through the terminal or by just double-clicking it.

Please note, it might take a little while for the main window to appear.

### Windows
After unzipping the archive which contains the Windows build, you're going to have to right click and open the properties of the executable file. In the properties window, click on the checkbox next to Unblock and hit Ok. Now, you can run the software by just double-clicking the exe.

Please note, it might take a little while for the main window to appear.

## Why did I make this?
* I was curious to see if I could use the capabilities of Python and PyQt6 to make a simple paint program that followed a specific theme.

* I also wanted to see if I could make a themed paint program that uses image assets that were created using it.

## How to use this program

### 1. Creating a new drawing
To create a new drawing, press the "Create new drawing" button on the first page of the program.

### 2. Changing the brush
To change the current brush, click on the orange box that sits right below the preview of the current brush and click on the name of the brush you want to select.

### 3. Changing the size of the brush
To change the size of the brush, you can either use the small up and down arrows located in the box labeled **Brush size (px):** or enter the the size wanted in pixels directly.

### 4. Changing the color of the brush
To change the color of the brush, click on the orange button labeled **Set color** and choose the color wanted from the dialog provided by your operating system.

## How to make the executable
### Linux
1. Install all necessary tools
    
    Debian and Debian-based distros:
    * `sudo apt install git python3-full`

    Arch Linux and Arch-based distros:
    * `sudo pacman -S git python`
2. `git clone https://github.com/DevMa7e1/SpookyPaintProgram.git`
3. `cd SpookyPaintProgram`
4. `python3 -m venv venv`
5. `source venv/bin/activate` (modify for your shell)
6. `pip install -r requirements.txt`
7. `pip install pyinstaller`
8. `python3 -m PyInstaller -F -n SpookyPaintProgram main.py --add-data assets/*:./assets --noconsole`

The resulting executable can be found in the **dist** folder.

## Windows
1. Install the latest version of Python
2. [Download the source code of SpookyPaintProgram](https://github.com/DevMa7e1/SpookyPaintProgram/archive/refs/heads/main.zip)
3. Unzip it and go into the created folder
4. Open a new CMD window
5. Copy the path of the previously opened folder and run the command `cd *your path here*`
6. Run the command `python -m venv venv`
7. Run the command `venv\Scripts\activate`
8. Run the command `pip install -r requirements.txt`
9. Run the command `pip install pyinstaller`
10. Run the command `python -m PyInstaller -F -n SpookyPaintProgram --noconsole main.py --add-data assets\*:.\assets --icon assets/pumpkin.png`

The resulting executable can be found in the **dist** folder.
