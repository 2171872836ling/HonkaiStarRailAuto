import warnings
# 忽略GPU加速驱动不能用的警告
warnings.filterwarnings("ignore", category=UserWarning, module="easyocr")
import cv2
import easyocr
import win32gui
import win32ui
import win32con
import numpy as np
import logging
import re
import time
"""
===========================================================声明======================================================
BitBlt：内存（缓存）截图
EasyOCR：流行的OCR识别第三方库，内含识别大模型
两者结合加快识别速度
"""
class OCR:
    # 初始化 EasyOCR 读取器,未调用GPU会报错
    __reader = easyocr.Reader(
        lang_list=['ch_sim', 'en'],  # 语言列表
        gpu=False,  # 是否使用 GPU
        # model_storage_directory='models',  # 模型存储目录
        # download_enabled=True,  # 是否自动下载模型，比如ch_sim和en
        # detector=True,  # 是否启用文本检测
        # recognizer=True,  # 是否启用文本识别
        # verbose=True  # 是否显示详细信息
    )
    def __capture_window(self,hwnd, region:tuple=None):
        """
        使用 BitBlt 捕获指定窗口或区域的屏幕截图。

        参数:
        hwnd (int): 窗口句柄。
        region (tuple): 截图区域的左上角和右下角坐标 (left, top, right, bottom)。

        返回:
        numpy.ndarray: 捕获的图像数据，格式为 BGR。
        """
        try:
            # 获取当前屏幕窗口尺寸
            left, top, right, bottom = win32gui.GetWindowRect(hwnd)
            width = right - left
            height = bottom - top

            # 如果指定了区域，则调整捕获范围
            if region:
                left, top, right, bottom = region
                width = right - left
                height = bottom - top

            # 创建设备上下文
            hwndDC = win32gui.GetWindowDC(hwnd)
            mfcDC = win32ui.CreateDCFromHandle(hwndDC)
            saveDC = mfcDC.CreateCompatibleDC()

            # 创建位图对象
            saveBitMap = win32ui.CreateBitmap()
            saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)

            # 保存截图
            saveDC.SelectObject(saveBitMap)
            saveDC.BitBlt((0, 0), (width, height), mfcDC, (left, top), win32con.SRCCOPY)

            # 转换为 numpy 数组，图片二值化->调整颜色通道（BGRA → RGB）。
            bmpinfo = saveBitMap.GetInfo()
            bmpstr = saveBitMap.GetBitmapBits(True)
            timg = np.frombuffer(bmpstr, dtype='uint8')
            timg = timg.reshape((bmpinfo['bmHeight'], bmpinfo['bmWidth'], 4))

            # 释放资源
            win32gui.DeleteObject(saveBitMap.GetHandle())  # 释放位图
            saveDC.DeleteDC()  # 释放保存的设备上下文
            mfcDC.DeleteDC()  # 释放窗口
            win32gui.ReleaseDC(hwnd, hwndDC)#释放临时的设备上下文

            return cv2.cvtColor(timg, cv2.COLOR_BGRA2RGB)
        except Exception as e:
            logging.error(f"捕获窗口时发生错误: {e}")
            return None


    def ocr_char(self,region: tuple = None,threshold=0):
        """
        识别屏幕指定区域文字。
        参数:
        region (tuple): 截图区域的左上角和右下角坐标 (left, top, right, bottom)。
        prob:相似度=置信度默认0,因为文字识别都是0.3左右
        返回:
        list: 识别结果列表，每个元素是一个元组 (text, pos ,prob)，其中 text 是识别的文本，pos 是文本的位置，prob是置信度
        """
        try:
            # 获取桌面窗口句柄
            hwnd = win32gui.GetDesktopWindow()
            # 捕获指定区域图像
            img = self.__capture_window(hwnd, region)
            if img is None:
                logging.error("未能捕获图像")
                return []

            # 执行 OCR 识别
            results = self.__reader.readtext(img)
            return [(text, pos) for (pos, text, prob) in results if prob >= threshold]#遍历后反过来

        except Exception as e:
            logging.error(f"OCR 识别时发生错误: {e}")
            return []

    def ocr_find_match_char(self,region: tuple,match_char: str=None,threshold=0,func=None, *args, **kwargs):
        """
        10毫秒一次，检测100次，共1秒+调用其他函数
        match_char=r"\"d+"，匹配所有数字.实际上要去掉",否则这行注释会报错
        :param region:
        :param match_char:
        :param threshold:
        :param func:
        :param args:
        :param kwargs:
        :return:
        """
        global pos, text
        for i in range(1):
            all_results=self.ocr_char(region=region,threshold=threshold)
            #检测是否为空列表
            if not len(all_results):
                print(f"“{match_char}”匹配失败,没有检测到文字返回[False]")
                return [False]
            # 遍历all_results，获取返回值
            for text, pos in all_results:
                if match_char is None:
                #如果match_char没写，返回检测的内容
                    return [True, [region[0] + int(pos[0][0]), region[1] + int(pos[0][1])], text]
                # 匹配match_char成功
                elif re.search(match_char, text):
                    # 如果有调用的函数,则调用传入的函数
                    if func is not None:
                        func(*args, **kwargs)
                    #如果匹配的是数字，直接返回数字
                    if match_char == r"\d+":
                        return [True, [region[0] + int(pos[0][0]), region[1] + int(pos[0][1])], re.search(match_char, text).group()]
                    # 返回：真+检测到文本的坐标+文本匹配文本的坐标
                    return [True,[region[0] + int(pos[0][0]), region[1] + int(pos[0][1])], text]
                else:
                    print(f"匹配\"{match_char}\"失败{i+1}次")
                    # pass
            # 匹配match_char失败
        return [False, [region[0] + int(pos[0][0]), region[1] + int(pos[0][1])], text]


