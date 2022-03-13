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
    'attack': (1537, 1215, 1570, 1250),
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
}

status = {
    'open_menu': False,
    'enemies': False,
    'target_all': False,
    'attack': False,
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

        # Проверки
        status['open_menu'] = check_frame(frame_set, 'open_menu')
        status['enemies'] = check_frame(frame_set, 'enemies', conf=0.9)
        status['target_all'] = check_frame(frame_set, 'target_all')
        status['attack'] = check_frame(frame_set, 'attack')

        status['shield_damage'] = check_pixel(coordinates['check_shield'], colors['damage'])
        status['armor_damage'] = check_pixel(coordinates['check_armor'], colors['damage'])
        status['cap_60'] = check_pixel(coordinates['cap_60'], colors['capacitor'])
        status['cap_30'] = check_pixel(coordinates['cap_30'], colors['capacitor'])
 
        for index, value in slots.items():
            value['status'] = check_pixel(value['check'], colors['activated_1']) or check_pixel(value['check'], colors['activated_2'])
        
        # Подтверждение, что модуль действительно выключен
        sleep(2)
        frame_set = makeScreenshot()
        for index, value in slots.items():
            if not value['status']:
                value['status'] = check_pixel(value['check'], colors['activated_1']) or check_pixel(value['check'], colors['activated_2'])

        # Действия на основании status
        # Озвучиваем изменение статуса боя
        if status['enemies'] and not status_before['enemies']:
            print('Вижу противников!')
        elif not status['enemies'] and status_before['enemies']:
            print('Бой окончен!')
        
        # Открываем меню
        if status['open_menu']:
            script_open_menu()
        
        # Берём в таргет
        if status['target_all']:
            script_target_all()
            script_target_1()

        # Атакуем дронами
        if status['enemies'] and status['attack'] == False:
            print("Кажется, дроны не атакуют...")
            sleep(2)
            frame_set = makeScreenshot()
            status['attack'] = check_frame(frame_set, 'attack')
            if status['attack'] == False:
                print("Отправляю дронов в атаку!")
                script_activate(coordinates['click_attack'])
        
        # Эвакуация, если урон в броню
        if status['armor_damage'] and status['enemies']:
            script_evacuate()

        # Эвакуация, если капы меньше 30 в бою
        if not status['cap_30'] and status['enemies']:
            script_evacuate()

        # Проходим по слотам
        for index, value in slots.items():
            if value['name'] == 'shield':
                if not value['status'] and status['shield_damage']:
                    print("ВКЛ щит")
                    script_activate(value['click'])
                elif value['status'] and not status['shield_damage']:
                    print("ВЫКЛ щит")
                    script_activate(value['click'])

            elif value['name'] == 'addon':
                if not value['status'] and status['enemies']:
                    print("ВКЛ аддон")
                    script_activate(value['click'])
                elif value['status'] and not status['enemies']:
                    print("ВЫКЛ аддон")
                    script_activate(value['click'])
            
            # Нажимаем 1 тарелку раз в 90 секунд
            elif value['name'] == 'atk_bonus' and status['atk_bonus'] + 30 < time() and status['enemies']:
                if value['last_act'] == None or value['last_act'] + 90 < time():
                    script_activate(value['click'])
                    value['last_act'] = time()
                    status['atk_bonus'] = time()

        # Конец миссии и выбор новой
        if check_frame(frame_set, 'mission_end', conf=0.9) and not status['enemies'] and not status['shield_damage']:
            print("Миссия выполнена!")
            script_end_mission(8)
            if not status['cap_60']:
                print("Жду минуту, регеню капу...")
                sleep(60)

            script_open_encounters()
            pyautogui.click(coordinates['click_news'])
            sleep(2)

            # Цикл принятия миссий
            while True:
                if status['system'] == 'Erzoh':
                    print(f"Так, мы в системе {status['system']}.")
                    status['0j-enc'] += choose_mission(0, 6)
                    frame_set = makeScreenshot()
                    if not check_frame(frame_set, 'refresh_timer', conf=0.9):
                        pyautogui.click(coordinates['click_refresh'])
                        status['refresh'] = time()
                        sleep(3)
                        status['0j-enc'] += choose_mission(0, 6)
                    
                    pyautogui.click(coordinates['click_journal'])
                    sleep(2)

                    if not check_pixel(coordinates['new_mission'], colors['new_mission']):
                        print("Миссии кончились...")
                        status['0j-enc'] = 0
                        pyautogui.click(coordinates['click_news_back'])
                        print("Беру миссии в 2 прыжках.")
                        status['2j-enc'] = choose_mission(2, 6)

                        if status['2j-enc'] == 0:
                            print("Миссий 2 прыжках нет, ожидаю обновление таймера...")
                            while True:
                                sleep(20)
                                frame_set = makeScreenshot()
                                if not correlate(frame_set, 'refresh_timer', conf=0.9):
                                    pyautogui.click(coordinates['click_refresh'])
                                    status['refresh'] = time()
                                    break
                            continue
                        else:
                            print("Миссии в 2 прыжках есть, лечу выполнять.")
                            status['system'] == 'Chemilip'
                            pyautogui.click(coordinates['click_journal'])
                            sleep(2)
                    break

                elif status['system'] == 'Chemilip':
                    print(f"Так, мы в системе {status['system']}.")
                    pyautogui.click(coordinates['click_journal'])
                    sleep(2)
                    if not check_pixel(coordinates['new_mission'], colors['new_mission']):
                        print("Миссии кончились... Лечу домой.")
                        script_warp_home()
                        script_open_encounters()
                        pyautogui.click(coordinates['click_news'])
                        sleep(2)
                        status['system'] = 'Erzoh'
                        continue
                    break

            pyautogui.click(coordinates['new_mission'])
            sleep(1)
            pyautogui.click(coordinates['mission_accept'])
            sleep(2)
            script_end_mission(8)
            pyautogui.click(coordinates['click_confirm'])
            sleep(6)
            while True:
                frame_set = makeScreenshot()
                confirm = check_frame(frame_set, 'confirm', conf=0.9)
                if confirm:
                    pyautogui.click(coordinates['click_confirm'])
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
    image_pos = pyautogui.locate(needle_path, frame_set[frame_name], confidence=0.5)
    return image_pos

def clicksleep(coords, times):
    for i in range(times):
        sleep(1)
        pyautogui.click(coords)

def script_open_menu():
    print("Открываю список врагов!")
    pyautogui.click(coordinates['click_eye'])
    sleep(1)
    pyautogui.click(coordinates['click_filters'])
    sleep(1)
    pyautogui.click(coordinates['click_combat'])
    sleep(1)
    print("Список открыт!")

def script_target_all():
    print('Вижу цели! Выжидаю...')
    sleep(settings['before_targeting'])
    pyautogui.click(coordinates['click_target_all'])
    print('Прицеливаюсь...')
    sleep(settings['after_targeting'])

def script_target_1():
    print('Выбираю самую резвую!')
    pyautogui.click(coordinates['click_target_1'])
    sleep(2)
    pyautogui.click(coordinates['click_target_1_off'])
    sleep(1)
    print('Готов вести огонь!')

def script_activate(coords):
    pyautogui.click(coords)
    sleep(1)

def script_evacuate():
    print('БЕЖИМ!')
    pyautogui.click(coordinates['click_filters'])
    sleep(2)
    pyautogui.click(coordinates['click_structures'])
    sleep(1)
    pyautogui.click(coordinates['click_target_1'])
    sleep(1)
    pyautogui.click(coordinates['click_dock'])
    sleep(1)
    print('Направляюсь в док!')

def script_end_mission(times):
    clicksleep(coordinates['click_dialog'], times)
    sleep(1)

def script_open_encounters():
    sleep(1)
    pyautogui.click(coordinates['click_char'])
    sleep(2)
    pyautogui.click(coordinates['click_encounters'])
    sleep(1)
    pyautogui.click(coordinates['click_news'])
    sleep(1)

def script_warp_home():
    sleep(2)
    pyautogui.click(coordinates['click_esc_enc'])
    sleep(3)
    pyautogui.click(coordinates['click_bookmarks'])
    sleep(2)
    pyautogui.click(coordinates['click_jump_1'])
    sleep(3)
    pyautogui.click(coordinates['click_esc_bookmarks'])
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
            pyautogui.click(pyautogui.center(mission))
            sleep(2)
            pyautogui.click(coordinates['mission_accept'])
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