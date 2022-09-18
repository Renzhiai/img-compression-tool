# coding = utf-8
# !/usr/bin/python

from tkinter import Tk, StringVar, Frame, Label, Entry, Button, E, W
import threading
import os
from tkinter.filedialog import askdirectory
import traceback
from PIL import Image


class Tool:
    def __init__(self):
        self.root = Tk()
        self.root.title('图片压缩工具')
        self.path = StringVar()
        self.frame_exe = Frame()
        self.frame_exe.pack()
        row_title, row_tips, row_rate, row_limit, row_path = 1, 2, 3, 4, 5
        row_exe, row_reminder = 6, 7
        padx_title, pady_title = 150, 10
        padx_label, pady_label = 10, 20
        # 标题
        label_title = Label(self.frame_exe, text='压缩前先备份图片', font=('微软雅黑', 20))
        label_title.grid(row=row_title, column=0, columnspan=4, padx=padx_title, pady=pady_title)
        # 说明
        label_title = Label(self.frame_exe, text='图片支持JPG、PNG、JPEG', font=('微软雅黑', 10))
        label_title['fg'] = 'red'
        label_title.grid(row=row_tips, column=0, columnspan=4, padx=padx_title, pady=pady_title)
        # 压缩比例
        label_rate = Label(self.frame_exe, text='压缩比例：')
        label_rate.grid(row=row_rate, column=1, sticky=E, padx=padx_label, pady=pady_label)
        self.entry_rate = Entry(self.frame_exe, textvariable='1')
        self.entry_rate.grid(row=row_rate, column=2, sticky=W, padx=padx_label, pady=pady_label)
        # 比例大小默认为0.8
        self.entry_rate.insert(0, '0.8')
        # 图片大小
        label_limit = Label(self.frame_exe, text='图片大于(KB)才压缩：')
        label_limit.grid(row=row_limit, column=1, sticky=E, padx=padx_label, pady=pady_label)
        self.entry_limit = Entry(self.frame_exe)
        self.entry_limit.grid(row=row_limit, column=2, sticky=W, padx=padx_label, pady=pady_label)
        # 路径
        self.entry_path = Entry(self.frame_exe, textvariable=self.path)
        self.entry_path.grid(row=row_path, column=0, columnspan=3, sticky=W + E, padx=padx_label, pady=pady_label)
        # 这里选择的是文件夹，程序会压缩文件夹里面所有符合格式的图片
        button_path = Button(self.frame_exe, text="路径选择", command=self.selectPath)
        button_path.grid(row=row_path, column=3, sticky=W + E, padx=padx_label, pady=pady_label)
        # 运行
        self.btn_exe = Button(self.frame_exe, text='执行', command=self.execute)
        self.btn_exe.grid(row=row_exe, column=1, sticky=E, padx=padx_label)
        # 退出
        self.btn_quit = Button(self.frame_exe, text='退出', command=self.quit)
        self.btn_quit.grid(row=row_exe, column=2, padx=padx_label)
        # 提示语
        self.label_remind = Label(self.frame_exe, text='')
        self.label_remind.grid(row=row_reminder, column=0, columnspan=3, sticky=W + E)

    def run(self):
        self.root.mainloop()

    def selectPath(self):
        _path = askdirectory()
        self.path.set(_path)

    def quit(self):
        self.root.destroy()

    def is_number(self, num):
        try:
            float(num)
            return True
        except ValueError:
            return False

    def execute(self):
        path = self.entry_path.get().strip()
        rate = self.entry_rate.get().strip()
        limit = self.entry_limit.get().strip()
        if len(path) == 0 or len(rate) == 0 or len(limit) == 0:
            self.label_remind['text'] = '输入不能为空'
            self.label_remind['fg'] = 'red'
            return
        if not self.is_number(rate) or not self.is_number(limit):
            self.label_remind['text'] = '请输入数字'
            self.label_remind['fg'] = 'red'
            return
        if float(limit) < 1:
            self.label_remind['text'] = '图片压缩设置不能小于1KB'
            self.label_remind['fg'] = 'red'
            return
        # 按钮置灰
        self.btn_exe['state'] = 'disabled'
        # 重置提示语
        self.label_remind['text'] = ''
        # 运行
        t1 = threading.Thread(target=self.convert)
        t1.start()

    def stop(self):
        self.btn_exe['state'] = 'active'  # 激活执行按钮

    def convert(self):
        count = 0
        path = self.entry_path.get().strip()
        rate = self.entry_rate.get().strip()
        limit = self.entry_limit.get().strip()
        path = path + '/'
        img_type = ['JPG', 'PNG', 'JPEG']
        try:
            for filename in os.listdir(path):
                if filename.split('.')[-1].upper() in img_type \
                        and os.path.getsize(path + filename) / 1024 >= int(limit):
                    s_img = Image.open(path + filename)
                    if s_img.mode in ['P', 'RGBA']:
                        s_img = s_img.convert('RGB')
                    w, h = s_img.size
                    d_img = s_img.resize((int(w * float(rate)), int(h * float(rate))),
                                         Image.Resampling.LANCZOS)  # 设置压缩尺寸和选项
                    d_img.save(path + filename)  # 也可以用srcFile原路径保存,或者更改后缀保存
                    count = count + 1
            self.label_remind['text'] = '压缩完成，共有{}张图片被压缩'.format(count)
            self.label_remind['fg'] = 'green'
        except:
            self.label_remind['text'] = traceback.format_exc()
            self.label_remind['fg'] = 'red'
        finally:
            self.stop()


t = Tool()
t.run()
