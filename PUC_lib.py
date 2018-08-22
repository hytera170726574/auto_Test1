# -*-coding:utf-8 -*-
from  ctypes import *
import struct
from PIL import ImageGrab
import mysql.connector
import socket
from time import ctime
import sys
import time
import os
from PIL import ImageFilter
from PIL import ImageChops
import pytesseract
import xlrd
from PIL import  Image
import math
import operator
from functools import reduce

class base_Test():

    def __int__(self):
        pass

    def return_Color(self,im,x,y):
        #TODO(LDF):此段代码中的某些阈值条件还有待确认，准确时，请注意调整
        c=im.getpixel((x,y))
        #print c
        if (150 <= c[0] <= 170) & (200 <= c[1] <= 220) & (0 <= c[2] <= 40):
            tmp = 'green'
        elif (70 <=c[0] <= 90) & (75 <=c[1] <= 85) & (80 <= c[2] <= 95):
            tmp = 'grey'
        elif (20 <= c[0] <= 35) & (110 <= c[1] <= 125) & (200 <= c[2] <=215):
            tmp = 'blue'
        elif (200 <= c[0] <= 215) & (120 <= c[1] <= 135) & (20 <= c[2] <= 35):
            tmp = 'orange'
        elif (195 <= c[0] <= 205) & (15 <= c[1] <= 35) & (25 <= c[2] <= 45):
            tmp = 'red'
            #白色
        elif (245 <= c[0] <= 255) & (245 <= c[1] <=255) & (245 <= c[2] <= 255):
            tmp = "white"
        else:
            tmp = 'unknown'
        #print tmp
        return tmp

    def cut_Image(self,x,y,m,n):
        x1=int(x)
        y1=int(y)
        w=int(x1+m)
        l=int(y1+n)
        im=ImageGrab.grab(bbox=(x1, y1, w,l))
       # im.save("D:\media\compare.png")
        return im

    def return_Text(self,im,threshold=190):
        Lim = im.convert('L')
        table=[]
        #the for{} is used to binarizate the image
        for i in range(256):
            if i < threshold:
                table.append(0)
            else:
                table.append(1)
        bim = Lim.point(table, "1")
        bim.show()
        text = pytesseract.image_to_string(bim)
        return text

    def excel_Pos(self,a,b,func=''):
        data=xlrd.open_workbook(r"C:\Python27\Lib\site-packages\auto_Test\config.xlsx")
        a=int(a)
        if 0<a<=5:
            b=int(b)
            sheet_pannel=data.sheet_by_index(0)
            tmp = sheet_pannel.col_values(0).index(func)
            width=sheet_pannel.cell(0,3).value
            height=sheet_pannel.cell(1,3).value
            pos=str(sheet_pannel.cell(tmp,1).value).split("-")
            tmp1=int(int(pos[0])+width*(a-1))
            tmp2=int(int(pos[1])+height*(b-1))
            #tmp1=str(tmp1)
            #tmp2=str(tmp2)
            pos_list=[str(tmp1),str(tmp2)]
            print (pos_list)
            return pos_list
        elif a<=0:
            sheet_button = data.sheet_by_index(1)
            tmp=sheet_button.col_values(0).index(b)
            pos_list=str(sheet_button.cell(tmp,1).value).split("-")
            print (pos_list)
            return pos_list
        else:
            pos_list=["Wrong Parameter"]
            return pos_list
            print ("Wrong Parameter")

    def image_Rec(self,im1,im2):
        '''
        用于两图像的对比工作，若量图像完全相同则返回1，相差越大返回值越大

        :param im1: 截得图像
        :param im2: 待对比图像
        :return: 区别越小返回值越小
        '''
        h1 = im1.histogram()
        h2 = im2.histogram()
        result = math.sqrt(reduce(operator.add, list(map(lambda a, b: (a - b) ** 2, h1, h2))) / len(h1))
        return result

    '''def image_Rec(self,func,img_comp):
    #TODO(LDF)：颖姐请解释一下这段代码
        image_one = Image.open("D:\media\compare.png")
        image_two = Image.open(im2)
        diff = ImageChops.difference(image_one, image_two)
        if diff.getbbox() is None:
            return 1
        else:
            return 0'''

    #TODO(LDF):此段代码还没有写入总体设计需要注意
    def log_Read(self,log_Type,Plugin,time_start):
        '''

        :param log_Type: 日志类型
        :param Plugin: 待查询插件名称
        :param time_start: 日志开始时间点
        :return: 返回符合条件的日志条目
        '''
        if log_Type=="client":
            path=r"C:\Users\Administrator\AppData\Roaming\PUC\PUC_Client\Log\Client_Log"
        elif log_Type=="server":
            path=r"C:\ProgramData\PUC\PUC_Server\Log\Log"
        elif log_Type=="gataway":
            path=r"C:\ProgramData\PUC\PUC_Gateway\Log\Log"
        elif log_Type=="client_api":
            path=r"C:\Users\Administrator\AppData\Roaming\PUC\PUC_Client\Log\Client_API_Log"
        dirs=os.listdir(path)
        #com=Mytool.compare(1,2)

        def compare(x, y):
            stat_x = os.stat(path + "/" + x)
            stat_y = os.stat(path + "/" + y)
            if stat_x.st_ctime < stat_y.st_ctime:
                return -1
            elif stat_x.st_ctime > stat_y.st_ctime:
                return 1
            else:
                return 0
        dirs.sort(compare)
        log_Path=path+"/"+dirs[-1]
        plugin_Line=[]

        for line in open(log_Path):
            if Plugin in line:
                line = str(line)
                plugin_Line.append(line)
        print (plugin_Line)

        for i in range(len(plugin_Line)):
            tmpline=str(plugin_Line[i])[4:23]
            time_start=time.strptime(time_start, "%Y-%m-%d %H:%M:%S")
            print (time_start)
            timeArrary=time.strptime(tmpline,"%Y-%m-%d %H:%M:%S")
            if timeArrary>=time_start:
                fplugin_Log=plugin_Line[i:]
                return fplugin_Log
                break


