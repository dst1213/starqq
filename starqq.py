#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 爬取星座网站 http://astro.fashion.qq.com/的子网站
# 例子：http://data.astro.qq.com/dayastro/20/20221/index.shtml
# 其中第一个20与第二个20需要一致，不然报错，代表日期区间，后面三位数字代表星座和日期

from bs4 import BeautifulSoup
import requests
import re
import os
import time
import sys

#展现2位数字的函数
def num2(x):
	x=int(x)
	if x<10:
		x='0'+str(x)
	x=str(x)
	return x

#展现3位数字的函数
def num3(x):
	x=int(x)
	if x<10:
		x='00'+str(x)
	elif (x>=10 and x<=99):
		x='0'+str(x)
	x=str(x)
	return x

#/变成-,防止非法路径
def leg(x):
	x=x.replace('/','-')
	return x

#去除区间
def my_sec(x):
	x=x[0:3]
	return x

#搞个2位数2次循环
x=93  #93以后位今年内容
while x<=99:
	y=0
	while y<=999:
		#先把需要的信息爬下来
		url=str('http://data.astro.qq.com/dayastro/'+num2(x)+'/'+num2(x)+num3(y)+'/index.shtml')
		r=requests.get(url,timeout=1000)

		#超时的处理
		if (r.status_code != 200 and r.status_code != 404):
			for i in range(10):
				print ("第",i,"次重试")
				time.sleep(3)
				url=str('http://data.astro.qq.com/dayastro/'+num2(x)+'/'+num2(x)+num3(y)+'/index.shtml')
				if r.status_code == 200:
					continue
		r.encoding=r.apparent_encoding
		html=r.content
		soup = BeautifulSoup(html,"lxml")
		
		#判断url是否没有内容，没有的话跳过
		iserror=soup.head.title.string
		if iserror=='404 Not Found':
			print ("结束",x,y) 
			y=y+1
			sys.exit(0)
		
		#输出区间
		section=soup.find(attrs={'class':'xiangxi'})
		section=section.div.div.span.string
		section=my_sec(section)
		
		#输出日期
		today=soup.find(attrs={'id':'Tomorrow2'})
		today=today.span.string

		#输出主文案
		maintext=soup.find(attrs={'id':'maintext'})
		maintext=maintext.string

		
		#输出综合、爱情、工作、财运运势，返回一个list
		luck=soup.find_all(attrs={'class':'timu'})
		#综合运势
		total=luck[0] 
		total_title=total.span.string
		total_star=total.find_all(attrs={'src':'http://mat1.gtimg.com/astro/2014zlk/jrys/xing1.jpg'})
		total_star=len(total_star)

		#爱情运势
		love=luck[1] 
		love_title=love.span.string
		love_star=love.find_all(attrs={'src':'http://mat1.gtimg.com/astro/2014zlk/jrys/xing1.jpg'})
		love_star=len(love_star)

		#工作运势
		work=luck[2] 
		work_title=work.span.string
		work_star=work.find_all(attrs={'src':'http://mat1.gtimg.com/astro/2014zlk/jrys/xing1.jpg'})
		work_star=len(work_star)

		#财运运势
		money=luck[3] 
		money_title=money.span.string
		money_star=money.find_all(attrs={'src':'http://mat1.gtimg.com/astro/2014zlk/jrys/xing1.jpg'})
		money_star=len(money_star)

		
		#输出贵人星座、幸运颜色、幸运数字、健康运势
		rest=soup.find_all(attrs={'class':'span2'})
		great=rest[0]#贵人星座
		great=great.string

		color=rest[1]#幸运颜色
		color=color.string

		number=rest[2]#幸运数字
		number=number.string

		health=rest[3]#健康运势
		health=health.string

		
		
		#创建类别文件夹
		isExists=os.path.exists(leg(today))
		if not isExists:
			os.makedirs(leg(today))

		#写到一个文件里
		f=open(leg(today)+'/'+leg(section)+'.txt','w')
		f.write(today)
		f.write('\n')
		f.write(section)
		f.write('\n')
		f.write(maintext)
		f.write('\n')
		f.write(total_title)
		f.write(' ')
		f.write(str(total_star))
		f.write('\n')
		f.write(love_title)
		f.write(' ')
		f.write(str(love_star))
		f.write('\n')
		f.write(work_title)
		f.write(' ')
		f.write(str(work_star))
		f.write('\n')
		f.write(great)
		f.write('\n')
		f.write(color)
		f.write('\n')
		f.write(health)
		f.write('\n')
		f.close()
		print("成功写入",x,y)
		y=y+1

	x=x+1