
import time
import os

from PIL import Image

import methods
from config import config

def current_milli_time(): return int(round(time.time() * 1000))

class BaseRecorder(object):

    def __init__(self):
        self.frame_count = 0
        self.is_recording = False

    def record_frame(self, image_array, angle, throttle):
        pass


class FileRecorder(BaseRecorder):

    def __init__(self):
        self.instance_path = self.make_instance_dir(config.recording.session_dir)
        super(FileRecorder, self).__init__()

    def make_instance_dir(self, sessions_path):
        '''
        Create a directory for the current session based on time,
        and a global sessions directory if it does not exist.
        '''
        real_path = os.path.abspath(os.path.expanduser(sessions_path))
        if not os.path.isdir(real_path):
            os.makedirs(real_path)
        instance_name = time.strftime('%Y_%m_%d__%I_%M_%S_%p')
        instance_path = os.path.join(real_path, instance_name)
        if not os.path.isdir(instance_path):
            os.makedirs(instance_path)
        return instance_path

    def record_frame(self, image_array, angle, throttle):
        '''
        Record a single frame, with frame index, angle and throttle values
        as its filename
        '''
        # throttle is inversed, i.e. forward is negative, backwards positive
        # we are only interested in forward values of throttle
        # angle is counter-clockwise, i.e. left is positive
        # TODO: make a proper value mapping here, and then transform
        if (throttle * -1.0 < config.recording.throttle_threshold or
            abs(angle) < config.recording.steering_threshold):
            self.is_recording = False
            return
        self.is_recording = True
        file_angle = int(angle * 10)
        file_throttle = int(throttle * 1000)
        filepath = self.create_img_filepath(
            self.instance_path,
            self.frame_count,
            file_angle,
            file_throttle)
        im = Image.fromarray(image_array)
        im.save(filepath, compress_level=0)
        self.frame_count += 1

    def create_img_filepath(self, directory, frame_count, 
        angle, throttle, file_type='png'):
        '''
        Generate the complete filepath for saving an image
        '''
        filepath = str("%s/" %
                       directory +
                       "frame_" +
                       str(frame_count).zfill(5) +
                       "_ttl_" +
                       str(throttle) +
                       "_agl_" +
                       str(angle) +
                       "_mil_" +
                       str(current_milli_time()) +
                       '.' + file_type)
        return filepath
