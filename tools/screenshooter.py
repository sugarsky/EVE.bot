import pyautogui

frames = {
    'open_menu': (2344, 772, 2402, 808),
    'target_all': (1547, 880, 1576, 910),
    'attack': (1537, 1215, 1570, 1250),
    'enemies': (2385, 175, 2405, 205),
    'mission_end': (350, 500, 450, 528),
    'refresh_timer': (1519, 294, 1560, 326)
}

def makeScreenshot(path='shots/'):
    scr_main = pyautogui.screenshot(path + 'main_mission_2j.png')

    for index, coords in frames.items():
        scr = scr_main.crop(coords)
        filepath = path + index + ".png"
        scr.save(filepath)

def main():
    makeScreenshot()

if __name__ == '__main__':
    main()

