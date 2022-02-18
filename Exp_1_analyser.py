import muselsl.viewer_v2 as viewing
from muselsl import record
import os
import datetime
import subprocess

def recordingorview(duration, file, recorview):
    # Note: an existing Muse LSL stream is required
    # p = subprocess.Popen('OpenBlueMuse.bat', shell=True, stdout=subprocess.PIPE)
    # stdout, stderr = p.communicate()
    # if p.returncode == 0:
    #     print('Blue Muse connected')
    if recorview == 2:
        print('Recording Started file {0}'.format(file))
        record(duration, file)
        print('Recording has ended')
    elif recorview == 1:
        viewing.view()
        print('Viewing')


# Note: Recording is synchronous, so code here will not execute until the stream has been closed

if __name__ == '__main__':
    # duration = sys.argv[1]
    # file = sys.argv[2]
    # file = file[1:-1]
    # recorview = sys.argv[3]
    # numbers = re.findall('[0-9]+', duration)
    # recorview = re.findall('[0-9]+', recorview);
    #
    # print(int(numbers[0]), file, int(recorview[0]))
    # recordingorview(int(numbers[0]), file, int(recorview[0]))

    # recordingorview(1, '', 1)  # VIEW
    os.system("OpenBlueMuse.bat")
    now = datetime.datetime.now()
    # Path to be created
    path = os.path.abspath(os.getcwd())
    foldename = os.path.join(path, now.strftime("%Y-%m-%d"))

    try:
        os.mkdir(foldename)
    except:
        print(foldename + ' exists')
    "Path is created"
    while True:
        now = datetime.datetime.now()
        recname = now.strftime("%H-%M")+'.csv'
        recordingorview(900, os.path.join(foldename,recname), 2)  # Record
        print(datetime.datetime.now())