class Mytool():

    def __int__(self):
        pass

    def Find_Item_on_Tree(self):
        '''

        :return: 返回资源树上第一个灰色位置
        '''
        bT=base_Test()
        tmpxy=bT.excel_Pos(0,"resource_tree_top")
        #print tmpxy
        tmpmn=bT.excel_Pos(0,"resource_tree_bottom")
        #print tmpmn
        tmpl=int(tmpmn[1])-int(tmpxy[1])
        tmpim=bT.cut_Image(tmpxy[0],tmpxy[1],270,tmpl)#180 should be change
        #tmpim.show()
        for i in range(1,tmpl):
            tmpc=bT.return_Color(tmpim,3,i)
            tmploc=260
            if tmpc=="grey":
                tmploc=tmploc+i
                print (tmploc)
                break

        return tmploc

    def cut_Panel_Number(self,x,y):
        bT=base_Test()
        tmp1xy=bT.excel_Pos(x,y,"cnumber")
        tmp2xy=bT.excel_Pos(x,y,"cnumber2")
        tmpim=bT.cut_Image(tmp1xy[0],tmp1xy[1],tmp2xy[0]-tmp1xy[0],tmp2xy[1]-tmp1xy[1])
        #tmpim.show()
        text=bT.return_Text(tmpim)
        print (text)
        return text

    def image_Comparsion_Panel(self,x,y,func):

        '''

        #用于呼叫面板状态对比
        :param x: 面板相对位置横坐标
        :param y: 面板相对位置纵坐标
        :param func: 所选择面板功能
        :return: 如果两个图像一致，返回1，不同则返回0
        '''

        bT=base_Test()
        tmp1xy=bT.excel_Pos(x,y,"lstate")
        tmp2xy=bT.excel_Pos(x,y,"lstate1")
        begin_x=int(tmp1xy[0])
        begin_y=int(tmp1xy[1])
        end_x=int(tmp2xy[0]) - int(tmp1xy[0])
        end_y=int(tmp2xy[1]) - int(tmp1xy[1])
        panelim = bT.cut_Image(begin_x, begin_y, end_x, end_y)
        print (func)
        #Image._show(panelim)
        #PUC界面中所截取的面板图形
        #impos='%s%s%s'%('C:\Python27\Lib\site-packages\auto_Test\',func,".png")
        standardpanel = Image.open("C:\Python27\Lib\site-packages\\auto_Test\\"+func + ".png")
        #Image._show(standardpanel)
        #截取好的标准面板图形
        #tmpim1="D:\Python27\Lib\site-packages\\auto_Test\Pecall.png"
        result=bT.image_Rec(panelim,standardpanel)
        #print result
        return result

    def return_Postion(self,x,y,func):
        func=str(func)
        pos=base_Test().excel_Pos(x,y,func)
        return pos

    def dgna_Pos(self,a,func):
        data = xlrd.open_workbook(r"c:\Python27\Lib\site-packages\auto_Test\config.xlsx")
        sheet_dgna = data.sheet_by_index(1)
        a=int(a)
        if a<=0:
            tmp = sheet_dgna.col_values(0).index(func)
            poslist = str(sheet_dgna.cell(tmp, 1).value).split("-")
            print (poslist)
            return poslist
        else:
            tmp = sheet_dgna.col_values(0).index(func)
            pos=str(sheet_dgna.cell(tmp, 1).value).split("-")
            tmp2 = int(int(pos[1]) + 31* (a - 1))
            poslist = [str(pos[0]), str(tmp2)]
            print (poslist)
            return poslist

    def return_Dgna_Input(self):

        '''

        :return: 返回新建动态重组输入框位置和动态组确认框位置，并且其横纵坐标按顺序放入了c_list中
        '''
        bT = base_Test()
        Top_left_concer = bT.excel_Pos(0, "dgna_input_left")
        Lower_right_corner = bT.excel_Pos(0, "dgna_input_right")
        a = int(Top_left_concer[0])
        b = int(Top_left_concer[1])
        c = int(Lower_right_corner[0])
        d = int(Lower_right_corner[1])
        print (a,b,c,d)
        im = bT.cut_Image(0, 0, 1920, 1080)
        #TODO(LDF):遍历图片步长改为5加快遍历速度
        for i in range(b, d,5):
            for x in range(a, c,5):
                #print x,i
                color = bT.return_Color(im, x, i)
                if color == "white":
                    c_list = [x, i]
                    c_list.append(x+97)
                    c_list.append(i+61)
                    print (c_list)
                    return c_list
                    break
                #else:
                 #   print "The element can not founded"

    def search_Pos(self, a, func):
        '''

        :param a:
        :param func:
        :return:
        '''
        data = xlrd.open_workbook(r"C:\Python27\Lib\site-packages\auto_Test\config.xlsx")
        sheet_pos = data.sheet_by_index(1)
        tmp = sheet_pos.col_values(0).index(func)
        poslist = str(sheet_pos.cell(tmp, 1).value).split("-")
        a = int(a)
        if a <= 1:
            print (poslist)
            return poslist
        else:
            if "dgna" in func:
                tmp2 = int(int(poslist[1]) + 30 * (a - 1))
            elif "cross" in func:
                tmp2 = int(int(poslist[1]) + 28 * (a - 1))
            pos = [str(poslist[0]), str(tmp2)]
            print (pos)
            return pos

    def Message_Find_MS(self):
        MS = base_Test()
        MSpic1 = MS.cut_Image(693, 373, 218, 276)
        #MSpic1.save("def.jpg")
        #MSpic1.show()
        def return_Green():
            for y_col in range(1, 275):
                for x_row in range(1, 217):
                    MScol = MS.return_Color(MSpic1, x_row, y_col)
                    #print str(x_row )+ "diyici" + str(y_col)
                    if MScol == "green":
                        print (str(x_row) + "jinru" + str(y_col))
                        return x_row,y_col
        def returnWhite(x_row,y_col):
            for y_col3 in range(y_col, y_col + 33):
                for x_row3 in range(x_row, x_row+150):
                    MSco2 = MS.return_Color(MSpic1, x_row3, y_col3)
                    if (MSco2 == 'white'):
                        print (x_row3, y_col3)
                        return x_row3 ,y_col3
        tmp1=return_Green()
        tmp2=returnWhite(tmp1[0],tmp1[1])
        rel_xrow=693+tmp2[0]
        rel_ycol=373+tmp2[1]
        print (rel_xrow,rel_ycol)
        return rel_xrow,rel_ycol

    #用于短信日志判断
    def test_SDS(self,content,sender,receiver,log_Type,Plugin,time_start):

        '''

        :param content: 短信内容
        :param sender: 发送者
        :param receiver: 接收者
        :param log_Type: 读取日志的类型
        :param Plugin: 插件名称
        :param time_start: 开始时间
        :return: 查询到返回true，未查询到返回false
        '''
        #content-短信内容，sender-发送者，receiver-接收者，log_Type-读取日志的类型，Plugin-插件名称，time_start-开始时间
        bT=base_Test()
        tmp_Lists=bT.log_Read(log_Type,Plugin,time_start)
        for lists in tmp_Lists:
            if ("content:"+content in lists) and ("sender:"+sender in lists) and ("receiver:"+receiver in lists):
                a="success"
                print ("true")
                return a
            else:
                a="false"
                print ("false")
                return a

    def panel_Color(self,x,y,descol,wait_time):
        '''

        :param x: 面板相对横坐标
        :param y: 面板相对纵坐标
        :param descol:目标颜色字符串
        :param wait_time:超时时间，整形，以秒为单位
        :return: 颜色字符串
        '''

        wait_time=int(wait_time)
        descol=str(descol)
        bT=base_Test()
        left_top=bT.excel_Pos(x,y,"cnumber")
        color="break"
        for i in range(1,10*wait_time):
            im = bT.cut_Image(left_top[0], left_top[1], 10, 10)
            #Image._show(im)
            color = bT.return_Color(im, 6, 6)
            print (color)
            if color==descol:
                break
            else:
                time.sleep(0.1)
        print (color)
        return str(color)


    def MS_Status(self,status):
        '''
        此函数用于当在资源树上找到某手台位置后判断其手台或组的状态

        :param status:需要判断的状态
        :return:
        '''
        if status=="RSS":
            descolor="blue"
        elif status=="group_select":
            descolor="green"
        elif status=="emergency_alarm":
            descolor="red"
        elif status=="GPS":
            descolor="red"

        left_top_concer=Mytool.Find_Item_on_Tree(self)
        im=base_Test().cut_Image(0,left_top_concer,270,35)
        #im.show()
        numcolor=0#目标颜色点数据
        for x in range(1,270):
            for y in range (1,35):
                color=base_Test().return_Color(im,x,y)
                if operator.eq(color,descolor):
                    numcolor=numcolor+1
        if (descolor=="blue")&(numcolor>10):
            status_real="online"
        elif (descolor=="blue")&(numcolor<10):
            status_real="offline"
        elif (descolor=="green")&(numcolor>10):
            status_real="group_selected"
        elif (descolor == "green") & (numcolor < 10):
            status_real = "group_select_failed"
        elif (descolor == "red") & (numcolor > 10):
            #TODO(ldf):10这个阈值还有待确认,别忘记加入一些注释
            status_real="emergency"
        elif (descolor == "red") & (0<numcolor < 10):
            status_real="GPS"
        else:
            status_real="wrong_status"
        print (status_real)
        return status_real



