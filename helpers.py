# Dependencies:
#   - Colorama

# Operating System Dependencies:
#   - sys 
#   - time 
#   - os 
#   - platform 
#   - ctypes 

from colorama import Fore, Style, Back, init
import platform
import ctypes
import sys
import time
import os

# Color Print Function
# Description:
# - Allows printing with the ability to customize the back color and the text color.

def cPrint(string, textColor, backColor='black'):
    colorText = getattr(Fore, textColor.upper())
    backText = getattr(Back, backColor.upper())
    print(colorText + backText + string + Style.RESET_ALL)

# Print Spacer + Partial Color Print
# Description:
# - Prints a spacer above the message being printed, allows the user to overide the color as well.

def printSpacer(string, textColor='white'):
    colorText = getattr(Fore, textColor.upper())
    print('')
    print(colorText + string + Style.RESET_ALL)
    
# Slow Print
# Description:
# - Prints text slowly at a set delay

def slowPrint(text, delay):
    for character in text:
        sys.stdout.write(character)
        sys.stdout.flush() # Forces the output to be written immediately
        time.sleep(delay) # Adjust the delay here

# Clear Terminal
# Description:
# - Clears the terminal based on the operating system type

def clearTerm():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')


# Full Screen Terminal
# Descrption:
# - Fullscreen's the terminal being used
# WARNING:
# - This script talks to the Windows kernel! There may be instability running this script

def fullscreenTerm():
    if platform.system() == 'Windows':
        kernel32 = ctypes.WinDLL('kernel32')
        user32 = ctypes.WinDLL('user32')
        SW_MAXIMIZE = 3
        hWnd = kernel32.GetConsoleWindow()
        user32.ShowWindow(hWnd, SW_MAXIMIZE)
    else:
        print('Automatic Fullscreen is not supported on this system!')
        print('It is recommended to fullscreen the window yourself')
        time.sleep(5)