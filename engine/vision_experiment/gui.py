import time
import numpy

import PyQt4.Qt as Qt
import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore

from visexpman.engine.generic import utils


################### New mouse widget #######################
class AnimalParametersGroupBox(QtGui.QGroupBox):
    def __init__(self, parent):
        QtGui.QGroupBox.__init__(self, 'Animal parameters', parent)
        self.create_widgets()
        self.create_layout()

    def create_widgets(self):
        default_date = QtCore.QDate(2012, 1, 1)
        date_format = QtCore.QString('dd-MM-yyyy')
        ear_punch_items = QtCore.QStringList(['0',  '1',  '2'])                
        self.mouse_birth_date_label = QtGui.QLabel('Mouse birth date',  self)        
        self.mouse_birth_date = QtGui.QDateEdit(self)
        self.mouse_birth_date.setDisplayFormat(date_format)
        self.mouse_birth_date.setDate(default_date)
        self.gcamp_injection_date_label = QtGui.QLabel('GCAMP injection date',  self)
        self.gcamp_injection_date = QtGui.QDateEdit(self)
        self.gcamp_injection_date.setDisplayFormat(date_format)
        self.gcamp_injection_date.setDate(default_date)
        self.ear_punch_l_label = QtGui.QLabel('Ear punch L',  self)
        self.ear_punch_l = QtGui.QComboBox(self)
        self.ear_punch_l.addItems(ear_punch_items)
        self.ear_punch_r_label = QtGui.QLabel('Ear punch R',  self)
        self.ear_punch_r = QtGui.QComboBox(self)                
        self.ear_punch_r.addItems(ear_punch_items)
        self.gender_label = QtGui.QLabel('Gender',  self)
        self.gender = QtGui.QComboBox(self)        
        self.gender.addItems(QtCore.QStringList(['male', 'female']))
        self.anesthesia_protocol_label = QtGui.QLabel('Anesthesia protocol',  self)
        self.anesthesia_protocol = QtGui.QComboBox(self)        
        self.anesthesia_protocol.addItems(QtCore.QStringList(['isoflCP 1.0', 'isoflCP 0.5', 'isoflCP 1.5']))
        self.mouse_strain_label = QtGui.QLabel('Mouse strain',  self)
        self.mouse_strain = QtGui.QComboBox(self)
        self.mouse_strain.addItems(QtCore.QStringList(['bl6', 'chat', 'chatdtr']))
        self.comments = QtGui.QComboBox(self)
        self.comments.setEditable(True)
        self.comments.setToolTip('Add comment')
        self.new_mouse_file_button = QtGui.QPushButton('Create new mouse file',  self)
        
    def create_layout(self):
        self.layout = QtGui.QGridLayout()
        self.layout.addWidget(self.mouse_birth_date_label, 0, 0)
        self.layout.addWidget(self.mouse_birth_date, 1, 0)
        self.layout.addWidget(self.gcamp_injection_date_label, 2, 0)
        self.layout.addWidget(self.gcamp_injection_date, 3, 0)
        self.layout.addWidget(self.ear_punch_l_label, 0, 1)
        self.layout.addWidget(self.ear_punch_l, 1, 1)
        self.layout.addWidget(self.ear_punch_r_label, 2, 1)
        self.layout.addWidget(self.ear_punch_r, 3, 1)
        self.layout.addWidget(self.gender_label, 0, 2)
        self.layout.addWidget(self.gender, 1, 2)
        self.layout.addWidget(self.mouse_strain_label, 2, 2)
        self.layout.addWidget(self.mouse_strain, 3, 2)
        self.layout.addWidget(self.anesthesia_protocol_label, 4, 0)
        self.layout.addWidget(self.anesthesia_protocol, 4, 1)
        self.layout.addWidget(self.comments, 5, 0, 1, 3)
        self.layout.addWidget(self.new_mouse_file_button, 6, 0, 1, 2)
        self.layout.setColumnStretch(7, 0)
        self.setLayout(self.layout)       
        
