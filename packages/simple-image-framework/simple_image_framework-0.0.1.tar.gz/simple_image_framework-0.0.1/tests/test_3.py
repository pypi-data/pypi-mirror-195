from image_processing_framework import core 

def inverter(matrix, args) : 
    m2 = matrix.copy() 
    for i in range(len(matrix)) : 
        for j in range(len(matrix[i])) : 
            m = matrix[i][j] 
            if type(m) is tuple : 
                m2[i][j] = list(m)
                for k in range(len(m)): 
                    m2[i][j][k] = 255 - m[k] 
                # the output pixel must be tuple | int 
                m2[i][j] = tuple(m2[i][j]) 
            else: 
                m2[i][j] = 255 - m 
    return m2 

if __name__ == '__main__' : 
    frame = core.ImageProcessingFramework(
        name = 'Inverger : 反相映射', 
        version = '0.0.1' , 
        author = 'Cutie', 
        description = '''
            用于直接对图像进行反相 
        '''
    )
    frame.pipeline |= inverter
    core.frame_run(frame) 