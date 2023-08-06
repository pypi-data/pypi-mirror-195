#!/usr/bin/env python
# -*- coding: utf-8 -*-

#This module handle interfacing for various output paltforms


try:
	get_ipython()#fails if not in IPython environment
	import IPython
except:
	IPython = None

from pydoc import importfile
import os
path = os.path.dirname(__file__)
output =  importfile(os.path.join(path,'output.py'))

import os
import numpy as np
import time



WEB_PAGE='paneltime.html'
TMP_PAGE='tmphtml'
pic_num=[1]





def get_channel(window,exe_tab,panel, console_output):
	if console_output:
		return console(panel)
	if not window is None:#tkinter gui
		return tk_widget(window,exe_tab,panel)
	if not IPython is None:
		n=IPython.get_ipython().__class__.__name__
		if n=='ZMQInteractiveShell':
			return web_output(True,panel)
	try:
		return web_output(False,panel)
	except:
		pass
	return console(panel)
		
class web_output:
	def __init__(self,Jupyter,panel):
		global webbrowser
		import webbrowser
		self.panel=panel	
		self.Jupyter=Jupyter
		if not Jupyter:
			self.save_html(get_web_page('None', 'None', 'None', '', True))
			if panel.options.web_open_tab.value:
				webbrowser.open(WEB_PAGE, new = 2)
		self.output_set = False
		#import charts
		#self.charts = charts.ProcessCharts(panel)
			
	def set_progress(self,perc, text, task):
		return True
		
	def set_output_obj(self,ll, comput, dx_norm):
		"sets the outputobject in the output" 
		if self.output_set:
			return		
		self.output=output.output(ll,self.panel, comput, dx_norm)
		self.output_set = True
		
		
	def update(self,comput, its, ll, incr, dx_norm):
		self.output.update(comput,its, ll, incr, dx_norm)
		self.its=its
		self.reg_table=self.output.reg_table()
		tbl,llength=self.reg_table.table(4,'(','HTML',True,
							   show_direction=True,
							   show_constraints=True)		
		web_page=get_web_page(ll.LL, 
							  ll.args.args_v, 
							  dx_norm,
							  tbl,
							  self.Jupyter==False)
		#self.charts.save_all(ll)
		if self.Jupyter:
			IPython.display.clear_output(wait=True)
			display(IPython.display.HTML(web_page))
		else:
			self.save_html(web_page)

		
	def save_html(self,htm_str):
		self.f = open(WEB_PAGE, "w")
		self.f.write(htm_str)
		self.f.close()

		
	def print_final(self, msg, fret, conv, t0, xsol, its, node):
		print(msg)
		print(f"LL={fret}  success={conv}  t={time.time()-t0}  its: {its}   node: {node}")
		print(xsol)	
		
class console:
	def __init__(self,panel):
		self.panel=panel
		self.output_set = False
		
	def set_progress(self,perc,text, task):
		if task=='done':
			print(text)
		#perc = f'{int(perc*100)}%'.ljust(5)
		#print(f"{perc} - {task}: {text}")
		return True
		
	def set_output_obj(self,ll, comput, dx_norm):
		if self.output_set:
			return
		self.output=output.output(ll,self.panel, comput, dx_norm)
		self.output_set = True
		self.comput = comput

	def update(self,comput, its,ll,incr, dx_norm):
		self.ll = ll
		self.incr = incr
		self.dx_norm = dx_norm

		
	def print_final(self, msg, fret, conv, t0, xsol, its, node):
		print(msg)
		if self.output_set:
			self.output.update(self.comput,its, self.ll, 0, self.dx_norm)
			self.its=its
			self.reg_table=self.output.reg_table()	
			tbl,llength=self.reg_table.table(5,'(','CONSOLE',False,
								   show_direction=False,
								   show_constraints=False)	
			print(tbl)
		else:
			print(f"LL={fret}  success={conv}  t={time.time()-t0}  its: {its}   node: {node}")
			print(xsol)		
				
class tk_widget:
	def __init__(self,window,exe_tab,panel):
		self.panel=panel
		self.tab=window.main_tabs._tabs.add_output(exe_tab)
		self.set_progress=self.tab.progress_bar.set_progress
		self.output_set = False
		
	def set_output_obj(self,ll, comput, dx_norm):
		if self.output_set:
			return		
		self.tab.set_output_obj(ll,self.panel, comput, dx_norm)
		self.output = self.tab.output
		self.output_set = True
		
	def update(self,comput, its, ll, incr, dx_norm):
		self.tab.update(self.panel, comput,its, ll, incr, dx_norm)
		
	def print_final(self, msg, fret, conv, t0, xsol, its, node):
		print(msg)
		print(f"LL={fret}  success={conv}  t={time.time()-t0} its: {its}")
		print(xsol)	

def get_web_page(LL, args, comput,tbl,auto_update):
	au_str=''
	if auto_update:
		au_str="""<meta http-equiv="refresh" content="1" >"""
	img_str=''
	pic_num[0]+=1
	if os.path.isfile('img/chart0.png'):
		img_str=(f"""<img src="img/histogram.png"><br>\n"""
				f"""<img src="img/correlogram.png"   ><br>\n"""
				f"""<img src="img/correlogram_variance.png"   >""")
	return f"""
<meta charset="UTF-8">
{au_str}
<head>
<title>paneltime output</title>
</head>
<style>
p {{
  margin-left: 60px;
  max-width: 980px;
  font-family: "Serif";
  text-align: left;
  color:#063f5c;
  font-size: 16;
}}
h1 {{
  margin-left: 20px;
  max-width: 980px;
  font-family: "Serif";
  text-align: left;
  color:black;
  font-size: 25;
  font-weight: bold;
}}

table.head {{
  font-family: "Serif";
  text-align: right;
  color:black;
  padding-left: 0px;
  font-size: 16;
}}
td.h:nth-child(odd) {{
  background: #CCC
}}
td {{
  padding-left: 0px;
}}
table {{
  font-family: "Serif";
  text-align: right;
  color:black;
  font-size: 16;
}}

th {{
border-collapse: collapse;
	border-bottom: double 3px;
	padding-left: 0px;
	white-space: nowrap;
}}
</style>
<body>
<div style='position:absolute;float:right;top:0;right:0'>
{img_str}
</div>
{tbl}
</body>
</html> """	

