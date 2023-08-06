from simba.read_config_unit_tests import (read_config_file,
                                          read_project_path_and_file_type,
                                          read_config_entry)
from simba.features_scripts.unit_tests import read_video_info_csv
from simba.misc_tools import SimbaTimer
from simba.train_model_functions import get_all_clf_names
import os, glob
from simba.enums import Paths, ReadConfig, Dtypes

class ConfigReader(object):
    def __init__(self,
                 config_path: str):

        self.timer = SimbaTimer()
        self.timer.start_timer()
        self.config = read_config_file(ini_path=config_path)
        self.project_path, self.file_type = read_project_path_and_file_type(config=self.config)
        self.features_dir = os.path.join(self.project_path, Paths.FEATURES_EXTRACTED_DIR.value)
        self.targets_folder = os.path.join(self.project_path, Paths.TARGETS_INSERTED_DIR.value)
        self.machine_results_dir = os.path.join(self.project_path, Paths.MACHINE_RESULTS_DIR.value)
        self.video_info_df = read_video_info_csv(os.path.join(self.project_path, Paths.VIDEO_INFO.value))
        self.clf_cnt = read_config_entry(self.config, ReadConfig.SML_SETTINGS.value, ReadConfig.TARGET_CNT.value, Dtypes.INT.value)
        self.clf_names = get_all_clf_names(config=self.config, target_cnt=self.clf_cnt)
        self.feature_file_paths = glob.glob(self.features_dir + '/*.' + self.file_type)
        self.machine_results_paths = glob.glob(self.machine_results_dir + '/*.' + self.file_type)
        self.logs_path = os.path.join(self.project_path, 'logs')
        self.body_parts_path = os.path.join(self.project_path, Paths.BP_NAMES.value)
        self.roi_coordinates_path = os.path.join(self.logs_path, Paths.ROI_DEFINITIONS.value)
        self.video_dir = os.path.join(self.project_path, 'videos')
        self.clf_validation_dir = os.path.join(self.project_path, Paths.CLF_VALIDATION_DIR.value)




