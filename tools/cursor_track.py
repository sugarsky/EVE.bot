import pyautogui, sys
from time import sleep
print('Press Ctrl-C to quit.')
sleep(2)
try:
    # while True:
    #     x, y = pyautogui.position()
    #     rgb = pyautogui.pixel(x, y)
    #     positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
    #     rgbStr = ' Red: ' + str(rgb[0]).rjust(3) + ' Green: ' + str(rgb[1]).rjust(3) + ' Blue: ' + str(rgb[2]).rjust(3)
    #     print(positionStr + rgbStr, end='')
    #     print('\b' * len(positionStr + rgbStr), end='', flush=True)
    
    while True:
        x, y = pyautogui.position()
        # rgb = pyautogui.pixel(x, y)
        positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
        # rgbStr = ' Red: ' + str(rgb[0]).rjust(3) + ' Green: ' + str(rgb[1]).rjust(3) + ' Blue: ' + str(rgb[2]).rjust(3)
        print(positionStr, end='')
        print('\b' * len(positionStr), end='', flush=True)
        
except KeyboardInterrupt:
    print('\n')