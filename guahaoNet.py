#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Michael Shen'

import requests
import pickle
import AnalysisHtml
import re,json
import time
import random
import hashlib
import http.cookiejar   #python 3
# import cookielib   python 2
import os
# from PIL import Image
# from pytesseract import pytesser

class Guahao(object):
    def __init__(self,membername,mobile,password):

        self.base_url       =   'http://www.114-91.com/'
        self.home_url       =   'http://www.114-91.com/index.jsp'
        self.login_url      =   'http://www.114-91.com/shmc_reg_login_do.jsp'
        self.validImage_url =   'http://www.114-91.com/checkcode?type=num'
        self.orderlist_url  =   'http://www.guahao.com/my/orderlist'
        self.search_url     =   'http://www.114-91.com/shmc_doctor_list_ajax.jsp?ipage=&issearch=1'
        self.person_url     =   'http://www.114-91.com/shmc_reg_info.jsp'
        self.mobile 	    = 	mobile
        self.isLogin        =   False;
        self.membername     = 	membername
        self.password 	    = 	password;#self.strToMd5(password)
        self.session        =   requests.Session()
        self.cookies_name   =   os.path.join(os.path.abspath('.'), 'cookies/' + self.mobile + '.txt');
        self.loginHeaders   =   {
            'Host': 'www.114-91.com',
            'Origin': 'www.114-91.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Referer': 'http://www.114-91.com/shmc_login_personal.jsp',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        self.validHeaders = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
			'Accept-Encoding':'gzip, deflate, sdch',
			'Accept-Language':'zh-CN,zh;q=0.8',
			'Connection':'keep-alive',
			'Host':'www.114-91.com',
			'Upgrade-Insecure-Requests':'1',
			'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'
        }
        self.homeHeaders={
            'Host': 'www.114-91.com',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:45.0) Gecko/20100101 Firefox/45.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'
        }

        self.searchHeaders  =   {
            'Accept':'*/*',
            'Accept-Encoding':'gzip,deflate',
            'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4,id;q=0.2',
            'Connection':'keep-alive',
            'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
            'Host':'www.114-91.com',
            'Origin':'www.114-91.com',
            'Referer':'www.114-91.com/shmc_doctor_list.jsp',
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
            'X-Requested-With':'XMLHttpRequest'
        }

        self.personHeaders  =   {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate, sdch',
            'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4,id;q=0.2',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive',
            'Host':'114-91.com',
            'Referer':'http://114-91.com/shmc_order_create.jsp?docid=4702&ctid=jKPc9XK%2FpxE%3D&reserdate=2017-03-01&docurl=C8BBiMAyj0MbCoYctsUdVkn2wZCShMbncTzk9XKXFNg%3D',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        }

        self.proxies_list=[]
        self.prox=dict()
        #初始化代理服务器列表
        with open('pro.txt','r') as f:
            for line in f.readlines():
                self.proxies_list.append(line.strip())

        try:
            load_cookiejar          =   http.cookiejar.LWPCookieJar();
            load_cookiejar.load(self.cookies_name, ignore_discard=True, ignore_expires = True);
            load_cookies            =   requests.utils.dict_from_cookiejar(load_cookiejar);
            self.session.cookies    =   requests.utils.cookiejar_from_dict(load_cookies);
            # print("has login\n");
            self.isLogin = True;
        except:
            #如果文件不存在
            self.getCookie()
            # return False;
            # self.getVaildImage()
            # self.login()


    def getIsLogin(self):
        return self.isLogin;


    #首次访问主页,用来获得cookie
    def getCookie(self):
        response = self.session.get(self.home_url,headers = self.homeHeaders)
        # AnalysisHtml.obtain_login_result(response.text);


    # 模拟登陆
    def login(self, _user, _phone, _pass, _code):
        validCode           =   _code   #input('input validCode:')
        self.membername     =   _user
        self.mobile         =   _phone
        self.password       =   _pass
        post_para = {
            'backurl':'',
            'membername' : self.membername,
            'membercardid':'身份证号码',
            'mobile':self.mobile,
            'password':self.password,
            'checkcode':validCode,
            'x':23,
            'y':13
        }
        res     =   self.session.post(self.login_url,post_para)
        check   =   AnalysisHtml.obtain_login(res.text);
        if(check == False):
            if not os.path.exists(self.cookies_name):
                f   =   open(self.cookies_name, 'w')
                f.close()
            new_cookie_jar                  =   http.cookiejar.LWPCookieJar(self.mobile + '.txt');
            requests.utils.cookiejar_from_dict({c.name:c.value for c in self.session.cookies}, new_cookie_jar);
            new_cookie_jar.save('cookies/' + self.mobile + '.txt', ignore_discard=True, ignore_expires=True)
            return True
        else:
            # print(check);
            return check
            # self.login()
        
        

    #获取登陆验证码
    def getVaildImage(self):
        r = self.session.get(self.validImage_url,headers = self.validHeaders)
        imageData = r.content
        with open('vaild.jpg','wb') as f:
            f.write(imageData)


    def visitHomePage(self):
        r = self.session.get(self.home_url,headers = self.homeHeaders)

    def search_doctor(self,doctor_name):
        post_para = {
            's_sectiongid':'',
            's_sectionid':'',
            's_postid':'',
            's_week':'',
            's_clinictypeid':'',
            's_musthaveno':'0',
            's_recommend':'0',
            'key_doc':doctor_name,
            'key_hos':'输入医院名称',
            'time': self.search_time()
        }
        r = self.session.post(self.search_url, post_para ,headers = self.searchHeaders)
        return r.text

    def search_time(self):
        t   =   time.time();
        t   =   int(t * 1000);
        return t;

    def get_person_info(self):
        r   =   self.session.get(self.person_url, headers = self.personHeaders,timeout=1)
        return r.text;

    def get_doctor_info(self, doctorUrlList):
        if doctorUrlList:
            for url in doctorUrlList:
                _url    =   self.base_url + url
                print(_url)

# t   =   ['a', 'b', 'c', 'd', 'e', 'f', 'g',  'h']
# for j in range(len(t)):
#     print(j,t[j])


# for k, v in t.items:
#     print(k,v)

# def gh():
#     guahao  =   Guahao('姜时新','13511677510', '2BW7QbCtE') #输入账号和密码
#     doctor  =   '马雄';
#     res     =   AnalysisHtml.obtain_docList(guahao.search_doctor(doctor), doctor);
#     guahao.get_doctor_info(res)
# guahao.get_person_info()
# guahao.visitHomePage()
# guahao.get_reg_info('叶惟靖','2016-04-04') #医生名称,就诊日期.请确保医生在该日期正常出诊




















