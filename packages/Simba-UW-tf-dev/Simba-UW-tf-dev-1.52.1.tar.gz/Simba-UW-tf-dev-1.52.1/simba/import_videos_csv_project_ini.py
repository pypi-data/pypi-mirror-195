__author__ = "Simon Nilsson", "JJ Choong"

import shutil
import glob
from configparser import ConfigParser, MissingSectionHeaderError
import pandas as pd
from simba.extract_frames_fast import *
from simba.rw_dfs import read_df, save_df
from simba.drop_bp_cords import get_fn_ext
from simba.read_config_unit_tests import (read_config_file,
                                          read_config_entry,
                                          read_project_path_and_file_type,
                                          check_file_exist_and_readable,
                                          check_if_filepath_list_is_empty)
from simba.misc_tools import SimbaTimer, get_number_of_header_columns_in_df

def extract_frames_from_all_videos_in_directory(directory: str,
                                                config_path: str):
    video_paths, video_types = [], ['.avi', '.mp4']
    files_in_folder = glob.glob(directory + '/*')
    for file_path in files_in_folder:
        _, _, ext = get_fn_ext(filepath=file_path)
        if ext.lower() in video_types:
            video_paths.append(file_path)
    if len(video_paths) == 0:
        print('SIMBA ERROR: 0 video files in mp4 or avi format found in {}'.format(directory))
        raise ValueError('SIMBA ERROR: 0 video files in mp4 or avi format found')
    config = read_config_file(config_path)
    project_path = read_config_entry(config, 'General settings', 'project_path', data_type='folder_path')

    print('Extracting frames for {} videos into project_folder/frames/input directory...'.format(len(video_paths)))
    for video_path in video_paths:
        dir_name, video_name, ext = get_fn_ext(video_path)
        save_path = os.path.join(project_path, 'frames', 'input', video_name)
        if not os.path.exists(save_path): os.makedirs(save_path)
        else: print('Frames for video {} already extracted. SimBA is overwriting prior frames...')
        video_to_frames(video_path, save_path, overwrite=True, every=1, chunk_size=1000)
    print('SIMBA COMPLETE: Frames created for {} videos.'.format(str(len(video_paths))))

def splitall(path):
    allparts = []
    while 1:
        parts = os.path.split(path)
        if parts[0] == path:  # sentinel for absolute paths
            allparts.insert(0, parts[0])
            break
        elif parts[1] == path: # sentinel for relative paths
            allparts.insert(0, parts[1])
            break
        else:
            path = parts[0]
            allparts.insert(0, parts[1])
    return allparts



def copy_frame_folders(source,inifile):
    dest = str(os.path.dirname(inifile))
    dest1 = os.path.join(dest, 'frames', 'input')
    files = []

    ########### FIND FILES ###########
    for i in os.listdir(source):
        files.append(i)

    for f in files:
        filetocopy = os.path.join(source, f)
        if os.path.exists(os.path.join(dest1, f)):
            print(f, 'already exist in', dest1)

        elif not os.path.exists(os.path.join(dest1, f)):
            print('Copying frames of',f)
            shutil.copytree(filetocopy, os.path.join(dest1,f))
            nametoprint = os.path.join('',*(splitall(dest1)[-4:]))
            print(f, 'copied to', nametoprint)

    print('Finished copying frames.')

def copy_singlevideo_DPKini(inifile,source):
    try:
        print('Copying video...')
        dest = str(os.path.dirname(inifile))
        dest1 = str(os.path.join(dest, 'videos', 'input'))

        if os.path.exists(os.path.join(dest1, os.path.basename(source))):
            print(os.path.basename(source), 'already exist in', dest1)
        else:
            shutil.copy(source, dest1)
            nametoprint = os.path.join('', *(splitall(dest1)[-4:]))
            print(os.path.basename(source),'copied to',nametoprint)

        print('Finished copying video.')
    except:
        pass

def copy_singlevideo_ini(simba_ini_path: str,
                         source_path: str) -> None:

    """ Helper to import single video file to SimBA project
    Parameters
    ----------
    simba_ini_path: str
        path to SimBA project config file in Configparser format
    source_path: str
        Path to video file.
    """

    print('Copying video file...')
    dir_name, filename, file_extension = get_fn_ext(source_path)
    new_filename = os.path.join(filename + file_extension)
    destination = os.path.join(os.path.dirname(simba_ini_path), 'videos', new_filename)
    if os.path.isfile(destination):
        print('SIMBA ERROR: {} already exist in SimBA project. To import, delete this video file before importing the new video file with the same name.'.format(filename))
        raise FileExistsError()
    else:
        shutil.copy(source_path, destination)
        print('SIMBA COMPLETE: Video {} imported to SimBA project (project_folder/videos directory).'.format(filename))

def copy_multivideo_DPKini(inifile,source,filetype):
    try:
        print('Copying videos...')
        dest = str(os.path.dirname(inifile))
        dest1 = os.path.join(dest, 'videos', 'input')
        files = []

        ########### FIND FILES ###########
        for i in os.listdir(source):
            if i.__contains__(str('.'+ filetype)):
                files.append(i)

        for f in files:
            filetocopy = os.path.join(source, f)
            if os.path.exists(os.path.join(dest1,f)):
                print(f, 'already exist in', dest1)

            elif not os.path.exists(os.path.join(dest1, f)):
                shutil.copy(filetocopy, dest1)
                nametoprint = os.path.join('', *(splitall(dest1)[-4:]))
                print(f, 'copied to', nametoprint)

        print('Finished copying videos.')
    except:
        print('Please select a folder and enter in the file type')





