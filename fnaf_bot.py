import time
import sys
import threading

import customtkinter
import pyautogui
import keyboard
import pygetwindow

facing_right = False
left_door_closed = False
right_door_closed = False
switch_time = 0.45
light_pause = 0.15
check_foxy_time = 160
foxy_stalling = False

mouse_positions = {
    "left_light" : (57, 452),
    "right_light" : (1216, 468),
    "left_door" : (54, 331),
    "right_door" : (1218, 351),
    "camera_lower" : (575, 695),
    "camera_upper" : (575, 642),
    "new_button_n" : (177, 407),
    "bonnie_door_open" : (193, 232),
    "bonnie_door_closed" : (436, 370),
    "chica" : (857, 383),
    "4BCamera" : (1085, 640),
    "2ACamera" : (979, 603),
    "1CCamera" : (928, 486),
    "star1" : (200, 340),
    "star2" : (275, 340),
    "star3" : (350, 340),
    "game_opened" : (177, 139),
    "custom_night" : (356, 622),
    "freddy_arrow" : (302, 494),
    "bonnie_arrow" : (585, 493),
    "chica_arrow" : (869, 495),
    "foxy_arrow" : (1146, 492),
    "ready_button" : (1137, 654),
    "night_started" : (745, 330),
    "night6" : (278, 565),
    "continue" : (175, 492)
}

pixel_colors = {
    "new_button_n" : (255, 255, 255),
    "bonnie_door_open" : (19, 25, 65),
    "bonnie_door_closed" : (34, 36, 54),
    "chica" : (86, 94, 8),
    "foxy_eye_stage2" : (200, 200, 200),
    "foxy_eye_stage3" : (199, 199, 199),
    "star" : (255, 255, 255),
    "game_opened" : (255, 255, 255),
    "night_started" : (64, 34, 19)
}

def fatal_error(error_message):
    print(error_message)
    sys.exit()

if sys.platform != "win32":
    fatal_error("FATAL ERROR: Your operating system is not windows!")

list_of_windows = pygetwindow.getWindowsWithTitle("Five Nights At Freddy's")
while len(list_of_windows) == 0:
    print("Searching for window")
    list_of_windows = pygetwindow.getWindowsWithTitle("Five Nights At Freddy's")
    time.sleep(0.2)
game_window: pygetwindow.BaseWindow = list_of_windows[0]

game_window.moveTo(0, 0)
game_window.maximize()

game_width = game_window.width
game_height = game_window.height

def turn_left_light(second_time = False):
    global facing_right
    add_some = 0
    if second_time:
        add_some = 7
    pyautogui.moveTo(mouse_positions["left_light"][0] + add_some, mouse_positions["left_light"][1])
    time.sleep(0.03)
    
    if facing_right:
        time.sleep(switch_time)
        facing_right = False

    pyautogui.click()

def turn_right_light(second_time = False):
    global facing_right
    add_some = 0
    if second_time:
        add_some = 7
    pyautogui.moveTo(mouse_positions["right_light"][0] + add_some, mouse_positions["left_light"][1])
    
    if not facing_right:
        time.sleep(switch_time)
        facing_right = True

    pyautogui.click()

def turn_left_door():
    global facing_right
    global left_door_closed
    pyautogui.moveTo(mouse_positions["left_door"])
    
    if facing_right:
        time.sleep(switch_time)
        facing_right = False

    pyautogui.click()

    if left_door_closed:
        left_door_closed = False
    else:
        left_door_closed = True

def turn_right_door():
    global facing_right
    global right_door_closed
    pyautogui.moveTo(mouse_positions["right_door"])
    
    if not facing_right:
        time.sleep(switch_time)
        facing_right = True

    pyautogui.click()

    if right_door_closed:
        right_door_closed = False
    else:
        right_door_closed = True

def toggle_camera():
    pyautogui.moveTo(*mouse_positions["camera_lower"])
    pyautogui.moveTo(*mouse_positions["camera_upper"])

