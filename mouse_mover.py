import pyautogui
import keyboard

def move_mouse_to_center(screen=1):
    # print("active screen ", screen)
    if screen == 1:
        pyautogui.moveTo(900, 500)
    elif screen == 2:
        pyautogui.moveTo(2912, 500)


def click_mouse():
    # print("clicking mouse")
    pyautogui.click(pyautogui.position())


def move_mouse(screen=1):
    # print("active screen ", screen)
    if screen == 1:
        # win32api.SetCursorPos((1918, 1000))
        pyautogui.moveTo(1920/2, 1080/2)
        pyautogui.click(pyautogui.position())
    elif screen == 2:
        pyautogui.moveTo(2912, 1000)
