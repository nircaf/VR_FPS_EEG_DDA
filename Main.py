# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import os
# basic setup
import sys
import time
import fixation
import instructions_Newline
import subprocess
import writetocsv
# import importlib
import json
import mouse_mover
import datetime
# import socket
import psutil
import pygame
import fnmatch
import pyautogui
import keyboard
import shutil

with open('experiment_config.json') as f:
    config = json.load(f)

patientname = config["patientname"]
DEVICE_TYPE = config["DEVICE_TYPE"]
LSL_RECORD_DEDUCT = config["LSL_RECORD_DEDUCT"]
FIXATION_1 = config["FIXATION_1"]
quake_run_trial = config["quake_run_trial"]
TRIALS = config["TRIALS"]
Quake_Trials = config["Quake_Trials"]

print("selected trials: ", TRIALS)
print("configured to work with device type: ", DEVICE_TYPE)


# UDP_IP = "127.0.0.1"
# UDP_PORT_CONTROL=8888
# UDP_PORT_RESPONSE = 8887
# UDP_HEADER = "EEG_DATA"
# recorder_control_sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
# recorder_control_sock.bind((UDP_IP, UDP_PORT_RESPONSE))
# def trigger_LSL_recorder_over_UDP(duration,logfile):

#     ctrl = {"command":"/start", "duration": duration, "file":logfile, "device_type": DEVICE_TYPE, "data_source": "EEG"}
#     recorder_control_sock.sendto(json.dumps(ctrl), (UDP_IP, UDP_PORT_CONTROL))
#     data, addr = recorder_control_sock.recvfrom(65535) 
#     if "OK" in data:
#         print("recorder trigger success")


def check_screen_resolution():
    x, y = pyautogui.size()
    if not (x == 1920 and y == 1080):
        sys.exit("screen resolution is not 1920*1080, please fix it!")


def mkdir(patientname):
    if not os.path.exists(patientname):
        os.mkdir(patientname)
        print("Directory ", patientname, " Created ")
    else:
        print("Directory ", patientname, " already exists")



def eyes_open_closed(patientname, logname):
    repetition_indices = 2
    instructions_Newline.instructions(
        'Welcome to NeuroBrave experiment:\n\n In this experiment you will be asked \n '
        'to OPEN and CLOSE your eyes for 30 seconds, twice. \n' 
        'Please try to move as little as possible\n\n Press space when ready\n\n Good luck', 'space')

    for repetition_index in range(repetition_indices):
        print("trial ", repetition_index+1, " out of ", repetition_indices)
        print("instruct the subject to OPEN the eyes!")
        print("recording eyes open")
        mouse_mover.move_mouse(screen=1)
        instructions_Newline.instructions('\n\n\n\n\nPlease keep your eyes open \n\n and look at the square', 5)
        call_with_args = "python LSL_recorder.py '%g' '%s' '%s' '%s'" % (25, logname, 'eyes_open_', DEVICE_TYPE)
        server_subprocessrec = subprocess.Popen(call_with_args, shell=True)
        mouse_mover.move_mouse(screen=1)
        fixation.fixat(2, 2, logname)
        print("waiting on recorder to finish", end='')
        while server_subprocessrec.poll() is None:
            print('.', end='')
            time.sleep(0.5)
        print('')

        print("instruct the subject to CLOSE the eyes!")
        print("recording eyes closed")
        mouse_mover.move_mouse(screen=1)
        instructions_Newline.instructions('\n\n\n\n\nPlease close your eyes \n\n a tone will be heard to open them\n', 5)
        call_with_args = "python LSL_recorder.py '%g' '%s' '%s' '%s'" % (25, logname, 'eyes_closed_', DEVICE_TYPE)
        server_subprocessrec = subprocess.Popen(call_with_args, shell=True)
        mouse_mover.move_mouse(screen=1)
        fixation.fixat(2, 2, logname)
        print("waiting on recorder to finish", end='')
        while server_subprocessrec.poll() is None:
            print('.', end='')
            time.sleep(0.5)
        print('')
        pygame.init()
        goodbeep = pygame.mixer.Sound('beep1.ogg')
        goodbeep.play()
        time.sleep(2)
        pygame.quit()
    print("ALL DONE.")

