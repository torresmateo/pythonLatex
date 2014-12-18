#-*- coding: utf-8 -*-
from django import template
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.servers.basehttp import FileWrapper
from django.conf import settings
import datetime
import LatexGenerator
from CbaFlowManuales import CBAFlowManuales
import os
import json
from django.views.decorators.csrf import csrf_exempt

def src_form(request):
	os.chdir(settings.PROJECT_PATH)
	cbaflow_manuales = CBAFlowManuales()
	return render(request, 'src_form.html',{'hola':settings.PROJECT_PATH})

@csrf_exempt
def submit(request):
	compilarManual = noPrefix = noData = noSrc = False
	compile_dir = settings.PROJECT_PATH
	os.chdir(compile_dir)
	errors = []
	if request.method == 'POST':
		if not request.POST.get('prefijo', ''):
			noPrefix = True
		if not request.POST.get('src', ''):
			noSrc = True
		if not request.POST.get('data',''):
			noData = True
		if noData and noSrc:
			errors.append("no pueden no definirse a la vez los datos y el codigo fuente")
		if not errors:
			if noSrc and not noData:#no hay codigo fuente debe ser una opcion del manual cba
				cbaflow_manuales = CBAFlowManuales()
				if cbaflow_manuales.validarDatos(unicode(request.POST['data'])):
					cbaflow_manuales.generarRolesTex()
					compile_dir += "/cbaflow_manuales"
					compilarManual = True 
				else:
					errors.append("los datos no son validos")
					return render(request, 'errors.html',{'errors': errors})
				source = None
			elif noData and not noSrc:#solamente tenemos el codigo fuente
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
			os.chdir(compile_dir)
			if compilarManual:
				lg = LatexGenerator.LatexGenerator(source, prefix, datetime.datetime.now(), "main")
			else:
				lg = LatexGenerator.LatexGenerator(source, prefix, datetime.datetime.now())
			response = HttpResponseRedirect('/pdf/' + lg.generatePDF())
			os.chdir(savedPath)
			return response
	return render(request, 'errors.html',{'errors': errors})

def pdf_test(request,filename):
	if(os.path.isfile(settings.PROJECT_PATH + filename)):
		pdf = open(settings.PROJECT_PATH + filename,'r')
		response  = HttpResponse(pdf.read(), content_type='application/pdf')
		response['Content-Disposition'] = 'inline; filename=asdf.pdf'
		pdf.close()
	else:
		basename, extension = os.path.splitext(settings.PROJECT_PATH + filename)
		if(os.path.isfile(basename+'.log')):
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
		else:
			response = HttpResponse(
				u"Hubo un error con los parámetros, no ha sido generado el reporte LaTeX",
				content_type='text/html; charset=utf-8'
			)
	return response
		