if __name__ == "__main__":
    def m(s, k):
        print(s, k)

    ocrcharrecong = OCR()
    # 识别屏幕特定区域(左,上,右,下)
    while True:
        time.sleep(1)
        print("开始检测")
        # print(ocrcharrecong.ocr_find_match_char((311, 345, 371,368  )))
        # print(ocrcharrecong.ocr_find_match_char((1203,697  , 1522,740  )))
        # print((ocrcharrecong.ocr_find_match_char((1203,697  , 1553,740))[2]).removesuffix("/120000"))

        # print(ocrcharrecong.ocr_find_match_char((1451,823    ,1594,846    ),"开启无名勋礼"))

        # print(ocrcharrecong.ocr_find_match_char((406, 810, 461, 839)))
        # print(ocrcharrecong.ocr_find_match_char((1590,346  ,1631,367  )))


        # print(ocrcharrecong.ocr_find_match_char((210,228,190,280     ),"开启无名勋礼"))
        # print(ocrcharrecong.ocr_find_match_char((231,228,263,283     )))等级
        # print(ocrcharrecong.ocr_find_match_char((102,41,181,62),"无名勋礼"))
        # print(ocrcharrecong.ocr_find_match_char((103,65,152,93),"奖励"))
        # print(ocrcharrecong.ocr_find_match_char((103,65,152,93),"任务"))
        # print(ocrcharrecong.ocr_find_match_char((1380,897,1478,923),"领取"))#奖励
        # print(ocrcharrecong.ocr_find_match_char((1633,903,1731,929  ),"领取"))#任务

        # print(ocrcharrecong.ocr_find_match_char((1808,195  ,1850,414),"登出",0.7))
        # print(ocrcharrecong.ocr_find_match_char((1808,195  ,1850,414),"登入",0.7))

        # print(ocrcharrecong.ocr_find_match_char((888,690,1031,715),"登录其他账号"))
        # print(ocrcharrecong.ocr_find_match_char((898,738,1020,759),"登录其他账号"))

        # print(ocrcharrecong.ocr_find_match_char((772,540+88*1,900,580+88*1)))
        # for i in range(5):
        #     print(ocrcharrecong.ocr_find_match_char((300,300+132*i,510,337+132*i)))

        # print(ocrcharrecong.ocr_char((300,300+132*i,510,337+132*i)))
        # for i in range(5):
        #     print(ocrcharrecong.ocr_find_match_char((300, 385 + 132 * i, 510, 423 + 132 * i), '金'))
        # print(ocrcharrecong.ocr_find_match_char((895,350  ,965,399  ))[2].removesuffix("/3"))
        # for i in range(4):
        #     print(ocrcharrecong.ocr_find_match_char((870,320+135*i,978,350+135*i)))
        # i =0
        # print(ocrcharrecong.ocr_find_match_char((870,320+135*i,978,350+135*i)))
        i = 0
        j = 1
        print(ocrcharrecong.ocr_find_match_char((290 + i * 473, 280 + j * 103, 490 + i * 473, 310 + j * 103)))





    # pass