def check_for_chica():
    turn_right_light()

    found_chica = False
    time_sum = 0

    while not found_chica:
        if pyautogui.pixelMatchesColor(*mouse_positions["chica"], pixel_colors["chica"]):
            found_chica = True
            break
        time_sum += 0.01
        time.sleep(0.01)
        if time_sum == light_pause:
            break
        
    
    if found_chica and not right_door_closed:
        turn_right_door()      
    elif not found_chica and right_door_closed:
        turn_right_door()

    turn_right_light(True)

line_y_position_stage1 = 113
line_y_position_stage2 = 154
line_y_position_stage3 = 368

def change_foxy_stalling():
    global foxy_stalling
    time.sleep(4)
    foxy_stalling = False


def return_foxy_stage():
    screen = pyautogui.screenshot()
    
    for i in range(594, 950):
        current_rgb = screen.getpixel((i, line_y_position_stage2))
    
        r_diff = abs(current_rgb[0] - pixel_colors["foxy_eye_stage2"][0])
        g_diff = abs(current_rgb[1] - pixel_colors["foxy_eye_stage2"][1])
        b_diff = abs(current_rgb[2] - pixel_colors["foxy_eye_stage2"][2])
        
        if r_diff < 30 and g_diff < 30 and b_diff < 30:
            
            print("Found it in stage 2!")
            return 2
    
    for i in range(220, 600):
        current_rgb = screen.getpixel((i, line_y_position_stage3))
        
        r_diff = abs(current_rgb[0] - pixel_colors["foxy_eye_stage3"][0])
        g_diff = abs(current_rgb[1] - pixel_colors["foxy_eye_stage3"][1])
        b_diff = abs(current_rgb[2] - pixel_colors["foxy_eye_stage3"][2])
        
        if r_diff < 30 and g_diff < 30 and b_diff < 30:
            print("Found it in stage 3!)")
            return 3
        
    number_of_black_pixels = 0
    for i in range(83, 1050):
        current_rgb = screen.getpixel((i, line_y_position_stage1))

        if current_rgb[0] <= 5 and current_rgb[0] <= 5 and current_rgb[0] <= 5:
            number_of_black_pixels += 1

    print("The number of black pixels is:", number_of_black_pixels)
    if number_of_black_pixels > 450:
        print("It's all black")
        return 5
    elif number_of_black_pixels > 250:
        print("Found it in stage 4!")
        return 4
    else:
        print("Found it in stage 1!)")
        return 1

def check_for_bunny():
    turn_left_light()

    found_bunny = False
    time_sum = 0

    while not found_bunny:
        if pyautogui.pixelMatchesColor(*mouse_positions["bonnie_door_open"], pixel_colors["bonnie_door_open"]):
            found_bunny = True
            break
        time_sum += 0.01
        time.sleep(0.01)
        if time_sum == light_pause:
            break
        
    
    if found_bunny and not left_door_closed:
        turn_left_door()     
    elif not found_bunny and left_door_closed and not foxy_stalling and pyautogui.pixelMatchesColor(*mouse_positions["bonnie_door_closed"], pixel_colors["bonnie_door_closed"], tolerance= 5):
        turn_left_door()

    turn_left_light(True)


stopping = False
stop_program = False
def stopping_func():
    global stop_program
    global stopping
    stopping = True
    stop_program = True
keyboard.add_hotkey("x", stopping_func)

def number_of_stars():
    if pyautogui.pixelMatchesColor(*mouse_positions["star3"], pixel_colors["star"], tolerance = 5):
        return 3
    
    if pyautogui.pixelMatchesColor(*mouse_positions["star2"], pixel_colors["star"], tolerance = 5):
        return 2
    
    if pyautogui.pixelMatchesColor(*mouse_positions["star1"], pixel_colors["star"], tolerance = 5):
        return 1
    
    return 0

