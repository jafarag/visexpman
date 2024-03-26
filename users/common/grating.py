from visexpman.engine.generic import utils
from visexpman.engine.vision_experiment import experiment
            
class MovingGrating(experiment.Stimulus):
    def configuration(self):
        self.SPEED=1600#um/s on retina
        self.DIRECTIONS=[0,45, 90, 135, 180, 225, 270, 315]
        self.STAND_TIME=1.0#Static grating is displayed for this duration first
        self.SWEEP_TIME=6.0#Then moving grating is presented for this duration
        self.BAR_WIDTH=2000.0#um
        self.DUTY_CYCLE=50.0#in percent
        self.COLOR=1.0
        self.BACKGROUND=0.0
        self.WAIT=0.5#wait time in seconds at beginning and end of stimulus
        self.REPETITIONS=2
#Do not edit below this!

    def run(self):
        self.show_fullscreen(color=self.BACKGROUND, duration=self.WAIT)
        for r in range(self.REPETITIONS):
            for d in self.DIRECTIONS:
                self.printl(self.frame_counter)
                self.show_grating(duration = self.STAND_TIME, white_bar_width = self.BAR_WIDTH,   
                                    duty_cycle=1.0/(1e-2*self.DUTY_CYCLE)-1,
                                    orientation = d, velocity = 0,  color_offset = 0.5*self.COLOR+self.BACKGROUND, 
                                    color_contrast = self.COLOR)  
                self.printl(self.frame_counter)
                self.block_start(('sweep', d))
                self.show_grating(duration = self.SWEEP_TIME,  white_bar_width = self.BAR_WIDTH,   
                                    duty_cycle=1.0/(1e-2*self.DUTY_CYCLE)-1,
                                    orientation = d, velocity = self.SPEED,  color_offset = 0.5*self.COLOR+self.BACKGROUND, 
                                    color_contrast = self.COLOR)
                self.printl(self.frame_counter)
                self.block_end()
        self.show_fullscreen(color=self.BACKGROUND, duration=self.WAIT)                

if __name__ == "__main__":
    from visexpman.applications.visexpman_main import stimulation_tester
    from visexpman.engine.generic import fileop
    stimulation_tester('zoltan', 'StimulusDevelopment', 'MovingGrating',experiment_config_source_code=fileop.read_text_file(__file__))