#class MasterPositionGroupBox(QtGui.QGroupBox):
#    def __init__(self, parent):        
#        QtGui.QGroupBox.__init__(self, 'Master position', parent)
#        self.create_widgets()
#        self.create_layout()
#        
#    def create_widgets(self):
#        self.z_stack_button = QtGui.QPushButton('Create Z stack',  self)
#        self.calculate_brain_surface_angle_button = QtGui.QPushButton('Calculate angle of brain surface',  self)
#        self.brain_surface_angle_display = QtGui.QComboBox(self)
#        self.brain_surface_angle_display.setEditable(True)
#        self.rotate_mouse_button = QtGui.QPushButton('Rotate mouse',  self)
#        self.save_master_position_button = QtGui.QPushButton('Save master position',  self)        
#        
#    def create_layout(self):
#        self.layout = QtGui.QGridLayout()
#        self.layout.addWidget(self.z_stack_button, 0, 1)
#        self.layout.addWidget(self.calculate_brain_surface_angle_button, 0, 2)
#        self.layout.addWidget(self.brain_surface_angle_display, 0, 3, 1, 1)
#        self.layout.addWidget(self.rotate_mouse_button, 0, 4)
#        self.layout.addWidget(self.save_master_position_button, 0, 5)
#        self.setLayout(self.layout)
        
class NewScanRegion(QtGui.QGroupBox):
    def __init__(self, parent, experiment_names):
        QtGui.QGroupBox.__init__(self, 'Add new scan region', parent)
        self.experiment_names = QtCore.QStringList(experiment_names)
        self.create_widgets()
        self.create_layout()

    def create_widgets(self):
        self.name_input = QtGui.QComboBox(self) #This combo box is to be updated with the added items
        self.name_input.setEditable(True)
        self.add_button = QtGui.QPushButton('Add',  self)
        self.z_stack_button = QtGui.QPushButton('Create Z stack',  self)
        self.experiment_name = QtGui.QComboBox(self)
        self.experiment_name.setEditable(True)
        self.experiment_name.addItems(self.experiment_names)
        self.start_experiment_button = QtGui.QPushButton('Start experiment',  self)
        self.stop_experiment_button = QtGui.QPushButton('Stop experiment',  self)
        self.save_experiment_results_button = QtGui.QPushButton('Save experiment results',  self)
        self.save_region_info_button = QtGui.QPushButton('Save region info',  self)
        
    def create_layout(self):
        self.layout = QtGui.QGridLayout()
        self.layout.addWidget(self.name_input, 0, 0)
        self.layout.addWidget(self.add_button, 0, 1)
        self.layout.addWidget(self.z_stack_button, 0, 2)
        self.layout.addWidget(self.experiment_name, 1, 0)
        self.layout.addWidget(self.start_experiment_button, 1, 1)
        self.layout.addWidget(self.stop_experiment_button, 1, 2)
        self.layout.addWidget(self.save_experiment_results_button, 1, 3)
        self.layout.addWidget(self.save_region_info_button, 2, 0)
        self.setLayout(self.layout)
        
class NewMouseWidget(QtGui.QWidget):
    def __init__(self, parent, config):
        QtGui.QWidget.__init__(self, parent)
        self.config = config
        self.create_widgets()
        self.create_layout()
        self.resize(self.config.GUI_SIZE['col'], self.config.GUI_SIZE['row'])
        
    def create_widgets(self):
        self.animal_parameters_groupbox = AnimalParametersGroupBox(self)
        self.master_position_groupbox = MasterPositionGroupBox(self)
        self.new_scan_region_groupbox = NewScanRegion(self, ['moving_dot', 'grating'])        
        
    def create_layout(self):
        self.layout = QtGui.QGridLayout()
        self.layout.addWidget(self.animal_parameters_groupbox, 0, 0, 1, 2)        
        self.layout.addWidget(self.master_position_groupbox, 2, 0, 1, 3)
        self.layout.addWidget(self.new_scan_region_groupbox, 3, 0, 1, 3)        
#        self.layout.setRowStretch(3, 300)
        self.setLayout(self.layout)

