import pyautogui
import os
from time import sleep, time

settings = {
    'before_targeting': 1, # for long range put 5
    'after_targeting': 3, # for long range put 12
    'tik_sleep': 5
}

frames = {
    'open_menu': (2344, 772, 2402, 808),
    'target_all': (1547, 880, 1576, 910),
    'attack': (1537, 1215, 1570, 1250), # 33x35
    'attack2': (2145, 1215, 2180, 1250), # 33x35
    'attack3': (2295, 1215, 2333, 1250), # 33x35
    'enemies': (2385, 175, 2405, 205),
    'mission_end': (350, 500, 450, 528),
    'refresh_timer': (1519, 294, 1560, 326),
    'confirm': (2158, 1048, 2318, 1084)
}

coordinates = {
    'click_eye': (2374, 792),
    'click_filters': (2186, 88),
    'click_combat': (2104, 278),
    'click_structures': (2100, 550),
    'click_dock': (1500, 200),
    'click_dialog': (570, 630),
    'click_char': (250,  100),
    'click_encounters': (500, 1000),
    'click_news': (500, 400),
    'click_news_back': (200, 400),
    'click_refresh': (1450, 300),
    'click_journal': (2350, 260),
    'click_confirm': (2200, 1075),
    'click_target_all': (1560, 900),
    'click_target_1': (2000, 200),
    'click_target_1_off': (150, 550),
    'click_attack': (1600, 1300),
    'click_esc_enc': (2379, 110),
    'click_bookmarks': (100, 350),
    'click_jump_1': (552, 595),
    'click_esc_bookmarks': (553, 482),
    'mission_accept': (1800, 1200),
    'check_shield': (1170, 1127),
    'check_armor': (1160, 1156),
    'cap_60': (1405, 1179),
    'cap_30': (1395, 1245),
    'new_mission': (535, 523)
}

colors = {
    'damage': (202, 3, 0),
    'activated_1': (201, 240, 226),
    'activated_2': (255, 255, 255),
    'capacitor': (255, 255, 220),
    'new_mission': (206, 206, 206)
}

checks = {
    'atk_bonus': 'pixel',
    'addon': 'pixel',
    'shield': 'pixel',
    'attack': 'frame',
    'attack2': 'frame',
    'attack3': 'frame',
}

slots = {
    1: {
        'name': 'atk_bonus',
        'status': False,
        'check': (1610, 1065),
        'click': (1610, 1125),
        'last_act': None
    },
    2: {
        'name': 'atk_bonus',
        'status': False,
        'check': (1760, 1065),
        'click': (1760, 1125),
        'last_act': None
    },
    3: {
        'name': 'atk_bonus',
        'status': False,
        'check': (1915, 1065),
        'click': (1915, 1125),
        'last_act': None
    },
    4: {
        'name': 'addon',
        'status': False,
        'check': (2065, 1065),
        'click': (2065, 1125),
        'last_act': None
    },
    5: {
        'name': 'addon',
        'status': False,
        'check': (2220, 1065),
        'click': (2210, 1125),
        'last_act': None
    },
    6: {
        'name': 'shield',
        'status': False,
        'check': (2380, 1067),
        'click': (2363, 1125),
        'last_act': None
    },
    7: {
        'name': 'attack',
        'status': False,
        'check': (1610, 1225),
        'click': (1610, 1275),
        'last_act': None
    },
    8: {
        'name': 'addon',
        'status': False,
        'check': (1760, 1225),
        'click': (1760, 1275),
        'last_act': None
    },
    9: {
        'name': 'addon',
        'status': False,
        'check': (1915, 1225),
        'click': (1915, 1275),
        'last_act': None
    },
    10: {
        'name': 'addon',
        'status': False,
        'check': (2065, 1225),
        'click': (2065, 1275),
        'last_act': None
    },
    11: {
        'name': 'attack2',
        'status': False,
        'check': (2220, 1225),
        'click': (2220, 1275),
        'last_act': None
    },
    12: {
        'name': 'attack3',
        'status': False,
        'check': (2380, 1225),
        'click': (2380, 1275),
        'last_act': None
    },
}

status = {
    'open_menu': False,
    'enemies': False,
    'target_all': False,
    'shield_damage': False,
    'armor_damage': False,
    'cap_60': True,
    'cap_30': True,
    'atk_bonus': 0,
    'refresh': 0,
    'system': 'Erzoh', # Chemilip, Erzoh
    '0j-enc': 0,
    '2j-enc': 0
}

