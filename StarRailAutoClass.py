import win32gui
from time import sleep, localtime
from win32gui import FindWindow #窗口控制
from FrontEndAutomationClass import FrontEndAutomation #前台按键模拟
from EasyOCRClass import OCR #OCR文字识别技术

"""
|==========================================使用说明===================================================|
最最重要：
	1.缩放必须手动调为100%，记住原来的缩放大小。分辨率运行脚本自动调，运行结束自动恢复。（具体操作：单击
	右键，找到“显示设置”并点击 ；或者按win键后，搜索分辨率，找到“更改屏幕分辨率”并点击。打开后修改缩 
	放为100%就行了。
	
	2.游戏分辨率为最高就行了（2560x1440越大越好），游戏调自动战斗
	
	3.该游戏不可挂后台
	
	4.可以手动进入游戏后启动脚本；也可以给我”游戏绝对路径“,启动脚本就启动游戏。脚本结束后游戏自动关闭，
	并会弹窗提示你“每日任务完成情况” 
		
	5.最下面有免责声明，有你关心的脚本稳定性
不重要的：
	6.脚本里面其实有“刷差分宇宙”的代码了，只是不稳定没启用。
	
	7.按键小精灵自带广告，已经在启动时移除广告了，但不稳定。建议断网打开后再联网。
	
	8.脚本封装了常用鼠标点击函数，键盘点击函数，屏幕分辨率转换函数等。
	
	9.目前调用的主要程序有，刷副本，合成，材料探索，每日领取，指南传送。还有一堆封装好的子功能程序函数嵌
	套调用。为了程序运行效率，只启动了一条线程函数。 
	
	10.坐标由电脑分辨率和缩放比例构成，分辨率可以代码调，放缩目前没办法修改，故放缩很重要。调整为100%。
	
	11.	开脚本以分辨率1920x1020,放缩100为例。若不是请在设置修改(按win键，搜索“分辨率”),记得放缩比例(这
	个你得手动改回去)，当前电脑分辨率会在执行脚本的时候修改为标准参考的，执行完会改回原来的，但放缩比例
	一定要记得没执行脚本前的，如果记不住也没关系，在设置自己改喜欢的放缩比例就行了。“初始系统标准量是为 
	了坐标对齐，偏移量不会太大”。
	最后声明：
	脚本已有“三重防封“”两层防检测“代码，已测3个月未出现问题，但不保证不会被封，有问题后果自负（实在怕 
	冲个小月卡，99.9%不被封，虽然现在已经是99%）。脚本内含水印代码，防伪盗证书，不要倒卖，不要轻传，我做
	这个是为了全自动化星铁游戏抽满命老婆。技术宅拯救世界：

|----------------------------------------------------------------------------------------|
"""


