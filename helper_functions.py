# functions to access the MIDI audio files in the problem dataset


import os

def make_composer_dict(Composers,data_dir='./Part One Data/Part1(PS1)/'):
    '''dict of composition files, composers as key 

    Composers: List of Composers
    dir_path: path to composer folders
    '''

    audio_files = dict()

    for composer in Composers:
    
        dir_path = data_dir + composer
    
        files = get_audio_files(dir_path)
    
        audio_files[composer] = files

    return audio_files

def get_audio_files(dir_path):
    
    files = []
    
    for path in os.listdir(dir_path):
        #check if path is a file
        if os.path.isfile(os.path.join(dir_path,path)):
            files.append(os.path.join(dir_path,path))
    
    return files
