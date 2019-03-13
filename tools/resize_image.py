
from PIL import Image
import os
import argparse


def get_args():
    '''
    参数解析器，获取执行的参数
    :return: 
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("-output_dir",type=str,default="",help="处理以后的输出目录")
    parser.add_argument('-input_dir',type=str,default="",help="待处理的文件目录")
    parser.add_argument('-size',type=int,default=300,help="需要处理到目标大小，默认400")
    return  parser.parse_args()



def mkdir(path):
    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)
        print("jian")
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print("no jian")
        return False


def walk_dir(dirname):
    '''
    遍历目录，返回所有文件的一个list
    :param dirname: 
    :return: 
    '''
    files_dict = {}
    for root, dirs, filenames in os.walk(dirname, topdown=True):
        if filenames != []:
            type_name = root.replace(dirname,"").replace("\\","")
            files_dict[type_name] = [os.path.join(root,file) for file in filenames]

    return  files_dict


def changeImageSize(imageRoot,resultRoot,reSize):
    reWidth = reHeight = reSize
    files_dict = walk_dir(imageRoot)

    resultPicRoot = os.path.join(resultRoot,str(reWidth)+'X'+str(reHeight))
    mkdir(resultPicRoot)


    if files_dict:
        for category in files_dict:
            new_cagegory_path = os.path.join(resultPicRoot, category)
            mkdir(new_cagegory_path)
            for i_file in files_dict[category]:
                if 'png' in i_file or 'jpg' in i_file :
                    img = Image.open(i_file)
                    width_origin, height_origin = img.size


                    # 缩小图片比例
                    #new_img = img.resize((reWidth, int(height_origin / (width_origin / reWidth))), Image.ANTIALIAS)

                    new_img = img.resize((int(  width_origin/ (height_origin / reHeight)),reHeight), Image.ANTIALIAS)
                    width4, height4 = new_img.size
                    print(width4,height4)
                    new_img = new_img.convert("RGB")
                    new_img.save(i_file.replace('png', 'jpg').replace(imageRoot,resultPicRoot))






if __name__ == '__main__':
    args = get_args()
    changeImageSize(args.input_dir,args.output_dir,args.size)
