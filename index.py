from tkinter import *
from PIL import Image, ImageTk
import tkinter.messagebox as messagebox
import guahaoNet
import AnalysisHtml
import io
try:
	from urllib2 import urlopen
except ImportError:
	from urllib.request import urlopen

class gh(object):

	def __init__(self):
		self.r 		=	4
		self.c 		=	2
		self.imgArea=	0
		self.seArea =	0
		self._user 	=	''
		self._pass 	=	''
		self._phone =	''
		self._code 	=	''
		self.arg 	=	{}
		self.args 	=	['subscribeA', 'subscribeB', 'subscribeC']
		self.doctorname 	=	''
		self.guahao =	guahaoNet.Guahao(self._user, self._pass, self._code)
		self.isLogin=	self.guahao.getIsLogin()
		self.root 	=	Tk();
		self.createWindow()

	def blankLable(self, row, column):
		blankLable 	=	Label(self.root, text=' ', width=13)
		blankLable.grid(row=row, column=column)

	def addColumn(self):
		self.c 	=	self.c + 1

	def addBlank(self):
		self.addColumn()
		for i in range(self.r):
			self.blankLable(self.c, i)

	def createWindow(self):

		for i in range(self.r):
			for j in range(self.c):
				self.blankLable(j, i)


		title 	=	Label(self.root, text='挂号系统登录')
		title.grid(row=self.c, column=0, columnspan=self.r)

		self.addBlank()

		self.addColumn()

		self.blankLable(self.c, 0)
		usernameLable 	=	Label(self.root, text='账号')
		usernameLable.grid(row=self.c, column=1, sticky=E)

		self._user 		=	Entry(self.root)
		self._user.insert(0, '姜时新')
		self._user.grid(row=self.c, column=2)

		self.addColumn()
		self.blankLable(self.c, 0)
		passwordLable 	=	Label(self.root, text='密码')
		passwordLable.grid(row=self.c, column=1, sticky=E)

		self._pass 		=	Entry(self.root)
		self._pass.insert(0, '2BW7QbCtE')
		self._pass.grid(row=self.c, column=2)


		self.addColumn()
		self.blankLable(self.c, 0)
		codeLable 	=	Label(self.root, text='验证码')
		codeLable.grid(row=self.c, column=1, sticky=E)

		self._code 		=	Entry(self.root, width=10)
		self._code.grid(row=self.c, column=2, sticky=W)


		self.loadVaildImage()#加载验证码

		self.addColumn()
		for i in range(self.r):
			self.blankLable(self.c, i)

		self.addColumn()



		# for i in range(3):
		# 	blankLable(3, i)

		self.blankLable(self.c, 0)
		closeBtn 	=	Button(self.root, text="关闭", command=self.root.quit)
		closeBtn.grid(row=self.c, column=1, sticky=E)

		submitBtn 	=	Button(self.root, text="登录", command=self.submit)
		submitBtn.grid(row=self.c, column=2, sticky=W)

		self.root.title("挂号")
		self.root.geometry("600x800")
		self.root.resizable(width=True, height=True)
		self.root.mainloop()

	def search(self):
		self.root.destroy();
		self.root.quit();
		self.root 	=	Tk();
		self.c 		=	0;

		self.addBlank()

		# self.addColumn()
		searchLable 	=	Label(self.root, text='医生搜索')
		searchLable.grid(row=self.c, column=1, sticky=E)

		self.doctorname 		=	Entry(self.root)
		self.doctorname.insert(0, '马雄')
		self.doctorname.grid(row=self.c, column=2)

		searchBtn 		=	Button(self.root, text='搜索', command=self.searchDoctor)
		searchBtn.grid(row=self.c, column=3)

		closeBtn 	=	Button(self.root, text="关闭", command=self.root.quit)
		closeBtn.grid(row=self.c, column=4, sticky=E)

		self.root.title("医生搜索")
		self.root.geometry("600x800")
		self.root.resizable(width=True, height=True)
		self.root.mainloop()


	def searchDoctor(self):
		doctorname 	=	self.doctorname.get() or '马雄'

		if self.seArea == 0:
			self.addColumn()
			self.seArea 	=	self.c

		title 		=	['图片', '姓名', '预定']
		for t  in range(len(title)):
			lb 	=	Label(self.root, text=title[t])
			lb.grid(row=self.seArea, column=t)


		doctorList 	=	self.guahao.search_doctor(doctorname)

		doctorArr 	=	AnalysisHtml.obtain_docList(doctorList, doctorname)



		for d in range(len(doctorArr)):
			item 			=	doctorArr[d]
			try:
				_arg 			=	self.args[d]	
			except:
				break

			if self.arg.get(_arg, 0) == 0:
				self.addColumn()

			cdata 			=	self.arg.get(_arg, {})
			cdata['url']	=	item['url']
			cdata['area']	=	cdata.get('area', self.c)
			self.arg[_arg]	=	cdata

			self.labelImg(item['img'], self.arg[_arg]['area'], 0, 1)
			self.lableText(item['name'], self.arg[_arg]['area'], 1)
			if _arg == 'subscribeA' :
				self.labelButton(self.arg[_arg]['area'], 2, self.subscribeA)

			if _arg == 'subscribeB' :
				self.labelButton(self.arg[_arg]['area'], 2, self.subscribeB)

			if _arg == 'subscribeC' :
				self.labelButton(self.arg[_arg]['area'], 2, self.subscribeC)


	def subscribeA(self):
		# messagebox.showinfo('提示', self.arg['subscribeA']['url'])
		self.subscribe(self.arg['subscribeA']['url'])
		

	def subscribeB(self):
		self.subscribe(self.arg['subscribeB']['url'])
		

	def subscribeC(self):
		self.subscribe(self.arg['subscribeC']['url'])
	

	def subscribe(self, url):
		url 	=	self.guahao.base_url + url
		messagebox.showinfo('搜索医生', url)


	def labelButton(self, row, column, command):
		btn 	=	Button(self.root, text="预约", command=command)
		btn.grid(row=row, column=column, sticky=E)

		# messagebox.showinfo('搜索医生', AnalysisHtml.obtain_docList(doctorList, doctorname))

	def lableText(self, text, row, column):
		textLabel 	=	Label(self.root, text=text)
		textLabel.grid(row=row, column=column, sticky=E)

	def labelImg(self, file, row, column, intnet = 0):

		if intnet:
			image_bytes 	=	urlopen(file).read()
			data_stream 	=	io.BytesIO(image_bytes)
		else:
			data_stream 	=	file

		image = Image.open(data_stream)
		image =	image.resize((90, 120), Image.NEAREST)
		photo = ImageTk.PhotoImage(image)
		label = Label(self.root, image=photo, width=90, height=120) #使用标签控件来引入图片
		label.image = photo

		label.grid(row=row, column=column)


	def loadVaildImage(self):
		# 说明：仅支持GIF、PGM、PPM格式
		# photo = PhotoImage(file="image.gif")

		if not self.isLogin:
			# self.getVaildImage()
			pass

		if self.imgArea == 0:
			self.addColumn()
			self.imgArea 	=	self.c

		image = Image.open("vaild.jpg")
		photo = ImageTk.PhotoImage(image)
		label = Label(self.root, image=photo) #使用标签控件来引入图片
		label.image = photo
		label.grid(row=self.imgArea, columnspan=self.r)




	def submit(self):
			_user 	=	self._user.get() or 'username'
			_pass 	=	self._pass.get() or 'password'
			_code 	=	self._code.get() or 'code'
			_phone 	=	'13511677510'
			# login 	=	self.guahao.login(_user, _phone, _pass, _code) #输入账号和密码
			# messagebox.showinfo('提示', login)
			messagebox.showinfo('提示', 'test')
			# self.loadVaildImage()
			self.search()

	def getVaildImage(self):
		self.guahao.getVaildImage()


gh 	=	gh()












