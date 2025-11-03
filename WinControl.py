import time
import win32gui
import win32con
import pywintypes
class WinControl:
    #私有成员
    __TemporaryHwnd=0 #临时句柄
    __CurrentHwnd= 0#当前窗口句柄
    __LocaLscaling=1
    def __init__(self,scaling=1):
        self.__LocaLscaling=scaling
        # print("WinControl类的句柄是：__CurrentHwnd")



    #展示句柄窗口的信息（无参数)
    def ShowInformation(self,Hwnd):
        if Hwnd:
            # 获取窗口标题
            title = win32gui.GetWindowText(Hwnd)
            # 获取窗口类名
            class_name = win32gui.GetClassName(Hwnd)
            #返回当前窗口句柄
            print(f"""当前窗口句柄: {Hwnd}\n当前窗口标题: {title}\n当前窗口类名: {class_name}""")
        else:
            print(f"未找到当前活动窗口句柄，当前句柄为：{Hwnd}")

    # 获取当前活动窗口的句柄无参数)
    def GetCurrentHwnd(self):
        self.__CurrentHwnd = win32gui.GetForegroundWindow()
        self.ShowInformation(self.__CurrentHwnd)
        return self.__CurrentHwnd

    #循环获取当前窗口句柄(无参数)
    def CycleCurrentWindow(self):
        print("每2秒获取1次句柄")
        while True:
            self.__CurrentHwnd = win32gui.GetForegroundWindow()
            try:
                self.ShowInformation(self.__CurrentHwnd)
                print("\n")
                time.sleep(2.0)  # 每2.0秒获取一次
            except KeyboardInterrupt:  # 捕获用户中断（Ctrl+C）
                print("程序被用户中断")
                break
            except Exception as e:  # 捕获其他异常
                print(f"发生错误: {e}")

    #获取句柄（类名，标题）
    def GetHwnd(self,classname, title):
         return win32gui.FindWindow(classname, title)
    #获取窗口信息（句柄）
    def GetWinBaseInformation(self,Hwnd):
        """
            left, top, right, bottom = win32gui.GetWindowRect(句柄)
            left：窗口左边界相对于屏幕的水平坐标。
            top：窗口上边界相对于屏幕的垂直坐标。
            right：窗口右边界相对于屏幕的水平坐标。
            bottom：窗口下边界相对于屏幕的垂直坐标。
        """
        left, top, right, bottom = win32gui.GetWindowRect(Hwnd)
        print(f"窗口:{Hwnd},坐标信息如下：")
        print(f"左上坐标({left,top})")
        print(f"右下坐标({right,bottom})")
        width = right - left
        height = bottom - top
        print(f"窗口宽度: {width}")
        print(f"窗口高度: {height}")
        #返回坐上坐标、宽、高
        return left, top, width, height

    #永久激活并置顶窗口（句柄，是/否），要解除的
    def WindowTop(hwnd, topmost=True):
        """
        设置窗口是否置顶
        :param hwnd: 窗口句柄
        :param topmost: 是否置顶，True为置顶，False为正常
        """
        flags = win32con.SWP_NOSIZE | win32con.SWP_NOMOVE  # 不改变窗口大小和位置
        if topmost:
            win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, flags)
        else:
            win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0, flags)

    # 将句柄窗口恢复、最大、最小
    def WindowMize(self,hwnd,cmd=0):
        """
            0:恢复窗口大小
            1：最大化窗口
            2：最小化窗口
            3.隐藏窗口：任务栏不显示
            4.激活窗口
            5.全屏窗口
        """
        try:
            if cmd == 0:
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                print(f"句柄{hwnd}，恢复初始化")
            elif cmd == 1:
                # 确保窗口在最上面
                win32gui.SetForegroundWindow(hwnd)
                # 最大化窗体
                win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
                print(f"句柄{hwnd}，最大化")
            elif cmd == 2:
                win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
                print(f"句柄{hwnd}，最小化")
            elif cmd == 3:
                win32gui.ShowWindow(hwnd, win32con.SW_HIDE)
                print(f"句柄{hwnd}，隐藏化")
            elif cmd == 4:
                win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
                print(f"句柄{hwnd}，显示化")
            else:
                print("无效的命令参数。请输入 0（恢复）、1（最大化）、2（最小化）、3（隐藏窗口）或 4（显示窗口）。")
        except SyntaxError or TypeError:
            print("未输入句柄")

    #移动窗口，默认不修改窗口大小
    def move_window(self,hwnd, x, y, width=None, height=None, repaint=True):
        """
        将窗口移动到指定位置，并可选地调整其大小
        :param hwnd: 窗口句柄
        :param x: 新位置的 X 坐标
        :param y: 新位置的 Y 坐标
        :param width: 新宽度（可选）
        :param height: 新高度（可选）
        :param repaint: 是否立即重绘窗口
        """
        # 获取当前窗口的大小
        if width is None or height is None:
            left, top, right, bottom = win32gui.GetWindowRect(hwnd)
            if width is None:
                width = right - left
            if height is None:
                height = bottom - top
        # 移动窗口到指定位置
        win32gui.MoveWindow(hwnd, x, y, width, height, repaint)




if __name__ == '__main__':
    i=WinControl()
    # i.GetCurrentHwnd()
    i.CycleCurrentWindow()
    # i.GetWinBaseInformation(16779096)


# for c in range(0,6):
#     i.WindowMize(16779096,c)

