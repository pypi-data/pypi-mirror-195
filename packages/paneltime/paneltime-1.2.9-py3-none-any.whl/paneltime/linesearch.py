from pydoc import importfile
import os
path = os.path.dirname(__file__)
logl =  importfile(os.path.join(path,'loglikelihood.py'))

import numpy as np

STPMX=100.0 
import time
class LineSearch:
	def __init__(self, x, comput, panel, step = 1):
		self.alf = 1.0e-3     #Ensures sufficient decrease in function value.
		self.tolx = 1.0e-14  #Convergence criterion on fx.		
		self.step = step
		self.stpmax = STPMX * max((abs(np.sum(x**2)	))**0.5,len(x))
		self.comput = comput
		self.panel = panel

	def lnsrch(self, x, f, g, dx):
		
		#(x, f, g, dx) 

		self.check=0
		self.g = g
		self.msg = ""
		n=len(x)
		self.rev = False
		if f is None:
			raise RuntimeError('f cannot be None')
	
		summ=np.sum(dx**2)**0.5
		if summ > self.stpmax:
			dx = dx*self.stpmax/summ 
		slope=np.sum(g*dx)					#Scale if attempted step is too big.
		if slope <= 0.0:
			self.msg = "Roundoff problem"
			dx=-dx
			slope=np.sum(g*dx)
			self.rev = True
		test=0.0 															#Compute lambda min.
		for i in range(0,n): 
			temp=abs(dx[i])/max(abs(x[i]),1.0) 
			if (temp > test): test=temp 
		alamin = self.tolx/test 
		#*******CUSTOMIZATION
		#multithread:

		for i in range(1000):#Setting alam so that the largest step is valid. Set func to return None when input is invalid
			self.alam = 0.5**i*self.step #Always try full Newton step first.
			self.x = x + self.alam * dx
			self.f, self.ll = self.func(self.x) 
			if self.f != None: break
		#*************************
		f2=0
		alam2 = self.alam
		alamstart = self.alam#***********CUSTOMIZATION
		max_iter = 1000
		for self.k in range (0,max_iter):			#Start of iteration loop.
			self.x = x + self.alam * dx			
			if self.k > 0: 
				self.f, self.ll = self.func(self.x) 
			if self.f is None:
				print('The function returned None')
				self.f = f
			if (self.alam < alamin):   #Convergence on delta x. For zero finding,the calling program should verify the convergence.
				self.x = x*1 
				self.check = 1
				self.f = f
				self.msg = "Convergence on delta dx"
				return
			elif (self.f >= f+self.alf*self.alam*slope): 
				self.msg = "Sufficient function increase"
				#print(f'LL single:{self.ll.LL}')
				#self.ll = self.ll2
				return							#Sufficient function increase
			else:  															#Backtrack.
				if (self.alam == alamstart):#***********CUSTOMIZATION  alam == 1.0
					tmplam = -slope/(2.0*(self.f-f-slope))  	#First time.
				else:  														#Subsequent backtracks.
					rhs1 = self.f-f-self.alam*slope 
					rhs2 = f2-f-alam2*slope 
					a=(rhs1/(self.alam**2)-rhs2/(alam2*alam2))/(self.alam-alam2) 
					b=(-alam2*rhs1/(self.alam**2)+self.alam*rhs2/(alam2*alam2))/(self.alam-alam2) 
					if (a == 0.0):
						tmplam = -slope/(2.0*b)  
					else:  
						disc=b*b-3.0*a*slope 
						if (disc < 0.0):
							tmplam = 0.5*self.alam  
						elif (b >= 0.0):
							tmplam=-(b+(disc)**0.5)/(3.0*a) 
						else:
							tmplam=slope/(-b+(disc)**0.5)
					if (tmplam > 0.5*self.alam): 
						tmplam = 0.5*self.alam   								#  lambda<=0.5*lambda1
			alam2 = self.alam 
			f2 = self.f
			self.alam = max(tmplam, 0.1*self.alam)								#lambda>=0.1*lambda1
			if alamstart<1.0:#*************CUSTOMIZATION
				self.alam = min((self.alam, alamstart*0.9**self.k))
				
			self.msg = f"No function increase after {max_iter} iterations"

	def func(self,x):	
		ll = logl.LL(x, self.panel, self.comput.constr)
		if ll is None:
			return None, None
		elif ll.LL is None:
			return None, None
		return ll.LL, ll

	