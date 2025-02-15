#coding: utf-8
from PIL import Image
import shutil
import os
import sys
import json
from datetime import datetime
#from ImageProcess import Graphics

class Graphics:  
    '''图片处理类
    
    参数
    -------
    infile: 输入文件路径
    outfile: 输出文件路径
    '''
    def __init__(self, infile, outfile):
        self.infile = infile
        self.outfile = outfile


    def fixed_size(self, width, height):  
        """按照固定尺寸处理图片"""  
        im = Image.open(self.infile)  
        out = im.resize((width, height),Image.ANTIALIAS)  
        out.save(self.outfile)  


    def resize_by_width(self, w_divide_h):  
        """按照宽度进行所需比例缩放"""  
        im = Image.open(self.infile)  
        (x, y) = im.size   
        x_s = x  
        y_s = x/w_divide_h  
        out = im.resize((x_s, y_s), Image.ANTIALIAS)   
        out.save(self.outfile)  


    def resize_by_height(self, w_divide_h):  
        """按照高度进行所需比例缩放"""  
        im = Image.open(self.infile)  
        (x, y) = im.size   
        x_s = y*w_divide_h  
        y_s = y  
        out = im.resize((x_s, y_s), Image.ANTIALIAS)   
        out.save(self.outfile)  


    def resize_by_size(self, size):  
        """按照生成图片文件大小进行处理(单位KB)"""  
        size *= 1024  
        im = Image.open(self.infile)  
        size_tmp = os.path.getsize(self.infile)  
        q = 100  
        while size_tmp > size and q > 0:  
            print (q)  
            out = im.resize(im.size, Image.ANTIALIAS)  
            out.save(self.outfile, quality=q)  
            size_tmp = os.path.getsize(self.outfile)  
            q -= 5  
        if q == 100:  
            shutil.copy(self.infile, self.outfile)  

  
    def cut_by_ratio(self):  
        """按照图片长宽进行分割
        
        ------------
        取中间的部分，裁剪成正方形
        """  
        im = Image.open(self.infile)  
        (x, y) = im.size  
        if x > y:  
            region = (int(x/2-y/2), 0, int(x/2+y/2), y)  
            #裁切图片  
            crop_img = im.crop(region)  
            #保存裁切后的图片  
            crop_img.save(self.outfile)             
        elif x < y:  
            region = (0, int(y/2-x/2), x, int(y/2+x/2))
            #裁切图片  
            crop_img = im.crop(region)  
            #保存裁切后的图片  
            crop_img.save(self.outfile)       


# 定义压缩比，数值越大，压缩越小
SIZE_normal = 1.0
SIZE_small = 1.5
SIZE_more_small = 2.0
SIZE_more_small_small = 3.0


def make_directory(directory):
    """创建目录"""
    os.makedirs(directory)


def directory_exists(directory):
    """判断目录是否存在"""
    if os.path.exists(directory):
        return True
    else:
        return False


def list_img_file(directory):
    """列出目录下所有文件，并筛选出图片文件列表返回"""
    old_list = os.listdir(directory)
    # print old_list
    new_list = []
    for filename in old_list:
        name, fileformat = filename.split(".")
        if fileformat.lower() == "jpg" or fileformat.lower() == "png" or fileformat.lower() == "gif":
            new_list.append(filename)
    # print new_list
    return new_list


def print_help():
    print("""
    This program helps compress many image files
    you can choose which scale you want to compress your img(jpg/png/etc)
    1) normal compress(4M to 1M around)
    2) small compress(4M to 500K around)
    3) smaller compress(4M to 300K around)
    """)


def compress(choose, des_dir, src_dir, file_list):
    """压缩算法，img.thumbnail对图片进行压缩，
    
    参数
    -----------
    choose: str
            选择压缩的比例，有4个选项，越大压缩后的图片越小
    """
    choose = input()
    if choose == '1':
        scale = SIZE_normal
    if choose == '2':
        scale = SIZE_small
    if choose == '3':
        scale = SIZE_more_small
    if choose == '4':
        scale = SIZE_more_small_small
    for infile in file_list:
        img = Image.open(src_dir+infile)
        # size_of_file = os.path.getsize(infile)
        w, h = img.size
        img.thumbnail((int(w/scale), int(h/scale)))
        img.save(des_dir + infile)


