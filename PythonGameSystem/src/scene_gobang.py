# 导入所需的库
from tkinter import *
import tkinter.messagebox  # 弹窗库
import numpy as np

# 创建窗口并设置窗口名字
root = Tk()
root.title("五子棋游戏")

# 创建画布
w1 = Canvas(root, width=600, height=600, background='chocolate')
w1.pack()

# 绘制棋盘线和五个黑子
for i in range(0, 15):
    w1.create_line(i * 40 + 20, 20, i * 40 + 20, 580)
    w1.create_line(20, i * 40 + 20, 580, i * 40 + 20)
w1.create_oval(135, 135, 145, 145, fill='black')
w1.create_oval(135, 455, 145, 465, fill='black')
w1.create_oval(465, 135, 455, 145, fill='black')
w1.create_oval(455, 455, 465, 465, fill='black')
w1.create_oval(295, 295, 305, 305, fill='black')

# 初始化变量
num = 0
A = np.full((15, 15), 0)
B = np.full((15, 15), '')


# 鼠标点击的回调函数
def callback(event):
    global num, A

    # 根据鼠标点击的位置确定落子的坐标
    for j in range(0, 15):
        for i in range(0, 15):
            if (event.x - 20 - 40 * i)**2 + (event.y - 20 -
                                             40 * j)**2 <= 2 * 20**2:
                break
        if (event.x - 20 - 40 * i)**2 + (event.y - 20 -
                                         40 * j)**2 <= 2 * 20**2:
            break

    # 根据落子的顺序和位置绘制黑白棋子，并检查游戏是否结束
    # 如果游戏结束，则弹窗显示结果
    # 每次落子后将计数加1
    # 如果黑白棋赢则终止游戏
    # 如果没有结果则继续游戏
    # 绘制黑白棋，并检查游戏是否结束
    # 如果游戏结束，则弹窗显示结果
    # 将计数加1


w1.bind("<Button -1>", callback)
w1.pack()


# 退出游戏的函数
def quit():
    root.quit()


# 创建退出按钮和返回按钮
u = Button(root, text="退出", width=10, height=1, command=quit, font=('楷体', 15))
b = Button(root, text="返回", width=10, height=1, command=quit, font=('楷体', 15))
u.pack()
b.pack()

# 运行窗口主体循环
mainloop()

