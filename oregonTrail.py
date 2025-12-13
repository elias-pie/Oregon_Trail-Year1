# helpers.py
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




# oregonTrail.py

#from helpers import *  #Details Above
from colorama import Fore, Style, Back, init
import platform
from random import randint
import os
import datetime

DEBUG = True #Shows more data to the player, for debuging purposes # Also allows for debug commands to be used
INSTANT_COMPLETION = False # Sets miles to 1999, for debuging purposes
INSTANT_FAILURE = False # Sets days to 304, for debuging purposes
FORCE_RIVER = False #Forces river as an event every time, for debuging purposes
FORCE_DISEASE = False #Used to force a disease on the players, for debuging purposes

if INSTANT_COMPLETION == True and INSTANT_FAILURE == True:
    print('DEBUGGING SETTINGS INCOMPATIBLE! PLEASE OVERWRITE')
    quit()

firstRun = True

restedCancel = False

clearTerm()
#fullscreenTerm()

skullAscii = '''
                 uuuuuuu
             uu$$$$$$$$$$$uu
          uu$$$$$$$$$$$$$$$$$uu
         u$$$$$$$$$$$$$$$$$$$$$u
        u$$$$$$$$$$$$$$$$$$$$$$$u
       u$$$$$$$$$$$$$$$$$$$$$$$$$u
       u$$$$$$$$$$$$$$$$$$$$$$$$$u
       u$$$$$$"   "$$$"   "$$$$$$u
       "$$$$"      u$u       $$$$"
        $$$u       u$u       u$$$
        $$$u      u$$$u      u$$$
         "$$$$uu$$$   $$$uu$$$$"
          "$$$$$$$"   "$$$$$$$"
            u$$$$$$$u$$$$$$$u
             u$"$"$"$"$"$"$u
  uuu        $$u$ $ $ $ $u$$       uuu
 u$$$$        $$$$$u$u$u$$$       u$$$$
  $$$$$uu      "$$$$$$$$$"     uu$$$$$$
u$$$$$$$$$$$uu    """""    uuuu$$$$$$$$$$
$$$$"""$$$$$$$$$$uuu   uu$$$$$$$$$"""$$$"
 """      ""$$$$$$$$$$$uu ""$"""
           uuuu ""$$$$$$$$$$uuu
  u$$$uuu$$$$$$$$$uu ""$$$$$$$$$$$uuu$$$
  $$$$$$$$$$""""           ""$$$$$$$$$$$"
   "$$$$$"                      ""$$$$""
     $$$"                         $$$$"
     '''

townAsciiArt = """
  ~         ~~          __
       _T      .,,.    ~--~ ^^
 ^^   // \\                    ~
      ][O]    ^^      ,-~ ~
   /''-I_I         _II____
__/_  /   \\ ______/ ''   /'\\_,__
  | II--'''' \\,--:--..,_/,.-{ },
; '/__\\,.--';|   |[] .-.| O{ _ }
:' |  | []  -|   ''--:.;[,.'\\,/
'  |[]|,.--'' '',   ''-,.    |
  ..    ..-''    ;       ''. ' 
"""


riverAsciiArt ="""
                  _.._
   _________....-~    ~-.______
~~~                            ~~~~-----...___________..--------
                                           |   |     |
                                           | |   |  ||
                                           |  |  |   |
                                           |'. .' .`.|
___________________________________________|0oOO0oO0o|____________
 -          -         -       -      -    / '  '. ` ` \\    -    -
      --                  --       --   /    '  . `   ` \\    --
---            ---          ---       /  '                \\ ---
     ----               ----        /       ' ' .    ` `    \\  ----
-----         -----         ----- /   '   '        `      `   \\
     .-~~-.          ------     /          '    . `     `    `  \\
    (_^..^_)-------           /  '    '      '      `
Lester||||AMC       --------/     '     '   '
"""

# Make system so health is fair at 80%
# Health = Poor when 50%
# Health = VERY POOR 25%
# Dead at 10% (Random chance of dying based on percentage (as a full number so if at 10%, it's a 1/10 chance you die everyday))
# Health can be increased by incrasing stats
# If a person gets 1 disease. It will decrease health by 3% every day instead of 1%

