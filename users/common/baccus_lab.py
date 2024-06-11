from visexpman.engine.vision_experiment import experiment
from visexpman.engine.generic import utils
import os

# class TemplateExperimentConfig(experiment.ExperimentConfig):
#     def _create_application_parameters(self):
#         #place for experiment parameters
#         #parameter with range: list[0] - value, list[1] - range
#         #path parameter: parameter name contains '_PATH'
#         #string list: list[1] - empty        
#         PARAMETER = 'dummy'
#         self._create_parameters_from_locals(locals())
        

class BaccusLabExperiment(experiment.Stimulus):
    def configuration(self):
        self.PIXEL_SIZE =50.0#um
        self.ILLUMINATED_AREA=1000#um
        self.BACKGROUND=0.5
        self.WAIT=100e-3#wait time in seconds at beginning and end of stimulus
        self.COLORS = [0.0, 1.0]
        self.DURATION = 0.4161
        self.config.SCREEN_EXPECTED_FRAME_RATE = 30
        self.config.YOUSSEF_FLIP_DELAY == 'no'
#Do not edit below this!
 
    def run(self):
        #accessing an experiment parameter
        epoch_list = []
        for i in range(10):
         if i == 9:
             epoch_list.append("epoch_010")
         else:
             epoch_list.append("epoch_00" + str(i+1))
        import numpy
        h5_path = 'c:/stim/visexpman/data/videos/gaze_shifted_20230706_30hz.h5'
        for k in ["wn","series_001","series_002","series_003"]:
          for i in range(1):
              self.show_fullscreen(color=self.BACKGROUND, duration=self.WAIT)
              self.config.YOUSSEF_FLIP_DELAY='yes'
              if k == 'wn':
                 numpy.random.seed(i)
                 self.config.YOUSSEF_FLIP_DELAY='yes'
                 self.block_start(('white_noise', i))
                 self.show_white_noise_YOUSSEF(square_size = self.PIXEL_SIZE, frame_rate=30.0, duration=25, screen_size=utils.rc((self.ILLUMINATED_AREA, self.ILLUMINATED_AREA)))
                 self.block_end(('white_noise', i))
              elif k == "series_001":
                 self.block_start(('white_noise_shifted', i))
                 self.show_white_noise_shifted(h5_path,k,epoch_list[i])
                 self.block_end(('white_noise_shifted', i))
              elif k == "series_002":                 
                 self.block_start(('natural_scene_1', i))
                 self.show_natural_scene_movie(h5_path,k,epoch_list[i])
                 self.block_end(('natural_scene_1', i))
              else:
                 self.block_start(('natural_scene_2', i))
                 self.show_natural_scene_movie(h5_path,k,epoch_list[i])
                 self.block_end(('natural_scene_2', i))
        numpy.random.seed(10)
        self.DURATION = 25
        self.config.YOUSSEF_FLIP_DELAY='yes'
        self.show_fullscreen(color=self.BACKGROUND, duration=self.WAIT)
        self.block_start(('white_noise', 10))
        self.show_white_noise_YOUSSEF(square_size = self.PIXEL_SIZE, frame_rate=30.0, duration = self.DURATION*60, screen_size=utils.rc((self.ILLUMINATED_AREA, self.ILLUMINATED_AREA)))
        self.block_end(('white_noise', 10))
        self.show_fullscreen(color=self.BACKGROUND, duration=self.WAIT)
        self.DURATION = 1/self.config.SCREEN_EXPECTED_FRAME_RATE
        self.block_start(('white_noise_shifted', 10))  
        self.show_white_noise_shifted(h5_path,'series_004',epoch_list[0])
        self.block_end(('white_noise_shifted', 10))        
        self.show_fullscreen(color=self.BACKGROUND, duration=self.WAIT)
        self.block_start(('natural_scene_1', 10))
        self.show_natural_scene_movie(h5_path,'series_005',epoch_list[0])
        self.block_end(('natural_scene_1', 10))
        self.show_fullscreen(color=self.BACKGROUND, duration=self.WAIT)
        self.block_start(('natural_scene_2', 10))
        self.show_natural_scene_movie(h5_path,'series_006',epoch_list[0])
        self.block_end(('natural_scene_2', 10))
      #   self.DURATION = 0.4161
      #   for k in ['wn',"/series_007","/series_008","/series_009"]:
      #      for i in range(10):
      #       self.show_fullscreen(color=self.BACKGROUND, duration=self.WAIT)
      #       if k == 'wn':
      #          numpy.random.seed(i)
      #          self.block_start(('white_noise', i+10))
      #          self.show_white_noise_YOUSSEF(duration = self.DURATION*60, square_size = self.PIXEL_SIZE, screen_size=utils.rc((self.ILLUMINATED_AREA, self.ILLUMINATED_AREA)))
      #          self.block_end(('white_noise', i+10))
      #       elif k == "series_007":
      #          self.block_start(('white_noise_shifted', i+10))
      #          self.show_white_noise_shifted(h5_path,k,epoch_list[i])
      #          self.block_end(('white_noise_shifted', i+10))
      #       elif k == "series_008":                 
      #          self.block_start(('natural_scene_1', i+10))
      #          self.show_natural_scene_movie(h5_path,k,epoch_list[i])
      #          self.block_end(('natural_scene_1', i+10))
      #       else:
      #          self.block_start(('natural_scene_2', i+10))
      #          self.show_natural_scene_movie(h5_path,k,epoch_list[i])
      #          self.block_end(('natural_scene_2', i+10))

      #   calls to stimulation library
      #   self.st.stimulation_library_function()
      #   pass