################### Registered mouse widget #######################
class FindMasterPositionGroupBox(QtGui.QGroupBox):
    def __init__(self, parent):        
        QtGui.QGroupBox.__init__(self, 'Find master position', parent)
        self.create_widgets()
        self.create_layout()
        
    def create_widgets(self):
        self.z_stack_button = QtGui.QPushButton('Create Z stack',  self)        
        self.calculate_position_offset_button = QtGui.QPushButton('Calculate position offset',  self)
        self.position_offset_display = QtGui.QComboBox(self)
        self.position_offset_display.setEditable(True)
        self.move_mouse_button = QtGui.QPushButton('Move mouse',  self)
        self.save_master_position_button = QtGui.QPushButton('Save master position',  self)        
        
    def create_layout(self):
        self.layout = QtGui.QGridLayout()
        self.layout.addWidget(self.z_stack_button, 0, 1)
        self.layout.addWidget(self.calculate_position_offset_button, 0, 2)
        self.layout.addWidget(self.position_offset_display, 0, 3, 1, 1)
        self.layout.addWidget(self.move_mouse_button, 0, 4)
        self.layout.addWidget(self.save_master_position_button, 0, 5)
        self.setLayout(self.layout)
       
class FindScanRegion(QtGui.QGroupBox):
    def __init__(self, parent, experiment_names):
        QtGui.QGroupBox.__init__(self, 'Find scan region', parent)
        self.experiment_names = QtCore.QStringList(experiment_names)
        self.create_widgets()
        self.create_layout()

    def create_widgets(self):
        self.select_scan_region = QtGui.QComboBox(self)
        self.select_scan_region.setEditable(True)
        self.move_mouse_button = QtGui.QPushButton('Move mouse',  self)
        self.add_button = QtGui.QPushButton('Add new',  self)
        self.z_stack_button = QtGui.QPushButton('Create Z stack',  self)
        self.calculate_position_offset_button = QtGui.QPushButton('Calculate position offset',  self)
        self.experiment_name = QtGui.QComboBox(self)
        self.experiment_name.setEditable(True)
        self.experiment_name.addItems(self.experiment_names)
        self.start_experiment_button = QtGui.QPushButton('Start experiment',  self)
        self.stop_experiment_button = QtGui.QPushButton('Stop experiment',  self)
        self.save_experiment_results_button = QtGui.QPushButton('Save experiment results',  self)
        self.save_region_info_button = QtGui.QPushButton('Save region info',  self)
        
    def create_layout(self):
        self.layout = QtGui.QGridLayout()
        self.layout.addWidget(self.select_scan_region, 0, 0)
        self.layout.addWidget(self.add_button, 0, 1)
        self.layout.addWidget(self.save_region_info_button, 0, 3)
        self.layout.addWidget(self.move_mouse_button, 0, 2, 2, 1)
        self.layout.addWidget(self.z_stack_button, 1, 0)
        self.layout.addWidget(self.calculate_position_offset_button, 1, 1)
        self.layout.addWidget(self.experiment_name, 2, 0)
        self.layout.addWidget(self.start_experiment_button, 2, 1)
        self.layout.addWidget(self.stop_experiment_button, 2, 2)
        self.layout.addWidget(self.save_experiment_results_button, 2, 3)       
        self.setLayout(self.layout)
       
class RegisteredMouseWidget(QtGui.QWidget):
    def __init__(self, parent, config):
        QtGui.QWidget.__init__(self, parent)
        self.config = config
        self.create_widgets()
        self.create_layout()
        self.resize(self.config.GUI_SIZE['col'], self.config.GUI_SIZE['row'])
        
    def create_widgets(self):
        self.select_mouse_file_label = QtGui.QLabel('Select mouse file', self)
        self.select_mouse_file = QtGui.QComboBox(self)
        self.find_master_position_groupbox = FindMasterPositionGroupBox(self)
        self.find_scan_region = FindScanRegion(self, ['moving_dot', 'grating'])
        
    def create_layout(self):
        self.layout = QtGui.QGridLayout()
        self.layout.addWidget(self.select_mouse_file_label, 0, 0, 1, 1)
        self.layout.addWidget(self.select_mouse_file, 0, 1, 1, 1)
        self.layout.addWidget(self.find_master_position_groupbox, 1, 0, 1, 2)
        self.layout.addWidget(self.find_scan_region, 2, 0, 1, 3)
        self.layout.setRowStretch(3, 3)
        self.layout.setColumnStretch(3, 3)
        self.setLayout(self.layout)
        
