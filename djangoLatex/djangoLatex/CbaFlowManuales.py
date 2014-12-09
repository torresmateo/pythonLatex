#!/usr/bin/python
#-*- coding: utf-8 -*-
import os
import json
from django.conf import settings

#genera un archivo latex a partir de una simulación
class CBAFlowManuales:
	def __init__(self):
		if not os.path.isdir("./cbaflow_manuales"):
			os.system("hg clone " + settings.CBAFLOW_MANUALES_REPO_URL)
		os.chdir("cbaflow_manuales")
		self.actualizarFuentes()
		self.datos = {}
	
	def actualizarFuentes(self):
		os.system("hg update --clean")
		os.system("hg pull " + settings.CBAFLOW_MANUALES_REPO_URL)

	"""
	Verifica la estructura del json recibido para configurar roles.tex antes de la compilacion de los manuales
	:param datos: Es el string json que viene de la aplicación C#
	"""
	def validarDatos(self, datosJson):
		valores_admitidos = set([True, False])
		datos = json.loads(datosJson)
		s = set(datos.values())
		if s == valores_admitidos:
			self.datos = datos
			return True
		return False

	"""
	Genera el archivo roles.tex basado en los datos validados
	"""
	def generarRolesTex(self):
		roles_tex = open("./roles.tex", "w")
		for variable, valor in self.datos.iteritems():
			roles_tex.write("\\newtoggle{"+ variable +"}")
			if valor:
				roles_tex.write("\\toggletrue{"+ variable +"}\n")
			else:
				roles_tex.write("\\togglefalse{"+ variable +"}\n")
		roles_tex.close()