#封装成类：Star_Rail_Game
class Star_Rail_Game:
    #===================================================================================================全局变量==================================================================================================#
    __account="13202051065"
    __password="Aa20041206"
    __Star_Rail_Game_Hwnd=None #星铁句柄
    __CurrentTime=None #当前系统的时间,年，月，日，星期
    __get_tiem=None #刷取参数
    __cooling_time=0#后摇冷却时间
    ocrfind=OCR()#ocr识
    frontauto=FrontEndAutomation()#前台按键
    __record_found_account=None
    __CurrentExplorationPoints=0#当前开扩力->体力
    __TemporalActiveProgress=0#当前活跃度,识别不到0
    __CurrentSupportReward=0# 当前的支援奖励
    __CurrentEchoesOFBattleTimes=0#当前的周本挑战次数
    __Double_Activity_coordinate_deviation=(0,0)#双倍活动坐标偏移，元组
    __Eroded_Tunnel={
        1:  "迷识之径",
        2:  "弦歌之径",
        3:  "勇骑之径",
        4:  "梦潜之径",
        5:  "幽冥之径",
        6:  "药使之径",
        7:  "野焰之径",
        8:  "圣颂之径",
        9:  "睿治之径",
        10: "漂泊之径",
        11: "迅拳之径",
        12: "霜风之径",
    }
    __Echoes_Of_Battle = {
        0: "心兽的战场",
        1: "尘梦的赞礼",
        2: "蛀星的旧魇",
        3: "不死的神实",
        4: "寒潮的落幕",
        5: "毁灭的开端"
    }
    __Error_Record={
        "Receive_Support_Reward":None,# 领取支援奖励
        "Receive_Commission_Materials":None,# 领取委托材料->材料探索
        "Receive_Nameless_Honor": None,  # 领取无名勋礼->领取大月卡
        "Receive_Daily_Training": None,  # 领取每日实训->领取每日奖励
        "Brush_Echoes_Of_Battle":None,# 历战余响->刷周本
        "Brush_Eroded_Tunnel":None,# 侵蚀隧洞->刷圣遗物
    }
    #===================================================================================================构造方法==================================================================================================#
    def __init__(self):
        #获取计算机本地时间
        current_time_struct  = localtime()# 获取当前时间的结构体
        # 提取年、月、日
        year = current_time_struct .tm_year
        month = current_time_struct .tm_mon
        day = current_time_struct .tm_mday
        # 获取当前星期几的数字表示统一+1（星期一=1，星期日=7）
        current_weekday_number  = current_time_struct.tm_wday+1
        #记录日期
        self.__CurrentTime=(year,month,day,current_weekday_number)
        print(f"当前日期：{self.__CurrentTime[0]}年{self.__CurrentTime[1]}月{self.__CurrentTime[2]}日,星期{self.__CurrentTime[3]}")
        #运行时创建对象自动为句柄赋值，检测是否打开游戏
        self.__Star_Rail_Game_Hwnd = win32gui.FindWindow("UnityWndClass", "崩坏：星穹铁道")
        if self.__Star_Rail_Game_Hwnd is None:
            print("未打开崩坏·星穹铁道")
        else:
            print(f"当前句柄为：{self.__Star_Rail_Game_Hwnd}")


    #===================================================================================================初始化游戏设置==================================================================================================#
    def Start_Game(self):
        # 检测是否进入游戏，等待更新下载时间, 最多10分钟->更新
        for q in range(600):
            sleep(1)
            # 更新检查句柄
            self.__Star_Rail_Game_Hwnd = win32gui.FindWindow("UnityWndClass", "崩坏：星穹铁道")
            # 置顶窗口，后台没什么必要
            # 有其他账号登录过，可以选择账号
            if self.ocrfind.ocr_find_match_char((910, 617, 1008, 642), "进入游戏")[0]:
                print("检测到已有账号登录，开始寻找账号:", self.__account)
                # ===============================检测当前账号======================================= #
                # 检测手机前三个号码和后两个号码,识别+切片
                if (self.ocrfind.ocr_find_match_char((789, 482, 897, 505), self.__account[0:3])[0]
                        and self.ocrfind.ocr_find_match_char((789, 482, 897, 505), self.__account[-2:])[0]):
                    self.frontauto.mouse_once_click(955, 625)
                    self.__record_found_account = True
                    print("当前账号与目标账号一致:", self.__account, "点击进入游戏")
                # ===============================检测登录过的账号======================================= #
                elif self.__record_found_account is None:
                    # 点击账号->打开更多账号
                    self.frontauto.mouse_once_click(1200, 495)
                    # 遍历所有账号,假设1页,2个账号
                    for j in range(1):
                        for i in range(2):
                            # 检测手机前三个号码和后两个号码
                            if (self.ocrfind.ocr_find_match_char((772, 540 + 88 * i, 900, 580 + 88 * i),
                                                                 self.__account[0:3])[0]
                                    and self.ocrfind.ocr_find_match_char((772, 540 + 88 * i, 900, 580 + 88 * i),
                                                                         self.__account[-2:])[0]):
                                self.frontauto.mouse_once_click(840, 584 + 88 * i)
                                self.__record_found_account = True
                                print("成功寻找账号,选择账号:", self.__account)
                                return self.Start_Game()
                            else:
                                print(f"第{j + 1},第{i + 1}行,账号匹配失败")
                        # 要初始化鼠标位置,这里不演示
                        # self.frontauto.mouse_once_click(955,625)
                        self.frontauto.mouse_wheel(1)  # 滚轮一页
                    # 点击账号->关闭更多账号
                    self.frontauto.mouse_once_click(1200, 495)
                    self.__record_found_account = False
                elif not self.__record_found_account:
                    print("寻找账号失败，换登录方式，点击：登录其他账号")
                    if self.ocrfind.ocr_find_match_char((888, 690, 1031, 715), "登录其他账号")[0]:
                        # 当前账号,点击：登录其他账号
                        self.frontauto.mouse_once_click(954, 701)
                    # 更多账号->点击：登录其他账号
                    elif self.ocrfind.ocr_find_match_char((888, 690, 1031, 715), "登录其他账号")[0]:
                        self.frontauto.mouse_once_click(952, 751)
            # ========================================检测是否密码/验证码登录界面（没有其他账号登录情况）============================================= #
            elif self.ocrfind.ocr_find_match_char((905,674, 1013,700), "进入游戏")[0]:
                print("检测到账号登入界面，开始登录账号")
                # ===============================密码登录界面======================================= #
                if self.ocrfind.ocr_find_match_char((693, 482, 809, 534), "输入密码")[0]:
                    # 先清空界面输入
                    print("清空界面输入")
                    self.frontauto.mouse_once_click(1026, 415)  # 清空账号输入
                    self.frontauto.key_down_times(8)  # 删除
                    self.frontauto.mouse_once_click(1040, 502)  # 清空密码/验证码输入
                    self.frontauto.key_down_times(8)  # 删除
                    # 输入账号
                    print("输入账号:", self.__account)
                    self.frontauto.mouse_once_click(1026, 415)
                    self.frontauto.MessageCV(self.__account)
                    # 输入密码
                    print("输入密码:", self.__password)
                    self.frontauto.mouse_once_click(1040, 502)
                    self.frontauto.MessageCV(self.__password)
                    # 回车检查同意,点击同意
                    self.frontauto.key_down_times(13)
                elif self.ocrfind.ocr_find_match_char((1062, 575, 1122, 606), "同意", 0, self.frontauto.mouse_once_click,1087, 591)[0]:
                    print("点击同意")
                # ===============================验证码登录界面======================================= #
                # elif self.ocrfind.ocr_find_match_char((693, 482, 809, 534), "验证码")[0]:
                # “账号密码”，验证码登录返回密码登录界面
                elif self.ocrfind.ocr_find_match_char((853,751, 946,783 ), "账号密码")[0]:
                    self.frontauto.mouse_once_click(874, 764)
            #===========================================================检测账号登入界面===============================================================#
            elif self.ocrfind.ocr_find_match_char((860, 814, 1066, 861), "开始游戏",0,self.frontauto.mouse_once_click, 960,540)[0]:
                print("开始游戏")
            elif self.ocrfind.ocr_find_match_char((906,999  , 1014,1025  ), "点击进入",0,self.frontauto.mouse_once_click, 960,540)[0]:
                print("点击进入")
            # ===========================================================检测月卡界面===============================================================#
            elif self.ocrfind.ocr_find_match_char((881,55, 1035,98), "列车补给")[0]:
                #提示月卡时间
                self.frontauto.mouse_once_click(961, 950)
                print("领取月卡，小月卡还剩下：",self.ocrfind.ocr_find_match_char((875, 114, 1039, 146), r"\d+")[2],"天")
                #点击领取月卡,点两次
                self.frontauto.mouse_many_click(961,950,delay=1500)
            # ==================================================检测刚刚更新->前往跃迁===============================================================#
            elif self.ocrfind.ocr_find_match_char((896,932  ,993,957  ),"前往跃迁")[0]:
                print("检测刚刚更新，前往跃迁，点击取消")
                self.frontauto.mouse_once_click(1862,65)
            # ==================================================检测刚刚更新->观看前景提要===============================================================#
            elif self.ocrfind.ocr_find_match_char((701, 749, 796, 777), "稍后再看")[0]:
                print("检测刚刚更新，观看前景提要，点击稍后观看")
                self.frontauto.mouse_once_click(728,757)
            # ===========================================================检测游戏主界面===============================================================#
            elif self.Initialization_Game_Inferface(False,1,0):
                print("检测到游戏主界面，已进入游戏,准备执行任务")
                return
            # ===========================================================检测游戏主界面===============================================================#
            else:
                print("等待加载...")
        #没有跳出，直到检测循环结束->没检测到->没进入游戏
        print("没有进入游戏界面，启动错误方案")




