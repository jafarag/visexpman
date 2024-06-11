import os
import os.path
import numpy
import tempfile
try:
    import serial
except:
    pass
from visexpman.engine.generic import utils,fileop
from visexpman.engine.vision_experiment.configuration import HiMEAConfig,MCMEAConfig

class MEAConfig(HiMEAConfig):
    def _set_user_parameters(self):
        FULLSCREEN =not  True
        SCREEN_RESOLUTION = utils.cr([1280, 800])#TODO: adjust this to projector's native resolution
        #SCREEN_POSITION=utils.cr([1280, 0])#Temporary, for calibration
        SCREEN_UM_TO_PIXEL_SCALE = 1/8.7#TODO: calibrate. Press button 'b' and a 100 um sized bullseye is displayed
        SCREEN_EXPECTED_FRAME_RATEa = 60.0 # 30 for baccus stim switch back to 60 for everything else
        BACKGROUND_COLOR=[0.0, 0.0, 0.0]
        LOG_PATH = fileop.select_folder_exists(['e:\\stim_data\\log', '/tmp', 'c:\\stim_data\\log'])
        EXPERIMENT_LOG_PATH = LOG_PATH        
        EXPERIMENT_DATA_PATH = fileop.select_folder_exists(['e:\\stim_data', '/tmp', 'c:\\stim_data'])
        CONTEXT_PATH = LOG_PATH
        EXPERIMENT_FILE_FORMAT = 'mat'
        PLATFORM='standalone'
        COORDINATE_SYSTEM='center'
        DIGITAL_IO_PORT = 'COM4'
        FRAME_TIMING_PIN = 1#RTS pin (green)
        BLOCK_TIMING_PIN = 0#TX pin (orange)
        INSERT_FLIP_DELAY=False
        ALTERNATIVE_TIMING=False
        YOUSSEF_FLIP_DELAY='no'
        FRAME_WAIT_FACTOR = 1.0 # to change the frame wait factor from 0.9
        self._create_parameters_from_locals(locals())

class MEAConfigDebug(MEAConfig):
    def _set_user_parameters(self):
        MEAConfig._set_user_parameters(self)
        self.FULLSCREEN = False
