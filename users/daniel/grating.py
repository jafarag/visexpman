from visexpman.users.zoltan.test import unit_test_runner
from visexpman.engine.generic.parameter import Parameter
from visexpman.engine.vision_experiment.configuration import VisionExperimentConfig
from visexpman.engine.hardware_interface import daq_instrument
from visexpman.engine.vision_experiment import experiment
from visexpman.engine.generic import utils
from visexpman.engine.generic import timing
import os
import serial
import numpy
import time
import shutil
import random
import copy

class MovingGratingConfig(experiment.ExperimentConfig):
    def _create_parameters(self):
        #Timing        
        self.NUMBER_OF_MARCHING_PHASES = 4
        self.NUMBER_OF_BAR_ADVANCE_OVER_POINT = 3
        self.MARCH_TIME = 2.5#3.0
        self.GRATING_STAND_TIME = 2.0#1.0        
        #Grating parameters
        self.ORIENTATIONS = range(0, 360, 45)
        self.WHITE_BAR_WIDTHS = [300.0]#300
        self.VELOCITIES = [1200.0]#1800
        self.DUTY_CYCLES = [3.0] #put 1.0 to a different config
        self.REPEATS = 3
        self.PAUSE_BEFORE_AFTER = 5.0
        self.runnable = 'MovingGrating'
        self.pre_runnable = 'MovingGratingPre'
        self._create_parameters_from_locals(locals())
        
class QuickStimulationMovingGratingConfig(experiment.ExperimentConfig):
    def _create_parameters(self):
        #Timing
        self.NUMBER_OF_MARCHING_PHASES = 3
        self.NUMBER_OF_BAR_ADVANCE_OVER_POINT = 3
        self.MARCH_TIME = 1.0
        self.GRATING_STAND_TIME = 1.0
        #Grating parameters
        self.ORIENTATIONS = range(0, 360, 90)
        self.WHITE_BAR_WIDTHS = [300.0]#300
        self.VELOCITIES = [1200.0]#1800
        self.DUTY_CYCLES = [3.0] #put 1.0 to a different config
        self.REPEATS = 2
        self.PAUSE_BEFORE_AFTER = 0.0
        self.runnable = 'MovingGrating'
        self.pre_runnable = 'MovingGratingPre'
        self._create_parameters_from_locals(locals())

class ShortMovingGratingConfig(experiment.ExperimentConfig):
    def _create_parameters(self):
        #Timing
        self.NUMBER_OF_MARCHING_PHASES = 1
        self.NUMBER_OF_BAR_ADVANCE_OVER_POINT = 1
        self.MARCH_TIME = 0.5
        self.GRATING_STAND_TIME = 0.5
        #Grating parameters        
        self.ORIENTATIONS = [0]
        self.WHITE_BAR_WIDTHS = [300.0]#300
        self.VELOCITIES = [1800.0]#1800
        self.DUTY_CYCLES = [3.0] #put 1.0 to a different config
        self.REPEATS = 1
        self.PAUSE_BEFORE_AFTER = 0.0
        self.runnable = 'MovingGrating'
        self.pre_runnable = 'MovingGratingPre'
        self._create_parameters_from_locals(locals())
        
class MovingGrating(experiment.Experiment):
    def prepare(self):
        self.marching_phases = -numpy.linspace(0, 360, self.experiment_config.NUMBER_OF_MARCHING_PHASES + 1)[:-1]        
        self.stimulus_units = []
        self.overall_duration = 0
        orientations = copy.deepcopy(self.experiment_config.ORIENTATIONS)
        for repeat in range(self.experiment_config.REPEATS):
            for white_bar_width in self.experiment_config.WHITE_BAR_WIDTHS:
                for velocity in self.experiment_config.VELOCITIES:
                    for duty_cycle in self.experiment_config.DUTY_CYCLES:
                        if repeat > 0:
                            random.shuffle(orientations)
                        for orientation in orientations:
                            stimulus_unit = {}
                            stimulus_unit['white_bar_width'] = white_bar_width
                            stimulus_unit['velocity'] = velocity
                            stimulus_unit['duty_cycle'] = duty_cycle
                            stimulus_unit['orientation'] = orientation
                            period_length = (duty_cycle + 1) * white_bar_width
                            required_movement = period_length * self.experiment_config.NUMBER_OF_BAR_ADVANCE_OVER_POINT
                            stimulus_unit['move_time'] = float(required_movement) / velocity
                            #round it to the multiple of frame rate
                            stimulus_unit['move_time'] = \
                                        numpy.round(stimulus_unit['move_time'] * self.machine_config.SCREEN_EXPECTED_FRAME_RATE) / self.machine_config.SCREEN_EXPECTED_FRAME_RATE
                            self.overall_duration += stimulus_unit['move_time'] + self.experiment_config.NUMBER_OF_MARCHING_PHASES * self.experiment_config.MARCH_TIME + self.experiment_config.GRATING_STAND_TIME
                            self.stimulus_units.append(stimulus_unit)
                    
        