# ===================================================================================================执行任务================================================================================================== #
# ==============================================================物品合成=========================================================== #
    def Conflate_Item(self,select_projection="奇巧零食"):
        # 物品合成
        print("开始执行任务：物品合成")
        # 记录错误值，把None变成False是为了记录已经启动过Conflate_Item(),这个函数了
        self.__Error_Record["Conflate_Item"] = False
        while True:
            # 打开手机，按Esc
            if self.Initialization_Game_Inferface(initialization_time=1):
                print("检测到初始界面,打开手机", )
                self.frontauto.key_down_times(27)
            # 进入合成界面
            elif (self.ocrfind.ocr_find_match_char((1580, 524, 1620, 548), "合成")[0]
                  and self.ocrfind.ocr_find_match_char((1710, 396, 1750, 417), "委托")[0]):
                print(f"打开手机界面成功，点击“合成”")
                self.frontauto.mouse_once_click(1599,492)
            #点击消耗品合成，开始寻找物品
            elif (not self.__Error_Record["Conflate_Item"] and self.ocrfind.ocr_find_match_char((101,64,230,95), "消耗品合成")[0]
                    and not self.ocrfind.ocr_find_match_char((1023,162,1397,204),select_projection)[0]):
            #========================================筛选算法，初始坐标(158,196),相隔坐标(75,89)=================================== #
                print("开始寻找物品:",select_projection)
                judge=False#终止循环
                #3页，5行,3列
                for i in range(6):  # 六页
                    if judge:break # 跳出滚轮循环
                    self.frontauto.mouse_wheel(26 if i>0 else 0)  # 翻页
                    for j in range(5):  # 五行
                        if judge: break  # 跳出行循环
                        for k in range(3):  # 三列
                            if judge: break  # 跳出列循环
                            # 点击物品，(初始坐标x+相隔x*k,初始坐标y+相隔y*j)
                            self.frontauto.mouse_once_click(158 + k * 132, 196 + j * 156)
                            #检测筛选物品,检测到了就跳出循环
                            result=self.ocrfind.ocr_find_match_char((1023,162,1397,204),select_projection)
                            if result[0]:
                                print("物品寻找成功:", select_projection)
                                judge=True#跳出行循环
                            #检测到字体为空，跳出翻页
                            elif len(result)<3:
                                print("未检测到物品！")
                                judge=True  # 跳出行循环
                            else:print("物品:",result[2])
            #========================================匹配成功，开始合成=================================== #
            # 检测该物品并点击合成
            elif (not self.__Error_Record["Conflate_Item"] and self.ocrfind.ocr_find_match_char((1023, 968,1210,998), "合成")[0]
                and self.ocrfind.ocr_find_match_char((1023,162,1397,204),select_projection)[0]):
                self.frontauto.mouse_once_click(1152, 983)
            # 点击确认合成
            elif not self.__Error_Record["Conflate_Item"] and self.ocrfind.ocr_find_match_char((1161,686,1213,712 ), "确认")[0]:
                self.frontauto.mouse_once_click(1165, 690)
            # 点击空白关闭
            elif not self.__Error_Record["Conflate_Item"] and self.ocrfind.ocr_find_match_char((909,170,1010,200), "获得物品")[0]:
                self.frontauto.mouse_once_click(956,771)
                self.__Error_Record["Conflate_Item"] = True
            #先判断Error_Record值，再执行self.Initialization_Game_Inferface，无论如何都会初始化界面
            # =========================Error_Record为假+初始化界失败=开始初始化失败->启动异常错误方案=============================== #
            elif not self.__Error_Record["Conflate_Item"] and not self.Initialization_Game_Inferface(True,dayle=self.__cooling_time):
                print("开始初始化失败，记录错误值，启动错误解决方案")
                self.__Error_Record["Conflate_Item"] = False
                self.Error_Solution()
            # =========================Error_Record为真+初始化界成功==结束初始化成功->退出循环，报告任务进度========================== #
            elif self.__Error_Record["Conflate_Item"] and self.Initialization_Game_Inferface(True,dayle=self.__cooling_time):
                print("结束初始化成功")
                break
            # =========================Error_Record为真+初始化界失败==结束初始化失败->退出循环，报告任务进度========================== #
            elif self.__Error_Record["Conflate_Item"] and not self.Initialization_Game_Inferface(True,dayle=self.__cooling_time):
                print("结束初始化失败，记录错误值，启动错误解决方案")
                self.__Error_Record["Conflate_Item"] = False
                self.Error_Solution()
        # ================================报告进度和初始化异常报错========================== #
        print("任务完成：领取委托材料")
        self.frontauto.random_delay(self.__cooling_time,0)#每次执行的后摇时间
        return #返回主线程



# =============================================================领取支援奖励==================================================================== #
    def Receive_Support_Reward(self):
        # 领取支援奖励
        print("开始执行任务：领取支援奖励")
        # 记录错误值，把None变成False是为了记录已经启d动过Receive_Commission_Materials(),这个函数了
        self.__Error_Record["Receive_Support_Reward"] = False
        while True:
            # 打开手机，按Esc
            if not self.__Error_Record["Receive_Support_Reward"] and self.Initialization_Game_Inferface(initialization_time=1):
                print("检测到初始界面,打开手机")
                self.frontauto.key_down_times(27)
                self.frontauto.random_delay(1000, 0)  # 每次执行的后摇时间
            # 点击更多，打开漫游签证
            elif (not self.__Error_Record["Receive_Support_Reward"]
                  and not self.ocrfind.ocr_find_match_char((1537, 127, 1633, 151), "漫游签证")[0]
                  and self.ocrfind.ocr_find_match_char((1580, 524, 1620, 548), "合成")[0]
                  and self.ocrfind.ocr_find_match_char((1710, 396, 1750, 417), "委托")[0]):
                print(f"打开手机界面成功，点击···")
                self.frontauto.mouse_once_click(1759,100)
            # 打开漫游签证
            elif (not self.__Error_Record["Receive_Support_Reward"]
                  and self.ocrfind.ocr_find_match_char((1537,127, 1633,151), "漫游签证")[0]):
                print(f"点击漫游签证")
                self.frontauto.mouse_once_click(1584,139)
            # 打开支援角色
            elif (not self.__Error_Record["Receive_Support_Reward"]
                  and self.ocrfind.ocr_find_match_char((1010,231, 1130,262), "支援角色")[0]):
                print(f"点击支援角色")
                self.frontauto.mouse_once_click(976,246)
            # 检测当前支援奖励并且领取
            elif (not self.__Error_Record["Receive_Support_Reward"]
                  and self.ocrfind.ocr_find_match_char((1312,617,1444,650),"支援奖励")[0]):
                result = self.ocrfind.ocr_find_match_char((1203, 697, 1553, 740))
                if result[0]:
                    # 检测当前支援奖励，检测+去空格+去杂字+转整型
                    self.__CurrentSupportReward+= int(result[2].removesuffix("/120000").strip())
                    print("当前支援奖励为:", self.__CurrentSupportReward)
                else:
                    # 未识别/空字符，防止->去空格+转整型报错
                    print("检测当前支援奖励失败")
                # 点击领取
                self.__Error_Record["Receive_Support_Reward"] = True
                self.frontauto.mouse_once_click(1384, 819)
                print("点击领取")
            # 先判断Error_Record值，无论值为什么，都会执行self.Initialization_Game_Inferface初始化界面，有not阻挡
            # =========================Error_Record为假+初始化界失败=开始初始化失败->启动异常错误方案=============================== #
            elif not self.__Error_Record["Receive_Support_Reward"]  and not self.Initialization_Game_Inferface(True,dayle=self.__cooling_time):
                print("开始初始化失败，记录错误值，启动错误解决方案")
                self.__Error_Record["Receive_Support_Reward"] = False
                self.Error_Solution()
            # =========================Error_Record为真+初始化界成功==结束初始化成功->退出循环，报告任务进度========================== #
            elif self.__Error_Record["Receive_Support_Reward"] and self.Initialization_Game_Inferface(True, dayle=self.__cooling_time):
                print("结束初始化成功")
                break
            # =========================Error_Record为真+初始化界失败==结束初始化失败->退出循环，报告任务进度========================== #
            elif self.__Error_Record["Receive_Support_Reward"] and not self.Initialization_Game_Inferface(True,dayle=self.__cooling_time):
                print("结束初始化失败，记录错误值，启动错误解决方案")
                self.__Error_Record["Receive_Support_Reward"] = False
                self.Error_Solution()
        # ================================报告进度和初始化异常报错========================== #
        print("任务完成：领取支援奖励")
        self.frontauto.random_delay(self.__cooling_time, 0)  # 每次执行的后摇时间
        return  # 返回主线程

