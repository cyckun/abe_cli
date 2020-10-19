#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import filedialog
import hashlib
import time
from python.cpabe_enc import cpabe_enc_cli
from python.cpabe_dec import cpabe_dec_cli

LOG_LINE_NUM = 0

class MY_GUI():
    def __init__(self,init_window_name):
        self.init_window_name = init_window_name
        self.filepath = ""
        self.policy_company = ""
        self.policy_dept = ""
        self.policy_level = ""


    #设置窗口
    def set_init_window(self):
        self.init_window_name.title("ABE客户端加密工具V0.1")          #窗口名
        #self.init_window_name.geometry('320x160+10+10')                         #290 160为窗口大小，+10 +10 定义窗口弹出时的默认展示位置
        self.init_window_name.geometry('568x281+10+10')
        #self.init_window_name["bg"] = "pink"                                    #窗口背景色，其他背景色见：blog.csdn.net/chl0000/article/details/7657887
        #self.init_window_name.attributes("-alpha",0.9)                          #虚化，值越小虚化程度越高
        #标签
        self.init_data_label = Label(self.init_window_name, text="待处理数据")
        self.init_data_label.grid(row=3, column=2)
        self.encpolicy_label = Label(self.init_window_name, text="设置加密策略")
        self.encpolicy_label.grid(row=15, column=2)
        self.encpolicy_Company_label = Label(self.init_window_name, text="Company")
        self.encpolicy_Company_label.grid(row=15, column=4)
        self.encpolicy_Dept_label = Label(self.init_window_name, text="Dept")
        self.encpolicy_Dept_label.grid(row=20, column=4)
        self.encpolicy_Level_label = Label(self.init_window_name, text="Level")
        self.encpolicy_Level_label.grid(row=25, column=4)
        self.encpolicy_sum_label = Label(self.init_window_name, text="策略描述")
        self.encpolicy_sum_label.grid(row=30, column=4)
        self.log_label = Label(self.init_window_name, text="日志")
        self.log_label.grid(row=70, column=2)

        #文本框
        self.init_data_Text = Text(self.init_window_name, width=50, height=2)  #原始数据录入框
        self.init_data_Text.grid(row=3, column=12)
        self.log_data_Text = Text(self.init_window_name, width=50, height=5)  # 日志框
        self.log_data_Text.grid(row=70, column=12)
        self.policy_Company_Text = Text(self.init_window_name, width=20, height=2)  # set enc policy, show position
        self.policy_Dept_Text = Text(self.init_window_name, width=20, height=2)  # set enc policy, show position
        self.policy_Level_Text = Text(self.init_window_name, width=20, height=2)  # set enc policy, show position
        self.policy_Descrip_Text = Text(self.init_window_name, width=20, height=2)
        self.policy_Company_Text.grid(row=15, column=8) # policy window size;
        self.policy_Dept_Text.grid(row=20, column=8)
        self.policy_Level_Text.grid(row=25, column=8)
        self.policy_Descrip_Text.grid(row=30, column=8)

        # browser files;
        self.str_abe_infile_button = Button(self.init_window_name, text="选择文件", bg="lightblue", width=10,
                                              command=self.abe_infile)  # 调用内部方法  加()为直接调用
        self.str_abe_infile_button.grid(row=2, column=12)
        # enc files;
        self.str_abe_enc_button = Button(self.init_window_name, text="加密", bg="lightblue", width=10,
                                            command=self.abe_enc)  # 调用内部方法  加()为直接调用
        self.str_abe_enc_button.grid(row=50, column=12)
        # dec files;
        self.str_abe_dec_button = Button(self.init_window_name, text="解密", bg="lightblue", width=10,
                                         command=self.abe_dec)  # 调用内部方法  加()为直接调用
        self.str_abe_dec_button.grid(row=60, column=12)


    def abe_infile(self):
       # Folderpath = filedialog.askdirectory() // test lator
        self.filepath = filedialog.askopenfilename()
       # print("path: ", filepath)
        self.init_data_Text.insert(END, str(self.filepath))

        return 0
    def abe_set_enc_policy(self):
        self.policy_company = self.policy_Company_Text.get(1.0, END).strip().replace("\n", "")
        self.policy_dept = self.policy_Dept_Text.get(1.0, END).strip().replace("\n", "")
        self.policy_level = self.policy_Level_Text.get(1.0, END).strip().replace("\n", "")
        if self.policy_company == "":
            self.policy_company = "ByteDance"
        if self.policy_dept == "":
            self.policy_dept = "Sec"
        if self.policy_level == "":
            self.policy_level = "1"
        self.enc_policy = self.policy_Descrip_Text.get(1.0, END).strip().replace("\n", "")

    def abe_enc(self):
        print("fiilpa:", self.filepath, type(self.filepath))
        if self.filepath == "":
            self.write_log_to_Text("未选择文件")
            return
        with open(self.filepath, "rb") as f:
            buffer = f.read()
            f.close()
        self.filepath = ""
        print("buffer:", buffer)

        policy = self.enc_policy
        print("policy:", policy)
        #policy = "(((Dept:SecurityResearch) and (level >= 4 )) and (Company:ByteDance))"
        ct = cpabe_enc_cli(buffer, policy)
        print("ct :", ct)
        with open("./cipher.txt", "wb") as f:
            f.write(ct)
            f.close()
        self.write_log_to_Text("enc sucess")

    def abe_dec(self):
        if self.filepath == "":
            self.write_log_to_Text("未选择文件")
            return
        with open(self.filepath, "rb") as f:
            buffer = f.read()
            f.close()
        self.filepath = ""
        plain = cpabe_dec_cli(buffer)
        if plain != 0:
            self.init_data_Text.insert(END, str(plain))
            self.write_log_to_Text("dec success.")
            with open("./dec_result.txt", "wb") as f:
                f.write(plain)
                f.close()
        else:
            self.write_log_to_Text("dec fail.")
        #print("ct :", plain)


    #获取当前时间
    def get_current_time(self):
        current_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        return current_time


    #日志动态打印
    def write_log_to_Text(self,logmsg):
        global LOG_LINE_NUM
        current_time = self.get_current_time()
        logmsg_in = str(current_time) +" " + str(logmsg) + "\n"      #换行
        if LOG_LINE_NUM <= 7:
            self.log_data_Text.insert(END, logmsg_in)
            LOG_LINE_NUM = LOG_LINE_NUM + 1
        else:
            self.log_data_Text.delete(1.0,2.0)
            self.log_data_Text.insert(END, logmsg_in)


def gui_start():
    init_window = Tk()              #实例化出一个父窗口
    ZMJ_PORTAL = MY_GUI(init_window)
    # 设置根窗口默认属性
    ZMJ_PORTAL.set_init_window()

    init_window.mainloop()          #父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示

if __name__ == '__main__':
    gui_start()
