#-*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.servers.basehttp import FileWrapper
from django.conf import settings
import datetime
import LatexGenerator
import os

def src_form(request):
	return render(request, 'src_form.html')

def submit(request):
	errors = []
	if request.method == 'POST':
		if not request.POST.get('src', ''):
			errors.append('el código fuente no puede estar vacío.')
		if not errors:
			savedPath = os.getcwd()
			os.chdir(settings.PROJECT_PATH)
			lg = LatexGenerator.LatexGenerator(request.POST['src'])
			response = HttpResponseRedirect('/pdf/' + lg.generatePDF())
			os.chdir(settings.PROJECT_PATH)
			return response
	return render(request, 'src_form.html',{'errors': errors})

def pdf_test(request,filename):
	pdf = open(settings.PROJECT_PATH + filename,'r')
	response  = HttpResponse(pdf.read(), content_type='application/pdf')
	response['Content-Disposition'] = 'inline; filename=asdf.pdf'
	return response
	pdf.closed
