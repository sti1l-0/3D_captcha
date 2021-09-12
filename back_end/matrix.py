from PIL import Image, ImageFont, ImageDraw
from random import randint, sample, random
import string
import json
import numpy as np

# import matplotlib.pyplot as plt


def randstrToImage():
    imageSize = 64
    # 随机生成四位字符的串
    randstr0 = "".join(sample(string.ascii_letters + string.digits, 2))
    randstr1 = "".join(sample(string.ascii_letters + string.digits, 2))
    # 弄成图片
    font = ImageFont.truetype("arialbi.ttf", imageSize // 2 + 8)
    im = Image.new("RGB", (imageSize, imageSize), (255, 255, 255))
    draw = ImageDraw.Draw(im)
    draw.text((0, 0), randstr0, font=font, fill="#000000")
    draw.text((0, imageSize // 2 - 2), randstr1, font=font, fill="#000000")
    # im.show()
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
                + str(v[2] * cubesize - pixel + 64)
                + " "
                + str(v[0] * cubesize - row + 32)
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
    return file, json.dumps({})


def get_obj():
    return rotate(MatrixOnBall(ImageToMatrix(randstrToImage()).tolist()))


def mackacube(x, y, z, count, cubesize=0.5) -> str:
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
    acube = "\no Object." + str(x) + "" + str(y) + "\n"
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
    # 切方片
    peace = 4  # 横竖各分一半，总共四片
    peace_size = len(matrix[0]) // peace  # 每一片的边长大小
    count = 0
    file = "# Exported by python code\n"
    max = [0,0]
    # 前两个循环遍历所有的方片，peace_x,peace_y标识现在是第几个方片
    for i in [1,2]:
        for peace_x in range(peace):
            for peace_y in range(peace):
                # 生成并随机选取一个球面方程或平面方程
                d = random()
                a = random()-0.5
                b = random()-0.5
                c = random()

                def ball_z(x, y) -> int:
                    return (962*(a**2+b**2+c**2)  - (x-31*a)**2 - (y-31*b)**2 )**0.5 + 31*c

                def plane_z(x, y):
                    return d + a*1.5 * x + b*1.5 * y

                final_z = plane_z if randint(1, 1) else ball_z
                # 双循环取方片内的所有点，inner_x,inner_y标识方片中的哪个点
                for inner_x in range(peace_size):
                    for inner_y in range(peace_size):
                        # 拼凑还原该点在图像矩阵中的横纵坐标xy
                        x = peace_x * peace_size + inner_x
                        y = peace_y * peace_size + inner_y
                        max[0] = x if x > max[0] else max[0]
                        max[1] = y if y > max[1] else max[1]
                        if matrix[x][y] == 0:
                            z = final_z(x, y)
                            file += mackacube(x, y, z, count)
                            count += 8
    return file


if __name__ == "__main__":
    __ObjFile(MatrixOnBall(ImageToMatrix(randstrToImage()).tolist()))