def printSpacer(num):
    loop = 1
    while loop <= num:
        print('')
        loop += 1

def enterToContinue():
    input('Press Enter to continue...')

trailer = { 
    'personSpots': {
    },
    'trailerSupplies' : {
        'food': 500, # Pounds of food
    },
    'stats': {
        'distanceTraveled': 0,
        'daysTraveled': 0,
        'money': 500  # Unused (for now)
    },
    'requirements': {
        'distanceTraveled': 2000,
        'daysTraveled': 305
    },
    'data': {
        'paceType': 1,  # 1 = Regular (around 10 hours a day) 2 = faster (around 13 hours a day) 3 = MUY RAPIDO (around 16 hours a day)
        'consumptionType': 1
    }
}

validConditionTypes = ['Measles', 'Cholera', 'Typhoid', 'Small Pox', 'Fever', 'Dysentery', 'Food posioning']

def asciiArt():
    asciiArt = '''    
################################################################################################################################
################################################################################################################################

     _____                              _____         _ _       \033[31m  (                                                            \033[0m
    |  _  |                            |_   _|       (_) |      \033[31m  )\ )                         (            )                  \033[0m
    | | | |_ __ ___  __ _  ___  _ __     | |_ __ __ _ _| |      \033[31m (()/(    )  (           (     )\ )  (   ( /( (                \033[0m
    | | | | '__/ _ \/ _` |/ _ \| '_ \    | | '__/ _` | | |      \033[31m  /(_))( /(  )\   (      )\   (()/(  )\  )\()))\   (    (      \033[0m
    \ \_/ / | |  __/ (_| | (_) | | | |   | | | | (_| | | |      \033[31m (_))  )(_))((_)  )\ )  ((_)   ((_))((_)(_))/((_)  )\   )\ )   \033[0m
     \___/|_|  \___|\__, |\___/|_| |_|   \_/_|  \__,_|_|_|      \033[31m | _ \((_)_  (_) _(_/(  | __|  _| |  (_)| |_  (_) ((_) _(_/(   \033[0m
                     __/ |                                     \033[31m  |  _// _` | | || ' \)) | _| / _` |  | ||  _| | |/ _ \| ' \)) \033[0m
                    |___/                                      \033[31m  |_|  \__,_| |_||_||_|  |___|\__,_|  |_| \__| |_|\___/|_||_|  \033[0m
    \033[0m
    
################################################################################################################################
################################################################################################################################
'''
    print(asciiArt)

# Debug :)
def debugConsole(trailer):
    command = input('\033[31mPlease Type a command: ')
    if command == 'SET_HEALTH':
        personToOverwrite = int(input('Person to overwrite (use 1,2, etc.): '))
        setHealth = input('Overwrite with?: ')
        trailer['personSpots'][personToOverwrite]['health'] = float(setHealth)
    if command == 'SET_HUNGER':
        personToOverwrite = int(input('Person to overwrite (use 1,2, etc.): '))
        setHunger = input('Overwrite with?: ')
        trailer['personSpots'][personToOverwrite]['hunger'] = float(setHunger)
    if command == 'SET_REST':
        personToOverwrite = int(input('Person to overwrite (use 1,2, etc.): '))
        setRest = input('Overwrite with?: ')
        trailer['personSpots'][personToOverwrite]['rest'] = float(setRest)
    if command == 'FOOD_AMOUNT_OVERIDE':
        setFoodAmount = input('Overwrite with?: ')
        trailer['trailerSupplies']['food'] = int(setFoodAmount)
    print('\033[0m')


def menu():
    printSpacer(2)
    print('What would you like to do?: ')
    print('#############################')
    print('1) Travel The Trail')
    print('2) Rest for certain amount of days')
    print('3) Hunt for food')
    print('4) Stats')
    print('5) Change Rations')
    print('6) Change Pace')
    action = input('Type Here: ')

    if action == 'DEBUG' and DEBUG == True:
        debugConsole(trailer)

    return action