# =============================================================领取委托材料->材料探索==================================================================== #
    def Receive_Commission_Materials(self):
        # 领取委托材料->材料探索
        print("开始执行任务：领取委托材料")
        # 记录错误值，把None变成False是为了记录已经启动过Receive_Commission_Materials(),这个函数了
        self.__Error_Record["Receive_Commission_Materials"] = False
        while True:
            # 打开手机，按Esc
            if self.Initialization_Game_Inferface(initialization_time=1):
                print("检测到初始界面,打开手机", )
                self.frontauto.key_down_times(27)
            # 点击委托
            elif (self.ocrfind.ocr_find_match_char((1580, 524, 1620, 548), "合成")[0]
                    and self.ocrfind.ocr_find_match_char((1710, 396, 1750, 417), "委托")[0]):
                print(f"打开手机界面成功，点击委托")
                self.frontauto.mouse_once_click(1731, 366)
            # ============================================检测委托时间并领取================================================ #
            # 没有委托领取，跳出循环，报告进度，直接返回
            elif (self.ocrfind.ocr_find_match_char((1404,892,1483,924),"派遣中")[0] and
                  self.Initialization_Game_Inferface(True,dayle=self.__cooling_time)):
                print("委托派遣中...，结束任务：领取委托材料")
                self.__Error_Record["Receive_Commission_Materials"] = False
                return
            # 有领取，点击一键领取
            elif (not self.__Error_Record["Receive_Commission_Materials"]
                  and self.ocrfind.ocr_find_match_char((440,895,540,923),"键领取")[0]):
                print("点击：一键领取")
                self.frontauto.mouse_once_click(480,905)
            # 点击再次派遣
            elif (not self.__Error_Record["Receive_Commission_Materials"]
                  and self.ocrfind.ocr_find_match_char((1175,939,1274,965),"再次派遣")[0]):
                print("点击：再次派遣")
                self.frontauto.mouse_once_click(1210,946)
                #记录错误值，把None变成True是为了记录已经启动过Receive_Commission_Materials(),这个函数了
                self.__Error_Record["Receive_Commission_Materials"]=True
            #先判断Error_Record值，无论值为什么，都会执行self.Initialization_Game_Inferface初始化界面，有not阻挡
            # =========================Error_Record为假+初始化界失败=开始初始化失败->启动异常错误方案=============================== #
            elif not self.__Error_Record["Receive_Commission_Materials"] and not self.Initialization_Game_Inferface(True,dayle=self.__cooling_time):
                print("开始初始化失败，记录错误值，启动错误解决方案")
                self.__Error_Record["Receive_Commission_Materials"]=False
                self.Error_Solution()
            # =========================Error_Record为真+初始化界成功==结束初始化成功->退出循环，报告任务进度========================== #
            elif self.__Error_Record["Receive_Commission_Materials"] and self.Initialization_Game_Inferface(True,dayle=self.__cooling_time):
                print("结束初始化成功")
                break
            # =========================Error_Record为真+初始化界失败==结束初始化失败->退出循环，报告任务进度========================== #
            elif self.__Error_Record[
                "Receive_Commission_Materials"]  and not self.Initialization_Game_Inferface(True,dayle=self.__cooling_time):
                print("结束初始化失败，记录错误值，启动错误解决方案")
                self.__Error_Record["Receive_Commission_Materials"]=False
                self.Error_Solution()
        # ================================报告进度和初始化异常报错========================== #
        print("任务完成：领取委托材料")
        self.frontauto.random_delay(self.__cooling_time,0)#每次执行的后摇时间
        return #返回主线程



