from image_processing_framework import core 

def red_filter(img, args) : 
    out = [[None for _ in range(len(img[0]))] for _ in range(len(img))] 
    check_type = type(img[0][0]) is tuple 
    if not check_type: 
        core.ct.warn('Desire the RGA image, but meets grey image. ')
    for i in range(len(img)) : 
        for j in range(len(img[i])) : 
            k = img[i][j] 
            if check_type: 
                out[i][j] = ( k[0] , 0 , 0 ) 
            else: 
                out[i][j] = 0 
    return out 

if __name__ == '__main__': 
    frame = core.ImageProcessingFramework(
        name = 'Filter: 红色萃取', 
        version = '0.0.1' , 
        author = 'Cutie', 
        description = '''
            用于将彩图转为纯红色图，灰度图像将被移除内容
        '''
    )
    frame.pipeline |= red_filter 
    core.frame_run(frame) 