class platform_Test():

    def __int__(self):
        pass

    def call_mso(self, data, mso_ip):
        '''
        用于向中控模拟源发送消息

        :param data: eg.fe000001,make mso do the first test case
        :param mso_ip: mso's ip add
        :return: 返回向模拟源发送的已编码字符串
        '''
        data_int16 = str(hex(int(data[2:], 10)))[2:].zfill(8)
        #将除去fe的10进制字符串转为8位16进制
        #data_int10=int(data[2:],10)
        data_int=data_int16.decode("hex")
        #解析为16进制字符串
        hex_data_int16=map(ord,data_int)
        send_data = struct.pack("%dB" % (len(hex_data_int16)), *hex_data_int16)
        f_hex="\xfe"+send_data
        #加入fe标志位
        s_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s_udp.sendto(f_hex, (mso_ip, 38000))
        s_udp.close()
        return f_hex

    def rev_mso(self, host, port,revdata):
        '''
        用于接收mso模拟源发回的ack，host为模拟源ip地址，端口为对端发送端口号

        :param host: mso'ip add
        :param port: mso send port
        :param revdata: 应该接收的信息,输入call_mso发送的用例号即可
        :return:mso's return ack,如果成功，返回success，未接收到返回fail
        '''
        s_udprev = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s_udprev.bind((host, port))
        #revdata=int(revdata)

        try:
            s_udprev.settimeout(25)
            data = s_udprev.recvfrom(1024)[0]
            print (data)
            if data==revdata:
                print ("success")
                return "success"
            else:
                print ("fail")
                return "fail"

        except socket.timeout:
            print ("time_out")
            return "time_out"

    def sql_search(self, host, user, password, database, sql):
        '''
        此函数用于数据库查询，后期根据数据表形式，拼接sql语句

        :param host: database ip addr
        :param user: database user name
        :param password: database password
        :param database: 数据库表名（带确认）
        :param sql:
        :return: 数据库查询结果
        '''
        # TODO(LDF):此函数用于数据库查询，后期根据数据表形式，拼接sql语句
        config = {
            'host': host,
            'user': user,
            'password': password,
            'port': '3306',
            'database': database
        }
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        cursor.execute(sql)
        # cursor.execute('select * from SDSMsGpsInfo where LDSID = %s', ('5555002',))
        values = cursor.fetchall()
        return values

#platform_test().socket_client("i love you")

#platform_test().socket_client("i love you,too")
'''data="fe000001"
data_int16 = str(hex(int(data[2:], 10)))[2:].zfill(8)
#将除去fe的10进制字符串转为8位16进制
data_int10=int(data[2:],10)
data_int=data_int16.decode("hex")
#解析为16进制字符串
hex_data_int16=map(ord,data_int)
send_data = struct.pack("%dB" % (len(hex_data_int16)), *hex_data_int16)
f_hex="\xfe"+send_data
#print f_hex
time.sleep(2)
platform_Test().rev_mso("10.110.15.134",38000,f_hex)
#platform_Test().call_mso("fe000501","10.110.15.134")
#platform_test().socket_client("fe000000")'''
#time.sleep(2)
#Mytool().panel_Color(2,2,'unknown',"5")
#Mytool().return_Dgna_Input()
#a="fe00000001"
#b=int("fe",16)
#print(b)
#b=int(a,16)
#print b
#b=a.encode("hex")
#date=struct.pack("%dB"%(len(b)),*b)
#print(b)
#print(a)
#print(date)
#time.sleep(2)
#Mytool().MS_Status("RSS")
#base_Test().excel_Pos(2,2,"cnumber")

