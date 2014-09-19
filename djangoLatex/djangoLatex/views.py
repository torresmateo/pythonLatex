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
	noPrefix = onlySrc = False
	os.chdir(settings.PROJECT_PATH)
	errors = []
	if request.method == 'POST':
		if not request.POST.get('prefijo', ''):
			noPrefix = True
		if not request.POST.get('src', ''):
			errors.append('el código fuente no puede estar vacío.')
		if not request.POST.get('data',''):
			onlySrc = True
		if not errors:
			if onlySrc:
				source = unicode(json.loads(request.POST['src']))
			else:
				datos = json.loads(unicode(request.POST['data']))
				t = template.Template(unicode(json.loads(request.POST['src'])))
				c = template.Context(datos)
				source = unicode(t.render(c))
			if noPrefix:
				prefix = 'PREFIJO_DEFAULT_'
			else:
				prefix = unicode(json.loads(request.POST['prefijo']))
			savedPath = os.getcwd()
			os.chdir(settings.PROJECT_PATH)
			lg = LatexGenerator.LatexGenerator(source, prefix, datetime.datetime.now())
			response = HttpResponseRedirect('/pdf/' + lg.generatePDF())
			os.chdir(savedPath)
			return response
	return render(request, 'src_form.html',{'errors': errors})

def pdf_test(request,filename):
	if(os.path.isfile(settings.PROJECT_PATH + filename)):
		pdf = open(settings.PROJECT_PATH + filename,'r')
		response  = HttpResponse(pdf.read(), content_type='application/pdf')
		response['Content-Disposition'] = 'inline; filename=asdf.pdf'
		pdf.close()
	else:
		basename, extension = os.path.splitext(settings.PROJECT_PATH + filename)
		log = open(basename+'.log', 'r')
		src = open(basename+'.tex', 'r')
		responseString = '<br><pre>' + log.read() + '</pre>'
		responseString += u'<h3>código fuente</h3><br><pre>' + src.read().decode('utf8') + '</pre>'
		response = HttpResponse(
			u"<h3>Error de compilación Latex para el archivo <div style='color=red;'>" + basename + "</div></h3> " + responseString,
			content_type='text/html; charset=utf-8'
		)
		log.close()
		src.close()
	return response
		
