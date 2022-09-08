# -*- coding: utf-8-*-
# Author: Jack Cui
#UI written by Frank Hua
import sys
from turtle import width
import cv2
from PIL import Image
import numpy as np
from tkinter import *
import tkinter.messagebox

from tkinter import filedialog
from tkinter.messagebox import *
my_path=""
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
    
    return(text)
def Text2Img(txt_fname, save_fname):
    with open(txt_fname, "r", encoding="utf-8") as f:
        text = f.read()
    text_len = len(text)
    img_w = 4000
    img_h = 3000
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

window = Tk()
window.title("基于卷积操作的图片隐藏程序")
window.geometry('400x300')
button = Button(text="选择一张加密图片", command=openFile,width=20,height=5)

button.pack()


window.mainloop()
if my_path == '':
          window=Tk()
          window.title('出现错误')
          lb=tkinter.Label(window,text="如果你看到此错误，\n说明你可能没有选择加密的图片，\n或者加密的图片放在系统盘（c盘），\n请将图片移动到其他盘（如D盘），\n然后重试。",font=('微软雅黑',14),width=30,height=10)
          lb.pack()
          window.mainloop()
          sys.exit()
       

print(my_path)
txt_res_img_path = (my_path)

   # 从藏有文本的大图中，解析出文本小图
parsed_img_text_fname = "pares_text_img.png"
parsed_img_text = parse_from_img(txt_res_img_path)
cv2.imwrite(parsed_img_text_fname, parsed_img_text)

    # 从文本图片中，解析出文字
final_text=Img2Text(parsed_img_text_fname)
root=tkinter.Tk()
root.title("解密结果")
lb=tkinter.Label(root,text=final_text,font=('微软雅黑',18),width=30,height=10)
lb.pack()
root.mainloop()





























                   