################### Debug/helper widgets #######################
class DebugWidget(QtGui.QWidget):
    def __init__(self, parent, config):
        QtGui.QWidget.__init__(self, parent)
        self.config = config
        #generate connection name list
        self.connection_names = ['']
        for k, v in self.config.COMMAND_RELAY_SERVER['CONNECTION_MATRIX'].items():
            if 'GUI' in k:
                self.connection_names.append(k.replace('GUI', '').replace('_', '').lower())
        self.create_widgets()
        self.create_layout()
        self.resize(self.config.GUI_SIZE['col'], self.config.GUI_SIZE['row'])
        
        
    def create_widgets(self):
        #MES related
        self.z_stack_button = QtGui.QPushButton('Create Z stack', self)
        self.line_scan_button = QtGui.QPushButton('Line scan', self)
        self.rc_scan_button = QtGui.QPushButton('RC scan point', self)
        self.rc_scan_point = QtGui.QComboBox(self)
        self.rc_scan_point.setEditable(True)
        #Stimulation/experiment control related
        self.experiment_name = QtGui.QComboBox(self)
        self.experiment_name.setEditable(True)
        self.experiment_name.addItems(QtCore.QStringList(['moving_dot', 'grating', 'led stimulation']))
        self.start_experiment_button = QtGui.QPushButton('Start experiment',  self)
        self.stop_experiment_button = QtGui.QPushButton('Stop experiment',  self)
        #Stage related
        self.set_stage_origin_button = QtGui.QPushButton('set stage origin', self)
        self.read_stage_button = QtGui.QPushButton('read stage', self)
        self.move_stage_button = QtGui.QPushButton('move stage', self)
        self.move_stage_to_origin_button = QtGui.QPushButton('move to origin', self)
        self.current_position_label = QtGui.QLabel('', self)
        #Network related
        self.show_connected_clients_button = QtGui.QPushButton('Show connected clients',  self)
        self.show_network_messages_button = QtGui.QPushButton('Show network messages',  self)
        self.select_connection_list = QtGui.QComboBox(self)        
        self.select_connection_list.addItems(QtCore.QStringList(self.connection_names))
        self.send_command_button = QtGui.QPushButton('Send command',  self)
        
        #Development
        self.animal_parameters_groupbox = AnimalParametersGroupBox(self)
        self.scan_region_groupbox = ScanRegionGroupBox(self)
        self.set_objective_button = QtGui.QPushButton('set objective', self)
        self.objective_position_label = QtGui.QLabel('', self)
        #Helpers
        self.save_two_photon_image_button = QtGui.QPushButton('Save two photon image',  self)
        
    def create_layout(self):
        self.layout = QtGui.QGridLayout()
        self.layout.addWidget(self.z_stack_button, 0, 0, 1, 1)
        self.layout.addWidget(self.line_scan_button, 0, 1, 1, 1)
        self.layout.addWidget(self.rc_scan_button, 0, 2, 1, 1)
        self.layout.addWidget(self.rc_scan_point, 0, 3, 1, 2)
        self.layout.addWidget(self.experiment_name, 1, 0, 1, 1)
        self.layout.addWidget(self.start_experiment_button, 1, 1, 1, 1)
        self.layout.addWidget(self.stop_experiment_button, 1, 2, 1, 1)
        self.layout.addWidget(self.set_stage_origin_button, 2, 0, 1, 1)
        self.layout.addWidget(self.read_stage_button, 2, 1, 1, 1)
        self.layout.addWidget(self.move_stage_button, 2, 2, 1, 1)
        self.layout.addWidget(self.move_stage_to_origin_button, 2, 3, 1, 1)
        self.layout.addWidget(self.current_position_label, 2, 4, 1, 3)
        self.layout.addWidget(self.set_objective_button, 2, 7, 1, 1)
        self.layout.addWidget(self.objective_position_label, 2, 8, 1, 1)
        self.layout.addWidget(self.show_connected_clients_button, 3, 0, 1, 1)
        self.layout.addWidget(self.show_network_messages_button, 3, 1, 1, 1)
        self.layout.addWidget(self.select_connection_list, 3, 2, 1, 1)
        self.layout.addWidget(self.send_command_button, 3, 3, 1, 1)
        self.layout.addWidget(self.animal_parameters_groupbox, 4, 0, 4, 4)
        self.layout.addWidget(self.scan_region_groupbox, 4, 5, 3, 4)
        
        self.layout.addWidget(self.save_two_photon_image_button, 8, 0, 1, 1)
        
        self.layout.setRowStretch(10, 10)
        self.layout.setColumnStretch(10, 10)
        self.setLayout(self.layout)
        
