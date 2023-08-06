from simba.read_config_unit_tests import (read_config_file,
                                          read_project_path_and_file_type,
                                          read_config_entry)
from simba.features_scripts.unit_tests import read_video_info_csv
from simba.misc_tools import SimbaTimer, find_core_cnt, check_multi_animal_status
from simba.train_model_functions import get_all_clf_names
from simba.drop_bp_cords import getBpNames, create_body_part_dictionary
import os, glob
from simba.enums import Paths, ReadConfig, Dtypes
from datetime import datetime

class ConfigReader(object):
    def __init__(self,
                 config_path: str):

        self.timer = SimbaTimer()
        self.timer.start_timer()
        self.config = read_config_file(ini_path=config_path)
        self.config_path = config_path
        self.datetime = datetime.now().strftime('%Y%m%d%H%M%S')
        self.project_path, self.file_type = read_project_path_and_file_type(config=self.config)
        self.features_dir = os.path.join(self.project_path, Paths.FEATURES_EXTRACTED_DIR.value)
        self.targets_folder = os.path.join(self.project_path, Paths.TARGETS_INSERTED_DIR.value)
        self.machine_results_dir = os.path.join(self.project_path, Paths.MACHINE_RESULTS_DIR.value)
        self.directionality_df_dir = os.path.join(self.project_path, Paths.DIRECTIONALITY_DF_DIR.value)
        self.outlier_corrected_dir = os.path.join(self.project_path, Paths.OUTLIER_CORRECTED.value)
        self.video_info_df = read_video_info_csv(os.path.join(self.project_path, Paths.VIDEO_INFO.value))
        self.directing_animals_video_output_path = os.path.join(self.project_path, Paths.DIRECTING_BETWEEN_ANIMALS_OUTPUT_PATH.value)
        self.animal_cnt = read_config_entry(config=self.config, section=ReadConfig.GENERAL_SETTINGS.value, option=ReadConfig.ANIMAL_CNT.value, data_type=Dtypes.INT.value)
        self.clf_cnt = read_config_entry(self.config, ReadConfig.SML_SETTINGS.value, ReadConfig.TARGET_CNT.value, Dtypes.INT.value)
        self.clf_names = get_all_clf_names(config=self.config, target_cnt=self.clf_cnt)
        self.feature_file_paths = glob.glob(self.features_dir + '/*.' + self.file_type)
        self.outlier_corrected_paths = glob.glob(self.outlier_corrected_dir + '/*.' + self.file_type)
        self.cpu_cnt, self.cpu_to_use = find_core_cnt()
        self.machine_results_paths = glob.glob(self.machine_results_dir + '/*.' + self.file_type)
        self.logs_path = os.path.join(self.project_path, 'logs')
        self.body_parts_path = os.path.join(self.project_path, Paths.BP_NAMES.value)
        self.roi_coordinates_path = os.path.join(self.logs_path, Paths.ROI_DEFINITIONS.value)
        self.video_dir = os.path.join(self.project_path, 'videos')
        self.clf_validation_dir = os.path.join(self.project_path, Paths.CLF_VALIDATION_DIR.value)
        self.data_table_path = os.path.join(self.project_path, Paths.DATA_TABLE.value)
        self.multi_animal_status, self.multi_animal_id_list = check_multi_animal_status(self.config, self.clf_cnt)
        self.x_cols, self.y_cols, self.p_cols = getBpNames(config_path)
        self.animal_bp_dict = create_body_part_dictionary(self.multi_animal_status, self.multi_animal_id_list, self.animal_cnt, self.x_cols, self.y_cols, [], [])




