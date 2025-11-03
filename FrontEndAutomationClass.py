import win32con
import time
import WinControl
import random
from win32api import SetCursorPos,mouse_event,keybd_event
# import win32clipboard
# wincontrol = WinControl.WinControl()

"""
============================时间定义===========================
单击：200~500毫秒时间内，按下一次
双击：200~500毫秒时间内，按下两次
长按：大于500毫秒时间外，按下一次
鼠标后摇：10~25毫秒
按键后摇:100~250毫秒
统一后摇：0~250毫秒
统一单击按下和弹起的时间延迟：300毫秒
统一双击按下和弹起的时间延迟：500毫秒
封装后所有操作在1000毫秒内实现
"""
class FrontEndAutomation:
    """======================================================鼠标模拟============================================================"""
    def random_delay(self,Delay=50,Cooldown=50):
        """
        :param Delay: （按下和弹起之间的）延迟时间,50比较好，200是电脑反应慢的
        :param Cooldown:弹起后的延迟时间=设备反应时间/加多的随机延迟时间
        :return:
        """
        TotalDelay = (random.randint(Delay,(Delay+Cooldown)))/1000.0
        #sleep函数是秒级别的参数，毫米要转换成毫秒需要/1000.0
        time.sleep(TotalDelay)

    def mouse_once_click(self ,x, y, mouse_style=2,delay=50,cooldown=50):
        """
        鼠标移动+鼠标单击，默认左击
        :param x:屏幕x坐标
        :param y:屏幕y坐标
        :param mouse_style:鼠标点击方式：
        win32con.MOUSEEVENTF_MOVE-移动:1
        win32con.MOUSEEVENTF_ABSOLUTE-屏幕为绝对坐标系:32768

        win32con.MOUSEEVENTF_LEFTDOWN-左键按下:2
        win32con.MOUSEEVENTF_LEFTUP-左键释放:4

        win32con.MOUSEEVENTF_RIGHTDOWN-右键按下:8
        win32con.MOUSEEVENTF_RIGHTUP-右键释放:16

        win32con.MOUSEEVENTF_MIDDLEDOWN-中键按下:32
        win32con.MOUSEEVENTF_MIDDLEUP-中键释放:64
        """
        # mouse_event(1 | 32768, x, y, 0, 0)  # 鼠标绝对移动,用不了
        SetCursorPos((x,y))#可以用这个代替
        self.random_delay() #随机延迟
        mouse_event(mouse_style, 0, 0, 0, 0)  # 按下鼠标
        self.random_delay() #随机延迟，小于300毫秒
        mouse_event(mouse_style * 2, 0, 0, 0, 0)  # 释放鼠标
        self.random_delay(delay,cooldown) #后摇时间


    def mouse_many_click(self,x, y, mouse_style=2,times=2,delay=100,cooldown=10):
        """
       鼠标多次点击，默认左击+双击
       :param x:屏幕x坐标
       :param y:屏幕y坐标
       :param mouse_style:鼠标点击方式：
       win32con.MOUSEEVENTF_MOVE-移动:1
       win32con.MOUSEEVENTF_ABSOLUTE-屏幕为绝对坐标系:32768

       win32con.MOUSEEVENTF_LEFTDOWN-左键按下:2
       win32con.MOUSEEVENTF_LEFTUP-左键释放:4

       win32con.MOUSEEVENTF_RIGHTDOWN-右键按下:8
       win32con.MOUSEEVENTF_RIGHTUP-右键释放:16

       win32con.MOUSEEVENTF_MIDDLEDOWN-中键按下:32
       win32con.MOUSEEVENTF_MIDDLEUP-中键释放:64
       :param Delay:必定延迟时间
       :param Cooldown:随机延迟时间
       """
        for i in range(times):
            # mouse_event(1 | 32768, x, y, 0, 0)  # 鼠标绝对移动，用不了
            SetCursorPos((x,y))#可以用这个代替
            self.random_delay()  # 随机延迟
            mouse_event(mouse_style, 0, 0, 0, 0)  # 按下鼠标
            self.random_delay()  # 随机延迟，小于300毫秒
            mouse_event(mouse_style * 2, 0, 0, 0, 0)  # 释放鼠标
            self.random_delay(delay, cooldown)  # 后摇时间


    def mouse_longdown_click(self, x, y,mouse_style=2,delay=1000):
        """
        :param x: 屏幕的x坐标
        :param y: 屏幕的x坐标
        :param delay:长按的延迟时间
        """
        mouse_event(1 | 32768, x, y, 0, 0)  # 鼠标绝对移动
        self.random_delay(200,50) #随机延迟
        mouse_event(mouse_style, 0, 0, 0, 0)  # 按下鼠标
        self.random_delay(delay,0) #随机延迟，小于500毫秒
        mouse_event(mouse_style * 2, 0, 0, 0, 0)  # 释放鼠标
        # SetCursorPos(x,y)#可以用这个代替
        self.random_delay(200,50) #后摇时间

    def mouse_wheel(self,times, up=False,delay=200):
        """
        鼠标滚轮模拟，默认一次120滚轮量
        :param times: 滚轮次数
        :param up: 默认向上滚轮关闭
        """
        for i in range(times):
            mouse_event(2048, 0, 0, (120 if up else -120), 0)
            # self.random_delay(100,0)鸣潮会反应不过来
        self.random_delay(delay,0)

    def mouse_perspective_move(self,move_x,move_y,move_time):
        """
        鼠标相对移动
        :param move_x:水平视角一次移动的大小
        :param move_y:垂直视角一次移动的大小
        :param move_time:移动的次数
        :return:
        """
        for i in range(move_time):
            mouse_event(1, move_x, move_y, 0, 0)
            self.random_delay(5,10)
    """====================================================键盘模拟============================================================"""
    def key_down_times(self, vk_code: int | str,times=1,delay=50,cooldown=50):
        """
        使用扫描码模拟按键操作更隐蔽
        以下是常见的游戏的按键码：
        "A"	65
        "W"	87
        "D"	68
        "S"	83
        "R"	82
        "Enter"   13
     "baskspace"  8,删除
        "Ctrl"    17
        "Shift"   16
        "Esc"     27
        "Delete"  127,执行不了，其他库也一样
        "F1-F5"   112-116
        :param vk_code: 虚拟键码,字符型转整型
        :param times:按键次数，默认一次
        """
        for i in range(times):
            vk_code = ord(vk_code.upper()) if isinstance(vk_code, str) else vk_code
            keybd_event(vk_code, 0, 0, 0)  # 按下
            self.random_delay(0, 50)  # 模拟按键按下后的延迟
            keybd_event(vk_code, 0, win32con.KEYEVENTF_KEYUP,0)  # 释放
            self.random_delay(delay,cooldown)  # 模拟按键释放后的延迟



    def key_down_long(self, vk_code: int | str, delaytime=1000):
        """
        使用扫描码模拟按键操作
        win32con.KEYEVENTF_KEYUP-按下:2
        :param vk_code: 虚拟键码
        """
        vk_code = ord(vk_code.upper()) if isinstance(vk_code, str) else vk_code
        keybd_event(vk_code, 0, 0, 0)  # 按下
        self.random_delay(delaytime, 0)  # 模拟按键按下后的延迟
        keybd_event(vk_code, 0,2,0)  # 释放
        self.random_delay()  # 模拟按键释放后的延迟

    def MessageCV(self,text):
        # 打开剪贴板
        win32clipboard.OpenClipboard()
        # 清空剪贴板
        win32clipboard.EmptyClipboard()
        # 设置文本
        win32clipboard.SetClipboardText(text, win32con.CF_UNICODETEXT)
        # 关闭剪贴板
        win32clipboard.CloseClipboard()
        # 模拟Ctrl+V粘贴
        keybd_event(win32con.VK_CONTROL, 0, 0, 0)
        keybd_event(ord('V'), 0, 0, 0)
        time.sleep(0.05)
        keybd_event(ord('V'), 0, win32con.KEYEVENTF_KEYUP, 0)
        keybd_event(win32con.VK_CONTROL, 0, win32con.KEYEVENTF_KEYUP, 0)

if __name__ == '__main__':
    # time.sleep(2)
    frontend=FrontEndAutomation()
    frontend.random_delay(1000,0)
    # frontend.MessageCV("我在哪")
    # frontend.mouse_once_click(1302,315)
    # frontend.mouse_many_click(1302, 315)
    # frontend.mouse_longdown_click(1302,315)
    # frontend.key_down_times("W")
    # frontend.key_down_long("W",5000)
    # frontend.text_input("231joi")
    # frontend.key_down_times(13)
    # frontend.key_down_times(win32con.DELETE)
    # frontend.key_down_times()
    # for i in range(5):
    #     frontend.mouse_once_click(360 + 120*i, 210)
    #     frontend.key_down_times(27)
    # for i in range(6):  # 三页
    #     frontend.mouse_wheel(26)  # 翻页
    #     for j in range(5):  # 五行
    #         for k in range(3):  # 三列
    #             # 点击物品，(初始坐标x+相隔x*k,初始坐标y+相隔y*j)
    #             frontend.mouse_once_click(158 + k * 132, 196 + j * 156)
        # frontend.random_delay(3000,0)

    # frontend.mouse_wheel(0)









