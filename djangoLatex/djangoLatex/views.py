#-*- coding: utf-8 -*-
from django import template
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.servers.basehttp import FileWrapper
from django.conf import settings
import datetime
import LatexGenerator
import os
import json
from django.views.decorators.csrf import csrf_exempt

def src_form(request):
	os.chdir(settings.PROJECT_PATH)
	a = open("hola.txt","w")
	a.write("hola")
	a.close()
	return render(request, 'src_form.html',{'hola':settings.PROJECT_PATH})

@csrf_exempt
def submit(request):
	os.chdir(settings.PROJECT_PATH)
	errors = []
	if request.method == 'POST':
	
		if not request.POST.get('src', ''):
			errors.append('el código fuente no puede estar vacío.')
		if not errors:
			datos = json.loads(unicode(request.POST['data']))
			t = template.Template(unicode(json.loads(request.POST['src'])))
			c = template.Context(datos)
			savedPath = os.getcwd()
			os.chdir(settings.PROJECT_PATH)
			lg = LatexGenerator.LatexGenerator(unicode(t.render(c)),datetime.datetime.now())
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