def checkIfProcessRunning(processName):
    '''
    Check if there is any running process that contains the given name processName.
    '''
    #Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False



def main(patientname, logname):
    timeout = quake_run_trial * 1.2
    for trialnum in TRIALS:
        print("starting trial ", trialnum)
        if trialnum == 2:
            if instructions_Newline.instructions(
                    'Next you will play 9 sessions of 3 minutes of a shooting game.\n\n'
                    'Press SPACE to continue to next trial set:\n\n Press ESC to finish now \n ', 'space') == "abort":
                print("aborting experiment")
                break
            trials_count = 0
            path_game_log = 'C:\\Program Files (x86)\\GOG Galaxy\\Games\\Quake III\\baseq3\\games.log'
            open(path_game_log, 'w').close()
            quake_run_process = subprocess.Popen("runQuake3.py '%g'" % (1), shell=True)
            time.sleep(1)
            a_file = open(path_game_log, "r")
            which_quake = 'quake_fast'
            while checkIfProcessRunning('quake3.exe'):
                lines = a_file.readlines()
                last_lines = lines[-20:]
                if fnmatch.filter(last_lines, '*ClientBegin:*'):  # check if game begins
                    print(' ClientBegin recording ', which_quake)
                    call_with_args = "python LSL_recorder.py '%g' '%s' '%s' '%s'" % (
                        quake_run_trial + 15, logname, which_quake, DEVICE_TYPE)
                    server_subprocessrec = subprocess.Popen(call_with_args, shell=True)
                    mouse_mover.move_mouse(screen=1)
                else:
                    start_time = time.time()
                    while not fnmatch.filter(last_lines, '*ClientBegin:*'): # Wait til game begins
                        lines = a_file.readlines()
                        last_lines = lines[-20:]
                        time.sleep(1)
                        if time.time() - start_time > timeout:
                            print("something bad happened")         # handle the bad event
                            break
                    ## Out of while - game started:
                    print('recording ClientBegin2 ', which_quake)

                    call_with_args = "python LSL_recorder.py '%g' '%s' '%s' '%s'" % (
                        quake_run_trial + 15, logname, which_quake, DEVICE_TYPE)
                    server_subprocessrec = subprocess.Popen(call_with_args, shell=True)
                    mouse_mover.move_mouse(screen=1)
                if which_quake == 'quake_fast': # Running fast quake mode
                    if trials_count == 0:
                        time.sleep(2)
                        keyboard.press_and_release('p')
                        print('p')
                    which_quake = 'quake_one'
                    trials_count += 1
                elif which_quake == 'quake_one': # Running one quake mode
                    which_quake = 'quake_none'
                    trials_count +=1
                elif which_quake == 'quake_none': # Running none quake mode
                    which_quake = 'quake_fast'
                    trials_count +=1

                start_time = time.time()
                while not fnmatch.filter(last_lines, '*Exit: Timelimit hit*'): # Check if game finished
                    print('Waiting for game to finish. Time {0}'.format(round(time.time() - start_time)))
                    lines = a_file.readlines()
                    last_lines = lines[-20:]
                    time.sleep(2)
                    if time.time() - start_time > timeout:
                        print("something bad happened")         # handle the bad event
                        break
                pausegame = True
                while server_subprocessrec.poll() is None:
                    print("waiting on recorder to finish", end='')
                    if pausegame: # stop of recording didnt finish
                        keyboard.press_and_release('esc')
                        pausegame = False
                    print(',', end='')
                    time.sleep(0.5)
                if not pausegame: # Continue game
                    keyboard.press_and_release('esc')
                while checkIfProcessRunning('quake3.exe') and trials_count >= Quake_Trials:
                    print("waiting on quake to EXIT " + trials_count, end='')
                    time.sleep(0.5)

            shutil.copy(path_game_log, (logname[:-4] +'_quake.log'))

        if trialnum == 3:
            if instructions_Newline.instructions(
                    'Next you will watch 3 minutes of you playing.\n\n'
                    'Press SPACE to continue to next trial set:\n\n Press ESC to finish now \n ', 'space') == "abort":
                print("aborting experiment")
                break
            print('Quake3 Demo')
            quake_run_process = subprocess.Popen("runQuake3.py '%g'" % (0), shell=True,  stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE)
            time.sleep(3)
            call_with_args = "python LSL_recorder.py '%g' '%s' '%s' '%s'" % (
                quake_run_trial, logname, 'quake_demo', DEVICE_TYPE)
            server_subprocessrec = subprocess.Popen(call_with_args, shell=True)
            time.sleep(quake_run_trial-5)
            print('process kill')
            for proc in psutil.process_iter():
                if proc.name() == 'quake3.exe':
                    proc.kill()
            print('kill quake process')
            instructions_Newline.instructions(
                'Thank you for participating\n\n Please wait for the experimenter\n to verify recording finish '
                '\n before removing the signal devices.'
                '\n\n Thank you, NeuroBrave team.', 20)
            print("waiting on recorder to finish", end='')
            while server_subprocessrec.poll() is None:
                print('.', end='')
                time.sleep(0.5)

        if trialnum == 1:
            mouse_mover.move_mouse(screen=1)
            writetocsv.writelogcsv('Welcome instructions ', logname)
            instructions_Newline.instructions(
                'Welcome to NeuroBrave experiment:\n\n In this experiment you will be presented \n  '
                'a task to close and open eyes,\n  and a task to play a first person shooter. Please try to preform the tasks the best you can.\n '
                'Also please keep your eyes on the screen at all times '
                'and try to move as little as necessary\n\n Press space when ready\n\n Good luck', 'space')
            mouse_mover.click_mouse()
            eyes_open_closed(patientname, logname)