# =========================================================================历战余响->刷周本================================================================================ #
    def Brush_Echoes_Of_Battle(self,select=0):
        # 历战余响->刷周本
        """
            历战余响—副本序号
            0:"心兽的战场",
            1:"尘梦的赞礼",
            2:"蛀星的旧魇",
            3:"不死的神实",
            4:"寒潮的落幕",
            5:"毁灭的开端",
            6:
            7:
        :param select: 选项
        :return: 无，有线程守护
        """
        #开始执行
        print("开始执行任务：历战余响->刷周本")
        #检测当前日期是否为星期：1 or 7
        if self.__CurrentTime[3]==1 or self.__CurrentTime[3]==6:
            print("当前星期：",self.__CurrentTime[3],"在任务时间范围内,执行任务")
            self.__Error_Record["Brush_Echoes_Of_Battle"] = False
            judge_continue = None  # 使用一轮未开始的标志，三态：1.None->未开始，2.False->未结束，3.True->已结束
        else:
            print("当前星期：", self.__CurrentTime[3], "不是星期一或星期日，结束任务")
            self.__Error_Record["Brush_Echoes_Of_Battle"] = True
            return
        while True:
        #====================================================寻找历战余响=================================================
        #打开历战余响，检测次数，记录数值
            if not self.__Error_Record["Brush_Echoes_Of_Battle"] and self.Select_Interastral_Peace_Guide(2) and self.Select_Survival_Index(6) and self.Select_Echoes_Of_Battle(select):
                print("检测是否为挑战界面")
            #===============================================检测挑战，点击挑战==================================================
            elif not self.__Error_Record["Brush_Echoes_Of_Battle"] and self.ocrfind.ocr_find_match_char((1558,963,1624,998),"挑战")[0]:
                print("开始挑战：",self.__Echoes_Of_Battle[select])
                self.frontauto.mouse_once_click(1590, 979)
            #检测队伍，点击开始挑战
            elif not self.__Error_Record["Brush_Echoes_Of_Battle"] and self.ocrfind.ocr_find_match_char((101,39,145,61),"队伍")[0]:
                self.frontauto.mouse_once_click(1672,981)
                judge_continue = False # 一轮未结束
            #检测是否耗尽周本次数继续挑战
            elif not self.__Error_Record["Brush_Echoes_Of_Battle"] and self.ocrfind.ocr_find_match_char((862,510,985,540),"已耗尽")[0]:
                self.__Error_Record["Brush_Echoes_Of_Battle"] = True
                print("当前周本次数已耗尽，退出执行：历战余响->刷周本")
            #检测挑战界面
            elif not self.__Error_Record["Brush_Echoes_Of_Battle"] and self.ocrfind.ocr_find_match_char((1764,7,1817,21),"ms")[0]:
                print("正在挑战...")
            # =============================================检测挑战成功，等待挑战结束======================================================
            elif not self.__Error_Record["Brush_Echoes_Of_Battle"] and not judge_continue and self.ocrfind.ocr_find_match_char((835,322,1080,382),"挑战成功")[0]:
                # ===================================检测体力===========================================
                result = self.ocrfind.ocr_find_match_char((1635,52,1735,76))
                if result[0]:
                    # 去空格+去杂字+转整型
                    self.__CurrentExplorationPoints = int(result[2].removesuffix("/300").strip())
                    print("当前体力为:", self.__CurrentExplorationPoints)
                else:
                    # 未识别/空字符，防止->去空格+转整型报错
                    print("检测当前体力失败")
                # ==============================重新检测本周领取次数=====================================
                result = self.ocrfind.ocr_find_match_char((1050,885,1362,912),r"\d+")
                if result[0]:
                    # 检测本周领取次数，检测+去空格+去杂字+转整型
                    self.__CurrentEchoesOFBattleTimes = int(result[2].removesuffix("/3").strip())
                    print("当前周本挑战次数为:", self.__CurrentEchoesOFBattleTimes)
                else:
                    # 未识别/空字符，防止->去空格+转整型报错
                    print("检测当前周本挑战次数失败")
                judge_continue=True
            # ================================================刷取一轮结束=======================================================
            # 如果当前次数=0次/如果当前体力小于30，退出任务。
            elif not self.__Error_Record["Brush_Echoes_Of_Battle"] and judge_continue and (self.__CurrentEchoesOFBattleTimes==0 or self.__CurrentExplorationPoints<30):
                self.__Error_Record["Brush_Echoes_Of_Battle"]=True
                print("当前周本次数已耗尽" if self.__CurrentEchoesOFBattleTimes==0 else "当前体力小于30","，退出执行：历战余响->刷周本")
                self.frontauto.mouse_once_click(723,940)#点击退出
            # 如果当前体力大于30（一次周本），次数大于0,点击再来一次,刷新检测周本次数
            elif not self.__Error_Record["Brush_Echoes_Of_Battle"] and judge_continue and self.__CurrentEchoesOFBattleTimes>0 and self.__CurrentExplorationPoints>=30:
                judge_continue=None#重置一轮刷取
                self.frontauto.mouse_once_click(1239,939)#点击再来一次
                print("点击再来一次")
            # #先判断Error_Record值，无论值为什么，都会执行self.Initialization_Game_Inferface初始化界面，有not阻挡
            # =========================Error_Record为假+初始化界失败=开始初始化失败->启动异常错误方案=============================== #
            elif not self.__Error_Record["Brush_Echoes_Of_Battle"] and judge_continue is None and not self.Initialization_Game_Inferface(True,dayle=self.__cooling_time):
                print("开始初始化失败，记录错误值，启动错误解决方案")
                self.Error_Solution()
            # =========================Error_Record为真+初始化界成功==结束初始化成功->退出循环，报告任务进度========================== #
            elif self.__Error_Record["Brush_Echoes_Of_Battle"] and self.Initialization_Game_Inferface(True,dayle=self.__cooling_time):
                print("结束初始化成功")
                break
            # =========================Error_Record为真+初始化界失败==结束初始化失败->退出循环，报告任务进度========================== #
            elif self.__Error_Record["Brush_Echoes_Of_Battle"] and self.Initialization_Game_Inferface(True,dayle=self.__cooling_time):
                print("结束初始化失败，记录错误值，启动错误解决方案")
                self.Error_Solution()
        # ================================报告进度和初始化异常报错========================== #
        print("任务完成：历战余响->刷周本")
        self.frontauto.random_delay(self.__cooling_time,0)#每次执行的后摇时间
        return #返回主线程





    # =====================================================侵蚀隧洞->刷圣遗物==================================================================
    def Brush_Eroded_Tunnel(self,select=0,brush_times=3):
        """
        1:  "迷识之径",
        2:  "弦歌之径",
        3:  "勇骑之径",
        4:  "梦潜之径",
        5:  "幽冥之径",
        6:  "药使之径",
        7:  "野焰之径",
        8:  "圣颂之径",
        9:  "睿治之径",
        10: "漂泊之径",
        11: "迅拳之径",
        12: "霜风之径",
        :param select: 选项
        :return: 无，有线程守护
        """
        #侵蚀隧洞->刷圣遗物
        #开始执行
        print("开始执行任务：侵蚀隧洞->刷圣遗物")
        #初始化变量
        judge_continue=None#使用一轮未开始的标志，三态：1.None->未开始，2.False->未结束，3.True->已结束
        self.__Error_Record["Brush_Eroded_Tunnel"] = False
        while True:
            # ====================================================寻找侵蚀隧洞=================================================
            # 打开侵蚀隧洞，检测次数，记录数值
            if not self.__Error_Record["Brush_Eroded_Tunnel"] and self.Select_Interastral_Peace_Guide(2) and self.Select_Survival_Index(4) and self.Select_Eroded_Tunnel(select):
                print("检测是否为挑战界面")
            # # ===============================================检测挑战，点击挑战==================================================
            # elif not self.__Error_Record["Brush_Eroded_Tunnel"] and self.ocrfind.ocr_find_match_char((1558, 963, 1624, 998), "挑战")[0]:
            #     print("开始挑战：", self.__Echoes_Of_Battle[select])
            #     self.frontauto.mouse_once_click(1590, 979)
            # # 检测队伍，点击开始挑战
            # elif not self.__Error_Record["Brush_Eroded_Tunnel"] and self.ocrfind.ocr_find_match_char((101, 39, 145, 61), "队伍")[0]:
            #     self.frontauto.mouse_once_click(1672, 981)
            #     judge_continue = False # 一轮未结束
            # # 检测体力是否可以继续挑战
            # elif not self.__Error_Record["Brush_Echoes_Of_Battle"] and self.ocrfind.ocr_find_match_char((862,510,985,540),"已耗尽")[0]:
            #     self.__Error_Record["Brush_Echoes_Of_Battle"] = True
            #     print("当前体力不足，退出执行：侵蚀隧洞->刷圣遗物")
            # # 检测挑战界面
            # elif not self.__Error_Record["Brush_Eroded_Tunnel"] and self.ocrfind.ocr_find_match_char((1764, 7, 1817, 21), "ms")[0]:
            #     # judge_continue = False # 一轮未结束
            #     print("正在挑战...")
            # # =============================================检测挑战成功，等待挑战结束======================================================
            # elif not self.__Error_Record["Brush_Eroded_Tunnel"] and not judge_continue and self.ocrfind.ocr_find_match_char((835, 322, 1080, 382), "挑战成功")[0]:
            #     # ========================================检测体力===========================================
            #     result = self.ocrfind.ocr_find_match_char((1635, 52, 1735, 76))
            #     if result[0]:
            #         # 去空格+去杂字+转整型
            #         self.__CurrentExplorationPoints = int(result[2].removesuffix("/300").strip())
            #         print("当前体力为:", self.__CurrentExplorationPoints)
            #     else:
            #         # 未识别/空字符，防止->去空格+转整型报错
            #         print("检测当前体力失败")
            #     # ==============================重新检测本周领取次数=====================================
            #     result = self.ocrfind.ocr_find_match_char((1050, 885, 1362, 912), r"\d+")
            #     if result[0]:
            #         # 检测本周领取次数，检测+去空格+去杂字+转整型
            #         self.__CurrentEchoesOFBattleTimes = int(result[2].removesuffix("/3").strip())
            #         print("当前周本挑战次数为:", self.__CurrentEchoesOFBattleTimes)
            #     else:
            #         # 未识别/空字符，防止->去空格+转整型报错
            #         print("检测当前周本挑战次数失败")
            #     judge_continue = True
            # # ================================================刷取一轮结束=======================================================
            # # 如果当前次数=0次/如果当前体力小于30，退出任务。
            # elif not self.__Error_Record["Brush_Eroded_Tunnel"] and judge_continue and self.__CurrentEchoesOFBattleTimes == 0 or self.__CurrentExplorationPoints < 30:
            #     self.frontauto.mouse_once_click(723, 940)  # 点击退出
            #     self.__Error_Record["Brush_Eroded_Tunnel"] = True
            #     print("当前周本次数已耗尽" if self.__CurrentEchoesOFBattleTimes == 0 else "当前体力小于30","，退出执行：历战余响->刷周本")
            # # 如果当前体力大于30（一次周本），次数大于0,点击再来一次,刷新检测周本次数
            # elif not self.__Error_Record["Brush_Eroded_Tunnel"] and judge_continue and self.__CurrentExplorationPoints >= 30 and self.__CurrentEchoesOFBattleTimes > 0:
            #     judge_continue = None  # 重置一轮刷取
            #     self.frontauto.mouse_once_click(1239, 939)  # 点击再来一次
            #     print("点击再来一次")
            # # #先判断Error_Record值，无论值为什么，都会执行self.Initialization_Game_Inferface初始化界面，有not阻挡
            # # =========================Error_Record为假+初始化界失败=开始初始化失败->启动异常错误方案=============================== #
            # elif not self.__Error_Record["Brush_Eroded_Tunnel"] and judge_continue is None and not self.Initialization_Game_Inferface(True,dayle=self.__cooling_time):
            #     print("开始初始化失败，记录错误值，启动错误解决方案")
            #     self.Error_Solution()
            # # =========================Error_Record为真+初始化界成功==结束初始化成功->退出循环，报告任务进度========================== #
            # elif self.__Error_Record["Brush_Eroded_Tunnel"] and self.Initialization_Game_Inferface(True,dayle=self.__cooling_time):
            #     print("结束初始化成功")
            #     break
            # # =========================Error_Record为真+初始化界失败==结束初始化失败->退出循环，报告任务进度========================== #
            # elif self.__Error_Record["Brush_Eroded_Tunnel"] and self.Initialization_Game_Inferface(True,dayle=self.__cooling_time):
            #     print("结束初始化失败，记录错误值，启动错误解决方案")
            #     self.Error_Solution()
        # ================================报告进度和初始化异常报错========================== #
        print("任务完成：侵蚀隧洞->刷圣遗物")
        self.frontauto.random_delay(self.__cooling_time, 0)  # 每次执行的后摇时间
        return  # 返回主线程