#         self.overall_duration *= len(self.experiment_config.ORIENTATIONS)
        self.period_time = self.overall_duration / self.experiment_config.REPEATS
        if self.period_time > self.machine_config.MAXIMUM_RECORDING_DURATION:
            raise RuntimeError('Stimulus too long')
        self.fragment_durations = [self.period_time*self.experiment_config.REPEATS + 2 * self.experiment_config.PAUSE_BEFORE_AFTER] 
        self.number_of_fragments = len(self.fragment_durations)
        #Group stimulus units into fragments
        segment_pointer = 0
        self.fragmented_stimulus_units = [self.stimulus_units]
        self.experiment_specific_data = {}

    def run(self, fragment_id = 0):
        frame_counter = 0
        segment_counter = 0
        self.experiment_specific_data['segment_info'] = {} 
        is_first_dislayed = False
        for stimulus_unit in self.fragmented_stimulus_units[fragment_id]:
                #Show marching grating
                orientation = stimulus_unit['orientation']
                for phase in self.marching_phases:
                    if not is_first_dislayed:
                        is_first_dislayed = True
                        static_grating_duration = self.experiment_config.PAUSE_BEFORE_AFTER + self.experiment_config.MARCH_TIME
                    else:
                        static_grating_duration = self.experiment_config.MARCH_TIME
                    self.show_grating(duration = static_grating_duration, 
                            orientation = orientation, 
                            velocity = 0, white_bar_width = stimulus_unit['white_bar_width'],
                            duty_cycle = stimulus_unit['duty_cycle'],
                            starting_phase = phase)
                #Show moving grating
                self.show_grating(duration = stimulus_unit['move_time'], 
                            orientation = orientation, 
                            velocity = stimulus_unit['velocity'], white_bar_width = stimulus_unit['white_bar_width'],
                            duty_cycle = stimulus_unit['duty_cycle'])
                #Show static grating
                self.show_grating(duration = self.experiment_config.GRATING_STAND_TIME, 
                            orientation = orientation, 
                            velocity = 0, white_bar_width = stimulus_unit['white_bar_width'],
                            duty_cycle = stimulus_unit['duty_cycle'])
                #Save segment info to help synchronizing stimulus with measurement data
                segment_info = {}
                segment_info['fragment_id'] = fragment_id
                segment_info['orientation'] = orientation
                segment_info['velocity'] = stimulus_unit['velocity']
                segment_info['white_bar_width'] = stimulus_unit['white_bar_width']
                segment_info['duty_cycle'] = stimulus_unit['duty_cycle']
                segment_info['marching_phases'] = self.marching_phases
                segment_info['marching_start_frame'] = frame_counter
                frame_counter += int(self.experiment_config.NUMBER_OF_MARCHING_PHASES * self.experiment_config.MARCH_TIME * self.machine_config.SCREEN_EXPECTED_FRAME_RATE)
                segment_info['moving_start_frame'] = frame_counter
                frame_counter += int(stimulus_unit['move_time'] * self.machine_config.SCREEN_EXPECTED_FRAME_RATE)
                segment_info['standing_start_frame'] = frame_counter
                frame_counter += int(self.experiment_config.GRATING_STAND_TIME * self.machine_config.SCREEN_EXPECTED_FRAME_RATE)
                segment_info['standing_last_frame'] = frame_counter-1
                segment_id = 'segment_{0:3.0f}' .format(segment_counter)
                segment_id = segment_id.replace(' ', '0')
                self.experiment_specific_data['segment_info'][segment_id] = segment_info
                segment_counter += 1
        time.sleep(self.experiment_config.PAUSE_BEFORE_AFTER)

    def cleanup(self):
        #add experiment identifier node to experiment hdf5
        experiment_identifier = '{0}_{1}'.format(self.experiment_name, int(self.experiment_control.start_time))
        self.experiment_hdf5_path = os.path.join(self.machine_config.EXPERIMENT_DATA_PATH, experiment_identifier + '.hdf5')
        setattr(self.hdf5, experiment_identifier, {'id': None})
        self.hdf5.save(experiment_identifier)
                
class MovingGratingPre(experiment.PreExperiment):    
    def run(self):
        self.show_grating(duration = 0, 
                            orientation = self.experiment_config.ORIENTATIONS[0], 
                            velocity = 0, white_bar_width = self.experiment_config.WHITE_BAR_WIDTHS[0],
                            duty_cycle = self.experiment_config.DUTY_CYCLES[0], part_of_drawing_sequence = True)

