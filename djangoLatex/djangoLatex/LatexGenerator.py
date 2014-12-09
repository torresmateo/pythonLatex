#!/usr/bin/python
#-*- coding: utf-8 -*-
import datetime
import os
from math import floor
import time
from django.conf import settings


#genera un archivo latex a partir de una simulación
class LatexGenerator:
	def __init__(self, 
				 src,
				 prefix, 
				 date = datetime.datetime.now(),
				 name = None
	):
		self.appendPrefixAfterCompile = False
		self.prefix = prefix
		self.date = date
		if name is None:
			self.basename = prefix + date.strftime("%Y-%m-%d,%H_%M_%S")
		else:
			self.appendPrefixAfterCompile = True
			self.basename = name
		self.filename = self.basename + ".tex"
		if src is not None:
			self.file = open(self.filename, "w")
			self.closedFile = False
			self.file.write(src.encode('utf8'))
		else:
			self.closedFile = True

	def closeFile(self):
		self.file.close()

	def generatePDF(self, makeindex=False):
		if not self.closedFile:
			self.closeFile()
		os.system("pdflatex " + self.filename)
		if makeindex:
			os.system("makeindex " + self.basename)
		os.system("pdflatex " + self.filename)
		os.system("pdflatex " + self.filename)
		if(os.path.isfile(self.basename + ".pdf")):
			if self.appendPrefixAfterCompile:
				os.rename(self.basename + ".pdf", settings.PROJECT_PATH + "/" + self.prefix + self.basename + ".pdf")
				self.basename = self.prefix + self.basename
			else:
				os.rename(self.basename + ".pdf", settings.PROJECT_PATH + "/" + self.basename + ".pdf")
		return self.basename + ".pdf"