# =============================================================领取每日实训->领取每日奖励==================================================================== #
    def Receive_Daily_Training(self):
        #领取每日实训->领取每日奖励,一个任务活跃度是100以上，最多领取五次
        #开始执行
        print("开始执行任务：领取每日实训->领取每日奖励")
        ACTIVEPROGRESS = 500  # 活跃度500
        # 记录错误值，把None变成False是为了记录已经启动过Conflate_Item(),这个函数了
        self.__Error_Record["Receive_Daily_Training"] = False
        while True:
            # ============================================领取每日实训正常流程========================================= #
            #如是每日实训界面，先检测活跃度，必须执行一次
            if self.ocrfind.ocr_find_match_char((103,66,200,92),"每日实训")[0]:
                print("检测当前活跃度中......")
                # self.frontauto.random_delay((1000 if 1000>self.__cooling_time else self.__cooling_time),0)
                #记录识别结果
                result=self.ocrfind.ocr_find_match_char((314, 341, 367, 369))
                if result[0]:
                    # 检测当前活跃度，检测+去空格+转整型
                    self.__TemporalActiveProgress = int(result[2].strip())
                    print("当前活跃度为:", self.__TemporalActiveProgress)
                else:
                    # 未识别/空字符，防止->去空格+转整型报错
                    print("检测当前活跃度失败")
            # 打开每日实训
            if not self.__Error_Record["Receive_Daily_Training"] and self.Select_Interastral_Peace_Guide(1):
                print("开始领取活跃度")
            # 领取活跃度：检测到"领取"就点击
            elif not self.__Error_Record["Receive_Daily_Training"] and self.ocrfind.ocr_find_match_char((406, 810, 461, 839), "领取")[0]:
                self.frontauto.mouse_once_click(422, 821)  # 点击领取
            # =================================================检测领取每日奖励===============================================#
            elif not self.__Error_Record["Receive_Daily_Training"] and self.__TemporalActiveProgress == ACTIVEPROGRESS:
                print("活跃度已满，领取全部每日奖励")
                self.frontauto.mouse_once_click(642, 307)  # 点击领取
                self.__Error_Record["Receive_Daily_Training"] = True
            elif not self.__Error_Record["Receive_Daily_Training"] and self.__TemporalActiveProgress < ACTIVEPROGRESS:
                self.frontauto.mouse_once_click(642, 307)  # 点击领取
                self.__Error_Record["Receive_Daily_Training"] = False
                print(f"领取前“{int((self.__TemporalActiveProgress/100))}”个每日奖励")
                print(f"活跃度“未”满，当前活跃度为：{self.__TemporalActiveProgress}")
                return
            #先判断Error_Record值，无论值为什么，都会执行self.Initialization_Game_Interface初始化界面，有not阻挡
            # =========================Error_Record为假+初始化界失败=开始初始化失败->启动异常错误方案=============================== #
            elif not self.__Error_Record["Receive_Daily_Training"] and not self.Initialization_Game_Inferface(True,dayle=self.__cooling_time):
                print("开始初始化失败，记录错误值，启动错误解决方案")
                self.Error_Solution()
            # =========================Error_Record为真+初始化界成功==结束初始化成功->退出循环，报告任务进度========================== #
            elif self.__Error_Record["Receive_Daily_Training"] and self.Initialization_Game_Inferface(True,dayle=self.__cooling_time):
                print("结束初始化成功")
                break
            # =========================Error_Record为真+初始化界失败==结束初始化失败->退出循环，报告任务进度========================== #
            elif self.__Error_Record["Receive_Daily_Training"] and not self.Initialization_Game_Inferface(True,dayle=self.__cooling_time):
                print("结束初始化失败，记录错误值，启动错误解决方案")
                self.Error_Solution()
        # ================================报告进度和初始化异常报错========================== #
        print("任务完成：领取每日实训")
        self.frontauto.random_delay(self.__cooling_time,0)#每次执行的后摇时间
        return #返回主线程