class MasterPositionGroupBox(QtGui.QGroupBox):
    def __init__(self, parent):
        QtGui.QGroupBox.__init__(self, 'Master position', parent)
        self.create_widgets()
        self.create_layout()
        
    def create_widgets(self):
        self.get_two_photon_image_button = QtGui.QPushButton('Get two photon image',  self)
        self.use_master_position_scan_settings_label = QtGui.QLabel('Use master position\'s scan settings', self)
        self.use_master_position_scan_settings_checkbox = QtGui.QCheckBox(self)
        self.select_mouse_file_label = QtGui.QLabel('Select mouse file', self)
        self.select_mouse_file = QtGui.QComboBox(self)      
        self.register_button = QtGui.QPushButton('Register',  self)
        self.move_to_master_position_button = QtGui.QPushButton('Move to  master position',  self)
        self.save_master_position_button = QtGui.QPushButton('Save master position',  self)
        
    def create_layout(self):
        self.layout = QtGui.QGridLayout()
        self.layout.addWidget(self.get_two_photon_image_button, 0, 0, 1, 1)
        self.layout.addWidget(self.use_master_position_scan_settings_label, 0, 1, 1, 1)
        self.layout.addWidget(self.use_master_position_scan_settings_checkbox, 0, 2, 1, 1)
        self.layout.addWidget(self.select_mouse_file_label, 1, 0, 1, 1)
        self.layout.addWidget(self.select_mouse_file, 1, 1, 1, 2)      
        self.layout.addWidget(self.register_button, 4, 0, 1, 1)
        self.layout.addWidget(self.move_to_master_position_button, 5, 1, 1, 1)
        self.layout.addWidget(self.save_master_position_button, 5, 0, 1, 1)
        self.layout.setRowStretch(10, 10)
        self.layout.setColumnStretch(10, 10)
        self.setLayout(self.layout)

