from tkinter import *
from simba.read_config_unit_tests import (read_config_file, read_config_entry, read_project_path_and_file_type)
from simba.enums import ReadConfig, Options
from simba.drop_bp_cords import (getBpHeaders,
                                 create_body_part_dictionary,
                                 getBpNames)
from simba.enums import Formats
from simba.misc_tools import (check_multi_animal_status,
                              find_core_cnt,
                              get_color_dict,
                              get_named_colors)
from simba.train_model_functions import get_all_clf_names
from simba.tkinter_functions import hxtScrollbar, DropDownMenu, Entry_Box
import os



class PopUpMixin(object):
    def __init__(self,
                 title: str,
                 config_path: str or None=None):

        self.main_frm = Toplevel()
        self.main_frm.minsize(400, 400)
        self.main_frm.wm_title(title)
        self.main_frm.lift()
        self.main_frm = Canvas(hxtScrollbar(self.main_frm))
        self.main_frm.pack(fill="both", expand=True)
        self.palette_options = Options.PALETTE_OPTIONS.value
        self.resolutions = Options.RESOLUTION_OPTIONS.value
        self.shading_options = Options.HEATMAP_SHADING_OPTIONS.value
        self.heatmap_bin_size_options = Options.HEATMAP_BIN_SIZE_OPTIONS.value
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
            self.bp_names = []
            for animal_name, coords in self.animal_bp_dict.items():
                for bp in coords['X_bps']:
                    self.bp_names.append(bp.rstrip('_x'))

    def create_choose_animal_cnt_dropdown(self):
        if hasattr(self, 'animal_cnt_frm'):
            self.animal_cnt_frm.destroy()
        animal_cnt_options = set(range(1, self.project_animal_cnt + 1))
        self.animal_cnt_frm = LabelFrame(self.main_frm, text='SELECT NUMBER OF ANIMALS', font=Formats.LABELFRAME_HEADER_FORMAT.value)
        self.animal_cnt_dropdown = DropDownMenu(self.animal_cnt_frm, '# of animals', animal_cnt_options, '12')
        self.animal_cnt_dropdown.setChoices(max(animal_cnt_options))
        self.animal_cnt_confirm_btn = Button(self.animal_cnt_frm, text="Confirm", command=lambda: self.update_body_parts())
        self.animal_cnt_frm.grid(row=self.children_cnt_main(), sticky=NW)
        self.animal_cnt_dropdown.grid(row=self.children_cnt_main(), column=1, sticky=NW)
        self.animal_cnt_confirm_btn.grid(row=self.children_cnt_main(), column=2, sticky=NW)
        self.create_choose_body_parts_frm()
        self.update_body_parts()

    def create_choose_body_parts_frm(self):
        if hasattr(self, 'body_part_frm'):
            self.body_part_frm.destroy()
        self.body_parts_dropdown_dict = {}
        self.body_part_frm = LabelFrame(self.main_frm, text="CHOOSE ANIMAL BODY-PARTS", font=Formats.LABELFRAME_HEADER_FORMAT.value, name='choose animal body-parts')
        self.body_part_frm.grid(row=self.children_cnt_main(), sticky=NW)

    def update_body_parts(self):
        for child in self.body_part_frm.winfo_children():
            child.destroy()
        for animal_cnt in range(int(self.animal_cnt_dropdown.getChoices())):
            animal_name = list(self.animal_bp_dict.keys())[animal_cnt]
            self.body_parts_dropdown_dict[animal_name] = DropDownMenu(self.body_part_frm, f'{animal_name} body-part:', self.bp_names, '25')
            self.body_parts_dropdown_dict[animal_name].grid(row=animal_cnt, column=1, sticky=NW)
            self.body_parts_dropdown_dict[animal_name].setChoices(self.bp_names[animal_cnt])

    def create_time_bin_entry(self):
        if hasattr(self, 'time_bin_frm'):
            self.time_bin_frm.destroy()
        self.time_bin_frm = LabelFrame(self.main_frm, text="TIME BIN", font=Formats.LABELFRAME_HEADER_FORMAT.value)
        self.time_bin_entrybox = Entry_Box(self.time_bin_frm, 'Time-bin size (s): ', '12', validation='numeric')
        self.time_bin_entrybox.grid(row=0, column=0, sticky=NW)
        self.time_bin_frm.grid(row=self.children_cnt_main(), column=0, sticky=NW)

    def create_run_frm(self, run_function: object, title: str='RUN'):
        if hasattr(self, 'run_frm'):
            self.run_frm.destroy()
        self.run_frm = LabelFrame(self.main_frm, text='RUN', font=Formats.LABELFRAME_HEADER_FORMAT.value, fg='black')
        self.run_btn = Button(self.run_frm, text=title, command=lambda: run_function())
        self.run_btn.grid(row=0, column=0, sticky=NW)
        self.run_frm.grid(row=self.children_cnt_main(), column=0, sticky=NW)

    def children_cnt_main(self):
        return int(len(list(self.main_frm.children.keys())))

    def update_config(self):
        with open(self.config_path, 'w') as f:
            self.config.write(f)


    def enable_dropdown_from_checkbox(self,
                                      check_box_var: BooleanVar,
                                      dropdown_menus: [DropDownMenu]):
        if check_box_var.get():
            for menu in dropdown_menus:
                menu.enable()
        else:
            for menu in dropdown_menus:
                menu.disable()

    def enable_entrybox_from_checkbox(self,
                                      check_box_var: BooleanVar,
                                      entry_boxes: [Entry_Box],
                                      reverse: bool = False):
        if reverse:
            if check_box_var.get():
                for box in entry_boxes:
                    box.set_state('disable')
            else:
                for box in entry_boxes:
                    box.set_state('normal')
        else:
            if check_box_var.get():
                for box in entry_boxes:
                    box.set_state('normal')
            else:
                for box in entry_boxes:
                    box.set_state('disable')