def rationsChangeAction():
    print('#################################')
    print('What would you like to change your rations to?')
    print('1) Normal - Best for Health Longevity')
    print('2) Execcssive - Best for Keeping Health Stable')
    print('3) Barebones - Best for low food')
    userResponse = str(input('Type Here: '))
    if userResponse == '1':
        trailer['data']['consumptionType'] = 1
    elif userResponse == '2':
        trailer['data']['consumptionType'] = 2
    elif userResponse == '3':
        trailer['data']['consumptionType'] = 3
    else:
        trailer['data']['consumptionType'] = 1

def paceChangeAction():
    print('#################################')
    print('What would you like to change your rations to?')
    print('1) Normal - Best for Health Longevity')
    print('2) Longer Hours - Best for speed - Not that Healthy')
    print('3) Longest Hours - Best if your running out of time - Least Healthy')
    userResponse = str(input('Type Here: '))
    if userResponse == '1':
        trailer['data']['paceType'] = 1
    elif userResponse == '2':
        trailer['data']['paceType'] = 2
    elif userResponse == '3':
        trailer['data']['paceType'] = 3
    else:
        trailer['data']['paceType'] = 1

def dailyChecks(trailer): 
    if trailer['stats']['daysTraveled'] >= trailer['requirements']['daysTraveled']:
        detailsAction(trailer, False, False)
        printSpacer(3)
        print('\033[33mUnfortunatly, Its December 31st, meaning the harsh winter is here. You and your squad have perished!\033[0m')
        print(skullAscii)
        quit()
    if trailer['stats']['distanceTraveled'] >= trailer['requirements']['distanceTraveled']:
        detailsAction(trailer, False, False)
        printSpacer(3)
        print('\033[33mAs you start to cross the hill, you see it. Oregon! Congratulations, You and your squad arrived to Oregon with someone alive to tell the tales!\033[0m')
        print(townAsciiArt)
        quit()
    if trailer['personSpots'][1]['dead'] == True:
        printSpacer(3)
        print('The Wagon Leader has died! Your wagon leader is the only one who can operate the wagon!')
        printSpacer(3)
        detailsAction(trailer, clear=False)
        printSpacer(3)
        quit()
    for person in trailer['personSpots']:
        if trailer['personSpots'][person]['health'] <= 0.1:
            chanceOfDeath = randint(1,3)
            if chanceOfDeath == 1:
                trailer['personSpots'][person]['dead'] = True
                print(trailer['personSpots'][person]['name'] + ' Has Died!')
        if trailer['personSpots'][person]['health'] <= 0.0:
                trailer['personSpots'][person]['dead'] = True
                print(trailer['personSpots'][person]['name'] + ' Has Died!')
        if trailer['personSpots'][person]['hunger'] <= 0.0:
                trailer['personSpots'][person]['dead'] = True
                print(trailer['personSpots'][person]['name'] + ' Has Died!')
        if trailer['personSpots'][person]['rest'] <= 0.0:
                trailer['personSpots'][person]['dead'] = True
                print(trailer['personSpots'][person]['name'] + ' Has Died!')

def events(trailer, cancel=False):
    if cancel == False:
        event = randint(20, 50)
        if FORCE_RIVER == True:
            event = 37
        if event == 37:
            print(riverAsciiArt)
            # River Event
            print('You Reached a river!')
            print('What do you want to do?')
            print('* Cross the River (1)')
            print('* Go Around the River (2)')
            printSpacer(2)
            solution = str(input('Type Here: '))
            if solution == '1':
                solutionTwo = randint(0, 2)
                if solutionTwo == 0:
                    print('You crossed the river using your raft')
                    print('It took you 1 day')
                    trailer['stats']['daysTraveled'] += 2
                    trailer['stats']['distanceTraveled'] += 20
                if solutionTwo == 1 or solutionTwo == 2:
                    print('You failed to cross the river using your raft')
                    print('Lost 3 Days')
                    print('Your Crew got injured along the way')
                    trailer['stats']['daysTraveled'] += 3
                    for person in trailer['personSpots']:
                        trailer['personSpots'][person]['health'] -= (randint(3,7) / 100)
            else:
                randChance = randint(1, 3)
                if randChance == 2:
                    print('You got lost going around the river. lost 20 days')
                    trailer['stats']['daysTraveled'] += 20
                else:
                    print('You went around the river, lost 3 days')
                    trailer['stats']['daysTraveled'] += 3
            print('')
            enterToContinue()
        
