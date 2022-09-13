import pyautogui
import pydirectinput
import asyncio
import argparse
import shutil
import re

# https://fraps.com/free/setup.exe


TIMEOUT_START_FRAPS  = 0
TIMEOUT_START_GAME   = 5  # FRAPS started
TIMEOUT_START_FPS    = 30 # Game loaded
TIMEOUT_START_MOVING = 31
TIMEOUT_STOP_MOVING  = 42
TIMEOUT_STOP_FPS     = 43
TIMEOUT_TOTAL        = 45

FRAPS_PATH = "C:/Fraps/"
FRAPS_EXE  = "fraps.exe"


def take_screenshot():
    pyautogui.hotkey("fn", "f10")
    
def toggle_fps():
    pyautogui.hotkey("fn", "f11")
    
def exit_game():
    pydirectinput.press("escape")
    pydirectinput.press("down")
    pydirectinput.press("down")
    pydirectinput.press("enter")
    pydirectinput.press("down")
    pydirectinput.press("down")
    pydirectinput.press("enter")


async def test_logic(number):
    for i in range(number + 1):
        if (i == TIMEOUT_START_FRAPS):
            proc = await asyncio.create_subprocess_exec(FRAPS_PATH + FRAPS_EXE)

        if (i == TIMEOUT_START_GAME):
            proc2 = await asyncio.create_subprocess_exec(args.file)

        if (i == TIMEOUT_START_FPS):
            toggle_fps()
            take_screenshot()

        if (i == TIMEOUT_START_MOVING):
            pydirectinput.press("enter")
            pydirectinput.press("enter")
            pydirectinput.keyDown("w")

        if (i == TIMEOUT_STOP_MOVING):
            pydirectinput.keyUp("w")

        if (i == TIMEOUT_STOP_FPS):
            toggle_fps()
            take_screenshot()

        if (i == TIMEOUT_TOTAL):
            exit_game()

        await asyncio.sleep(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="Path to game")
    parser.add_argument("-o", "--output", dest = "output_path", default = ".", help="Output directory")
    args = parser.parse_args()

    # Clear FRAPSLOG file
    open(FRAPS_PATH + "Benchmarks/FRAPSLOG.txt", "w").close()

    loop = asyncio.get_event_loop()

    tasks = [
        asyncio.ensure_future(test_logic(TIMEOUT_TOTAL)),
    ]

    loop.run_until_complete(asyncio.gather(*tasks))
    loop.close()

    try:
        shutil.move(FRAPS_PATH + "Benchmarks/FRAPSLOG.txt", args.output_path + "/FRAPSLOG.txt")
        res_file = open(args.output_path + "/FRAPSLOG.txt")
        fps_avg_file = open(args.output_path + "/fpsavg.txt", "w")
        string = "Avg"

        fps_avg = [line for line in res_file if string in line][0].split()[7]
        fps_avg_file.write(fps_avg)

        res_file.close()
        fps_avg_file.close()
    except FileNotFoundError:
        print("Please provide an existing output directory")