def main():
    initializePyAutoGUI()
    countdownTimer()
    global status
    while True:
        frame_set = makeScreenshot()
        loop_start = time()
        status_before = status.copy()

        # ????????????????
        status['open_menu'] = check_frame(frame_set, 'open_menu')
        status['enemies'] = check_frame(frame_set, 'enemies', conf=0.9)
        status['target_all'] = check_frame(frame_set, 'target_all')

        status['shield_damage'] = check_pixel(coordinates['check_shield'], colors['damage'])
        status['armor_damage'] = check_pixel(coordinates['check_armor'], colors['damage'])
        status['cap_60'] = check_pixel(coordinates['cap_60'], colors['capacitor'])
        status['cap_30'] = check_pixel(coordinates['cap_30'], colors['capacitor'])
 
        for index, value in slots.items():
            if checks[value['name']] == 'pixel':
                value['status'] = check_pixel(value['check'], colors['activated_1']) or check_pixel(value['check'], colors['activated_2'])
            elif checks[value['name']] == 'frame':
                value['status'] = check_frame(frame_set, value['name'])
        
        # ??????????????????????????, ?????? ???????????? ?????????????????????????? ????????????????
        sleep(2)
        frame_set = makeScreenshot()
        for index, value in slots.items():
            if not value['status']:
                if checks[value['name']] == 'pixel':
                    value['status'] = check_pixel(value['check'], colors['activated_1']) or check_pixel(value['check'], colors['activated_2'])
                elif checks[value['name']] == 'frame':
                    value['status'] = check_frame(frame_set, value['name'])

        # ???????????????? ???? ?????????????????? status
        # ???????????????????? ?????????????????? ?????????????? ??????
        if status['enemies'] and not status_before['enemies']:
            print('???????? ??????????????????????!')
        elif not status['enemies'] and status_before['enemies']:
            print('?????? ??????????????!')
        
        # ?????????????????? ????????
        if status['open_menu']:
            script_open_menu()
        
        # ?????????? ?? ????????????
        if status['target_all']:
            script_target_all()
            script_target_1()

        # ?????????????? ??????????????
        if status['enemies']:
            for index, value in slots.items():
                if checks[value['name']] == 'frame' and not value['status']:
                    print("?????????????????? ???????????? ?? ??????????!")
                    script_activate(value['click'])

        # if status['enemies'] and status['attack'] == False:
        #     print("??????????????, ?????????? ???? ??????????????...")
        #     sleep(2)
        #     frame_set = makeScreenshot()
        #     status['attack'] = check_frame(frame_set, 'attack')
        #     if status['attack'] == False:
        #         print("?????????????????? ???????????? ?? ??????????!")
        #         script_activate(coordinates['click_attack'])
        
        # ??????????????????, ???????? ???????? ?? ??????????
        if status['armor_damage'] and status['enemies']:
            script_evacuate()

        # ??????????????????, ???????? ???????? ???????????? 30 ?? ??????
        if not status['cap_30'] and status['enemies']:
            script_evacuate()

        # ???????????????? ???? ????????????
        for index, value in slots.items():
            if value['name'] == 'shield':
                if not value['status'] and status['shield_damage']:
                    print("?????? ??????")
                    script_activate(value['click'])
                elif value['status'] and not status['shield_damage']:
                    print("???????? ??????")
                    script_activate(value['click'])

            elif value['name'] == 'addon':
                if not value['status'] and status['enemies']:
                    print("?????? ??????????")
                    script_activate(value['click'])
                elif value['status'] and not status['enemies']:
                    print("???????? ??????????")
                    script_activate(value['click'])
            
            # ???????????????? 1 ?????????????? ?????? ?? 90 ????????????
            elif value['name'] == 'atk_bonus' and status['atk_bonus'] + 30 < time() and status['enemies']:
                if value['last_act'] == None or value['last_act'] + 90 < time():
                    script_activate(value['click'])
                    value['last_act'] = time()
                    status['atk_bonus'] = time()

        # ?????????? ???????????? ?? ?????????? ??????????
        if check_frame(frame_set, 'mission_end', conf=0.9) and not status['enemies'] and not status['shield_damage']:
            print("???????????? ??????????????????!")
            script_end_mission(8)
            if not status['cap_60']:
                print("?????? ????????????, ???????????? ????????...")
                sleep(60)

            script_open_encounters()
            sleep(2)

            # ???????? ???????????????? ????????????
            while True:
                if status['system'] == 'Erzoh':
                    print(f"??????, ???? ?? ?????????????? {status['system']}.")
                    choose_mission(0, 6)
                    frame_set = makeScreenshot()
                    if not check_frame(frame_set, 'refresh_timer', conf=0.9):
                        click(coordinates['click_refresh'])
                        status['refresh'] = time()
                        sleep(3)
                        choose_mission(0, 6)
                    
                    sleep(2)
                    click(coordinates['click_journal'])
                    sleep(2)

                    if not check_pixel(coordinates['new_mission'], colors['new_mission']):
                        print("???????????? ??????????????????...")
                        click(coordinates['click_news_back'])
                        print("???????? ???????????? ?? 2 ??????????????.")
                        status['2j-enc'] = choose_mission(2, 6)

                        if status['2j-enc'] == 0:
                            print("???????????? 2 ?????????????? ??????, ???????????? ???????????????????? ??????????????...")
                            while True:
                                sleep(20)
                                frame_set = makeScreenshot()
                                if not correlate(frame_set, 'refresh_timer', conf=0.9):
                                    click(coordinates['click_refresh'])
                                    status['refresh'] = time()
                                    break
                            continue
                        else:
                            print("???????????? ?? 2 ?????????????? ????????, ???????? ??????????????????.")
                            status['system'] = 'Chemilip'
                            click(coordinates['click_journal'])
                            sleep(2)
                    break

                elif status['system'] == 'Chemilip':
                    print(f"??????, ???? ?? ?????????????? {status['system']}.")
                    click(coordinates['click_journal'])
                    sleep(2)
                    if not check_pixel(coordinates['new_mission'], colors['new_mission']):
                        print("???????????? ??????????????????... ???????? ??????????.")
                        script_warp_home()
                        script_open_encounters()
                        sleep(2)
                        status['system'] = 'Erzoh'
                        continue
                    break

            click(coordinates['new_mission'])
            sleep(2)
            click(coordinates['mission_accept'])
            sleep(2)
            script_end_mission(8)
            click(coordinates['click_confirm'])
            sleep(6)
            while True:
                frame_set = makeScreenshot()
                confirm = check_frame(frame_set, 'confirm', conf=0.9)
                if confirm:
                    click(coordinates['click_confirm'])
                    break
                sleep(10)

        loop_end = time()
        wait = max(0, settings['tik_sleep'] - loop_end + loop_start)
        sleep(wait)
        print("_________________________")


