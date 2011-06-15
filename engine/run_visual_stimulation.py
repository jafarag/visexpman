import visexpman
import os
#While psychopy is not completely eliminated, this import is necessary under windows systems
if os.name == 'nt':
    from OpenGL.GL import *
    from OpenGL.GLUT import *
    
import visexpman
import generic.utils
import visual_stimulation.user_interface
import hardware_interface.udp_interface
import visual_stimulation.stimulation_control
import visual_stimulation.command_handler
import visual_stimulation.configuration
import visexpman.users as users


class UnsupportedCommandLineArguments(Exception):
    pass

class VisualStimulation(object):
    def __init__(self, config_class, user):
        '''
        Find out configuration and load the appropriate config and experiment modules, classes

		At the initialization the followings has to be accomplised:
        - find config class and instantiate it 
        - instantiate user interface, udp, stimulation control and command handler
        - create experiment list containing all the experiment classes residing in user folder
        - instantiate pre experiment config and pre experiment
        - experiment has to be instantiated in stimulation control not here!!!!     

        '''
        self.config=generic.utils.fetch_classes('visexpman.users.'+user, classname=config_class, classtype=visexpman.engine.visual_stimulation.configuration.VisualStimulationConfig)[0][1]()
        self.config.user=user
        #Lists all folders and python modules residing in the user's folder
        # this way of discovering classes has the drawback that modules searched must not have syntax errors
        classname = self.config.EXPERIMENT_CONFIG
        self.experiment_config_list = generic.utils.fetch_classes('visexpman.users.'+self.config.user,  classtype=visexpman.engine.visual_stimulation.experiment.ExperimentConfig)
        if len(self.experiment_config_list) > 10: raise RuntimeError('Maximum 10 different experiment types are allowed') 
        self.selected_experiment_config = [ex1[1] for ex1 in self.experiment_config_list if ex1[1].__name__ == self.config.EXPERIMENT_CONFIG][0](self.config) # select and instantiate stimulus as specified in machine config
        #create screen        
        self.user_interface = visual_stimulation.user_interface.UserInterface(self.config, self)
        #initialize network interface
        self.udp_interface = hardware_interface.udp_interface.UdpInterface(self.config)
        #initialize stimulation control
        self.stimulation_control = visual_stimulation.stimulation_control.StimulationControl(self, self.config,  self.user_interface,  self.udp_interface)
        #set up command handler
        self.command_handler =  visual_stimulation.command_handler.CommandHandler(self.config,  self.stimulation_control,  self.udp_interface,   self.user_interface)
        self.stimulation_control.runStimulation()

    def run(self):
        '''
        Run application. Check for commands coming from either keyboard or network. Command is parsed and handled by command handler
        '''        
        if self.config.RUN_MODE == 'single experiment':
                self.stimulation_control.runStimulation()
        elif self.config.RUN_MODE == 'user interface':
                while True:
                    #check command interfaces:
                    command_buffer = self.user_interface.user_interface_handler()
                    udp_command =  self.udp_interface.checkBuffer()
                    if udp_command != '':
                        self.udp_interface.send(udp_command + ' OK') 
                    command_buffer = command_buffer + udp_command
                    #parse commands
                    res = self.command_handler.parse(self.stimulation_control.state,  command_buffer)            
                    if res != 'no command executed':
                        self.user_interface.user_interface_handler(res)
                        if self.config.ENABLE_PRE_EXPERIMENT:
                            #rerun pre experiment
                            self.stimulation_control.runStimulation(self.config.PRE_EXPERIMENT)
                        if res == 'quit':
                            self.user_interface.close()
                            break
        else:
            print 'invalid run mode'
    
def find_out_config():
    '''
    Finds out configuration from the calling arguments. The following options are supported:
    - No argument: SafestartConfig is loaded
    - Username and config class name is encoded into one argument in the following form:
        user<separator>configclass, where separator can be: . , / \ <space> 
    - username and config class are provided as separate arguments
    '''        
    separators = [' ',  '.',  ',',  '/',  '\\']
    if len(sys.argv) == 1:
        config_class = 'SafestartConfig'
        user = ''
    elif len(sys.argv) == 2:
        for separator in separators:
            if sys.argv[1].find(separator) != -1:
                user = sys.argv[1].split(separator)[0]
                config_class = sys.argv[1].split(separator)[1]
    elif len(sys.argv) == 3:
        config_class = sys.argv[1]
        user = sys.argv[2]
    else:
        raise UnsupportedCommandLineArguments
    return config_class,  user

if __name__ == "__main__":    
    VisualStimulation(*find_out_config()).run()
