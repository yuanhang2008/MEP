# -*- coding: utf-8 -*-


import os


BASE_PATH = 'dist'

def getname():
    if not os.path.exists(BASE_PATH):
        print(f'{BASE_PATH} was not found')
        os._exit()
    files = [file for file in os.listdir(BASE_PATH) if file.endswith('.whl')]
    if len(files) == 1:
        return files[0]
    print('wheel file was not unique')
    os._exit()


if __name__ == '__main__':
    path = f'{BASE_PATH}/' + getname()
    os.system(f'pip install {path}')