import network_interface
import unittest
import time
import PyQt4.QtCore as QtCore
import visexpman.engine.generic.configuration
import socket
import Queue
import sys
import scipy.io
import visexpA.engine.datahandlers.matlabfile as matlabfile
import numpy
import os.path
import visexpman.engine.generic.utils as utils
import re
#TODO: This module needs to be reworked: two group of functions: communication helpers and mat interfacing, mes intrerface class shall take care of both
#TODO: generate reference mat files without the unnecessary numpy.object parts

#================ Z stack ========================#
def acquire_z_stack(command_queue, response_queue, config, timeout = -1, channel = 'pmtUGraw', test_mat_file = None):
    z_stack_path, z_stack_path_on_mes = generate_paths('z_stack.mat', config)    
    #Acquire z stack
    command_queue.put('SOCacquire_z_stackEOC{0}EOP' .format(z_stack_path_on_mes))
    results = []
    results.append(network_interface.wait_for_response(response_queue, 'SOCacquire_z_stackEOCstartedEOP', error_response = 'error', timeout = timeout))
    results.append(network_interface.wait_for_response(response_queue, ['SOCacquire_z_stackEOCOKEOP', 'SOCacquire_z_stackEOCUSEOP'], error_response = 'error', timeout = timeout))
    results.append(network_interface.wait_for_response(response_queue, 'SOCacquire_z_stackEOCsaveOKEOP', error_response = 'error', timeout = timeout))
    #Extract z stack from mat file
    if test_mat_file != None:
        z_stack_path = test_mat_file
    z_stack = {}
    if isinstance(z_stack_path, str):
        if os.path.exists(z_stack_path):            
            z_stack['data'], z_stack['origin'], z_stack['scale'], z_stack['size'] = z_stack_from_mes_file(z_stack_path, channel = channel)
    return z_stack, results

def z_stack_from_mes_file(mes_file, channel = 'pmtUGraw'):
    '''
    Extract the following form a mes file containing a Z stack:
    -z stack data as a 3D array where the dimensions are: row, col, depth
    -mes system origin [um]
    -step size [um/pixel]
    -z stack size [um; row, col, depth]
    '''
    data = matlabfile.MatData(mes_file).get_field('DATA')
    n_frames = data[0].shape[0]
    n_average = int(data[0][0]['Average'][0][0][0])
    frames = []
    for i in range(n_frames):
        frame = data[0][i]['IMAGE'][0]
        channel_name = str(data[0][i]['Channel'][0][0])
        if channel_name == channel:
            frames.append(frame)
        
    z_stack_data = numpy.array(frames).transpose()
    depth_step = data[0][0]['D3Step'][0][0]
    col_origin = data[0][0]['WidthOrigin'][0][0]
    row_origin = data[0][0]['HeightOrigin'][0][0]
    depth_origin = data[0][0]['D3Origin'][0][0]
    col_step = data[0][0]['WidthStep'][0][0]
    row_step = data[0][0]['HeightStep'][0][0]
    origin  = numpy.array([row_origin, col_origin, depth_origin]).flatten()
    step = numpy.array([row_step, col_step, depth_step]).flatten()
    size = step * (numpy.array(z_stack_data.shape)    -1)
    return z_stack_data, origin, step, size
    
#======================  RC scan =======================#
def rc_scan(trajectory, command_queue, response_queue, config, timeout = -1):
    #Send trajectory points to mes
    set_points(trajectory, command_queue, response_queue, config, timeout = timeout)
    rc_scan_path, rc_scan_path_on_mes = generate_paths('rc_scan.mat', config)
    command_queue.put('SOCrc_scanEOC{0}EOP' .format(rc_scan_path_on_mes))
    results = []
    results.append(network_interface.wait_for_response(response_queue, 'SOCrc_scanEOCstartedEOP', error_response = 'error', timeout = timeout))
    results.append(network_interface.wait_for_response(response_queue, ['SOCrc_scanEOCOKEOP', 'SOCrc_scanEOCUSEOP'], error_response = 'error', timeout = timeout))
    results.append(network_interface.wait_for_response(response_queue, 'SOCrc_scanEOCsaveOKEOP', error_response = 'error', timeout = timeout))
    scanned_trajectory = {}
    if os.path.exists(rc_scan_path):
        #Extract data from file
        pass
    return scanned_trajectory, results

def set_points(points, command_queue, response_queue, config, timeout = -1):
    points_mat, points_mat_on_mes = generate_paths('rc_points.mat', config)
    generate_scan_points_mat(points, points_mat)
    command_queue.put('SOCset_pointsEOC{0}EOP' .format(points_mat_on_mes))
    return network_interface.wait_for_response(response_queue, 'SOCset_pointsEOCpoints_setEOP', error_response = 'error', timeout = timeout)