# ============================================================领取无名勋礼->领取大月卡==================================================================== #
    def Receive_Nameless_Honor(self):
        # 领取无名勋礼->领取大月卡
        #开始执行
        print("开始执行任务：领取无名勋礼->领取大月卡")
        # 记录错误值，把None变成False是为了记录已经启动过Conflate_Item(),这个函数了
        self.__Error_Record["Receive_Nameless_Honor"] = False
        If_Expert_receive=False#检测是否领取月卡经验值
        while True:
            # ============================================领取领取无名勋礼正常流程========================================= #
            # 无名勋礼，按F
            if not self.__Error_Record["Receive_Nameless_Honor"] and self.Initialization_Game_Inferface(initialization_time=1):
                print("检测到初始界面,打开无名勋礼")
                self.frontauto.key_down_times(113,delay=(1000 if 1000 > self.__cooling_time else self.__cooling_time))#按F2
            # 检测到无名勋礼界面，打开奖励区域，检测点击一键领取。没领取+成功打开无名勋礼界面+成功打开奖励界面+没一键领取
            if (not self.__Error_Record["Receive_Nameless_Honor"]
                and
                not If_Expert_receive  # 检测是否领取过月卡经验值
                and
                # 打开任务界面
                self.ocrfind.ocr_find_match_char((102, 41, 181, 62), "无名勋礼", 0,
                                                 self.frontauto.mouse_once_click, 956, 60, 2,(1000 if 1000 > self.__cooling_time else self.__cooling_time))[0]
                and
                # 检测任务界面
                self.ocrfind.ocr_find_match_char((103, 65, 152, 93), "任务")[0]
                and
                # 任务点击一键领取
                self.ocrfind.ocr_find_match_char((1633, 903, 1731, 929), "领取", 0,
                                                 self.frontauto.mouse_once_click,1670, 915, 2,(1000 if 1000 > self.__cooling_time else self.__cooling_time))[0]):
                # 这时候可以检测等级+经验上限
                print(self.ocrfind.ocr_find_match_char((231,228,263,283)))
                If_Expert_receive=True
                print("任务经验值已领取")
            elif (not self.__Error_Record["Receive_Nameless_Honor"]
                and
                # 打开奖励界面
                self.ocrfind.ocr_find_match_char((102, 41, 181, 62), "无名勋礼", 0,
                                                 self.frontauto.mouse_once_click,861,59, 2,(1000 if 1000 > self.__cooling_time else self.__cooling_time))[0]
                and
                  # 检测奖励界面
                self.ocrfind.ocr_find_match_char((103,65,152,93),"奖励")
                  # 奖励点击一键领取
                and
                not self.ocrfind.ocr_find_match_char((1380, 897, 1478, 923), "领取",0, self.frontauto.mouse_once_click, 1432, 910, 2,(1000 if 1000 > self.__cooling_time else self.__cooling_time))[0]):
                self.__Error_Record["Receive_Nameless_Honor"]=True
                print("奖励已领取")

            #先判断Error_Record值，无论值为什么，都会执行self.Initialization_Game_Inferface初始化界面，有not阻挡
            # =========================Error_Record为假+初始化界失败=开始初始化失败->启动异常错误方案=============================== #
            elif not self.__Error_Record["Receive_Nameless_Honor"] and not self.Initialization_Game_Inferface(True,dayle=self.__cooling_time):
                print("开始初始化失败，记录错误值，启动错误解决方案")
                self.Error_Solution()
            # =========================Error_Record为真+初始化界成功==结束初始化成功->退出循环，报告任务进度========================== #
            elif self.__Error_Record["Receive_Nameless_Honor"] and self.Initialization_Game_Inferface(True,dayle=self.__cooling_time):
                print("结束初始化成功")
                break
            # =========================Error_Record为真+初始化界失败==结束初始化失败->退出循环，报告任务进度========================== #
            elif self.__Error_Record["Receive_Nameless_Honor"] and not self.Initialization_Game_Inferface(True,dayle=self.__cooling_time):
                print("结束初始化失败，记录错误值，启动错误解决方案")
                self.Error_Solution()
        # ================================报告进度和初始化异常报错========================== #
        print("任务完成：领取无名勋礼->领取大月卡")
        self.frontauto.random_delay(self.__cooling_time,0)#每次执行的后摇时间
        return #返回主线程

    # ===================================================================================================游戏内必要功能================================================================================================== #




    def Initialization_Game_Inferface(self,KeyDownEsc=False, initialization_time=30,dayle=800,func=None, *args, **kwargs) -> bool:
        """
        1.初始化界面，检测到游戏界面返回真
        2.检测时间默认30秒,30次，一秒一次
        :return:布尔值
        """
        for i in range(initialization_time):  # 检测次数
            #识别初始化界面
            if (self.ocrfind.ocr_find_match_char((84,966, 149,987),"Enter")[0]
                    and self.ocrfind.ocr_find_match_char((1807,86,1883,105),"ms")[0]):
                print("初始化游戏主界面完成")
                return True
            #没检测到调用其他函数
            else:
                # 按Esc
                if KeyDownEsc:
                    self.frontauto.key_down_times(27)
                    # self.frontauto.random_delay(1000, 0)  # 后摇时间
                    # print("按Esc")
                #调用回调函数
                if func is not None:
                    func(*args, **kwargs)
            self.frontauto.random_delay((800 if 800 > dayle else dayle),0)
        # 循环结束后检测不到返回假
        print("初始化游戏主界面失败")
        return False

    def Select_Interastral_Peace_Guide(self, select:int):
        """
        打开星际和平指南：
        1.每日实训
        2.生存索引
        3.模拟宇宙
        4.逐光捡金
        初始坐标为(360,210)，相隔(120,0), 统一从0开始遍历(360+120*select,210)
        :param select:打开的
        :return:
        """
        #为了代码统一，从0开始，检测范围
        if select > 5 or select < 1:
            print(f"select={select}，Open_Interastral_Peace_Guide->select超范围错误！")
        select -= 1
        #写个字典不用遍历
        Interastral_Peace_Guide={
            0:"每日实训",
            1:"生存索引",
            2:"模拟宇宙",
            3:"逐光捡金",
            4:"行动摘要",
            5:"战术训练"
        }
        # 先检测一遍是否为界面,再按F4
        if self.Initialization_Game_Inferface(initialization_time=1):
            print(f"检测到初始化界面，打开界面:{Interastral_Peace_Guide[select]}")
        else:
            print(f"未检测到初始化界面,打开{Interastral_Peace_Guide[select]}失败")
            return False
        #开始执行,按F4
        self.frontauto.key_down_times(115,delay=(1200 if 1200>self.__cooling_time else self.__cooling_time))
        # ==================================检测星际和平指南界面==================================#
        if self.ocrfind.ocr_find_match_char((104,40,219,63), "星际和平指南")[0]:
            print("打开星际和平指南界面成功")
            #点击所有的界面,字典遍历出来是0，1，2，3...5
            for i in Interastral_Peace_Guide:
                self.frontauto.mouse_once_click(360+120*i, 210,delay=(200 if 200>self.__cooling_time else self.__cooling_time))
                #寻找界面
                if self.ocrfind.ocr_find_match_char((104,67,200,92))[2]==Interastral_Peace_Guide[select]:
                    print(f"打开:{Interastral_Peace_Guide[select]}成功")
                    return True
            #如果点击所有界面都找不到，直接返回界面报错
            print(f"打开:{Interastral_Peace_Guide[select]}失败")
            return False

    def Open_Phone(self):
        """
        1.初始化界面，检测到游戏界面
        3.按Esc，打开手机界面，检测界面
        2.检测次数默认20次
        :return:布尔值
        """

        # ==================================检测手机界面==================================#
        # 开始执行
        self.frontauto.key_down_times(27,delay=1000,cooldown=0)
        if (self.ocrfind.ocr_find_match_char((1580,524, 1620,548),"合成")[0]
            and self.ocrfind.ocr_find_match_char((1710,396 , 1750,417),"委托")[0]):
            print(f"打开:手机界面成功")
            return True
        else:
            print(f"打开:手机界面失败")
            return False

    def Select_Survival_Index(self,select):
        """
        打开星际和平指南：
        0.饰品提取
        1.拟造花萼(金)
        2.拟造花萼(赤)
        3.凝滞虚影
        4.侵蚀隧洞
        5.历战回响
        初始坐标为(472,344)，相隔(0,132), 统一从0开始遍历(472,344+i*132)
        :param select:打开的
        :return:
        """
        #为了代码统一，从0开始，检测范围
        if select > 6 or select < 0:
            print(f"select={select}，OPen_Survival_Index->select超范围错误！")
        select -= 1
        #写个字典不用遍历
        Survival_Index={
            0:"饰品提取",# Accessory Extraction
            1:"金",# Golden Simulated Sepal
            2:"赤",# Crimson Simulated Sepa
            3:"凝滞虚影",# Stagnant Phantom
            4:"侵蚀隧洞",# Eroded Tunnel
            5:"历战余响",# Echoes of Battle
        }
        # ==================================生存索引界面==================================#
        #点击所有的界面,字典遍历出来是0，1，2，3...5
        #初始化后，一共有6个
        for i in range(6):
            if i==5:
                #初始化鼠标位置
                self.frontauto.mouse_once_click(448,584)
                #滚轮到底
                self.frontauto.mouse_wheel(10,delay=(1000 if 1000 > self.__cooling_time else self.__cooling_time))
                if self.ocrfind.ocr_find_match_char((300, 781, 510, 819), Survival_Index[select])[0]:
                    self.frontauto.mouse_once_click(472, 820,delay=(200 if 200 > self.__cooling_time else self.__cooling_time))
                    print(f"打开:{Survival_Index[select]}成功")
                    return True
            # #识别从"赤"开始,后期添加维护可能需要
            #     for j in range(4):
            #         if self.ocrfind.ocr_find_match_char((300, 385 + 132 * j, 510, 423 + 132 * j), Survival_Index[select])[0]:
            #             self.frontauto.mouse_once_click(472, 517 + 132 * j,delay=(200 if 200 > self.__cooling_time else self.__cooling_time))
            # 如果是“凝滞虚影”之前的，规律写,寻找字体识别+点击+提示
            elif i<5 and self.ocrfind.ocr_find_match_char((300,300+132*i,510,337+132*i), Survival_Index[select])[0]:
                self.frontauto.mouse_once_click(472, 344 + 132 * i,delay=(200 if 200 > self.__cooling_time else self.__cooling_time))
                print(f"打开:{Survival_Index[select]}成功")
                return True
        #for循环都没有找到的，直接返回
        print(f"未找识到，打开:{Survival_Index[select]}失败")
        return False

    # ---------------------------------------寻找侵蚀隧洞(圣遗物)副本-------------------------------------------- #
    def Select_Eroded_Tunnel(self, select):
        # 检测select
        if select > len(self.__Eroded_Tunnel) or select < 0:
            print("Select_Eroded_Tunnel异常，select超出范围")
            return False
        # 检测体力
        result = self.ocrfind.ocr_find_match_char((1635, 52, 1735, 76))
        if result[0]:
            # 去空格+去杂字+转整型
            self.__CurrentExplorationPoints = int(result[2].removesuffix("/300").strip())
            print("当前体力为:", self.__CurrentExplorationPoints)
        else:
            # 未识别/空字符，防止->去空格+转整型报错
            print("检测当前体力失败")
        # 初始化鼠标+滚轮位置
        self.frontauto.mouse_once_click(700,340)
        self.frontauto.mouse_wheel(32,up=True,delay=1000 if 1000 > self.__cooling_time else self.__cooling_time)#初始化滚轮
        # 两页，三个
        for i in range(2):
            for j in range(4):
                # 识别三行
                if self.ocrfind.ocr_find_match_char((870,320+135*i,978,350+135*i),self.__Eroded_Tunnel[select])[0]:
                    print("成功寻找：",self.__Echoes_Of_Battle[select])
                    # 点击进入
                    self.frontauto.mouse_once_click(1566,405+190*j,delay=(200 if 200 > self.__cooling_time else self.__cooling_time))
                    return True
            # #一轮翻页
            self.frontauto.mouse_once_click(782, 359)
            self.frontauto.mouse_wheel(18)
        #没找到
        print("没找到:",self.__Echoes_Of_Battle[select])
        return False

    # ---------------------------------------寻找历战余响(周本)副本-------------------------------------------- #
    def Select_Echoes_Of_Battle(self,select):
        #检测select
        if select > len(self.__Echoes_Of_Battle) or select < 0:
            print("Select_Echoes_Of_Battle，select超出范围")
            return False
        #检测本周领取次数
        result = self.ocrfind.ocr_find_match_char((890,355,970,395))
        if result[0]:
            # 检测本周领取次数，检测+去空格+去杂字+转整型
            self.__CurrentEchoesOFBattleTimes=int(result[2].removesuffix("/3").strip())
            print("当前周本挑战次数为:", self.__CurrentEchoesOFBattleTimes)
        else:
            # 未识别/空字符，防止->去空格+转整型报错
            print("检测当前周本挑战次数失败")
        # 检测体力
        result = self.ocrfind.ocr_find_match_char((1635, 52, 1735, 76))
        if result[0]:
            # 去空格+去杂字+转整型
            self.__CurrentExplorationPoints = int(result[2].removesuffix("/300").strip())
            print("当前体力为:", self.__CurrentExplorationPoints)
        else:
            # 未识别/空字符，防止->去空格+转整型报错
            print("检测当前体力失败")
        # 初始化鼠标+滚轮位置
        self.frontauto.mouse_once_click(782,359)
        self.frontauto.mouse_wheel(32,up=True,delay=1000 if 1000 > self.__cooling_time else self.__cooling_time)#初始化滚轮
        self.frontauto.mouse_wheel(5)
        #3页，4个
        for i in range(2):
            for j in range(4):
                #识别4行
                if self.ocrfind.ocr_find_match_char((890,305+190*j,1030,410+190*j),self.__Echoes_Of_Battle[select])[0]:
                    print("成功寻找：",self.__Echoes_Of_Battle[select])
                    # 点击进入
                    self.frontauto.mouse_once_click(1566,405+190*j,delay=(200 if 200 > self.__cooling_time else self.__cooling_time))
                    return True
            # 一轮翻页
            self.frontauto.mouse_once_click(782, 359)
            self.frontauto.mouse_wheel(18)
        #没找到
        print("没找到:",self.__Echoes_Of_Battle[select])
        return False

    # ===================================================================================================任务报错处理================================================================================================== #
    def Error_Solution(self):
        # 重新启动星铁
        # 根据Record的字典值，回溯运行的方案
        print("启动错误解决方案")



