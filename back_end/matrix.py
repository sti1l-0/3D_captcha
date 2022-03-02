from tkinter import CENTER
from PIL import Image, ImageFont, ImageDraw
from random import randint, sample, random
import string
import json
import numpy as np

imageSize = 64

def randstrToImage():
    # 随机生成四位字符的串
    randstr00 = "".join(sample(string.ascii_letters + string.digits, 1))
    randstr01 = "".join(sample(string.ascii_letters + string.digits, 1))
    randstr10 = "".join(sample(string.ascii_letters + string.digits, 1))
    randstr11 = "".join(sample(string.ascii_letters + string.digits, 1))
    # 弄成图片
    font = ImageFont.truetype("./firacode.ttf", imageSize//2)
    im = Image.new("RGB", (imageSize, imageSize), (255, 255, 255))
    draw = ImageDraw.Draw(im)
    center = (imageSize//2,imageSize//2)
    draw.text(center, randstr00, anchor='rs', font=font, fill="#000000")
    draw.text(center, randstr01, anchor='rt', font=font, fill="#000000")
    draw.text(center, randstr10, anchor='ls', font=font, fill="#000000")
    draw.text(center, randstr11, anchor='lt', font=font, fill="#000000")
    print(randstr00,randstr01,randstr10,randstr11)
    return im


def ImageToMatrix(image):
    im = image
    width, height = im.size
    im = im.convert("L")
    data = im.getdata()
    data = np.matrix(data, dtype="float") // (255.0 * 0.7)
    new_data = np.reshape(data, (height, width))
    return new_data


def MatrixToImage(data):
    data = data * 255
    new_im = Image.fromarray(data.astype(np.uint8))
    return new_im


def __ObjFile(_file):
    """
    旧版生成一个文件
    """

    # 建一个文件，这个地方文件名要改
    filename = "newobj.obj"
    file = open(filename, "w")
    file.write(_file)
    file.close()


def MatrixToObj(matrix):
    def make_cube(row, pixel, file, cubesize, length, count):
        # 定义一个立方体的顶点和面
        vs = [
            [-1, -1, 1],
            [1, -1, 1],
            [-1, 1, 1],
            [1, 1, -1],
            [-1, -1, -1],
            [-1, 1, -1],
            [1, -1, -1],
            [1, 1, 1],
        ]
        fs = [
            [1, 2, 3],
            [4, 5, 6],
            [5, 4, 7],
            [8, 3, 2],
            [5, 7, 2],
            [5, 3, 6],
            [8, 2, 7],
            [6, 3, 8],
            [5, 1, 3],
            [7, 4, 8],
            [2, 1, 5],
            [8, 4, 6],
        ]
        # 定义一个方块
        file += "\no Object." + str(row) + "" + str(pixel) + "\n"
        # 单维度打乱
        z = randint(-length // 8, length // 8)
        # 写入一个方块
        for v in vs:
            #
            file += (
                "v "
                + str(v[2] * cubesize - pixel + imageSize//2)
                + " "
                + str(v[0] * cubesize - row + imageSize//4)
                + " "
                + str(v[1] * cubesize + z)
                + "\n"
            )
        for f in fs:
            # count用来统计连接的面
            file += (
                "f "
                + str(f[0] + count)
                + " "
                + str(f[1] + count)
                + " "
                + str(f[2] + count)
                + "\n"
            )
        return file

    file = "# Exported by python code\n"
    count = 0
    # 把算出来的像素逐个铺上方块
    for row in range(len(matrix)):
        for pixel in range(len(matrix[row])):
            if matrix[row][pixel] == 1:
                pass
            else:
                file = make_cube(row, pixel, file, 0.8, len(matrix[0]), count)
                count += 8
    return file


def rotate(file):
    """
    返回旋转后obj和旋转的角度
    """
    # 测试，暂时不旋转
    return file, 'rotation data'


def get_obj():
    # return rotate(MatrixOnBall(ImageToMatrix(parallel()).tolist()))
    return rotate(MatrixOnBall(ImageToMatrix(randstrToImage()).tolist()))


def mackacube(x, y, z, count, cubesize=0.8) -> str:
    """
    这里的xy应该是原图片矩阵的xy
    z为根据计算得到的纵轴坐标
    count统计已有方块数量
    """
    vs = [
        [-1, -1, 1],
        [1, -1, 1],
        [-1, 1, 1],
        [1, 1, -1],
        [-1, -1, -1],
        [-1, 1, -1],
        [1, -1, -1],
        [1, 1, 1],
    ]
    fs = [
        [1, 2, 3],
        [4, 5, 6],
        [5, 4, 7],
        [8, 3, 2],
        [5, 7, 2],
        [5, 3, 6],
        [8, 2, 7],
        [6, 3, 8],
        [5, 1, 3],
        [7, 4, 8],
        [2, 1, 5],
        [8, 4, 6],
    ]
    # 定义一个方块
    acube = "\no Object." + str(x) + "_" + str(y) + "_" + str(z) + "\n"
    # 写入一个方块
    for v in vs:
        #
        acube += (
            "v "
            + str(v[0] * cubesize + y)
            + " "
            + str(v[1] * cubesize - x)
            + " "
            + str(v[2] * cubesize + z)
            + "\n"
        )
    for f in fs:
        # count用来统计连接的面
        acube += (
            "f "
            + str(f[0] + count)
            + " "
            + str(f[1] + count)
            + " "
            + str(f[2] + count)
            + "\n"
        )
    return acube


def MatrixOnBall(matrix):
    count = 0
    file = "# Exported by python code\n"
    def final_z(x,y):
        return randint(0, 48)
    for x in range(imageSize):
        for y in range(imageSize):
            if matrix[x][y] == 0:
                z = final_z(x, y)
                def extand(x, z):
                    return int((x-imageSize//2) * (2-z/72))
                px = extand(x, z)
                py = extand(y, z)
                file += mackacube(px, py, z, count)
                count += 8
    return file

def parallel():
    im = Image.new("RGB", (imageSize, imageSize), (255, 255, 255))
    draw = ImageDraw.Draw(im)
    draw.chord([(16, 0), (16,64)], start=0, end=30, fill=128)
    draw.chord([(48, 0), (48,64)], start=0, end=30, fill=128)
    draw.chord([(24, 0), (24,64)], start=0, end=30, fill=128)
    draw.chord([(40, 0), (40,64)], start=0, end=30, fill=128)
    # im.show()
    return im

if __name__ == "__main__":
    # __ObjFile(MatrixOnBall(ImageToMatrix(randstrToImage()).tolist()))
    __ObjFile(MatrixOnBall(ImageToMatrix(parallel()).tolist()))