def initializePyAutoGUI():

    pyautogui.FAILSAFE = True

def countdownTimer():
    print("Sarting", end="")
    for i in range(0, 5):
        print(".", end="")
        sleep(1)
    print("GO")

def makeScreenshot(path='shots/'):
    scr_main = pyautogui.screenshot()
    frame_set = {
        'scr_main': scr_main
    }

    for index, coords in frames.items():
        scr = scr_main.crop(coords)
        frame_set.update({index: scr})
    
    return frame_set

def correlate(frame_set, frame_name, conf=0.5):
    script_dir = os.path.dirname(__file__)
    needle_path = os.path.join(
        script_dir, 
        'needles', 
        'needle_' + frame_name +'.png'
    )
    image_pos = pyautogui.locate(needle_path, frame_set[frame_name], confidence=conf)
    return image_pos

def click(coord):
    x, y = coord
    x0, y0 = pyautogui.position()
    pyautogui.moveTo(x, y, duration=0)
    pyautogui.click(coord)
    pyautogui.moveTo(x0, y0, duration=0)

def clicksleep(coords, times):
    for i in range(times):
        sleep(1)
        click(coords)

def script_open_menu():
    print("???????????????? ???????????? ????????????!")
    click(coordinates['click_eye'])
    sleep(1)
    click(coordinates['click_filters'])
    sleep(1)
    click(coordinates['click_combat'])
    sleep(1)
    print("???????????? ????????????!")

def script_target_all():
    print('???????? ????????! ??????????????...')
    sleep(settings['before_targeting'])
    click(coordinates['click_target_all'])
    print('????????????????????????...')
    sleep(settings['after_targeting'])

def script_target_1():
    print('?????????????? ?????????? ????????????!')
    click(coordinates['click_target_1'])
    sleep(2)
    click(coordinates['click_target_1_off'])
    sleep(1)
    print('?????????? ?????????? ??????????!')

def script_activate(coords):
    click(coords)
    sleep(1)

def script_evacuate():
    print('??????????!')
    click(coordinates['click_filters'])
    sleep(2)
    click(coordinates['click_structures'])
    sleep(1)
    click(coordinates['click_target_1'])
    sleep(1)
    click(coordinates['click_dock'])
    sleep(1)
    print('?????????????????????? ?? ??????!')

def script_end_mission(times):
    clicksleep(coordinates['click_dialog'], times)
    sleep(1)

def script_open_encounters():
    sleep(1)
    click(coordinates['click_char'])
    sleep(2)
    click(coordinates['click_encounters'])
    sleep(3)
    click(coordinates['click_news'])
    sleep(2)

def script_warp_home():
    sleep(2)
    click(coordinates['click_esc_enc'])
    sleep(3)
    click(coordinates['click_bookmarks'])
    sleep(2)
    click(coordinates['click_jump_1'])
    sleep(3)
    click(coordinates['click_esc_bookmarks'])
    sleep(240)

def choose_mission(jumps, times):
    count = 0
    for i in range(0, times):
        frame_set = makeScreenshot()
        script_dir = os.path.dirname(__file__)
        needle_path = os.path.join(
            script_dir, 
            'needles',
            'needle_encounter_' + str(jumps) + '.png'
        )
        mission = pyautogui.locate(needle_path, frame_set['scr_main'], confidence=0.98)
        if mission:
            click(pyautogui.center(mission))
            sleep(2)
            click(coordinates['mission_accept'])
            sleep(2)
            count += 1
    return count

def check_frame(frame_set, frame_name, conf=0.7):
    script_dir = os.path.dirname(__file__)
    needle_path = os.path.join(
        script_dir, 
        'needles',
        'needle_' + frame_name +'.png'
    )
    image_pos = pyautogui.locate(needle_path, frame_set[frame_name], confidence=conf)
    if image_pos:
        return True
    else:
        return False

def check_pixel(coordinates, color, tol=15):
    x, y = coordinates
    if pyautogui.pixelMatchesColor(x, y, color, tolerance=tol):
        return True
    else:
        return False

if __name__ == '__main__':
    main()