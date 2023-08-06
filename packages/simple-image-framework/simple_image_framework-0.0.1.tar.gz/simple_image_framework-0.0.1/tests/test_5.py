from image_processing_framework import core 

import test_3
import test_4

if __name__ == '__main__' : 
    frame = core.ImageProcessingFramework(
        name = 'inverter then red filter ~', 
        version = '0.0.1' , 
        author = 'Cutie', 
        description = '''
            操作合成：先反相，再保留红色像素
        '''
    )
    frame.pipeline = frame.pipeline | test_3.inverter | test_4.red_filter 
    core.frame_run(frame) 
    pass 