def generate_scan_points_mat(points, mat_file):
    '''
    Points shall be a struct array of numpy.float64 with x, y and z fields.
    numpy.zeros((3,100), {'names': ('x', 'y', 'z'), 'formats': (numpy.float64, numpy.float64, numpy.float64)})
    '''
    if points.dtype != [('row', '<f8'), ('col', '<f8'), ('depth', '<f8')]:
        raise RuntimeError('Data format is incorrect')
    data_to_mes_mat = {}
    data_to_mes_mat['DATA'] = points
    scipy.io.savemat(mat_file, data_to_mes_mat, oned_as = 'column')
    
def get_rc_range(command_queue, response_queue, timeout = -1):
    '''
    MES returns the range as follows: xmin, xmax, ymin, ymax, z range
    '''
    command_queue.put('SOCget_rangeEOCEOP')
    result = network_interface.wait_for_response(response_queue, 'SOCget_rangeEOC', error_response = 'error', timeout = timeout)[0]
    ranges =  re.findall('EOC(.+)EOP',result).split(',')
    mes_scan_range = {}
    if len(ranges) == 5:
        mes_scan_range['col'] = map(float, result[:2])
        mes_scan_range['row'] = map(float, result[2:4])
        mes_scan_range['depth'] = map(float, result[4])
    return mes_scan_range

#=========== General helpers ========================#
def generate_paths(filename, config):
    path = utils.generate_filename(os.path.join(config.EXPERMENT_DATA_PATH, filename))
    path_on_mes = utils.convert_path_to_remote_machine_path(path, config.MES_DATA_FOLDER)
    return path, path_on_mes
    
def get_objective_position(mat_file):    
    m = matlabfile.MatData(mat_file)
    data = m.get_field('DATA')
    n_frames = data[0].shape[0]
    if n_frames <= 2: #For some reason sometimes two data units reside in the mat file
        data = m.get_field('DATA.Zlevel.0')[0].flatten()
    else:
        data = []
        data_set = m.get_field('DATA.Zlevel') 
        for i in range(n_frames):
            data.append(data_set[0][i][0][0][0])
        data = numpy.array(data)
    return data

def set_mes_mesaurement_save_flag(mat_file, flag):
    m = matlabfile.MatData(reference_path, target_path)
    m.rawmat['DATA'][0]['DELETEE'] = int(flag) #Not tested, this addressing might be wrong
    m.flush()
    
class MesInterface(object):
    '''
    Protocol:
        1. acquire_line_scan, parameter: mat file path on MES computer
        2. Response from MES computer: acquire_line_scan, started
        3. visual stimulation
        4. acquire_line_scan, OK is received when the two photon acquisition is finished
        5. acquire_line_scan, saveOK is received when saving data is complete
    '''
    def __init__(self, config, command_queue, response_queue, command_server, screen = None, log = None, ):
        self.config = config
        self.command_queue = command_queue
        self.response_queue = response_queue
        self.screen = screen
        self.log = log
        self.command_server = command_server
        self.stop = False


    def set_scan_time(self, scan_time, reference_path, target_path):        

        m = matlabfile.MatData(reference_path, target_path)
        ts = m.get_field(m.name2path('ts'))[0][0][0][0]
        ts = numpy.array([ts[0],ts[1],ts[2],float(1000*scan_time)], dtype = numpy.float64)
        m.set_field(m.name2path('ts'), ts, allow_dtype_change=True)
            
    def _watch_keyboard(self):
        #Keyboard commands
        if self.screen != None:
            return self.screen.experiment_user_interface_handler() #Here only commands with running experiment domain are considered
        
        #TODO: handle US parameter from mes: user abort
    def start_line_scan(self, mat_file_path):
        aborted = False
        self.stop = False
        if True: #self.command_server.connection_state:
            self.command_queue.put('SOCacquire_line_scanEOC{0}EOP'.format(mat_file_path))
            #Wait for MES response        
            while True:
                try:
                    response = self.response_queue.get(False)
                except:
                    response = ''
                if 'SOCacquire_line_scanEOCstartedEOP' in response:
                    if self.log != None:
                        self.log.info('line scan started')
#                        self.command_server.enable_keep_alive_check = False
                    break
                elif 'SOCacquire_line_scanEOCerror_starting_measurementEOP' in response:
                    aborted = True
                    if self.log != None:
                        self.log.info('error starting measurement')
                        self.stop = True
#                        self.command_server.enable_keep_alive_check = False
                    break
                user_command = self._watch_keyboard()
                if user_command != None:
                    if user_command.find('stop') != -1:
                        aborted = True
                        if self.log != None:
                            self.log.info('stopped')
                        break
                time.sleep(0.1)
        return aborted
                
    def wait_for_line_scan_complete(self):        
        aborted = False
        if True: #self.command_server.connection_state:
