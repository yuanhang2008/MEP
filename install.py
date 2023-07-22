# -*- coding: utf-8 -*-


import os
import threading as thread
import easygui as gui

BASE_PATH = 'dist'
is_rebuilt = False
is_uninstalled = False
is_installed = False


def getname():
    if not os.path.exists(BASE_PATH):
        print(f'{BASE_PATH} was not found')
        os._exit()
    files = [file for file in os.listdir(BASE_PATH) if file.endswith('.whl')]
    if len(files) == 1:
        return files[0]
    print('wheel file was not unique')
    os._exit()

def rebuild():
    global is_rebuilt
    os.system('del /s /q dist\*.*')
    os.system('python setup.py bdist_wheel')
    is_rebuilt = True

def uninstall():
    global is_uninstalled
    os.system('pip uninstall MEP -y')
    is_uninstalled = True

def install():
    global is_installed
    while not (is_rebuilt or is_uninstalled):
        pass
    path = f'{BASE_PATH}/' + getname()
    os.system(f'pip install {path}')
    is_installed = True


def create_threads():
    return [
        thread.Thread(target=rebuild), 
        thread.Thread(target=uninstall), 
        thread.Thread(target=install)
    ]

def main():
    for t in create_threads():
        t.start()
    while True:
        if is_installed:
            gui.msgbox('Successfully install MEP')
            os._exit(0)


if __name__ == '__main__':
    main()
