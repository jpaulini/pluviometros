import datetime
from google.appengine.ext import db
from google.appengine.api import users

#JSON de Estación INTA
#{"id_estacion":9,
#"Nombre":"NH0358",
#"Latitud":-34.6055,
#"Longitud":-58.671,
#"ubicacion":"Las Caba\u00f1as y De Los Reseros s\/n"}

class Estacion(db.Model):
    #JSON de Estación INTA
    #{"id_estacion":9,
    id_estacion = db.IntegerProperty(required=True)
    #"Nombre":"NH0358",
    Nombre = db.StringProperty(required=True)    
    #"Latitud":-34.6055,
    Latitud= db.FloatProperty()
    #"Longitud":-58.671,
    Longitud= db.FloatProperty()
    # GeoPt
    LatLng = db.GeoPTProperty()
    #"ubicacion":"Las Caba\u00f1as y De Los Reseros s\/n"}
    ubicacion = db.StringProperty(required=True)
  