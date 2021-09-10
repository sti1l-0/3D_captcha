from PIL import Image, ImageFont, ImageDraw
from random import randint, sample
import string
import os
import numpy as np
#import matplotlib.pyplot as plt


def randstrToImage():
    randstr = ''.join(sample(string.ascii_letters + string.digits, 4))
    font = ImageFont.truetype("arial.ttf", 48)
    im = Image.new("RGB", (128, 64), (255, 255, 255))
    draw = ImageDraw.Draw(im)
    draw.text((2, 5), randstr, font=font, fill="#000000")
    #im.show()
    return im


def ImageToMatrix(image):
    im = image
    width, height = im.size
    im = im.convert("L")
    data = im.getdata()
    data = np.matrix(data, dtype='float')//(255.0 * 0.7)
    new_data = np.reshape(data, (height, width))
    return new_data


def MatrixToImage(data):
    data = data*255
    new_im = Image.fromarray(data.astype(np.uint8))
    return new_im


def __MatrixToObj(matrix):
    """
        旧版生成一个文件
    """
    def make_cube(row, pixel, file, cubesize, length, count):
        #定义一个立方体的顶点和面
        vs = [[-1, -1, 1], [1, -1, 1], [-1, 1, 1], [1, 1, -1],
              [-1, -1, -1], [-1, 1, -1], [1, -1, -1], [1, 1, 1]]
        fs = [[1, 2, 3], [4, 5, 6], [5, 4, 7], [8, 3, 2], [5, 7, 2], [5, 3, 6], [
            8, 2, 7], [6, 3, 8], [5, 1, 3], [7, 4, 8], [2, 1, 5], [8, 4, 6]]
        #定义一个方块
        file.writelines('\no Object.'+str(row)+''+str(pixel)+'\n')
        #单维度打乱
        z = randint(-length//13, length//13)
        #写入一个方块
        for v in vs:
            file.writelines('v '+str(v[2]*cubesize-pixel+64)+' ' +
                            str(v[0]*cubesize-row+32)+' '+str(v[1]*cubesize+z)+'\n')
        for f in fs:
            file.writelines('f '+str(f[0]+count)+' ' +
                            str(f[1]+count)+' '+str(f[2]+count)+'\n')

    #建一个文件，这个地方文件名要改
    filename = 'newobj.obj'
    file = open(filename, 'w')
    file.writelines('# Exported by python code\n')
    count = 0
    #把算出来的像素逐个铺上方块
    for row in range(len(matrix)):
        for pixel in range(len(matrix[row])):
            if matrix[row][pixel] == 1:
                pass
            else:
                make_cube(row, pixel, file, 0.5, len(matrix[0]), count)
                count += 8

def MatrixToObj(matrix):
    def make_cube(row, pixel, file, cubesize, length, count):
        #定义一个立方体的顶点和面
        vs = [[-1, -1, 1], [1, -1, 1], [-1, 1, 1], [1, 1, -1],
              [-1, -1, -1], [-1, 1, -1], [1, -1, -1], [1, 1, 1]]
        fs = [[1, 2, 3], [4, 5, 6], [5, 4, 7], [8, 3, 2], [5, 7, 2], [5, 3, 6], [
            8, 2, 7], [6, 3, 8], [5, 1, 3], [7, 4, 8], [2, 1, 5], [8, 4, 6]]
        #定义一个方块
        file += '\no Object.'+str(row)+''+str(pixel)+'\n'
        #单维度打乱
        z = randint(-length//13, length//13)
        #写入一个方块
        for v in vs:
            file += 'v '+str(v[2]*cubesize-pixel+64)+' ' + str(v[0]*cubesize-row+32)+' '+str(v[1]*cubesize+z)+'\n'
        for f in fs:
            file += 'f '+str(f[0]+count)+' ' + str(f[1]+count)+' '+str(f[2]+count)+'\n'
        return file

    file = '# Exported by python code\n'
    count = 0
    #把算出来的像素逐个铺上方块
    for row in range(len(matrix)):
        for pixel in range(len(matrix[row])):
            if matrix[row][pixel] == 1:
                pass
            else:
                file = make_cube(row, pixel, file, 0.5, len(matrix[0]), count)
                count += 8
    return file