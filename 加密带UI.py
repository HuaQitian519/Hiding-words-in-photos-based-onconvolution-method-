# -*- coding: utf-8-*-
# Author: Jack Cui
# UI and self-adaption algorithm programmed by ：Frank Hua 
import sys
from turtle import width
import cv2
from PIL import Image as editer
import numpy as np
from tkinter import *
import tkinter.messagebox
import tkinter as TK
from tkinter import filedialog
from tkinter.messagebox import *
my_path=""
class _Inputbox():
    def  __init__(self,text=""):
        self._root = TK.Tk()
        self.get=""
        sw = self._root.winfo_screenwidth()
        sh = self._root.winfo_screenheight()
        width=600
        height=200
        startx=(sw-width)/2
        starty=(sh-height)/2
        
        self._root.geometry("%dx%d%+d%+d"%(width,height,startx,starty))
        self._root.title("基于卷积操作的图片隐藏程序")
        self.label_file_name=TK.Label(self._root,text=text,font=('微软雅黑',14))
        self.label_file_name.pack()
        self.entry=TK.Text(width=70,height=10)
        self.entry.pack(padx=10,side=TK.LEFT)
        self.entry.focus()
        self.entry.bind()
        self.submit=TK.Button(self._root,text="确定",command=self.getinput,height=2,width=8)
        self.submit.pack(padx=25,side=TK.RIGHT)
        self._root.mainloop()
    def getinput(self):
        self.get=self.entry.get("1.0","end")
        self._root.destroy()
def parse_from_img(img_path):
    img = cv2.imread(img_path)
    img_h, img_w, _ = img.shape

    stepx = 10
    stepy = 10

    sml_w = img_w // stepx
    sml_h = img_h // stepy

    res_img = np.zeros((sml_h, sml_w, 3), np.uint8)

    for m in range(0, sml_w):
        for n in range(0, sml_h):
            map_col = int(m * stepx + stepx * 0.5)
            map_row = int(n * stepy + stepy * 0.5)
            res_img[n, m] = img[map_row, map_col]

    return res_img

def generate_img(big_img_path, small_img_path):

    big_img = cv2.imread(big_img_path)
    sml_img = cv2.imread(small_img_path)
    
    dst_img = big_img.copy()

    big_h, big_w, _ = big_img.shape
    sml_h, sml_w, _ = sml_img.shape

    stepx = big_w / sml_w
    stepy = big_h / sml_h

    for m in range(0, sml_w):
        for n in range(0, sml_h):
            map_col = int(m * stepx + stepx * 0.5)
            map_row = int(n * stepy + stepy * 0.5)

            if map_col < big_w and map_row < big_h:
                dst_img[map_row, map_col] = sml_img[n, m]

    return dst_img

def Img2Text(img_fname):
    img = cv2.imread(img_fname)
    height, width, _ = img.shape
    text_list = []
    for h in range(height):
        for w in range(width):
            R, G, B = img[h, w]
            if R | G | B == 0:
                break
            idx = (G << 8) + B
            text_list.append(chr(idx))
    text = "".join(text_list)
    with open("斗破苍穹_dec.txt", "a", encoding="utf-8") as f:
        f.write(text)

def Text2Img( save_fname):
   
    text_len = len(text)
    #匹配图像分辨率
    img_w = int(size[0]/10)
    img_h = int(size[1]/10)
    img = np.zeros((img_h, img_w, 3))
    x = 0
    y = 0
    for each_text in text:
        idx = ord(each_text)
        rgb = (0, (idx & 0xFF00) >> 8, idx & 0xFF)
        img[y, x] = rgb
        if x == img_w - 1:
            x = 0
            y += 1
        else:
            x += 1
    cv2.imwrite(save_fname, img)

def big_with_small(big_img_path, small_img_path, res_img_path):
    """
    大图里藏小图
    """
    dst_img = generate_img(big_img_path, small_img_path)
    cv2.imwrite(res_img_path, dst_img)




def openFile():
    
      global my_path
      filePath = filedialog.askopenfilename(filetypes=(("PNG图片（目前仅支持，后期会拓展其他格式）", "*.png"),))
      my_path = filePath
      
      window.destroy()
#获取图片
window = Tk()
window.title("基于卷积操作的图片隐藏程序")
window.geometry('400x180')
button = Button(text="选择一张图片", command=openFile,width=20,height=10,font=('微软雅黑',14))

button.pack()


window.mainloop()
if my_path == '':
          window=Tk()
          window.title('出现错误')
          lb=tkinter.Label(window,text="请选择一张图片，然后点击确定！",font=('微软雅黑',14),width=30,height=10)
          lb.pack()
          window.mainloop()
          sys.exit()
          
          
          
       

big_img_path = my_path
i = _Inputbox('请输入要加密的内容：')
global text
text=i.get
global size
size = editer.open(big_img_path).size#获取图片分辨率进行自适应加密
txt_img_fname = "cache.png"
txt_res_img_path = "final.png"
Text2Img(txt_img_fname)

# 将生成的文本图片，藏于大图中，并保存结果
big_with_small(big_img_path, txt_img_fname, txt_res_img_path)






























                   