#            self.command_server.enable_keep_alive_check = False
           #wait for finishing two photon acquisition
            while True:
                if self.stop:
                    break
                try:
                    response = self.response_queue.get(False)
                except:
                    response = ''
                if 'SOCacquire_line_scanEOCOKEOP' in response or 'SOCacquire_line_scanEOCUSEOP' in response:
                    if self.log != None:
                        self.log.info('line scan complete')
                    break
                user_command = self._watch_keyboard()
                if user_command != None:
                    if user_command.find('stop') != -1:
                        aborted = True
                        if self.log != None:
                            self.log.info('stopped')
                        break                    
                time.sleep(0.1)
        return aborted
                
    def wait_for_data_save_complete(self):
        aborted = False
        if True:#self.command_server.connection_state:
            #Wait for saving data to disk
            while True:
                if self.stop:
                    break
                try:
                    response = self.response_queue.get(False)
                except:
                    response = ''
                if 'SOCacquire_line_scanEOCsaveOKEOP' in response:
                    if self.log != None:
                        self.log.info('line scan data saved')
                    break
                user_command = self._watch_keyboard()
                if user_command != None:
                    if user_command.find('stop') != -1:
                        aborted = True
                        if self.log != None:
                            self.log.info('stopped')
                        break                    
                time.sleep(0.1)
#            self.command_server.enable_keep_alive_check = True
        return aborted
    
class MesEmulator(QtCore.QThread):
    def __init__(self, config, port):
        self.config = config
        self.port = port
        QtCore.QThread.__init__(self)

        self.commands  = [['', 0.5], 
                        ['SOCacquire_line_scanEOCstartedEOP', 0.35], 
                        ['SOCacquire_line_scanEOCOKEOP', 0.35], 
                        ['SOCacquire_line_scanEOCsaveOKEOP', 0.35], ]

    def run(self):
        self.sock = socket.create_connection(('localhost', self.port))
        self.sock.send('create_connection')
        self.sock.recv(256)
        time.sleep(0.1)        
        for command in self.commands:
            if len(command[0]) > 0:
                try:
                    self.sock.send(command[0])
                except:
                    print 'Error'
                    pass
            time.sleep(command[1])
            
        self.sock.close()
            
class ExperimentThread(QtCore.QThread):
    def __init__(self, config, command_queue, response_queue, command_server):
        QtCore.QThread.__init__(self)
        self.config = config
        self.command_queue = command_queue
        self.response_queue = response_queue
        self.command_server = command_server
        self.done = False        
        
    def run(self):
        self.mes_if = MesInterface(self.config, self.command_queue, self.response_queue, self.command_server)
        time.sleep(0.1)
        self.mes_if.start_line_scan('dummy.mat')        
        time.sleep(1.0)
        self.mes_if.wait_for_line_scan_complete()
        time.sleep(0.3)
        self.mes_if.wait_for_data_save_complete()
        self.done = True        
            
class NetworkInterfaceTestConfig(visexpman.engine.generic.configuration.Config):
    def _create_application_parameters(self):
        import random
        port = 10000 + int(10000*random.random())
        VISEXPMAN_MES = {'ENABLE' : True, 'IP': '',  'PORT' : port,  'RECEIVE_BUFFER' : 256}
        self._create_parameters_from_locals(locals())

            
class TestMesInterface(unittest.TestCase):
    def setUp(self):
       #TODO: this test has to be reworked because of the network thing
        self.config = NetworkInterfaceTestConfig()
        self.command_queue = Queue.Queue()
        self.response_queue = Queue.Queue()
        self.command_server = network_interface.CommandServer(self.command_queue, self.response_queue, self.config.VISEXPMAN_MES['PORT'])
        self.mes = MesEmulator(self.config, self.config.VISEXPMAN_MES['PORT'])
        self.experiment = ExperimentThread(self.config, self.command_queue, self.response_queue, self.command_server)

    def test_01_interaction_with_mes_emulator(self):
        self.command_server.start()
        self.mes.start()
        self.experiment.start()
        time.sleep(3.0)
        self.assertEqual(self.experiment.done,  True)
        
    def tearDown(self):
        self.command_server.terminate()
        self.mes.terminate()        
        self.experiment.terminate()
        
    
if __name__ == "__main__":
#    unittest.main()
    mat_file = '/media/sf_M_DRIVE/Zoltan/visexpman/data/0_X-820381_Y-252527_Z+57516/acquire_z_stack_parameters_MovingDot_1321687013_0.mat'
    print get_objective_position(mat_file)    
    mat_file = '/media/sf_M_DRIVE/Zoltan/visexpman/data/test.mat'    
    print get_objective_position(mat_file)
