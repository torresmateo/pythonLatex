#!/usr/bin/python
#-*- coding: utf-8 -*-
import datetime
import os
from math import floor
import time

#genera un archivo latex a partir de una simulación
class LatexGenerator:
	def __init__(self, 
				 src,
				 prefix, 
				 date = datetime.datetime.now()
	):
		self.prefix = prefix
		self.date = date
		self.basename = prefix + date.strftime("%Y-%m-%d,%H_%M_%S")
		self.filename = self.basename + ".tex"
		self.file = open(self.filename, "w")
		self.closedFile = False
		self.file.write(src.encode('utf8'))

	def closeFile(self):
		self.file.close()
		
	def generatePDF(self):
		if not self.closedFile:
			self.closeFile()
		os.system("pdflatex " + self.filename)
		os.system("pdflatex " + self.filename)
		os.system("pdflatex " + self.filename)
		return self.basename + ".pdf"