class ScanRegionGroupBox(QtGui.QGroupBox):
    def __init__(self, parent):
        QtGui.QGroupBox.__init__(self, 'Scan regions', parent)
        self.create_widgets()
        self.create_layout()

    def create_widgets(self):
        self.select_mouse_file_label = QtGui.QLabel('Select mouse file', self)
        self.select_mouse_file = QtGui.QComboBox(self)
        self.get_two_photon_image_button = QtGui.QPushButton('Get two photon image',  self)
        self.use_saved_scan_settings_label = QtGui.QLabel('Use saved scan settings', self)
        self.use_saved_scan_settings_settings_checkbox = QtGui.QCheckBox(self)
        self.snap_brain_surface_button = QtGui.QPushButton('Snap brain surface',  self)
        
        self.add_button = QtGui.QPushButton('Add',  self)
        self.scan_regions_combobox = QtGui.QComboBox(self)
        self.scan_regions_combobox.setEditable(True)
        self.remove_button = QtGui.QPushButton('Remove',  self)
        
        self.move_to_button = QtGui.QPushButton('Move to',  self)
        self.region_position = QtGui.QLabel('',  self)
        self.register_button = QtGui.QPushButton('Register',  self)
        self.realign_button = QtGui.QPushButton('Realign',  self)

        #Vertical alignment
        self.vertical_scan_button = QtGui.QPushButton('Vertical scan',  self)
        self.move_to_focus_button = QtGui.QPushButton('Focus',  self)
        self.move_to_brain_surface_button = QtGui.QPushButton('Brain surface',  self)

    def create_layout(self):
        self.layout = QtGui.QGridLayout()
        
        self.layout.addWidget(self.select_mouse_file_label, 0, 0, 1, 1)
        self.layout.addWidget(self.select_mouse_file, 0, 1, 1, 3)
        self.layout.addWidget(self.use_saved_scan_settings_label, 1, 1, 1, 1)
        self.layout.addWidget(self.use_saved_scan_settings_settings_checkbox, 1, 2, 1, 1)
        
        self.layout.addWidget(self.get_two_photon_image_button, 2, 0, 1, 1)
        self.layout.addWidget(self.snap_brain_surface_button, 2, 3, 1, 1)
        
        self.layout.addWidget(self.add_button, 3, 0, 1, 1)
        self.layout.addWidget(self.scan_regions_combobox, 3, 1, 1, 2)
        self.layout.addWidget(self.remove_button, 3, 3, 1, 1)
        self.layout.addWidget(self.move_to_button, 4, 1, 1, 1)
        self.layout.addWidget(self.region_position, 4, 2, 1, 2)
        self.layout.addWidget(self.register_button, 5, 0, 1, 1)
        self.layout.addWidget(self.realign_button, 5, 1, 1, 1)
        
        self.layout.addWidget(self.vertical_scan_button, 6, 0, 1, 1)
        self.layout.addWidget(self.move_to_focus_button, 7, 0, 1, 1)
        self.layout.addWidget(self.move_to_brain_surface_button, 7, 1, 1, 1)

        self.layout.setRowStretch(10, 10)
        self.layout.setColumnStretch(10, 10)
        self.setLayout(self.layout)

class StandardIOWidget(QtGui.QWidget):
    def __init__(self, parent, config):
        QtGui.QWidget.__init__(self, parent)
        self.config = config
        self.create_widgets()
        self.create_layout()
        self.resize(self.config.GUI_SIZE['col'], 0.5*self.config.GUI_SIZE['row'])
        
    def create_widgets(self):
        self.text_out = QtGui.QTextEdit(self)
        self.text_out.setPlainText('')
        self.text_out.setReadOnly(True)
        self.text_out.ensureCursorVisible()
        self.text_out.setCursorWidth(5)
        self.text_in = QtGui.QTextEdit(self)
        self.text_in.setToolTip('self.printc()')
        
        self.execute_python_button = QtGui.QPushButton('Execute python code',  self)
        self.clear_console_button = QtGui.QPushButton('Clear console',  self)
        
    def create_layout(self):
        self.layout = QtGui.QGridLayout()
        self.layout.addWidget(self.text_out, 0, 0, 3, 3)
        self.layout.addWidget(self.text_in, 1, 3, 1, 2)
        self.layout.addWidget(self.execute_python_button, 0, 3, 1, 1)#, alignment = QtCore.Qt.AlignTop)
        self.layout.addWidget(self.clear_console_button, 0, 4, 1, 1)#, alignment = QtCore.Qt.AlignTop)
        self.layout.setRowStretch(300, 300)
        self.layout.setColumnStretch(0, 100)
        self.setLayout(self.layout)
        
class Poller(QtCore.QThread):
    def __init__(self, parent):
        self.parent = parent
        self.config = self.parent.config
        QtCore.QThread.__init__(self)
        self.abort = False
        self.parent.connect(self, QtCore.SIGNAL('printc'),  self.parent.printc)
        self.parent.connect(self, QtCore.SIGNAL('update_gui'),  self.parent.update_gui_items)
    
    def abort_poller(self):
        self.abort = True

    def printc(self, text):
        self.emit(QtCore.SIGNAL('printc'), text)
        
    def run(self):
        self.printc('poller starts')
        last_time = time.time()
        while not self.abort:
            now = time.time()
            elapsed_time = now - last_time
            if elapsed_time > self.config.GUI_REFRESH_PERIOD:
                last_time = now
                self.periodic()
            time.sleep(1e-2)
        self.printc('poller stopped')
        
    def periodic(self):
        self.emit(QtCore.SIGNAL('update_gui'))
        
if __name__ == '__main__':
    pass
    