class PixelSizeCalibrationConfig(experiment.ExperimentConfig):
    def _create_parameters(self):
        self.runnable = 'PixelSizeCalibration'
        self._create_parameters_from_locals(locals())

class PixelSizeCalibration(experiment.Experiment):
    '''
    Helps pixel size calibration by showing 50 and 20 um circles
    '''
    def prepare(self):
        self.fragment_durations = [1.0]
        self.number_of_fragments = len(self.fragment_durations)

    def run(self):
        pattern = 0
        self.add_text('Circle at 100,100 um, diameter is 20 um.', color = (1.0,  0.0,  0.0), position = utils.cr((10.0, 30.0)))        
        while True:
            if pattern == 0:
                self.change_text(0, text = 'Circle at 100,100 um, diameter is 20 um.\n\nPress \'n\' to switch, \'s\' to stop.')
                self.show_shape(shape = 'circle', size = 20.0, pos = utils.cr((100, 100)))
            elif pattern == 1:
                self.change_text(0, text = 'Circle at 50,50 um, diameter is 50 um.\n\nPress \'n\' to switch, \'s\' to stop.')
                self.show_shape(shape = 'circle', size = 50.0, pos = utils.cr((50, 50)))
            else:
                pass
            if 'stop' in self.command_buffer:
                break
            elif 'next' in self.command_buffer:
                pattern += 1
                if pattern == 2:
                    pattern = 0
                self.command_buffer = ''
                
class LedStimulationConfig(experiment.ExperimentConfig):
    def _create_parameters(self):
        self.PAUSE_BETWEEN_FLASHES = 60.0 #10.0
        self.NUMBER_OF_FLASHES = 5.0
        self.FLASH_DURATION = 100e-3
        self.FLASH_AMPLITUDE = 10.0 #10.0
        self.DELAY_BEFORE_FIRST_FLASH = 15.0
        self.runnable = 'LedStimulation'
        self.pre_runnable = 'LedPre'
        self._create_parameters_from_locals(locals())
        
class LedPre(experiment.PreExperiment):
    def run(self):
        self.show_fullscreen(color = 0.0, duration = 0.0, flip = False)
                
class LedStimulation(experiment.Experiment):
    '''
    
    '''
    def prepare(self):
        self.period_time = self.experiment_config.FLASH_DURATION + self.experiment_config.PAUSE_BETWEEN_FLASHES
        self.stimulus_duration = self.experiment_config.NUMBER_OF_FLASHES * self.period_time
        self.fragment_durations, self.fragment_repeats = timing.schedule_fragments(self.period_time, self.experiment_config.NUMBER_OF_FLASHES, self.machine_config.MAXIMUM_RECORDING_DURATION)
        self.number_of_fragments = len(self.fragment_durations)
    
    def run(self, fragment_id = 0):
        self.show_fullscreen(color = 0.0, duration = 0.0)
        time.sleep(self.experiment_config.DELAY_BEFORE_FIRST_FLASH)
        number_of_flashes_in_fragment = self.fragment_repeats[fragment_id]
        fragment_duration = self.fragment_durations[fragment_id]
        offsets = numpy.linspace(0, self.period_time * (number_of_flashes_in_fragment -1), number_of_flashes_in_fragment)
        self.led_controller.set([[offsets, self.experiment_config.FLASH_DURATION, self.experiment_config.FLASH_AMPLITUDE]], fragment_duration)
        self.led_controller.start()
        for i in range(int(numpy.ceil(fragment_duration))):
            if utils.is_abort_experiment_in_queue(self.queues['gui']['in']):
                break
            else:
                time.sleep(1.0)
        
    def cleanup(self):
        #add experiment identifier node to experiment hdf5
        experiment_identifier = '{0}_{1}'.format(self.experiment_name, int(self.experiment_control.start_time))
        self.experiment_hdf5_path = os.path.join(self.machine_config.EXPERIMENT_DATA_PATH, experiment_identifier + '.hdf5')
        setattr(self.hdf5, experiment_identifier, {'id': None})
        self.hdf5.save(experiment_identifier)

class Dummy(experiment.ExperimentConfig):
    def _create_parameters(self):     
        self.runnable = 'DummyExp'
        self._create_parameters_from_locals(locals())
        
class DummyExp(experiment.Experiment):
    
    def prepare(self):
        self.fragment_durations = [1.0]
        self.number_of_fragments = len(self.fragment_durations)

    def run(self, fragment_id=0):
        pass