def office_loop():
    global foxy_stalling
    global check_foxy_time
    global facing_right
    global left_door_closed
    global right_door_closed
    global check_foxy_time
    global stopping

    night_start = time.time()

    left_door_closed = False
    right_door_closed = False
    facing_right = False
    foxy_stalling = False
    check_foxy_time = 160

    game_start = time.time()
    toggle_camera()
    time.sleep(0.2)
    pyautogui.moveTo(*mouse_positions["4BCamera"])
    pyautogui.click()
    toggle_camera()
    time.sleep(0.1)
    while not stopping:
        check_for_bunny()
        if pyautogui.pixelMatchesColor(*mouse_positions["new_button_n"], pixel_colors["new_button_n"]):
            stopping = True
        if time.time() - game_start > check_foxy_time:
            game_start = time.time()
            if not right_door_closed:
                turn_right_door()
            toggle_camera()
            time.sleep(0.15)
            pyautogui.moveTo(*mouse_positions["1CCamera"])
            pyautogui.click()
            time.sleep(1.5)
            foxy_stage = return_foxy_stage()

            if foxy_stage == 1:
                check_foxy_time = 160
                pyautogui.moveTo(*mouse_positions["4BCamera"])
                pyautogui.click()
                toggle_camera()
            elif foxy_stage == 2:
                check_foxy_time = 120
                pyautogui.moveTo(*mouse_positions["4BCamera"])
                pyautogui.click()
                toggle_camera()
            elif foxy_stage == 3:
                check_foxy_time = 30
                pyautogui.moveTo(*mouse_positions["4BCamera"])
                pyautogui.click()
                toggle_camera()
            elif foxy_stage == 4:  
                check_foxy_time = 120   
                pyautogui.moveTo(*mouse_positions["2ACamera"])
                pyautogui.click()
                pyautogui.moveTo(*mouse_positions["4BCamera"])
                pyautogui.click()
                toggle_camera()
                foxy_stalling = True
                threading.Thread(target = change_foxy_stalling, daemon = True).start()
                if not left_door_closed:
                    turn_left_door()
            elif foxy_stage == 5:
                check_foxy_time = 30
                pyautogui.moveTo(*mouse_positions["4BCamera"])
                pyautogui.click()
                toggle_camera()
        check_for_chica()
        toggle_camera()
        time.sleep(0.5)
        toggle_camera()

        if time.time() - night_start > 550:
            pyautogui.moveTo(game_width / 2, game_height / 2)
            wait_until_pixel_matches("night_started", "night_started", tolerance = 2)
            office_loop()
            break

def wait_until_pixel_matches(position_name, pixel_name, delay = 0.1, tolerance = 0):
    while not pyautogui.pixelMatchesColor(*mouse_positions[position_name], pixel_colors[pixel_name], tolerance = tolerance):
        time.sleep(delay)
    

wait_until_pixel_matches("game_opened", "game_opened")
while not stop_program:
    if number_of_stars() == 3:
        print("The bot finished the game. Terminating program.")
        break

    if number_of_stars() == 2:
        print("Trying 4/20.")
        stopping = False
        pyautogui.moveTo(*mouse_positions["custom_night"])
        pyautogui.click()
        time.sleep(1)

        for i in range(0, 20):
            pyautogui.moveTo(*mouse_positions["freddy_arrow"])
            pyautogui.click()
            pyautogui.moveTo(*mouse_positions["bonnie_arrow"])
            pyautogui.click()
            pyautogui.moveTo(*mouse_positions["chica_arrow"])
            pyautogui.click()
            pyautogui.moveTo(*mouse_positions["foxy_arrow"])
            pyautogui.click()

        pyautogui.moveTo(*mouse_positions["ready_button"])
        pyautogui.click()
        pyautogui.moveTo(game_width / 2, game_height / 2)
        wait_until_pixel_matches("night_started", "night_started", tolerance = 2)
        office_loop()
        wait_until_pixel_matches("game_opened", "game_opened")
    
    if number_of_stars() == 1:
        print("Trying night 6.")
        stopping = False
        pyautogui.moveTo(*mouse_positions["night6"])
        pyautogui.click()
        pyautogui.moveTo(game_width / 2, game_height / 2)
        time.sleep(1)
        wait_until_pixel_matches("night_started", "night_started", tolerance = 2)
        office_loop()
        wait_until_pixel_matches("game_opened", "game_opened")

    if number_of_stars() == 0:
        print("Trying to continue.")
        stopping = False
        pyautogui.moveTo(*mouse_positions["continue"])
        pyautogui.click()
        pyautogui.moveTo(game_width / 2, game_height / 2)
        time.sleep(1)
        wait_until_pixel_matches("night_started", "night_started", tolerance = 2)
        office_loop()
        wait_until_pixel_matches("game_opened", "game_opened")