if __name__ == '__main__':
    #获取凑口句柄
    hwnd = FindWindow("UnityWndClass", "崩坏：星穹铁道")
    # 游戏绝对路径，后期改成其他的全局的搜索
    GamePath = r"G:\星铁\Star Rail Game\StarRail.exe"

    # #创建游戏对象
    game=Star_Rail_Game()
    # game.Initialization_Game_Inferface(True)#初始化游戏界面

    #任务

    # game.Initialization_Game_Inferface()#初始化游戏界面
    # game.Receive_Daily_Training()#每日领取
    # for i in range(1,7):#遍历星际指南
    #     game.Open_Interastral_Peace_Guide(i)
    #     game.Initialization_Game_Inferface(True)  # 初始化游戏界面

    # game.Open_Phone()#打开手机
    # game.Initialization_Game_Inferface()#初始化游戏界面


    game.Start_Game()#进入运行游戏
    game.Conflate_Item()#物品合成
    game.Receive_Commission_Materials()# 领取委托材料->材料探索
    game.Receive_Support_Reward()#支援点
    game.Brush_Echoes_Of_Battle()#刷周本
    game.Brush_Eroded_Tunnel()#数圣遗物
    game.Receive_Daily_Training()#每人奖励
    game.Receive_Nameless_Honor()#大月卡


    game.Brush_Echoes_Of_Battle()#刷周本



    # game.Initialization_Game_Inferface(True)
    # game.Initialization_Game_Inferface(True)#初始化游戏界面
    # game.Brush_Eroded_Tunnel()
    # game.Select_Survival_Index(6)
    # for i in range(6):
    #     game.Select_Echoes_Of_Battle(i)
    # game.Brush_Echoes_Of_Battle(0)
    # game.Select_Eroded_Tunnel(0)
    # game.Brush_Eroded_Tunnel()#数圣遗物




    input()
    # #线程守护游戏进程
    # game.run_game()
    # #检测电脑配置，获取参数

    #
    #
    # #打开星际和平指南
























































