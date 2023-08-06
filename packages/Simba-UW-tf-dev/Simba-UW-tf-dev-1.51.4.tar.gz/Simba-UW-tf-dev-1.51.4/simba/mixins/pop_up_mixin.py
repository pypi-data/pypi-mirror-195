from tkinter import *
from simba.read_config_unit_tests import (read_config_file, read_config_entry, read_project_path_and_file_type)
from simba.enums import ReadConfig, Options
from simba.drop_bp_cords import (getBpHeaders,
                                 create_body_part_dictionary,
                                 getBpNames)
from simba.misc_tools import (check_multi_animal_status,
                              find_core_cnt,
                              get_color_dict,
                              get_named_colors)
from simba.train_model_functions import get_all_clf_names
import os



class PopUpMixin(object):
    def __init__(self,
                 title: str,
                 config_path: str or None=None):

        self.main_frm = Toplevel()
        self.main_frm.minsize(400, 400)
        self.main_frm.wm_title(title)
        self.palette_options = Options.PALETTE_OPTIONS.value
        self.resolutions = Options.RESOLUTION_OPTIONS.value
        self.colors = get_named_colors()
        self.colors_dict = get_color_dict()
        self.cpu_cnt, _ = find_core_cnt()

        if config_path:
            self.config_path = config_path
            self.config = read_config_file(ini_path=config_path)
            self.project_path, self.file_type = read_project_path_and_file_type(config=self.config)
            self.project_animal_cnt = read_config_entry(config=self.config, section=ReadConfig.GENERAL_SETTINGS.value, option=ReadConfig.ANIMAL_CNT.value, data_type='int')
            self.multi_animal_status, self.multi_animal_id_lst = check_multi_animal_status(self.config, self.project_animal_cnt)
            self.x_cols, self.y_cols, self.pcols = getBpNames(config_path)
            self.animal_bp_dict = create_body_part_dictionary(self.multi_animal_status, list(self.multi_animal_id_lst), self.project_animal_cnt, self.x_cols, self.y_cols, [], [])
            self.target_cnt = read_config_entry(config=self.config, section=ReadConfig.SML_SETTINGS.value, option=ReadConfig.TARGET_CNT.value, data_type='int')
            self.clf_names = get_all_clf_names(config=self.config, target_cnt=self.target_cnt)
            self.videos_dir = os.path.join(self.project_path, 'videos')