def detailsAction(trailer, clear=True, enter=True):
    if clear == True:
        clearTerm()
    print('##################################################')
    print('Distance Traveled: ' + str(trailer['stats']['distanceTraveled']))
    print('Miles left: ' + str(trailer['requirements']['distanceTraveled'] - trailer['stats']['distanceTraveled']))
    print('Days Traveled: ' + str(trailer['stats']['daysTraveled']))
    print('Days Left: ' + str(trailer['requirements']['daysTraveled'] - trailer['stats']['daysTraveled']))
    print('Food: ' + str(trailer['trailerSupplies']['food']), 'Pounds of food')
    print('##################################################')

    printSpacer(2)
    for person in trailer['personSpots']:
        if trailer['personSpots'][person]['dead'] == False:
            print(trailer['personSpots'][person]['name'],':')
            print('##################################################')
            print('Health: ' + str(trailer['personSpots'][person]['health'] * 100) + '%')
            print('Conditions: ' + str(trailer['personSpots'][person]['conditionTypes']))
            print('##################################################')
            if 2 in trailer['personSpots']:
                printSpacer(2)
    if enter == True:
        enterToContinue()


def quitAction():
    verify = input('Are you sure (y/N): ')
    if verify == 'y':
        detailsAction(trailer)
        sys.quit()

def restAction(trailer):
    dayAmount = randint(1,3)
    trailer['stats']['daysTraveled'] += dayAmount
    for person in trailer['personSpots']:
        if trailer['personSpots'][person]['dead'] == False:
            if trailer['personSpots'][person]['rest'] < 1.00:
                trailer['personSpots'][person]['rest'] += 0.1
                if trailer['personSpots'][person]['rest'] > 1.0:
                    trailer['personSpots'][person]['rest'] = 1
                trailer['personSpots'][person]['hunger'] == 1
                trailer['trailerSupplies']['food'] -= 16
            cureDiesases = randint(0,1)
            if cureDiesases == 1 and trailer['personSpots'][person]['conditionTypes'] != '':
                if len(trailer['personSpots'][person]['conditionTypes']) != 0:
                    trailer['personSpots'][person]['conditionTypes'].pop(0)
    print('\nYou Rested for', dayAmount, 'days!')

    if randint(0, 2) == 1:
        lostFood = randint(0, 100)
        print('Unforuntunalty, you were robbed for',lostFood,'pounds of food')
        trailer['trailerSupplies']['food'] -= lostFood
    enterToContinue()

def getPersonsAtStart(trailer):
    loop = 1
    while loop <= 5:
        print("You must have one person! You don't have to enter a name after that")
        activePerson = input('What is the name of adventurer #' + str(loop) + '?: ')
        if activePerson != '':
            trailer['personSpots'][loop] = {
            'name': activePerson,
            'health': 1.00, # Health %, higher is better
            'hunger': 1.00, # Hunger %, higher = more hungry
            'rest': 1.00, # rest %, lower = less energy
            'conditionTypes': [], 
            'dead': False
        }  
        if loop == 1 and activePerson == '':
            printSpacer(2)
            print('You need alteast one person to join your ride!')
            quit()
        printSpacer(2)
        loop += 1

