from . import color_terminal as ct 
import sys 
import time 

from PIL import Image 

class ImageProcessingPipelineElement: 
    def __init__ ( self , *calls ) : 
        self.callables = list(calls)
    def __len__ (self) : 
        return len(self.callables) 
    def __getitem__ ( self , index ) : 
        return self.callables[index] 
    def __or__ ( self, other ) : 
        ans = ImageProcessingPipelineElement() 
        ans.callables.extend(self.callables) 
        if type(other) is ImageProcessingPipelineElement: 
            ans.callables.extend(other.callables) 
        elif callable(other): 
            ans.callables.append(other) 
        return ans 
    
def process_identity(): 
    return ImageProcessingPipelineElement() 

class ImageProcessingFramework: 
    def __init__ ( self , name = 'unknown' , version = '0.0.1' , author = 'unknown' , description = 'unknown' , pipelines : ImageProcessingPipelineElement = process_identity() ) : 
        self.name = name 
        self.version = version 
        self.author = author 
        self.description = description 
        if type(pipelines) is not ImageProcessingPipelineElement: 
            self.pipeline = ImageProcessingPipelineElement(pipelines) 
        else: 
            self.pipeline = pipelines

# abbr. 
proci = process_identity 

def frame_run( i : ImageProcessingFramework = ImageProcessingFramework() ): 
    ct.debug('Image Processing Step 1: Boot the framework ')
    if type(i) is not ImageProcessingFramework: 
        ct.warn( f'You give me a {type(i)} as the framework, but I need a ImageProcessingFramework. ' )
        ct.warn( 'Maybe you would fail in the next step. ' ) 
    ct.info(f'Start {i.name} v{i.version} by {i.author} ...') 
    ct.info('Description: ' + i.description) 
    args = sys.argv 
    # args[1] : input image file 
    # args[2] : output image file (optional) 
    # next : -- ( optional for all next ) 
    # next : other arguments here ~ 
    if len(args) < 2 : 
        ct.error('You just only give me one argument, which is the input image file? ') 
        ct.warn(f'Usage: {args[0]} <input image file> [output image file] [-- (other arguments)]')
        exit(1) 
    input_file_name = args[1] 
    ct.info(f'Parse Input Image Path "{input_file_name}" ...') 
    if len(args) == 2: 
        output_file_name = None 
    else: 
        output_file_name = args[2] 
    start_index = 4 
    if output_file_name == '--': 
        output_file_name = None 
        start_index = 3  
    if output_file_name is not None: 
        ct.info(f'Parse Output File Path "{output_file_name}" ...') 
    else: 
        ct.debug('Can not find the output file path, it would be asked in later. ')
    if len(args) >= start_index and args[start_index - 1] != '--': 
        ct.warn(f'You miss the "--" before other arguments, please add it next time. ')
        ct.warn(f'Usage: {args[0]} <input image file> [output image file] [-- (other arguments)]')
        ct.warn('In the future version, maybe this operation would break the purpose you want. ')
        start_index -= 1 
    ct.debug(f'Parse Other Arguments ...') 
    if len(args) > start_index: 
        other_args = args[start_index:] 
        ct.info(f'Other Arguments: {other_args}') 
    else: 
        other_args = [] 
        ct.info('No other arguments.') 
    ct.debug('Image Processing Step 2: Read from image file ')
    index = 0 
    try: 
        ct.debug('Open the image file')
        with Image.open( input_file_name ) as im : 
            col, row = im.size 
            ct.debug(f'The image "{input_file_name} is with dimension {col}x{row}. ')
            pixels = im.load() 
            ct.debug('load the info from origin image')
            pixels_data = [[pixels[x, y] for y in range(row)] for x in range(col)] 
            ct.debug('parse the image to python list')
    except Exception as e: 
        ct.error(f'Attempt to open and parse image "{input_file_name}" but fails with {e}')
        exit(1)
    time_clock = time.time() 
    try: 
        while index < len(i.pipeline) : 
            n = time.time() 
            ct.debug(f'{n-time_clock:.2}s start to transform on step {index}')
            image_map = i.pipeline[index] 
            pixels_data = image_map( pixels_data , other_args )
            n = time.time() 
            ct.debug(f'{n-time_clock:.2}s end of step {index}')
            if pixels_data is None: 
                ct.warn(f'In the transform step {index}, the output pixel matrix is None! Are you sure the behaviors on it? ') 
            index += 1 
    except BaseException as e: 
        ct.error(f'Error when the transform step {index} : {e}')
        exit(1)
    if pixels_data is None: 
        ct.error('Transform layer done: the end output is None. ')
        exit(1) 
    while output_file_name is None: 
        ct.info('Transformation done. ') 
        print( 'Can you tell me the output image path? ') 
        read_file_name = input( 'output-image-path >>> ' ) 
        if read_file_name is not None and read_file_name != '' : 
            output_file_name = read_file_name 
    ct.debug('Image Processing Step 3: Output the image file ')
    ct.info(f'The output image path: "{output_file_name}"')
    ct.debug('Check the output image type ... ')
    inner_type = type( pixels_data[0][0] )
    if inner_type is list or inner_type is tuple : 
        mode = 'RGB' 
        ct.info('The output image type is RGB type. ')
    else: 
        mode = 'L'
        ct.info('The output image type is Grey type. ')
    dimensions = ( len(pixels_data) , len(pixels_data[0]) ) 
    ct.info( f'The output image dimension is: {dimensions[0]}x{dimensions[1]}' )
    output_image = Image.new( mode , dimensions )
    raw_pixels = [ pixels_data[i][j] for j in range(dimensions[1]) for i in range(dimensions[0]) ] 
    output_image.putdata ( raw_pixels ) 
    ct.debug('Prepare to write the pixels info to file ' + output_file_name )
    output_image.save( output_file_name ) 
    ct.info(f'Write to file "{output_file_name}" successfully. ')
    