def copy_allcsv_ini(inifile,source):
    configFile = str(inifile)
    config = ConfigParser()
    try:
        config.read(configFile)
    except MissingSectionHeaderError:
        print('ERROR:  Not a valid project_config file. Please check the project_config.ini path.')
    wfileType = config.get('General settings', 'workflow_file_type')
    print('Copying tracking files to project using ' + str(wfileType) + ' file format.')
    dest = str(os.path.dirname(inifile))
    dest1 = os.path.join(dest, 'csv', 'input_csv', 'original_filename')
    if not os.path.exists(dest1):
        os.makedirs(dest1)
    dest2 = os.path.join(dest, 'csv', 'input_csv')
    files = glob.glob(source + '/*.csv')

    ###copy files to project_folder
    for file in files:
        filebasename = os.path.basename(file)
        if os.path.exists(os.path.join(dest1, filebasename)):
            print(file, 'already exist in', dest1)
        elif not os.path.exists(os.path.join(dest1, filebasename)):
            shutil.copy(file, dest1)
            shutil.copy(file, dest2)
            print(filebasename, 'copied into SimBA project')
            if (('.csv') and ('DeepCut') in filebasename) or (('.csv') and ('DLC_') in filebasename):
                if (('.csv') and ('DeepCut') in filebasename):
                    newFname = str(filebasename.split('DeepCut')[0]) + '.' + wfileType
                if (('.csv') and ('DLC_') in filebasename):
                    newFname = str(filebasename.split('DLC_')[0]) + '.' + wfileType
            else:
                newFname = str(filebasename.split('.')[0]) + '.' + wfileType
            if wfileType == 'parquet':
                currDf = pd.read_csv(os.path.join(dest2, filebasename))
                currDf = currDf.apply(pd.to_numeric, errors='coerce')
                currDf.to_parquet(os.path.join(dest2,newFname))
                os.remove(os.path.join(dest2, filebasename))
            if wfileType == 'csv':
                try:
                    os.rename(os.path.join(dest2,filebasename),os.path.join(dest2,newFname))
                except FileExistsError:
                    os.remove(os.path.join(dest2,filebasename))
                    print(filebasename + ' already exist in project')
            else:
                pass


def import_dlc_csv(config_path: str, source: str) -> list:
    timer = SimbaTimer()
    timer.start_timer()
    config = read_config_file(ini_path=config_path)
    project_path, file_type = read_project_path_and_file_type(config=config)
    original_file_name_dir = os.path.join(project_path, 'csv', 'input_csv', 'original_filename')
    input_csv_dir = os.path.join(project_path, 'csv', 'input_csv')
    imported_files = glob.glob(input_csv_dir + '/*.' + file_type)
    imported_file_names = []
    imported_file_paths = []
    for file_path in imported_files:
        _, video_name, _ = get_fn_ext(filepath=file_path)
        imported_file_names.append(video_name)
    if not os.path.exists(original_file_name_dir): os.makedirs(original_file_name_dir)
    if os.path.isdir(source):
        csv_files = glob.glob(source + '/*.csv')
        check_if_filepath_list_is_empty(csv_files, error_msg=f'SIMBA ERROR: NO .csv files found in {source} directory.')
    else:
        csv_files = [source]

    for file_path in csv_files:
        check_file_exist_and_readable(file_path=file_path)
        _, video_name, file_ext = get_fn_ext(filepath=file_path)
        if 'DLC_' in video_name:
            new_file_name = video_name.split('DLC_')[0] + '.csv'
        elif 'DeepCut' in video_name:
            new_file_name = video_name.split('DeepCut')[0] + '.csv'
        else:
            new_file_name = video_name.split('.')[0] + '.csv'
        new_file_name_wo_ext = new_file_name.split('.')[0]
        video_basename = os.path.basename(file_path)
        print(f'Importing {video_name} to SimBA project...')
        if new_file_name_wo_ext in imported_file_names:
            print(f'SIMBA IMPORT ERROR: {new_file_name} already exist in project. Remove file from project or rename imported video file name before importing.')
            raise FileExistsError(f'SIMBA IMPORT ERROR: {new_file_name} already exist in project. Remove file from project or rename imported video file name before importing.')
        shutil.copy(file_path, input_csv_dir)
        shutil.copy(file_path, original_file_name_dir)
        os.rename(os.path.join(input_csv_dir, video_basename), os.path.join(input_csv_dir, new_file_name))
        df = pd.read_csv(os.path.join(input_csv_dir, new_file_name))
        header_cols = get_number_of_header_columns_in_df(df=df)
        if header_cols == 3:
            df = df.iloc[1:]
        if file_type == 'parquet':
            df = pd.read_csv(os.path.join(input_csv_dir, video_basename))
            df = df.apply(pd.to_numeric, errors='coerce')
            df.to_parquet(os.path.join(input_csv_dir, new_file_name))
            os.remove(os.path.join(input_csv_dir, video_basename))
        if file_type == 'csv':
            df.to_csv(os.path.join(input_csv_dir, new_file_name), index=False)
        imported_file_paths.append(os.path.join(input_csv_dir, new_file_name))
        print(f'Pose-estimation data for video {video_name} imported to SimBA project...')
    return imported_file_paths