def huntAction(trailer):
    input('When you hit enter.. the you will have to shoot under 1 second at random points, miss a shot, you loose possible food!')
    sucesses = 0
    injuries = 0
    additionAmount = 0
    fullAmount = 0
    amountOfRandomHunts = randint(1,4)
    loop = 1
    while loop <= amountOfRandomHunts:
        time.sleep(randint(0,5))
        startTime =  datetime.datetime.now()
        input('\033[33mPRESS ENTER NOW!!! (SHOOT)\033[00m')
        endTime = datetime.datetime.now()
        difference = (endTime) - (startTime)
        difference = int(difference.microseconds / 1000)
        if difference < 1000:
            sucesses += 1
        loop += 1
    loop = 1
    while loop <= sucesses:
        additionAmount = randint(20,50)
        trailer['trailerSupplies']['food'] += additionAmount
        fullAmount += additionAmount
        loop += 1
    for person in trailer['personSpots']:
        if trailer['personSpots'][person]['dead'] == False:
            if randint(1, 10) == 1:
                injuries + 1
                trailer['personSpots'][person]['health'] -= 0.1

    print('The Hunt has concluded!')
    print('You got ' + str(fullAmount) + ' Pounds of food' )
    print('Your group sustained ' + str(injuries) + ' injuries!')
    enterToContinue()

def dailyStatChanges(trailer):
    def paceDecreases(trailer, person):    # I use functions inside of functions here so I can have an more efficent and more debugable code
        if trailer['data']['paceType'] == 1:
            trailer['personSpots'][person]['rest'] -= (randint(0,1) / 100)
        if trailer['data']['paceType'] == 2:
            trailer['personSpots'][person]['rest'] -= (randint(1,3) / 100)
        if trailer['data']['paceType'] == 3:
            trailer['personSpots'][person]['rest'] -= (randint(3,6) / 100)
    def rationsDecrease(trailer, person):
        if trailer['trailerSupplies']['food'] != 0:
            if trailer['data']['consumptionType'] == 1:
                trailer['personSpots'][person]['hunger'] -= (randint(0, 1) / 100)
                trailer['trailerSupplies']['food'] -= randint(3,4)
            if trailer['data']['consumptionType'] == 2:
                trailer['trailerSupplies']['food'] -= randint(5, 8)
            if trailer['data']['consumptionType'] == 3:
                trailer['personSpots'][person]['hunger'] -= (randint(3,8) / 100)
                trailer['trailerSupplies']['food'] -= randint(0, 1)
        elif trailer['trailerSupplies']['food'] == 0:
            trailer['personSpots'][person]['hunger'] -= 0.35 #dorado refrence
    def randomHealthChange(trailer, person):
        if trailer['personSpots'][person]['hunger'] < .70 or trailer['personSpots'][person]['rest'] < .7:
            trailer['personSpots'][person]['health'] -= (randint(0,2) / 100)
        for i in trailer['personSpots'][person]['conditionTypes']:
            if trailer['personSpots'][person]['dead'] == False:
                trailer['personSpots'][person]['health'] -= (randint(2,8) / 100)
    def travelAdditions(trailer):
        milesTraveled = randint(3,13) # I realized at the requested time, it would take well over 
        trailer['stats']['daysTraveled'] += 1
        trailer['stats']['distanceTraveled'] += milesTraveled
    def restChange(trailer, person):
        if trailer['data']['paceType'] == 1:
            trailer['personSpots'][person]['rest'] -= 0.01
        if trailer['data']['paceType'] == 2:
            trailer['personSpots'][person]['rest'] -= 0.03
        if trailer['data']['paceType'] == 3:
            trailer['personSpots'][person]['rest'] -= 0.05

    for person in trailer['personSpots']:
        paceDecreases(trailer, person)
        rationsDecrease(trailer, person)
        randomHealthChange(trailer, person)
        restChange(trailer, person)
    travelAdditions(trailer)


# Conditions to lower health
# trailer['personSpots'][person]['hunger'] < .70 and trailer['personSpots'][person]['thirst'] < .80 and trailer['personSpots'][person]['rest'] < trailer['personSpots'][person]['dead'] == False:

