  from visexpman.engine.vision_experiment import experiment
from visexpman.engine.generic import utils
import h5py

class TemplateExperimentConfig(experiment.ExperimentConfig):
    def _create_application_parameters(self):
        #place for experiment parameters
        #parameter with range: list[0] - value, list[1] - range
        #path parameter: parameter name contains '_PATH'
        #string list: list[1] - empty        
        PARAMETER = 'dummy'
        self._create_parameters_from_locals(locals())
        

class BaccusLabExperiment(experiment.Experiment):
    def configuration(self):
        self.PIXEL_SIZE =50.0#um
        self.ILLUMINATED_AREA=1000#um
        self.BACKGROUND=0.5
        self.WAIT=100e-3#wait time in seconds at beginning and end of stimulus
        self.COLORS = [0.0, 1.0]
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
        for k in ['wn',"series_001","series_002","series_003"]:
          for i in range(10):
              self.show_fullscreen(color=self.BACKGROUND, duration=self.WAIT)
              if k == 'wn':
                 numpy.random.seed(i)
                 self.show_white_noise(duration = self.DURATION*60, square_size = self.PIXEL_SIZE, screen_size=utils.rc((self.ILLUMINATED_AREA, self.ILLUMINATED_AREA)))
              elif k == "/series_001":
                 self.show_white_noise_shifted(h5_path,k,epoch_list[i])
              elif k == "/series_002":
                 self.show_natural_scene_movie(h5_path,k,epoch_list[i])
              else:
                 self.show_natural_scene_movie(h5_path,k,epoch_list[i])
        numpy.random.seed(10)
        self.show_white_noise(duration = self.DURATION*60, square_size = self.PIXEL_SIZE, screen_size=utils.rc((self.ILLUMINATED_AREA, self.ILLUMINATED_AREA)))
        self.show_white_noise_shifted()
        self.show_natural_scene_movie()
        self.show_natural_scene_movie()
        for k in ['wn',"/series_007","/series_008","/series_009"]:
           for i in range(10):
            self.show_fullscreen(color=self.BACKGROUND, duration=self.WAIT)
            if k == 'wn':
              numpy.random.seed(i)
              self.show_white_noise(duration = self.DURATION*60, square_size = self.PIXEL_SIZE, screen_size=utils.rc((self.ILLUMINATED_AREA, self.ILLUMINATED_AREA)))
            elif k == "/series_007":
               self.show_white_noise_shifted()
            elif k == "/series_008":
               self.show_natural_scene_movie()
            else:
               self.show_natural_scene_movie()

        #calls to stimulation library
        #self.st.stimulation_library_function()
        pass

class TemplatePreExperiment(experiment.PreExperiment):    
  def run(self):
    #calls to stimulation library
    pass