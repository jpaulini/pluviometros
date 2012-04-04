# -*- coding: cp1252 -*-
import datetime
from google.appengine.ext import db
from google.appengine.tools import bulkloader
import models

class EstacionLoader(bulkloader.Loader):
  def __init__(self):
    bulkloader.Loader.__init__(self, 'Estacion',
                               [('id_estacion', int),
                                ('Nombre', str),
                                ('Latitud', float),
                                ('Longitud', float),
                                ('ubicacion', str)
                               ])

loaders = [EstacionLoader]