def diseasePersonRandomApply(trailer):
    def giveDisease(trailer):
        randomChoice = randint(0, (len(validConditionTypes) - 1))
        disease = validConditionTypes[randomChoice]
        trailer['personSpots'][person]['conditionTypes'].append(disease) 
        print(trailer['personSpots'][person]['name'] + ' has ' + disease + '!')
        enterToContinue()
    for person in trailer['personSpots']:
        if FORCE_DISEASE == True:
            giveDisease(trailer)
        if trailer['personSpots'][person]['health'] < .10:
            chance = randint(0, 1)
            if chance == 1:
                giveDisease(trailer)
        elif trailer['personSpots'][person]['health'] < .20:
            chance = randint(0, 5)
            if chance == 1:
                giveDisease(trailer)
        elif trailer['personSpots'][person]['health'] < .30:
            chance = randint(0, 10)
            if chance == 1:
                giveDisease(trailer)
        elif trailer['personSpots'][person]['health'] < .40:
            chance = randint(0, 15)
            if chance == 1:
                giveDisease(trailer)
        elif trailer['personSpots'][person]['health'] < .50:
            chance = randint(0, 20)
            if chance == 1:
                giveDisease(trailer)
        elif trailer['personSpots'][person]['health'] < .60:
            chance = randint(0, 25)
            if chance == 1:
                giveDisease(trailer)
        elif trailer['personSpots'][person]['health'] < .70:
            chance = randint(0, 30)
            if chance == 1:
                giveDisease(trailer)


while True:
    clearTerm()
    asciiArt()

    # First Run
    if firstRun == True:
        yesOrNo = input('Ready to start? (Y/n): ')
        if yesOrNo == 'n':
            print('ok')
            quit()
        getPersonsAtStart(trailer)
        firstRun = False
        clearTerm()
        asciiArt()
        if INSTANT_COMPLETION == True:
            trailer['stats']['distanceTraveled'] = 1999
        if INSTANT_FAILURE == True:
            trailer['stats']['daysTraveled'] = 304
    
    # :)
    if DEBUG == True:
        print('\033[31mDEBUG MODE IS ENABLED, SPECIAL COMMANDS CAN BE USED\033[0m')
        print('\033[31m' + str(trailer) + '\033[0m')


    # The mess called spagetti code
    printSpacer(2)
    print('Distance Traveled: ' + str(trailer['stats']['distanceTraveled']))
    print('Days Traveled: ' + str(trailer['stats']['daysTraveled']))
    print('Food: ' + str(trailer['trailerSupplies']['food']), 'Pounds of food')
    printSpacer(2)

    # Rested Cancel is just in case you rest you dont increase in milage
    dailyChecks(trailer)
    if restedCancel == False:
        events(trailer)
        restedCancel = False

    # Constantly checking if the wagon leader is alive
    if trailer['personSpots'][1]['dead'] == True:
        printSpacer(3)
        print('The Wagon Leader has died! Your wagon leader is the only one who can operate the wagon!')
        printSpacer(3)
        detailsAction(trailer, clear=False)
        printSpacer(3)
        quit()
    
    if trailer['trailerSupplies']['food'] < 0:
        trailer['trailerSupplies']['food'] = 0

    response = str(menu())
    if response == '1':
        print()
        dailyStatChanges(trailer)
        diseasePersonRandomApply(trailer)
    elif response == '2':
        restAction(trailer)
        restedCancel = True
    elif response == '3':
        huntAction(trailer)
    elif response == '4':
        detailsAction(trailer)
    elif response == '5':
       rationsChangeAction()
    elif response == '6':
        paceChangeAction()
    else:
        print()

    # Checks for very specific cases
    for person in trailer['personSpots']:
        trailer['personSpots'][person]['hunger'] = round(trailer['personSpots'][person]['hunger'], 2)
        trailer['personSpots'][person]['health'] = round(trailer['personSpots'][person]['health'], 2)
        trailer['personSpots'][person]['rest'] =round(trailer['personSpots'][person]['rest'], 2)

        # If this somehow happens
        if trailer['personSpots'][person]['rest'] > 1:
            trailer['personSpots'][person]['rest'] = 1.0
        if trailer['personSpots'][person]['hunger'] > 1:
            trailer['personSpots'][person]['hunger'] = 1.0
        if trailer['personSpots'][person]['health'] > 1:
            trailer['personSpots'][person]['hunger'] = 1.0