def copy_and_overwrite(from_path, to_path):
    if os.path.exists(to_path):
        shutil.rmtree(to_path)
    shutil.copytree(from_path, to_path)

def copyQuakeConfigFilesToGameFolder():

    copy_and_overwrite("\Qauke3_config_files", config["Quake3InstallDir"])
def copyQuakeConfigFilesToGameFolder():
    # this function copies files and folders from a source folder into destination folder.
    # only works on 1 subfolder level, this means that sub-subfolders are ignored.
    try:
        source_folder ='Qauke3_config_files'
        dest_folder  =config["Quake3InstallDir"]  
        print("copying game config files to target directory: ", dest_folder)
        tree=os.listdir(source_folder)
        for entry in tree:
            if '.' in entry:
                shutil.copy(source_folder + '\\' +entry, dest_folder)
            else:  #we hit a subfolder
                subtree = os.listdir(source_folder+'\\' + entry)
                for subentry in subtree:
                    shutil.copy(source_folder + '\\' +entry + '\\' + subentry, dest_folder + '\\'+entry)
    except:
        print("FAILED copying game config files to target directory!")
    

if __name__ == '__main__':
    check_screen_resolution()
    # Create target Directory if don't exist
    foldername = patientname+'_'+DEVICE_TYPE[0:1]+'_'+datetime.date.today().strftime("%d.%m.%Y")
    mkdir(foldername)
    logname = os.path.join(foldername, patientname + '_Log.csv')

    if DEVICE_TYPE == "MUSE":
        pyautogui.moveTo(2500, 500)
        os.system('start bluemuse://start?streamfirst=true')
        time.sleep(3)
    elif DEVICE_TYPE == "SYNTHETIC":
        # syntheic LSL generator for testing:
        print("running synthetic LSL sender: ")
        sender_subprocess = subprocess.Popen("python send_lsl.py", shell=True)
        time.sleep(5)

    if not DEVICE_TYPE == "OPENBCI":
        mouse_mover.move_mouse()
        LSL_viewer = subprocess.Popen("python view_live_data.py", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE)
        time.sleep(5)
        out = LSL_viewer.communicate()
        err = str(out[1])
        msg = str(out[0])
        if 'Error' in err:
            print(err)
            sys.exit("no active LSL stream found, terminating experiment program")
        LSL_viewer.kill()
        writetocsv.writelogcsv('EEG View ', logname)

    main(patientname, logname)