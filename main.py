import pyautogui
import time
import random
import pyautogui as pag
import keyboard
import tkinter as tk
import tkinter.messagebox
import threading

import sys

"""
阴阳师自动脚本
v1.0
*点击事件需插入随机坐标/延时
"""


# 点击位置（屏幕右下角）
def default_position():
    click_x = random.randint(1500, 2000)
    click_y = random.randint(700, 1000)
    position = (click_x, click_y)
    return position


# 随机生成时间（输出为输入时间-1秒到1+秒内）
def random_time(get_time=1, Range=1):
    return random.uniform(get_time - Range, get_time - Range)


# 获取鼠标位置函数()按p打印
def get_mouse():
    while True:
        if keyboard.read_key() == "p":
            print(pag.position())


# 普通目标副本
class CommonTarget:

    def __init__(self, fight_target):
        self.fight_target = fight_target
        self.center = None
        self.position = None
        self.button = True

    # 获取目标位置函数
    def get_target(self):
        fight_target = self.fight_target
        tar = pyautogui.locateOnScreen(fight_target, confidence=0.8)
        if tar is None:

            print("{0}无目标".format(fight_target))

        else:

            left, top, width, height = tar
            print("目标：", tar)
            self.center = pyautogui.center((left, top, width, height))

    # 随机生成目标周围一点并返回
    def generate_points(self, random_range=10):
        if self.center is not None:
            click_x, click_y = self.center
            click_x = click_x + random.randint(-random_range, random_range)
            click_y = click_y + random.randint(-random_range, random_range)
            self.position = (click_x, click_y)
            print("随机生成坐标：", self.position)

    # 点击指定位置函数
    def click_target(self, count=1, wait_time=random_time()):
        if self.position is not None:
            for i in range(count):
                print("点击", self.position)
                pyautogui.click(self.position)
                time.sleep(wait_time)

    # 运行
    def run(self):
        if self.center is not None:
            self.generate_points()
            if self.position is not None:
                self.click_target()
                self.center = None
                self.position = None
                time.sleep(2)

    # 鼠标拖动函数
    # def mouse_drag(self, start_x, start_y, stop_x, stop_y):
    #     start_ = start_x, start_y
    #     stop_ = stop_x, stop_y
    #     x1, y1 = self.generate_points()
    #     x2, y2 = self.generate_points()
    #     pyautogui.mouseDown(x1, y1, button='left')
    #     pyautogui.moveTo(x2, y2, 4, pyautogui.easeInOutQuad)
    #     pyautogui.mouseUp(button='left')


# 其他类型脚本（点击位置为固定右下脚）
class AnotherTarget(CommonTarget):
    def __init__(self, fight_target):
        CommonTarget.__init__(self, fight_target)
        self.fight_target = fight_target
        self.position = None

    def click_target(self, count=1, wait_time=random_time()):
        if self.position is not None:
            for i in range(count):
                print("点击", default_position())
                pyautogui.click(default_position())
                time.sleep(wait_time)


# 初始化需要点击的目标
x = AnotherTarget('win_2.png')
y = CommonTarget('target.png')
z = AnotherTarget('win.png')


# 进程的启动/暂停/继续
class MyThread(threading.Thread):

    def __init__(self, *args, **kwargs):
        super(MyThread, self).__init__(*args, **kwargs)
        self.__flag = threading.Event()  # 用于暂停线程的标识
        self.__flag.set()  # 设置为True
        self.__running = threading.Event()  # 用于停止线程的标识
        self.__running.set()  # 将running设置为True

    def run(self):
        while self.__running.is_set():
            self.__flag.wait()  # 为True时立即返回, 为False时阻塞直到内部的标识位为True后返回
            time.sleep(2)
            z.get_target()
            x.get_target()
            y.get_target()
            x.run()
            y.run()
            z.run()

    def pause(self):
        self.__flag.clear()  # 设置为False, 让线程阻塞

    def resume(self):
        self.__flag.set()  # 设置为True, 让线程停止阻塞

    def stop(self):
        self.__flag.set()  # 将线程从暂停状态恢复, 如何已经暂停的话
        self.__running.clear()  # 设置为False


button = 1


# 线程控制方法
def Thread_to():
    global button
    if button == 0:
        print("开始进程")
        t1.start()
    elif button == 1:
        print("暂停进程")
        t1.pause()
    elif button == 2:
        print("停止进程")
        t1.pause()
        t1.stop()


# 主函数
class MainClass:

    def __init__(self):
        self.oc = False

        self.root = tk.Tk()
        self.var = tk.StringVar()
        self.var.set('关闭中')
        self.root.geometry('480x240')
        self.root.title("小陈yys防检测脚本V1.0"),
        self.root.resizable(width=True, height=True),

        self.button = tk.Button(self.root,
                                textvariable=self.var,
                                command=self.Open_Close
                                )
        self.button.pack()
        self.root.protocol("WM_DELETE_WINDOW", self.JieShu)
        self.root.mainloop()

    def JieShu(self):
        global button
        tk.messagebox.showwarning(title='警告', message='正在退出脚本！')
        button = False
        button = 2
        Thread_to()

        sys.exit(0)

        # 销毁root窗口

    # 修改按钮文字（向线程控制发送数据）
    def Open_Close(self):
        global button
        if not self.oc:
            self.oc = True
            self.var.set('开启中')
            button = 0
            Thread_to()

        else:
            self.oc = False
            self.var.set('关闭中')
            button = 1
            Thread_to()


if __name__ == '__main__':
    t1 = MyThread()

Run = MainClass
Run()
