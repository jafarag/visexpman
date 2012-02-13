import time
import Queue
import os
import numpy
import traceback

import PyQt4.QtCore as QtCore

from visexpman.engine.generic import command_parser
from visexpman.engine.vision_experiment import screen
from visexpman.engine.generic import utils
from visexpman.engine.hardware_interface import network_interface
from visexpman.engine.hardware_interface import stage_control


class CommandHandler(command_parser.CommandParser, screen.ScreenAndKeyboardHandler):
    def __init__(self):
        self.keyboard_command_queue = Queue.Queue()
        #Here the set of queues are defined from commands are parsed
        queue_in = [self.queues['mes']['in'], self.queues['gui']['in'], self.keyboard_command_queue, self.queues['udp']['in']]
        #Set of queues where command parser output is relayed NOT YET IMPLEMENTED IN command_parser
        queue_out = self.queues['gui']['out']
        command_parser.CommandParser.__init__(self, queue_in, queue_out, log = self.log, failsafe = False)
        screen.ScreenAndKeyboardHandler.__init__(self)
        self.stage_origin = numpy.zeros(3)
        
###### Commands ######    
    def quit(self):
        if hasattr(self, 'loop_state'):
            self.loop_state = 'end loop'
        return 'quit'
        
    def bullseye(self):
        self.show_bullseye = not self.show_bullseye
        return 'bullseye'

    def color(self, color):
        self.user_background_color = int(color)
        return 'color'
        
    def hide_menu(self):
        self.hide_menu = not self.hide_menu
        if self.hide_menu:
            return ''
        else:
            return 'menu is unhidden'

    def echo(self, par=''):
        self.queues['mes']['out'].put('SOCechoEOCvisexpmanEOP')
        result = network_interface.wait_for_response(self.queues['mes']['in'], ['SOCechoEOCvisexpmanEOP'], timeout = self.config.MES_TIMEOUT)
        return 'echo ' + str(result)
        
    def filterwheel(self, filterwheel_id, filter_position):
        if hasattr(self.config, 'FILTERWHEEL_SERIAL_PORT'):            
            filterwheel = instrument.Filterwheel(self.config, id = filterwheel_id)
            filterwheel.set(filter_position)
            if os.name == 'nt':
                filterwheel.release_instrument()
        return 'filterwheel ' + par
        
    def stage(self,par):
        '''
        read stage:
            command: SOCstageEOCreadEOP
            response: SOCstageEOCx,y,zEOP
        set stage:
            command: SOCstageEOCset,y,zEOP
            response: SOCstageEOC<status>,x,y,zEOP, <status> = OK, error
        '''
        try:
            st = time.time()
            if 'read' in par or 'set' in par or 'origin' in par:
                stage = stage_control.AllegraStage(self.config, log = self.log)
                position = stage.read_position()
                if 'set' not in par:
                    self.queues['gui']['out'].put('SOCstageEOC{0},{1},{2}EOP'.format(position[0], position[1], position[2]))
                if 'origin' in par:
                    self.stage_origin = position                
                if 'set' in par:
                    new_position = par.split(',')[1:]
                    new_position = numpy.array([float(new_position[0]), float(new_position[1]), float(new_position[2])])
                    reached = stage.move(new_position)
                    position = stage.position
                    self.queues['gui']['out'].put('SOCstageEOC{0},{1},{2}EOP'.format(position[0], position[1], position[2]))
                stage.release_instrument()
            return str(par) + ' ' + str(position) + '\n' + str(time.time() - st) + ' ' + str(stage.command_counter )
        except:
            return str(traceback.format_exc())
            
###### Experiment related commands ###############

    def select_experiment(self, experiment_index):
        '''
        Selects experiment config based on keyboard command and instantiates the experiment config class
        '''
        self.selected_experiment_config_index = int(experiment_index)
        self.experiment_config = self.experiment_config_list[int(self.selected_experiment_config_index)][1](self.config, self.queues, self.connections, self.log)
        return 'selected experiment: ' + str(experiment_index) + ' '
        
    def execute_experiment(self, source_code = ''):
        if source_code == '':
            self.experiment_config = self.experiment_config_list[int(self.selected_experiment_config_index)][1](self.config, self.queues, self.connections, self.log)
        else:
            self.experiment_config = None#TODO: instantiate class from string
        context = {}
        context['stage_origin'] = self.stage_origin
        return self.experiment_config.runnable.run_experiment(context)
        
class CommandSender(QtCore.QThread):
    def __init__(self, config, caller, commands):
        self.config = config
        self.caller = caller
        self.commands = commands
        QtCore.QThread.__init__(self)
        
    def send_command(self, command):
        self.caller.keyboard_command_queue.put(command)
        
    def run(self):
        for command in self.commands:
            time.sleep(command[0])
            self.send_command(command[1])            

    def close(self):
        self.terminate()
        self.wait()