def compress_photo():
    '''调用压缩图片的函数
    '''
    src_dir, des_dir = "photos/", "min_photos/"
    
    if directory_exists(src_dir):
        if not directory_exists(src_dir):
            make_directory(src_dir)
        # business logic
        file_list_src = list_img_file(src_dir)
    if directory_exists(des_dir):
        if not directory_exists(des_dir):
            make_directory(des_dir)
        file_list_des = list_img_file(des_dir)
        # print file_list
    '''如果已经压缩了，就不再压缩'''
    for i in range(len(file_list_des)):
        if file_list_des[i] in file_list_src:
            file_list_src.remove(file_list_des[i])
    compress('1', des_dir, src_dir, file_list_src)


def handle_photo():
    '''根据图片的文件名处理成需要的json格式的数据
    
    -----------
    最后将data.json文件存到博客的source/photos文件夹下
    '''
    src_dir, des_dir = "photos/", "min_photos/"
    file_list = list_img_file(src_dir)
    list_info = []
    for i in range(len(file_list)):
        filename = file_list[i]
        date_str, *info = filename.split("_")
        info='_'.join(info)
        info, _ = info.split(".")
        date = datetime.strptime(date_str, "%Y-%m-%d")
        year_month = date_str[0:7]            
        if i == 0:  # 处理第一个文件
            new_dict = {"date": year_month, "arr":{'year': date.year,
                                                                   'month': date.month,
                                                                   'link': [filename],
                                                                   'text': [info],
                                                                   'type': ['image']
                                                                   }
                                        } 
            list_info.append(new_dict)
        elif year_month != list_info[-1]['date']:  # 不是最后的一个日期，就新建一个dict
            new_dict = {"date": year_month, "arr":{'year': date.year,
                                                   'month': date.month,
                                                   'link': [filename],
                                                   'text': [info],
                                                   'type': ['image']
                                                   }
                        }
            list_info.append(new_dict)
        else:  # 同一个日期
            list_info[-1]['arr']['link'].append(filename)
            list_info[-1]['arr']['text'].append(info)
            list_info[-1]['arr']['type'].append('image')
    list_info.reverse()  # 翻转
    final_dict = {"list": list_info}
    with open("../../blog/themes/next/source/lib/album/data.json","w") as fp:
        json.dump(final_dict, fp)


def cut_photo():
    """裁剪算法
    
    ----------
    调用Graphics类中的裁剪算法，将src_dir目录下的文件进行裁剪（裁剪成正方形）
    """
    src_dir = "photos/"
    if directory_exists(src_dir):
        if not directory_exists(src_dir):
            make_directory(src_dir)
        # business logic
        file_list = list_img_file(src_dir)
        # print file_list
        if file_list:
            print_help()
            for infile in file_list:
                img = Image.open(src_dir+infile)
                Graphics(infile=src_dir+infile, outfile=src_dir + infile).cut_by_ratio()            
        else:
            pass
    else:
        print("source directory not exist!")     


def git_operation():
    
    os.system('git add --all')
    os.system('git commit -m "add photos"')
    os.system('git push origin master')


# if __name__ == "__main__":
#     cut_photo()        # 裁剪图片，裁剪成正方形，去中间部分
#     compress_photo()   # 压缩图片，并保存到mini_photos文件夹下
#     git_operation()    # 提交到github仓库
#     handle_photo()     # 将文件处理成json格式，存到博客仓库中
cut_photo()        # 裁剪图片，裁剪成正方形，去中间部分
compress_photo()   # 压缩图片，并保存到mini_photos文件夹下
git_operation()    # 提交到github仓库
handle_photo()     # 将文件处理成json格式，存到博客仓库中   
    
    
    